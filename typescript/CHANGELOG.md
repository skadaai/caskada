# brainyflow

## 1.0.0

### Major Changes

- Refactor: Introduce Memory, trigger mechanism; remove Batch classes and params

  This release introduces a major architectural refactor:

  - Replaced the dictionary-based `shared` store with a `Memory` class managing global and local state via proxy access.
  - Nodes now use `this.trigger("action", forkingData)` in `post` to control flow instead of returning action strings.
  - Removed the `params` mechanism (`setParams`). Context should be passed via `Memory` (global or local via `forkingData`).
  - Removed `BatchNode`, `ParallelBatchNode`, `SequentialBatchFlow`, `ParallelBatchFlow`. Batch processing is now achieved using standard `Node`s within `Flow` or `ParallelFlow` (e.g., fan-out pattern).
  - Updated documentation and tests extensively to reflect these changes.
