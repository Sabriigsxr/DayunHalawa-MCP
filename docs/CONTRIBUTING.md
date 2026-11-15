# Contributing

Contributions must preserve RIFT's local-first design, offline capability,
bundled knowledge base, and authorized-use scope. See the repository-wide
[../CONTRIBUTING.md](../CONTRIBUTING.md) for the full guide; this page is the
quick reference and the docs-specific rules.

## Quickstart

```bash
python3 -m venv .venv
.venv/bin/pip install -e '.[dev]'
.venv/bin/pytest
.venv/bin/ruff check .
python -m compileall -q rift_mcp scripts tests
```

## Rules

- No cloud-only or paid runtime requirements.
- No autonomous exploitation, shell execution tools, or arbitrary command
  execution in the server.
- Do not regenerate, reduce, or replace `data/index.tar.gz`.
- Do not invent capabilities in docs — describe only what the code does.
- Preserve authorized-use framing in all security content.
- Documentation pages must keep the same structure, tone, and footer nav;
  verify all internal links (`scripts/` link checks, or manual).

## Documentation contributions

1. Match the heading hierarchy of the page you edit; keep the footer line.
2. Commands must be copy-pasteable and verified against the real CLI
   (`rift --help`, `rift_mcp` entry points) — never invent flags.
3. Label captured output as captured, and trims as trims.
4. Keep RIFT naming consistent: **RIFT — Red-team Intelligence & Fusion
   Toolkit**.

## Graphics and diagrams

Brand and diagram assets (`assets/branding/`, `docs/diagrams/`) are original.
Reuse them via the guidelines in `assets/branding/rift-brand-guidelines.md`;
do not add third-party logos or stock imagery.

---

RIFT · Red-team Intelligence & Fusion Toolkit ·
[Documentation index](README.md) · [GitHub](https://github.com/Sabriigsxr/RIFT) ·
[Ethical use](ETHICAL_USE.md) · [Security](SECURITY.md)
