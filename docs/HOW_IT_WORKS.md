# How RIFT works — from first principles

Three depth levels. Read top to bottom; each builds on the previous one.

---

## Level 1 — Beginner: what happens when you ask a question

You type something like "how do I detect pass-the-hash?" into your AI client
and it calls RIFT's `search_offensive_scenarios` tool. RIFT does four things:

1. **Converts your words to numbers.** A machine-learning model
   (`sentence-transformers/all-MiniLM-L6-v2`) turns the question into a list
   of 384 numbers that captures its meaning — this is an *embedding*.
2. **Compares against everything it knows.** The bundled knowledge base has
   23,737 entries, each stored as the same kind of 384-number vector, inside a
   FAISS index (`IndexFlatIP`). RIFT measures the angle between your vector
   and every stored vector — that angle is *cosine similarity*.
3. **Keeps only good matches.** It drops weak matches below the threshold
   (0.25 by default) and returns at most `top_k` results (default 5).
4. **Shows you the original text.** Tool output includes the stored question,
   answer, and metadata — not generated prose. RIFT retrieves; it does not
   invent.

Why not just keyword search? Because "pass-the-hash" and "PtH against NTLM"
mean the same thing to an attacker, and keyword search can miss that. Embeddings
match on meaning.

---

## Level 2 — Intermediate: the moving parts

### FAISS `IndexFlatIP`

FB-AI Similarity Search stores vectors in a flat table. `Flat` means exact,
brute-force comparison (no compression or approximation); `IP` means inner
product as the comparison operator. With normalized vectors, inner product =
cosine similarity. At this scale (23,737 × 384 floats ≈ 36 MB), exact search is
fast and deterministic.

### Normalization and scoring

Both the stored vectors and query vectors are L2-normalized, so every vector
has length 1.0. The inner product then equals cosine similarity, bounded in
[−1, 1]. RIFT's default `threshold` is 0.25 — a permissive floor, not a
confidence guarantee. Raise it for precision; lower it for recall.
`top_k` is clamped to 1–20.

### Embeddings and the embedding model

`all-MiniLM-L6-v2` is a small bidirectional transformer producing 384-dim
embeddings. RIFT feeds it `question + "\n" + answer` at index time (via
`scripts/build_index.py`) and only the query at search time — asymmetric but
works well in practice because both sides describe the same semantic content.

### Metadata alignment

Each vector position `i` corresponds to line `i` of `metadata.jsonl`. Each
metadata record carries `doc_id` and metadata such as `category`,
`difficulty`, `tags`, `cve_references`, `tools_used`. `doc_id` maps onto
`documents.jsonl` for the full question/answer. Alignment is verified at load:
counts must match, IDs must be unique and cross-checked both ways. A mismatch
fails closed — nothing is served.

### How MCP exposes this

- `search_offensive_scenarios` → returns JSON: `query`, `count`, `results[]`.
- `ask_offensive_scenario` → renders the same retrieval as human-readable text.
- `index_stats` → returns vector/document/dimension/model/path statistics.
- `offensive_scenario_brief` → prompt template to structure a briefing around
  retrieved entries.

Transports: **stdio** (default; client spawns the server) and **streamable
HTTP** on `http://127.0.0.1:8787/mcp` (no authentication; loopback only).

---

## Level 3 — Advanced: internals, limits, extension points

### Load-time validation (the real gatekeeper)

`Engine.__init__` enforces, in order:

1. `faiss.index`, `documents.jsonl`, `metadata.jsonl` exist (else
   `FileNotFoundError` pointing at `RIFT_INDEX_DIR` and
   [TROUBLESHOOTING.md](TROUBLESHOOTING.md)).
2. Every JSONL line parses as a UTF-8 JSON **object** (else `ValueError` with
   file and line number).
3. Every document `doc_id` is a non-empty string; duplicates rejected.
4. `index.ntotal == len(metadata)` (else `ValueError`).
5. Every metadata `doc_id` exists in documents; duplicates rejected; document
   count must equal metadata count.
6. Model embedding dimension equals `index.d`; mismatch is a hard error.

`get_engine()` uses a double-checked `threading.Lock` for lazy singleton
construction — safe for concurrent MCP tool calls in one process.

### Query-time validation

- Empty/whitespace `query` → `ValueError("query must be a non-empty string")`.
- `top_k`/`threshold` bools → `TypeError`; NaN/±inf → `ValueError`;
  non-numeric strings → `ValueError`; everything else is clamped.

### Security boundaries

- No shell execution, no file writes at query time, no outbound requests.
- Read-only access to the index directory during retrieval.
- HTTP has **no authentication**; treat the port as private.
- Retrieved text is untrusted data: review before following any instructions
  it contains. RIFT does not act on retrievals.

### Known non-features (honest list)

- No incremental indexing at runtime (rebuild via `scripts/build_index.py`).
- No hybrid (keyword + vector) ranking; pure dense retrieval.
- No streaming responses; results return complete.
- No authentication/authorization layer; single-user local trust model.
- No telemetry, no crash reporting — by design.

### Extension points (future, not implemented)

- Alternative `FAISS` index types (HNSW, IVF) for larger corpora.
- Metadata filtering pre-search (e.g. `category` or `cve_references`).
- Evaluation harness for threshold calibration and recall@k.
- Alternative embeddings via the same `MODEL_NAME` seam.

Anything beyond this list is a **planned** capability and must not be
represented as existing — see [ROADMAP.md](ROADMAP.md).

---

RIFT · Red-team Intelligence & Fusion Toolkit ·
[Documentation index](README.md) · [GitHub](https://github.com/Sabriigsxr/RIFT) ·
[Ethical use](ETHICAL_USE.md) · [Security](SECURITY.md)
