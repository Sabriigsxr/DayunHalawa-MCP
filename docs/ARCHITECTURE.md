# Architecture

RIFT is a retrieval MCP server, not an autonomous agent. The pipeline is:

```text
Knowledge base (JSONL)
  → Embedding model (Sentence Transformers, 384 dims, normalized)
  → Vector index (FAISS IndexFlatIP)
  → Metadata alignment (documents.jsonl ↔ metadata.jsonl, 1:1 by doc_id)
  → Retrieval engine (validation at load, threshold + top_k at query time)
  → MCP server (stdio default, localhost HTTP optional)
  → AI client (OpenCode, Claude Desktop, others)
```

Full diagram sources live in [diagrams/](diagrams/README.md); they describe
the real code, not an idealized stack.

## Components

| Component | File | Responsibility |
|---|---|---|
| CLI entry | `rift_mcp/__main__.py` | Argument parsing (`--transport`, `--host`, `--port`), stdio/HTTP selection, version |
| MCP server | `rift_mcp/server.py` | Tool and prompt registration, instructions, response formatting (JSON vs. extractive text) |
| Retrieval engine | `rift_mcp/engine.py` | Lazy thread-safe singleton, all load-time validation, FAISS search, threshold filtering |
| Index build | `scripts/build_index.py` | Validated rebuild from authorized JSONL (refuses silent overwrite) |
| Index restore | `scripts/restore_index.sh` | SHA-256 check, path/type archive checks, atomic extract |

## Index type: `IndexFlatIP`

Vectors are L2-normalized before indexing, so the inner product equals cosine
similarity. `IndexFlatIP` is exact — no quantization, no approximation, no
training step. With 23,737 vectors at 384 dimensions, a full scan is
inexpensive and fully deterministic.

## Query lifecycle

1. Tool call arrives (`search_offensive_scenarios`, `ask_offensive_scenario`,
   or `index_stats`).
2. `get_engine()` builds the shared Engine on first call (double-checked
   locking) and runs all validation.
3. The query is validated (non-empty string; `top_k` clamped to 1–20;
   `threshold` clamped to 0.0–1.0; NaN/±inf rejected).
4. `SentenceTransformer.encode` produces a normalized float32 vector.
5. One `faiss.index.search(q, top_k)` call; results come back in descending
   inner-product order.
6. Hits below `threshold` or with index `-1` are dropped; remaining hits are
   mapped `idx → metadata[idx].doc_id → documents[doc_id]` and returned.

## Transports

- **stdio** (default): client spawns `python -m rift_mcp`; no socket.
- **Streamable HTTP** (`--transport http`): serves on
  `http://<host>:<port>/mcp`; default bind `127.0.0.1:8787`. **No built-in
  authentication** — loopback only unless you add an access-controlled TLS
  boundary in front.

## Failure model

Every integrity problem is a hard error at engine construction:
missing files, malformed JSONL, duplicate/missing `doc_id`, FAISS/metadata
count mismatch, document/metadata mismatch, or model-dimension mismatch.
RIFT never serves partial or silently "best-effort" results.

## Why no resources or shell tools

RIFT registers tools and one prompt, and **no MCP resources and no command
execution** — deliberately. The knowledge base is read-only reference
material; it is not a payload channel and must not become one.

---

RIFT · Red-team Intelligence & Fusion Toolkit ·
[Documentation index](README.md) · [GitHub](https://github.com/Sabriigsxr/RIFT) ·
[Ethical use](ETHICAL_USE.md) · [Security](SECURITY.md)
