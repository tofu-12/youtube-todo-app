#!/bin/bash
# install.sh - One-command installer for slack-notify skill

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="${1:-$(pwd)}"

echo "Installing slack-notify to: $PROJECT_DIR"

# Update settings.json (add Stop hook)
python3 "$SKILL_DIR/scripts/setup/update_settings.py" \
    "$PROJECT_DIR/.claude/settings.json"

# Update CLAUDE.md (add notification rules)
python3 "$SKILL_DIR/scripts/setup/update_claude_md.py" \
    "$PROJECT_DIR/CLAUDE.md"

# Make send_pending.sh executable
chmod +x "$SKILL_DIR/scripts/send_pending.sh"

# Copy slash commands to .claude/commands/
mkdir -p "$PROJECT_DIR/.claude/commands"
cp "$SKILL_DIR/commands/"*.md "$PROJECT_DIR/.claude/commands/" 2>/dev/null || true

echo ""
echo "Done! Next step:"
echo "  cp $SKILL_DIR/assets/config.json.template $SKILL_DIR/assets/config.json"
echo "  # Fill in SLACK_BOT_TOKEN and SLACK_CHANNEL_ID"
