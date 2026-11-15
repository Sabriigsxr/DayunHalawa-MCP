# Development

```bash
python3 -m venv .venv
.venv/bin/pip install -e '.[dev]'
.venv/bin/pytest
.venv/bin/ruff check .
python -m compileall -q rift_mcp scripts tests
```

Keep the `rift_mcp` package import path stable. Public configuration uses
`RIFT_*` variables. Do not regenerate the bundled index as part of tests. Use
temporary directories for extraction and index-building tests.
