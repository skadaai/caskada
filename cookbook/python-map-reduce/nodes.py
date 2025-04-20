from brainyflow import Node, Memory
from utils import call_llm
import yaml
import os
from asyncio import Lock

def _get_flow_lock(memory: Memory) -> Lock:
    """Return (and memoise) a lock that is private to this flow instance."""
    if not hasattr(memory, "_agg_lock"):
        memory._agg_lock = Lock()
    return memory._agg_lock

class ReadResumesNode(Node):
    """Map phase: Read all resumes from the data directory into memory."""

    async def exec(self, _):
        resume_files = {}
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        if not os.path.isdir(data_dir):
            raise FileNotFoundError(f"Expected resume folder not found: {data_dir}")

        for filename in os.listdir(data_dir):
            if filename.endswith(".txt"):
                file_path = os.path.join(data_dir, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    resume_files[filename] = file.read()

        return resume_files

    async def post(self, memory: Memory, prep_res, exec_res):
        memory.resumes = exec_res
        self.trigger("default")

# 1. Mapper Node: Triggers evaluation for each resume
class TriggerEvaluationsNode(Node):
    """Node to trigger evaluation for each resume."""

    async def prep(self, memory: Memory):
        # Get resume data from memory
        resumes_dict = getattr(memory, "resumes", {})
        return list(resumes_dict.items()) # [("resume1.txt", "content1"), ...]

    async def exec(self, resumes: list):
        # No main computation needed here, just return the count for info
        return len(resumes)

    async def post(self, memory: Memory, resumes_to_process: list, resume_count: int):
        print(f"Mapper: Triggering evaluation for {resume_count} resumes.")
        # Initialize results list and counter in global memory
        memory.evaluations = [None] * resume_count
        memory.remaining_evaluations = resume_count # Add counter
        # Trigger an 'evaluate_resume' action for each resume
        for index, (filename, content) in enumerate(resumes_to_process):
            self.trigger('evaluate_resume', { "filename": filename, "content": content, "index": index })
        # NOTE: 'aggregate_results' is now triggered by EvaluateOneResumeNode when the counter reaches zero.

# 2. Processor Node: Evaluates a single resume
class EvaluateOneResumeNode(Node):
    """Node to evaluate a single resume."""

    async def prep(self, memory: Memory):
        # Read specific resume data from local memory (passed via forkingData)
        return memory.filename, memory.content, memory.index

    async def exec(self, prep_res):
        filename, content, index = prep_res
        # Evaluate the resume
        print(f"Processor: Evaluating {filename} (Index {index})")
        prompt = f"""
Evaluate the following resume and determine if the candidate qualifies for an advanced technical role.
Criteria for qualification:
- At least a bachelor's degree in a relevant field
- At least 3 years of relevant work experience
- Strong technical skills relevant to the position

Resume:
{content}

Return your evaluation in YAML format:
```yaml
candidate_name: [Name of the candidate]
qualifies: [true/false]
reasons:
  - [First reason for qualification/disqualification]
  - [Second reason, if applicable]
```
"""
        response = call_llm(prompt)
        
        # Extract YAML content
        yaml_content = response.split("```yaml")[1].split("```")[0].strip() if "```yaml" in response else response
        result = yaml.safe_load(yaml_content)

        return {"filename": filename, "evaluation": result, "index": index}

    async def post(self, memory: Memory, prep_res, evaluation_result: dict):
        filename, content, index = prep_res
        # Store individual evaluation result in global memory at the correct index
        print(f"Processor: Finished {filename} (Index {evaluation_result['index']})")
        # Decrement counter and trigger aggregate if this is the last evaluation
        # Use a lock to prevent race conditions when multiple nodes update shared memory concurrently.
        # Without the lock, two nodes could read remaining_evaluations, both see it > 0,
        # decrement it, and potentially both miss the condition to trigger the aggregation.
        async with _get_flow_lock(memory):
            memory.evaluations[evaluation_result["index"]] = evaluation_result
            memory.remaining_evaluations -= 1
            is_last = memory.remaining_evaluations == 0
        if is_last:
            print("Processor: All evaluations collected, triggering aggregate.")
            self.trigger('aggregate_results')
        else:
            self.trigger("default") # Continue in sequential flow (though aggregate_results handles the next step)

# 3. Reducer Node: Aggregates individual evaluation results
class AggregateResultsNode(Node):
    """Node to aggregate individual evaluation results."""

    async def prep(self, memory: Memory):
        # Read the array of individual results (filter out None if any failed)
        results = [r for r in (memory.evaluations or []) if r is not None]
        return results

    async def exec(self, evaluation_results_list: list):
        print(f"Reducer: Aggregating {len(evaluation_results_list)} evaluation results.")
        qualified_count = 0
        total_count = len(evaluation_results_list)
        qualified_candidates = []

        for result in evaluation_results_list:
            evaluation = result.get("evaluation", {})
            if evaluation.get("qualifies", False):
                qualified_count += 1
                qualified_candidates.append(evaluation.get("candidate_name", "Unknown"))

        summary = {
            "total_candidates": total_count,
            "qualified_count": qualified_count,
            "qualified_percentage": round(qualified_count / total_count * 100, 1) if total_count > 0 else 0,
            "qualified_names": qualified_candidates
        }

        return summary

    async def post(self, memory: Memory, prep_res, final_summary: dict):
        # Store the final aggregated summary
        memory.summary = final_summary
        print("Reducer: Evaluation aggregation complete.")
        self.trigger("default") # Move to the next step (e.g., print summary)

# Assuming a PrintSummaryNode is defined elsewhere or will be created later
# class PrintSummaryNode(Node): ...
