# Understanding BrainyFlow's Core Abstractions

BrainyFlow is built around a simple yet powerful abstraction: the **nested directed graph with shared store**. This mental model separates _data flow_ from _computation_, making complex LLM applications more maintainable and easier to reason about.

<div align="center">
  <img src="https://raw.githubusercontent.com/zvictor/brainyflow/main/.github/media/abstraction.jpg" width="1300"/>
</div>

## Core Philosophy

BrainyFlow follows these fundamental principles:

1. **Modularity & Composability**: Build complex systems from simple, reusable components that are easy to build, test, and maintain
2. **Explicitness**: Make data dependencies between steps clear and traceable
3. **Separation of Concerns**: Data storage (shared store) remains separate from computation logic (nodes)
4. **Minimalism**: The framework provides only essential abstractions, avoiding vendor-specific implementations while supporting various high-level AI design paradigms (agents, workflows, map-reduce, etc.)
5. **Resilience**: Handle failures gracefully with retries and fallbacks

## The Graph + Shared Store Pattern

The fundamental pattern in BrainyFlow combines two key elements:

- **Computation Graph**: A directed graph where nodes represent discrete units of work and edges represent the flow of control.
- **Shared `Memory` Object**: A state management store that enables communication between nodes, separating `global` and `local` state.

This pattern offers several advantages:

- **Clear visualization** of application logic
- **Easy identification** of bottlenecks
- **Simple debugging** of individual components
- **Natural parallelization** opportunities

## Key Components

BrainyFlow's architecture is based on these fundamental building blocks:

| Component             | Description                                    | Key Features                                                                                                |
| --------------------- | ---------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| [Node](./node.md)     | The basic unit of work                         | Clear lifecycle (`prep` → `exec` → `post`), fault tolerance (retries), graceful fallbacks                   |
| [Flow](./flow.md)     | Connects nodes together                        | Action-based transitions, branching, looping (with cycle detection), nesting, sequential/parallel execution |
| [Memory](./memory.md) | Manages state accessible during flow execution | Shared `global` store, forkable `local` store, cloning for isolation                                        |

## How They Work Together

1. **Nodes** perform individual tasks with a clear lifecycle:

   - `prep`: Read from shared store and prepare data
   - `exec`: Execute computation (often LLM calls), cannot access memory directly.
   - `post`: Process results, write to shared store, and trigger next actions

2. **Flows** orchestrate nodes by:

   - Starting with a designated `start` node.
   - Following action-based transitions (driven by `trigger` calls in `post`) between nodes.
   - Supporting branching, looping, and nested flows.
   - Executing triggered branches sequentially (`Flow`) or concurrently (`ParallelFlow`).
   - Supporting nested batch operations.

3. **Communication** happens through the `memory` instance provided to each node's lifecycle methods (in `prep` and `post` methods):

   - **Global Store**: A shared object accessible throughout the flow. Nodes typically write results here.
   - **Local Store**: An isolated object specific to a node and its downstream path, typically populated via `forkingData` in `trigger` calls.

## Getting Started

If you're new to BrainyFlow, we recommend exploring these core abstractions in the following order:

1. [Node](./node.md) - Understand the basic building block
2. [Flow](./flow.md) - Learn how to connect nodes together
3. [Memory](./memory.md) - See how nodes share data

Once you understand these core abstractions, you'll be ready to implement various [Design Patterns](../design_pattern/index.md) to solve real-world problems.
