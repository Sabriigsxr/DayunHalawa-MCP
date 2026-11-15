# RIFT — Implementation report

Product-presentation and documentation transformation executed on branch
`feat/rift-product-presentation` (based on `fix/recheck-errors`, i.e. it
includes the pending PR #4 fixes). **No commits were pushed; nothing was
published**, per instruction.

## Completion matrix

| Deliverable | Status | Evidence |
|---|---|---|
| Brand identity | COMPLETE | `assets/branding/` — palette (`rift-color-palette.md`), typography (`rift-typography.md`), guidelines (`rift-brand-guidelines.md`) |
| Logo assets | COMPLETE | `rift-logo.svg`, `rift-logo-mark.svg`, `rift-wordmark.svg` — original artwork, XML-validated, render-checked with ImageMagick |
| Social preview | PARTIAL | `rift-social-preview.svg` + faithful raster `rift-social-preview.png` (1280×640) created; GitHub upload requires Settings → Social preview (manual, PNG only) |
| Architecture diagrams | COMPLETE | 5 Mermaid diagrams in `docs/diagrams/` + `README.md`; GitHub renders Mermaid; not rasterized locally (no `mmdc` in env) |
| Root README | COMPLETE | Product landing page: identity, problem, capabilities, quick start, real example, 18 required elements |
| Beginner guide | COMPLETE | `docs/GETTING_STARTED.md` — What is MCP/vector DB/embeddings + "From Zero to Your First RIFT MCP Search" with real captures |
| Advanced documentation | COMPLETE | `docs/HOW_IT_WORKS.md` (3 levels), `docs/RETRIEVAL_ENGINE.md` updated for NaN/±inf validation |
| MCP integration guide | COMPLETE | `docs/MCP_INTEGRATION.md` — verified tool/prompt contracts, error behavior, real invocations |
| Real screenshots | NOT DONE | No GUI screenshot tool available (`scrot`/`gnome-screenshot`/`grim` absent); no fabricated images produced. Checklist: `assets/screenshots/CAPTURE_CHECKLIST.md` |
| Demo workflow | COMPLETE | `docs/demo/` (DEMO, SEARCH_EXAMPLE, MCP_CLIENT_SETUP, EXPECTED_WORKFLOW) — all transcripts from a real offline session |
| Roadmap | COMPLETE | `docs/ROADMAP.md` — Phases 1–4, current state marked, no speculative claims |
| Documentation links | COMPLETE | 139 internal links machine-checked — all resolve; naming sweep clean (164/164 "RIFT") |
| Tests | COMPLETE | `pytest` → **12 passed** (3 new regression tests added); `ruff` clean; `compileall` OK |
| Security review | COMPLETE | NaN/±inf rejection in engine; archive member-type check (fifo/device rejected) in restore script; SHA-256 `shasum` fallback; HTTP-no-auth documented; license not selected (documented as reserved) |

## Files created

```text
assets/branding/rift-brand-guidelines.md
assets/branding/rift-color-palette.md
assets/branding/rift-logo-mark.svg
assets/branding/rift-logo.svg
assets/branding/rift-social-preview.png
assets/branding/rift-social-preview.svg
assets/branding/rift-typography.md
assets/branding/rift-wordmark.svg
assets/screenshots/CAPTURE_CHECKLIST.md
docs/CONTRIBUTING.md
docs/demo/DEMO.md
docs/demo/EXPECTED_WORKFLOW.md
docs/demo/MCP_CLIENT_SETUP.md
docs/demo/SEARCH_EXAMPLE.md
docs/diagrams/README.md
docs/diagrams/data-ingestion-flow.mmd
docs/diagrams/deployment-architecture.mmd
docs/diagrams/mcp-integration-flow.mmd
docs/diagrams/semantic-search-flow.mmd
docs/diagrams/system-architecture.mmd
docs/GETTING_STARTED.md
docs/HOW_IT_WORKS.md
docs/README.md
docs/ROADMAP.md
docs/USAGE_EXAMPLES.md
```

## Files modified

```text
README.md                  CONTRIBUTING.md
docs/ARCHITECTURE.md       docs/CONFIGURATION.md   docs/DATASET.md
docs/ETHICAL_USE.md        docs/INSTALLATION.md    docs/MCP_INTEGRATION.md
docs/RELEASE_NOTES.md      docs/RETRIEVAL_ENGINE.md docs/SECURITY.md
docs/TROUBLESHOOTING.md
rift_mcp/engine.py         scripts/restore_index.sh
tests/test_engine.py       tests/test_restore.py
```

(Note: `main...HEAD` also includes the five commits from the pending
`fix/recheck-errors` branch, listed below under "Base this builds on".)

## Visual identity summary

Dark charcoal `#090A0D`, subtle `#17181F` technical grid, deep crimson
`#D7193F` accent (`#F04A68` on dark for small text, `#8F0F29` on light), near-white
`#F2F3F5` and muted gray `#9CA0AA` typography. Original angular-miter
"rift R" mark, reused consistently from the existing RIFT logo geometry. No
clichés (no skulls/neon/hoodies). Wordmark is all-caps Inter 800 with wide
tracking; descriptors uppercase 600 with wide tracking. All artwork is SVG
(original), grid-aligned, and safe at ≥32 px.

## Architecture diagrams summary

- `system-architecture.mmd` — clients → transports (stdio default, loopback
  HTTP) → server → tools/prompt → engine → local FAISS + JSONL stores
- `data-ingestion-flow.mmd` — authorized JSONL → validation → normalized
  embeddings → `IndexFlatIP` → bundled archive → checksum/restore
- `semantic-search-flow.mmd` — query validation → encode → single
  `index.search` call → `-1`/threshold filtering → doc_id mapping
- `mcp-integration-flow.mmd` — sequence diagram of the real request path,
  incl. lazy engine singleton and the explicit no-auth HTTP boundary
- `deployment-architecture.mmd` — single-host local-first deployment;
  no inbound exposure required

All reference the implementation, not aspirational design. RIFT is not
represented as an autonomous exploitation engine anywhere.

## Documentation navigation map

```text
README.md (landing)
 └ docs/README.md (index)
     ├ GETTING_STARTED.md → USAGE_EXAMPLES.md → MCP_INTEGRATION.md
     │      └ "From Zero to Your First RIFT MCP Search" tutorial (real captures)
     ├ INSTALLATION.md → CONFIGURATION.md → TROUBLESHOOTING.md
     ├ ARCHITECTURE.md ─ diagrams/ (5 .mmd + README)
     ├ HOW_IT_WORKS.md (Beginner → Intermediate → Advanced)
     ├ MCP_INTEGRATION.md (contracts) ↔ demo/ (DEMO, SEARCH_EXAMPLE, setup, workflow)
     ├ RETRIEVAL_ENGINE.md · DATASET.md
     ├ SECURITY.md · ETHICAL_USE.md
     ├ CONTRIBUTING.md (root guide) → ROADMAP.md
     └ RELEASE_NOTES.md · ROADMAP.md
```

Every page ends with the same footer (index · GitHub · ethical use · security).

## Actual features documented

- Stdio MCP transport (default) and streamable HTTP on `127.0.0.1:8787/mcp`
  (**no authentication** — documented everywhere relevant).
- `search_offensive_scenarios`, `ask_offensive_scenario`, `index_stats`,
  `offensive_scenario_brief` — contracts with inputs, defaults, validation,
  output formats, error behavior, and real captured invocations.
- Load-time index validation and its six checks; NaN/±inf input rejection;
  `top_k` 1–20; `threshold` 0.0–1.0; cosine-similarity scoring via normalized
  inner product; `IndexFlatIP`; 23,737 vectors / 384 dims.
- SHA-256-verified bundled index with path/type archive checks and atomic
  restore; rebuild via `scripts/build_index.py`.
- Offline operation after model cache; `HF_HUB_OFFLINE` / `TRANSFORMERS_OFFLINE`.

## Screenshots captured

None — not possible in this environment (no GUI capture tool); no fabricated
images included. `assets/screenshots/CAPTURE_CHECKLIST.md` lists exactly what
to capture and how; the README and `docs/demo/` point at it.

## Screenshots still pending

All six (startup, index stats, search result, readable output, client
integration, example workflow) — see `assets/screenshots/CAPTURE_CHECKLIST.md`.

## Tests executed (real results)

```text
python -m pytest -q    → 12 passed in 0.29s
python -m ruff check . → All checks passed!
python -m compileall -q rift_mcp scripts tests → OK
bash -n scripts/restore_index.sh → syntax OK
restore_index.sh end-to-end on the real archive (temp copy) → SHA-256 OK, 155 MB extracted
```

## Remaining issues

1. **Screenshots pending** (above).
2. **Branch stacking:** this branch sits on `fix/recheck-errors` (PR #4).
   Merge order: PR #4 first, or merge this branch as-is (it contains #4's commits).
3. **License** remains unselected; project and bundled data are all-rights-reserved.
4. **GitHub social preview** must be uploaded manually in repo Settings
   (SVG/PNG present; GitHub needs PNG — use `assets/branding/rift-social-preview.png`).
5. **Mermaid diagrams** not rasterized here; they render on GitHub.
6. **Vercel** from earlier remains a Vercel-side disconnect (no repo change needed).
7. Nothing has been pushed; all work is local on this branch.

## Roadmap summary

Phase 1 (Stability) — input validation, restore hardening, tests, MCP SDK
shim; CI matrix and signed releases pending. Phase 2 (Developer experience) —
CLI doctor, structured logging, config helper, more verified client examples.
Phase 3 (Intelligence) — match explanations, metadata filtering, query
expansion, evaluation harness — all future, none implemented. Phase 4
(Ecosystem) — more clients, optional read-only web UI, KB maintenance tools —
future, none implemented.

## Git diff summary (`main...HEAD`)

```text
40 files changed, 1965 insertions(+), 204 deletions(-)
 24 added · 16 modified · data/ untouched (knowledge base intact)
```

Data integrity statement: **`data/index.tar.gz` and `data/index.tar.gz.sha256`
were not modified at any point in this work.** Checksum remains
`1effa2e31436d2dc6d2f3cb35cd3ed08b34041fe59c9bfa0f3dc79f44a3975e4`.

## Base this builds on

```text
48790a5 Fix restore portability and stale doc references   (PR #4, pending)
a9c684b Add RIFT brand identity kit (assets/branding/)
1a9ff96 Add Mermaid architecture diagrams matching the implementation
c8ae96a Harden engine input validation and restore script
300292b Documentation system rebuild + product README
ea8dab9  Add implementation report (this file)
```
