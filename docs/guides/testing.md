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
        memory = {"text": "This is a long text that needs to be summarized."}

        # Mock the LLM call
        with patch('utils.call_llm', new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = "Short summary."

            # Run the node
            await summarize_node.run(memory)

            # Verify the node called the LLM with the right prompt
            mock_llm.assert_called_once()
            call_args = mock_llm.call_args[0][0]
            self.assertIn("summarize", call_args.lower())

            # Verify the result was stored correctly
            self.assertEqual(memory.summary, "Short summary.") # Access memory object

if __name__ == "__main__":
    # Use asyncio.run for async tests if needed, or run within an existing loop
    # For simplicity, assuming standard unittest runner handles async test cases
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
    const memory = { text: 'This is a long text that needs to be summarized.' }

    // Run the node's lifecycle (prep -> exec -> post)
    await summarizeNode.run(memory) // Pass memory object

    // Verify the LLM call
    expect(callLLM).toHaveBeenCalledTimes(1)
    const callArgs = vi.mocked(callLLM).mock.calls[0][0] // Get the first argument of the first call
    expect(callArgs.toLowerCase()).toContain('summarize') // Check if prompt contains 'summarize'

    // Verify the result was stored correctly in the global memory object
    expect(memory.summary).toBe('Short summary.') // Access memory object
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
        memory = {"question": "What is the capital of France?"}

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
            await qa_flow.run(memory)

            # Verify the final answer
            self.assertEqual(memory.answer, "The capital of France is Paris.") # Access memory object

            # Verify the LLM was called the expected number of times
            self.assertEqual(mock_llm.call_count, 2)

if __name__ == '__main__':
    # Use asyncio.run for async tests if needed
    unittest.main()
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { createQaFlow } from './qaFlow' // Your function that creates the Flow
import { callLLM } from './utils/callLLM' // Your LLM utility

// Mock the LLM utility
vi.mock('./utils/callLLM', () => ({
  callLLM: vi.fn(),
}))

describe('Question Answering Flow', () => {
  beforeEach(() => {
    // Clear any previous mock calls before each test
    vi.clearAllMocks()
  })

  it('should generate an answer using the flow', async () => {
    // Configure mock to return different values based on the prompt
    vi.mocked(callLLM).mockImplementation((prompt: string) => {
      // Simulate different stages of a potential QA flow (e.g., search vs. answer)
      if (prompt.toLowerCase().includes('search')) {
        return Promise.resolve('Paris is the capital of France.')
      } else if (prompt.toLowerCase().includes('answer')) {
        return Promise.resolve('The capital of France is Paris.')
      }
      return Promise.resolve('Unexpected prompt')
    })

    // Create the flow
    const qaFlow = createQaFlow()

    // Create initial memory state
    const memory = { question: 'What is the capital of France?' }

    // Run the flow
    await qaFlow.run(memory) // Pass memory object

    // Verify the final answer
    expect(memory.answer).toBe('The capital of France is Paris.') // Access memory object

    // Verify the LLM was called the expected number of times
    expect(callLLM).toHaveBeenCalledTimes(2)

    // Verify the calls were made with appropriate prompts
    const calls = vi.mocked(callLLM).mock.calls
    const retrieveCall = calls.some(
      (call) => typeof call === 'string' && call.toLowerCase().includes('retrieve'),
    )
    const generateCall = calls.some(
      (call) => typeof call === 'string' && call.toLowerCase().includes('generate'),
    )

    expect(retrieveCall).toBe(true)
    expect(generateCall).toBe(true)
  })
})

// Example testing a MapReduce flow (Trigger, Processor, Reducer)
describe('MapReduce Flow Test', () => {
  // Mock the nodes used in the MapReduce example
  const TriggerNode = class extends Node {
    async post(memory: Memory, prepRes: any, execRes: any): Promise<void> {
      const items = memory.items || []
      memory.results = [] // Initialize results
      items.forEach((item: any, index: number) => {
        this.trigger('process_item', { item, index })
      })
      this.trigger('reduce')
    }
  }
  const ProcessorNode = class extends Node {
     async prep(memory: Memory): Promise<any> { return { item: memory.item, index: memory.index }; }
     async exec(prepRes: { item: any, index: number }): Promise<string> { return `Processed ${prepRes.item}`; }
     async post(memory: Memory, prepRes: { item: any, index: number }, execRes: string): Promise<void> {
         if (!memory.results) memory.results = [];
         // Store result at the correct index if possible, or just push
         memory.results[prepRes.index] = execRes;
     }
  }
  const ReducerNode = class extends Node {
     async prep(memory: Memory): Promise<any[]> { return memory.results || []; }
     async exec(results: any[]): Promise<string> { return `Combined: ${results.join(', ')}`; }
     async post(memory: Memory, prepRes: any, execRes: string): Promise<void> { memory.final_result = execRes; }
  }

  it('should process items via map and reduce steps', async () => {
    // Instantiate nodes
    const trigger = new TriggerNode()
    const processor = new ProcessorNode()
    const reducer = new ReducerNode()

    // Connect nodes
    trigger.on('process_item', processor)
    trigger.on('reduce', reducer) // This action is triggered after all 'process_item'

    // Use ParallelFlow for the map phase
    const mapReduceFlow = new ParallelFlow(trigger)

    // Initial memory
    const memory = { items: ['A', 'B', 'C'] }

    // Run the flow
    await mapReduceFlow.run(memory)

    // Verify final result in memory
    expect(memory.results).toEqual(['Processed A', 'Processed B', 'Processed C'])
    expect(memory.final_result).toBe('Combined: Processed A, Processed B, Processed C')
  })
})

{% endtab %}
{% endtabs %}

## Testing Approaches

### Unit Testing Individual Nodes

1. **Isolate Dependencies**: Mock external services and LLM calls
2. **Test Each Lifecycle Method**: Verify `prep`, `exec`, and `post` individually
3. **Test Error Handling**: Ensure `exec_fallback` works as expected
4. **Verify Memory Updates**: Check if memory is modified correctly
5. **Test Triggers**: Ensure the right actions are triggered

### Integration Testing Flows

1. **Mock External Services**: Keep tests deterministic by mocking APIs
2. **Verify End-to-End Behavior**: Test the entire flow from start to finish
3. **Test Branching Logic**: Ensure different paths work correctly
4. **Check Final Memory State**: Verify that the memory contains expected results
5. **Test Error Handling**: Make sure flows handle errors gracefully

### Testing Strategies

#### Testing LLM-Based Nodes

For nodes that call LLMs, you can use these approaches:

1. **Canned Responses**: Prepare fixed responses for specific prompts
2. **Prompt Verification**: Check if prompts contain expected information
3. **Response Validation**: Test if the node correctly handles various LLM responses

```

# Mock LLM with canned responses

def mock_llm(prompt):
if "summarize" in prompt.lower():
return "This is a summary."
elif "extract" in prompt.lower():
return "{'key': 'value'}"
else:
return "Default response"

# Use mock in test

with patch('utils.call_llm', side_effect=mock_llm): # Run node or flow
pass

```

#### Testing Retry Logic

To test retry behavior:

1. **Simulate Transient Failures**: Make the mock function fail a few times before succeeding
2. **Check Retry Count**: Verify that retries happened the expected number of times
3. **Test Backoff**: Ensure that wait times between retries are correct

```

# Mock that fails twice, then succeeds

call_count = 0
def failing_mock(\*args):
global call_count
call_count += 1
if call_count <= 2:
raise Exception("Temporary failure")
return "Success on third try"

# Use in test

with patch('some_function', side_effect=failing_mock): # Run node with retry logic
pass

```

## Test Fixtures and Helpers

Creating helper functions can make tests more readable and maintainable:

```

# Helper to create a standard test memory

def create_test_memory():
return {"input": "test data", "config": {"setting": "value"}}

# Helper to run a node with standard setup

async def run_test_node(node, memory=None):
if memory is None:
memory = create_test_memory()
return await node.run(memory)

# Helper to check memory structure

def assert_memory_has_fields(memory, \*fields): # Check if properties exist on the memory object
for field in fields:
assert hasattr(memory, field), f"Memory missing field: {field}"

```

## Common Testing Patterns

### 1. Input Validation Testing

Test that nodes properly handle invalid inputs:

```

@pytest.mark.parametrize("input_value", [None, "", {}, []])
async def test_node_handles_invalid_input(input_value):
node = MyNode() # Assuming MyNode handles invalid input appropriately
memory = Memory.create({"input": input_value}) # Create memory object

    # Should not raise exception (or handle it gracefully)
    await node.run(memory)

    # Check for an error flag or expected state in memory
    assert hasattr(memory, "error") or memory.state == "handled_invalid" # Example assertion

```

### 2. Flow Path Testing

Test that flows follow the expected paths:

```

async def test_flow_follows_success_path(): # Create flow with mocks that track which nodes were visited
visited_nodes = []

    class TrackingNode(Node):
        def __init__(self, name):
            super().__init__()
            self.name = name

        async def post(self, memory, prep_res, exec_res):
            visited_nodes.append(self.name)
            self.trigger("default")

    # Create flow with tracking nodes
    node1 = TrackingNode("node1")
    node2 = TrackingNode("node2")
    node3 = TrackingNode("node3")

    node1.next(node2)
    node2.next(node3)

    flow = Flow(start=node1)
    await flow.run({}) # Pass empty memory object

    # Verify all nodes were visited in order
    assert visited_nodes == ["node1", "node2", "node3"]

```

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

By applying these testing techniques, you can ensure your BrainyFlow applications are reliable and maintainable.


```
