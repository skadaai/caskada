<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://cdn.jsdelivr.net/gh/skadaai/caskada@main/.github/media/logo-dark.png">
    <source media="(prefers-color-scheme: light)" srcset="https://cdn.jsdelivr.net/gh/skadaai/caskada@main/.github/media/logo-light.png">
    <img width="280" alt="Caskada 로고" src="https://cdn.jsdelivr.net/gh/skadaai/caskada@main/.github/media/logo-light.png">
  </picture>
<p>

<p align="center">
  혁신적으로 미니멀한 AI 프레임워크 (<a href="https://github.com/skadaai/caskada/blob/main/python/caskada.py">파이썬으로 단 200줄</a>! 🤯)

  <br />
  최소한의 코드와 최대한의 자유로 강력한 AI 에이전트를 구축하세요.
  <br />
  <sub>에이전트가 에이전트를 만들 수 있게 하세요. 불필요한 기능, 의존성, 벤더 종속성 없이 😮</sub>
</p>

<p align="center">

  <a href="https://pypi.org/project/caskada">
   <img src="https://img.shields.io/pypi/dw/caskada?logo=python&label=Python&style=flat-square" alt="python 버전">
  </a>
  <a href="https://npmjs.com/packages/caskada">
   <img src="https://img.shields.io/npm/d18m/caskada?logo=typescript&label=Typescript&style=flat-square" alt="typescript 버전">
  </a>
  <a href="https://discord.gg/N9mVvxRXyH">
    <img src="https://img.shields.io/discord/1346833819172601907?logo=discord&style=flat-square" alt="Discord">
  </a>
  <a href="https://github.com/skadaai/caskada">
    <img src="https://img.shields.io/github/stars/skadaai/caskada?logo=github&style=flat-square" alt="GitHub 저장소">
  </a>
  <a href="https://github.com/sponsors/zvictor">
    <img src="https://img.shields.io/github/sponsors/zvictor?logo=github&style=flat-square" alt="GitHub 스폰서">
  </a>
</p>

Caskada는 _에이전트 코딩_을 가능하게 하는 강력한 추상화를 제공하는 프레임워크입니다.

공유 상태를 가진 _중첩된 방향성 그래프_를 기반으로 복잡한 AI 애플리케이션을 구축하기 위한 간단한 인터페이스를 제공합니다.  
인간과 AI 어시스턴트가 효과적으로 협업하여 AI 시스템을 설계하고 구현할 수 있도록 합니다.

## 특징

- **뇌 친화적 🧠**: 인간과 AI 어시스턴트 모두에게 직관적
- **미니멀한 디자인 ✨**: 핵심 추상화가 단 (_들어보셨나요!_) 200줄의 코드로 구현
- **자유로움 🔓**: 불필요한 기능, 의존성, 벤더 종속성 없음
- **조합 가능 🧩**: 간단하고 재사용 가능한 컴포넌트로 복잡한 시스템 구축
- **강력함 🦾**: 여러분이 좋아하는 모든 것 지원—([멀티](https://skadaai.gitbook.io/caskada/design_pattern/multi_agent))[에이전트](https://skadaai.gitbook.io/caskada/design_pattern/agent), [워크플로우](https://skadaai.gitbook.io/caskada/design_pattern/workflow), [RAG](https://skadaai.gitbook.io/caskada/design_pattern/rag) 등
- **에이전트 코딩 🤖**: AI 지원 개발을 위해 설계
- **범용성 🌈**: 모든 LLM 제공자나 API와 호환
- **다언어 지원 🌍**: <!-- gitbook-ignore-start --><a href="https://pypi.org/project/caskada"><img src="https://github.com/skadaai/caskada/raw/main/.github/media/python.svg" width="16" height="16" alt="Python 로고" style="vertical-align: middle; margin: 0 2px;"></a><!-- gitbook-ignore-end --> 파이썬과 <!-- gitbook-ignore-start --><a href="https://npmjs.com/packages/caskada"><img src="https://github.com/skadaai/caskada/raw/main/.github/media/typescript.svg" width="16" height="16" alt="Typescript 로고" style="vertical-align: middle; margin: 0 2px;"></a><!-- gitbook-ignore-end --> 타입스크립트 모두 지원

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

<!-- gitbook-ignore-start -->

## 문서

우리의 문서는 생물학적 마음과 인공 마음 모두에게 적합합니다.<br />
여러분의 상태—아니면 _믿도록 조건화된 상태_—를 선택해 보세요:

\>> [나는 탄소 기반입니다 🐥](https://skadaai.gitbook.io/caskada/introduction/getting_started) <<

\>> [나는 실리콘 기반입니다 🤖](https://flow.brainy.sh/docs.txt) <<

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

<!-- gitbook-ignore-end -->

## 왜 Brainy Flow인가요?

현재 LLM 프레임워크들은 비대합니다... 사실 견고한 LLM 프레임워크를 만들려면 200줄만 있으면 됩니다!

<div align="center">
  <img src="https://raw.githubusercontent.com/skadaai/caskada/main/.github/media/meme.jpg" width="500"/>

|                                                                                                                                                                                                                | **추상화** |                     **앱 전용 래퍼**                      |                       **벤더 전용 래퍼**                       |                **코드 줄 수**                 |                  **크기**                   |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------: | :----------------------------------------------------------------: | :----------------------------------------------------------------------: | :--------------------------------------: | :-----------------------------------------: |
| LangChain                                                                                                                                                                                                      |  에이전트, 체인   |      많음 <br><sup><sub>(예: QA, 요약)</sub></sup>      |      많음 <br><sup><sub>(예: OpenAI, Pinecone 등)</sub></sup>       |                   405K                   |                   +166MB                    |
| CrewAI                                                                                                                                                                                                         |  에이전트, 체인   | 많음 <br><sup><sub>(예: FileReadTool, SerperDevTool)</sub></sup> | 많음 <br><sup><sub>(예: OpenAI, Anthropic, Pinecone 등)</sub></sup> |                   18K                    |                   +173MB                    |
| SmolAgent                                                                                                                                                                                                      |      에이전트      |   일부 <br><sup><sub>(예: CodeAgent, VisitWebTool)</sub></sup>   |  일부 <br><sup><sub>(예: DuckDuckGo, Hugging Face 등)</sub></sup>   |                    8K                    |                   +198MB                    |
| LangGraph                                                                                                                                                                                                      |  에이전트, 그래프   |       일부 <br><sup><sub>(예: 의미론적 검색)</sub></sup>       | 일부 <br><sup><sub>(예: PostgresStore, SqliteSaver 등) </sub></sup> |                   37K                    |                    +51MB                    |
| AutoGen                                                                                                                                                                                                        |      에이전트      |   일부 <br><sup><sub>(예: 도구 에이전트, 채팅 에이전트)</sub></sup>    | 많음 <sup><sub>[선택]<br> (예: OpenAI, Pinecone 등)</sub></sup> | 7K <br><sup><sub>(코어만)</sub></sup> | +26MB <br><sup><sub>(코어만)</sub></sup> |
| **Caskada** <!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/typescript.svg" width="16" height="16" alt="Typescript 로고"><!-- gitbook-ignore-end -->.ts |    **그래프**    |                              **없음**                              |                                 **없음**                                 |                 **300**                  |                 **몇 KB**                  |
| **Caskada** <!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/python.svg" width="16" height="16" alt="Python 로고"><!-- gitbook-ignore-end -->.py         |    **그래프**    |                              **없음**                              |                                 **없음**                                 |                 **200**                  |                 **몇 KB**                  |

</div>

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

## Caskada는 어떻게 동작하나요?

<a href="https://github.com/skadaai/caskada/blob/main/python/caskada.py"><!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/python.svg" width="16" height="16" alt="Python 로고" style="vertical-align: middle; margin: 0 2px;"> <!-- gitbook-ignore-end -->파이썬</a> 또는 <a href="https://github.com/skadaai/caskada/blob/main/typescript/caskada.ts"><!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/typescript.svg" width="16" height="16" alt="Typescript 로고" style="vertical-align: middle; margin: 0 2px;"> <!-- gitbook-ignore-end -->타입스크립트</a>의 단일 파일은 LLM 프레임워크의 핵심 추상화인 그래프를 담고 있습니다!
<br>

<div align="center">
  <img src="https://raw.githubusercontent.com/skadaai/caskada/main/.github/media/abstraction.jpg" width="1300"/>
</div>
<br>

- [노드](https://skadaai.gitbook.io/caskada/core_abstraction/node)는 명확한 라이프사이클(`prep` → `exec` → `post`)을 가지는 간단한 (LLM) 작업을 처리합니다.
- [플로우](https://skadaai.gitbook.io/caskada/core_abstraction/flow)는 **액션**(라벨이 있는 간선)을 통해 노드를 연결하고 실행을 조율합니다.
- [메모리](https://skadaai.gitbook.io/caskada/core_abstraction/memory)는 공유(`global`) 및 분리된(`local`) 상태를 관리하여 노드 간 통신을 가능하게 합니다.

여기서부터 인기 있는 모든 디자인 패턴을 쉽게 구현할 수 있습니다:
<br>

<div align="center">
  <img src="https://raw.githubusercontent.com/skadaai/caskada/main/.github/media/design.jpg" width="1300"/>
</div>
<br>

- [에이전트](https://skadaai.gitbook.io/caskada/design_pattern/agent)는 컨텍스트를 기반으로 자율적으로 결정을 내립니다.
- [워크플로우](https://skadaai.gitbook.io/caskada/design_pattern/workflow)는 여러 작업을 순차적인 파이프라인으로 연결합니다.
- [RAG](https://skadaai.gitbook.io/caskada/design_pattern/rag)는 데이터 검색과 생성을 통합합니다.
- [맵 리듀스](https://skadaai.gitbook.io/caskada/design_pattern/mapreduce)는 데이터 작업을 맵과 리듀스 단계로 분할합니다.
- [구조화된 출력](https://skadaai.gitbook.io/caskada/design_pattern/structure)은 출력을 일관되게 포맷팅합니다.
- [멀티 에이전트](https://skadaai.gitbook.io/caskada/design_pattern/multi_agent)는 여러 에이전트를 조율합니다.

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

## 튜토리얼

<div align="center">
  
|  이름  | 난이도    |  설명  |  
| :-------------:  | :-------------: | :--------------------- |  
| [채팅](https://github.com/skadaai/caskada/tree/main/cookbook/python-chat) | ☆☆☆ <br> *초급*   | 대화 기록이 있는 기본적인 챗봇 |
| [RAG](https://github.com/skadaai/caskada/tree/main/cookbook/python-rag) | ☆☆☆ <br> *초급*   | 간단한 검색-보강 생성 과정 |
| [워크플로우](https://github.com/skadaai/caskada/tree/main/cookbook/python-workflow) | ☆☆☆ <br> *초급*   | 개요 작성, 콘텐츠 작성, 스타일 적용을 포함하는 글쓰기 워크플로우 |
| [맵-리듀스](https://github.com/skadaai/caskada/tree/main/cookbook/python-map-reduce) | ☆☆☆ <br> *초급* | 일괄 평가를 위한 맵-리듀스 패턴을 사용한 이력서 자격 처리 |
| [에이전트](https://github.com/skadaai/caskada/tree/main/cookbook/python-agent) | ☆☆☆ <br> *초급*   | 웹을 검색하고 질문에 답할 수 있는 연구 에이전트 |
| [스트리밍](https://github.com/skadaai/caskada/tree/main/cookbook/python-llm-streaming) | ☆☆☆ <br> *초급*   | 사용자 중단 기능이 있는 실시간 LLM 스트리밍 데모 |
| [멀티 에이전트](https://github.com/skadaai/caskada/tree/main/cookbook/python-multi-agent) | ★☆☆ <br> *중급* | 두 에이전트 간의 비동기 통신을 위한 금지어 게임 |
| [감독자](https://github.com/skadaai/caskada/tree/main/cookbook/python-supervisor) | ★☆☆ <br> *중급* | 연구 에이전트가 신뢰할 수 없어지면... 감독 프로세스를 구축해 보세요|
| [병렬](https://github.com/skadaai/caskada/tree/main/cookbook/python-parallel-batch) | ★☆☆ <br> *중급*   | 3배 빠른 속도 향상을 보여주는 병렬 실행 데모 |
| [사고](https://github.com/skadaai/caskada/tree/main/cookbook/python-thinking) | ★☆☆ <br> *중급*   | 사고의 연쇄를 통해 복잡한 추론 문제 해결 |
| [메모리](https://github.com/skadaai/caskada/tree/main/cookbook/python-chat-memory) | ★☆☆ <br> *중급* | 단기 및 장기 메모리가 있는 챗봇 |

</div>

더 많은 튜토리얼이 모든 수준에 맞게 준비되어 있습니다! [전체 확인하기!](https://github.com/skadaai/caskada/tree/main/cookbook)

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

<!-- ## Brainy Flow 사용 방법

🚀 **에이전트 코딩**을 통해—_사람이 설계_하고 _에이전트가 코드를 작성_하는 가장 빠른 LLM 앱 개발 패러다임입니다!

<br />

- **에이전트 코딩**을 배우고 싶나요?
  - 설정 방법은 이 [포스트](https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to)를 읽어보세요!
  - [내 YouTube](https://www.youtube.com/@ZacharyLLM?sub_confirmation=1)를 확인하세요! 이 [가이드](https://skadaai.gitbook.io/caskada/guides/agentic_coding)를 읽어보세요!

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png) -->

## 빠른 시작

Caskada가 처음이신가요? [시작하기](https://skadaai.gitbook.io/caskada/introduction/getting_started) 가이드를 확인하여 첫 번째 플로우를 빠르게 구축해 보세요.

## 자기 코딩 앱을 구축할 준비가 되셨나요?

[에이전트 코딩 가이드](https://skadaai.gitbook.io/caskada/guides/agentic_coding)를 확인하세요. Caskada로 자기 코딩 LLM 프로젝트를 개발하는 가장 빠른 방법입니다!

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

## 감사의 말

Caskada가 포크로 시작된 PocketFlow 프레임워크의 창작자와 기여자들에게 깊은 감사를 표합니다.

## 면책 조항

Caskada는 "있는 그대로" 제공되며 어떠한 보증이나 보장도 없습니다.  
생성된 출력의 사용 방식, 정확성, 합법성 또는 그 사용으로 인해 발생할 수 있는 모든 잠재적 결과에 대해 책임을 지지 않습니다.

## 스폰서

<p align="center">
  <a style="color: inherit" href="https://github.com/sponsors/zvictor?utm_source=caskada&utm_medium=sponsorship&utm_campaign=caskada&utm_id=caskada">
    <img width="150" src="https://cdn.jsdelivr.net/gh/skadaai/caskada@main/.github/media/brain.png" alt="Caskada 로고" />
  </a><br /><br />
  Caskada는 200줄의 코드와 여러분의 관대함으로 동작합니다! 💰<br />
    <a style="color: inherit" href="https://github.com/sponsors/zvictor?utm_source=caskada&utm_medium=sponsorship&utm_campaign=caskada&utm_id=caskada">
      더 많은 AI를 더 적은 코드로 제공할 수 있도록 도와주세요 (그러나 커피는 더 필요할지도 모릅니다)
    </a> ☕<br /><br />
    <a style="color: inherit" href="https://github.com/sponsors/zvictor?utm_source=caskada&utm_medium=sponsorship&utm_campaign=caskada&utm_id=caskada">여러분의 지원</a>이 Caskada를 미니멀하고 강력하며 의존성 없이 유지하는 데 도움이 됩니다! 🚀
  </a>
</p>

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)