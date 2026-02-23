#!/bin/bash
# write_pending.sh - Write a message to state/pending_message for deferred Slack notification.
# Usage: write_pending.sh "message content"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STATE_DIR="$SCRIPT_DIR/../state"

printf '%s' "$1" > "$STATE_DIR/pending_message" && echo "✓ pending_message saved"
