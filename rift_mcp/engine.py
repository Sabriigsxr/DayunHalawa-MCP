"""RIFT retrieval engine for the offensive-scenario knowledge base.

Loads a local FAISS index of pentesting / DFIR / TTPs Q&A pairs and performs
semantic search. No network access is required at query time once the
sentence-transformers model is cached (or present locally).
"""
from __future__ import annotations

import json
import os
import threading
from pathlib import Path
from typing import Any

# Package root = repo root (parent of this file's directory)
REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INDEX_DIR = REPO_ROOT / "index"

DEFAULT_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def _first_env(*names: str, default: str) -> str:
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return default


MODEL_NAME = _first_env("RIFT_MODEL", default=DEFAULT_MODEL_NAME)


def _resolve_index_dir(index_dir: str | os.PathLike | None = None) -> Path:
    if index_dir:
        return Path(index_dir).expanduser().resolve()
    env = _first_env("RIFT_INDEX_DIR", default="")
    if env:
        return Path(env).expanduser().resolve()
    return DEFAULT_INDEX_DIR


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    try:
        with path.open(encoding="utf-8") as fh:
            for line_number, line in enumerate(fh, 1):
                if not line.strip():
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ValueError(f"Invalid JSON in {path} at line {line_number}: {exc}") from exc
                if not isinstance(record, dict):
                    raise TypeError(f"Expected an object in {path} at line {line_number}")
                records.append(record)
    except UnicodeDecodeError as exc:
        raise ValueError(f"{path} is not valid UTF-8: {exc}") from exc
    return records


class Engine:
    """FAISS + sentence-transformers retrieval engine (lazy singleton)."""

    def __init__(self, index_dir: str | os.PathLike | None = None):
        import faiss  # deferred import so configuration errors remain inspectable without FAISS
        from sentence_transformers import SentenceTransformer  # deferred import

        self.index_dir = _resolve_index_dir(index_dir)
        faiss_path = self.index_dir / "faiss.index"
        docs_path = self.index_dir / "documents.jsonl"
        meta_path = self.index_dir / "metadata.jsonl"
        for p in (faiss_path, docs_path, meta_path):
            if not p.exists():
                raise FileNotFoundError(
                    f"Index file missing: {p}. Expected faiss.index, documents.jsonl "
                    f"and metadata.jsonl in RIFT_INDEX_DIR (current: {self.index_dir}). "
                    "See docs/TROUBLESHOOTING.md."
                )

        self.index = faiss.read_index(str(faiss_path))
        self.metadata = _read_jsonl(meta_path)
        self.documents: dict[str, dict] = {}
        for document in _read_jsonl(docs_path):
            doc_id = document.get("doc_id")
            if not isinstance(doc_id, str) or not doc_id:
                raise ValueError(f"Document in {docs_path} is missing a non-empty doc_id")
            if doc_id in self.documents:
                raise ValueError(f"Duplicate doc_id {doc_id!r} in {docs_path}")
            self.documents[doc_id] = document

        if self.index.ntotal != len(self.metadata):
            raise ValueError(
                f"Index/data mismatch in {self.index_dir}: FAISS contains {self.index.ntotal} "
                f"vectors but metadata.jsonl contains {len(self.metadata)} records"
            )
        metadata_ids = []
        for position, metadata in enumerate(self.metadata, 1):
            doc_id = metadata.get("doc_id")
            if not isinstance(doc_id, str) or not doc_id:
                raise ValueError(f"Metadata record {position} is missing a non-empty doc_id")
            metadata_ids.append(doc_id)
            if doc_id not in self.documents:
                raise ValueError(f"Metadata doc_id {doc_id!r} has no matching document")
        if len(set(metadata_ids)) != len(metadata_ids):
            raise ValueError(f"Duplicate doc_id values in {meta_path}")
        if len(self.documents) != len(self.metadata):
            raise ValueError(
                f"Document/metadata mismatch in {self.index_dir}: documents.jsonl contains "
                f"{len(self.documents)} records but metadata.jsonl contains {len(self.metadata)}"
            )

        self.model = SentenceTransformer(MODEL_NAME)
        if hasattr(self.model, "get_embedding_dimension"):
            model_dimension = self.model.get_embedding_dimension()
        else:
            model_dimension = self.model.get_sentence_embedding_dimension()
        if model_dimension and model_dimension != self.index.d:
            raise ValueError(
                f"Embedding dimension mismatch: model {MODEL_NAME!r} produces {model_dimension} "
                f"dimensions but the FAISS index expects {self.index.d}"
            )

    @property
    def stats(self) -> dict[str, Any]:
        return {
            "index_dir": str(self.index_dir),
            "model": MODEL_NAME,
            "vectors": int(self.index.ntotal),
            "dimensions": int(self.index.d),
            "index_type": type(self.index).__name__,
            "metadata_entries": len(self.metadata),
            "documents": len(self.documents),
        }

    def search(self, query: str, top_k: int = 5, threshold: float = 0.25) -> list[dict[str, Any]]:
        if not isinstance(query, str) or not query.strip():
            raise ValueError("query must be a non-empty string")
        if isinstance(top_k, bool):
            raise TypeError("top_k must be an integer between 1 and 20")
        if isinstance(threshold, bool):
            raise TypeError("threshold must be a number between 0 and 1")
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
_engine: Engine | None = None


def get_engine() -> Engine:
    global _engine
    if _engine is None:
        with _lock:
            if _engine is None:
                _engine = Engine()
    return _engine
