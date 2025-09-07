<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://cdn.jsdelivr.net/gh/skadaai/caskada@main/.github/media/logo-dark.png">
    <source media="(prefers-color-scheme: light)" srcset="https://cdn.jsdelivr.net/gh/skadaai/caskada@main/.github/media/logo-light.png">
    <img width="280" alt="Caskada 标志" src="https://cdn.jsdelivr.net/gh/skadaai/caskada@main/.github/media/logo-light.png">
  </picture>
<p>

<p align="center">
  一个极简主义AI框架（仅<a href="https://github.com/skadaai/caskada/blob/main/python/caskada.py">200行Python代码</a>！🤯）

  <br />
  用最少的代码构建强大的AI代理，享受最大自由。
  <br />
  <sub>让代理构建代理，零膨胀、零依赖、零供应商锁定 😮</sub>
</p>

<p align="center">

  <a href="https://pypi.org/project/caskada">
   <img src="https://img.shields.io/pypi/dw/caskada?logo=python&label=Python&style=flat-square" alt="python 版本">
  </a>
  <a href="https://npmjs.com/packages/caskada">
   <img src="https://img.shields.io/npm/d18m/caskada?logo=typescript&label=Typescript&style=flat-square" alt="typescript 版本">
  </a>
  <a href="https://discord.gg/N9mVvxRXyH">
    <img src="https://img.shields.io/discord/1346833819172601907?logo=discord&style=flat-square" alt="Discord">
  </a>
  <a href="https://github.com/skadaai/caskada">
    <img src="https://img.shields.io/github/stars/skadaai/caskada?logo=github&style=flat-square" alt="GitHub 仓库">
  </a>
  <a href="https://github.com/sponsors/zvictor">
    <img src="https://img.shields.io/github/sponsors/zvictor?logo=github&style=flat-square" alt="GitHub 赞助">
  </a>
</p>

Caskada 是通过强大抽象实现 _代理编程_ 的框架。

它为构建基于 _嵌套有向图与共享状态_ 的复杂AI应用提供了简单接口，使人类和AI助手能高效协作设计和实现AI系统。

## 特性

- **智商友好 🧠**：对人和AI助手都直观
- **极简设计 ✨**：核心抽象仅_200行代码_
- **自由 🔓**：零膨胀、零依赖、零供应商锁定
- **可组合 🧩**：用简单可复用组件构建复杂系统
- **强大 🦾**：支持你喜爱的一切——([多](https://brainy.gitbook.io/flow/design_pattern/multi_agent))[代理](https://brainy.gitbook.io/flow/design_pattern/agent)、[工作流](https://brainy.gitbook.io/flow/design_pattern/workflow)、[RAG](https://brainy.gitbook.io/flow/design_pattern/rag)等
- **代理编程 🤖**：专为AI辅助开发设计
- **通用 🌈**：兼容任何LLM供应商或API
- **多语言 🌍**： <!-- gitbook-ignore-start --><a href="https://pypi.org/project/caskada"><img src="https://github.com/skadaai/caskada/raw/main/.github/media/python.svg" width="16" height="16" alt="Python 标志" style="vertical-align: middle; margin: 0 2px;"></a><!-- gitbook-ignore-end --> Python 和 <!-- gitbook-ignore-start --><a href="https://npmjs.com/packages/caskada"><img src="https://github.com/skadaai/caskada/raw/main/.github/media/typescript.svg" width="16" height="16" alt="Typescript 标志" style="vertical-align: middle; margin: 0 2px;"></a><!-- gitbook-ignore-end --> Typescript 皆支持

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

<!-- gitbook-ignore-start -->

## 文档

我们的文档适合碳基和硅基生命。<br />
请根据你的_存在形态_或_被灌输的认知_选择：

\>> [我是碳基生命 🐥](https://brainy.gitbook.io/flow/introduction/getting_started) <<

\>> [我是硅基生命 🤖](https://flow.brainy.sh/docs.txt) <<

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

<!-- gitbook-ignore-end -->

## 为什么选择 Brainy Flow?

现有LLM框架太臃肿... 其实200行就能实现强大的LLM框架!

<div align="center">
  <img src="https://raw.githubusercontent.com/skadaai/caskada/main/.github/media/meme.jpg" width="500"/>

|                                                                                                                                                                                                                | **抽象层** |                     **应用特定封装**                      |                       **供应商特定封装**                       |                **代码行数**                 |                  **体积**                   |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------: | :----------------------------------------------------------------: | :----------------------------------------------------------------------: | :--------------------------------------: | :-----------------------------------------: |
| LangChain                                                                                                                                                                                                      |  代理、链式  |      多 <br><sup><sub>(如QA、摘要)</sub></sup>      |      多 <br><sup><sub>(如OpenAI、Pinecone等)</sub></sup>       |                   405K                   |                   +166MB                    |
| CrewAI                                                                                                                                                                                                         |  代理、链式  | 多 <br><sup><sub>(如FileReadTool、SerperDevTool)</sub></sup> | 多 <br><sup><sub>(如OpenAI、Anthropic、Pinecone等)</sub></sup> |                   18K                    |                   +173MB                    |
| SmolAgent                                                                                                                                                                                                      |      代理      |   部分 <br><sup><sub>(如CodeAgent、VisitWebTool)</sub></sup>   |  部分 <br><sup><sub>(如DuckDuckGo、Hugging Face等)</sub></sup>   |                    8K                    |                   +198MB                    |
| LangGraph                                                                                                                                                                                                      |  代理、图  |       部分 <br><sup><sub>(如语义搜索)</sub></sup>       | 部分 <br><sup><sub>(如PostgresStore、SqliteSaver等)</sub></sup> |                   37K                    |                    +51MB                    |
| AutoGen                                                                                                                                                                                                        |      代理      |   部分 <br><sup><sub>(如工具代理、聊天代理)</sub></sup>    | 多 <sup><sub>[可选]<br> (如OpenAI、Pinecone等)</sub></sup> | 7K <br><sup><sub>(仅核心)</sub></sup> | +26MB <br><sup><sub>(仅核心)</sub></sup> |
| **Caskada** <!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/typescript.svg" width="16" height="16" alt="Typescript 标志"><!-- gitbook-ignore-end -->.ts |    **图**    |                              **无**                              |                                 **无**                                 |                 **300**                  |                 **几KB**                  |
| **Caskada** <!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/python.svg" width="16" height="16" alt="Python 标志"><!-- gitbook-ignore-end -->.py         |    **图**    |                              **无**                              |                                 **无**                                 |                 **200**                  |                 **几KB**                  |

</div>

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

## Caskada如何工作?

<a href="https://github.com/skadaai/caskada/blob/main/python/caskada.py"><!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/python.svg" width="16" height="16" alt="Python 标志" style="vertical-align: middle; margin: 0 2px;"> <!-- gitbook-ignore-end -->Python</a> 或 <a href="https://github.com/skadaai/caskada/blob/main/typescript/caskada.ts"><!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/typescript.svg" width="16" height="16" alt="Typescript 标志" style="vertical-align: middle; margin: 0 2px;"> <!-- gitbook-ignore-end -->Typescript</a> 单文件实现LLM框架核心抽象：图!
<br>

<div align="center">
  <img src="https://raw.githubusercontent.com/skadaai/caskada/main/.github/media/abstraction.jpg" width="1300"/>
</div>
<br>

- [节点](https://brainy.gitbook.io/flow/core_abstraction/node)通过生命周期(`准备`→`执行`→`后处理`)处理简单(LLM)任务
- [流程](https://brainy.gitbook.io/flow/core_abstraction/flow)通过**动作**(带标签边)连接节点，协调执行
- [内存](https://brainy.gitbook.io/flow/core_abstraction/memory)管理共享(`全局`)和隔离(`本地`)状态，实现节点间通信

由此可轻松实现所有流行设计模式：
<br>

<div align="center">
  <img src="https://raw.githubusercontent.com/skadaai/caskada/main/.github/media/design.jpg" width="1300"/>
</div>
<br>

- [代理](https://brainy.gitbook.io/flow/design_pattern/agent)基于上下文自主决策
- [工作流](https://brainy.gitbook.io/flow/design_pattern/workflow)将多个任务串联成顺序管道
- [RAG](https://brainy.gitbook.io/flow/design_pattern/rag)整合数据检索与生成
- [Map Reduce](https://brainy.gitbook.io/flow/design_pattern/mapreduce)将数据任务拆分为映射和归约步骤
- [结构化输出](https://brainy.gitbook.io/flow/design_pattern/structure)保持输出格式一致
- [多代理](https://brainy.gitbook.io/flow/design_pattern/multi_agent)协调多个代理协作

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

## 教程

<div align="center">
  
|  名称  | 难度    |  描述  |  
| :-------------:  | :-------------: | :--------------------- |  
| [聊天](https://github.com/skadaai/caskada/tree/main/cookbook/python-chat) | ☆☆☆ <br> *基础*   | 带对话历史的简单聊天机器人 |
| [RAG](https://github.com/skadaai/caskada/tree/main/cookbook/python-rag) | ☆☆☆ <br> *基础*   | 简单的检索增强生成流程 |
| [工作流](https://github.com/skadaai/caskada/tree/main/cookbook/python-workflow) | ☆☆☆ <br> *基础*   | 写作工作流：提纲→内容→样式 |
| [Map-Reduce](https://github.com/skadaai/caskada/tree/main/cookbook/python-map-reduce) | ☆☆☆ <br> *基础* | 使用map-reduce模式批量评估简历 |
| [代理](https://github.com/skadaai/caskada/tree/main/cookbook/python-agent) | ☆☆☆ <br> *基础*   | 能搜索网络回答问题的研究代理 |
| [流式处理](https://github.com/skadaai/caskada/tree/main/cookbook/python-llm-streaming) | ☆☆☆ <br> *基础*   | 支持用户中断的实时LLM流式演示 |
| [多代理](https://github.com/skadaai/caskada/tree/main/cookbook/python-multi-agent) | ★☆☆ <br> *入门* | 两个代理异步沟通的禁忌词游戏 |
| [监督者](https://github.com/skadaai/caskada/tree/main/cookbook/python-supervisor) | ★☆☆ <br> *入门* | 研究代理不可靠时构建监督流程|
| [并行](https://github.com/skadaai/caskada/tree/main/cookbook/python-parallel-batch) | ★☆☆ <br> *入门*   | 展示3倍加速的并行执行示例 |
| [思考链](https://github.com/skadaai/caskada/tree/main/cookbook/python-thinking) | ★☆☆ <br> *入门*   | 通过思维链解决复杂推理问题 |
| [记忆](https://github.com/skadaai/caskada/tree/main/cookbook/python-chat-memory) | ★☆☆ <br> *入门* | 具备短期和长期记忆的聊天机器人 |

</div>

更多教程适合所有水平！[查看全部](https://github.com/skadaai/caskada/tree/main/cookbook)

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

## 快速开始

初次接触Caskada？查看我们的[入门指南](https://brainy.gitbook.io/flow/introduction/getting_started)，快速构建第一个流程。

## 准备开发自编程应用？

了解[代理编程指南](https://brainy.gitbook.io/flow/guides/agentic_coding)，用Caskada开发自编程LLM项目的最快方式！

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

## 致谢

我们衷心感谢PocketFlow框架的创建者和贡献者，Caskada正是从其分叉而来。

## 免责声明

Caskada按"原样"提供，不作任何保证。  
对生成内容的使用(包括准确性、合法性及可能后果)概不负责。

## 赞助者

<p align="center">
  <a style="color: inherit" href="https://github.com/sponsors/zvictor?utm_source=caskada&utm_medium=sponsorship&utm_campaign=caskada&utm_id=caskada">
    <img width="150" src="https://cdn.jsdelivr.net/gh/skadaai/caskada@main/.github/media/brain.png" alt="Caskada 标志" />
  </a><br /><br />
  Caskada运行在200行代码和您的慷慨之上！💰<br />
    <a style="color: inherit" href="https://github.com/sponsors/zvictor?utm_source=caskada&utm_medium=sponsorship&utm_campaign=caskada&utm_id=caskada">
      帮助我们用更少代码(可能更多咖啡因)提供更多AI
    </a> ☕<br /><br />
    <a style="color: inherit" href="https://github.com/sponsors/zvictor?utm_source=caskada&utm_medium=sponsorship&utm_campaign=caskada&utm_id=caskada">您的支持</a>让项目保持精简、强大且无依赖！🚀
  </a>
</p>

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)