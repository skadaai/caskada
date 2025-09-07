<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://cdn.jsdelivr.net/gh/skadaai/caskada@main/.github/media/logo-dark.png">
    <source media="(prefers-color-scheme: light)" srcset="https://cdn.jsdelivr.net/gh/skadaai/caskada@main/.github/media/logo-light.png">
    <img width="280" alt="Logo de Caskada" src="https://cdn.jsdelivr.net/gh/skadaai/caskada@main/.github/media/logo-light.png">
  </picture>
<p>

<p align="center">
  Un framework de IA radicalmente minimalista (¡solo <a href="https://github.com/skadaai/caskada/blob/main/python/caskada.py">200 líneas en Python</a>! 🤯)

  <br />
  Construye agentes de IA poderosos con código mínimo y máxima libertad.
  <br />
  <sub>Permite que los agentes construyan agentes sin bloat, dependencias ni vendor lock-in 😮</sub>
</p>

<p align="center">

  <a href="https://pypi.org/project/caskada">
   <img src="https://img.shields.io/pypi/dw/caskada?logo=python&label=Python&style=flat-square" alt="versión de python">
  </a>
  <a href="https://npmjs.com/packages/caskada">
   <img src="https://img.shields.io/npm/d18m/caskada?logo=typescript&label=Typescript&style=flat-square" alt="versión de typescript">
  </a>
  <a href="https://discord.gg/N9mVvxRXyH">
    <img src="https://img.shields.io/discord/1346833819172601907?logo=discord&style=flat-square" alt="Discord">
  </a>
  <a href="https://github.com/skadaai/caskada">
    <img src="https://img.shields.io/github/stars/skadaai/caskada?logo=github&style=flat-square" alt="Repositorio de GitHub">
  </a>
  <a href="https://github.com/sponsors/zvictor">
    <img src="https://img.shields.io/github/sponsors/zvictor?logo=github&style=flat-square" alt="Patrocinadores de GitHub">
  </a>
</p>

Caskada es un framework que habilita la _Programación Agéntica_ mediante potentes abstracciones.

Proporciona una interfaz sencilla para construir aplicaciones complejas de IA basadas en _grafos dirigidos anidados_ con estado compartido.
Permite que tanto humanos como asistentes de IA colaboren eficazmente en el diseño e implementación de sistemas de IA.

## Características

- **Fácil de usar 🧠**: Intuitivo tanto para humanos como para asistentes de IA
- **Diseño minimalista ✨**: Abstracciones centrales en solo (¡sí, lo leíste bien!) 200 líneas de código
- **Libertad 🔓**: Sin bloat, dependencias ni vendor lock-in
- **Componible 🧩**: Construye sistemas complejos a partir de componentes simples y reutilizables
- **Potente 🦾**: Soporta todo lo que amas—([Multi-](https://skadaai.gitbook.io/caskada/design_pattern/multi_agent))[Agentes](https://skadaai.gitbook.io/caskada/design_pattern/agent), [Workflow](https://skadaai.gitbook.io/caskada/design_pattern/workflow), [RAG](https://skadaai.gitbook.io/caskada/design_pattern/rag), y más
- **Programación Agéntica 🤖**: Diseñado para desarrollo asistido por IA
- **Universal 🌈**: Funciona con cualquier proveedor de LLM o API
- **Políglota 🌍**: <!-- gitbook-ignore-start --><a href="https://pypi.org/project/caskada"><img src="https://github.com/skadaai/caskada/raw/main/.github/media/python.svg" width="16" height="16" alt="Logo de Python" style="vertical-align: middle; margin: 0 2px;"></a><!-- gitbook-ignore-end --> Python y <!-- gitbook-ignore-start --><a href="https://npmjs.com/packages/caskada"><img src="https://github.com/skadaai/caskada/raw/main/.github/media/typescript.svg" width="16" height="16" alt="Logo de Typescript" style="vertical-align: middle; margin: 0 2px;"></a><!-- gitbook-ignore-end --> Typescript son compatibles

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

<!-- gitbook-ignore-start -->

## Documentación

Nuestra documentación es inclusiva, adecuada tanto para mentes biológicas como sintéticas.<br />
Comienza seleccionando tu condición - o quizás _la que has sido condicionado a creer_:

\>> [Soy de Carbono 🐥](https://skadaai.gitbook.io/caskada/introduction/getting_started) <<

\>> [Soy de Silicio 🤖](https://flow.brainy.sh/docs.txt) <<

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

<!-- gitbook-ignore-end -->

## ¿Por qué Caskada?

Los frameworks actuales de LLM están hinchados... ¡En realidad solo necesitas 200 líneas para un framework robusto de LLM!

<div align="center">
  <img src="https://raw.githubusercontent.com/skadaai/caskada/main/.github/media/meme.jpg" width="500"/>

|                                                                                                                                                                                                                | **Abstracción** |                     **Wrappers Específicos de Aplicación**                      |                       **Wrappers Específicos de Proveedor**                       |                **Líneas**                 |                  **Tamaño**                   |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------: | :----------------------------------------------------------------: | :----------------------------------------------------------------------: | :--------------------------------------: | :-----------------------------------------: |
| LangChain                                                                                                                                                                                                      |  Agente, Cadena |      Muchos <br><sup><sub>(p.ej., QA, Resumen)</sub></sup>      |      Muchos <br><sup><sub>(p.ej., OpenAI, Pinecone, etc.)</sub></sup>       |                   405K                   |                   +166MB                    |
| CrewAI                                                                                                                                                                                                         |  Agente, Cadena | Muchos <br><sup><sub>(p.ej., FileReadTool, SerperDevTool)</sub></sup> | Muchos <br><sup><sub>(p.ej., OpenAI, Anthropic, Pinecone, etc.)</sub></sup> |                   18K                    |                   +173MB                    |
| SmolAgent                                                                                                                                                                                                      |      Agente      |   Algunos <br><sup><sub>(p.ej., CodeAgent, VisitWebTool)</sub></sup>   |  Algunos <br><sub>(p.ej., DuckDuckGo, Hugging Face, etc.)</sub></sup>   |                    8K                    |                   +198MB                    |
| LangGraph                                                                                                                                                                                                      |  Agente, Grafo   |       Algunos <br><sup><sub>(p.ej., Búsqueda Semántica)</sub></sup>       | Algunos <br><sup><sub>(p.ej., PostgresStore, SqliteSaver, etc.) </sub></sup> |                   37K                    |                    +51MB                    |
| AutoGen                                                                                                                                                                                                        |      Agente      |   Algunos <br><sup><sub>(p.ej., Agente de Herramientas, Agente de Chat)</sub></sup>    | Muchos <sup><sub>[Opcional]<br> (p.ej., OpenAI, Pinecone, etc.)</sub></sup> | 7K <br><sup><sub>(solo núcleo)</sub></sup> | +26MB <br><sup><sub>(solo núcleo)</sub></sup> |
| **Caskada** <!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/typescript.svg" width="16" height="16" alt="Logo de Typescript"><!-- gitbook-ignore-end -->.ts |    **Grafo**    |                              **Ninguno**                              |                                 **Ninguno**                                 |                 **300**                  |                 **pocos KB**                  |
| **Caskada** <!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/python.svg" width="16" height="16" alt="Logo de Python"><!-- gitbook-ignore-end -->.py         |    **Grafo**    |                              **Ninguno**                              |                                 **Ninguno**                                 |                 **200**                  |                 **pocos KB**                  |

</div>

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

## ¿Cómo funciona Caskada?

El archivo único en <a href="https://github.com/skadaai/caskada/blob/main/python/caskada.py"><!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/python.svg" width="16" height="16" alt="Logo de Python" style="vertical-align: middle; margin: 0 2px;"> <!-- gitbook-ignore-end -->Python</a> o <a href="https://github.com/skadaai/caskada/blob/main/typescript/caskada.ts"><!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/typescript.svg" width="16" height="16" alt="Logo de Typescript" style="vertical-align: middle; margin: 0 2px;"> <!-- gitbook-ignore-end -->Typescript</a> captura la abstracción central de los frameworks LLM: ¡Grafo!
<br>

<div align="center">
  <img src="https://raw.githubusercontent.com/skadaai/caskada/main/.github/media/abstraction.jpg" width="1300"/>
</div>
<br>

- [Nodo](https://skadaai.gitbook.io/caskada/core_abstraction/node) maneja tareas simples (LLM) con un ciclo de vida claro (`prep` → `exec` → `post`).
- [Flujo](https://skadaai.gitbook.io/caskada/core_abstraction/flow) conecta nodos mediante **Acciones** (bordes etiquetados), orquestando la ejecución.
- [Memoria](https://skadaai.gitbook.io/caskada/core_abstraction/memory) gestiona el estado compartido (`global`) y aislado (`local`), permitiendo la comunicación entre nodos.

A partir de ahí, es fácil implementar todos los patrones de diseño populares:
<br>

<div align="center">
  <img src="https://raw.githubusercontent.com/skadaai/caskada/main/.github/media/design.jpg" width="1300"/>
</div>
<br>

- [Agente](https://skadaai.gitbook.io/caskada/design_pattern/agent) toma decisiones de forma autónoma basadas en el contexto.
- [Workflow](https://skadaai.gitbook.io/caskada/design_pattern/workflow) encadena múltiples tareas en pipelines secuenciales.
- [RAG](https://skadaai.gitbook.io/caskada/design_pattern/rag) integra recuperación de datos con generación.
- [Map Reduce](https://skadaai.gitbook.io/caskada/design_pattern/mapreduce) divide tareas de datos en pasos de Map y Reduce.
- [Salida Estructurada](https://skadaai.gitbook.io/caskada/design_pattern/structure) formatea salidas de manera consistente.
- [Multi-Agentes](https://skadaai.gitbook.io/caskada/design_pattern/multi_agent) coordina múltiples agentes.

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

## Tutoriales

<div align="center">
  
|  Nombre  | Dificultad    |  Descripción  |  
| :-------------:  | :-------------: | :--------------------- |  
| [Chat](https://github.com/skadaai/caskada/tree/main/cookbook/python-chat) | ☆☆☆ <br> *Básico*   | Un bot de chat básico con historial de conversación |
| [RAG](https://github.com/skadaai/caskada/tree/main/cookbook/python-rag) | ☆☆☆ <br> *Básico*   | Un proceso simple de Generación Aumentada por Recuperación |
| [Workflow](https://github.com/skadaai/caskada/tree/main/cookbook/python-workflow) | ☆☆☆ <br> *Básico*   | Un flujo de trabajo de escritura que genera esquemas, escribe contenido y aplica estilos |
| [Map-Reduce](https://github.com/skadaai/caskada/tree/main/cookbook/python-map-reduce) | ☆☆☆ <br> *Básico* | Un procesador de cualificaciones de currículum usando el patrón map-reduce para evaluación por lotes |
| [Agente](https://github.com/skadaai/caskada/tree/main/cookbook/python-agent) | ☆☆☆ <br> *Básico*   | Un agente de investigación que puede buscar en la web y responder preguntas |
| [Streaming](https://github.com/skadaai/caskada/tree/main/cookbook/python-llm-streaming) | ☆☆☆ <br> *Básico*   | Una demo de streaming de LLM en tiempo real con capacidad de interrupción del usuario |
| [Multi-Agente](https://github.com/skadaai/caskada/tree/main/cookbook/python-multi-agent) | ★☆☆ <br> *Principiante* | Un juego de palabras Tabú para comunicación asíncrona entre dos agentes |
| [Supervisor](https://github.com/skadaai/caskada/tree/main/cookbook/python-supervisor) | ★☆☆ <br> *Principiante* | El agente de investigación se vuelve poco fiable... Construyamos un proceso de supervisión|
| [Paralelo](https://github.com/skadaai/caskada/tree/main/cookbook/python-parallel-batch) | ★☆☆ <br> *Principiante*   | Una demo de ejecución paralela que muestra una aceleración de 3x |
| [Razonamiento](https://github.com/skadaai/caskada/tree/main/cookbook/python-thinking) | ★☆☆ <br> *Principiante*   | Resuelve problemas complejos de razonamiento mediante Cadena de Pensamiento |
| [Memoria](https://github.com/skadaai/caskada/tree/main/cookbook/python-chat-memory) | ★☆☆ <br> *Principiante* | Un bot de chat con memoria a corto y largo plazo |

</div>

¡Y muchos más disponibles para todos los niveles! [¡Míralos todos!](https://github.com/skadaai/caskada/tree/main/cookbook)

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

## Comenzando Rápido

¿Nuevo en Caskada? Consulta nuestra guía [Comenzando](https://skadaai.gitbook.io/caskada/introduction/getting_started) para construir tu primer flujo en poco tiempo.

## ¿Listo para Construir Aplicaciones de Auto-Codificación?

Mira la [Guía de Programación Agéntica](https://skadaai.gitbook.io/caskada/guides/agentic_coding), ¡la forma más rápida de desarrollar proyectos LLM de auto-codificación con Caskada!

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

## Agradecimientos

Queremos extender nuestro más profundo agradecimiento a los creadores y contribuyentes del framework PocketFlow, del cual Caskada se originó como un fork.

## Descargo de Responsabilidad

Caskada se proporciona "tal cual" sin garantías ni garantías.  
No nos hacemos responsables del uso que se le dé a la salida generada, incluyendo pero no limitándose a su precisión, legalidad o cualquier consecuencia potencial derivada de su uso.

## Patrocinadores

<p align="center">
  <a style="color: inherit" href="https://github.com/sponsors/zvictor?utm_source=caskada&utm_medium=sponsorship&utm_campaign=caskada&utm_id=caskada">
    <img width="150" src="https://cdn.jsdelivr.net/gh/skadaai/caskada@main/.github/media/brain.png" alt="Logo de Caskada" />
  </a><br /><br />
  ¡Caskada funciona con 200 líneas de código y tu generosidad! 💰<br />
    <a style="color: inherit" href="https://github.com/sponsors/zvictor?utm_source=caskada&utm_medium=sponsorship&utm_campaign=caskada&utm_id=caskada">
      Ayúdanos a entregar más IA con menos código (pero quizás más cafeína)
    </a> ☕<br /><br />
    <a style="color: inherit" href="https://github.com/sponsors/zvictor?utm_source=caskada&utm_medium=sponsorship&utm_campaign=caskada&utm_id=caskada">Tu apoyo</a> ayuda a mantenerlo minimalista, potente y libre de dependencias! 🚀
  </a>
</p>

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)