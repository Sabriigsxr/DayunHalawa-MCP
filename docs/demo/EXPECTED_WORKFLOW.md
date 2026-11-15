# Expected workflow

The canonical RIFT workflow from discovery to a cited answer.

```text
1. Install            git clone … && python3 -m venv .venv && .venv/bin/pip install -e .
2. Restore data       bash scripts/restore_index.sh        (SHA-256 verified)
3. Verify             .venv/bin/rift --version             (rift 2.0.0)
4. Connect client     stdio: client spawns `python -m rift_mcp`
5. Ask                "Use RIFT to find detection guidance for Kerberoasting."
6. Inspect            results + doc_ids (e.g. cybersec-14323::q1172)
7. Cite               client answer references retrieved doc_ids
8. Iterate            lower `threshold` or rephrase for broader/narrower results
```

The back-of-the-envelope decision tree:

```text
Need a fact from the bundled Q&A set? ── yes → search_offensive_scenarios / ask_offensive_scenario
                     └── no  → RIFT cannot answer it; use external tooling (in
                              an authorized, reviewed workflow).
```

## Screenshot capture checklist

The environment used to build this demo had no GUI screenshot tool (`scrot`,
`gnome-screenshot`, `grim`, `import -window root` are all unavailable), and
project rules forbid fabricated screenshots. To capture the real thing:

- [ ] **RIFT startup** — run `rift` with the client, capture the client UI
      showing the `rift` server connected and its tool list.
- [ ] **Index statistics** — ask the client to call `index_stats`; capture the
      JSON output (vectors 23,737, dimensions 384).
- [ ] **Semantic search result** — capture a `search_offensive_scenarios`
      result with scores visible.
- [ ] **Readable scenario output** — capture `ask_offensive_scenario` output.
- [ ] **MCP client integration** — capture OpenCode or Claude Desktop settings
      showing the `rift` MCP server entry.
- [ ] **Example workflow** — capture a short conversation showing question →
      tool call → cited doc_ids.

When captured, save PNGs under `assets/screenshots/` with `SCREEN-N-name.png`
and update `assets/screenshots/CAPTURE_CHECKLIST.md` (checked off) and the
README's visuals section. Do not hand-draw terminals.

---

RIFT · Red-team Intelligence & Fusion Toolkit ·
[Demo index](DEMO.md) · [Documentation index](../README.md)
