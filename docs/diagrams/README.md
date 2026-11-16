# RIFT — Architecture diagrams

Mermaid sources of the diagrams referenced by
[`../ARCHITECTURE.md`](../ARCHITECTURE.md) and
[`../HOW_IT_WORKS.md`](../HOW_IT_WORKS.md). Render them with any Mermaid
renderer (GitHub renders Mermaid natively; `mmdc` for CLI export).

| Diagram | What it shows | Primary reference |
|---|---|---|
| [`system-architecture.mmd`](system-architecture.mmd) | End-to-end system: clients → transport → MCP server → engine → local data | [`../ARCHITECTURE.md`](../ARCHITECTURE.md) |
| [`data-ingestion-flow.mmd`](data-ingestion-flow.mmd) | `documents.jsonl` → validation → embeddings → FAISS `IndexFlatIP` → bundled archive → restore | [`../HOW_IT_WORKS.md`](../HOW_IT_WORKS.md) |
| [`semantic-search-flow.mmd`](semantic-search-flow.mmd) | Query → validation → encode → `index.search` → threshold → result mapping | [`../HOW_IT_WORKS.md`](../HOW_IT_WORKS.md) |
| [`mcp-integration-flow.mmd`](mcp-integration-flow.mmd) | Real request path over stdio and HTTP, including lazy engine load | [`../MCP_INTEGRATION.md`](../MCP_INTEGRATION.md) |
| [`deployment-architecture.mmd`](deployment-architecture.mmd) | Single-host local-first deployment and its boundaries | [`../../README.md`](../../README.md) |

Rendered exports are available in [`rendered/`](rendered/):
`system-architecture.svg`, `data-ingestion-flow.svg`,
`semantic-search-flow.svg`, `mcp-integration-flow.svg`, and
`deployment-architecture.svg`.

All diagrams describe the **actual implementation** in `rift_mcp/`,
`scripts/`, and `data/` — they do not depict unimplemented features, and RIFT
is not an autonomous exploitation engine.
