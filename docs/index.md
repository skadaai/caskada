---
title: 'BrainyFlow'
machine-display: false
---
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://cdn.jsdelivr.net/gh/zvictor/brainyflow@main/.github/media/logo-dark.png">
    <source media="(prefers-color-scheme: light)" srcset="https://cdn.jsdelivr.net/gh/zvictor/brainyflow@main/.github/media/logo-light.png">
    <img width="280"  src="https://cdn.jsdelivr.net/gh/zvictor/brainyflow@main/.github/media/logo-light.png">
  </picture>
<p>

<p align="center">
  A <a href="https://github.com/zvictor/BrainyFlow/blob/main/python/brainyflow.py">65-line</a> minimalist AI framework 🤯
  <br />
  <sub>Let Agents build Agents with zero bloat, zero dependencies, zero vendor lock-in 😮</sub>
</p>

<p align="center">

  <a href="https://pypi.org/project/brainyflow">
   <img src="https://img.shields.io/pypi/dw/brainyflow?logo=python&label=Python&style=flat-square" >
  </a>
  <a href="https://npm.com/packages/brainyflow">
   <img src="https://img.shields.io/npm/d18m/brainyflow?logo=typescript&label=Typescript&style=flat-square" >
  </a>
  <a href="https://discord.gg/hUHHE9Sa6T">
    <img src="https://img.shields.io/discord/1346833819172601907?logo=discord&style=flat-square" >
  </a>
  <a href="https://github.com/zvictor/brainyflow">
    <img src="https://img.shields.io/github/stars/zvictor/BrainyFlow?logo=github&style=flat-square" >
  </a>
  <a href="https://github.com/sponsors/zvictor">
    <img src="https://img.shields.io/github/sponsors/zvictor?logo=github&style=flat-square" >
  </a>
</p>

BrainyFlow is a framework enabling _Agentic Coding_ through powerful abstractions.

It provides a simple interface for building complex AI applications based on _nested directed graphs_ with shared state.
It enables both humans and AI assistants to collaborate effectively on designing and implementing AI systems.

## Features

- **Brain-Easy 🧠**: Intuitive for both humans and AI assistants
- **Minimalist Design ✨**: Core abstractions in just (_you heard it right!_) 65 lines of code
- **Freedom 🔓**: Zero bloat, zero dependencies, zero vendor lock-in.
- **Composable 🧩**: Build complex systems from simple, reusable components
- **Powerful 💪**: Supports everything you love—([Multi-](./design_pattern/multi_agent))[Agents](./design_pattern/agent), [Workflow](./design_pattern/workflow), [RAG](./design_pattern/rag), and more.
- **Agentic-Coding 🤖**: Let AI Agents (e.g., Cursor AI) build Agents for 10x productivity
- **Universal 🌈**: Works with any LLM provider or API

## Why Brainy Flow?

Current LLM frameworks are bloated... You actually only need 65 lines for a robust LLM Framework!

<div align="center">
  <img src="https://raw.githubusercontent.com/zvictor/brainyflow/main/.github/media/meme.jpg" width="500"/>

|                | **Abstraction** |                     **App-Specific Wrappers**                      |                       **Vendor-Specific Wrappers**                       |                **Lines**                 |                  **Size**                   |
| -------------- | :-------------: | :----------------------------------------------------------------: | :----------------------------------------------------------------------: | :--------------------------------------: | :-----------------------------------------: |
| LangChain      |  Agent, Chain   |      Many <br><sup><sub>(e.g., QA, Summarization)</sub></sup>      |      Many <br><sup><sub>(e.g., OpenAI, Pinecone, etc.)</sub></sup>       |                   405K                   |                   +166MB                    |
| CrewAI         |  Agent, Chain   | Many <br><sup><sub>(e.g., FileReadTool, SerperDevTool)</sub></sup> | Many <br><sup><sub>(e.g., OpenAI, Anthropic, Pinecone, etc.)</sub></sup> |                   18K                    |                   +173MB                    |
| SmolAgent      |      Agent      |   Some <br><sup><sub>(e.g., CodeAgent, VisitWebTool)</sub></sup>   |  Some <br><sup><sub>(e.g., DuckDuckGo, Hugging Face, etc.)</sub></sup>   |                    8K                    |                   +198MB                    |
| LangGraph      |  Agent, Graph   |       Some <br><sup><sub>(e.g., Semantic Search)</sub></sup>       | Some <br><sup><sub>(e.g., PostgresStore, SqliteSaver, etc.) </sub></sup> |                   37K                    |                    +51MB                    |
| AutoGen        |      Agent      |   Some <br><sup><sub>(e.g., Tool Agent, Chat Agent)</sub></sup>    | Many <sup><sub>[Optional]<br> (e.g., OpenAI, Pinecone, etc.)</sub></sup> | 7K <br><sup><sub>(core-only)</sub></sup> | +26MB <br><sup><sub>(core-only)</sub></sup> |
| **BrainyFlow** |    **Graph**    |                              **None**                              |                                 **None**                                 |                  **65**                  |                 **few KB**                  |

</div>

![](https://raw.githubusercontent.com/zvictor/brainyflow/master/.github/media/divider.png)

## How does BrainyFlow work?

