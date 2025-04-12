<div align="center">
  <img src="https://github.com/zvictor/BrainyFlow/raw/main/.github/media/banner-light.jpg" width="600"/>
</div>

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
[![Docs](https://img.shields.io/badge/docs-latest-blue)](https://brainy.gitbook.io/flow/)
<a href="https://discord.gg/MdJJ29Xd">
<img src="https://img.shields.io/discord/1346833819172601907?logo=discord&style=flat">
</a>

BrainyFlow — это минималистичный фреймворк для LLM, состоящий всего из [100 строк](https://github.com/zvictor/BrainyFlow/blob/main/python/__init__.py)

- **Легкий**: Всего 100 строк. Никакого избыточного кода, никаких зависимостей, никакой привязки к поставщикам.
- **Выразительный**: Всё, что вы любите — ([Мульти-](https://brainy.gitbook.io/flow/design_pattern/multi_agent))[Агенты](https://brainy.gitbook.io/flow/design_pattern/agent), [Рабочие процессы](https://brainy.gitbook.io/flow/design_pattern/workflow), [RAG](https://brainy.gitbook.io/flow/design_pattern/rag) и многое другое.

- **[Агентное программирование](https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to)**: Позвольте ИИ-агентам (например, Cursor AI) создавать других агентов — повышение продуктивности в 10 раз!

- Для установки выполните `pip install brainyflow` или просто скопируйте [исходный код](https://github.com/zvictor/BrainyFlow/blob/main/python/__init__.py) (всего 100 строк).
- Чтобы узнать больше, ознакомьтесь с [документацией](https://brainy.gitbook.io/flow/). Чтобы понять мотивацию, прочитайте [историю создания](https://zacharyhuang.substack.com/p/i-built-an-llm-framework-in-just).
- 🎉 Присоединяйтесь к нашему [Discord-серверу](https://discord.gg/MdJJ29Xd)!

- 🎉 Благодаря [@zvictor](https://www.github.com/zvictor), [@jackylee941130](https://www.github.com/jackylee941130) и [@ZebraRoy](https://www.github.com/ZebraRoy), у нас теперь есть [версия на TypeScript](https://github.com/The-Pocket/PocketFlow-Typescript)!

## Почему BrainyFlow?

Текущие фреймворки для LLM перегружены... Для фреймворка LLM вам нужно всего 100 строк!

<div align="center">
  <img src="https://github.com/zvictor/brainyflow/raw/main/.github/media/meme.jpg" width="400"/>

|                | **Абстракция** |                **Специфичные обертки для приложений**                |                      **Специфичные обертки для вендоров**                       |               **Строк кода**               |                  **Размер**                   |
| -------------- | :------------: | :------------------------------------------------------------------: | :-----------------------------------------------------------------------------: | :----------------------------------------: | :-------------------------------------------: |
| LangChain      |  Agent, Chain  |      Много <br><sup><sub>(напр., QA, Summarization)</sub></sup>      |        Много <br><sup><sub>(напр., OpenAI, Pinecone и т.д.)</sub></sup>         |                    405K                    |                    +166MB                     |
| CrewAI         |  Agent, Chain  | Много <br><sup><sub>(напр., FileReadTool, SerperDevTool)</sub></sup> |   Много <br><sup><sub>(напр., OpenAI, Anthropic, Pinecone и т.д.)</sub></sup>   |                    18K                     |                    +173MB                     |
| SmolAgent      |     Agent      | Несколько <br><sup><sub>(напр., CodeAgent, VisitWebTool)</sub></sup> |  Несколько <br><sup><sub>(напр., DuckDuckGo, Hugging Face и т.д.)</sub></sup>   |                     8K                     |                    +198MB                     |
| LangGraph      |  Agent, Graph  |     Несколько <br><sup><sub>(напр., Semantic Search)</sub></sup>     | Несколько <br><sup><sub>(напр., PostgresStore, SqliteSaver и т.д.) </sub></sup> |                    37K                     |                     +51MB                     |
| AutoGen        |     Agent      | Несколько <br><sup><sub>(напр., Tool Agent, Chat Agent)</sub></sup>  | Много <sup><sub>[Опционально]<br> (напр., OpenAI, Pinecone и т.д.)</sub></sup>  | 7K <br><sup><sub>(только ядро)</sub></sup> | +26MB <br><sup><sub>(только ядро)</sub></sup> |
| **BrainyFlow** |   **Graph**    |                               **Нет**                                |                                     **Нет**                                     |                  **100**                   |                   **+56KB**                   |

</div>

## Как работает BrainyFlow?

[100 строк](https://github.com/zvictor/BrainyFlow/blob/main/python/__init__.py) охватывают основную абстракцию фреймворков LLM: Граф!
<br>

<div align="center">
  <img src="https://github.com/zvictor/brainyflow/raw/main/.github/media/abstraction.jpg" width="900"/>
</div>
<br>

Отсюда легко реализовать популярные шаблоны проектирования, такие как ([Мульти-](https://brainy.gitbook.io/flow/design_pattern/multi_agent))[Агенты](https://brainy.gitbook.io/flow/design_pattern/agent), [Рабочие процессы](https://brainy.gitbook.io/flow/design_pattern/workflow), [RAG](https://brainy.gitbook.io/flow/design_pattern/rag) и т.д.
<br>

<div align="center">
  <img src="https://github.com/zvictor/brainyflow/raw/main/.github/media/design.jpg" width="900"/>
</div>
<br>
✨ Ниже представлены базовые руководства:

<div align="center">
  
|  Название  | Сложность    |  Описание  |  
| :-------------:  | :-------------: | :--------------------- |  
| [Чат](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-chat) | ☆☆☆ <br> *Простейший*   | Базовый чат-бот с историей разговора |
| [Структурированный вывод](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-structured-output) | ☆☆☆ <br> *Простейший* | Извлечение структурированных данных из резюме с помощью промптов |
| [Рабочий процесс](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-workflow) | ☆☆☆ <br> *Простейший*   | Рабочий процесс создания текста, который составляет план, пишет контент и применяет стилистику |
| [Агент](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-agent) | ☆☆☆ <br> *Простейший*   | Исследовательский агент, который может искать в интернете и отвечать на вопросы |
| [RAG](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-rag) | ☆☆☆ <br> *Простейший*   | Простой процесс генерации с извлечением (Retrieval-augmented Generation) |
| [Map-Reduce](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-map-reduce) | ☆☆☆ <br> *Простейший* | Обработчик квалификаций резюме с использованием паттерна map-reduce для пакетной оценки |
| [Потоковая обработка](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-llm-streaming) | ☆☆☆ <br> *Простейший*   | Демонстрация потоковой обработки LLM в реальном времени с возможностью прерывания |
| [Ограничения чата](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-chat-guardrail) | ☆☆☆ <br> *Простейший*  | Чат-бот для путешествий, обрабатывающий только запросы, связанные с путешествиями |
| [Мульти-агент](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-multi-agent) | ★☆☆ <br> *Начальный* | Игра в Табу для асинхронного общения между двумя агентами |
| [Супервизор](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-supervisor) | ★☆☆ <br> *Начальный* | Исследовательский агент становится ненадежным... Построим процесс надзора |
| [Параллельное выполнение](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-parallel-batch) | ★☆☆ <br> *Начальный*   | Демонстрация параллельного выполнения с ускорением в 3 раза |
| [Параллельный поток](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-parallel-batch-flow) | ★☆☆ <br> *Начальный*   | Демонстрация параллельной обработки изображений с ускорением в 8 раз при использовании нескольких фильтров |
| [Голосование большинством](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-majority-vote) | ★☆☆ <br> *Начальный* | Повышение точности рассуждений путем объединения нескольких попыток решения |
| [Мышление](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-thinking) | ★☆☆ <br> *Начальный*   | Решение сложных задач рассуждения с помощью цепочки мыслей (Chain-of-Thought) |
| [Память](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-chat-memory) | ★☆☆ <br> *Начальный* | Чат-бот с краткосрочной и долгосрочной памятью |
| [MCP](https://github.com/zvictor/BrainyFlow/tree/main/cookbook/python-mcp) | ★☆☆ <br> *Начальный* | Агент с использованием протокола контекста модели (Model Context Protocol) для числовых операций |

</div>

👀 Хотите увидеть другие руководства для начинающих? [Создайте задачу!](https://github.com/zvictor/BrainyFlow/issues/new)

## Как использовать BrainyFlow?

🚀 Через **Агентное программирование** — самую быструю парадигму разработки LLM-приложений, где _люди проектируют_, а _агенты программируют_!

<br>
<div align="center">
  <a href="https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to" target="_blank">
    <img src="https://substackcdn.com/image/fetch/f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F423a39af-49e8-483b-bc5a-88cc764350c6_1050x588.png" width="700" alt="IMAGE ALT TEXT" style="cursor: pointer;">
  </a>
</div>
<br>

✨ Ниже представлены примеры более сложных LLM-приложений:

<div align="center">
  
|  Название приложения     |  Сложность    | Темы  | Дизайн от человека | Код от агента |
| :-------------:  | :-------------: | :---------------------: |  :---: |  :---: |
| [Создаем Cursor с помощью Cursor](https://github.com/The-Pocket/Tutorial-Cursor) <br> <sup><sub>Скоро достигнем сингулярности ...</sup></sub> | ★★★ <br> *Продвинутый*   | [Агент](https://brainy.gitbook.io/flow/design_pattern/agent) | [Дизайн-документ](https://github.com/The-Pocket/Tutorial-Cursor/blob/main/docs/design.md) | [Код потока](https://github.com/The-Pocket/Tutorial-Cursor/blob/main/flow.py)
| [Спроси AI Пола Грэма](https://github.com/The-Pocket/Tutorial-YC-Partner) <br> <sup><sub>Спроси AI Пола Грэма, если не попал в программу</sup></sub> | ★★☆ <br> *Средний*   | [RAG](https://brainy.gitbook.io/flow/design_pattern/rag) <br> [Map Reduce](https://brainy.gitbook.io/flow/design_pattern/mapreduce) <br> [TTS](https://brainy.gitbook.io/flow/utility_function/text_to_speech) | [Дизайн-документ](https://github.com/The-Pocket/Tutorial-AI-Paul-Graham/blob/main/docs/design.md) | [Код потока](https://github.com/The-Pocket/Tutorial-AI-Paul-Graham/blob/main/flow.py)
| [Youtube Summarizer](https://github.com/The-Pocket/Tutorial-Youtube-Made-Simple)  <br> <sup><sub> Объясняет YouTube-видео так, как будто вам 5 лет </sup></sub> | ★☆☆ <br> *Начальный*   | [Map Reduce](https://brainy.gitbook.io/flow/design_pattern/mapreduce) |  [Дизайн-документ](https://github.com/The-Pocket/Tutorial-Youtube-Made-Simple/blob/main/docs/design.md) | [Код потока](https://github.com/The-Pocket/Tutorial-Youtube-Made-Simple/blob/main/flow.py)
| [Генератор "холодных" открытий](https://github.com/The-Pocket/Tutorial-Cold-Email-Personalization)  <br> <sup><sub> Мгновенные ледоколы, превращающие холодные контакты в горячие </sup></sub> | ★☆☆ <br> *Начальный*   | [Map Reduce](https://brainy.gitbook.io/flow/design_pattern/mapreduce) <br> [Веб-поиск](https://brainy.gitbook.io/flow/utility_function/websearch) |  [Дизайн-документ](https://github.com/The-Pocket/Tutorial-Cold-Email-Personalization/blob/master/docs/design.md) | [Код потока](https://github.com/The-Pocket/Tutorial-Cold-Email-Personalization/blob/master/flow.py)

</div>

- Хотите изучить **Агентное программирование**?

  - Посмотрите [мой YouTube-канал](https://www.youtube.com/@ZacharyLLM?sub_confirmation=1) для видеоуроков о том, как были созданы некоторые вышеуказанные приложения!

  - Хотите создать свое собственное LLM-приложение? Прочитайте эту [статью](https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to)! Начните с [этого шаблона](https://github.com/The-Pocket/PocketFlow-Template-Python)!

  - Хотите узнать подробные шаги? Прочитайте это [Руководство](https://brainy.gitbook.io/flow/guide)!
