#!/bin/bash
# install.sh - One-command installer for slack-notify skill

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="${1:-$(pwd)}"
SETTINGS_FILE="$PROJECT_DIR/.claude/settings.json"

echo "Installing slack-notify to: $PROJECT_DIR"

# Copy slash commands to .claude/commands/
mkdir -p "$PROJECT_DIR/.claude/commands"
cp "$SKILL_DIR/commands/"*.md "$PROJECT_DIR/.claude/commands/" 2>/dev/null || true

if [ ! -f "$SETTINGS_FILE" ] || ! command -v jq &>/dev/null; then
    echo ""
    echo "  [Manual step] Add to $SETTINGS_FILE:"
    echo '  "hooks": {'
    echo '    "Stop": [{ "hooks": [{ "type": "command", "command": "bash \"$CLAUDE_PROJECT_DIR\"/.claude/slack-notify/scripts/send_complete.sh" }] }],'
    echo '    "Notification": [{ "matcher": "permission_prompt|idle_prompt|elicitation_dialog", "hooks": [{ "type": "command", "command": "bash \"$CLAUDE_PROJECT_DIR\"/.claude/slack-notify/scripts/send_alert.sh" }] }]'
    echo '  }'
    echo ""
    echo "  Also add to permissions.allow:"
    echo '  "Bash(test -f .claude/slack-notify/state/enabled*)"'
    echo '  "Bash(mkdir -p .claude/slack-notify/state && touch .claude/slack-notify/state/enabled)"'
    echo '  "Bash(rm -f .claude/slack-notify/state/enabled)"'
    echo ""
    echo "  And to permissions.deny:"
    echo '  "Read(./.claude/slack-notify/assets/config.sh)"'
else
    STOP_CMD='bash "$CLAUDE_PROJECT_DIR"/.claude/slack-notify/scripts/send_complete.sh'
    ALERT_CMD='bash "$CLAUDE_PROJECT_DIR"/.claude/slack-notify/scripts/send_alert.sh'

    UPDATED=$(jq \
        --arg stop "$STOP_CMD" \
        --arg alert "$ALERT_CMD" '
        # Stop hook (append if not already present)
        if ([.hooks.Stop // [] | .[].hooks[]? | select(.command == $stop)] | length) == 0 then
            .hooks.Stop += [{"hooks": [{"type": "command", "command": $stop}]}]
        else . end |

        # Notification hook (append if not already present)
        if ([.hooks.Notification // [] | .[].hooks[]? | select(.command == $alert)] | length) == 0 then
            .hooks.Notification += [{"matcher": "permission_prompt|idle_prompt|elicitation_dialog", "hooks": [{"type": "command", "command": $alert}]}]
        else . end |

        # permissions.allow
        .permissions.allow = (
            (.permissions.allow // []) +
            ["Bash(test -f .claude/slack-notify/state/enabled*)",
             "Bash(mkdir -p .claude/slack-notify/state && touch .claude/slack-notify/state/enabled)",
             "Bash(rm -f .claude/slack-notify/state/enabled)"]
            | unique
        ) |

        # permissions.deny
        .permissions.deny = (
            (.permissions.deny // []) +
            ["Read(./.claude/slack-notify/assets/config.sh)"]
            | unique
        )
    ' "$SETTINGS_FILE")

    echo "$UPDATED" > "$SETTINGS_FILE"
    echo "Updated: $SETTINGS_FILE"
fi

echo ""
echo "Done! Next steps:"
echo ""
echo "  1. Copy config template and fill in credentials:"
echo "     cp $SKILL_DIR/assets/config.sh.template $SKILL_DIR/assets/config.sh"
echo "     # Edit config.sh: set SLACK_BOT_TOKEN and SLACK_CHANNEL_ID"
echo ""
echo "  2. Enable notifications:"
echo "     /slack-on"
