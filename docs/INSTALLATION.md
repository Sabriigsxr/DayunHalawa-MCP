# Installation

RIFT supports Python 3.10+ on Linux, macOS, and Windows (via WSL). No paid
API, cloud service, or GPU is required.

## From GitHub (recommended)

```bash
git clone https://github.com/Sabriigsxr/RIFT.git
cd RIFT
python3 -m venv .venv
.venv/bin/pip install -e .
bash scripts/restore_index.sh
```

- `pip install -e .` installs the `rift-mcp` distribution and creates the
  `rift` console command and the `rift_mcp` import package.
- `scripts/restore_index.sh` verifies the tracked SHA-256 for
  `data/index.tar.gz`, validates member paths and types, extracts to the
  git-ignored `./index/` directory, and refuses to clobber existing content
  without `--force`.
- To use a separately built index, set `RIFT_INDEX_DIR=/path/to/index` instead
  of restoring.

## Verify the install

```bash
.venv/bin/rift --version        # expected: rift 2.0.0
```

Restoring a working index and performing a search is covered end-to-end in
[GETTING_STARTED.md](GETTING_STARTED.md#from-zero-to-your-first-rift-mcp-search).

## Model cache and offline use

The first query downloads
`sentence-transformers/all-MiniLM-L6-v2` (~80 MB) into the local
Hugging Face cache. After that, RIFT can run fully offline:

```bash
export HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1
```

The model dimensions are checked against the FAISS index at load time; a
mismatch fails with an explicit error (see
[TROUBLESHOOTING.md](TROUBLESHOOTING.md)).

## Platform notes

- **Linux:** `apt install python3 python3-venv` if needed; ensure
  `sha256sum` and `tar` are present (both are standard on mainstream distros;
  the restore script also requires Python 3).
- **macOS:** the restore script uses `sha256sum` when present, otherwise
  falls back to `shasum -a 256`, and needs Python 3. Both are available via
  macOS's default toolset or Homebrew coreutils.
- **Windows:** use WSL2 for the restore script, or extract `data/index.tar.gz`
  with a tool that preserves paths, then run RIFT with `RIFT_INDEX_DIR` set.
- **CI:** `.github/workflows/ci.yml` installs the package with `.[dev]`,
  runs pytest, ruff, and compileall. It does not restore the bundled index.

## Development install

```bash
.venv/bin/pip install -e '.[dev]'
.venv/bin/pytest
.venv/bin/ruff check .
```

---

RIFT · Red-team Intelligence & Fusion Toolkit ·
[Documentation index](README.md) · [GitHub](https://github.com/Sabriigsxr/RIFT) ·
[Ethical use](ETHICAL_USE.md) · [Security](SECURITY.md)
