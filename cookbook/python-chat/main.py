import asyncio
from brainyflow import Node, Flow, Memory # Import Memory
from utils import call_llm

class ChatNode(Node):
    async def prep(self, memory: Memory): # Use memory and add type hint
        # Initialize messages if this is the first run
        if not hasattr(memory, 'messages'): # Use property access
            memory.messages = [] # Use property access
            print("Welcome to the chat! Type 'exit' to end the conversation.")

        # Get user input
        user_input = input("\nYou: ")

        # Check if user wants to exit
        if user_input.lower() == 'exit':
            return None

        # Add user message to history
        memory.messages.append({"role": "user", "content": user_input}) # Use property access

        # Return all messages for the LLM
        return memory.messages # Use property access

    async def exec(self, messages):
        if messages is None:
            return None

        # Call LLM with the entire conversation history
        response = call_llm(messages)
        return response

    async def post(self, memory: Memory, prep_res, exec_res): # Use memory and add type hint
        if prep_res is None or exec_res is None:
            print("\nGoodbye!")
        
        # Print the assistant's response
        print(f"\nAssistant: {exec_res}")

        # Add assistant message to history
        memory.messages.append({"role": "assistant", "content": exec_res}) # Use property access

        # Loop back to continue the conversation
        self.trigger("continue") # Use trigger

# Create the flow with self-loop
chat_node = ChatNode()
chat_node - "continue" >> chat_node  # Loop back to continue conversation

flow = Flow(start=chat_node)

async def main():
    memory = Memory({}) # Use Memory object
    await flow.run(memory) # Pass memory object

# Start the chat
if __name__ == "__main__":
    asyncio.run(main())
