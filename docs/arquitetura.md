---
title: Architecture — MCP Slack
kind: architecture
area: engineering
project: mcp-slack
collection: mcp-slack
owner: maintainers
status: current
canonical: docs/arquitetura.md
globalRef: qmd://mcp-slack/docs/arquitetura.md
reviewCadenceDays: 90
lastReviewedAt: 2026-09-28
sourceRefs:
  - pyproject.toml
  - src/mcp_slack
related:
  - docs/fluxos-negocio.md
  - docs/operacao.md
  - docs/index.md
supersedes: []
supersededBy: []
sensitivity: public
---
# Architecture

## Components

| Component | Responsibility |
| --- | --- |
| `server.py` | Creates the FastMCP server, imports the messaging module and starts stdio transport. |
| `config.py` | Reads the required bot token and optional default channel from environment variables. |
| `client.py` | Lazily creates and caches the Slack configuration and asynchronous Web API client. |
| `tools/messaging.py` | Implements channel listing, channel history, channel-name resolution and message posting. |

## Request path

```text
MCP client
  -> FastMCP tool registration
  -> environment-backed SlackConfig
  -> cached AsyncWebClient
  -> Slack Web API
  -> formatted text response
```

The server has no application database. Slack remains the system of record;
only configuration and the SDK client are retained in process memory.

## Authentication and scope boundary

`SLACK_BOT_TOKEN` enters through the environment and is passed to the Slack SDK.
The bot sees only conversations and operations allowed by its OAuth scopes and
workspace membership. The tool-to-scope matrix is maintained in `README.md`.

## Read and write boundary

Channel listing and history calls are observational. `slack_post_message` calls
Slack immediately and changes external state. Explicit MCP safety annotations
are tracked in
[Issue #13](https://github.com/antonio-mello-ai/mcp-slack/issues/13), while the
explicit-destination contract is tracked in Issue #9.

## Resilience boundary

The current client is created without custom retry handlers. Rate-limit and
method-aware retry behavior are tracked in
[Issue #2](https://github.com/antonio-mello-ai/mcp-slack/issues/2). Stable,
redacted error mapping is tracked in
[Issue #10](https://github.com/antonio-mello-ai/mcp-slack/issues/10).

## Known structural gaps

- Channel discovery and name resolution are unbounded; see Issue #11.
- Non-public conversation ID handling does not match the documented contract;
  see Issue #8.
- Responses are formatted strings rather than typed MCP content; see Issue #14.
- The version hook references a removed file; see Issue #12.
