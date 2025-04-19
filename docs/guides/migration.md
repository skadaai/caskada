---
machine-display: false
---

# Migration Guide

This guide helps you migrate from older versions of BrainyFlow to the latest version. It covers breaking changes and provides examples for upgrading your code.

## Migrating to v0.3

Version 0.3 includes several major architectural improvements that require code updates:

### Key Changes

1. **Memory Management**: Changed from dictionary-based `shared` to object-based `memory`
2. **Explicit Triggers**: Flow control now requires explicit `trigger()` calls
3. **Node Lifecycle**: Minor adjustments to method signatures
4. **Flow Configuration**: Added options for configuration
5. **Removal of `params`**: The `setParams` approach has been removed
6. **Batch Processing**: Batch node classes have been removed in favor of flow-based patterns

### Memory Management Changes

{% tabs %}
{% tab title="Python" %}

```python
# Before (v0.2)
class MyNode(Node):
    async def prep(self, shared):
        return shared["input_text"]

    async def post(self, shared, prep_res, exec_res):
        shared["result"] = exec_res
        return "default"  # Action name as return value
```

```python
# After (v0.3)
class MyNode(Node):
    async def prep(self, memory):
        return memory.input_text  # Property access syntax

    async def post(self, memory, prep_res, exec_res):
        memory.result = exec_res  # Property assignment syntax
        self.trigger("default")   # Explicit trigger call
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
// Before (v0.2)
class MyNode extends Node {
  async prep(shared: Record): Promise {
    return shared['input_text']
  }

  async post(shared: Record, prepRes: string, execRes: string): Promise {
    shared['result'] = execRes
    return 'default' // Action name as return value
  }
}
```

```typescript
// After (v0.3)
class MyNode extends Node {
  async prep(memory: Memory): Promise {
    return memory.input_text // Property access syntax
  }

  async post(memory: Memory, prepRes: string, execRes: string): Promise {
    memory.result = execRes // Property assignment syntax
    this.trigger('default') // Explicit trigger call
  }
}
```

{% endtab %}
{% endtabs %}

### Explicit Triggers

{% tabs %}
{% tab title="Python" %}

```python
# Before (v0.2)
async def post(self, shared, prep_res, exec_res):
    if exec_res > 10:
        shared["status"] = "high"
        return "high_value"
    else:
        shared["status"] = "low"
        return "low_value"
```

```python
# After (v0.3)
async def post(self, memory, prep_res, exec_res):
    if exec_res > 10:
        memory.status = "high"
        self.trigger("high_value")
    else:
        memory.status = "low"
        self.trigger("low_value")
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
// Before (v0.2)
async post(shared: Record, prepRes: any, execRes: number): Promise {
  if (execRes > 10) {
    shared["status"] = "high";
    return "high_value";
  } else {
    shared["status"] = "low";
    return "low_value";
  }
}
```

```typescript
// After (v0.3)
async post(memory: Memory, prepRes: any, execRes: number): Promise {
  if (execRes > 10) {
    memory.status = "high";
    this.trigger("high_value");
  } else {
    memory.status = "low";
    this.trigger("low_value");
  }
}
```

{% endtab %}
{% endtabs %}

### Flow Configuration

{% tabs %}
{% tab title="Python" %}

```python
# Before (v0.2)
flow = Flow(start=start_node)

# After (v0.3)
# With default options
flow = Flow(start=start_node)

# With custom options
flow = Flow(start=start_node, options={"max_visits": 10})
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
// Before (v0.2)
const flow = new Flow(startNode)

// After (v0.3)
// With default options
const flow = new Flow(startNode)

// With custom options
const flow = new Flow(startNode, { maxVisits: 10 })
```

{% endtab %}
{% endtabs %}

### Removal of `params` and `setParams`

In v0.3, `setParams` has been removed in favor of direct property access through the streamlined memory management.
Replace `params` with **local memory** and remove `setParams` from the code.

### Batch Processing Changes (`*BatchNode` and `*BatchFlow` Removal)

In v0.3, dedicated batch processing classes like `BatchNode`, `ParallelBatchNode`, `BatchFlow`, and `ParallelBatchFlow` have been **removed** from the core library.

The core concept of batching (processing multiple items, often in parallel) is now achieved using a more fundamental pattern built on standard `Node`s and `Flow`s:

1.  **Fan-Out Trigger Node**: A standard `Node` (let's call it `TriggerNode`) is responsible for initiating the processing for each item in a batch.
    - In its `prep` method, it typically reads the list of items from memory.
    - In its `post` method, it iterates through the items and calls `this.trigger("process_one", forkingData={...})` **for each item**.
    - The `forkingData` argument is crucial: it passes the specific item (and potentially its index or other context) to the **local memory** of the successor node instance created for that trigger. This isolates the data for each parallel branch.
2.  **Processor Node**: Another standard `Node` (let's call it `ProcessorNode`) handles the actual processing of a single item.
    - It's connected to the `TriggerNode` via the `"process_one"` action (e.g., `triggerNode.on("process_one", processorNode)`).
    - Its `prep` method reads the specific item data from its **local memory** (e.g., `memory.item`, `memory.index`), which was populated by the `forkingData` from the `TriggerNode`.
    - Its `exec` method contains the logic previously found in `exec_one`. It performs the computation for the single item.
    - Its `post` method takes the result and typically stores it back into the **global memory**, often in a list or dictionary indexed by the item's original index to handle potential out-of-order completion in parallel scenarios.
3.  **Flow Orchestration**:
    - To process items **sequentially**, use a standard `Flow` containing the `TriggerNode` and `ProcessorNode`. The flow will execute the branch triggered for item 1 completely before starting the branch for item 2, and so on.
    - To process items **concurrently**, use a `ParallelFlow`. This flow will execute all the branches triggered by `TriggerNode` in parallel (using `Promise.all` or `asyncio.gather`).
4.  **Aggregation (Optional)**: If you need to combine the results after all items are processed (like a Reduce step), the `TriggerNode` can fire an additional, final trigger (e.g., `this.trigger("aggregate")`) after the loop. Alternatively, the `ProcessorNode` can maintain a counter in global memory and trigger the aggregation step only when the counter reaches zero (see the [MapReduce pattern](../design_pattern/mapreduce.md)).

This approach simplifies the core library by handling batching as an _orchestration pattern_ rather than requiring specialized node types.

#### Example: Translating Text into Multiple Languages

Let's adapt the `TranslateTextNode` example provided earlier. Before, it might have been a `BatchNode`. Now, we split it into a `TriggerTranslationsNode` and a `TranslateOneLanguageNode`.

{% tabs %}
{% tab title="Python" %}

```python
# Before (v0.2) - Conceptual BatchNode
# class TranslateTextBatchNode(BatchNode):
#     async def prep(self, shared):
#         text = shared.get("text", "(No text provided)")
#         languages = shared.get("languages", ["Chinese", "Spanish", "Japanese"])
#         # BatchNode prep would return items for exec_one
#         return [(text, lang) for lang in languages]
#
#     async def exec_one(self, item):
#         text, lang = item
#         # Assume translate_text exists
#         return await translate_text(text, lang)
#
#     async def post(self, shared, prep_res, exec_results):
#         # BatchNode post might aggregate results
#         shared["translations"] = exec_results
#         return "default"
```

```python
# After (v0.3) - Using Flow Patterns with ParallelFlow

from brainyflow import Node, ParallelFlow, Memory
import asyncio # For example

# Assume get_languages exists or is defined
def get_languages() -> list[str]:
    return ["Chinese", "Spanish", "Japanese", "German", "Russian", "Portuguese", "French", "Korean"]

# 1. Trigger Node (Fans out work)
class TriggerTranslationsNode(Node):
    async def prep(self, memory: Memory):
        text = memory.get("text", "(No text provided)")
        languages = memory.get("languages", get_languages())
        return {"text": text, "languages": languages}

    async def post(self, memory: Memory, prep_res, exec_res):
        text = prep_res["text"]
        languages = prep_res["languages"]
        # Initialize results list in global memory
        memory.translations = [None] * len(languages)

        # Trigger processing for each language
        for index, lang in enumerate(languages):
            self.trigger("translate_one", {
                "text_to_translate": text,
                "language": lang,
                "result_index": index
            })

        # Optional: Trigger an aggregation step if needed after all parallel tasks
        # self.trigger("aggregate_results")

# 2. Processor Node (Handles one language)
class TranslateOneLanguageNode(Node):
    async def prep(self, memory: Memory):
        # Read data passed via forkingData from local memory
        return {
            "text": memory.text_to_translate,
            "lang": memory.language,
            "index": memory.result_index
        }

    async def exec(self, prep_res):
        text = prep_res["text"]
        lang = prep_res["lang"]
        # --- Call external translation API ---
        # translated_text = await call_translation_api(text, lang)
        translated_text = f"'{text}' translated to {lang}" # Placeholder
        # -------------------------------------
        return {"translated": translated_text, "index": prep_res["index"], "lang": lang}

    async def post(self, memory: Memory, prep_res, exec_res):
        index = exec_res["index"]
        lang = exec_res["lang"]
        result = exec_res["translated"]
        # Store result in the global list at the correct index
        memory.translations[index] = {"language": lang, "translation": result}
        # No trigger needed here, this branch ends.


# 3. Flow Setup (Using ParallelFlow for concurrency)
trigger_node = TriggerTranslationsNode()
processor_node = TranslateOneLanguageNode()

trigger_node.on("translate_one", processor_node)
# trigger_node.on("aggregate_results", aggregation_node) # If aggregation is needed

# Use ParallelFlow to run translations concurrently
translation_flow = ParallelFlow(trigger_node)

# --- Example Execution (Conceptual) ---
# import asyncio
# async def main():
#     memory_store = {"text": "Hello World"}
#     await translation_flow.run(memory_store)
#     # Results are in memory_store["translations"]
# asyncio.run(main())
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
// Before (v0.2) - Conceptual BatchNode
// class TranslateTextBatchNode extends BatchNode<any, any, any, [string, string], string> {
//   async prep(shared: Record<string, any>): Promise<[string, string][]> {
//     const text = shared['text'] ?? '(No text provided)';
//     const languages = shared['languages'] ?? ['Chinese', 'Spanish', 'Japanese'];
//     return languages.map((lang: string) => [text, lang]);
//   }
//
//   async execOne(item: [string, string]): Promise<string> {
//     const [text, lang] = item;
//     // Assume translateText exists
//     return await translateText(text, lang);
//   }
//
//   async post(shared: Record<string, any>, prepRes: any, execResults: string[]): Promise<string> {
//     shared['translations'] = execResults;
//     return 'default';
//   }
// }
```

```typescript
// After (v0.3) - Using Flow Patterns with ParallelFlow

import { Memory, Node, ParallelFlow } from 'brainyflow'

// Assume getLanguages exists or is defined
declare function getLanguages(): string[]

// Define Memory structure (optional but recommended)
interface TranslationGlobalStore {
  text?: string
  languages?: string[]
  translations?: ({ language: string; translation: string } | null)[]
}
interface TranslationLocalStore {
  text_to_translate?: string
  language?: string
  result_index?: number
}
type TranslationActions = 'translate_one' | 'aggregate_results' // Add aggregate if needed

// 1. Trigger Node (Fans out work)
class TriggerTranslationsNode extends Node<
  TranslationGlobalStore,
  TranslationLocalStore,
  TranslationActions[]
> {
  async prep(
    memory: Memory<TranslationGlobalStore, TranslationLocalStore>,
  ): Promise<{ text: string; languages: string[] }> {
    const text = memory.text ?? '(No text provided)'
    const languages = memory.languages ?? getLanguages()
    return { text, languages }
  }

  // No exec needed for this trigger node

  async post(
    memory: Memory<TranslationGlobalStore, TranslationLocalStore>,
    prepRes: { text: string; languages: string[] },
    execRes: void, // No exec result
  ): Promise<void> {
    const { text, languages } = prepRes
    // Initialize results array in global memory
    memory.translations = new Array(languages.length).fill(null)

    // Trigger processing for each language
    languages.forEach((lang, index) => {
      this.trigger('translate_one', {
        text_to_translate: text,
        language: lang,
        result_index: index,
      })
    })

    // Optional: Trigger an aggregation step if needed after all parallel tasks
    // this.trigger("aggregate_results");
  }
}

// 2. Processor Node (Handles one language)
class TranslateOneLanguageNode extends Node<TranslationGlobalStore, TranslationLocalStore> {
  async prep(
    memory: Memory<TranslationGlobalStore, TranslationLocalStore>,
  ): Promise<{ text: string; lang: string; index: number }> {
    // Read data passed via forkingData from local memory
    const text = memory.text_to_translate ?? ''
    const lang = memory.language ?? 'unknown'
    const index = memory.result_index ?? -1
    return { text, lang, index }
  }

  async exec(prepRes: {
    text: string
    lang: string
    index: number
  }): Promise<{ translated: string; index: number; lang: string }> {
    const { text, lang, index } = prepRes
    // --- Call external translation API ---
    // const translated_text = await callTranslationApi(text, lang);
    const translated_text = `'${text}' translated to ${lang}` // Placeholder
    // -------------------------------------
    return { translated: translated_text, index, lang }
  }

  async post(
    memory: Memory<TranslationGlobalStore, TranslationLocalStore>,
    prepRes: { text: string; lang: string; index: number }, // prepRes is passed through
    execRes: { translated: string; index: number; lang: string },
  ): Promise<void> {
    const { index, lang, translated } = execRes
    // Store result in the global list at the correct index
    // Ensure the global array exists and is long enough (important for parallel)
    if (!memory.translations) memory.translations = []
    while (memory.translations.length <= index) {
      memory.translations.push(null)
    }
    memory.translations[index] = { language: lang, translation: translated }
    // No trigger needed here, this branch ends.
  }
}

// 3. Flow Setup (Using ParallelFlow for concurrency)
const triggerNode = new TriggerTranslationsNode()
const processorNode = new TranslateOneLanguageNode()

triggerNode.on('translate_one', processorNode)
// triggerNode.on("aggregate_results", aggregationNode); // If aggregation is needed

// Use ParallelFlow to run translations concurrently
const translationFlow = new ParallelFlow<TranslationGlobalStore>(triggerNode)

// --- Example Execution (Conceptual) ---
// async function main() {
//   const memoryStore: TranslationGlobalStore = { text: 'Hello World' };
//   await translationFlow.run(memoryStore);
//   // Results are in memoryStore.translations
// }
// main().catch(console.error);
```

{% endtab %}
{% endtabs %}

## Need Help?

If you encounter issues during migration, you can:

1. Check the [documentation](../index.md) for detailed explanations
2. Look at the [examples](../examples/index.md) for reference implementations
3. File an issue on [GitHub](https://github.com/zvictor/brainyflow/issues)

Happy migrating!
