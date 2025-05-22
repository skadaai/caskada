<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://cdn.jsdelivr.net/gh/zvictor/brainyflow@main/.github/media/logo-dark.png">
    <source media="(prefers-color-scheme: light)" srcset="https://cdn.jsdelivr.net/gh/zvictor/brainyflow@main/.github/media/logo-light.png">
    <img width="280" alt="Logo de Brainyflow" src="https://cdn.jsdelivr.net/gh/zvictor/brainyflow@main/.github/media/logo-light.png">
  </picture>
<p>

<p align="center">
  Un framework AI radicalement minimaliste (seulement <a href="https://github.com/zvictor/BrainyFlow/blob/main/python/brainyflow.py">200 lignes en Python</a> ! 🤯)

  <br />
  Construisez des agents IA puissants avec un code minimal et une liberté maximale.
  <br />
  <sub>Laissez les agents construire d'autres agents sans encombrement, dépendances ou enfermement propriétaire 😮</sub>
</p>

<p align="center">

  <a href="https://pypi.org/project/brainyflow">
   <img src="https://img.shields.io/pypi/dw/brainyflow?logo=python&label=Python&style=flat-square" alt="version python">
  </a>
  <a href="https://npmjs.com/packages/brainyflow">
   <img src="https://img.shields.io/npm/d18m/brainyflow?logo=typescript&label=Typescript&style=flat-square" alt="version typescript">
  </a>
  <a href="https://discord.gg/N9mVvxRXyH">
    <img src="https://img.shields.io/discord/1346833819172601907?logo=discord&style=flat-square" alt="Discord">
  </a>
  <a href="https://github.com/zvictor/brainyflow">
    <img src="https://img.shields.io/github/stars/zvictor/BrainyFlow?logo=github&style=flat-square" alt="Dépôt GitHub">
  </a>
  <a href="https://github.com/sponsors/zvictor">
    <img src="https://img.shields.io/github/sponsors/zvictor?logo=github&style=flat-square" alt="Sponsors GitHub">
  </a>
</p>

BrainyFlow est un framework permettant le _Codage Agentique_ grâce à des abstractions puissantes.

Il fournit une interface simple pour construire des applications IA complexes basées sur des _graphes orientés imbriqués_ avec un état partagé.
Il permet aux humains et aux assistants IA de collaborer efficacement sur la conception et la mise en œuvre de systèmes IA.

## Fonctionnalités

- **Simplicité 🧠** : Intuitif pour les humains et les assistants IA
- **Design Minimaliste ✨** : Abstractions principales en seulement (_vous avez bien entendu !_) 200 lignes de code
- **Liberté 🔓** : Aucun encombrement, dépendances ou enfermement propriétaire
- **Composable 🧩** : Construisez des systèmes complexes à partir de composants simples et réutilisables
- **Puissant 🦾** : Prend en charge tout ce que vous aimez—([Multi-](https://brainy.gitbook.io/flow/design_pattern/multi_agent))[Agents](https://brainy.gitbook.io/flow/design_pattern/agent), [Workflow](https://brainy.gitbook.io/flow/design_pattern/workflow), [RAG](https://brainy.gitbook.io/flow/design_pattern/rag), et plus encore
- **Codage Agentique 🤖** : Conçu pour le développement assisté par IA
- **Universel 🌈** : Fonctionne avec n'importe quel fournisseur ou API LLM
- **Polyglotte 🌍** : <!-- gitbook-ignore-start --><a href="https://pypi.org/project/brainyflow"><img src="https://github.com/zvictor/brainyflow/raw/main/.github/media/python.svg" width="16" height="16" alt="Logo Python" style="vertical-align: middle; margin: 0 2px;"></a><!-- gitbook-ignore-end --> Python et <!-- gitbook-ignore-start --><a href="https://npmjs.com/packages/brainyflow"><img src="https://github.com/zvictor/brainyflow/raw/main/.github/media/typescript.svg" width="16" height="16" alt="Logo Typescript" style="vertical-align: middle; margin: 0 2px;"></a><!-- gitbook-ignore-end --> Typescript sont tous deux supportés

![](https://raw.githubusercontent.com/zvictor/brainyflow/master/.github/media/divider.png)

<!-- gitbook-ignore-start -->

## Documentation

Notre documentation est inclusive, adaptée aux esprits biologiques et synthétiques.<br />
Commencez par sélectionner votre condition - ou peut-être _celle que vous avez été conditionné à croire_ :

\>> [Je suis à base de carbone 🐥](https://brainy.gitbook.io/flow/introduction/getting_started) <<

\>> [Je suis à base de silicium 🤖](https://flow.brainy.sh/docs.txt) <<

![](https://raw.githubusercontent.com/zvictor/brainyflow/master/.github/media/divider.png)

<!-- gitbook-ignore-end -->

## Pourquoi Brainy Flow ?

Les frameworks LLM actuels sont encombrés... Vous n'avez en réalité besoin que de 200 lignes pour un framework LLM robuste !

<div align="center">
  <img src="https://raw.githubusercontent.com/zvictor/brainyflow/main/.github/media/meme.jpg" width="500"/>

|                                                                                                                                                                                                                | **Abstraction** |                     **Wrappers Spécifiques à l'Application**                      |                       **Wrappers Spécifiques au Fournisseur**                       |                **Lignes**                 |                  **Taille**                   |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------: | :----------------------------------------------------------------: | :----------------------------------------------------------------------: | :--------------------------------------: | :-----------------------------------------: |
| LangChain                                                                                                                                                                                                      |  Agent, Chaîne  |      Beaucoup <br><sup><sub>(ex : QA, Résumé)</sub></sup>      |      Beaucoup <br><sup><sub>(ex : OpenAI, Pinecone, etc.)</sub></sup>       |                   405K                   |                   +166MB                    |
| CrewAI                                                                                                                                                                                                         |  Agent, Chaîne  | Beaucoup <br><sup><sub>(ex : FileReadTool, SerperDevTool)</sub></sup> | Beaucoup <br><sup><sub>(ex : OpenAI, Anthropic, Pinecone, etc.)</sub></sup> |                   18K                    |                   +173MB                    |
| SmolAgent                                                                                                                                                                                                      |      Agent      |   Quelques <br><sup><sub>(ex : CodeAgent, VisitWebTool)</sub></sup>   |  Quelques <br><sup><sub>(ex : DuckDuckGo, Hugging Face, etc.)</sub></sup>   |                    8K                    |                   +198MB                    |
| LangGraph                                                                                                                                                                                                      |  Agent, Graphe  |       Quelques <br><sup><sub>(ex : Recherche Sémantique)</sub></sup>       | Quelques <br><sup><sub>(ex : PostgresStore, SqliteSaver, etc.) </sub></sup> |                   37K                    |                    +51MB                    |
| AutoGen                                                                                                                                                                                                        |      Agent      |   Quelques <br><sup><sub>(ex : Tool Agent, Chat Agent)</sub></sup>    | Beaucoup <sup><sub>[Optionnel]<br> (ex : OpenAI, Pinecone, etc.)</sub></sup> | 7K <br><sup><sub>(core uniquement)</sub></sup> | +26MB <br><sup><sub>(core uniquement)</sub></sup> |
| **BrainyFlow** <!-- gitbook-ignore-start --><img src="https://github.com/zvictor/brainyflow/raw/main/.github/media/typescript.svg" width="16" height="16" alt="Logo Typescript"><!-- gitbook-ignore-end -->.ts |    **Graphe**    |                              **Aucun**                              |                                 **Aucun**                                 |                 **300**                  |                 **quelques KB**                  |
| **BrainyFlow** <!-- gitbook-ignore-start --><img src="https://github.com/zvictor/brainyflow/raw/main/.github/media/python.svg" width="16" height="16" alt="Logo Python"><!-- gitbook-ignore-end -->.py         |    **Graphe**    |                              **Aucun**                              |                                 **Aucun**                                 |                 **200**                  |                 **quelques KB**                  |

</div>

![](https://raw.githubusercontent.com/zvictor/brainyflow/master/.github/media/divider.png)

## Comment fonctionne BrainyFlow ?

Le fichier unique en <a href="https://github.com/zvictor/BrainyFlow/blob/main/python/brainyflow.py"><!-- gitbook-ignore-start --><img src="https://github.com/zvictor/brainyflow/raw/main/.github/media/python.svg" width="16" height="16" alt="Logo Python" style="vertical-align: middle; margin: 0 2px;"> <!-- gitbook-ignore-end -->Python</a> ou <a href="https://github.com/zvictor/BrainyFlow/blob/main/typescript/brainyflow.ts"><!-- gitbook-ignore-start --><img src="https://github.com/zvictor/brainyflow/raw/main/.github/media/typescript.svg" width="16" height="16" alt="Logo Typescript" style="vertical-align: middle; margin: 0 2px;"> <!-- gitbook-ignore-end -->Typescript</a> capture l'abstraction centrale des frameworks LLM : le Graphe !
<br>

<div align="center">
  <img src="https://raw.githubusercontent.com/zvictor/brainyflow/main/.github/media/abstraction.jpg" width="1300"/>
</div>
<br>

- [Node](https://brainy.gitbook.io/flow/core_abstraction/node) gère des tâches simples (LLM) avec un cycle de vie clair (`prep` → `exec` → `post`).
- [Flow](https://brainy.gitbook.io/flow/core_abstraction/flow) connecte les nœuds via des **Actions** (arêtes étiquetées), orchestrant l'exécution.
- [Memory](https://brainy.gitbook.io/flow/core_abstraction/memory) gère l'état partagé (`global`) et isolé (`local`), permettant la communication entre les nœuds.

À partir de là, il est facile d'implémenter tous les modèles de conception populaires :
<br>

<div align="center">
  <img src="https://raw.githubusercontent.com/zvictor/brainyflow/main/.github/media/design.jpg" width="1300"/>
</div>
<br>

- [Agent](https://brainy.gitbook.io/flow/design_pattern/agent) prend des décisions autonomes basées sur le contexte.
- [Workflow](https://brainy.gitbook.io/flow/design_pattern/workflow) enchaîne plusieurs tâches en pipelines séquentiels.
- [RAG](https://brainy.gitbook.io/flow/design_pattern/rag) intègre la récupération de données avec la génération.
- [Map Reduce](https://brainy.gitbook.io/flow/design_pattern/mapreduce) divise les tâches de données en étapes Map et Reduce.
- [Structured Output](https://brainy.gitbook.io/flow/design_pattern/structure) formate les sorties de manière cohérente.
- [Multi-Agents](https://brainy.gitbook.io/flow/design_pattern/multi_agent) coordonne plusieurs agents.

![](https://raw.githubusercontent.com/zvictor/brainyflow/master/.github/media/divider.png)

## Tutoriels

<div align="center">
  
|  Nom  | Difficulté    |  Description  |  
| :-------------:  | :-------------: | :--------------------- |  
| [Chat](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-chat) | ☆☆☆ <br> *Débutant*   | Un chatbot basique avec historique de conversation |
| [RAG](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-rag) | ☆☆☆ <br> *Débutant*   | Un processus simple de Génération Augmentée par Récupération |
| [Workflow](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-workflow) | ☆☆☆ <br> *Débutant*   | Un workflow d'écriture qui planifie, rédige du contenu et applique des styles |
| [Map-Reduce](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-map-reduce) | ☆☆☆ <br> *Débutant* | Un processeur de qualification de CV utilisant le modèle map-reduce pour une évaluation par lots |
| [Agent](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-agent) | ☆☆☆ <br> *Débutant*   | Un agent de recherche capable de chercher sur le web et répondre aux questions |
| [Streaming](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-llm-streaming) | ☆☆☆ <br> *Débutant*   | Une démo de streaming LLM en temps réel avec capacité d'interruption par l'utilisateur |
| [Multi-Agent](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-multi-agent) | ★☆☆ <br> *Intermédiaire* | Un jeu de mots Taboo pour la communication asynchrone entre deux agents |
| [Supervisor](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-supervisor) | ★☆☆ <br> *Intermédiaire* | L'agent de recherche devient peu fiable... Construisons un processus de supervision|
| [Parallel](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-parallel-batch) | ★☆☆ <br> *Intermédiaire*   | Une démo d'exécution parallèle montrant une accélération de 3x |
| [Thinking](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-thinking) | ★☆☆ <br> *Intermédiaire*   | Résoudre des problèmes de raisonnement complexes via Chain-of-Thought |
| [Memory](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-chat-memory) | ★☆☆ <br> *Intermédiaire* | Un chatbot avec mémoire à court et long terme |

</div>

Et bien d'autres disponibles pour tous les niveaux ! [Découvrez-les tous !](https://github.com/zvictor/BrainyFlow/tree/main/cookbook)

![](https://raw.githubusercontent.com/zvictor/brainyflow/master/.github/media/divider.png)

<!-- ## Comment utiliser Brainy Flow ?

🚀 Grâce au **Codage Agentique**—le paradigme de développement d'applications LLM le plus rapide, où _les humains conçoivent_ et _les agents codent_ !

<br />

- Vous voulez apprendre le **Codage Agentique** ?
  - Pour configurer, lisez ce [post](https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to) !
  - Consultez [ma chaîne YouTube](https://www.youtube.com/@ZacharyLLM?sub_confirmation=1) ! Lisez ce [Guide](https://brainy.gitbook.io/flow/guides/agentic_coding) !
- Vous voulez construire votre propre application LLM ? Commencez avec notre [modèle Python](https://github.com/zvictor/Brainyflow-Template-Python) ou [modèle Typescript](https://github.com/zvictor/Brainyflow-Template-Typescript) !

![](https://raw.githubusercontent.com/zvictor/brainyflow/master/.github/media/divider.png) -->

## Démarrage Rapide

Nouveau sur BrainyFlow ? Consultez notre guide [Démarrage Rapide](https://brainy.gitbook.io/flow/introduction/getting_started) pour construire votre premier flow en un rien de temps.

## Prêt à Construire des Applications Auto-Codantes ?

Consultez le [Guide de Codage Agentique](https://brainy.gitbook.io/flow/guides/agentic_coding), la manière la plus rapide de développer des projets LLM auto-codants avec BrainyFlow !

![](https://raw.githubusercontent.com/zvictor/brainyflow/master/.github/media/divider.png)

## Remerciements

Nous tenons à exprimer notre profonde gratitude aux créateurs et contributeurs du framework PocketFlow, dont brainyFlow est issu en tant que fork.

## Clause de Non-Responsabilité

BrainyFlow est fourni "tel quel" sans aucune garantie.  
Nous ne sommes pas responsables de l'utilisation qui est faite des sorties générées, y compris mais sans s'y limiter, leur exactitude, leur légalité ou toute conséquence potentielle découlant de leur utilisation.

## Sponsors

<p align="center">
  <a style="color: inherit" href="https://github.com/sponsors/zvictor?utm_source=brainyflow&utm_medium=sponsorship&utm_campaign=brainyflow&utm_id=brainyflow">
    <img width="150" src="https://cdn.jsdelivr.net/gh/zvictor/brainyflow@main/.github/media/brain.png" alt="Logo de Brainyflow" />
  </a><br /><br />
  BrainyFlow fonctionne avec 200 lignes de code et votre générosité ! 💰<br />
    <a style="color: inherit" href="https://github.com/sponsors/zvictor?utm_source=brainyflow&utm_medium=sponsorship&utm_campaign=brainyflow&utm_id=brainyflow">
      Aidez-nous à fournir plus d'IA avec moins de code (mais peut-être plus de caféine)
    </a> ☕<br /><br />
    <a style="color: inherit" href="https://github.com/sponsors/zvictor?utm_source=brainyflow&utm_medium=sponsorship&utm_campaign=brainyflow&utm_id=brainyflow">Votre soutien</a> nous aide à rester minimalistes, puissants et sans dépendances ! 🚀
  </a>
</p>

![](https://raw.githubusercontent.com/zvictor/brainyflow/master/.github/media/divider.png)