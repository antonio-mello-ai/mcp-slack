---
title: Operations — MCP Slack
kind: runbook
area: operations
project: mcp-slack
collection: mcp-slack
owner: maintainers
status: current
canonical: docs/operacao.md
globalRef: qmd://mcp-slack/docs/operacao.md
reviewCadenceDays: 90
lastReviewedAt: 2026-09-28
sourceRefs:
  - README.md
  - .env.example
  - .github/workflows/ci.yml
related:
  - docs/fluxos-negocio.md
  - docs/arquitetura.md
  - docs/index.md
supersedes: []
supersededBy: []
sensitivity: public
---
# Operations

## Local installation

```bash
git config core.hooksPath .githooks
uv sync --all-extras --all-groups
```

Create a Slack App, grant only the scopes required by the tools in use, install
it to the target workspace and inject `SLACK_BOT_TOKEN` from a local secret
source. `SLACK_DEFAULT_CHANNEL` is optional. `.env.example` contains
placeholders only.

## Credential and content handling

- Treat bot tokens as credentials and rotate them if exposed.
- Do not pass tokens in command-line arguments retained in shell history or
  process listings.
- Do not print tokens, private messages, real channel inventories or workspace
  membership into public issues, terminal transcripts or shared logs.
- Use a dedicated Slack App with the smallest practical OAuth scope set.
- Invite the bot only to conversations it must access.

## Run

```bash
uv run mcp-slack
```

The process communicates over stdio. Keep stdout reserved for the MCP protocol.
Before invoking `slack_post_message`, confirm the destination and content; the
tool performs the external write immediately.

## Validation

```bash
uv run --all-extras --all-groups pytest -q
uvx ruff check src/ tests/
uvx ruff format --check src/ tests/
gitleaks git --redact --no-banner --log-opts='--all' .
```

CI runs lint, formatting and tests on Python 3.12 and 3.13 for pushes and pull
requests targeting `main`.

## Release

The repository currently has GitHub tags and releases, while the documented
installation path is from a source checkout. The canonical version source,
broken `VERSION`-file hook and supported publication path are tracked together
in [Issue #12](https://github.com/antonio-mello-ai/mcp-slack/issues/12).

## Failure modes

| Symptom | Check |
| --- | --- |
| Configuration fails before a tool call | Confirm `SLACK_BOT_TOKEN` is present without printing its value. |
| `missing_scope` | Compare the failing tool with the scope matrix in `README.md`, update the app and reinstall it. |
| Channel not found | Use an exact visible channel name or currently supported ID; see Issue #8. |
| Bot cannot read or post | Confirm bot membership and the relevant history or `chat:write` scope. |
| Rate-limited or transient failure | Bounded retry behavior is tracked in Issue #2. |
| Raw or unclear Slack API failure | Safe error normalization is tracked in Issue #10. |

Roadmap and operational follow-ups belong in GitHub Issues, not in this runbook.
