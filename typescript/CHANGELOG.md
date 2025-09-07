# caskada

## 2.2.0

### Minor Changes

- 1643a98: Package has been renamed from `brainyflow` to `caskada`

## 2.1.0

### Minor Changes

- 83cb809: ## Automatic Triggers Propagation

  Since v2.0, Caskada propagates triggers from **terminal nodes** (i.e. _nodes missing successors_) to subsequent flows. This let you permeate an action from a node directly to outside of the parent flow, skipping the need to explicitly re-trigger the actions at the end of every flow execution.

  This allows for more fluid and permeable flows, and effectively stops the parent flow from being a rigid barrier in the graph execution.
  Think about it as "_handing over unfinished tasks in a flow to the first node in the next flow_".

  It also means that you can **preserve the concurrency of that execution path as you navigate into the next flow**: the execution doesn’t end at the leaf node, it continues into the next flow.

  ### Ignoring Implicit Triggers Propagation

  In v2.1 we are stopping the propagation of **Implicit Triggers** - _the default action that is automatically triggered when no `.trigger()` was explicitly called_ - to give users more control over trigger's propagation and avoid unexpected behavior.

  Thus, this is the behaviour you can expect:

  1. If a terminal node **does NOT** explicitly call `.trigger()`, **no action is propagated** from that terminal node.
  2. If a terminal node **calls** `.trigger()`, then the parent flow **propagates** that action to its own sucessors - and any forking data passed is preserved.

## 2.0.0

### Major Changes

- 7dc9291: # Major Refactor and Enhancement for TypeScript

  This release introduces significant improvements to `Memory` management, `Flow` execution, and overall type safety.

  ## Breaking Changes

  - **Flow as Node - Trigger Propagation**: When a sub-flow (acting as a node) has an internal node triggering an action for which the sub-flow has no defined successor, this action now correctly propagates as a trigger from the sub-flow node itself in the parent flow's `ExecutionTree`.
  - **Simplified Generic Types**: The generic type hints for `Flow` and `Node` have been simplified, removing the `L` (i.e. `LocalMemory`) type parameter and moving the `ActionT` to the end of the list as it is rarely used. The local memory type can be defined inside the Global by using the property `.local`. Before: `Node[G, L, ActionT, PrepResultT, ExecResultT]`; Now: `Node[G, PrepResultT, ExecResultT, ActionT]`.
  - **New License**: Caskada is now licensed under the Mozilla Public License 2.0.

  Rarely used other than internally, but still breaking changes:

  - **Memory Creation**: `Memory.create(global, local)` static method is removed. To create a memory object, just pass a plain object to `flow.run({ ... })` as you always did or call the `createMemory(global, local)` factory function instead. This aligns with a more functional approach for creating the proxied `Memory` objects.
  - **Memory Type**: `Memory` is now an exported type alias representing the complex proxied structure, not a class to be instantiated directly with `new`.
  - **Flow Execution Result**: `Flow.run()` now returns an `ExecutionTree` object, providing a structured representation of the flow's execution path, triggered actions, and sub-node results. This replaces the previous less-structured result. The `ExecutionTree` structure is:
    ```typescript
    type ExecutionTree = {
      order: number
      type: string
      triggered: Record<Action, ExecutionTree[]> | null
    }
    ```
  - **Node `__nodeOrder`**: The `__nodeOrder` property on `BaseNode` is now consistently a number.

  ## Core Library Changes & New Features

  ### Memory Management (`createMemory`)

  - **Proxy-Based Implementation**: `createMemory` function now constructs `Memory` objects using nested proxies to manage global and local scopes, closely mirroring the advanced Python `Memory` behavior.
  - **Deletion and Existence**: The `Memory` proxy handler now supports `deleteProperty` (for `delete memory.key`) and `has` (for `'key' in memory`), operating on both local and global stores appropriately. `memory.local` proxy also supports these for the local scope.
  - **Type Safety**: `Memory` type uses generics `GlobalStore` and `LocalStore` for better type inference. `_isMemoryObject` flag added for runtime type assertions if needed.

  ### Flow Execution & `ExecutionTree`

  - **`Flow.run()`**: Returns a detailed `ExecutionTree`.
  - **Cycle Detection**: Default `maxVisits` for `Flow` instances increased from 5 to 15. Error messages for cycle detection now include node class name and ID (e.g., `Maximum cycle count (15) reached for TestNode#0`).
  - **Node `__nodeOrder`**: Now consistently a number. The `order` field in `ExecutionTree` is also a number.

  ### Node Lifecycle and Error Handling

  - **`BaseNode.triggers`**: Changed from private to protected to allow manipulation in subclasses if necessary (e.g., for complex trigger logic in `ParallelFlow` tests).
  - **`NodeError`**: Remains an `Error` subtype with an optional `retryCount`.
  - **Warnings**:
    - The warning "Node won't run successors. Use Flow!" when `run()` is called on a `BaseNode` with successors has been **removed** to reduce noise. #20
    - Warning for an "orphan action" (action triggered with no successor) in `get_next_nodes` has been refined for better clarity: `Flow ends for node {ClassName}#{node_order}: Action '{action}' not found in its defined successors [...]`.

  ### Developer Experience & Testing

  - **Test Suite**: Comprehensive updates to `memory.test.ts` and `flow.test.ts` to cover new `Memory` functionalities (including cloning, local proxy operations, deletion, existence checks) and the new `ExecutionTree` structure.
  - **Mock Resetting**: Improved mock handling in tests for better isolation, particularly for `TestNode` instances.
  - **Type Generics**: Enhanced use of generics in `TestNode` and `BranchingNode` for better type safety in tests.

  ## Bug Fixes

  - **V8 Debugger Craskeeping `structuredClone` and Proxies**: Resolved by ensuring `structuredClone` in `memory.clone()` operates on plain object representations of proxied data.
  - **`ExecutionTree` Structure**: Standardized and made more robust.
  - **Type Inconsistencies**: Addressed various type issues for a more stable and predictable API.

  This major update significantly enhances the capabilities and reliability of the TypeScript port, especially around state management and flow execution tracking.

## 1.0.0

### Major Changes

- Refactor: Introduce Memory, trigger mechanism; remove Batch classes and params

  This release introduces a major architectural refactor:

  - Replaced the dictionary-based `shared` store with a `Memory` class managing global and local state via proxy access.
  - Nodes now use `this.trigger("action", forkingData)` in `post` to control flow instead of returning action strings.
  - Removed the `params` mechanism (`setParams`). Context should be passed via `Memory` (global or local via `forkingData`).
  - Removed `BatchNode`, `ParallelBatchNode`, `SequentialBatchFlow`, `ParallelBatchFlow`. Batch processing is now achieved using standard `Node`s within `Flow` or `ParallelFlow` (e.g., fan-out pattern).
  - Updated documentation and tests extensively to reflect these changes.
