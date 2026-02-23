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
| DB（開発） | SQLite | — |
| DB（本番候補） | PostgreSQL | ^16 |
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

### 2.3 データベース: SQLite → PostgreSQL

**選定理由:**

- MVP はローカル・1 ユーザーのため SQLite で十分（セットアップゼロ）
- SQLAlchemy 経由のため、本番移行時は接続文字列変更のみで対応可能

### 2.4 ORM: SQLAlchemy + Alembic

**選定理由:**

- FastAPI との相性が最良
- Alembic でマイグレーション管理・スキーマ変更を追跡可能
- 情報量・安定性・エコシステムが Python ORM 中最多

---

## 3. Post-MVP 追加スタック

### 3.1 認証: Auth0

- FE: Auth.js（next-auth）で Auth0 ログイン
- BE: pyjwt による JWT 検証
- Issue #8 で明示指定のため採用

### 3.2 AI 要約機能

| 選択肢 | 概要 | 実装コスト |
|---|---|---|
| A: youtube-transcript-api + LLM | 字幕テキスト取得 → 要約 | 中（字幕取得処理が必要） |
| B: 説明文 + LLM | YouTube API → 概要欄テキスト → 要約 | 中（API 認証が必要） |
| C: Gemini API（URL 直接） | URL 指定のみで要約 | 低（最もシンプル） |

**推奨: Gemini API（URL 直接）** — 字幕取得・API 認証が不要で実装が最もシンプル。

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
| DATABASE_URL | DB 接続文字列 | `sqlite:///./dev.db` |
| NEXT_PUBLIC_API_URL | バックエンド URL | `http://localhost:8000` |

---

## 5. 想定ディレクトリ構成

```
youtube-todo-app/
├── backend/            # FastAPI アプリ
│   ├── app/
│   │   ├── main.py
│   │   ├── models/     # SQLAlchemy モデル
│   │   ├── schemas/    # Pydantic スキーマ
│   │   ├── routers/    # API ルーター
│   │   └── services/  # ビジネスロジック
│   └── migrations/    # Alembic マイグレーション
└── frontend/           # Next.js アプリ
    └── src/app/        # App Router
```
