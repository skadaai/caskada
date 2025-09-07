# Best Practices for Caskada Development

Developing robust and maintainable applications with Caskada involves adhering to certain best practices. These guidelines help ensure your flows are clear, efficient, and easy to debug and extend.

## General Principles

- **Modularity**: Break down complex problems into smaller, manageable nodes and sub-flows.
- **Explicitness**: Make data dependencies and flow transitions clear and easy to follow.
- **Separation of Concerns**: Keep computation logic (in `exec`) separate from data handling (`prep`, `post`) and orchestration (`Flow`).

## Design & Architecture

- **Memory Planning**: Clearly define the structure of your global and local memory stores upfront (e.g., using `TypedDict` in Python or interfaces/types in TypeScript). Decide what state needs to be globally accessible versus what should be passed down specific branches via `forkingData` into the local store.
- **Action Naming**: Use descriptive, meaningful action names (e.g., `'user_clarification_needed'`, `'data_validated'`) rather than generic names like `'next'` or `'step2'`. This improves the readability of your flow logic and the resulting `ExecutionTree`.
- **Explicit Transitions**: Clearly define transitions for all expected actions a node might trigger using `.on()` or `>>`. Consider adding a default `.next()` transition for unexpected or general completion actions.
- **Cycle Management**: Be mindful of loops. Use the `maxVisits` option in the `Flow` constructor (default is now 15, can be customized) to prevent accidental infinite loops. The `ExecutionTree` can also help visualize loops.
- **Error Handling Strategy**:
  - Use the built-in retry mechanism (`maxRetries`, `wait` in Node constructor) for transient errors in `exec()`.
  - Implement `execFallback(prepRes, error: NodeError)` to provide a default result or perform cleanup if retries fail.
  - Define specific error-handling nodes and transitions (e.g., `node.on('error', errorHandlerNode)`) for critical errors.
- **Parallelism Choice**: Use `ParallelFlow` when a node fans out to multiple independent branches that can benefit from concurrent execution. Stick with the standard `Flow` (sequential branch execution) if branches have interdependencies or if concurrent modification of shared global memory state is a concern.
- **Memory Isolation with `forkingData`**: When triggering successors, use the `forkingData` argument to pass data specifically to the `local` store of the next node(s) in a branch. This keeps the `global` store cleaner and is essential for correct state management in parallel branches.
- **Test Incrementally**:
  - Test individual nodes in isolation using `node.run(memory)`. Remember this only runs the single node and does not follow graph transitions.
  - Test sub-flows before integrating them into larger pipelines.
  - Write tests that verify the final state of the `Memory` object and, if important, the structure of the `ExecutionTree` returned by `flow.run()`.
- **Avoid Deep Nesting of Flows**: While nesting flows is a powerful feature for modularity, keep the hierarchy reasonably flat (e.g., 2-3 levels deep) to maintain understandability and ease of debugging.

## Code Quality

- **Type Hinting/Interfaces**: Use Python's type hints (`TypedDict`, `List`, `Dict`, `Optional`, `Union`) and TypeScript interfaces/types to clearly define the expected shapes of `Memory` stores, `prep_res`, `exec_res`, and `actions`. This improves readability, enables static analysis, and reduces runtime errors.
- **Docstrings/Comments**: Document your nodes, their purpose, expected inputs/outputs, and any complex logic.
- **Consistent Naming**: Follow consistent naming conventions for nodes, actions, and memory keys.
- **Idempotent `exec`**: Strive to make your `exec` methods idempotent where possible, meaning running them multiple times with the same input produces the same result and no additional side effects. This simplifies retries and debugging.


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
