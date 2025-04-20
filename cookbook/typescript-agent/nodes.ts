import { Memory, Node, SharedStore } from 'brainyflow'
import { parse } from 'yaml'
import { callLLM, webSearch } from './utils'

export interface SearchAgentGlobalStore {
  // Rename to GlobalStore
  question: string
  context?: string
  searchQuery?: string
  answer?: string
}

// Define allowed actions for DecideNode
type DecideNodeActions = ['search', 'answer', 'error']

interface LLMDecision {
  thinking: string
  action: 'search' | 'answer'
  reason: string
  answer?: string
  searchQuery?: string
}

interface SearchResult {
  title: string
  href: string
  body: string
}

export class DecideNode extends Node<SearchAgentGlobalStore, SharedStore, DecideNodeActions> {
  async prep(memory: Memory<SearchAgentGlobalStore, SharedStore>) {
    // Use memory
    const context = memory.context || 'No previous search.' // Use property access
    const question = memory.question // Use property access
    return { context, question }
  }

  async exec(input: { context: string; question: string }) {
    const { context, question } = input
    const now = new Date()
    console.log('Deciding whether to search or answer the question...')

    const prompt = `
        ### Context
        Current date is ${now.toISOString()}
        You are helpful assistance that can searching the web to gather real time data.
        Question: ${question}
        Context: ${context}

        ### Action Space
        [1] search
            description: look up for more information on internet
            parameter:
                - query (str): what to search for
        [2] answer
            description: answer the question based on the context
            parameter:
                - answer (str): the answer to the question
        
        ### Next Action
        Decide the next action based on the context and available actions.
        Return your response in this format:

        \`\`\`yaml
        thinking: |
            <your step-by-step reasoning process>
        action: search OR answer
        reason: <why you chose this action>
        answer: <if action is answer>
        searchQuery: <specific search query if action is search>
        \`\`\`

        IMPORTANT: Make sure to:
        1. Use proper indentation (4 spaces) for all multi-line fields
        2. Use the | character for multi-line text fields
        3. Keep single-line fields without the | character
        4. thinking about search query, make sure that you understand the question and use query that appropriate for search engine, not just copying the question
        `
    const response = await callLLM([{ role: 'user', content: prompt }])
    if (!response?.includes('```yaml')) {
      throw new Error('LLM response missing YAML block')
    }

    const yamlStr = response.split('```yaml')[1].split('```')[0].trim()
    const decision = parse(yamlStr) as LLMDecision
    return decision
  }

  async post(
    memory: Memory<SearchAgentGlobalStore, SharedStore>,
    prepRes?: { context: string; question: string },
    execRes?: LLMDecision,
  ) {
    // Use memory
    if (!prepRes) {
      console.log('No context or question provided.')
      this.trigger('error') // Use trigger
      return
    }

    if (!execRes) {
      console.log('No decision made.')
      this.trigger('error') // Use trigger
      return
    }

    if (execRes.action === 'search') {
      memory.searchQuery = execRes.searchQuery // Use property access
      console.log(`Searching for: ${execRes.searchQuery}`)
      console.log(`Reason: ${execRes.reason}`)
    } else {
      memory.answer = execRes.answer // Persist final answer
      console.log(`Answering: ${execRes.answer}`)
      console.log(`Reason: ${execRes.reason}`)
    }

    this.trigger(execRes.action) // Use trigger
  }
}

// Define allowed actions for SearchNode
type SearchNodeActions = ['decide', 'error']

export class SearchNode extends Node<
  SearchAgentGlobalStore,
  SharedStore,
  SearchNodeActions // Use defined actions
> {
  async prep(memory: Memory<SearchAgentGlobalStore, SharedStore>) {
    // Use memory
    return memory.searchQuery // Use property access
  }

  async exec(searchQuery: string) {
    console.log(`Calling web search tool.`)
    const result = await webSearch(searchQuery)
    return result as SearchResult[]
  }

  async post(
    memory: Memory<SearchAgentGlobalStore, SharedStore>,
    prepRes?: string,
    execRes?: SearchResult[],
  ) {
    // Use memory
    if (!prepRes) {
      console.log('No search query provided.')
      this.trigger('error') // Use trigger
      return
    }

    if (!execRes) {
      console.log('No search results found.')
      this.trigger('error') // Use trigger
      return
    }

    const previous = memory.context || '' // Use property access
    memory.context =
      previous + '\n\nSearch: ' + memory.searchQuery + '\nResult :' + JSON.stringify(execRes) // Use property access
    this.trigger('decide') // Use trigger
  }
}

// Define allowed actions for AnswerNode
type AnswerNodeActions = ['done', 'error']

export class AnswerNode extends Node<
  SearchAgentGlobalStore,
  SharedStore,
  AnswerNodeActions // Use defined actions
> {
  async prep(memory: Memory<SearchAgentGlobalStore, SharedStore>) {
    // Use memory
    const context = memory.context || 'No previous context.' // Use property access
    const question = memory.question // Use property access
    return { question, context }
  }

  async exec(input: { question: string; context: string }) {
    const { question, context } = input
    console.log('Answering the question...')
    const prompt = `
        ### Context
        Based on the following information, answer the question.
        Question: ${question}
        Research: ${context}
        
        ## Your Answer:
        Provide a comprehensive answer using the research results.
        `
    const response = await callLLM([{ role: 'user', content: prompt }])
    return response
  }

  async post(
    memory: Memory<SearchAgentGlobalStore, SharedStore>,
    prepRes?: { question: string; context: string },
    execRes?: string,
  ) {
    // Use memory
    if (!prepRes) {
      console.log('No answer provided.')
      this.trigger('error') // Use trigger
      return
    }

    if (!execRes) {
      console.log('No answer generated.')
      this.trigger('error') // Use trigger
      return
    }

    memory.answer = execRes // Use property access
    console.log(`Final Answer: ${execRes}`)
    this.trigger('done') // Use trigger
  }
}
