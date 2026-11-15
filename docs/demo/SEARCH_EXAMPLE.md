# Search example — captured session

The following transcripts were produced by a real stdio MCP client against a
clean clone running RIFT 2.0.0 with the restored bundled index and offline
model cache. Paths are elided with `…`; nothing else is edited.

## Tool inventory

```text
TOOLS: ["search_offensive_scenarios", "ask_offensive_scenario", "index_stats"]
PROMPTS: ["offensive_scenario_brief"]
```

## `index_stats`

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

## `search_offensive_scenarios` — "kerberoasting detection" (top_k=2, threshold=0.6)

```text
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
      "answer": "Detecting Kerberoasting attacks targeting compromised administrative accounts requires a multi-layered approach combining behavioral analysis, anomaly detection, and log correlation. According to NIST SP 800-94, organizations should implement comprehensive monitoring of Kerberos authentication events.\n\n**Primary Detection Techniques:**\n\n1. **Kerberos Ticket Request Anomaly Detection**: Monitor for unusual AS-REQ (Authentication Service Request) patterns targeting service accounts with high-value SPNs. Legitimate administrative access typically follows predictable patterns, while Kerberoasting generates systematic requests for multiple service tickets within compressed timeframes.\n\n2. **MITRE ATT&CK T1558.003 Mapping**: Implement detection rules identifying T1558.003 (Kerberoasting) by analyzing Event ID 4769 (Kerberos Service Ticket Operations). …"
    },
    {
      "doc_id": "cybersec-53707::q7339",
      "score": 0.6771,
      "question": "What strategies would you implement to detect Kerberos sidecar attacks?",
      "answer": "Kerberos sidecar attacks exploit legitimate authentication flows by leveraging valid tickets to access resources without proper authorization verification. …"
    }
  ]
}
```

## `ask_offensive_scenario` — "how do I detect Pass-the-Hash attacks?" (top_k=1, default threshold)

```text
Top 1 result(s) from the offensive-scenario knowledge base:

--- 1 (relevance 0.495) ---
ID: cybersec-51393::q2128
Q: What methodologies would you use to detect pass-the-hash attacks using native Windows tools?
A: Pass-the-Hash (PtH) attacks exploit NTLM authentication by leveraging captured password hashes without requiring plaintext passwords. Detection requires monitoring anomalous authentication patterns and credential usage behaviors through native Windows instrumentation.

**Event Log Analysis:**
Windows Security Event Logs provide primary detection vectors. Monitor Event ID 4624 (logon events) for Type 9 (NewCredentials) logons, particularly focusing on unusual service account behavior or lateral movement patterns. Event ID 4648 captures explicit credential usage, indicating potential PtH activity when credentials are used across different systems than expected. …
```

## Same question at `threshold=0.6` — honest negative result

```text
No relevant entries found in the offensive-scenario knowledge base. Try rephrasing, lowering `threshold` (e.g. 0.15), or broadening the query.
```

## Verification facts from this capture

- Index and documents are aligned 1:1 and verified at load (23,737 = 23,737).
- Relevance score 0.7102 — the entry exists **in the bundled knowledge base**;
  RIFT returned it, it did not generate it.
- Everything above ran with `HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1`.

---

RIFT · Red-team Intelligence & Fusion Toolkit ·
[Demo index](DEMO.md) · [Documentation index](../README.md)
