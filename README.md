# DayunHalawa-MCP

**Offensive Scenario RAG — MCP Server**

A local [Model Context Protocol](https://modelcontextprotocol.io) (MCP) server that exposes a
large offensive-security / pentesting / DFIR Q&A knowledge base to agentic coding apps
(OpenCode, Claude Desktop, Cursor, and any MCP-capable client).

Retrieval-only (extractive): the server searches a local FAISS index and returns the most
relevant stored Q&A entries with scores and metadata. It does **not** generate attack plans,
and it does **not** require an LLM API key or internet access at query time.

> ⚠️ **EDUCATIONAL / AUTHORIZED USE ONLY.** This project is for authorized defensive security
> testing, education and research on systems you own or have explicit written permission to
> assess. Do not use it to access systems, accounts or data without authorization, or to defeat
> security controls you do not own. See [`WARNING.txt`](./WARNING.txt) for the full terms.

---

## What's inside

| Component | Description |
|---|---|
| `dayunhalawa_mcp/engine.py` | FAISS + `sentence-transformers` retrieval engine (lazy singleton) |
| `dayunhalawa_mcp/server.py` | MCP server (FastMCP): tools and prompt |
| `dayunhalawa_mcp/__main__.py` | CLI entry point: stdio (default) or localhost HTTP transport |
| `scripts/build_index.py` | Rebuild the FAISS index from a `documents.jsonl` file |

### MCP tools

| Tool | Purpose |
|---|---|
| `search_offensive_scenarios(query, top_k=5, threshold=0.25)` | Semantic search; returns JSON with score/category/tags/CVEs/tools/Q&A |
| `ask_offensive_scenario(question, top_k=5, threshold=0.25)` | Formatted extractive answer for humans/agents |
| `index_stats()` | Vector/document counts, model name, resolved index path |

### MCP prompt

- `offensive_scenario_brief(topic)` — structures a briefing request (technique → ATT&CK mapping, detection, mitigation, CVEs) grounded in retrieved entries.

### Knowledge base

~23,000+ Q&A entries spanning ATT&CK techniques, detection engineering, DFIR, offensive
tradecraft (detection-focused), mitigations and tooling. **The built index is not committed to
this repository** (`documents.jsonl` ≈ 120 MB, over GitHub's 100 MB per-file limit and not
redistributable in-repo). Bring or build your own index — see below.

## Requirements

- Python ≥ 3.10
- ~300 MB disk for model + deps (embedding model cached on first run)
- Local index directory containing:
  - `faiss.index` — FAISS `IndexFlatIP` over normalized embeddings
  - `documents.jsonl` — one JSON object per line: `{"doc_id", "question", "answer", ...}`
  - `metadata.jsonl` — one JSON object per line with the non-Q&A fields (`category`, `tags`,
    `cve_references`, `tools_used`, …), indexed in the same order as `documents.jsonl`

## Install

```bash
git clone https://github.com/<YOUR_OWNER>/DayunHalawa-MCP.git
cd DayunHalawa-MCP

python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
# or, editable console script:
.venv/bin/pip install -e .
```

## Index setup

The server reads the index from `$DAYUNHALAWA_INDEX_DIR` if set, otherwise `./index/` in the
repo root.

Option A — point it at an existing build:

```bash
export DAYUNHALAWA_INDEX_DIR=/path/to/index   # contains faiss.index, documents.jsonl, metadata.jsonl
```

Option B — build one from a `documents.jsonl` you have rights to use:

```bash
.venv/bin/python scripts/build_index.py --documents /path/to/documents.jsonl --out ./index
```

First run downloads `sentence-transformers/all-MiniLM-L6-v2` (~80 MB) unless already cached;
after that, everything runs locally offline.

## Run

### stdio (default — what agent coding apps use)

```bash
.venv/bin/python -m dayunhalawa_mcp
```

Console script equivalent after `pip install -e .`:

```bash
dayunhalawa-mcp
```

### Localhost HTTP (any MCP-capable app)

```bash
.venv/bin/python -m dayunhalawa_mcp --transport http --host 127.0.0.1 --port 8787
# MCP endpoint: http://127.0.0.1:8787/mcp
```

## Client configuration

### OpenCode (`opencode.json` / project or global config)

```jsonc
{
  "mcp": {
    "dayunhalawa-mcp": {
      "type": "local",
      "enabled": true,
      "command": [
        "/absolute/path/to/DayunHalawa-MCP/.venv/bin/python",
        "-m",
        "dayunhalawa_mcp"
      ],
      "environment": {
        "DAYUNHALAWA_INDEX_DIR": "/absolute/path/to/DayunHalawa-MCP/index"
      }
    }
  }
}
```

Then reference the tools as `dayunhalawa-mcp_search_offensive_scenarios` in your agent prompts.

### Claude Desktop (`claude_desktop_config.json`)

```json
{
  "mcpServers": {
    "dayunhalawa-mcp": {
      "command": "/absolute/path/to/DayunHalawa-MCP/.venv/bin/python",
      "args": ["-m", "dayunhalawa_mcp"],
      "env": {
        "DAYUNHALAWA_INDEX_DIR": "/absolute/path/to/DayunHalawa-MCP/index"
      }
    }
  }
}
```

Restart the client after editing its config.

### Generic MCP client over HTTP

Start the HTTP transport (above), then point your client's MCP configuration at
`http://127.0.0.1:8787/mcp` (streamable HTTP transport).

## Environment variables

| Variable | Default | Purpose |
|---|---|---|
| `DAYUNHALAWA_INDEX_DIR` | `<repo>/index` | Directory with `faiss.index`, `documents.jsonl`, `metadata.jsonl` |
| `DAYUNHALAWA_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` | Embedding model for query encoding |
| `HF_HUB_OFFLINE` | unset | Set to `1` to forbid model-hub network checks at query time |
| `TRANSFORMERS_OFFLINE` | unset | Set to `1` to force fully local model loading |

## Notes on behavior and scope

- Query encoding is local; the FAISS index is opened read-only.
- If the index or model is missing, tools return an error describing what is missing and how to fix it.
- Retrieve first with `threshold≈0.25`; lower it (e.g. 0.15) for broader recall.
- No shell execution, no file writes, no network calls are made by this server.

## License & attribution

No license has been selected yet — treat all rights as reserved until one is added. The bundled
warning (`WARNING.txt`) applies regardless of license. You are responsible for having rights to
any `documents.jsonl` you build an index from.
