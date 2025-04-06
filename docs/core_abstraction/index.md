# Understanding BrainyFlow's Mental Model

BrainyFlow is built around a simple but powerful mental model that separates _data flow_ from _computation_. This separation of concerns makes complex LLM applications more maintainable and easier to reason about.

## Core Philosophy

1. **Separation of Concerns**: Keep data storage (shared store) separate from computation logic (nodes)
2. **Explicit Data Flow**: Make data dependencies between steps clear and traceable
3. **Composability**: Build complex systems from simple, reusable components
4. **Resilience**: Handle failures gracefully with retries and fallbacks

## The Graph + Shared Store Pattern

The fundamental pattern in BrainyFlow combines two key elements:

- **Computation Graph**: A directed graph where nodes represent discrete units of work and edges represent the flow of control
- **Shared Store**: A global data structure that enables communication between nodes

This pattern offers several advantages:

- Clear visualization of application logic
- Easy identification of bottlenecks
- Simple debugging of individual components
- Natural parallelization opportunities

## Key Components

BrainyFlow's architecture is based on these fundamental building blocks:

- **[Node](./node.md)**: The basic unit of work with a clear lifecycle (`prep -> exec -> post`)
- **[Flow](./flow.md)**: Connects nodes together through action-based transitions
- **[Communication](./communication.md)**: Enables data sharing between nodes via Shared Store and Params
- **[Batch](./batch.md)**: Handles processing of multiple items sequentially or in parallel
- **[Throttling](./throttling.md)**: Manages concurrency and rate limits for external API calls

## How They Work Together

1. **Nodes** perform individual tasks with a clear lifecycle:

   - `prep`: Read from shared store and prepare data
   - `exec`: Execute computation (often LLM calls)
   - `post`: Process results and write to shared store

2. **Flows** orchestrate nodes by:

   - Starting with a designated node
   - Following action-based transitions between nodes
   - Supporting branching, looping, and nested flows

3. **Communication** happens through:

   - **Shared Store**: A global dictionary accessible to all nodes
   - **Params**: Node-specific configuration passed down from parent flows

4. **Batch Processing** enables:
   - Processing multiple items sequentially or in parallel
   - Handling large datasets efficiently
   - Supporting nested batch operations

## Design Philosophy

BrainyFlow's core abstractions follow these principles:

- **Separation of Concerns**: Data storage (shared store) is separate from computation logic (nodes)
- **Composability**: Nodes and flows can be combined in various ways to create complex workflows
- **Flexibility**: The framework imposes minimal constraints while providing powerful patterns
- **Reliability**: Built-in retry mechanisms and error handling improve robustness

## Getting Started

If you're new to BrainyFlow, we recommend exploring these core abstractions in the following order:

1. [Node](./node.md) - Understand the basic building block
2. [Flow](./flow.md) - Learn how to connect nodes together
3. [Communication](./communication.md) - See how nodes share data
4. [Batch](./batch.md) - Explore handling multiple items
5. [Throttling](./throttling.md) - Learn about managing concurrency

Once you understand these core abstractions, you'll be ready to implement various [Design Patterns](../design_pattern/index.md) to solve real-world problems.
