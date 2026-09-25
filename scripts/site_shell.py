#!/usr/bin/env python3
"""
site_shell.py — canonical rail / sidebar / footer shell for the Apollyon wiki.

Every page gets the same top rail, the same grouped sidebar (with its own
"On this page" table of contents carried over), and the same footer.

Usage:
    python3 wiki/scripts/site_shell.py            # apply to every page
    python3 wiki/scripts/site_shell.py --check    # report pages needing rewrite
"""
import os
import re
import sys
import html as html_mod

WIKI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FONTS = ('https://fonts.googleapis.com/css2?'
         'family=Inter:wght@400;500;600;700;800&'
         'family=JetBrains+Mono:wght@400;500;600;700&'
         'family=Newsreader:ital,opsz,wght@1,6..72,400&display=swap')

FAVICON = "assets/logos/favicon-red.png"

RAIL = [
    ("thesis", "Thesis", "index.html#thesis"),
    ("products", "Products", "index.html#products"),
    ("architecture", "Architecture", "architecture/index.html"),
    ("strategy", "Strategy", "strategy/trajectory.html"),
    ("doctrine", "Doctrine", "doctrine/new-arsenal.html"),
    ("company", "Company", "about/history.html"),
]

# The sidebar, in reading order. The prev/next pager walks this same list, so
# the order here is the order a first-time reader is led through the wiki.
SIDEBAR_GROUPS = [
    ("Overview", [
        ("The argument", "index.html"),
    ]),
    ("Products", [
        ("Nightshade family", "products/nightshade-adx1.html"),
        ("Hemlock", "products/hemlock.html"),
        ("Ahuti interceptor", "products/ahuti.html"),
        ("Piranha USV", "products/usv-strike.html"),
    ]),
    ("Architecture", [
        ("The shared core", "architecture/index.html"),
        ("Robust flight control", "subsystems/near-envelope-control.html"),
        ("GNSS-denied navigation", "subsystems/gnss-denied-navigation.html"),
        ("Edge compute", "subsystems/onboard-compute.html"),
        ("Flight software", "subsystems/flight-software.html"),
        ("Seekers", "subsystems/seekers.html"),
        ("Airframe &amp; structures", "subsystems/airframe-structures.html"),
        ("Launch &amp; ground systems", "subsystems/launch-systems.html"),
    ]),
    ("Strategy", [
        ("Trajectory &amp; cost per kg&middot;km", "strategy/trajectory.html"),
        ("The market", "strategy/market.html"),
        ("The competitive field", "strategy/competitive.html"),
        ("Supply chain", "strategy/supply-chain.html"),
    ]),
    ("Doctrine", [
        ("The New Arsenal", "doctrine/new-arsenal.html"),
        ("Precision is Mercy", "doctrine/precision-is-mercy.html"),
        ("The Missing Middle", "doctrine/missing-middle.html"),
        ("Strike design space", "doctrine/strike-design-space.html"),
    ]),
    ("Record", [
        ("Company history", "about/history.html"),
        ("Team &amp; advisors", "about/team.html"),
        ("The full record &middot; 70 episodes", "strategic-dependency/full-record.html"),
    ]),
]

READING_ORDER = [(g, label, href) for g, links in SIDEBAR_GROUPS for label, href in links]


def esc(s):
    return html_mod.escape(str(s), quote=False)


def depth(path):
    return 0 if "/" not in path.replace("\\", "/") else 1


def prefix(path):
    return "../" if depth(path) else ""


def page_key(path):
    p = path.replace("\\", "/")
    if p == "index.html":
        return "thesis"
    if p.startswith("products/"):
        return "products"
    if p.startswith("strategy/"):
        return "strategy"
    if p.startswith("architecture/") or p.startswith("subsystems/"):
        return "architecture"
    if p.startswith("doctrine/"):
        return "doctrine"
    if p.startswith("strategic-dependency/"):
        return "company"
    if p.startswith("about/"):
        return "company"
    return "thesis"


def resolve(path, href):
    # hrefs in the shell are wiki-root-relative; normalise for comparison with
    # the current page key. (The old join-with-prefix version never matched on
    # depth-1 pages, so "here" highlighting silently failed outside the root.)
    return os.path.normpath(href).replace("\\", "/")


def rail_html(path):
    key = page_key(path)
    pf = prefix(path)
    links = []
    for k, label, href in RAIL:
        cls = ' class="on"' if k == key else ""
        links.append(f'<a id="rail-{k}" href="{pf}{href}"{cls}>{label}</a>')
    return (
        '<div class="rail">\n'
        '  <div class="rail-inner">\n'
        '    <button class="rail-menu" type="button" aria-controls="site-nav" aria-expanded="false">'
        '<span class="bars" aria-hidden="true"></span><span class="lbl">Menu</span></button>\n'
        f'    <a class="rail-brand" href="{pf}index.html"><span class="glyph"></span>'
        'Apollyon Dynamics <em>&middot; Engineering Wiki</em></a>\n'
        '    <nav class="rail-links" aria-label="Sections">\n      ' + "\n      ".join(links) + '\n    </nav>\n'
        '  </div>\n'
        '  <div class="rail-progress" aria-hidden="true"><i></i></div>\n'
        '</div>\n'
    )


def _toc_items(block):
    ul = re.search(r"<ul[^>]*>(.*?)</ul>", block, re.S)
    if not ul:
        return []
    items = re.findall(r'<li>\s*<a href="([^"]+)"[^>]*>(.*?)</a>\s*</li>', ul.group(1), re.S)
    out = []
    for href, label in items:
        label = re.sub(r"<[^>]+>", "", label)
        label = re.sub(r"\s+", " ", label).strip()
        if href.startswith("#"):
            out.append((href, label))
    return out


def extract_toc(html):
    """The page's own 'On this page' anchors: from the right-hand TOC once the
    page has one, otherwise from the first list in the legacy sidebar."""
    m = re.search(r'<nav class="toc"[^>]*>(.*?)</nav>', html, re.S)
    if m:
        return _toc_items(m.group(1))
    m = re.search(r'<aside class="aside"[^>]*>(.*?)</aside>', html, re.S)
    return _toc_items(m.group(1)) if m else []


def aside_html(path, toc):
    pf = prefix(path)
    own = path.replace("\\", "/")
    parts = ['<aside class="aside" id="site-nav" aria-label="Wiki navigation">\n']
    for gi, (group, links) in enumerate(SIDEBAR_GROUPS, 1):
        on = any(resolve(path, h) == own for _, h in links)
        parts.append(f'  <div class="nav-group{" on" if on else ""}">\n')
        parts.append(f'    <h4><span class="n">{gi:02d}</span>{group}</h4>\n    <ul>\n')
        for label, href in links:
            if resolve(path, href) == own:
                parts.append(f'      <li class="here"><a href="{pf}{href}" aria-current="page">{label}</a>')
                if toc:
                    parts.append('\n        <ul class="nav-toc">\n')
                    for th, tl in toc:
                        parts.append(f'          <li><a href="{th}">{tl}</a></li>\n')
                    parts.append('        </ul>\n      ')
                parts.append('</li>\n')
            else:
                parts.append(f'      <li><a href="{pf}{href}">{label}</a></li>\n')
        parts.append('    </ul>\n  </div>\n')
    parts.append('</aside>\n')
    return "".join(parts)


def toc_html(toc):
    if not toc:
        return '<nav class="toc empty" aria-label="On this page"></nav>\n'
    parts = ['<nav class="toc" aria-label="On this page">\n  <h4>On this page</h4>\n  <ul>\n']
    for href, label in toc:
        parts.append(f'    <li><a href="{href}">{label}</a></li>\n')
    parts.append('  </ul>\n  <a class="toc-top" href="#top">Back to top &uarr;</a>\n</nav>\n')
    return "".join(parts)


def pager_html(path):
    own = path.replace("\\", "/")
    pf = prefix(path)
    idx = next((i for i, (_, _, h) in enumerate(READING_ORDER) if h == own), None)
    if idx is None:
        return ""
    cells = []
    if idx > 0:
        g, label, href = READING_ORDER[idx - 1]
        cells.append(f'<a class="prev" href="{pf}{href}"><span class="k">&larr; Previous &middot; {g}</span>'
                     f'<span class="t">{label}</span></a>')
    else:
        cells.append('<span></span>')
    if idx < len(READING_ORDER) - 1:
        g, label, href = READING_ORDER[idx + 1]
        cells.append(f'<a class="next" href="{pf}{href}"><span class="k">Next &middot; {g} &rarr;</span>'
                     f'<span class="t">{label}</span></a>')
    return '<nav class="pager" aria-label="Reading order">\n  ' + "\n  ".join(cells) + '\n</nav>\n'


def footer_html(path):
    pf = prefix(path)
    return (
        '<footer>\n'
        '  <div>Apollyon Dynamics &middot; Neo-Prime Wiki &middot; Rev 3.0</div>\n'
        f'  <div><a href="{pf}doctrine/new-arsenal.html">The New Arsenal</a> &middot; '
        f'<a href="{pf}about/history.html">Company</a> &middot; '
        f'<a href="{pf}strategy/competitive.html">Competitive field</a> &middot; '
        'apollyondynamics.com</div>\n'
        '</footer>\n'
    )


HEAD_RE = re.compile(r"<head>.*?</head>", re.S)


def head_html(path, html):
    title = re.search(r"<title>(.*?)</title>", html, re.S)
    title = title.group(1).strip() if title else "Apollyon Dynamics"
    desc = re.search(r'<meta name="description" content="(.*?)">', html)
    desc = desc.group(1) if desc else (
        "Apollyon Dynamics engineering wiki — autonomous strike, interception and "
        "battlefield-intelligence systems, with the shared architecture they are built from.")
    return (
        '<head>\n'
        '<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        f'<title>{title}</title>\n'
        f'<meta name="description" content="{desc}">\n'
        f'<link rel="icon" href="{prefix(path)}{FAVICON}">\n'
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        f'<link href="{FONTS}" rel="stylesheet">\n'
        f'<link rel="stylesheet" href="{prefix(path)}css/wiki.css">\n'
        f'<script src="{prefix(path)}js/wiki.js" defer></script>\n'
        '</head>'
    )


def rewrite(path, html):
    new = HEAD_RE.sub(lambda m: head_html(path, m.group(0)), html, count=1)
    new = re.sub(r"<body[^>]*>", f'<body id="top" data-section="{page_key(path)}">', new, count=1)

    # rail
    new = re.sub(r'<div class="rail">.*?</div>\s*</div>\s*(?:<div class="rail-progress".*?</div>\s*</div>\s*)?(?=<div class="shell">)',
                 rail_html(path), new, count=1, flags=re.S)

    # left navigation (with the page TOC nested under the current page)
    toc = extract_toc(html)
    new = re.sub(r'<aside class="aside"[^>]*>.*?</aside>',
                 lambda m: aside_html(path, toc), new, count=1, flags=re.S)

    # right-hand "On this page", placed after <main> inside the layout grid
    new = re.sub(r'\s*<nav class="toc[^"]*"[^>]*>.*?</nav>\n?', "\n", new, count=1, flags=re.S)
    new = re.sub(r'(</main>\s*)', lambda m: m.group(1) + toc_html(toc), new, count=1)

    # prev / next in reading order, just above the footer
    new = re.sub(r'<nav class="pager".*?</nav>\s*', "", new, count=1, flags=re.S)
    new = re.sub(r'<footer>', lambda m: pager_html(path) + '<footer>', new, count=1)

    # footer
    new = re.sub(r'<footer>.*?</footer>', lambda m: footer_html(path), new, count=1, flags=re.S)

    # normalise whitespace introduced by replacements
    new = re.sub(r"\n{3,}", "\n\n", new)
    return new


def main():
    check = "--check" in sys.argv
    changed = 0
    for root, _dirs, files in os.walk(WIKI):
        if "scripts" in root or "assets" in root or "css" in root or "js" in root:
            continue
        for f in sorted(files):
            if not f.endswith(".html"):
                continue
            full = os.path.join(root, f)
            rel = os.path.relpath(full, WIKI).replace("\\", "/")
            html = open(full, encoding="utf-8").read()
            new = rewrite(rel, html)
            if new != html:
                changed += 1
                if check:
                    print(f"needs update: {rel}")
                else:
                    open(full, "w", encoding="utf-8").write(new)
                    print(f"updated: {rel}")
    print(f"\n{changed} page(s) {'would change' if check else 'updated'}.")


if __name__ == "__main__":
    main()
