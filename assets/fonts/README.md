# Fonts

| File | Family | Role | Source and licence |
|---|---|---|---|
| `endless-regular.woff2` | Endless | Body text | Endless by Sreejith Shashi, released April 2026 as a free font "for personal and commercial work" (Behance). One weight, basic Latin only (94 glyphs): characters it lacks, such as ₹ · × – → and curly quotes, fall back to the next font in the stack, one character at a time. Bold is synthesized by the browser. |
| `uav-osd-sans-mono.woff2` | UAV OSD Sans Mono | Display: the homepage title, large figures, status badges | Designed by Nicholas Kruse (nicholaskruse.com). Same file the company website already serves. About 100 glyphs; lowercase is drawn at cap height. |

Converted from the TTF originals with fontTools (WOFF2 flavour); the outlines are unchanged.

Not embedded:

- **Helvetica Neue** (headings). A Linotype commercial font, licensed per computer. The CSS asks for the reader's installed copy (macOS and iOS have it) and falls back to Helvetica, then Arial. Embed it only if the company buys a web licence.
- **JetBrains Mono** (code, tables, chart labels). Loaded from Google Fonts under the SIL Open Font License. The generated charts in `assets/visuals.json` name it directly.

Before adding a font here, confirm its licence allows web embedding and record it in this table.
