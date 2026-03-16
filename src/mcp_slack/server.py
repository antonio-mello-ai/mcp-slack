"""FastMCP server for Slack integration."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mcp-slack")

from mcp_slack.tools import messaging  # noqa: E402, F401


def main() -> None:
    """Entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
