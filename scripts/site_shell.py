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
    ("strategy", "Strategy", "strategy/trajectory.html"),
    ("architecture", "Architecture", "architecture/index.html"),
    ("dependencies", "Dependencies", "strategic-dependency/full-record.html"),
    ("doctrine", "Doctrine", "doctrine/new-arsenal.html"),
    ("company", "Company", "about/history.html"),
]

SIDEBAR_GROUPS = [
    ("Products", [
        ("Nightshade family", "products/nightshade-adx1.html"),
        ("Hemlock", "products/hemlock.html"),
        ("Ahuti interceptor", "products/ahuti.html"),
        ("Piranha USV", "products/usv-strike.html"),
    ]),
    ("Strategy", [
        ("Trajectory &amp; cost per kg&middot;km", "strategy/trajectory.html"),
        ("The competitive field", "strategy/competitive.html"),
        ("Supply chain", "strategy/supply-chain.html"),
    ]),
    ("Architecture", [
        ("The shared core", "architecture/index.html"),
        ("Robust flight control", "subsystems/near-envelope-control.html"),
        ("GNSS-denied navigation", "subsystems/gnss-denied-navigation.html"),
        ("Edge compute", "subsystems/onboard-compute.html"),
        ("Flight software", "subsystems/flight-software.html"),
        ("Seekers", "subsystems/seekers.html"),
        ("Airframe &amp; structures", "subsystems/airframe-structures.html"),
        ("Launch &amp; ground", "subsystems/launch-systems.html"),
    ]),
    ("Doctrine", [
        ("The New Arsenal", "doctrine/new-arsenal.html"),
        ("Precision is Mercy", "doctrine/precision-is-mercy.html"),
        ("The missing middle", "doctrine/missing-middle.html"),
        ("Strike design space", "doctrine/strike-design-space.html"),
    ]),
    ("Record", [
        ("Company history", "about/history.html"),
        ("Team &amp; advisors", "about/team.html"),
        ("The full record &middot; 70 episodes", "strategic-dependency/full-record.html"),
    ]),
]

# The atlas is the wiki's structure as a drawing: two hubs (the index argument
# and the architecture core), four reading clusters hanging off the index, and
# the subsystem tier under the core. Pages are links; the current page is red.
ATLAS_CLUSTERS = [
    ("PRODUCTS", [
        ("Nightshade family", "products/nightshade-adx1.html"),
        ("Hemlock", "products/hemlock.html"),
        ("Ahuti interceptor", "products/ahuti.html"),
        ("Piranha USV", "products/usv-strike.html"),
    ]),
    ("STRATEGY", [
        ("Trajectory & cost per kg\u00b7km", "strategy/trajectory.html"),
        ("The competitive field", "strategy/competitive.html"),
        ("Supply chain", "strategy/supply-chain.html"),
    ]),
    ("DOCTRINE", [
        ("The New Arsenal", "doctrine/new-arsenal.html"),
        ("Precision is Mercy", "doctrine/precision-is-mercy.html"),
        ("The missing middle", "doctrine/missing-middle.html"),
        ("Strike design space", "doctrine/strike-design-space.html"),
    ]),
    ("RECORD", [
        ("Company history", "about/history.html"),
        ("Team & advisors", "about/team.html"),
        ("The full record \u00b7 70 episodes", "strategic-dependency/full-record.html"),
    ]),
]

ATLAS_SUBSYSTEMS = [
    ("Robust flight control", "subsystems/near-envelope-control.html"),
    ("GNSS-denied navigation", "subsystems/gnss-denied-navigation.html"),
    ("Edge compute", "subsystems/onboard-compute.html"),
    ("Flight software", "subsystems/flight-software.html"),
    ("Seekers", "subsystems/seekers.html"),
    ("Airframe & structures", "subsystems/airframe-structures.html"),
    ("Launch & ground", "subsystems/launch-systems.html"),
]


def esc(s):
    return html_mod.escape(str(s), quote=False)


def atlas_svg(path):
    """Layered map of the wiki, generated per page with the current node lit."""
    own = path.replace("\\", "/")
    pf = prefix(path)
    W, L, R = 232, 16, 222

    def is_here(href):
        return resolve(path, href) == own

    def hub(label, sub, num, href, y):
        cls = "atlas-hub here" if is_here(href) else "atlas-hub"
        return (
            f'<a href="{pf}{href}" class="{cls}">'
            f'<rect class="hub-plate" x="6" y="{y}" width="220" height="42"/>'
            f'<text class="hub-t" x="18" y="{y + 17}">{esc(label)}</text>'
            f'<text class="hub-s" x="18" y="{y + 30}">{esc(sub)}</text>'
            f'<text class="hub-n" x="216" y="{y + 17}" text-anchor="end">{num}</text>'
            '</a>'
        )

    body = []
    y = 10
    body.append(hub("INDEX", "the argument \u00b7 every path starts here", "01", "index.html", y))
    top = y + 42
    y = top + 20

    for ci, (label, pages) in enumerate(ATLAS_CLUSTERS):
        on = " on" if any(is_here(h) for _, h in pages) else ""
        body.append(f'<line class="spine" x1="{L}" y1="{y - 3}" x2="28" y2="{y - 3}"/>')
        body.append(f'<text class="cl{on}" x="30" y="{y}">{esc(label)}</text>')
        body.append(f'<line class="rule" x1="30" y1="{y + 5}" x2="{R}" y2="{y + 5}"/>')
        y += 17
        for name, href in pages:
            here = " here" if is_here(href) else ""
            body.append(
                f'<a href="{pf}{href}" class="atlas-node{here}">'
                f'<rect class="mk" x="30" y="{y - 4.5}" width="5" height="5"/>'
                f'<text class="lb" x="41" y="{y + 3.5}">{esc(name)}</text>'
                '</a>'
            )
            y += 17
        if ci == 0:
            body.append(f'<text class="bridge" x="41" y="{y + 2}">each machine configures the core \u2193</text>')
            y += 16
        y += 10

    y += 6
    body.append(hub("ARCHITECTURE", "the core \u00b7 method, machine, loop", "02", "architecture/index.html", y))
    mid = y + 42
    y = mid + 20

    on = " on" if any(is_here(h) for _, h in ATLAS_SUBSYSTEMS) else ""
    body.append(f'<line class="spine" x1="{L}" y1="{y - 3}" x2="28" y2="{y - 3}"/>')
    body.append(f'<text class="cl{on}" x="30" y="{y}">SUBSYSTEMS</text>')
    body.append(f'<line class="rule" x1="30" y1="{y + 5}" x2="{R}" y2="{y + 5}"/>')
    y += 17
    for name, href in ATLAS_SUBSYSTEMS:
        here = " here" if is_here(href) else ""
        body.append(
            f'<a href="{pf}{href}" class="atlas-node{here}">'
            f'<rect class="mk" x="30" y="{y - 4.5}" width="5" height="5"/>'
            f'<text class="lb" x="41" y="{y + 3.5}">{esc(name)}</text>'
            '</a>'
        )
        y += 17

    bottom = y + 4
    H = int(bottom + 8)
    spine = (
        f'<line class="spine" x1="{L}" y1="{top}" x2="{L}" y2="{mid + 6}"/>'
        f'<line class="spine" x1="{L}" y1="{mid + 6}" x2="{L}" y2="{bottom}"/>'
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">' + spine + "".join(body) + '</svg>'
    )


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
        return "dependencies"
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
        links.append(f'<a href="{pf}{href}"{cls}>{label}</a>')
    return (
        '<div class="rail">\n'
        '  <div class="rail-inner">\n'
        f'    <a class="rail-brand" href="{pf}index.html"><span class="glyph"></span>'
        'Apollyon Dynamics <em>&middot; Engineering Wiki</em></a>\n'
        '    <nav class="rail-links">\n      ' + "\n      ".join(links) + '\n    </nav>\n'
        '  </div>\n'
        '</div>\n'
    )


def extract_toc(html):
    """Carry over the page's own 'On this page' anchors from the old sidebar."""
    m = re.search(r'<aside class="aside">(.*?)</aside>', html, re.S)
    if not m:
        return []
    block = m.group(1)
    ul = re.search(r"<ul>(.*?)</ul>", block, re.S)
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


def aside_html(path, toc):
    pf = prefix(path)
    own = path.replace("\\", "/")
    parts = ['<aside class="aside">\n']
    if toc:
        parts.append('  <h4>On this page</h4>\n  <ul>\n')
        for href, label in toc:
            parts.append(f'    <li><a href="{href}">{label}</a></li>\n')
        parts.append('  </ul>\n')
    parts.append('  <nav class="atlas" aria-label="Wiki map">\n    <h4>Wiki map</h4>\n')
    parts.append(atlas_svg(path))
    parts.append('\n  </nav>\n')
    parts.append('  <div class="groups">\n')
    for group, links in SIDEBAR_GROUPS:
        parts.append(f'  <h4>{group}</h4>\n  <ul>\n')
        for label, href in links:
            here = ' class="here"' if resolve(path, href) == own else ""
            parts.append(f'    <li><a href="{pf}{href}"{here}>{label}</a></li>\n')
        parts.append('  </ul>\n')
    parts.append('  </div>\n')
    parts.append('</aside>\n')
    return "".join(parts)


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
        '</head>'
    )


def rewrite(path, html):
    new = HEAD_RE.sub(lambda m: head_html(path, m.group(0)), html, count=1)

    # rail
    new = re.sub(r'<div class="rail">.*?</div>\s*</div>\s*(?=<div class="shell">)',
                 rail_html(path), new, count=1, flags=re.S)

    # sidebar
    toc = extract_toc(html)
    new = re.sub(r'<aside class="aside">.*?</aside>',
                 lambda m: aside_html(path, toc), new, count=1, flags=re.S)

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
