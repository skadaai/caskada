# Multi-Agents (Advanced)

Multiple [Agents](./flow.md) can work together by handling subtasks and communicating the progress.
Communication between agents is typically implemented using message queues in shared storage.

{% hint style="success" %}
Most of time, you don't need Multi-Agents. Start with a simple solution first.
{% endhint %}

### Example Agent Communication: Message Queue

Here's a simple example showing how to implement agent communication using `asyncio.Queue`.
The agent listens for messages, processes them, and continues listening:

{% tabs %}
{% tab title="Python" %}

```python
import asyncio
from brainyflow import Node, Flow

class AgentNode(Node):
    async def prep(self, _):
        message_queue = self.params["messages"]
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

    while True:
        message = f"{messages[counter % len(messages)]} | timestamp_{counter}"
        await message_queue.put(message)
        counter += 1
        await asyncio.sleep(1)

async def main():
    message_queue = asyncio.Queue()
    shared = {}
    flow.set_params({"messages": message_queue})

    # Run both coroutines
    await asyncio.gather(
        flow.run(shared),
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

### Interactive Multi-Agent Example: Taboo Game

Here's a more complex example where two agents play the word-guessing game Taboo.
One agent provides hints while avoiding forbidden words, and another agent tries to guess the target word:

{% tabs %}
{% tab title="Python" %}

```python
import asyncio
from brainyflow import Node, Flow

class Hinter(Node):
    async def prep(self, shared):
        guess = await shared["hinter_queue"].get()
        if guess == "GAME_OVER":
            return None
        return shared["target_word"], shared["forbidden_words"], shared.get("past_guesses", [])

    async def exec(self, inputs):
        if inputs is None:
            return None
        target, forbidden, past_guesses = inputs
        prompt = f"Generate hint for '{target}'\nForbidden words: {forbidden}"
        if past_guesses:
            prompt += f"\nPrevious wrong guesses: {past_guesses}\nMake hint more specific."
        prompt += "\nUse at most 5 words."

        hint = call_llm(prompt)
        print(f"\nHinter: Here's your hint - {hint}")
        return hint

    async def post(self, shared, prep_res, exec_res):
        if exec_res is None:
            return "end"
        await shared["guesser_queue"].put(exec_res)
        return "continue"

class Guesser(Node):
    async def prep(self, shared):
        hint = await shared["guesser_queue"].get()
        return hint, shared.get("past_guesses", [])

    async def exec(self, inputs):
        hint, past_guesses = inputs
        prompt = f"Given hint: {hint}, past wrong guesses: {past_guesses}, make a new guess. Directly reply a single word:"
        guess = call_llm(prompt)
        print(f"Guesser: I guess it's - {guess}")
        return guess

    async def post(self, shared, prep_res, exec_res):
        if exec_res.lower() == shared["target_word"].lower():
            print("Game Over - Correct guess!")
            await shared["hinter_queue"].put("GAME_OVER")
            return "end"

        if "past_guesses" not in shared:
            shared["past_guesses"] = []
        shared["past_guesses"].append(exec_res)

        await shared["hinter_queue"].put(exec_res)
        return "continue"

async def main():
    # Set up game
    shared = {
        "target_word": "nostalgia",
        "forbidden_words": ["memory", "past", "remember", "feeling", "longing"],
        "hinter_queue": asyncio.Queue(),
        "guesser_queue": asyncio.Queue()
    }

    print("Game starting!")
    print(f"Target word: {shared['target_word']}")
    print(f"Forbidden words: {shared['forbidden_words']}")

    # Initialize by sending empty guess to hinter
    await shared["hinter_queue"].put("")

    # Create nodes and flows
    hinter = Hinter()
    guesser = Guesser()

    # Set up flows
    hinter_flow = Flow(start=hinter)
    guesser_flow = Flow(start=guesser)

    # Connect nodes to themselves
    hinter - "continue" >> hinter
    guesser - "continue" >> guesser

    # Run both agents concurrently
    await asyncio.gather(
        hinter_flow.run(shared),
        guesser_flow.run(shared)
    )

asyncio.run(main())
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
import { Flow, Memory, Node } from 'brainyflow'

declare function callLLM(prompt: string): Promise<string> // Assuming callLLM is defined elsewhere

class Hinter extends Node {
  async prep(memory: Memory): Promise<any> {
    const guess = await memory.hinterQueue.get() // Read from queue in memory
    if (guess === 'GAME_OVER') {
      return null // Signal to stop
    }
    // Return data needed for exec
    return {
      target: memory.targetWord,
      forbidden: memory.forbiddenWords,
      pastGuesses: memory.pastGuesses ?? [],
    }
  }

  async exec(prepRes: any): Promise<string | null> {
    if (!prepRes) return null // Stop if prep returned null
    const { target, forbidden, pastGuesses } = prepRes
    let prompt = `Generate hint for '${target}'\nForbidden words: ${forbidden}`
    if (pastGuesses.length > 0) {
      prompt += `\nPrevious wrong guesses: ${pastGuesses}\nMake hint more specific.`
    }
    prompt += '\nUse at most 5 words.'

    const hint = await callLLM(prompt)
    console.log(`\nHinter: Here's your hint - ${hint}`)
    return hint
  }

  async post(memory: Memory, prepRes: any, hint: string | null): Promise<void> {
    if (hint === null) {
      return this.trigger('end') // Use trigger to end
    }
    await memory.guesserQueue.put(hint) // Send hint to guesser queue
    this.trigger('continue') // Trigger self to continue
  }
}

class Guesser extends Node {
  async prep(memory: Memory): Promise<any> {
    const hint = await memory.guesserQueue.get() // Read hint from queue
    return { hint, pastGuesses: memory.pastGuesses ?? [] }
  }

  async exec(prepRes: any): Promise<string> {
    const { hint, pastGuesses } = prepRes
    const prompt = `Given hint: ${hint}, past wrong guesses: ${pastGuesses}, make a new guess. Directly reply a single word:`
    const guess = await callLLM(prompt)
    console.log(`Guesser: I guess it's - ${guess}`)
    return guess
  }

  async post(memory: Memory, prepRes: any, guess: string): Promise<void> {
    if (guess.toLowerCase() === memory.targetWord.toLowerCase()) {
      console.log('Game Over - Correct guess!')
      await memory.hinterQueue.put('GAME_OVER') // Signal hinter to stop
      this.trigger('end') // End this flow
      return
    }

    // Update past guesses in global memory
    const pastGuesses = memory.pastGuesses ?? []
    memory.pastGuesses = [...pastGuesses, guess]

    await memory.hinterQueue.put(guess) // Send wrong guess back to hinter
    this.trigger('continue') // Trigger self to continue
  }
}

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

The Output:

```
Game starting!
Target word: nostalgia
Forbidden words: ['memory', 'past', 'remember', 'feeling', 'longing']

Hinter: Here's your hint - Thinking of childhood summer days
Guesser: I guess it's - popsicle

Hinter: Here's your hint - When childhood cartoons make you emotional
Guesser: I guess it's - nostalgic

Hinter: Here's your hint - When old songs move you
Guesser: I guess it's - memories

Hinter: Here's your hint - That warm emotion about childhood
Guesser: I guess it's - nostalgia
Game Over - Correct guess!
```
