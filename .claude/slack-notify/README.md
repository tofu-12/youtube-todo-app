# slack-notify

A self-contained Claude Code skill that sends Slack notifications when Claude judges work is complete.

## Installation

Copy the entire folder into your project or global Claude skills directory:

```bash
# Project-scoped
cp -r slack-notify /path/to/your-project/.claude/slack-notify

# Global (works across all projects)
cp -r slack-notify ~/.claude/skills/slack-notify
```

Then copy the slash commands to activate them:

```bash
cp .claude/slack-notify/commands/*.md .claude/commands/
```

## Setup

1. Copy the config template and fill in your credentials:

```bash
cp .claude/slack-notify/assets/config.json.template .claude/slack-notify/assets/config.json
```

2. Edit `assets/config.json`:

```json
{
    "SLACK_BOT_TOKEN": "xoxb-your-token-here",
    "SLACK_CHANNEL_ID": "C0123456789"
}
```

> **Note:** Invite your Slack bot to the target channel with `/invite @your-bot-name`.

## Activation

For Claude to auto-check at stopping points, add one line to your `CLAUDE.md`:

```markdown
At natural stopping points, follow .claude/slack-notify/SKILL.md for notification instructions.
```

Or install globally (`~/.claude/skills/slack-notify`) so the skill is always available.

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
