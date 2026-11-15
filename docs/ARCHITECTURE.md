# Architecture

```mermaid
flowchart TD
    C[MCP client] --> T[RIFT MCP server]
    T --> API[Tools and prompt]
    API --> E[Retrieval engine]
    E --> M[Sentence Transformer]
    E --> F[FAISS IndexFlatIP]
    E --> MD[metadata.jsonl]
    E --> D[documents.jsonl]
    E --> R[Ranked extractive results]
    R --> C
    I[documents.jsonl input] --> B[build_index.py]
    B --> M
    B --> F
    B --> MD
    B --> D
```

Index construction embeds `question` plus `answer` with normalized
Sentence-Transformers vectors, writes an inner-product FAISS index, and keeps
the document and metadata lines in the same order. Query handling embeds one
non-empty query, searches up to 20 vectors, applies the configured threshold,
and maps each vector position through metadata to a document ID.

The server returns either structured JSON (`search_offensive_scenarios`) or a
human-readable extractive rendering (`ask_offensive_scenario`). It does not
generate attack plans, execute commands, or write query-time files. Missing
files, malformed JSONL, alignment errors, and dimension mismatches are
reported as explicit startup errors.
