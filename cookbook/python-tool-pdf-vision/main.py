import asyncio
from flow import create_vision_flow

async def main():
    # Create and run flow
    flow = create_vision_flow()
    shared = {}
    await flow.run(shared)
    
    # Print results
    # Access results directly from the Memory object
    if hasattr(memory, "results"):
        for result in memory.results:
            print(f"\nFile: {result['filename']}")
            print("-" * 50)
            print(result["text"])

if __name__ == "__main__":
    asyncio.run(main())
