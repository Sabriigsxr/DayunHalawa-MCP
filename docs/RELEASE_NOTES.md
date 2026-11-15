# RIFT 2.0.0 — release notes

## Status

Prepared, not published. Tag and publish only after maintainer review of
ownership, dataset redistribution rights, final repository metadata, and the
security contact.

## Highlights

- RIFT — Red-team Intelligence & Fusion Toolkit identity and original
  visual assets. Made in Egypt 🇪🇬 — Ahmed Sabry, Cyber Security Researcher.
- Local-first MCP server with stdio and localhost streamable HTTP.
- Integrity checks for JSONL parsing, document/metadata alignment, FAISS
  vector counts, doc IDs, and embedding dimensions.
- SHA-256-verified bundled index with safe, traversal-checked restoration.
- Fail-closed validation: malformed inputs produce explicit errors rather
  than partial or misleading results.
- Documentation, CI workflow, tests, examples, and contributor files.
- Extractive retrieval: no generated attack plans, no network at query
  time after setup.

## Known limitations

- No selected license yet; treat the project and bundled data as reserved.
- The HTTP endpoint has no built-in authentication; bind localhost only or
  put it behind an access-controlled boundary.
- Retrieval quality is not a substitute for human review.
- CI validates fixtures and code paths; it does not restore or rebuild the
  bundled index archive (about 53 MB compressed, ~155 MB restored).
- MCP SDK 1.x/2.x compatibility is provided by an import shim, not by a
  version matrix.

## Verification checklist

- [x] Bundled archive and checksum preserved and verified.
- [x] Focused tests pass locally.
- [x] Ruff and compile checks pass locally.
- [x] Package installation and `rift` console script verified.
- [x] Real FAISS index loaded and queried offline locally.
- [x] Localhost HTTP startup verified.
- [ ] Maintainer confirms licensing and dataset rights.
- [ ] Maintainer performs a clean-machine install.
- [ ] Maintainer tags and publishes only after explicit approval.
