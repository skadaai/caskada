---
title: 'BrainyFlow'
machine-display: false
---

# BrainyFlow

A [65-line](https://github.com/zvictor/BrainyFlow/blob/main/python/brainyflow.py) minimalist AI framework for _Agents, Task Decomposition, RAG, and more_.

- **Lightweight**: Just the core graph abstraction in 65 lines. ZERO dependencies, and vendor lock-in.
- **Expressive**: Everything you love from larger frameworks—([Multi-](./design_pattern/multi_agent.html))[Agents](./design_pattern/agent.html), [Workflow](./design_pattern/workflow.html), [RAG](./design_pattern/rag.html), and more.
- **Agentic-Coding**: Intuitive enough for AI agents to help humans build complex LLM applications.

<div align="center">
  <img src="https://github.com/the-pocket/.github/raw/main/assets/meme.jpg?raw=true" width="400"/>
</div>

## Core Abstraction

BrainyFlow models LLM workflows as a **Graph + Shared Store**:

- [Node](./core_abstraction/node.md) handles simple (LLM) tasks with a clear lifecycle.
- [Flow](./core_abstraction/flow.md) connects nodes through **Actions** (labeled edges).
- [Shared Store](./core_abstraction/communication.md) enables communication between nodes within flows.
- [Batch](./core_abstraction/batch.md) nodes/flows allow for data-intensive tasks.
- [(Advanced) Throttling](./core_abstraction/throttling.md) helps manage concurrency and rate limits.

<div align="center">
  <img src="https://github.com/the-pocket/.github/raw/main/assets/abstraction.png" width="500"/>
</div>

## Design Patterns

BrainyFlow makes it easy to implement popular design patterns:

- [Agent](./design_pattern/agent.md) autonomously makes decisions based on context.
- [Workflow](./design_pattern/workflow.md) chains multiple tasks into sequential pipelines.
- [RAG](./design_pattern/rag.md) integrates data retrieval with generation.
- [Map Reduce](./design_pattern/mapreduce.md) splits data tasks into Map and Reduce steps.
- [Structured Output](./design_pattern/structure.md) formats outputs consistently.
- [(Advanced) Multi-Agents](./design_pattern/multi_agent.md) coordinate multiple agents.

<div align="center">
  <img src="https://github.com/the-pocket/.github/raw/main/assets/design.png" width="500"/>
</div>

## Utility Functions

BrainyFlow **does not** provide built-in utilities. Instead, we offer _examples_ that you can implement yourself:

- [LLM Wrapper](./utility_function/llm.md)
- [Visualization and Debugging](./utility_function/viz.md)
- [Web Search](./utility_function/websearch.md)
- [Chunking](./utility_function/chunking.md)
- [Embedding](./utility_function/embedding.md)
- [Vector Databases](./utility_function/vector.md)
- [Text-to-Speech](./utility_function/text_to_speech.md)

**Why not built-in?** We believe it's a _bad practice_ to include vendor-specific APIs in a general framework:

- _API Volatility_: Frequent changes lead to heavy maintenance for hardcoded APIs.
- _Flexibility_: You may want to switch vendors, use fine-tuned models, or run them locally.
- _Optimizations_: Prompt caching, batching, and streaming are easier without vendor lock-in.

## Quick Start

New to BrainyFlow? Check out our [Getting Started](./getting_started.md) guide to build your first flow in no time.

## Ready to Build Self-Coding Apps?

Check out [Agentic Coding Guidance](./agentic_coding.md), the fastest way to develop self-coding LLM projects with BrainyFlow!
