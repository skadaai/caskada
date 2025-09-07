from caskada import Flow
from nodes import Map, ReadResumesNode, EvaluateResumesNode, Reduce, ResultsNode

def create_resume_processing_flow():
    """Create a map-reduce flow for processing resumes."""
    # Create nodes
    map = Map()
    reduce = Reduce()
    read_resumes_node = ReadResumesNode()
    evaluate_resumes_node = EvaluateResumesNode()
    results_node = ResultsNode()
    
    # Connect nodes
    read_resumes_node >> map >> evaluate_resumes_node >> reduce >> results_node
    
    # Create flow
    return Flow(start=read_resumes_node)