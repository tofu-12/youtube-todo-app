# slack-notify

A self-contained Claude Code skill that sends a Slack notification when Claude stops working.

## How it works

Two hooks send Slack notifications automatically:

| Hook | Script | Trigger |
|---|---|---|
| `Stop` | `send_complete.sh` | Claudeが作業を終了したとき |
| `Notification` | `send_alert.sh` | 権限ダイアログ表示時 / アイドル待ち時 |

`state/enabled` が存在しない場合、通知は送信されません。

## Installation

1. Copy `.claude/slack-notify/` to your project's `.claude/` directory
2. Run the installer (updates `settings.json` and copies commands):
   ```bash
   bash .claude/slack-notify/install.sh
   ```
   > Requires `jq`. Without it, the installer prints manual instructions.
3. Copy the config template and fill in credentials:
   ```bash
   cp .claude/slack-notify/assets/config.sh.template \
      .claude/slack-notify/assets/config.sh
   # Edit config.sh: set SLACK_BOT_TOKEN and SLACK_CHANNEL_ID
   ```
4. Enable notifications:
   ```
   /slack-on
   ```

> **Note:** Invite your Slack bot to the target channel with `/invite @your-bot-name`.

## Commands

| Command | Description |
|---|---|
| `/slack-on` | Enable notifications |
| `/slack-off` | Disable notifications |

## File structure

```
slack-notify/
├── README.md
├── install.sh
├── .gitignore
├── commands/
│   ├── slack-on.md
│   └── slack-off.md
├── scripts/
│   ├── send_complete.sh   ← Stop hook: 作業完了通知
│   └── send_alert.sh          ← Notification hook: 権限/アイドル通知
├── assets/
│   ├── config.sh.template     ← credentials template
│   └── config.sh              ← gitignored (real credentials)
└── state/
    ├── .gitkeep
    └── enabled                ← exists when notifications are ON
```

## Requirements

- `curl` (standard on macOS/Linux)
- A Slack app with `chat:write` permission and a Bot Token (`xoxb-...`)
