# MCP client setup — verified configurations

## Claude Desktop

`claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "rift": {
      "command": "/absolute/path/to/RIFT/.venv/bin/python",
      "args": ["-m", "rift_mcp"],
      "env": {
        "RIFT_INDEX_DIR": "/absolute/path/to/RIFT/index",
        "HF_HUB_OFFLINE": "1",
        "TRANSFORMERS_OFFLINE": "1"
      }
    }
  }
}
```

Restart Claude Desktop; the tools `search_offensive_scenarios`,
`ask_offensive_scenario`, and `index_stats` appear under the `rift` server,
along with the `offensive_scenario_brief` prompt.

## OpenCode

`opencode.jsonc` (copy from [`../../examples/opencode.jsonc`](../../examples/opencode.jsonc)):

```jsonc
{
  "mcp": {
    "rift": {
      "type": "local",
      "enabled": true,
      "command": ["/absolute/path/to/RIFT/.venv/bin/python", "-m", "rift_mcp"],
      "environment": {
        "RIFT_INDEX_DIR": "/absolute/path/to/RIFT/index",
        "HF_HUB_OFFLINE": "1",
        "TRANSFORMERS_OFFLINE": "1"
      }
    }
  }
}
```

Verify the server lists its tools after launch:

```bash
.venv/bin/rift --version     # rift 2.0.0
```

Sanity checks from a terminal (real session was captured in
[SEARCH_EXAMPLE.md](SEARCH_EXAMPLE.md)):

1. Ask *"Use RIFT to list your tools."* → expect the three tool names.
2. Ask *"Call index_stats."* → expect 23,737 vectors, 384 dimensions.
3. Ask *"Find Kerberoasting detection guidance."* → expect results with
   doc_ids such as `cybersec-14323::q1172`.

## What the client sees

- stdio: client spawns `python -m rift_mcp`; no socket, no auth needed.
- HTTP (optional): client connects to `http://127.0.0.1:8787/mcp`. The
  endpoint is **unauthenticated** — loopback only.

## Troubleshooting the connection

- Wrong path → client shows the server as failed; use absolute paths.
- First run needs the model; if the cache is empty and offline mode is on,
  startup fails. Load the model once without offline mode, then re-enable it.
- `RIFT_INDEX_DIR` must contain all three files; check with
  [../TROUBLESHOOTING.md](../TROUBLESHOOTING.md).

---

RIFT · Red-team Intelligence & Fusion Toolkit ·
[Demo index](DEMO.md) · [Documentation index](../README.md)
