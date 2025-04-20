from brainyflow import Node, Memory, ParallelFlow # Import Memory and ParallelFlow
from tools.pdf import pdf_to_images
from tools.vision import extract_text_from_image
from typing import List, Dict, Any
from pathlib import Path
import os

class TriggerPDFProcessingNode(Node):
    """Node for triggering processing of multiple PDFs from a directory"""

    async def prep(self, memory: Memory):
        # Get PDF directory path
        root_dir = Path(__file__).parent
        pdf_dir = root_dir / "pdfs"

        # List all PDFs
        pdf_files = []
        for file in os.listdir(pdf_dir):
            if file.lower().endswith('.pdf'):
                pdf_files.append({
                    "pdf_path": str(pdf_dir / file),
                    "extraction_prompt": memory.extraction_prompt if hasattr(memory, "extraction_prompt") else "Extract all text from this document, preserving formatting and layout."
                })

        if not pdf_files:
            print("No PDF files found in 'pdfs' directory!")
            return []

        print(f"Found {len(pdf_files)} PDF files")
        memory.pdf_files_to_process = pdf_files # Store for post
        memory.results = [] # Initialize results list in global memory
        return pdf_files # Return for exec (though exec is not used here)

    async def post(self, memory: Memory, pdf_files_to_process: list, exec_res):
        """Trigger the single PDF processing flow for each PDF."""
        for pdf_params in pdf_files_to_process:
            # Trigger the single PDF flow, passing parameters via forkingData
            # The single_pdf_flow will run with its own local memory initialized with pdf_params.
            # The single_pdf_flow's CombineResultsNode needs to write its result
            # to the global memory (memory.results).
            self.trigger("process_single_pdf", forkingData=pdf_params)
        # No trigger to aggregate here. The ParallelFlow will handle waiting.

class LoadPDFNode(Node):
    """Node for loading and converting a single PDF to images"""

    async def prep(self, memory: Memory):
        return memory.pdf_path if hasattr(memory, "pdf_path") else ""

    async def exec(self, pdf_path):
        return pdf_to_images(pdf_path)

    async def post(self, memory: Memory, prep_res, exec_res):
        memory.page_images = exec_res
        self.trigger("default")

class ExtractTextNode(Node):
    """Node for extracting text from images using Vision API"""

    async def prep(self, memory: Memory):
        return (
            memory.page_images if hasattr(memory, "page_images") else [],
            memory.extraction_prompt if hasattr(memory, "extraction_prompt") else None
        )

    async def exec(self, inputs):
        images, prompt = inputs
        results = []

        for img, page_num in images:
            text = extract_text_from_image(img, prompt)
            results.append({
                "page": page_num,
                "text": text
            })

        return results

    async def post(self, memory: Memory, prep_res, exec_res):
        memory.extracted_text = exec_res
        self.trigger("default")

class CombineResultsNode(Node):
    """Node for combining and formatting extracted text"""

    async def prep(self, memory: Memory):
        return memory.extracted_text if hasattr(memory, "extracted_text") else []

    async def exec(self, results):
        # Sort by page number
        sorted_results = sorted(results, key=lambda x: x["page"])

        # Combine text with page numbers
        combined = []
        for result in sorted_results:
            combined.append(f"=== Page {result['page']} ===\n{result['text']}\n")

        return "\n".join(combined)

    async def post(self, memory: Memory, prep_res, final_text):
        # Store the final text for this PDF in the global results list
        # Need the filename to associate the text with the PDF.
        # The filename was passed via forkingData to the single_pdf_flow.
        # It should be available in the local memory of this node's flow instance.
        filename = memory.pdf_path # Assuming pdf_path is available in local memory

        # Append result to the global results list
        memory.results.append({
            "filename": os.path.basename(filename),
            "text": final_text
        })
        self.trigger("default") # Signal completion of this single PDF flow instance

class AggregatePDFResultsNode(Node):
    """Node for collecting results from each PDF processing and triggering final aggregation."""

    async def prep(self, memory: Memory):
        """Get results from memory."""
        return memory.results or []

    async def exec(self, results):
        """Combine results into a final output."""
        final_output = "--- PDF Extraction Results ---\n\n"
        for result in results:
            final_output += f"File: {result['filename']}\n"
            final_output += f"{result['text']}\n\n"
        return final_output

    async def post(self, memory: Memory, prep_res, final_output):
        """Store the final output."""
        memory.final_output = final_output
        print("\n--- Final Aggregated Results ---")
        print(final_output)
        self.trigger("default") # End of the main flow


def create_single_pdf_flow():
    """Create a flow for processing a single PDF"""
    from brainyflow import Flow

    # Create nodes
    load_pdf = LoadPDFNode()
    extract_text = ExtractTextNode()
    combine_results = CombineResultsNode() # Use the modified CombineResultsNode

    # Connect nodes
    load_pdf >> extract_text >> combine_results

    # Create and return flow
    return Flow(start=load_pdf)

def create_main_flow():
    """Create the main flow for processing multiple PDFs."""
    # Create the trigger node
    trigger_node = TriggerPDFProcessingNode()

    # Create the single PDF processing flow (used as a sub-flow)
    single_pdf_flow = create_single_pdf_flow()

    # Create the aggregation node
    aggregate_node = AggregatePDFResultsNode()

    # Connect the trigger node to the single PDF flow using ParallelFlow
    # The trigger node triggers 'process_single_pdf'.
    # The ParallelFlow will run the single_pdf_flow for each trigger concurrently.
    # After all single_pdf_flow instances complete, the ParallelFlow completes,
    # and the main flow moves to the next node connected via the ParallelFlow's default trigger.
    trigger_node - "process_single_pdf" >> single_pdf_flow

    # The main flow structure: Trigger -> ParallelFlow(Single PDF Flow) -> Aggregate
    # The ParallelFlow will start with the trigger node and run the single_pdf_flow
    # for each triggered 'process_single_pdf' action.
    # After the ParallelFlow finishes, it will trigger its default action,
    # which should go to the aggregate node.

    # Let's define the main flow using ParallelFlow
    main_flow = ParallelFlow(start=trigger_node) # ParallelFlow starts with the trigger
    main_flow - "default" >> aggregate_node # After ParallelFlow completes, go to aggregate

    return main_flow
