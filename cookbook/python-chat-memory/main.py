import asyncio
from flow import chat_flow

async def run_chat_memory_demo():
    """
    Run an interactive chat interface with memory retrieval.
    
    Features:
    1. Maintains a window of the 3 most recent conversation pairs
    2. Archives older conversations with embeddings
    3. Retrieves 1 relevant past conversation when needed
    4. Total context to LLM: 3 recent pairs + 1 retrieved pair
    """
    
    print("=" * 50)
    print("Caskada Chat with Memory")
    print("=" * 50)
    print("This chat keeps your 3 most recent conversations")
    print("and brings back relevant past conversations when helpful")
    print("Type 'exit' to end the conversation")
    print("=" * 50)
    
    # Run the chat flow
    await chat_flow.run({})

if __name__ == "__main__":
    asyncio.run(run_chat_memory_demo())