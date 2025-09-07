---
complexity: 3
---

# Text Summarization

A practical example demonstrating how to use Caskada to build a robust text summarization tool with error handling and retries. This example showcases core Caskada concepts in a real-world application.

## Features

- Text summarization using LLMs (Large Language Models)
- Automatic retry mechanism (up to 3 attempts) on API failures
- Graceful error handling with fallback responses
- Clean separation of concerns using Caskada's Node architecture

## Project Structure

```
.
├── docs/          # Documentation files
├── utils/         # Utility functions (LLM API wrapper)
├── flow.py        # Caskada implementation with Summarize Node
├── main.py        # Main application entry point
└── README.md      # Project documentation
```

## Implementation Details

The example implements a simple but robust text summarization workflow:

1. **Summarize Node** (`flow.py`):

   - `prep()`: Retrieves text from the shared store
   - `exec()`: Calls LLM to summarize text in 10 words
   - `exec_fallback()`: Provides graceful error handling
   - `post()`: Stores the summary back in shared store

2. **Flow Structure**:
   - Single node flow for demonstration
   - Configured with 3 retries for reliability
   - Uses shared store for data passing

## Setup

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure your environment:

   - Set up your LLM API key (check utils/call_llm.py for configuration)

4. Run the example:

```bash
python main.py
```

## Example Usage

The example comes with a sample text about Caskada, but you can modify `main.py` to summarize your own text:

```python
shared = {"data": "Your text to summarize here..."}
await flow.run(shared)
print("Summary:", shared["summary"])
```

## What You'll Learn

This example demonstrates several key Caskada concepts:

- **Node Architecture**: How to structure LLM tasks using prep/exec/post pattern
- **Error Handling**: Implementing retry mechanisms and fallbacks
- **Shared Store**: Using shared storage for data flow between steps
- **Flow Creation**: Setting up a basic Caskada workflow

## Additional Resources

- [Caskada Documentation](https://skadaai.gitbook.io/caskada/)
- [Node Concept Guide](https://skadaai.gitbook.io/caskada/core-abstraction/node)
- [Flow Design Patterns](https://skadaai.gitbook.io/caskada/core-abstraction/flow)
