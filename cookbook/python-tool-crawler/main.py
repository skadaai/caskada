from flow import create_flow

async def main():
    """Run the web crawler flow"""
    
    # Get website URL from user
    url = input("Enter website URL to crawl (e.g., https://example.com): ")
    if not url:
        print("Error: URL is required")
        return
    
    max_pages = input("How many pages to crawl? (Enter a number): ")
        
    # Initialize shared data
    shared = {
        "base_url": url,
        "max_pages": int(max_pages) if max_pages else 10
    }
    
    # Create and run flow
    flow = create_flow()
    await flow.run(shared)
    
    # Results are in shared["report"]
    
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
