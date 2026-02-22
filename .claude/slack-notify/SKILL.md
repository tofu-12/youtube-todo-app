---
name: slack-notify
description: "Auto-check at every work stopping point: run `test -f .claude/slack-notify.enabled` - if enabled, detect language via `cat .claude/slack-notify.lang 2>/dev/null || echo en`, then always send a summary (work/plan/conversation) via `python .claude/slack-notify/scripts/notify_slack.py -m '...'`. Toggle with /slack-on /slack-off /slack-lang-en /slack-lang-jp."
---

# Slack Notify Skill

Send a Slack notification when work reaches a natural stopping point.

## What counts as a "stopping point"

- You have completed file edits and reported results to the user
- You have finished brainstorming / planning and the design is approved
- You are about to hand back to the user with no pending actions

## Step 1: Check if notifications are enabled

```bash
test -f .claude/slack-notify.enabled && echo "enabled" || echo "disabled"
```

If the output is `disabled`, do nothing and continue.

## Step 2: Detect language

```bash
cat .claude/slack-notify.lang 2>/dev/null || echo "en"
```

| Output | Language |
|---|---|
| `en` (or file missing) | English |
| `jp` | Japanese |

## Step 3: Detect mode

| Mode | Condition | Action |
|---|---|---|
| `auto_edit` | Used Edit / Write / Bash for code changes | Send work summary |
| `plan` | Only planning / design discussion, no code changes | Send plan summary |
| `default` | Research, Q&A, conversation only | Send conversation summary |

## Step 4: Send the notification

```bash
python .claude/slack-notify/scripts/notify_slack.py -m "<summary>"
```

## Message format

Write 2–4 lines in the detected language:
- What was done (`auto_edit`) or decided (`plan`)
- Key files changed or key decisions made

**auto_edit — jp:**
```
認証機能を実装しました。
変更ファイル: src/auth.py, tests/test_auth.py
```

**auto_edit — en:**
```
Implemented authentication feature.
Changed files: src/auth.py, tests/test_auth.py
```

**plan — jp:**
```
Slack通知機能の設計が完了しました。
アーキテクチャ: SKILL.md + scripts/notify_slack.py + /slack-on|off コマンド
```

**plan — en:**
```
Completed design for Slack notification feature.
Architecture: SKILL.md + scripts/notify_slack.py + /slack-on|off commands
```

**default — jp:**
```
認証エラーの原因について調査・回答しました。
原因: トークンの有効期限切れ。対処法: 再発行して環境変数を更新。
```

**default — en:**
```
Investigated and answered a question about authentication errors.
Cause: expired token. Fix: reissue and update the environment variable.
```

## Setup

```bash
cp .claude/slack-notify/assets/config.json.template .claude/slack-notify/assets/config.json
# Fill in SLACK_BOT_TOKEN and SLACK_CHANNEL_ID
```
