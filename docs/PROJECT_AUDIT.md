# Project audit

## Audit scope and baseline

This audit was performed against the local clone of `Sabriigsxr/DayunHalawa-MCP`
at commit `3cb4632f63120fc57367455404e8c331ad710788` on 2026-11-15. The
working tree was clean before migration changes. The history contains two
commits:

| Commit | Verified change |
|---|---|
| `bf902e9` | Initial offensive-scenario RAG MCP server |
| `3cb4632` | Bundled `data/index.tar.gz`, its hash, and `scripts/restore_index.sh` |

The migration branch is `feature/rift-transformation`. The original default
branch was not modified, pushed, or published.

## Verified architecture

The repository is a small Python package:

```text
MCP client
  -> dayunhalawa_mcp.server
     -> dayunhalawa_mcp.engine.Engine
        -> SentenceTransformer query embedding
        -> FAISS IndexFlatIP search
        -> metadata.jsonl and documents.jsonl mapping
```

`engine.py` resolves an index directory from `DAYUNHALAWA_INDEX_DIR` or the
repository `index/` directory, loads the embedding model lazily through the
singleton `get_engine()`, and searches normalized query embeddings. The
default model is `sentence-transformers/all-MiniLM-L6-v2`. The index is read
with `faiss.read_index`; the server does not write to it during retrieval.

`server.py` registers three tools and one prompt:

- `search_offensive_scenarios`
- `ask_offensive_scenario`
- `index_stats`
- `offensive_scenario_brief`

No MCP resources were registered in the original implementation. The server
supports stdio and streamable HTTP through the MCP SDK. The original CLI
defaults to stdio and HTTP binds to `127.0.0.1:8787`.

## Verified data and integrity

The tracked archive is `data/index.tar.gz` (55,017,949 bytes in the baseline
working tree). It contains exactly:

- `./faiss.index`
- `./documents.jsonl`
- `./metadata.jsonl`

The recorded SHA-256 is
`1effa2e31436d2dc6d2f3cb35cd3ed08b34041fe59c9bfa0f3dc79f44a3975e4`.
The checksum file is hash-only rather than the standard `hash  filename`
format; the original restore script accounts for that format.

The bundled JSONL files each contain 23,737 records. The local ignored index
was inspected without modifying it and also contains 23,737 document and
metadata records. The archive was not replaced or regenerated. A FAISS
runtime was not installed at the start of the audit, so the baseline vector
dimension and `ntotal` were not independently read from the binary in this
environment; the README's `23,737 vectors` statement is retained as a
repository claim, not re-presented as a newly measured fact.

## Dependencies and integrations

Verified runtime dependencies are `mcp`, `sentence-transformers`, `faiss-cpu`,
and `numpy`. The package requires Python 3.10 or newer. The source includes
configuration examples for Claude Desktop and OpenCode. No client handshake
or integration tests were present in the baseline.

The installed environment exposes MCP 2.x, where `MCPServer` replaces the
MCP 1.x `FastMCP` import. The existing fallback was preserved and the
dependency remains intentionally broad rather than blindly pinning a major
version.

## Limitations and risks

- Retrieval quality depends on the selected embedding model matching the
  vectors used to build the index.
- The baseline loader trusted JSONL structure and did not verify vector,
  metadata, document, or embedding dimensions.
- The baseline restore script verified a checksum but extracted directly into
  the destination and did not reject traversal entries.
- Retrieved records are extractive but the dataset contains mixed-quality
  material, including imperative or target-specific examples. A client must
  treat results as untrusted reference material.
- The repository did not include a license, CI, tests, security policy,
  contributor guide, or release notes. Licensing remains pending; no license
  was invented during migration.
- HTTP authentication is not provided. Localhost is the safe default and
  remote binding must be treated as an explicitly controlled deployment.

## Migration risks

The primary compatibility risk is identity: package imports remain
`dayunhalawa_mcp`, the legacy `dayunhalawa-mcp` command remains available, and
the old environment variables remain accepted. The new `rift` command and
`RIFT_*` variables are additive. Tool names remain unchanged so existing MCP
client prompts and configurations continue to resolve.

The other material risk is data integrity. The bundled archive and checksum
are preserved byte-for-byte. The new validation is fail-closed: malformed
data, alignment errors, or model/index dimension mismatches produce explicit
errors rather than silently returning misleading results.

## Recommended improvements

The migration adds focused integrity checks, safe archive restoration,
developer tooling, CI, documentation, and compatibility aliases. Future work
should add a separately governed data provenance process, signed release
artifacts, reproducible index builds, and an authorized-content review process
for knowledge-base updates.
