# RIFT 2.0.0 release notes

## Status

Prepared, not published. This release must not be tagged or uploaded until
ownership, dataset redistribution rights, repository metadata, and the final
security contact are reviewed by the maintainer.

## Highlights

- RIFT identity and original visual assets.
- Local-first MCP server with stdio and localhost streamable HTTP.
- Legacy package, command, environment variables, tools, and prompt retained.
- Integrity checks for JSONL, FAISS/document alignment, IDs, and dimensions.
- Safe checksum verification and archive extraction.
- Documentation, CI, tests, contributor files, and migration guidance.

## Known limitations

- The repository still has no selected license.
- The HTTP endpoint has no built-in authentication.
- Retrieval quality is not a substitute for human review or dataset
  provenance.
- CI validates fixtures and code paths but does not restore or regenerate the
  207 MB-class index artifact.
- Cross-version MCP behavior is covered by the compatibility import path but
  not by a matrix of every MCP SDK release.

## Verification checklist

- [x] Original HEAD and working-tree state recorded.
- [x] Original archive and checksum preserved.
- [x] Focused tests pass locally.
- [x] Ruff and compile checks pass locally.
- [x] Package installation and both CLI aliases verified.
- [x] Real FAISS index loaded and queried offline in the local environment.
- [x] Localhost HTTP startup verified.
- [ ] Maintainer confirms licensing and dataset rights.
- [ ] Maintainer reviews GitHub metadata and repository rename.
- [ ] Maintainer performs a clean-machine install from the eventual RIFT URL.
- [ ] Maintainer tags and publishes only after explicit approval.
