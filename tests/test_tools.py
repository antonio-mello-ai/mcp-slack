"""Tests for Slack MCP tools with mocked Slack API responses."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

import mcp_slack.client as client_module
from mcp_slack.tools.messaging import (
    _resolve_channel_id,
    slack_list_channels,
    slack_post_message,
    slack_read_channel,
)


@pytest.fixture(autouse=True)
def _reset_client():
    """Reset the cached client and config before each test."""
    client_module._client = None
    client_module._config = None
    yield
    client_module._client = None
    client_module._config = None


def _make_mock_client() -> AsyncMock:
    """Create a mock AsyncWebClient."""
    return AsyncMock()


def _patch_get_client(mock_client: AsyncMock):
    """Patch get_client to return the given mock."""
    return patch("mcp_slack.tools.messaging.get_client", return_value=mock_client)


def _patch_get_config(**overrides):
    """Patch get_config to return a mock config."""
    from mcp_slack.config import SlackConfig

    cfg = SlackConfig(
        bot_token="xoxb-fake-token",
        default_channel=overrides.get("default_channel"),
    )
    return patch("mcp_slack.tools.messaging.get_config", return_value=cfg)


class TestSlackListChannels:
    async def test_returns_channels(self):
        mock_client = _make_mock_client()
        mock_client.conversations_list.return_value = {
            "channels": [
                {
                    "id": "C123",
                    "name": "general",
                    "topic": {"value": "General discussion"},
                    "num_members": 42,
                    "is_private": False,
                },
                {
                    "id": "C456",
                    "name": "random",
                    "topic": {"value": ""},
                    "num_members": 10,
                    "is_private": False,
                },
            ],
            "response_metadata": {"next_cursor": ""},
        }

        with _patch_get_client(mock_client):
            result = await slack_list_channels()

        assert "Found 2 channels" in result
        assert "general" in result
        assert "C123" in result
        assert "random" in result

    async def test_no_channels(self):
        mock_client = _make_mock_client()
        mock_client.conversations_list.return_value = {
            "channels": [],
            "response_metadata": {"next_cursor": ""},
        }

        with _patch_get_client(mock_client):
            result = await slack_list_channels()

        assert "No channels found" in result

    async def test_private_channel_prefix(self):
        mock_client = _make_mock_client()
        mock_client.conversations_list.return_value = {
            "channels": [
                {
                    "id": "C789",
                    "name": "secret",
                    "topic": {"value": ""},
                    "num_members": 3,
                    "is_private": True,
                },
            ],
            "response_metadata": {"next_cursor": ""},
        }

        with _patch_get_client(mock_client):
            result = await slack_list_channels()

        assert "\U0001f512 secret" in result


class TestSlackReadChannel:
    async def test_reads_messages(self):
        mock_client = _make_mock_client()
        mock_client.conversations_history.return_value = {
            "messages": [
                {"user": "U123", "text": "Hello world", "ts": "1700000002.000"},
                {"user": "U456", "text": "Hi there", "ts": "1700000001.000"},
            ],
        }

        with _patch_get_client(mock_client):
            result = await slack_read_channel(channel="C123ABC00", limit=10)

        assert "Hello world" in result
        assert "Hi there" in result
        mock_client.conversations_history.assert_called_once_with(
            channel="C123ABC00", limit=10
        )

    async def test_no_messages(self):
        mock_client = _make_mock_client()
        mock_client.conversations_history.return_value = {"messages": []}

        with _patch_get_client(mock_client):
            result = await slack_read_channel(channel="C123ABC00")

        assert "No messages found" in result

    async def test_limit_clamped(self):
        mock_client = _make_mock_client()
        mock_client.conversations_history.return_value = {"messages": []}

        with _patch_get_client(mock_client):
            await slack_read_channel(channel="C123ABC00", limit=999)

        mock_client.conversations_history.assert_called_once_with(
            channel="C123ABC00", limit=100
        )

    async def test_resolves_channel_name(self):
        mock_client = _make_mock_client()
        mock_client.conversations_list.return_value = {
            "channels": [{"id": "C999ZZZ00", "name": "general"}],
            "response_metadata": {"next_cursor": ""},
        }
        mock_client.conversations_history.return_value = {
            "messages": [{"user": "U1", "text": "test", "ts": "1700000000.000"}],
        }

        with _patch_get_client(mock_client):
            result = await slack_read_channel(channel="general")

        mock_client.conversations_history.assert_called_once_with(
            channel="C999ZZZ00", limit=20
        )
        assert "test" in result


class TestSlackPostMessage:
    async def test_posts_message(self):
        mock_client = _make_mock_client()
        mock_client.chat_postMessage.return_value = {"ts": "1700000003.000"}

        with _patch_get_client(mock_client), _patch_get_config():
            result = await slack_post_message(
                channel="C123ABC00", text="Hello from MCP"
            )

        assert "Message sent" in result
        assert "1700000003.000" in result
        mock_client.chat_postMessage.assert_called_once_with(
            channel="C123ABC00", text="Hello from MCP"
        )

    async def test_uses_default_channel(self):
        mock_client = _make_mock_client()
        mock_client.conversations_list.return_value = {
            "channels": [{"id": "CDEFAULT0", "name": "alerts"}],
            "response_metadata": {"next_cursor": ""},
        }
        mock_client.chat_postMessage.return_value = {"ts": "1700000004.000"}

        with (
            _patch_get_client(mock_client),
            _patch_get_config(default_channel="alerts"),
        ):
            result = await slack_post_message(channel="", text="fallback test")

        assert "Message sent" in result

    async def test_no_channel_no_default(self):
        mock_client = _make_mock_client()

        with _patch_get_client(mock_client), _patch_get_config():
            result = await slack_post_message(channel="", text="oops")

        assert "Error" in result
        assert "SLACK_DEFAULT_CHANNEL" in result


class TestResolveChannelId:
    async def test_returns_id_as_is(self):
        mock_client = _make_mock_client()

        with _patch_get_client(mock_client):
            result = await _resolve_channel_id("C123ABC00")

        assert result == "C123ABC00"
        mock_client.conversations_list.assert_not_called()

    async def test_resolves_name(self):
        mock_client = _make_mock_client()
        mock_client.conversations_list.return_value = {
            "channels": [
                {"id": "CABC12300", "name": "dev"},
                {"id": "CDEF45600", "name": "general"},
            ],
            "response_metadata": {"next_cursor": ""},
        }

        with _patch_get_client(mock_client):
            result = await _resolve_channel_id("general")

        assert result == "CDEF45600"

    async def test_raises_on_not_found(self):
        mock_client = _make_mock_client()
        mock_client.conversations_list.return_value = {
            "channels": [],
            "response_metadata": {"next_cursor": ""},
        }

        with (
            _patch_get_client(mock_client),
            pytest.raises(ValueError, match="not found"),
        ):
            await _resolve_channel_id("nonexistent")
