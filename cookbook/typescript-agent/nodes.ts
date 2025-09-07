import { Memory, Node } from 'caskada'
import { parse } from 'yaml'
import { callLLM, webSearch } from './utils'

export type SearchAgentGlobalStore = {
  question: string
  context?: string
  searchQuery?: string
  answer?: string
}

interface PrepResult {
  question: string
  context?: string
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

export class DecideNode extends Node<SearchAgentGlobalStore, PrepResult, LLMDecision, DecideNodeActions> {
  async prep(memory: Memory<SearchAgentGlobalStore>) {
    const context = memory.context || 'No previous search.'
    const question = memory.question
    return { context, question }
  }

  async exec(input: PrepResult) {
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
    return parse(yamlStr) as LLMDecision
  }

  async post(memory: Memory<SearchAgentGlobalStore>, prepRes: PrepResult, execRes: LLMDecision) {
    if (!prepRes) {
      console.log('No context or question provided.')
      this.trigger('error')
      return
    }

    if (!execRes) {
      console.log('No decision made.')
      this.trigger('error')
      return
    }

    if (execRes.action === 'search') {
      memory.searchQuery = execRes.searchQuery
      console.log(`Searching for: ${execRes.searchQuery}`)
      console.log(`Reason: ${execRes.reason}`)
    } else {
      memory.answer = execRes.answer // Persist final answer
      console.log(`Answering: ${execRes.answer}`)
      console.log(`Reason: ${execRes.reason}`)
    }

    this.trigger(execRes.action)
  }
}

// Define allowed actions for SearchNode
type SearchNodeActions = ['decide', 'error']

export class SearchNode extends Node<SearchAgentGlobalStore, string, SearchResult[], SearchNodeActions> {
  async prep(memory: Memory<SearchAgentGlobalStore>) {
    return memory.searchQuery
  }

  async exec(searchQuery: string) {
    console.log(`Calling web search tool.`)
    return await webSearch(searchQuery)
  }

  async post(memory: Memory<SearchAgentGlobalStore>, prepRes: string, execRes: SearchResult[]) {
    if (!prepRes) {
      console.log('No search query provided.')
      this.trigger('error')
      return
    }

    if (!execRes) {
      console.log('No search results found.')
      this.trigger('error')
      return
    }

    const previous = memory.context || ''
    memory.context = previous + '\n\nSearch: ' + memory.searchQuery + '\nResult :' + JSON.stringify(execRes)
    this.trigger('decide')
  }
}

// Define allowed actions for AnswerNode
type AnswerNodeActions = ['done', 'error']

export class AnswerNode extends Node<SearchAgentGlobalStore, PrepResult, string | null, AnswerNodeActions> {
  async prep(memory: Memory<SearchAgentGlobalStore>) {
    const context = memory.context || 'No previous context.'
    const question = memory.question
    return { question, context }
  }

  async exec(input: PrepResult) {
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

  async post(memory: Memory<SearchAgentGlobalStore>, prepRes: PrepResult, execRes: string | null) {
    if (!prepRes) {
      console.log('No answer provided.')
      this.trigger('error')
      return
    }

    if (!execRes) {
      console.log('No answer generated.')
      this.trigger('error')
      return
    }

    memory.answer = execRes
    console.log(`Final Answer: ${execRes}`)
    this.trigger('done')
  }
}
