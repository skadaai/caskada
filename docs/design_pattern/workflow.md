---
title: 'Workflow'
---

# Workflow

Many real-world tasks are too complex for one LLM call. The solution is **Task Decomposition**: decompose them into a [chain](../core_abstraction/flow.md) of multiple Nodes.

<div align="center">
  <img src="https://github.com/zvictor/brainyflow/raw/main/.github/media/workflow.png?raw=true" width="400"/>
</div>

{% hint style="success" %}
You don't want to make each task **too coarse**, because it may be _too complex for one LLM call_.
You don't want to make each task **too granular**, because then _the LLM call doesn't have enough context_ and results are _not consistent across nodes_.

You usually need multiple _iterations_ to find the _sweet spot_. If the task has too many _edge cases_, consider using [Agents](./agent.md).
{% endhint %}

### Example: Article Writing

{% tabs %}
{% tab title="Python" %}

```python
import asyncio
from brainyflow import Node, Flow

class GenerateOutline(Node):
    async def prep(self, shared): return shared["topic"]
    async def exec(self, topic): return call_llm(f"Create a detailed outline for an article about {topic}")
    async def post(self, shared, prep_res, exec_res): shared["outline"] = exec_res

class WriteSection(Node):
    async def prep(self, shared): return shared["outline"]
    async def exec(self, outline): return call_llm(f"Write content based on this outline: {outline}")
    async def post(self, shared, prep_res, exec_res): shared["draft"] = exec_res

class ReviewAndRefine(Node):
    async def prep(self, shared): return shared["draft"]
    async def exec(self, draft): return call_llm(f"Review and improve this draft: {draft}")
    async def post(self, shared, prep_res, exec_res): shared["final_article"] = exec_res

# Connect nodes
outline = GenerateOutline()
write = WriteSection()
review = ReviewAndRefine()

outline >> write >> review

# Create and run flow
writing_flow = Flow(start=outline)

async def main():
    shared = {"topic": "AI Safety"}
    await writing_flow.run(shared)
    print("Final Article:", shared.get("final_article", "Not generated"))

if __name__ == "__main__":
    asyncio.run(main())
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
class GenerateOutline extends Node {
  async prep(shared: any): Promise<any> {
    return shared['topic']
  }
  async exec(topic: string): Promise<any> {
    return await callLLM(`Create a detailed outline for an article about ${topic}`)
  }
  async post(shared: any, prepRes: any, execRes: any): Promise<void> {
    shared['outline'] = execRes
  }
}

class WriteSection extends Node {
  async prep(shared: any): Promise<any> {
    return shared['outline']
  }
  async exec(outline: string): Promise<any> {
    return await callLLM(`Write content based on this outline: ${outline}`)
  }
  async post(shared: any, prepRes: any, execRes: any): Promise<void> {
    shared['draft'] = execRes
  }
}

class ReviewAndRefine extends Node {
  async prep(shared: any): Promise<any> {
    return shared['draft']
  }
  async exec(draft: string): Promise<any> {
    return await callLLM(`Review and improve this draft: ${draft}`)
  }
  async post(shared: any, prepRes: any, execRes: any): Promise<void> {
    shared['final_article'] = execRes
  }
}

// Connect nodes
const outline = new GenerateOutline()
const write = new WriteSection()
const review = new ReviewAndRefine()

outline.next(write).next(review)

// Create and run flow
const writingFlow = new Flow(outline)

async function main() {
  const shared = { topic: 'AI Safety' }
  await writingFlow.run(shared)
  console.log(`Final Article: ${shared['final_article'] || 'Not generated'}`)
}

main().catch(console.error) // Execute async main function
```

{% endtab %}
{% endtabs %}

For _dynamic cases_, consider using [Agents](./agent.md).
