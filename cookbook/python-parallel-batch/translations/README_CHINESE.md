<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://cdn.jsdelivr.net/gh/zvictor/brainyflow@main/.github/media/logo-dark.png">
    <source media="(prefers-color-scheme: light)" srcset="https://cdn.jsdelivr.net/gh/zvictor/brainyflow@main/.github/media/logo-light.png">
    <img width="280" alt="Brainyflow的Logo" src="https://cdn.jsdelivr.net/gh/zvictor/brainyflow@main/.github/media/logo-light.png">
  </picture>
<p>

<p align="center">
  一个极度极简的AI框架（仅<a href="https://github.com/zvictor/BrainyFlow/blob/main/python/brainyflow.py">200行Python代码</a>！🤯）

  <br />
  用最少的代码和最大的自由构建强大的AI代理。
  <br />
  <sub>让代理相互构建，零冗余、零依赖、零厂商锁定 😮</sub>
</p>

<p align="center">

  <a href="https://pypi.org/project/brainyflow">
   <img src="https://img.shields.io/pypi/dw/brainyflow?logo=python&label=Python&style=flat-square" alt="Python版本">
  </a>
  <a href="https://npmjs.com/packages/brainyflow">
   <img src="https://img.shields.io/npm/d18m/brainyflow?logo=typescript&label=Typescript&style=flat-square" alt="Typescript版本">
  </a>
  <a href="https://discord.gg/N9mVvxRXyH">
    <img src="https://img.shields.io/discord/1346833819172601907?logo=discord&style=flat-square" alt="Discord">
  </a>
  <a href="https://github.com/zvictor/brainyflow">
    <img src="https://img.shields.io/github/stars/zvictor/BrainyFlow?logo=github&style=flat-square" alt="GitHub仓库">
  </a>
  <a href="https://github.com/sponsors/zvictor">
    <img src="https://img.shields.io/github/sponsors/zvictor?logo=github&style=flat-square" alt="GitHub赞助者">
  </a>
</p>

BrainyFlow是一个通过强大抽象实现_代理编程_的框架。

它提供了一个简单的接口，用于构建基于_嵌套有向图_和共享状态的复杂AI应用。它使得人类和AI助手能够高效协作，共同设计和实现AI系统。

## 特性

- **脑易用 🧠**：对人类和AI助手都直观易懂
- **极简设计 ✨**：核心抽象仅需（没错！）200行代码
- **自由 🔓**：零冗余、零依赖、零厂商锁定
- **可组合 🧩**：用简单可复用的组件构建复杂系统
- **强大 🦾**：支持你喜爱的一切——([多](https://brainy.gitbook.io/flow/design_pattern/multi_agent))[代理](https://brainy.gitbook.io/flow/design_pattern/agent)、[工作流](https://brainy.gitbook.io/flow/design_pattern/workflow)、[RAG](https://brainy.gitbook.io/flow/design_pattern/rag)等
- **代理编程 🤖**：专为AI辅助开发设计
- **通用 🌈**：兼容任何LLM提供商或API
- **多语言 🌍**：<!-- gitbook-ignore-start --><a href="https://pypi.org/project/brainyflow"><img src="https://github.com/zvictor/brainyflow/raw/main/.github/media/python.svg" width="16" height="16" alt="Python Logo" style="vertical-align: middle; margin: 0 2px;"></a><!-- gitbook-ignore-end --> Python和<!-- gitbook-ignore-start --><a href="https://npmjs.com/packages/brainyflow"><img src="https://github.com/zvictor/brainyflow/raw/main/.github/media/typescript.svg" width="16" height="16" alt="Typescript Logo" style="vertical-align: middle; margin: 0 2px;"></a><!-- gitbook-ignore-end --> TypeScript皆支持

![](https://raw.githubusercontent.com/zvictor/brainyflow/master/.github/media/divider.png)

<!-- gitbook-ignore-start -->

## 文档

我们的文档包容性强，适合生物和合成智能体。<br />
根据你（或你被设定的）认知起点选择：

\>> [我是碳基生命 🐥](https://brainy.gitbook.io/flow/introduction/getting_started) <<

\>> [我是硅基生命 🤖](https://flow.brainy.sh/docs.txt) <<

![](https://raw.githubusercontent.com/zvictor/brainyflow/master/.github/media/divider.png)

<!-- gitbook-ignore-end -->

## 为什么选择Brainy Flow?

现有的LLM框架过于臃肿... 实际上，200行代码就能实现一个健壮的LLM框架！

<div align="center">
  <img src="https://raw.githubusercontent.com/zvictor/brainyflow/main/.github/media/meme.jpg" width="500"/>

|                                                                                                                                                                                                                | **抽象层** |                     **应用特定封装**                      |                       **厂商特定封装**                       |                **代码行数**                 |                  **体积**                   |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------: | :----------------------------------------------------------------: | :----------------------------------------------------------------------: | :--------------------------------------: | :-----------------------------------------: |
| LangChain                                                                                                                                                                                                      |  代理, 链式  |      大量 <br><sup><sub>(如问答、摘要生成)</sub></sup>       |      大量 <br><sup><sub>(如OpenAI、Pinecone等)</sub></sup>       |                   405K                   |                   +166MB                    |
| CrewAI                                                                                                                                                                                                         |  代理, 链式  | 大量 <br><sup><sub>(如文件读取工具、搜索工具)</sub></sup> | 大量 <br><sup><sub>(如OpenAI、Anthropic、Pinecone等)</sub></sup> |                   18K                    |                   +173MB                    |
| SmolAgent                                                                                                                                                                                                      |      代理      |   部分 <br><sup><sub>(如代码代理、网页访问工具)</sub></sup>    |  部分 <br><sup><sub>(如DuckDuckGo、Hugging Face等)</sub></sup>   |                    8K                    |                   +198MB                    |
| LangGraph                                                                                                                                                                                                      |  代理, 图结构  |       部分 <br><sup><sub>(如语义搜索)</sub></sup>        | 部分 <br><sup><sub>(如Postgres存储、Sqlite存储等)</sub></sup> |                   37K                    |                    +51MB                    |
| AutoGen                                                                                                                                                                                                        |      代理      |   部分 <br><sup><sub>(如工具代理、聊天代理)</sub></sup>     | 大量 <sup><sub>[可选]<br> (如OpenAI、Pinecone等)</sub></sup> | 7K <br><sup><sub>(仅核心)</sub></sup> | +26MB <br><sup><sub>(仅核心)</sub></sup> |
| **BrainyFlow** <!-- gitbook-ignore-start --><img src="https://github.com/zvictor/brainyflow/raw/main/.github/media/typescript.svg" width="16" height="16" alt="Typescript Logo"><!-- gitbook-ignore-end -->.ts |    **图结构**    |                              **无**                              |                                 **无**                                 |                 **300**                  |                 **几KB**                  |
| **BrainyFlow** <!-- gitbook-ignore-start --><img src="https://github.com/zvictor/brainyflow/raw/main/.github/media/python.svg" width="16" height="16" alt="Python Logo"><!-- gitbook-ignore-end -->.py         |    **图结构**    |                              **无**                              |                                 **无**                                 |                 **200**                  |                 **几KB**                  |

</div>

![](https://raw.githubusercontent.com/zvictor/brainyflow/master/.github/media/divider.png)

## BrainyFlow如何工作?

<a href="https://github.com/zvictor/BrainyFlow/blob/main/python/brainyflow.py"><!-- gitbook-ignore-start --><img src="https://github.com/zvictor/brainyflow/raw/main/.github/media/python.svg" width="16" height="16" alt="Python Logo" style="vertical-align: middle; margin: 0 2px;"> <!-- gitbook-ignore-end -->Python</a>或<a href="https://github.com/zvictor/BrainyFlow/blob/main/typescript/brainyflow.ts"><!-- gitbook-ignore-start --><img src="https://github.com/zvictor/brainyflow/raw/main/.github/media/typescript.svg" width="16" height="16" alt="Typescript Logo" style="vertical-align: middle; margin: 0 2px;"> <!-- gitbook-ignore-end -->TypeScript</a>的单文件封装了LLM框架的核心抽象：图结构！
<br>

<div align="center">
  <img src="https://raw.githubusercontent.com/zvictor/brainyflow/main/.github/media/abstraction.jpg" width="1300"/>
</div>
<br>

- [节点](https://brainy.gitbook.io/flow/core_abstraction/node)处理简单的(LLM)任务，具有明确的生命周期(`准备` → `执行` → `后处理`)。
- [流程](https://brainy.gitbook.io/flow/core_abstraction/flow)通过**动作**(标记边)连接节点，协调执行。
- [内存](https://brainy.gitbook.io/flow/core_abstraction/memory)管理共享(`全局`)和隔离(`局部`)状态，促进节点间通信。

基于此，可以轻松实现所有热门设计模式：
<br>

<div align="center">
  <img src="https://raw.githubusercontent.com/zvictor/brainyflow/main/.github/media/design.jpg" width="1300"/>
</div>
<br>

- [代理](https://brainy.gitbook.io/flow/design_pattern/agent)根据上下文自主决策。
- [工作流](https://brainy.gitbook.io/flow/design_pattern/workflow)将多个任务串联成顺序管道。
- [RAG](https://brainy.gitbook.io/flow/design_pattern/rag)整合数据检索与生成。
- [Map Reduce](https://brainy.gitbook.io/flow/design_pattern/mapreduce)将数据处理任务分解为映射和归约步骤。
- [结构化输出](https://brainy.gitbook.io/flow/design_pattern/structure)规范化输出格式。
- [多代理](https://brainy.gitbook.io/flow/design_pattern/multi_agent)协调多个代理协作。

![](https://raw.githubusercontent.com/zvictor/brainyflow/master/.github/media/divider.png)

## 教程

<div align="center">
  
|  名称  | 难度    |  描述  |  
| :-------------:  | :-------------: | :--------------------- |  
| [聊天机器人](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-chat) | ☆☆☆ <br> *入门*   | 带对话历史的基础聊天机器人 |
| [RAG](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-rag) | ☆☆☆ <br> *入门*   | 简单的检索增强生成流程 |
| [工作流](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-workflow) | ☆☆☆ <br> *入门*   | 包含大纲编写、内容创作和样式应用的写作流程 |
| [Map-Reduce](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-map-reduce) | ☆☆☆ <br> *入门* | 使用map-reduce模式批量评估简历 |
| [代理](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-agent) | ☆☆☆ <br> *入门*   | 能搜索网络并回答问题的研究代理 |
| [流式处理](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-llm-streaming) | ☆☆☆ <br> *入门*   | 支持用户中断的实时LLM流式演示 |
| [多代理](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-multi-agent) | ★☆☆ <br> *初级* | 两个代理间异步沟通的禁忌词游戏 |
| [监督者](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-supervisor) | ★☆☆ <br> *初级* | 研究代理不可靠？建立监督流程 |
| [并行处理](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-parallel-batch) | ★☆☆ <br> *初级*   | 3倍加速的并行执行演示 |
| [思考链](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-thinking) | ★☆☆ <br> *初级*   | 通过思维链解决复杂推理问题 |
| [记忆](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-chat-memory) | ★☆☆ <br> *初级* | 带短期和长期记忆的聊天机器人 |

</div>

还有更多适合各个水平的教程！[全部查看](https://github.com/zvictor/BrainyFlow/tree/main/cookbook)

![](https://raw.githubusercontent.com/zvictor/brainyflow/master/.github/media/divider.png)

## 快速开始

初次使用BrainyFlow? 查看[入门指南](https://brainy.gitbook.io/flow/introduction/getting_started)，快速构建你的第一个流程。

## 准备好构建自编程应用了吗？

了解[代理编程指南](https://brainy.gitbook.io/flow/guides/agentic_coding)，用BrainyFlow快速开发自编程LLM项目的最快方式！

![](https://raw.githubusercontent.com/zvictor/brainyflow/master/.github/media/divider.png)

## 致谢

我们衷心感谢PocketFlow框架的创建者和贡献者，BrainyFlow最初是从其分支发展而来。

## 免责声明

BrainyFlow按"原样"提供，不附带任何保证。<br />
我们对生成输出的使用方式不承担责任，包括但不限于其准确性、合法性或使用可能产生的任何后果。

## 赞助商

<p align="center">
  <a style="color: inherit" href="https://github.com/sponsors/zvictor?utm_source=brainyflow&utm_medium=sponsorship&utm_campaign=brainyflow&utm_id=brainyflow">
    <img width="150" src="https://cdn.jsdelivr.net/gh/zvictor/brainyflow@main/.github/media/brain.png" alt="Brainyflow的Logo" />
  </a><br /><br />
  BrainyFlow运行在200行代码和您的慷慨之上！💰<br />
    <a style="color: inherit" href="https://github.com/sponsors/zvictor?utm_source=brainyflow&utm_medium=sponsorship&utm_campaign=brainyflow&utm_id=brainyflow">
      帮助我们用更少的代码(也许需要更多咖啡)交付更多AI
    </a> ☕<br /><br />
    <a style="color: inherit" href="https://github.com/sponsors/zvictor?utm_source=brainyflow&utm_medium=sponsorship&utm_campaign=brainyflow&utm_id=brainyflow">您的支持</a>让框架保持极简、强大且无依赖！🚀
  </a>
</p>

![](https://raw.githubusercontent.com/zvictor/brainyflow/master/.github/media/divider.png)