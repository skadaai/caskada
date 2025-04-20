# Sequential vs Parallel Processing

Demonstrates how using a ParallelFlow with Trigger and Processor nodes accelerates processing by 3x over a sequential Flow.

## Features

- Processes identical tasks with two approaches using Trigger and Processor nodes within Flow and ParallelFlow
- Compares sequential vs parallel execution time
- Shows 3x speed improvement with parallel processing

## Run It

```bash
pip install brainyflow
python main.py
```

## Output

```
=== Running Sequential ===
Trigger: Triggering summary for 3 files.
Processor: Summarizing file1.txt (Index 0)...
Processor: Summarizing file2.txt (Index 1)...
Processor: Summarizing file3.txt (Index 2)...

=== Running Parallel ===
Trigger: Triggering summary for 3 files.
Processor: Summarizing file1.txt (Index 0)...
Processor: Summarizing file2.txt (Index 1)...
Processor: Summarizing file3.txt (Index 2)...

--- Results ---
Sequential Summaries: {'file1.txt': 'Summarized(13 chars)', 'file2.txt': 'Summarized(13 chars)', 'file3.txt': 'Summarized(13 chars)'}
Parallel Summaries:   {'file1.txt': 'Summarized(13 chars)', 'file2.txt': 'Summarized(13 chars)', 'file3.txt': 'Summarized(13 chars)'}
Sequential took: 3.00 seconds
Parallel took:   1.00 seconds
```

## Key Points

- **Sequential Flow**: Total time = sum of all item times

  - Good for: Rate-limited APIs, maintaining order

- **Parallel Flow**: Total time ≈ longest single item time
  - Good for: I/O-bound tasks, independent operations

## Tech Dive Deep

- **Python's GIL** prevents true CPU-bound parallelism, but LLM calls are I/O-bound
- **Async/await** overlaps waiting time between requests
  - Example: `await client.chat.completions.create(...)`
  - See: [OpenAI's async usage](https://github.com/openai/openai-python?tab=readme-ov-file#async-usage)

For maximum performance and cost efficiency, consider using batch APIs:

- [OpenAI's Batch API](https://platform.openai.com/docs/guides/batch) lets you process multiple prompts in a single request
- Reduces overhead and can be more cost-effective for large workloads
