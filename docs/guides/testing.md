# Testing and Debugging BrainyFlow Applications

Effective testing and debugging are essential for building reliable applications. This guide covers strategies for testing and debugging complex flows, and monitoring applications in production.

## Testing Approaches

BrainyFlow supports multiple testing approaches to ensure your applications work correctly:

### Unit Testing (Nodes)

Individual nodes can be tested in isolation to verify their behavior:

{% tabs %}
{% tab title="Python" %}

```python
import unittest
from unittest.mock import AsyncMock, patch
from brainyflow import Node

class TestSummarizeNode(unittest.TestCase):
    async def test_summarize_node(self):
        # Create the node
        summarize_node = SummarizeNode()

        # Create a mock shared store
        shared = {"text": "This is a long text that needs to be summarized."}

        # Mock the LLM call
        with patch('utils.call_llm', new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = "Short summary."

            # Run the node
            await summarize_node.run(shared)

            # Verify the node called the LLM with the right prompt
            mock_llm.assert_called_once()
            call_args = mock_llm.call_args[0][0]
            self.assertIn("summarize", call_args.lower())

            # Verify the result was stored correctly
            self.assertEqual(shared["summary"], "Short summary.")

if __name__ == '__main__':
    unittest.main()
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
import { describe, expect, it, vi } from 'vitest'
import { SummarizeNode } from './SummarizeNode' // Your Node implementation
import { callLLM } from './utils/callLLM' // Your LLM utility

// Mock the LLM utility
vi.mock('./utils/callLLM', () => ({
  callLLM: vi.fn().mockResolvedValue('Short summary.'),
}))

describe('SummarizeNode', () => {
  it('should summarize text correctly', async () => {
    // Create the node instance
    const summarizeNode = new SummarizeNode()

    // Create initial global memory state
    const shared = { text: 'This is a long text that needs to be summarized.' }

    // Run the node's lifecycle (prep -> exec -> post)
    await summarizeNode.run(shared)

    // Verify the LLM call
    expect(callLLM).toHaveBeenCalledTimes(1)
    const callArgs = vi.mocked(callLLM).mock.calls[0][0] // Get the first argument of the first call
    expect(callArgs.toLowerCase()).toContain('summarize') // Check if prompt contains 'summarize'

    // Verify the result was stored correctly in the global memory object
    expect(shared.summary).toBe('Short summary.')
  })
})
```

{% endtab %}
{% endtabs %}

### Integration Testing (Flows)

Test complete flows to verify that nodes work together correctly:

{% tabs %}
{% tab title="Python" %}

```python
import unittest
from unittest.mock import AsyncMock, patch
from brainyflow import Flow

class TestQuestionAnsweringFlow(unittest.TestCase):
    async def test_qa_flow(self):
        # Create the flow
        qa_flow = create_qa_flow()

        # Create a mock shared store
        shared = {"question": "What is the capital of France?"}

        # Mock all LLM calls
        with patch('utils.call_llm', new_callable=AsyncMock) as mock_llm:
            # Configure the mock to return different values for different prompts
            def mock_llm_side_effect(prompt):
                if "search" in prompt.lower():
                    return "Paris is the capital of France."
                elif "answer" in prompt.lower():
                    return "The capital of France is Paris."
                return "Unexpected prompt"

            mock_llm.side_effect = mock_llm_side_effect

            # Run the flow
            await qa_flow.run(shared)

            # Verify the final answer
            self.assertEqual(shared["answer"], "The capital of France is Paris.")

            # Verify the LLM was called the expected number of times
            self.assertEqual(mock_llm.call_count, 2)

if __name__ == '__main__':
    unittest.main()
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
import { describe, expect, it, vi } from 'vitest'
import { createQaFlow } from './qaFlow' // Your function that creates the Flow
import { callLLM } from './utils/callLLM' // Your LLM utility

// Mock the LLM utility
vi.mock('./utils/callLLM')

describe('Question Answering Flow', () => {
  it('should process questions correctly', async () => {
    // Configure the mock LLM to return different responses based on the prompt
    vi.mocked(callLLM).mockImplementation(async (prompt: string): Promise<string> => {
      // Simulate different stages of a potential QA flow (e.g., search vs. answer)
      if (prompt.toLowerCase().includes('search')) {
        // Example condition
        return 'Paris is the capital of France.'
      } else if (prompt.toLowerCase().includes('answer')) {
        // Example condition
        return 'The capital of France is Paris.'
      }
      return 'Unexpected prompt' // Fallback for other prompts
    })

    // Create the flow instance
    const qaFlow = createQaFlow()

    // Define the initial global memory state for the flow run
    const shared = { question: 'What is the capital of France?' }

    // Run the entire flow
    await qaFlow.run(shared)

    // Verify the final answer stored in the global memory object
    expect(shared.answer).toBe('The capital of France is Paris.')

    // Verify the LLM was called the expected number of times during the flow
    expect(callLLM).toHaveBeenCalledTimes(2) // Adjust based on expected calls in your flow
  })
})
```

{% endtab %}
{% endtabs %}

## Best Practices

### Testing Best Practices

1. **Test Each Node Individually**: Verify that each node performs its specific task correctly
2. **Test Flows as Integration Tests**: Ensure nodes work together as expected
3. **Mock External Dependencies**: Use mocks for LLMs, APIs, and databases to ensure consistent testing
4. **Test Error Handling**: Explicitly test how your application handles failures
5. **Automate Tests**: Include BrainyFlow tests in your CI/CD pipeline

### Debugging Best Practices

1. **Start Simple**: Begin with a minimal flow and add complexity incrementally
2. **Visualize Your Flow**: Generate flow diagrams to understand the structure
3. **Isolate Issues**: Test individual nodes to narrow down problems
4. **Check Shared Store**: Verify that data is correctly passed between nodes
5. **Monitor Actions**: Ensure nodes are returning the expected actions

### Monitoring Best Practices

1. **Monitor Node Performance**: Track execution time for each node
2. **Watch for Bottlenecks**: Identify nodes that take longer than expected
3. **Track Error Rates**: Monitor how often nodes and flows fail
4. **Set Up Alerts**: Configure alerts for critical failures
5. **Log Judiciously**: Log important events without overwhelming storage
6. **Implement Distributed Tracing**: Use tracing for complex, distributed applications

By following these testing, debugging, and monitoring practices, you can build reliable BrainyFlow applications that perform well in production environments.
