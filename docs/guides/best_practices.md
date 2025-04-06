# BrainyFlow Best Practices

## Node Design

1. **Keep Nodes Focused**: Each node should do one thing well
2. **Idempotent Execution**: Design `exec()` methods to be safely retryable
3. **Graceful Degradation**: Implement fallbacks for when things go wrong
4. **Proper Error Handling**: Use `exec_fallback` to handle failures gracefully

## Shared Store Management

1. **Schema Design**: Define a clear schema for your shared store
2. **Namespacing**: Use namespaces to avoid key collisions
3. **Immutability**: Treat shared store values as immutable when possible
4. **Documentation**: Document the expected structure of your shared store

## Flow Design

1. **Visualization First**: Design your flow visually before coding
2. **Test Incrementally**: Build and test one section of your flow at a time
3. **Error Paths**: Always include paths for handling errors
4. **Monitoring**: Add logging at key points in your flow

## Project Structure

A well-organized project structure enhances maintainability and collaboration:

{% tabs %}
{% tab title="Python (simple)" %}

```
my_simple_project/
├── main.py
├── nodes.py
├── flow.py
├── utils/
│   ├── __init__.py
│   ├── call_llm.py
│   └── search_web.py
├── requirements.txt
└── docs/
    └── design.md
```

{% endtab %}

{% tab title="Python (complex)" %}

```
my_complex_project/
├── main.py                # Entry point
├── nodes/                 # Node implementations
│   ├── __init__.py
│   ├── input_nodes.py
│   ├── processing_nodes.py
│   └── output_nodes.py
├── flows/                 # Flow definitions
│   ├── __init__.py
│   └── main_flow.py
├── utils/                 # Utility functions
│   ├── __init__.py
│   ├── llm.py
│   ├── database.py
│   └── web_search.py
├── tests/                 # Test cases
│   ├── test_nodes.py
│   └── test_flows.py
├── config/                # Configuration
│   └── settings.py
├── requirements.txt       # Dependencies
└── docs/                  # Documentation
    ├── design.md          # High-level design
    └── api.md             # API documentation
```

{% endtab %}

{% tab title="TypeScript (simple)" %}

```
my_project/
├── src/
│   ├── main.ts
│   ├── nodes.ts
│   ├── flow.ts
│   └── utils/
│       ├── callLLM.ts
│       └── searchWeb.ts
├── package.json
└── docs/
    └── design.md
```

{% endtab %}

{% tab title="TypeScript (complex)" %}

```
my_complex_project/
├── src/                      # Source code
│   ├── index.ts              # Entry point
│   ├── nodes/                # Node implementations
│   │   ├── index.ts          # Exports all nodes
│   │   ├── inputNodes.ts
│   │   ├── processingNodes.ts
│   │   └── outputNodes.ts
│   ├── flows/                # Flow definitions
│   │   ├── index.ts          # Exports all flows
│   │   └── mainFlow.ts
│   ├── utils/                # Utility functions
│   │   ├── index.ts          # Exports all utilities
│   │   ├── llm.ts
│   │   ├── database.ts
│   │   └── webSearch.ts
│   ├── types/                # Type definitions
│   │   ├── index.ts          # Exports all types
│   │   ├── node.types.ts
│   │   └── flow.types.ts
│   └── config/               # Configuration
│       └── settings.ts
├── dist/                     # Compiled JavaScript
├── tests/                    # Test cases
│   ├── nodes.test.ts
│   └── flows.test.ts
├── package.json              # Dependencies and scripts
└── docs/                     # Documentation
    ├── design.md             # High-level design
    └── api.md                # API documentation
```

{% endtab %}
{% endtabs %}

- **`docs/design.md`**: Contains project documentation for each step designed in [agentic coding](./agentic_coding.md). This should be _high-level_ and _no-code_.
- **`utils/`**: Contains all utility functions.
  - It's recommended to dedicate one file to each API call, for example `call_llm.py` or `search_web.ts`.
  - Each file should also include a `main()` function to try that API call
- **`nodes.py`** or **`nodes.ts`**: Contains all the node definitions.
- **`flow.py`** or **`flow.ts`**: Implements functions that create flows by importing node definitions and connecting them.
- **`main.py`** or **`main.ts`**: Serves as the project's entry point.
