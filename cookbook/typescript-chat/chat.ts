import readline from 'node:readline'
import { Flow, Memory, Node } from 'brainyflow' // Import Memory
import { callLLM, Message } from './utils'

function promptUser(): Promise<string> {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  })

  return new Promise((resolve) => {
    rl.question('You: ', (userInput) => {
      rl.close()
      resolve(userInput)
    })
  })
}

interface ChatGlobalStore {
  // Rename shared context to GlobalStore
  messages?: Message[]
}

class ChatNode extends Node<ChatGlobalStore> {
  // Use GlobalStore type hint
  async prep(memory: Memory<ChatGlobalStore>) {
    // Use memory and add type hint
    if (!memory.messages) {
      // Use property access
      memory.messages = [] // Use property access
      console.log("Welcome to the chat! Type 'exit' to end the conversation.")
    }

    const input = await promptUser()

    if (input === 'exit') {
      return
    }

    memory.messages.push({ role: 'user', content: input }) // Use property access
    return memory.messages // Use property access
  }

  async exec(messages?: Message[]) {
    if (!messages) {
      return
    }

    const response = await callLLM(messages)
    return response
  }

  async post(memory: Memory<ChatGlobalStore>, prepRes?: Message[], execRes?: string) {
    // Use memory and add type hint
    if (!prepRes) {
      console.log('Goodbye!')
      this.trigger('end') // Use trigger to end the flow
      return
    }

    if (!execRes) {
      console.log('Goodbye!')
      this.trigger('end') // Use trigger to end the flow
      return
    }

    console.log(`Assistant: ${execRes}`)
    memory.messages?.push({ role: 'assistant', content: execRes }) // Use property access
    this.trigger('continue') // Use trigger
  }
}

const chatNode = new ChatNode()
chatNode.on('continue', chatNode)

const flow = new Flow(chatNode)

const memory: ChatGlobalStore = {} // Use Memory object
await flow.run(memory) // Use await and pass memory object
