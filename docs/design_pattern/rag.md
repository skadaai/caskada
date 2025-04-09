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
class ChunkDocs extends SequentialBatchNode {
  async prep(shared: any): Promise<string[]> {
    // A list of file paths in shared["files"]. We process each file.
    return shared['files']
  }

  async exec(filepath: string): Promise<string[]> {
    // read file content. In real usage, do error handling.
    const text = fs.readFileSync(filepath, 'utf-8')
    // chunk by 100 chars each
    const chunks: string[] = []
    const size = 100
    for (let i = 0; i < text.length; i += size) {
      chunks.push(text.slice(i, i + size))
    }
    return chunks
  }

  async post(shared: any, prepRes: string[], execResList: string[][]): Promise<void> {
    // execResList is a list of chunk-lists, one per file.
    // flatten them all into a single list of chunks.
    const allChunks: string[] = []
    for (const chunkList of execResList) {
      allChunks.push(...chunkList)
    }
    shared['all_chunks'] = allChunks
  }
}
```

{% endtab %}
{% endtabs %}

{% tabs %}
{% tab title="Python" %}

```python
class EmbedDocs(SequentialBatchNode):
    async def prep(self, shared):
        return shared["all_chunks"]

    async def exec(self, chunk):
        return get_embedding(chunk)

    async def post(self, shared, prep_res, exec_res_list):
        # Store the list of embeddings.
        shared["all_embeds"] = exec_res_list
        print(f"Total embeddings: {len(exec_res_list)}")
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
class EmbedDocs extends SequentialBatchNode {
  async prep(shared: any): Promise<string[]> {
    return shared['all_chunks']
  }

  async exec(chunk: string): Promise<number[]> {
    return await getEmbedding(chunk)
  }

  async post(shared: any, prepRes: string[], execResList: number[][]): Promise<void> {
    // Store the list of embeddings.
    shared['all_embeds'] = execResList
    console.log(`Total embeddings: ${execResList.length}`)
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
class StoreIndex extends Node {
  async prep(shared: any): Promise<number[][]> {
    // We'll read all embeds from shared.
    return shared['all_embeds']
  }

  async exec(allEmbeds: number[][]): Promise<any> {
    // Create a vector index (faiss or other DB in real usage).
    const index = createIndex(allEmbeds)
    return index
  }

  async post(shared: any, prepRes: number[][], index: any): Promise<void> {
    shared['index'] = index
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
// Wire them in sequence
const chunkNode = new ChunkDocs()
const embedNode = new EmbedDocs()
const storeNode = new StoreIndex()

chunkNode.next(embedNode).next(storeNode)

const OfflineFlow = new Flow(chunkNode)
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
const shared = {
  files: ['doc1.txt', 'doc2.txt'], // any text files
}
await OfflineFlow.run(shared)
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
class EmbedQuery extends Node {
  async prep(shared: any): Promise<string> {
    return shared['question']
  }

  async exec(question: string): Promise<number[]> {
    return await getEmbedding(question)
  }

  async post(shared: any, prepRes: string, qEmb: number[]): Promise<void> {
    shared['q_emb'] = qEmb
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
class RetrieveDocs extends Node {
  async prep(shared: any): Promise<[number[], any, string[]]> {
    // We'll need the query embedding, plus the offline index/chunks
    return [shared['q_emb'], shared['index'], shared['all_chunks']]
  }

  async exec(inputs: [number[], any, string[]]): Promise<string> {
    const [qEmb, index, chunks] = inputs
    const [I, D] = searchIndex(index, qEmb, 1)
    const bestId = I[0][0]
    const relevantChunk = chunks[bestId]
    return relevantChunk
  }

  async post(
    shared: any,
    prepRes: [number[], any, string[]],
    relevantChunk: string,
  ): Promise<void> {
    shared['retrieved_chunk'] = relevantChunk
    console.log(`Retrieved chunk: ${relevantChunk.slice(0, 60)}...`)
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
class GenerateAnswer extends Node {
  async prep(shared: any): Promise<[string, string]> {
    return [shared['question'], shared['retrieved_chunk']]
  }

  async exec(inputs: [string, string]): Promise<string> {
    const [question, chunk] = inputs
    const prompt = `Question: ${question}\nContext: ${chunk}\nAnswer:`
    return await callLLM(prompt)
  }

  async post(shared: any, prepRes: [string, string], answer: string): Promise<void> {
    shared['answer'] = answer
    console.log(`Answer: ${answer}`)
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
const embedQNode = new EmbedQuery()
const retrieveNode = new RetrieveDocs()
const generateNode = new GenerateAnswer()

embedQNode.next(retrieveNode).next(generateNode)
const OnlineFlow = new Flow(embedQNode)
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
async function runOnline(sharedFromOffline: any): Promise<any> {
  // Suppose we already ran OfflineFlow (runOffline) and have:
  // sharedFromOffline["all_chunks"], sharedFromOffline["index"], etc.
  sharedFromOffline['question'] = 'Why do people like cats?'

  await OnlineFlow.run(sharedFromOffline)
  // final answer in sharedFromOffline["answer"]
  console.log(`Final Answer: ${sharedFromOffline['answer']}`)
  return sharedFromOffline
}

// Example usage combining both stages
async function main() {
  const offlineShared = await runOffline()
  await runOnline(offlineShared)
}

main().catch(console.error) // Execute async main function
```

{% endtab %}
{% endtabs %}
