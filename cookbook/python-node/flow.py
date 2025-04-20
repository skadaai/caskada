from brainyflow import Node, Flow, Memory # Import Memory
from utils.call_llm import call_llm

class Summarize(Node):
    async def prep(self, memory: Memory): # Use memory and add type hint
        """Read and preprocess data from memory."""
        return memory.data if hasattr(memory, 'data') else "" # Use property access

    async def exec(self, prep_res):
        """Execute the summarization using LLM."""
        if not prep_res:
            return "Empty text"
        prompt = f"Summarize this text in 10 words: {prep_res}"
        summary = call_llm(prompt)  # might fail
        return summary

    async def exec_fallback(self, memory: Memory, prep_res, exc):
        """Provide a simple fallback instead of crashing."""
        print(f"Error during summarization: {exc}") # Optional: log the error
        return "There was an error processing your request."

    async def post(self, memory: Memory, prep_res, exec_res):
        """Store the summary in memory."""
        memory.summary = exec_res # Use property access
        # Trigger "default" by not returning

# Create the flow
summarize_node = Summarize(max_retries=3)
flow = Flow(start=summarize_node)
