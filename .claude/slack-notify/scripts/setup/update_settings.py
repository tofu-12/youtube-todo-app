"""Add Stop hook to .claude/settings.json (idempotent)."""
import json
import sys
from pathlib import Path

HOOK_COMMAND = (
    '"$CLAUDE_PROJECT_DIR"'
    '/.claude/slack-notify/scripts/send_pending.sh'
)


def main():
    """Add Stop hook entry to settings.json if not already present."""
    path = Path(sys.argv[1])
    settings = json.loads(path.read_text()) if path.exists() else {}

    hooks = settings.setdefault("hooks", {})
    stop_hooks = hooks.setdefault("Stop", [])

    already_set = any(
        h.get("command") == HOOK_COMMAND
        for entry in stop_hooks
        for h in entry.get("hooks", [])
    )
    if already_set:
        print("settings.json: Stop hook already set, skipping")
        return

    stop_hooks.append({
        "hooks": [{"type": "command", "command": HOOK_COMMAND}]
    })
    path.write_text(json.dumps(settings, indent=2, ensure_ascii=False) + "\n")
    print("settings.json: Stop hook added")


if __name__ == "__main__":
    main()
