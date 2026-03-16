"""Async Slack client wrapper with lazy initialization."""

from __future__ import annotations

from slack_sdk.web.async_client import AsyncWebClient

from mcp_slack.config import SlackConfig

_client: AsyncWebClient | None = None
_config: SlackConfig | None = None


def get_config() -> SlackConfig:
    """Return cached SlackConfig, creating on first call."""
    global _config
    if _config is None:
        _config = SlackConfig.from_env()
    return _config


def get_client() -> AsyncWebClient:
    """Return cached AsyncWebClient, creating on first call."""
    global _client
    if _client is None:
        cfg = get_config()
        _client = AsyncWebClient(token=cfg.bot_token)
    return _client
