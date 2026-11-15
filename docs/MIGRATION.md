# Migration from DayunHalawa-MCP to RIFT

RIFT 2.0.0 is a branding and hardening migration, not a replacement of the
knowledge base.

## Compatibility retained

- Python imports remain under `dayunhalawa_mcp`.
- `dayunhalawa-mcp` remains an installed command.
- Existing tools and prompt names are unchanged.
- `DAYUNHALAWA_INDEX_DIR` and `DAYUNHALAWA_MODEL` remain accepted.
- Existing Claude Desktop and OpenCode process configurations continue to
  launch the same module.
- `data/index.tar.gz` and its original hash are preserved byte-for-byte.

## Preferred changes

Use the new package metadata and command:

```bash
.venv/bin/pip install -e .
.venv/bin/rift
```

Prefer `RIFT_INDEX_DIR` and `RIFT_MODEL` in new configurations, and use
`rift` as the MCP client display name. No tool-name migration is required.

## Breaking or operational changes

- The distribution metadata is now `rift-mcp` version `2.0.0`; users who
  install by distribution name should reinstall from the RIFT repository.
- Malformed JSONL, document/metadata misalignment, FAISS count mismatches, and
  embedding dimension mismatches now fail closed instead of producing partial
  results.
- Archive restoration refuses symlink destinations and unsafe member paths.
  `--force` is required to replace an existing index directory.

No automatic index regeneration or cloud dependency was introduced.
