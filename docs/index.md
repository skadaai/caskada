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
  <a href="https://npmjs.com/packages/brainyflow">
   <img src="https://img.shields.io/npm/d18m/brainyflow?logo=typescript&label=Typescript&style=flat-square" >
  </a>
  <a href="https://discord.gg/MdJJ29Xd">
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
- **Polyglot 🌍**:  Python and  Typescript are both supported.

![](https://raw.githubusercontent.com/zvictor/brainyflow/master/.github/media/divider.png)



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

The single file in <a href="https://github.com/zvictor/BrainyFlow/blob/main/python/brainyflow.py">Python</a> or <a href="https://github.com/zvictor/BrainyFlow/blob/main/typescript/brainyflow.ts">Typescript</a> capture the core abstraction of LLM frameworks: Graph!
<br>

<div align="center">
  <img src="https://raw.githubusercontent.com/zvictor/brainyflow/main/.github/media/abstraction.jpg" width="1300"/>
</div>
<br>

- [Node](./core_abstraction/node) handles simple (LLM) tasks with a clear lifecycle.
- [Flow](./core_abstraction/flow) connects nodes through **Actions** (labeled edges).
- [Shared Store](./core_abstraction/communication) enables communication between nodes within flows.
- [Batch](./core_abstraction/batch) nodes/flows allow for data-intensive tasks.

From there, it's easy to implement all popular design patterns:
<br>

<div align="center">
  <img src="https://raw.githubusercontent.com/zvictor/brainyflow/main/.github/media/design.jpg" width="1300"/>
</div>
<br>

- [Agent](./design_pattern/agent) autonomously makes decisions based on context.
- [Workflow](./design_pattern/workflow) chains multiple tasks into sequential pipelines.
- [RAG](./design_pattern/rag) integrates data retrieval with generation.
- [Map Reduce](./design_pattern/mapreduce) splits data tasks into Map and Reduce steps.
- [Structured Output](./design_pattern/structure) formats outputs consistently.
- [Multi-Agents](./design_pattern/multi_agent) coordinate multiple agents.

![](https://raw.githubusercontent.com/zvictor/brainyflow/master/.github/media/divider.png)

## Tutorials

<div align="center">
  
|  Name  | Difficulty    |  Description  |  
| :-------------:  | :-------------: | :--------------------- |  
| [Chat](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-chat) | ☆☆☆ <br> *Dummy*   | A basic chat bot with conversation history |
| [RAG](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-rag) | ☆☆☆ <br> *Dummy*   | A simple Retrieval-augmented Generation process |
| [Workflow](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-workflow) | ☆☆☆ <br> *Dummy*   | A writing workflow that outlines, writes content, and applies styling |
| [Map-Reduce](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-map-reduce) | ☆☆☆ <br> *Dummy* | A resume qualification processor using map-reduce pattern for batch evaluation |
| [Agent](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-agent) | ☆☆☆ <br> *Dummy*   | A research agent that can search the web and answer questions |
| [Streaming](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-llm-streaming) | ☆☆☆ <br> *Dummy*   | A real-time LLM streaming demo with user interrupt capability |
| [Multi-Agent](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-multi-agent) | ★☆☆ <br> *Beginner* | A Taboo word game for asynchronous communication between two agents |
| [Supervisor](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-supervisor) | ★☆☆ <br> *Beginner* | Research agent is getting unreliable... Let's build a supervision process|
| [Parallel](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-parallel-batch) | ★☆☆ <br> *Beginner*   | A parallel execution demo that shows 3x speedup |
| [Thinking](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-thinking) | ★☆☆ <br> *Beginner*   | Solve complex reasoning problems through Chain-of-Thought |
| [Memory](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-chat-memory) | ★☆☆ <br> *Beginner* | A chat bot with short-term and long-term memory |

</div>

And many more available for all levels! [Check them all out!](https://github.com/zvictor/BrainyFlow/tree/main/cookbook)

![](https://raw.githubusercontent.com/zvictor/brainyflow/master/.github/media/divider.png)

<!-- ## How to Use Brainy Flow?

🚀 Through **Agentic Coding**—the fastest LLM App development paradigm-where _humans design_ and _agents code_!

<br />

- Want to learn **Agentic Coding**?
  - To setup, read this [post](https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to)!
  - Check out [my YouTube](https://www.youtube.com/@ZacharyLLM?sub_confirmation=1)! Read this [Guide](./agentic_coding)!
- Want to build your own LLM App? Start with our [Python template](https://github.com/zvictor/Brainyflow-Template-Python) or [Typescript template](https://github.com/zvictor/Brainyflow-Template-Typescript)!

![](https://raw.githubusercontent.com/zvictor/brainyflow/master/.github/media/divider.png) -->

## Quick Start

New to BrainyFlow? Check out our [Getting Started](./introduction/getting_started) guide to build your first flow in no time.

## Ready to Build Self-Coding Apps?

Check out [Agentic Coding Guidance](./guides/agentic_coding), the fastest way to develop self-coding LLM projects with BrainyFlow!

![](https://raw.githubusercontent.com/zvictor/brainyflow/master/.github/media/divider.png)

## Acknowledgement

We would like to extend our deepest gratitude to the creators and contributors of the PocketFlow framework, from which brainyFlow originated as a fork.

## Liability Disclaimer

BrainyFlow is provided "as is" without any warranties or guarantees.  
We do not take responsibility for how the generated output is used, including but not limited to its accuracy, legality, or any potential consequences arising from its use.

## Sponsors

<p align="center">
  <a style="color: inherit" href="https://github.com/sponsors/zvictor?utm_source=brainyflow&utm_medium=sponsorship&utm_campaign=brainyflow&utm_id=brainyflow">
    <img width="150" src="https://cdn.jsdelivr.net/gh/zvictor/brainyflow@main/.github/media/brain.png"  />
  </a><br /><br />
  BrainyFlow runs on 65 lines of code and your generosity! 💰<br />
    <a style="color: inherit" href="https://github.com/sponsors/zvictor?utm_source=brainyflow&utm_medium=sponsorship&utm_campaign=brainyflow&utm_id=brainyflow">
      Help us deliver more AI with less code (but maybe more caffeine)
    </a> ☕<br /><br />
    <a style="color: inherit" href="https://github.com/sponsors/zvictor?utm_source=brainyflow&utm_medium=sponsorship&utm_campaign=brainyflow&utm_id=brainyflow">Your support</a> helps keep it minimal, powerful, and dependency-free! 🚀
  </a>
</p>

![](https://raw.githubusercontent.com/zvictor/brainyflow/master/.github/media/divider.png)
