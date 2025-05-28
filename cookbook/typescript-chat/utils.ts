import OpenAI from 'openai'

export interface Message {
  role: 'user' | 'assistant'
  content: string
}

export async function callLLM(messages: Message[]) {
  const client = new OpenAI(
    process.env.OPENROUTER_API_KEY
      ? {
          apiKey: process.env.OPENROUTER_API_KEY,
          baseURL: 'https://openrouter.ai/api/v1',
        }
      : {
          apiKey: process.env.OPENAI_API_KEY,
        },
  )

  const response = await client.chat.completions.create({
    model: 'gpt-4o-mini',
    messages: messages,
    temperature: 0.7,
  })

  return response.choices[0].message.content
}
