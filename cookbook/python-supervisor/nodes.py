from brainyflow import Node, Memory # Import Memory
from utils import call_llm, search_web
import yaml
import random

class DecideAction(Node):
    async def prep(self, memory: Memory): # Use memory and add type hint
        """Prepare the context and question for the decision-making process."""
        # Get the current context (default to "No previous search" if none exists)
        context = memory.context if hasattr(memory, 'context') else "No previous search" # Use property access
        # Get the question from memory
        question = memory.question if hasattr(memory, 'question') else "" # Use property access
        # Return both for the exec step
        return question, context

    async def exec(self, inputs):
        """Call the LLM to decide whether to search or answer."""
        question, context = inputs

        print(f"🤔 Agent deciding what to do next...")

        # Create a prompt to help the LLM decide what to do next
        prompt = f"""
### CONTEXT
You are a research assistant that can search the web.
Question: {question}
Previous Research: {context}

### ACTION SPACE
[1] search
  Description: Look up more information on the web
  Parameters:
    - query (str): What to search for

[2] answer
  Description: Answer the question with current knowledge
  Parameters:
    - answer (str): Final answer to the question

## NEXT ACTION
Decide the next action based on the context and available actions.
Return your response in this format:

```yaml
thinking: |
    <your step-by-step reasoning process>
action: search OR answer
reason: <why you chose this action>
search_query: <specific search query if action is search>
```"""

        # Call the LLM to make a decision
        response = call_llm(prompt)
        
        # Parse the response to get the decision
        # Handle potential errors if the response doesn't contain the expected yaml block
        try:
            yaml_str = response.split("```yaml")[1].split("```")[0].strip()
            decision = yaml.safe_load(yaml_str)
        except (IndexError, yaml.YAMLError) as e:
            print(f"Error parsing LLM response: {e}")
            # Return a default or error decision if parsing fails
            return {"action": "error", "reason": f"Failed to parse LLM response: {response[:100]}..."}

        return decision

    async def post(self, memory: Memory, prep_res, exec_res):
        """Save the decision and determine the next step in the flow."""
        # If LLM decided to search, save the search query
        if exec_res.get("action") == "search":
            memory.search_query = exec_res.get("search_query")
            print(f"🔍 Agent decided to search for: {memory.search_query}")
        elif exec_res.get("action") == "answer":
             print(f"💡 Agent decided to answer the question")
        else:
             print(f"⚠️ Agent returned an unexpected action: {exec_res.get('action')}")
             # Handle unexpected actions, maybe trigger an error or fallback
             self.trigger("error")
             return

        # Trigger the action returned by the LLM
        self.trigger(exec_res.get("action"))

class SearchWeb(Node):
    async def prep(self, memory: Memory):
        """Get the search query from memory."""
        return memory.search_query if hasattr(memory, 'search_query') else ""

    async def exec(self, search_query):
        """Search the web for the given query."""
        # Call the search utility function
        print(f"🌐 Searching the web for: {search_query}")
        results = await search_web(search_query)
        return results

    async def post(self, memory: Memory, prep_res, exec_res):
        """Save the search results and go back to the decision node."""
        # Add the search results to the context in memory
        previous = memory.context if hasattr(memory, 'context') else ""
        memory.context = previous + "\n\nSEARCH: " + (memory.search_query if hasattr(memory, 'search_query') else "") + "\nRESULTS: " + exec_res

        print(f"📚 Found information, analyzing results...")

        # Always go back to the decision node after searching
        self.trigger("decide")

class UnreliableAnswerNode(Node):
    async def prep(self, memory: Memory):
        """Get the question and context for answering."""
        return memory.question if hasattr(memory, 'question') else "", memory.context if hasattr(memory, 'context') else ""

    async def exec(self, inputs):
        """Call the LLM to generate a final answer with 50% chance of returning a dummy answer."""
        question, context = inputs

        # 50% chance to return a dummy answer
        if random.random() < 0.5:
            print(f"🤪 Generating unreliable dummy answer...")
            return "Sorry, I'm on a coffee break right now. All information I provide is completely made up anyway. The answer to your question is 42, or maybe purple unicorns. Who knows? Certainly not me!"

        print(f"✍️ Crafting final answer...")

        # Create a prompt for the LLM to answer the question
        prompt = f"""
### CONTEXT
Based on the following information, answer the question.
Question: {question}
Research: {context}

## YOUR ANSWER:
Provide a comprehensive answer using the research results.
"""
        # Call the LLM to generate an answer
        answer = call_llm(prompt)
        return answer

    async def post(self, memory: Memory, prep_res, exec_res):
        """Save the final answer and complete the flow."""
        # Save the answer in memory
        memory.answer = exec_res

        print(f"✅ Answer generated successfully")
        self.trigger("default")

class SupervisorNode(Node):
    async def prep(self, memory: Memory):
        """Get the current answer for evaluation."""
        return memory.answer if hasattr(memory, 'answer') else None

    async def exec(self, answer):
        """Check if the answer is valid or nonsensical."""
        if answer is None:
             print(f"    🔍 Supervisor received no answer to check.")
             return {"valid": False, "reason": "No answer provided"}

        print(f"    🔍 Supervisor checking answer quality...")

        # Check for obvious markers of the nonsense answers
        nonsense_markers = [
            "coffee break",
            "purple unicorns",
            "made up",
            "42",
            "Who knows?"
        ]

        # Check if the answer contains any nonsense markers
        is_nonsense = any(marker in answer for marker in nonsense_markers)

        if is_nonsense:
            return {"valid": False, "reason": "Answer appears to be nonsensical or unhelpful"}
        else:
            return {"valid": True, "reason": "Answer appears to be legitimate"}

    async def post(self, memory: Memory, prep_res, exec_res):
        """Decide whether to accept the answer or restart the process."""
        if exec_res.get("valid", False):
            print(f"    ✅ Supervisor approved answer: {exec_res.get('reason', 'N/A')}")
            self.trigger("approved")
        else:
            print(f"    ❌ Supervisor rejected answer: {exec_res.get('reason', 'N/A')}")
            # Clean up the bad answer
            memory.answer = None
            # Add a note about the rejected answer
            context = memory.context if hasattr(memory, 'context') else ""
            memory.context = context + "\n\nNOTE: Previous answer attempt was rejected by supervisor."
            self.trigger("retry")
