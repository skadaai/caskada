---
machine-display: false
---

# Migrating from PocketFlow to BrainyFlow

BrainyFlow is an asynchronous successor to PocketFlow, designed for enhanced performance and concurrency. Migrating is straightforward:

## Key Changes

1. **All core methods are now async**

   - `prep()`, `exec()`, `post()`, `_exec()`, `_run()`, and `run()` methods now use `async/await` syntax
   - All method calls to these functions must now be awaited

2. **Simplified class hierarchy**

   - Removed separate async classes (`AsyncNode`, `AsyncFlow`, etc.)
   - All classes now use async methods by default

3. **Batch processing changes**

   - `BatchNode` → `SequentialBatchNode` (sequential processing) or `ParallelBatchNode` (concurrent processing)
   - `BatchFlow` → `SequentialBatchFlow` (sequential processing) or `ParallelBatchFlow` (concurrent processing)

## Why Async?

The move to async brings several benefits:

- **Improved performance**: Asynchronous code can handle I/O-bound operations more efficiently
- **Better concurrency**: Easier to implement parallel processing patterns
- **Simplified codebase**: No need for separate sync and async implementations
- **Modern Python**: Aligns with Python's direction for handling concurrent operations

## Migration Steps

### Step 1: Update Imports

Replace `pocketflow` imports with `brainyflow` and add `import asyncio`.

```python
# Before
from pocketflow import Node, Flow, BatchNode # ... etc

# After
import asyncio
from brainyflow import Node, Flow, SequentialBatchNode # ... etc
```

### Step 2: Add `async` / `await`:

- Add `async` before `def` for your `prep`, `exec`, `post`, and `exec_fallback` methods in Nodes and Flows.
- Add `await` before any calls to these methods, `run()` methods, `asyncio.sleep()`, or other async library functions.

#### Node Example (Before):

```python
class MyNode(Node):
    def prep(self, shared):
        # Preparation logic
        return some_data

    def exec(self, prep_res):
        # Execution logic
        return result

    def post(self, shared, prep_res, exec_res):
        # Post-processing logic
        return action

    def exec_fallback(self, prep_res, exc):
        # Handle exception
        return fallback_result
```

#### Node Example (After):

```python
class MyNode(Node):
    async def prep(self, shared):
        # Preparation logic
        # If you call other async functions here, use await
        return some_data

    async def exec(self, prep_res):
    async def post(self, shared, prep_res, exec_res):
        # Post-processing logic
        # If you call other async functions here, use await
        return action

    async def exec_fallback(self, prep_res, exc):
        # Handle exception
        # If you call other async functions here, use await
        return fallback_result
```

_(Flow methods follow the same pattern)_

### Step 3: Rename Classes

As we got rid of separated async classes, `AsyncNode` and `AsyncFlow` are now just `Node` and `Flow`.

BrainyFlow makes the choice between sequential vs. parallel batch processing explicit:

- If you used `BatchNode` (or `AsyncBatchNode`) -> Use `SequentialBatchNode`.
- If you used `BatchFlow` (or `AsyncBatchFlow`) -> Use `SequentialBatchFlow`.
- If you used `AsyncParallelBatchNode` -> Use `ParallelBatchNode`.
- If you used `AsyncParallelBatchFlow` -> Use `ParallelBatchFlow`.

Remember to make their methods (`exec`, `prep`, `post`) `async` as per Step 2.

```python
# Before (Sequential)
class MySeqBatch(BatchNode):
    def exec(self, item): ...

# After (Sequential)
class MySeqBatch(SequentialBatchNode):
    async def exec(self, item): ... # Added async

# Before (Parallel)
class MyParBatch(AsyncParallelBatchNode):
    async def exec_async(self, item): ...

# After (Parallel)
class MyParBatch(ParallelBatchNode):
    async def exec(self, item): ... # Renamed and added async
```

### Step 4: Run with `asyncio`:

BrainyFlow code must be run within an async event loop. The standard way is using `asyncio.run()`:

```python
import asyncio

async def main():
    # ... setup your BrainyFlow nodes/flows ...
    result = await my_flow.run(shared_data) # Use await
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

## Conclusion

Migrating from PocketFlow to BrainyFlow primarily involves:

1.  Updating imports to `brainyflow` and adding `import asyncio`.
2.  Adding `async` to your Node/Flow method definitions (`prep`, `exec`, `post`, `exec_fallback`).
3.  Using `await` when calling `run()` methods and any other asynchronous operations within your methods.
4.  Replacing `BatchNode`/`BatchFlow` with the appropriate `Sequential*` or `Parallel*` BrainyFlow classes.
5.  Running your main execution logic within an `async def main()` function called by `asyncio.run()`.

This transition enables you to leverage the performance and concurrency benefits of asynchronous programming in your workflows.
