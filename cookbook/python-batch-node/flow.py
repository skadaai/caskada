from caskada import Flow, Node
from nodes import CSVProcessor, CSVTrigger

class ShowStats(Node):
    """Node to display the final statistics."""
    
    async def prep(self, shared):
        """Get statistics from shared store."""
        return shared["statistics"]
    
    async def post(self, shared, prep_res, exec_res):
        """Display the statistics."""
        stats = prep_res
        print("\nFinal Statistics:")
        print(f"- Total Sales: ${stats['total_sales']:,.2f}")
        print(f"- Average Sale: ${stats['average_sale']:,.2f}")
        print(f"- Total Transactions: {stats['total_transactions']:,}\n")
        self.trigger("end")

def create_flow():
    """Create and return the processing flow."""
    # Create nodes
    trigger = CSVTrigger(chunk_size=1000)
    processor = CSVProcessor()
    show_stats = ShowStats()
    
    # Connect nodes
    trigger >> processor
    processor - "show_stats" >> show_stats
    
    # Create and return flow
    return Flow(start=trigger) 