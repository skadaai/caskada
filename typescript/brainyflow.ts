// This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
// Copyright (c) 2025, Victor Duarte
export const DEFAULT_ACTION = 'default' as const

export type SharedStore = Record<string, unknown>
type Action = string | typeof DEFAULT_ACTION
type NestedActions<T extends Action[]> = Record<T[number], ExecutionTree[]>

export type InferLocal<GS extends SharedStore> = GS extends { local: infer L } ? (L extends SharedStore ? L : {}) : {}
export type Memory<GS extends SharedStore = SharedStore, LS extends SharedStore = InferLocal<GS>> = GS &
  LS & {
    local: LS
    clone<T extends SharedStore = SharedStore>(forkingData?: T): Memory<GS, LS & T>
    _isMemoryObject: true
  }

export type NodeError = Error & {
  retryCount?: number
}

export type ExecutionTree = {
  order: number
  type: string
  triggered: NestedActions<Action[]> | null
}

interface Trigger<A extends Action, L extends SharedStore = SharedStore> {
  action: A
  forkingData: L
}

function _get_from_stores(key: string | symbol, closer: SharedStore, further?: SharedStore): unknown {
  if (key in closer) return Reflect.get(closer, key)
  if (further && key in further) return Reflect.get(further, key)
}

function _delete_from_stores(key: string | symbol, closer: SharedStore, further?: SharedStore): boolean {
  // JS does not usually throw errors when key is not found. Otherwise uncomment: `if (!(key in closer) && (!further || !(key in further))) throw new Error(`Key '${key}' not found in store${further ? "s" : ""}`)`
  let removed = false
  if (key in closer) removed = Reflect.deleteProperty(closer, key)
  if (further && key in further) removed = Reflect.deleteProperty(further, key) || removed
  return removed
}

function createProxyHandler<T extends SharedStore>(closer: T, further?: SharedStore): ProxyHandler<SharedStore> {
  return {
    get: (target, prop) => {
      if (Reflect.has(target, prop)) return Reflect.get(target, prop)
      return _get_from_stores(prop, closer, further)
    },
    set: (target, prop, value) => {
      if (target._isMemoryObject && prop in target) {
        throw new Error(`Reserved property '${String(prop)}' cannot be set to ${target}`)
      }
      _delete_from_stores(prop, closer, further)
      if (further) return Reflect.set(further, prop, value)
      return Reflect.set(closer, prop, value)
    },
    deleteProperty: (target, prop) => _delete_from_stores(prop, closer, further),
    has: (target, prop) => Reflect.has(target, prop) || Reflect.has(closer, prop) || (further ? Reflect.has(further, prop) : false),
    ownKeys: (target) =>
      Array.from(new Set([...Reflect.ownKeys(target), ...Reflect.ownKeys(closer), ...(further ? Reflect.ownKeys(further) : [])])),
    getOwnPropertyDescriptor: (target, prop) => {
      if (Reflect.has(target, prop)) return Reflect.getOwnPropertyDescriptor(target, prop)
      if (Reflect.has(closer, prop)) return Reflect.getOwnPropertyDescriptor(closer, prop)
      if (further && Reflect.has(further, prop)) return Reflect.getOwnPropertyDescriptor(further, prop)
      return undefined
    },
  }
}

export function createMemory<GS extends SharedStore, LS extends SharedStore = InferLocal<GS>>(
  global: GS,
  local: LS = (typeof global.local === 'object' && global.local !== null ? { ...global.local } : {}) as LS,
): Memory<GS, LS> {
  const localProxy = new Proxy(local, createProxyHandler(local))
  return new Proxy(
    {
      _isMemoryObject: true,
      local: localProxy,
      clone: <T extends SharedStore = SharedStore>(forkingData: T = {} as T): Memory<GS, LS & T> =>
        createMemory<GS, LS & T>(global, {
          ...structuredClone({ ...local } /* de-proxy it first */),
          ...structuredClone({ ...forkingData } /* de-proxyfy it first */),
        }),
    },
    createProxyHandler(localProxy, global),
  ) as Memory<GS, LS>
}

export abstract class BaseNode<
  GS extends SharedStore = SharedStore,
  PrepResult = any,
  ExecResult = any,
  AllowedActions extends Action[] = Action[],
> {
  private successors: Map<Action, BaseNode<GS>[]> = new Map()
  protected triggers: Trigger<AllowedActions[number], SharedStore>[] = []
  private locked = true
  private static __nextId = 0
  readonly __nodeOrder = BaseNode.__nextId++

  clone<T extends this>(this: T, seen: Map<BaseNode, BaseNode> = new Map()): T {
    if (seen.has(this)) return seen.get(this) as T

    const cloned = Object.create(Object.getPrototypeOf(this)) as T
    seen.set(this, cloned)

    for (const key of Object.keys(this)) {
      ;(cloned as any)[key] = (this as any)[key]
    }

    cloned.successors = new Map()
    for (const [key, value] of this.successors.entries()) {
      cloned.successors.set(
        key,
        Symbol.iterator in value ? value.map((node) => (node && typeof node.clone === 'function' ? node.clone(seen) : node)) : value,
      )
    }
    return cloned
  }

  on<N extends BaseNode<GS>>(action: Action, node: N): N {
    if (!this.successors.has(action)) {
      this.successors.set(action, [])
    }
    this.successors.get(action)!.push(node)
    return node
  }

  next<N extends BaseNode<GS>>(node: N, action: Action = DEFAULT_ACTION): N {
    return this.on(action, node)
  }

  getNextNodes(action: Action = DEFAULT_ACTION): BaseNode<GS>[] {
    const next = this.successors.get(action) || []
    if (!next.length && this.successors.size > 0 && action !== DEFAULT_ACTION) {
      console.warn(
        `Flow ends for node ${this.constructor.name}#${this.__nodeOrder}: Action '${action}' not found in its defined successors`,
        Array.from(this.successors.keys()),
      )
    }
    return next
  }

  async prep(memory: Memory<GS, InferLocal<GS>>): Promise<PrepResult | void> {}
  async exec(prepRes: PrepResult | void): Promise<ExecResult | void> {}
  async post(memory: Memory<GS, InferLocal<GS>>, prepRes: PrepResult | void, execRes: ExecResult | void): Promise<void> {}

  trigger(action: AllowedActions[number], forkingData: SharedStore = {}): void {
    if (this.locked) {
      throw new Error(`An action can only be triggered inside post()`)
    }
    this.triggers.push({ action, forkingData })
  }

  private listTriggers(memory: Memory<GS, InferLocal<GS>>): [AllowedActions[number], Memory<GS, InferLocal<GS> & SharedStore>][] {
    if (!this.triggers.length) {
      return [[DEFAULT_ACTION, memory.clone() as Memory<GS, InferLocal<GS> & SharedStore>]]
    }
    return this.triggers.map((t) => [t.action, memory.clone(t.forkingData)])
  }

  protected abstract execRunner(memory: Memory<GS, InferLocal<GS>>, prepRes: PrepResult | void): Promise<ExecResult | void>

  async run(memory: Memory<GS, InferLocal<GS>> | GS, propagate: true): Promise<ReturnType<typeof this.listTriggers>>
  async run(memory: Memory<GS, InferLocal<GS>> | GS, propagate?: false): Promise<ReturnType<typeof this.execRunner>>
  async run(
    memory: Memory<GS, InferLocal<GS>> | GS,
    propagate?: boolean,
  ): Promise<ReturnType<typeof this.execRunner> | ReturnType<typeof this.listTriggers>> {
    const _memory: Memory<GS, InferLocal<GS>> = memory._isMemoryObject
      ? (memory as Memory<GS, InferLocal<GS>>)
      : createMemory<GS, InferLocal<GS>>(memory)

    this.triggers = []
    const prepRes = await this.prep(_memory)
    const execRes = await this.execRunner(_memory, prepRes)
    this.locked = false
    await this.post(_memory, prepRes, execRes)
    this.locked = true

    if (propagate) {
      return this.listTriggers(_memory)
    }
    return execRes
  }
}

class RetryNode<
  GS extends SharedStore = SharedStore,
  PrepResult = any,
  ExecResult = any,
  AllowedActions extends Action[] = Action[],
> extends BaseNode<GS, PrepResult, ExecResult, AllowedActions> {
  private curRetry = 0
  private readonly maxRetries: number
  private readonly wait: number

  constructor(options: { maxRetries?: number; wait?: number } = {}) {
    super()
    this.maxRetries = options.maxRetries ?? 1
    this.wait = options.wait ?? 0
  }

  async execFallback(prepRes: PrepResult | void, error: NodeError): Promise<ExecResult | void> {
    throw error
  }

  protected async execRunner(memory: Memory<GS, InferLocal<GS>>, prepRes: PrepResult | void): Promise<ExecResult | void> {
    for (this.curRetry = 0; this.curRetry < this.maxRetries; this.curRetry++) {
      try {
        return await this.exec(prepRes)
      } catch (error: any) {
        if (this.curRetry < this.maxRetries - 1) {
          if (this.wait > 0) {
            await new Promise((resolve) => setTimeout(resolve, this.wait * 1000))
          }
          continue
        }
        error.retryCount = error.retryCount || this.curRetry
        return await this.execFallback(prepRes, error as NodeError)
      }
    }
    throw new Error('Max retries reached in execRunner without returning or throwing via exec/execFallback.')
  }
}

export const Node = RetryNode

export class Flow<GS extends SharedStore = SharedStore, AllowedActions extends Action[] = Action[]> extends BaseNode<
  GS,
  void,
  ExecutionTree,
  AllowedActions
> {
  private visitCounts: Map<number, number> = new Map()

  constructor(
    public readonly start: BaseNode<GS>,
    private readonly options: { maxVisits?: number } = {},
  ) {
    super()
    this.options.maxVisits = options.maxVisits ?? 15
  }

  async exec(prepRes: void): Promise<never> {
    throw new Error('Flow.exec() must never be called directly.')
  }

  protected async execRunner(memory: Memory<GS, InferLocal<GS>>, prepRes: void): Promise<ExecutionTree> {
    this.visitCounts.clear()
    return await this.runNode(this.start, memory)
  }

  protected async runTasks<TaskResult>(tasks: (() => TaskResult | Promise<TaskResult>)[]): Promise<TaskResult[]> {
    const results: TaskResult[] = []
    for (const task of tasks) {
      results.push(await task())
    }
    return results
  }

  private async runNodes<CurrentLS extends SharedStore>(
    nodes: BaseNode<GS>[],
    memory: Memory<GS, CurrentLS>,
  ): Promise<ExecutionTree[]> {
    return await this.runTasks(nodes.map((node) => () => this.runNode(node, memory)))
  }

  private async runNode<CurrentLS extends SharedStore>(node: BaseNode<GS>, memory: Memory<GS, CurrentLS>): Promise<ExecutionTree> {
    const nodeOrder = node.__nodeOrder
    const currentVisitCount = (this.visitCounts.get(nodeOrder) || 0) + 1
    if (currentVisitCount > this.options.maxVisits!) {
      throw new Error(`Maximum cycle count (${this.options.maxVisits}) reached for ${node.constructor.name}#${nodeOrder}`)
    }
    this.visitCounts.set(nodeOrder, currentVisitCount)

    const clonedNode = node.clone()
    const triggers = await clonedNode.run(memory.clone(), true)
    const triggered: NestedActions<Action[]> = {}
    const tasks: (() => Promise<[Action, ExecutionTree[]]>)[] = []

    for (const [action, nodeMemory] of triggers) {
      let nextNodes = clonedNode.getNextNodes(action)
      if (nextNodes.length > 0) {
        tasks.push(async () => [action, await this.runNodes(nextNodes, nodeMemory)])
      } else if ((clonedNode as any).triggers.length) {
        // If the sub-node explicitly triggered an action that has no successors, that action becomes a terminal trigger for this Flow itself (if Flow is nested).
        this.triggers.push({ action, forkingData: nodeMemory.local || {} })
        triggered[action] = [] // Log that this action was triggered but led to no further nodes within this Flow.
      }
    }

    const tree = await this.runTasks(tasks)
    for (const [action, executionTrees] of tree) {
      triggered[action] = executionTrees
    }

    return { order: nodeOrder, type: node.constructor.name, triggered: Object.keys(triggered).length > 0 ? triggered : null }
  }
}

export class ParallelFlow<GS extends SharedStore = SharedStore, AllowedActions extends Action[] = Action[]> extends Flow<
  GS,
  AllowedActions
> {
  protected async runTasks<TaskResult>(tasks: (() => Promise<TaskResult>)[]): Promise<TaskResult[]> {
    return await Promise.all(tasks.map((task) => task()))
  }
}

// @ts-ignore Make classes available globally in the browser for UMD bundle
if (typeof window !== 'undefined' && !(globalThis as any).brainyflow) {
  ;(globalThis as any).brainyflow = { createMemory, BaseNode, Node, Flow, ParallelFlow, DEFAULT_ACTION }
}
