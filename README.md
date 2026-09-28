# mcp-slack

MCP server for Slack integration, built with FastMCP. Provides tools for listing channels, reading messages, and posting to Slack.

Channel listing and reading are observational. `slack_post_message` performs an
external write immediately when invoked, so callers should confirm the resolved
destination and message content before calling it.

## Install

```bash
pip install -e ".[dev]"
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SLACK_BOT_TOKEN` | Yes | Bot User OAuth Token (`xoxb-...`) |
| `SLACK_DEFAULT_CHANNEL` | No | Current fallback channel when `slack_post_message` receives an empty channel |

Copy `.env.example` to `.env` and fill in your values.

## Tools

| Tool | Description |
|------|-------------|
| `slack_list_channels` | List all channels accessible by the bot |
| `slack_read_channel(channel, limit?)` | Read last N messages from a channel (default: 20, max: 100) |
| `slack_post_message(channel, text)` | Send a message to a channel |

The `channel` parameter accepts a channel name (without `#`) or a public-channel
ID beginning with `C`. Correct handling for other Slack conversation ID types is
tracked in [Issue #8](https://github.com/antonio-mello-ai/mcp-slack/issues/8).

## Slack App Setup

1. Go to [api.slack.com/apps](https://api.slack.com/apps) and create a new app
2. Under **OAuth & Permissions**, add the required **Bot Token Scopes** for the tools you want to use:

   | Tool | Required Bot Scopes |
   |------|---------------------|
   | `slack_list_channels` | `channels:read`, `groups:read` |
   | `slack_read_channel` | `channels:history`, `groups:history` |
   | `slack_post_message` | `chat:write` |
   
   *Note: Private-channel access requires the corresponding `groups:*` scopes
   and bot membership. Direct-message and multi-party conversation support is
   not currently implemented; the supported conversation contract is tracked
   in [Issue #8](https://github.com/antonio-mello-ai/mcp-slack/issues/8).*

3. Install the app to your workspace
4. Copy the **Bot User OAuth Token** (`xoxb-...`) to `SLACK_BOT_TOKEN`
5. Invite the bot to channels it should access: `/invite @your-bot-name`

### Troubleshooting: `missing_scope` Error
If a tool fails with a `missing_scope` error, it means the bot doesn't have the necessary permissions to perform that action. Check the error message to see which scope is missing, cross-reference it with the table above, and add the missing scope in your Slack App's **OAuth & Permissions** page. (Remember to reinstall the app to your workspace after changing scopes!)

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

## License

MIT

## Documentation and roadmap

- [Current product flows](docs/fluxos-negocio.md)
- [Architecture](docs/arquitetura.md)
- [Operations](docs/operacao.md)
- [Documentation index](docs/index.md)
- [Open roadmap items](https://github.com/antonio-mello-ai/mcp-slack/issues)

Priorities live in GitHub Issues and Projects. Delivery history lives in closed
Issues, pull requests and GitHub Releases.
