# Dataset and index

The tracked `data/index.tar.gz` contains the FAISS index plus aligned JSONL
stores. The archive's
record counts are 23,737 document lines and 23,737 metadata lines. Its
SHA-256 is recorded in `data/index.tar.gz.sha256`.

The archive is restored into the git-ignored `index/` directory:

```bash
bash scripts/restore_index.sh
```

RIFT never regenerates or downloads a replacement index automatically. Build a
new index only from data you are authorized to use:

```bash
.venv/bin/python scripts/build_index.py \
  --documents /path/to/documents.jsonl \
  --out /path/to/new-index
```

The builder validates records and refuses to overwrite a populated output
directory unless `--force` is explicitly supplied. Dataset provenance,
redistribution rights, and content quality remain the responsibility of the
index owner; the repository currently has no dataset license statement.

---

RIFT · Red-team Intelligence & Fusion Toolkit ·
[Documentation index](README.md) · [GitHub](https://github.com/Sabriigsxr/RIFT) ·
[Ethical use](ETHICAL_USE.md) · [Security](SECURITY.md)
