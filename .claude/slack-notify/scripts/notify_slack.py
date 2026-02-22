"""Send a message to Slack via Bot Token.

Usage:
    python notify_slack.py --message "your message"
    python notify_slack.py -m "line1\\nline2"   # \\n converted to newline

Config:
    Reads SLACK_BOT_TOKEN and SLACK_CHANNEL_ID from
    ../assets/config.json relative to this script.
"""
import argparse
import json
import urllib.error
import urllib.request
from pathlib import Path


_CONFIG_PATH = Path(__file__).parent.parent / "assets" / "config.json"

try:
    with open(_CONFIG_PATH) as _f:
        _config = json.load(_f)
except FileNotFoundError:
    raise FileNotFoundError(
        f"config.json not found at {_CONFIG_PATH}. "
        "Copy assets/config.json.template to assets/config.json and fill in your credentials."
    )

_SLACK_BOT_TOKEN = _config["SLACK_BOT_TOKEN"]
_SLACK_CHANNEL_ID = _config["SLACK_CHANNEL_ID"]

SLACK_API_URL = "https://slack.com/api/chat.postMessage"


def send_message_to_slack(message: str) -> None:
    """Send a plain-text message to the configured Slack channel."""
    data = json.dumps({"channel": _SLACK_CHANNEL_ID, "text": message}).encode()
    req = urllib.request.Request(
        SLACK_API_URL,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {_SLACK_BOT_TOKEN}",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
    except urllib.error.URLError as e:
        print(f"Error: failed to reach Slack API: {e.reason}")
        return
    if result.get("ok"):
        print(f"Message sent: {message}")
    else:
        print(f"Error: {result.get('error')}")


def main() -> None:
    """Entry point: parse --message argument and send to Slack."""
    parser = argparse.ArgumentParser(description="Send a message to Slack")
    parser.add_argument(
        "--message", "-m",
        type=str,
        required=True,
        help="Message to send to Slack",
    )
    args = parser.parse_args()
    message = args.message.replace("\\n", "\n")
    send_message_to_slack(message)


if __name__ == "__main__":
    main()
