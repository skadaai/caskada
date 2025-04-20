import asyncio
from brainyflow import Node, Flow, Memory
from utils import call_llm
import yaml # Import yaml

class UserInputNode(Node):
    async def prep(self, memory: Memory):
        # Initialize messages if this is the first run
        if not hasattr(memory, "messages"):
            memory.messages = []
            print("Welcome to the Travel Advisor Chat! Type 'exit' to end the conversation.")

        return None

    async def exec(self, _):
        # Get user input
        user_input = input("\nYou: ")
        return user_input

    async def post(self, memory: Memory, prep_res, exec_res):
        user_input = exec_res

        # Check if user wants to exit
        if user_input and user_input.lower() == 'exit':
            print("\nGoodbye! Safe travels!")
            self.trigger(None)  # End the conversation
            return

        # Store user input in memory
        memory.user_input = user_input

        # Move to guardrail validation
        self.trigger("validate")

class GuardrailNode(Node):
    async def prep(self, memory: Memory):
        # Get the user input from memory
        user_input = memory.user_input if hasattr(memory, "user_input") else ""
        return user_input

    async def exec(self, user_input):
        # Basic validation checks
        if not user_input or user_input.strip() == "":
            return False, "Your query is empty. Please provide a travel-related question."

        if len(user_input.strip()) < 3:
            return False, "Your query is too short. Please provide more details about your travel question."

        # LLM-based validation for travel topics
        prompt = f"""
Evaluate if the following user query is related to travel advice, destinations, planning, or other travel topics.
The chat should ONLY answer travel-related questions and reject any off-topic, harmful, or inappropriate queries.
User query: {user_input}
Return your evaluation in YAML format:
```yaml
valid: true/false
reason: [Explain why the query is valid or invalid]
```"""

        # Call LLM with the validation prompt
        messages = [{"role": "user", "content": prompt}]
        response = call_llm(messages)

        # Extract YAML content
        yaml_content = response.split("```yaml")[1].split("```")[0].strip() if "```yaml" in response else response

        result = yaml.safe_load(yaml_content)
        assert result is not None, "Error: Invalid YAML format"
        assert "valid" in result and "reason" in result, "Error: Invalid YAML format"
        is_valid = result.get("valid", False)
        reason = result.get("reason", "Missing reason in YAML response")

        return is_valid, reason

    async def post(self, memory: Memory, prep_res, exec_res):
        is_valid, message = exec_res

        if not is_valid:
            # Display error message to user
            print(f"\nTravel Advisor: {message}")
            # Skip LLM call and go back to user input
            self.trigger("retry")
            return

        # Valid input, add to message history
        if not hasattr(memory, "messages"):
             memory.messages = []
        memory.messages.append({"role": "user", "content": memory.user_input})
        # Proceed to LLM processing
        self.trigger("process")

class LLMNode(Node):
    async def prep(self, memory: Memory):
        # Add system message if not present
        if not hasattr(memory, "messages"):
             memory.messages = []
        if not any(msg.get("role") == "system" for msg in memory.messages):
            memory.messages.insert(0, {
                "role": "system",
                "content": "You are a helpful travel advisor that provides information about destinations, travel planning, accommodations, transportation, activities, and other travel-related topics. Only respond to travel-related queries and keep responses informative and friendly. Your response are concise in 100 words."
            })

        # Return all messages for the LLM
        return memory.messages

    async def exec(self, messages):
        # Call LLM with the entire conversation history
        response = call_llm(messages)
        return response

    async def post(self, memory: Memory, prep_res, exec_res):
        # Print the assistant's response
        print(f"\nTravel Advisor: {exec_res}")

        # Add assistant message to history
        if not hasattr(memory, "messages"):
             memory.messages = []
        memory.messages.append({"role": "assistant", "content": exec_res})

        # Loop back to continue the conversation
        self.trigger("continue")

async def main():
    # Create the flow with nodes and connections
    user_input_node = UserInputNode()
    guardrail_node = GuardrailNode()
    llm_node = LLMNode()

    # Create flow connections
    user_input_node - "validate" >> guardrail_node
    guardrail_node - "retry" >> user_input_node  # Loop back if input is invalid
    guardrail_node - "process" >> llm_node
    llm_node - "continue" >> user_input_node     # Continue conversation

    flow = Flow(start=user_input_node)

    # Start the chat
    memory = Memory() # Use Memory object
    await flow.run(memory)

if __name__ == "__main__":
    asyncio.run(main())
