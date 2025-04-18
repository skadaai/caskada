# Getting Started with BrainyFlow

Welcome to BrainyFlow! This framework helps you build powerful, modular AI applications using a simple yet expressive abstraction based on nested directed graphs.

## 1. Installation

First, ensure you have BrainyFlow installed:

{% tabs %}
{% tab title="Python" %}

```bash
pip install brainyflow
```

{% endtab %}

{% tab title="TypeScript" %}

```bash
npm install brainyflow
```

{% endtab %}
{% endtabs %}

For more installation options, see the [Installation Guide](./installation.md).

## 2. Core Concepts

BrainyFlow is built around a minimalist yet powerful abstraction that separates data flow from computation:

- **[Node](./core_abstraction/node.md)**: The fundamental building block that performs a single task with a clear lifecycle (`prep` → `exec` → `post`).
- **[Flow](./core_abstraction/flow.md)**: Orchestrates nodes in a directed graph, supporting branching, looping, and nesting.
- **[Memory](./core_abstraction/memory.md)**: Manages state, separating it into a shared `global` store and a forkable `local` store for isolated data flow between nodes.

## 3. Your First Flow

Let's build a simple Question-Answering flow to demonstrate BrainyFlow's core concepts:

### Step 1: Design Your Flow

Our flow will have two nodes:

1. `GetQuestionNode`: Captures the user's question
2. `AnswerNode`: Generates an answer using an LLM

```mermaid
graph LR
    A[GetQuestionNode] --> B[AnswerNode]
```

### Step 2: Implement the Nodes

{% tabs %}
{% tab title="Python" %}

```python
from brainyflow import Node
from utils import call_llm  # Your LLM implementation

class GetQuestionNode(Node):
    async def prep(self, memory):
        """Get text input from user."""
        memory.question = input("Enter your question: ")

class AnswerNode(Node):
    async def prep(self, memory):
        """Extract the question from memory."""
        return memory.question

    async def exec(self, question):
        """Call LLM to generate an answer."""
        return await call_llm(question)

    async def post(self, memory, prep_res, exec_res):
        """Store the answer in memory."""
        memory.answer = exec_res
        self.trigger('default')  # Explicitly trigger next node
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
import { Node } from 'brainyflow'
import { input } from '@inquirer/prompts'
import { callLLM } from './utils/callLLM' // Your LLM implementation

class GetQuestionNode extends Node {
  async prep(memory): Promise {
    memory.question = await input({ message: 'Enter your question: ' })
  }
}

class AnswerNode extends Node {
  async prep(memory): Promise {
    return memory.question
  }

  async exec(question: string): Promise {
    return await callLLM(question)
  }

  async post(memory, prepRes: string, execRes: string): Promise {
    memory.answer = execRes
  }
}
```

{% endtab %}
{% endtabs %}

{% hint style="info" %}

**Review:** What was achieved here?

- `GetQuestionNode` writes the user's question to the `shared` store.
- `AnswerNode` reads the question from the `shared` store, calling an LLM utility, and writing the answer back to the `shared` store.

{% endhint %}

### Step 3: Connect the Nodes into a Flow

{% tabs %}
{% tab title="Python" %}

```python
from brainyflow import Flow

def create_qa_flow():
    get_question_node = GetQuestionNode()
    answer_node = AnswerNode()

    # Connect nodes get_question_node → answer_node using the default action
    get_question_node >> answer_node  # >> is shorthand for .on('default', node)

    # Create the Flow, specifying the starting node
    # The Flow itself can be typed with the GlobalStore structure
    return Flow(start=get_question_node)
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
import { Flow } from 'brainyflow'

function createQaFlow(): Flow {
  const getQuestionNode = new GetQuestionNode()
  const answerNode = new AnswerNode()

  // Connect nodes getQuestionNode → answerNode using the default action
  getQuestionNode.next(answerNode) // .next() is shorthand for .on('default', node)

  // Create the Flow, specifying the starting node
  // The Flow itself can be typed with the GlobalStore structure
  return new Flow(getQuestionNode)
}
```

{% endtab %}
{% endtabs %}

{% hint style="info" %}

**Review:** What was achieved here?

- We created a flow that connects the nodes, letting the user's question propagate from `GetQuestionNode` to `AnswerNode` to generate an answer.

{% endhint %}

### Step 4: Run the Flow

{% tabs %}
{% tab title="Python" %}

```python
import asyncio

async def main():
    shared = {}  # Initialize empty shared store (can be an empty dict)
    qa_flow = create_qa_flow()


    # Run the flow, passing the initial global store.
    # The run method returns the final execution tree, but we can
    # access the final state directly from our initial globalStore object.
    await qa_flow.run(shared)

    # Access the results stored in the global store
    print(f"Question: {shared.question}")
    print(f"Answer: {shared.answer}")

if __name__ == '__main__':
    asyncio.run(main())
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
async function main() {
  // Initialize the global store (can be an empty object)
  const globalStore: QAGlobalStore = {}
  const qaFlow = createQaFlow()

  // Run the flow, passing the initial global store.
  // The run method returns the final execution tree, but we can
  // access the final state directly from our initial globalStore object.
  await qaFlow.run(globalStore)

  // Access the results stored in the global store
  console.log(`Question: ${globalStore.question}`)
  console.log(`Answer: ${globalStore.answer}`)
}

main().catch(console.error)
```

{% endtab %}
{% endtabs %}

{% hint style="info" %}

**Review:** What was achieved here?

- `qaFlow.run(globalStore)` executed the flow. The `Memory` instance managed the state, and the final `question` and `answer` are available in the `globalStore` object we passed in.

{% endhint %}

## 4. Key Design Principles

BrainyFlow follows these core design principles:

1. **Separation of Concerns**: Data storage (shared store) is separate from computation logic (`Node` classes).
2. **Explicit Data Flow**: Data dependencies between steps are clear and traceable through `Memory` access and `prep`/`exec`/`post` results.
3. **Composability**: Complex systems (`Flow`s) are built from simple, reusable components (`Node`s), and Flows can be nested.
4. **Minimalism**: The framework provides only essential abstractions (`Node`, `Flow`, `Memory`), avoiding vendor-specific implementations.

## 5. Next Steps

Now that you understand the basics, explore these resources to build sophisticated applications:

- [Core Abstractions](./core_abstraction/index.md): Dive deeper into nodes, flows, and communication
- [Design Patterns](./design_pattern/index.md): Learn more complex patterns like Agents, RAG, and MapReduce
- [Agentic Coding Guide](./guides/agentic_coding.md): Best practices for human-AI collaborative development
- [Best Practices](./guides/best_practices.md): Tips for building robust, maintainable applications
