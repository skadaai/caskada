# Memory: Managing State Between Nodes

BrainyFlow provides a streamlined approach for components to communicate with each other. This chapter explains how data is stored, accessed, and isolated.

## Memory Scopes: Global vs. Local

Each `Memory` instance encapsulates two distinct scopes:

1.  **Global Store (`memory`)**: A single object shared across _all_ nodes within a single `flow.run()` execution. Changes made here persist throughout the flow. Think of it as the main shared state.
2.  **Local Store (`memory.local`)**: An object specific to a particular execution path within the flow. It's created when a node `trigger`s a successor. Changes here are isolated to that specific branch and its descendants.

This dual-scope system allows for both shared application state (global) and controlled, path-specific data propagation (local).

{% hint style="success" %}
**Real-World Analogies**:

Think of the memory system like **a river delta**:

- **Global Store**: The main river water that flows everywhere
- **Local Store**: Specific channels that might carry unique properties that only affect downstream areas fed by that channel


Alternatively, think of it like **nested scopes in programming**:

- **Global Store**: Like variables declared in the outermost scope of a program, accessible everywhere.
- **Local Store**: Like variables declared inside a function or block. They are only accessible within that block and any nested blocks (downstream nodes in the flow). If a local variable has the same name as a global one, the local variable "shadows" the global one within its scope.

This model gives you the flexibility to share data across your entire flow (global) or isolate context to specific execution paths (local).
{% endhint %}

## Accessing Memory (Reading)

Nodes access data stored in either scope through the `memory` proxy instance passed to their `prep` and `post` methods. When you read a property (e.g., `memory.someValue`), the proxy automatically performs a lookup:

1.  It checks the **local store (`memory.local`)** first.
2.  If the property is not found locally, it checks the **global store (`memory`)**.

```typescript
import { Memory, Node } from 'brainyflow'

interface MyGlobal {
  config?: object
  commonData?: string
  pathSpecificData?: string
}
interface MyLocal {
  pathSpecificData?: string
} // Can shadow global

class MyNode extends Node<MyGlobal, MyLocal> {
  async prep(memory: Memory<MyGlobal, MyLocal>): Promise<void> {
    // Reads from global store (assuming not set locally)
    const config = memory.config
    const common = memory.commonData

    // Reads from local store if set via forkingData, otherwise reads from global
    const specific = memory.pathSpecificData
  }
  // ... exec, post ...
}
```

When accessing memory, you should always use `memory.someValue` and let the `Memory` manager figure out where to fetch the value for you.
You could also directly access the entire local store object using `memory.local` - or a value at `memory.local.someValue` - but that's an anti-pattern that should be avoided.

```typescript
async post(memory: Memory<MyGlobal, MyLocal>, /*...*/) {
    const allLocalData = memory.local; // Access the internal __local object directly
    console.log('Current local store:', allLocalData);
}
```

## Writing to Memory (Global Store)

- Writing properties directly onto the `memory` object (e.g., `memory.someValue = 'new data'`) modifies the **global store** by default. The proxy ensures that if a property with the same name existed in the local store, it is removed before setting the global value.
- Writing properties directly onto the `memory.local` object (e.g., `memory.local.someValue = 'new data'`) modifies the **local store** by default.
- The primary way to populate the **local store (`memory.local`)** for a specific execution branch is by providing the `forkingData` argument when calling `this.trigger()` in the parent node's `post` method.

```typescript
import { Memory, Node } from 'brainyflow'

interface MyGlobal {
  fileList?: string[]
  processedCount?: number
}
interface MyLocal {}

class DataWriterNode extends Node<MyGlobal, MyLocal> {
  async post(
    memory: Memory<MyGlobal, MyLocal>,
    prepRes: any,
    execRes: { files: string[]; count: number }, // Assume exec returns in this format
  ): Promise<void> {
    // --- Writing to Global Store ---
    // Accessible to all nodes in the flow
    memory.fileList = execRes.files

    // --- Writing to Local Store ---
    // Accessible to this node and all descendants
    memory.processedCount = execRes.count

    console.log('Memory updated:', memory)

    for(const file of fileList)
      // Trigger next node with exclusive local value for `memory.file` (set at `memory.local.file`)
      this.trigger('default', { file })
  }
}
```

## Best Practices

- **Read in `prep()`**: Gather necessary input data from `memory` at the beginning of a node's execution.
- **Write Global State in `post()`**: Update the shared global store by writing to `memory` (e.g., `memory.results = ...`) in the `post()` phase after processing is complete.
- **Set Local State via `forkingData`**: Pass branch-specific context to successors by providing the `forkingData` argument in `this.trigger()` within the parent's `post()` method.
- **Read Transparently**: Always read data via the `memory` proxy (e.g., `memory.someValue`). It handles the local-then-global lookup automatically. Avoid reading directly from `memory.__global` or `memory.__local` unless you have a specific reason.

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

1.  **Reading**: Always read via the `memory` proxy (e.g., `memory.value`). It checks local then global.
2.  **Writing**: Direct assignment `memory.property = value` writes to the **global** store.
3.  **Local State Creation**: Use `trigger(action, forkingData)` in `post()` to populate the local store for the _next_ node(s) in a specific branch.
4.  **Lifecycle**: Read in `prep`, compute in `exec` (no memory access), write global state and trigger successors (potentially with `forkingData` for local state) in `post`.
