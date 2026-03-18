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
- ユーザー設定（日付切り替え時刻）

---

## 2. 用語定義

| 用語 | 定義 |
|---|---|
| ワークアウト | 動画を見て行う運動セッション |
| タグ | 動画を分類するラベル（例: "背中", "有酸素"） |
| 有効期限 | ワークアウト記録の保持期限（日数で指定） |
| スケジュール | 動画ごとの「最終実施日」と「次回予定日」の組み合わせ |
| 日付切り替え時刻 | 「今日」の始まりとみなす時刻。例: 04:00 に設定すると、03:59 まで前日の TODO が表示される |
| 論理的な今日 | 日付切り替え時刻を基準に算出した「現在の日付」 |
| 繰り返しルール | 動画ごとに設定する実施頻度（none / daily / weekly / interval） |

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

- **機能:** 動画に繰り返しルールを設定し、最終実施日から次回予定日を自動計算する
- **入力:** 動画 URL、繰り返しルール（Video に設定）、最終実施日
- **次回予定日の計算ルール:**

| recurrence_type | 計算方法 |
|---|---|
| `none` | 自動計算なし（手動設定のみ） |
| `daily` | 最終実施日 + 1日 |
| `weekly` | 最終実施日以降の最も近い指定曜日 |
| `interval` | 最終実施日 + N日 |

### 3.4 本日の TODO リスト表示

- **機能:** 当日実施すべきワークアウトを一覧表示する
- **表示条件:** 次回日付 <= 論理的な今日 かつ 有効期限内
- **論理的な今日の算出:** 現在時刻 >= ユーザーの日付切り替え時刻 → 当日、現在時刻 < 日付切り替え時刻 → 前日

---

## 4. Post-MVP 機能要件（将来拡張）

### 4.1 YouTube 動画メタデータ取得・保存

- **概要:** YouTube Data API を用いて動画のメタデータを取得し、DB に保存する
- **取得対象:** タイトル、動画時間（秒）、概要欄テキスト、サムネイル URL
- **保存先:** `Video` テーブルに以下カラムを追加

| カラム | 型 | 説明 |
|---|---|---|
| title | string | 動画タイトル |
| duration_seconds | int | 動画時間（秒） |
| description | string | 概要欄テキスト |
| thumbnail_url | string | サムネイル URL |

- **更新タイミング:** 動画登録時に自動取得。手動での再取得も可能とする

### 4.2 ユーザー認証（Auth0）

- FE: Auth0 ログイン画面（Auth.js 経由）
- BE: JWT トークン検証

### 4.3 習慣度スコア

- **概要:** 動画ごとに習慣化の度合いを 0〜1 のスコアで管理する
- **データソース:** `TodoHistory` の `status`（completed / skipped）の履歴
- **モデル:** NN 等を用いて過去の習慣度スコアと TodoHistory から次回実施有無を予測し、実際の結果（completed / skipped）をもとにスコアを更新する
- **更新タイミング:** TODO 完了/スキップ記録時にバックグラウンドで再計算
- **保存先:** `Video` テーブルに `habit_score`（float, 0〜1）カラムを追加

### 4.4 ユーザーレベル・経験値（RPG 風）

- **概要:** ワークアウトの実施や習慣度スコアの向上に応じて経験値（XP）が付与され、レベルが上がる RPG 風の成長システム
- **保存先:** `User` テーブルに以下カラムを追加

| カラム | 型 | 説明 |
|---|---|---|
| level | int | 現在のレベル（1〜） |
| experience_points | int | 累積経験値（XP） |

- **XP 付与ロジック（案）:**
  - TODO を `completed` にした場合: 基本 XP を付与
  - 習慣度スコアが高い動画を完了した場合: ボーナス XP を付与
  - 連続実施（streak）達成時: ボーナス XP を付与
- **レベルアップ:** 累積 XP が閾値を超えるとレベルアップ（閾値は別途設計）
- **XP 計算への習慣度スコアの活用:** 習慣度スコア（4.3）が低い動画を完了した場合に高い XP を付与するなど、難易度に応じたメリハリをつける

### 4.5 AI 要約機能（動画サマリー）

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

### User（ユーザー）

| フィールド | 型 | Nullable | 説明 |
|---|---|---|---|
| id | UUID | NO | 主キー |
| day_change_time | time | NO | 日付切り替え時刻（デフォルト: 00:00） |
| timezone | string | NO | IANA タイムゾーン名（デフォルト: `Asia/Tokyo`） |
| created_at | datetime | NO | 登録日時（UTC） |
| updated_at | datetime | NO | 更新日時（UTC） |

> MVP は 1 ユーザー固定のため、初回アクセス時に自動生成する。

### Video（動画）

| フィールド | 型 | Nullable | 説明 |
|---|---|---|---|
| id | UUID | NO | 主キー |
| user_id | UUID | NO | FK（User, CASCADE DELETE） |
| name | string | NO | 動画名（ユーザーが任意に命名） |
| url | string | NO | YouTube URL |
| comment | string | YES | メモ（任意） |
| last_performed_date | date | YES | 最終実施日（論理日付、NULL = 未実施） |
| next_scheduled_date | date | YES | 次回予定日（論理日付、VideoRecurrence から自動計算） |
| created_at | datetime | NO | 登録日時（UTC） |
| updated_at | datetime | NO | 更新日時（UTC） |

### VideoRecurrence（繰り返しルール）

Video と 1:1。繰り返し設定を Video テーブルから分離して管理する。

| フィールド | 型 | Nullable | 説明 |
|---|---|---|---|
| id | UUID | NO | 主キー |
| user_id | UUID | NO | FK（User, CASCADE DELETE） |
| video_id | UUID | NO | FK（Video, CASCADE DELETE, UNIQUE） |
| recurrence_type | enum | NO | `none` / `daily` / `weekly` / `interval` |
| interval_days | int | YES | interval 時の日数（他は NULL） |
| created_at | datetime | NO | 登録日時（UTC） |
| updated_at | datetime | NO | 更新日時（UTC） |

> チェック制約: `recurrence_type = 'interval'` の場合、`interval_days IS NOT NULL AND interval_days >= 1` が必須

### VideoWeekday（週次曜日設定）

VideoRecurrence と 1:多。`recurrence_type = weekly` の場合のみ使用。

| フィールド | 型 | Nullable | 説明 |
|---|---|---|---|
| id | UUID | NO | 主キー |
| user_id | UUID | NO | FK（User, CASCADE DELETE） |
| video_recurrence_id | UUID | NO | FK（VideoRecurrence, CASCADE DELETE） |
| day_of_week | enum | NO | `MON` / `TUE` / `WED` / `THU` / `FRI` / `SAT` / `SUN` |
| created_at | datetime | NO | 登録日時（UTC） |
| updated_at | datetime | NO | 更新日時（UTC） |

### Tag（タグ）

タグを独立テーブルで管理する。Video とは VideoTag（中間テーブル）を介した多対多リレーション。

| フィールド | 型 | Nullable | 説明 |
|---|---|---|---|
| id | UUID | NO | 主キー |
| user_id | UUID | NO | FK（User, CASCADE DELETE） |
| name | string(50) | NO | タグ名 |
| created_at | datetime | NO | 登録日時（UTC） |
| updated_at | datetime | NO | 更新日時（UTC） |

> ユニーク制約: `(user_id, name)` — 同一ユーザー内でタグ名は一意

### VideoTag（動画タグ中間テーブル）

Video と Tag の多対多リレーションを管理する中間テーブル。

| フィールド | 型 | Nullable | 説明 |
|---|---|---|---|
| id | UUID | NO | 主キー |
| user_id | UUID | NO | FK（User, CASCADE DELETE） |
| video_id | UUID | NO | FK（Video, CASCADE DELETE） |
| tag_id | UUID | NO | FK（Tag, CASCADE DELETE） |
| created_at | datetime | NO | 登録日時（UTC） |
| updated_at | datetime | NO | 更新日時（UTC） |

> ユニーク制約: `(video_id, tag_id)` — 同一動画に同じタグの重複登録を防止

### TodoHistory（TODO履歴）

| フィールド | 型 | Nullable | 説明 |
|---|---|---|---|
| id | UUID | NO | 主キー |
| user_id | UUID | NO | FK（User, CASCADE DELETE） |
| video_id | UUID | NO | FK（Video, CASCADE DELETE） |
| scheduled_date | date | NO | TODO として表示された日付（論理日付） |
| status | enum | NO | `completed` / `skipped` |
| created_at | datetime | NO | 登録日時（UTC） |
| updated_at | datetime | NO | 更新日時（UTC） |

> ユニーク制約: `(video_id, scheduled_date)` — 同一動画・同一日付の重複記録を防止

### WorkoutHistory（ワークアウト履歴）

| フィールド | 型 | Nullable | 説明 |
|---|---|---|---|
| id | UUID | NO | 主キー |
| user_id | UUID | NO | FK（User, CASCADE DELETE） |
| video_id | UUID | NO | FK（Video, CASCADE DELETE） |
| performed_date | date | NO | 実施日（論理日付） |
| performed_at | datetime | NO | 実施日時（UTC） |
| expires_date | date | NO | 有効期限日（論理日付、この日まで有効） |
| created_at | datetime | NO | 登録日時（UTC） |
| updated_at | datetime | NO | 更新日時（UTC） |

> ユニーク制約: `(video_id, performed_date)` — 同一動画・同一日付の重複記録を防止

### カスケード削除ルール

すべてのテーブルは `user_id` を外部キーとして持ち、ユーザーごとにデータを分離する。外部キーにはカスケード削除を設定し、親レコード削除時に関連データを自動削除する。

| 親テーブル | 子テーブル | 削除時の動作 |
|---|---|---|
| User | Video, VideoRecurrence, VideoWeekday, Tag, VideoTag, TodoHistory, WorkoutHistory | CASCADE DELETE |
| Video | VideoRecurrence, VideoTag, TodoHistory, WorkoutHistory | CASCADE DELETE |
| VideoRecurrence | VideoWeekday | CASCADE DELETE |
| Tag | VideoTag | CASCADE DELETE |

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

### VideoRecurrence（繰り返しルール）

| メソッド | パス | 説明 |
|---|---|---|
| GET | /api/videos/{id}/recurrence | 繰り返しルール取得 |
| PUT | /api/videos/{id}/recurrence | 繰り返しルール作成・更新 |
| DELETE | /api/videos/{id}/recurrence | 繰り返しルール削除 |

### WorkoutHistories

| メソッド | パス | 説明 |
|---|---|---|
| GET | /api/workout-histories | 履歴一覧（有効期限フィルタ） |
| POST | /api/workout-histories | 履歴記録 |
| DELETE | /api/workout-histories/{id} | 履歴削除 |

### TodoHistories

| メソッド | パス | 説明 |
|---|---|---|
| GET | /api/todo-histories | TODO履歴一覧（日付フィルタ対応） |
| POST | /api/todo-histories | TODO完了/スキップを記録 |
| DELETE | /api/todo-histories/{id} | 記録を取り消す |

### Today's TODO

| メソッド | パス | 説明 |
|---|---|---|
| GET | /api/today | 本日の TODO 一覧 |
| GET | /api/overdue | 予定日超過の未実施動画一覧 |

### User Settings

| メソッド | パス | 説明 |
|---|---|---|
| GET | /api/settings | ユーザー設定取得 |
| PUT | /api/settings | ユーザー設定更新（日付切り替え時刻など） |

### Health Check

| メソッド | パス | 説明 |
|---|---|---|
| GET | /health | ヘルスチェック（サーバー死活監視） |

---

## 8. 画面一覧（MVP）

| 画面名 | URL | 内容 |
|---|---|---|
| TODO リスト | / | 本日実施すべき動画一覧 |
| 未実施リスト | /overdue | 予定日を過ぎても未実施の動画一覧 |
| 動画登録 | /videos/new | URL・タグ・コメント入力フォーム |
| 動画一覧 | /videos | 登録済み動画の一覧 |
| 動画詳細 | /videos/{id} | 動画情報・履歴・スケジュール |

---

## 9. 制約・前提条件

- YouTube URL は `youtube.com/watch?v=xxx` および `youtu.be/xxx` 形式を受け付ける
- `recurrence_type = daily` の場合、毎日 TODO に表示される
- `recurrence_type = weekly` の場合、VideoWeekday に 1 件以上登録が必要
- `recurrence_type = interval` の場合、`interval_days` は 1 以上の整数
- `recurrence_type = none` の場合、`next_scheduled_date` は手動設定のみ
- 日付切り替え時刻は `HH:MM` 形式（00:00〜23:59）で指定する
- 日付切り替え時刻のデフォルト値は `00:00`（深夜0時）
- 論理的な今日の算出はサーバーサイドで行い、`/api/today` のレスポンスに反映する
- タイムゾーンは IANA タイムゾーン名（例: `Asia/Tokyo`, `UTC`）で指定する
- `day_change_time` はユーザーの `timezone` 基準で評価する
- `datetime` 型フィールドは UTC で保存し、表示時にユーザーの `timezone` へ変換する
- `date` 型フィールドはユーザーの論理日付をそのまま保存する（UTC 変換なし）
- `timezone` は原則変更不可。変更した場合、既存の `date` フィールドはすべてそのまま保持する（再計算しない）
