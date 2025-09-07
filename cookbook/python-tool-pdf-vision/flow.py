from caskada import Flow
from nodes import TriggerPDFNode, ProcessPDFNode

def create_vision_flow():
    """Create a flow for batch PDF processing with Vision API"""
    trigger_node = TriggerPDFNode()
    process_node = ProcessPDFNode()

    trigger_node >> process_node
    return Flow(start=trigger_node)
