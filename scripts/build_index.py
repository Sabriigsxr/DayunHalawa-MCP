#!/usr/bin/env python3
"""Build a validated FAISS index from a documents.jsonl file.

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
from tempfile import TemporaryDirectory

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


def main() -> int:
    ap = argparse.ArgumentParser(description="Build FAISS index from documents.jsonl")
    ap.add_argument("--documents", required=True, help="Path to documents.jsonl")
    ap.add_argument("--out", required=True, help="Output index directory")
    ap.add_argument("--model", default="sentence-transformers/all-MiniLM-L6-v2")
    ap.add_argument("--batch-size", type=int, default=64)
    ap.add_argument("--force", action="store_true", help="Replace an existing populated output directory")
    args = ap.parse_args()

    if args.batch_size < 1:
        ap.error("--batch-size must be positive")

    docs = []
    with open(args.documents, encoding="utf-8") as fh:
        for line_number, line in enumerate(fh, 1):
            if not line.strip():
                continue
            try:
                document = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON at line {line_number}: {exc}") from exc
            if not isinstance(document, dict):
                raise TypeError(f"Line {line_number} is not a JSON object")
            doc_id = document.get("doc_id")
            if not isinstance(doc_id, str) or not doc_id:
                raise ValueError(f"Line {line_number} is missing a non-empty doc_id")
            if not document.get("question") and not document.get("answer"):
                raise ValueError(f"Line {line_number} must contain question or answer text")
            docs.append(document)
    if not docs:
        raise ValueError("documents.jsonl does not contain any records")
    ids = [d["doc_id"] for d in docs]
    if len(set(ids)) != len(ids):
        raise ValueError("documents.jsonl contains duplicate doc_id values")

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

    out = Path(args.out).expanduser().resolve()
    if out.exists() and not out.is_dir():
        raise NotADirectoryError(f"Output path is not a directory: {out}")
    out.parent.mkdir(parents=True, exist_ok=True)
    existing = [p for p in out.glob("*")] if out.exists() else []
    if existing and not args.force:
        raise FileExistsError(f"Refusing to overwrite populated output directory {out}; use --force")

    with TemporaryDirectory(prefix=".rift-index-", dir=out.parent) as temp_dir:
        temp = Path(temp_dir)
        index = faiss.IndexFlatIP(mat.shape[1])
        index.add(mat)
        faiss.write_index(index, str(temp / "faiss.index"))

        with (temp / "documents.jsonl").open("w", encoding="utf-8") as fh:
            for d in docs:
                fh.write(json.dumps(d, ensure_ascii=False) + "\n")

        with (temp / "metadata.jsonl").open("w", encoding="utf-8") as fh:
            for d in docs:
                meta = {k: v for k, v in d.items() if k not in ("question", "answer")}
                fh.write(json.dumps(meta, ensure_ascii=False) + "\n")

        out.mkdir(parents=True, exist_ok=True)
        for artifact in temp.iterdir():
            target = out / artifact.name
            if target.exists():
                target.unlink()
            artifact.replace(target)

    print(f"Built index: {mat.shape[0]} vectors @ {mat.shape[1]} dims -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
