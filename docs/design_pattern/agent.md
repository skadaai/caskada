---
machine-display: false
---

# Agent

Agent is a powerful design pattern in which nodes can take dynamic actions based on the context.

<div align="center">
  <img src="https://github.com/zvictor/brainyflow/raw/main/.github/media/agent.png?raw=true" width="350"/>
</div>

## Implement Agent with Graph

1. **Context and Action:** Implement nodes that supply context and perform actions.
2. **Branching:** Use branching to connect each action node to an agent node. Use action to allow the agent to direct the [flow](../core_abstraction/flow.md) between nodes—and potentially loop back for multi-step.
3. **Agent Node:** Provide a prompt to decide action—for example:

{% tabs %}
{% tab title="Python" %}

````python
f"""
### CONTEXT
Task: {task_description}
Previous Actions: {previous_actions}
Current State: {current_state}

### ACTION SPACE
[1] search
  Description: Use web search to get results
  Parameters:
    - query (str): What to search for

[2] answer
  Description: Conclude based on the results
  Parameters:
    - result (str): Final answer to provide

### NEXT ACTION
Decide the next action based on the current context and available action space.
Return your response in the following format:

```yaml
thinking: |
    <your step-by-step reasoning process>
action: <action_name>
parameters:
    <parameter_name>: <parameter_value>
```"""
````

{% endtab %}

{% tab title="TypeScript" %}

```typescript
;`### CONTEXT
Task: ${taskDescription}
Previous Actions: ${previousActions}
Current State: ${currentState}

### ACTION SPACE
[1] search
  Description: Use web search to get results
  Parameters:
    - query (string): What to search for

[2] answer
  Description: Conclude based on the results  
  Parameters:
    - result (string): Final answer to provide

### NEXT ACTION
Decide the next action based on the current context and available action space.
Return your response in the following format:

\`\`\`yaml
thinking: |
    <your step-by-step reasoning process>
action: <action_name>
parameters:
    <parameter_name>: <parameter_value>
\`\`\``
```

{% endtab %}
{% endtabs %}

The core of building **high-performance** and **reliable** agents boils down to:

1. **Context Management:** Provide _relevant, minimal context._ For example, rather than including an entire chat history, retrieve the most relevant via [RAG](./rag.md). Even with larger context windows, LLMs still fall victim to ["lost in the middle"](https://arxiv.org/abs/2307.03172), overlooking mid-prompt content.

2. **Action Space:** Provide _a well-structured and unambiguous_ set of actions—avoiding overlap like separate `read_databases` or `read_csvs`. Instead, import CSVs into the database.

## Example Good Action Design

- **Incremental:** Feed content in manageable chunks (500 lines or 1 page) instead of all at once.

- **Overview-zoom-in:** First provide high-level structure (table of contents, summary), then allow drilling into details (raw texts).

- **Parameterized/Programmable:** Instead of fixed actions, enable parameterized (columns to select) or programmable (SQL queries) actions, for example, to read CSV files.

- **Backtracking:** Let the agent undo the last step instead of restarting entirely, preserving progress when encountering errors or dead ends.

## Example: Search Agent

This agent:

1. Decides whether to search or answer
2. If searches, loops back to decide if more search needed
3. Answers when enough context gathered

{% tabs %}
{% tab title="Python" %}

````python
import asyncio
import yaml
from brainyflow import Node, Flow, Memory
# Assuming call_llm and search_web are defined elsewhere
# async def call_llm(prompt: str) -> str: ...
# async def search_web(query: str) -> str: ...


class DecideAction(Node):
    async def prep(self, memory: Memory):
        context = memory.context if hasattr(memory, 'context') else "No previous search"
        query = memory.query
        return query, context

    async def exec(self, inputs):
        query, context = inputs
        prompt = f"""
Given input: {query}
Previous search results: {context}
Should I: 1) Search web for more info 2) Answer with current knowledge
Output in yaml:
```yaml
action: search/answer
reason: why this action
search_term: search phrase if action is search
```"""
        resp = call_llm(prompt)
        yaml_str = resp.split("```yaml")[1].split("```")[0].strip()
        result = yaml.safe_load(yaml_str)

        assert isinstance(result, dict)
        assert "action" in result
        assert "reason" in result
        assert result["action"] in ["search", "answer"]
        if result["action"] == "search":
            assert "search_term" in result

        return result

    async def post(self, memory: Memory, prep_res, exec_res: dict):
        if exec_res["action"] == "search":
            memory.search_term = exec_res["search_term"]
        self.trigger(exec_res["action"])
````

{% endtab %}

{% tab title="TypeScript" %}

````typescript
import { Flow, Memory, Node } from 'brainyflow'

// Assume callLLM and parseYaml are defined elsewhere
declare function callLLM(prompt: string): Promise<string>
declare function parseYaml(text: string): any

class DecideAction extends Node {
  async prep(memory: Memory): Promise<{ query: string; context: any }> {
    // Read from memory
    const context = memory.context ?? 'No previous search'
    const query = memory.query
    return { query, context }
  }

  async exec(prepRes: { query: string; context: any }): Promise<any> {
    const { query, context } = prepRes
    const prompt = `
Given input: ${query}
Previous search results: ${JSON.stringify(context)}
Should I: 1) Search web for more info ('search') 2) Answer with current knowledge ('answer')
Output in yaml:
\`\`\`yaml
action: search | answer
reason: <why this action>
search_term: <search phrase if action is search>
\`\`\``
    const resp = await callLLM(prompt)
    // Simplified parsing/validation for docs
    const yamlStr = resp.split(/```(?:yaml)?/)[1]?.trim()
    if (!yamlStr) {
      throw new Error('Missing YAML response')
    }

    const result = parseYaml(yamlStr)

    if (typeof result !== 'object' || !result) {
      throw new Error('Invalid YAML response')
    }
    if (!('action' in result)) {
      throw new Error('Missing action in response')
    }
    if (!('reason' in result)) {
      throw new Error('Missing reason in response')
    }
    if (!['search', 'answer'].includes(result.action)) {
      throw new Error('Invalid action value')
    }
    if (result.action === 'search' && !('search_term' in result)) {
      throw new Error('Missing search_term for search action')
    }

    return result
  }

  async post(memory: Memory, prepRes: any, execRes: any): Promise<void> {
    // Write search term if needed
    if (execRes.action === 'search' && execRes.search_term) {
      memory.search_term = execRes.search_term
    }
    // Trigger the decided action
    this.trigger(execRes.action)
  }
}
````

{% endtab %}
{% endtabs %}

{% tabs %}
{% tab title="Python" %}

```python
class SearchWeb(Node):
    async def prep(self, memory: Memory):
        return memory.search_term

    async def exec(self, search_term):
        return await search_web(search_term)

    async def post(self, memory: Memory, prep_res, exec_res):
        prev_searches = memory.context if hasattr(memory, 'context') else []
        memory.context = prev_searches + [
            {"term": prep_res, "result": exec_res}
        ]
        self.trigger('decide')
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
import { Memory, Node } from 'brainyflow'

declare function searchWeb(query: string): Promise<any> // Assume `searchWeb` is defined elsewhere

class SearchWeb extends Node {
  async prep(memory: Memory): Promise<string> {
    // Read search term from memory
    return memory.search_term
  }

  async exec(searchTerm: string): Promise<any> {
    return await searchWeb(searchTerm)
  }

  async post(memory: Memory, prepRes: string, execRes: any): Promise<void> {
    // Add search result to context (simplified)
    const prevContext = memory.context ?? []
    memory.context = [...prevContext, { term: prepRes, result: execRes }]
    // Trigger loop back to decide
    this.trigger('decide')
  }
}
```

{% endtab %}
{% endtabs %}

{% tabs %}
{% tab title="Python" %}

```python
class DirectAnswer(Node):
    async def prep(self, memory: Memory):
        return memory.query, memory.context if hasattr(memory, 'context') else ""

    async def exec(self, inputs):
        query, context = inputs
        return call_llm(f"Context: {context}\nAnswer: {query}")

    async def post(self, memory: Memory, prep_res, exec_res):
       print(f"Answer: {exec_res}")
       memory.answer = exec_res
       # No trigger needed if this is the end of the path
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
import { Memory, Node } from 'brainyflow'

declare function callLLM(prompt: string): Promise<string> // Assuming callLLM is defined elsewhere

class DirectAnswer extends Node {
  async prep(memory: Memory): Promise<{ query: string; context: any }> {
    // Read query and context
    return { query: memory.query, context: memory.context ?? 'No context' }
  }

  async exec(prepRes: { query: string; context: any }): Promise<string> {
    // Generate answer based on context
    const prompt = `Context: ${JSON.stringify(prepRes.context)}\nAnswer Query: ${prepRes.query}`
    return await callLLM(prompt)
  }

  async post(memory: Memory, prepRes: any, execRes: string): Promise<void> {
    // Store final answer
    memory.answer = execRes
    console.log(`Answer: ${execRes}`)
    // No trigger needed - end of this path
  }
}
```

{% endtab %}
{% endtabs %}

{% tabs %}
{% tab title="Python" %}

```python
# Connect nodes
decide = DecideAction()
search = SearchWeb()
answer = DirectAnswer()

decide - "search" >> search
decide - "answer" >> answer
search - "decide" >> decide # Loop back

flow = Flow(start=decide)

async def main():
    memory_data = {"query": "Who won the Nobel Prize in Physics 2024?"}
    result = await flow.run(memory_data) # Pass memory object
    print(result) # Or handle result as needed
    print(memory_data) # See final memory state

if __name__ == "__main__":
    asyncio.run(main())
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
import { Flow } from 'brainyflow'

// Assuming DecideAction, SearchWeb, DirectAnswer classes are defined

// Instantiate nodes
const decide = new DecideAction()
const search = new SearchWeb()
const answer = new DirectAnswer()

// Define transitions
decide.on('search', search)
decide.on('answer', answer)
search.on('decide', decide) // Loop back

// Create the flow
const agentFlow = new Flow(decide)

// --- Main execution function ---
async function runAgent() {
  const initialMemory = { query: 'Who won the Nobel Prize in Physics 2024?' }
  console.log(`Starting agent flow with query: "${initialMemory.query}"`)

  try {
    await agentFlow.run(initialMemory) // Run the flow with memory object
    console.log('\n--- Flow Complete ---')
    console.log('Final Memory State:', initialMemory) // Log final memory state
    console.log('\nFinal Answer:', initialMemory.answer ?? 'No answer found')
  } catch (error) {
    console.error('\n--- Agent Flow Failed ---', error)
    console.error('Memory State on Failure:', initialMemory) // Log memory state on failure
  }
}

// Run the main function
runAgent()
```

{% endtab %}
{% endtabs %}
