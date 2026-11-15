# Installation

RIFT supports Python 3.10+ and local execution. No paid API or cloud service
is required at query time.

```bash
git clone https://github.com/Sabriigsxr/RIFT.git
cd RIFT
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/pip install -e .
bash scripts/restore_index.sh
```

The restore script verifies the tracked SHA-256 before extracting the bundled
archive. It will not replace an existing `index/` unless `--force` is passed.
To use a separately built index, set `RIFT_INDEX_DIR` (the legacy
`DAYUNHALAWA_INDEX_DIR` remains supported).

The first query may require the embedding model to be present in the local
Hugging Face cache. After the model and index are available, retrieval can run
offline with `HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1`.
