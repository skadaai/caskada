---
'brainyflow': major
---

# Major Refactor and Enhancement Release (Python)

This release introduces a significant overhaul of the `Memory` class, refines `Flow` execution and cycle detection, and improves overall type safety and developer experience.

## Breaking Changes

- **Flow as Node - Trigger Propagation**: When a sub-flow (acting as a node) has an internal node triggering an action for which the sub-flow has no defined successor, this action now correctly propagates as a trigger from the sub-flow node itself in the parent flow's `ExecutionTree`.
- **NodeError**: Changed from an `Exception` subclass to a `Protocol` (`runtime_checkable`). This affects how `NodeError` might be caught or checked, promoting structural typing and fixing the double-raising of the exception.

Rarely used other than internally, but still breaking changes:

- **Memory Creation**: The static method `Memory.create(global_store, local_store=None)` has been removed. To create `Memory` instances, just pass a dict to `flow.run({ ... })` as you always did, or use the standard constructor: `Memory(global_store, local_store=None)`.
- **Flow Execution Result (`Flow.run()`)**: The `run()` method of a `Flow` now returns an `ExecutionTree` (a `TypedDict` with `order: int`, `type: str`, `triggered: Optional[Dict[Action, List[ExecutionTree]]]`). This provides a structured log of the execution, replacing the previous, less defined dictionary structure. Code that previously traversed the `run()` result will need to be updated to work with the new `ExecutionTree` format.
- **Internal Node Order (`_node_order`)**: This is now consistently an integer.

## Core Library Changes & New Features

### Memory Management (`Memory` Class)

- **Enhanced Proxy Behavior**:
  - `memory.local` now returns a dedicated `LocalProxy` instance, providing isolated attribute and item access (`getattr`, `getitem`, `setattr`, `setitem`, `delattr`, `delitem`, `contains`) that operates _only_ on the local store.
  - The main `Memory` object's attribute/item access (`memory.foo`, `memory['foo']`) continues to prioritize local then global for reads.
  - Writes (`memory.foo = 'bar'`, `memory['foo'] = 'bar'`) now consistently write to the global store, removing the key from the local store first if it exists there.
- **Comprehensive Deletion Support**:
  - `del memory.attr` and `del memory[key]` now delete the key from _both_ global and local stores if present in either (delegating to `_delete_from_stores`).
  - `del memory.local.attr` and `del memory.local[key]` delete _only_ from the local store.
- **Helper Functions**: Internal `_get_from_stores` and `_delete_from_stores` utility functions have been added to centralize store access logic.
- **Cloning**: `memory.clone(forking_data=None)` remains, ensuring deep copy of the local store and merging of `forking_data`. Global store is shared by reference.

### Flow Execution & Cycle Detection

- **`Flow.run()` and `ExecutionTree`**: As mentioned in Breaking Changes, returns a structured `ExecutionTree`.
- **Default `maxVisits`**: Increased from 5 to 15 in the `Flow` constructor for cycle detection.
- **Cycle Detection Error Message**: Improved format to: `Maximum cycle count ({max_visits}) reached for {ClassName}#{node_order}`.

### Node Lifecycle and Error Handling

- **`NodeError` Protocol**: Now a `typing.Protocol` for more flexible error handling. `error.retry_count` is added to exceptions during the retry mechanism in `Node.exec_runner`.
- **Warnings**:
  - The warning "Node won't run successors. Use Flow!" when `run()` is called on a `BaseNode` with successors has been **removed** to reduce noise. #20
  - Warning for an "orphan action" (action triggered with no successor) in `get_next_nodes` has been refined for better clarity: `Flow ends for node {ClassName}#{node_order}: Action '{action}' not found in its defined successors [...]`.

### Type Annotations & Developer Experience

- **Improved Type Hints**: Extensive improvements to type annotations throughout the library using `TypeVar`, `Generic`, `Protocol`, `TypeAlias`, and `TypedDict` for better static analysis and developer understanding. All MyPy errors and inconsistencies addressed.
- **Test Suite Enhancements**:
  - Tests for new `Memory` deletion features and `LocalProxy` behavior.
  - Updated assertions for the new `ExecutionTree` structure.
  - `BaseNode._next_id` is reset in test fixtures/setups for predictable node ordering in tests.
  - More robust mocking and assertions for flow execution paths.
- **Documentation**:
  - Migration guide (`migrating_from_pocketflow.md`) updated with clearer steps for `async`, trigger usage, memory access, and the new batch processing pattern.
  - Core abstraction documentation (`flow.md`, `design.md`) updated to reflect changes (e.g., `maxVisits`, `Memory` creation).
  - "Contributors Wanted!" section added to `README.md`.

## Infrastructure Improvements

- **CI/CD**: GitHub Actions workflow `changeset-check.yml` updated to use `changesets/action@v1.4.9` and properly prepare the Python directory for changeset tooling.
- **`.envrc`**: Added `dotenv_if_exists`.
- **`.gitignore`**: Added `python/README.md` (if it's auto-generated and shouldn't be committed).

This release significantly modernizes the Python BrainyFlow library, especially its state management capabilities and execution tracking, while enhancing type safety and the overall development experience.
