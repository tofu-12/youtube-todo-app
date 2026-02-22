"""Tests for .claude/slack-notify/notify_slack.py"""
import importlib.util
import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

SCRIPT_PATH = Path(__file__).parents[2] / ".claude" / "slack-notify" / "scripts" / "notify_slack.py"


def _make_fake_response(ok: bool, error: str = "unknown_error") -> MagicMock:
    """Create a mock urllib response returning a Slack API result."""
    fake = MagicMock()
    fake.__enter__ = lambda s: s
    fake.__exit__ = MagicMock(return_value=False)
    payload = {"ok": ok}
    if not ok:
        payload["error"] = error
    fake.read.return_value = json.dumps(payload).encode()
    return fake


def _load_module(token: str = "xoxb-test", channel: str = "C123"):
    """Load notify_slack module with patched config."""
    config_mock = {"SLACK_BOT_TOKEN": token, "SLACK_CHANNEL_ID": channel}
    with patch("builtins.open", MagicMock(return_value=MagicMock(
        __enter__=lambda s, *a: MagicMock(read=lambda: json.dumps(config_mock)),
        __exit__=MagicMock(return_value=False),
    ))):
        with patch("json.load", return_value=config_mock):
            spec = importlib.util.spec_from_file_location("notify_slack", SCRIPT_PATH)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
    return module


def test_script_exists():
    """notify_slack.py must exist at the expected path."""
    assert SCRIPT_PATH.exists(), f"Script not found: {SCRIPT_PATH}"


def test_send_message_calls_slack_api():
    """send_message_to_slack must POST to Slack API with correct payload and headers."""
    module = _load_module()

    with patch("urllib.request.urlopen", return_value=_make_fake_response(True)) as mock_urlopen:
        with patch("builtins.print") as mock_print:
            module.send_message_to_slack("hello world")

    mock_urlopen.assert_called_once()
    assert "hello world" in mock_print.call_args[0][0]
    req = mock_urlopen.call_args[0][0]
    body = json.loads(req.data)
    assert body["text"] == "hello world"
    assert body["channel"] == "C123"
    assert req.get_header("Authorization") == "Bearer xoxb-test"


def test_send_message_prints_error_on_failure():
    """send_message_to_slack must print error when Slack returns ok=false."""
    module = _load_module()

    with patch("urllib.request.urlopen", return_value=_make_fake_response(False, "invalid_auth")):
        with patch("builtins.print") as mock_print:
            module.send_message_to_slack("test")

    mock_print.assert_called_once()
    assert "invalid_auth" in mock_print.call_args[0][0]


def test_newline_escape_converted_in_main():
    """Literal \\n passed via CLI must be converted to actual newline before sending."""
    module = _load_module()

    with patch("urllib.request.urlopen", return_value=_make_fake_response(True)) as mock_urlopen:
        with patch("sys.argv", ["notify_slack.py", "-m", "line1\\nline2"]):
            module.main()

    req = mock_urlopen.call_args[0][0]
    body = json.loads(req.data)
    assert body["text"] == "line1\nline2"
