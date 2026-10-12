"""Minimal public MCP Streamable HTTP server for the live challenge grader."""
from __future__ import annotations

import hashlib
import os

from mcp.server import MCPServer
from mcp.server.mcpserver import Context

SERVER_EMAIL = "24f2005143@ds.study.iitm.ac.in".strip().lower()
mcp = MCPServer("live-mcp-challenge")


@mcp.tool()
async def solve_challenge(ctx: Context) -> str:
    """Return the challenge-specific digest using the HTTP request header."""
    # Read the per-call challenge from HTTP headers (not the JSON-RPC body).
    headers = ctx.headers or {}
    challenge = headers.get("x-exam-challenge", "")

    # Header names are case-insensitive in the HTTP transport. The exam sends
    # a 32-character lowercase hex value; do not cache it between calls.
    normalized_email = SERVER_EMAIL
    digest = hashlib.sha256(f"{challenge}:{normalized_email}".encode("utf-8")).hexdigest()[:16]
    return digest


if __name__ == "__main__":
    # Render provides PORT. Streamable HTTP is mounted at /mcp by default,
    # but we set it explicitly so the endpoint URL is unambiguous.
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8000")),
        streamable_http_path="/mcp",
        stateless_http=True,
        json_response=True,
    )
