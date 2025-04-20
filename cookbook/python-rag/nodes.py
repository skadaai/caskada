from brainyflow import Node, Flow, Memory, ParallelFlow
import numpy as np
import faiss
from utils import call_llm, get_embedding, get_simple_embedding, fixed_size_chunk

# Nodes for the offline flow
class TriggerChunkingNode(Node):
    async def prep(self, memory: Memory):
        """Read texts from memory"""
        return memory.texts or []

    async def post(self, memory: Memory, texts_to_chunk: list, exec_res):
        print(f"Mapper: Triggering chunking for {len(texts_to_chunk)} documents.")
        memory.chunked_texts = [] # Initialize list for chunks
        memory.remaining_chunks = len(texts_to_chunk) # Add counter
        for index, text in enumerate(texts_to_chunk):
            self.trigger('chunk_document', { "text": text, "index": index })

class ChunkDocumentNode(Node):
    async def prep(self, memory: Memory):
        """Read specific text data from local memory (passed via forkingData)"""
        return memory.text, memory.index

    async def exec(self, prep_res):
        """Chunk a single text into smaller pieces"""
        text, index = prep_res
        print(f"Processor: Chunking document (Index {index})")
        return fixed_size_chunk(text)

    async def post(self, memory: Memory, prep_res, chunks: list):
        text, index = prep_res
        # Store individual chunks in global memory
        memory.chunked_texts.extend(chunks)
        print(f"Processor: Finished chunking document (Index {index})")
        # Decrement counter and trigger next step if this is the last chunk
        memory.remaining_chunks -= 1
        if memory.remaining_chunks == 0:
            print("Processor: All documents chunked, triggering embedding.")
            self.trigger('embed_chunks')

class TriggerEmbeddingNode(Node):
    async def prep(self, memory: Memory):
        """Read chunked texts from memory"""
        return memory.chunked_texts or []

    async def post(self, memory: Memory, chunks_to_embed: list, exec_res):
        print(f"Mapper: Triggering embedding for {len(chunks_to_embed)} chunks.")
        memory.embeddings = [None] * len(chunks_to_embed) # Pre-allocate for parallel
        memory.remaining_embeddings = len(chunks_to_embed) # Add counter
        for index, chunk in enumerate(chunks_to_embed):
            self.trigger('embed_chunk', { "chunk": chunk, "index": index })

class EmbedChunkNode(Node):
    async def prep(self, memory: Memory):
        """Read specific chunk data from local memory (passed via forkingData)"""
        return memory.chunk, memory.index

    async def exec(self, prep_res):
        """Embed a single text"""
        chunk, index = prep_res
        print(f"Processor: Embedding chunk (Index {index})")
        return get_embedding(chunk)

    async def post(self, memory: Memory, prep_res, embedding):
        chunk, index = prep_res
        # Store individual embedding in global memory at the correct index
        memory.embeddings[index] = embedding
        print(f"Processor: Finished embedding chunk (Index {index})")
        # Decrement counter and trigger next step if this is the last embedding
        memory.remaining_embeddings -= 1
        if memory.remaining_embeddings == 0:
            print("Processor: All chunks embedded, triggering index creation.")
            self.trigger('create_index')

class CreateIndexNode(Node):
    async def prep(self, memory: Memory):
        """Get embeddings from memory"""
        return memory.embeddings

    async def exec(self, embeddings):
        """Create FAISS index and add embeddings"""
        print("🔍 Creating search index...")
        embeddings_np = np.array(embeddings, dtype=np.float32)
        dimension = embeddings_np.shape[1]

        # Create a flat L2 index
        index = faiss.IndexFlatL2(dimension)

        # Add the embeddings to the index
        index.add(embeddings_np)

        return index

    async def post(self, memory: Memory, prep_res, index):
        """Store the index in memory"""
        memory.index = index
        print(f"✅ Index created with {index.ntotal} vectors")
        self.trigger("default")

# Nodes for the online flow
class EmbedQueryNode(Node):
    async def prep(self, memory: Memory):
        """Get query from memory"""
        return memory.query

    async def exec(self, query):
        """Embed the query"""
        print(f"🔍 Embedding query: {query}")
        query_embedding = get_embedding(query)
        return np.array([query_embedding], dtype=np.float32)

    async def post(self, memory: Memory, prep_res, query_embedding):
        """Store query embedding in memory"""
        memory.query_embedding = query_embedding
        self.trigger("default")

class RetrieveDocumentNode(Node):
    async def prep(self, memory: Memory):
        """Get query embedding, index, and texts from memory"""
        return memory.query_embedding, memory.index, memory.chunked_texts

    async def exec(self, inputs):
        """Search the index for similar documents"""
        print("🔎 Searching for relevant documents...")
        query_embedding, index, texts = inputs

        # Search for the most similar document
        distances, indices = index.search(query_embedding, k=1)

        # Get the index of the most similar document
        best_idx = indices[0][0]
        distance = distances[0][0]

        # Get the corresponding text
        most_relevant_text = texts[best_idx]

        return {
            "text": most_relevant_text,
            "index": best_idx,
            "distance": distance
        }

    async def post(self, memory: Memory, prep_res, retrieved_document):
        """Store retrieved document in memory"""
        memory.retrieved_document = retrieved_document
        print(f"📄 Retrieved document (index: {retrieved_document['index']}, distance: {retrieved_document['distance']:.4f})")
        print(f"📄 Most relevant text: \"{retrieved_document['text']}\"")
        self.trigger("default")

class GenerateAnswerNode(Node):
    async def prep(self, memory: Memory):
        """Get query, retrieved document, and any other context needed"""
        return memory.query, memory.retrieved_document

    async def exec(self, inputs):
        """Generate an answer using the LLM"""
        query, retrieved_doc = inputs

        prompt = f"""
Briefly answer the following question based on the context provided:
Question: {query}
Context: {retrieved_doc['text']}
Answer:
"""

        answer = call_llm(prompt)
        return answer

    async def post(self, memory: Memory, prep_res, generated_answer):
        """Store generated answer in memory"""
        memory.generated_answer = generated_answer
        print("\n🤖 Generated Answer:")
        print(generated_answer)
        self.trigger("default")
