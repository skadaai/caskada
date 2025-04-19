---
machine-display: false
---

# Migrating from PocketFlow to BrainyFlow (Python)

{% hint style="info" %}
This guide specifically addresses migrating from the older synchronous Python library `PocketFlow` to the asynchronous Python version of `BrainyFlow`. While the core concepts of apply broadly, the specific approaches mentioned here may slightly differ from the TypeScript implementation.
{% endhint %}

BrainyFlow is an asynchronous successor to PocketFlow, designed for enhanced performance and concurrency. Migrating your Python codebase is straightforward:

## Key Changes

1. **All core methods are now async**

   - `prep()`, `exec()`, `post()`, `_exec()`, `_run()`, and `run()` methods now use `async/await` syntax
   - All method calls to these functions must now be awaited

2. **Simplified class hierarchy**

   - Removed separate async classes (`AsyncNode`, `AsyncFlow`, etc.)
   - All classes now use async methods by default

3. **Batch Processing Patterns**:
   - The way batch processing is handled has evolved. Instead of specific `BatchNode`/`BatchFlow` classes, BrainyFlow encourages using standard `Node`s with fan-out patterns (i.e. `trigger`/`forkingData` within a `Flow`).
   - Use `Flow` for sequential batch steps or `ParallelFlow` for concurrent batch steps. See the [MapReduce design pattern](../design_pattern/mapreduce.md) for examples.

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
    # Prefer using 'memory' parameter name for consistency
    async def prep(self, memory):
        # Preparation logic
        # If you call other async functions here, use await
        return some_data

    async def exec(self, prep_res):
        # Execution logic
        # If you call other async functions here, use await
        result = await some_async_task(prep_res)
        return result

    async def post(self, memory, prep_res, exec_res):
        # Post-processing logic
        # If you call other async functions here, use await
        memory.result = exec_res # Write to memory (global store)
        self.trigger(action) # Use trigger instead of returning action string

    async def exec_fallback(self, prep_res, exc):
        # Handle exception
        # If you call other async functions here, use await
        return fallback_result
```

_(Flow methods follow the same pattern)_

### Step 3: Update Batch Processing Implementation

As we got rid of separated async classes and separated batch classes, you should start by renaming many of your classes:

- If you used `AsyncNode`, `BatchNode`, `AsyncBatchNode`, or `AsyncParallelBatchNode` -> Use `Node`.
- If you used `AsyncFlow`, `BatchFlow`, or `AsyncBatchFlow` -> Use `Flow`.
- If you used `AsyncParallelBatchFlow` -> Use `ParallelFlow`.

Remember to make their methods (`exec`, `prep`, `post`) `async` as per Step 2.

To reproduce PocketFlow's batches, use standard BrainyFlow patterns. Any batch pattern can easily be reproduced with simple flow control:

- Iterate through items calling `self.trigger('process_item', forkingData={'item': item})` per item, effectively creating a fan-out pattern.
- Create a "Processor" node connected to the 'process_item' action that reads `memory.item` in its `prep` method.
- Choose between `Flow` (if sequential) or `ParallelFlow` (if items can be processed concurrently) for the flow containing the Trigger and Processor nodes described above.

_(See the [design pattern examples](../design_pattern/index.md) for illustrations of this fan-out/aggregate approach which replaces dedicated Batch classes in the core library)._

### Step 4: Run with `asyncio`:

BrainyFlow code must be run within an async event loop. The standard way is using `asyncio.run()`:

```python
import asyncio

async def main():
    # ... setup your BrainyFlow nodes/flows ...
    memory = {}
    result = await my_flow.run(memory) # Use await and pass memory object
    print(result)
    print(memory)

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
