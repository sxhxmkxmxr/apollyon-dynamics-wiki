# Apollyon Dynamics — Neo-Prime Wiki

A static HTML reference for investors, evaluators and due-diligence readers.
Open `index.html` in a browser, or serve the directory:

```sh
python3 -m http.server 8901     # from inside wiki/
```

## Structure

```
index.html                    The argument, summarised with links out: origin →
                              doctrine → the world → dependency history → the
                              window → strike per rupee → architecture → the
                              arsenal → the business → compounding moats →
                              track record → engage
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
css/wiki.css                  Single shared stylesheet
js/wiki.js                    Shell behaviour: mobile menu drawer, "On this page"
                              scroll-spy, reading progress, full-screen figures
js/dependency_corpus_data.js  Corpus behind the full record
assets/                       Photography, logos and assets/visuals.json (the
                              generated charts, inlined into pages)
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
| Piranha | Design targets given as ranges; sea trials from the end of 2026 |
| Flight-control baseline | Veronte Autopilot 1x (Embention) now; in-house replacement developed in parallel once production is steady |
| Funding | Equity-funded (₹4 Cr pre-seed, Naandi Ventures) plus tactical revenue |

There is no Nightshade Mk III. Prices are selling prices; the wiki does not
discuss margins.

## Tone

Doctrine pages are philosophical and may argue. Product, subsystem, strategy
and company pages are technical: state what the system does, mark estimates and
claims, give ranges where the figure is not yet measured, and leave out
superlatives ("dominates", "first", "zero", "unmatched").

## Design system

Black ground (`#060606`), bone ink, one signal red (`#D92323` fills /
`#F04B4B` small text). Hairline rules only; no gradients, shadows or rounded
cards. Inter for text, JetBrains Mono for labels and figures, Newsreader for
pull-quotes. Figures, tables and plates span the full column; running prose is
held to a ~70-character measure inside it. Visuals are embedded inline so the
page fonts and alignment hold, and every plate can be expanded full-screen.
Three-column shell: wiki navigation left, the page, "On this page" right (the
right column folds into the left nav below 1320px; below 1020px the nav becomes
a drawer behind the Menu button). Keep mono labels at 10px or larger.

**Do not regress** the war timeline with its hanging case files (`.war-*` in
`css/wiki.css`, JS at the bottom of `index.html`).

## Build tools (`scripts/`)

| Script | Purpose |
|---|---|
| `site_shell.py` | Canonical rail, left navigation, right-hand "On this page", prev/next pager and footer on every page. `SIDEBAR_GROUPS` is the reading order the pager follows. Run after adding a page or nav entry. |
| `gen_visuals.py` | Regenerates every chart and diagram into `assets/visuals.json`. Chart data (prices, ranges, product names) lives here; change it here first. |
| `inline_visuals.py` | Refreshes inlined SVGs in pages: fills `<!-- VISUAL:name -->` placeholders and re-replaces embedded SVGs by aria-label. |
| `gen_full_record.py` | Regenerates `strategic-dependency/full-record.html` from `js/dependency_corpus_data.js`. |
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

**Pages to deepen**

- Team (short today), launch and ground systems, airframe and structures.
- Hemlock: the representative image is an SVG / HTML render; add real
  engineering imagery as it exists.

**Housekeeping**

- `audit/wiki-review.md` (17 September 2026) predates the current page set and
  is out of date.
