# MCP integration

RIFT exposes three tools and one prompt over the Model Context Protocol. This
page is the contract: what each capability accepts, returns, and does on bad
input — all verified against the implementation in `rift_mcp/server.py` and
`rift_mcp/engine.py`.

Transports:

- **stdio** (default) — the client spawns the server; no socket.
- **Streamable HTTP** — `http://127.0.0.1:8787/mcp` with
  `--transport http`; loopback by default; **no built-in authentication**.

## Capabilities

### `search_offensive_scenarios`

| Aspect | Contract |
|---|---|
| Purpose | JSON semantic search over the knowledge base |
| Inputs | `query: str` (required), `top_k: int = 5`, `threshold: float = 0.25` |
| Validation | `query` non-empty string; `top_k` clamped to 1–20 (bool rejected, NaN/±inf rejected); `threshold` clamped to 0.0–1.0 (bool rejected, NaN/±inf rejected) |
| Output | JSON string: `{"query", "count", "results": [...]}`; each result: `doc_id`, `score` (4dp), `category`, `difficulty`, `tags`, `cve_references`, `tools_used`, `question`, `answer` |
| Errors | Tool error on empty query / non-finite inputs / index failure |
| Order | Results follow FAISS inner-product (descending score) order |

### `ask_offensive_scenario`

| Aspect | Contract |
|---|---|
| Purpose | Human-readable, extractive rendering of the same retrieval |
| Inputs | `question: str` (required), `top_k: int = 5`, `threshold: float = 0.25` |
| Output | Text: header line plus one `--- i (relevance s) ---` block per hit, with ID, metadata, `Q:` and `A:` |
| Empty case | Returns a guidance message (rephrase / lower threshold); no error |
| Errors | Same validation as above |

### `index_stats`

| Aspect | Contract |
|---|---|
| Purpose | Report vector count, dimensions, index type, model, and path |
| Inputs | none |
| Output | JSON string: `index_dir`, `model`, `vectors`, `dimensions`, `index_type`, `metadata_entries`, `documents` |
| Use | Smoke checks, config verification, integrity audits |

### `offensive_scenario_brief` (prompt)

| Aspect | Contract |
|---|---|
| Purpose | Structured briefing template grounded in the retrieved entries |
| Input | `topic: str` |
| Output | Single user-message prompt: technique, ATT&CK mapping, detection, mitigations, CVEs/tooling, with instruction to cite doc_ids |
| Note | A prompt template only — RIFT does not fill it in |

RIFT registers **no MCP resources** and exposes **no shell or file tools**.

## Real invocations (captured)

Against the restored bundled index, an MCP stdio session lists:

```text
TOOLS: ["search_offensive_scenarios", "ask_offensive_scenario", "index_stats"]
PROMPTS: ["offensive_scenario_brief"]
```

`index_stats()` returns:

```json
{
  "index_dir": "…/RIFT/index",
  "model": "sentence-transformers/all-MiniLM-L6-v2",
  "vectors": 23737,
  "dimensions": 384,
  "index_type": "IndexFlatIP",
  "metadata_entries": 23737,
  "documents": 23737
}
```

A search for `kerberoasting detection` with `threshold=0.6`, `top_k=2`
returns `cybersec-14323::q1172` (relevance 0.7102) and
`cybersec-53707::q7339` (0.6771) — see [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md)
for the full capture.

## Client configuration

Claude Desktop (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "rift": {
      "command": "/absolute/path/to/RIFT/.venv/bin/python",
      "args": ["-m", "rift_mcp"],
      "env": {
        "RIFT_INDEX_DIR": "/absolute/path/to/RIFT/index",
        "HF_HUB_OFFLINE": "1",
        "TRANSFORMERS_OFFLINE": "1"
      }
    }
  }
}
```

OpenCode (`opencode.jsonc`):

```jsonc
{
  "mcp": {
    "rift": {
      "type": "local",
      "command": ["/absolute/path/to/RIFT/.venv/bin/python", "-m", "rift_mcp"],
      "environment": {
        "RIFT_INDEX_DIR": "/absolute/path/to/RIFT/index",
        "HF_HUB_OFFLINE": "1",
        "TRANSFORMERS_OFFLINE": "1"
      }
    }
  }
}
```

Both clients spawn the server per configuration; the model loads from the
local Hugging Face cache (see
[CONFIGURATION.md](CONFIGURATION.md#model-cache-and-offline-use)).

**Notes for operators**

- The HTTP endpoint is unauthenticated. Do not expose it beyond localhost or
  an access-controlled boundary with TLS.
- `examples/` in the repository mirrors these files.
- No additional clients are documented without a verified integration.

---

RIFT · Red-team Intelligence & Fusion Toolkit ·
[Documentation index](README.md) · [GitHub](https://github.com/Sabriigsxr/RIFT) ·
[Ethical use](ETHICAL_USE.md) · [Security](SECURITY.md)
