---
machine-display: true
---

# Utility Functions

BrainyFlow does not provide built-in utilities. Instead, we offer examples that you can implement yourself. This approach gives you more flexibility and control over your project's dependencies and functionality.

## Available Utility Function Examples

1. [LLM Wrapper](./llm.md): Interact with Language Models
2. [Web Search](./websearch.md): Perform web searches
3. [Chunking](./chunking.md): Split large texts into manageable chunks
4. [Embedding](./embedding.md): Generate vector embeddings for text
5. [Vector Databases](./vector.md): Store and query vector embeddings
6. [Text-to-Speech](./text_to_speech.md): Convert text to speech

## Why Not Built-in?

We believe it's a bad practice to include vendor-specific APIs in a general framework for several reasons:

1. **API Volatility**: Frequent changes in external APIs lead to heavy maintenance for hardcoded APIs.
2. **Flexibility**: You may want to switch vendors, use fine-tuned models, or run them locally.
3. **Optimizations**: Prompt caching, batching, and streaming are easier to implement without vendor lock-in.

## Implementing Utility Functions

When implementing utility functions for your BrainyFlow project:

1. Create a separate file for each utility function in the `utils/` directory.
2. Include a simple test or example usage in each file.
3. Document the input/output and purpose of each utility function.

Example structure:

{% tabs %}
{% tab title="Python" %}

```
my_project/
├── utils/
│   ├── __init__.py
│   ├── call_llm.py
│   ├── search_web.py
│   └── embed_text.py
└── ...
```

{% endtab %}

{% tab title="TypeScript" %}

```
my_project/
├── utils/
│   ├── callLlm.ts
│   ├── searchWeb.ts
│   └── embedText.ts
└── ...
```

{% endtab %}
{% endtabs %}

By following this approach, you can easily maintain and update your utility functions as needed, without being constrained by the framework's built-in utilities.
