"""Slack configuration loaded from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SlackConfig:
    """Immutable Slack configuration."""

    bot_token: str
    default_channel: str | None = None

    @classmethod
    def from_env(cls) -> SlackConfig:
        """Build config from environment variables.

        Raises:
            ValueError: If SLACK_BOT_TOKEN is missing or empty.
        """
        bot_token = os.environ.get("SLACK_BOT_TOKEN", "").strip()
        if not bot_token:
            raise ValueError(
                "SLACK_BOT_TOKEN environment variable is required. "
                "Create a Slack App and set the Bot User OAuth Token (xoxb-...)."
            )

        default_channel = os.environ.get("SLACK_DEFAULT_CHANNEL", "").strip() or None

        return cls(bot_token=bot_token, default_channel=default_channel)
