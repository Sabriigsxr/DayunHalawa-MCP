#!/usr/bin/env python3
"""RIFT MCP server.

Exposes the local pentesting / DFIR / offensive-scenario Q&A knowledge base
to MCP clients (OpenCode, Claude Desktop, Cursor, etc.).

Retrieval-only (extractive): no LLM generation, no external API keys required.
Educational / authorized use only — see WARNING.txt.
"""
from __future__ import annotations

import json
import sys
from typing import Any

try:  # mcp 1.x
    from mcp.server.fastmcp import FastMCP as _Server  # type: ignore
except ModuleNotFoundError:  # mcp 2.x renamed FastMCP -> MCPServer
    try:
        from mcp.server.mcpserver import MCPServer as _Server  # type: ignore
    except ModuleNotFoundError:  # pragma: no cover
        sys.stderr.write(
            "Missing dependency 'mcp'. Install with: pip install -r requirements.txt "
            "(or: pip install 'mcp>=1.2.0')\n"
        )
        raise

from .engine import get_engine

INSTRUCTIONS = (
    "RIFT is a retrieval layer over a local offensive-scenario / pentesting "
    "Q&A knowledge base (ATT&CK-mapped detection, DFIR, offensive techniques, mitigations). "
    "Answers are extractive: the server returns the most relevant stored Q&A entries, not "
    "newly generated attack plans. EDUCATIONAL / AUTHORIZED USE ONLY — for defensive testing, "
    "education and research on systems you own or have explicit written permission to assess. "
    "Do not use to access systems or data without authorization."
)

mcp = _Server("rift", instructions=INSTRUCTIONS)


@mcp.tool()
def search_offensive_scenarios(query: str, top_k: int = 5, threshold: float = 0.25) -> str:
    """Semantic search over the offensive-scenario Q&A knowledge base.

    Args:
        query: Natural-language question or topic (e.g. "detect pass-the-hash",
            "T1003.006 mitigation", "kerberoasting detection").
        top_k: Max results to return (1-20, default 5).
        threshold: Minimum cosine-similarity score in [0, 1] (default 0.25).

    Returns:
        JSON string with a list of results: doc_id, score, category, difficulty,
        tags, cve_references, tools_used, question, answer.
    """
    results = get_engine().search(query, top_k=top_k, threshold=threshold)
    return json.dumps(
        {"query": query, "count": len(results), "results": results},
        ensure_ascii=False,
        indent=2,
    )


@mcp.tool()
def ask_offensive_scenario(question: str, top_k: int = 5, threshold: float = 0.25) -> str:
    """Answer an offensive-security knowledge question with extractive retrieval.

    Returns the most relevant stored Q&A entries formatted as text, with
    relevance scores and metadata (category, tags, CVEs, tools). This is not
    generated content — it is verbatim retrieval from the knowledge base.
    """
    results = get_engine().search(question, top_k=top_k, threshold=threshold)
    if not results:
        return (
            "No relevant entries found in the offensive-scenario knowledge base. "
            "Try rephrasing, lowering `threshold` (e.g. 0.15), or broadening the query."
        )
    lines = [f"Top {len(results)} result(s) from the offensive-scenario knowledge base:\n"]
    for i, r in enumerate(results, 1):
        lines.append(f"--- {i} (relevance {r['score']:.3f}) ---")
        lines.append(f"ID: {r['doc_id']}")
        if r.get("category"):
            lines.append(f"Category: {r['category']}")
        if r.get("difficulty"):
            lines.append(f"Difficulty: {r['difficulty']}")
        if r.get("tags"):
            lines.append(f"Tags: {', '.join(r['tags'])}")
        if r.get("cve_references"):
            lines.append(f"CVEs: {', '.join(r['cve_references'])}")
        if r.get("tools_used"):
            lines.append(f"Tools: {', '.join(r['tools_used'])}")
        if r.get("question"):
            lines.append(f"Q: {r['question']}")
        if r.get("answer"):
            lines.append(f"A: {r['answer']}")
        lines.append("")
    return "\n".join(lines)


@mcp.tool()
def index_stats() -> str:
    """Return stats about the local index (vector count, documents, model, path)."""
    return json.dumps(get_engine().stats, indent=2)


@mcp.prompt()
def offensive_scenario_brief(topic: str) -> list[dict[str, Any]]:
    """Prompt template for a structured offensive-scenario briefing on a topic."""
    return [
        {
            "role": "user",
            "content": (
                f"Using the RIFT knowledge base, produce a briefing on: {topic}\n\n"
                "1. What the technique is and how it maps to MITRE ATT&CK.\n"
                "2. How defenders detect it (logs, event IDs, tools).\n"
                "3. Mitigations and hardening steps.\n"
                "4. Relevant CVEs and tooling mentioned in the retrieved entries.\n\n"
                "Cite the retrieved entries (doc_ids) at the end. Keep it factual; do not "
                "invent commands or targets beyond what the knowledge base supports."
            ),
        }
    ]
