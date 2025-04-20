import pandas as pd
from brainyflow import Node, Memory

# 1. Trigger Node (Fans out chunk processing)
class TriggerCSVChunksNode(Node):
    """Node to trigger processing for each CSV chunk."""

    def __init__(self, chunk_size=1000):
        """Initialize with chunk size."""
        super().__init__()
        self.chunk_size = chunk_size

    async def prep(self, memory: Memory):
        """Split CSV file into chunks.

        Returns an iterator of DataFrames, each containing chunk_size rows.
        """
        # Read CSV in chunks
        chunks = pd.read_csv(
            memory.input_file,
            chunksize=self.chunk_size
        )
        # Convert iterator to list for easier processing in post
        return list(chunks)

    async def exec(self, chunks: list):
        # No main computation needed here, just return the count for info
        return len(chunks)

    async def post(self, memory: Memory, chunks_to_process: list, chunk_count: int):
        print(f"Trigger: Triggering processing for {chunk_count} CSV chunks.")
        # Initialize results list and counter in global memory
        memory.chunk_statistics = [None] * chunk_count
        memory.remaining_chunks = chunk_count # Add counter
        # Trigger a 'process_chunk' action for each chunk
        for index, chunk in enumerate(chunks_to_process):
            self.trigger('process_chunk', { "chunk_data": chunk, "index": index })
        # NOTE: 'aggregate_stats' is now triggered by ProcessOneChunkNode when the counter reaches zero.

# 2. Processor Node (Processes a single chunk)
class ProcessOneChunkNode(Node):
    """Node to process a single chunk of the CSV."""

    async def prep(self, memory: Memory):
        # Read specific chunk data and index from local memory (passed via forkingData)
        return memory.chunk_data, memory.index

    async def exec(self, prep_res):
        chunk, index = prep_res
        # Process the single chunk
        print(f"Processor: Processing chunk (Index {index})")
        return {
            "total_sales": chunk["amount"].sum(),
            "num_transactions": len(chunk),
            "total_amount": chunk["amount"].sum(),
            "index": index # Include index in result for aggregation
        }

    async def post(self, memory: Memory, prep_res, chunk_stats: dict):
        chunk, index = prep_res
        # Store individual chunk statistics in global memory at the correct index
        memory.chunk_statistics[chunk_stats["index"]] = chunk_stats
        print(f"Processor: Finished chunk (Index {chunk_stats['index']})")
        # Decrement counter and trigger aggregate if this is the last chunk
        memory.remaining_chunks -= 1
        if memory.remaining_chunks == 0:
            print("Processor: All chunks processed, triggering aggregate.")
            self.trigger('aggregate_stats')
        else:
            self.trigger("default") # Continue in sequential flow (though aggregate_stats handles the next step)


# 3. Reducer Node (Aggregates individual chunk statistics)
class AggregateStatsNode(Node):
    """Node to aggregate individual chunk statistics."""

    async def prep(self, memory: Memory):
        # Read the array of individual results (filter out None if any failed)
        results = [r for r in (memory.chunk_statistics or []) if r is not None]
        return results

    async def exec(self, chunk_stats_list: list):
        print(f"Reducer: Aggregating {len(chunk_stats_list)} chunk statistics.")
        if not chunk_stats_list:
             return {
                "total_sales": 0,
                "average_sale": 0,
                "total_transactions": 0
            }

        # Combine statistics from all chunks
        total_sales = sum(res["total_sales"] for res in chunk_stats_list)
        total_transactions = sum(res["num_transactions"] for res in chunk_stats_list)
        total_amount = sum(res["total_amount"] for res in chunk_stats_list) # Use total_amount for average calculation

        # Calculate final statistics
        average_sale = total_amount / total_transactions if total_transactions > 0 else 0

        return {
            "total_sales": total_sales,
            "average_sale": average_sale,
            "total_transactions": total_transactions
        }

    async def post(self, memory: Memory, prep_res, final_statistics: dict):
        # Store the final aggregated statistics
        memory.statistics = final_statistics
        print("Reducer: Statistics aggregation complete.")
        self.trigger("show_stats") # Move to the next step (ShowStatsNode, defined elsewhere)

# Assuming ShowStatsNode is defined in another file or will be created later
# class ShowStatsNode(Node): ...
