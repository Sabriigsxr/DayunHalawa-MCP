# Configuration

| Variable | Name | Default |
|---|---|---|
| Index directory | `RIFT_INDEX_DIR` | `<repo>/index` |
| Embedding model | `RIFT_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` |
| Hugging Face offline mode | `HF_HUB_OFFLINE` | unset |
| Transformers offline mode | `TRANSFORMERS_OFFLINE` | unset |

The model must be the same model family and embedding dimension used to build
the FAISS index. RIFT checks the dimension during startup and fails
explicitly on mismatch.

HTTP is localhost-only by default:

```bash
.venv/bin/rift --transport http --host 127.0.0.1 --port 8787
```

Binding to a non-loopback address exposes an unauthenticated MCP endpoint and
must only be done behind an appropriate access-control boundary.
