import readline from 'node:readline';
import { Node, Flow } from "brainyflow";
import { Message, callLLM } from './utils';

function promptUser(): Promise<string> {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  return new Promise((resolve) => {
    rl.question('You: ', (userInput) => {
      rl.close();
      resolve(userInput);
    });
  });
}

interface ChatSharedContext {
  messages?: Message[]
}

class ChatNode extends Node {
  async prep(shared: ChatSharedContext) {
    if (!shared.messages) {
      shared.messages = []
      console.log("Welcome to the chat! Type 'exit' to end the conversation.")
    }

    const input = await promptUser()

    if (input === 'exit') {
      return
    }

    shared.messages.push({ role: 'user', content: input })
    return shared.messages
  }

  async exec(messages?: Message[]) {
    if (!messages) {
      return
    }

    const response = await callLLM(messages)
    return response
  }

  async post(shared: ChatSharedContext, prepRes?: Message[], execRes?: string) {
    if (!prepRes) {
      console.log("Goodbye!")
      return;
    }

    if (!execRes) {
      console.log("Goodbye!")
      return;
    }

    console.log(`Assistant: ${execRes}`)
    shared.messages?.push({ role: 'assistant', content: execRes })
    return 'continue'
  }
}

const chatNode = new ChatNode()
chatNode.on('continue', chatNode)

const flow = new Flow(chatNode)

const shared: ChatSharedContext = {}
flow.run(shared)
