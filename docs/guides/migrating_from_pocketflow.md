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

### Step 3: Update Batch Processing Implementation (`*BatchNode` / `*BatchFlow` Removal)

PocketFlow had dedicated classes like `BatchNode`, `ParallelBatchNode`, `BatchFlow`, and `ParallelBatchFlow`. BrainyFlow v0.3+ **removes these specialized classes**.

The functionality is now achieved using standard `Node`s and `Flow`s combined with a specific pattern:

1.  **Rename Classes**:

    - Replace `BatchNode`, `AsyncBatchNode`, `ParallelBatchNode`, `AsyncParallelBatchNode` with the standard `brainyflow.Node`.
    - Replace `BatchFlow`, `AsyncBatchFlow` with `brainyflow.Flow`.
    - Replace `AsyncParallelBatchFlow` with `brainyflow.ParallelFlow`.
    - Remember to make `prep`, `exec`, `post` methods `async` as per Step 2.

2.  **Adopt the Fan-Out Trigger Pattern**:

    - The node that previously acted as the `BatchNode` (or the starting node of a `BatchFlow`) needs to be refactored into a **Trigger Node**.
      - Its `prep` method usually fetches the list of items to process.
      - Its `post` method iterates through these items. For **each item**, it calls `self.trigger("process_one", forkingData={"item": current_item, "index": i, ...})`. The `forkingData` dictionary passes item-specific data into the **local memory** of the triggered successor.
    - The logic previously in the `exec_one` method of the `BatchNode` must be moved into the `exec` method of a new **Processor Node**.
      - This `ProcessorNode` is connected to the `TriggerNode` via the `"process_one"` action (e.g., `trigger_node.on("process_one", processor_node)`).
      - The `ProcessorNode`'s `prep` method reads the specific item data (e.g., `memory.item`, `memory.index`) from its **local memory**, which was populated by the `forkingData`.
      - Its `post` method typically writes the result back to the **global memory**, often using the index to place it correctly in a shared list or dictionary.

3.  **Choose the Right Flow**:
    - Wrap the `TriggerNode` and `ProcessorNode` in a standard `brainyflow.Flow` if you need items processed **sequentially**.
    - Wrap them in a `brainyflow.ParallelFlow` if items can be processed **concurrently**.

#### Example Migration: Document Summarization

Let's migrate a conceptual PocketFlow `SummarizeDocsBatchNode`.

```python
# Before (PocketFlow - Conceptual)
# from pocketflow import BatchNode
# import some_llm_library
#
# class SummarizeDocsBatchNode(BatchNode):
#     def prep(self, shared):
#         # Returns list of (doc_id, doc_content) tuples
#         return shared.get("documents", []) # Assume documents = [(id1, content1), (id2, content2)]
#
#     def exec_one(self, item):
#         doc_id, doc_content = item
#         print(f"Summarizing doc {doc_id}...")
#         summary = some_llm_library.summarize(doc_content)
#         return (doc_id, summary) # Return tuple (id, result)
#
#     def post(self, shared, prep_res, exec_results):
#         # exec_results is a list of tuples: [(id1, summary1), (id2, summary2)]
#         shared["summaries"] = dict(exec_results) # Store as a dictionary
#         print("All documents summarized.")
#         return "default" # Or trigger next action
```

```python
# After (BrainyFlow v0.3+ - Using Flow Patterns)
from brainyflow import Node, Flow, ParallelFlow, Memory # Import necessary classes

# Assume an async function `summarize_content_api` exists
# async def summarize_content_api(content: str) -> str:
#     # ... call external LLM API ...
#     return "Summary result"

# 1. Trigger Node (Replaces BatchNode's prep and loop logic)
class TriggerSummarizationNode(Node):
    async def prep(self, memory: Memory):
        # Get list of (doc_id, doc_content) tuples
        return memory.get("documents", [])

    async def post(self, memory: Memory, prep_res: list[tuple[str, str]], exec_res):
        documents = prep_res
        num_docs = len(documents)
        # Initialize results structure in global memory
        memory.summaries = {} # Use dict for potentially out-of-order results
        memory.summaries_list = [None] * num_docs # Or list if order is critical and handled

        if not documents:
            self.trigger("summarization_complete") # Skip if no docs
            return

        # Trigger 'summarize_one' for each document
        for index, (doc_id, doc_content) in enumerate(documents):
            self.trigger("summarize_one", {
                "doc_id": doc_id,
                "content": doc_content,
                "result_index": index # Pass index if using list
            })

        # Optional: Trigger aggregation only after all items are processed.
        # This can be complex with ParallelFlow. Often, aggregation is a separate
        # node triggered after the ParallelFlow completes, or managed via counters.
        # For simplicity here, we might assume a later step reads memory.summaries.
        # self.trigger("summarization_complete") # Or trigger an aggregation node

# 2. Processor Node (Replaces BatchNode's exec_one logic)
class SummarizeOneDocNode(Node):
    async def prep(self, memory: Memory):
        # Read item-specific data from local memory
        return {
            "doc_id": memory.doc_id,
            "content": memory.content,
            "index": memory.result_index
        }

    async def exec(self, prep_res):
        doc_id = prep_res["doc_id"]
        content = prep_res["content"]
        # --- Call external summarization API ---
        # summary = await summarize_content_api(content)
        summary = f"Summary of '{content[:20]}...'" # Placeholder
        # ---------------------------------------
        return {"doc_id": doc_id, "summary": summary, "index": prep_res["index"]}

    async def post(self, memory: Memory, prep_res, exec_res):
        doc_id = exec_res["doc_id"]
        summary = exec_res["summary"]
        index = exec_res["index"]
        # Store result in global memory
        memory.summaries[doc_id] = summary
        # If using a list for ordered results:
        # memory.summaries_list[index] = summary
        # (Add counter logic here if triggering aggregation from processor)


# 3. Flow Setup
trigger_node = TriggerSummarizationNode()
processor_node = SummarizeOneDocNode()
# completion_node = Node() # Optional node after completion

trigger_node.on("summarize_one", processor_node)
# trigger_node.on("summarization_complete", completion_node) # If using explicit completion trigger

# Use ParallelFlow for concurrent summarization
summarization_flow = ParallelFlow(trigger_node)
# Or use Flow for sequential summarization
# summarization_flow = Flow(trigger_node)


# --- Example Execution (Conceptual) ---
# import asyncio
# async def main():
#     initial_memory = { "documents": [("doc1", "Content1"), ("doc2", "Content2")] }
#     await summarization_flow.run(initial_memory)
#     # Results are in initial_memory["summaries"]
# asyncio.run(main())

```

_(See the [MapReduce design pattern](../design_pattern/mapreduce.md) for more detailed examples of fan-out/aggregate patterns)._

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
