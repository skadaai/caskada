import asyncio
from flow import create_flow

async def main():
    """Run the web search flow"""
    
    # Get search query from user
    query = input("Enter search query: ")
    if not query:
        print("Error: Query is required")
        return
        
    # Initialize shared data
    shared = {
        "query": query,
        "num_results": 5
    }
    
    # Create and run flow
    flow = create_flow()
    await flow.run(shared)
    
    # Results are in shared["analysis"]
    
if __name__ == "__main__":
    asyncio.run(main())
