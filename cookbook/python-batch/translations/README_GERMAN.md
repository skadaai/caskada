<div align="center">
  <img src="https://github.com/zvictor/BrainyFlow/raw/main/.github/media/banner-light.jpg" width="600"/>
</div>

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
[![Docs](https://img.shields.io/badge/docs-latest-blue)](https://brainy.gitbook.io/flow/)
<a href="https://discord.gg/N9mVvxRXyH">
<img src="https://img.shields.io/discord/1346833819172601907?logo=discord&style=flat">
</a>

BrainyFlow ist ein [100-Zeilen](https://github.com/zvictor/BrainyFlow/blob/main/python/__init__.py) minimalistisches LLM-Framework

- **Leichtgewichtig**: Nur 100 Zeilen. Keine Aufblähung, keine Abhängigkeiten, keine Anbieter-Bindung.
- **Ausdrucksstark**: Alles, was du liebst—([Multi-](https://brainy.gitbook.io/flow/design_pattern/multi_agent))[Agenten](https://brainy.gitbook.io/flow/design_pattern/agent), [Workflow](https://brainy.gitbook.io/flow/design_pattern/workflow), [RAG](https://brainy.gitbook.io/flow/design_pattern/rag) und mehr.

- **[Agentisches Programmieren](https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to)**: Lass KI-Agenten (z.B. Cursor AI) Agenten bauen—10-fache Produktivitätssteigerung!

- Zur Installation, `pip install brainyflow` oder kopiere einfach den [Quellcode](https://github.com/zvictor/BrainyFlow/blob/main/python/__init__.py) (nur 100 Zeilen).
- Um mehr zu erfahren, schau dir die [Dokumentation](https://brainy.gitbook.io/flow/) an. Um die Motivation zu verstehen, lies die [Geschichte](https://zacharyhuang.substack.com/p/i-built-an-llm-framework-in-just).
- 🎉 Tritt unserem [Discord](https://discord.gg/N9mVvxRXyH) bei!

- 🎉 Dank [@zvictor](https://www.github.com/zvictor), [@jackylee941130](https://www.github.com/jackylee941130) und [@ZebraRoy](https://www.github.com/ZebraRoy) haben wir jetzt eine [TypeScript-Version](https://github.com/The-Pocket/PocketFlow-Typescript)!

## Warum BrainyFlow?

Aktuelle LLM-Frameworks sind aufgebläht... Du brauchst nur 100 Zeilen für ein LLM-Framework!

<div align="center">
  <img src="https://github.com/zvictor/brainyflow/raw/main/.github/media/meme.jpg" width="400"/>

|                | **Abstraktion** |                    **App-spezifische Wrapper**                     |                     **Anbieter-spezifische Wrapper**                      |               **Zeilen**                |                 **Größe**                  |
| -------------- | :-------------: | :----------------------------------------------------------------: | :-----------------------------------------------------------------------: | :-------------------------------------: | :----------------------------------------: |
| LangChain      |  Agent, Chain   |     Viele <br><sup><sub>(z.B. QA, Zusammenfassung)</sub></sup>     |       Viele <br><sup><sub>(z.B. OpenAI, Pinecone, usw.)</sub></sup>       |                  405K                   |                   +166MB                   |
| CrewAI         |  Agent, Chain   | Viele <br><sup><sub>(z.B. FileReadTool, SerperDevTool)</sub></sup> | Viele <br><sup><sub>(z.B. OpenAI, Anthropic, Pinecone, usw.)</sub></sup>  |                   18K                   |                   +173MB                   |
| SmolAgent      |      Agent      |  Einige <br><sup><sub>(z.B. CodeAgent, VisitWebTool)</sub></sup>   |  Einige <br><sup><sub>(z.B. DuckDuckGo, Hugging Face, usw.)</sub></sup>   |                   8K                    |                   +198MB                   |
| LangGraph      |  Agent, Graph   |     Einige <br><sup><sub>(z.B. Semantische Suche)</sub></sup>      | Einige <br><sup><sub>(z.B. PostgresStore, SqliteSaver, usw.) </sub></sup> |                   37K                   |                   +51MB                    |
| AutoGen        |      Agent      |   Einige <br><sup><sub>(z.B. Tool Agent, Chat Agent)</sub></sup>   | Viele <sup><sub>[Optional]<br> (z.B. OpenAI, Pinecone, usw.)</sub></sup>  | 7K <br><sup><sub>(nur Kern)</sub></sup> | +26MB <br><sup><sub>(nur Kern)</sub></sup> |
| **BrainyFlow** |    **Graph**    |                             **Keine**                              |                                 **Keine**                                 |                 **100**                 |                 **+56KB**                  |

</div>

## Wie funktioniert BrainyFlow?

Die [100 Zeilen](https://github.com/zvictor/BrainyFlow/blob/main/python/__init__.py) erfassen die Kernabstraktion von LLM-Frameworks: Graph!
<br>

<div align="center">
  <img src="https://github.com/zvictor/brainyflow/raw/main/.github/media/abstraction.jpg" width="900"/>
</div>
<br>

Von dort aus ist es einfach, beliebte Designmuster wie ([Multi-](https://brainy.gitbook.io/flow/design_pattern/multi_agent))[Agenten](https://brainy.gitbook.io/flow/design_pattern/agent), [Workflow](https://brainy.gitbook.io/flow/design_pattern/workflow), [RAG](https://brainy.gitbook.io/flow/design_pattern/rag) usw. zu implementieren.
<br>

<div align="center">
  <img src="https://github.com/zvictor/brainyflow/raw/main/.github/media/design.jpg" width="900"/>
</div>
<br>
✨ Hier sind grundlegende Tutorials:

<div align="center">
  
|  Name  | Schwierigkeit    |  Beschreibung  |  
| :-------------:  | :-------------: | :--------------------- |  
| [Chat](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-chat) | ☆☆☆ <br> *Dummy*   | Ein einfacher Chatbot mit Konversationsverlauf |
| [Strukturierte Ausgabe](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-structured-output) | ☆☆☆ <br> *Dummy* | Extrahieren strukturierter Daten aus Lebensläufen durch Prompting |
| [Workflow](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-workflow) | ☆☆☆ <br> *Dummy*   | Ein Schreibworkflow, der Gliederungen erstellt, Inhalte schreibt und Styling anwendet |
| [Agent](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-agent) | ☆☆☆ <br> *Dummy*   | Ein Recherche-Agent, der im Web suchen und Fragen beantworten kann |
| [RAG](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-rag) | ☆☆☆ <br> *Dummy*   | Ein einfacher Retrieval-augmented Generation-Prozess |
| [Map-Reduce](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-map-reduce) | ☆☆☆ <br> *Dummy* | Ein Lebenslauf-Qualifikationsprozessor mit Map-Reduce-Muster für Batch-Auswertung |
| [Streaming](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-llm-streaming) | ☆☆☆ <br> *Dummy*   | Eine Echtzeit-LLM-Streaming-Demo mit Benutzerunterbrechungsfähigkeit |
| [Chat-Absicherung](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-chat-guardrail) | ☆☆☆ <br> *Dummy*  | Ein Reiseberater-Chatbot, der nur reisebezogene Anfragen verarbeitet |
| [Multi-Agent](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-multi-agent) | ★☆☆ <br> *Anfänger* | Ein Tabu-Wortspiel für asynchrone Kommunikation zwischen zwei Agenten |
| [Supervisor](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-supervisor) | ★☆☆ <br> *Anfänger* | Forschungsagent wird unzuverlässig... Bauen wir einen Überwachungsprozess! |
| [Parallel](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-parallel-batch) | ★☆☆ <br> *Anfänger*   | Eine parallele Ausführungs-Demo, die 3x Beschleunigung zeigt |
| [Parallel Flow](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-parallel-batch-flow) | ★☆☆ <br> *Anfänger*   | Eine parallele Bildverarbeitungs-Demo, die 8x Beschleunigung mit mehreren Filtern zeigt |
| [Mehrheitsvotum](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-majority-vote) | ★☆☆ <br> *Anfänger* | Verbessere die Reasoning-Genauigkeit durch Aggregation mehrerer Lösungsversuche |
| [Thinking](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-thinking) | ★☆☆ <br> *Anfänger*   | Löse komplexe Reasoning-Probleme durch Chain-of-Thought |
| [Memory](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-chat-memory) | ★☆☆ <br> *Anfänger* | Ein Chatbot mit Kurz- und Langzeitgedächtnis |
| [MCP](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-mcp) | ★☆☆ <br> *Anfänger* | Agent, der das Model Context Protocol für numerische Operationen verwendet |

</div>

👀 Möchtest du andere Tutorials für Anfänger sehen? [Erstelle ein Issue!](https://github.com/zvictor/BrainyFlow/issues/new)

## Wie verwendet man BrainyFlow?

🚀 Durch **Agentisches Programmieren**—das schnellste LLM-App-Entwicklungsparadigma, bei dem _Menschen designen_ und _Agenten programmieren_!

<br>
<div align="center">
  <a href="https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to" target="_blank">
    <img src="https://substackcdn.com/image/fetch/f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F423a39af-49e8-483b-bc5a-88cc764350c6_1050x588.png" width="700" alt="IMAGE ALT TEXT" style="cursor: pointer;">
  </a>
</div>
<br>

✨ Hier sind Beispiele für komplexere LLM-Apps:

<div align="center">
  
|  App-Name     |  Schwierigkeit    | Themen  | Menschliches Design | Agent-Code |
| :-------------:  | :-------------: | :---------------------: |  :---: |  :---: |
| [Cursor mit Cursor bauen](https://github.com/The-Pocket/Tutorial-Cursor) <br> <sup><sub>Wir werden bald die Singularität erreichen ...</sup></sub> | ★★★ <br> *Fortgeschritten*   | [Agent](https://brainy.gitbook.io/flow/design_pattern/agent) | [Design-Dokument](https://github.com/The-Pocket/Tutorial-Cursor/blob/main/docs/design.md) | [Flow-Code](https://github.com/The-Pocket/Tutorial-Cursor/blob/main/flow.py)
| [Frag KI Paul Graham](https://github.com/The-Pocket/Tutorial-YC-Partner) <br> <sup><sub>Frag KI Paul Graham, falls du nicht reinkommst</sup></sub> | ★★☆ <br> *Mittel*   | [RAG](https://brainy.gitbook.io/flow/design_pattern/rag) <br> [Map Reduce](https://brainy.gitbook.io/flow/design_pattern/mapreduce) <br> [TTS](https://brainy.gitbook.io/flow/utility_function/text_to_speech) | [Design-Dokument](https://github.com/The-Pocket/Tutorial-AI-Paul-Graham/blob/main/docs/design.md) | [Flow-Code](https://github.com/The-Pocket/Tutorial-AI-Paul-Graham/blob/main/flow.py)
| [Youtube-Zusammenfasser](https://github.com/The-Pocket/Tutorial-Youtube-Made-Simple)  <br> <sup><sub> Erklärt dir YouTube-Videos, als wärst du 5 </sup></sub> | ★☆☆ <br> *Anfänger*   | [Map Reduce](https://brainy.gitbook.io/flow/design_pattern/mapreduce) |  [Design-Dokument](https://github.com/The-Pocket/Tutorial-Youtube-Made-Simple/blob/main/docs/design.md) | [Flow-Code](https://github.com/The-Pocket/Tutorial-Youtube-Made-Simple/blob/main/flow.py)
| [Kaltakquise-Generator](https://github.com/The-Pocket/Tutorial-Cold-Email-Personalization)  <br> <sup><sub> Sofortige Eisbrecher, die kalte Leads heiß machen </sup></sub> | ★☆☆ <br> *Anfänger*   | [Map Reduce](https://brainy.gitbook.io/flow/design_pattern/mapreduce) <br> [Web-Suche](https://brainy.gitbook.io/flow/utility_function/websearch) |  [Design-Dokument](https://github.com/The-Pocket/Tutorial-Cold-Email-Personalization/blob/master/docs/design.md) | [Flow-Code](https://github.com/The-Pocket/Tutorial-Cold-Email-Personalization/blob/master/flow.py)

</div>

- Willst du **Agentisches Programmieren** lernen?

  - Schau dir [meinen YouTube-Kanal](https://www.youtube.com/@ZacharyLLM?sub_confirmation=1) für Video-Tutorials an, wie einige der obigen Apps erstellt wurden!

  - Willst du deine eigene LLM-App bauen? Lies diesen [Beitrag](https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to)! Beginne mit [dieser Vorlage](https://github.com/The-Pocket/PocketFlow-Template-Python)!

  - Willst du die detaillierten Schritte lernen? Lies diesen [Leitfaden](https://brainy.gitbook.io/flow/guide)!
