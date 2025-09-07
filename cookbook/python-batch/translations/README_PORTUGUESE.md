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
  <sub>Deixe os agentes construírem agentes sem bloat, dependências ou lock-in de fornecedor 😮</sub>
</p>

<p align="center">

  <a href="https://pypi.org/project/caskada">
   <img src="https://img.shields.io/pypi/dw/caskada?logo=python&label=Python&style=flat-square" alt="python version">
  </a>
  <a href="https://npmjs.com/package/caskada">
   <img src="https://img.shields.io/npm/d18m/caskada?logo=typescript&label=Typescript&style=flat-square" alt="typescript version">
  </a>
  <a href="https://discord.gg/N9mVvxRXyH">
    <img src="https://img.shields.io/discord/1346833819172601907?logo=discord&style=flat-square" alt="Discord">
  </a>
  <a href="https://github.com/skadaai/caskada">
    <img src="https://img.shields.io/github/stars/skadaai/caskada?logo=github&style=flat-square" alt="GitHub Repository">
  </a>
  <a href="https://github.com/sponsors/zvictor">
    <img src="https://img.shields.io/github/sponsors/zvictor?logo=github&style=flat-square" alt="GitHub Sponsors">
  </a>
</p>

Brainy Flow é um framework que permite a programação de agentes através de poderosas abstrações.

Ele fornece uma interface simples para construir aplicações complexas de IA baseadas em grafos direcionados aninhados com estado compartilhado. Ele permite que humanos e assistentes de IA colaborem efetivamente no design e implementação de sistemas de IA.

## Características

- **Fácil para o cérebro 🧠**: Intuitivo tanto para humanos quanto para assistentes de IA
- **Design minimalista ✨**: Abstrações principais em apenas 200 linhas de código
- **Liberdade 🔓**: Sem bloat, dependências ou lock-in de fornecedor
- **Componível 🧩**: Construa sistemas complexos a partir de componentes simples e reutilizáveis
- **Poderoso 🦾**: Suporta tudo que você ama - ([Multi-](https://brainy.gitbook.io/flow/design_pattern/multi_agent))[Agentes](https://brainy.gitbook.io/flow/design_pattern/agent), [Fluxos de trabalho](https://brainy.gitbook.io/flow/design_pattern/workflow), [RAG](https://brainy.gitbook.io/flow/design_pattern/rag) e mais
- **Programação de agentes 🤖**: Projetado para desenvolvimento assistido por IA
- **Universal 🌈**: Funciona com qualquer provedor de LLM ou API
- **Poliglota 🌍**: <!-- gitbook-ignore-start --><a href="https://pypi.org/project/caskada"><img src="https://github.com/skadaai/caskada/raw/main/.github/media/python.svg" width="16" height="16" alt="Python Logo" style="vertical-align: middle; margin: 0 2px;"></a><!-- gitbook-ignore-end --> Python e <!-- gitbook-ignore-start --><a href="https://npmjs.com/package/caskada"><img src="https://github.com/skadaai/caskada/raw/main/.github/media/typescript.svg" width="16" height="16" alt="Typescript Logo" style="vertical-align: middle; margin: 0 2px;"></a><!-- gitbook-ignore-end --> TypeScript são suportados

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

<!-- gitbook-ignore-start -->

## Documentação

Nossa documentação é inclusiva, adequada tanto para mentes biológicas quanto sintéticas.<br />
Comece selecionando sua condição - ou talvez aquela que você foi condicionado a acreditar:

\>> [Eu sou baseado em carbono 🐥](https://brainy.gitbook.io/flow/introduction/getting_started) <<

\>> [Eu sou baseado em silício 🤖](https://flow.brainy.sh/docs.txt) <<

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

<!-- gitbook-ignore-end -->

## Por que Brainy Flow?

Os frameworks atuais de LLM são inchados... Você só precisa de 200 linhas para um framework robusto de LLM!

<div align="center">
  <img src="https://raw.githubusercontent.com/skadaai/caskada/main/.github/media/meme.jpg" width="500"/>

|                                                                                                                                                                                                                | **Abstração** |                     **Wrappers específicos de aplicação**                      |                       **Wrappers específicos de fornecedor**                       |                **Linhas**                 |                  **Tamanho**                  |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------: | :----------------------------------------------------------------: | :----------------------------------------------------------------------: | :--------------------------------------: | :-----------------------------------------: |
| LangChain                                                                                                                                                                                                      |  Agente, Cadeia  |      Muitos <br><sup><sub>(ex: QA, sumarização)</sub></sup>      |      Muitos <br><sup><sub>(ex: OpenAI, Pinecone, etc.)</sub></sup>      |                   405K                   |                   +166MB                    |
| CrewAI                                                                                                                                                                                                         |  Agente, Cadeia  | Muitos <br><sup><sub>(ex: FileReadTool, SerperDevTool)</sub></sup> | Muitos <br><sup><sub>(ex: OpenAI, Anthropic, Pinecone, etc.)</sub></sup> |                   18K                    |                   +173MB                    |
| SmolAgent                                                                                                                                                                                                      |      Agente      |   Alguns <br><sup><sub>(ex: CodeAgent, VisitWebTool)</sub></sup>   |  Alguns <br><sup><sub>(ex: DuckDuckGo, Hugging Face, etc.)</sub></sup>   |                    8K                    |                   +198MB                    |
| LangGraph                                                                                                                                                                                                      |  Agente, Grafo  |       Alguns <br><sup><sub>(ex: busca semântica)</sub></sup>       | Alguns <br><sup><sub>(ex: PostgresStore, SqliteSaver, etc.)</sub></sup> |                   37K                    |                    +51MB                    |
| AutoGen                                                                                                                                                                                                        |      Agente      |   Alguns <br><sup><sub>(ex: Tool Agent, Chat Agent)</sub></sup>    | Muitos <sup><sub>[Opcional]<br> (ex: OpenAI, Pinecone, etc.)</sub></sup> | 7K <br><sup><sub>(núcleo)</sub></sup> | +26MB <br><sup><sub>(núcleo)</sub></sup> |
| **Brainy Flow** <!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/typescript.svg" width="16" height="16" alt="Typescript Logo"><!-- gitbook-ignore-end -->.ts |    **Grafo**    |                              **Nenhum**                              |                                 **Nenhum**                                 |                 **300**                  |                 **poucos KB**                 |
| **Brainy Flow** <!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/python.svg" width="16" height="16" alt="Python Logo"><!-- gitbook-ignore-end -->.py         |    **Grafo**    |                              **Nenhum**                              |                                 **Nenhum**                                 |                 **200**                  |                 **poucos KB**                 |

</div>

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

## Como o Brainy Flow funciona?

O arquivo único em <a href="https://github.com/skadaai/caskada/blob/main/python/caskada.py"><!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/python.svg" width="16" height="16" alt="Python Logo" style="vertical-align: middle; margin: 0 2px;"> <!-- gitbook-ignore-end -->Python</a> ou <a href="https://github.com/skadaai/caskada/blob/main/typescript/caskada.ts"><!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/typescript.svg" width="16" height="16" alt="Typescript Logo" style="vertical-align: middle; margin: 0 2px;"> <!-- gitbook-ignore-end -->TypeScript</a> captura a abstração central dos frameworks LLM: o grafo!
<br>

<div align="center">
  <img src="https://raw.githubusercontent.com/skadaai/caskada/main/.github/media/abstração.jpg" width="1300"/>
</div>
<br>

- [Nó](https://brainy.gitbook.io/flow/core_abstraction/node) lida com tarefas simples (LLM) com um ciclo de vida claro (`prep` → `exec` → `post`).
- [Fluxo](https://brainy.gitbook.io/flow/core_abstraction/flow) conecta nós através de **Ações** (bordas rotuladas), orquestrando a execução.
- [Memória](https://brainy.gitbook.io/flow/core_abstraction/memory) gerencia estado compartilhado (`global`) e isolado (`local`), permitindo comunicação entre nós.

A partir daí, é fácil implementar todos os padrões de design populares:
<br>

<div align="center">
  <img src="https://raw.githubusercontent.com/skadaai/caskada/main/.github/media/design.jpg" width="1300"/>
</div>
<br>

- [Agente](https://brainy.gitbook.io/flow/design_pattern/agent) toma decisões autonomamente baseado no contexto.
- [Fluxo de trabalho](https://brainy.gitbook.io/flow/design_pattern/workflow) encadeia múltiplas tarefas em um pipeline sequencial.
- [RAG](https://brainy.gitbook.io/flow/design_pattern/rag) integra recuperação de dados com geração.
- [Map Reduce](https://brainy.gitbook.io/flow/design_pattern/mapreduce) divide tarefas de dados em etapas de mapeamento e redução.
- [Saída estruturada](https://brainy.gitbook.io/flow/design_pattern/structure) formata saídas consistentemente.
- [Multi-Agentes](https://brainy.gitbook.io/flow/design_pattern/multi_agent) coordena múltiplos agentes.

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

## Tutoriais

<div align="center">
  
|  Nome  | Dificuldade    |  Descrição 