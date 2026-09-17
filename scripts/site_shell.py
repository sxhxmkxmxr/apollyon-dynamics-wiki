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

WIKI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FONTS = ('https://fonts.googleapis.com/css2?'
         'family=Inter:wght@400;500;600;700;800&'
         'family=JetBrains+Mono:wght@400;500;600;700&'
         'family=Newsreader:ital,opsz,wght@1,6..72,400&display=swap')

FAVICON = "assets/logos/favicon-red.png"

RAIL = [
    ("thesis", "Thesis", "index.html"),
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
        ("Hemlock family", "products/hemlock.html"),
        ("Ahuti interceptor", "products/ahuti.html"),
        ("Piranha USV", "products/usv-strike.html"),
        ("Apollyon Cortex", "products/cortex.html"),
        ("Mobile command centre", "products/mdcc.html"),
        ("Mobile drone lab", "products/mobile-drone-lab.html"),
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
        ("Propulsion", "subsystems/propulsion.html"),
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
        ("The full record &middot; 70 episodes", "strategic-dependency/full-record.html"),
        ("Research platforms", "products/research-platforms.html"),
    ]),
]


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
    return os.path.normpath(os.path.join(prefix(path), href)).replace("\\", "/")


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
    for group, links in SIDEBAR_GROUPS:
        parts.append(f'  <h4>{group}</h4>\n  <ul>\n')
        for label, href in links:
            here = ' class="here"' if resolve(path, href) == own else ""
            parts.append(f'    <li><a href="{pf}{href}"{here}>{label}</a></li>\n')
        parts.append('  </ul>\n')
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
        f'<link rel="icon" href="{FAVICON}">\n'
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
