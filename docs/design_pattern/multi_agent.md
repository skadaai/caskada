---
machine-display: false
---

# Multi-Agent Systems

Multi-agent systems involve multiple autonomous agents (or sub-flows) that interact and collaborate to achieve a common goal. Caskada's modularity and flexible communication mechanisms make it well-suited for building such systems.

{% hint style="success" %}
Most of time, you don't need Multi-Agents. Start with a simple solution first.
{% endhint %}

## Key Concepts

1.  **Agent Specialization**: Each agent (or sub-flow) can be designed with a specific role or expertise (e.g., a "researcher" agent, a "coder" agent, a "critic" agent).
2.  **Communication Channels**: Agents need ways to exchange information. This can be achieved through:
    - **Shared Memory**: Agents read from and write to a common `Memory` object.
    - **Message Queues**: Agents send and receive structured messages through a queue (e.g., `asyncio.Queue` in Python, custom `AsyncQueue` in TypeScript).
    - **Dedicated Nodes**: A "broker" or "router" node can facilitate communication between agents.
3.  **Orchestration**: A higher-level flow or a "supervisor" agent can manage the interaction and execution order of individual agents.

## Example: Simple Message-Passing Agents

Let's create a simple multi-agent system where agents communicate via a shared message queue.

For simplicity, these will be overly-simplified mock tools/nodes. For a more in-depth implementation, check the implementations in our cookbook for [Multi-Agent Taboo Game (Python)](https://github.com/skadaai/caskada/tree/main/cookbook/python-multi-agent) or [Agent with A2A Protocol (Python)](https://github.com/skadaai/caskada/tree/main/cookbook/python-a2a) - _more TypeScript examples coming soon ([PRs welcome](https://github.com/skadaai/caskada)!)_.

### 1. Define Agent Node

This node represents an individual agent that processes messages from a queue.

{% tabs %}
{% tab title="Python" %}

```python
import asyncio
from brainyflow import Node

class AgentNode(Node):
    async def prep(self, memory):
        # We'll store the queue in global memory for simplicity here,
        # though in real apps, dependency injection might be better.
        message_queue = memory.message_queue
        if message_queue.empty():
            print("AgentNode: Queue is empty, waiting...")
            # In a real app, you might want a timeout or a more sophisticated wait
            await asyncio.sleep(1) # Small delay to prevent busy-waiting
            return None # No message to process yet

        message = await message_queue.get()
        print(f"AgentNode: Received message: {message}")
        return message

    async def exec(self, message: str):
        # Simulate processing the message
        processed_message = f"Processed: {message.upper()}"
        return processed_message

    async def post(self, memory, prep_res: str, exec_res: str):
        if prep_res: # Only trigger if a message was processed
            memory.last_processed_message = exec_res
            print(f"AgentNode: Stored processed message: {exec_res}")
            self.trigger("default") # Continue processing
        else:
            # If no message was processed, re-trigger self to check queue again
            self.trigger("check_queue")
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
import { Flow, Node } from 'brainyflow'

class AgentNode extends Node {
  // We'll store the queue in global memory for simplicity here,
  // though in real apps, dependency injection might be better.
  async prep(memory): Promise<string | null> {
    const messageQueue = memory.messageQueue as AsyncQueue
    if (messageQueue.isEmpty()) {
      console.log('AgentNode: Queue is empty, waiting...')
      // In a real app, you might want a timeout or a more sophisticated wait
      await new Promise((resolve) => setTimeout(resolve, 1000)) // Small delay
      return null // No message to process yet
    }

    const message = await messageQueue.dequeue()
    console.log(`AgentNode: Received message: ${message}`)
    return message
  }

  async exec(message: string | null): Promise<string | null> {
    if (message === null) return null
    // Simulate processing the message
    const processedMessage = `Processed: ${message.toUpperCase()}`
    return processedMessage
  }

  async post(memory, prepRes: string | null, execRes: string | null): Promise<void> {
    if (prepRes !== null) {
      // Only trigger if a message was processed
      memory.last_processed_message = execRes
      console.log(`AgentNode: Stored processed message: ${execRes}`)
      this.trigger('default') // Continue processing
    } else {
      // If no message was processed, re-trigger self to check queue again
      this.trigger('check_queue')
    }
  }
}
```

{% endtab %}
{% endtabs %}

### 2. Define Message Sender (External Process)

This function simulates an external system sending messages to the queue.

{% tabs %}
{% tab title="Python" %}

```python
import asyncio

async def send_system_messages(queue: asyncio.Queue):
    messages = ["Hello Agent 1", "Task A", "Task B", "Shutdown"]
    for i, msg in enumerate(messages):
        await asyncio.sleep(0.5) # Simulate delay
        await queue.put(msg)
        print(f"System: Sent message: {msg}")
        if msg == "Shutdown":
            break
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
class AsyncQueue<T> {
  private queue: T[] = []
  private resolvers: ((value: T) => void)[] = []

  enqueue(item: T) {
    if (this.resolvers.length > 0) {
      const resolver = this.resolvers.shift()
      if (resolver) {
        resolver(item)
      }
    } else {
      this.queue.push(item)
    }
  }

  dequeue(): Promise<T> {
    if (this.queue.length > 0) {
      return Promise.resolve(this.queue.shift()!)
    } else {
      return new Promise((resolve) => this.resolvers.push(resolve))
    }
  }

  isEmpty(): boolean {
    return this.queue.length === 0 && this.resolvers.length === 0
  }
}

async function sendSystemMessages(queue: AsyncQueue<string>) {
  const messages = ['Hello Agent 1', 'Task A', 'Task B', 'Shutdown']
  for (const msg of messages) {
    await new Promise((resolve) => setTimeout(resolve, 500)) // Simulate delay
    queue.enqueue(msg)
    console.log(`System: Sent message: ${msg}`)
    if (msg === 'Shutdown') {
      break
    }
  }
}
```

{% endtab %}
{% endtabs %}

### 3. Assemble the Flow and Run

We create a flow where the `AgentNode` loops back to itself to continuously check the message queue.

{% tabs %}
{% tab title="Python" %}

```python
import asyncio
from brainyflow import Flow, Memory

# Instantiate agent node
agent_node = AgentNode()

# Agent loops back to itself to keep checking the queue
agent_node >> agent_node # After processing, check again
agent_node - "check_queue" >> agent_node # If queue was empty, check again

flow = Flow(start=agent_node)

async def main():
    message_queue = asyncio.Queue()
    # Pass queue via initial memory object
    memory_obj = Memory(global_store={"message_queue": message_queue})

    print("Starting agent listener and message sender...")
    # Run both coroutines
    # Note: This will run indefinitely without a termination mechanism
    await asyncio.gather(
        flow.run(memory_obj),
        send_system_messages(message_queue)
    )

if __name__ == "__main__":
    asyncio.run(main())
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
import { Flow, Memory, Node } from 'brainyflow'

// (AgentNode and AsyncQueue definitions as above)

// Instantiate agent node
const agentNode = new AgentNode()

// Agent loops back to itself to keep checking the queue
agentNode.next(agentNode) // After processing, check again
agentNode.on('check_queue', agentNode) // If queue was empty, check again

const agentFlow = new Flow(agentNode)

async function main() {
  const messageQueue = new AsyncQueue()
  // Pass the queue via the shared memory
  const memory = { messageQueue }

  console.log('Starting agent listener and message sender...')
  // Run the agent flow and the message sender concurrently
  // Note: This will run indefinitely without a termination mechanism
  await Promise.all([agentFlow.run(memory), sendSystemMessages(messageQueue)])
}

main().catch(console.error)
```

{% endtab %}
{% endtabs %}

This example demonstrates a basic multi-agent setup using a shared message queue and a looping flow.

This pattern demonstrates several key advantages:

1. **Specialization**: Each agent can focus on a specific task
2. **Independence**: Agents can operate on different schedules or priorities
3. **Coordination**: Agents can collaborate through shared memory and queues
4. **Flexibility**: Easy to add new agents or modify existing ones
5. **Scalability**: The system can grow to include many specialized agents

More complex multi-agent systems can be built by introducing:

- **Supervisor Flows**: A main flow that orchestrates multiple sub-flows (agents).
- **Tool Calling**: Agents can use tools to interact with external systems or other agents.
- **Shared Global State**: Beyond message queues, agents can update a shared global memory for broader coordination.
- **Dynamic Agent Creation**: Agents could dynamically create and manage other agents based on task requirements.
