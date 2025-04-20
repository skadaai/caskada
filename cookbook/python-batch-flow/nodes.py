"""Node implementations for image processing."""

import os
from PIL import Image, ImageEnhance, ImageFilter
from brainyflow import Node, Memory # Import Memory

class LoadImage(Node):
    """Node that loads an image file."""
    
    async def prep(self, memory: Memory): # Use memory and add type hint
        """Get image path from memory."""
        if not hasattr(memory, "input_image_name"):
            raise ValueError("input_image_name not provided in memory")
        return os.path.join("images", memory.input_image_name)    

    async def exec(self, image_path):
        """Load the image using PIL."""
        return Image.open(image_path)
    
    async def post(self, memory: Memory, prep_res, exec_res): # Use memory and add type hint
        """Store the image in memory."""
        memory.image = exec_res # Use property access
        self.trigger("default") # Use trigger

class ApplyFilter(Node):
    """Node that applies a filter to an image."""
    
    async def prep(self, memory: Memory): # Use memory and add type hint
        """Get image and filter type from memory."""
        return memory.image if hasattr(memory, 'image') else None, memory.filter_type if hasattr(memory, 'filter_type') else None # Use property access
    
    async def exec(self, inputs):
        """Apply the specified filter."""
        image, filter_type = inputs
        
        if image is None or filter_type is None:
            raise ValueError("Image or filter type not provided")

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
    
    async def post(self, memory: Memory, prep_res, exec_res): # Use memory and add type hint
        """Store the filtered image."""
        memory.filtered_image = exec_res # Use property access
        self.trigger("default") # Use trigger

class SaveImage(Node):
    """Node that saves the processed image."""
    
    async def prep(self, memory: Memory): # Use memory and add type hint
        """Get filtered image and prepare output path."""
        # Create output directory if it doesn't exist
        os.makedirs("output", exist_ok=True)
        
        # Generate output filename
        input_name = os.path.splitext(memory.input_image_name if hasattr(memory, 'input_image_name') else "processed")[0] # Use property access
        filter_name = memory.filter_type if hasattr(memory, 'filter_type') else "nofilter" # Use property access
        output_path = os.path.join("output", f"{input_name}_{filter_name}.jpg")
        
        return memory.filtered_image if hasattr(memory, 'filtered_image') else None, output_path # Use property access
    
    async def exec(self, inputs):
        """Save the image to file."""
        image, output_path = inputs
        if image is None:
            raise ValueError("No filtered image to save")
        image.save(output_path, "JPEG")
        return output_path
    
    async def post(self, memory: Memory, prep_res, exec_res): # Use memory and add type hint
        """Print success message."""
        print(f"Saved filtered image to: {exec_res}")
        self.trigger("default") # Use trigger
