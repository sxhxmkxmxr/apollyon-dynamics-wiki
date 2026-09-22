# Apollyon Dynamics — Neo-Prime Wiki

A static HTML reference for investors, evaluators and due-diligence readers.
Open `index.html` in a browser, or serve the directory:

```sh
python3 -m http.server 8901     # from inside wiki/
```

## Structure

```
index.html                    The narrative: origin → doctrine → the world →
                              dependency history → the window → the plan →
                              architecture → products → business → moats →
                              record → engage
architecture/index.html       The shared core: hardware, software, the flight
                              loop, control at the envelope, latency, GNSS-denied
                              navigation, and what is shared across the portfolio
strategy/trajectory.html      Capability per rupee: strike envelope, cost per kg·km,
                              generation economics, salvo arithmetic, open risks
strategy/competitive.html     The comparison field: cUAS matrices, strike matrices,
                              capital efficiency, the three reads
strategy/supply-chain.html    Component posture, partners, and the open gaps
products/                     nightshade-adx1 (family MKI–MKIII + target drone),
                              hemlock (Hemlock cruise missile), ahuti (interceptor),
                              usv-strike (Piranha)
subsystems/                   One page per shared technology; the authority for it
doctrine/                     The New Arsenal · Precision is Mercy · The missing middle
about/history.html            Founding, chronology, deployments, market, testimonials
strategic-dependency/         The full record — 70 denials, one by one
css/wiki.css                  Single shared stylesheet (design system v3)
assets/                       Generated SVG plates, photography, data files
scripts/                      Build and verification tools (see below)
```

## Design system

Black ground (`#060606`), bone ink, one signal red (`#D92323` fills /
`#F04B4B` small text). Hairline rules only; no gradients, shadows or rounded
cards. Inter for text, JetBrains Mono for labels and figures, Newsreader for
pull-quotes. Every block spans the same reading column; visuals are embedded
inline so the page fonts and alignment hold.

**Never regress these two hand-built components:** the war timeline with its
hanging case files (`.war-*` in `css/wiki.css`, JS at the bottom of
`index.html`) and the synthesis architecture grid (`.synthesis-*`).

## Build tools (`scripts/`)

| Script | Purpose |
|---|---|
| `site_shell.py` | Canonical rail / sidebar / footer on every page. Run after adding a page or nav entry. |
| `gen_visuals.py` | Regenerates every chart and diagram in `assets/*.svg` + `assets/visuals.json`. |
| `inline_visuals.py` | Refreshes inlined SVGs in pages: fills `<!-- VISUAL:name -->` placeholders and re-replaces embedded SVGs by aria-label. |
| `gen_full_record.py` | Regenerates `strategic-dependency/full-record.html` from the corpus JSON. |
| `verify_links.py` | Checks every link and anchor across all pages. Must report 0 errors. |
| `legacy/` | Superseded scripts from earlier themes. Do **not** run — they overwrite live pages and the stylesheet with obsolete content. |

Build order after editing content or generator:

```sh
python3 scripts/gen_visuals.py
python3 scripts/inline_visuals.py
python3 scripts/site_shell.py
python3 scripts/verify_links.py
```
