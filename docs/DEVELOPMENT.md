# Development

```bash
python3 -m venv .venv
.venv/bin/pip install -e '.[dev]'
.venv/bin/pytest
.venv/bin/ruff check .
python -m compileall -q dayunhalawa_mcp scripts
```

Keep the original `dayunhalawa_mcp` import path stable. New public
configuration should prefer `RIFT_*`, while legacy `DAYUNHALAWA_*` names must
remain documented until a future deprecation decision. Do not regenerate the
bundled index as part of tests. Use temporary directories for extraction and
index-building tests.
