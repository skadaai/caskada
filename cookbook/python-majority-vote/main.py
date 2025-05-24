import argparse
from brainyflow import Node, Flow
import collections
from utils import call_llm
import yaml


class TriggerMajorityVoteNode(Node):
    async def prep(self, shared):
        question = getattr(shared, "question", "(No question provided)")
        attempts_count = getattr(shared, "num_tries", 3)
        return [question for _ in range(attempts_count)]

    async def post(self, memory, prep_res, exec_res):
        memory.remaining_items = len(prep_res)

        for index, input in enumerate(prep_res):
            self.trigger("default", {"index": index, "data": input})
          

class MajorityVoteNode(Node):
    async def prep(self, memory):# -> tuple[Any, Any]:# -> tuple[Any, Any]:
        return memory.index, memory.data

    async def exec(self, data_tuple):
        index, single_question = data_tuple

        prompt = f"""
You are a helpful assistant. Please answer the user's question below.
Question: {single_question}

Return strictly using the following YAML structure:
```yaml
thinking: |
    (Your thinking process here)
answer: 0.123 # Final answer as a decimal with 3 decimal places
```

IMPORTANT: Make sure to:
1. Use proper indentation (4 spaces) for all multi-line fields
2. Use the | character for multi-line text fields
3. Keep single-line fields without the | character
4. Your answer must be wrapped in yaml code block or it will result in an error. Do not forget to include the ```yaml sequence at the beginning and end it with ```.
"""
        raw_response = call_llm(prompt)
        assert "```yaml" in raw_response, "Response must contain yaml block"
        yaml_part = raw_response.split("```yaml")[1].split("```")[0].strip()
        parsed = yaml.safe_load(yaml_part)

        # Validate we have at least 'answer' field
        if not isinstance(parsed, dict) or 'answer' not in parsed:
            raise RuntimeError(f"Missing 'answer' in YAML: {parsed}")

        # Return only the 'answer' field for the majority vote.
        return str(parsed['answer'])
    
    async def exec_fallback(self, prep_res, exc):
        return None

    async def post(self, memory, prep_res, exec_res):
        if not hasattr(memory, "results"):
            memory.results = [None] * memory.remaining_items
        memory.results[prep_res[0]] = exec_res
        print(f"Processor: Finished item {prep_res[0]}")

        # Decrement counter and trigger combine if this is the last summary
        memory.remaining_items -= 1
        if not memory.remaining_items == 0:
            return
        
        exec_res_list = memory.results
        print(f"Processor: exec_res_list: {exec_res_list}")
        

        # Count frequency for non-None answers
        exec_res_list = [res for res in exec_res_list if res is not None]
        counter = collections.Counter(exec_res_list)
        best_answer, freq = counter.most_common(1)[0]

        # Store final
        memory["majority_answer"] = best_answer

        print("========================")
        print("All structured answers:", exec_res_list)
        print("Majority vote =>", best_answer)
        print("Frequency =>", freq)
        print("========================")

        # End the flow
        self.trigger("end")

async def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Run majority vote reasoning on a problem")
    parser.add_argument("--problem", type=str, help="Your reasoning problem to solve")
    parser.add_argument("--tries", type=int, default=5, help="Number of attempts to make (default: 5)")
    args = parser.parse_args()
    
    # Default problem if none provided
    default_problem = """You work at a shoe factory. In front of you, there are three pairs of shoes (six individual shoes) with the following sizes: two size 4s, two size 5s, and two size 6s. The factory defines an "acceptable pair" as two shoes that differ in size by a maximum of one size (e.g., a size 5 and a size 6 would be an acceptable pair). If you close your eyes and randomly pick three pairs of shoes without replacement, what is the probability that you end up drawing three acceptable pairs?"""
    
    shared = {
        "question": args.problem if args.problem else default_problem,
        "num_tries": args.tries
    }

    trigger = TriggerMajorityVoteNode()
    majority_node = MajorityVoteNode()
    trigger >> majority_node

    flow = Flow(start=trigger)
    await flow.run(shared)

    print("\n=== Final Answer ===")
    print(shared["majority_answer"])
    print("====================")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 