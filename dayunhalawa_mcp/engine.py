"""
DayunHalawa-MCP — retrieval engine for the offensive-scenario knowledge base.

Loads a local FAISS index of pentesting / DFIR / TTPs Q&A pairs and performs
semantic search. No network access is required at query time once the
sentence-transformers model is cached (or present locally).
"""
from __future__ import annotations

import json
import os
import threading
from pathlib import Path
from typing import Any, Optional

import faiss
import numpy as np

# Package root = repo root (parent of this file's directory)
REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INDEX_DIR = REPO_ROOT / "index"

MODEL_NAME = os.environ.get("DAYUNHALAWA_MODEL", "sentence-transformers/all-MiniLM-L6-v2")


def _resolve_index_dir(index_dir: Optional[str | os.PathLike] = None) -> Path:
    if index_dir:
        return Path(index_dir).expanduser().resolve()
    env = os.environ.get("DAYUNHALAWA_INDEX_DIR")
    if env:
        return Path(env).expanduser().resolve()
    return DEFAULT_INDEX_DIR


class Engine:
    """FAISS + sentence-transformers retrieval engine (lazy singleton)."""

    def __init__(self, index_dir: Optional[str | os.PathLike] = None):
        from sentence_transformers import SentenceTransformer  # deferred import

        self.index_dir = _resolve_index_dir(index_dir)
        faiss_path = self.index_dir / "faiss.index"
        docs_path = self.index_dir / "documents.jsonl"
        meta_path = self.index_dir / "metadata.jsonl"
        for p in (faiss_path, docs_path, meta_path):
            if not p.exists():
                raise FileNotFoundError(
                    f"Index file missing: {p}. Expected faiss.index, documents.jsonl "
                    f"and metadata.jsonl in DAYUNHALAWA_INDEX_DIR (current: {self.index_dir}). "
                    "See README.md#building-the-index."
                )

        self.model = SentenceTransformer(MODEL_NAME)
        self.index = faiss.read_index(str(faiss_path))
        with meta_path.open(encoding="utf-8") as fh:
            self.metadata = [json.loads(l) for l in fh if l.strip()]
        self.documents: dict[str, dict] = {}
        with docs_path.open(encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                d = json.loads(line)
                doc_id = d.get("doc_id")
                if doc_id:
                    self.documents[doc_id] = d

    @property
    def stats(self) -> dict[str, Any]:
        return {
            "index_dir": str(self.index_dir),
            "model": MODEL_NAME,
            "vectors": int(self.index.ntotal),
            "metadata_entries": len(self.metadata),
            "documents": len(self.documents),
        }

    def search(self, query: str, top_k: int = 5, threshold: float = 0.25) -> list[dict[str, Any]]:
        top_k = max(1, min(int(top_k), 20))
        threshold = float(max(0.0, min(threshold, 1.0)))
        q = self.model.encode(
            [query],
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
        ).astype("float32")
        scores, idxs = self.index.search(q, top_k)
        out: list[dict[str, Any]] = []
        for score, idx in zip(scores[0], idxs[0]):
            if idx == -1:
                continue
            s = float(score)
            if s < threshold:
                continue
            meta = self.metadata[idx] if idx < len(self.metadata) else {}
            doc = self.documents.get(meta.get("doc_id", ""), {})
            out.append(
                {
                    "doc_id": meta.get("doc_id"),
                    "score": round(s, 4),
                    "category": meta.get("category"),
                    "difficulty": meta.get("difficulty"),
                    "tags": meta.get("tags") or [],
                    "cve_references": meta.get("cve_references") or [],
                    "tools_used": meta.get("tools_used") or [],
                    "question": doc.get("question"),
                    "answer": doc.get("answer"),
                }
            )
        return out


_lock = threading.Lock()
_engine: Optional[Engine] = None


def get_engine() -> Engine:
    global _engine
    if _engine is None:
        with _lock:
            if _engine is None:
                _engine = Engine()
    return _engine
