# MCP integration

RIFT provides three registered tools:

- `search_offensive_scenarios(query, top_k=5, threshold=0.25)`
- `ask_offensive_scenario(question, top_k=5, threshold=0.25)`
- `index_stats()`

The registered prompt is `offensive_scenario_brief(topic)`. RIFT registers no
MCP resources.

## Claude Desktop

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

## OpenCode

```jsonc
{
  "mcp": {
    "rift": {
      "type": "local",
      "enabled": true,
      "command": ["/absolute/path/to/RIFT/.venv/bin/python", "-m", "rift_mcp"],
      "environment": {
        "RIFT_INDEX_DIR": "/absolute/path/to/RIFT/index"
      }
    }
  }
}
```

RIFT also supports streamable HTTP at
`http://127.0.0.1:8787/mcp`. No other client is claimed here without a
verified repository integration.
