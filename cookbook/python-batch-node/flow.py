from brainyflow import Flow, Node, ParallelFlow, Memory
from nodes import TriggerCSVChunksNode, ProcessOneChunkNode, AggregateStatsNode

class ShowStats(Node):
    """Node to display the final statistics."""
    
    async def prep(self, memory: Memory):
        """Get statistics from memory."""
        return memory.statistics if hasattr(memory, 'statistics') else {}
    
    async def exec(self, stats: dict):
        """Display the statistics."""
        print("\nFinal Statistics:")
        print(f"- Total Sales: ${stats.get('total_sales', 0):,.2f}")
        print(f"- Average Sale: ${stats.get('average_sale', 0):,.2f}")
        print(f"- Total Transactions: {stats.get('total_transactions', 0):,}\n")
        return stats

    async def post(self, memory: Memory, prep_res, exec_res):
        """No further action needed."""
        self.trigger("end")

def create_flow():
    """Create and return the processing flow."""
    # Create nodes
    trigger_chunks = TriggerCSVChunksNode(chunk_size=1000)
    process_chunk = ProcessOneChunkNode()
    aggregate_stats = AggregateStatsNode()
    show_stats = ShowStats()
    
    # Connect nodes
    trigger_chunks - "process_chunk" >> process_chunk # Fan out chunk processing
    process_chunk - "aggregate_stats" >> aggregate_stats # Trigger aggregation after all chunks are processed
    aggregate_stats - "show_stats" >> show_stats # After aggregation, show stats
    
    # Create and return flow
    # Use ParallelFlow for concurrent chunk processing
    return ParallelFlow(start=trigger_chunks)
