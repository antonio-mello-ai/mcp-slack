---
title: Product flows — MCP Slack
kind: guide
area: product
project: mcp-slack
collection: mcp-slack
owner: maintainers
status: current
canonical: docs/fluxos-negocio.md
globalRef: qmd://mcp-slack/docs/fluxos-negocio.md
reviewCadenceDays: 90
lastReviewedAt: 2026-09-28
sourceRefs:
  - README.md
  - src/mcp_slack/tools/messaging.py
related:
  - docs/arquitetura.md
  - docs/operacao.md
  - docs/index.md
supersedes: []
supersededBy: []
sensitivity: public
---
# Product flows

MCP Slack exposes three tools to an MCP client. The operator supplies a Slack
Bot User OAuth Token and the client invokes tools through the stdio server.

## List channels

`slack_list_channels` calls `conversations.list` for public and private channels
visible to the bot. It follows Slack cursors, sorts the combined result by name
and returns formatted names, IDs, topics, member counts and privacy markers.

The current implementation accumulates the complete visible inventory before
responding. Bounded pagination and reuse of channel discovery are tracked in
[Issue #11](https://github.com/antonio-mello-ai/mcp-slack/issues/11).

## Read channel messages

`slack_read_channel` accepts a channel name or recognized channel ID, clamps the
requested limit to 1–100 and loads one `conversations.history` page. It formats
the returned messages from oldest to newest using Slack timestamps and raw user
IDs.

- User display-name resolution is tracked in
  [Issue #4](https://github.com/antonio-mello-ai/mcp-slack/issues/4).
- Reading thread replies is tracked in
  [Issue #1](https://github.com/antonio-mello-ai/mcp-slack/issues/1).
- Conversation ID and DM/private-channel support alignment is tracked in
  [Issue #8](https://github.com/antonio-mello-ai/mcp-slack/issues/8).

## Post a message

`slack_post_message` resolves a channel name or recognized ID and immediately
calls `chat.postMessage`. When its channel argument is empty, the current
implementation uses `SLACK_DEFAULT_CHANNEL` if configured. The result includes
the destination channel ID and Slack timestamp.

Posting is an external side effect. Requiring an explicit destination contract
is tracked in
[Issue #9](https://github.com/antonio-mello-ai/mcp-slack/issues/9). Thread
replies and Block Kit are tracked in Issues
[#1](https://github.com/antonio-mello-ai/mcp-slack/issues/1) and
[#3](https://github.com/antonio-mello-ai/mcp-slack/issues/3).

## Current boundaries

- The server uses stdio transport.
- One bot token and one optional default channel are configured per process.
- The Slack client and configuration are initialized lazily and cached in
  process memory.
- Tools return formatted text; structured MCP responses are tracked in
  [Issue #14](https://github.com/antonio-mello-ai/mcp-slack/issues/14).
- The repository does not proxy or persist Slack workspace content.
