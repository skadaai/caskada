"""Node implementations for image processing."""

import os
from PIL import Image, ImageEnhance, ImageFilter
from brainyflow import Node

class LoadImage(Node):
    """Node that loads an image file."""
    
    async def prep(self, shared):
        """Get image path from parameters."""
        return os.path.join(os.path.dirname(__file__), "images", shared["input"])
    
    async def exec(self, image_path):
        """Load the image using PIL."""
        return Image.open(image_path)
    
    async def post(self, shared, prep_res, exec_res):
        """Store the image in shared store."""
        shared["image"] = exec_res
        self.trigger("apply_filter")

class ApplyFilter(Node):
    """Node that applies a filter to an image."""
    
    async def prep(self, shared):
        """Get image and filter type."""
        return shared["image"], shared["filter"]
    
    async def exec(self, inputs):
        """Apply the specified filter."""
        image, filter_type = inputs
        
        if filter_type == "grayscale":
            return image.convert("L")
        elif filter_type == "blur":
            return image.filter(ImageFilter.BLUR)
        elif filter_type == "sepia":
            # Sepia implementation
            enhancer = ImageEnhance.Color(image)
            grayscale = enhancer.enhance(0.3)
            colorize = ImageEnhance.Brightness(grayscale)
            return colorize.enhance(1.2)
        else:
            raise ValueError(f"Unknown filter: {filter_type}")
    
    async def post(self, shared, prep_res, exec_res):
        """Store the filtered image."""
        shared["filtered_image"] = exec_res
        self.trigger("save")

class SaveImage(Node):
    """Node that saves the processed image."""
    
    async def prep(self, shared):
        """Get filtered image and prepare output path."""
        # Create output directory if it doesn't exist
        os.makedirs(os.path.join(os.path.dirname(__file__), "output"), exist_ok=True)
        
        # Generate output filename
        input_name = os.path.splitext(shared["input"])[0]
        filter_name = shared["filter"]
        output_path = os.path.join(os.path.dirname(__file__), "output", f"{input_name}_{filter_name}.jpg")
        
        return shared["filtered_image"], output_path
    
    async def exec(self, inputs):
        """Save the image to file."""
        image, output_path = inputs
        image.save(output_path, "JPEG")
        return output_path
    
    async def post(self, shared, prep_res, exec_res):
        """Print success message."""
        print(f"Saved filtered image to: {exec_res}")
        self.trigger("default")