# RIFT — Brand guidelines

**RIFT — Red-team Intelligence & Fusion Toolkit** is a local-first MCP server
for authorized offensive-security research, detection engineering, DFIR, and
education. The identity communicates **intelligence, precision, and technical
reliability** — not shock value.

## Personality

- Calm, precise, technical.
- Engineered, not marketed.
- Authorized and defensive by framing, always.
- Egyptian-built. Proud, understated, specific.

## Voice and tone

- Write for security practitioners: direct, factual, no hype.
- Never claim autonomous exploitation, “guaranteed” hacks, or unverified
  capabilities. Describe what the software actually does.
- Always preserve the authorized-use framing when describing offensive content.
- Prefer lowercase-ish, terse engineering phrasing in docs; full sentences.

## Logo system

Assets in `assets/branding/`:

| File | Use |
|---|---|
| `rift-logo-mark.svg` | App icons, avatars, favicons, tight spaces (≥ 32 px) |
| `rift-logo.svg` | README hero, docs header, dark backgrounds |
| `rift-wordmark.svg` | Light or dark backgrounds (uses `currentColor`) |
| `rift-social-preview.svg` | GitHub social preview / link unfurls (1280×640) |

The mark is an angular **R constructed from mitered crimson strokes** — the
"rift" through the letter. It is intentionally geometric and grid-aligned; do
not redraw it freehand or add gradients, glows, or 3D effects.

## Construction and clear space

- Mark bounding box: 128 units (viewBox `0 0 128 128`).
- Stroke width: 15 units for the mark (scales with the artwork).
- **Clear space:** keep 0.5× mark height of empty space on all sides — no text,
  borders, or imagery inside the clear zone.
- **Minimum size:** the mark stays recognizable at 32 px; the full lockup needs
  ≥ 240 px width to remain legible.

## Background rules

- On dark (`#090A0D` or `#14151C`): crimson `#D7193F` mark, `#F2F3F5` wordmark.
- On light (`#F2F3F5`): deep crimson `#8F0F29` mark, `#14151C` wordmark.
- Never place the crimson mark on a mid-tone or saturated red/orange background.
- `rift-wordmark.svg` uses `currentColor`: set the `color` property and the
  whole lockup adapts.

## Do / Don't

**Do**
- Use the provided SVGs. Keep stroke alignment, miters, and letter-spacing.
- Pair the mark with the descriptor line in documentation headers.
- Attribute the project as **RIFT — Red-team Intelligence & Fusion Toolkit**.
- Keep the Egypt provenance line on first-party surfaces
  (`Made in Egypt · Ahmed Sabry (Sabriigsxr) · Cyber Security Researcher`).

**Don't**
- No skulls, hoodies, masks, circuit-board clichés, rainbow-matrix rain, or
  excessive neon.
- No recoloring outside the palette; no outlining the mark in white on white.
- No tagline edits of the attribution line; no removing it from social assets.
- No stretching, skewing, or rotating the lockup.
- No using the logo to imply endorsement by any third party.

## File naming and reuse

- First-party assets live in `assets/branding/` and are original work of the
  RIFT project. Downstream redistribution must keep the attribution line
  intact; see `WARNING.txt` and repository notices.
- Raster exports, when needed, must be generated from these SVGs — never from
  screenshots of the running app.

## Provenance line (required on social surfaces)

```
MADE IN EGYPT · AHMED SABRY (SABRIIGSXR) · CYBER SECURITY RESEARCHER
```

This line is part of the identity, not an advertisement slot. Keep it on the
social preview, release banners, and project pages.
