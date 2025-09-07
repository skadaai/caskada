from caskada import Node
from tools.pdf import pdf_to_images
from tools.vision import extract_text_from_image
from typing import List, Dict, Any
from pathlib import Path
import os

class TriggerPDFNode(Node):
    """Node for triggering the processing of multiple PDFs from a directory"""
    
    async def prep(self, shared):
        # Get PDF directory path
        root_dir = Path(__file__).parent
        pdf_dir = root_dir / "pdfs"
        
        # List all PDFs
        pdf_files = []
        for file in os.listdir(pdf_dir):
            if file.lower().endswith('.pdf'):
                pdf_files.append({
                    "pdf_path": str(pdf_dir / file),
                    "extraction_prompt": getattr(shared, "extraction_prompt", 
                        "Extract all text from this document, preserving formatting and layout.")
                })
        
        if not pdf_files:
            print("No PDF files found in 'pdfs' directory!")
            return []
            
        print(f"Found {len(pdf_files)} PDF files")
        return pdf_files

    async def post(self, memory, pdf_files, exec_res):
        for pdf_file in pdf_files:
            self.trigger("default", {"item": pdf_file})

class ProcessPDFNode(Node):
    """Node for processing multiple PDFs from a directory"""
    
    async def prep(self, memory):
        return memory.item            

    async def exec(self, item):
        # Create flow for single PDF
        flow = create_single_pdf_flow()
        
        # Process PDF
        print(f"\nProcessing: {os.path.basename(item['pdf_path'])}")
        print("-" * 50)
        
        # Run flow
        shared = item.copy()
        await flow.run(shared)
        
        return {
            "filename": os.path.basename(item["pdf_path"]),
            "text": shared.get("final_text", "No text extracted")
        }
    
    async def post(self, memory, prep_res, exec_res):
        if not hasattr(memory, "results"):
            memory.results = []
        memory.results.append(exec_res)

class LoadPDFNode(Node):
    """Node for loading and converting a single PDF to images"""
    
    async def prep(self, shared):
        return getattr(shared, "pdf_path", "")
        
    async def exec(self, pdf_path):
        return pdf_to_images(pdf_path)
        
    async def post(self, shared, prep_res, exec_res):
        shared["page_images"] = exec_res

class ExtractTextNode(Node):
    """Node for extracting text from images using Vision API"""
    
    async def prep(self, shared):
        return (
            getattr(shared, "page_images", []),
            getattr(shared, "extraction_prompt", None)
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
        
    async def post(self, shared, prep_res, exec_res):
        shared["extracted_text"] = exec_res

class CombineResultsNode(Node):
    """Node for combining and formatting extracted text"""
    
    async def prep(self, shared):
        return getattr(shared, "extracted_text", [])
        
    async def exec(self, results):
        # Sort by page number
        sorted_results = sorted(results, key=lambda x: x["page"])
        
        # Combine text with page numbers
        combined = []
        for result in sorted_results:
            combined.append(f"=== Page {result['page']} ===\n{result['text']}\n")
            
        return "\n".join(combined)
        
    async def post(self, shared, prep_res, exec_res):
        shared["final_text"] = exec_res

def create_single_pdf_flow():
    """Create a flow for processing a single PDF"""
    from caskada import Flow
    
    # Create nodes
    load_pdf = LoadPDFNode()
    extract_text = ExtractTextNode()
    combine_results = CombineResultsNode()
    
    # Connect nodes
    load_pdf >> extract_text >> combine_results
    
    # Create and return flow
    return Flow(start=load_pdf)
