# RIFT product overview

Short, visual-first presentation. Each slide has one dominant visual and a
single message.

## Slide 1 — Identity

![RIFT](../../assets/visuals/rift-hero.svg)

**RIFT — Local Offensive Security Knowledge Engine**

## Slide 2 — The problem

![Product overview](../../assets/visuals/rift-product-overview.svg)

Security knowledge is valuable only when a team can find and inspect it during
real work.

## Slide 3 — The solution

RIFT gives an MCP client a local, citable retrieval layer over the existing
knowledge base.

## Slide 4 — How it works

![Data flow](../../assets/visuals/rift-data-flow.svg)

Question → embedding → FAISS similarity search → aligned source records.

![Main architecture diagram](rift-main-architecture.svg)

## Slide 5 — Semantic search

![Semantic search](../../assets/visuals/rift-comparison.svg)

Related wording can match by meaning. The illustration is conceptual, not a
benchmark.

## Slide 6 — MCP integration

![MCP](../../assets/visuals/rift-mcp-workflow.svg)

stdio is the default transport; streamable HTTP is optional and should remain
protected.

## Slide 7 — Local-first architecture

![Local first](../../assets/visuals/rift-local-first.svg)

Model, index, records, and retrieval stay on the host after model caching.

## Slide 8 — Real product screenshots

Runtime screenshots are pending in this environment because no terminal
screenshot capture tool is installed. See the implementation report and
`assets/screenshots/CAPTURE_CHECKLIST.md`; no mockups are labeled as real.

## Slide 9 — Example workflow

![Getting started](../../assets/visuals/rift-getting-started.svg)

Install → restore the verified index → connect an MCP client → inspect sources.

## Slide 10 — Capabilities and limitations

Implemented: semantic search, extractive answers, index stats, and one prompt.
Not implemented: shell tools, command execution, autonomous exploitation,
streaming responses, or HTTP authentication.

## Slide 11 — Roadmap

See the maintained [roadmap](../ROADMAP.md). Roadmap items are not presented
as shipped capabilities.

## Slide 12 — Getting started

Follow [FIRST_SEARCH_TUTORIAL.md](../visual-guide/FIRST_SEARCH_TUTORIAL.md),
then read [ETHICAL_USE.md](../ETHICAL_USE.md) and
[SECURITY.md](../SECURITY.md).
