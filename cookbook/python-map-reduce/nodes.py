from caskada import Node
from utils import call_llm
import yaml
import os

class Map(Node):
    async def prep(self, memory):
        assert hasattr(memory, "items"), "list of items must be set in memory"
        return memory.items
    
    async def post(self, memory, items, exec_res):
        memory.processed_items = {} if isinstance(items, dict) else [None] * len(items)
        memory.remaining_items = len(items)

        for index, data in (items.items() if isinstance(items, dict) else enumerate(items)):
            self.trigger("default", {"index": index, "data": data})

class Reduce(Node):
    async def prep(self, memory):
        assert hasattr(memory, "index"), "index of processed item must be set in memory"
        assert hasattr(memory, "data"), "processed data must be set in memory"
        return memory.index, memory.data
    
    async def post(self, memory, prep_res, exec_res):
        memory.processed_items[prep_res[0]] = prep_res[1]
        memory.remaining_items -= 1
        if not memory.remaining_items == 0:
            return self.trigger(None)
        
        self.trigger("default", {"data": memory.processed_items})

class ReadResumesNode(Node):
    """Map phase: Read all resumes from the data directory into shared storage."""
    
    async def exec(self, _):
        resume_files = {}
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        
        for filename in os.listdir(data_dir):
            if filename.endswith(".txt"):
                file_path = os.path.join(data_dir, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    resume_files[filename] = file.read()
        
        return resume_files
    
    async def post(self, shared, prep_res, exec_res):
        self.trigger("default", {"items": exec_res})


class EvaluateResumesNode(Node):
    """Batch processing: Evaluate each resume to determine if the candidate qualifies."""
    
    async def prep(self, memory):
        return memory.index, memory.data
    
    async def exec(self, item):
        """Evaluate a single resume."""
        filename, content = item
        
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

IMPORTANT: Make sure to:
1. Use proper indentation (4 spaces) for all multi-line fields
2. Use the | character for multi-line text fields
3. Keep single-line fields without the | character
4. Your answer must be wrapped in yaml code block or it will result in an error. Do not forget to include the ```yaml sequence at the beginning and end it with ```.
"""
        response = call_llm(prompt)
        assert "```yaml" in response, "Response must contain yaml block"
        
        # Extract YAML content
        yaml_content = response.split("```yaml")[1].split("```")[0].strip() if "```yaml" in response else response
        result = yaml.safe_load(yaml_content)
        
        return (filename, result)

    async def post(self, shared, prep_res, exec_res):
        self.trigger("default", { "index": exec_res[0], "data": exec_res[1]})


class ResultsNode(Node):
    """Results: Count and print out how many candidates qualify."""
    
    async def prep(self, memory):
        return memory.data
    
    async def exec(self, evaluations):
        qualified_count = 0
        total_count = len(evaluations)
        qualified_candidates = []
        
        for evaluation in evaluations.values():
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
    
    async def post(self, shared, prep_res, exec_res):
        shared["summary"] = exec_res
        
        print("\n===== Resume Qualification Summary =====")
        print(f"Total candidates evaluated: {exec_res['total_candidates']}")
        print(f"Qualified candidates: {exec_res['qualified_count']} ({exec_res['qualified_percentage']}%)")
        
        if exec_res['qualified_names']:
            print("\nQualified candidates:")
            for name in exec_res['qualified_names']:
                print(f"- {name}")
        