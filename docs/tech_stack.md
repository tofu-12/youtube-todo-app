# youtube-todo-app 技術スタック選定書

## 1. 選定サマリ

| レイヤー | 採用技術 | バージョン |
|---|---|---|
| バックエンド言語 | Python | 3.13 |
| バックエンド FW | FastAPI | ^0.115 |
| ASGI サーバー | Uvicorn | ^0.34 |
| ORM | SQLAlchemy | ^2.0 |
| マイグレーション | Alembic | ^1.13 |
| バリデーション | Pydantic | ^2.0（FastAPI 同梱） |
| フロントエンド言語 | TypeScript | ^5.0 |
| フロントエンド FW | Next.js | ^15 |
| スタイリング | Tailwind CSS | ^3.0 |
| DB | PostgreSQL | ^16 |
| パッケージ管理（BE） | UV | 最新 |

---

## 2. 各技術の選定理由

### 2.1 バックエンド: FastAPI

| フレームワーク | 評価 |
|---|---|
| Django | オーバースペック。管理画面・独自 ORM・テンプレートエンジン等、不要機能が多い |
| Flask | 型安全性が弱い。非同期サポートが限定的 |
| **FastAPI** | Pydantic 統合で型安全・OpenAPI 自動生成・Python 3.13 の型ヒントを最大限活用できる |

**選定理由:** Pydantic による入出力バリデーションと OpenAPI ドキュメントの自動生成により、API 開発の生産性が高い。Python 3.13 の型ヒントと相性が良く、非同期処理も標準でサポートしている。

### 2.2 フロントエンド: Next.js (TypeScript)

| フレームワーク | 評価 |
|---|---|
| React + Vite | SPA のみ。SSR・Auth.js 統合が別途必要 |
| **Next.js** | App Router で SSR/SSG を標準サポート。Auth.js との公式統合が存在する |

**選定理由:**

- App Router により TODO リストのリアルタイム更新が実装しやすい
- Post-MVP で Auth0 を使う際、Auth.js（next-auth）との公式統合が存在する
- TypeScript 公式テンプレートが充実しており、即開始できる

### 2.3 データベース: PostgreSQL

| 項目 | SQLite | PostgreSQL | MySQL |
|---|---|---|---|
| セットアップ | 不要（ファイルベース） | サーバー起動が必要 | サーバー起動が必要 |
| 同時接続 | 制限あり（書き込みロック） | 高い並列性をサポート | 高い並列性をサポート |
| データ型 | 最小限（型の強制が緩い） | 豊富（UUID, JSONB, 配列など） | 標準的（JSON サポートあり） |
| スケーラビリティ | 小規模向け | 大規模・本番向け | 大規模・本番向け |
| 認証・権限管理 | なし | あり | あり |
| 標準 SQL 準拠 | 部分的 | 高い | 中程度 |
| 移行コスト（SQLAlchemy 経由） | — | 接続文字列の変更のみ | 接続文字列の変更のみ |

**PostgreSQL vs MySQL 詳細比較:**

| 項目 | PostgreSQL | MySQL |
|---|---|---|
| UUID 型 | ネイティブサポート | CHAR/BINARY で代替が必要 |
| ENUM 型 | ネイティブサポート | ネイティブサポート |
| タイムゾーン | `TIMESTAMPTZ` で UTC 管理が堅牢 | `DATETIME` はタイムゾーン非対応（アプリ側で管理） |
| JSON | `JSONB`（インデックス付き、高速） | `JSON`（インデックス不可） |
| 標準 SQL 準拠 | 高い | 中程度（独自拡張が多い） |
| 複雑なクエリ | 得意（CTE・ウィンドウ関数が強力） | 基本的なクエリに最適化 |
| 拡張機能 | `pgvector`（ML 埋め込み）など豊富 | 少ない |
| ホスティング | Supabase・Neon・RDS など選択肢が多い | RDS・PlanetScale など |
| Python / SQLAlchemy | 完全サポート | 完全サポート |

**本番 DB の選定: PostgreSQL**

- UUID・ENUM をネイティブサポートしており、本プロジェクトのスキーマと相性が良い
- `TIMESTAMPTZ` により UTC 管理が確実（本プロジェクトの datetime 管理方針と一致）
- Post-MVP の ML 機能（習慣度スコア）で `pgvector` 等の拡張が活用できる
- SQLite → PostgreSQL の移行コストが最小（SQLAlchemy 経由）

**選定理由:**

- MVP から PostgreSQL を使用することで、開発・本番環境の差異をなくす
- UUID・ENUM・TIMESTAMPTZ など、本プロジェクトのスキーマに必要な型をすべてネイティブサポート
- Docker Compose でローカル起動も容易（セットアップコストは最小）

### 2.4 ORM: SQLAlchemy + Alembic

**選定理由:**

- FastAPI との相性が最良
- Alembic でマイグレーション管理・スキーマ変更を追跡可能
- 情報量・安定性・エコシステムが Python ORM 中最多

---

## 3. Post-MVP 追加スタック

### 3.1 YouTube 動画メタデータ取得

- **採用技術:** YouTube Data API v3
- タイトル・動画時間・概要欄・サムネイル URL を動画登録時に自動取得
- API キーのみで利用可能（OAuth 不要）
- **追加環境変数:** `YOUTUBE_API_KEY`

### 3.2 認証: Auth0

- FE: Auth.js（next-auth）で Auth0 ログイン
- BE: pyjwt による JWT 検証
- Issue #8 で明示指定のため採用

### 3.3 習慣度スコア（ML）

| 選択肢 | 概要 | 実装コスト |
|---|---|---|
| A: scikit-learn | 軽量な分類モデル（ロジスティック回帰・ランダムフォレスト等） | 低 |
| B: PyTorch / TensorFlow | NN による時系列モデル | 高 |
| C: statsmodels | 時系列統計モデル（ARIMA 等） | 中 |

**推奨: scikit-learn** — MVP 後の初期実装として軽量かつ十分な精度。データ量が増えた段階で PyTorch へ移行可能。

- 学習データ: `TodoHistory.status`（completed / skipped）の時系列
- スコア更新: TODO 完了/スキップ記録時にバックグラウンドジョブで再計算

### 3.4 ユーザーレベル・経験値

- 追加ライブラリなし（既存スタックで実装可能）
- XP 計算ロジックはサービス層に実装
- レベルアップ閾値テーブルを DB で管理

### 3.5 AI 要約機能（動画サマリー）

| 選択肢 | 概要 | 実装コスト |
|---|---|---|
| A: youtube-transcript-api + LLM | 字幕テキスト取得 → 要約 | 中（字幕取得処理が必要） |
| B: 説明文 + LLM | YouTube API → 概要欄テキスト → 要約 | 中（API 認証が必要） |
| C: Gemini API（URL 直接） | URL 指定のみで要約 | 低（最もシンプル） |

**推奨: Gemini API（URL 直接）** — 字幕取得・API 認証が不要で実装が最もシンプル。3.1 で概要欄テキストを取得済みの場合は選択肢 B も低コストで実現可能。

---

## 4. 開発環境

### 4.1 ローカル起動手順

```bash
# バックエンド（ポート 8000）
uv run uvicorn app.main:app --reload

# フロントエンド（ポート 3000）
npm run dev
```

### 4.2 環境変数

| 変数名 | 説明 | MVP 値 |
|---|---|---|
| DATABASE_URL | DB 接続文字列 | `postgresql://user:password@localhost:5432/youtube_todo` |
| NEXT_PUBLIC_API_URL | バックエンド URL | `http://localhost:8000` |
