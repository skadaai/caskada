"""Node implementations for the communication example."""

from brainyflow import Node, Memory # Import Memory

class EndNode(Node):
    """Node that handles flow termination."""
    pass

class TextInput(Node):
    """Node that reads text input and initializes memory."""

    async def prep(self, memory: Memory): # Add type hint
        """Get user input."""
        return input("Enter text (or 'q' to quit): ")

    async def post(self, memory: Memory, prep_res, exec_res): # Add type hint
        """Store text and initialize/update statistics."""
        if prep_res == 'q':
            self.trigger("exit")
            return

        # Store the text
        memory.text = prep_res

        # Initialize statistics if they don't exist
        if not hasattr(memory, 'stats'):
            memory.stats = {
                "total_texts": 0,
                "total_words": 0
            }
        memory.stats["total_texts"] += 1

        self.trigger("count")

class WordCounter(Node):
    """Node that counts words in the text."""

    async def prep(self, memory: Memory): # Add type hint
        """Get text from memory."""
        return memory.text

    async def exec(self, text):
        """Count words in the text."""
        return len(text.split())

    async def post(self, memory: Memory, prep_res, exec_res): # Add type hint
        """Update word count statistics."""
        memory.stats["total_words"] += exec_res
        self.trigger("show")

class ShowStats(Node):
    """Node that displays statistics from memory."""

    async def prep(self, memory: Memory): # Add type hint
        """Get statistics from memory."""
        return memory.stats

    async def post(self, memory: Memory, prep_res, exec_res): # Add type hint
        """Display statistics and continue the flow."""
        stats = prep_res
        print(f"\nStatistics:")
        print(f"- Texts processed: {stats['total_texts']}")
        print(f"- Total words: {stats['total_words']}")
        # Add check for division by zero
        avg_words = stats['total_words'] / stats['total_texts'] if stats['total_texts'] > 0 else 0
        print(f"- Average words per text: {avg_words:.1f}\n")
        self.trigger("continue")
