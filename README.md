# Apollyon Dynamics — Engineering Wiki

A static, dependency-free HTML wiki. Open `index.html` in a browser, or serve the
directory (`python3 -m http.server` from inside `wiki/`).

## Structure

```
index.html              Landing page: overview, ethos, product classes,
                        product register, subsystem register, commonality matrix
products/               One page per system. Every page opens with a spec table,
                        then use cases, then product-specific engineering detail,
                        then the subsystems it is assembled from.
subsystems/             One page per shared technology. The subsystem page is the
                        authority; product pages state their configuration and link here.
doctrine/               The New Arsenal (founding manifesto), Precision is Mercy
                        (ethical doctrine), The missing middle (design-space argument)
about/history.html      Founding, track record, deployments, market, testimonials
css/wiki.css            Single shared stylesheet
assets/                 Figures cropped from the source decks
assets/slides/          Capability slides, exported as web figures
```

## Page conventions

- **Product pages** always run: `01 Specification` (an at-a-glance four-column
  spec card) → `02 Use cases` → specifics → `Subsystems used` cross-reference strip.
- **Subsystem pages** always end with a `Used by` strip listing the products that
  carry them, so commonality is navigable in both directions.
- The landing page `#matrix` table is the single place where subsystem × product
  coverage is stated; update it when a product gains or drops a subsystem.

## Design system

Inherited from the Sovereign Strike specification sheets in `../reference/`:
bone paper (`--paper`), ink linework, mono draughtsman's caps for labels, and a
single reserved oxblood accent (`--accent`) used only for the argument — never as
decoration. Fonts are Newsreader (serif headings), Inter (sans body) and
JetBrains Mono (labels and figures), loaded from Google Fonts with local fallbacks.

## Sources

Everything in this wiki traces to `../reference/`:

| Source | Used for |
|---|---|
| `The New Arsenal — A Manifesto for Apollyon Dynamics.txt` | `doctrine/new-arsenal.html`, ethos sections |
| `hacm_350_sovereign_strike_spec.html` | `products/hacm-350.html`, propulsion, anti-jam GNSS |
| `strike_systems_design_space.html` | `doctrine/missing-middle.html` |
| `slides/near-envelope-control.pdf` | `subsystems/near-envelope-control.html` |
| `slides/gnss-denied-navigation.pdf` | `subsystems/gnss-denied-navigation.html` |
| `slides/apollyon-engineering-capability.pdf` | `subsystems/physics-backbone.html`, `onboard-compute.html`, `flight-software.html` |
| `pitches/CFB v10_merged-1.pdf` | Nightshade, Ahuti, Cortex, MDCC, history |
| `pitches/IAF pitch deck.pdf` | Nightshade marks, seekers, mission roles |
| `pitches/ADB pitch deck.pdf` | Market sizing, track record, Nightshade Mk III |

PDFs were rasterised page-by-page and read as images (they are visual documents);
the rendered pages live in `../reference/slides_images/` and `../reference/pitches_images/`.

## Adding a page

Copy the nearest existing page in the same section, keep the rail, sidebar and
footer blocks, and add the new entry to: the landing page register, the landing
page `#matrix` row (if a subsystem), and the sidebar lists of its siblings.
