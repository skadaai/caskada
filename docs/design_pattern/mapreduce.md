---
title: 'Map Reduce'
---

# Map Reduce

MapReduce is a design pattern suitable when you have either:

- Large input data (e.g., multiple files to process), or
- Large output data (e.g., multiple forms to fill)

and there is a logical way to break the task into smaller, ideally independent parts.

<div align="center">
  <img src="https://github.com/zvictor/brainyflow/raw/main/.github/media/mapreduce.png?raw=true" width="400"/>
</div>

You first break down the task using [BatchNode](../core_abstraction/batch.md) in the map phase, followed by aggregation in the reduce phase.

### Example: Document Summarization

{% tabs %}
{% tab title="Python" %}

```python
import asyncio
from brainyflow import Node, SequentialBatchNode

class SummarizeAllFiles(SequentialBatchNode):
    async def prep(self, shared):
        files_dict = shared["files"]  # e.g. 10 files
        return list(files_dict.items())  # [("file1.txt", "aaa..."), ("file2.txt", "bbb..."), ...]

    async def exec(self, one_file):
        filename, file_content = one_file
        summary_text = call_llm(f"Summarize the following file:\n{file_content}")
        return (filename, summary_text)

    async def post(self, shared, prep_res, exec_res_list):
        shared["file_summaries"] = dict(exec_res_list)

class CombineSummaries(Node):
    async def prep(self, shared):
        return shared["file_summaries"]

    async def exec(self, file_summaries):
        # format as: "File1: summary\nFile2: summary...\n"
        text_list = []
        for fname, summ in file_summaries.items():
            text_list.append(f"{fname} summary:\n{summ}\n")
        big_text = "\n---\n".join(text_list)

        return call_llm(f"Combine these file summaries into one final summary:\n{big_text}")

    async def post(self, shared, prep_res, final_summary):
        shared["all_files_summary"] = final_summary

batch_node = SummarizeAllFiles()
combine_node = CombineSummaries()
batch_node >> combine_node

flow = Flow(start=batch_node)

async def main():
    shared = {
        "files": {
            "file1.txt": "Alice was beginning to get very tired of sitting by her sister...",
            "file2.txt": "Some other interesting text ...",
            # ...
        }
    }
    await flow.run(shared)
    print("Individual Summaries:", shared["file_summaries"])
    print("\nFinal Summary:\n", shared["all_files_summary"])

if __name__ == "__main__":
    asyncio.run(main())
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
class SummarizeAllFiles extends SequentialBatchNode {
  async prep(shared: any): Promise<[string, string][]> {
    const filesDict = shared.files // e.g. 10 files
    return Object.entries(filesDict) // [["file1.txt", "aaa..."], ["file2.txt", "bbb..."], ...]
  }

  async exec(oneFile: [string, string]): Promise<[string, string]> {
    const [filename, fileContent] = oneFile
    const summaryText = await callLLM(`Summarize the following file:\n${fileContent}`)
    return [filename, summaryText]
  }

  async post(shared: any, prepRes: any, execResList: [string, string][]): Promise<void> {
    shared.file_summaries = Object.fromEntries(execResList)
  }
}

class CombineSummaries extends Node {
  async prep(shared: any): Promise<Record<string, string>> {
    return shared.file_summaries
  }

  async exec(fileSummaries: Record<string, string>): Promise<string> {
    // format as: "File1: summary\nFile2: summary...\n"
    const textList: string[] = []
    for (const [fname, summ] of Object.entries(fileSummaries)) {
      textList.push(`${fname} summary:\n${summ}\n`)
    }
    const bigText = textList.join('\n---\n')

    return await callLLM(`Combine these file summaries into one final summary:\n${bigText}`)
  }

  async post(shared: any, prepRes: any, finalSummary: string): Promise<void> {
    shared.all_files_summary = finalSummary
  }
}

const batchNode = new SummarizeAllFiles()
const combineNode = new CombineSummaries()
batchNode.next(combineNode)

const flow = new Flow(batchNode)

async function main() {
  const shared = {
    files: {
      'file1.txt': 'Alice was beginning to get very tired of sitting by her sister...',
      'file2.txt': 'Some other interesting text ...',
      // ...
    },
  }
  await flow.run(shared)
  console.log('Individual Summaries:', shared.file_summaries)
  console.log('\nFinal Summary:\n', shared.all_files_summary)
}

main().catch(console.error)
```

{% endtab %}
{% endtabs %}
