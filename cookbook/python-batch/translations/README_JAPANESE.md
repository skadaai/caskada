<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://cdn.jsdelivr.net/gh/skadaai/caskada@main/.github/media/logo-dark.png">
    <source media="(prefers-color-scheme: light)" srcset="https://cdn.jsdelivr.net/gh/skadaai/caskada@main/.github/media/logo-light.png">
    <img width="280" alt="Caskadaのロゴ" src="https://cdn.jsdelivr.net/gh/skadaai/caskada@main/.github/media/logo-light.png">
  </picture>
<p>

<p align="center">
  革新的にミニマルなAIフレームワーク（<a href="https://github.com/skadaai/caskada/blob/main/python/brainyflow.py">たった200行のPythonコード</a>！🤯）

  <br />
  最小限のコードで強力なAIエージェントを構築し、最大限の自由を実現。
  <br />
  <sub>余計な機能、依存関係、ベンダーロックインなしでエージェントにエージェントを構築させましょう 😮</sub>
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

Caskadaは、強力な抽象化を通じて_エージェンティックコーディング_を可能にするフレームワークです。

共有状態を持つ_ネストされた有向グラフ_に基づいて複雑なAIアプリケーションを構築するためのシンプルなインターフェースを提供します。
人間とAIアシスタントが効果的に協力してAIシステムを設計・実装することを可能にします。

## 特徴

- **Brain-Easy 🧠**: 人間とAIアシスタントの両方にとって直感的
- **ミニマルデザイン ✨**: 核心的な抽象化が（驚くべきことに！）たった200行のコードで実現
- **自由 🔓**: 余計な機能、依存関係、ベンダーロックインなし
- **コンポーザブル 🧩**: シンプルで再利用可能なコンポーネントから複雑なシステムを構築
- **強力 🦾**: お気に入りの機能をすべてサポート - ([マルチ](https://brainy.gitbook.io/flow/design_pattern/multi_agent))[エージェント](https://brainy.gitbook.io/flow/design_pattern/agent)、[ワークフロー](https://brainy.gitbook.io/flow/design_pattern/workflow)、[RAG](https://brainy.gitbook.io/flow/design_pattern/rag)など
- **エージェンティックコーディング 🤖**: AI支援開発向けに設計
- **ユニバーサル 🌈**: 任意のLLMプロバイダーやAPIと連携可能
- **ポリグロット 🌍**: <!-- gitbook-ignore-start --><a href="https://pypi.org/project/brainyflow"><img src="https://github.com/skadaai/caskada/raw/main/.github/media/python.svg" width="16" height="16" alt="Pythonロゴ" style="vertical-align: middle; margin: 0 2px;"></a><!-- gitbook-ignore-end --> Pythonと<!-- gitbook-ignore-start --><a href="https://npmjs.com/packages/brainyflow"><img src="https://github.com/skadaai/caskada/raw/main/.github/media/typescript.svg" width="16" height="16" alt="Typescriptロゴ" style="vertical-align: middle; margin: 0 2px;"></a><!-- gitbook-ignore-end --> Typescriptの両方をサポート

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

<!-- gitbook-ignore-start -->

## ドキュメント

私たちのドキュメントは包括的で、生物学的頭脳と人工知能の両方に適しています。<br />
あなたの条件 - あるいはあなたが信じ込まされている条件 - を選択してください:

\>> [私は炭素ベースです 🐥](https://brainy.gitbook.io/flow/introduction/getting_started) <<

\>> [私はシリコンベースです 🤖](https://flow.bbrainy.sh/docs.txt) <<

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

<!-- gitbook-ignore-end -->

## Brainy Flowを選ぶ理由？

現在のLLMフレームワークは肥大化しています... 実際には堅牢なLLMフレームワークに必要なのはたった200行だけです！

<div align="center">
  <img src="https://raw.githubusercontent.com/skadaai/caskada/main/.github/media/meme.jpg" width="500"/>

|                                                                                                                                                                                                                | **抽象化** |                     **アプリ固有ラッパー**                      |                       **ベンダー固有ラッパー**                       |                **行数**                 |                  **サイズ**                   |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------: | :----------------------------------------------------------------: | :----------------------------------------------------------------------: | :--------------------------------------: | :-----------------------------------------: |
| LangChain                                                                                                                                                                                                      |  エージェント, チェーン |      多数 <br><sup><sub>(例: QA, 要約)</sub></sup>      |      多数 <br><sub>(例: OpenAI, Pineconeなど)</sub></sup>       |                   405K                   |                   +166MB                    |
| CrewAI                                                                                                                                                                                                         |  エージェント, チェーン | 多数 <br><sub>(例: FileReadTool, SerperDevTool)</sub></sup> | 多数 <br><sub>(例: OpenAI, Anthropic, Pineconeなど)</sub></sup> |                   18K                    |                   +173MB                    |
| SmolAgent                                                                                                                                                                                                      |      エージェント      |   一部 <br><sub>(例: CodeAgent, VisitWebTool)</sub></sup>   |  一部 <br><sub>(例: DuckDuckGo, Hugging Faceなど)</sub></sup>   |                    8K                    |                   +198MB                    |
| LangGraph                                                                                                                                                                                                      |  エージェント, グラフ |       一部 <br><sub>(例: セマンティック検索)</sub></sup>       | 一部 <br><sub>(例: PostgresStore, SqliteSaverなど)</sub></sup> |                   37K                    |                    +51MB                    |
| AutoGen                                                                                                                                                                                                        |      エージェント      |   一部 <br><sub>(例: ツールエージェント, チャットエージェント)</sub></sup>    | 多数 <sub>[オプション]<br> (例: OpenAI, Pineconeなど)</sub></sup> | 7K <br><sub>(コアのみ)</sub></sup> | +26MB <br><sub>(コアのみ)</sub></sup> |
| **Caskada** <!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/typescript.svg" width="16" height="16" alt="Typescriptロゴ"><!-- gitbook-ignore-end -->.ts |    **グラフ**    |                              **なし**                              |                                 **なし**                                 |                 **300**                  |                 **数KB**                  |
| **Caskada** <!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/python.svg" width="16" height="16" alt="Pythonロゴ"><!-- gitbook-ignore-end -->.py         |    **グラフ**    |                              **なし**                              |                                 **なし**                                 |                 **200**                  |                 **数KB**                  |

</div>

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

## Caskadaの仕組み

<a href="https://github.com/skadaai/caskada/blob/main/python/brainyflow.py"><!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/python.svg" width="16" height="16" alt="Pythonロゴ" style="vertical-align: middle; margin: 0 2px;"> <!-- gitbook-ignore-end -->Python</a>または<a href="https://github.com/skadaai/caskada/blob/main/typescript/brainyflow.ts"><!-- gitbook-ignore-start --><img src="https://github.com/skadaai/caskada/raw/main/.github/media/typescript.svg" width="16" height="16" alt="Typescriptロゴ" style="vertical-align: middle; margin: 0 2px;"> <!-- gitbook-ignore-end -->Typescript</a>の単一ファイルがLLMフレームワークの核心的な抽象化であるグラフを実装しています！
<br>

<div align="center">
  <img src="https://raw.githubusercontent.com/skadaai/caskada/main/.github/media/abstraction.jpg" width="1300"/>
</div>
<br>

- [ノード](https://brainy.gitbook.io/flow/core_abstraction/node)は明確なライフサイクル（`prep` → `exec` → `post`）を持つシンプルな(LLM)タスクを処理します。
- [フロー](https://brainy.gitbook.io/flow/core_abstraction/flow)はノードを**アクション**（ラベル付きエッジ）で接続し、実行をオーケストレーションします。
- [メモリ](https://brainy.gitbook.io/flow/core_abstraction/memory)は共有（`global`）状態と分離（`local`）状態を管理し、ノード間の通信を可能にします。

そこから、全ての人気デザインパターンを簡単に実装できます:
<br>

<div align="center">
  <img src="https://raw.githubusercontent.com/skadaai/caskada/main/.github/media/design.jpg" width="1300"/>
</div>
<br>

- [エージェント](https://brainy.gitbook.io/flow/design_pattern/agent)はコンテキストに基づいて自律的に意思決定します。
- [ワークフロー](https://brainy.gitbook.io/flow/design_pattern/workflow)は複数のタスクを連鎖させたシーケンシャルパイプラインを構築します。
- [RAG](https://brainy.gitbook.io/flow/design_pattern/rag)はデータ取得と生成を統合します。
- [マップリデュース](https://brainy.gitbook.io/flow/design_pattern/mapreduce)はデータタスクをマップとリデュースのステップに分割します。
- [構造化出力](https://brainy.gitbook.io/flow/design_pattern/structure)は出力を一貫した形式で整形します。
- [マルチエージェント](https://brainy.gitbook.io/flow/design_pattern/multi_agent)は複数のエージェントを調整します。

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

## チュートリアル

<div align="center">
  
|  名前  | 難易度    |  説明  |  
| :-------------:  | :-------------: | :--------------------- |  
| [チャット](https://github.com/skadaai/caskada/tree/main/cookbook/python-chat) | ☆☆☆ <br> *初級*   | 会話履歴を持つ基本的なチャットボット |
| [RAG](https://github.com/skadaai/caskada/tree/main/cookbook/python-rag) | ☆☆☆ <br> *初級*   | シンプルな検索拡張生成プロセス |
| [ワークフロー](https://github.com/skadaai/caskada/tree/main/cookbook/python-workflow) | ☆☆☆ <br> *初級*   | アウトライン作成、コンテンツ執筆、スタイル適用を行うライティングワークフロー |
| [マップリデュース](https://github.com/skadaai/caskada/tree/main/cookbook/python-map-reduce) | ☆☆☆ <br> *初級* | バッチ評価のためのマップリデュースパターンを使用した履歴書選考プロセッサ |
| [エージェント](https://github.com/skadaai/caskada/tree/main/cookbook/python-agent) | ☆☆☆ <br> *初級*   | ウェブを検索して質問に答えられるリサーチエージェント |
| [ストリーミング](https://github.com/skadaai/caskada/tree/main/cookbook/python-llm-streaming) | ☆☆☆ <br> *初級*   | ユーザー中断機能付きのリアルタイムLLMストリーミングデモ |
| [マルチエージェント](https://github.com/skadaai/caskada/tree/main/cookbook/python-multi-agent) | ★☆☆ <br> *中級* | 2つのエージェント間の非同期通信のためのタブー語ゲーム |
| [スーパーバイザー](https://github.com/skadaai/caskada/tree/main/cookbook/python-supervisor) | ★☆☆ <br> *中級* | 信頼性の低いリサーチエージェント...監視プロセスを構築しよう|
| [並列処理](https://github.com/skadaai/caskada/tree/main/cookbook/python-parallel-batch) | ★☆☆ <br> *中級*   | 3倍の高速化を示す並列実行デモ |
| [思考](https://github.com/skadaai/caskada/tree/main/cookbook/python-thinking) | ★☆☆ <br> *中級*   | 連鎖思考を通じた複雑な推論問題の解決 |
| [メモリ](https://github.com/skadaai/caskada/tree/main/cookbook/python-chat-memory) | ★☆☆ <br> *中級* | 短期記憶と長期記憶を持つチャットボット |

</div>

他にも多数のチュートリアルがすべてのレベルに対応！[こちらで全てチェック！](https://github.com/skadaai/caskada/tree/main/cookbook)

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

## クイックスタート

Caskadaが初めてですか？[スタートガイド](https://brainy.gitbook.io/flow/introduction/getting_started)をチェックして、すぐに最初のフローを構築しましょう。

## 自動コーディングアプリを構築する準備は？

[エージェンティックコーディングガイド](https://brainy.gitbook.io/flow/guides/agentic_coding)をチェックし、Caskadaで自動コーディングLLMプロジェクトを最速で開発しましょう！

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)

## 謝辞

brainyFlowの元となったPocketFlowフレームワークの作成者と貢献者に深く感謝いたします。

## 免責事項

Caskadaは「現状のまま」提供され、いかなる保証もありません。  
生成された出力の使用方法、正確性、合法性、またはその使用から生じる可能性のある結果について、私たちは責任を負いません。

## スポンサー

<p align="center">
  <a style="color: inherit" href="https://github.com/sponsors/zvictor?utm_source=brainyflow&utm_medium=sponsorship&utm_campaign=brainyflow&utm_id=brainyflow">
    <img width="150" src="https://cdn.jsdelivr.net/gh/skadaai/caskada@main/.github/media/brain.png" alt="Caskadaのロゴ" />
  </a><br /><br />
  Caskadaは200行のコードとあなたの寛大さで動いています！ 💰<br />
    <a style="color: inherit" href="https://github.com/sponsors/zvictor?utm_source=brainyflow&utm_medium=sponsorship&utm_campaign=brainyflow&utm_id=brainyflow">
      より少ないコードでより多くのAIを届けるのを支援してください（ただしカフェインは多めに必要かも）
    </a> ☕<br /><br />
    <a style="color: inherit" href="https://github.com/sponsors/zvictor?utm_source=brainyflow&utm_medium=sponsorship&utm_campaign=brainyflow&utm_id=brainyflow">あなたの支援</a>がCaskadaをミニマルで強力、依存関係なしで保ちます！ 🚀
  </a>
</p>

![](https://raw.githubusercontent.com/skadaai/caskada/master/.github/media/divider.png)
```