#!/bin/bash
# send_alert.sh - Called by Claude Code Notification hook.
# Sends a Slack alert when Claude needs user action (permission or idle).

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STATE_DIR="$SCRIPT_DIR/../state"
CONFIG_FILE="$SCRIPT_DIR/../assets/config.sh"

[ -f "$STATE_DIR/enabled" ] || exit 0
[ -f "$CONFIG_FILE" ] || { echo "Error: config.sh not found at $CONFIG_FILE"; exit 1; }

# shellcheck source=/dev/null
source "$CONFIG_FILE"

[ -n "$SLACK_BOT_TOKEN" ] || { echo "Error: SLACK_BOT_TOKEN is not set in config.sh"; exit 1; }
[ -n "$SLACK_CHANNEL_ID" ] || { echo "Error: SLACK_CHANNEL_ID is not set in config.sh"; exit 1; }

INPUT=$(cat)
NOTIFICATION_TYPE=$(echo "$INPUT" | jq -r '.notification_type // empty')
MESSAGE=$(echo "$INPUT" | jq -r '.message // empty')

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel 2>/dev/null || echo "")}"
REPO_NAME="$(basename "${PROJECT_DIR:-unknown}")"
BRANCH="$(git -C "${PROJECT_DIR:-$SCRIPT_DIR}" symbolic-ref --short HEAD 2>/dev/null || echo "unknown")"
TIMESTAMP="$(date '+%Y-%m-%d %H:%M')"

case "$NOTIFICATION_TYPE" in
    permission_prompt)
        HEADER="Claude needs your permission"
        COLOR="#E8B84B"
        ;;
    idle_prompt)
        HEADER="Claude is waiting for your input"
        COLOR="#E8B84B"
        ;;
    elicitation_dialog)
        HEADER="Claude is asking for your input"
        COLOR="#E8B84B"
        ;;
    *)
        exit 0
        ;;
esac

PAYLOAD=$(cat <<EOF
{
  "channel": "$SLACK_CHANNEL_ID",
  "attachments": [{
    "color": "$COLOR",
    "blocks": [
      {
        "type": "header",
        "text": {"type": "plain_text", "text": "$HEADER"}
      },
      {
        "type": "section",
        "text": {"type": "mrkdwn", "text": "$MESSAGE"}
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
