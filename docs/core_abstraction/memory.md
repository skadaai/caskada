# Communication Between Nodes

BrainyFlow provides a streamlined approach for components to communicate with each other. This chapter explains how data flows through your application.

## Memory Types

Each flow execution maintains two types of memory:

1. **Global Memory**: Shared across all nodes, known to all components in the flow (a _shared store_)
2. **Local Memory**: Passed from a node to its descendants only (a _local store_)

This dual memory system allows for both shared state and isolated communication paths.

{% hint style="success" %}
**Real-World Analogy**:

Think of the memory system like a river delta:

- **Global Memory**: The main river water that flows everywhere
- **Local Memory**: Specific channels that might carry unique properties that only affect downstream areas fed by that channel

This model gives you the flexibility to share data across your entire flow or isolate it to specific execution paths as needed.

{% endhint %}

## Accessing Memory

Nodes can read from memory using direct property access:

```typescript
async prep(memory: Memory): Promise {
  // Read from memory (checks local first, then global)
  const filePath = memory.filePath;
  const config = memory.config;

  return filePath;
}
```

The memory system automatically checks local memory first, then falls back to global memory if the property isn't found locally.

## Writing to Memory

- Writing directly to `memory` affects the global state.
- Writing to `memory.local` affects the local state.

```typescript
async post(memory: Memory, prepResult: string, fileList: string[]): Promise {
  // Store in global memory
  memory.fileList = fileList;

  // Set local memory for current node and its child nodes
  memory.local.currentFile = fileList[0];

  // Trigger default action (clild node will inherit global & local memories)
  this.trigger('default');
}
```

### Creating Exclusive Local Memory for a Descendant

When triggering a child node, you can create exclusive local memory for that downstream node by passing forking data.

```typescript
async post(memory: Memory, prepResult: string, fileList: string[]): Promise {
  // Store metadata in global memory
  memory.filesAmount = fileList.length;
  // Make list of files accessible to all child nodes (but not to outer world!)
  memory.local.fileList = fileList;

  // Process each file individually
  for (const file of fileList) {
    // Fork local memory for this specific execution branch
    this.trigger('default', { filePath: file });
  }
}
```

The `trigger()` method activates child nodes with the specified local memory, which is only accessible to those descendants.

## Best Practices

- **Read in `prep()`**: Gather input data at the beginning of execution
- **Write in `post()`**: Update memory after processing is complete
- **Always read from `memory`**: Never read directly from `memory.local`

## Type Safety

For better type safety, define your memory structure:

```typescript
interface MyGlobalMemory {
  files: string[]
  config: { apiKey: string }
  results: Record
}

interface MyLocalMemory {
  filePath: string
  priority: number
}

class ProcessorNode extends Node {
  async prep(memory: Memory<MyGlobalMemory, MyLocalMemory>): Promise {
    // TypeScript now provides intellisense and type checking
    return memory.filePath
  }
}
```

## Batch Processing Pattern

A common pattern that explores the memory system well is to process multiple items in parallel:

```typescript
class ParentNode extends Node {
  // Parent node generates items
  async post(memory: Memory, input: any, items: string[]): Promise {
    for (const item of items) {
      this.trigger('default', { currentItem: item })
    }
  }
}

class ChildNode extends Node {
  // Child node processes each item independently
  async prep(memory: Memory): Promise {
    return memory.currentItem // Gets the local value
  }
}
```

## When to Use The Memory

- **Ideal for**: Sharing data results, large content, or information needed by multiple components
- **Benefits**: Separates data from computation logic (separation of concerns)
- **Global Memory**: Use for application-wide state, configuration, and final results
- **Local Memory**: Use for passing contextual data down a specific execution path

## Technical Concepts

The memory system in BrainyFlow implements several established computer science patterns:

- **Lexical Scoping**: Local memory "shadows" global memory, similar to how local variables in functions can shadow global variables
- **Context Propagation**: Local memory propagates down the execution tree, similar to how context flows in React or middleware systems
- **Transparent Resolution**: The system automatically resolves properties from the appropriate memory scope

## Remember

1. Always read from `memory` directly
2. Write to `memory` for global state, `memory.local` for downstream-only state
3. Use `trigger(action, forkingData)` to start child nodes with specific local memory
4. Maintain a clear read/write pattern with `prep()` and `post()`
