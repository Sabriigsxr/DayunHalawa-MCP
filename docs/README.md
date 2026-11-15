# RIFT documentation

**RIFT — Red-team Intelligence & Fusion Toolkit** · Local offensive security
knowledge engine

This index is the map of the RIFT documentation. Every page is checked against
the implementation in `rift_mcp/`, `scripts/`, and the tracked `data/`
artifacts — nothing here describes vaporware.

## Start here

| If you are… | Read |
|---|---|
| New to RIFT, MCP, or embeddings | [GETTING_STARTED.md](GETTING_STARTED.md) — includes **“From Zero to Your First RIFT MCP Search”** |
| Installing RIFT | [INSTALLATION.md](INSTALLATION.md) |
| Wiring RIFT into an AI client | [MCP_INTEGRATION.md](MCP_INTEGRATION.md) |
| Looking for real command examples | [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) |
| Something broke | [TROUBLESHOOTING.md](TROUBLESHOOTING.md) |

## How it works (intermediate and advanced)

| Page | Audience |
|---|---|
| [ARCHITECTURE.md](ARCHITECTURE.md) | Intermediate — system overview, real flow |
| [HOW_IT_WORKS.md](HOW_IT_WORKS.md) | Intermediate + advanced — FAISS, embeddings, metadata alignment, validation, scoring |
| [diagrams/](diagrams/README.md) | All — Mermaid sources of every diagram |
| [CONFIGURATION.md](CONFIGURATION.md) | Intermediate — `RIFT_INDEX_DIR`, `RIFT_MODEL`, offline mode, transports |
| [RETRIEVAL_ENGINE.md](RETRIEVAL_ENGINE.md) | Advanced — engine internals and validation rules |
| [DATASET.md](DATASET.md) | All — bundled knowledge base, restore procedure |

## Capabilities (implemented, verified)

| Tool | Purpose |
|---|---|
| `search_offensive_scenarios` | JSON semantic search over the Q&A knowledge base |
| `ask_offensive_scenario` | Extractive, human-readable rendering of results |
| `index_stats` | Index, model, and alignment statistics |
| `offensive_scenario_brief` | MCP prompt template for a grounded briefing |

RIFT registers **no MCP resources** and ships **no shell/command tools** by
design. See [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) for real invocations and
[MCP_INTEGRATION.md](MCP_INTEGRATION.md#capabilities) for parameters,
validation, and error behavior.

## Policies and project health

- [SECURITY.md](SECURITY.md) — security posture (HTTP has **no
  authentication**; keep it on localhost)
- [ETHICAL_USE.md](ETHICAL_USE.md) — authorized use only
- [RELEASE_NOTES.md](RELEASE_NOTES.md) — 2.0.0 release state
- [ROADMAP.md](ROADMAP.md) — phased future work
- [CONTRIBUTING.md](CONTRIBUTING.md) — how to contribute (root guide:
  [../CONTRIBUTING.md](../CONTRIBUTING.md))
- [DATASET.md](DATASET.md) — data integrity, SHA-256, restore

## Try a real session

Captured, unedited output from a real stdio MCP session lives in
[demo/](demo/DEMO.md) — including tool list, `index_stats`, a semantic search,
threshold behavior, and the HTTP startup probe.

---

RIFT · Red-team Intelligence & Fusion Toolkit ·
[GitHub](https://github.com/Sabriigsxr/RIFT) ·
[Ethical use](ETHICAL_USE.md) · [Security](SECURITY.md)
