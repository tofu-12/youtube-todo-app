# youtube-todo-app 要件定義書

## 1. プロジェクト概要

### 1.1 目的・背景

YouTube の筋トレ動画を活用したトレーニング管理を効率化するため、動画 URL をタグ・コメント付きで保存し、ワークアウトの履歴とスケジュールを管理する Todo アプリを開発する。

### 1.2 対象ユーザー

個人利用（1 ユーザー想定）。MVP はローカル環境で動作し、認証なし。

### 1.3 MVP スコープ

- YouTube URL のタグ・コメント付き保存
- ワークアウト履歴の記録（有効期限付き）
- ワークアウトスケジュール管理
- 本日の TODO リスト表示

---

## 2. 用語定義

| 用語 | 定義 |
|---|---|
| ワークアウト | 動画を見て行う運動セッション |
| タグ | 動画を分類するラベル（例: "背中", "有酸素"） |
| 有効期限 | ワークアウト記録の保持期限（日数で指定） |
| スケジュール | 動画ごとの「最終実施日」と「次回予定日」の組み合わせ |

---

## 3. MVP 機能要件

### 3.1 YouTube URL 管理

- **機能:** YouTube URL をタグ・コメント付きで保存する
- **入力:** URL（必須）、タグ（複数可）、コメント（任意）
- **出力:** 保存済み URL 一覧の表示

### 3.2 ワークアウト履歴記録

- **機能:** ワークアウトを実施した記録を残す（有効期限付き）
- **入力:** 実施日、対象動画 URL、有効期限（日数）
- **出力:** 有効期限内の履歴一覧

### 3.3 ワークアウトスケジュール管理

- **機能:** 「最後に行った日」「次回予定日」を設定する
- **入力:** 動画 URL、最終実施日、次回日付 または `"daily"`
- **ルール:** `"daily"` の場合は毎日 TODO に表示

### 3.4 本日の TODO リスト表示

- **機能:** 当日実施すべきワークアウトを一覧表示する
- **表示条件:** 次回日付 <= 今日 かつ 有効期限内

---

## 4. Post-MVP 機能要件（将来拡張）

### 4.1 ユーザー認証（Auth0）

- FE: Auth0 ログイン画面（Auth.js 経由）
- BE: JWT トークン検証

### 4.2 AI 要約機能

| 選択肢 | 概要 |
|---|---|
| A: 字幕テキスト → LLM 要約 | youtube-transcript-api で字幕取得後に要約 |
| B: 説明文 → LLM 要約 | YouTube API で概要欄テキストを取得後に要約 |
| C: Gemini API（URL 直接） | URL 指定のみで要約（最もシンプル） |

---

## 5. 非機能要件

- API レスポンスタイム < 500ms（通常リクエスト）
- MVP はローカル動作（認証なし、1 ユーザー想定）

---

## 6. ドメインモデル

### Video（動画）

| フィールド | 型 | 説明 |
|---|---|---|
| id | UUID | 主キー |
| url | string | YouTube URL |
| tags | string[] | タグ一覧（最大 10 件） |
| comment | string | メモ（任意） |
| created_at | datetime | 登録日時 |

### WorkoutHistory（ワークアウト履歴）

| フィールド | 型 | 説明 |
|---|---|---|
| id | UUID | 主キー |
| video_id | UUID | 対象動画 |
| performed_at | date | 実施日 |
| expires_at | date | 有効期限 |

### WorkoutSchedule（スケジュール）

| フィールド | 型 | 説明 |
|---|---|---|
| id | UUID | 主キー |
| video_id | UUID | 対象動画 |
| last_performed_at | date | 最終実施日 |
| next_scheduled_at | date または "daily" | 次回予定 |

---

## 7. API エンドポイント一覧（MVP）

### Videos

| メソッド | パス | 説明 |
|---|---|---|
| GET | /api/videos | 動画一覧取得 |
| POST | /api/videos | 動画登録 |
| GET | /api/videos/{id} | 動画詳細取得 |
| PUT | /api/videos/{id} | 動画更新 |
| DELETE | /api/videos/{id} | 動画削除 |

### WorkoutHistories

| メソッド | パス | 説明 |
|---|---|---|
| GET | /api/histories | 履歴一覧（有効期限フィルタ） |
| POST | /api/histories | 履歴記録 |
| DELETE | /api/histories/{id} | 履歴削除 |

### WorkoutSchedules

| メソッド | パス | 説明 |
|---|---|---|
| GET | /api/schedules | スケジュール一覧 |
| POST | /api/schedules | スケジュール作成 |
| PUT | /api/schedules/{id} | スケジュール更新 |

### Today's TODO

| メソッド | パス | 説明 |
|---|---|---|
| GET | /api/today | 本日の TODO 一覧 |

---

## 8. 画面一覧（MVP）

| 画面名 | URL | 内容 |
|---|---|---|
| TODO リスト | / | 本日実施すべき動画一覧 |
| 動画登録 | /videos/new | URL・タグ・コメント入力フォーム |
| 動画一覧 | /videos | 登録済み動画の一覧 |
| 動画詳細 | /videos/{id} | 動画情報・履歴・スケジュール |

---

## 9. 制約・前提条件

- YouTube URL は `youtube.com/watch?v=xxx` および `youtu.be/xxx` 形式を受け付ける
- タグは 1 動画につき最大 10 個
- `"daily"` スケジュールは毎日 TODO に表示される
