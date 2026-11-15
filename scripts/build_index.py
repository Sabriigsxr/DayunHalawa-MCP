#!/usr/bin/env python3
"""
Rebuild the FAISS index from a documents.jsonl file.

Each line in documents.jsonl must be a JSON object with at least:
    {"doc_id": "...", "question": "...", "answer": "..."}
Any additional keys (category, difficulty, tags, cve_references, tools_used, ...)
are copied into metadata.jsonl.

Usage:
    python scripts/build_index.py --documents /path/to/documents.jsonl \
        --out /path/to/index
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


def main() -> int:
    ap = argparse.ArgumentParser(description="Build FAISS index from documents.jsonl")
    ap.add_argument("--documents", required=True, help="Path to documents.jsonl")
    ap.add_argument("--out", required=True, help="Output index directory")
    ap.add_argument("--model", default="sentence-transformers/all-MiniLM-L6-v2")
    ap.add_argument("--batch-size", type=int, default=64)
    args = ap.parse_args()

    docs = []
    with open(args.documents, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                docs.append(json.loads(line))

    model = SentenceTransformer(args.model)
    texts = [f"{d.get('question', '')}\n{d.get('answer', '')}" for d in docs]
    embs = []
    for i in range(0, len(texts), args.batch_size):
        embs.append(
            model.encode(
                texts[i : i + args.batch_size],
                normalize_embeddings=True,
                convert_to_numpy=True,
                show_progress_bar=True,
                batch_size=args.batch_size,
            )
        )
    mat = np.vstack(embs).astype("float32")

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    index = faiss.IndexFlatIP(mat.shape[1])
    index.add(mat)
    faiss.write_index(index, str(out / "faiss.index"))

    with (out / "documents.jsonl").open("w", encoding="utf-8") as fh:
        for d in docs:
            fh.write(json.dumps(d, ensure_ascii=False) + "\n")

    with (out / "metadata.jsonl").open("w", encoding="utf-8") as fh:
        for d in docs:
            meta = {k: v for k, v in d.items() if k not in ("question", "answer")}
            fh.write(json.dumps(meta, ensure_ascii=False) + "\n")

    print(f"Built index: {mat.shape[0]} vectors @ {mat.shape[1]} dims -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
