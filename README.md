# YouTube Todo App

## 概要

YouTube の筋トレ動画を活用したトレーニング管理アプリ。動画 URL をタグ・コメント付きで保存し、ワークアウトの履歴とスケジュールを管理する Todo アプリ。

主な機能:
- YouTube URL のタグ・コメント付き保存
- ワークアウト履歴の記録（有効期限付き）
- 繰り返しルールによるスケジュール自動計算
- 本日の TODO リスト表示

## 技術スタック

| レイヤー | 技術 |
|---|---|
| バックエンド | Python 3.13 / FastAPI |
| ORM | SQLAlchemy + Alembic |
| DB | PostgreSQL 16 |
| パッケージ管理 | uv |
| コンテナ | Docker Compose |

## セットアップ

### 前提条件

- [Docker](https://docs.docker.com/get-docker/) および Docker Compose
- [uv](https://docs.astral.sh/uv/)（テストをローカル実行する場合）

### 起動方法

```bash
# 一括起動（DB + バックエンド + マイグレーション）
bash start_app.sh
```

`start_app.sh` は以下を自動実行します:
1. Docker Compose で PostgreSQL + バックエンドを起動
2. バックエンドの `/health` エンドポイントで起動完了を確認
3. テスト用データベース（`youtube_todo_test`）を作成
4. Alembic マイグレーションを実行

起動後のアクセス先:
- バックエンド: http://localhost:8000
- Swagger UI: http://localhost:8000/docs

## テスト実行

### 前提条件

- Docker Compose でサービスが起動済みであること（`./start_app.sh` 実行済み）
- テスト用データベース（`youtube_todo_test`）が作成済みであること

### コマンド

```bash
# 全テスト実行
cd backend && ENV=test uv run pytest ./tests/

# Unit テストのみ
cd backend && ENV=test uv run pytest ./tests/unit/

# Integration テストのみ
cd backend && ENV=test uv run pytest ./tests/integration/
```

### テストの種類

| 種類 | 内容 | DB |
|---|---|---|
| Unit | スキーマバリデーション、モデル定義、Enum 型、環境設定 | 不要 |
| Integration | CRUD 操作、DB 制約、カスケード削除、トリガー | テスト用 PostgreSQL |

## プロジェクト構成

```
youtube-todo-app/
├── backend/          # FastAPI バックエンド
│   ├── app/
│   │   ├── api/      # ルーター + API スキーマ
│   │   ├── services/ # ビジネスロジック
│   │   ├── crud/     # DB 操作 + CRUD スキーマ
│   │   ├── models/   # SQLAlchemy ORM モデル
│   │   ├── core/     # DB接続、依存性注入、Enum、日付ユーティリティ
│   │   ├── config.py # 環境別設定
│   │   └── main.py   # FastAPI エントリポイント
│   ├── alembic/      # マイグレーション
│   ├── tests/        # Unit / Integration テスト
│   ├── Dockerfile
│   └── pyproject.toml
├── frontend/         # Next.js フロントエンド（未実装）
├── start_app.sh      # 起動スクリプト
├── docker-compose.yml
├── CLAUDE.md
├── docs/             # 設計ドキュメント
└── README.md
```

## API エンドポイント一覧

### Health Check

| メソッド | パス | 説明 |
|---|---|---|
| GET | `/health` | ヘルスチェック |

### Videos

| メソッド | パス | 説明 |
|---|---|---|
| GET | `/api/videos` | 動画一覧取得 |
| POST | `/api/videos` | 動画登録 |
| GET | `/api/videos/{id}` | 動画詳細取得 |
| PUT | `/api/videos/{id}` | 動画更新 |
| DELETE | `/api/videos/{id}` | 動画削除 |

### VideoRecurrence（繰り返しルール）

| メソッド | パス | 説明 |
|---|---|---|
| GET | `/api/videos/{id}/recurrence` | 繰り返しルール取得 |
| PUT | `/api/videos/{id}/recurrence` | 繰り返しルール作成・更新 |
| DELETE | `/api/videos/{id}/recurrence` | 繰り返しルール削除 |

### WorkoutHistories

| メソッド | パス | 説明 |
|---|---|---|
| GET | `/api/workout-histories` | 履歴一覧取得 |
| POST | `/api/workout-histories` | 履歴記録 |
| DELETE | `/api/workout-histories/{id}` | 履歴削除 |

### TodoHistories

| メソッド | パス | 説明 |
|---|---|---|
| GET | `/api/todo-histories` | TODO 履歴一覧取得 |
| POST | `/api/todo-histories` | TODO 完了/スキップを記録 |
| DELETE | `/api/todo-histories/{id}` | 記録を取り消す |

### Today's TODO

| メソッド | パス | 説明 |
|---|---|---|
| GET | `/api/today` | 本日の TODO 一覧 |
| GET | `/api/overdue` | 予定日超過の未実施動画一覧 |

### User Settings

| メソッド | パス | 説明 |
|---|---|---|
| GET | `/api/settings` | ユーザー設定取得 |
| PUT | `/api/settings` | ユーザー設定更新 |

## 停止方法

```bash
# サービス停止
docker compose down

# サービス停止 + データ削除
docker compose down -v
```

## ドキュメント

- [要件定義書](./docs/requirements.md)
- [技術スタック選定書](./docs/tech_stack.md)
- [アーキテクチャ設計書](./docs/architecture.md)
