# Memory: Managing State Between Nodes

In Caskada, the `Memory` object is the central mechanism for state management and communication between nodes in a flow. It's designed to be flexible yet robust, providing both shared global state and isolated local state for different execution paths.

## Creating Memory

The proxied memory instance is automatically created when you pass the initial memory object to a Flow. Alternatively, you can explicitly create it using the `createMemory` function (in TypeScript) or the standard constructor `Memory()` (in Python):

{% tabs %}
{% tab title="Python" %}

```python
from caskada import Memory

global_store = {"initial_config": "abc"}
local_store_for_start_node = {"start_node_specific": 123} # Optional

memory_instance = Memory(global_store, local_store_for_start_node)
# or just: memory_instance = Memory(global_store)
```

{% endtab %}
{% tab title="TypeScript" %}

```typescript
import { createMemory, Memory, SharedStore } from 'caskada'

interface MyGlobal extends SharedStore {
  initial_config?: string
}
interface MyLocal extends SharedStore {
  start_node_specific?: number
}

const globalStore: MyGlobal = { initial_config: 'abc' }
const localStoreForStartNode: MyLocal = { start_node_specific: 123 } // Optional

const memoryInstance: Memory = createMemory(globalStore, localStoreForStartNode)
// or just: const memoryInstance = createMemory(globalStore);
```

{% endtab %}
{% endtabs %}

## Memory Scopes: Global vs. Local

Caskada's `Memory` object manages two distinct scopes:

1.  **Global Store (`memory`)**: A single object shared across _all_ nodes within a single `flow.run()` execution. Changes made here persist throughout the flow. Think of it as the main shared state.
2.  **Local Store (`memory.local`)**: An object specific to a particular execution path within the flow. It's created when a node `trigger`s a successor. Changes here are isolated to that specific branch and its descendants.
    Accessing `memory.local` directly (e.g., `memory.local.someKey`) allows you to read from or write to _only_ the local store of the current memory instance.

This dual-scope system allows for both shared application state (global) and controlled, path-specific data propagation (local).

{% hint style="success" %} **Real-World Analogies**:

Think of the memory system like **a river delta**:

- **Global Store**: The main river, carrying essential data that all branches need.
- **Local Store**: The smaller streams and tributaries that branch off. They carry specific data relevant only to their path, but can still access the main river's water (global store).

Or, consider **programming scopes**:

- **Global Store**: Like variables declared in the outermost scope of a program, accessible everywhere.
- **Local Store**: Like variables declared inside a function or block. They are only accessible within that block and any nested blocks (downstream nodes in the flow). If a local variable has the same name as a global one, the local variable "shadows" the global one within its scope.

This model gives you the flexibility to share data across your entire flow (global) or isolate context to specific execution paths (local).
{% endhint %}

## Accessing Memory (Reading)

Nodes access data stored in either scope through the `memory` proxy instance passed to their `prep` and `post` methods. When you read a property (e.g., `memory.someValue`), the proxy automatically performs a lookup:

1.  It checks the **local store (`memory.local`)** first.
2.  If the property is not found locally, it checks the **global store (`memory`)**.

```typescript
import { Memory, Node } from 'caskada'

interface MyGlobal {
  config?: object
  commonData?: string
  pathSpecificData?: string // Can be global or shadowed by local
}
interface MyLocal {
  pathSpecificData?: string
} // Can shadow global properties

class MyNode extends Node<MyGlobal, MyLocal> {
  async prep(memory: Memory<MyGlobal, MyLocal>): Promise<void> {
    // Reads from global store (assuming not set locally)
    const config = memory.config
    const common = memory.commonData

    // Reads 'pathSpecificData' from local store if it exists there,
    // otherwise falls back to reading from the global store.
    const specific = memory.pathSpecificData

    // To read ONLY from the local store:
    const onlyLocal = memory.local.pathSpecificData
  }
  // ... exec, post ...
}
```

As a rule of thumb, when accessing memory, you should always prefer using `memory.someValue` and let the `Memory` manager figure out where to fetch the value for you.
Even though you could directly access the entire local store object using `memory.local` - or a value at `memory.local.someValue` - that approach adds little value and is pattern that can be safely avoided, unless you want to be very explicit about your design choice.

As you will see in the next section, _it's at the writing time that you want to be more careful about where to place your data._

```typescript
async post(memory: Memory<MyGlobal, MyLocal>, /*...*/) {
    const allLocalData = memory.local; // Access the internal __local object directly
    console.log('Current local store:', allLocalData);
}
```

## Writing to Memory

- **Writing to Global Store**: Assigning a value directly to a property on the `memory` object (e.g., `memory.someValue = 'new data'`) writes to the **global store**. The proxy automatically removes the property from the local store first if it exists there.
- **Writing to Local Store**: You can write directly to the local store of the current memory instance using `memory.local.someValue = 'new data'`. This affects _only_ the current node's local context and any downstream nodes that inherit this specific memory clone.
  However, the most convenient way to populate the local store for _newly created branches_ (i.e., for successor nodes) is by providing the `forkingData` argument in `this.trigger(action[, forkingData])`.

## Deleting from Memory

- **Deleting from Global/Local (via main proxy)**: Using `del memory.someKey` (Python) or `delete memory.someKey` (TypeScript) will attempt to delete the key from the global store and also from the current local store.
- **Deleting from Local Only (via `memory.local`)**: Using `del memory.local.someKey` (Python) or `delete memory.local.someKey` (TypeScript) will delete the key _only_ from the current local store.

## Checking for Existence (`in` operator)

- **`'key' in memory`**: Checks if `'key'` exists in either the local store or the global store.
- **`'key' in memory.local`**: Checks if `'key'` exists _only_ in the local store.

{% tabs %}
{% tab title="Python" %}

Note that you can set types to the memory, like in TypeScript!
That is optional, but helps you keep your code organized.

```python
from typing import List, TypedDict
from caskada import Memory, Node

class GlobalStore(TypedDict, total=False):
    fileList: List[str]
    config: dict
    results: dict

class DataWriterLocalStore(TypedDict, total=False):
    processedCount: int
    file: str
    branch_id: str

# Assume exec returns a dict like {"files": [...], "count": ...}
class DataWriterNode(Node[GlobalStore, DataWriterLocalStore]):
    async def post(self, memory, prep_res, exec_res) -> None:
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
     async def prep(self, memory):
         # Reads 'file' from the local store first, then global
         file_to_process = memory.file
         print(f"Processing file (fetched from local memory): {file_to_process}")
         return file_to_process
     # ... exec, post ...
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
import { Memory, Node } from 'caskada'

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
    console.log(`Memory updated locally: processedCount=${memory.processedCount}`)

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

The memory system in Caskada implements several established computer science patterns:

- **Lexical Scoping**: Local memory "shadows" global memory, similar to how local variables in functions can shadow global variables
- **Context Propagation**: Local memory propagates down the execution tree, similar to how context flows in React or middleware systems
- **Transparent Resolution**: The system automatically resolves properties from the appropriate memory scope

## Remember

1.  **Reading**: Always read via the `memory` proxy (e.g., `memory.value`). It checks local then global.
2.  **Writing to Global**: Direct assignment `memory.property = value` writes to the **global** store (and removes `property` from local if it was there).
3.  **Writing to Local (Current Node & Successors)**: Assignment `memory.local.property = value` writes _only_ to the current memory instance's local store. and its descendents.
4.  **Creating Local State for Successors**: Use `trigger(action, forkingData)` in `post()` to populate the `local` store for the _next_ node(s) in a specific branch.
5.  **Lifecycle**: Read from `memory` in `prep`, compute in `exec` (no memory access), write global state to `memory` and trigger successors (potentially with `forkingData` for local state) in `post`.
6.  **Cloning**: When a flow proceeds to a new node, or when `memory.clone()` is called, the global store is shared by reference, while the local store is deeply cloned. `forkingData` provided to `clone` is also deeply cloned and merged into the new local store.

## Advanced: `memory.clone()`

The `memory.clone(forkingData?)` method is primarily used internally by the `Flow` execution logic when transitioning between nodes. However, you can also use it manually if you need to create a new `Memory` instance that shares the same global store but has an independent, optionally modified, local store.

This cloning mechanism is fundamental to how Caskada isolates state between different branches of execution within a flow.
