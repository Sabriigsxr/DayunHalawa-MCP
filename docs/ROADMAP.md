# RIFT roadmap

This roadmap is a plan, not a promise. Items are **not implemented** unless
listed in [RELEASE_NOTES.md](RELEASE_NOTES.md) or the README's "implemented"
table. Nothing here is a commitment of dates or releases.

## Phase 1 — Stability

- [x] Runtime input validation (NaN/±inf rejection for `top_k` and `threshold`)
- [x] Archive restoration hardening (SHA-256, member path/type checks, atomic extract)
- [x] Regression tests for validation and restore paths
- [x] MCP SDK 1.x/2.x compatibility shim (`FastMCP` / `MCPServer`)
- [ ] Expanded test coverage (HTTP transport, concurrency, CLI parsing)
- [ ] Dependency compatibility matrix in CI (mcp 1.x vs 2.x)
- [ ] Signed, checksummed releases with artifact attestation

## Phase 2 — Developer experience

- [ ] Improved CLI ergonomics (`rift --doctor` self-check: index, model, transport)
- [ ] Structured logging (opt-in, no telemetry)
- [ ] Clearer, actionable error messages across startup failures
- [ ] More verified client configuration examples (only clients actually tested)
- [ ] Configuration generation and validation helper

## Phase 3 — Intelligence improvements

Potential, subject to architecture review:

- [ ] Retrieval explanations (why an entry matched)
- [ ] Advanced metadata filtering (`category`, `cve_references`, `tags`)
- [ ] Query expansion for recall
- [ ] Retrieval evaluation harness (recall@k, MRR) with a frozen gold set
- [ ] Source provenance and knowledge-base entry attestations

These would extend the engine behind the existing tool contracts; none are
started, and all would ship as opt-in behavior behind unchanged defaults.

## Phase 4 — Ecosystem

- [ ] Additional MCP clients verified and documented
- [ ] Optional local web UI (read-only) for browsing the knowledge base
- [ ] Knowledge-base maintenance tools (validation, dedup, re-embedding) with provenance
- [ ] Import pipelines for authorized datasets
- [ ] Benchmarking and evaluation publication

## What will not change

- Local-first, offline-capable retrieval.
- No paid APIs, no telemetry, no autonomous exploitation.
- No license selection until redistribution rights are verified.
- The knowledge base in `data/index.tar.gz` is never regenerated automatically.

---

RIFT · Red-team Intelligence & Fusion Toolkit ·
[Documentation index](README.md) · [GitHub](https://github.com/Sabriigsxr/RIFT) ·
[Ethical use](ETHICAL_USE.md) · [Security](SECURITY.md)
