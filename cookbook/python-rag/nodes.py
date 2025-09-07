from caskada import Node
import numpy as np
import faiss
from utils import call_llm, get_embedding, fixed_size_chunk

# Nodes for the offline flow
class ProcessChunkDocumentsNode(Node):
    async def prep(self, memory):
        return memory.index, memory.item            
    
    async def exec(self, prep_res):
        """Chunk a single text into smaller pieces"""
        return fixed_size_chunk(prep_res[1])

    async def post(self, shared, prep_res, exec_res):
        self.trigger("default", { "index": prep_res[0], "chunks": exec_res})

class EmbedDocumentsNode(Node):
    async def prep(self, memory):
        """Read texts from shared store and return as an iterable"""
        return memory.index, memory.chunks
    
    async def exec(self, prep_res):
        """Embed the list of chunks"""
        all = []
        for chunk in prep_res[1]:
            all.append(get_embedding(chunk))
        return all
    
    async def post(self, shared, prep_res, exec_res_list):
        """Store embeddings in the shared store"""
        print(f"✅ Created {len(exec_res_list)} document embeddings")
        self.trigger("default", { "index": prep_res[0], "item": {
            "embeddings": exec_res_list,
            "chunks": prep_res[1]
        } })

class ReduceChunksAndEmbeddingsNode(Node):
    async def prep(self, memory):
        return memory.output            

    async def post(self, shared, prep_res, exec_res):
        """Store chunked texts in the shared store"""
        # Flatten the list of lists into a single list of chunks
        all_chunks = []
        all_embeddings = []
        for item in prep_res:
            all_chunks.extend(item["chunks"])
            all_embeddings.extend(item["embeddings"])

        # Replace the original texts with the flat list of chunks
        shared["texts"] = all_chunks
        shared["embeddings"] = all_embeddings


class CreateIndexNode(Node):
    async def prep(self, shared):
        """Get embeddings from shared store"""
        return shared["embeddings"]
    
    async def exec(self, embeddings):
        """Create FAISS index and add embeddings"""
        print("🔍 Creating search index...")
        embeddings = np.array(embeddings, dtype=np.float32)
        dimension = embeddings.shape[1]
        
        # Create a flat L2 index
        index = faiss.IndexFlatL2(dimension)
        
        # Add the embeddings to the index
        index.add(embeddings)
        
        return index
    
    async def post(self, shared, prep_res, exec_res):
        """Store the index in shared store"""
        shared["index"] = exec_res
        print(f"✅ Index created with {exec_res.ntotal} vectors")

# Nodes for the online flow
class EmbedQueryNode(Node):
    async def prep(self, shared):
        """Get query from shared store"""
        return shared["query"]
    
    async def exec(self, query):
        """Embed the query"""
        print(f"🔍 Embedding query: {query}")
        query_embedding = get_embedding(query)
        return np.array([query_embedding], dtype=np.float32)
    
    async def post(self, shared, prep_res, exec_res):
        """Store query embedding in shared store"""
        shared["query_embedding"] = exec_res

class RetrieveDocumentNode(Node):
    async def prep(self, shared):
        """Get query embedding, index, and texts from shared store"""
        return shared["query_embedding"], shared["index"], shared["texts"]
    
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
    
    async def post(self, shared, prep_res, exec_res):
        """Store retrieved document in shared store"""
        shared["retrieved_document"] = exec_res
        print(f"📄 Retrieved document (index: {exec_res['index']}, distance: {exec_res['distance']:.4f})")
        print(f"📄 Most relevant text: \"{exec_res['text']}\"")
    
class GenerateAnswerNode(Node):
    async def prep(self, shared):
        """Get query, retrieved document, and any other context needed"""
        return shared["query"], shared["retrieved_document"]
    
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
    
    async def post(self, shared, prep_res, exec_res):
        """Store generated answer in shared store"""
        shared["generated_answer"] = exec_res
        print("\n🤖 Generated Answer:")
        print(exec_res)
