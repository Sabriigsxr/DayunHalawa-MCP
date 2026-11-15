# Changelog

## 2.0.0 — Initial public RIFT release

- **RIFT — Red-team Intelligence & Fusion Toolkit.** MCP-powered offensive
  security intelligence engine using local semantic retrieval (FAISS +
  Sentence Transformers).
- MCP server exposing `search_offensive_scenarios`, `ask_offensive_scenario`,
  and `index_stats`, plus the `offensive_scenario_brief` prompt.
- stdio transport by default; streamable HTTP on localhost (`--transport http`).
- Bundled 23,737-entry offensive-security Q&A knowledge base, SHA-256-verified
  and alignment-checked before use.
- Made in Egypt 🇪🇬 — Ahmed Sabry, Cyber Security Researcher.
- Offline query operation once the embedding model is cached.
- Only authorized defensive/educational use is permitted; see WARNING.txt.

No prior code history is carried forward.

No license has been selected yet.
