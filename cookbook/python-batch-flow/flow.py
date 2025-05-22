from brainyflow import Flow, Node
from nodes import LoadImage, ApplyFilter, SaveImage

def create_base_flow():
    """Create the base Flow for processing a single image."""
    # Create nodes
    load = LoadImage()
    filter_node = ApplyFilter()
    save = SaveImage()
    
    # Connect nodes
    load - "apply_filter" >> filter_node
    filter_node - "save" >> save
    
    # Create and return flow
    return Flow(start=load)

class ImageTriggerNode(Node):
    """Node for processing multiple images with different filters."""
    
    async def post(self, memory, prep_res, exec_res):
        """Generate parameters for each image-filter combination."""
        # List of images to process
        images = ["cat.jpg", "dog.jpg", "bird.jpg"]
        
        # List of filters to apply
        filters = ["grayscale", "blur", "sepia"]
        
        # Generate all combinations
        for img in images:
            for f in filters:
                self.trigger("default", {
                    "input": img,
                    "filter": f
                })
        
def create_flow():
    """Create the complete batch processing flow."""
    # Create base flow for single image processing
    base_flow = create_base_flow()
    trigger = ImageTriggerNode()
    trigger >> base_flow
    
    return Flow(start=trigger)
    