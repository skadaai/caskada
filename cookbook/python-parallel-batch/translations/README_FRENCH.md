<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://cdn.jsdelivr.net/gh/skadaai/caskada@main/.github/media/logo-dark.png">
    <source media="(prefers-color-scheme: light)" srcset="https://cdn.jsdelivr.net/gh/skadaai/caskada@main/.github/media/logo-light.png">
    <img width="280" alt="Logo de Caskada" src="https://cdn.jsdelivr.net/gh/skadaai/caskada@main/.github/media/logo-light.png">
  </picture>
<p>

<p align="center">
  Un framework AI radicalement minimaliste (seulement <a href="https://github.com/skadaai/caskada/blob/main/python/caskada.py">200 lignes en Python</a> ! 🤯)

  <br />
  Construisez des agents IA puissants avec un code minimal et une liberté maximale.
  <br />
  <sub>Laissez les agents construire des agents sans bloat, dépendances ou enfermement fournisseur 😮</sub>
</p>

<p align="center">

  <a href="https://pypi.org/project/caskada">
   <img src="https://img.shields.io/pypi/dw/caskada?logo=python&label=Python&style=flat-square" alt="version python">
  </a>
  <a href="https://npmjs.com/packages/caskada">
   <img src="https://img.shields.io/npm/d18m/caskada?logo=typescript&label=Typescript&style=flat-square" alt="version typescript">
  </a>
  <a href="https://discord.gg/N9mVvxRXyH">
    <img src="https://img.shields.io/discord/1346833819172601907?logo=discord&style=flat-square" alt="Discord">
  </a>
  <a href="https://github.com/skadaai/caskada">
    <img src="https://img.shields.io/github/stars/skadaai/caskada?logo=github&style=flat-square" alt="Dépôt GitHub">
  </a>
  <a href="https://github.com/sponsors/zvictor">
    <img src="https://img.shields.io/github/sponsors/zvictor?logo=github&style=flat-square" alt="Sponsors GitHub">
  </a>
</p>

Caskada est un framework permettant le _Codage Agentique_ grâce à des abstractions puissantes.

Il fournit une interface simple pour construire des applications IA complexes basées sur des _graphes orientés imbriqués_ avec un état partagé.
Il permet aux humains et aux assistants IA de collaborer efficacement sur la conception et l'implémentation de systèmes IA.

## Fonctionnalités

- **Facilité d'utilisation 🧠** : Intuitif pour les humains et les assistants IA
- **Design minimaliste ✨** : Abstractions principales en seulement (_vous avez bien entendu !_) 200 lignes de code
- **Liberté 🔓** : Zéro bloat, dépendances ou enfermement fournisseur
- **Composable 🧩** : Construisez des systèmes complexes à partir de composants simples et réutilisables
- **Puissant 🦾** : Prend en charge tout ce que vous aimez—([Multi-](https://skadaai.gitbook.io/caskada/design_pattern/multi_agent))[Agents](https://skadaai.gitbook.io/caskada/design_pattern/agent), [Workflow](https://skadaai.gitbook.io/caskada/design_pattern/workflow), [RAG](https://skadaai.gitbook.io/caskada/design_pattern/rag), et plus encore
- **Codage Agentique 🤖** : Conçu pour le développement assisté par IA
- **Universel 🌈** : Fonctionne avec n'importe quel fournisseur ou API LLM
- **Polyglotte 🌍** : <!-- gitbook-ignore-start --><a href="https://pypi.org/project/caskada"><img src="https://github.com/skadaai/caskada/raw/main/.github/media/python.svg" width="16" height="16" alt="Logo Python" style="vertical-align: middle; margin: 0 2px;"></a><!-- gitbook-ignore-end --> Python et <!-- gitbook-ignore-start --><a href="https://npmjs.com/packages/caskada"><img src="https://github.com/skadaai/caskada/raw/main/.github/media/typescript.svg" width="16" height="16" alt="Logo Typescript" style="vertical-align: middle; margin: 0 2px;"></a><!-- gitbook-ignore-end --> Typescript sont tous deux supportés

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

<!-- gitbook-ignore-start -->

## Documentation

Notre documentation est inclusive, adaptée aux esprits biologiques et synthétiques.<br />
Commencez par sélectionner votre condition - ou peut-être _celle que vous avez été conditionné à croire_ :

\>> [Je suis à base de carbone 🐥](https://skadaai.gitbook.io/caskada/introduction/getting_started) <<

\>> [Je suis à base de silicium 🤖](https://flow.b brainy.sh/docs.txt) <<

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

<!-- gitbook-ignore-end -->

## Pourquoi Caskada ?

Les frameworks LLM actuels sont gonflés... Vous n'avez en fait besoin que de 200 lignes pour un framework LLM robuste !

<div align="center">
  <img src="https://raw.githubusercontent.com/skadaai/caskada/main/.github/media/meme.jpg" width="500"/>

|                                                                                                                                                                                                                | **Abstraction** |                     **Wrappers Spécifiques à l'Application**                      |                       **Wrappers Spécifiques au Fournisseur**                       |                **Lignes**                 |                  **Taille**                   |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------: | :----------------------------------------------------------------: | :----------------------------------------------------------------------: | :--------------------------------------: | :-----------------------------------------: |
| LangChain                                                                                                                                                                                                      |  Agent, Chaîne   |      Beaucoup <br><sup><sub>(e.g., QA, Résumé)</sub></sup>      |      Beaucoup <br><sup><sub>(e.g., OpenAI, Pinecone, etc.)</sub></sup>       |                   405K                   |                   +166MB                    |
| CrewAI                                                                                                                                                                                                         |  Agent, Chaîne   | Beaucoup <br><sup><sub>(e.g., FileReadTool, SerperDevTool)</sub></sup> | Beaucoup <br><sup><sub>(e.g., OpenAI, Anthropic, Pinecone, etc.)</sub></sup> |                   18K                    |                   +173MB                    |
| SmolAgent                                                                                                                                                                                                      |      Agent      |   Quelques <br><sup><sub>(e.g., CodeAgent, VisitWebTool)</sub></sup>   |  Quelques <br><sub>(e.g., DuckDuckGo, Hugging Face, etc.)</sub></sup>   |                    8K                    |                   +198MB                    |
| LangGraph                                                                                                                                                                                                      |  Agent, Graphe   |       Quelques <br><sup><sub>(e.g., Recherche Sémantique)</sub></sup>       | Quelques <br><sup><sub>(e.g., PostgresStore, SqliteSaver, etc.) </sub></sup> |                   37K                    |                    +51MB                    |
| AutoGen                                                                                                                                                                                                        |      Agent      |   Quelques <br><sup><sub>(e.g., Outil Agent, Chat Agent)</sub></sup>    | Beaucoup <sup><sub>[Optionnel]<br> (e.g., OpenAI, Pinecone, etc.)</sub></sup> | 7K <br><sup><sub>(noyau uniquement)</sub></sup> | +26MB <br><sup><sub>(noyau uniquement)</sub></sup> |
| **Caskada** <!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/typescript.svg" width="16" height="16" alt="Logo Typescript"><!-- gitbook-ignore-end -->.ts |    **Graphe**    |                              **Aucun**                              |                                 **Aucun**                                 |                 **300**                  |                 **quelques Ko**                  |
| **Caskada** <!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/python.svg" width="16" height="16" alt="Logo Python"><!-- gitbook-ignore-end -->.py         |    **Graphe**    |                              **Aucun**                              |                                 **Aucun**                                 |                 **200**                  |                 **quelques Ko**                  |

</div>

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

## Comment fonctionne Caskada ?

Le fichier unique en <a href="https://github.com/skadaai/caskada/blob/main/python/caskada.py"><!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/python.svg" width="16" height="16" alt="Logo Python" style="vertical-align: middle; margin: 0 2px;"> <!-- gitbook-ignore-end -->Python</a> ou <a href="https://github.com/skadaai/caskada/blob/main/typescript/caskada.ts"><!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/typescript.svg" width="16" height="16" alt="Logo Typescript" style="vertical-align: middle; margin: 0 2px;"> <!-- gitbook-ignore-end -->Typescript</a> capture l'abstraction centrale des frameworks LLM : le Graphe !
<br>

<div align="center">
  <img src="https://raw.githubusercontent.com/skadaai/caskada/main/.github/media/abstraction.jpg" width="1300"/>
</div>
<br>

- [Node](https://skadaai.gitbook.io/caskada/core_abstraction/node) gère des tâches simples (LLM) avec un cycle de vie clair (`prep` → `exec` → `post`).
- [Flow](https://skadaai.gitbook.io/caskada/core_abstraction/flow) connecte les nœuds via des **Actions** (arêtes étiquetées), orchestrant l'exécution.
- [Memory](https://skadaai.gitbook.io/caskada/core_abstraction/memory) gère les états partagés (`global`) et isolés (`local`), permettant la communication entre les nœuds.

À partir de là, il est facile d'implémenter tous les modèles de conception populaires :
<br>

<div align="center">
  <img src="https://raw.githubusercontent.com/skadaai/caskada/main/.github/media/design.jpg" width="1300"/>
</div>
<br>

- [Agent](https://skadaai.gitbook.io/caskada/design_pattern/agent) prend des décisions autonomes basées sur le contexte.
- [Workflow](https://skadaai.gitbook.io/caskada/design_pattern/workflow) enchaîne plusieurs tâches en pipelines séquentiels.
- [RAG](https://skadaai.gitbook.io/caskada/design_pattern/rag) intègre la récupération de données avec la génération.
- [Map Reduce](https://skadaai.gitbook.io/caskada/design_pattern/mapreduce) divise les tâches de données en étapes Map et Reduce.
- [Structured Output](https://skadaai.gitbook.io/caskada/design_pattern/structure) formate les sorties de manière cohérente.
- [Multi-Agents](https://skadaai.gitbook.io/caskada/design_pattern/multi_agent) coordonne plusieurs agents.

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

## Tutoriels

<div align="center">
  
|  Nom  | Difficulté    |  Description  |  
| :-------------:  | :-------------: | :--------------------- |  
| [Chat](https://github.com/skadaai/caskada/tree/main/cookbook/python-chat) | ☆☆☆ <br> *Basique*   | Un chatbot basique avec historique de conversation |
| [RAG](https://github.com/skadaai/caskada/tree/main/cookbook/python-rag) | ☆☆☆ <br> *Basique*   | Un processus simple de Génération augmentée par récupération |
| [Workflow](https://github.com/skadaai/caskada/tree/main/cookbook/python-workflow) | ☆☆☆ <br> *Basique*   | Un workflow d'écriture qui crée un plan, rédige du contenu et applique un style |
| [Map-Reduce](https://github.com/skadaai/caskada/tree/main/cookbook/python-map-reduce) | ☆☆☆ <br> *Basique* | Un processeur de qualification de CV utilisant le modèle map-reduce pour une évaluation en lot |
| [Agent](https://github.com/skadaai/caskada/tree/main/cookbook/python-agent) | ☆☆☆ <br> *Basique*   | Un agent de recherche capable de chercher sur le web et répondre aux questions |
| [Streaming](https://github.com/skadaai/caskada/tree/main/cookbook/python-llm-streaming) | ☆☆☆ <br> *Basique*   | Une démo de streaming LLM en temps réel avec capacité d'interruption utilisateur |
| [Multi-Agent](https://github.com/skadaai/caskada/tree/main/cookbook/python-multi-agent) | ★☆☆ <br> *Débutant* | Un jeu de mots Tabou pour la communication asynchrone entre deux agents |
| [Supervisor](https://github.com/skadaai/caskada/tree/main/cookbook/python-supervisor) | ★☆☆ <br> *Débutant* | L'agent de recherche devient peu fiable... Créons un processus de supervision|
| [Parallel](https://github.com/skadaai/caskada/tree/main/cookbook/python-parallel-batch) | ★☆☆ <br> *Débutant*   | Une démo d'exécution parallèle montrant une accélération de 3x |
| [Thinking](https://github.com/skadaai/caskada/tree/main/cookbook/python-thinking) | ★☆☆ <br> *Débutant*   | Résoudre des problèmes de raisonnement complexes via Chain-of-Thought |
| [Memory](https://github.com/skadaai/caskada/tree/main/cookbook/python-chat-memory) | ★☆☆ <br> *Débutant* | Un chatbot avec mémoire à court et long terme |

</div>

Et bien d'autres disponibles pour tous les niveaux ! [Découvrez-les tous !](https://github.com/skadaai/caskada/tree/main/cookbook)

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

<!-- ## Comment utiliser Caskada ?

🚀 Grâce au **Codage Agentique**—le paradigme de développement d'applications LLM le plus rapide où _les humains conçoivent_ et _les agents codent_ !

<br />

- Vous voulez apprendre le **Codage Agentique** ?
  - Pour configurer, lisez cet [article](https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to) !
  - Consultez [ma chaîne YouTube](https://www.youtube.com/@ZacharyLLM?sub_confirmation=1) ! Lisez ce [Guide](https://skadaai.gitbook.io/caskada/guides/agentic_coding) !

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png) -->

## Démarrage rapide

Nouveau sur Caskada ? Consultez notre guide [Démarrage rapide](https://skadaai.gitbook.io/caskada/introduction/getting_started) pour construire votre premier flux en un rien de temps.

## Prêt à construire des applications auto-codantes ?

Consultez le [Guide de Codage Agentique](https://skadaai.gitbook.io/caskada/guides/agentic_coding), la manière la plus rapide de développer des projets LLM auto-codants avec Caskada !

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

## Remerciements

Nous tenons à exprimer notre profonde gratitude aux créateurs et contributeurs du framework PocketFlow, à partir duquel Caskada a été forké.

## Clause de non-responsabilité

Caskada est fourni "tel quel" sans aucune garantie.  
Nous ne sommes pas responsables de l'utilisation faite des résultats générés, y compris mais sans s'y limiter, leur exactitude, leur légalité ou toute conséquence découlant de leur utilisation.

## Sponsors

<p align="center">
  <a style="color: inherit" href="https://github.com/sponsors/zvictor?utm_source=caskada&utm_medium=sponsorship&utm_campaign=caskada&utm_id=caskada">
    <img width="150" src="https://cdn.jsdelivr.net/gh/skadaai/caskada@main/.github/media/brain.png" alt="Logo de Caskada" />
  </a><br /><br />
  Caskada fonctionne sur 200 lignes de code et votre générosité ! 💰<br />
    <a style="color: inherit" href="https://github.com/sponsors/zvictor?utm_source=caskada&utm_medium=sponsorship&utm_campaign=caskada&utm_id=caskada">
      Aidez-nous à fournir plus d'IA avec moins de code (mais peut-être plus de caféine)
    </a> ☕<br /><br />
    <a style="color: inherit" href="https://github.com/sponsors/zvictor?utm_source=caskada&utm_medium=sponsorship&utm_campaign=caskada&utm_id=caskada">Votre soutien</a> permet de le garder minimal, puissant et sans dépendances ! 🚀
  </a>
</p>

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)