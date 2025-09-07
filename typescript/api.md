# Caskada TypeScript API Reference

This document lists the classes, methods, types, and constants available in the `brainyflow.ts` module.

## Constants

- `DEFAULT_ACTION`: `'default'` - The default action identifier used in node transitions.

## Types

- `SharedStore`: `Record<string, any>` - Represents a generic object store for memory.
- `Action`: `string | typeof DEFAULT_ACTION` - Defines the type for action identifiers.
- `NestedActions<T extends Action[]>`: `Record<T[number], NestedActions<T>[]>` - Recursive type for the nested result structure returned by `Flow`.
- `NodeError`: `Error & { retryCount?: number }` - Custom error type potentially including retry count information.

## Classes

### `Memory<G extends SharedStore, L extends SharedStore>`

Manages global (`__global`) and local (`__local`) state using a Proxy for access control.

- `constructor(private __global: G, private __local: L = {} as L)`: Initializes memory with global and optional local stores.
- `clone<T extends SharedStore = SharedStore>(forkingData: T = {} as T): Memory<G, L & T>`: Creates a new Memory instance with a shared global store reference and a deep-cloned local store, merging optional `forkingData`.
- `static create<G extends SharedStore = SharedStore, L extends SharedStore = SharedStore>(global: G, local: L = {} as L): Memory<G, L>`: Factory method to create a proxied Memory instance.
- _Property Access_: Uses a Proxy. Getting checks local then global. Setting writes to global (removing from local if present). `local` property provides direct access to `__local`.

### `BaseNode<GlobalStore, LocalStore, AllowedActions, PrepResult, ExecResult>`

Abstract base class for all computational nodes.

- `readonly __nodeOrder`: `number` - Unique, auto-incrementing ID for the node instance.
- `clone<T extends this>(this: T, seen?: Map<BaseNode, BaseNode>): T`: Creates a deep copy of the node and its successors, handling cycles.
- `on<T extends BaseNode>(action: Action, node: T): T`: Adds a successor node for a specific action. Returns the added node.
- `next<T extends BaseNode>(node: T, action?: Action): T`: Convenience method for `on` with the default action. Returns the added node.
- `getNextNodes(action?: Action): BaseNode[]`: Retrieves the list of successor nodes for a given action.
- `async prep(memory: Memory<GlobalStore, LocalStore>): Promise<PrepResult | void>`: Asynchronous preparation phase. Override in subclasses.
- `async exec(prepRes: PrepResult | void): Promise<ExecResult | void>`: Asynchronous execution phase (core logic). Override in subclasses.
- `async post(memory: Memory<GlobalStore, LocalStore>, prepRes: PrepResult | void, execRes: ExecResult | void): Promise<void>`: Asynchronous post-processing phase. Override in subclasses.
- `trigger(action: AllowedActions[number], forkingData?: SharedStore): void`: Triggers a subsequent action during the `post` phase, optionally passing data to the local scope of the next branch.
- `private listTriggers(memory: Memory<GlobalStore, LocalStore>): [AllowedActions[number], Memory<GlobalStore, LocalStore>][]`: Returns a list of `[action, memory_clone]` tuples based on `trigger` calls.
- `protected abstract execRunner(memory: Memory<GlobalStore, LocalStore>, prepRes: PrepResult | void): Promise<ExecResult | void>`: Abstract method for core execution logic (implemented by subclasses like `Node`).
- `async run(memory: Memory<GlobalStore, LocalStore> | GlobalStore, propagate?: boolean)`: Runs the node's full lifecycle (`prep` -> `execRunner` -> `post`). Returns `execRunner` result or triggers if `propagate=true`.

### `Node` (aliased from `RetryNode<...>` )

Standard node implementation extending `BaseNode` with retry capabilities.

- `constructor(options?: { maxRetries?: number; wait?: number })`: Initializes the node with retry configuration (`maxRetries`, `wait` in seconds).
- `async execFallback(prepRes: PrepResult, error: NodeError): Promise<ExecResult>`: Called if all retry attempts in `exec` fail. Default throws the error.
- `protected async execRunner(memory: Memory<GlobalStore, LocalStore>, prepRes: PrepResult): Promise<ExecResult | void>`: Runs the `exec` method with retry logic.

### `Flow<GlobalStore, AllowedActions>`

Orchestrates sequential execution of a node graph, extending `BaseNode`.

- `constructor(public start: BaseNode<GlobalStore>, private options?: { maxVisits: number })`: Initializes the flow with a starting node and options (e.g., `maxVisits`).
- `exec(): never`: Throws an error (Flows orchestrate, not execute directly).
- `protected async execRunner(memory: Memory<GlobalStore, SharedStore>): Promise<NestedActions<AllowedActions>>`: Starts the flow execution from the `start` node.
- `async runTasks<T>(tasks: (() => T)[]): Promise<Awaited<T>[]>`: Executes a list of async task functions sequentially.
- `private async runNodes(nodes: BaseNode[], memory: Memory<GlobalStore, SharedStore>): Promise<NestedActions<AllowedActions>[]>`: Runs a list of nodes sequentially using `runTasks`.
- `private async runNode(node: BaseNode, memory: Memory<GlobalStore, SharedStore>): Promise<NestedActions<AllowedActions>>`: Runs a single node within the flow, handling cloning, execution, triggers, recursion, and cycle detection.

### `ParallelFlow<GlobalStore, AllowedActions>`

Orchestrates parallel execution of node graph branches, extending `Flow`.

- `async runTasks<T>(tasks: (() => T)[]): Promise<Awaited<T>[]>`: Overrides `Flow.runTasks` to execute tasks concurrently using `Promise.all`.

## Browser Compatibility

- If run in a browser environment (`typeof window !== 'undefined'`), the core classes (`BaseNode`, `Node`, `Flow`, `ParallelFlow`) are exposed on `globalThis.brainyflow`.
