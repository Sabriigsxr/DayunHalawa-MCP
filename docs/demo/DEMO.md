# RIFT — Demo

This directory documents a **real** RIFT session: captured output from a
clean local clone of the repository, with the bundled index restored and
`HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1` so retrieval provably ran offline.

All transcripts below are copy-pasted from actual runs (RIFT 2.0.0, local
clone on a Linux workstation). No fabricated output appears in this folder.

## Contents

| File | What it contains |
|---|---|
| [SEARCH_EXAMPLE.md](SEARCH_EXAMPLE.md) | Full captured transcript: tool list, `index_stats`, a real semantic search, and threshold behavior |
| [MCP_CLIENT_SETUP.md](MCP_CLIENT_SETUP.md) | Verified client configs and what a working session looks like |
| [EXPECTED_WORKFLOW.md](EXPECTED_WORKFLOW.md) | The canonical end-to-end workflow and a capture checklist for terminal screenshots |

## Reproduce this demo

```bash
git clone https://github.com/Sabriigsxr/RIFT.git
cd RIFT
python3 -m venv .venv
.venv/bin/pip install -e .
bash scripts/restore_index.sh
.venv/bin/rift --version        # rift 2.0.0
```

Then ask the server a question from your MCP client, e.g.
*"Use RIFT to find Kerberoasting detection guidance, cite the doc_ids."*

## About terminal screenshots

No GUI screenshot tool is available in this build environment, and the
project rules forbid fabricated screenshots. Real terminal captures are
therefore **pending**; see the capture checklist in
[EXPECTED_WORKFLOW.md](EXPECTED_WORKFLOW.md#screenshot-capture-checklist).
The `assets/screenshots/` directory contains the checklist instead of images.

---

RIFT · Red-team Intelligence & Fusion Toolkit ·
[Documentation index](../README.md) · [GitHub](https://github.com/Sabriigsxr/RIFT)
