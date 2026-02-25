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

# Update settings.json with Stop hook
HOOK_COMMAND='bash "$CLAUDE_PROJECT_DIR"/.claude/slack-notify/scripts/send_complete.sh'
if [ -f "$SETTINGS_FILE" ] && command -v jq &>/dev/null; then
    ALREADY=$(jq --arg cmd "$HOOK_COMMAND" \
        '[.hooks.Stop // [] | .[].hooks[]? | select(.command == $cmd)] | length' \
        "$SETTINGS_FILE")
    if [ "$ALREADY" -gt 0 ]; then
        echo "Stop hook already installed, skipping."
    else
        UPDATED=$(jq --arg cmd "$HOOK_COMMAND" \
            '.hooks.Stop += [{"hooks": [{"type": "command", "command": $cmd}]}]' \
            "$SETTINGS_FILE")
        echo "$UPDATED" > "$SETTINGS_FILE"
        echo "Updated: $SETTINGS_FILE"
    fi
else
    echo ""
    echo "  [Manual step] Add the Stop hook to $SETTINGS_FILE:"
    echo '  "hooks": { "Stop": [{ "hooks": [{ "type": "command", "command": "bash \"$CLAUDE_PROJECT_DIR\"/.claude/slack-notify/scripts/send_complete.sh" }] }] }'
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
