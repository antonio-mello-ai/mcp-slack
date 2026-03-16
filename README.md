# mcp-slack

MCP server for Slack integration, built with FastMCP. Provides tools for listing channels, reading messages, and posting to Slack.

## Install

```bash
pip install -e ".[dev]"
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SLACK_BOT_TOKEN` | Yes | Bot User OAuth Token (`xoxb-...`) |
| `SLACK_DEFAULT_CHANNEL` | No | Fallback channel for `slack_post_message` |

Copy `.env.example` to `.env` and fill in your values.

## Tools

| Tool | Description |
|------|-------------|
| `slack_list_channels` | List all channels accessible by the bot |
| `slack_read_channel(channel, limit?)` | Read last N messages from a channel (default: 20, max: 100) |
| `slack_post_message(channel, text)` | Send a message to a channel |

The `channel` parameter accepts either a channel name (without `#`) or a Slack channel ID.

## Slack App Setup

1. Go to [api.slack.com/apps](https://api.slack.com/apps) and create a new app
2. Under **OAuth & Permissions**, add these **Bot Token Scopes**:
   - `channels:read`
   - `channels:history`
   - `chat:write`
   - `groups:read`
   - `groups:history`
3. Install the app to your workspace
4. Copy the **Bot User OAuth Token** (`xoxb-...`) to `SLACK_BOT_TOKEN`
5. Invite the bot to channels it should access: `/invite @your-bot-name`

## Usage

### Standalone

```bash
mcp-slack
```

### Claude Desktop config

```json
{
  "mcpServers": {
    "slack": {
      "command": "mcp-slack",
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-your-token"
      }
    }
  }
}
```

## Development

```bash
pip install -e ".[dev]"
ruff check src/ tests/
ruff format src/ tests/
pytest
```
