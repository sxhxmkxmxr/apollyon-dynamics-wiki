# Apollyon Dynamics — Neo-Prime Wiki

A static HTML reference for investors, evaluators and due-diligence readers.
Open `index.html` in a browser, or serve the directory:

```sh
python3 -m http.server 8901     # from inside wiki/
```

## Structure

```
index.html                    Summary first, then the argument: at a glance →
                              three principles → products and maturity → the
                              world → dependency history → the market (the main
                              graph) → strike per rupee → architecture → the
                              business → compounding moats → origin → track
                              record → explore the wiki (directory, status key)
                              → working with us
architecture/index.html       The shared engineering method: vehicle architecture,
                              the machine / twin / loop, the subsystem register,
                              and what is shared across the portfolio
strategy/trajectory.html      Strike per rupee: strike envelope, cost per kg·km,
                              generation economics, salvo arithmetic, roadmap,
                              open risks
strategy/market.html          Addressable market, Budget 2026 / Vision 2047,
                              demand pillars, export provenance, channels
strategy/competitive.html     The comparison field: cUAS matrices, the Nightshade
                              field by configuration (target drones, loitering
                              munition in two price bands, jet-effector reference
                              class), capital efficiency
strategy/supply-chain.html    Component posture, partners, and the open gaps
products/nightshade-adx1      Nightshade family: one airframe in three
                              configurations — Economical target drone, Premium
                              target drone (ADX-1 Premium), Mk II loitering munition
products/hemlock              Hemlock long-range cruise missile (concept)
products/ahuti                Ahuti high-speed interceptor
products/usv-strike           Piranha unmanned surface vessel (in build)
subsystems/                   One page per shared technology; the authority for it
doctrine/                     The New Arsenal · Precision is Mercy · The Missing
                              Middle · strike design space
about/history.html            Founding, track record (done / next), deployments,
                              testimonials
about/team.html               Founders, team and advisors
strategic-dependency/         The full record — 70 denials, one by one
css/wiki.css                  Single shared stylesheet (contents list at the top)
js/wiki.js                    Shell behaviour: wiki-map drawer, "On this page"
                              scroll-spy, full-screen figures
js/dependency_corpus_data.js  Corpus behind the full record
assets/                       Photography, logos and assets/visuals.json (the
                              generated charts, inlined into pages)
assets/fonts/                 Self-hosted fonts and their licence notes
assets/schematics/            Copies of the Hemlock and Piranha CAD drawings used on
                              the homepage cards; edit together with the pages
scripts/                      Build and verification tools (see below)
drafts/                       Internal working notes; not linked from the wiki
```

Source documents (product PDFs, notes) live in `docs/`, which is not tracked.
`docs/NIGHTSHADE_ADX1_V6.pdf` is the reference for every Nightshade figure;
the wiki should not claim more than it does.

## Facts to keep consistent

These appear on several pages. Change them everywhere or nowhere.

| Fact | Value |
|---|---|
| Team | 17+ engineers and operators |
| Field footprint | 8 fielded formations, four theatres; one mobile drone lab (15 Guards, Jammu) |
| Nightshade Mk II loitering munition | ₹1.5 Cr (~$150,000) · 15 kg · 300 km · 550 / 650 km/h · prototype Q1 2027 |
| Nightshade target drones | Economical $90,000 · Premium ~$150,000 · prototypes Q4 2026 |
| Nightshade indigenous content | ~45–50% |
| Hemlock | 450–500 kg warhead · 1,000–1,500 km · ₹3–5 Cr · concept |
| Piranha | Small USV (~4 m class), 65 km/h top speed, marine radar + EO/IR on every hull, 50 kg+ warhead on the strike configuration, recon and one-way strike from one hull, ~₹1.5–2.5 Cr estimated unit cost; sea trials from the end of 2026 |
| Flight-control baseline | Veronte Autopilot 1x (Embention) now; in-house replacement developed in parallel once production is steady |
| Funding | Equity-funded (₹4 Cr pre-seed, Naandi Ventures) plus tactical revenue |

There is no Nightshade Mk III. Prices are selling prices; the wiki does not
discuss margins.

## Tone

Doctrine pages are philosophical and may argue. Product, subsystem, strategy
and company pages are technical: state what the system does, mark estimates and
claims, give ranges where the figure is not yet measured, and leave out
superlatives ("dominates", "first", "zero", "unmatched").

## Navigation: one job per element

| Element | Job | Built by |
|---|---|---|
| Top bar | Where you are: brand and breadcrumb (group / page). No section links. | `site_shell.py` |
| Wiki map (left) | Everything that exists, grouped; current page marked; status badges | `site_shell.py` from `SIDEBAR_GROUPS` |
| On this page (right; a collapsed box under the title below 1280px) | This page's sections | the page's own `<nav class="toc">` list |
| Pager | Previous and next in reading order | `SIDEBAR_GROUPS` order |

Every item in the wiki map is a page; every item under "On this page" is an
anchor on the current page. Links to other pages end in →. A breadcrumb's group
links to the group's landing page where one exists (`GROUP_LANDING`), otherwise
to its entry in the homepage directory ("Explore the wiki").

## Status: maturity, evidence, images

Status is always a word plus a shape, never colour alone.

- **Product maturity** (`MATURITY` in `site_shell.py`; shown in the wiki map,
  the homepage cards and the directory): *Fielded* (in service with a user,
  filled square), *Flight testing* (built and flying, half-filled), *In
  development* (design and build under way, outline), *Concept* (studies and
  schematics, dashed). Take the level from the product page's own status line
  and ask the product owner before changing one.
- **Page status** (`PAGE_STATUS`): *In progress* puts a badge in the map and
  directory and a notice under the page title. Say what is there; never invent
  the missing content.
- **Evidence markers** on figures (`.prov`): `obs` observed (measured in a test
  or record), `est` estimate, `target` design target, `claim` a third party's
  figure. Specifications of products not yet built are headed "Design targets".
- **Images** say what they are: Render (computer-generated), Photo, Schematic.

## Design system

`css/wiki.css` opens with its contents and house rules; every value is a token.

- **Colour.** Black ground `#060606`; text steps `#f2efe9` (headings),
  `#d4d0c8` (body), `#a8a49c` (secondary), `#938f88` (muted), all at least
  4.5:1 on every surface; hairline rules; one signal red `#d92323` for fills,
  rules and markers. **No red text on the dark ground**: text on a red fill is
  white. The old names (`--ink`, `--line`, `--red`...) remain as aliases.
- **Type.** Body: Endless, 17px / 1.65 (one weight, basic Latin; other symbols
  fall back per character). Headings: the reader's Helvetica Neue (Arial on
  Windows), sentence case. Display: UAV OSD Sans Mono, for the homepage title,
  key figures, section numbers and the brand. Code, tables and chart labels:
  JetBrains Mono. No user-facing text below 12px. Licences:
  `assets/fonts/README.md`.
- **No small label above a heading.** Section numbers sit inside the heading;
  supporting lines (page meta, kickers) go below.
- **Motion.** Transitions only; nothing animates on its own. Reduced motion is
  respected.
- **Figures.** Numbered plates with a head (number, title, Expand), a caption,
  a source line where one exists, and a data table for key charts. Charts are
  generated; keep their text in ink and put the red on marks.
- **Print.** Dark ink on white, navigation hidden, charts inverted for paper.
- **Layout.** Wiki map 256px, content up to 880px (prose about 68 characters),
  "On this page" 208px. Breakpoints: 1280 (three columns), 1020 (the map becomes
  a drawer), 720 (compact charts), 640 (phone).

**Do not regress** the war timeline with its hanging case files (`.war-*` in
`css/wiki.css`, JS at the bottom of `index.html`): the case files are the
keyboard controls (`aria-pressed`), the rail dots repeat them for pointer users,
and the plain `.war-static` list serves print and readers without JavaScript.

The homepage's main graph is Fig. 02, annual defence production. Its data
lives in `INDIA_PRODUCTION` in `scripts/gen_visuals.py` and is mirrored in the
data table under the chart: change both together.

## Build tools (`scripts/`)

| Script | Purpose |
|---|---|
| `site_shell.py` | The shared shell of every page: head, top bar and breadcrumb, wiki map, "On this page" (right column and collapsed box), status notice, pager, footer, and the homepage directory. Data at the top: `SIDEBAR_GROUPS` (map and reading order), `GROUP_LANDING`, `MATURITY`, `PAGE_STATUS`, `DESCRIPTIONS`. Generated blocks sit between `<!-- shell:NAME -->` comments and are replaced on each run; a second run must change nothing. It refuses to write a page that ends up malformed. `--check` exits 1 when pages would change. Run after adding a page or nav entry. |
| `gen_visuals.py` | Regenerates every chart and diagram into `assets/visuals.json`. Chart data (prices, ranges, product names) lives here; change it here first. Refuses to write if a visual is unclosed or an aria-label repeats. |
| `inline_visuals.py` | Refreshes inlined SVGs in pages: fills `<!-- VISUAL:name -->` placeholders and re-replaces embedded SVGs by aria-label. The wrapper must be exactly `<div class="blueprint-body">` with nothing after the `</svg>` inside it; a renamed aria-label detaches the embed. Refuses to write a page with unbalanced `<svg>`. |
| `gen_full_record.py` | Regenerates `strategic-dependency/full-record.html` from `js/dependency_corpus_data.js`. **Stale: do not run.** The live page has edits the generator does not know about. |
| `verify_links.py` | Checks every link and anchor across all pages. Must report 0 errors. |
| `generate_architecture_graph.py` | Draws an overview graph of the wiki as a PNG. Optional; no page uses the output. |

Each topic has one owning page; other pages summarise it in a paragraph and
link there. Owners: strike economics, salvo model and requirement sheet →
trajectory; market, exports and channels → market; head-to-head comparisons and
the three strike philosophies → competitive; testimonials and full chronology →
history; each subsystem → its subsystem page.

Build order after editing content or generator:

```sh
python3 scripts/gen_visuals.py
python3 scripts/inline_visuals.py
python3 scripts/site_shell.py
python3 scripts/verify_links.py
```

## Pending

Work that is known and not yet done.

**Redundant for now.** The landing page's "Compounding Moats" section repeats
material owned elsewhere: loop 04 (distribution: export footprint and demand
channels) and loop 05 (sovereignty table) overlap `strategy/market.html` and
`strategy/supply-chain.html`; loop 06 (position map) and loop 07 (proof in
products) overlap `strategy/competitive.html`. Doctrine §02 on the landing page
repeats `doctrine/precision-is-mercy.html`. They stay in place for the reading
order; once the owning pages carry more detailed information, cut the landing
page versions to a short summary and a link.

**Pages to write**

- **Propulsion subsystem** (`subsystems/propulsion.html`). Engines by platform
  (40 kgf-class micro-turbine on Nightshade, GTRE Manik 450 kgf turbofan on
  Hemlock, electric drive on Ahuti, marine diesel and waterjets on Piranha),
  suppliers and second sources, thrust and fuel figures, test results, and
  the plan for domestic sourcing.
- **Evidence and test record.** Test campaigns by product, what was measured,
  what failed and what changed; flight logs summarised; certificates (India
  Book of Records, trial reports, user letters).
- **Investor pages.** Use of funds, milestones against capital, order book
  and pipeline, and unit economics at the level of price and volume.
- **Risk register.** One page that gathers the risks now spread across
  trajectory ("what has to be true"), competitive ("what we must fix") and
  supply chain ("exposures"), each with an owner and a mitigation.
- **Sources.** Citations for market sizes, export figures, partner claims
  (Tonbo markets and contracts, "80+ nations") and competitor data, with the
  estimate / claim / observed markers used on the competitive page.
- **Glossary.** SEAD, CRPA, CEP, LOS / BVLOS, DFPDS, IDDM, DAP, Make-I / II and
  the other acronyms used across the wiki.

**Design system, next pages.** The homepage and the shared shell follow the
design system above; the other pages keep their older markup:

- `.sec-tag` labels still sit above section headings on 23 pages (now muted,
  not red). Move the numbers into the headings, as on the homepage.
- Product pages: show the maturity badge under the title, label renders as
  renders in the visible caption, head unbuilt specs "Design targets".
- The full record's timeline graphic still uses 8.5-9.5px labels.
- Page titles say "Neo-Prime Wiki"; the shell says "Engineering Wiki". Pick one.

**Pages to deepen**

- Team (short today), launch and ground systems, airframe and structures
  (marked In progress; content awaited).
- Hemlock: the representative image is an SVG / HTML render; add real
  engineering imagery as it exists.

**Housekeeping**

- `audit/wiki-review.md` (17 September 2026) predates the current page set and
  is out of date.
