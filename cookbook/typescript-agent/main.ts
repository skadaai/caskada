import { createAgentFlow } from './flow'

async function main() {
  const question = process.argv[2] || 'What is the latest Deepseek LLM model?'
  const agentFlow = createAgentFlow()
  const sharedContext = {
    question: question,
  }
  await agentFlow.run(sharedContext)
}

main().catch((error) => {
  console.error('Error running the agent:', error)
})
