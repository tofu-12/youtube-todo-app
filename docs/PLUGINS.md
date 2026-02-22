# 導入プラグイン 使い方まとめ

## 導入プラグイン一覧

| プラグイン名 | マーケットプレイス | 役割 |
|---|---|---|
| context7 | claude-plugins-official | ライブラリの最新ドキュメント・コード例をAIに提供 |
| frontend-design | claude-plugins-official | 本番品質のフロントエンドUI生成 |
| claude-mem | thedotmack | セッション間の記憶を永続化・セマンティック検索 |
| superpowers | superpowers-marketplace | 開発ワークフロー全体（計画→TDD→実装→レビュー）を強制 |
| ralph-loop | claude-plugins-official | タスク完了まで自律的にループ実行 |

---

## context7

### 概要
ライブラリの最新公式ドキュメントとコード例をリアルタイムでAIに提供するMCPサーバー。学習データのカットオフを超えた最新APIに対応できる。

### 使い方
会話中に「〜のドキュメントを参照して」「〜の使い方を調べて」と指示するだけで自動的に動作する。明示的に呼び出す場合はAIが内部でツールを使用する。

```
# 例：特定ライブラリのドキュメントを参照した実装を依頼
"React 19のuseActionStateを使ってフォームを実装して"
"Prisma 6のupsert構文で書いて"
```

### 内部ツール
- `resolve-library-id` — ライブラリ名からContext7のIDを解決
- `query-docs` — ドキュメント・コード例を取得

### 向いているケース
- バージョンアップ後のAPIを使いたいとき
- 普段使わないライブラリのコードを書いてもらうとき
- AIの誤った古い知識を上書きしたいとき

---

## frontend-design

### 概要
汎用的なAI生成UIではなく、デザイン品質の高い本番レベルのUIコンポーネント・ページを生成するスキル。

### 使い方
```
/frontend-design
```
または会話でUIの作成・修正を依頼すると自動的に適用される。

### 特徴
- 独自性のあるデザイン（ありきたりなAI感を排除）
- レスポンシブ対応
- アクセシビリティ考慮
- アニメーション・インタラクションの実装

### 向いているケース
- 新しいページ・コンポーネントをゼロから作るとき
- 既存UIのデザインをリファインしたいとき
- プロトタイプを素早く高品質に仕上げたいとき

---

## claude-mem

### 概要
セッションをまたいだ記憶の永続化プラグイン。AIが行ったすべてのツール使用を自動キャプチャし、AIが圧縮・要約して次回セッション時に関連コンテキストを自動注入する。

### アーキテクチャ
- SQLite + ChromaベクトルDBによるセマンティック検索
- 5つのライフサイクルフックで自動記録
  - SessionStart → UserPromptSubmit → PostToolUse → Summary → SessionEnd
- Web UIビューア: `http://localhost:37777`

### 使い方

#### 記憶を検索する
```
/claude-mem:mem-search
```
または会話で「以前〜をどう解決したっけ？」と聞くと自動的に検索する。

#### 計画を立てる（記憶を活用した実装計画）
```
/claude-mem:make-plan
```

#### 計画を実行する
```
/claude-mem:do
```

### 向いているケース
- 数週間〜数ヶ月続く長期プロジェクト
- 複雑なコードベースで毎回説明し直すのが辛いとき
- セッションが頻繁に中断する環境

### 注意
- ライセンス: AGPL-3.0（企業環境ではコピーレフト条項を確認）

---

## superpowers

### 概要
ソフトウェア開発のワークフロー全体をClaude Codeに組み込むプラグイン。「とりあえずコードを書く→手戻り」を防ぎ、計画→テスト→実装の順番を強制する。

### 7フェーズのワークフロー

| フェーズ | スキル | 内容 |
|---|---|---|
| 1 | brainstorming | 要件を対話で深掘り、いきなりコードを書かない |
| 2 | writing-plans | 詳細な設計仕様の策定 |
| 3 | writing-plans | 実装計画の作成 |
| 4 | test-driven-development | TDD（テスト駆動開発） |
| 5 | subagent-driven-development | サブエージェントによる並列実装 |
| 6 | requesting-code-review | コードレビュー依頼 |
| 7 | verification-before-completion | 統合・検証 |

### 主なスキルと使い方

#### セッション開始時（必須）
```
/superpowers:using-superpowers
```

#### ブレインストーミング（実装前に必ず実行）
```
/superpowers:brainstorming
```
新機能・コンポーネント追加・動作変更のすべてで実行する。

#### 実装計画を書く
```
/superpowers:writing-plans
```

#### 計画を実行する
```
/superpowers:executing-plans
```

#### TDD
```
/superpowers:test-driven-development
```

#### 並列サブエージェントで実装
```
/superpowers:dispatching-parallel-agents
/superpowers:subagent-driven-development
```

#### コードレビュー
```
/superpowers:requesting-code-review
/superpowers:receiving-code-review
```

#### 完了前の検証
```
/superpowers:verification-before-completion
```
「完了」「修正済み」「テスト通過」を宣言する前に必ず実行する。

#### ブランチ作業の完了
```
/superpowers:finishing-a-development-branch
```

#### Gitワークツリー管理
```
/superpowers:using-git-worktrees
```

#### デバッグ
```
/superpowers:systematic-debugging
```
バグ・テスト失敗・予期しない動作に遭遇したとき。

### ライセンス
MIT（完全無料のOSS、Anthropic製ではなくコミュニティプロジェクト）

---

## ralph-loop

### 概要
タスクが本当に完了するまでClaude Codeを自律的にループさせるプラグイン。Stopフックでセッションの早期終了をブロックし、完了条件を満たすまで同じプロンプトを再投入し続ける。

### 使い方

#### ループを開始する
```
/ralph-loop:ralph-loop
```

#### ループをキャンセルする
```
/ralph-loop:cancel-ralph
```

#### ヘルプを表示する
```
/ralph-loop:help
```

### プロンプト例
```
/ralph-loop "Feature Xを実装して" --max-iterations 20 --completion-promise "DONE"
```

### ループの動作フロー
1. タスクに取り組む
2. 終了しようとする
3. Stopフックが終了をブロック
4. 同じプロンプトを再投入
5. 完了条件を満たすまで繰り返す

### 向いているケース
- 複数ステップの実装を放置しておきたいとき
- 長時間の自律作業（ドキュメント整備、テスト追加など）
- 「まあこれでいいか」という早期終了を防ぎたいとき

### 注意
- **必ず `--max-iterations` で上限を設定すること**（トークン大量消費を防ぐ）
- 行き詰まった場合の指示もプロンプトに含めておく
- ループはトークンを多く消費するため、コスト管理に注意

---

## 推奨ワークフロー

### 新機能を開発するとき
1. `/superpowers:brainstorming` — 要件を深掘り
2. `/superpowers:writing-plans` — 実装計画を作成
3. `/superpowers:test-driven-development` — テストを先に書く
4. `/superpowers:subagent-driven-development` — 実装
5. `/superpowers:verification-before-completion` — 完了前に検証
6. `/superpowers:finishing-a-development-branch` — ブランチ完了

### 長時間の自律作業をさせたいとき
1. `/superpowers:writing-plans` — 計画を作成
2. `/ralph-loop:ralph-loop` — ループ実行（max-iterations必須）

### バグを修正するとき
1. `/superpowers:systematic-debugging` — 体系的にデバッグ
2. `/superpowers:verification-before-completion` — 修正確認

### 以前の作業を引き継ぐとき
1. `/claude-mem:mem-search` — 過去の記憶を検索
2. 関連コンテキストが自動注入されてから作業開始
