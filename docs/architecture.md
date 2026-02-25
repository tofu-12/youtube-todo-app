# アーキテクチャ設計書

作成日: 2026-02-24

---

## 1. リポジトリ構成

モノレポ構成。バックエンド（FastAPI）とフロントエンド（Next.js）を1リポジトリで管理する。

```
youtube-todo-app/
├── backend/
│   ├── app/
│   │   ├── api/                     ← FastAPI Routers（リソース単位）
│   │   │   ├── schemas/             ← APIエンドポイント用スキーマ（Request/Response）
│   │   │   │   ├── video.py
│   │   │   │   └── ...
│   │   │   ├── videos.py
│   │   │   ├── recurrences.py
│   │   │   ├── workout_histories.py
│   │   │   ├── todo_histories.py
│   │   │   ├── today.py             ← /today, /overdue
│   │   │   └── settings.py
│   │   ├── services/                ← ビジネスロジック
│   │   │   ├── video_service.py
│   │   │   ├── recurrence_service.py  ← next_scheduled_date 計算
│   │   │   └── settings_service.py
│   │   ├── crud/                    ← DB操作（SQLAlchemy）
│   │   │   ├── schemas/             ← CRUD操作用スキーマ（内部データ構造）
│   │   │   │   ├── video.py
│   │   │   │   └── ...
│   │   │   ├── video.py
│   │   │   ├── recurrence.py
│   │   │   └── ...
│   │   ├── models/                  ← SQLAlchemy ORM モデル
│   │   │   ├── user.py
│   │   │   ├── video.py
│   │   │   ├── video_recurrence.py
│   │   │   ├── video_weekday.py
│   │   │   ├── todo_history.py
│   │   │   └── workout_history.py
│   │   ├── core/
│   │   │   ├── config.py            ← 環境別設定（DevSettings / TestSettings）
│   │   │   ├── database.py          ← SQLAlchemy engine / Session
│   │   │   ├── dependencies.py      ← Depends(get_db) 等
│   │   │   └── date.py              ← 論理的な今日の算出（横断的ユーティリティ）
│   │   └── main.py                      ← FastAPI app インスタンス
│   ├── alembic/                     ← マイグレーション
│   ├── tests/
│   │   ├── unit/
│   │   │   ├── test_date.py
│   │   │   └── test_recurrence.py
│   │   ├── integration/
│   │   │   ├── test_videos.py
│   │   │   ├── test_today.py
│   │   │   └── ...
│   │   └── conftest.py
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── app/                     ← Next.js App Router
│   │   │   ├── page.tsx             ← / TODOリスト（Server Component）
│   │   │   ├── overdue/page.tsx
│   │   │   ├── videos/
│   │   │   │   ├── page.tsx
│   │   │   │   ├── new/page.tsx
│   │   │   │   └── [id]/page.tsx
│   │   │   └── layout.tsx
│   │   ├── components/              ← 再利用コンポーネント
│   │   │   ├── TodoItem.tsx         ← 'use client'（操作あり）
│   │   │   └── VideoForm.tsx        ← 'use client'（フォーム）
│   │   └── lib/
│   │       └── api.ts               ← API クライアント（fetch wrapper）
│   ├── package.json
│   └── tsconfig.json
├── docker-compose.yml
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

### `core/config.py` の構成

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
├── unit/
│   ├── test_date.py          ← core/date.py（論理日付算出）
│   └── test_recurrence.py    ← recurrence_service.py（次回予定日計算）
├── integration/
│   ├── test_videos.py        ← API + DB 結合テスト
│   ├── test_today.py
│   └── ...
└── conftest.py               ← DBセッション・テスト用フィクスチャ
```

### テスト方針

| テスト種別 | 対象 | DB | 優先度 |
|---|---|---|---|
| Unit | `core/date.py`, `services/` のロジック | 不要（モック） | **高** |
| Integration | `api/` エンドポイント全体 | テスト用PostgreSQL | 中 |

### 重点テスト対象

**`core/date.py`（論理日付）** — エッジケースが多いためUnit Testを重点的に書く

- `day_change_time = 04:00` のとき、03:59 → 前日になること
- `day_change_time = 04:00` のとき、04:00 → 当日になること
- タイムゾーンが `Asia/Tokyo` / `UTC` で正しく動くこと

**`recurrence_service.py`（次回予定日）** — recurrence_type 別に網羅テスト

- `none`: next_scheduled_date が変化しないこと
- `daily`: last_performed_date + 1日になること
- `weekly`: 正しい曜日に飛ぶこと（週またぎも含む）
- `interval`: last_performed_date + N日になること

### テスト実行

```bash
# 通常テスト（開発環境）
uv run pytest ./tests/

# テスト用DBを使ったテスト
ENV=test uv run pytest ./tests/
```

---

## 5. ローカル開発環境

Docker Compose で PostgreSQL・FastAPI・Next.js をまとめて起動する。

```yaml
# docker-compose.yml（概要）
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_DB: youtube_todo

  backend:
    build: ./backend
    command: uv run uvicorn app.main:app --reload
    ports:
      - "8000:8000"
    depends_on:
      - db

  frontend:
    build: ./frontend
    command: npm run dev
    ports:
      - "3000:3000"
```

```bash
# 起動コマンド
docker compose up
```
