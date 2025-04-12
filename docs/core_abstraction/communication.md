# Communication

Nodes and Flows in BrainyFlow communicate through two primary mechanisms:

1. **Shared Store (recommended for most cases)**

   - A global data structure (typically an in-memory dictionary) that all nodes can read from (`prep()`) and write to (`post()`)
   - Ideal for sharing data results, large content, or information needed by multiple nodes
   - Follows the principle of separation of concerns by keeping data separate from computation logic

2. **Params (primarily for [Batch](./batch.md) operations)**
   - Node-specific configuration passed down from parent flows
   - Best for identifiers like filenames or IDs, especially in Batch processing
   - Parameter keys and values should be **immutable** during execution

If you know memory management, think of the **Shared Store** like a **heap** (shared by all function calls), and **Params** like a **stack** (assigned by the caller).

## Shared Store

The Shared Store is the primary communication mechanism in BrainyFlow, embodying the principle of separation between data storage and computation logic.

### Overview

A shared store is typically an in-memory dictionary that serves as a global data repository:

{% tabs %}
{% tab title="Python" %}

```python
shared = {
    "data": {...},
    "results": {...},
    "config": {...},
    # Any other data you need to share
}
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
const shared = {
  data: {...},
  results: {...},
  config: {...},
  // Any other data you need to share
}
```

{% endtab %}
{% endtabs %}

The shared store can also contain file handlers, database connections, or other resources that need to be accessible across nodes.

### Best Practices

1. **Define a Clear Schema**: Plan your shared store structure before implementation
2. **Use Namespaces**: Group related data under descriptive keys
3. **Document Structure**: Comment on expected data types and formats
4. **Avoid Deep Nesting**: Keep the structure reasonably flat for readability

### Example Usage

{% tabs %}
{% tab title="Python" %}

```python
class LoadData(Node):
    async def post(self, shared, prep_res, exec_res):
        # Write data to shared store
        shared["data"] = "Some text content"

class Summarize(Node):
    async def prep(self, shared):
        # Read data from shared store
        return shared["data"]

    async def exec(self, prep_res):
        # Call LLM to summarize
        prompt = f"Summarize: {prep_res}"
        summary = call_llm(prompt)
        return summary

    async def post(self, shared, prep_res, exec_res):
        # Write summary to shared store
        shared["summary"] = exec_res

load_data = LoadData()
summarize = Summarize()
load_data >> summarize
flow = Flow(start=load_data)

shared = {}
await flow.run(shared)
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
class LoadData extends Node {
  async post(shared: Record): Promise {
    // Write data to shared store
    shared.data = 'Some text content'
  }
}

class Summarize extends Node {
  async prep(shared: Record): Promise {
    // Read data from shared store
    return shared.data
  }

  async exec(prepRes: string): Promise {
    // Call LLM to summarize
    const prompt = `Summarize: ${prepRes}`
    const summary = await callLLM(prompt)
    return summary
  }

  async post(shared: Record, prepRes: string, execRes: string): Promise {
    // Write summary to shared store
    shared.summary = execRes
  }
}

const loadData = new LoadData()
const summarize = new Summarize()
loadData.next(summarize)
const flow = new Flow(loadData)

const shared = {}
await flow.run(shared)
```

{% endtab %}
{% endtabs %}

## Params

While the Shared Store is the primary communication mechanism, Params provide a way to configure individual nodes with specific settings.

### Key Characteristics

- **Immutable**: Params don't change during a node's execution cycle
- **Hierarchical**: Params are passed down from parent flows to child nodes
- **Local**: Each node or flow has its own params that don't affect other nodes

### When to Use Params

- **Batch Processing**: To identify which item is being processed
- **Configuration**: For node-specific settings that don't need to be shared
- **Identification**: For tracking the source or purpose of a computation

### Example Usage

{% tabs %}
{% tab title="Python" %}

```python
# 1) Create a Node that uses params
class SummarizeFile(Node):
    async def prep(self, shared):
        # Access the node's param
        filename = self.params["filename"]
        return shared["data"].get(filename, "")

    async def exec(self, prep_res):
        prompt = f"Summarize: {prep_res}"
        return call_llm(prompt)

    async def post(self, shared, prep_res, exec_res):
        filename = self.params["filename"]
        shared["summary"][filename] = exec_res

# 2) Set params directly on a node (for testing)
node = SummarizeFile()
node.set_params({"filename": "doc1.txt"})
await node.run(shared)

# 3) Set params on a flow (overrides node params)
flow = Flow(start=node)
flow.set_params({"filename": "doc2.txt"})
await flow.run(shared)  # The node summarizes doc2.txt, not doc1.txt
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
// 1) Create a Node that uses params
class SummarizeFile extends Node {
  async prep(shared: Record): Promise {
    // Access the node's param
    const filename = this.params.filename
    return shared.data[filename] || ''
  }

  async exec(prepRes: string): Promise {
    const prompt = `Summarize: ${prepRes}`
    return await callLLM(prompt)
  }

  async post(shared: Record, prepRes: string, execRes: string): Promise {
    const filename = this.params.filename
    shared.summary[filename] = execRes
  }
}

// 2) Set params directly on a node (for testing)
const node = new SummarizeFile()
node.setParams({ filename: 'doc1.txt' })
await node.run(shared)

// 3) Set params on a flow (overrides node params)
const flow = new Flow(node)
flow.setParams({ filename: 'doc2.txt' })
await flow.run(shared) // The node summarizes doc2.txt, not doc1.txt
```

{% endtab %}
{% endtabs %}

## Choosing Between Shared Store and Params

| Use Shared Store when...                    | Use Params when...                           |
| ------------------------------------------- | -------------------------------------------- |
| Data needs to be accessed by multiple nodes | Configuration is specific to a single node   |
| Information persists across the entire flow | Working with Batch processing                |
| Storing large amounts of data               | Passing identifiers or simple values         |
| Maintaining state throughout execution      | Configuring behavior without affecting state |

{% hint style="success" %}
**Best Practice**: Use Shared Store for almost all cases to maintain separation of concerns. Params are primarily useful for Batch processing and node-specific configuration.
{% endhint %}
