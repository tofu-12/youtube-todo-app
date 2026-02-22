#!/bin/bash
# send_pending.sh - Called by Claude Code Stop hook.
# Reads state/pending_message and sends it to Slack, then deletes the file.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STATE_DIR="$SCRIPT_DIR/../state"
ENABLED_FILE="$STATE_DIR/enabled"
PENDING_FILE="$STATE_DIR/pending_message"
NOTIFY_SCRIPT="$SCRIPT_DIR/notify_slack.py"

[ -f "$ENABLED_FILE" ] || exit 0
[ -f "$PENDING_FILE" ] || exit 0

message=$(cat "$PENDING_FILE")
rm -f "$PENDING_FILE"
python3 "$NOTIFY_SCRIPT" -m "$message"
