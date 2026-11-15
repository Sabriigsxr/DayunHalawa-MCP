import json
import sys
import types

import pytest

from rift_mcp import engine


class FakeIndex:
    d = 2
    ntotal = 2

    def search(self, query, top_k):
        return [[0.9, 0.2]], [[0, 1]]


class FakeEmbeddings:
    def astype(self, _dtype):
        return self


class FakeModel:
    def get_sentence_embedding_dimension(self):
        return 2

    def encode(self, queries, **kwargs):
        return FakeEmbeddings()


def write_index(tmp_path, metadata=None, documents=None):
    metadata = metadata or [{"doc_id": "a"}, {"doc_id": "b"}]
    documents = documents or [
        {"doc_id": "a", "question": "first", "answer": "one"},
        {"doc_id": "b", "question": "second", "answer": "two"},
    ]
    (tmp_path / "faiss.index").write_bytes(b"fixture")
    for name, records in (("metadata.jsonl", metadata), ("documents.jsonl", documents)):
        (tmp_path / name).write_text(
            "".join(json.dumps(record) + "\n" for record in records),
            encoding="utf-8",
        )


@pytest.fixture
def fake_dependencies(monkeypatch):
    monkeypatch.setitem(
        sys.modules,
        "faiss",
        types.SimpleNamespace(read_index=lambda _: FakeIndex()),
    )
    monkeypatch.setitem(
        sys.modules,
        "sentence_transformers",
        types.SimpleNamespace(SentenceTransformer=lambda _: FakeModel()),
    )
    monkeypatch.setattr(engine, "MODEL_NAME", "test-model")


def test_engine_validates_alignment_and_searches(tmp_path, fake_dependencies):
    write_index(tmp_path)
    instance = engine.Engine(tmp_path)

    assert instance.stats["vectors"] == 2
    assert instance.stats["dimensions"] == 2
    assert instance.search("find it", top_k=2)[0]["doc_id"] == "a"


@pytest.mark.parametrize(
    "metadata",
    [
        [{"doc_id": "a"}],
        [{"doc_id": "a"}, {"doc_id": "missing"}],
        [{"doc_id": "a"}, {"doc_id": "a"}],
    ],
)
def test_engine_rejects_bad_metadata(tmp_path, fake_dependencies, metadata):
    write_index(tmp_path, metadata=metadata)
    with pytest.raises(ValueError):
        engine.Engine(tmp_path)


def test_engine_rejects_empty_query(tmp_path, fake_dependencies):
    write_index(tmp_path)
    instance = engine.Engine(tmp_path)
    with pytest.raises(ValueError, match="non-empty"):
        instance.search("   ")


def test_engine_rejects_dimension_mismatch(tmp_path, monkeypatch, fake_dependencies):
    write_index(tmp_path)

    class WrongModel(FakeModel):
        def get_sentence_embedding_dimension(self):
            return 3

    monkeypatch.setitem(
        sys.modules,
        "sentence_transformers",
        types.SimpleNamespace(SentenceTransformer=lambda _: WrongModel()),
    )
    with pytest.raises(ValueError, match="dimension mismatch"):
        engine.Engine(tmp_path)
