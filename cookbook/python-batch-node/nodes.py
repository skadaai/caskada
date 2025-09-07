import pandas as pd
from caskada import Node

class CSVTrigger(Node):
    """Node that triggers the batch processing of a large CSV file."""
    
    def __init__(self, chunk_size=1000):
        """Initialize with chunk size."""
        super().__init__()
        self.chunk_size = chunk_size
    
    async def prep(self, shared):
        """Split CSV file into chunks.
        
        Returns an iterator of DataFrames, each containing chunk_size rows.
        """
        # Read CSV in chunks
        chunks = pd.read_csv(
            shared["input_file"],
            chunksize=self.chunk_size
        )
        return chunks
    
    async def post(self, memory, chunks, exec_res):
        memory.remaining_chunks = 0
        for index, chunk in enumerate(chunks):
            memory.remaining_chunks += 1
            self.trigger("default", {"index": index, "chunk": chunk})
    

class CSVProcessor(Node):
    """Node that processes a large CSV file in chunks."""
    
    async def prep(self, memory):
        return memory.index, memory.chunk
       
    async def exec(self, data_tuple):
        """Process a single chunk of the CSV.
        
        Args:
            chunk: pandas DataFrame containing chunk_size rows
            
        Returns:
            dict: Statistics for this chunk
        """
        index, chunk = data_tuple

        return {
            "total_sales": chunk["amount"].sum(),
            "num_transactions": len(chunk),
            "total_amount": chunk["amount"].sum()
        }
    
    async def post(self, memory, prep_res, chunk_stats):
        """Combine results from all chunks.
        
        Args:
            prep_res: Original chunks iterator
            chunk_stats: List of results from each chunk
            
        Returns:
            str: Action to take next
        """

        if not hasattr(memory, "chunk_stats"):
            memory.chunk_stats = [None] * memory.remaining_chunks
        memory.chunk_stats[prep_res[0]] = chunk_stats
        print(f"Processor: Finished chunk {prep_res[0]}")

        # Decrement counter and trigger combine if this is the last summary
        memory.remaining_chunks -= 1
        if not memory.remaining_chunks == 0:
            return
        
        exec_res_list = memory.chunk_stats
        print(f"Processor: exec_res_list: {exec_res_list}")
        
        # Combine statistics from all chunks
        total_sales = sum(res["total_sales"] for res in exec_res_list)
        total_transactions = sum(res["num_transactions"] for res in exec_res_list)
        total_amount = sum(res["total_amount"] for res in exec_res_list)
        
        # Calculate final statistics
        memory["statistics"] = {
            "total_sales": total_sales,
            "average_sale": total_amount / total_transactions,
            "total_transactions": total_transactions
        }
        
        self.trigger("show_stats") 