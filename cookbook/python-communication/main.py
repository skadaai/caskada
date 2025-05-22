from flow import create_flow

async def main():
    """Run the communication example."""
    flow = create_flow()
    shared = {}
    await flow.run(shared)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())