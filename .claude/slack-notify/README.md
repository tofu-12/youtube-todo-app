# slack-notify

A self-contained Claude Code skill that sends Slack notifications when Claude judges work is complete.

## Installation

1. Copy `.claude/slack-notify/` to your project's `.claude/` directory
2. Run the installer:
   ```bash
   bash .claude/slack-notify/install.sh
   ```
3. Copy the config template and fill in credentials:
   ```bash
   cp .claude/slack-notify/assets/config.json.template \
      .claude/slack-notify/assets/config.json
   # Edit config.json: set SLACK_BOT_TOKEN and SLACK_CHANNEL_ID
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
| `/slack-lang-en` | Set message language to English (default) |
| `/slack-lang-jp` | Set message language to Japanese |

## How it works

1. At every work stopping point, Claude checks `.claude/slack-notify/state/enabled`
2. If enabled, Claude detects the session mode:
   - **auto_edit** — code was written or changed → sends a work summary
   - **plan** — planning/design only → sends a plan summary
   - **default** — research/Q&A only → sends a conversation summary
3. Claude reads `.claude/slack-notify/state/lang` to determine the message language
4. Sends the message via `scripts/notify_slack.py`

## File structure

```
slack-notify/
├── README.md                   # This file
├── SKILL.md                    # Skill definition (front matter + instructions)
├── .gitignore                  # Excludes assets/config.json
├── commands/
│   ├── slack-on.md
│   ├── slack-off.md
│   ├── slack-lang-en.md
│   └── slack-lang-jp.md
├── scripts/
│   └── notify_slack.py         # Standard library only, no dependencies
├── state/
│   └── .gitkeep
└── assets/
    └── config.json.template    # Credentials template
```

## State files

These files are created at runtime and excluded from git via `.claude/.gitignore`:

| File | Purpose |
|---|---|
| `.claude/slack-notify/state/enabled` | Exists when notifications are ON |
| `.claude/slack-notify/state/lang` | Contains `en` or `jp` (default: `en`) |

## Requirements

- Python 3.x (standard library only — no pip installs needed)
- A Slack app with `chat:write` permission and a Bot Token (`xoxb-...`)
