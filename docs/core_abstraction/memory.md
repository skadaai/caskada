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

## Writing to Memory

- **Writing to Global Store**: Assigning a value directly to a property on the `memory` object (e.g., `memory.someValue = 'new data'`) writes to the **global store**. The proxy automatically removes the property from the local store first if it exists there.
- **Writing to Local Store**: While possible via `memory.local.someValue = 'new data'`, the primary and recommended way to populate the local store for downstream nodes is using the `forkingData` argument in `this.trigger()`.

{% tabs %}
{% tab title="Python" %}

```python
from brainyflow import Node, Memory

# Assume exec returns a dict like {"files": [...], "count": ...}
class DataWriterNode(Node):
    async def post(self, memory: Memory, prep_res, exec_res: dict):
        # --- Writing to Global Store ---
        # Accessible to all nodes in the flow and outside
        memory.fileList = exec_res["files"]
        print(f"Memory updated globally: fileList={memory.fileList}")
        
        # --- Writing to Local Store ---
        # Accessible to this node and all descendants
        memory.local.processedCount = exec_res["count"]
        print(f"Memory updated locally: processedCount={memory.processedCount}")

        # --- Triggering with Local Data (Forking Data) ---
        # 'file' will be added to the local store of the memory clone
        # passed to the node(s) triggered by the 'process_file' action.
        for file_item in exec_res["files"]:
            self.trigger('process_file', { "file": file_item })

# Example Processor Node (triggered by 'process_file')
class FileProcessorNode(Node):
     async def prep(self, memory: Memory):
         # Reads 'file' from the local store first, then global
         file_to_process = memory.file
         print(f"Processing file (fetched from local memory): {file_to_process}")
         return file_to_process
     # ... exec, post ...
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
import { Memory, Node } from 'brainyflow'

interface MyGlobal {
  fileList?: string[]
  results?: Record<string, any>
}
interface MyLocal {
  processedCount?: number // Data passed via memory.local assignment
  file?: string // Data passed via forkingData
}

class DataWriterNode extends Node<MyGlobal, MyLocal, ['process_file']> {
  async post(
    memory: Memory<MyGlobal, MyLocal>,
    prepRes: any,
    execRes: { files: string[]; count: number }, // Assume exec returns this format
  ): Promise<void> {
    // --- Writing to Global Store ---
    // Accessible to all nodes in the flow
    memory.fileList = execRes.files
    console.log(`Memory updated globally: fileList=${memory.fileList}`)

    // --- Writing to Local Store ---
    // Accessible to this node and all descendants
    memory.local.processedCount = execRes.count
    console.log(`Memory updated locally: processedCount={memory.processedCount}`)

    // --- Triggering with Local Data (Forking Data) ---
    // 'file' will be added to the local store of the memory clone
    // passed to the node(s) triggered by the 'process_file' action.
    for (const file of execRes.files) {
      this.trigger('process_file', { file: file })
    }
  }
}

// Example Processor Node (triggered by 'process_file')
class FileProcessorNode extends Node<MyGlobal, MyLocal> {
  async prep(memory: Memory<MyGlobal, MyLocal>): Promise<string | undefined> {
    // Reads 'file' from the local store first, then global
    const fileToProcess = memory.file
    console.log(`Processing file (from local memory): ${fileToProcess}`)
    return fileToProcess
  }
  // ... exec, post ...
}
```

{% endtab %}
{% endtabs %}

## Best Practices

- **Read in `prep()`**: Gather necessary input data from `memory` at the beginning of a node's execution.
- **Write Global State in `post()`**: Update the shared global store by assigning to `memory` properties (e.g., `memory.results = ...`) in the `post()` phase after processing is complete.
- **Set Local State via `forkingData`**: Pass branch-specific context to successors by providing the `forkingData` argument in `this.trigger()` within the parent's `post()` method. This populates the `local` store for the next node(s).
- **Read Transparently**: Always read data via the `memory` proxy (e.g., `memory.someValue`). It handles the local-then-global lookup automatically. Avoid reading directly from `memory.local` or other internal properties unless strictly needed.

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
3.  **Local State Creation**: Use `trigger(action, forkingData)` in `post()` to populate the `local` store for the _next_ node(s) in a specific branch.
4.  **Lifecycle**: Read from `memory` in `prep`, compute in `exec` (no memory access), write global state to `memory` and trigger successors (potentially with `forkingData` for local state) in `post`.
