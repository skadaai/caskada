from caskada import Node
from tools.embeddings import get_embedding

class EmbeddingNode(Node):
    """Node for getting embeddings from OpenAI API"""
    
    async def prep(self, shared):
        # Get text from shared store
        return getattr(shared, "text", "")
        
    async def exec(self, text):
        # Get embedding using tool function
        return get_embedding(text)
        
    async def post(self, shared, prep_res, exec_res):
        # Store embedding in shared store
        shared["embedding"] = exec_res
