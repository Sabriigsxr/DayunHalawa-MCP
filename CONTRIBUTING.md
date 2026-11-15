# Contributing

Contributions should preserve local-first operation, the existing knowledge
base, and the authorized-use scope. Do not add cloud-only or paid runtime
requirements, autonomous exploitation, arbitrary command execution, or
unreviewed target data.

Before opening a pull request:

```bash
.venv/bin/pip install -e '.[dev]'
.venv/bin/pytest
.venv/bin/ruff check .
python -m compileall -q rift_mcp scripts
```

Describe compatibility impact, data provenance, security implications, and
manual verification. Do not commit generated indexes, model caches, secrets,
or target data. The project currently has no license; contributions should
not assume redistribution rights for third-party data.
