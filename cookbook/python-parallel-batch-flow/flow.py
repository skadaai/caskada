"""Flow definitions for parallel image processing."""

from brainyflow import Flow, ParallelFlow
from nodes import LoadImage, ApplyFilter, SaveImage

def create_base_flow():
    """Create flow for processing a single image with one filter."""
    # Create nodes
    load = LoadImage()
    apply_filter = ApplyFilter()
    save = SaveImage()
    
    # Connect nodes
    load - "apply_filter" >> apply_filter
    apply_filter - "save" >> save
    
    # Create flow
    return load

class ImageTriggerNode(Node):
    """Node for processing multiple images with different filters."""
    
    async def post(self, shared, prep_res, exec_res)
        """Generate parameters for each image-filter combination."""
        # Get list of images and filters
        images = getattr(shared, "images", [])
        filters = ["grayscale", "blur", "sepia"]
        
        # Create parameter combinations
        for image_path in images:
            for filter_type in filters:
                self.trigger("default", {
                    "image_path": image_path,
                    "filter": filter_type
                })
        
        print(f"Processing {len(images)} images with {len(filters)} filters...")
        print(f"Total combinations: {len(images) * len(filters)}")


def create_flows():
    """Create the complete parallel processing flow."""
    # Create base flow for single image processing
    base_flow = create_base_flow()
    trigger = ImageTriggerNode()
    trigger >> base_flow
    
    return Flow(start=trigger), ParallelFlow(start=base_flow)
