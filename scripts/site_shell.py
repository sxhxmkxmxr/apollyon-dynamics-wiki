#!/usr/bin/env python3
"""
site_shell.py: the shared shell of every wiki page.

One navigation model, one job per element:
  top bar       brand and breadcrumb (plus a Menu button below 1020px)
  wiki map      left column: every page, grouped, the current page marked,
                status badges on products and on unfinished pages
  on this page  right column: the page's own sections. Below 1280px the same
                list becomes a collapsed box under the page title.
  pager         previous and next in reading order (the order of SIDEBAR_GROUPS)
  footer        identity, revision, status key, contact

Every generated block sits between <!-- shell:NAME --> and <!-- /shell:NAME -->,
so each run replaces exactly what it wrote. The older shell markup (rail,
aside, in-page crumb, bare footer) is migrated on the first run, and a
masthead label sitting above the page title is moved below the standfirst
(house rule: no small label above a heading).

The page owns its <title>, meta description, masthead and its "On this page"
list (the <ul> inside <nav class="toc">). Edit those in the page itself.

Usage:
    python3 scripts/site_shell.py            # apply to every page
    python3 scripts/site_shell.py --check    # list pages that would change; exit 1 if any
"""
import html as html_mod
import os
import re
import sys

WIKI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SITE = "Apollyon Dynamics"
WIKI_NAME = "Engineering Wiki"
REVISION = "Rev 3.0"
COMPANY_SITE = "https://www.apollyondynamics.com"

# Only JetBrains Mono comes from Google (code, tables, chart labels). Body and
# display fonts are self-hosted in assets/fonts; headings use the reader's
# installed Helvetica Neue (see assets/fonts/README.md).
FONTS = "https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700;800&display=swap"
FONT_FILES = ["assets/fonts/endless-regular.woff2", "assets/fonts/uav-osd-sans-mono.woff2"]
FAVICON = "assets/logos/favicon-red.png"

# The wiki map, in reading order. The pager walks this list, so this is the
# order a first-time reader is led through the wiki. URLs never change here;
# only labels and grouping do.
#   (group label, slug, [(page label, path), ...])
SIDEBAR_GROUPS = [
    ("Overview", "overview", [
        ("Home", "index.html"),
    ]),
    ("Products", "products", [
        ("Ahuti interceptor", "products/ahuti.html"),
        ("Nightshade family", "products/nightshade-adx1.html"),
        ("Piranha USV", "products/usv-strike.html"),
        ("Hemlock", "products/hemlock.html"),
    ]),
    ("Architecture", "architecture", [
        ("The shared core", "architecture/index.html"),
        ("Robust flight control", "subsystems/near-envelope-control.html"),
        ("GNSS-denied navigation", "subsystems/gnss-denied-navigation.html"),
        ("Edge compute", "subsystems/onboard-compute.html"),
        ("Flight software", "subsystems/flight-software.html"),
        ("Seekers", "subsystems/seekers.html"),
        ("Airframe &amp; structures", "subsystems/airframe-structures.html"),
        ("Launch &amp; ground systems", "subsystems/launch-systems.html"),
    ]),
    ("Strategy", "strategy", [
        ("Trajectory &amp; cost per kg&middot;km", "strategy/trajectory.html"),
        ("The market", "strategy/market.html"),
        ("The competitive field", "strategy/competitive.html"),
        ("Supply chain", "strategy/supply-chain.html"),
    ]),
    ("Doctrine", "doctrine", [
        ("The New Arsenal", "doctrine/new-arsenal.html"),
        ("Precision is Mercy", "doctrine/precision-is-mercy.html"),
        ("The Missing Middle", "doctrine/missing-middle.html"),
        ("Strike design space", "doctrine/strike-design-space.html"),
    ]),
    ("Context", "context", [
        ("The full record &middot; 70 episodes", "strategic-dependency/full-record.html"),
    ]),
    ("Company", "company", [
        ("Company history", "about/history.html"),
        ("Team &amp; advisors", "about/team.html"),
    ]),
]

# Where a breadcrumb's group links: a landing page where one exists, otherwise
# the group's entry in the homepage directory ("Explore the wiki").
GROUP_LANDING = {
    "products": "index.html#products",
    "architecture": "architecture/index.html",
}

# Maturity of each product page, shown as a word plus a shape (never colour alone).
#   fielded         in service with a user
#   flight-testing  built and flying, not yet delivered
#   in-development  design and build under way; not yet tested as a complete system
#   concept         studies and schematics; no hardware
# Take the wording from the product page's own status line; ask the owner
# before changing one.
MATURITY = {
    "products/ahuti.html": "flight-testing",
    "products/nightshade-adx1.html": "in-development",
    "products/usv-strike.html": "in-development",
    "products/hemlock.html": "concept",
}

# Pages whose content is known to be incomplete. Shown in the wiki map, in the
# homepage directory and as a notice under the page title. Say what is there;
# never invent what is missing.
PAGE_STATUS = {
    "subsystems/airframe-structures.html": (
        "in-progress",
        "This page is being expanded. What is here is current; more detail on "
        "airframe and structures work is being prepared and will be added here.",
    ),
}

STATUS_LABEL = {
    "fielded": "Fielded",
    "flight-testing": "Flight testing",
    "in-development": "In development",
    "concept": "Concept",
    "in-progress": "In progress",
}

# One line per page for the homepage directory, condensed from each page's
# own opening. Keep them factual and short.
DESCRIPTIONS = {
    "products/ahuti.html": "A high-speed electric interceptor for hostile reconnaissance drones and loitering munitions.",
    "products/nightshade-adx1.html": "One turbojet airframe in three configurations: two target drones and the Mk II loitering munition.",
    "products/usv-strike.html": "A small unmanned surface vessel with marine radar and EO/IR, for reconnaissance and one-way strike.",
    "products/hemlock.html": "A high-subsonic cruise missile concept built around the GTRE Manik 450 kgf turbofan.",
    "architecture/index.html": "The permanent engineering method behind every product: hardware, software and the flight loop.",
    "subsystems/near-envelope-control.html": "Flight control for fast aircraft at high dynamic pressure, high-G turns and actuator limits.",
    "subsystems/gnss-denied-navigation.html": "Navigating when satellite signals are jammed or spoofed: anti-jam antennas and scene matching.",
    "subsystems/onboard-compute.html": "Mission and perception compute on a second domain, alongside the flight-critical autopilot.",
    "subsystems/flight-software.html": "The Veronte autopilot baseline, Apollyon-authored control laws and hardware-in-the-loop verification.",
    "subsystems/seekers.html": "Modular seekers for terminal guidance: passive imaging and anti-radiation homing.",
    "subsystems/airframe-structures.html": "How airframes are designed to be built fast: composites, stamped metal and manufacturability.",
    "subsystems/launch-systems.html": "Launchers, canisters and readiness time for the strike and intercept systems.",
    "strategy/trajectory.html": "The long-term strategy: strike envelope, cost per kg&middot;km and salvo arithmetic.",
    "strategy/market.html": "Addressable segments, Budget 2026 and Vision 2047, demand pillars, exports and channels.",
    "strategy/competitive.html": "The products benchmarked against the interceptor and loitering-munition fields.",
    "strategy/supply-chain.html": "Component posture: multi-sourced engines, Tonbo seekers, partners and the open gaps.",
    "doctrine/new-arsenal.html": "The founding doctrine: why a neo-prime can be built from the bottom up in India now.",
    "doctrine/precision-is-mercy.html": "The ethical doctrine: how a state that values restraint should design destructive force.",
    "doctrine/missing-middle.html": "India lacks an industrial tempo, not technology: the unbuilt middle tier of defence manufacturing.",
    "doctrine/strike-design-space.html": "A worked analysis of the standoff strike layer between cruise missiles and loitering munitions.",
    "strategic-dependency/full-record.html": "70 documented wartime denials of equipment to India, 1947 to 2026, in order.",
    "about/history.html": "From a student workshop at BITS Pilani Hyderabad to fielded formations: the company record.",
    "about/team.html": "Founders, engineers and advisors: a team of 17+.",
}

READING_ORDER = [(g, slug, label, href) for g, slug, links in SIDEBAR_GROUPS for label, href in links]
PAGES = {href: (g, slug, label) for g, slug, label, href in READING_ORDER}

SKIP_DIRS = {"scripts", "assets", "css", "js", "drafts", "docs", "audit"}
BLOCKS = ("topbar", "sidebar", "notice", "page-toc", "pager", "toc", "footer")


def esc(s):
    return html_mod.escape(str(s), quote=False)


def prefix(path):
    """Relative prefix from a page back to the wiki root, at any depth."""
    return "../" * path.count("/")


def block(name, body):
    return f"<!-- shell:{name} -->\n{body.rstrip()}\n<!-- /shell:{name} -->\n"


def badge(key):
    return f'<span class="status" data-status="{key}">{STATUS_LABEL[key]}</span>'


def status_of(path):
    """(status key, note) for a page, or (None, None)."""
    if path in MATURITY:
        return MATURITY[path], None
    if path in PAGE_STATUS:
        return PAGE_STATUS[path]
    return None, None


# ── Blocks ────────────────────────────────────────────────────────────────
def head_html(path, title, desc):
    pf = prefix(path)
    preload = "".join(
        f'<link rel="preload" href="{pf}{f}" as="font" type="font/woff2" crossorigin>\n'
        for f in FONT_FILES)
    return (
        '<head>\n'
        '<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<meta name="color-scheme" content="dark">\n'
        f'<title>{title}</title>\n'
        f'<meta name="description" content="{desc}">\n'
        f'<link rel="icon" href="{pf}{FAVICON}">\n'
        f'{preload}'
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        f'<link href="{FONTS}" rel="stylesheet">\n'
        f'<link rel="stylesheet" href="{pf}css/wiki.css">\n'
        f'<script src="{pf}js/wiki.js" defer></script>\n'
        '</head>'
    )


def crumbs_html(path):
    if path == "index.html" or path not in PAGES:
        return ""
    pf = prefix(path)
    group, slug, label = PAGES[path]
    target = GROUP_LANDING.get(slug, f"index.html#explore-{slug}")
    if target == path:
        group_item = f"<li>{group}</li>"
    else:
        group_item = f'<li><a href="{pf}{target}">{group}</a></li>'
    return (
        '    <nav class="crumbs" aria-label="Breadcrumb"><ol>'
        f'{group_item}<li><span aria-current="page">{label}</span></li>'
        '</ol></nav>\n'
    )


def topbar_html(path):
    pf = prefix(path)
    return block("topbar", (
        '<a class="skip" href="#main">Skip to content</a>\n'
        '<header class="topbar">\n'
        '  <div class="topbar-inner">\n'
        '    <button class="topbar-menu" type="button" aria-controls="site-nav" aria-expanded="false">'
        '<span class="bars" aria-hidden="true"></span>Menu</button>\n'
        # aria-label: on phones the visible name is hidden and only the mark shows
        f'    <a class="brand" href="{pf}index.html" aria-label="{SITE} {WIKI_NAME}, home">'
        '<span class="wiki-mark" aria-hidden="true"></span>'
        f'<span class="brand-name">{SITE}</span><span class="brand-wiki">{WIKI_NAME}</span></a>\n'
        f'{crumbs_html(path)}'
        '  </div>\n'
        '</header>'
    ))


def sidebar_html(path):
    pf = prefix(path)
    parts = ['<nav class="sidebar" id="site-nav" aria-label="Wiki map">\n']
    for group, slug, links in SIDEBAR_GROUPS:
        parts.append(f'  <div class="map-group">\n    <p class="map-label" id="map-{slug}">{group}</p>\n'
                     f'    <ul aria-labelledby="map-{slug}">\n')
        for label, href in links:
            key, _ = status_of(href)
            tag = f'<span class="vh">,</span> {badge(key)}' if key else ""
            here = ' aria-current="page"' if href == path else ""
            parts.append(f'      <li><a href="{pf}{href}"{here}><span class="map-t">{label}</span>{tag}</a></li>\n')
        parts.append('    </ul>\n  </div>\n')
    parts.append(f'  <p class="map-key"><a href="{pf}index.html#status-key">How to read the status labels</a></p>\n')
    parts.append('</nav>')
    return block("sidebar", "".join(parts))


def notice_html(path):
    key, note = status_of(path)
    if not note:
        return ""
    return block("notice", (
        '<div class="notice" role="note">\n'
        f'  <p>{badge(key)}</p>\n'
        f'  <p>{note}</p>\n'
        '</div>'
    ))


def page_toc_html(toc):
    if not toc:
        return ""
    items = "".join(f'    <li><a href="{h}">{t}</a></li>\n' for h, t in toc)
    return block("page-toc", (
        '<details class="page-toc">\n'
        '  <summary>On this page</summary>\n'
        f'  <ul>\n{items}  </ul>\n'
        '</details>'
    ))


def toc_html(toc):
    if not toc:
        return ""
    items = "".join(f'    <li><a href="{h}">{t}</a></li>\n' for h, t in toc)
    return block("toc", (
        '<nav class="toc" aria-label="On this page">\n'
        '  <p class="toc-h">On this page</p>\n'
        f'  <ul>\n{items}  </ul>\n'
        '  <a class="toc-top" href="#top">Back to top</a>\n'
        '</nav>'
    ))


def pager_html(path):
    pf = prefix(path)
    idx = next((i for i, (_, _, _, h) in enumerate(READING_ORDER) if h == path), None)
    if idx is None:
        return ""
    cells = []
    if idx > 0:
        g, _, label, href = READING_ORDER[idx - 1]
        cells.append(f'  <a class="prev" href="{pf}{href}"><span class="k">&larr; Previous &middot; {g}</span>'
                     f'<span class="t">{label}</span></a>\n')
    else:
        cells.append('  <span></span>\n')
    if idx < len(READING_ORDER) - 1:
        g, _, label, href = READING_ORDER[idx + 1]
        cells.append(f'  <a class="next" href="{pf}{href}"><span class="k">Next &middot; {g} &rarr;</span>'
                     f'<span class="t">{label}</span></a>\n')
    return block("pager", '<nav class="pager" aria-label="Reading order">\n' + "".join(cells) + '</nav>')


def footer_html(path):
    pf = prefix(path)
    return block("footer", (
        '<footer class="site-footer">\n'
        '  <div class="site-footer-inner">\n'
        f'    <p class="site-footer-id"><span class="wiki-mark" aria-hidden="true"></span>{SITE} &middot; {WIKI_NAME} &middot; {REVISION}</p>\n'
        f'    <p><a href="{pf}index.html#status-key">Status key</a> &middot; '
        f'<a href="{pf}about/history.html">Company history</a> &middot; '
        f'<a href="{pf}about/history.html#contact">Contact</a> &middot; '
        f'<a href="{COMPANY_SITE}" rel="noopener">apollyondynamics.com<span class="vh"> (company website)</span> &nearr;</a></p>\n'
        '  </div>\n'
        '</footer>'
    ))


def directory_html(path):
    """The homepage's "Explore the wiki": every group and page with its one-line
    description and status, generated from the same data as the wiki map."""
    pf = prefix(path)
    parts = ['<!-- shell:directory -->\n<div class="directory">\n']
    for group, slug, links in SIDEBAR_GROUPS:
        if slug == "overview":
            continue
        parts.append(f'  <div class="dir-group" id="explore-{slug}">\n    <h3>{group}</h3>\n    <ul>\n')
        for label, href in links:
            key, _ = status_of(href)
            tag = f' {badge(key)}' if key else ""
            desc = DESCRIPTIONS.get(href, "")
            d = f'<span class="dir-d">{desc}</span>' if desc else ""
            parts.append(f'      <li><a href="{pf}{href}">{label}</a>{tag}{d}</li>\n')
        parts.append('    </ul>\n  </div>\n')
    parts.append('</div>\n<!-- /shell:directory -->')
    return "".join(parts)


# ── Extraction and migration ──────────────────────────────────────────────
TOC_ITEM = re.compile(r'<li[^>]*>\s*<a\b[^>]*?href="(#[^"]+)"[^>]*>(.*?)</a>\s*</li>', re.S)


def extract_toc(html):
    """The page's own "On this page" anchors, from the right-hand TOC."""
    m = re.search(r'<nav class="toc(?: empty)?"[^>]*>(.*?)</nav>', html, re.S)
    if not m:
        return []
    ul = re.search(r"<ul[^>]*>(.*?)</ul>", m.group(1), re.S)
    out = []
    for href, label in TOC_ITEM.findall(ul.group(1) if ul else ""):
        label = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", label)).strip()
        out.append((href, label))
    return out


def strip_generated(html):
    # blocks this script wrote before (the homepage directory is refreshed in place)
    html = re.sub(r'[ \t]*<!-- shell:(?!directory\b)([\w-]+) -->.*?<!-- /shell:\1 -->\n?', "", html, flags=re.S)
    # the older shell, migrated once
    html = re.sub(r'<div class="rail">.*?(?=<div class="shell">)', "", html, count=1, flags=re.S)
    html = re.sub(r'<aside class="aside"[^>]*>.*?</aside>\s*', "", html, count=1, flags=re.S)
    html = re.sub(r'\s*<nav class="toc(?: empty)?"[^>]*>.*?</nav>\n?', "\n", html, count=1, flags=re.S)
    html = re.sub(r'<nav class="pager"[^>]*>.*?</nav>\s*', "", html, count=1, flags=re.S)
    html = re.sub(r'<footer>.*?</footer>\s*', "", html, count=1, flags=re.S)
    html = re.sub(r'[ \t]*<div class="crumb">.*?</div>\n?', "", html, flags=re.S)
    return html


MAST_RE = re.compile(r'(<header class="masthead"[^>]*>)(.*?)(</header>)', re.S)


def fix_masthead(html):
    """House rule: no small label above the page title. A .mast-meta line that
    sits above the <h1> moves below the last standfirst (or below the <h1>)."""
    m = MAST_RE.search(html)
    if not m:
        return html
    inner = m.group(2)
    meta = re.search(r'[ \t]*<div class="mast-meta">.*?</div>\n?', inner, re.S)
    h1 = inner.find("<h1")
    if meta and h1 > meta.start():
        piece = meta.group(0)
        if not piece.endswith("\n"):
            piece += "\n"
        inner = inner[:meta.start()] + inner[meta.end():]
        last = None
        for sm in re.finditer(r'<p class="standfirst">.*?</p>\n?', inner, re.S):
            last = sm
        at = last.end() if last else inner.find("</h1>") + len("</h1>")
        if not inner[:at].endswith("\n"):
            piece = "\n" + piece
        inner = inner[:at] + piece + inner[at:]
    return html[:m.start(2)] + inner + html[m.end(2):]


def rewrite(path, html):
    head = re.search(r"<head>.*?</head>", html, re.S)
    title = re.search(r"<title>(.*?)</title>", head.group(0), re.S)
    title = title.group(1).strip() if title else SITE
    desc = re.search(r'<meta name="description" content="(.*?)">', head.group(0))
    desc = desc.group(1) if desc else (
        "Apollyon Dynamics engineering wiki: autonomous strike, interception and "
        "battlefield-intelligence systems, with the shared architecture they are built from.")
    toc = extract_toc(html)
    group = PAGES.get(path, (None, "overview", None))[1]

    new = strip_generated(html)
    new = new.replace(head.group(0), head_html(path, title, desc), 1)

    body = f'<body id="top" data-section="{group}"' + (' data-page="home"' if path == "index.html" else "") + ">"
    new = re.sub(r"<body[^>]*>\n?", lambda _m: body + "\n" + topbar_html(path), new, count=1)
    new = re.sub(r'<main class="main"[^>]*>', '<main class="main" id="main">', new, count=1)
    new = fix_masthead(new)

    new = re.sub(r'(<div class="layout">\n?)', lambda m: m.group(1) + "\n" + sidebar_html(path) + "\n", new, count=1)
    after_mast = notice_html(path) + page_toc_html(toc)
    if after_mast:
        mast = re.search(r'<main class="main" id="main">\s*<header class="masthead"[^>]*>.*?</header>\n?', new, re.S)
        if mast:
            new = new[:mast.end()] + "\n" + after_mast + new[mast.end():]
        else:
            print(f"  warning: {path} has no masthead first in <main>; contents box placed at the top")
            new = new.replace('<main class="main" id="main">', '<main class="main" id="main">\n' + after_mast, 1)
    new = re.sub(r"\s*</main>\n?", lambda _m: "\n\n" + pager_html(path) + "\n</main>\n" + toc_html(toc), new, count=1)
    new = re.sub(r"\s*</body>", lambda _m: "\n\n" + footer_html(path) + "\n</body>", new, count=1)
    new = re.sub(r"<!-- shell:directory -->.*?<!-- /shell:directory -->",
                 lambda _m: directory_html(path), new, flags=re.S)
    new = re.sub(r"\n{3,}", "\n\n", new)
    return new


def check_invariants(path, html):
    has_toc = bool(extract_toc(html))
    expected = {
        "topbar": 1, "sidebar": 1, "footer": 1,
        "notice": 1 if status_of(path)[1] else 0,
        "page-toc": 1 if has_toc else 0,
        "toc": 1 if has_toc else 0,
        "pager": 1 if path in PAGES else 0,
    }
    problems = []
    for name in BLOCKS:
        n = html.count(f"<!-- shell:{name} -->")
        if n != expected[name]:
            problems.append(f"{n} x shell:{name} (expected {expected[name]})")
    for needle in ('class="rail', 'class="aside"', "nav-toc", 'class="crumb"', "<footer>"):
        if needle in html:
            problems.append(f"legacy markup left: {needle}")
    if html.count("<main") != 1 or html.count('id="main"') != 1:
        problems.append("expected exactly one <main id=\"main\">")
    if html.count("<svg") != html.count("</svg>"):
        problems.append("unbalanced <svg>")
    if problems:
        raise SystemExit(f"{path}: " + "; ".join(problems) + " (nothing written)")


def pages():
    for root, dirs, files in os.walk(WIKI):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not d.startswith((".", "_")))
        for f in sorted(files):
            if f.endswith(".html"):
                full = os.path.join(root, f)
                yield os.path.relpath(full, WIKI).replace("\\", "/"), full


def main():
    check = "--check" in sys.argv
    changed, seen = 0, set()
    for rel, full in pages():
        seen.add(rel)
        if rel not in PAGES:
            print(f"  warning: {rel} is not in SIDEBAR_GROUPS (no map entry, breadcrumb or pager)")
        html = open(full, encoding="utf-8").read()
        new = rewrite(rel, html)
        check_invariants(rel, new)
        ids = set(re.findall(r'\sid="([^"]+)"', new))
        for h, _ in extract_toc(new):
            if h[1:] not in ids:
                print(f"  warning: {rel} lists {h} under On this page, but no element has that id")
        if new != html:
            changed += 1
            if check:
                print(f"needs update: {rel}")
            else:
                open(full, "w", encoding="utf-8", newline="\n").write(new)
                print(f"updated: {rel}")
    for href in PAGES:
        if href not in seen:
            print(f"  warning: SIDEBAR_GROUPS lists {href}, which does not exist")
    print(f"\n{changed} page(s) {'would change' if check else 'updated'}.")
    if check and changed:
        sys.exit(1)


if __name__ == "__main__":
    main()
