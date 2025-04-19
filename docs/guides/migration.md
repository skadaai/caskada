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

### Batch Processing Changes

In v0.3, batch processing classes like `BatchNode` and `ParallelBatchNode` have been removed. Instead, you should use flow patterns for batch processing.

#### Sequential Batch Processing

{% tabs %}
{% tab title="Python" %}

```python
# Before (v0.2) - Using BatchNode
class ProcessBatch(BatchNode):
    async def exec_one(self, item):
        return transformed_item
```

```python
# After (v0.3) - Using Flow Patterns
class BatchInitNode(Node):
    async def prep(self, memory):
        return memory.items

    async def post(self, memory, prep_res, items):
        memory.results = []

        if items and len(items) > 0:
            # Fork with first item
            self.trigger("process_item", {
                "item": items[0],
                "remaining_items": items[1:],
                "index": 0
            })
        else:
            self.trigger("complete")

class ProcessItemNode(Node):
    async def prep(self, memory):
        return memory.item  # From local memory

    async def exec(self, item):
        return process_item(item)

    async def post(self, memory, prep_res, result):
        memory.results.append(result)

        if memory.remaining_items and len(memory.remaining_items) > 0:
            self.trigger("process_item", {
                "item": memory.remaining_items[0],
                "remaining_items": memory.remaining_items[1:],
                "index": memory.index + 1
            })
        else:
            self.trigger("complete")
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
// Before (v0.2) - Using BatchNode
class ProcessBatch extends BatchNode {
  async execOne(item: Item): Promise {
    return transformedItem
  }
}
```

```typescript
// After (v0.3) - Using Flow Patterns
class BatchInitNode extends Node {
  async prep(memory: Memory): Promise {
    return memory.items
  }

  async post(memory: Memory, prepRes: any[], items: any[]): Promise {
    memory.results = []

    if (items && items.length > 0) {
      // Fork with first item
      this.trigger('process_item', {
        item: items[0],
        remaining_items: items.slice(1),
        index: 0,
      })
    } else {
      this.trigger('complete')
    }
  }
}

class ProcessItemNode extends Node {
  async prep(memory: Memory): Promise {
    return memory.item // From local memory
  }

  async exec(item: any): Promise {
    return processItem(item)
  }

  async post(memory: Memory, prepRes: any, result: any): Promise {
    memory.results.push(result)

    if (memory.remaining_items && memory.remaining_items.length > 0) {
      this.trigger('process_item', {
        item: memory.remaining_items[0],
        remaining_items: memory.remaining_items.slice(1),
        index: memory.index + 1,
      })
    } else {
      this.trigger('complete')
    }
  }
}
```

{% endtab %}
{% endtabs %}

#### Parallel Batch Processing

{% tabs %}
{% tab title="Python" %}

```python
# Before (v0.2)
class ParallelProcessBatch(ParallelBatchNode):
    async def exec_one(self, item):
        return processed_item
```

```python
# After (v0.3)
class BatchTriggerNode(Node):
    async def prep(self, memory):
        return memory.items

    async def post(self, memory, prep_res, items):
        memory.results = []

        for index, item in enumerate(items):
            self.trigger("process_item", {
                "item": item,
                "item_index": index
            })
        self.trigger("all_triggered")

class ProcessItemNode(Node):
    async def prep(self, memory):
        return memory.item  # From local memory

    async def exec(self, item):
        return process_item(item)

    async def post(self, memory, prep_res, result):
        memory.results.append((memory.item_index, result))

# Use ParallelFlow to execute in parallel
parallel_batch_flow = ParallelFlow(start=batch_trigger_node)
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
// Before (v0.2)
class ParallelProcessBatch extends ParallelBatchNode {
  async execOne(item: Item): Promise {
    return processedItem
  }
}
```

```typescript
// After (v0.3)
class BatchTriggerNode extends Node {
  async prep(memory: Memory): Promise {
    return memory.items;
  }

  async post(memory: Memory, prepRes: any[], items: any[]): Promise {
    memory.results = [];

  for (let index = 0; index < items.length; index++) {
    this.trigger("process_item", {
      item: items[index],
      item_index: index
    });
  }
  this.trigger("all_triggered");
}

class ProcessItemNode extends Node {
  async prep(memory: Memory): Promise {
    return memory.item;  // From local memory
  }

  async exec(item: any): Promise {
    return processItem(item);
  }

  async post(memory: Memory, prepRes: any, result: any): Promise {
    memory.results.push([memory.item_index, result]);
  }
}

// Use ParallelFlow to execute in parallel
const parallelBatchFlow = new ParallelFlow(batchTriggerNode);
```

{% endtab %}
{% endtabs %}

## Need Help?

If you encounter issues during migration, you can:

1. Check the [documentation](../index.md) for detailed explanations
2. Look at the [examples](../examples/index.md) for reference implementations
3. File an issue on [GitHub](https://github.com/zvictor/brainyflow/issues)

Happy migrating!
