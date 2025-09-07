<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://cdn.jsdelivr.net/gh/skadaai/caskada@main/.github/media/logo-dark.png">
    <source media="(prefers-color-scheme: light)" srcset="https://cdn.jsdelivr.net/gh/skadaai/caskada@main/.github/media/logo-light.png">
    <img width="280" alt="Brainyflowのロゴ" src="https://cdn.jsdelivr.net/gh/skadaai/caskada@main/.github/media/logo-light.png">
  </picture>
<p>

<p align="center">
  革命的にミニマルなAIフレームワーク（たった<a href="https://github.com/skadaai/caskada/blob/main/python/brainyflow.py">Pythonで200行</a>! 🤯）

  <br />
  最小限のコードで強力なAIエージェントを構築し、最大限の自由度を実現。
  <br />
  <sub>余計な機能、依存関係、ベンダーロックインなしでエージェントがエージェントを構築 😮</sub>
</p>

<p align="center">

  <a href="https://pypi.org/project/brainyflow">
   <img src="https://img.shields.io/pypi/dw/brainyflow?logo=python&label=Python&style=flat-square" alt="pythonバージョン">
  </a>
  <a href="https://npmjs.com/packages/brainyflow">
   <img src="https://img.shields.io/npm/d18m/brainyflow?logo=typescript&label=Typescript&style=flat-square" alt="typescriptバージョン">
  </a>
  <a href="https://discord.gg/N9mVvxRXyH">
    <img src="https://img.shields.io/discord/1346833819172601907?logo=discord&style=flat-square" alt="Discord">
  </a>
  <a href="https://github.com/skadaai/caskada">
    <img src="https://img.shields.io/github/stars/skadaai/caskada?logo=github&style=flat-square" alt="GitHubリポジトリ">
  </a>
  <a href="https://github.com/sponsors/zvictor">
    <img src="https://img.shields.io/github/sponsors/zvictor?logo=github&style=flat-square" alt="GitHubスポンサー">
  </a>
</p>

BrainyFlowは、強力な抽象化を通じて_エージェンシックコーディング_を可能にするフレームワークです。

共有状態を持つ_ネストされた有向グラフ_に基づいて複雑なAIアプリケーションを構築するためのシンプルなインターフェースを提供します。
人間とAIアシスタントが効果的に協力してAIシステムを設計・実装することを可能にします。

## 特徴

- **直感的 🧠**: 人間とAIアシスタントの両方にとって直感的
- **ミニマルデザイン ✨**: コア抽象化はたった（驚くべきことに！）200行のコード
- **自由 🔓**: 余計な機能、依存関係、ベンダーロックインなし
- **構成可能 🧩**: シンプルで再利用可能なコンポーネントから複雑なシステムを構築
- **強力 🦾**: お気に入りのすべてをサポート（[マルチ](https://brainy.gitbook.io/flow/design_pattern/multi_agent)）[エージェント](https://brainy.gitbook.io/flow/design_pattern/agent)、[ワークフロー](https://brainy.gitbook.io/flow/design_pattern/workflow)、[RAG](https://brainy.gitbook.io/flow/design_pattern/rag)など
- **エージェンシックコーディング 🤖**: AI支援開発向けに設計
- **ユニバーサル 🌈**: 任意のLLMプロバイダーまたはAPIと連携
- **多言語対応 🌍**: <!-- gitbook-ignore-start --><a href="https://pypi.org/project/brainyflow"><img src="https://github.com/skadaai/caskada/raw/main/.github/media/python.svg" width="16" height="16" alt="Pythonロゴ" style="vertical-align: middle; margin: 0 2px;"></a><!-- gitbook-ignore-end --> Pythonと<!-- gitbook-ignore-start --><a href="https://npmjs.com/packages/brainyflow"><img src="https://github.com/skadaai/caskada/raw/main/.github/media/typescript.svg" width="16" height="16" alt="Typescriptロゴ" style="vertical-align: middle; margin: 0 2px;"></a><!-- gitbook-ignore-end --> Typescriptの両方をサポート

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

<!-- gitbook-ignore-start -->

## ドキュメント

私たちのドキュメントは包括的で、生物学的および合成のマインドの両方に適しています。<br />
あなたの状態、あるいは_信じ込まされている状態_を選択してください:

\>> [私は炭素ベースです 🐥](https://brainy.gitbook.io/flow/introduction/getting_started) <<

\>> [私はシリコンベースです 🤖](https://flow.brainy.sh/docs.txt) <<

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

<!-- gitbook-ignore-end -->

## Brainy Flowを選ぶ理由？

現在のLLMフレームワークは肥大化しています... 実際には、堅牢なLLMフレームワークにはたった200行しか必要ありません！

<div align="center">
  <img src="https://raw.githubusercontent.com/skadaai/caskada/main/.github/media/meme.jpg" width="500"/>

|                                                                                                                                                                                                                | **抽象化** |                     **アプリ固有のラッパー**                      |                       **ベンダー固有のラッパー**                       |                **行数**                 |                  **サイズ**                   |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------: | :----------------------------------------------------------------: | :----------------------------------------------------------------------: | :--------------------------------------: | :-----------------------------------------: |
| LangChain                                                                                                                                                                                                      |  エージェント、チェーン  |      多数 <br><sup><sub>（例: QA、要約）</sub></sup>      |      多数 <br><sup><sub>（例: OpenAI、Pineconeなど）</sub></sup>       |                   405K                   |                   +166MB                    |
| CrewAI                                                                                                                                                                                                         |  エージェント、チェーン  | 多数 <br><sup><sub>（例: FileReadTool、SerperDevTool）</sub></sup> | 多数 <br><sup><sub>（例: OpenAI、Anthropic、Pineconeなど）</sub></sup> |                   18K                    |                   +173MB                    |
| SmolAgent                                                                                                                                                                                                      |      エージェント      |   いくつか <br><sup><sub>（例: CodeAgent、VisitWebTool）</sub></sup>   |  いくつか <br><sub>（例: DuckDuckGo、Hugging Faceなど）</sub></sup>   |                    8K                    |                   +198MB                    |
| LangGraph                                                                                                                                                                                                      |  エージェント、グラフ  |       いくつか <br><sup><sub>（例: セマンティック検索）</sub></sup>       | いくつか <br><sup><sub>（例: PostgresStore、SqliteSaverなど） </sub></sup> |                   37K                    |                    +51MB                    |
| AutoGen                                                                                                                                                                                                        |      エージェント      |   いくつか <br><sup><sub>（例: ツールエージェント、チャットエージェント）</sub></sup>    | 多数 <sup><sub>[オプション]<br> （例: OpenAI、Pineconeなど）</sub></sup> | 7K <br><sup><sub>（コアのみ）</sub></sup> | +26MB <br><sup><sub>（コアのみ）</sub></sup> |
| **BrainyFlow** <!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/typescript.svg" width="16" height="16" alt="Typescriptロゴ"><!-- gitbook-ignore-end -->.ts |    **グラフ**    |                              **なし**                              |                                 **なし**                                 |                 **300**                  |                 **数KB**                  |
| **BrainyFlow** <!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/python.svg" width="16" height="16" alt="Pythonロゴ"><!-- gitbook-ignore-end -->.py         |    **グラフ**    |                              **なし**                              |                                 **なし**                                 |                 **200**                  |                 **数KB**                  |

</div>

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

## BrainyFlowの仕組み

単一ファイルの<a href="https://github.com/skadaai/caskada/blob/main/python/brainyflow.py"><!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/python.svg" width="16" height="16" alt="Pythonロゴ" style="vertical-align: middle; margin: 0 2px;"> <!-- gitbook-ignore-end -->Python</a>または<a href="https://github.com/skadaai/caskada/blob/main/typescript/brainyflow.ts"><!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/typescript.svg" width="16" height="16" alt="Typescriptロゴ" style="vertical-align: middle; margin: 0 2px;"> <!-- gitbook-ignore-end -->Typescript</a>がLLMフレームワークのコア抽象化であるグラフをキャプチャします！
<br>

<div align="center">
  <img src="https://raw.githubusercontent.com/skadaai/caskada/main/.github/media/abstraction.jpg" width="1300"/>
</div>
<br>

- [ノード](https://brainy.gitbook.io/flow/core_abstraction/node)は明確なライフサイクル（`prep` → `exec` → `post`）を持つシンプルな（LLM）タスクを処理します。
- [フロー](https://brainy.gitbook.io/flow/core_abstraction/flow)は**アクション**（ラベル付きエッジ）を通じてノードを接続し、実行を調整します。
- [メモリ](https://brainy.gitbook.io/flow/core_abstraction/memory)は共有（`global`）および隔離（`local`）状態を管理し、ノード間の通信を可能にします。

そこから、すべての人気デザインパターンを簡単に実装できます:
<br>

<div align="center">
  <img src="https://raw.githubusercontent.com/skadaai/caskada/main/.github/media/design.jpg" width="1300"/>
</div>
<br>

- [エージェント](https://brainy.gitbook.io/flow/design_pattern/agent)はコンテキストに基づいて自律的に決定を行います。
- [ワークフロー](https://brainy.gitbook.io/flow/design_pattern/workflow)は複数のタスクを順次パイプラインに連結します。
- [RAG](https://brainy.gitbook.io/flow/design_pattern/rag)はデータ検索と生成を統合します。
- [Map Reduce](https://brainy.gitbook.io/flow/design_pattern/mapreduce)はデータタスクをMapとReduceのステップに分割します。
- [構造化出力](https://brainy.gitbook.io/flow/design_pattern/structure)は出力を一貫した形式に整えます。
- [マルチエージェント](https://brainy.gitbook.io/flow/design_pattern/multi_agent)は複数のエージェントを調整します。

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

## チュートリアル

<div align="center">
  
|  名前  | 難易度    |  説明  |  
| :-------------:  | :-------------: | :--------------------- |  
| [チャット](https://github.com/skadaai/caskada/tree/main/cookbook/python-chat) | ☆☆☆ <br> *初心者*   | 会話履歴を持つ基本的なチャットボット |
| [RAG](https://github.com/skadaai/caskada/tree/main/cookbook/python-rag) | ☆☆☆ <br> *初心者*   | シンプルな検索拡張生成プロセス |
| [ワークフロー](https://github.com/skadaai/caskada/tree/main/cookbook/python-workflow) | ☆☆☆ <br> *初心者*   | アウトラインを作成し、コンテンツを書き、スタイルを適用するライティングワークフロー |
| [Map-Reduce](https://github.com/skadaai/caskada/tree/main/cookbook/python-map-reduce) | ☆☆☆ <br> *初心者* | バッチ評価のためにmap-reduceパターンを使用した履歴書選考プロセッサ |
| [エージェント](https://github.com/skadaai/caskada/tree/main/cookbook/python-agent) | ☆☆☆ <br> *初心者*   | ウェブを検索して質問に答える研究エージェント |
| [ストリーミング](https://github.com/skadaai/caskada/tree/main/cookbook/python-llm-streaming) | ☆☆☆ <br> *初心者*   | ユーザー中断機能を備えたリアルタイムLLMストリーミングデモ |
| [マルチエージェント](https://github.com/skadaai/caskada/tree/main/cookbook/python-multi-agent) | ★☆☆ <br> *初級* | 2つのエージェント間の非同期通信のためのタブー単語ゲーム |
| [スーパーバイザー](https://github.com/skadaai/caskada/tree/main/cookbook/python-supervisor) | ★☆☆ <br> *初級* | 研究エージェントが不安定になってきた... 監視プロセスを構築しよう |
| [並列処理](https://github.com/skadaai/caskada/tree/main/cookbook/python-parallel-batch) | ★☆☆ <br> *初級*   | 3倍の高速化を示す並列実行デモ |
| [思考](https://github.com/skadaai/caskada/tree/main/cookbook/python-thinking) | ★☆☆ <br> *初級*   | 連鎖思考を通じて複雑な推論問題を解決 |
| [メモリ](https://github.com/skadaai/caskada/tree/main/cookbook/python-chat-memory) | ★☆☆ <br> *初級* | 短期記憶と長期記憶を持つチャットボット |

</div>

その他、すべてのレベルに対応したチュートリアルが用意されています！ [すべてチェックしてください！](https://github.com/skadaai/caskada/tree/main/cookbook)

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

<!-- ## Brainy Flowの使い方？

🚀 **エージェンシックコーディング**を通じて、最速のLLMアプリ開発パラダイムで _人間が設計_ し _エージェントがコーディング_ します！

<br />

- **エージェンシックコーディング**を学びたいですか？
  - セットアップ方法は、この[ポスト](https://zacharyhuang.substack.com/p/agentic-coding-the-most-fun-way-to)を読んでください！
  - [私のYouTube](https://www.youtube.com/@ZacharyLLM?sub_confirmation=1)をチェック！ この[ガイド](https://brainy.gitbook.io/flow/guides/agentic_coding)を読んでください！

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png) -->

## クイックスタート

BrainyFlowが初めてですか？ [はじめに](https://brainy.gitbook.io/flow/introduction/getting_started)ガイドをチェックして、すぐに最初のフローを構築しましょう。

## 自己コーディングアプリを構築する準備はできましたか？

BrainyFlowを使用した自己コーディングLLMプロジェクトを最速で開発する方法である[エージェンシックコーディングガイダンス](https://brainy.gitbook.io/flow/guides/agentic_coding)をチェックしてください！

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

## 謝辞

PocketFlowフレームワークの作成者および貢献者に深く感謝します。brainyFlowはこのフォークから始まりました。

## 免責事項

BrainyFlowは「現状のまま」提供され、いかなる保証もありません。  
生成された出力の使用方法、その正確性、合法性、または使用から生じる潜在的な結果について、私たちは責任を負いません。

## スポンサー

<p align="center">
  <a style="color: inherit" href="https://github.com/sponsors/zvictor?utm_source=brainyflow&utm_medium=sponsorship&utm_campaign=brainyflow&utm_id=brainyflow">
    <img width="150" src="https://cdn.jsdelivr.net/gh/skadaai/caskada@main/.github/media/brain.png" alt="Brainyflowのロゴ" />
  </a><br /><br />
  BrainyFlowは200行のコードとあなたの寛大さで動いています！ 💰<br />
    <a style="color: inherit" href="https://github.com/sponsors/zvictor?utm_source=brainyflow&utm_medium=sponsorship&utm_campaign=brainyflow&utm_id=brainyflow">
      より多くのAIをより少ないコードで提供するのを手伝ってください（ただし、カフェインはもっと必要かもしれません）
    </a> ☕<br /><br />
    <a style="color: inherit" href="https://github.com/sponsors/zvictor?utm_source=brainyflow&utm_medium=sponsorship&utm_campaign=brainyflow&utm_id=brainyflow">あなたのサポート</a>が、BrainyFlowをミニマルで強力で依存関係のない状態に保つのに役立ちます！ 🚀
  </a>
</p>

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)