---
title: 'LLM Wrapper'
machine-display: false
---

# LLM Wrappers

{% hint style="warning" %}

**BrainyFlow does NOT provide built-in utilities**

Instead, we offer examples that you can implement yourself. This approach gives you [more flexibility and control](./index.md#why-not-built-in) over your project's dependencies and functionality.

{% endhint %}

BrainyFlow doesn't provide built-in LLM wrappers.
You are better of checking out libraries like [litellm](https://github.com/BerriAI/litellm) (Python).
Here's a simple example of how you might implement your own wrapper:

## Basic Implementation

{% tabs %}
{% tab title="Python" %}

```python
# utils/call_llm.py
import os
from openai import OpenAI

def call_llm(prompt, model="gpt-4o", temperature=0.7):
    """Simple wrapper for calling OpenAI's API"""
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature
    )
    return response.choices[0].message.content
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
// utils/callLLM.ts
import OpenAI from 'openai'

export async function callLLM(prompt: string, model: string = 'gpt-4o', temperature: number = 0.7): Promise<string> {
  const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY,
  })

  const response = await openai.chat.completions.create({
    model,
    messages: [{ role: 'user', content: prompt }],
    temperature,
  })

  return response.choices[0]?.message?.content || ''
}
```

{% endtab %}
{% endtabs %}

## Why Implement Your Own?

BrainyFlow intentionally doesn't include vendor-specific APIs for several reasons:

1. **API Volatility**: External APIs change frequently
2. **Flexibility**: You may want to switch providers or use fine-tuned models
3. **Optimizations**: Custom implementations allow for caching, batching, and other optimizations

## Integration with BrainyFlow

Here's how to use your LLM wrapper in a BrainyFlow node:

{% tabs %}
{% tab title="Python" %}

```python
from brainyflow import Node
from utils import call_llm

class LLMNode(Node):
    async def prep(self, memory):
        return memory.prompt

    async def exec(self, prompt):
        return await call_llm(prompt)

    async def post(self, memory, prep_res, exec_res):
        memory.response = exec_res
        self.trigger('default')
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
import { Memory, Node } from 'brainyflow'
import { callLLM } from './utils/callLLM' // Your wrapper

class LLMNode extends Node {
  async prep(memory): Promise<string> {
    // Read prompt from memory
    return memory.prompt ?? '' // Provide default if needed
  }

  async exec(prompt: string): Promise<string> {
    // Call the LLM wrapper
    if (!prompt) throw new Error('No prompt provided.')
    return await callLLM(prompt)
  }

  async post(memory, prepRes: string, llmResponse: string): Promise<void> {
    // Store the response in memory
    memory.response = llmResponse
    this.trigger('default') // Or another action based on response
  }
}
```

{% endtab %}
{% endtabs %}

## Additional Considerations

- Add error handling for API failures
- Consider implementing caching for repeated queries
- For production systems, add rate limiting to avoid quota issues

Remember that this is just a starting point. You can extend this implementation based on your specific needs.
