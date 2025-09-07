<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://cdn.jsdelivr.net/gh/skadaai/caskada@main/.github/media/logo-dark.png">
    <source media="(prefers-color-scheme: light)" srcset="https://cdn.jsdelivr.net/gh/skadaai/caskada@main/.github/media/logo-light.png">
    <img width="280" alt="Логотип Brainyflow" src="https://cdn.jsdelivr.net/gh/skadaai/caskada@main/.github/media/logo-light.png">
  </picture>
<p>

<p align="center">
  Радикально минималистичный каркас ИИ (всего <a href="https://github.com/skadaai/caskada/blob/main/python/brainyflow.py">200 строк на Python</a>! 🤯)

  <br />
  Создавайте мощные агенты ИИ с минимальным кодом и максимальной свободой.
  <br />
  <sub>Пусть агенты создают агентов без лишнего кода, зависимостей или привязки к поставщику 😮</sub>
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

BrainyFlow - это каркас, обеспечивающий _Agentic Coding_ с помощью мощных абстракций.

Он предоставляет простой интерфейс для создания сложных приложений ИИ на основе _вложенных направленных графов_ с общим состоянием.
Он позволяет как людям, так и помощникам ИИ эффективно сотрудничать в проектировании и реализации систем ИИ.

## Особенности

- **Простота 🧠**: Понятен как для людей, так и для помощников ИИ
- **Минималистичный дизайн ✨**: Основные абстракции всего в (_вы слышали это правильно!_) 200 строках кода
- **Свобода 🔓**: Нет лишнего кода, зависимостей или привязки к поставщику
- **Компонуемость 🧩**: Создавайте сложные системы из простых, повторно используемых компонентов
- **Мощный 🦾**: Поддерживает все, что вам нравится—([Multi-](https://brainy.gitbook.io/flow/design_pattern/multi_agent))[Агенты](https://brainy.gitbook.io/flow/design_pattern/agent), [Рабочий процесс](https://brainy.gitbook.io/flow/design_pattern/workflow), [RAG](https://brainy.gitbook.io/flow/design_pattern/rag) и многое другое
- **Agentic-Coding 🤖**: Разработан для разработки с помощью ИИ
- **Универсальный 🌈**: Работает с любым поставщиком LLM или API
- **Полиглот 🌍**: <!-- gitbook-ignore-start --><a href="https://pypi.org/project/brainyflow"><img src="https://github.com/skadaai/caskada/raw/main/.github/media/python.svg" width="16" height="16" alt="Логотип Python" style="vertical-align: middle; margin: 0 2px;"></a><!-- gitbook-ignore-end --> Python и <!-- gitbook-ignore-start --><a href="https://npmjs.com/packages/brainyflow"><img src="https://github.com/skadaai/caskada/raw/main/.github/media/typescript.svg" width="16" height="16" alt="Логотип Typescript" style="vertical-align: middle; margin: 0 2px;"></a><!-- gitbook-ignore-end --> Typescript поддерживаются

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

<!-- gitbook-ignore-start -->

## Документация

Наша документация инклюзивна, подходит как для биологических, так и для синтетических умов.<br />
Начните с выбора вашего состояния - или, возможно, _того, которое вам внушили_:

\>> [Я основан на углероде 🐥](https://brainy.gitbook.io/flow/introduction/getting_started) <<

\>> [Я основан на кремнии 🤖](https://flow.brainy.sh/docs.txt) <<

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

<!-- gitbook-ignore-end -->

## Почему Brainy Flow?

Текущие каркасы LLM перегружены... Вам на самом деле нужно всего 200 строк для прочного каркаса LLM!

<div align="center">
  <img src="https://raw.githubusercontent.com/skadaai/caskada/main/.github/media/meme.jpg" width="500"/>

|                                                                                                                                                                                                                | **Абстракция** |                     **Обертки, специфичные для приложения**                      |                       **Обертки, специфичные для поставщика**                       |                **Строки**                 |                  **Размер**                   |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------: | :----------------------------------------------------------------: | :----------------------------------------------------------------------: | :--------------------------------------: | :-----------------------------------------: |
| LangChain                                                                                                                                                                                                      |  Агент, Цепь   |      Многие <br><sup><sub>(например, QA, Summarization)</sub></sup>      |      Многие <br><sup><sub>(например, OpenAI, Pinecone и т. д.)</sub></sup>       |                   405K                   |                   +166MB                    |
| CrewAI                                                                                                                                                                                                         |  Агент, Цепь   | Многие <br><sup><sub>(например, FileReadTool, SerperDevTool)</sub></sup> | Многие <br><sup><sub>(например, OpenAI, Anthropic, Pinecone и т. д.)</sub></sup> |                   18K                    |                   +173MB                    |
| SmolAgent                                                                                                                                                                                                      |      Агент      |   Некоторые <br><sup><sub>(например, CodeAgent, VisitWebTool)</sub></sup>   |  Некоторые <br><sup><sub>(например, DuckDuckGo, Hugging Face и т. д.)</sub></sup>   |                    8K                    |                   +198MB                    |
| LangGraph                                                                                                                                                                                                      |  Агент, Граф   |       Некоторые <br><sup><sub>(например, Semantic Search)</sub></sup>       | Некоторые <br><sup><sub>(например, PostgresStore, SqliteSaver и т. д.) </sub></sup> |                   37K                    |                    +51MB                    |
| AutoGen                                                                                                                                                                                                        |      Агент      |   Некоторые <br><sup><sub>(например, Tool Agent, Chat Agent)</sub></sup>    | Многие <sup><sub>[Необязательно]<br> (например, OpenAI, Pinecone и т. д.)</sub></sup> | 7K <br><sup><sub>(только ядро)</sub></sup> | +26MB <br><sup><sub>(только ядро)</sub></sup> |
| **BrainyFlow** <!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/typescript.svg" width="16" height="16" alt="Логотип Typescript"><!-- gitbook-ignore-end -->.ts |    **Граф**    |                              **Нет**                              |                                 **Нет**                                 |                 **300**                  |                 **несколько КБ**                  |
| **BrainyFlow** <!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/python.svg" width="16" height="16" alt="Логотип Python"><!-- gitbook-ignore-end -->.py         |    **Граф**    |                              **Нет**                              |                                 **Нет**                                 |                 **200**                  |                 **несколько КБ**                  |

</div>

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

## Как работает BrainyFlow?

Один файл в <a href="https://github.com/skadaai/caskada/blob/main/python/brainyflow.py"><!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/python.svg" width="16" height="16" alt="Логотип Python" style="vertical-align: middle; margin: 0 2px;"> <!-- gitbook-ignore-end -->Python</a> или <a href="https://github.com/skadaai/caskada/blob/main/typescript/brainyflow.ts"><!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/typescript.svg" width="16" height="16" alt="Логотип Typescript" style="vertical-align: middle; margin: 0 2px;"> <!-- gitbook-ignore-end -->Typescript</a> содержит основную абстракцию каркасов LLM: Граф!
<br>

<div align="center">
  <img src="https://raw.githubusercontent.com/skadaai/caskada/main/.github/media/abstraction.jpg" width="1300"/>
</div>
<br>

- [Узел](https://brainy.gitbook.io/flow/core_abstraction/node) обрабатывает простые (LLM) задачи с четким жизненным циклом (`prep` → `exec` → `post`).
- [Поток](https://brainy.gitbook.io/flow/core_abstraction/flow) соединяет узлы через **Действия** (помеченные ребра), координируя выполнение.
- [Память](https://brainy.gitbook.io/flow/core_abstraction/memory) управляет общим (`глобальным`) и изолированным (`локальным`) состоянием, обеспечивая связь между узлами.

Отсюда легко реализовать все популярные шаблоны проектирования:
<br>

<div align="center">
  <img src="https://raw.githubusercontent.com/skadaai/caskada/main/.github/media/design.jpg" width="1300"/>
</div>
<br>

- [Агент](https://brainy.gitbook.io/flow/design_pattern/agent) автономно принимает решения на основе контекста.
- [Рабочий процесс](https://brainy.gitbook.io/flow/design_pattern/workflow) связывает несколько задач в последовательные конвейеры.
- [RAG](https://brainy.gitbook.io/flow/design_pattern/rag) интегрирует извлечение данных с генерацией.
- [Map Reduce](https://brainy.gitbook.io/flow/design_pattern/mapreduce) разделяет задачи данных на этапы Map и Reduce.
- [Структурированный вывод](https://brainy.gitbook.io/flow/design_pattern/structure) форматирует выводы последовательно.
- [Несколько агентов](https://brainy.gitbook.io/flow/design_pattern/multi_agent) координирует несколько агентов.

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

## Уроки

<div align="center">
  
|  Название  | Сложность    |  Описание  |  
| :-------------:  | :-------------: | :--------------------- |  
| [Чат](https://github.com/skadaai/caskada/tree/main/cookbook/python-chat) | ☆☆☆ <br> *Простой*   | Базовый чат-бот с историей разговоров |
| [RAG](https://github.com/skadaai/caskada/tree/main/cookbook/python-rag) | ☆☆☆ <br> *Простой*   | Простой процесс генерации с извлечением |
| [Рабочий процесс](https://github.com/skadaai/caskada/tree/main/cookbook/python-workflow) | ☆☆☆ <br> *Простой*   | Рабочий процесс написания, который вычерчивает, пишет контент и применяет стили |
| [Map-Reduce](https://github.com/skadaai/caskada/tree/main/cookbook/python-map-reduce) | ☆☆☆ <br> *Простой* | Процессор квалификации резюме с использованием шаблона map-reduce для пакетной оценки |
| [Агент](https://github.com/skadaai/caskada/tree/main/cookbook/python-agent) | ☆☆☆ <br> *Простой*   | Исследовательский агент, который может искать в Интернете и отвечать на вопросы |
| [Потоковое вещание](https://github.com/skadaai/caskada/tree/main/cookbook/python-llm-streaming) | ☆☆☆ <br> *Простой*   | Демонстрация потокового вещания LLM в реальном времени с возможностью прерывания пользователем |
| [Несколько агентов](https://github.com/skadaai/caskada/tree/main/cookbook/python-multi-agent) | ★☆☆ <br> *Начинающий* | Игра в "Табу" для асинхронного общения между двумя агентами |
| [Супервайзер](https://github.com/skadaai/caskada/tree/main/cookbook/python-supervisor) | ★☆☆ <br> *Начинающий* | Исследовательский агент становится ненадежным... Давайте построим процесс надзора|
| [Параллельный](https://github.com/skadaai/caskada/tree/main/cookbook/python-parallel-batch) | ★☆☆ <br> *Начинающий*   | Демонстрация параллельного выполнения, показывающая 3-кратное ускорение |
| [Мышление](https://github.com/skadaai/caskada/tree/main/cookbook/python-thinking) | ★☆☆ <br> *Начинающий*   | Решение сложных задач рассуждения через цепочку рассуждений |
| [Память](https://github.com/skadaai/caskada/tree/main/cookbook/python-chat-memory) | ★☆☆ <br> *Начинающий* | Чат-бот с краткосрочной и долгосрочной памятью |

</div>

И многие другие доступны для всех уровней! [Проверьте их все!](https://github.com/skadaai/caskada/tree/main/cookbook)

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

## Быстрый старт

Новичок в BrainyFlow? Ознакомьтесь с нашим [Руководством по началу работы](https://brainy.gitbook.io/flow/introduction/getting_started), чтобы создать свой первый поток в считанные минуты.

## Готовы построить самокодирующиеся приложения?

Проверьте [Руководство по Agentic Coding](https://brainy.gitbook.io/flow/guides/agentic_coding), самый быстрый способ разработать самокодирующиеся проекты LLM с BrainyFlow!

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

## Благодарность

Мы хотели бы выразить свою глубочайшую благодарность создателям и участникам каркаса PocketFlow, от которого BrainyFlow произошел как форк.

## Нужны участники!

Мы ищем участников для всех аспектов проекта. Будь то документация, тестирование или реализация функций, мы будем рады вашей помощи!

Присоединяйтесь к нам на сервере Discord!

## Отказ от ответственности

BrainyFlow предоставляется "как есть" без каких-либо гарантий или обязательств.  
Мы не несем ответственности за то, как используется сгенерированный вывод, включая, но не ограничиваясь, его точность, законность или любые потенциальные последствия, возникающие в результате его использования.

## Спонсоры

<p align="center">
  <a style="color: inherit" href="https://github.com/sponsors/zvictor?utm_source=brainyflow&utm_medium=sponsorship&utm_campaign=brainyflow&utm_id=brainyflow">
    <img width="150" src="https://cdn.jsdelivr.net/gh/skadaai/caskada@main/.github/media/brain.png" alt="Логотип Brainyflow" />
  </a><br /><br />
  BrainyFlow работает на 200 строках кода и вашей щедрости! 💰<br />
    <a style="color: inherit" href="https://github.com/sponsors/zvictor?utm_source=brainyflow&utm_medium=sponsorship&utm_campaign=brainyflow&utm_id=brainyflow">
      Помогите нам доставлять больше ИИ с меньшим количеством кода (но, может быть, больше кофеина)
    </a> ☕<br /><br />
    <a style="color: inherit" href="https://github.com/sponsors/zvictor?utm_source=brainyflow&utm_medium=sponsorship&utm_campaign=brainyflow&utm_id=brainyflow">Ваша поддержка</a> помогает держать его минимальным, мощным и свободным от зависимостей! 🚀
  </a>
</p>

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)