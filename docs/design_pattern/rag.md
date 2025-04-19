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
import os # Assuming file operations
from brainyflow import Node, Flow, Memory, ParallelFlow

# Assume get_embedding, create_index, search_index are defined elsewhere
# async def get_embedding(text: str) -> list[float]: ...
# def create_index(embeddings: list[list[float]]) -> Any: ... # Returns index object
# def search_index(index: Any, query_embedding: list[float], top_k: int) -> tuple[list[list[int]], list[list[float]]]: ...

# --- Stage 1: Offline Indexing Nodes ---

# 1a. Node to trigger chunking for each file
class TriggerChunkingNode(Node):
    async def prep(self, memory: Memory):
        return memory.files or []

    async def exec(self, files: list):
         # Optional: could return file count or validate paths
         return len(files)

    async def post(self, memory: Memory, files: list, file_count: int):
        print(f"Triggering chunking for {file_count} files.")
        memory.all_chunks = [] # Initialize chunk store
        memory.chunk_metadata = [] # Store metadata like source file
        for index, filepath in enumerate(files):
            if os.path.exists(filepath): # Basic check
                 self.trigger('chunk_file', { "filepath": filepath, "file_index": index })
            else:
                 print(f"Warning: File not found {filepath}")
        # Trigger next major step after attempting all files
        self.trigger('embed_chunks')

# 1b. Node to chunk a single file
class ChunkFileNode(Node):
    async def prep(self, memory: Memory):
        # Read filepath from local memory
        return memory.filepath, memory.file_index

    async def exec(self, prep_res):
        filepath, file_index = prep_res
        print(f"Chunking {filepath}")
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
            # Simple fixed-size chunking
            chunks = []
            size = 100
            for i in range(0, len(text), size):
                chunks.append(text[i : i + size])
            return chunks, filepath # Pass filepath for metadata
        except Exception as e:
            print(f"Error chunking {filepath}: {e}")
            return [], filepath # Return empty list on error

    async def post(self, memory: Memory, prep_res, exec_res):
        chunks, filepath = exec_res
        file_index = prep_res[1]
        # Append chunks and their source metadata to global lists
        # Note: If using ParallelFlow, direct append might lead to race conditions.
        # Consider storing per-file results then combining in the next step.
        start_index = len(memory.all_chunks)
        memory.all_chunks.extend(chunks)
        for i, chunk in enumerate(chunks):
             memory.chunk_metadata.append({"source": filepath, "chunk_index_in_file": i, "global_chunk_index": start_index + i})
        # This node doesn't trigger further processing for this specific file branch

# 1c. Node to trigger embedding for each chunk
class TriggerEmbeddingNode(Node):
     async def prep(self, memory: Memory):
         # This node runs after all 'chunk_file' triggers are processed by the Flow
         return memory.all_chunks or []

     async def exec(self, chunks: list):
         return len(chunks)

     async def post(self, memory: Memory, chunks: list, chunk_count: int):
         print(f"Triggering embedding for {chunk_count} chunks.")
         memory.all_embeds = [None] * chunk_count # Pre-allocate list for parallel writes
         for index, chunk in enumerate(chunks):
             # Pass chunk and its global index via forkingData
             self.trigger('embed_chunk', { "chunk": chunk, "global_index": index })
         # Trigger storing index after all embedding triggers are fired
         self.trigger('store_index')

# 1d. Node to embed a single chunk
class EmbedChunkNode(Node):
     async def prep(self, memory: Memory):
         # Read chunk and global index from local memory
         return memory.chunk, memory.global_index

     async def exec(self, prep_res):
         chunk, index = prep_res
         # print(f"Embedding chunk {index}") # Can be noisy
         return await get_embedding(chunk), index # Pass index through

     async def post(self, memory: Memory, prep_res, exec_res):
         embedding, index = exec_res
         # Store embedding at the correct index in the pre-allocated list
         memory.all_embeds[index] = embedding
         # This node doesn't trigger further processing for this chunk branch
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
# 1e. Node to store the final index
class StoreIndexNode(Node):
    async def prep(self, memory: Memory):
        # Read all embeddings from global memory
        # Filter out potential None values if embedding failed for some chunks
        embeddings = [emb for emb in (memory.all_embeds or []) if emb is not None]
        if len(embeddings) != len(memory.all_embeds or []):
             print(f"Warning: Some chunks failed to embed. Indexing {len(embeddings)} embeddings.")
        return embeddings

    async def exec(self, all_embeds: list):
        if not all_embeds:
             print("No embeddings to store.")
             return None
        print(f"Storing index for {len(all_embeds)} embeddings.")
        # Create a vector index (implementation depends on library)
        index = create_index(all_embeds)
        return index

    async def post(self, memory: Memory, prep_res, index):
        # Store the created index in global memory
        memory.index = index
        if index:
             print('Index created and stored.')
        else:
             print('Index creation skipped.')
        # End of offline flow
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
# --- Offline Flow Definition ---
trigger_chunking = TriggerChunkingNode()
chunk_file = ChunkFileNode()
trigger_embedding = TriggerEmbeddingNode()
embed_chunk = EmbedChunkNode()
store_index = StoreIndexNode()

# Define transitions using syntax sugar
trigger_chunking - 'chunk_file' >> chunk_file
trigger_chunking - 'embed_chunks' >> trigger_embedding
trigger_embedding - 'embed_chunk' >> embed_chunk
trigger_embedding - 'store_index' >> store_index

# Use ParallelFlow for potentially faster chunking and embedding
OfflineFlow = ParallelFlow(start=trigger_chunking)
# Or sequential: OfflineFlow = Flow(start=trigger_chunking)
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
# --- Offline Flow Execution ---
async def run_offline():
    # Create dummy files for example
    if not os.path.exists('doc1.txt'): fs.writeFileSync('doc1.txt', 'Alice was beginning to get very tired.')
    if not os.path.exists('doc2.txt'): fs.writeFileSync('doc2.txt', 'The quick brown fox jumps over the lazy dog.')

    initial_memory = {
        "files": ["doc1.txt", "doc2.txt"], # Example file paths
    }
    print('Starting offline indexing flow...')

    await OfflineFlow.run(initial_memory)

    print('Offline indexing complete.')
    # Clean up dummy files
    # os.remove('doc1.txt')
    # os.remove('doc2.txt')
    return initial_memory # Return memory containing index, chunks, embeds

# asyncio.run(run_offline()) # Example call
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
# --- Stage 2: Online Query Nodes ---

# 2a. Embed Query Node
class EmbedQueryNode(Node):
    async def prep(self, memory: Memory):
        return memory.question # Read from memory

    async def exec(self, question):
        print(f"Embedding query: \"{question}\"")
        return await get_embedding(question)

    async def post(self, memory: Memory, prep_res, q_emb):
        memory.q_emb = q_emb # Write to memory
        self.trigger('retrieve_docs')
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
# 2b. Retrieve Docs Node
class RetrieveDocsNode(Node):
    async def prep(self, memory: Memory):
        # Need query embedding, index, and original chunks
        # Also retrieve metadata to know the source
        return memory.q_emb, memory.index, memory.all_chunks, memory.chunk_metadata

    async def exec(self, inputs):
        q_emb, index, chunks, metadata = inputs
        if not q_emb or not index or not chunks:
            raise ValueError("Missing data for retrieval in memory")
        print("Retrieving relevant chunk...")
        # Assuming search_index returns [[ids]], [[distances]]
        I, D = search_index(index, q_emb, top_k=1)
        if not I or not I[0]:
             return "Could not find relevant chunk.", None
        best_global_id = I[0][0]
        if best_global_id >= len(chunks):
             return "Index out of bounds.", None

        relevant_chunk = chunks[best_global_id]
        relevant_metadata = metadata[best_global_id] if metadata and best_global_id < len(metadata) else {}
        return relevant_chunk, relevant_metadata

    async def post(self, memory: Memory, prep_res, exec_res):
        relevant_chunk, relevant_metadata = exec_res
        memory.retrieved_chunk = relevant_chunk # Write to memory
        memory.retrieved_metadata = relevant_metadata # Write metadata too
        print(f"Retrieved chunk: {relevant_chunk[:60]}... (Source: {relevant_metadata.get('source', 'N/A')})")
        self.trigger('generate_answer')
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
# 2c. Generate Answer Node
class GenerateAnswerNode(Node):
    async def prep(self, memory: Memory):
        return memory.question, memory.retrieved_chunk # Read from memory

    async def exec(self, inputs):
        question, chunk = inputs
        if not chunk or chunk == "Could not find relevant chunk.":
             return "Sorry, I couldn't find relevant information to answer the question."
        prompt = f"Using the following context, answer the question.\nContext: {chunk}\nQuestion: {question}\nAnswer:"
        print("Generating final answer...")
        return await call_llm(prompt)

    async def post(self, memory: Memory, prep_res, answer):
        memory.answer = answer # Write to memory
        print("Answer:", answer)
        # End of online flow
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
# --- Online Flow Definition ---
embed_qnode = EmbedQueryNode()
retrieve_node = RetrieveDocsNode()
generate_node = GenerateAnswerNode()

# Define transitions using syntax sugar
embed_qnode - 'retrieve_docs' >> retrieve_node
retrieve_node - 'generate_answer' >> generate_node

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
# --- Online Flow Execution ---
async def run_online(memory_from_offline: dict):
    # Add the user's question to the memory from the offline stage
    memory_from_offline["question"] = "Why do people like cats?"

    print(f"\nStarting online RAG flow for question: \"{memory_from_offline['question']}\"")
    await OnlineFlow.run(memory_from_offline) # Pass memory object
    # final answer in memory_from_offline["answer"]
    print("Final Answer:", memory_from_offline.get("answer", "N/A")) # Read from memory
    return memory_from_offline

# Example usage combining both stages
async def main():
    # Mock external functions if not defined
    # global get_embedding, create_index, search_index, call_llm
    # get_embedding = ...
    # create_index = ...
    # search_index = ...
    # call_llm = ...

    memory_after_offline = await run_offline()
    if memory_after_offline.get("index"): # Only run online if index exists
        await run_online(memory_after_offline)
    else:
        print("Skipping online flow due to missing index.")

if __name__ == "__main__":
    # Note: Ensure dummy files exist or are created before running
    # For simplicity, file creation moved to run_offline
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
