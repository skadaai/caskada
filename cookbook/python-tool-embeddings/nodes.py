from brainyflow import Node, Memory # Import Memory
from tools.embeddings import get_embedding

class EmbeddingNode(Node):
    """Node for getting embeddings from OpenAI API"""

    async def prep(self, memory: Memory): # Use memory and add type hint
        # Get text from memory
        return memory.text if hasattr(memory, 'text') else ""

    async def exec(self, text):
        # Get embedding using tool function
        return get_embedding(text)

    async def post(self, memory: Memory, prep_res, exec_res): # Use memory and add type hint
        # Store embedding in memory
        memory.embedding = exec_res
        self.trigger("default") # Use trigger
