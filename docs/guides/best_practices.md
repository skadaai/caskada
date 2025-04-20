# BrainyFlow Best Practices

## Node Design

1.  **Keep Nodes Focused**: Each node should perform a single, well-defined task.
2.  **Idempotent Execution**: If using retries (`maxRetries > 1`), design the `exec()` method to be idempotent (produce the same result for the same input) as it might be called multiple times.
3.  **Clear Lifecycle**: Use `prep` to read/prepare data, `exec` for computation (no memory access), and `post` to write results and trigger successors.
4.  **Graceful Degradation**: Implement `execFallback` in `Node` subclasses to handle errors gracefully after all retries are exhausted, potentially returning a default value instead of throwing an error.

## Memory (State) Management

1.  **Schema Design**: Define clear interfaces (in TypeScript) or conventions (in Python) for your `GlobalStore` and `LocalStore` structures.
2.  **Global vs. Local**: Use the `GlobalStore` (accessed via `memory.prop = value`) for state shared across the entire flow. Use the `LocalStore` (populated via `forkingData` in `trigger`) for context specific to a particular execution branch.
3.  **Minimize Global State**: Prefer passing data locally via `forkingData` when possible to keep the global state clean and reduce potential conflicts, especially in parallel flows.
4.  **Read Transparently**: Always read via the `memory` proxy (e.g., `memory.value`); it handles the local-then-global lookup.

## Flow Design

1.  **Visualization First**: Sketch your flow diagram (e.g., using Mermaid) before coding to clarify logic and transitions.
2.  **Modularity**: Break complex processes into smaller, potentially nested, sub-flows (`Flow` extends `BaseNode`).
3.  **Explicit Transitions**: Clearly define transitions using descriptive action names (`node.on('action', nextNode)`). Consider default paths (`node.next(defaultNode)`).
4.  **Error Paths**: Define explicit transitions for error conditions (e.g., `node.on('error', errorHandlerNode)`) or handle errors within `execFallback`.
5.  **Cycle Management**: Use the `maxVisits` option in the `Flow` constructor to prevent infinite loops.
6.  **Parallelism**: Choose `ParallelFlow` for independent branches that can run concurrently; use `Flow` (sequential) otherwise or if order matters.
7.  **Test Incrementally**: Test individual nodes (`node.run()`) and sub-flows before integrating them.

## Project Structure

A well-organized project structure enhances maintainability and collaboration:

{% tabs %}
{% tab title="Python (simple)" %}

```haskell
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

```haskell
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

```haskell
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

```haskell
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
