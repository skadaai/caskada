---
machine-display: false
---

# Structured Output

In many use cases, you may want the LLM to output a specific structure, such as a list or a dictionary with predefined keys.

There are several approaches to achieve a structured output:

- **Prompting** the LLM to strictly return a defined structure.
- Using LLMs that natively support **schema enforcement**.
- **Post-processing** the LLM's response to extract structured content.

In practice, **Prompting** is simple and reliable for modern LLMs.

### Example Use Cases

- Extracting Key Information

```yaml
product:
  name: Widget Pro
  price: 199.99
  description: |
    A high-quality widget designed for professionals.
    Recommended for advanced users.
```

- Summarizing Documents into Bullet Points

```yaml
summary:
  - This product is easy to use.
  - It is cost-effective.
  - Suitable for all skill levels.
```

- Generating Configuration Files

```yaml
server:
  host: 127.0.0.1
  port: 8080
  ssl: true
```

## Prompt Engineering

When prompting the LLM to produce **structured** output:

1. **Wrap** the structure in code fences (e.g., `yaml`).
2. **Validate** that all required fields exist (and let `Node` handles retry).

### Example Text Summarization

{% tabs %}
{% tab title="Python" %}

````python
import yaml
from brainyflow import Node, Memory

# Assume call_llm is defined elsewhere
# async def call_llm(prompt: str) -> str: ...

class SummarizeNode(Node):
    async def prep(self, memory):
        # Assuming the text to summarize is in memory.text
        return memory.text or ""

    async def exec(self, text_to_summarize: str):
        if not text_to_summarize:
             return {"summary": ["No text provided"]}

        prompt = f"""
Please summarize the following text as YAML, with exactly 3 bullet points:

{text_to_summarize}

Now, output ONLY the YAML structure:
```yaml
summary:
  - bullet 1
  - bullet 2
  - bullet 3
```"""
        response = await call_llm(prompt)
        structured_result: dict

        try:
            # Extract YAML block
            yaml_str = response.split("```yaml")[1].split("```")[0].strip()
            structured_result = yaml.safe_load(yaml_str)

            # Basic validation
            if not isinstance(structured_result, dict) or "summary" not in structured_result or not isinstance(structured_result["summary"], list):
                 raise ValueError("Invalid YAML structure")

        except (IndexError, ValueError, yaml.YAMLError) as e:
            print(f"Failed to parse structured output: {e}")
            # Handle error, maybe return a default structure or re-throw
            return {"summary": [f"Error parsing summary: {e}"]}

        return structured_result # e.g., {"summary": ["Point 1", "Point 2", "Point 3"]}

    async def post(self, memory, prep_res, exec_res: dict):
        # Store the structured result in memory
        memory.structured_summary = exec_res
        print("Stored structured summary:", exec_res)
        # No trigger needed if this is the end of the flow/branch
````

{% endtab %}

{% tab title="TypeScript" %}

````typescript
import { Memory, Node } from 'brainyflow'

// Assuming callLLM and a YAML parser are available
declare function callLLM(prompt: string): Promise<string>
declare function parseYaml(text: string): any

class SummarizeNode extends Node {
  async prep(memory): Promise<string> {
    // Assuming the text to summarize is in memory.text
    return memory.text ?? ''
  }

  async exec(textToSummarize: string): Promise<any> {
    if (!textToSummarize) return { summary: ['No text provided'] }

    const prompt = `
Please summarize the following text as YAML, with exactly 3 bullet points:

${textToSummarize}

Now, output ONLY the YAML structure:
\`\`\`yaml
summary:
  - bullet 1
  - bullet 2
  - bullet 3
\`\`\``

    const response = await callLLM(prompt)
    let structuredResult: any
    try {
      const yamlStr = response.split(/```(?:yaml)?/)[1]?.trim()
      if (!yamlStr) throw new Error('No YAML block found')
      structuredResult = parseYaml(yamlStr)

      // Basic validation
      if (!structuredResult?.summary || !Array.isArray(structuredResult.summary)) {
        throw new Error('Invalid YAML structure: missing or non-array summary')
      }
    } catch (e: any) {
      console.error('Failed to parse structured output:', e.message)
      // Handle error, maybe return a default structure or re-throw
      // Returning the raw response might be an option too
      return { summary: [`Error parsing summary: ${e.message}`] }
    }

    return structuredResult // e.g., { summary: ['Point 1', 'Point 2', 'Point 3'] }
  }

  async post(memory, prepRes: any, execRes: any): Promise<void> {
    // Store the structured result in memory
    memory.structured_summary = execRes
    console.log('Stored structured summary:', execRes)
    // No trigger needed if this is the end of the flow/branch
  }
}
````

{% endtab %}
{% endtabs %}

{% hint style="info" %}
Besides using `assert` statements, another popular way to validate schemas is [Pydantic](https://github.com/pydantic/pydantic)
{% endhint %}

### Why YAML instead of JSON?

Current LLMs struggle with escaping. YAML is easier with strings since they don't always need quotes.

**In JSON**

```json
{
  "dialogue": "Alice said: \"Hello Bob.\\nHow are you?\\nI am good.\""
}
```

- Every double quote inside the string must be escaped with `\"`.
- Each newline in the dialogue must be represented as `\n`.

**In YAML**

```yaml
dialogue: |
  Alice said: "Hello Bob.
  How are you?
  I am good."
```

- No need to escape interior quotes—just place the entire text under a block literal (`|`).
- Newlines are naturally preserved without needing `\n`.
