<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://cdn.jsdelivr.net/gh/skadaai/caskada@main/.github/media/logo-dark.png">
    <source media="(prefers-color-scheme: light)" srcset="https://cdn.jsdelivr.net/gh/skadaai/caskada@main/.github/media/logo-light.png">
    <img width="280" alt="Brainyflow's Logo" src="https://cdn.jsdelivr.net/gh/skadaai/caskada@main/.github/media/logo-light.png">
  </picture>
<p>

<p align="center">
  Ein radikal minimalistisches AI-Framework (nur <a href="https://github.com/skadaai/caskada/blob/main/python/brainyflow.py">200 Zeilen in Python</a>! 🤯)

  <br />
  Entwickeln Sie leistungsstarke AI-Agenten mit minimalem Code und maximaler Freiheit.
  <br />
  <sub>Lassen Sie Agenten Agenten ohne unnötigen Ballast, Abhängigkeiten oder Herstellerbindung entwickeln 😮</sub>
</p>

<p align="center">

  <a href="https://pypi.org/project/brainyflow">
   <img src="https://img.shields.io/pypi/dw/brainyflow?logo=python&label=Python&style=flat-square" alt="Python-Version">
  </a>
  <a href="https://npmjs.com/packages/brainyflow">
   <img src="https://img.shields.io/npm/d18m/brainyflow?logo=typescript&label=Typescript&style=flat-square" alt="Typescript-Version">
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

Es bietet eine einfache Schnittstelle zum Entwickeln komplexer AI-Anwendungen auf Basis von _verschachtelten gerichteten Graphen_ mit gemeinsamem Zustand.
Es ermöglicht sowohl Menschen als auch AI-Assistenten, effektiv bei der Entwicklung und Implementierung von AI-Systemen zusammenzuarbeiten.

## Funktionen

- **Brain-Easy 🧠**: Intuitiv für Menschen und AI-Assistenten
- **Minimalistisches Design ✨**: Kernabstraktionen in nur (_Sie hörten es richtig!_) 200 Zeilen Code
- **Freiheit 🔓**: Kein unnötiger Ballast, Abhängigkeiten oder Herstellerbindung
- **Komponierbar 🧩**: Entwickeln Sie komplexe Systeme aus einfachen, wiederverwendbaren Komponenten
- **Leistungsstark 🦾**: Unterstützt alles, was Sie lieben—([Multi-](https://brainy.gitbook.io/flow/design_pattern/multi_agent))[Agenten](https://brainy.gitbook.io/flow/design_pattern/agent), [Workflow](https://brainy.gitbook.io/flow/design_pattern/workflow), [RAG](https://brainy.gitbook.io/flow/design_pattern/rag) und mehr
- **Agentic-Coding 🤖**: Entwickelt für die AI-unterstützte Entwicklung
- **Universell 🌈**: Funktioniert mit jedem LLM-Anbieter oder API
- **Polyglot 🌍**: <!-- gitbook-ignore-start --><a href="https://pypi.org/project/brainyflow"><img src="https://github.com/skadaai/caskada/raw/main/.github/media/python.svg" width="16" height="16" alt="Python-Logo" style="vertical-align: middle; margin: 0 2px;"></a><!-- gitbook-ignore-end --> Python und <!-- gitbook-ignore-start --><a href="https://npmjs.com/packages/brainyflow"><img src="https://github.com/skadaai/caskada/raw/main/.github/media/typescript.svg" width="16" height="16" alt="Typescript-Logo" style="vertical-align: middle; margin: 0 2px;"></a><!-- gitbook-ignore-end --> Typescript werden beide unterstützt

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

<!-- gitbook-ignore-start -->

## Dokumentation

Unsere Dokumentation ist inklusiv, geeignet für biologische und synthetische Gehirne.<br />
Beginnen Sie, indem Sie Ihre Bedingung auswählen - oder vielleicht _die, an die Sie glauben sollen_:

\>> [Ich bin kohlenstoffbasiert 🐥](https://brainy.gitbook.io/flow/introduction/getting_started) <<

\>> [Ich bin siliziumbasiert 🤖](https://flow.brainy.sh/docs.txt) <<

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

<!-- gitbook-ignore-end -->

## Warum Brainy Flow?

Aktuelle LLM-Frameworks sind aufgebläht... Sie benötigen tatsächlich nur 200 Zeilen für ein robustes LLM-Framework!

<div align="center">
  <img src="https://raw.githubusercontent.com/skadaai/caskada/main/.github/media/meme.jpg" width="500"/>

|                                                                                                                                                                                                                | **Abstraktion** |                     **App-spezifische Wrapper**                      |                       **Hersteller-spezifische Wrapper**                       |                **Zeilen**                 |                  **Größe**                   |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------: | :----------------------------------------------------------------: | :----------------------------------------------------------------------: | :--------------------------------------: | :-----------------------------------------: |
| LangChain                                                                                                                                                                                                      |  Agent, Kette   |      Viele <br><sup><sub>(z.B. QA, Zusammenfassung)</sub></sup>      |      Viele <br><sup><sub>(z.B. OpenAI, Pinecone usw.)</sub></sup>       |                   405K                   |                   +166MB                    |
| CrewAI                                                                                                                                                                                                         |  Agent, Kette   | Viele <br><sup><sub>(z.B. FileReadTool, SerperDevTool)</sub></sup> | Viele <br><sup><sub>(z.B. OpenAI, Anthropic, Pinecone usw.)</sub></sup> |                   18K                    |                   +173MB                    |
| SmolAgent                                                                                                                                                                                                      |      Agent      |   Einige <br><sup><sub>(z.B. CodeAgent, VisitWebTool)</sub></sup>   |  Einige <br><sup><sub>(z.B. DuckDuckGo, Hugging Face usw.)</sub></sup>   |                    8K                    |                   +198MB                    |
| LangGraph                                                                                                                                                                                                      |  Agent, Graph   |       Einige <br><sup><sub>(z.B. semantische Suche)</sub></sup>       | Einige <br><sup><sub>(z.B. PostgresStore, SqliteSaver usw.) </sub></sup> |                   37K                    |                    +51MB                    |
| AutoGen                                                                                                                                                                                                        |      Agent      |   Einige <br><sup><sub>(z.B. Tool-Agent, Chat-Agent)</sub></sup>    | Viele <sup><sub>[Optional]<br> (z.B. OpenAI, Pinecone usw.)</sub></sup> | 7K <br><sup><sub>(nur Kern)</sub></sup> | +26MB <br><sup><sub>(nur Kern)</sub></sup> |
| **Caskada** <!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/typescript.svg" width="16" height="16" alt="Typescript-Logo"><!-- gitbook-ignore-end -->.ts |    **Graph**    |                              **Keine**                              |                                 **Keine**                                 |                 **300**                  |                 **einige KB**                  |
| **Caskada** <!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/python.svg" width="16" height="16" alt="Python-Logo"><!-- gitbook-ignore-end -->.py         |    **Graph**    |                              **Keine**                              |                                 **Keine**                                 |                 **200**                  |                 **einige KB**                  |

</div>

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

## Wie funktioniert Caskada?

Die einzelne Datei in <a href="https://github.com/skadaai/caskada/blob/main/python/brainyflow.py"><!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/python.svg" width="16" height="16" alt="Python-Logo" style="vertical-align: middle; margin: 0 2px;"> <!-- gitbook-ignore-end -->Python</a> oder <a href="https://github.com/skadaai/caskada/blob/main/typescript/brainyflow.ts"><!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/typescript.svg" width="16" height="16" alt="Typescript-Logo" style="vertical-align: middle; margin: 0 2px;"> <!-- gitbook-ignore-end -->Typescript</a> erfasst die Kernabstraktion von LLM-Frameworks: Graph!
<br>

<div align="center">
  <img src="https://raw.githubusercontent.com/skadaai/caskada/main/.github/media/abstraction.jpg" width="1300"/>
</div>
<br>

- [Knoten](https://brainy.gitbook.io/flow/core_abstraction/node) verarbeiten einfache (LLM-)Aufgaben mit einem klaren Lebenszyklus (`prep` → `exec` → `post`).
- [Fluss](https://brainy.gitbook.io/flow/core_abstraction/flow) verbindet Knoten durch **Aktionen** (markierte Kanten), die die Ausführung orchestrieren.
- [Speicher](https://brainy.gitbook.io/flow/core_abstraction/memory) verwaltet gemeinsamen (`global`) und isolierten (`lokal`) Zustand, ermöglicht die Kommunikation zwischen Knoten.

Von dort aus ist es einfach, alle beliebten Designmuster zu implementieren:
<br>

<div align="center">
  <img src="https://raw.githubusercontent.com/skadaai/caskada/main/.github/media/design.jpg" width="1300"/>
</div>
<br>

- [Agent](https://brainy.gitbook.io/flow/design_pattern/agent) trifft autonome Entscheidungen auf der Grundlage des Kontexts.
- [Workflow](https://brainy.gitbook.io/flow/design_pattern/workflow) verkettet mehrere Aufgaben in sequenzielle Pipelines.
- [RAG](https://brainy.gitbook.io/flow/design_pattern/rag) integriert Datenbeschaffung mit Generierung.
- [Map Reduce](https://brainy.gitbook.io/flow/design_pattern/mapreduce) teilt Datenaufgaben in Map- und Reduce-Schritte auf.
- [Strukturierte Ausgabe](https://brainy.gitbook.io/flow/design_pattern/structure) formatiert Ausgaben konsistent.
- [Multi-Agenten](https://brainy.gitbook.io/flow/design_pattern/multi_agent) koordiniert mehrere Agenten.

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

## Tutorials

<div align="center">
  
|  Name  | Schwierigkeitsgrad    |  Beschreibung  |  
| :-------------:  | :-------------: | :--------------------- |  
| [Chat](https://github.com/skadaai/caskada/tree/main/cookbook/python-chat) | ☆☆☆ <br> *Dummy*   | Ein einfacher Chatbot mit Gesprächsverlauf |
| [RAG](https://github.com/skadaai/caskada/tree/main/cookbook/python-rag) | ☆☆☆ <br> *Dummy*   | Ein einfacher RAG-Prozess (Retrieval-augmented Generation) |
| [Workflow](https://github.com/skadaai/caskada/tree/main/cookbook/python-workflow) | ☆☆☆ <br> *Dummy*   | Ein Schreib-Workflow, der Inhalte gliedert, schreibt und formatiert |
| [Map-Reduce](https://github.com/skadaai/caskada/tree/main/cookbook/python-map-reduce) | ☆☆☆ <br> *Dummy* | Ein Resume-Qualifizierungsprozessor, der das Map-Reduce-Muster für die Stapelverarbeitung verwendet |
| [Agent](https://github.com/skadaai/caskada/tree/main/cookbook/python-agent) | ☆☆☆ <br> *Dummy*   | Ein Recherche-Agent, der im Web suchen und Fragen beantworten kann |
| [Streaming](https://github.com/skadaai/caskada/tree/main/cookbook/python-llm-streaming) | ☆☆☆ <br> *Dummy*   | Eine Echtzeit-LLM-Streaming-Demo mit Benutzerunterbrechung |
| [Multi-Agent](https://github.com/skadaai/caskada/tree/main/cookbook/python-multi-agent) | ★☆☆ <br> *Anfänger* | Ein Tabu-Wort-Spiel für die asynchrone Kommunikation zwischen zwei Agenten |
| [Supervisor](https://github.com/skadaai/caskada/tree/main/cookbook/python-supervisor) | ★☆☆ <br> *Anfänger* | Recherche-Agent wird unzuverlässig... Lassen Sie uns einen Überwachungsprozess entwickeln|
| [Parallel](https://github.com/skadaai/caskada/tree/main/cookbook/python-parallel-batch) | ★☆☆ <br> *Anfänger*   | Eine Demo für parallele Ausführung, die eine 3-fache Beschleunigung zeigt |
| [Denken](https://github.com/skadaai/caskada/tree/main/cookbook/python-thinking) | ★☆☆ <br> *Anfänger*   | Lösen Sie komplexe Denkprobleme durch Chain-of-Thought |
| [Speicher](https://github.com/skadaai/caskada/tree/main/cookbook/python-chat-memory) | ★☆☆ <br> *Anfänger* | Ein Chatbot mit Kurzzeit- und Langzeitspeicher |

</div>

Und viele weitere für alle Niveaus verfügbar! [Sehen Sie sich alle an!](https://github.com/skadaai/caskada/tree/main/cookbook)

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

## Schnellstart

Neu bei Caskada? Sehen Sie sich unseren [Schnellstart](https://brainy.gitbook.io/flow/introduction/getting_started) an, um Ihren ersten Fluss in kürzester Zeit zu entwickeln.

## Bereit, selbstkodierende Apps zu entwickeln?

Sehen Sie sich die [Agentic-Coding-Anleitung](https://brainy.gitbook.io/flow/guides/agentic_coding) an, die schnellste Möglichkeit, selbstkodierende LLM-Projekte mit Caskada zu entwickeln!

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

## Anerkennung

Wir möchten den Erstellern und Mitwirkenden des PocketFlow-Frameworks, von dem Caskada abstammt, unseren tiefsten Dank aussprechen.

## Mitwirkende gesucht!

Wir suchen Mitwirkende für alle Aspekte des Projekts. Ob Sie sich für Dokumentation, Tests oder die Implementierung von Funktionen interessieren, wir freuen uns über Ihre Hilfe!

Werden Sie Teil unseres Discord-Servers!

## Haftungsausschluss

Caskada wird "wie besehen" ohne jegliche Gewährleistungen oder Garantien bereitgestellt.  
Wir übernehmen keine Verantwortung für die Verwendung der generierten Ausgabe, einschließlich, aber nicht beschränkt auf ihre Genauigkeit, Rechtmäßigkeit oder mögliche Folgen, die sich aus ihrer Verwendung ergeben.

## Sponsoren

<p align="center">
  <a style="color: inherit" href="https://github.com/sponsors/zvictor?utm_source=brainyflow&utm_medium=sponsorship&utm_campaign=brainyflow&utm_id=brainyflow">
    <img width="150" src="https://cdn.jsdelivr.net/gh/skadaai/caskada@main/.github/media/brain.png" alt="Brainyflow's Logo" />
  </a><br /><br />
  Caskada läuft auf 200 Zeilen Code und Ihrer Großzügigkeit! 💰<br />
    <a style="color: inherit" href="https://github.com/sponsors/zvictor?utm_source=brainyflow&utm_medium=sponsorship&utm_campaign=brainyflow&utm_id=brainyflow">
      Helfen Sie uns, mehr KI mit weniger Code (aber vielleicht mehr Koffein) zu entwickeln
    </a> ☕<br /><br />
    <a style="color: inherit" href="https://github.com/sponsors/zvictor?utm_source=brainyflow&utm_medium=sponsorship&utm_campaign=brainyflow&utm_id=brainyflow">Ihre Unterstützung</a> hilft, es minimal, leistungsstark und abhängigkeitsfrei zu halten! 🚀
  </a>
</p>

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)