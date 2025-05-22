import os
from PIL import Image
import numpy as np
from flow import create_flow

async def main():
    # Create and run flow
    print("Processing images with filters...")
    
    flow = create_flow()
    await flow.run({}) 
    
    print("\nAll images processed successfully!")
    print("Check the 'output' directory for results.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())