# Multi-Agent Systems Pattern

The multi-agent pattern enables complex behaviors by coordinating multiple specialized agents. Each agent focuses on a specific capability while communicating through shared memory and queues.

{% hint style="success" %}
Most of time, you don't need Multi-Agents. Start with a simple solution first.
{% endhint %}

## Example: Agent Communication through Message Queue

Here's a simple example showing how to implement agent communication using `asyncio.Queue`.
The agent listens for messages, processes them, and continues listening:

{% tabs %}
{% tab title="Python" %}

```python
import asyncio
from brainyflow import Node, Flow

class AgentNode(Node):
    async def prep(self, memory: Memory):
        message = await message_queue.get()
        print(f"Agent received: {message}")
        return message

# Create node and flow
agent = AgentNode()
agent >> agent  # connect to self
flow = Flow(start=agent)

# Create heartbeat sender
async def send_system_messages(message_queue):
    counter = 0
    messages = [
        "System status: all systems operational",
        "Memory usage: normal",
        "Network connectivity: stable",
        "Processing load: optimal"
    ]

    while True: # In a real app, add a termination condition
        message = f"{messages[counter % len(messages)]} | timestamp_{counter}"
        await message_queue.put(message)
        counter += 1
        await asyncio.sleep(1)

async def main():
    message_queue = asyncio.Queue()
    # Pass queue via initial memory object
    memory = {"message_queue": message_queue}

    print("Starting agent listener and message sender...")
    # Run both coroutines
    # Note: This will run indefinitely without a termination mechanism
    await asyncio.gather(
        flow.run(memory), # Pass memory object
        send_system_messages(message_queue)
    )

asyncio.run(main())
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
import { Flow, Memory, Node } from 'brainyflow'

// Agent node that processes messages from a queue
class AgentNode extends Node {
  // We'll store the queue in global memory for simplicity here,
  // though in real apps, dependency injection might be better.
  async prep(memory: Memory): Promise<string> {
    const messageQueue = memory.messageQueue as AsyncQueue<string>
    if (!messageQueue) throw new Error('Message queue not found in memory')

    const message = await messageQueue.get() // Wait for a message
    console.log(`Agent received: ${message}`)
    return message // Pass message to exec (optional)
  }

  async exec(message: string): Promise<void> {
    // Process the message (optional)
    // console.log(`Agent processing: ${message}`);
  }

  async post(memory: Memory): Promise<void> {
    // Trigger self to listen for the next message
    this.trigger('continue')
  }
}

// --- Flow Setup ---
const agent = new AgentNode()
agent.on('continue', agent) // Loop back to self

const agentFlow = new Flow(agent)

// --- Message Sender ---
async function sendSystemMessages(messageQueue: AsyncQueue<string>) {
  let counter = 0
  const messages = [
    'System status: all systems operational',
    'Memory usage: normal',
    'Network connectivity: stable',
    'Processing load: optimal',
  ]

  while (true) {
    // In a real app, you'd have a termination condition
    const message = `${messages[counter % messages.length]} | timestamp_${counter}`
    await messageQueue.put(message)
    counter++
    await new Promise((resolve) => setTimeout(resolve, 1000)) // Wait 1s
  }
}

// --- Main Execution ---
async function main() {
  const messageQueue = new AsyncQueue<string>()
  // Pass the queue via the shared memory
  const data = { messageQueue }

  console.log('Starting agent listener and message sender...')
  // Run the agent flow and the message sender concurrently
  // Note: This will run indefinitely without a termination mechanism
  await Promise.all([agentFlow.run(data), sendSystemMessages(messageQueue)])
}

class AsyncQueue<T> {
  private queue: T[] = []
  private waiting: ((value: T) => void)[] = []

  async get(): Promise<T> {
    if (this.queue.length > 0) {
      return this.queue.shift()!
    }
    return new Promise((resolve) => {
      this.waiting.push(resolve)
    })
  }

  async put(item: T): Promise<void> {
    if (this.waiting.length > 0) {
      const resolve = this.waiting.shift()!
      resolve(item)
    } else {
      this.queue.push(item)
    }
  }
}

main().catch(console.error)
```

{% endtab %}
{% endtabs %}

The output:

```
Agent received: System status: all systems operational | timestamp_0
Agent received: Memory usage: normal | timestamp_1
Agent received: Network connectivity: stable | timestamp_2
Agent received: Processing load: optimal | timestamp_3
```

## Example: Word Guessing Game (Taboo)

Two agents collaborate in a word guessing game:

- **Hinter**: Provides clues without using forbidden words
- **Guesser**: Attempts to guess the target word based on hints

{% tabs %}
{% tab title="Python" %}

```python
from brainyflow import Node, Flow
from utils import call_llm
import asyncio

class Hinter(Node):
    async def prep(self, memory: Memory):
        """Get the next hint or game state"""
        # Read necessary info from memory
        guess = await memory.guesser_queue.get() # Read from memory queue
        if guess == "GAME_OVER":
            return None # Signal to stop
        return {
            "guess": guess,
            "target_word": memory.target_word, # Pass target word
            "forbidden_words": memory.forbidden_words # Pass forbidden words
        }

    async def exec(self, prep_res):
        """Generate a hint avoiding forbidden words"""
        if prep_res is None:  # Game over signal from prep
            return None

        prompt = f"""
Given target word: {prep_res["target_word"]}
Forbidden words: {prep_res["forbidden_words"]}
Last wrong guess: {prep_res.get('guess')}
Generate a creative hint that helps guess the target word without using forbidden words.
Reply only with the hint text.
"""
        return await call_llm(prompt)

    async def post(self, memory: Memory, prep_res, hint):
        if hint is None:
            self.trigger("end")
            return
        await memory.hinter_queue.put(hint) # Write to memory queue
        self.trigger('continue')

class Guesser(Node):
    async def prep(self, memory: Memory):
        hint = await memory.guesser_queue.get() # Read from memory queue
        # Pass target word for comparison in post
        return {
            "hint": hint,
            "past_guesses": memory.past_guesses if hasattr(memory, 'past_guesses') else [],
            "target_word": memory.target_word
        }

    async def exec(self, prep_res):
        """Make a guess based on the hint"""
        hint = prep_res["hint"]
        past_guesses = prep_res["past_guesses"]
        prompt = f"""
Given hint: {hint}
Past wrong guesses: {past_guesses}
Make a new guess for the target word.
Reply only with the guessed word.
"""
        return await call_llm(prompt)

    async def post(self, memory: Memory, prep_res, guess):
        target_word = prep_res["target_word"] # Get target word from prep_res
        if guess.lower() == target_word.lower():
            print('Game Over - Correct guess!')
            await memory.hinter_queue.put("GAME_OVER") # Write to memory queue
            self.trigger('end')
            return

        # Update past guesses in memory
        if not hasattr(memory, 'past_guesses'):
            memory.past_guesses = []
        memory.past_guesses.append(guess) # Write to memory

        await memory.hinter_queue.put(guess) # Write to memory queue
        self.trigger('continue')
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
import { Memory, Node } from 'brainyflow'
import { callLLM } from '../utils/callLLM'

class Hinter extends Node {
  async prep(memory: Memory): Promise<any> {
    if (memory.guesserQueue) {
      try {
        const guess = await memory.guesserQueue.get()
        if (guess === 'GAME_OVER') {
          return null
        }
        return { guess }
      } catch (e) {
        // Queue empty
      }
    }
    return {}
  }

  async exec(prepRes: any): Promise<string | null> {
    if (prepRes === null) return null

    const prompt = `
Given target word: ${memory.targetWord}
Forbidden words: ${memory.forbiddenWords}
Last wrong guess: ${prepRes.guess || ''}
Generate a creative hint that helps guess the target word without using forbidden words.
Reply only with the hint text.
`
    return await callLLM(prompt)
  }

  async post(memory: Memory, data: any, hint: string | null): Promise<void> {
    if (hint === null) {
      this.trigger('end')
      return
    }
    await memory.hinterQueue.put(hint)
    this.trigger('continue')
  }
}

class Guesser extends Node {
  async prep(memory: Memory): Promise<any> {
    const hint = await memory.guesserQueue.get()
    return {
      hint,
      pastGuesses: memory.pastGuesses || [],
    }
  }

  async exec(prepRes: any): Promise<string> {
    const prompt = `
Given hint: ${prepRes.hint}
Past wrong guesses: ${prepRes.pastGuesses}
Make a new guess for the target word.
Reply only with the guessed word.
`
    return await callLLM(prompt)
  }

  async post(memory: Memory, prepRes: any, guess: string): Promise<void> {
    if (guess.toLowerCase() === memory.targetWord.toLowerCase()) {
      console.log('Game Over - Correct guess!')
      await memory.hinterQueue.put('GAME_OVER')
      this.trigger('end')
      return
    }

    // Update past guesses
    memory.pastGuesses = [...(memory.pastGuesses || []), guess]
    await memory.hinterQueue.put(guess)
    this.trigger('continue')
  }
}
```

{% endtab %}
{% endtabs %}

## Running the Game

{% tabs %}
{% tab title="Python" %}

```python
async def main():
    # Set up game state in initial memory object
    memory = {
        "target_word": "nostalgia",
        "forbidden_words": ["memory", "past", "remember", "feeling", "longing"],
        "hinter_queue": asyncio.Queue(),
        "guesser_queue": asyncio.Queue(),
        "past_guesses": [] # Initialize past_guesses
    }

    print("Game starting!")
    print(f"Target word: {memory['target_word']}") # Access memory object
    print(f"Forbidden words: {memory['forbidden_words']}") # Access memory object

    # Initialize by sending empty guess to hinter queue in memory
    await memory["hinter_queue"].put("")

    # Create nodes
    hinter = Hinter()
    guesser = Guesser()

    # Set up flows
    hinter_flow = Flow(start=hinter)
    guesser_flow = Flow(start=guesser)

    # Connect nodes to themselves using actions
    hinter - "continue" >> hinter
    guesser - "continue" >> guesser

    # Run both agents concurrently, passing the same memory object
    print('Running agents...')
    await asyncio.gather(
        hinter_flow.run(memory), # Pass memory object
        guesser_flow.run(memory)  # Pass memory object
    )
    print('\nGame finished.')
    print('Final memory state:', memory)

asyncio.run(main())
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
// --- Main Execution ---
async function main() {
  // Set up game state in initial memory
  const data = {
    targetWord: 'nostalgia',
    forbiddenWords: ['memory', 'past', 'remember', 'feeling', 'longing'],
    hinterQueue: new AsyncQueue<string>(),
    guesserQueue: new AsyncQueue<string>(),
    pastGuesses: [],
  }

  console.log('Game starting!')
  console.log(`Target word: ${data.targetWord}`)
  console.log(`Forbidden words: ${data.forbiddenWords}`)

  // Initialize by sending empty guess to hinter queue
  await data.hinterQueue.put('')

  // Create nodes
  const hinterNode = new Hinter()
  const guesserNode = new Guesser()

  // Define transitions for looping and ending
  hinterNode.on('continue', hinterNode)
  guesserNode.on('continue', guesserNode)

  // Create separate flows for each agent
  const hinterFlow = new Flow(hinterNode)
  const guesserFlow = new Flow(guesserNode)

  // Run both agent flows concurrently using the same memory object
  console.log('Running agents...')
  await Promise.all([hinterFlow.run(data), guesserFlow.run(data)])
  console.log('\nGame finished normally.')
  console.log('Final memory state:', data)
}

// Assuming AsyncQueue and callLLM are defined elsewhere
// class AsyncQueue<T> { ... }
// async function callLLM(prompt: string): Promise<string> { return 'mock'; }

main().catch(console.error)
```

{% endtab %}
{% endtabs %}

When you run this code, the multi-agent system works as follows:

1. The Hinter agent creates clues (avoiding forbidden words)
2. The Guesser agent makes guesses based on the hints
3. Both agents operate independently but communicate via queues
4. The game continues until the correct word is guessed

The output will look something like:

```
Game starting!
Target word: nostalgia
Forbidden words: ['memory', 'past', 'remember', 'feeling', 'longing']

Hinter: Here's your hint - Thinking about childhood summers
Guesser: I guess it's - happiness

Hinter: Here's your hint - The warm sensation when seeing old photos
Guesser: I guess it's - nostalgia

Game Over - Correct guess!
```

## Benefits of Multi-Agent Systems

This pattern demonstrates several key advantages:

1. **Specialization**: Each agent can focus on a specific task
2. **Independence**: Agents can operate on different schedules or priorities
3. **Coordination**: Agents can collaborate through shared memory and queues
4. **Flexibility**: Easy to add new agents or modify existing ones
5. **Scalability**: The system can grow to include many specialized agents
