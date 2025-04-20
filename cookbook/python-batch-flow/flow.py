from brainyflow import Flow, ParallelFlow, Node, Memory # Import Memory
from nodes import LoadImage, ApplyFilter, SaveImage

# Define a sub-flow for processing a single image
def create_image_processing_flow():
    """Create a Flow for processing a single image."""
    # Create nodes
    load = LoadImage()
    filter_node = ApplyFilter()
    save = SaveImage()
    
    # Connect nodes
    load >> filter_node # Default transition after loading
    filter_node >> save # Default transition after applying filter
    
    # Create and return flow
    return Flow(start=load)

# 1. Trigger Node (Fans out image processing)
class TriggerImageProcessingNode(Node):
    """Node to trigger processing for each image-filter combination."""
    
    async def prep(self, memory: Memory): # Use memory and add type hint
        """Generate parameters for each image-filter combination."""
        # List of images to process
        images = memory.images if hasattr(memory, 'images') else ["cat.jpg", "dog.jpg", "bird.jpg"] # Use property access
        
        # List of filters to apply
        filters = memory.filters if hasattr(memory, 'filters') else ["grayscale", "blur", "sepia"] # Use property access
        
        # Generate all combinations
        params = []
        for img in images:
            for f in filters:
                params.append({
                    "input_image_name": img, # Use input_image_name to match LoadImage node
                    "filter_type": f # Use filter_type to match ApplyFilter node
                })
        
        return params

    async def post(self, memory: Memory, combinations: list, exec_res): # Use memory and add type hint
        print(f"Trigger: Triggering processing for {len(combinations)} image-filter combinations.")
        # Trigger a 'process_image' action for each combination
        for combination in combinations:
            self.trigger('process_image', combination) # Pass combination data via forkingData
        self.trigger("default") # Trigger next step after fanning out

def create_flow():
    """Create the complete batch processing flow."""
    # Create the sub-flow for single image processing
    image_processing_sub_flow = create_image_processing_flow()
    
    # Create the trigger node
    trigger_node = TriggerImageProcessingNode()
    
    # Connect the trigger node to the sub-flow using the 'process_image' action
    trigger_node - "process_image" >> image_processing_sub_flow
    
    # Create the main flow starting with the trigger node
    # Use ParallelFlow for concurrent image processing
    return ParallelFlow(start=trigger_node)
