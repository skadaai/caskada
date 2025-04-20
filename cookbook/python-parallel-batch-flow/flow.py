"""Flow definitions for parallel image processing."""

from brainyflow import Node, Flow, ParallelFlow, Memory
from nodes import LoadImage, ApplyFilter, SaveImage, NoOp

def create_base_flow():
    """Create flow for processing a single image with one filter."""
    # Create nodes
    load = LoadImage()
    apply_filter = ApplyFilter()
    save = SaveImage()
    noop = NoOp()

    # Connect nodes
    load - "apply_filter" >> apply_filter
    apply_filter - "save" >> save
    save - "default" >> noop

    # Create flow
    return Flow(start=load) # Return a Flow instance

class TriggerImageProcessingNode(Node):
    """Node that triggers processing for each image-filter combination."""
    async def prep(self, memory: Memory):
        """Generate parameters for each image-filter combination."""
        # Get list of images and filters
        images = getattr(memory, "images", [])
        filters = ["grayscale", "blur", "sepia"]

        # Create parameter combinations
        params = []
        for image_path in images:
            for filter_type in filters:
                params.append({
                    "image_path": image_path,
                    "filter": filter_type
                })

        print(f"Processing {len(images)} images with {len(filters)} filters...")
        print(f"Total combinations: {len(params)}")
        return params

    async def post(self, memory: Memory, combinations: list, exec_res):
        """Trigger the base flow for each combination."""
        for combo in combinations:
            # Pass combination data as forkingData to the local memory of the triggered flow
            self.trigger("process_combination", forkingData=combo)

def create_flows():
    """Create the complete sequential and parallel processing flows."""
    # Create base flow for single image processing
    base_flow_instance = create_base_flow()

    # Create trigger node
    trigger_node = TriggerImageProcessingNode()

    # Sequential Flow: Processes combinations one by one
    # The trigger node triggers the base_flow for each combination sequentially
    trigger_node - "process_combination" >> base_flow_instance
    sequential_flow = Flow(start=trigger_node)

    # Parallel Flow: Processes combinations concurrently
    # The trigger node triggers the base_flow for each combination in parallel
    trigger_node_parallel = TriggerImageProcessingNode() # Need a separate trigger for the parallel flow
    trigger_node_parallel - "process_combination" >> base_flow_instance # Connect to the same base_flow instance
    parallel_flow = ParallelFlow(start=trigger_node_parallel)

    return sequential_flow, parallel_flow
