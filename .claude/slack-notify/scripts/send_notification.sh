#!/bin/bash
# send_notification.sh - Called by Claude Code Stop hook.
# Sends a fixed notification to Slack via curl.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STATE_DIR="$SCRIPT_DIR/../state"
CONFIG_FILE="$SCRIPT_DIR/../assets/config.sh"

[ -f "$STATE_DIR/enabled" ] || exit 0
[ -f "$CONFIG_FILE" ] || { echo "Error: config.sh not found at $CONFIG_FILE"; exit 1; }

# shellcheck source=/dev/null
source "$CONFIG_FILE"

[ -n "$SLACK_BOT_TOKEN" ] || { echo "Error: SLACK_BOT_TOKEN is not set in config.sh"; exit 1; }
[ -n "$SLACK_CHANNEL_ID" ] || { echo "Error: SLACK_CHANNEL_ID is not set in config.sh"; exit 1; }

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel 2>/dev/null || echo "")}"
REPO_NAME="$(basename "${PROJECT_DIR:-unknown}")"
BRANCH="$(git -C "${PROJECT_DIR:-$SCRIPT_DIR}" symbolic-ref --short HEAD 2>/dev/null || echo "unknown")"
TIMESTAMP="$(date '+%Y-%m-%d %H:%M')"

PAYLOAD=$(cat <<EOF
{
  "channel": "$SLACK_CHANNEL_ID",
  "attachments": [{
    "color": "#2EB67D",
    "blocks": [
      {
        "type": "header",
        "text": {"type": "plain_text", "text": "Claude has stopped working"}
      },
      {
        "type": "section",
        "fields": [
          {"type": "mrkdwn", "text": "*Repo*\n$REPO_NAME"},
          {"type": "mrkdwn", "text": "*Branch*\n$BRANCH"},
          {"type": "mrkdwn", "text": "*Time*\n$TIMESTAMP"}
        ]
      }
    ]
  }]
}
EOF
)

RESPONSE=$(curl -s -X POST https://slack.com/api/chat.postMessage \
    -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD")

if [ $? -ne 0 ]; then
    echo "Error: curl failed"
    exit 1
fi

case "$RESPONSE" in
    *'"ok":true'*) ;;
    *) echo "Error: Slack API returned an error: $RESPONSE"; exit 1 ;;
esac
