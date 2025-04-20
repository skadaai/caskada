import os
import asyncio
from brainyflow import Memory
from flow import create_flow

async def main():
    """Run the web crawler flow"""

    # Get website URL from user
    url = input("Enter website URL to crawl (e.g., https://example.com): ")
    if not url:
        print("Error: URL is required")
        return

    # Initialize memory
    memory = Memory({
        "base_url": url,
        "max_pages": 1
    })

    # Create and run flow
    flow = create_flow()
    await flow.run(memory)

    # Results are in memory.report
    # The report is printed by the GenerateReportNode, so no need to print here.

if __name__ == "__main__":
    asyncio.run(main())
