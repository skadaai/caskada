<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://cdn.jsdelivr.net/gh/skadaai/caskada@main/.github/media/logo-dark.png">
    <source media="(prefers-color-scheme: light)" srcset="https://cdn.jsdelivr.net/gh/skadaai/caskada@main/.github/media/logo-light.png">
    <img width="280" alt="Logo do Caskada" src="https://cdn.jsdelivr.net/gh/skadaai/caskada@main/.github/media/logo-light.png">
  </picture>
<p>

<p align="center">
  Um framework de IA radicalmente minimalista (apenas <a href="https://github.com/skadaai/caskada/blob/main/python/caskada.py">200 linhas em Python</a>! 🤯)

  <br />
  Construa agentes de IA poderosos com código mínimo e liberdade máxima.
  <br />
  <sub>Deixe os agentes construírem agentes sem bloat, dependências ou bloqueio de fornecedor 😮</sub>
</p>

<p align="center">

  <a href="https://pypi.org/project/caskada">
   <img src="https://img.shields.io/pypi/dw/caskada?logo=python&label=Python&style=flat-square" alt="versão do python">
  </a>
  <a href="https://npmjs.com/packages/caskada">
   <img src="https://img.shields.io/npm/d18m/caskada?logo=typescript&label=Typescript&style=flat-square" alt="versão do typescript">
  </a>
  <a href="https://discord.gg/N9mVvxRXyH">
    <img src="https://img.shields.io/discord/1346833819172601907?logo=discord&style=flat-square" alt="Discord">
  </a>
  <a href="https://github.com/skadaai/caskada">
    <img src="https://img.shields.io/github/stars/skadaai/caskada?logo=github&style=flat-square" alt="Repositório GitHub">
  </a>
  <a href="https://github.com/sponsors/z1190">
    <img src="https://img.shields.io/github/sponsors/z1190?logo=github&style=flat-square" alt="Patrocinadores GitHub">
  </a>
</p>

Caskada é um framework que permite a *programação de agentes* por meio de abstrações poderosas.

Ele fornece uma interface simples para construir aplicativos complexos de IA baseados em *grafos direcionados aninhados* com estado compartilhado. Ele permite que humanos e assistentes de IA colaborem efetivamente no design e implementação de sistemas de IA.

## Recursos

- **Fácil para o cérebro 🧠**: Intuitivo tanto para humanos quanto para assistentes de IA
- **Design minimalista ✨**: Abstrações principais em apenas (você ouviu direito!) 200 linhas de código
- **Liberdade 🔓**: Sem bloat, dependências ou bloqueio de fornecedor
- **Componível 🧩**: Construa sistemas complexos a partir de componentes simples e reutilizáveis
- **Poderoso 🦾**: Suporta tudo o que você ama - ([Multi-](https://skadaai.gitbook.io/caskada/design_pattern/multi_agent))[Agentes](https://skadaai.gitbook.io/caskada/design_pattern/agent), [Fluxo de trabalho](https://skadaai.gitbook.io/caskada/design_pattern/workflow), [RAG](https://skadaai.gitbook.io/caskada/design_pattern/rag) e muito mais
- **Programação de agentes 🤖**: Projetado para desenvolvimento assistido por IA
- **Universal 🌈**: Funciona com qualquer provedor ou API de LLM
- **Poliglota 🌍**: <!-- gitbook-ignore-start --><a href="https://pypi.org/project/caskada"><img src="https://github.com/skadaai/caskada/raw/main/.github/media/python.svg" width="16" height="16" alt="Logo Python" style="vertical-align: middle; margin: 0 2px;"></a><!-- gitbook-ignore-end --> Python e <!-- gitbook-ignore-start --><a href="https://npmjs.com/packages/caskada"><img src="https://github.com/skadaai/caskada/raw/main/.github/media/typescript.svg" width="16" height="16" alt="Logo Typescript" style="vertical-align: middle; margin: 0 2px;"></a><!-- gitbook-ignore-end --> Typescript são suportados

![](https://raw.githubusercontent.com/skadaai/caskada/main/.github/media/divider.png)

<!-- gitbook-ignore-start -->

## Documentação

Nossa documentação é inclusiva, adequada tanto para mentes biológicas quanto sintéticas.<br />
Comece selecionando sua condição - ou talvez *aquela em que você foi condicionado a acreditar*:

\>> [Eu sou baseado em carbono 🐥](https://skadaai.gitbook.io/caskada/introduction/getting_started) <<

\>> [Eu sou baseado em silício 🤖](https://flow.brainy.sh/docs.txt) <<

![](https://raw.githubusercontent.com/skadaai/caskada/main/.github/media/divider.png)

<!-- gitbook-ignore-end -->

## Por que Brainy Flow?

Os frameworks atuais de LLM são inchados... Você só precisa de 200 linhas para um framework robusto de LLM!

<div align="center">
  <img src="https://raw.githubusercontent.com/skadaai/caskada/main/.github/media/meme.jpg" width="500"/>

|                                                                                                                                                                                                                | **Abstração** |                     **Wrappers específicos de aplicativo**                      |                       **Wrappers específicos de fornecedor**                       |                **Linhas**                 |                  **Tamanho**                  |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-----------: | :-----------------------------------------------------------------------------: | :-------------------------------------------------------------------------------: | :---------------------------------------: | :------------------------------------------: |
| LangChain                                                                                                                                                                                                      |  Agente, Cadeia  |      Muitos <br><sup><sub>(por exemplo, QA, resumo)</sub></sup>      |      Muitos <br><sup><sub>(por exemplo, OpenAI, Pinecone, etc.)</sub></sup>      |                   405K                   |                   +166MB                    |
| CrewAI                                                                                                                                                                                                         |  Agente, Cadeia  | Muitos <br><sup><sub>(por exemplo, FileReadTool, SerperDevTool)</sub></sup> | Muitos <br><sup><sub>(por exemplo, OpenAI, Anthropic, Pinecone, etc.)</sub></sup> |                   18K                    |                   +173MB                    |
| SmolAgent                                                                                                                                                                                                      |      Agente      |   Alguns <br><sup><sub>(por exemplo, CodeAgent, VisitWebTool)</sub></sup>   |  Alguns <br><sup><sub>(por exemplo, DuckDuckGo, Hugging Face, etc.)</sub></sup>  |                    8K                    |                   +198MB                    |
| LangGraph                                                                                                                                                                                                      |  Agente, Grafo  |       Alguns <br><sup><sub>(por exemplo, busca semântica)</sub></sup>       | Alguns <br><sup><sub>(por exemplo, PostgresStore, SqliteSaver, etc.)</sub></sup> |                   37K                    |                    +51MB                    |
| AutoGen                                                                                                                                                                                                        |      Agente      |   Alguns <br><sup><sub>(por exemplo, Tool Agent, Chat Agent)</sub></sup>   | Muitos <br><sup><sub>[Opcional]<br> (por exemplo, OpenAI, Pinecone, etc.)</sub></sup> | 7K <br><sup><sub>(somente núcleo)</sub></sup> | +26MB <br><sup><sub>(somente núcleo)</sub></sup> |
| **Caskada** <!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/typescript.svg" width="16" height="16" alt="Logo Typescript"><!-- gitbook-ignore-end -->.ts |    **Grafo**    |                              **Nenhum**                              |                                 **Nenhum**                                 |                 **300**                  |                 **Poucos KB**                 |
| **Caskada** <!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/python.svg" width="16" height="16" alt="Logo Python"><!-- gitbook-ignore-end -->.py         |    **Grafo**    |                              **Nenhum**                              |                                 **Nenhum**                                 |                 **200**                  |                 **Poucos KB**                 |

</div>

![](https://raw.githubusercontent.com/skadaai/caskada/main/.github/media/divider.png)

## Como o Caskada funciona?

O arquivo único em <a href="https://github.com/skadaai/caskada/blob/main/python/caskada.py"><!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/python.svg" width="16" height="16" alt="Logo Python" style="vertical-align: middle; margin: 0 2px;"> <!-- gitbook-ignore-end -->Python</a> ou <a href="https://github.com/skadaai/caskada/blob/main/typescript/caskada.ts"><!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/typescript.svg" width="16" height="16" alt="Logo Typescript" style="vertical-align: middle; margin: 0 2px;"> <!-- gitbook-ignore-end -->Typescript</a> captura a abstração central dos frameworks LLM: Grafo!
<br>

<div align="center">
  <img src="https://raw.githubusercontent.com/skadaai/caskada/main/.github/media/abstraction.jpg" width="1300"/>
</div>
<br>

- [Nó](https://skadaai.gitbook.io/caskada/core_abstraction/node) lida com tarefas simples (LLM) com um ciclo de vida claro (`prep` → `exec` → `post`).
- [Fluxo](https://skadaai.gitbook.io/caskada/core_abstraction/flow) conecta nós por meio de **Ações** (borda rotulada), orquestrando a execução.
- [Memória](https://skadaai.gitbook.io/caskada/core_abstraction/memory) gerencia estado compartilhado (`global`) e isolado (`local`), permitindo comunicação entre nós.

A partir daí, é fácil implementar todos os padrões de design populares:
<br>

<div align="center">
  <img src="https://raw.githubusercontent.com/skadaai/caskada/main/.github/media/design.jpg" width="1300"/>
</div>
<br>

- [Agente](https://skadaai.gitbook.io/caskada/design_pattern/agent) toma decisões autonomamente com base no contexto.
- [Fluxo de trabalho](https://skadaai.gitbook.io/caskada/design_pattern/workflow) encadeia várias tarefas em um pipeline sequencial.
- [RAG](https://skadaai.gitbook.io/caskada/design_pattern/rag) integra recuperação de dados com geração.
- [Map Reduce](https://skadaai.gitbook.io/caskada/design_pattern/mapreduce) divide tarefas de dados em etapas de mapeamento e redução.
- [Saída estruturada](https://skadaai.gitbook.io/caskada/design_pattern/structure) formata saídas de forma consistente.
- [Multi-Agentes](https://skadaai.gitbook.io/caskada/design_pattern/multi_agent) coordena vários agentes.

![](https://raw.githubusercontent.com/skadaai/caskada/main/.github/media/divider.png)

## Tutoriais

<div align="center">
  
|  Nome  | Dificuldade    |  Descrição  |  
| :-------------:  | :-------------: | :--------------------- |  
| [Chat](https://github.com/skadaai/caskada/tree/main/cookbook/python-chat) | ☆☆☆ <br> *Básico*   | Um chatbot básico com histórico de conversa |
| [RAG](https://github.com/skadaai/caskada/tree/main/cookbook/python-rag) | ☆☆☆ <br> *Básico*   | Um processo simples de Geração Aumentada por Recuperação |
| [Fluxo de trabalho](https://github.com/z1190