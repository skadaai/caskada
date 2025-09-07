<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://cdn.jsdelivr.net/gh/skadaai/caskada@main/.github/media/logo-dark.png">
    <source media="(prefers-color-scheme: light)" srcset="https://cdn.jsdelivr.net/gh/skadaai/caskada@main/.github/media/logo-light.png">
    <img width="280" alt="Логотип Brainyflow" src="https://cdn.jsdelivr.net/gh/skadaai/caskada@main/.github/media/logo-light.png">
  </picture>
<p>

<p align="center">
  Радикально минималистичный фреймворк для ИИ (всего <a href="https://github.com/skadaai/caskada/blob/main/python/brainyflow.py">200 строк на Python</a>! 🤯)

  <br />
  Создавайте мощных ИИ-агентов с минимальным кодом и максимальной свободой.
  <br />
  <sub>Позвольте агентам создавать агентов без лишнего кода, зависимостей или привязки к вендору 😮</sub>
</p>

<p align="center">

  <a href="https://pypi.org/project/brainyflow">
   <img src="https://img.shields.io/pypi/dw/brainyflow?logo=python&label=Python&style=flat-square" alt="версия python">
  </a>
  <a href="https://npmjs.com/packages/brainyflow">
   <img src="https://img.shields.io/npm/d18m/brainyflow?logo=typescript&label=Typescript&style=flat-square" alt="версия typescript">
  </a>
  <a href="https://discord.gg/N9mVvxRXyH">
    <img src="https://img.shields.io/discord/1346833819172601907?logo=discord&style=flat-square" alt="Discord">
  </a>
  <a href="https://github.com/skadaai/caskada">
    <img src="https://img.shields.io/github/stars/skadaai/caskada?logo=github&style=flat-square" alt="Репозиторий GitHub">
  </a>
  <a href="https://github.com/sponsors/zvictor">
    <img src="https://img.shields.io/github/sponsors/zvictor?logo=github&style=flat-square" alt="Спонсоры GitHub">
  </a>
</p>

BrainyFlow — это фреймворк, позволяющий создавать _агентное программирование_ через мощные абстракции.

Он предоставляет простой интерфейс для построения сложных ИИ-приложений на основе _вложенных направленных графов_ с общим состоянием.
Он позволяет как людям, так и ИИ-ассистентам эффективно сотрудничать в проектировании и разработке ИИ-систем.

## Возможности

- **Простота 🧠**: Интуитивно понятен как для людей, так и для ИИ-ассистентов
- **Минималистичный дизайн ✨**: Основные абстракции всего в (_вы не ослышались!_) 200 строках кода
- **Свобода 🔓**: Ничего лишнего, никаких зависимостей или привязки к вендору
- **Компонуемость 🧩**: Создавайте сложные системы из простых, переиспользуемых компонентов
- **Мощь 🦾**: Поддерживает всё, что вам нравится — ([Мульти-](https://brainy.gitbook.io/flow/design_pattern/multi_agent))[Агенты](https://brainy.gitbook.io/flow/design_pattern/agent), [Рабочие процессы](https://brainy.gitbook.io/flow/design_pattern/workflow), [RAG](https://brainy.gitbook.io/flow/design_pattern/rag) и многое другое
- **Агентное программирование 🤖**: Создан для разработки с помощью ИИ
- **Универсальность 🌈**: Работает с любым провайдером LLM или API
- **Полиглот 🌍**: <!-- gitbook-ignore-start --><a href="https://pypi.org/project/brainyflow"><img src="https://github.com/skadaai/caskada/raw/main/.github/media/python.svg" width="16" height="16" alt="Логотип Python" style="vertical-align: middle; margin: 0 2px;"></a><!-- gitbook-ignore-end --> Python и <!-- gitbook-ignore-start --><a href="https://npmjs.com/packages/brainyflow"><img src="https://github.com/skadaai/caskada/raw/main/.github/media/typescript.svg" width="16" height="16" alt="Логотип Typescript" style="vertical-align: middle; margin: 0 2px;"></a><!-- gitbook-ignore-end --> Typescript поддерживаются

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

<!-- gitbook-ignore-start -->

## Документация

Наша документация инклюзивна и подходит как для биологических, так и для искусственных умов.<br />
Начните с выбора вашего состояния — или, возможно, _того, в которое вас запрограммировали верить_:

\>> [Я углеродный 🐥](https://brainy.gitbook.io/flow/introduction/getting_started) <<

\>> [Я кремниевый 🤖](https://flow.brainy.sh/docs.txt) <<

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

<!-- gitbook-ignore-end -->

## Почему Brainy Flow?

Современные фреймворки для LLM слишком раздуты... Вам на самом деле нужно всего 200 строк для надежного фреймворка LLM!

<div align="center">
  <img src="https://raw.githubusercontent.com/skadaai/caskada/main/.github/media/meme.jpg" width="500"/>

|                                                                                                                                                                                                                | **Абстракция** |                     **Специфичные обёртки**                      |                       **Вендор-специфичные обёртки**                       |                **Строки**                 |                  **Размер**                   |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------: | :----------------------------------------------------------------: | :----------------------------------------------------------------------: | :--------------------------------------: | :-----------------------------------------: |
| LangChain                                                                                                                                                                                                      |  Агент, Цепь   |      Много <br><sup><sub>(например, QA, суммаризация)</sub></sup>      |      Много <br><sup><sub>(например, OpenAI, Pinecone и др.)</sub></sup>       |                   405K                   |                   +166MB                    |
| CrewAI                                                                                                                                                                                                         |  Агент, Цепь   | Много <br><sup><sub>(например, FileReadTool, SerperDevTool)</sub></sup> | Много <br><sup><sub>(например, OpenAI, Anthropic, Pinecone и др.)</sub></sup> |                   18K                    |                   +173MB                    |
| SmolAgent                                                                                                                                                                                                      |      Агент      |   Некоторые <br><sup><sub>(например, CodeAgent, VisitWebTool)</sub></sup>   |  Некоторые <br><sup><sub>(например, DuckDuckGo, Hugging Face и др.)</sub></sup>   |                    8K                    |                   +198MB                    |
| LangGraph                                                                                                                                                                                                      |  Агент, Граф   |       Некоторые <br><sup><sub>(например, семантический поиск)</sub></sup>       | Некоторые <br><sup><sub>(например, PostgresStore, SqliteSaver и др.) </sub></sup> |                   37K                    |                    +51MB                    |
| AutoGen                                                                                                                                                                                                        |      Агент      |   Некоторые <br><sup><sub>(например, Tool Agent, Chat Agent)</sub></sup>    | Много <sup><sub>[Опционально]<br> (например, OpenAI, Pinecone и др.)</sub></sup> | 7K <br><sup><sub>(только ядро)</sub></sup> | +26MB <br><sup><sub>(только ядро)</sub></sup> |
| **BrainyFlow** <!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/typescript.svg" width="16" height="16" alt="Логотип Typescript"><!-- gitbook-ignore-end -->.ts |    **Граф**    |                              **Нет**                              |                                 **Нет**                                 |                 **300**                  |                 **несколько KB**                  |
| **BrainyFlow** <!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/python.svg" width="16" height="16" alt="Логотип Python"><!-- gitbook-ignore-end -->.py         |    **Граф**    |                              **Нет**                              |                                 **Нет**                                 |                 **200**                  |                 **несколько KB**                  |

</div>

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

## Как работает BrainyFlow?

Единственный файл в <a href="https://github.com/skadaai/caskada/blob/main/python/brainyflow.py"><!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/python.svg" width="16" height="16" alt="Логотип Python" style="vertical-align: middle; margin: 0 2px;"> <!-- gitbook-ignore-end -->Python</a> или <a href="https://github.com/skadaai/caskada/blob/main/typescript/brainyflow.ts"><!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/typescript.svg" width="16" height="16" alt="Логотип Typescript" style="vertical-align: middle; margin: 0 2px;"> <!-- gitbook-ignore-end -->Typescript</a> содержит основную абстракцию фреймворков LLM: Граф!
<br>

<div align="center">
  <img src="https://raw.githubusercontent.com/skadaai/caskada/main/.github/media/abstraction.jpg" width="1300"/>
</div>
<br>

- [Узел](https://brainy.gitbook.io/flow/core_abstraction/node) обрабатывает простые (LLM) задачи с четким жизненным циклом (`prep` → `exec` → `post`).
- [Поток](https://brainy.gitbook.io/flow/core_abstraction/flow) соединяет узлы через **Действия** (помеченные рёбра), управляя выполнением.
- [Память](https://brainy.gitbook.io/flow/core_abstraction/memory) управляет общим (`global`) и изолированным (`local`) состоянием, обеспечивая коммуникацию между узлами.

Отсюда легко реализовать все популярные паттерны:
<br>

<div align="center">
  <img src="https://raw.githubusercontent.com/skadaai/caskada/main/.github/media/design.jpg" width="1300"/>
</div>
<br>

- [Агент](https://brainy.gitbook.io/flow/design_pattern/agent) автономно принимает решения на основе контекста.
- [Рабочий процесс](https://brainy.gitbook.io/flow/design_pattern/workflow) объединяет несколько задач в последовательные цепочки.
- [RAG](https://brainy.gitbook.io/flow/design_pattern/rag) интегрирует поиск данных с генерацией.
- [Map Reduce](https://brainy.gitbook.io/flow/design_pattern/mapreduce) разделяет задачи данных на этапы Map и Reduce.
- [Структурированный вывод](https://brainy.gitbook.io/flow/design_pattern/structure) обеспечивает единообразное форматирование результатов.
- [Мульти-Агенты](https://brainy.gitbook.io/flow/design_pattern/multi_agent) координируют работу нескольких агентов.

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

## Руководства

<div align="center">
  
|  Название  | Сложность    |  Описание  |  
| :-------------:  | :-------------: | :--------------------- |  
| [Чат](https://github.com/skadaai/caskada/tree/main/cookbook/python-chat) | ☆☆☆ <br> *Просто*   | Простой чат-бот с историей диалога |
| [RAG](https://github.com/skadaai/caskada/tree/main/cookbook/python-rag) | ☆☆☆ <br> *Просто*   | Простой процесс генерации с дополненным поиском |
| [Рабочий процесс](https://github.com/skadaai/caskada/tree/main/cookbook/python-workflow) | ☆☆☆ <br> *Просто*   | Процесс написания, включающий создание плана, написание и стилизацию |
| [Map-Reduce](https://github.com/skadaai/caskada/tree/main/cookbook/python-map-reduce) | ☆☆☆ <br> *Просто* | Обработка резюме с использованием паттерна map-reduce для пакетной оценки |
| [Агент](https://github.com/skadaai/caskada/tree/main/cookbook/python-agent) | ☆☆☆ <br> *Просто*   | Исследовательский агент, который может искать в интернете и отвечать на вопросы |
| [Потоковая передача](https://github.com/skadaai/caskada/tree/main/cookbook/python-llm-streaming) | ☆☆☆ <br> *Просто*   | Демонстрация потоковой передачи LLM в реальном времени с возможностью прерывания |
| [Мульти-Агент](https://github.com/skadaai/caskada/tree/main/cookbook/python-multi-agent) | ★☆☆ <br> *Новичок* | Игра в табу для асинхронной коммуникации между двумя агентами |
| [Супервизор](https://github.com/skadaai/caskada/tree/main/cookbook/python-supervisor) | ★☆☆ <br> *Новичок* | Исследовательский агент становится ненадежным... Давайте создадим процесс контроля |
| [Параллельное выполнение](https://github.com/skadaai/caskada/tree/main/cookbook/python-parallel-batch) | ★☆☆ <br> *Новичок*   | Демонстрация параллельного выполнения с трёхкратным ускорением |
| [Мышление](https://github.com/skadaai/caskada/tree/main/cookbook/python-thinking) | ★☆☆ <br> *Новичок*   | Решение сложных задач с помощью "цепочки мыслей" |
| [Память](https://github.com/skadaai/caskada/tree/main/cookbook/python-chat-memory) | ★☆☆ <br> *Новичок* | Чат-бот с краткосрочной и долгосрочной памятью |

</div>

И многие другие для всех уровней! [Посмотрите их все!](https://github.com/skadaai/caskada/tree/main/cookbook)

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

## Быстрый старт

Новичок в BrainyFlow? Ознакомьтесь с нашим руководством [Начало работы](https://brainy.gitbook.io/flow/introduction/getting_started), чтобы создать свой первый поток в кратчайшие сроки.

## Готовы создать само-кодирующие приложения?

Ознакомьтесь с [Руководством по агентному программированию](https://brainy.gitbook.io/flow/guides/agentic_coding), самым быстрым способом разработки само-кодирующих LLM-проектов с BrainyFlow!

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

## Благодарности

Мы хотели бы выразить глубочайшую благодарность создателям и участникам фреймворка PocketFlow, из которого BrainyFlow появился как форк.

## Отказ от ответственности

BrainyFlow предоставляется «как есть» без каких-либо гарантий.  
Мы не несем ответственности за использование сгенерированного вывода, включая, помимо прочего, его точность, законность или любые возможные последствия, возникшие в результате его использования.

## Спонсоры

<p align="center">
  <a style="color: inherit" href="https://github.com/sponsors/zvictor?utm_source=brainyflow&utm_medium=sponsorship&utm_campaign=brainyflow&utm_id=brainyflow">
    <img width="150" src="https://cdn.jsdelivr.net/gh/skadaai/caskada@main/.github/media/brain.png" alt="Логотип Brainyflow" />
  </a><br /><br />
  BrainyFlow работает на 200 строках кода и вашей щедрости! 💰<br />
    <a style="color: inherit" href="https://github.com/sponsors/zvictor?utm_source=brainyflow&utm_medium=sponsorship&utm_campaign=brainyflow&utm_id=brainyflow">
      Помогите нам делать больше ИИ с меньшим кодом (но, возможно, большим количеством кофе)
    </a> ☕<br /><br />
    <a style="color: inherit" href="https://github.com/sponsors/zvictor?utm_source=brainyflow&utm_medium=sponsorship&utm_campaign=brainyflow&utm_id=brainyflow">Ваша поддержка</a> помогает оставаться минималистичным, мощным и свободным от зависимостей! 🚀
  </a>
</p>

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)