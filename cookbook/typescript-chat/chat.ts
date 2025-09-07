import readline from 'node:readline'
import { Flow, Memory, Node } from 'caskada'
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

type ChatGlobalStore = {
  messages?: Message[]
}

class ChatNode extends Node<ChatGlobalStore> {
  // Use memory and add type hint
  async prep(memory: Memory<ChatGlobalStore>) {
    if (!memory.messages) {
      memory.messages = []
      console.log("Welcome to the chat! Type 'exit' to end the conversation.")
    }

    const input = await promptUser()
    if (input === 'exit') {
      return
    }

    memory.messages.push({ role: 'user', content: input })
    return memory.messages
  }

  async exec(messages?: Message[]) {
    if (!messages) {
      return
    }

    const response = await callLLM(messages)
    return response
  }

  // Use memory and add type hint
  async post(memory: Memory<ChatGlobalStore>, prepRes?: Message[], execRes?: string) {
    if (!prepRes) {
      console.log('Goodbye!')
      this.trigger('end')
      return
    }

    if (!execRes) {
      console.log('Goodbye!')
      this.trigger('end')
      return
    }

    console.log(`Assistant: ${execRes}`)
    memory.messages?.push({ role: 'assistant', content: execRes })
    this.trigger('continue')
  }
}

const chatNode = new ChatNode()
chatNode.on('continue', chatNode)

const flow = new Flow(chatNode)

const memory: ChatGlobalStore = {} // Use Memory object
await flow.run(memory) // Use await and pass memory object
