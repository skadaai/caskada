<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://cdn.jsdelivr.net/gh/skadaai/caskada@main/.github/media/logo-dark.png">
    <source media="(prefers-color-scheme: light)" srcset="https://cdn.jsdelivr.net/gh/skadaai/caskada@main/.github/media/logo-light.png">
    <img width="280" alt="Caskadas Logo" src="https://cdn.jsdelivr.net/gh/skadaai/caskada@main/.github/media/logo-light.png">
  </picture>
<p>

<p align="center">
  Ein radikal minimalistisches KI-Framework (nur <a href="https://github.com/skadaai/caskada/blob/main/python/caskada.py">200 Zeilen in Python</a>! 🤯)

  <br />
  Erstelle leistungsstarke KI-Agenten mit minimalem Code und maximaler Freiheit.
  <br />
  <sub>Lass Agenten Agenten ohne überflüssigen Ballast, Abhängigkeiten oder Vendor Lock-in erstellen 😮</sub>
</p>

<p align="center">

  <a href="https://pypi.org/project/caskada">
   <img src="https://img.shields.io/pypi/dw/caskada?logo=python&label=Python&style=flat-square" alt="Python-Version">
  </a>
  <a href="https://npmjs.com/packages/caskada">
   <img src="https://img.shields.io/npm/d18m/caskada?logo=typescript&label=Typescript&style=flat-square" alt="Typescript-Version">
  </a>
  <a href="https://discord.gg/N9mVvxRXyH">
    <img src="https://img.shields.io/discord/1346833819172601907?logo=discord&style=flat-square" alt="Discord">
  </a>
  <a href="https://github.com/skadaai/caskada">
    <img src="https://img.shields.io/github/stars/skadaai/caskada?logo=github&style=flat-square" alt="GitHub-Repository">
  </a>
  <a href="https://github.com/sponsors/zvictor">
    <img src="https://img.shields.io/github/sponsors/zvictor?logo=github&style=flat-square" alt="GitHub-Sponsoren">
  </a>
</p>

Caskada ist ein Framework, das _Agentic Coding_ durch leistungsstarke Abstraktionen ermöglicht.

Es bietet eine einfache Schnittstelle zum Erstellen komplexer KI-Anwendungen basierend auf _verschachtelten gerichteten Graphen_ mit gemeinsamem Zustand.
Es ermöglicht sowohl Menschen als auch KI-Assistenten, effektiv an der Gestaltung und Implementierung von KI-Systemen zusammenzuarbeiten.

## Funktionen

- **Gehirnfreundlich 🧠**: Intuitiv für Menschen und KI-Assistenten
- **Minimalistisches Design ✨**: Kernabstraktionen in nur (_richtig gehört!_) 200 Codezeilen
- **Freiheit 🔓**: Kein überflüssiger Ballast, Abhängigkeiten oder Vendor Lock-in
- **Komponierbar 🧩**: Baue komplexe Systeme aus einfachen, wiederverwendbaren Komponenten
- **Leistungsstark 🦾**: Unterstützt alles, was du liebst – ([Multi-](https://skadaai.gitbook.io/caskada/design_pattern/multi_agent))[Agenten](https://skadaai.gitbook.io/caskada/design_pattern/agent), [Workflow](https://skadaai.gitbook.io/caskada/design_pattern/workflow), [RAG](https://skadaai.gitbook.io/caskada/design_pattern/rag) und mehr
- **Agentic-Coding 🤖**: Für die KI-unterstützte Entwicklung konzipiert
- **Universell 🌈**: Funktioniert mit jedem LLM-Anbieter oder API
- **Polyglott 🌍**: <!-- gitbook-ignore-start --><a href="https://pypi.org/project/caskada"><img src="https://github.com/skadaai/caskada/raw/main/.github/media/python.svg" width="16" height="16" alt="Python-Logo" style="vertical-align: middle; margin: 0 2px;"></a><!-- gitbook-ignore-end --> Python und <!-- gitbook-ignore-start --><a href="https://npmjs.com/packages/caskada"><img src="https://github.com/skadaai/caskada/raw/main/.github/media/typescript.svg" width="16" height="16" alt="Typescript-Logo" style="vertical-align: middle; margin: 0 2px;"></a><!-- gitbook-ignore-end --> Typescript werden beide unterstützt

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

<!-- gitbook-ignore-start -->

## Dokumentation

Unsere Dokumentation ist inklusiv und für biologische sowie synthetische Geister geeignet.<br />
Starte, indem du deine Bedingung auswählst – oder vielleicht _die, von der du glaubst, dass du darauf konditioniert bist_:

\>> [Ich bin kohlenstoffbasiert 🐥](https://skadaai.gitbook.io/caskada/introduction/getting_started) <<

\>> [Ich bin siliziumbasiert 🤖](https://flow.brainy.sh/docs.txt) <<

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

<!-- gitbook-ignore-end -->

## Warum Brainy Flow?

Aktuelle LLM-Frameworks sind aufgebläht... Du brauchst tatsächlich nur 200 Zeilen für ein robustes LLM-Framework!

<div align="center">
  <img src="https://raw.githubusercontent.com/skadaai/caskada/main/.github/media/meme.jpg" width="500"/>

|                                                                                                                                                                                                                | **Abstraktion** |                     **App-Spezifische Wrapper**                      |                       **Anbieter-Spezifische Wrapper**                       |                **Zeilen**                 |                  **Größe**                   |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------: | :----------------------------------------------------------------: | :----------------------------------------------------------------------: | :--------------------------------------: | :-----------------------------------------: |
| LangChain                                                                                                                                                                                                      |  Agent, Kette   |      Viele <br><sup><sub>(z.B. QA, Zusammenfassung)</sub></sup>      |      Viele <br><sup><sub>(z.B. OpenAI, Pinecone, etc.)</sub></sup>       |                   405K                   |                   +166MB                    |
| CrewAI                                                                                                                                                                                                         |  Agent, Kette   | Viele <br><sup><sub>(z.B. FileReadTool, SerperDevTool)</sub></sup> | Viele <br><sup><sub>(z.B. OpenAI, Anthropic, Pinecone, etc.)</sub></sup> |                   18K                    |                   +173MB                    |
| SmolAgent                                                                                                                                                                                                      |      Agent      |   Einige <br><sup><sub>(z.B. CodeAgent, VisitWebTool)</sub></sup>   |  Einige <br><sup><sub>(z.B. DuckDuckGo, Hugging Face, etc.)</sub></sup>   |                    8K                    |                   +198MB                    |
| LangGraph                                                                                                                                                                                                      |  Agent, Graph   |       Einige <br><sup><sub>(z.B. Semantische Suche)</sub></sup>       | Einige <br><sup><sub>(z.B. PostgresStore, SqliteSaver, etc.) </sub></sup> |                   37K                    |                    +51MB                    |
| AutoGen                                                                                                                                                                                                        |      Agent      |   Einige <br><sup><sub>(z.B. Tool Agent, Chat Agent)</sub></sup>    | Viele <sup><sub>[Optional]<br> (z.B. OpenAI, Pinecone, etc.)</sub></sup> | 7K <br><sup><sub>(nur Kern)</sub></sup> | +26MB <br><sup><sub>(nur Kern)</sub></sup> |
| **Caskada** <!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/typescript.svg" width="16" height="16" alt="Typescript-Logo"><!-- gitbook-ignore-end -->.ts |    **Graph**    |                              **Keine**                              |                                 **Keine**                                 |                 **300**                  |                 **wenige KB**                  |
| **Caskada** <!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/python.svg" width="16" height="16" alt="Python-Logo"><!-- gitbook-ignore-end -->.py         |    **Graph**    |                              **Keine**                              |                                 **Keine**                                 |                 **200**                  |                 **wenige KB**                  |

</div>

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

## Wie funktioniert Caskada?

Die einzelne Datei in <a href="https://github.com/skadaai/caskada/blob/main/python/caskada.py"><!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/python.svg" width="16" height="16" alt="Python-Logo" style="vertical-align: middle; margin: 0 2px;"> <!-- gitbook-ignore-end -->Python</a> oder <a href="https://github.com/skadaai/caskada/blob/main/typescript/caskada.ts"><!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/typescript.svg" width="16" height="16" alt="Typescript-Logo" style="vertical-align: middle; margin: 0 2px;"> <!-- gitbook-ignore-end -->Typescript</a> erfasst die Kernabstraktion von LLM-Frameworks: Graph!
<br>

<div align="center">
  <img src="https://raw.githubusercontent.com/skadaai/caskada/main/.github/media/abstraction.jpg" width="1300"/>
</div>
<br>

- [Node](https://skadaai.gitbook.io/caskada/core_abstraction/node) behandelt einfache (LLM-)Aufgaben mit einem klaren Lebenszyklus (`prep` → `exec` → `post`).
- [Flow](https://skadaai.gitbook.io/caskada/core_abstraction/flow) verbindet Knoten durch **Aktionen** (beschriftete Kanten) und orchestriert die Ausführung.
- [Memory](https://skadaai.gitbook.io/caskada/core_abstraction/memory) verwaltet gemeinsamen (`global`) und isolierten (`local`) Zustand und ermöglicht die Kommunikation zwischen Knoten.

Von dort aus ist es einfach, alle beliebten Designmuster zu implementieren:
<br>

<div align="center">
  <img src="https://raw.githubusercontent.com/skadaai/caskada/main/.github/media/design.jpg" width="1300"/>
</div>
<br>

- [Agent](https://skadaai.gitbook.io/caskada/design_pattern/agent) trifft autonome Entscheidungen basierend auf dem Kontext.
- [Workflow](https://skadaai.gitbook.io/caskada/design_pattern/workflow) verkettet mehrere Aufgaben zu sequenziellen Pipelines.
- [RAG](https://skadaai.gitbook.io/caskada/design_pattern/rag) integriert Datenabruf mit Generierung.
- [Map Reduce](https://skadaai.gitbook.io/caskada/design_pattern/mapreduce) teilt Datenaufgaben in Map- und Reduce-Schritte auf.
- [Structured Output](https://skadaai.gitbook.io/caskada/design_pattern/structure) formatiert Ausgaben konsistent.
- [Multi-Agenten](https://skadaai.gitbook.io/caskada/design_pattern/multi_agent) koordinieren mehrere Agenten.

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

## Tutorials

<div align="center">
  
|  Name  | Schwierigkeit    |  Beschreibung  |  
| :-------------:  | :-------------: | :--------------------- |  
| [Chat](https://github.com/skadaai/caskada/tree/main/cookbook/python-chat) | ☆☆☆ <br> *Einfach*   | Ein einfacher Chat-Bot mit Konversationsverlauf |
| [RAG](https://github.com/skadaai/caskada/tree/main/cookbook/python-rag) | ☆☆☆ <br> *Einfach*   | Ein einfacher Retrieval-augmented Generation Prozess |
| [Workflow](https://github.com/skadaai/caskada/tree/main/cookbook/python-workflow) | ☆☆☆ <br> *Einfach*   | Ein Schreib-Workflow, der Inhalte gliedert, schreibt und formatiert |
| [Map-Reduce](https://github.com/skadaai/caskada/tree/main/cookbook/python-map-reduce) | ☆☆☆ <br> *Einfach* | Ein Lebenslauf-Qualifikationsprozessor, der das Map-Reduce-Muster für die Stapelauswertung verwendet |
| [Agent](https://github.com/skadaai/caskada/tree/main/cookbook/python-agent) | ☆☆☆ <br> *Einfach*   | Ein Forschungsagent, der das Web durchsuchen und Fragen beantworten kann |
| [Streaming](https://github.com/skadaai/caskada/tree/main/cookbook/python-llm-streaming) | ☆☆☆ <br> *Einfach*   | Eine Echtzeit-LLM-Streaming-Demo mit Unterbrechungsmöglichkeit durch den Benutzer |
| [Multi-Agent](https://github.com/skadaai/caskada/tree/main/cookbook/python-multi-agent) | ★☆☆ <br> *Anfänger* | Ein Tabu-Wortspiel für asynchrone Kommunikation zwischen zwei Agenten |
| [Supervisor](https://github.com/skadaai/caskada/tree/main/cookbook/python-supervisor) | ★☆☆ <br> *Anfänger* | Der Forschungsagent wird unzuverlässig... Lass uns einen Überwachungsprozess erstellen|
| [Parallel](https://github.com/skadaai/caskada/tree/main/cookbook/python-parallel-batch) | ★☆☆ <br> *Anfänger*   | Eine Parallelausführungs-Demo, die eine 3-fache Beschleunigung zeigt |
| [Thinking](https://github.com/skadaai/caskada/tree/main/cookbook/python-thinking) | ★☆☆ <br> *Anfänger*   | Löse komplexe Denkaufgaben durch Chain-of-Thought |
| [Memory](https://github.com/skadaai/caskada/tree/main/cookbook/python-chat-memory) | ★☆☆ <br> *Anfänger* | Ein Chat-Bot mit Kurzzeit- und Langzeitgedächtnis |

</div>

Und viele mehr für alle Levels! [Schau sie dir alle an!](https://github.com/skadaai/caskada/tree/main/cookbook)

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

## Schnellstart

Neu bei Caskada? Schau dir unseren [Schnellstart](https://skadaai.gitbook.io/caskada/introduction/getting_started) an, um deinen ersten Flow im Handumdrehen zu erstellen.

## Bereit, selbstcodierende Apps zu bauen?

Schau dir die [Anleitung zum Agentic Coding](https://skadaai.gitbook.io/caskada/guides/agentic_coding) an, den schnellsten Weg, selbstcodierende LLM-Projekte mit Caskada zu entwickeln!

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

## Danksagung

Wir möchten uns herzlich bei den Schöpfern und Mitwirkenden des PocketFlow-Frameworks bedanken, von dem Caskada als Fork entstanden ist.

## Haftungsausschluss

Caskada wird "wie besehen" ohne jegliche Gewährleistung oder Garantie bereitgestellt.  
Wir übernehmen keine Verantwortung für die Verwendung der generierten Ausgaben, einschließlich, aber nicht beschränkt auf deren Genauigkeit, Legalität oder mögliche Folgen aus deren Verwendung.

## Sponsoren

<p align="center">
  <a style="color: inherit" href="https://github.com/sponsors/zvictor?utm_source=caskada&utm_medium=sponsorship&utm_campaign=caskada&utm_id=caskada">
    <img width="150" src="https://cdn.jsdelivr.net/gh/skadaai/caskada@main/.github/media/brain.png" alt="Caskadas Logo" />
  </a><br /><br />
  Caskada läuft mit 200 Codezeilen und deiner Großzügigkeit! 💰<br />
    <a style="color: inherit" href="https://github.com/sponsors/zvictor?utm_source=caskada&utm_medium=sponsorship&utm_campaign=caskada&utm_id=caskada">
      Hilf uns, mehr KI mit weniger Code (aber vielleicht mehr Koffein) zu liefern
    </a> ☕<br /><br />
    <a style="color: inherit" href="https://github.com/sponsors/zvictor?utm_source=caskada&utm_medium=sponsorship&utm_campaign=caskada&utm_id=caskada">Deine Unterstützung</a> hilft, es minimalistisch, leistungsstark und abhängigkeitsfrei zu halten! 🚀
  </a>
</p>

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)