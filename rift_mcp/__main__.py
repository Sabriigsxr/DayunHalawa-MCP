#!/usr/bin/env python3
"""Command-line entry point for RIFT.

Usage:
    python -m rift_mcp                  # stdio transport (default; for OpenCode/Claude)
    python -m rift_mcp --transport http  # HTTP transport on 127.0.0.1:8787
    python -m rift_mcp --transport http --port 9000
"""
from __future__ import annotations

import argparse
import sys

from . import __version__
from .server import mcp


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="RIFT — Red-team Intelligence & Fusion Toolkit")
    ap.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    ap.add_argument("--transport", choices=["stdio", "http"], default="stdio")
    ap.add_argument("--host", default="127.0.0.1", help="HTTP bind host (default 127.0.0.1)")
    ap.add_argument("--port", type=int, default=8787, help="HTTP port (default 8787)")
    args = ap.parse_args(argv)

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    else:
        # Serve MCP over streamable HTTP on localhost for any MCP-capable client.
        sys.stderr.write(f"[rift] HTTP transport listening on http://{args.host}:{args.port}/mcp\n")
        mcp.run(transport="streamable-http", host=args.host, port=args.port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
