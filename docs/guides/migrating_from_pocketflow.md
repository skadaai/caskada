---
machine-display: false
---

# Migrating from PocketFlow to Caskada

Caskada originated as a fork of PocketFlow, aiming to refine its core concepts, enhance type safety (in both language ports), and improve the developer experience for building agentic systems. If you have an existing PocketFlow application, migrating to Caskada involves several key changes.
This guide focuses on migrating from typical PocketFlow patterns to the modern Caskada (v2.0+).

## Key Conceptual Differences & Changes

- **`Async*` Classes Removed**: Caskada's `Node` and `Flow` are inherently async-capable in both Python and TypeScript. All `AsyncNode`, `AsyncFlow`, etc., from PocketFlow are removed. Simply make your `prep`, `exec`, `post` methods `async` and use `await` where appropriate.
- **`Memory` Object**:
  - Caskada's `Memory` object is more central and refined.
  - PocketFlow's `Params` concept is absorbed into the `Memory` object's local store, typically populated via `forkingData`.
- **Triggering Actions**: In `post`, instead of `return "action_name"`, you **must** use `self.trigger("action_name", forking_data={...})` (Python) or `this.trigger("action_name", { ... })` (TypeScript).
- **Batch Processing (`*BatchNode` / `*BatchFlow` Removal)**: PocketFlow's specialized batch classes are **removed**. Caskada handles batching via a "fan-out" pattern: a standard `Node` calls `trigger` multiple times in its `post` method, each call typically including item-specific `forkingData`. This is then orchestrated by a `Flow` (for sequential batching) or `ParallelFlow` (for concurrent batching).
- **`Flow.run()` Result**: Returns a structured `ExecutionTree` detailing the execution path, rather than a simple dictionary of results.

## Why Async?

The move to async brings several benefits:

- **Improved performance**: Asynchronous code can handle I/O-bound operations more efficiently
- **Better concurrency**: Easier to implement parallel processing patterns
- **Simplified codebase**: No need for separate sync and async implementations
- **Modern Python**: Aligns with Python's direction for handling concurrent operations

## Migration Steps

### Step 1: Update Imports and Dependencies

- Replace all `from pocketflow import ...` with `from caskada import ...` (Python) or `import { ... } from 'caskada'` (TypeScript).
```python
# Before
from pocketflow import Node, Flow, BatchNode # ... etc

# After
import asyncio
from caskada import Node, Flow # ... etc
```
- Update your `requirements.txt` or `package.json` to use `caskada`.

### Step 2: Convert to Async and Update Method Signatures

- Add `async` before `def` for your `prep`, `exec`, `post`, and `exec_fallback` methods in Nodes and Flows.
- Remove any `_async` suffix from the method names.
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

### Step 3: Use `.trigger()` for next actions

In all `Node` subclasses, within the `post` method:

- Replace any `return "action_name"` statements with `self.trigger("action_name")` (Python) or `this.trigger("action_name")` (TypeScript).
- If you were passing data to the next node's local context (PocketFlow's `params`), pass this data as the second argument to `trigger` (the `forkingData` object).
  Example: `self.trigger("process_item", {"item": current_item})`
- If `post` simply completed without returning an action (implying default), you can either explicitly call `self.trigger("default)` or rely on the implicit default trigger if no `trigger` calls are made.

### Step 4: Update Batch Processing Implementation (`*BatchNode` / `*BatchFlow` Removal)

Caskada **removes all specialized `BatchNode` and `BatchFlow` classes**. Batch functionality is achieved using standard `Node`s and `Flow`s combined with the "fan-out/fan-in" trigger pattern.

The batch functionality is now achieved using standard `Node`s and `Flow`s combined with a specific pattern:

1.  **Fan-Out (Map) Phase**:

    All `BatchNode` need to be replaced by a fan-out flow. You can either implement a [MapReduce pattern](../design_pattern/mapreduce.md) for it, or split the node into two, a **Trigger Node** and a **Processor Node**:

    The **Prepare/Trigger Node** (replaces the `prep` part of a `BatchNode`):
      - Use the `prep` method to fetch the list of items to process, as usual.
      - Use the `post` method to iterate through these items. For **each item**, calls `self.trigger(action, forkingData={"item": current_item, "index": i, ...})`. The `forkingData` dictionary passes item-specific data into the **local memory** of the triggered successor. (the `action` name can be any of your choice as long as you connect the nodes in the flow; e.g. `process_one`, `default`)
      - This node might also initialize an aggregate result structure in the global memory (e.g., `memory.batch_results = {}`).

    The **Item Processor Node** (replaces the `exec_one` part of a `BatchNode`):
      - Its `prep` method reads the specific item data (e.g., `memory.item`, `memory.index`) from its **local memory** (which was populated by `forkingData` from the trigger node).
      - The logic previously in the `exec_one` method of the `BatchNode` should now be in this node's `exec` method.
      - Its `post` method typically writes the individual item's result back to the **global memory**, often using an index or unique key (e.g., `memory.batch_results[prep_res.index] = exec_res.item_result`).

    **Aggregation (Optional Fan-In Node)**: If you need to aggregate results after all items are processed (you probably should implement mapreduce), you might have the _Item Processor Node_ also trigger an "aggregation_pending" action, and another (final) node conditionalized on all items being done (e.g., via a counter in global memory or by checking the length of results). Or, the Prepare/Trigger node itself might have a separate trigger for an aggregation step after it has fanned out all items.

2.  **Choose the Right Flow**:

    - Wrap the `TriggerNode` and `ProcessorNode` in a standard `caskada.Flow` if you need items processed **sequentially**.
    - Wrap them in a `ParallelFlow` if you need items processed **concurrently**.

3.  **Rename All Classes**:

    - Replace `AsyncParallelBatchFlow` with `ParallelFlow`.
    - Replace `AsyncParallelBatchNode`, `ParallelBatchNode`, `AsyncBatchNode`, `BatchNode` with the standard `Node`.
    - Replace `AsyncBatchFlow`, `BatchFlow` with `caskada.Flow`.
    - Remember to make `prep`, `exec`, `post` methods `async` as per Step 2.

### Step 6: Python `NodeError` Protocol

If you were catching `NodeError` exceptions, note that in Python it's now a `typing.Protocol`. This means you'd typically catch the underlying error (e.g., `ValueError`) and then check if it conforms to `NodeError` via `isinstance(error, NodeError)` if you need to access `error.retry_count`. For TypeScript, it remains an `Error` subtype.

### Step 6: Run with `asyncio`:

Ensure your main application entry point uses `asyncio.run()` (Python) or `Promise.all()`/`async` functions (TypeScript) to execute your flows.

```python
import asyncio

async def main():
    # ... setup your Caskada nodes/flows ...
    memory = {}
    result = await my_flow.run(memory) # Use await and pass memory object
    print(result)
    print(memory)

if __name__ == "__main__":
    asyncio.run(main())
```

**Summary of Key Migration Points:**

1.  Updating imports to `caskada` and adding `import asyncio`.
2.  Adding `async` to your Node/Flow method definitions (`prep`, `exec`, `post`, `exec_fallback`) and removing any `_async` suffix from the method names.
3.  Replacing any `return action` in `post()` with `self.trigger(action, forking_data={...})` (Python) or `this.trigger(action, { ... })` (TypeScript).
4.  Using `await` when calling `run()` methods and any other asynchronous operations within your methods.
5.  Refactoring `BatchNode`/`BatchFlow` usage to the fan-out pattern using standard `Node`s orchestrated by `Flow` or `ParallelFlow`.
5.  Running your main execution logic within an `async def main()` function called by `asyncio.run()`.

This transition enables you to leverage the performance and concurrency benefits of asynchronous programming in your workflows.
