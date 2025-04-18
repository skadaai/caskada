---
title: 'RAG'
---

# RAG (Retrieval Augmented Generation)

For certain LLM tasks like answering questions, providing relevant context is essential. One common architecture is a **two-stage** RAG pipeline:

<div align="center">
  <img src="https://github.com/zvictor/brainyflow/raw/main/.github/media/rag.png?raw=true" width="400"/>
</div>

1. **Offline stage**: Preprocess and index documents ("building the index").
2. **Online stage**: Given a question, generate answers by retrieving the most relevant context.

---

## Stage 1: Offline Indexing

We create three Nodes:

1. `ChunkDocs` – [chunks](../utility_function/chunking.md) raw text.
2. `EmbedDocs` – [embeds](../utility_function/embedding.md) each chunk.
3. `StoreIndex` – stores embeddings into a [vector database](../utility_function/vector.md).

{% tabs %}
{% tab title="Python" %}

```python
import asyncio
from brainyflow import Node, Flow, SequentialBatchNode

class ChunkDocs(SequentialBatchNode):
    async def prep(self, shared):
        # A list of file paths in shared["files"]. We process each file.
        return shared["files"]

    async def exec(self, filepath):
        # read file content. In real usage, do error handling.
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
        # chunk by 100 chars each
        chunks = []
        size = 100
        for i in range(0, len(text), size):
            chunks.append(text[i : i + size])
        return chunks

    async def post(self, shared, prep_res, exec_res_list):
        # exec_res_list is a list of chunk-lists, one per file.
        # flatten them all into a single list of chunks.
        all_chunks = []
        for chunk_list in exec_res_list:
            all_chunks.extend(chunk_list)
        shared["all_chunks"] = all_chunks
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
import * as fs from 'fs'
import { Flow, Memory, Node, ParallelFlow } from 'brainyflow'

// Assume getEmbedding and createIndex/searchIndex are defined elsewhere
declare function getEmbedding(text: string): Promise<number[]>
declare function createIndex(embeddings: number[][]): any // Returns index object
declare function searchIndex(
  index: any,
  queryEmbedding: number[],
  topK: number,
): [number[][], number[][]] // Returns [[ids]], [[distances]]

// --- Stage 1: Offline Indexing Nodes ---

// 1a. Node to trigger chunking for each file
class TriggerChunkingNode extends Node {
  async prep(memory: Memory): Promise<string[]> {
    return memory.files ?? [] // Expects memory.files = ['doc1.txt', ...]
  }
  async exec(files: string[]): Promise<number> {
    return files.length
  }
  async post(memory: Memory, prepRes: string[], fileCount: number): Promise<void> {
    console.log(`Triggering chunking for ${fileCount} files.`)
    memory.all_chunks = [] // Initialize chunk store
    ;(prepRes as string[]).forEach((filepath, index) => {
      this.trigger('chunk_file', { filepath, index }) // Pass filepath via local memory
    })
    this.trigger('embed_chunks') // Trigger embedding after all files are processed
  }
}

// 1b. Node to chunk a single file
class ChunkFileNode extends Node {
  async prep(memory: Memory): Promise<{ filepath: string; index: number }> {
    return { filepath: memory.filepath, index: memory.index } // Read from local memory
  }
  async exec(prepRes: { filepath: string; index: number }): Promise<string[]> {
    console.log(`Chunking ${prepRes.filepath}`)
    const text = fs.readFileSync(prepRes.filepath, 'utf-8')
    const chunks: string[] = []
    const size = 100 // Simple fixed-size chunking
    for (let i = 0; i < text.length; i += size) {
      chunks.push(text.slice(i, i + size))
    }
    return chunks
  }
  async post(memory: Memory, prepRes: { index: number }, chunks: string[]): Promise<void> {
    // Add chunks to the global list (careful with concurrency if using ParallelFlow)
    // A safer parallel approach might store chunks per file then combine later.
    memory.all_chunks.push(...chunks)
  }
}

// 1c. Node to trigger embedding for each chunk
class TriggerEmbeddingNode extends Node {
  async prep(memory: Memory): Promise<string[]> {
    return memory.all_chunks ?? []
  }
  async exec(chunks: string[]): Promise<number> {
    return chunks.length
  }
  async post(memory: Memory, prepRes: string[], chunkCount: number): Promise<void> {
    console.log(`Triggering embedding for ${chunkCount} chunks.`)
    memory.all_embeds = [] // Initialize embedding store
    ;(prepRes as string[]).forEach((chunk, index) => {
      this.trigger('embed_chunk', { chunk, index })
    })
    this.trigger('store_index') // Trigger storing after all chunks processed
  }
}

// 1d. Node to embed a single chunk
class EmbedChunkNode extends Node {
  async prep(memory: Memory): Promise<{ chunk: string; index: number }> {
    return { chunk: memory.chunk, index: memory.index } // Read from local memory
  }
  async exec(prepRes: { chunk: string; index: number }): Promise<number[]> {
    console.log(`Embedding chunk ${prepRes.index}`)
    return await getEmbedding(prepRes.chunk)
  }
  async post(memory: Memory, prepRes: { index: number }, embedding: number[]): Promise<void> {
    // Store embedding in global list (careful with concurrency)
    memory.all_embeds[prepRes.index] = embedding
  }
}
```

{% endtab %}
{% endtabs %}

{% tabs %}
{% tab title="Python" %}

```python
class StoreIndex(Node):
    async def prep(self, shared):
        # We'll read all embeds from shared.
        return shared["all_embeds"]

    async def exec(self, all_embeds):
        # Create a vector index (faiss or other DB in real usage).
        index = create_index(all_embeds)
        return index

    async def post(self, shared, prep_res, index):
        shared["index"] = index
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
// 1e. Node to store the final index
class StoreIndexNode extends Node {
  async prep(memory: Memory): Promise<number[][]> {
    // Read all embeddings from global memory
    return memory.all_embeds ?? []
  }

  async exec(allEmbeds: number[][]): Promise<any> {
    console.log(`Storing index for ${allEmbeds.length} embeddings.`)
    // Create a vector index (implementation depends on library)
    const index = createIndex(allEmbeds)
    return index
  }

  async post(memory: Memory, prepRes: any, index: any): Promise<void> {
    // Store the created index in global memory
    memory.index = index
    console.log('Index created and stored.')
  }
}
```

{% endtab %}
{% endtabs %}

{% tabs %}
{% tab title="Python" %}

```python
# Wire them in sequence
chunk_node = ChunkDocs()
embed_node = EmbedDocs()
store_node = StoreIndex()

chunk_node >> embed_node >> store_node

OfflineFlow = Flow(start=chunk_node)
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
// --- Offline Flow Definition ---
const triggerChunking = new TriggerChunkingNode()
const chunkFile = new ChunkFileNode()
const triggerEmbedding = new TriggerEmbeddingNode()
const embedChunk = new EmbedChunkNode()
const storeIndex = new StoreIndexNode()

// Define transitions
triggerChunking.on('chunk_file', chunkFile)
triggerChunking.on('embed_chunks', triggerEmbedding)
triggerEmbedding.on('embed_chunk', embedChunk)
triggerEmbedding.on('store_index', storeIndex)

// Use ParallelFlow for chunking and embedding if desired
const OfflineFlow = new ParallelFlow(triggerChunking)
// Or sequential: const OfflineFlow = new Flow(triggerChunking);
```

{% endtab %}
{% endtabs %}

Usage example:

{% tabs %}
{% tab title="Python" %}

```python
shared = {
    "files": ["doc1.txt", "doc2.txt"],  # any text files
}
await OfflineFlow.run(shared)
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
// --- Offline Flow Execution ---
async function runOffline() {
  const initialMemory = {
    files: ['doc1.txt', 'doc2.txt'], // Example file paths
  }
  console.log('Starting offline indexing flow...')
  // Create dummy files for example
  fs.writeFileSync('doc1.txt', 'Alice was beginning to get very tired.')
  fs.writeFileSync('doc2.txt', 'The quick brown fox jumps over the lazy dog.')

  await OfflineFlow.run(initialMemory)
  console.log('Offline indexing complete.')
  // Clean up dummy files
  fs.unlinkSync('doc1.txt')
  fs.unlinkSync('doc2.txt')
  return initialMemory // Return memory containing index, chunks, embeds
}
// runOffline(); // Example call
```

{% endtab %}
{% endtabs %}

---

## Stage 2: Online Query & Answer

We have 3 nodes:

1. `EmbedQuery` – embeds the user’s question.
2. `RetrieveDocs` – retrieves top chunk from the index.
3. `GenerateAnswer` – calls the LLM with the question + chunk to produce the final answer.

{% tabs %}
{% tab title="Python" %}

```python
class EmbedQuery(Node):
    async def prep(self, shared):
        return shared["question"]

    async def exec(self, question):
        return get_embedding(question)

    async def post(self, shared, prep_res, q_emb):
        shared["q_emb"] = q_emb
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
// --- Stage 2: Online Query Nodes ---

// 2a. Embed Query Node
class EmbedQueryNode extends Node {
  async prep(memory: Memory): Promise<string> {
    return memory.question // Expects question in global memory
  }
  async exec(question: string): Promise<number[]> {
    console.log(`Embedding query: "${question}"`)
    return await getEmbedding(question)
  }
  async post(memory: Memory, prepRes: any, qEmb: number[]): Promise<void> {
    memory.q_emb = qEmb // Store query embedding
    this.trigger('retrieve_docs')
  }
}
```

{% endtab %}
{% endtabs %}

{% tabs %}
{% tab title="Python" %}

```python
class RetrieveDocs(Node):
    async def prep(self, shared):
        # We'll need the query embedding, plus the offline index/chunks
        return shared["q_emb"], shared["index"], shared["all_chunks"]

    async def exec(self, inputs):
        q_emb, index, chunks = inputs
        I, D = search_index(index, q_emb, top_k=1)
        best_id = I[0][0]
        relevant_chunk = chunks[best_id]
        return relevant_chunk

    async def post(self, shared, prep_res, relevant_chunk):
        shared["retrieved_chunk"] = relevant_chunk
        print("Retrieved chunk:", relevant_chunk[:60], "...")
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
// 2b. Retrieve Docs Node
class RetrieveDocsNode extends Node {
  async prep(memory: Memory): Promise<{ qEmb: number[]; index: any; chunks: string[] }> {
    // Need query embedding, index, and original chunks
    return { qEmb: memory.q_emb, index: memory.index, chunks: memory.all_chunks }
  }
  async exec(prepRes: { qEmb: number[]; index: any; chunks: string[] }): Promise<string> {
    const { qEmb, index, chunks } = prepRes
    if (!qEmb || !index || !chunks) {
      throw new Error('Missing data for retrieval')
    }
    console.log('Retrieving relevant chunk...')
    const [I, D] = searchIndex(index, qEmb, 1) // Find top 1 chunk
    const bestId = I?.[0]?.[0]
    if (bestId === undefined || bestId >= chunks.length) {
      return 'Could not find relevant chunk.'
    }
    const relevantChunk = chunks[bestId]
    return relevantChunk
  }
  async post(memory: Memory, prepRes: any, relevantChunk: string): Promise<void> {
    memory.retrieved_chunk = relevantChunk
    console.log(`Retrieved chunk: ${relevantChunk.slice(0, 60)}...`)
    this.trigger('generate_answer')
  }
}
```

{% endtab %}
{% endtabs %}

{% tabs %}
{% tab title="Python" %}

```python
class GenerateAnswer(Node):
    async def prep(self, shared):
        return shared["question"], shared["retrieved_chunk"]

    async def exec(self, inputs):
        question, chunk = inputs
        prompt = f"Question: {question}\nContext: {chunk}\nAnswer:"
        return call_llm(prompt)

    async def post(self, shared, prep_res, answer):
        shared["answer"] = answer
        print("Answer:", answer)
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
// 2c. Generate Answer Node
class GenerateAnswerNode extends Node {
  async prep(memory: Memory): Promise<{ question: string; chunk: string }> {
    return { question: memory.question, chunk: memory.retrieved_chunk }
  }
  async exec(prepRes: { question: string; chunk: string }): Promise<string> {
    const { question, chunk } = prepRes
    const prompt = `Using the following context, answer the question.
Context: ${chunk}
Question: ${question}
Answer:`
    console.log('Generating final answer...')
    return await callLLM(prompt)
  }
  async post(memory: Memory, prepRes: any, answer: string): Promise<void> {
    memory.answer = answer // Store final answer
    console.log(`Answer: ${answer}`)
    // End of flow
  }
}
```

{% endtab %}
{% endtabs %}

{% tabs %}
{% tab title="Python" %}

```python
embed_qnode = EmbedQuery()
retrieve_node = RetrieveDocs()
generate_node = GenerateAnswer()

embed_qnode >> retrieve_node >> generate_node
OnlineFlow = Flow(start=embed_qnode)
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
// --- Online Flow Definition ---
const embedQueryNode = new EmbedQueryNode()
const retrieveDocsNode = new RetrieveDocsNode()
const generateAnswerNode = new GenerateAnswerNode()

// Define transitions
embedQueryNode.on('retrieve_docs', retrieveDocsNode)
retrieveDocsNode.on('generate_answer', generateAnswerNode)

const OnlineFlow = new Flow(embedQueryNode)
```

{% endtab %}
{% endtabs %}

Usage example:

{% tabs %}
{% tab title="Python" %}

```python
async def run_online(shared_from_offline):
    # Suppose we already ran OfflineFlow (run_offline) and have:
    # shared_from_offline["all_chunks"], shared_from_offline["index"], etc.
    shared_from_offline["question"] = "Why do people like cats?"

    await OnlineFlow.run(shared_from_offline)
    # final answer in shared_from_offline["answer"]
    print("Final Answer:", shared_from_offline["answer"])
    return shared_from_offline

# Example usage combining both stages
async def main():
    offline_shared = await run_offline()
    await run_online(offline_shared)

if __name__ == "__main__":
    asyncio.run(main())
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
// --- Online Flow Execution ---
async function runOnline(memoryFromOffline: any) {
  // Add the user's question to the memory from the offline stage
  memoryFromOffline.question = 'Why do people like cats?'

  console.log(`\nStarting online RAG flow for question: "${memoryFromOffline.question}"`)
  await OnlineFlow.run(memoryFromOffline)
  console.log('Online RAG complete.')
  return memoryFromOffline
}

// --- Combined Example ---
async function runFullRAG() {
  // Mock external functions for example
  globalThis.getEmbedding = async (text: string) => Array(5).fill(Math.random())
  globalThis.createIndex = (embeds: number[][]) => ({
    search: (q: number[], k: number) => [[Math.floor(Math.random() * embeds.length)]],
  }) // Mock index
  globalThis.searchIndex = (index: any, q: number[], k: number) => index.search(q, k)
  globalThis.callLLM = async (prompt: string) => `Mock LLM answer for: ${prompt.split('\n')[1]}`

  const memoryAfterOffline = await runOffline()
  const finalMemory = await runOnline(memoryAfterOffline)

  console.log('\n--- Full RAG Result ---')
  console.log('Final Answer:', finalMemory.answer)
}

runFullRAG().catch(console.error)
```

{% endtab %}
{% endtabs %}
