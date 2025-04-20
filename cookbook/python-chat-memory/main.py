import asyncio
from brainyflow import Memory
from flow import chat_flow

async def main():
    """
    Run an interactive chat interface with memory retrieval.

    Features:
    1. Maintains a window of the 3 most recent conversation pairs
    2. Archives older conversations with embeddings
    3. Retrieves 1 relevant past conversation when needed
    4. Total context to LLM: 3 recent pairs + 1 retrieved pair
    """

    print("=" * 50)
    print("BrainyFlow Chat with Memory")
    print("=" * 50)
    print("This chat keeps your 3 most recent conversations")
    print("and brings back relevant past conversations when helpful")
    print("Type 'exit' to end the conversation")
    print("=" * 50)

    # Run the chat flow
    memory = Memory() # Use Memory object
    await chat_flow.run(memory)

if __name__ == "__main__":
    asyncio.run(main())
