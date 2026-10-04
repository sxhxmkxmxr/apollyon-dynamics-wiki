#!/usr/bin/env python3
"""
site_shell.py — the Vector 2022 (Wikipedia) skin around every wiki page.

Each page keeps its article between two markers:

    <!-- article:start -->  …hand-edited content…  <!-- article:end -->

and everything around it — header, main menu, contents, page tabs, tools,
appearance menu, succession box, navbox, categories, footer and sticky
header — is written here. The page title (h1#firstHeading) and the grey
subtitle under "From Apollyon Wiki" (#mw-content-subtitle) are read back from
the page on every run, so edit them in place. Inline scripts that belong to a
page sit between <!-- page-scripts:start --> and <!-- page-scripts:end -->.

The contents list is built from the article's headings: every
<section id="…"> contributes its <h2>, and each <h3> directly inside it
(missing ids are added, MediaWiki style).

Also written, from the pages on disk and from git:
    js/wiki-map-data.js      pages, sections, extracts, thumbnails, backlinks
                             (search suggestions, page previews, contents)
    js/wiki-search-data.js   section text for Special:Search (loaded on demand)
    js/wiki-history-data.js  revisions per page (history, info, recent changes)
    special/*.html           Search, Contents, Recent changes, Random article

Pages written by the old dark shell (a <header class="masthead"> inside
<main class="main">) are migrated on first run; gen_full_record.py still
writes that form.

Usage:
    python3 wiki/scripts/site_shell.py            # apply to every page
    python3 wiki/scripts/site_shell.py --check    # report pages needing rewrite
"""
import html as html_mod
import json
import os
import re
import subprocess
import sys

WIKI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SITENAME = "Apollyon Wiki"
SITESUB = "From Apollyon Wiki"
PUBLISHER = "Apollyon Dynamics"
WEBSITE = "https://apollyondynamics.com"
REVISION = "Rev 3.0"
CONTACT = "about/history.html#contact"

# Inter and JetBrains Mono are the diagram faces (the SVG labels were fitted to
# them). Page text uses Wikipedia's own stacks and needs no web font.
FONTS = ('https://fonts.googleapis.com/css2?'
         'family=Inter:wght@400;500;600;700;800&'
         'family=JetBrains+Mono:wght@400;500;600;700;800&display=swap')

FAVICON = "assets/logos/favicon-red.png"
LOGO = "assets/logos/logo-ad-white.png"

# The main menu, in reading order. The succession box walks this same list, so
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
GROUP_OF = {href: g for g, _, href in READING_ORDER}

# Generated special pages: path → (title, <title>, what the page renders)
SPECIAL = {
    "special/search.html": ("Search results", "Search results", "search"),
    "special/contents.html": ("Contents", "Contents", "contents"),
    "special/recent-changes.html": ("Recent changes", "Recent changes", "recentchanges"),
    "special/random.html": ("Random article", "Random article", "random"),
}

SKIP_DIRS = ("scripts", "assets", "css", "js", "docs", "audit", "drafts", ".git")


# ── helpers ──────────────────────────────────────────────────────────────
def esc(s):
    return html_mod.escape(str(s), quote=True)


def plain(s):
    s = re.sub(r"<(svg|script|style)\b.*?</\1>", " ", s, flags=re.S)
    return re.sub(r"\s+", " ", html_mod.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def tidy(s):
    """Plain text for labels: tags dropped, spacing around punctuation fixed."""
    t = plain(s)
    return re.sub(r"\s+([,.;:)])", r"\1", t)


def prefix(path):
    return "../" if "/" in path.replace("\\", "/") else ""


def slug(text):
    """MediaWiki-style anchor: words joined with underscores."""
    t = re.sub(r"[^\w\s\-().]", " ", plain(text), flags=re.U)
    t = re.sub(r"\s+", "_", t.strip())
    return re.sub(r"_+", "_", t).strip("_") or "section"


def page_key(path):
    p = path.replace("\\", "/")
    if p.startswith("special/"):
        return "special"
    return (GROUP_OF.get(p) or "Overview").lower()


# ── icons (Codex, 20×20) ─────────────────────────────────────────────────
def icon(name):
    return f'<span class="vector-icon mw-ui-icon-{name} mw-ui-icon-wikimedia-{name}"></span>'


# ── reading a page ───────────────────────────────────────────────────────
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
        "param", "source", "track", "wbr"}
TAG = re.compile(r"<!--.*?-->|<(/?)([a-zA-Z][a-zA-Z0-9-]*)\b[^>]*?(/?)>", re.S)


def direct_children(inner, name):
    """(start, end) spans of <name> elements that are direct children of the
    fragment `inner`, found by tracking tag depth."""
    out, depth, start = [], 0, None
    for m in TAG.finditer(inner):
        if m.group(0).startswith("<!--"):
            continue
        close, tag, selfclose = m.group(1), m.group(2).lower(), m.group(3)
        if tag in VOID or selfclose:
            continue
        if not close:
            if depth == 0 and tag == name:
                start = m.start()
            depth += 1
        else:
            depth -= 1
            if depth == 0 and tag == name and start is not None:
                out.append((start, m.end()))
                start = None
    return out


def section_blocks(article):
    """[(id, start, end, inner_start, inner_end)] for top-level <section id>."""
    out = []
    for s, e in direct_children(article, "section"):
        block = article[s:e]
        m = re.match(r"<section\b[^>]*\bid=\"([^\"]+)\"[^>]*>", block)
        if m:
            out.append((m.group(1), s, e, s + m.end(), e - len("</section>")))
    return out


def ensure_h3_ids(article):
    """Give every <h3> directly inside a <section> an id, as MediaWiki does."""
    taken = set(re.findall(r'\bid="([^"]+)"', article))
    edits = []
    for _sid, _s, _e, a, b in section_blocks(article):
        inner = article[a:b]
        for hs, he in direct_children(inner, "h3"):
            tag = re.match(r"<h3\b[^>]*>", inner[hs:he]).group(0)
            if re.search(r'\bid="', tag):
                continue
            text = re.sub(r'<span class="hno">.*?</span>', "", inner[hs + len(tag):he - 5], flags=re.S)
            base = new = slug(text)
            n = 2
            while new in taken:
                new, n = f"{base}_{n}", n + 1
            taken.add(new)
            edits.append((a + hs + 3, f' id="{new}"'))
    for pos, ins in sorted(edits, reverse=True):
        article = article[:pos] + ins + article[pos:]
    return article


def heading_label(h):
    return tidy(re.sub(r'<span class="(hno|mw-editsection)">.*?</span>', "", h, flags=re.S))


def extract_toc(article):
    """[(id, label, [(id, label), …]), …] from the article's sections."""
    toc = []
    for sid, _s, _e, a, b in section_blocks(article):
        inner = article[a:b]
        h2 = re.search(r"<h2\b[^>]*>(.*?)</h2>", inner, re.S)
        label = heading_label(h2.group(1)) if h2 else sid
        subs = []
        for hs, he in direct_children(inner, "h3"):
            m = re.match(r'<h3\b[^>]*\bid="([^"]+)"[^>]*>(.*?)</h3>', inner[hs:he], re.S)
            if m:
                subs.append((m.group(1), heading_label(m.group(2))))
        toc.append((sid, label, subs))
    return toc


def between(html, a, b):
    i = html.find(a)
    j = html.find(b, i + len(a)) if i >= 0 else -1
    return html[i + len(a):j] if i >= 0 and j >= 0 else None


def parse_page(path, html):
    """Title, subtitle, article and page scripts, from either form of page."""
    title_tag = re.search(r"<title>(.*?)</title>", html, re.S)
    desc = re.search(r'<meta name="description" content="(.*?)">', html)
    page = {
        "title_tag": title_tag.group(1).strip() if title_tag else PUBLISHER,
        "description": desc.group(1) if desc else "",
        "scripts": "",
    }
    article = between(html, "<!-- article:start -->", "<!-- article:end -->")
    if article is not None:
        h1 = re.search(r'<span class="mw-page-title-main">(.*?)</span>\s*</h1>', html, re.S)
        sub = re.search(r'<div id="mw-content-subtitle">(.*?)</div>', html, re.S)
        page["title"] = h1.group(1).strip() if h1 else page["title_tag"]
        page["subtitle"] = sub.group(1).strip() if sub else ""
        page["article"] = article.strip("\n")
        page["scripts"] = (between(html, "<!-- page-scripts:start -->", "<!-- page-scripts:end -->") or "").strip("\n")
        return page

    # ── legacy (dark shell) page: migrate ────────────────────────────────
    main = re.search(r'<main class="main">(.*)</main>', html, re.S)
    if not main:
        raise SystemExit(f"{path}: no article markers and no <main class=\"main\">")
    body = main.group(1)
    body = re.sub(r'<nav class="pager".*?</nav>\s*', "", body, flags=re.S)
    body = re.sub(r"<footer>.*?</footer>\s*", "", body, flags=re.S)
    body = re.sub(r'<div class="crumb">.*?</div>\s*', "", body, count=1, flags=re.S)
    mast = re.search(r'<header class="masthead"[^>]*>(.*?)</header>\s*', body, re.S)
    lead = ""
    title, subtitle = page["title_tag"], ""
    if mast:
        m = mast.group(1)
        h1 = re.search(r"<h1>(.*?)</h1>", m, re.S)
        if h1:
            title = re.sub(r"\s+", " ", h1.group(1)).strip()
        meta = re.search(r'<div class="mast-meta">(.*?)</div>', m, re.S)
        if meta:
            subtitle = re.sub(r"\s+", " ", meta.group(1)).strip()
        lead = "\n".join(p.strip() for p in re.findall(r'<p class="standfirst">.*?</p>', m, re.S))
        body = body[:mast.start()] + body[mast.end():]
    body = body.strip("\n")
    hero = re.match(r'\s*(<div class="hero-plate">.*?</div>\s*</div>\s*</div>)', body, re.S)
    if hero:
        plate = hero.group(1)
        alt = re.search(r'alt="([^"]*)"', plate)
        short = short_title(page["title_tag"])
        plate = plate.replace('<div class="hero-plate">',
                              f'<div class="hero-plate">\n  <div class="infobox-above">{short}</div>', 1)
        if alt:
            plate = re.sub(r"(<img [^>]*>)", r'\1\n  <div class="infobox-caption">' + alt.group(1) + "</div>", plate, count=1)
        body = body[hero.end():].lstrip("\n")
        lead = plate + "\n\n" + lead
    page["title"] = title
    page["subtitle"] = subtitle
    page["article"] = (lead + "\n\n" + body).strip("\n") if lead else body
    after = html[main.end():]
    scripts = re.findall(r"<script>(?!\s*\(function\(\)\{var c=).*?</script>", after, re.S)
    page["scripts"] = "\n".join(scripts)
    return page


def short_title(title_tag):
    """'Hemlock - Apollyon Wiki' → 'Hemlock'; legacy 'X — Apollyon Dynamics Wiki' → 'X'."""
    t = html_mod.unescape(title_tag).strip()
    suffix = f" - {SITENAME}"
    if t.endswith(suffix):
        t = t[:-len(suffix)]
    elif " — " in t:
        t = t.rsplit(" — ", 1)[0]
    return esc(t.strip()).replace("&#x27;", "'")


# ── shell pieces ─────────────────────────────────────────────────────────
def dropdown(did, label_html, content, cls="", icon_only=True, title=None, label_text=""):
    """A Vector checkbox-hack dropdown: works without JS; wiki.js adds
    outside-click and Escape handling."""
    btn = "cdx-button--icon-only" if icon_only else ""
    t = f' title="{esc(title)}"' if title else ""
    return (
        f'<div id="{did}" class="vector-dropdown {cls}"{t}>\n'
        f'  <input type="checkbox" id="{did}-checkbox" role="button" aria-haspopup="true" '
        f'class="vector-dropdown-checkbox" aria-label="{esc(label_text)}">\n'
        f'  <label id="{did}-label" for="{did}-checkbox" class="vector-dropdown-label cdx-button '
        f'cdx-button--fake-button cdx-button--weight-quiet {btn}" aria-hidden="true">{label_html}</label>\n'
        f'  <div class="vector-dropdown-content">\n{content}\n  </div>\n'
        f'</div>'
    )


def pinnable_header(label, feature, pinned):
    return (
        f'<div class="vector-pinnable-header vector-{feature}-pinnable-header'
        f'{" vector-pinnable-header-pinned" if pinned else ""}" data-feature-name="{feature}-pinned">\n'
        f'  <div class="vector-pinnable-header-label">{label}</div>\n'
        f'  <button class="vector-pinnable-header-toggle-button vector-pinnable-header-pin-button" '
        f'data-event-name="pinnable-header.{feature}.pin">move to sidebar</button>\n'
        f'  <button class="vector-pinnable-header-toggle-button vector-pinnable-header-unpin-button" '
        f'data-event-name="pinnable-header.{feature}.unpin">hide</button>\n'
        f'</div>'
    )


def portlet(pid, heading, items, heading_hidden=False):
    lis = "\n".join(items)
    h = f'<div class="vector-menu-heading{" vector-menu-heading-hidden" if heading_hidden else ""}">{heading}</div>\n'
    return (f'<div id="{pid}" class="vector-menu mw-portlet mw-portlet-{pid[2:]}">\n{h}'
            f'<div class="vector-menu-content"><ul class="vector-menu-content-list">\n{lis}\n</ul></div>\n</div>')


def li(lid, href, text, title=None, accesskey=None, cls="", extra=""):
    t = f' title="{esc(title)}{f" [{accesskey}]" if accesskey else ""}"' if title else ""
    a = f' accesskey="{accesskey}"' if accesskey else ""
    return f'<li id="{lid}" class="mw-list-item {cls}"><a href="{href}"{t}{a}{extra}><span>{text}</span></a></li>'


def main_menu(path):
    pf = prefix(path)
    own = path.replace("\\", "/")
    parts = [pinnable_header("Main menu", "main-menu", False)]
    parts.append(portlet("p-navigation", "Navigation", [
        li("n-mainpage-description", f"{pf}index.html", "Main page", "Visit the main page", "z"),
        li("n-contents", f"{pf}special/contents.html", "Contents", "Guides to browsing Apollyon Wiki"),
        li("n-randompage", f"{pf}special/random.html", "Random article", "Visit a randomly selected article", "x"),
        li("n-aboutsite", f"{pf}about/history.html", "About Apollyon Dynamics", "Find out about Apollyon Dynamics"),
        li("n-contactpage", f"{pf}{CONTACT}", "Contact us", "How to contact Apollyon Dynamics"),
    ], heading_hidden=True))
    for group, links in SIDEBAR_GROUPS[1:]:
        items = []
        for label, href in links:
            cur = ' aria-current="page"' if href == own else ""
            items.append(li(f"n-{slug(label).lower()}", f"{pf}{href}", label, extra=cur,
                            cls="mw-list-item-current" if href == own else ""))
        parts.append(portlet(f"p-{group.lower()}", group, items))
    parts.append(portlet("p-interaction", "Wiki", [
        li("n-recentchanges", f"{pf}special/recent-changes.html", "Recent changes", "A list of recent changes to the wiki", "r"),
    ]))
    return ('<div id="vector-main-menu" class="vector-main-menu vector-pinnable-element">\n'
            + "\n".join(parts) + "\n</div>")


def toc_html(toc):
    items = ['<li id="toc-mw-content-text" class="vector-toc-list-item vector-toc-level-1 vector-toc-list-item-active">\n'
             '  <a href="#" class="vector-toc-link"><div class="vector-toc-text">(Top)</div></a>\n</li>']
    for n, (sid, label, subs) in enumerate(toc, 1):
        sub_html, toggle = "", ""
        if subs:
            sl = "\n".join(
                f'    <li id="toc-{esc(h)}" class="vector-toc-list-item vector-toc-level-2">\n'
                f'      <a class="vector-toc-link" href="#{esc(h)}"><div class="vector-toc-text">'
                f'<span class="vector-toc-numb">{n}.{k}</span><span>{esc(t)}</span></div></a>\n    </li>'
                for k, (h, t) in enumerate(subs, 1))
            toggle = (f'  <button aria-controls="toc-{esc(sid)}-sublist" class="cdx-button cdx-button--weight-quiet '
                      f'cdx-button--icon-only vector-toc-toggle">{icon("expand")}'
                      f'<span>Toggle {esc(label)} subsection</span></button>\n')
            sub_html = f'  <ul id="toc-{esc(sid)}-sublist" class="vector-toc-list">\n{sl}\n  </ul>\n'
        items.append(
            f'<li id="toc-{esc(sid)}" class="vector-toc-list-item vector-toc-level-1">\n'
            f'  <a class="vector-toc-link" href="#{esc(sid)}"><div class="vector-toc-text">'
            f'<span class="vector-toc-numb">{n}</span><span>{esc(label)}</span></div></a>\n'
            f'{toggle}{sub_html}</li>')
    return ('<div id="vector-toc" class="vector-toc vector-pinnable-element">\n'
            + pinnable_header("Contents", "toc", True) + "\n"
            '<ul class="vector-toc-contents" id="mw-panel-toc-list">\n' + "\n".join(items) + "\n</ul>\n</div>")


def page_tools(path, special):
    if special:
        items = [portlet("p-cactions", "General", [
            li("t-specialpages", f"{prefix(path)}special/contents.html", "Contents", "Every page on the wiki"),
            li("t-recentchanges", f"{prefix(path)}special/recent-changes.html", "Recent changes", "Recent changes to the wiki"),
            li("t-print", "#", "Printable version", "Printable version of this page", "p", extra=' data-action="print"'),
        ])]
    else:
        items = [
            portlet("p-cactions", "Actions", [
                li("ca-more-view", "?", "Read", cls="selected vector-more-collapsible-item"),
                li("ca-more-viewsource", "?action=edit", "View source", cls="vector-more-collapsible-item"),
                li("ca-more-history", "?action=history", "View history", cls="vector-more-collapsible-item"),
            ]),
            portlet("p-tb", "General", [
                li("t-whatlinkshere", "?action=whatlinkshere", "What links here", "A list of all wiki pages that link here", "j"),
                li("t-recentchangeslinked", f"{prefix(path)}special/recent-changes.html", "Related changes", "Recent changes across the wiki", "k"),
                li("t-permalink", "#", "Permanent link", "Permanent link to this revision of this page", extra=' data-action="permalink"'),
                li("t-info", "?action=info", "Page information", "More information about this page"),
                li("t-cite", "?action=cite", "Cite this page", "Information on how to cite this page"),
            ]),
            portlet("p-coll-print_export", "Print/export", [
                li("coll-download-as-rl", "#", "Download as PDF", "Download this page as a PDF file", extra=' data-action="print"'),
                li("t-print", "#", "Printable version", "Printable version of this page", "p", extra=' data-action="print"'),
            ]),
        ]
    return ('<div id="vector-page-tools" class="vector-page-tools vector-pinnable-element">\n'
            + pinnable_header("Tools", "page-tools", False) + "\n" + "\n".join(items) + "\n</div>")


def radio_group(name, heading, options, note):
    opts = "\n".join(
        f'  <div class="cdx-radio"><input class="cdx-radio__input" type="radio" name="{name}" id="{name}-{v}" '
        f'value="{v}"><span class="cdx-radio__icon"></span><label for="{name}-{v}" class="cdx-radio__label">{lbl}</label></div>'
        for v, lbl in options)
    return (f'<div class="vector-menu mw-portlet mw-portlet-{name}" data-clientpref="{name}">\n'
            f'<div class="vector-menu-heading">{heading}</div>\n'
            f'<div class="vector-menu-content"><form class="cdx-radio-group">\n{opts}\n</form>\n'
            f'<p class="skin-client-pref-note">{note}</p></div>\n</div>')


def appearance():
    return ('<div id="vector-appearance" class="vector-appearance vector-pinnable-element">\n'
            + pinnable_header("Appearance", "appearance", True) + "\n"
            + radio_group("vector-feature-custom-font-size", "Text",
                          [("0", "Small"), ("1", "Standard"), ("2", "Large")],
                          "This page is always in small font size") + "\n"
            + radio_group("vector-feature-limited-width", "Width",
                          [("1", "Standard"), ("0", "Wide")],
                          "The content is as wide as possible for your browser window.") + "\n"
            + radio_group("skin-theme", "Color <span class=\"skin-beta\">(beta)</span>",
                          [("os", "Automatic"), ("day", "Light"), ("night", "Dark")],
                          "This page is always in light mode.") + "\n</div>")


def search_box(path, sticky=False):
    pf = prefix(path)
    sid = "vector-sticky-search-form" if sticky else "searchform"
    iid = "" if sticky else ' id="searchInput" accesskey="f"'
    return (
        f'<div class="cdx-typeahead-search cdx-typeahead-search--show-thumbnail">\n'
        f'  <form action="{pf}special/search.html" id="{sid}" class="cdx-search-input cdx-search-input--has-end-button">\n'
        f'    <div class="cdx-search-input__input-wrapper">\n'
        f'      <div class="cdx-text-input cdx-text-input--has-start-icon">\n'
        f'        <input class="cdx-text-input__input" type="search" name="search" placeholder="Search {SITENAME}" '
        f'aria-label="Search {SITENAME}" autocapitalize="sentences" autocomplete="off" spellcheck="false" '
        f'title="Search {SITENAME} [f]"{iid}>\n'
        f'        <span class="cdx-text-input__icon cdx-text-input__start-icon"></span>\n'
        f'      </div>\n'
        f'    </div>\n'
        f'    <button class="cdx-button cdx-search-input__end-button">Search</button>\n'
        f'  </form>\n'
        f'</div>')


def header_html(path):
    pf = prefix(path)
    menu = dropdown(
        "vector-main-menu-dropdown",
        icon("menu") + '<span class="vector-dropdown-label-text">Main menu</span>',
        '<div id="vector-main-menu-unpinned-container" class="vector-unpinned-container">\n'
        + main_menu(path) + "\n</div>",
        cls="vector-main-menu-dropdown vector-button-flush-left vector-button-flush-right",
        title="Main menu", label_text="Main menu")
    appear = dropdown(
        "vector-appearance-dropdown",
        icon("appearance") + '<span class="vector-dropdown-label-text">Appearance</span>',
        '<div id="vector-appearance-unpinned-container" class="vector-unpinned-container"></div>',
        cls="vector-appearance-dropdown", title="Change the appearance of the page's font size, width, and color",
        label_text="Appearance")
    return f'''<a class="mw-jump-link" href="#bodyContent">Jump to content</a>
<div class="vector-header-container">
<header class="vector-header mw-header">
<div class="vector-header-start">
<nav class="vector-main-menu-landmark" aria-label="Site">
{menu}
</nav>
<a href="{pf}index.html" class="mw-logo" title="Visit the main page">
  <img class="mw-logo-icon" src="{pf}{LOGO}" alt="" aria-hidden="true" width="50" height="15">
  <span class="mw-logo-container">
    <strong class="mw-logo-wordmark">{SITENAME}</strong>
  </span>
</a>
</div>
<div class="vector-header-end">
<nav class="vector-user-links" aria-label="Personal tools">
<div class="vector-user-links-main">
{appear}
<div id="p-vector-user-menu-preferences" class="vector-menu mw-portlet"><div class="vector-menu-content"><ul class="vector-menu-content-list">
<li id="pt-contact" class="mw-list-item"><a href="{pf}{CONTACT}"><span>Contact</span></a></li>
<li id="pt-team" class="mw-list-item"><a href="{pf}about/team.html"><span>Team</span></a></li>
<li id="pt-website" class="mw-list-item"><a href="{WEBSITE}" class="external"><span>apollyondynamics.com</span></a></li>
</ul></div></div>
</div>
</nav>
</div>
</header>
</div>'''


def titlebar_html(page, special):
    toc_dd = "" if special else dropdown(
        "vector-page-titlebar-toc",
        icon("listBullet") + '<span class="vector-dropdown-label-text">Toggle the table of contents</span>',
        '<div id="vector-page-titlebar-toc-unpinned-container" class="vector-unpinned-container"></div>',
        cls="vector-page-titlebar-toc vector-button-flush-left", title="Toggle the table of contents",
        label_text="Toggle the table of contents")
    nav = f'<nav aria-label="Contents" class="vector-toc-landmark">\n{toc_dd}\n</nav>\n' if toc_dd else ""
    return (f'<header class="mw-body-header vector-page-titlebar">\n{nav}'
            f'<h1 id="firstHeading" class="firstHeading mw-first-heading"><span class="mw-page-title-main">'
            f'{page["title"]}</span></h1>\n</header>')


def indicators_html(special):
    if special:
        return '<div class="mw-indicators"></div>'
    return ('<div class="mw-indicators">\n<div id="mw-indicator-pp-default" class="mw-indicator">'
            '<a href="?action=info#mw-pageinfo-restrictions" title="This article is protected. Its source is kept in the '
            'repository and published by rebuilding the wiki.">'
            '<span class="mw-protection-lock" aria-hidden="true"></span><span class="mw-indicator-label">This article is protected</span>'
            '</a></div>\n</div>')


def toolbar_html(path, special):
    pf = prefix(path)
    self_href = os.path.basename(path)
    tools = dropdown(
        "vector-page-tools-dropdown",
        '<span class="vector-dropdown-label-text">Tools</span>',
        '<div id="vector-page-tools-unpinned-container" class="vector-unpinned-container">\n'
        + page_tools(path, special) + "\n</div>",
        cls="vector-page-tools-dropdown", icon_only=False, label_text="Tools")
    if special:
        left = (f'<li id="ca-nstab-special" class="selected vector-tab-noicon mw-list-item">'
                f'<a href="{self_href}" title="This is a special page, and it cannot be edited"><span>Special page</span></a></li>')
        views = ""
    else:
        left = (f'<li id="ca-nstab-main" class="selected vector-tab-noicon mw-list-item">'
                f'<a href="{self_href}" title="View the content page [c]" accesskey="c"><span>Article</span></a></li>\n'
                f'<li id="ca-talk" class="new vector-tab-noicon mw-list-item">'
                f'<a href="?action=talk" rel="discussion" title="Discussion about the content page (page does not exist) [t]" '
                f'accesskey="t"><span>Talk</span></a></li>')
        views = (f'<nav aria-label="Views">\n<div id="p-views" class="vector-menu vector-menu-tabs mw-portlet">\n'
                 f'<div class="vector-menu-content"><ul class="vector-menu-content-list">\n'
                 f'<li id="ca-view" class="selected vector-tab-noicon mw-list-item"><a href="{self_href}"><span>Read</span></a></li>\n'
                 f'<li id="ca-viewsource" class="vector-tab-noicon mw-list-item"><a href="?action=edit" '
                 f'title="This page is protected.&#10;You can view its source [e]" accesskey="e"><span>View source</span></a></li>\n'
                 f'<li id="ca-history" class="vector-tab-noicon mw-list-item"><a href="?action=history" '
                 f'title="Past revisions of this page [h]" accesskey="h"><span>View history</span></a></li>\n'
                 f'</ul></div>\n</div>\n</nav>\n')
    return f'''<div class="vector-page-toolbar">
<div class="vector-page-toolbar-container">
<div id="left-navigation">
<nav aria-label="Namespaces">
<div id="p-associated-pages" class="vector-menu vector-menu-tabs mw-portlet">
<div class="vector-menu-content"><ul class="vector-menu-content-list">
{left}
</ul></div>
</div>
</nav>
</div>
<div id="right-navigation" class="vector-collapsible">
{views}<nav class="vector-page-tools-landmark" aria-label="Page tools">
{tools}
</nav>
</div>
</div>
</div>'''


def succession_html(path):
    own = path.replace("\\", "/")
    pf = prefix(path)
    idx = next((i for i, (_, _, h) in enumerate(READING_ORDER) if h == own), None)
    if idx is None:
        return ""
    group = READING_ORDER[idx][0]

    def cell(cls, lbl, i):
        if 0 <= i < len(READING_ORDER):
            g, label, href = READING_ORDER[i]
            return (f'<td class="{cls}"><span class="succession-label">{lbl}</span><br>'
                    f'<a href="{pf}{href}">{label}</a><br><small>{g}</small></td>')
        return f'<td class="{cls}"><span class="succession-label">{lbl}</span><br><i>Start of the wiki</i></td>' \
            if i < 0 else f'<td class="{cls}"><span class="succession-label">{lbl}</span><br><i>End of the wiki</i></td>'

    return (f'<table class="wikitable succession-box noprint" role="presentation">\n'
            f'<tbody>\n<tr><th colspan="3" class="succession-header">{SITENAME} reading order</th></tr>\n'
            f'<tr>\n{cell("succession-before", "Preceded&nbsp;by", idx - 1)}\n'
            f'<td class="succession-title"><b>{READING_ORDER[idx][1]}</b><br>'
            f'{group} &middot; {idx + 1} of {len(READING_ORDER)}</td>\n'
            f'{cell("succession-after", "Succeeded&nbsp;by", idx + 1)}\n</tr>\n</tbody>\n</table>')


def navbox_html(path):
    own = path.replace("\\", "/")
    pf = prefix(path)
    rows = []
    for i, (group, links) in enumerate(SIDEBAR_GROUPS):
        items = []
        for label, href in links:
            if href == own:
                items.append(f'<li><a class="mw-selflink selflink">{label}</a></li>')
            else:
                items.append(f'<li><a href="{pf}{href}">{label}</a></li>')
        parity = "odd" if i % 2 == 0 else "even"
        rows.append(f'<tr><th scope="row" class="navbox-group">{group}</th>'
                    f'<td class="navbox-list-with-group navbox-list navbox-{parity} hlist"><div><ul>'
                    + "".join(items) + '</ul></div></td></tr>')
    vte = (f'<div class="navbar plainlinks hlist navbar-mini"><ul>'
           f'<li class="nv-view"><a href="{pf}special/contents.html"><abbr title="View this template">v</abbr></a></li>'
           f'<li class="nv-talk"><a href="{pf}special/recent-changes.html"><abbr title="Discuss this template">t</abbr></a></li>'
           f'<li class="nv-edit"><a href="{pf}special/contents.html"><abbr title="Edit this template">e</abbr></a></li>'
           f'</ul></div>')
    return (f'<div role="navigation" class="navbox" aria-labelledby="{slug(SITENAME)}_navbox">\n'
            f'<table class="nowraplinks mw-collapsible navbox-inner">\n<tbody>\n'
            f'<tr><th scope="col" class="navbox-title" colspan="2">{vte}'
            f'<div id="{slug(SITENAME)}_navbox"><a href="{pf}index.html">{PUBLISHER}</a></div></th></tr>\n'
            + "\n".join(rows) +
            f'\n<tr><td class="navbox-abovebelow" colspan="2"><div>'
            f'<span class="nowrap">{icon("article")} <a href="{pf}special/contents.html">Contents</a></span> &middot; '
            f'<span class="nowrap"><a href="{pf}special/recent-changes.html">Recent changes</a></span> &middot; '
            f'<span class="nowrap"><a href="{pf}special/random.html">Random article</a></span></div></td></tr>\n'
            f'</tbody>\n</table>\n</div>')


def catlinks_html(path):
    pf = prefix(path)
    group = GROUP_OF.get(path.replace("\\", "/"))
    if not group:
        return ""
    return (f'<div id="catlinks" class="catlinks" data-mw="interface"><div id="mw-normal-catlinks" class="mw-normal-catlinks">'
            f'<a href="{pf}special/contents.html" title="Contents">Category</a>: <ul>'
            f'<li><a href="{pf}special/contents.html#{slug(group)}" title="Category:{group}">{group}</a></li>'
            f'</ul></div></div>')


def footer_html(path):
    pf = prefix(path)
    return f'''<div class="mw-footer-container">
<footer id="footer" class="mw-footer">
<ul id="footer-info">
<li id="footer-info-lastmod"></li>
<li id="footer-info-copyright">Published by {PUBLISHER} for investors, evaluators and due-diligence readers. Prices are selling prices; figures marked <i>estimate</i> or <i>claim</i> are not measured results. {REVISION}.</li>
</ul>
<ul id="footer-places">
<li id="footer-places-about"><a href="{pf}about/history.html">About {PUBLISHER}</a></li>
<li id="footer-places-contact"><a href="{pf}{CONTACT}">Contact {PUBLISHER}</a></li>
<li id="footer-places-contents"><a href="{pf}special/contents.html">Contents</a></li>
<li id="footer-places-recentchanges"><a href="{pf}special/recent-changes.html">Recent changes</a></li>
</ul>
<ul id="footer-icons" class="noprint">
<li id="footer-copyrightico"><a href="{WEBSITE}" class="cdx-button cdx-button--fake-button cdx-button--size-large cdx-button--fake-button--enabled"><img src="{pf}{LOGO}" width="44" height="13" alt="" loading="lazy"><span>{PUBLISHER}</span></a></li>
<li id="footer-poweredbyico"><a href="{pf}special/contents.html" class="cdx-button cdx-button--fake-button cdx-button--size-large cdx-button--fake-button--enabled"><span class="mw-powered">Powered by<br><b>site_shell.py</b></span></a></li>
</ul>
</footer>
</div>'''


def sticky_header_html(page, special):
    toc_dd = "" if special else dropdown(
        "vector-sticky-header-toc",
        icon("listBullet") + '<span class="vector-dropdown-label-text">Toggle the table of contents</span>',
        '<div id="vector-sticky-header-toc-unpinned-container" class="vector-unpinned-container"></div>',
        cls="vector-sticky-header-toc vector-button-flush-left", label_text="Toggle the table of contents")
    icons = "" if special else (
        f'<a href="?action=talk" class="cdx-button cdx-button--fake-button cdx-button--weight-quiet cdx-button--icon-only" '
        f'title="Talk" tabindex="-1">{icon("speechBubbles")}<span>Talk</span></a>'
        f'<a href="?action=history" class="cdx-button cdx-button--fake-button cdx-button--weight-quiet cdx-button--icon-only" '
        f'title="View history" tabindex="-1">{icon("history")}<span>View history</span></a>'
        f'<a href="?action=edit" class="cdx-button cdx-button--fake-button cdx-button--weight-quiet cdx-button--icon-only" '
        f'title="View source" tabindex="-1">{icon("wikiText")}<span>View source</span></a>')
    return f'''<div class="vector-header-container vector-sticky-header-container">
<div id="vector-sticky-header" class="vector-sticky-header">
<div class="vector-sticky-header-start">
<div class="vector-sticky-header-context-bar">
<nav aria-label="Contents" class="vector-toc-landmark">{toc_dd}</nav>
<div class="vector-sticky-header-context-bar-primary" aria-hidden="true"><span class="mw-page-title-main">{page["title"]}</span></div>
</div>
</div>
<div class="vector-sticky-header-end" aria-hidden="true">
<div class="vector-sticky-header-icons">{icons}</div>
</div>
</div>
</div>'''


HTML_CLASSES = ("client-nojs vector-feature-language-in-header-enabled vector-feature-custom-font-size-clientpref-1 "
                "vector-feature-limited-width-clientpref-1 vector-feature-main-menu-pinned-clientpref-0 "
                "vector-feature-toc-pinned-clientpref-1 vector-feature-appearance-pinned-clientpref-1 "
                "vector-feature-page-tools-pinned-clientpref-0 vector-feature-page-previews-clientpref-1 "
                "skin-theme-clientpref-day")

# MediaWiki's startup trick: swap client-nojs for client-js and apply the
# reader's saved preferences before first paint, so nothing flashes.
CLIENTPREF_JS = ('<script>(function(){var d=document.documentElement,c=d.className;'
                 'c=c.replace(/(^|\\s)client-nojs(\\s|$)/,"$1client-js$2");'
                 'try{var p=localStorage.getItem("mwclientpreferences");if(p){p.split(",").forEach(function(v){'
                 'var k=v.replace(/-clientpref-\\w+$/,"");if(!/^[\\w-]+$/.test(v))return;'
                 'c=c.replace(new RegExp("(^|\\\\s)"+k+"-clientpref-\\\\w+(?=\\\\s|$)"),"$1"+v);});}}catch(e){}'
                 'd.className=c;})();</script>')


def head_html(page):
    pf = prefix(page["path"])
    title = short_title(page["title_tag"])
    desc = page["description"] or (
        f"{PUBLISHER} engineering wiki — autonomous strike, interception and "
        "battlefield-intelligence systems, with the shared architecture they are built from.")
    return f'''<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} - {SITENAME}</title>
<meta name="description" content="{desc}">
{CLIENTPREF_JS}
<link rel="icon" href="{pf}{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONTS}" rel="stylesheet">
<link rel="stylesheet" href="{pf}css/wiki.css">
<script src="{pf}js/wiki-map-data.js" defer></script>
<script src="{pf}js/wiki.js" defer></script>
</head>'''


def render(page):
    path = page["path"]
    special = path.startswith("special/")
    toc = [] if special else extract_toc(page["article"])
    body_cls = (f"skin--responsive skin-vector skin-vector-2022 mediawiki ltr sitedir-ltr "
                f"{'ns-special' if special else 'ns-0 ns-subject'} page-{slug(short_title(page['title_tag']))} "
                f"action-view")
    toc_col = "" if special else (
        '<div class="vector-sticky-pinned-container">\n<nav id="mw-panel-toc" aria-label="Contents" '
        'class="mw-table-of-contents-container vector-toc-landmark">\n'
        '<div id="vector-toc-pinned-container" class="vector-pinned-container">\n'
        + toc_html(toc) + '\n</div>\n</nav>\n</div>')
    below = "" if special else "\n" + succession_html(path) + "\n" + navbox_html(path) + "\n"
    subtitle = page.get("subtitle", "")
    scripts = (f"\n<!-- page-scripts:start -->\n{page['scripts']}\n<!-- page-scripts:end -->"
               if page.get("scripts") else "")
    html_cls = HTML_CLASSES + (" vector-toc-available" if toc else " vector-toc-not-available")
    return f'''<!DOCTYPE html>
<html class="{html_cls}" lang="en" dir="ltr">
{head_html(page)}
<body id="top" class="{body_cls}" data-page="{esc(path)}">
{header_html(path)}
<div class="mw-page-container">
<div class="mw-page-container-inner">
<div class="vector-sitenotice-container"><div id="siteNotice"></div></div>
<div class="vector-column-start">
<div class="vector-main-menu-container">
<div id="mw-navigation">
<nav id="mw-panel" class="vector-main-menu-landmark" aria-label="Site">
<div id="vector-main-menu-pinned-container" class="vector-pinned-container"></div>
</nav>
</div>
</div>
{toc_col}
</div>
<div class="mw-content-container">
<main id="content" class="mw-body">
{titlebar_html(page, special)}
{toolbar_html(path, special)}
<div class="vector-column-end">
<div class="vector-sticky-pinned-container">
<nav class="vector-page-tools-landmark" aria-label="Page tools">
<div id="vector-page-tools-pinned-container" class="vector-pinned-container"></div>
</nav>
<nav class="vector-appearance-landmark" aria-label="Appearance">
<div id="vector-appearance-pinned-container" class="vector-pinned-container">
{appearance()}
</div>
</nav>
</div>
</div>
<div id="bodyContent" class="vector-body" aria-labelledby="firstHeading">
<div class="vector-body-before-content">
{indicators_html(special)}
<div id="siteSub" class="noprint">{SITESUB}</div>
</div>
<div id="contentSub"><div id="mw-content-subtitle">{subtitle}</div></div>
<div id="mw-content-text" class="mw-body-content">
<div class="mw-content-ltr mw-parser-output" lang="en" dir="ltr">
<!-- article:start -->
{page["article"]}
<!-- article:end -->
{below}</div>
<div class="printfooter">Retrieved from "<a dir="ltr" href="{esc(os.path.basename(path))}">{esc(path)}</a>"</div>
</div>
{"" if special else catlinks_html(path)}
</div>
</main>
</div>
{footer_html(path)}
</div>
</div>
{sticky_header_html(page, special)}{scripts}
</body>
</html>
'''


# ── special pages ────────────────────────────────────────────────────────
SPECIAL_BODY = {
    "search": '<div id="mw-special-root" data-special="search"><p class="mw-special-loading">Searching&hellip;</p>'
              '<noscript><p>Search needs JavaScript. Every page is listed on the <a href="contents.html">Contents</a> page.</p></noscript></div>',
    "recentchanges": '<div id="mw-special-root" data-special="recentchanges"><noscript><p>Recent changes needs JavaScript.</p></noscript></div>',
    "random": '<div id="mw-special-root" data-special="random"><p>Picking a random article&hellip; '
              '<noscript>Random article needs JavaScript; go to the <a href="contents.html">Contents</a>.</noscript></p></div>',
}


def contents_body(pages):
    """Special:Contents — every group, page and section, in reading order.
    Written here so it works without JS; wiki.js adds the filter box."""
    total, secs, groups = 0, 0, []
    for group, links in SIDEBAR_GROUPS:
        items = []
        for label, href in links:
            pg = pages[href]
            toc = extract_toc(pg["article"])
            total += 1
            secs += len(toc)
            desc = tidy(pg.get("subtitle", ""))
            words = " ".join([tidy(label), tidy(pg["title"]), desc] + [t for _, t, _ in toc]).lower()
            sections = "".join(f'<li><a href="../{href}#{esc(i)}">{esc(t)}</a></li>' for i, t, _ in toc)
            items.append(
                f'<li class="mw-contents-page" data-text="{esc(words)}"><a href="../{href}">{label}</a>'
                + (f' <span class="mw-contents-desc">&ndash; {esc(desc)}</span>' if desc else "")
                + (f'<div class="hlist"><ul>{sections}</ul></div>' if sections else "") + "</li>")
        groups.append(f'<div class="mw-contents-group" data-group><h2 id="{slug(group)}">{group} '
                      f'<span class="mw-contents-count">({len(links)})</span></h2>\n'
                      f'<ul class="mw-contents-list">\n' + "\n".join(items) + "\n</ul></div>")
    intro = (f'<p>Every article on {SITENAME}, grouped as in the main menu and listed in reading order, '
             f'with the sections of each: {total} articles, {secs} sections. Articles are also reachable from '
             f'the navigation box at the foot of every page.</p>')
    return f'<div id="mw-special-root" data-special="contents">\n{intro}\n' + "\n".join(groups) + \
        '\n<p class="mw-contents-none" hidden>Nothing matches.</p>\n</div>'


def special_page(path, pages):
    title, title_tag, kind = SPECIAL[path]
    return {
        "path": path, "title": title, "title_tag": title_tag, "subtitle": "",
        "description": f"{title} — {SITENAME}.", "scripts": "",
        "article": contents_body(pages) if kind == "contents" else SPECIAL_BODY[kind],
    }


# ── data: map, search, history ───────────────────────────────────────────
def git(*args):
    try:
        r = subprocess.run(["git", "-C", WIKI, *args], capture_output=True, text=True, check=True)
        return r.stdout
    except (OSError, subprocess.CalledProcessError):
        return ""


def history(paths):
    """{path: [{h, a, d, s, b}, …]} newest first, following renames."""
    out = {}
    for p in paths:
        log = git("log", "--follow", "--format=%x1e%H%x1f%an%x1f%aI%x1f%s", "--name-only", "--", p)
        revs = []
        for chunk in log.split("\x1e")[1:]:
            head, _, names = chunk.partition("\n")
            h, a, d, s = head.split("\x1f")
            name = next((n for n in names.split("\n") if n.strip()), p)
            revs.append({"h": h, "a": a, "d": d, "s": s, "p": name.strip()})
        if revs:
            req = "".join(f'{r["h"]}:{r["p"]}\n' for r in revs)
            sizes = subprocess.run(["git", "-C", WIKI, "cat-file", "--batch-check=%(objectsize)"],
                                   input=req, capture_output=True, text=True).stdout.split("\n")
            for r, size in zip(revs, sizes):
                r["b"] = int(size) if size.strip().isdigit() else None
                del r["p"]
        out[p] = revs
    return out


def page_text_sections(article):
    """[(id, heading, text)] with the lead first."""
    blocks = section_blocks(article)
    lead_end = blocks[0][1] if blocks else len(article)
    out = [("", "", plain(article[:lead_end]))]
    for sid, s, e, a, b in blocks:
        inner = article[a:b]
        h2 = re.search(r"<h2\b[^>]*>(.*?)</h2>", inner, re.S)
        inner = re.sub(r'<div class="sec-tag">.*?</div>', " ", inner, flags=re.S)
        out.append((sid, heading_label(h2.group(1)) if h2 else sid, plain(inner)))
    return out


def extract_of(article, limit=330):
    for p in re.findall(r"<p\b[^>]*>(.*?)</p>", article, re.S):
        t = plain(p)
        if len(t) > 60:
            if len(t) <= limit:
                return t
            cut = t[:limit]
            stop = max(cut.rfind(". "), cut.rfind("; "))
            return (cut[:stop + 1] if stop > 120 else cut.rsplit(" ", 1)[0] + "…").strip()
    return ""


def thumb_of(article):
    m = re.search(r'<img\b[^>]*\bsrc="([^"]+\.(?:jpe?g|png|webp))"', article)
    return m.group(1) if m else ""


def resolve_href(page_path, href):
    href = href.split("#", 1)[0].split("?", 1)[0]
    if not href or re.match(r"^[a-z]+:", href):
        return None
    base = os.path.dirname(page_path)
    return os.path.normpath(os.path.join(base, href)).replace("\\", "/")


def write_if_changed(rel, body):
    path = os.path.join(WIKI, rel)
    old = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
    if body != old:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w", encoding="utf-8").write(body)
        print(f"updated: {rel}")
        return True
    return False


def write_data(pages):
    order = [h for _, _, h in READING_ORDER]
    hist = history(order)
    links = {}
    for p in order:
        art = pages[p]["article"]
        for href in re.findall(r'href="([^"]+)"', art):
            t = resolve_href(p, href)
            if t and t != p and t in pages:
                links.setdefault(t, [])
                if p not in links[t]:
                    links[t].append(p)
    groups = []
    for group, entries in SIDEBAR_GROUPS:
        items = []
        for label, href in entries:
            pg = pages[href]
            art = pg["article"]
            thumb = thumb_of(art)
            if thumb:
                thumb = resolve_href(href, thumb)
            text = plain(art)
            items.append({
                "title": tidy(label),
                "href": href,
                "heading": tidy(pg["title"]),
                "description": tidy(pg.get("subtitle", "")),
                "extract": extract_of(art),
                "thumb": thumb or "",
                "sections": [{"id": s, "label": l, "subs": [{"id": h, "label": t} for h, t in subs]}
                             for s, l, subs in extract_toc(art)],
                "words": len(text.split()),
                "bytes": len(pg["html"].encode("utf-8")),
                "lastmod": hist[href][0]["d"] if hist.get(href) else "",
                "links": links.get(href, []),
            })
        groups.append({"name": group, "slug": slug(group), "pages": items})
    note = "/* Generated by scripts/site_shell.py from the pages on disk. Do not edit by hand. */\n"
    write_if_changed("js/wiki-map-data.js", note + "window.WIKI_MAP = " +
                     json.dumps({"site": SITENAME, "groups": groups}, ensure_ascii=False, indent=1) + ";\n")

    search = []
    for href in order:
        pg = pages[href]
        search.append({"href": href, "title": tidy(pg["title"]),
                       "sections": [{"id": i, "h": h, "t": t} for i, h, t in page_text_sections(pg["article"])]})
    write_if_changed("js/wiki-search-data.js", note + "window.WIKI_SEARCH = " +
                     json.dumps(search, ensure_ascii=False, separators=(",", ":")) + ";\n")
    write_if_changed("js/wiki-history-data.js", note + "window.WIKI_HISTORY = " +
                     json.dumps(hist, ensure_ascii=False, separators=(",", ":")) + ";\n")


# ── main ─────────────────────────────────────────────────────────────────
def article_pages():
    for root, dirs, files in os.walk(WIKI):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and d != "special")
        for f in sorted(files):
            if f.endswith(".html"):
                full = os.path.join(root, f)
                yield os.path.relpath(full, WIKI).replace("\\", "/"), full


def main():
    check = "--check" in sys.argv
    changed = 0
    pages = {}
    for rel, full in article_pages():
        html = open(full, encoding="utf-8").read()
        page = parse_page(rel, html)
        page["path"] = rel
        page["article"] = ensure_h3_ids(page["article"])
        new = render(page)
        page["html"] = new
        pages[rel] = page
        if new != html:
            changed += 1
            if check:
                print(f"needs update: {rel}")
            else:
                open(full, "w", encoding="utf-8").write(new)
                print(f"updated: {rel}")
    missing = [h for _, _, h in READING_ORDER if h not in pages]
    if missing:
        raise SystemExit(f"SIDEBAR_GROUPS names missing pages: {missing}")
    if not check:
        for sp in SPECIAL:
            if write_if_changed(sp, render(special_page(sp, pages))):
                changed += 1
        write_data(pages)
    print(f"\n{changed} page(s) {'would change' if check else 'updated'}.")


if __name__ == "__main__":
    main()
