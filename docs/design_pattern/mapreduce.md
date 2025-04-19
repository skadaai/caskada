# Map Reduce

MapReduce is a design pattern suitable when you need to process multiple pieces of data (e.g., files, records) independently and then combine the results.

<div align="center">
  <img src="https://github.com/zvictor/brainyflow/raw/main/.github/media/mapreduce.png?raw=true" width="400"/>
</div>

In BrainyFlow, this pattern is typically implemented using:

1.  **Map Phase:** A "Mapper" node triggers multiple instances of a "Processor" node, one for each piece of data. It uses `trigger` with `forkingData` to pass the specific data item to each processor via its local memory. Using `ParallelFlow` here allows processors to run concurrently.
2.  **Reduce Phase:** A "Reducer" node runs after the map phase. It reads the individual results (accumulated in the global memory by the processor nodes) and aggregates them into a final output.

### Example: Document Summarization

{% tabs %}
{% tab title="Python" %}

```python
import asyncio
from brainyflow import Node, Flow, Memory, ParallelFlow

# Assume call_llm is defined elsewhere
# async def call_llm(prompt: str) -> str: ...

# 1. Mapper Node: Triggers processing for each file
class TriggerSummariesNode(Node):
    async def prep(self, memory: Memory):
        # Get file data from global memory
        files_dict = memory.files or {}
        return list(files_dict.items()) # [("file1.txt", "content1"), ...]

    async def exec(self, files: list):
        # No main computation needed here, just return the count for info
        return len(files)

    async def post(self, memory: Memory, files_to_process: list, file_count: int):
        print(f"Mapper: Triggering summary for {file_count} files.")
        # Initialize results list in global memory (pre-allocate for parallel writes)
        memory.file_summaries = [None] * file_count
        # Trigger a 'summarize_file' action for each file
        for index, (filename, content) in enumerate(files_to_process):
            self.trigger('summarize_file', { "filename": filename, "content": content, "index": index })
        # After triggering all files, trigger the 'combine' step
        self.trigger('combine_summaries')

# 2. Processor Node: Summarizes a single file
class SummarizeFileNode(Node):
    async def prep(self, memory: Memory):
        # Read specific file data from local memory (passed via forkingData)
        return memory.filename, memory.content, memory.index

    async def exec(self, prep_res):
        filename, content, index = prep_res
        # Summarize the content
        print(f"Processor: Summarizing {filename} (Index {index})")
        return await call_llm(f"Summarize this:\n{content}")

    async def post(self, memory: Memory, prep_res, summary: str):
        filename, content, index = prep_res
        # Store individual summary in global memory at the correct index
        memory.file_summaries[index] = { "filename": filename, "summary": summary }
        print(f"Processor: Finished {filename} (Index {index})")
        # This node doesn't trigger anything further in this branch

# 3. Reducer Node: Combines individual summaries
class CombineSummariesNode(Node):
    async def prep(self, memory: Memory):
        # Read the array of individual summaries (filter out None if any failed)
        summaries = [s for s in (memory.file_summaries or []) if s is not None]
        return summaries

    async def exec(self, summaries: list):
        print(f"Reducer: Combining {len(summaries)} summaries.")
        if not summaries:
            return "No summaries to combine."
        # Format summaries for the final prompt
        combined_text = "\n\n---\n\n".join([f"{s['filename']}:\n{s['summary']}" for s in summaries])
        return await call_llm(f"Combine these summaries into one final summary:\n{combined_text}")

    async def post(self, memory: Memory, prep_res, final_summary: str):
        # Store the final combined summary
        memory.final_summary = final_summary
        print("Reducer: Final summary generated.")
        # No trigger needed if this is the end

# --- Flow Definition ---
trigger_node = TriggerSummariesNode()
processor_node = SummarizeFileNode()
reducer_node = CombineSummariesNode()

# Define transitions
trigger_node - 'summarize_file' >> processor_node # Map step
trigger_node - 'combine_summaries' >> reducer_node # Reduce step

# Use ParallelFlow for potentially faster summarization
map_reduce_flow = ParallelFlow(start=trigger_node)
# If order of summaries matters strictly, use: map_reduce_flow = Flow(trigger_node);

# --- Execution ---
async def main():
    memory = {
        "files": {
            "file1.txt": "Alice was beginning to get very tired of sitting by her sister...",
            "file2.txt": "The quick brown fox jumps over the lazy dog.",
            "file3.txt": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        }
    }
    await map_reduce_flow.run(memory) # Pass memory object
    print('\n--- MapReduce Complete ---')
    print("Individual Summaries:", memory.get("file_summaries"))
    print("\nFinal Summary:\n", memory.get("final_summary"))

if __name__ == "__main__":
    asyncio.run(main())
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
import { Flow, Memory, Node, ParallelFlow } from 'brainyflow'

// Assume callLLM is defined elsewhere
declare function callLLM(prompt: string): Promise<string>

// 1. Mapper Node: Triggers processing for each file
class TriggerSummariesNode extends Node {
  async prep(memory: Memory): Promise<[string, string][]> {
    // Get file data from global memory
    const filesDict = memory.files ?? {}
    return Object.entries(filesDict) // [["file1.txt", "content1"], ...]
  }

  async exec(files: [string, string][]): Promise<number> {
    // No main computation needed here, just return the count for info
    return files.length
  }

  async post(memory: Memory, filesToProcess: [string, string][], fileCount: number): Promise<void> {
    console.log(`Mapper: Triggering summary for ${fileCount} files.`)
    // Initialize results array in global memory
    memory.file_summaries = []
    // Trigger a 'summarize_file' action for each file
    filesToProcess.forEach(([filename, content], index) => {
      this.trigger('summarize_file', { filename, content, index })
    })
    // After triggering all files, trigger the 'combine' step
    this.trigger('combine_summaries')
  }
}

// 2. Processor Node: Summarizes a single file
class SummarizeFileNode extends Node {
  async prep(memory: Memory): Promise<{ filename: string; content: string; index: number }> {
    // Read specific file data from local memory (passed via forkingData)
    return { filename: memory.filename, content: memory.content, index: memory.index }
  }

  async exec(fileData: { filename: string; content: string; index: number }): Promise<string> {
    // Summarize the content
    console.log(`Processor: Summarizing ${fileData.filename} (Index ${fileData.index})`)
    return await callLLM(`Summarize this:\n${fileData.content}`)
  }

  async post(
    memory: Memory,
    prepRes: { index: number; filename: string },
    summary: string,
  ): Promise<void> {
    // Store individual summary in global memory at the correct index
    // Note: Direct array index assignment might cause issues with ParallelFlow if order matters
    // A safer approach might be to push {filename, summary} and sort later, or use an object.
    memory.file_summaries[prepRes.index] = { filename: prepRes.filename, summary }
    console.log(`Processor: Finished ${prepRes.filename} (Index ${prepRes.index})`)
    // This node doesn't trigger anything further in this branch
  }
}

// 3. Reducer Node: Combines individual summaries
class CombineSummariesNode extends Node {
  async prep(memory: Memory): Promise<any[]> {
    // Read the array of individual summaries
    return memory.file_summaries ?? []
  }

  async exec(summaries: { filename: string; summary: string }[]): Promise<string> {
    console.log(`Reducer: Combining ${summaries.length} summaries.`)
    if (!summaries || summaries.length === 0) {
      return 'No summaries to combine.'
    }
    // Format summaries for the final prompt
    const combinedText = summaries.map((s) => `${s.filename}:\n${s.summary}`).join('\n\n---\n\n')
    return await callLLM(`Combine these summaries into one final summary:\n${combinedText}`)
  }

  async post(memory: Memory, prepRes: any, finalSummary: string): Promise<void> {
    // Store the final combined summary
    memory.final_summary = finalSummary
    console.log('Reducer: Final summary generated.')
  }
}

// --- Flow Definition ---
const triggerNode = new TriggerSummariesNode()
const processorNode = new SummarizeFileNode()
const reducerNode = new CombineSummariesNode()

// Define transitions
triggerNode.on('summarize_file', processorNode) // Map step
triggerNode.on('combine_summaries', reducerNode) // Reduce step (runs after all triggers are processed by the flow runner)

// Use ParallelFlow for potentially faster summarization
const mapReduceFlow = new ParallelFlow(triggerNode)
// If order of summaries matters strictly, use: const mapReduceFlow = new Flow(triggerNode);

// --- Execution ---
async function main() {
  const memory = {
    files: {
      'file1.txt': 'Alice was beginning to get very tired of sitting by her sister...',
      'file2.txt': 'The quick brown fox jumps over the lazy dog.',
      'file3.txt': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
    },
  }
  await mapReduceFlow.run(memory)
  console.log('\n--- MapReduce Complete ---')
  console.log('Individual Summaries:', memory.file_summaries)
  console.log('\nFinal Summary:\n', memory.final_summary)
}

main().catch(console.error)
```

{% endtab %}
{% endtabs %}
