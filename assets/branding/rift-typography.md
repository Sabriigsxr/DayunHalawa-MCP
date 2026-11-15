# RIFT — Typography

RIFT uses a two-typeface system. No web font is required for correct
rendering; every face has a system fallback so the brand renders offline and
identically in docs, terminals, and emails.

## Display and body

| Role | Preferred | Fallback stack (use this in assets and CSS) |
|---|---|---|
| Wordmark / Headings | **Inter**, weight 700/800 | `Inter, Arial, Helvetica, sans-serif` |
| Body / UI | **Inter**, weight 400/500 | `Inter, Arial, Helvetica, sans-serif` |

Inter was chosen for its tall x-height (excellent at small sizes), open
counters, and neutral technical tone. The SVGs reference the fallback stack
directly so they render without Inter installed.

### Wordmark rules

- `RIFT` is always **uppercase**, weight **800**, letter-spacing ≈ **0.16–0.22 em**
  (`16–34 px` depending on size).
- The descriptor line
  `RED-TEAM INTELLIGENCE & FUSION TOOLKIT` is uppercase, weight 600,
  letter-spacing ≈ **0.26–0.30 em**, in muted gray `#9CA0AA`.
- Never set the wordmark in bold italics, outline, or gradient.

## Monospace (code, commands, identifiers)

| Role | Preferred | Fallback stack |
|---|---|---|
| Code blocks, CLI, file paths | **JetBrains Mono** | `JetBrains Mono, ui-monospace, SFMono-Regular, Menlo, Consolas, monospace` |

Use monospace for: command examples, tool names, doc IDs, JSON keys, environment
variables (`RIFT_INDEX_DIR`, `HF_HUB_OFFLINE`), and file paths.

## Documentation scale

| Element | Size | Weight | Tracking |
|---|---|---|---|
| Page H1 (README hero) | 40–56 px | 800 | 0.02 em |
| Section H2 | 28–32 px | 700 | 0 |
| Section H3 | 20–22 px | 700 | 0 |
| Body | 15–17 px | 400 | 0 |
| Descriptor / caps line | 14–17 px | 600 | 0.26 em, uppercase |
| Code | 13–15 px | 400 | 0 |

## Don'ts

- No display/decorative faces (Blackletter, stencil, techno/futuristic novelty fonts).
- No synthetic italics for the wordmark.
- No all-caps for body copy — reserved for descriptors and section labels.
