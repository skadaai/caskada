export type SharedStore = Record<string, any>
type Params = Record<string, any>

type Action = string
const DEFAULT_ACTION = 'default'

export type NodeError = Error & {
  retryCount: number
}

export abstract class BaseNode<
  PrepResult = any,
  ExecResult = any,
  PostResult extends Action = Action,
> {
  private successors: Map<Action, BaseNode> = new Map()
  protected params: Params = {}

  clone<T extends this>(this: T, seen = new Map()): T {
    if (seen.has(this)) return seen.get(this) as T

    const cloned = Object.create(Object.getPrototypeOf(this))
    seen.set(this, cloned)

    for (const key of Object.keys(this)) {
      ;(cloned as any)[key] = (this as any)[key]
    }

    cloned.successors = new Map()
    for (const [key, value] of this.successors.entries()) {
      if (typeof value.clone === 'function') {
        cloned.successors.set(key, value.clone(seen))
      } else {
        cloned.successors.set(key, value)
      }
    }
    return cloned
  }

  setParams(params: Params): this {
    this.params = { ...params }
    return this
  }

  addParams(params: Params): this {
    return this.setParams({ ...this.params, ...params })
  }

  on(action: Action, node: BaseNode): BaseNode {
    if (action in this.successors) {
      console.warn(`Overwriting successor for action '${action}'`)
    }
    this.successors.set(action, node)
    return node
  }

  next(node: BaseNode, action: Action = DEFAULT_ACTION): BaseNode {
    return this.on(action, node)
  }

  getNextNode(action: Action = DEFAULT_ACTION): BaseNode | null {
    const next = this.successors.get(action)
    if (!next && Object.keys(this.successors).length > 0) {
      console.warn(`Flow ends: '${action}' not found in ${Object.keys(this.successors)}`)
    }
    return next || null
  }

  async prep(shared: SharedStore): Promise<PrepResult | void> {}
  async exec(prepRes: PrepResult | void): Promise<ExecResult | void> {}
  async post(
    shared: SharedStore,
    prepRes: PrepResult | void,
    execRes: ExecResult | void,
  ): Promise<PostResult | void> {}

  protected abstract execRunner(
    shared: SharedStore,
    prepRes: PrepResult | void,
  ): Promise<ExecResult | void>

  async run(shared: SharedStore): Promise<Action> {
    if (this.successors.size > 0) {
      console.warn("Node won't run successors. Use Flow!")
    }

    const prepRes = await this.prep(shared)
    const execRes = await this.execRunner(shared, prepRes)
    const action = (await this.post(shared, prepRes, execRes)) || DEFAULT_ACTION

    return action
  }
}

class RetryNode<
  PrepResult = any,
  ExecResult = any,
  PostResult extends Action = Action,
> extends BaseNode<PrepResult, ExecResult, PostResult> {
  private curRetry = 0
  private maxRetries: number = 1
  private wait: number = 0

  constructor(options: { maxRetries?: number; wait?: number } = {}) {
    super()

    this.maxRetries = options.maxRetries ?? 1
    this.wait = options.wait ?? 0
  }

  async execFallback(prepRes: PrepResult, error: NodeError): Promise<ExecResult> {
    throw error
  }

  protected async execRunner(shared: SharedStore, prepRes: PrepResult): Promise<ExecResult | void> {
    for (this.curRetry = 0; this.curRetry < this.maxRetries; this.curRetry++) {
      try {
        return await this.exec(prepRes)
      } catch (error) {
        if (this.curRetry < this.maxRetries - 1) {
          if (this.wait > 0) {
            await new Promise((resolve) => setTimeout(resolve, this.wait * 1000))
          }
          continue
        }

        ;(error as NodeError).retryCount = this.curRetry
        return await this.execFallback(prepRes, error as NodeError)
      }
    }
    throw new Error('Unreachable')
  }
}

export const Node = RetryNode

export class Flow<PrepResult = any, PostResult extends Action = Action> extends BaseNode<
  PrepResult,
  PostResult,
  PostResult
> {
  constructor(public start: BaseNode) {
    super()
  }

  exec(prepRes: PrepResult): never {
    throw new Error('This method should never be called in Flow')
  }

  async post(
    shared: SharedStore,
    prepRes: void | PrepResult,
    execRes: void | PostResult,
  ): Promise<void | PostResult> {
    return execRes as PostResult
  }

  protected async execRunner(shared: SharedStore, prepRes: PrepResult): Promise<PostResult> {
    let currentNode: BaseNode | null = this.start
    let action: Action = DEFAULT_ACTION

    while (currentNode) {
      action = await currentNode.clone().addParams(this.params).run(shared)

      currentNode = currentNode.getNextNode(action)
    }

    return action as PostResult
  }
}

export abstract class BatchNode<
  ItemType = any,
  ExecResult = any,
  PostResult extends Action = Action,
> extends RetryNode<ItemType[], ExecResult[], PostResult> {
  async prep(shared: SharedStore): Promise<ItemType[]> {
    return []
  }

  protected abstract processBatch(items: (() => Promise<ExecResult>)[]): Promise<ExecResult[]>

  protected async execRunner(shared: SharedStore, items: ItemType[]): Promise<ExecResult[]> {
    const queue = items.map((item) => () => super.execRunner(shared, item as any))
    return this.processBatch(queue as (() => Promise<ExecResult>)[])
  }
}

export abstract class BatchFlow<ItemType = any, PostResult extends Action = Action> extends Flow<
  ItemType[],
  PostResult
> {
  async prep(shared: SharedStore): Promise<ItemType[]> {
    return []
  }

  protected abstract processBatch(items: (() => Promise<PostResult>)[]): Promise<PostResult[]>

  protected async execRunner(shared: SharedStore, items: ItemType[]): Promise<PostResult[]> {
    const queue = items.map((item) => () => super.execRunner(shared, item as any))
    return this.processBatch(queue as (() => Promise<PostResult>)[])
  }
}

export class SequentialBatchNode<
  ItemType = any,
  ExecResult extends Action = Action,
  PostResult extends Action = Action,
> extends BatchNode<ItemType[], ExecResult, PostResult> {
  protected async processBatch(items: (() => Promise<ExecResult>)[]): Promise<ExecResult[]> {
    const results: ExecResult[] = []
    for (const runner of items) {
      results.push(await runner())
    }
    return results
  }
}

export class ParallelBatchNode<
  ItemType = any,
  ExecResult extends Action = Action,
  PostResult extends Action = Action,
> extends BatchNode<ItemType[], ExecResult, PostResult> {
  protected async processBatch(items: (() => Promise<ExecResult>)[]): Promise<ExecResult[]> {
    return Promise.all(items.map((item) => item()))
  }
}

export class SequentialBatchFlow<
  PrepResult extends any[] = any[],
  PostResult extends Action = Action,
> extends BatchFlow<PrepResult[], PostResult> {
  async processBatch(items: (() => Promise<PostResult>)[]): Promise<PostResult[]> {
    let results: PostResult[] = []
    for (const runner of items) {
      results.push(await runner())
    }
    return results
  }
}

export class ParallelBatchFlow<
  PrepResult extends any[] = any[],
  PostResult extends Action = Action,
> extends BatchFlow<PrepResult[], PostResult> {
  async processBatch(items: (() => Promise<PostResult>)[]): Promise<PostResult[]> {
    return Promise.all(items.map((item) => item()))
  }
}

// Make classes available globally in the browser
// @ts-ignore
if (typeof window !== 'undefined' && !globalThis.brainyflow) {
  // @ts-ignore
  globalThis.brainyflow = {
    BaseNode,
    Node,
    Flow,
    SequentialBatchNode,
    ParallelBatchNode,
    SequentialBatchFlow,
    ParallelBatchFlow,
  }
}
