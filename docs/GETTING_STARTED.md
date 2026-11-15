# Getting started with RIFT

**RIFT — Red-team Intelligence & Fusion Toolkit** is a local-first MCP server
that searches an existing offensive-security knowledge base and returns the
stored Q&A entries that match your question. This page teaches it from the
ground up — no prior security, MCP, or machine-learning background required.

> **Authorized use only.** Use RIFT only on systems and datasets you own or are
> explicitly authorized to assess. See [ETHICAL_USE.md](ETHICAL_USE.md) and
> [../WARNING.txt](../WARNING.txt).

---

## Beginner — what is RIFT?

### What is MCP?

The **Model Context Protocol (MCP)** is an open standard for connecting AI
applications (the *client*, e.g. OpenCode or Claude Desktop) to context
providers (the *server*, e.g. RIFT). Instead of scraping websites, the client
asks the server for structured answers over a defined channel.

### What is a vector database?

A knowledge base with thousands of Q&A entries is too large to feed to a model
at once, and keyword search misses meaning (“privilege escalation” vs.
“getting root”). A vector database stores each entry as a list of numbers —
an **embedding** — so similar meanings land near each other. RIFT uses
**FAISS**, Facebook AI Similarity Search, as a local, in-process vector index.
The index type is `IndexFlatIP`: an exact flat scan using inner products.

### What is an embedding?

An embedding is a fixed-length numeric vector representing text meaning. RIFT
embeds entries with `sentence-transformers/all-MiniLM-L6-v2` (384 numbers per
text). Because vectors are normalized, the **inner product is cosine
similarity** — a 1.0 means "identical direction" and 0.0 means "unrelated".

### Why semantic search is useful

Ask “detect Kerberoasting” and RIFT finds entries about Event ID 4769 and
T1558 even if they never use the word “Kerberoasting” the same way — matching
on meaning, not spelling.

### Who RIFT is for

Authorized penetration testers, detection engineers, DFIR teams, educators,
and researchers who want local, inspectable retrieval of existing knowledge —
**not** an autopilot for attacks.

---

## From Zero to Your First RIFT MCP Search

A complete, copy-pasteable path. Every command below was run for real while
writing this page; captured output is shown inline, trimmed with
`…` where shortened.

### Step 1 — Install

```bash
git clone https://github.com/Sabriigsxr/RIFT.git
cd RIFT
python3 -m venv .venv
.venv/bin/pip install -e .
```

### Step 2 — Restore the knowledge base

The tracked `data/index.tar.gz` holds the FAISS index plus aligned JSONL
stores. Restore it (SHA-256 verified) into the git-ignored `index/` directory:

```bash
bash scripts/restore_index.sh
```

Expected output (real capture):

```text
[*] Verifying checksum...
[*] Checking archive paths...
[✓] Index restored to …/index
```

### Step 3 — Confirm the console script

```bash
.venv/bin/rift --version
```

Expected: `rift 2.0.0`

### Step 4 — Ask your first questions

Start an MCP stdio session from your client, or probe the server directly.
Against the restored index, `index_stats()` returns (real capture):

```json
{
  "index_dir": "…/RIFT/index",
  "model": "sentence-transformers/all-MiniLM-L6-v2",
  "vectors": 23737,
  "dimensions": 384,
  "index_type": "IndexFlatIP",
  "metadata_entries": 23737,
  "documents": 23737
}
```

`search_offensive_scenarios(query="kerberoasting detection", top_k=2,
threshold=0.6)` returns the top match `cybersec-14323::q1172` with relevance
`0.7102` (real capture, trimmed):

```json
"results": [
  {
    "doc_id": "cybersec-14323::q1172",
    "score": 0.7102,
    "question": "What techniques would you implement to detect Kerberoasting …"
  }
]
```

`ask_offensive_scenario(question="how do I detect Pass-the-Hash attacks?",
top_k=1)` at the default threshold returns a readable entry (relevance
`0.495`, real capture, trimmed):

```text
--- 1 (relevance 0.495) ---
ID: cybersec-51393::q2128
Q: What methodologies would you use to detect pass-the-hash attacks using native Windows tools?
A: Pass-the-Hash (PtH) attacks exploit NTLM authentication by leveraging captured password hashes …
```

And a negative example — with `threshold=0.6` the same question returns no
entries, which is the threshold doing its job:

```text
No relevant entries found in the offensive-scenario knowledge base. Try rephrasing, lowering `threshold` (e.g. 0.15), or broadening the query.
```

Full captures live in [demo/](demo/DEMO.md); more invocations are in
[USAGE_EXAMPLES.md](USAGE_EXAMPLES.md).

### Step 5 — Connect your AI client

Add RIFT to your client configuration; see
[MCP_INTEGRATION.md](MCP_INTEGRATION.md). For OpenCode:

```jsonc
{
  "mcp": {
    "rift": {
      "type": "local",
      "command": ["/absolute/path/to/RIFT/.venv/bin/python", "-m", "rift_mcp"],
      "environment": { "RIFT_INDEX_DIR": "/absolute/path/to/RIFT/index" }
    }
  }
}
```

Then ask, for example: *"Use RIFT to find detection guidance for Kerberoasting
and cite the doc_ids."*

---

## What RIFT is not

- Not an autonomous exploitation engine — it has no shell, filesystem, or
  network tools, and it cannot attack anything.
- Not a chatbot that invents answers — output is verbatim retrieval from the
  indexed knowledge base.
- Not a replacement for authorization, review, or expertise.

## Next steps

- [INSTALLATION.md](INSTALLATION.md) — detailed install reference
- [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) — verified invocations
- [HOW_IT_WORKS.md](HOW_IT_WORKS.md) — embeddings, FAISS, and validation
- [MCP_INTEGRATION.md](MCP_INTEGRATION.md) — client setup and tool contracts

---

RIFT · Red-team Intelligence & Fusion Toolkit ·
[Documentation index](README.md) · [GitHub](https://github.com/Sabriigsxr/RIFT) ·
[Ethical use](ETHICAL_USE.md) · [Security](SECURITY.md)
