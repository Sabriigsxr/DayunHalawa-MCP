# Configuration

| Variable | Purpose | Default |
|---|---|---|
| `RIFT_INDEX_DIR` | Directory containing `faiss.index`, `documents.jsonl`, `metadata.jsonl` | `<repo>/index` |
| `RIFT_MODEL` | Sentence Transformers model name/path | `sentence-transformers/all-MiniLM-L6-v2` |
| `HF_HUB_OFFLINE` | Set `1` to forbid Hugging Face network access | unset |
| `TRANSFORMERS_OFFLINE` | Set `1` to forbid Transformers network access | unset |

Configuration is read at engine-load time (first tool call), not at process
start. If the model or index fails validation, RIFT reports an explicit error
instead of answering with partial data.

## Model and index compatibility

The embedding model must produce the same vector dimension the FAISS index was
built with. RIFT checks this at load time (`get_embedding_dimension()`, with a
fallback to `get_sentence_embedding_dimension()`) and fails explicitly on
mismatch. Changing `RIFT_MODEL` to a different dimension requires rebuilding
the index (`scripts/build_index.py`).

## HTTP transport

```bash
.venv/bin/rift --transport http --host 127.0.0.1 --port 8787
```

- The endpoint is `http://127.0.0.1:8787/mcp` (streamable HTTP).
- **There is no built-in authentication.** Bind localhost only, or place the
  listener behind an access-controlled boundary with TLS. Do not expose it
  to untrusted networks.
- `--host` and `--port` are the only HTTP knobs; there is no TLS, no auth
  token, and no CORS configuration in-process.

## stdio transport (default)

```bash
.venv/bin/rift
```

No network socket is opened. The MCP client spawns the process and talks over
stdin/stdout. This is the recommended desktop mode.

## Environment for clients

Client configurations set `RIFT_INDEX_DIR` (and optionally the offline
variables) per process — see
[MCP_INTEGRATION.md](MCP_INTEGRATION.md) and the examples in
[../examples/](../examples/).

## What RIFT validates before answering

1. All three index files exist.
2. Every JSONL line is a UTF-8 JSON object.
3. `doc_id` values are unique and non-empty (documents and metadata).
4. FAISS `ntotal` equals the metadata record count.
5. Every metadata `doc_id` maps to a document (1:1 alignment, order matters).
6. Model embedding dimension equals the FAISS index dimension.

Details: [RETRIEVAL_ENGINE.md](RETRIEVAL_ENGINE.md).

---

RIFT · Red-team Intelligence & Fusion Toolkit ·
[Documentation index](README.md) · [GitHub](https://github.com/Sabriigsxr/RIFT) ·
[Ethical use](ETHICAL_USE.md) · [Security](SECURITY.md)
