import argparse
import asyncio # Import asyncio
from brainyflow import Node, Flow, Memory # Import Node, Flow, Memory
import collections
from utils import call_llm
import yaml

class TriggerAttemptsNode(Node):
    async def prep(self, memory: Memory):
        question = memory.question if hasattr(memory, "question") else "(No question provided)"
        attempts_count = memory.num_tries if hasattr(memory, "num_tries") else 3
        memory.attempts_count = attempts_count # Store count for aggregation
        memory.answers = [] # Initialize list for answers
        return question, attempts_count

    async def post(self, memory: Memory, prep_res, exec_res):
        question, attempts_count = prep_res
        for i in range(attempts_count):
            # Trigger the processing node for each attempt
            self.trigger("process_question", forkingData={"question": question, "attempt_num": i + 1})
        # The aggregation node will be triggered when all attempts are processed

class ProcessQuestionNode(Node):
    async def prep(self, memory: Memory):
        # Read data passed via forkingData from local memory
        return memory.question, memory.attempt_num

    async def exec(self, inputs):
        question, attempt_num = inputs
        print(f"Attempt {attempt_num}: Processing question...")
        prompt = f"""
You are a helpful assistant. Please answer the user's question below.
Question: {question}

Return strictly using the following YAML structure:
```yaml
thinking: |
    (Your thinking process here)
answer: 0.123 # Final answer as a decimal with 3 decimal places
```"""
        raw_response = call_llm(prompt)
        yaml_part = raw_response.split("```yaml")[1].split("```")[0].strip()
        parsed = yaml.safe_load(yaml_part)

        # Validate we have at least 'answer' field
        if not isinstance(parsed, dict) or 'answer' not in parsed:
            raise RuntimeError(f"Missing 'answer' in YAML: {parsed}")

        # Return only the 'answer' field for the majority vote.
        return str(parsed['answer'])

    async def exec_fallback(self, prep_res, exc):
        return None

    async def post(self, memory: Memory, prep_res, exec_res):
        # Store the answer in the global list
        memory.answers.append(exec_res)
        # Decrement the counter and trigger aggregation if this is the last attempt
        memory.attempts_count -= 1
        if memory.attempts_count == 0:
            print("Processor: All attempts processed, triggering majority vote.")
            self.trigger("aggregate_votes")

class AggregateVotesNode(Node):
    async def prep(self, memory: Memory):
        # Get all answers from memory
        return memory.answers or []

    async def exec(self, answers: list):
        """Calculate majority vote."""
        # Count frequency for non-None answers
        valid_answers = [res for res in answers if res is not None]
        counter = collections.Counter(valid_answers)
        if not counter:
            return None, 0
        best_answer, freq = counter.most_common(1)[0]
        return best_answer, freq

    async def post(self, memory: Memory, prep_res, exec_res):
        best_answer, freq = exec_res
        # Store final
        memory.majority_answer = best_answer

        print("========================")
        print("All structured answers:", prep_res) # prep_res contains the list of answers
        print("Majority vote =>", best_answer)
        print("Frequency =>", freq)
        print("========================")

        # End the flow
        self.trigger("end")


if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Run majority vote reasoning on a problem")
    parser.add_argument("--problem", type=str, help="Your reasoning problem to solve")
    parser.add_argument("--tries", type=int, default=5, help="Number of attempts to make (default: 5)")
    args = parser.parse_args()

    # Default problem if none provided
    default_problem = """You work at a shoe factory. In front of you, there are three pairs of shoes (six individual shoes) with the following sizes: two size 4s, two size 5s, and two size 6s. The factory defines an "acceptable pair" as two shoes that differ in size by a maximum of one size (e.g., a size 5 and a size 6 would be an acceptable pair). If you close your eyes and randomly pick three pairs of shoes without replacement, what is the probability that you end up drawing three acceptable pairs?"""

    memory = Memory({ # Use Memory object
        "question": args.problem if args.problem else default_problem,
        "num_tries": args.tries
    })

    # Create nodes
    trigger_attempts = TriggerAttemptsNode()
    process_question = ProcessQuestionNode()
    aggregate_votes = AggregateVotesNode()

    # Connect nodes
    trigger_attempts - "process_question" >> process_question
    process_question - "aggregate_votes" >> aggregate_votes # ProcessQuestion triggers aggregation

    # Create flow
    flow = Flow(start=trigger_attempts) # Flow starts with the trigger node

    # Run the flow
    asyncio.run(flow.run(memory)) # Use asyncio.run and pass memory

    print("\n=== Final Answer ===")
    print(memory.majority_answer) # Access from memory
    print("====================")
