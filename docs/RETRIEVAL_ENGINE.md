# Retrieval engine

RIFT uses normalized Sentence-Transformers embeddings and FAISS inner-product
search. With normalized vectors, the inner product is cosine similarity. The
default result threshold is `0.25`; `top_k` is clamped to 1–20 to bound
result size and cost.

The loader validates:

1. `faiss.index`, `documents.jsonl`, and `metadata.jsonl` exist.
2. Every JSONL line is a UTF-8 JSON object.
3. Every document and metadata record has a unique non-empty `doc_id`.
4. FAISS `ntotal` equals the metadata record count.
5. Every metadata ID maps to one document.
6. The embedding model dimension equals the FAISS index dimension.

These checks do not judge the truth or safety of retrieved text. The data is
reference material and must be reviewed in its authorization and operational
context before use.
