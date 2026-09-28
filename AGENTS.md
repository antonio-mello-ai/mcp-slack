---
title: AGENTS.md — MCP Slack
kind: policy
area: engineering
project: mcp-slack
collection: mcp-slack
owner: maintainers
status: current
canonical: AGENTS.md
globalRef: qmd://mcp-slack/AGENTS.md
reviewCadenceDays: 90
lastReviewedAt: 2026-09-28
sourceRefs:
  - github:antonio-mello-ai/mcp-slack
related:
  - README.md
  - docs/fluxos-negocio.md
  - docs/arquitetura.md
  - docs/operacao.md
  - docs/index.md
supersedes:
  - CLAUDE.md
  - GEMINI.md
supersededBy: []
sensitivity: public
---
# AGENTS.md — MCP Slack

## Purpose

This repository provides a public, self-hostable MCP server for listing Slack
channels, reading channel messages and posting messages. Keep code, examples,
issues and documentation generic and safe for public collaboration.

## Public repository boundary

- Never commit Slack tokens, real workspace or channel inventories, private
  messages, user directories, private hostnames, local user paths or internal
  topology.
- Use placeholders and synthetic Slack IDs and content in documentation and
  tests.
- Do not copy operational context from private deployments into this repository.
- Treat `slack_post_message` as an external side effect. Tests must mock Slack
  APIs and must not post to live workspaces.

## Stack

- Python 3.12+
- FastMCP
- Slack SDK asynchronous Web API client
- `uv`, Ruff and pytest

## Local setup and validation

```bash
git config core.hooksPath .githooks
uv sync --all-extras --all-groups
uv run --all-extras --all-groups pytest -q
uvx ruff check src/ tests/
uvx ruff format --check src/ tests/
```

The current version and release inconsistency is tracked in GitHub Issue #12.
Do not add another version source while resolving it.

## Documentation sources of truth

- `README.md`: public installation, Slack App setup and usage entry point
- `docs/fluxos-negocio.md`: behavior exposed to MCP clients
- `docs/arquitetura.md`: implementation model and boundaries
- `docs/operacao.md`: credentials, validation and release operation
- `docs/index.md`: navigable documentation index

Roadmap, backlog and priority live in GitHub Issues and the Felhen GitHub
Project. Delivery history lives in closed Issues, pull requests and GitHub
Releases. Do not add `roadmap.md`, `docs/backlog.md` or `CHANGELOG.md`.
