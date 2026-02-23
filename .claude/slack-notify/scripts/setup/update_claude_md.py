"""Append Slack Notification Rules to CLAUDE.md (idempotent)."""
import sys
from pathlib import Path

NOTIFICATION_RULES = """
---

# Slack Notification Rules

Before ending every response, check if notifications are enabled:

```bash
test -f .claude/slack-notify/state/enabled && echo "enabled" || echo "disabled"
```

If **enabled**, write a 2-4 line summary to `.claude/slack-notify/state/pending_message`:

```bash
.claude/slack-notify/scripts/write_pending.sh "<line1>\\n<line2>"
```

- Detect language from `state/lang` (default: `en` if missing)
- Follow the message format in `.claude/slack-notify/SKILL.md`
- The Stop hook sends this file automatically — do NOT call notify_slack.py directly
"""


def main():
    """Append notification rules to CLAUDE.md if not already present."""
    path = Path(sys.argv[1])
    content = path.read_text() if path.exists() else ""

    if "Slack Notification Rules" in content:
        print("CLAUDE.md: Notification rules already present, skipping")
        return

    path.write_text(content.rstrip() + "\n" + NOTIFICATION_RULES)
    print("CLAUDE.md: Notification rules added")


if __name__ == "__main__":
    main()
