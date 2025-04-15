export type SharedStore = Record<string, any>
type Params = Record<string, any>

type Action = string | typeof DEFAULT_ACTION
type NestedActions<T extends Action[]> = Record<T[number], NestedActions<T>[] | undefined>
const DEFAULT_ACTION = 'default' as const

export type NodeError = Error & {
  retryCount: number
}

export abstract class BaseNode<
  PrepResult = any,
  ExecResult = any,
  AllowedActions extends Action[] = Action[],
> {
  private successors: Map<Action, BaseNode<any, any, Action[]>[]> = new Map()
  protected params: Params = {}

  clone<T extends this>(this: T, seen = new Map()): T {
    if (seen.has(this)) return seen.get(this) as T

    const cloned = Object.create(Object.getPrototypeOf(this))
    seen.set(this, cloned)

    for (const key of Object.keys(this)) {
      ;(cloned as any)[key] = (this as any)[key]
    }

    cloned.successors = new Map()
    for (const [key, nodesArray] of this.successors.entries()) {
      const clonedNodesArray = nodesArray.map((node) =>
        typeof node.clone === 'function' ? node.clone(seen) : node,
      )
      cloned.successors.set(key, clonedNodesArray)
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

  on<T extends BaseNode<any, any, any>>(action: Action, node: T): T {
    if (!this.successors.has(action)) {
      this.successors.set(action, [])
    }
    this.successors.get(action)!.push(node)
    return node
  }

  next<T extends BaseNode<any, any, any>>(node: T, action: Action = DEFAULT_ACTION): T {
    return this.on(action, node)
  }

  getNextNodes(action: Action = DEFAULT_ACTION): BaseNode<any, any, any>[] {
    const next = this.successors.get(action) || []
    if (!next.length && this.successors.size > 0 && action !== DEFAULT_ACTION) {
      console.warn(`Flow ends: '${action}' not found in ${Object.keys(this.successors)}`)
    }
    return next
  }

  async prep(shared: SharedStore): Promise<PrepResult | void> {}
  async exec(prepRes: PrepResult | void): Promise<ExecResult | void> {}
  async post(
    shared: SharedStore,
    prepRes: PrepResult | void,
    execRes: ExecResult | void,
  ): Promise<AllowedActions | void> {}

  protected abstract execRunner(
    shared: SharedStore,
    prepRes: PrepResult | void,
  ): Promise<ExecResult | void>

  async run(shared: SharedStore): Promise<AllowedActions> {
    if (this.successors.size > 0) {
      console.warn("Node won't run successors. Use Flow!")
    }

    const prepRes = await this.prep(shared)
    const execRes = await this.execRunner(shared, prepRes)
    const actions = (await this.post(shared, prepRes, execRes)) || [DEFAULT_ACTION]

    return actions as AllowedActions
  }
}

class RetryNode<
  PrepResult = any,
  ExecResult = any,
  AllowedActions extends Action[] = Action[],
> extends BaseNode<PrepResult, ExecResult, AllowedActions> {
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

export class Flow<PrepResult = any, AllowedActions extends Action[] = Action[]> extends BaseNode<
  PrepResult,
  NestedActions<AllowedActions>,
  AllowedActions
> {
  constructor(public start: BaseNode<any, any, Action[]>) {
    super()
  }

  exec(prepRes: PrepResult): never {
    throw new Error('This method should never be called in Flow')
  }

  // @ts-ignore
  async post(
    shared: SharedStore,
    prepRes: void | PrepResult,
    execRes: NestedActions<AllowedActions>,
  ): Promise<NestedActions<AllowedActions>> {
    return execRes
  }

  protected async execRunner(
    shared: SharedStore,
    prepRes: void | PrepResult,
  ): Promise<NestedActions<AllowedActions>> {
    return await this.executeNode(this.start, shared)
  }

  async runTasks<T>(tasks: (() => T)[]): Promise<Awaited<T>[]> {
    const res: Awaited<T>[] = []
    for (const task of tasks) {
      res.push(await task())
    }
    return res
  }

  private async executeNodes(
    nodes: BaseNode[],
    shared: SharedStore,
  ): Promise<NestedActions<AllowedActions>[]> {
    return await this.runTasks(nodes.map((node) => () => this.executeNode(node, shared)))
  }

  private async executeNode(
    node: BaseNode,
    shared: SharedStore,
  ): Promise<NestedActions<AllowedActions>> {
    const actions = await node.clone().addParams(this.params).run(shared)
    if (!Array.isArray(actions)) {
      throw new Error('Node.run must return an array')
    }

    const tasks = actions.map((action) => async () => {
      const nextNodes = node.getNextNodes(action)
      return !nextNodes.length ? [action] : [action, await this.executeNodes(nextNodes, shared)]
    })

    return Object.fromEntries(await this.runTasks(tasks))
  }
}

export class ParallelFlow<
  PrepResult = any,
  AllowedActions extends Action[] = Action[],
> extends Flow<PrepResult, AllowedActions> {
  async runTasks<T>(tasks: (() => T)[]): Promise<Awaited<T>[]> {
    return await Promise.all(tasks.map((task) => task()))
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
    ParallelFlow,
  }
}
