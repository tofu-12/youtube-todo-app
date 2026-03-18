# アーキテクチャ設計書

作成日: 2026-02-24

---

## 1. リポジトリ構成

モノレポ構成。バックエンド（FastAPI）とフロントエンド（Next.js）を1リポジトリで管理する。

```
youtube-todo-app/
├── backend/
│   ├── app/
│   │   ├── api/                           # FastAPI Routers（リソース単位）
│   │   │   ├── schemas/                   # APIエンドポイント用スキーマ（Request/Response）
│   │   │   │   ├── video.py
│   │   │   │   └── ...
│   │   │   ├── videos.py
│   │   │   ├── recurrences.py
│   │   │   ├── workout_histories.py
│   │   │   ├── todo_histories.py
│   │   │   ├── today.py                   # /today, /overdue
│   │   │   └── settings.py
│   │   ├── services/                      # ビジネスロジック
│   │   │   ├── video_service.py
│   │   │   ├── recurrence_service.py      # next_scheduled_date 計算
│   │   │   └── settings_service.py
│   │   ├── crud/                          # DB操作（SQLAlchemy）
│   │   │   ├── schemas/                   # CRUD操作用スキーマ（内部データ構造）
│   │   │   │   ├── user.py
│   │   │   │   ├── video.py
│   │   │   │   ├── recurrence.py
│   │   │   │   ├── tag.py
│   │   │   │   ├── todo_history.py
│   │   │   │   └── workout_history.py
│   │   │   ├── user.py
│   │   │   ├── video.py
│   │   │   ├── recurrence.py
│   │   │   ├── tag.py
│   │   │   ├── video_tag.py
│   │   │   ├── todo_history.py
│   │   │   └── workout_history.py
│   │   ├── models/                        # SQLAlchemy ORM モデル
│   │   │   ├── base.py                    # 共通ベースモデル（TimestampMixin 等）
│   │   │   ├── user.py
│   │   │   ├── video.py
│   │   │   ├── video_recurrence.py
│   │   │   ├── video_weekday.py
│   │   │   ├── tag.py
│   │   │   ├── video_tag.py
│   │   │   ├── todo_history.py
│   │   │   └── workout_history.py
│   │   ├── core/
│   │   │   ├── database.py                # SQLAlchemy engine / Session
│   │   │   ├── dependencies.py            # Depends(get_db) 等
│   │   │   ├── types.py                   # Enum 定義（RecurrenceType / DayOfWeek / TodoStatus）
│   │   │   └── date.py                    # 論理的な今日の算出（横断的ユーティリティ）
│   │   ├── config.py                      # 環境別設定（DevSettings / TestSettings）
│   │   └── main.py                        # FastAPI app インスタンス（/health 含む）
│   ├── alembic/                           # マイグレーション
│   ├── Dockerfile                         # バックエンド用 Docker イメージ
│   ├── tests/
│   │   ├── unit/
│   │   │   ├── test_config.py             # 環境設定のテスト
│   │   │   ├── test_models.py             # ORM モデル定義のテスト
│   │   │   ├── test_types.py              # Enum 型のテスト
│   │   │   ├── test_unique_constraints.py # ユニーク制約のテスト
│   │   │   └── test_schemas/              # スキーマバリデーションのテスト
│   │   │       ├── test_recurrence_schema.py
│   │   │       ├── test_tag_schema.py
│   │   │       ├── test_todo_history_schema.py
│   │   │       ├── test_user_schema.py
│   │   │       ├── test_video_schema.py
│   │   │       └── test_workout_history_schema.py
│   │   ├── integration/
│   │   │   ├── test_cascade.py            # カスケード削除のテスト
│   │   │   ├── test_constraints.py        # DB 制約のテスト
│   │   │   ├── test_triggers.py           # DB トリガーのテスト
│   │   │   └── test_crud/                 # CRUD 操作のテスト
│   │   │       ├── test_crud_recurrence.py
│   │   │       ├── test_crud_tag.py
│   │   │       ├── test_crud_todo_history.py
│   │   │       ├── test_crud_user.py
│   │   │       ├── test_crud_video.py
│   │   │       ├── test_crud_video_tag.py
│   │   │       └── test_crud_workout_history.py
│   │   ├── test_imports.py                # モジュールインポートのテスト
│   │   └── conftest.py                    # DBセッション・テスト用フィクスチャ
│   └── pyproject.toml
├── frontend/                              # ※未実装（設計のみ）
│   ├── src/
│   │   ├── app/                           # Next.js App Router
│   │   │   ├── page.tsx                   # / TODOリスト（Server Component）
│   │   │   ├── overdue/page.tsx
│   │   │   ├── videos/
│   │   │   │   ├── page.tsx
│   │   │   │   ├── new/page.tsx
│   │   │   │   └── [id]/page.tsx
│   │   │   └── layout.tsx
│   │   ├── components/                    # 再利用コンポーネント
│   │   │   ├── TodoItem.tsx               # 'use client'（操作あり）
│   │   │   └── VideoForm.tsx              # 'use client'（フォーム）
│   │   └── lib/
│   │       └── api.ts                     # API クライアント（fetch wrapper）
│   ├── package.json
│   └── tsconfig.json
├── start_app.sh                           # 起動スクリプト（Docker Compose + マイグレーション）
├── docker-compose.yml
├── CLAUDE.md
├── docs/
└── README.md
```

---

## 2. データフローとレイヤー責務

### リクエスト処理の流れ

```
クライアント（Next.js）
    │  HTTP Request
    ▼
api/ (Router)
    │  ・api/schemas/ でバリデーション
    │  ・Depends(get_db) でDBセッション注入
    ▼
services/
    │  ・ビジネスロジック担当
    │  ・next_scheduled_date の計算（recurrence_service.py）
    │  ・core/date.py を呼んで論理日付を取得
    ▼
crud/
    │  ・SQLAlchemy でDB操作
    ▼
models/ → PostgreSQL
```

### レイヤーごとの責務

| レイヤー | 責務 | 触れるもの |
|---|---|---|
| `api/` | ルーティング・バリデーション・レスポンス整形 | `api/schemas/`, `services/` |
| `services/` | ビジネスロジック・ドメインルール | `crud/`, `crud/schemas/`, `core/date.py` |
| `crud/` | DB CRUD 操作 | `models/`, `crud/schemas/` |
| `core/date.py` | 論理的な今日の算出（横断的ユーティリティ） | どのレイヤーからも参照可 |
| `models/` | テーブル定義 | PostgreSQL |
| `main.py` | アプリケーションエントリポイント・`/health` エンドポイント | `api/` ルーター |

### スキーマの役割分担

| 場所 | 役割 | 例 |
|---|---|---|
| `api/schemas/` | クライアントとのやり取り | `VideoCreateRequest`, `VideoResponse` |
| `crud/schemas/` | CRUD 関数への入力型 | `VideoInsert`, `VideoFilter` |

### `core/date.py` の責務

論理的な今日の算出を担う横断的ユーティリティ。`/today`・`/overdue`・`next_scheduled_date` 計算など複数のサービスから参照される。

```python
def get_logical_today(day_change_time, timezone) -> date:
    """
    現在時刻(UTC) → ユーザーのtimezone変換 → day_change_time比較
    現在時刻 >= day_change_time → 当日
    現在時刻 <  day_change_time → 前日
    """
```

### `recurrence_service.py` の責務

| recurrence_type | 計算方法 |
|---|---|
| `none` | 自動計算なし（手動のみ） |
| `daily` | last_performed_date + 1日 |
| `weekly` | last_performed_date 以降の最も近い VideoWeekday の曜日 |
| `interval` | last_performed_date + interval_days |

---

## 3. 環境設定

### `config.py` の構成

`.env` ファイルは使用しない。デフォルト値を pydantic-settings に直書きし、`ENV` 環境変数で切り替える。

```python
import os
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    """全環境共通の設定"""
    ENV: str
    DATABASE_URL: str


class DevSettings(AppSettings):
    """開発環境用設定"""
    ENV: str = "development"
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/youtube_todo"


class TestSettings(AppSettings):
    """テスト環境用設定"""
    ENV: str = "test"
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/youtube_todo_test"


def get_settings() -> AppSettings:
    env = os.getenv("ENV", "development")
    if env == "test":
        return TestSettings()
    return DevSettings()


settings = get_settings()
```

### 環境ごとのDB

| 環境 | DB名 | 切り替え方法 |
|---|---|---|
| 開発 | `youtube_todo` | デフォルト（ENV未設定） |
| テスト | `youtube_todo_test` | `ENV=test` を設定 |

---

## 4. テスト戦略

### テスト構成

```
tests/
├── unit/                          # DB不要のテスト
│   ├── test_config.py             # 環境設定
│   ├── test_models.py             # ORM モデル定義
│   ├── test_types.py              # Enum 型
│   ├── test_unique_constraints.py # ユニーク制約
│   └── test_schemas/              # スキーマバリデーション
│       ├── test_recurrence_schema.py
│       ├── test_tag_schema.py
│       ├── test_todo_history_schema.py
│       ├── test_user_schema.py
│       ├── test_video_schema.py
│       └── test_workout_history_schema.py
├── integration/                   # テスト用PostgreSQL必須
│   ├── test_cascade.py            # カスケード削除
│   ├── test_constraints.py        # DB 制約（UniqueConstraint, CheckConstraint）
│   ├── test_triggers.py           # DB トリガー
│   └── test_crud/                 # CRUD 操作
│       ├── test_crud_recurrence.py
│       ├── test_crud_tag.py
│       ├── test_crud_todo_history.py
│       ├── test_crud_user.py
│       ├── test_crud_video.py
│       ├── test_crud_video_tag.py
│       └── test_crud_workout_history.py
├── test_imports.py                # モジュールインポート
└── conftest.py                    # DBセッション・テスト用フィクスチャ
```

### テスト方針

| テスト種別 | 対象 | DB | 優先度 |
|---|---|---|---|
| Unit | スキーマバリデーション、モデル定義、Enum 型、環境設定 | 不要 | **高** |
| Integration | CRUD 操作、DB 制約、カスケード削除、トリガー | テスト用PostgreSQL | **高** |

### 重点テスト対象

**Unit Test（スキーマバリデーション）** — 全モデルの入力バリデーションを網羅

- 各スキーマの必須フィールド・型チェック
- Enum 型（RecurrenceType, DayOfWeek, TodoStatus）の値バリデーション
- 環境設定（DevSettings / TestSettings）の切り替え

**Integration Test（CRUD・制約）** — DB 層の動作を実 DB で検証

- 全テーブルの CRUD 操作（Create / Read / Update / Delete）
- ユニーク制約（TodoHistory, WorkoutHistory, Tag, VideoTag 等）
- チェック制約（VideoRecurrence の interval_days）
- カスケード削除の連鎖動作
- DB トリガーの動作

### テスト実行

```bash
# テスト用DBを使ったテスト（backend ディレクトリで実行）
cd backend && ENV=test uv run pytest ./tests/

# Unit テストのみ
cd backend && ENV=test uv run pytest ./tests/unit/

# Integration テストのみ
cd backend && ENV=test uv run pytest ./tests/integration/
```

---

## 5. ローカル開発環境

Docker Compose で PostgreSQL とバックエンドを起動する。`start_app.sh` で一括起動が可能。

```yaml
# docker-compose.yml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: youtube_todo
    ports:
      - "5432:5432"
    volumes:
      - db_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d youtube_todo"]
      interval: 5s
      timeout: 3s
      retries: 5

  backend:
    build:
      context: ./backend
    environment:
      ENV: development
      DATABASE_URL: postgresql://user:password@db:5432/youtube_todo
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy

volumes:
  db_data:
```

```bash
# 一括起動（推奨）— DB + バックエンド起動 → テスト用DB作成 → マイグレーション実行
./start_app.sh

# 停止
docker compose down

# 停止 + データ削除
docker compose down -v
```
