"""Messaging tools: list channels, read messages, post messages."""

from __future__ import annotations

from mcp_slack.client import get_client, get_config
from mcp_slack.server import mcp


@mcp.tool()
async def slack_list_channels() -> str:
    """List all Slack channels accessible by the bot.

    Returns a formatted list of channel names with their IDs and topics.
    """
    client = get_client()
    channels: list[dict] = []
    cursor: str | None = None

    while True:
        kwargs: dict = {"types": "public_channel,private_channel", "limit": 200}
        if cursor:
            kwargs["cursor"] = cursor

        response = await client.conversations_list(**kwargs)
        channels.extend(response.get("channels", []))

        cursor = response.get("response_metadata", {}).get("next_cursor")
        if not cursor:
            break

    if not channels:
        return "No channels found."

    lines: list[str] = []
    for ch in sorted(channels, key=lambda c: c.get("name", "")):
        name = ch.get("name", "unknown")
        cid = ch.get("id", "")
        topic = ch.get("topic", {}).get("value", "")
        member_count = ch.get("num_members", "?")
        prefix = "🔒" if ch.get("is_private") else "#"
        line = f"{prefix} {name} ({cid}) — {member_count} members"
        if topic:
            line += f" — {topic}"
        lines.append(line)

    return f"Found {len(channels)} channels:\n\n" + "\n".join(lines)


@mcp.tool()
async def slack_read_channel(channel: str, limit: int = 20) -> str:
    """Read the last N messages from a Slack channel.

    Args:
        channel: Channel name (without #) or channel ID.
        limit: Number of messages to retrieve (default: 20, max: 100).
    """
    client = get_client()
    limit = max(1, min(limit, 100))

    channel_id = await _resolve_channel_id(channel)

    response = await client.conversations_history(channel=channel_id, limit=limit)
    messages = response.get("messages", [])

    if not messages:
        return f"No messages found in <#{channel_id}>."

    lines: list[str] = []
    for msg in reversed(messages):
        user = msg.get("user", "unknown")
        text = msg.get("text", "")
        ts = msg.get("ts", "")
        lines.append(f"[{ts}] <@{user}>: {text}")

    return f"Last {len(messages)} messages from <#{channel_id}>:\n\n" + "\n".join(lines)


@mcp.tool()
async def slack_post_message(channel: str, text: str) -> str:
    """Send a message to a Slack channel.

    Args:
        channel: Channel name (without #) or channel ID.
        text: The message text to send. Supports Slack markdown.
    """
    client = get_client()
    config = get_config()

    resolved_channel = channel or config.default_channel
    if not resolved_channel:
        return "Error: No channel specified and SLACK_DEFAULT_CHANNEL is not set."

    channel_id = await _resolve_channel_id(resolved_channel)

    response = await client.chat_postMessage(channel=channel_id, text=text)
    ts = response.get("ts", "unknown")

    return f"Message sent to <#{channel_id}> (ts: {ts})."


async def _resolve_channel_id(channel: str) -> str:
    """Resolve a channel name to its ID. If already an ID, return as-is.

    Args:
        channel: Channel name (without #) or channel ID.

    Returns:
        The Slack channel ID.

    Raises:
        ValueError: If the channel cannot be found.
    """
    if channel.startswith("C") and len(channel) >= 9 and channel[1:].isalnum():
        return channel

    client = get_client()
    cursor: str | None = None

    while True:
        kwargs: dict = {"types": "public_channel,private_channel", "limit": 200}
        if cursor:
            kwargs["cursor"] = cursor

        response = await client.conversations_list(**kwargs)
        for ch in response.get("channels", []):
            if ch.get("name") == channel:
                return ch["id"]

        cursor = response.get("response_metadata", {}).get("next_cursor")
        if not cursor:
            break

    raise ValueError(
        f"Channel '{channel}' not found. Use the channel ID or exact name."
    )
