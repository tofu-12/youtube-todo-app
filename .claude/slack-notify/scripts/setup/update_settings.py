"""Add Stop hook and allow permissions to .claude/settings.json (idempotent)."""
import json
import sys
from pathlib import Path

HOOK_COMMAND = (
    '"$CLAUDE_PROJECT_DIR"'
    '/.claude/slack-notify/scripts/send_pending.sh'
)

ALLOW_ENTRIES = [
    "Bash(test -f .claude/slack-notify/state/enabled*)",
    "Bash(cat .claude/slack-notify/state/lang*)",
    "Bash(.claude/slack-notify/scripts/write_pending.sh *)",
]


def add_stop_hook(settings: dict) -> bool:
    """Add Stop hook entry if not already present. Returns True if changed."""
    hooks = settings.setdefault("hooks", {})
    stop_hooks = hooks.setdefault("Stop", [])

    already_set = any(
        h.get("command") == HOOK_COMMAND
        for entry in stop_hooks
        for h in entry.get("hooks", [])
    )
    if already_set:
        print("settings.json: Stop hook already set, skipping")
        return False

    stop_hooks.append({
        "hooks": [{"type": "command", "command": HOOK_COMMAND}]
    })
    print("settings.json: Stop hook added")
    return True


def add_allow_permissions(settings: dict) -> bool:
    """Add slack-notify Bash permissions to allow list. Returns True if changed."""
    permissions = settings.setdefault("permissions", {})
    allow = permissions.setdefault("allow", [])

    changed = False
    for entry in ALLOW_ENTRIES:
        if entry not in allow:
            allow.append(entry)
            print(f"settings.json: allow added: {entry}")
            changed = True
        else:
            print(f"settings.json: allow already set, skipping: {entry}")
    return changed


def main():
    """Update settings.json with Stop hook and allow permissions."""
    path = Path(sys.argv[1])
    settings = json.loads(path.read_text()) if path.exists() else {}

    hook_changed = add_stop_hook(settings)
    allow_changed = add_allow_permissions(settings)

    if hook_changed or allow_changed:
        path.write_text(json.dumps(settings, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
