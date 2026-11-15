# Usage examples — verified invocations

Every output block on this page is a **real capture** from a clean local clone
of this repository with the bundled index restored (October-capture, RIFT
2.0.0). Long answers are trimmed with `…`; trimming is marked in place.
No output here is hand-written or simulated.

## 1. Restore and verify

```bash
bash scripts/restore_index.sh
```

```text
[*] Verifying checksum...
[*] Checking archive paths...
[✓] Index restored to …/RIFT/index
```

```bash
.venv/bin/rift --version
```

```text
rift 2.0.0
```

## 2. Tool inventory

```text
TOOLS: ["search_offensive_scenarios", "ask_offensive_scenario", "index_stats"]
PROMPTS: ["offensive_scenario_brief"]
```

## 3. `index_stats`

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

## 4. `search_offensive_scenarios` — kerberoasting

Call:

```json
{ "query": "kerberoasting detection", "top_k": 2, "threshold": 0.6 }
```

Result (first two hits shown; answers trimmed):

```json
{
  "query": "kerberoasting detection",
  "count": 2,
  "results": [
    {
      "doc_id": "cybersec-14323::q1172",
      "score": 0.7102,
      "category": "",
      "difficulty": "",
      "tags": [],
      "cve_references": [],
      "tools_used": [],
      "question": "What techniques would you implement to detect Kerberoasting that occurs through compromised administrative accounts?",
      "answer": "Detecting Kerberoasting attacks targeting compromised administrative accounts requires a multi-layered approach combining behavioral analysis, anomaly detection, and log correlation. According to NIST SP 800-94 … (full text omitted)"
    },
    {
      "doc_id": "cybersec-53707::q7339",
      "score": 0.6771,
      "question": "What strategies would you implement to detect Kerberos sidecar attacks?"
    }
  ]
}
```

## 5. `ask_offensive_scenario` — pass-the-hash

Call:

```json
{ "question": "how do I detect Pass-the-Hash attacks?", "top_k": 1 }
```

Result (default threshold, answer trimmed):

```text
Top 1 result(s) from the offensive-scenario knowledge base:

--- 1 (relevance 0.495) ---
ID: cybersec-51393::q2128
Q: What methodologies would you use to detect pass-the-hash attacks using native Windows tools?
A: Pass-the-Hash (PtH) attacks exploit NTLM authentication by leveraging captured password hashes without requiring plaintext passwords. Detection requires monitoring anomalous authentication patterns and credential usage behaviors through native Windows instrumentation.

**Event Log Analysis:**
Windows Security Event Logs provide primary detection vectors. Monitor Event ID 4624 (logon events) for Type 9 (NewCredentials) logons …
```

## 6. Threshold behavior — the honest negative case

Same question with `threshold=0.6`:

```text
No relevant entries found in the offensive-scenario knowledge base. Try rephrasing, lowering `threshold` (e.g. 0.15), or broadening the query.
```

This is expected: 0.495 < 0.6. Lower the threshold to recover the 0.495 hit, or
rephrase. Threshold tuning is your main dial.

## 7. Typical MCP client session (workflow)

```text
You: "Use RIFT to find detection guidance for Kerberoasting and cite doc_ids."
Client → RIFT: search_offensive_scenarios({"query": "kerberoasting detection"})
Client reads results (e.g. cybersec-14323::q1172)
You: "Summarize detection Event IDs from the retrieved entries, citing IDs."
```

RIFT stays extractive — it returns the stored Q&A; the client model does the
summarizing, and should cite `doc_id` values in its answer.

## 8. HTTP smoke check (loopback only)

```bash
.venv/bin/rift --transport http --host 127.0.0.1 --port 8799
```

```text
[rift] HTTP transport listening on http://127.0.0.1:8799/mcp
INFO:     Started server process […]
```

A valid MCP `initialize` JSON-RPC POST to `http://127.0.0.1:8799/mcp` returned
**HTTP 200** in the same capture. The endpoint has no built-in authentication;
keep it on loopback or behind an access-controlled boundary with TLS.

---

RIFT · Red-team Intelligence & Fusion Toolkit ·
[Documentation index](README.md) · [GitHub](https://github.com/Sabriigsxr/RIFT) ·
[Ethical use](ETHICAL_USE.md) · [Security](SECURITY.md)
