# Batch Processing

Batch processing in BrainyFlow enables efficient handling of multiple items, whether sequentially or in parallel. This is particularly useful for:

- Processing large datasets or lists (e.g., multiple files, database records)
- Applying the same operation to multiple inputs
- Dividing large tasks into manageable chunks

## How Params Work in Batch Processing

Batch item params override flow params, which override node params. Params are read-only during execution.

For a full explanation, example, and cheat sheet, see [How Params Work](./memory.md#how-params-work).

## Node-Level Batch Processing

BrainyFlow provides two specialized node types for batch processing:

### SequentialBatchNode

A `SequentialBatchNode` processes items one after another, which is useful when:

- Order of processing matters
- Operations have dependencies between items
- You need to conserve resources or manage rate limits

It extends `Node`, with changes to:

- **`async prep(shared)`**: returns an **iterable** (e.g., list, generator).
- **`async exec(item)`**: called **once** per item in that iterable.
- **`async post(shared, prep_res, exec_res_list)`**: after all items are processed, receives a **list** of results (`exec_res_list`) and returns an **Action**.

#### Example: Sequential Summarize File

{% tabs %}
{% tab title="Python" %}
{% hint style="info" %}
**Python GIL Note**: Due to Python's GIL, parallel nodes can't truly parallelize CPU-bound tasks but excel at I/O-bound work like API calls.
{% endhint %}

```python
class SequentialSummaries(SequentialBatchNode):
    async def prep(self, shared):
        """Return an iterable of items to process."""
        content = shared["data"]
        chunk_size = 10000
        # Suppose we have a big file; chunk it!
        return [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]

    async def exec(self, chunk):
        """Process a single chunk. Called once per item."""
        prompt = f"Summarize this chunk in 10 words: {chunk}"
        return call_llm(prompt)

    async def post(self, shared, prep_res, exec_res_list):
        """Process all results after all items are processed."""
        shared["summary"] = "\n".join(exec_res_list)
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
class SequentialSummaries extends SequentialBatchNode {
  async prep(shared: Record): Promise {
    const content = shared.data
    const chunkSize = 10000
    const chunks: string[] = []

    // Suppose we have a big file; chunk it!
    for (let i = 0; i < content.length; i += chunkSize) {
      chunks.push(content.slice(i, i + chunkSize))
    }
    return chunks
  }

  async exec(chunk: string): Promise<string> {
    const prompt = `Summarize this chunk in 10 words: ${chunk}`
    return await callLLM(prompt)
  }

  async post(shared: Record, prepRes: string[], execResList: string[]): Promise {
    shared.summary = execResList.join('\n')
  }
}
```

{% endtab %}
{% endtabs %}

### ParallelBatchNode

A `ParallelBatchNode` processes items concurrently, which is useful when:

- Operations are independent of each other
- You want to maximize throughput
- Tasks are primarily I/O-bound (like API calls)

{% hint style="warning" %}
**Concurrency Considerations**:

- Ensure operations are truly independent before using parallel processing
- Be mindful of rate limits when making API calls
- Consider using [Throttling](../guides/throttling.md) to control concurrency

{% endhint %}

It extends `Node`, with changes to:

- **`async prep(shared)`**: returns an **iterable** (e.g., list, generator).
- **`async exec(item)`**: called **concurrently** for each item.
- **`async post(shared, prep_res, exec_res_list)`**: after all items are processed, receives a **list** of results (`exec_res_list`) and returns an **Action**.

#### Example: Parallel Summarize of a Large File

{% tabs %}
{% tab title="Python" %}

```python
class ParallelSummaries(ParallelBatchNode):
    async def prep(self, shared):
        """Return an iterable of items to process in parallel."""
        content = shared["data"]
        chunk_size = 10000
        # Suppose we have a big file; chunk it!
        return [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]

    async def exec(self, chunk):
        """Process a single chunk. Called concurrently for all items."""
        prompt = f"Summarize this chunk in 10 words: {chunk}"
        return call_llm(prompt)

    async def post(self, shared, prep_res, exec_res_list):
        """Process all results after all items are processed."""
        shared["summary"] = "\n".join(exec_res_list)
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
class ParallelSummaries extends ParallelBatchNode {
  async prep(shared: Record): Promise {
    const content = shared.data
    const chunkSize = 10000
    const chunks: string[] = []

    // Suppose we have a big file; chunk it!
    for (let i = 0; i < content.length; i += chunkSize) {
      chunks.push(content.slice(i, i + chunkSize))
    }
    return chunks
  }

  async exec(chunk: string): Promise<string> {
    const prompt = `Summarize this chunk in 10 words: ${chunk}`
    return await callLLM(prompt)
  }

  async post(shared: Record, prepRes: string[], execResList: string[]): Promise {
    shared.summary = execResList.join('\n')
  }
}
```

{% endtab %}
{% endtabs %}

## Flow-Level Batch Processing

BrainyFlow also supports batch processing at the flow level, allowing you to run an entire flow multiple times with different parameters:

### SequentialBatchFlow

A `SequentialBatchFlow` runs a flow multiple times in sequence, with different `params` each time. Think of it as a loop that replays the Flow for each parameter set.

{% hint style="info" %}
**When to use**: Choose sequential processing when order matters or when working with APIs that have strict rate limits. See [Throttling](../guides/throttling.md) for managing rate limits.
{% endhint %}

#### Example: Summarize Many Files

{% tabs %}
{% tab title="Python" %}

```python
class SummarizeAllFiles(SequentialBatchFlow):
    async def prep(self, shared):
        """Return a list of parameter dictionaries, one per file."""
        filenames = list(shared["data"].keys()) # e.g., ["file1.txt", "file2.txt", ...]
        return [{"filename": fn} for fn in filenames]

summarize_file = Flow(start=load_file)

# Create a batch flow that processes all files sequentially
summarize_all_files = SummarizeAllFiles(start=summarize_file)
await summarize_all_files.run(shared)
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
class SummarizeAllFiles extends SequentialBatchFlow {
  async prep(shared: Record): Promise<Array<Record<string, string>>> {
    const filenames = Object.keys(shared.data) // e.g., ["file1.txt", "file2.txt", ...]
    return filenames.map((fn) => ({ filename: fn }))
  }
}

const summarizeFile = new Flow(loadFile)

// Create a batch flow that processes all files sequentially
const summarizeAllFiles = new SummarizeAllFiles(summarizeFile)
await summarizeAllFiles.run(shared)
```

{% endtab %}
{% endtabs %}

#### Under the Hood

1. `prep(shared)` returns a list of param dicts—e.g., `[{filename: "file1.txt"}, {filename: "file2.txt"}, ...]`.
2. The **BatchFlow** loops through each dict. For each one:
   - It merges the dict with the BatchFlow’s own `params`.
   - It calls `flow.run(shared)` using the merged result.
3. This means the sub-Flow is run **repeatedly**, once for every param dict.

### ParallelBatchFlow

A `ParallelBatchFlow` runs a flow multiple times concurrently, with different `params` each time:

{% tabs %}
{% tab title="Python" %}

```python
class SummarizeAllFiles(ParallelBatchFlow):
    async def prep(self, shared):
        """Return a list of parameter dictionaries, one per file."""
        filenames = list(shared["data"].keys())
        return [{"filename": fn} for fn in filenames]

# Create a flow for processing a single file
summarize_file = Flow(start=load_file)

# Create a batch flow that processes all files in parallel
summarize_all_files = ParallelBatchFlow(start=summarize_file)
await summarize_all_files.run(shared)
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
class SummarizeAllFiles extends ParallelBatchFlow {
  async prep(shared: Record): Promise>> {
    const filenames = Object.keys(shared.data)
    return filenames.map(fn => ({ filename: fn }))
  }
}

// Create a flow for processing a single file
const summarizeFile = new Flow(loadFile)

// Create a batch flow that processes all files in parallel
const summarizeAllFiles = new ParallelBatchFlow(summarizeFile)
await summarizeAllFiles.run(shared)
```

{% endtab %}
{% endtabs %}

## Nested Batch Processing

You can nest a **SequentialBatchFlow** or **ParallelBatchFlow** in another batch flow. For instance:

- **Outer** batch: returns a list of diretory param dicts (e.g., `{"directory": "/pathA"}`, `{"directory": "/pathB"}`, ...).
- **Inner** batch: returning a list of per-file param dicts.

At each level, **BatchFlow** merges its own param dict with the parent’s. By the time you reach the **innermost** node, the final `params` is the merged result of **all** parents in the chain. This way, a nested structure can keep track of the entire context (e.g., directory + file name) at once.

{% tabs %}
{% tab title="Python" %}

```python
class FileBatchFlow(SequentialBatchFlow):
    async def prep(self, shared):
        directory = self.params["directory"]
        # e.g., files = ["file1.txt", "file2.txt", ...]
        files = [f for f in os.listdir(directory) if f.endswith(".txt")]
        return [{"filename": f} for f in files]

class DirectoryBatchFlow(SequentialBatchFlow):
    async def prep(self, shared):
        directories = ["/path/to/dirA", "/path/to/dirB"]
        return [{"directory": d} for d in directories]

# MapSummaries have params like {"directory": "/path/to/dirA", "filename": "file1.txt"}
inner_flow = FileBatchFlow(start=MapSummaries())
outer_flow = DirectoryBatchFlow(start=inner_flow)
await outer_flow.run(shared)
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
class FileBatchFlow extends SequentialBatchFlow {
  async prep(shared: Record): Promise<Array<Record<string, string>>> {
    const directory = this.params.directory
    // In a real implementation, use fs.readdirSync or similar
    const files = ['file1.txt', 'file2.txt']
    return files.map((f) => ({ filename: f }))
  }
}

class DirectoryBatchFlow extends SequentialBatchFlow {
  async prep(shared: Record): Promise<Array<Record<string, string>>> {
    const directories = ['/path/to/dirA', '/path/to/dirB']
    return directories.map((d) => ({ directory: d }))
  }
}

// MapSummaries have params like {"directory": "/path/to/dirA", "filename": "file1.txt"}
const innerFlow = new FileBatchFlow(new MapSummaries())
const outerFlow = new DirectoryBatchFlow(innerFlow)
await outerFlow.run(shared)
```

{% endtab %}
{% endtabs %}

In this nested batch example:

1. The outer flow iterates through directories
2. For each directory, the inner flow processes all files
3. Parameters are merged, so the innermost node receives both directory and filename

## Best Practices

1. **Choose the Right Type**: Use sequential processing when order matters or when managing rate limits; use parallel processing for independent operations
2. **Manage Chunk Size**: Balance between too many small chunks (overhead) and too few large chunks (memory issues)
3. **Error Handling**: Implement proper error handling to prevent one failure from stopping the entire batch
4. **Progress Tracking**: Add logging or progress indicators for long-running batch operations
5. **Resource Management**: Be mindful of memory usage, especially with large datasets
