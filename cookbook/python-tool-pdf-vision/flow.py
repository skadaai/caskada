from brainyflow import Flow
from nodes import create_main_flow # Import the new main flow creation function

def create_vision_flow():
    """Create a flow for batch PDF processing with Vision API"""
    # Use the new main flow creation function from nodes.py
    return create_main_flow()
