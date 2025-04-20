# Resume Qualification - Map Reduce Example

A BrainyFlow example that demonstrates how to implement a Map-Reduce pattern for processing and evaluating resumes.

## Features

- Read and process multiple resume files using a Map-Reduce pattern
- Evaluate each resume individually using an LLM with structured YAML output
- Determine if candidates qualify for technical roles based on specific criteria
- Aggregate results to generate qualification statistics and summaries

## Getting Started

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY=your_api_key_here
```

3. Run the application:

```bash
python main.py
```

## How It Works

The workflow follows a classic Map-Reduce pattern implemented using standard BrainyFlow Nodes and a ParallelFlow for concurrent processing:

```mermaid
flowchart LR
    ReadResumes[Read Resumes] --> TriggerEvaluations[Map: Trigger Evaluations]
    TriggerEvaluations -->|evaluate_resume| EvaluateOneResume[Process: Evaluate One Resume]
    EvaluateOneResume -->|aggregate_results| AggregateResults[Reduce: Aggregate Results]
```

Here's what each node does:

1.  **`ReadResumesNode`**: Reads all resume files from the data directory and stores them in memory.
2.  **`TriggerEvaluationsNode` (Map Phase)**: Reads the resume data from memory and triggers an `evaluate_resume` action for each resume, passing the resume content and index to the local memory of the next node.
3.  **`EvaluateOneResumeNode` (Processor Node)**: Receives a single resume from its local memory, evaluates it using an LLM, stores the result in global memory at the correct index, and triggers the `aggregate_results` action when all evaluations are complete.
4.  **`AggregateResultsNode` (Reduce Phase)**: Reads all the individual evaluation results from global memory, aggregates them into a final summary of qualified candidates, and stores the summary in memory.

This pattern demonstrates how BrainyFlow can efficiently process multiple related tasks concurrently using standard nodes and flows, replacing the need for specialized batch node types.

## Files

- [`main.py`](./main.py): Main entry point for running the resume qualification workflow
- [`flow.py`](./flow.py): Defines the flow that connects the nodes
- [`nodes.py`](./nodes.py): Contains the node classes for each step in the workflow
- [`utils.py`](./utils.py): Utility functions including the LLM wrapper
- [`requirements.txt`](./requirements.txt): Lists the required dependencies
- [`data/`](./data/): Directory containing sample resume files for evaluation

## Example Output

```
Starting resume qualification processing...

===== Resume Qualification Summary =====
Total candidates evaluated: 5
Qualified candidates: 2 (40.0%)

Qualified candidates:
- Emily Johnson
- John Smith

Detailed evaluation results:
✗ Michael Williams (resume3.txt)
✓ Emily Johnson (resume2.txt)
✗ Lisa Chen (resume4.txt)
✗ Robert Taylor (resume5.txt)
✓ John Smith (resume1.txt)

Resume processing complete!
```
