import os
import asyncio
from PIL import Image, ImageFilter
import numpy as np
from brainyflow import Node

class LoadImage(Node):
    """Node that loads an image from file."""
    async def prep(self, shared):
        """Get image path from parameters."""
        image_path = shared["image_path"]
        print(f"Loading image: {image_path}")
        return image_path
    
    async def exec(self, image_path):
        """Load image using PIL."""
        # Simulate I/O delay
        await asyncio.sleep(0.5)
        return Image.open(image_path)
    
    async def post(self, shared, prep_res, exec_res):
        """Store image in the isolated local store."""
        self.trigger("apply_filter", { "image": exec_res })

class ApplyFilter(Node):
    """Node that applies a filter to an image."""
    async def prep(self, shared):
        """Get image and filter type."""
        image = shared["image"]
        filter_type = shared["filter"]
        print(f"Applying {filter_type} filter...")
        return image, filter_type
    
    async def exec(self, inputs):
        """Apply the specified filter."""
        image, filter_type = inputs
        
        # Simulate processing delay
        await asyncio.sleep(0.5)
        
        match filter_type:
            case "grayscale":
                return image.convert("L")
            case "blur":
                return image.filter(ImageFilter.BLUR)
            case "sepia":
                # Convert to array for sepia calculation
                img_array = np.array(image)
                sepia_matrix = np.array([
                    [0.393, 0.769, 0.189],
                    [0.349, 0.686, 0.168],
                    [0.272, 0.534, 0.131]
                ])
                sepia_array = img_array.dot(sepia_matrix.T)
                sepia_array = np.clip(sepia_array, 0, 255).astype(np.uint8)
                return Image.fromarray(sepia_array)
            case _:
                raise ValueError(f"Unknown filter: {filter_type}")
    
    async def post(self, shared, prep_res, exec_res):
        """Store filtered image in the isolated local store."""
        self.trigger("save", { "filtered_image": exec_res })

class SaveImage(Node):
    """Node that saves the processed image."""
    async def prep(self, shared):
        """Prepare output path."""
        image = shared["filtered_image"]
        base_name = os.path.splitext(os.path.basename(shared["image_path"]))[0]
        filter_type = shared["filter"]
        output_path = os.path.join(os.path.dirname(__file__), "output", f"{base_name}_{filter_type}.jpg")
        
        # Create output directory if needed
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        return image, output_path
    
    async def exec(self, inputs):
        """Save the image."""
        image, output_path = inputs
        
        # Simulate I/O delay
        await asyncio.sleep(0.5)
        
        image.save(output_path)
        return output_path
    
    async def post(self, shared, prep_res, exec_res):
        """Print success message."""
        print(f"Saved: {exec_res}")
