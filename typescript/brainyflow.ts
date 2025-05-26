export const DEFAULT_ACTION = 'default' as const

export type SharedStore = Record<string, unknown>
type Action = string | typeof DEFAULT_ACTION
type NestedActions<T extends Action[]> = Record<T[number], NestedActions<T>[]>

export type Memory<GlobalStore extends SharedStore = SharedStore, LocalStore extends SharedStore = SharedStore> = GlobalStore &
  LocalStore & {
    local: LocalStore
    clone<T extends SharedStore = SharedStore>(forkingData?: T): Memory<GlobalStore, LocalStore & T>
    _isMemoryObject: true
  }

export type NodeError = Error & {
  retryCount?: number
}

interface Trigger<Action = string, L extends SharedStore = SharedStore> {
  action: Action
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
    has: (target, prop) => Reflect.has(closer, prop) || (further ? Reflect.has(further, prop) : false),
  }
}

export function createMemory<GlobalStore extends SharedStore = SharedStore, LocalStore extends SharedStore = SharedStore>(
  global: GlobalStore,
  local: LocalStore = {} as LocalStore,
): Memory<GlobalStore, LocalStore> {
  const localProxy = new Proxy(local, createProxyHandler(local))
  return new Proxy(
    {
      _isMemoryObject: true,
      local: localProxy,
      clone: <T extends SharedStore = SharedStore>(forkingData: T = {} as T): Memory<GlobalStore, LocalStore & T> =>
        createMemory<GlobalStore, LocalStore & T>(global, {
          ...structuredClone(local),
          ...structuredClone(forkingData),
        }),
    },
    createProxyHandler(localProxy, global),
  ) as Memory<GlobalStore, LocalStore>
}

export abstract class BaseNode<
  GlobalStore extends SharedStore = SharedStore,
  LocalStore extends SharedStore = SharedStore,
  AllowedActions extends Action[] = Action[],
  PrepResult = any,
  ExecResult = any,
> {
  private successors: Map<Action, BaseNode<GlobalStore>[]> = new Map()
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

  on<N extends BaseNode<GlobalStore>>(action: Action, node: N): N {
    if (!this.successors.has(action)) {
      this.successors.set(action, [])
    }
    this.successors.get(action)!.push(node)
    return node
  }

  next<N extends BaseNode<GlobalStore>>(node: N, action: Action = DEFAULT_ACTION): N {
    return this.on(action, node)
  }

  getNextNodes(action: Action = DEFAULT_ACTION): BaseNode<GlobalStore>[] {
    const next = this.successors.get(action) || []
    if (!next.length && this.successors.size > 0 && action !== DEFAULT_ACTION) {
      console.warn(
        `Flow ends for node ${this.constructor.name}#${this.__nodeOrder}: Action '${action}' not found in its defined successors`,
        Array.from(this.successors.keys()),
      )
    }
    return next
  }

  async prep(memory: Memory<GlobalStore, LocalStore>): Promise<PrepResult | void> {}
  async exec(prepRes: PrepResult | void): Promise<ExecResult | void> {}
  async post(memory: Memory<GlobalStore, LocalStore>, prepRes: PrepResult | void, execRes: ExecResult | void): Promise<void> {}

  /**
   * Trigger a child node with optional local memory
   * @param action Action identifier
   * @param forkingData Memory to fork to the triggered node
   */
  trigger(action: AllowedActions[number], forkingData: SharedStore = {}): void {
    if (this.locked) {
      throw new Error(`An action can only be triggered inside post()`)
    }
    this.triggers.push({ action, forkingData })
  }

  private listTriggers(memory: Memory<GlobalStore, LocalStore>): [AllowedActions[number], Memory<GlobalStore>][] {
    if (!this.triggers.length) {
      return [[DEFAULT_ACTION, memory.clone()]]
    }
    return this.triggers.map((t) => [t.action, memory.clone(t.forkingData)])
  }

  protected abstract execRunner(memory: Memory<GlobalStore, LocalStore>, prepRes: PrepResult | void): Promise<ExecResult | void>

  async run(memory: Memory<GlobalStore, LocalStore> | GlobalStore, propagate: true): Promise<ReturnType<typeof this.listTriggers>>
  async run(memory: Memory<GlobalStore, LocalStore> | GlobalStore, propagate?: false): Promise<ReturnType<typeof this.execRunner>>
  async run(
    memory: Memory<GlobalStore, LocalStore> | GlobalStore,
    propagate?: boolean,
  ): Promise<ReturnType<typeof this.execRunner> | ReturnType<typeof this.listTriggers>> {
    const _memory: Memory<GlobalStore, LocalStore> = memory._isMemoryObject
      ? (memory as Memory<GlobalStore, LocalStore>)
      : createMemory<GlobalStore, LocalStore>(memory as GlobalStore)

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
  GlobalStore extends SharedStore = SharedStore,
  LocalStore extends SharedStore = SharedStore,
  AllowedActions extends Action[] = Action[],
  PrepResult = any,
  ExecResult = any,
> extends BaseNode<GlobalStore, LocalStore, AllowedActions, PrepResult, ExecResult> {
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

  protected async execRunner(memory: Memory<GlobalStore, LocalStore>, prepRes: PrepResult | void): Promise<ExecResult | void> {
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
  }
}

export const Node = RetryNode

export class Flow<GlobalStore extends SharedStore = SharedStore, AllowedActions extends Action[] = Action[]> extends BaseNode<
  GlobalStore,
  SharedStore,
  AllowedActions,
  void,
  NestedActions<AllowedActions>
> {
  private visitCounts: Map<number, number> = new Map()

  constructor(
    public readonly start: BaseNode<GlobalStore>,
    private readonly options: { maxVisits?: number } = {},
  ) {
    super()
    this.options.maxVisits = options.maxVisits ?? 15
  }

  async exec(prepRes: void): Promise<never> {
    throw new Error('Flow.exec() must never be called directly.')
  }

  protected async execRunner(memory: Memory<GlobalStore, SharedStore>, prepRes: void): Promise<NestedActions<AllowedActions>> {
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

  private async runNodes(nodes: BaseNode<GlobalStore>[], memory: Memory<GlobalStore>): Promise<NestedActions<AllowedActions>[]> {
    return await this.runTasks(nodes.map((node) => () => this.runNode(node, memory)))
  }

  private async runNode(node: BaseNode<GlobalStore>, memory: Memory<GlobalStore, SharedStore>): Promise<NestedActions<AllowedActions>> {
    const nodeOrder = node.__nodeOrder
    const currentVisitCount = (this.visitCounts.get(nodeOrder) || 0) + 1
    if (currentVisitCount > this.options.maxVisits!) {
      throw new Error(`Maximum cycle count (${this.options.maxVisits}) reached for ${node.constructor.name}#${nodeOrder}`)
    }
    this.visitCounts.set(nodeOrder, currentVisitCount)

    const clone = node.clone()
    const triggers = await clone.run(memory.clone(), true)
    if (!Array.isArray(triggers)) {
      throw new Error('Node.run with propagate:true must return an array of triggers')
    }

    const tasks = triggers.map(([action, nodeMemory]) => async () => {
      const nextNodes = clone.getNextNodes(action)
      return [action, !nextNodes.length ? [] : await this.runNodes(nextNodes, nodeMemory as Memory<GlobalStore, SharedStore>)]
    })

    const tree = await this.runTasks(tasks)
    return Object.fromEntries(tree)
  }
}

export class ParallelFlow<GlobalStore extends SharedStore = SharedStore, AllowedActions extends Action[] = Action[]> extends Flow<
  GlobalStore,
  AllowedActions
> {
  protected async runTasks<TaskResult>(tasks: (() => Promise<TaskResult>)[]): Promise<TaskResult[]> {
    return await Promise.all(tasks.map((task) => task()))
  }
}

// @ts-ignore - Make classes available globally in the browser for UMD bundle
if (typeof window !== 'undefined' && !globalThis.brainyflow) {
  ;(globalThis as any).brainyflow = { createMemory, BaseNode, Node, Flow, ParallelFlow, DEFAULT_ACTION }
}
