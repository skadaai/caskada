from flow import create_vision_flow

async def main():
    # Create and run flow
    flow = create_vision_flow()
    shared = {}
    await flow.run(shared)
    
    # Print results
    if "results" in shared:
        for result in shared["results"]:
            print(f"\nFile: {result['filename']}")
            print("-" * 50)
            print(result["text"])
    else:
        print("No results found")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
