<div align="center">
  <img src="https://github.com/zvictor/BrainyFlow/raw/main/.github/media/banner-light.jpg" width="600"/>
</div>

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
[![Docs](https://img.shields.io/badge/docs-latest-blue)](https://brainy.gitbook.io/flow/)
<a href="https://discord.gg/MdJJ29Xd">
<img src="https://img.shields.io/discord/1346833819172601907?logo=discord&style=flat">
</a>

BrainyFlow est un framework LLM minimaliste de [100 lignes](https://github.com/zvictor/BrainyFlow/blob/main/python/__init__.py)

- **Léger**: Seulement 100 lignes. Zéro surcharge, zéro dépendances, zéro verrouillage de fournisseur.
- **Expressif**: Tout ce que vous aimez—([Multi-](https://brainy.gitbook.io/flow/design_pattern/multi_agent))[Agents](https://brainy.gitbook.io/flow/design_pattern/agent), [Workflow](https://brainy.gitbook.io/flow/design_pattern/workflow), [RAG](https://brainy.gitbook.io/flow/design_pattern/rag), et plus encore.

- **[Programmation Agentique](https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to)**: Laissez les Agents IA (par exemple, Cursor AI) construire des Agents—productivité multipliée par 10 !

- Pour installer, `pip install brainyflow` ou copiez simplement le [code source](https://github.com/zvictor/BrainyFlow/blob/main/python/__init__.py) (seulement 100 lignes).
- Pour en savoir plus, consultez la [documentation](https://brainy.gitbook.io/flow/). Pour comprendre la motivation, lisez l'[histoire](https://zacharyhuang.substack.com/p/i-built-an-llm-framework-in-just).
- 🎉 Rejoignez notre [discord](https://discord.gg/MdJJ29Xd) !

- 🎉 Merci à [@zvictor](https://www.github.com/zvictor), [@jackylee941130](https://www.github.com/jackylee941130) et [@ZebraRoy](https://www.github.com/ZebraRoy), nous avons maintenant une [version TypeScript](https://github.com/The-Pocket/PocketFlow-Typescript) !

## Pourquoi BrainyFlow ?

Les frameworks LLM actuels sont surchargés... Vous n'avez besoin que de 100 lignes pour un framework LLM !

<div align="center">
  <img src="https://github.com/zvictor/brainyflow/raw/main/.github/media/meme.jpg" width="400"/>

|                | **Abstraction** |               **Wrappers spécifiques aux applications**               |                  **Wrappers spécifiques aux fournisseurs**                   |                **Lignes**                |                 **Taille**                  |
| -------------- | :-------------: | :-------------------------------------------------------------------: | :--------------------------------------------------------------------------: | :--------------------------------------: | :-----------------------------------------: |
| LangChain      |  Agent, Chain   |         Nombreux <br><sup><sub>(ex., QA, Résumé)</sub></sup>          |       Nombreux <br><sup><sub>(ex., OpenAI, Pinecone, etc.)</sub></sup>       |                   405K                   |                   +166MB                    |
| CrewAI         |  Agent, Chain   | Nombreux <br><sup><sub>(ex., FileReadTool, SerperDevTool)</sub></sup> | Nombreux <br><sup><sub>(ex., OpenAI, Anthropic, Pinecone, etc.)</sub></sup>  |                   18K                    |                   +173MB                    |
| SmolAgent      |      Agent      |   Quelques <br><sup><sub>(ex., CodeAgent, VisitWebTool)</sub></sup>   |   Quelques <br><sup><sub>(ex., DuckDuckGo, Hugging Face, etc.)</sub></sup>   |                    8K                    |                   +198MB                    |
| LangGraph      |  Agent, Graph   |    Quelques <br><sup><sub>(ex., Recherche Sémantique)</sub></sup>     | Quelques <br><sup><sub>(ex., PostgresStore, SqliteSaver, etc.) </sub></sup>  |                   37K                    |                    +51MB                    |
| AutoGen        |      Agent      |   Quelques <br><sup><sub>(ex., Tool Agent, Chat Agent)</sub></sup>    | Nombreux <sup><sub>[Optionnel]<br> (ex., OpenAI, Pinecone, etc.)</sub></sup> | 7K <br><sup><sub>(core-only)</sub></sup> | +26MB <br><sup><sub>(core-only)</sub></sup> |
| **BrainyFlow** |    **Graph**    |                               **Aucun**                               |                                  **Aucun**                                   |                 **100**                  |                  **+56KB**                  |

</div>

## Comment fonctionne BrainyFlow ?

Les [100 lignes](https://github.com/zvictor/BrainyFlow/blob/main/python/__init__.py) capturent l'abstraction principale des frameworks LLM : le Graphe !
<br>

<div align="center">
  <img src="https://github.com/zvictor/brainyflow/raw/main/.github/media/abstraction.jpg" width="900"/>
</div>
<br>

À partir de là, il est facile d'implémenter des modèles de conception populaires comme ([Multi-](https://brainy.gitbook.io/flow/design_pattern/multi_agent))[Agents](https://brainy.gitbook.io/flow/design_pattern/agent), [Workflow](https://brainy.gitbook.io/flow/design_pattern/workflow), [RAG](https://brainy.gitbook.io/flow/design_pattern/rag), etc.
<br>

<div align="center">
  <img src="https://github.com/zvictor/brainyflow/raw/main/.github/media/design.jpg" width="900"/>
</div>
<br>
✨ Voici les tutoriels de base :

<div align="center">
  
|  Nom  | Difficulté    |  Description  |  
| :-------------:  | :-------------: | :--------------------- |  
| [Chat](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-chat) | ☆☆☆ <br> *Débutant*   | Un chatbot de base avec historique de conversation |
| [Sortie Structurée](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-structured-output) | ☆☆☆ <br> *Débutant* | Extraction de données structurées à partir de CV par prompt |
| [Workflow](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-workflow) | ☆☆☆ <br> *Débutant*   | Un workflow d'écriture qui structure, écrit du contenu et applique un style |
| [Agent](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-agent) | ☆☆☆ <br> *Débutant*   | Un agent de recherche qui peut effectuer des recherches sur le web et répondre aux questions |
| [RAG](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-rag) | ☆☆☆ <br> *Débutant*   | Un processus simple de génération augmentée par récupération |
| [Map-Reduce](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-map-reduce) | ☆☆☆ <br> *Débutant* | Un processeur de qualification de CV utilisant le modèle map-reduce pour l'évaluation par lots |
| [Streaming](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-llm-streaming) | ☆☆☆ <br> *Débutant*   | Une démo de streaming LLM en temps réel avec capacité d'interruption utilisateur |
| [Garde-fou de Chat](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-chat-guardrail) | ☆☆☆ <br> *Débutant*  | Un chatbot conseiller de voyage qui ne traite que les requêtes liées au voyage |
| [Multi-Agent](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-multi-agent) | ★☆☆ <br> *Intermédiaire* | Un jeu de Taboo pour la communication asynchrone entre deux agents |
| [Superviseur](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-supervisor) | ★☆☆ <br> *Intermédiaire* | L'agent de recherche devient peu fiable... Construisons un processus de supervision |
| [Parallèle](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-parallel-batch) | ★☆☆ <br> *Intermédiaire*   | Une démo d'exécution parallèle qui montre une accélération 3x |
| [Flux Parallèle](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-parallel-batch-flow) | ★☆☆ <br> *Intermédiaire*   | Une démo de traitement d'image parallèle montrant une accélération 8x avec plusieurs filtres |
| [Vote à la majorité](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-majority-vote) | ★☆☆ <br> *Intermédiaire* | Améliore la précision du raisonnement en agrégeant plusieurs tentatives de solution |
| [Réflexion](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-thinking) | ★☆☆ <br> *Intermédiaire*   | Résout des problèmes de raisonnement complexes grâce à la Chaîne de Pensée |
| [Mémoire](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-chat-memory) | ★☆☆ <br> *Intermédiaire* | Un chatbot avec mémoire à court et long terme |
| [MCP](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-mcp) | ★☆☆ <br> *Intermédiaire* | Agent utilisant le Protocole de Contexte de Modèle pour des opérations numériques |

</div>

👀 Vous voulez voir d'autres tutoriels pour débutants ? [Créez une issue!](https://github.com/zvictor/BrainyFlow/issues/new)

## Comment utiliser BrainyFlow ?

🚀 Grâce à la **Programmation Agentique**—le paradigme de développement d'applications LLM le plus rapide—où _les humains conçoivent_ et _les agents codent_ !

<br>
<div align="center">
  <a href="https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to" target="_blank">
    <img src="https://substackcdn.com/image/fetch/f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F423a39af-49e8-483b-bc5a-88cc764350c6_1050x588.png" width="700" alt="IMAGE ALT TEXT" style="cursor: pointer;">
  </a>
</div>
<br>

✨ Voici des exemples d'applications LLM plus complexes :

<div align="center">
  
|  Nom de l'application     |  Difficulté    | Sujets  | Conception Humaine | Code Agent |
| :-------------:  | :-------------: | :---------------------: |  :---: |  :---: |
| [Construire Cursor avec Cursor](https://github.com/The-Pocket/Tutorial-Cursor) <br> <sup><sub>Nous atteindrons bientôt la singularité ...</sup></sub> | ★★★ <br> *Avancé*   | [Agent](https://brainy.gitbook.io/flow/design_pattern/agent) | [Document de conception](https://github.com/The-Pocket/Tutorial-Cursor/blob/main/docs/design.md) | [Code Flow](https://github.com/The-Pocket/Tutorial-Cursor/blob/main/flow.py)
| [Demandez à l'IA Paul Graham](https://github.com/The-Pocket/Tutorial-YC-Partner) <br> <sup><sub>Demandez à l'IA Paul Graham, au cas où vous n'êtes pas accepté</sup></sub> | ★★☆ <br> *Moyen*   | [RAG](https://brainy.gitbook.io/flow/design_pattern/rag) <br> [Map Reduce](https://brainy.gitbook.io/flow/design_pattern/mapreduce) <br> [TTS](https://brainy.gitbook.io/flow/utility_function/text_to_speech) | [Document de conception](https://github.com/The-Pocket/Tutorial-AI-Paul-Graham/blob/main/docs/design.md) | [Code Flow](https://github.com/The-Pocket/Tutorial-AI-Paul-Graham/blob/main/flow.py)
| [Résumeur Youtube](https://github.com/The-Pocket/Tutorial-Youtube-Made-Simple)  <br> <sup><sub> Explique les vidéos YouTube comme si vous aviez 5 ans </sup></sub> | ★☆☆ <br> *Intermédiaire*   | [Map Reduce](https://brainy.gitbook.io/flow/design_pattern/mapreduce) |  [Document de conception](https://github.com/The-Pocket/Tutorial-Youtube-Made-Simple/blob/main/docs/design.md) | [Code Flow](https://github.com/The-Pocket/Tutorial-Youtube-Made-Simple/blob/main/flow.py)
| [Générateur d'Introduction](https://github.com/The-Pocket/Tutorial-Cold-Email-Personalization)  <br> <sup><sub> Des brise-glaces instantanés qui transforment les prospects froids en prospects chauds </sup></sub> | ★☆☆ <br> *Intermédiaire*   | [Map Reduce](https://brainy.gitbook.io/flow/design_pattern/mapreduce) <br> [Recherche Web](https://brainy.gitbook.io/flow/utility_function/websearch) |  [Document de conception](https://github.com/The-Pocket/Tutorial-Cold-Email-Personalization/blob/master/docs/design.md) | [Code Flow](https://github.com/The-Pocket/Tutorial-Cold-Email-Personalization/blob/master/flow.py)

</div>

- Vous voulez apprendre la **Programmation Agentique** ?

  - Consultez [ma chaîne YouTube](https://www.youtube.com/@ZacharyLLM?sub_confirmation=1) pour des tutoriels vidéo sur la façon dont certaines applications ci-dessus sont créées !

  - Vous souhaitez créer votre propre application LLM ? Lisez cet [article](https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to) ! Commencez avec [ce modèle](https://github.com/The-Pocket/PocketFlow-Template-Python) !

  - Vous voulez apprendre les étapes détaillées ? Lisez ce [Guide](https://brainy.gitbook.io/flow/guide) !
