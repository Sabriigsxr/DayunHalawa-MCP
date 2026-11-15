# RIFT — Color palette

All colors are used as defined below. Do not introduce new accent colors without
an update to this file and `rift-brand-guidelines.md`.

## Core colors

| Token | Hex | Usage |
|---|---|---|
| `--rift-black` | `#090A0D` | Primary background (dark mode first) |
| `--rift-surface` | `#14151C` | Panels, elevated cards, dividers on black |
| `--rift-surface-2` | `#1C1E27` | Highest elevation, hover states |
| `--rift-crimson` | `#D7193F` | Primary accent: mark, links, key highlights |
| `--rift-crimson-bright` | `#F04A68` | Crimson on dark backgrounds (better contrast) |
| `--rift-crimson-deep` | `#8F0F29` | Crimson on light backgrounds |
| `--rift-text` | `#F2F3F5` | Primary text on dark |
| `--rift-text-muted` | `#9CA0AA` | Secondary text, descriptors |
| `--rift-text-dim` | `#6E727C` | Tertiary text, captions |
| `--rift-grid` | `#17181F` | Technical grid lines on `#090A0D` |
| `--rift-divider` | `#2B2C35` | Dividers, rules, separators |

## Semantic usage

- **Crimson** is reserved for the mark, active/important states, and a single
  key accent per view. Never use it as body-text color.
- **Near-white** `#F2F3F5` is body text on dark; never pure `#FFFFFF` at large
  sizes (reduces glare on OLED displays).
- **Muted gray** `#9CA0AA` for captions, descriptors, and metadata.
- **Success / warning** semantics are intentionally **not** part of the brand
  palette; UIs should reuse crimson for emphasis and grays for neutrals.

## Backgrounds

- Dark (default): `#090A0D` with 1 px `#17181F` grid lines spaced at 64 px —
  see `rift-social-preview.svg` for the canonical pattern.
- Light: `#F2F3F5` background, `#14151C` text, `#8F0F29` accent
  (`rift-crimson-deep`). Do not use `#D7193F` for body text on white.

## Contrast notes

- `#D7193F` on `#090A0D` — large graphics and large type only (below WCAG AA
  for small text). Use `#F04A68` for small accent text on dark.
- `#F04A68` on `#090A0D` — AA-compliant for small text accent
  (luminance ratio ≈ 5.1:1).
- `#F2F3F5` on `#090A0D` — AAA for body text.
- `#9CA0AA` on `#090A0D` — AA for small text.
