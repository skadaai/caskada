import asyncio
from brainyflow import Memory # Import Memory
from flow import flow

async def main():
    # Example text to summarize
    text = """
    BrainyFlow is a minimalist LLM framework that models workflows as a Nested Directed Graph.
    Nodes handle simple LLM tasks, connecting through Actions for Agents.
    Flows orchestrate these nodes for Task Decomposition, and can be nested.
    It also supports Batch processing and Async execution.
    """

    # Initialize shared store
    memory = {"data": text}
    
    # Run the flow
    await flow.run(memory)

    # Print result
    print("\nInput text:", text)
    print("\nSummary:", memory.summary if hasattr(memory, 'summary') else "No summary generated")

if __name__ == "__main__":
    asyncio.run(main())
