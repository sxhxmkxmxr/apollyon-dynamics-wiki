#!/usr/bin/env python3
"""
gen_visuals.py — every chart and diagram on the Apollyon wiki.

Design language: black ground, bone ink, one signal red, hairline rules,
mono labels. No gradients, no shadows, no rounded corners.

Text is budgeted: every label is fitted to the space it sits in, and
multi-line prose is wrapped, so nothing overruns a box or collides.

Outputs:
  wiki/assets/<name>.svg      — standalone files
  wiki/assets/visuals.json    — {name: "<svg>…</svg>"} for inline builders
"""
import html
import json
import math
import os

WIKI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(WIKI, "assets")

BG = "#050505"
INK = "#F2EFE9"
INK2 = "#C7C4BD"
INK3 = "#A19E97"
INK4 = "#7F7C76"
LINE = "#1D1D1D"
LINE2 = "#2B2B2B"
LINE3 = "#414141"
RED = "#D92323"
RED2 = "#F04B4B"
RED_W = "#3A1212"

MONO = "JetBrains Mono, ui-monospace, monospace"
SANS = "Inter, Helvetica Neue, sans-serif"

CW = {MONO: 0.62, SANS: 0.53}          # width of one character per px of size


def esc(s):
    return html.escape(str(s), quote=True)


def charw(size, fam):
    return size * CW[fam]


def fit(s, maxw, size, fam=MONO, min_size=6.2):
    """Return [(text, size), ...] that fits maxw. Sshrinks, then splits at a space."""
    if not s:
        return [("", size)]
    if len(s) * charw(size, fam) <= maxw:
        return [(s, size)]
    for factor in (0.94, 0.88, 0.82, 0.76, 0.7):
        sz = size * factor
        if len(s) * charw(sz, fam) <= maxw and sz >= min_size:
            return [(s, sz)]
    words = s.split()
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        if len(a) * charw(size, fam) <= maxw and len(b) * charw(size, fam) <= maxw:
            return [(a, size), (b, size)]
    sz = max(min_size, maxw / (len(s) * CW[fam]))
    return [(s, sz)]


def txt(x, y, s, size=10.5, fill=INK3, fam=MONO, anchor="start", weight=None, ls=None):
    a = f'font-family="{fam}" font-size="{size:.1f}" fill="{fill}"'
    if anchor != "start":
        a += f' text-anchor="{anchor}"'
    if weight:
        a += f' font-weight="{weight}"'
    if ls:
        a += f' letter-spacing="{ls}"'
    return f'<text x="{x:.1f}" y="{y:.1f}" {a}>{esc(s)}</text>'


def wrap(x, y, s, maxw, size, fill=INK3, fam=SANS, lh=None, weight=None, anchor="start"):
    """Wrapped paragraph. Returns svg for as many lines as needed."""
    lh = lh or size * 1.45
    words, lines, cur = s.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if cur and len(trial) * charw(size, fam) > maxw:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return "".join(txt(x, y + i * lh, ln, size, fill, fam, anchor=anchor, weight=weight) for i, ln in enumerate(lines))


def rect(x, y, w, h, stroke=LINE, fill="none", sw=1, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>'


def line(x1, y1, x2, y2, stroke=LINE2, sw=1, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"{d}/>'


def defs_arrow(ns, colors=None):
    colors = colors or {"ink": INK2, "red": RED2, "grey": LINE3}
    m = []
    for key, col in colors.items():
        m.append(
            f'<marker id="{ns}-{key}" viewBox="0 0 8 8" refX="6.4" refY="4" '
            f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0.6 L7.4,4 L0,7.4 z" fill="{col}"/></marker>'
        )
    return "<defs>" + "".join(m) + "</defs>"


def arrow(x1, y1, x2, y2, ns, color="ink", sw=1.1, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    stroke = {"ink": INK2, "red": RED2, "grey": LINE3}[color]
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" '
            f'stroke-width="{sw}"{d} marker-end="url(#{ns}-{color})"/>')


def poly(points, stroke=INK2, fill="none", sw=1.2, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    return f'<polyline points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>'


def steps(points, stroke=RED2, sw=1.6):
    out = []
    for i in range(1, len(points)):
        (x0, y0), (x1, y1) = points[i - 1], points[i]
        out.append(f'<path d="M{x0:.1f},{y0:.1f} H{x1:.1f} V{y1:.1f}" fill="none" stroke="{stroke}" stroke-width="{sw}"/>')
    return "".join(out)


def dot(x, y, r=4, fill=RED, stroke=None, sw=1):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}"{s}/>'


def sq(x, y, s=7, fill="none", stroke=INK4, sw=1.2):
    return rect(x - s / 2, y - s / 2, s, s, stroke=stroke, fill=fill, sw=sw)


def lg(v, a, b):
    return (math.log10(v) - math.log10(a)) / (math.log10(b) - math.log10(a))


def panel_box(x, y, w, h, label, sub=None, stroke=LINE3, fill=BG, sw=1,
              tcol=INK2, size=10.5, sub_size=8.6, lh=None, scol=None, pad=16):
    """A box whose label and sub-label are guaranteed to fit inside it."""
    out = [rect(x, y, w, h, stroke=stroke, fill=fill, sw=sw)]
    inner = w - pad
    sub_color = scol or INK3
    if sub:
        label_lines = fit(label, inner, size, MONO)
        sub_lines = fit(sub, inner, sub_size, MONO)
        block_h = len(label_lines) * (size + 1.5) + len(sub_lines) * (sub_size + 2.5) + 1
        cy = y + h / 2 - block_h / 2
        for ln, sz in label_lines:
            cy += sz + 1.5
            out.append(txt(x + w / 2, cy - 1.5, ln, sz, tcol, MONO, anchor="middle", weight=600))
            cy += 0
        cy += 2
        for ln, sz in sub_lines:
            cy += sz + 2.5
            out.append(txt(x + w / 2, cy - 2.5, ln, sz, sub_color, MONO, anchor="middle"))
    else:
        lines = fit(label, inner, size, MONO)
        lh = lh or size + 3
        top = y + h / 2 - (len(lines) - 1) * lh / 2
        for i, (ln, sz) in enumerate(lines):
            out.append(txt(x + w / 2, top + i * lh + sz * 0.36, ln, sz, tcol, MONO, anchor="middle", weight=600))
    return "".join(out)


# ══════════════════════════════════════════════════════════════════════
# 1 · THE WAR CHANGED SHAPE — four inversions + the exchange rate
# ══════════════════════════════════════════════════════════════════════
def war_inversions():
    W, H = 1000, 560
    ns = "wi"
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="Four inversions of modern warfare and the exchange rate between interceptors and strike rounds">',
         defs_arrow(ns, {"ink": INK4, "red": RED2, "grey": LINE3})]

    o.append(txt(40, 30, "THEN", 9.5, INK4, MONO, ls="0.18em"))
    o.append(txt(552, 30, "NOW", 9.5, RED2, MONO, ls="0.18em"))
    o.append(line(40, 40, 960, 40, LINE2))

    rows = [
        ("01", "PLATFORM",
         "Manned and exquisite. A single sortie costs more than the target it services, and the pilot cannot be replaced.",
         "Autonomous and attritable. The machine goes first, at a unit cost that permits it to be lost."),
        ("02", "INVENTORY",
         "Stockpiles of a few hundred. A real campaign empties the magazine within weeks.",
         "Production of thousands. Output rate becomes a performance parameter, alongside range and speed."),
        ("03", "SPECTRUM",
         "Permissive GNSS. Precision depends on satellite signals the adversary can deny at will.",
         "Contested and denied. Navigation falls back on inertial, terrain and optical references."),
        ("04", "EXCHANGE",
         "The defender fires an ₹18–35 crore interceptor at whatever arrives.",
         "A ₹15–35 lakh strike round arrives instead. The exchange now bankrupts the defence."),
    ]
    y = 74
    for no, label, then, now in rows:
        o.append(txt(40, y + 4, no, 10, RED2, MONO, weight=700))
        o.append(txt(72, y + 4, label, 10.5, INK, MONO, weight=700, ls="0.12em"))
        o.append(wrap(72, y + 30, then, 400, 12.5, INK3, SANS, lh=17))
        o.append(line(72, y + 60, 468, y + 60, LINE))
        o.append(arrow(492, y + 22, 532, y + 22, ns, "red", 1.4))
        o.append(wrap(552, y + 30, now, 398, 13, INK, SANS, lh=18, weight=600))
        y += 88

    gy = 432
    o.append(line(40, gy - 26, 960, gy - 26, LINE2))
    o.append(txt(40, gy - 8, "THE EXCHANGE RATE", 10.5, RED2, MONO, weight=700, ls="0.12em"))
    cells = []
    cs = 10
    for i in range(10):
        for j in range(10):
            fill = RED if (i, j) == (0, 0) else "none"
            cells.append(rect(40 + i * cs, gy + 6 + j * cs, cs - 1, cs - 1, stroke=LINE2, fill=fill))
    o.append("".join(cells))
    o.append(txt(170, gy + 22, "= 100 attritable strike rounds", 12.5, INK, SANS, weight=600))
    o.append(wrap(170, gy + 44, "bought for the price of one air-defence interceptor. A defence built on expensive "
                                "interceptors loses the arithmetic before it loses the battle.", 420, 11.5, INK3, SANS, lh=16))
    o.append(txt(660, gy + 22, "RATIO ≈ 50–200 : 1", 10, INK4, MONO, ls="0.1em"))
    o.append(wrap(660, gy + 44, "depending on the pairing. The interceptor is not the only party losing this "
                                "exchange — national magazines are finite too.", 300, 10.5, INK4, MONO, lh=15))
    o.append("</svg>")
    return "".join(o)


# ══════════════════════════════════════════════════════════════════════
# 2 · COST PER KG·KM — envelope against in-service comparators
# ══════════════════════════════════════════════════════════════════════
def cost_curve():
    W, H = 1000, 570
    L, R, T, B = 96, 930, 88, 462
    xmin, xmax = 100, 2200
    ymin, ymax = 10, 10000

    def X(v):
        return L + lg(v, xmin, xmax) * (R - L)

    def Y(v):
        return B - lg(v, ymin, ymax) * (B - T)

    o = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" '
        f'aria-label="Cost per kilogram-kilometre by range: Apollyon family against in-service comparators">',
        f'<rect width="{W}" height="{H}" fill="{BG}"/>'
    ]

    # Minor log ticks & faint grid
    for gv in [20, 30, 40, 50, 60, 70, 80, 90, 200, 300, 400, 500, 600, 700, 800, 900, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000]:
        y = Y(gv)
        if gv in (50, 500, 5000):
            o.append(line(L, y, R, y, "#161f30", 0.8, "3,4"))
        o.append(line(L - 4, y, L, y, "#334155", 0.8))

    # Major horizontal gridlines and Y tick labels
    for gv, lbl in [(10, "₹10"), (100, "₹100"), (1000, "₹1,000"), (10000, "₹10,000")]:
        y = Y(gv)
        o.append(line(L, y, R, y, "#232d42", 1))
        o.append(line(L - 7, y, L, y, "#475569", 1.2))
        o.append(txt(L - 12, y + 4, lbl, 10.5, "#cbd5e1", MONO, anchor="end", weight=600))

    # Minor X ticks
    for gv in [200, 400, 600, 700, 800, 1200, 1800]:
        x = X(gv)
        o.append(line(x, B, x, B + 4, "#334155", 0.8))

    # Major vertical gridlines and X tick labels
    for gv, lbl in [(150, "150"), (300, "300"), (500, "500"), (1000, "1,000"), (1500, "1,500"), (2000, "2,000")]:
        x = X(gv)
        o.append(line(x, T, x, B, "#1e293b", 1))
        o.append(line(x, B, x, B + 6, "#475569", 1.2))
        o.append(txt(x, B + 22, lbl, 10.5, "#cbd5e1", MONO, anchor="middle", weight=600))

    # Axis spines
    o.append(line(L, B, R, B, "#475569", 1.2))
    o.append(line(L, T, L, B, "#475569", 1.2))

    # Header directives
    o.append(txt(L, 44, "LOWER IS BETTER ↓", 10.5, "#38bdf8", MONO, weight=700, ls="0.08em"))
    o.append(txt(L + 155, 44, "·   UNIT COST ÷ (PAYLOAD × RANGE)", 10, "#94a3b8", MONO, ls="0.08em"))
    o.append(txt((L + R) / 2, B + 48, "OPERATIONAL RANGE, KM (LOG SCALE)", 9.5, "#94a3b8", MONO, anchor="middle", ls="0.12em", weight=600))
    o.append(txt(L - 12, T - 16, "COST PER KG·KM (INR)", 9.5, "#94a3b8", MONO, ls="0.12em", weight=600))

    # Comparators in service
    comps = [
        ("Berkut-BM", 150, 4500),
        ("Barracuda-250", 380, 3200),
        ("Barracuda-500", 900, 500),
        ("Tomahawk", 1600, 480),
    ]
    c_pts = [(X(r), Y(c)) for _, r, c in comps]
    pts_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in c_pts)
    o.append(f'<polyline points="{pts_str}" fill="none" stroke="#64748b" stroke-width="1.8" stroke-dasharray="6,4" stroke-linecap="round" stroke-linejoin="round"/>')

    for name, r, c in comps:
        x, y = X(r), Y(c)
        o.append(line(x, y - 8, x, y - 5.5, "#64748b", 1))
        o.append(txt(x, y - 24, name, 11.5, "#e2e8f0", MONO, anchor="middle", weight=600))
        o.append(txt(x, y - 11, f"₹{c:,}", 10.5, "#94a3b8", MONO, anchor="middle"))
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.5" fill="{BG}" stroke="#94a3b8" stroke-width="2"/>')

    # Apollyon long-range strike family
    fam = [
        ("Nightshade Mk II", 300, 2600),
        ("Nightshade Mk III", 500, 1700),
        ("Hemlock Mk I", 1000, 350),
        ("Hemlock Mk II", 1500, 35),
    ]
    f_pts = [(X(r), Y(c)) for _, r, c in fam]
    pts_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in f_pts)
    o.append(f'<polyline points="{pts_str}" fill="none" stroke="rgba(255, 59, 48, 0.22)" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>')
    o.append(f'<polyline points="{pts_str}" fill="none" stroke="#ff3b30" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>')

    # Mk II: left
    x2, y2 = X(300), Y(2600)
    o.append(line(379, 160.9, 386.6, 160.9, "#f87171", 1))
    o.append(txt(376, 156, "Nightshade Mk II", 12, "#ffffff", MONO, anchor="end", weight=700))
    o.append(txt(376, 171, "₹2,600 / kg·km", 10.5, "#fca5a5", MONO, anchor="end", weight=500))
    o.append(f'<circle cx="{x2:.1f}" cy="{y2:.1f}" r="{5.8}" fill="#ff3b30" stroke="#ffffff" stroke-width="1.6"/>')

    # Mk III: left-below
    x3, y3 = X(500), Y(1700)
    o.append(line(518, 204, 525, 189, "#f87171", 1))
    o.append(txt(514, 210, "Nightshade Mk III", 12, "#ffffff", MONO, anchor="end", weight=700))
    o.append(txt(514, 225, "₹1,700 / kg·km", 10.5, "#fca5a5", MONO, anchor="end", weight=500))
    o.append(f'<circle cx="{x3:.1f}" cy="{y3:.1f}" r="{5.8}" fill="#ff3b30" stroke="#ffffff" stroke-width="1.6"/>')

    # Hemlock Mk I: right
    x1, y1 = X(1000), Y(350)
    o.append(line(723.1, 269.5, 728, 269.5, "#f87171", 1))
    o.append(txt(732, 266, "Hemlock Mk I", 12, "#ffffff", MONO, anchor="start", weight=700))
    o.append(txt(732, 280, "₹350 / kg·km", 10.5, "#fca5a5", MONO, anchor="start", weight=500))
    o.append(f'<circle cx="{x1:.1f}" cy="{y1:.1f}" r="{5.8}" fill="#ff3b30" stroke="#ffffff" stroke-width="1.6"/>')

    # Hemlock Mk II: left
    xh2, yh2 = X(1500), Y(35)
    o.append(line(814, 394.2, 820.9, 394.2, "#f87171", 1))
    o.append(txt(810, 398, "Hemlock Mk II", 12, "#ffffff", MONO, anchor="end", weight=700))
    o.append(txt(810, 413, "₹35 / kg·km", 10.5, "#fca5a5", MONO, anchor="end", weight=500))
    o.append(txt(810, 430, "about 14× below Tomahawk", 11, "#ff453a", MONO, anchor="end", weight=700))
    o.append(f'<circle cx="{xh2:.1f}" cy="{yh2:.1f}" r="{5.8}" fill="#ff3b30" stroke="#ffffff" stroke-width="1.6"/>')

    # Legend
    o.append(line(694, 44, 718, 44, "#64748b", 1.8, "4,3"))
    o.append(f'<circle cx="706" cy="44" r="5" fill="{BG}" stroke="#94a3b8" stroke-width="1.8"/>')
    o.append(txt(726, 47.5, "IN SERVICE", 9.5, "#cbd5e1", MONO, weight=600))

    o.append(line(816, 44, 840, 44, "#ff3b30", 2.5))
    o.append('<circle cx="828" cy="44" r="5.2" fill="#ff3b30" stroke="#ffffff" stroke-width="1.4"/>')
    o.append(txt(848, 47.5, "APOLLYON", 9.5, "#ffffff", MONO, weight=700))

    # Footnote
    o.append(txt(L, 524, "USD 1 = INR 95 · Comparator prices from public sources · Berkut-BM unit cost estimated", 9.5, "#64748b", MONO))
    o.append("</svg>")
    return "".join(o)


# ══════════════════════════════════════════════════════════════════════
# 3 · THE FAMILY — strike envelope by generation
# ══════════════════════════════════════════════════════════════════════
def strike_family():
    W, H = 1000, 580
    L, R, T, B = 100, 900, 75, 320

    def X(i):
        return L + i * (R - L) / 4

    def Y(v):
        return B - lg(v, 10, 3000000) * (B - T)

    fam = [
        ("NIGHTSHADE MK I", 20, ["GNSS-Only", "Proof of Concept"], "20 km range · No warhead", "650 km/h flight test"),
        ("NIGHTSHADE MK II", 4500, ["One-Way Effector", "+ Target Drone"], "15 kg warhead · 300 km", "700 km/h terminal dive"),
        ("NIGHTSHADE MK III", 12500, ["Long-Range", "One-Way Effector"], "25 kg warhead · 500 km", "800 km/h terminal dive"),
        ("HEMLOCK MK I", 75000, ["Miniature", "Cruise Missile"], "75 kg warhead · 1,000 km", "900 km/h high-subsonic"),
        ("HEMLOCK MK II", 1500000, ["Long-Range", "Cruise Missile"], "1,000 kg · 1,500 km", "900 km/h high-subsonic"),
    ]
    years = ["FLOWN 2026", "2027", "2028", "2029", "2030–31"]

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="Strike envelope by generation: Nightshade Mk I to Hemlock Mk II">']
    o.append(txt(L - 30, 32, "STRIKE ENVELOPE — PAYLOAD × RANGE (KG·KM, LOG SCALE)", 11, INK3, MONO, ls="0.12em"))

    for gv in (10, 100, 1000, 10000, 100000, 1000000):
        y = Y(gv)
        o.append(line(L - 10, y, R + 10, y, LINE))
        label = {10: "10", 100: "100", 1000: "1K", 10000: "10K", 100000: "100K", 1000000: "1M"}[gv]
        o.append(txt(L - 18, y + 4, label, 11, INK4, MONO, anchor="end"))

    pts = [(X(i), Y(e)) for i, (_, e, _, _, _) in enumerate(fam)]
    o.append(steps(pts, RED2, 2.2))
    o.append(line(L - 20, B, R + 20, B, LINE2, sw=1.2))

    for i, ((name, env, role_lines, spec_pld, spec_spd), (x, y)) in enumerate(zip(fam, pts)):
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{RED}" stroke="#FFFFFF" stroke-width="1.6"/>')
        o.append(txt(x, y - 14, f"{env:,}", 15, "#FFFFFF", MONO, anchor="middle", weight=800))
        o.append(txt(x, 54, name, 12, "#FFFFFF", MONO, anchor="middle", weight=700, ls="0.06em"))

        if i < len(fam) - 1:
            sep_x = (x + pts[i+1][0]) / 2
            o.append(line(sep_x, B + 10, sep_x, 505, stroke="#1C1C1C", sw=1, dash="3,3"))

        yr = years[i]
        if i == 0:
            o.append(f'<rect x="{x - 54:.1f}" y="{B + 16}" width="108" height="24" fill="{RED}" rx="3"/>')
            o.append(txt(x, B + 33, yr, 11.5, "#FFFFFF", MONO, anchor="middle", weight=800, ls="0.08em"))
        else:
            o.append(f'<rect x="{x - 46:.1f}" y="{B + 16}" width="92" height="24" fill="#161616" stroke="#333333" rx="3"/>')
            o.append(txt(x, B + 33, yr, 11.5, "#FFFFFF", MONO, anchor="middle", weight=700, ls="0.08em"))

        for r_idx, r_line in enumerate(role_lines):
            o.append(txt(x, B + 64 + r_idx * 18, r_line, 14, "#FFFFFF", SANS, anchor="middle", weight=700))

        o.append(txt(x, B + 116, spec_pld, 12.5, "#E2DFD8", MONO, anchor="middle", weight=600))
        o.append(txt(x, B + 136, spec_spd, 12, INK3, MONO, anchor="middle"))

    o.append(line(L - 20, B + 155, R + 20, B + 155, LINE2))
    o.append(txt(L - 20, B + 178, "Mk I carries no payload and does not run the shared core; every system above it inherits it.", 13, INK3, MONO))
    o.append("</svg>")
    return "".join(o)


# ══════════════════════════════════════════════════════════════════════
# 4 · VELOCITY — the Ahuti speed staircase
# ══════════════════════════════════════════════════════════════════════
def ahuti_speed():
    W, H = 1000, 430
    ns = "as"
    L, R, T, B = 90, 930, 70, 330
    ymin, ymax = 0, 560

    def X(i):
        return L + i * (R - L) / 4

    def Y(v):
        return B - (v - ymin) / (ymax - ymin) * (B - T)

    speeds = [180, 282, 337, 352, 498]
    labels = ["BUILD 1", "BUILD 2", "BUILD 3", "BUILD 4", "MK II"]
    dates = ["LATE 2025", "Q1 2026", "Q2 2026", "Q3 2026", "SEP 2026"]

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="Ahuti interceptor top speed across four build standards in eight months">']

    for gv in (0, 100, 200, 300, 400, 500):
        y = Y(gv)
        o.append(line(L, y, R, y, LINE if gv else LINE2))
        o.append(txt(L - 14, y + 4, f"{gv}", 10, INK4, MONO, anchor="end"))
    o.append(txt(L - 14, T - 16, "TOP SPEED (KM/H)", 9.5, INK4, MONO, ls="0.12em"))

    ty = Y(400)
    o.append(line(L, ty, R, ty, RED_W, 1.2, dash="5 5"))
    o.append(txt(L + 4, ty - 8, "JET GERAN THREAT BAND ≈ 400", 9.5, RED2, MONO, ls="0.08em"))

    pts = [(X(i), Y(v)) for i, v in enumerate(speeds)]
    o.append(poly(pts, RED2, sw=1.8))
    for i, (x, y) in enumerate(pts):
        o.append(dot(x, y, 5, RED))
        o.append(txt(x, y - 16, f"{speeds[i]}", 13, INK, MONO, anchor="middle", weight=700))
        o.append(txt(x, B + 26, labels[i], 10, INK, MONO, anchor="middle", weight=700, ls="0.1em"))
        o.append(txt(x, B + 44, dates[i], 9.5, INK4, MONO, anchor="middle"))
    o.append(line(L, B, R, B, LINE2))
    o.append(txt(L, 396, "Five flight standards in eight months · certified national record, India Book of Records,", 10, INK4, MONO))
    o.append(txt(L, 414, "1 Sep 2026 · 400 km/h is the target threat envelope used to drive the programme.", 10, INK4, MONO))
    o.append("</svg>")
    return "".join(o)


# ══════════════════════════════════════════════════════════════════════
# 5/6 · INDIA — production and exports
# ══════════════════════════════════════════════════════════════════════
def india_production():
    W, H = 1000, 520
    L, R, T, B = 72, 928, 140, 380
    years = ["FY21", "FY22", "FY23", "FY24", "FY25", "FY26"]
    vals = [84643, 94846, 106000, 127000, 151000, 178000]
    top = 200000
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="India annual defence production FY21 to FY26 in crore rupees">']
    o.append(txt(L - 10, 46, "ANNUAL DEFENCE PRODUCTION", 19, INK, MONO, weight=700, ls="0.08em"))
    o.append(txt(R + 10, 46, "₹ LAKH CRORE", 17, INK3, MONO, anchor="end", ls="0.08em"))
    o.append(line(L - 10, 66, R + 10, 66, LINE))

    bw = (R - L) / len(vals) * 0.56
    for i, (yr, v) in enumerate(zip(years, vals)):
        cx = L + (i + 0.5) * (R - L) / len(vals)
        h = (v / top) * (B - T)
        first = i == 0
        last = i == len(vals) - 1
        if last:
            o.append(rect(cx - bw / 2, B - h, bw, h, stroke=RED2, fill=RED, sw=1.5))
            o.append(f'<rect x="{cx - 84:.1f}" y="70" width="168" height="34" fill="{RED}" rx="4"/>')
            o.append(txt(cx, 93, "▲ 4.1× GROWTH", 18, "#FFFFFF", MONO, anchor="middle", weight=800, ls="0.08em"))
            o.append(txt(cx, 136, "₹1.78L Cr", 34, "#FFFFFF", MONO, anchor="middle", weight=800))
            o.append(txt(cx, 412, yr, 19, "#FFFFFF", MONO, anchor="middle", weight=700))
        elif first:
            o.append(rect(cx - bw / 2, B - h, bw, h, stroke="#666666", fill="#222222", sw=1.5))
            o.append(f'<rect x="{cx - 65:.1f}" y="70" width="130" height="34" fill="#181818" stroke="#444444" stroke-width="1.2" rx="4"/>')
            o.append(txt(cx, 92, "START · BASE", 15, INK3, MONO, anchor="middle", weight=700, ls="0.08em"))
            o.append(txt(cx, 136, "₹85K Cr", 34, "#FFFFFF", MONO, anchor="middle", weight=800))
            o.append(f'<line x1="{cx:.1f}" y1="148" x2="{cx:.1f}" y2="{B - h - 4:.1f}" stroke="#444444" stroke-width="1.2" stroke-dasharray="3,3"/>')
            o.append(txt(cx, 412, yr, 19, "#FFFFFF", MONO, anchor="middle", weight=700))
        else:
            o.append(rect(cx - bw / 2, B - h, bw, h, stroke="#2A2A2A", fill="#141414", sw=1))
            o.append(txt(cx, B - h - 10, f"₹{v/1000:.0f}K", 12.5, "#666666", MONO, anchor="middle"))
            o.append(txt(cx, 410, yr, 13, "#666666", MONO, anchor="middle"))

    o.append(line(L - 10, B, R + 10, B, LINE2, sw=1.2))
    o.append(txt(L - 10, 458, "4.1× since FY14 (₹43,746 Cr) · FY26 total ₹1.78 lakh Cr", 16, INK2, MONO, weight=500))
    o.append(txt(L - 10, 486, "75% of FY27 capital acquisition reserved for domestic industry (₹1.39 lakh Cr).", 15, INK4, MONO))
    o.append("</svg>")
    return "".join(o)


def india_exports():
    W, H = 1000, 520
    L, R, T, B = 72, 928, 140, 380
    years = ["FY14", "FY21", "FY22", "FY23", "FY24", "FY25", "FY26"]
    vals = [686, 8434, 12815, 15920, 21083, 23622, 38424]
    top = 44000
    n = len(vals)
    bw = (R - L) / n * 0.52
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="India defence exports FY14 to FY26 in crore rupees">']
    o.append(txt(L - 10, 46, "ANNUAL DEFENCE EXPORTS", 19, INK, MONO, weight=700, ls="0.08em"))
    o.append(txt(R + 10, 46, "₹ CRORE", 17, INK3, MONO, anchor="end", ls="0.08em"))
    o.append(line(L - 10, 66, R + 10, 66, LINE))

    for i, (yr, v) in enumerate(zip(years, vals)):
        cx = L + (i + 0.5) * (R - L) / n
        h = max(4.0, (v / top) * (B - T))
        last = i == n - 1
        first = i == 0
        if last:
            o.append(rect(cx - bw / 2, B - h, bw, h, stroke=RED2, fill=RED, sw=1.5))
            o.append(f'<rect x="{cx - 84:.1f}" y="70" width="168" height="34" fill="{RED}" rx="4"/>')
            o.append(txt(cx, 93, "▲ 56× GROWTH", 18, "#FFFFFF", MONO, anchor="middle", weight=800, ls="0.08em"))
            o.append(txt(cx, 136, "₹38,424 Cr", 34, "#FFFFFF", MONO, anchor="middle", weight=800))
            o.append(txt(cx, 412, yr, 19, "#FFFFFF", MONO, anchor="middle", weight=700))
        elif first:
            o.append(rect(cx - bw / 2, B - h, bw, h, stroke="#666666", fill="#222222", sw=1.5))
            o.append(f'<rect x="{cx - 65:.1f}" y="70" width="130" height="34" fill="#181818" stroke="#444444" stroke-width="1.2" rx="4"/>')
            o.append(txt(cx, 92, "START · BASE", 15, INK3, MONO, anchor="middle", weight=700, ls="0.08em"))
            o.append(txt(cx, 136, "₹686 Cr", 34, "#FFFFFF", MONO, anchor="middle", weight=800))
            o.append(f'<line x1="{cx:.1f}" y1="148" x2="{cx:.1f}" y2="{B - h - 4:.1f}" stroke="#444444" stroke-width="1.2" stroke-dasharray="3,3"/>')
            o.append(txt(cx, 412, yr, 19, "#FFFFFF", MONO, anchor="middle", weight=700))
        else:
            label = f"₹{v:,}"
            o.append(rect(cx - bw / 2, B - h, bw, h, stroke="#2A2A2A", fill="#141414", sw=1))
            o.append(txt(cx, B - h - 10, label, 12, "#666666", MONO, anchor="middle"))
            o.append(txt(cx, 410, yr, 13, "#666666", MONO, anchor="middle"))

    o.append(line(L - 10, B, R + 10, B, LINE2, sw=1.2))
    o.append(txt(L - 10, 458, "56× since FY14 · ₹38,424 Cr in FY26 · private firms 45.16% of exports", 16, INK2, MONO, weight=500))
    o.append(txt(L - 10, 486, "across 145 domestic firms and more than 80 destination nations.", 15, INK4, MONO))
    o.append("</svg>")
    return "".join(o)


# ══════════════════════════════════════════════════════════════════════
# 7 · VEHICLE HARDWARE ARCHITECTURE — functional view
# ══════════════════════════════════════════════════════════════════════
def arch_vehicle():
    W, H = 1000, 620
    ns = "av"
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="Core vehicle architecture: navigation and sensing, flight control, propulsion, actuation and power">',
         defs_arrow(ns, {"ink": INK2, "red": RED2, "grey": LINE3})]

    o.append(panel_box(70, 30, 150, 36, "POWER UNIT", size=10))
    o.append(line(220, 48, 930, 48, LINE3, 1.4))
    o.append(txt(300, 40, "POWER RAIL", 9, INK4, MONO, ls="0.14em"))
    for dx in (300, 505, 815, 900):
        o.append(line(dx, 48, dx, 86, LINE3, 1.2))

    o.append(rect(60, 86, 330, 336, stroke=LINE3, dash="4 4"))
    o.append(txt(74, 108, "NAVIGATION & SENSING", 9.5, RED2, MONO, weight=700, ls="0.14em"))
    o.append(panel_box(80, 126, 130, 36, "CRPA ANTENNA", size=9))
    o.append(panel_box(250, 126, 120, 36, "MULTI-BAND GNSS", size=8.8))
    o.append(arrow(210, 144, 250, 144, ns, "ink"))
    o.append(panel_box(80, 182, 130, 36, "PITOT TUBE", size=9))
    o.append(panel_box(250, 182, 120, 36, "AIR DATA COMPUTER", size=8))
    o.append(arrow(210, 200, 250, 200, ns, "ink"))
    o.append(panel_box(80, 238, 290, 36, "INS — INERTIAL NAVIGATION", size=9))
    o.append(panel_box(80, 294, 290, 44, "TONBO EO/IR SEEKER", sub="TERMINAL GUIDANCE, NO RF", size=9, sub_size=7.6))
    o.append(panel_box(80, 358, 290, 52, "AI-DSMAC SCENE MATCHING", sub="GNSS-DENIED NAVIGATION BRIDGE", size=9, sub_size=7.6))

    o.append(rect(410, 86, 250, 336, stroke=RED, dash="4 4"))
    o.append(txt(424, 108, "FLIGHT CONTROL", 9.5, RED2, MONO, weight=700, ls="0.14em"))
    o.append(panel_box(435, 190, 200, 130, "FLIGHT CONTROLLER", stroke=RED, fill=RED_W, sw=1.4,
                       tcol=INK, size=12))
    o.append(panel_box(435, 340, 200, 50, "TELEMETRY", sub="STATUS · POSITION · ABORT", size=9.5, sub_size=7.6))
    o.append(arrow(535, 320, 535, 340, ns, "ink"))

    # sensor bus into the flight controller, and control out to propulsion
    o.append(line(392, 144, 392, 384, INK2, 1.1))
    for sy in (144, 200, 256, 316, 384):
        o.append(line(370, sy, 392, sy, INK2, 1.1))
    o.append(arrow(392, 250, 435, 250, ns, "ink"))
    o.append('<path d="M635,250 H672 V155 H710" fill="none" stroke="%s" stroke-width="1.1" marker-end="url(#%s-ink)"/>' % (INK2, ns))

    o.append(rect(690, 86, 250, 336, stroke=LINE3, dash="4 4"))
    o.append(txt(704, 108, "PROPULSION", 9.5, RED2, MONO, weight=700, ls="0.14em"))
    o.append(panel_box(710, 130, 105, 50, "ENGINE CONTROL UNIT", sub="ECU", size=7.8, sub_size=7.4))
    o.append(panel_box(835, 130, 90, 50, "TURBOJET ENGINE", size=7.2))
    o.append(arrow(815, 155, 835, 155, ns, "ink"))
    o.append(panel_box(710, 214, 105, 42, "FUEL TANK", size=9))
    o.append(panel_box(835, 214, 90, 42, "FUEL PUMP", size=9))
    o.append(arrow(815, 235, 835, 235, ns, "ink"))
    o.append(arrow(880, 214, 880, 180, ns, "red", dash="4 4"))

    o.append(rect(60, 444, 880, 88, stroke=LINE3, dash="4 4"))
    o.append(txt(74, 466, "ACTUATION", 9.5, RED2, MONO, weight=700, ls="0.14em"))
    for i, x in enumerate((80, 300, 520, 740)):
        o.append(panel_box(x, 478, 180, 40, f"ACTUATOR {i+1}", size=9.5))
    o.append(line(535, 422, 535, 444, INK2, 1.1))
    o.append(line(535, 444, 170, 444, INK2, 1.1))
    o.append(line(762, 444, 762, 444, INK2, 1.1))

    o.append(line(60, 572, 100, 572, INK2, 1.3))
    o.append(txt(110, 576, "SIGNAL / CONTROL", 9.5, INK3, MONO, ls="0.1em"))
    o.append(line(280, 572, 320, 572, LINE3, 1.3))
    o.append(txt(330, 576, "POWER RAIL", 9.5, INK3, MONO, ls="0.1em"))
    o.append(line(460, 572, 500, 572, RED2, 1.3, dash="4 4"))
    o.append(txt(510, 576, "FUEL FLOW", 9.5, INK3, MONO, ls="0.1em"))
    o.append(txt(940, 576, "ONE STACK, SHARED BY THE FAMILY", 9.5, INK4, MONO, anchor="end", ls="0.12em"))
    o.append("</svg>")
    return "".join(o)


# ══════════════════════════════════════════════════════════════════════
# 8 · VEHICLE SOFTWARE ARCHITECTURE — functional view
# ══════════════════════════════════════════════════════════════════════
def arch_software():
    W, H = 1000, 690
    ns = "asw"
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="Core vehicle software architecture: sensor drivers, estimation and control, mission autonomy, platform services and foundation">',
         defs_arrow(ns, {"ink": INK2, "red": RED2, "grey": LINE3})]

    o.append(txt(50, 40, "ONE CODEBASE · DIFFERENCES ARE CONFIGURATION, NOT BRANCHES", 10, INK3, MONO, ls="0.12em"))

    o.append(rect(50, 60, 210, 390, stroke=LINE3, dash="4 4"))
    o.append(txt(64, 82, "SENSOR DRIVERS", 9.5, RED2, MONO, weight=700, ls="0.13em"))
    sensors = ["MULTI-BAND GNSS + CRPA", "INERTIAL NAVIGATION", "AIR DATA", "EO/IR SEEKER", "SCENE MATCHING"]
    for i, s in enumerate(sensors):
        o.append(panel_box(66, 96 + i * 70, 178, 44, s, size=8.4))

    o.append(rect(300, 60, 380, 390, stroke=RED, dash="4 4"))
    o.append(txt(314, 82, "ESTIMATION & CONTROL", 9.5, RED2, MONO, weight=700, ls="0.13em"))
    o.append(panel_box(322, 100, 336, 58, "STATE ESTIMATOR", sub="FUSES EVERY NAVIGATION INPUT",
                       stroke=RED, fill=RED_W, sw=1.3, tcol=INK, size=10, sub_size=7.8))
    o.append(panel_box(322, 178, 336, 58, "GUIDANCE LAW", sub="WAYPOINT · TERRAIN-FOLLOW · TERMINAL", size=10, sub_size=7.8))
    o.append(panel_box(322, 256, 336, 58, "CONTROL LAW", sub="DIRECT-ACTUATOR POLICY", size=10, sub_size=7.8))
    o.append(panel_box(322, 334, 336, 58, "ENVELOPE PROTECTION", sub="SATURATION · G-LIMIT · ABORT", size=10, sub_size=7.8))
    for y in (158, 236, 314):
        o.append(arrow(490, y, 490, y + 20, ns, "red"))

    o.append(rect(720, 60, 230, 390, stroke=LINE3, dash="4 4"))
    o.append(txt(734, 82, "MISSION & AUTONOMY", 9.5, RED2, MONO, weight=700, ls="0.13em"))
    for i, (lbl, sub) in enumerate([
        ("MISSION INGEST", "WAYPOINTS · TARGET · ABORT"),
        ("ROUTE PLANNER", "TERRAIN FOLLOWING"),
        ("TERMINAL MANAGER", "SEEKER CUE · LOCK · DIVE"),
        ("AUTONOMY SUPERVISOR", "RETASK · GEOFENCE"),
    ]):
        o.append(panel_box(734, 96 + i * 88, 202, 64, lbl, sub=sub, size=9, sub_size=7.4))
    o.append(arrow(720, 300, 658, 285, ns, "ink"))

    o.append(rect(300, 488, 650, 84, stroke=LINE3, dash="4 4"))
    o.append(txt(314, 510, "PLATFORM SERVICES", 9.5, RED2, MONO, weight=700, ls="0.13em"))
    for i, s in enumerate(["DETERMINISTIC SCHEDULER", "HEALTH & FDIR", "HIGH-RATE LOGGING", "TELEMETRY ENCODER"]):
        o.append(panel_box(314 + i * 160, 522, 150, 38, s, size=7.6))
    o.append(arrow(490, 392, 490, 488, ns, "ink"))

    o.append(rect(50, 596, 900, 62, stroke=LINE3, fill="#0A0A0A"))
    o.append(txt(64, 618, "FOUNDATION", 9.5, RED2, MONO, weight=700, ls="0.13em"))
    for i, s in enumerate(["REAL-TIME RUNTIME · IN-HOUSE FORK", "HAL + PER-PLATFORM CONFIG", "HIL / SIL VALIDATION BENCH"]):
        o.append(txt(210 + i * 246, 626, s, 9.3, INK3, MONO))
    o.append(arrow(250, 572, 250, 596, ns, "ink"))

    o.append(txt(950, 578, "EW HARDENING + CYBER · QUALIFICATION EVIDENCE PER SUBSYSTEM", 9, INK4, MONO, anchor="end"))
    o.append("</svg>")
    return "".join(o)


# ══════════════════════════════════════════════════════════════════════
# 9 · CORTEX — the battlefield data stack
# ══════════════════════════════════════════════════════════════════════
def cortex_stack():
    W, H = 1000, 770
    ns = "cs"
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="Apollyon Cortex architecture: sensors to world graph to role-adapted outputs, memory federation and dissemination">',
         defs_arrow(ns, {"ink": INK2, "red": RED2, "grey": LINE3})]

    o.append(txt(40, 34, "WHAT ENTERS THE FORMATION", 9.5, INK4, MONO, ls="0.13em"))
    inputs = ["UAV VIDEO", "CCTV / THERMAL", "RADAR PLOTS", "PATROL REPORTS", "REGISTRIES"]
    for i, s in enumerate(inputs):
        o.append(panel_box(40 + i * 186, 48, 168, 46, s, size=8.6))
        o.append(arrow(40 + i * 186 + 84, 94, 40 + i * 186 + 84, 124, ns, "grey"))

    o.append(panel_box(40, 124, 920, 46, "NORMALISATION & REGISTRATION",
                       sub="TIME SYNC · PLATFORM POSE · RAY-TO-GROUND PROJECTION · CALIBRATION", size=9.5, sub_size=8.2))
    for x in (250, 500, 750):
        o.append(arrow(x, 170, x, 200, ns, "grey"))

    o.append(rect(40, 200, 440, 110, stroke=LINE3, dash="4 4"))
    o.append(txt(54, 222, "LEARNED VISUAL PIPELINE", 9.5, RED2, MONO, weight=700, ls="0.12em"))
    o.append(txt(54, 242, "SPATIAL-VIDEO FOUNDATION MODEL", 9, INK3, MONO))
    for i, s in enumerate(["INSTANCE MASKS", "OBJECT TUBES", "OPEN-VOCAB QUERY"]):
        o.append(panel_box(56 + i * 140, 256, 130, 40, s, size=7.2))
    o.append(rect(520, 200, 440, 110, stroke=LINE3, dash="4 4"))
    o.append(txt(534, 222, "CLASSICAL KINEMATIC PIPELINE", 9.5, RED2, MONO, weight=700, ls="0.12em"))
    o.append(txt(534, 242, "KALMAN FILTER · IMM ESTIMATION", 9, INK3, MONO))
    for i, s in enumerate(["TRACK ASSOCIATION", "ERROR ELLIPSES", "VELOCITY / HEADING"]):
        o.append(panel_box(536 + i * 140, 256, 130, 40, s, size=7.2))
    o.append(arrow(260, 310, 260, 340, ns, "grey"))
    o.append(arrow(740, 310, 740, 340, ns, "grey"))

    o.append(panel_box(180, 340, 640, 70, "TOPOLOGICAL WORLD GRAPH",
                       sub="PERSISTENT ENTITIES · RELATIONS · EVENTS · AUTHORITY TAGS · CONFIDENCE",
                       stroke=RED, fill=RED_W, sw=1.5, tcol=INK, size=11, sub_size=8))
    o.append(arrow(500, 410, 500, 440, ns, "red"))

    o.append(panel_box(330, 440, 340, 50, "ASSESSED EVENT", sub="ANOMALY AGAINST BASELINE MEMORY", size=9.5, sub_size=7.8))
    for x in (140, 380, 620, 860):
        o.append(arrow(x, 490, x, 520, ns, "grey"))

    outs = [
        ("HQ DOSSIER", "FULL EVIDENCE"),
        ("ENGINEER TASK", "INSPECTION ORDERS"),
        ("VEHICLE ALERT", "MAP VECTOR + DETOUR"),
        ("PATROL TEXT", "50-BYTE RADIO ALERT"),
    ]
    for i, (lbl, sub) in enumerate(outs):
        o.append(panel_box(40 + i * 240, 520, 200, 56, lbl, sub=sub, size=8.8, sub_size=7.4))

    o.append(rect(40, 608, 920, 74, stroke=LINE3, dash="4 4"))
    o.append(txt(54, 630, "FOUR-TIER MEMORY FEDERATION", 9.5, RED2, MONO, weight=700, ls="0.12em"))
    for i, (lbl, sub) in enumerate([
        ("RAW EVIDENCE", "CHAIN OF CUSTODY"),
        ("LATENT FEATURES", "RETROSPECTIVE SEARCH"),
        ("WORLD GRAPH", "AUTHORITATIVE STATE"),
        ("DERIVED SUMMARIES", "BRIEFINGS"),
    ]):
        o.append(panel_box(54 + i * 226, 638, 212, 38, lbl, sub=sub, size=8, sub_size=7.2))

    o.append(rect(40, 698, 920, 56, stroke=LINE3))
    o.append(txt(54, 718, "DISSEMINATION", 9, RED2, MONO, weight=700, ls="0.12em"))
    o.append(txt(54, 738, "SEMANTIC COMPRESSION: FIBRE / MANET / VHF ≤ 200 BYTES PER UPDATE · DISCONNECTED STORE-FORWARD", 8.6, INK3, MONO))
    o.append(txt(946, 718, "OBJECT-LEVEL CLASSIFICATION · PKI ZERO TRUST · CRYPTOGRAPHIC WIPE", 8, INK4, MONO, anchor="end"))
    o.append("</svg>")
    return "".join(o)


# ══════════════════════════════════════════════════════════════════════
# 10 · SALVO ARITHMETIC
# ══════════════════════════════════════════════════════════════════════
def salvo_curve():
    W, H = 1000, 500
    ns = "sc"
    L, R, T, B = 96, 930, 80, 340
    budget, cc, ce = 120.0, 200.0, 3000.0
    n_intr, p_k, sal = 400, 0.75, 2
    w_soft, w_hard = 0.45, 0.55
    soft_t, hard_t = 120, 15

    def score(mix, att_first=True):
        nC = budget * mix / (cc / 1000.0)
        nE = budget * (1 - mix) / (ce / 1000.0)
        intr = n_intr

        def engage(n):
            nonlocal intr
            eng = min(n, math.floor(intr / sal))
            intr -= eng * sal
            return max(0.0, n - eng * p_k)

        if att_first:
            leakC, leakE = engage(nC), engage(nE)
        else:
            leakE, leakC = engage(nE), engage(nC)
        soft = min(soft_t, leakC * 0.30)
        hard = min(hard_t, leakE * 0.70)
        return w_soft * (soft / soft_t) + w_hard * (hard / hard_t)

    def X(m):
        return L + m * (R - L)

    def Y(s):
        return B - s * (B - T)

    xs = [i / 200 for i in range(201)]
    cur = [score(m, True) for m in xs]
    opp = [score(m, False) for m in xs]
    best_i = max(range(len(xs)), key=lambda i: cur[i])
    best_m, best_s = xs[best_i], cur[best_i]
    dry_i = max(range(1, len(xs)), key=lambda i: cur[i] - cur[i - 1])

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="Campaign objectives met against the share of budget spent on attritable rounds">']

    for gv in (0, 25, 50, 75, 100):
        y = Y(gv / 100)
        o.append(line(L, y, R, y, LINE if gv else LINE2))
        o.append(txt(L - 14, y + 4, f"{gv}%", 10, INK4, MONO, anchor="end"))
    for gv in (0, 25, 50, 75, 100):
        x = X(gv / 100)
        o.append(line(x, B, x, B + 6, LINE2))
        o.append(txt(x, B + 24, f"{gv}%", 10.5, INK4, MONO, anchor="middle"))

    o.append(poly([(X(m), Y(s)) for m, s in zip(xs, opp)], INK4, sw=1.2, dash="5 4"))
    o.append(poly([(X(m), Y(s)) for m, s in zip(xs, cur)], RED2, sw=1.8))

    o.append(line(X(xs[dry_i]), T + 8, X(xs[dry_i]), B, LINE3, 1, dash="4 4"))
    o.append(txt(X(xs[dry_i]) + 10, T + 20, "MAGAZINE RUNS DRY", 9.5, INK3, MONO, weight=700))

    o.append(line(X(best_m), T + 8, X(best_m), B, RED_W, 1, dash="4 4"))
    o.append(dot(X(best_m), Y(best_s), 5, RED))
    o.append(txt(X(best_m), Y(best_s) - 16, f"BEST SPLIT {int(round(best_m*100))}%", 11.5, RED2, MONO, anchor="middle", weight=700))
    o.append(txt(X(best_m), Y(best_s) + 26, f"{int(best_s*100)}% of objectives", 10, INK3, MONO, anchor="middle"))

    o.append(txt(L, T - 20, "OBJECTIVES MET", 9.5, INK4, MONO, ls="0.12em"))
    o.append(txt((L + R) / 2, B + 52, "SHARE OF BUDGET SPENT ON ATTRITABLE ROUNDS", 9.5, INK4, MONO, anchor="middle", ls="0.12em"))
    o.append(line(L, B + 74, L + 26, B + 74, RED2, 1.8))
    o.append(txt(L + 36, B + 78, "ATTRITABLE FIRED FIRST", 9.5, INK3, MONO))
    o.append(line(L + 250, B + 74, L + 276, B + 74, INK4, 1.2, dash="5 4"))
    o.append(txt(L + 286, B + 78, "EXQUISITE FIRED FIRST", 9.5, INK3, MONO))
    o.append(txt(L, B + 108, "All-exquisite leaves most targets untouched; all-attritable clears the soft set and nothing hardened.", 10, INK4, MONO))
    o.append(txt(L, B + 126, "The mixture beats both corners, and the firing order is worth as much as the mixture.", 10, INK4, MONO))
    return "".join(o)


# ══════════════════════════════════════════════════════════════════════
# 11 · THE ENGINEERING SYSTEM — machine, loop, compounding asset
# ══════════════════════════════════════════════════════════════════════
def eng_system():
    W, H = 1000, 810
    ns = "es"
    o = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" '
        f'aria-label="The engineering system: the machine, the flight loop that upgrades four systems, and the assets that compound across generations">',
        f'<rect width="{W}" height="{H}" fill="{BG}"/>',
        defs_arrow(ns, {"ink": INK2, "red": RED2, "grey": LINE3})
    ]

    def band(y, letter, title, note=None):
        parts = [txt(40, y, f"{letter} · {title}", 10, RED2, MONO, weight=700, ls="0.14em")]
        if note:
            parts.append(txt(960, y, note, 9.5, INK2, MONO, anchor="end", ls="0.08em", weight=600))
        parts.append(line(40, y + 14, 960, y + 14, LINE2, 1))
        return "".join(parts)

    # ── A · the machine ───────────────────────────────────────────────
    o.append(band(36, "A", "THE MACHINE — WHAT FLIES", "ONE CODEBASE · ONE NAVIGATION STACK · ONE RUNTIME"))

    o.append(panel_box(40, 64, 650, 54, "SHARED CORE",
                       sub="NAVIGATION & SENSING · ESTIMATION · CONTROL · FLIGHT SOFTWARE · TELEMETRY",
                       stroke=RED, fill=RED_W, sw=1.4, tcol="#ffffff", scol="#cbd5e1", size=11, sub_size=8.0))

    o.append(panel_box(710, 64, 250, 54, "PER-PLATFORM DELTA",
                       sub="ENGINE CLASS · STRUCTURE · LAUNCH MODE",
                       stroke=LINE2, fill="#090d14", sw=1.1, tcol=INK2, scol=INK3, size=10, sub_size=7.8))

    o.append(line(40, 140, 960, 140, LINE3, 1.2))
    o.append(txt(48, 134, "POWER RAIL", 8.5, INK3, MONO, ls="0.12em", weight=600))

    # 4 Subsystems
    cards_a = [
        ("NAVIGATION & SENSING", False),
        ("FLIGHT CONTROL", True),
        ("PROPULSION", False),
        ("ACTUATION", False),
    ]
    for i, (name, is_core) in enumerate(cards_a):
        x = 40 + i * 235
        cx = x + 107.5
        o.append(line(cx, 140, cx, 156, LINE3, 1.1))
        stroke = RED if is_core else LINE2
        fill = RED_W if is_core else "#090d14"
        tcol = "#ffffff" if is_core else INK2
        o.append(panel_box(x, 156, 215, 56, name, stroke=stroke, fill=fill, sw=1.3 if is_core else 1.0, tcol=tcol, size=9.5))
        if i < 3:
            o.append(arrow(x + 215, 184, x + 235, 184, ns, "ink"))

    o.append(line(40, 236, 90, 236, INK2, 1.3))
    o.append(txt(98, 240, "SIGNAL / CONTROL", 8.5, INK2, MONO, ls="0.1em"))
    o.append(line(250, 236, 290, 236, LINE3, 1.3))
    o.append(txt(298, 240, "POWER", 8.5, INK3, MONO, ls="0.1em"))
    o.append(line(370, 236, 410, 236, RED2, 1.3, dash="4,4"))
    o.append(txt(418, 240, "FUEL", 8.5, RED2, MONO, ls="0.1em"))
    o.append(txt(960, 240, "EVERY LIMIT THAT IS BOUGHT IS A LIMIT ON THE NEXT ITERATION", 8.5, INK3, MONO, anchor="end", ls="0.08em"))

    # ── B · the loop ──────────────────────────────────────────────────
    o.append(band(278, "B", "THE LOOP — HOW IT GETS BETTER", "ONE PASS: DAYS · ONE CAMPAIGN: LESS THAN THE LAST"))

    # Left column: x = 56 to 524 (w = 468). Center = 290.
    o.append(panel_box(56, 306, 468, 46, "FLY AT THE EDGE",
                       sub="INSTRUMENTED FOR CURRENT · BUS LATENCY · ACCELERATION",
                       stroke=RED, fill=RED_W, sw=1.3, tcol="#ffffff", scol="#cbd5e1", size=10.5, sub_size=7.8))

    o.append(arrow(290, 352, 290, 370, ns, "ink"))

    o.append(panel_box(56, 370, 468, 42, "MISMATCH & PREDICTION",
                       sub="LOGS REPLAYED AGAINST THE TWIN",
                       stroke=LINE2, fill="#090d14", sw=1.1, tcol=INK2, scol=INK3, size=9.8, sub_size=7.8))

    o.append(arrow(290, 412, 290, 426, ns, "ink"))

    # 4 upgrade boxes: w = 114, gaps: 4, 4, 4. Total = 468.
    cells = [
        ("SIMULATOR PHYSICS", "AERO AND COMPONENT TERMS"),
        ("ONBOARD RUNTIME", "KERNEL AND SCHEDULING"),
        ("CONTROL POLICIES", "RETRAINED AT THE EDGE"),
        ("HARDWARE SPEC", "POWER, THERMAL, STRUCTURE"),
    ]
    xs = [56, 174, 292, 410]
    cxs = [x + 57 for x in xs]
    o.append(line(cxs[0], 426, cxs[-1], 426, LINE2, 1))
    for i, (lbl, sub) in enumerate(cells):
        x = xs[i]
        cx = cxs[i]
        o.append(line(cx, 426, cx, 438, LINE2, 1))
        o.append(panel_box(x, 438, 114, 56, lbl, sub=sub, stroke=LINE2, fill="#090d14", size=7.8, sub_size=6.4, scol=INK3, pad=8))
        o.append(line(cx, 494, cx, 506, LINE2, 1))
    o.append(line(cxs[0], 506, cxs[-1], 506, LINE2, 1))

    o.append(arrow(290, 506, 290, 520, ns, "ink"))

    o.append(panel_box(56, 520, 468, 46, "THE NEXT AIRCRAFT",
                       sub="SOONER · FASTER · MORE MARGIN",
                       stroke=RED, fill=RED_W, sw=1.3, tcol="#ffffff", scol="#cbd5e1", size=10.5, sub_size=8.0))

    # Loopback wire: exits left of NEXT AIRCRAFT at (56, 543), runs along x=34, enters FLY AT THE EDGE at (56, 329)
    o.append(line(56, 543, 34, 543, LINE2, 1.2))
    o.append(line(34, 543, 34, 329, LINE2, 1.2))
    o.append(arrow(34, 329, 56, 329, ns, "ink", 1.2))

    # Right column (twin stack): x = 640 to 960 (w = 320). Center = 800.
    o.append(panel_box(640, 306, 320, 52, "PHYSICS BACKBONE",
                       sub="ONE PACKAGE PER AIRFRAME — THE SAME TWIN ARCHITECTURE FOR EVERY VEHICLE",
                       stroke=RED, fill=RED_W, sw=1.3, tcol="#ffffff", scol="#cbd5e1", size=10, sub_size=7.4))

    o.append(arrow(800, 358, 800, 372, ns, "ink"))

    o.append(panel_box(640, 372, 320, 44, "TRAINING",
                       sub="RL + DOMAIN RANDOMISATION · BEHAVIOUR CLONING · WORLD MODEL",
                       stroke=LINE2, fill="#090d14", size=9.6, sub_size=7.2, scol=INK3))

    o.append(arrow(800, 416, 800, 434, ns, "ink"))

    o.append(panel_box(640, 434, 320, 44, "HIL VALIDATION",
                       sub="THE FIRST FLIGHT HAPPENS IN THE LAB",
                       stroke=LINE2, fill="#090d14", size=9.6, sub_size=7.2, scol=INK3))

    o.append(arrow(800, 478, 800, 496, ns, "ink"))

    o.append(panel_box(640, 496, 320, 44, "FLEET FLYWHEEL",
                       sub="RACES & FLEET FLIGHTS → LIMIT-FLIGHT DATA",
                       stroke=LINE2, fill="#090d14", size=9.6, sub_size=7.2, scol=INK3))

    # Flywheel loopback to training
    o.append(f'<path d="M960,518 H976 V394 H960" fill="none" stroke="{LINE3}" stroke-width="1.2" marker-end="url(#{ns}-ink)"/>')

    # Cross connection: FLIGHT LOGS (from NEXT AIRCRAFT right edge 524 to PHYSICS BACKBONE left edge 640)
    # Channel is x=524 to 640 (w=116). Wire at x=572, text at 572
    o.append(f'<path d="M524,543 H572 V332 H640" fill="none" stroke="{LINE3}" stroke-width="1.2" marker-end="url(#{ns}-grey)"/>')
    o.append(txt(572, 535, "FLIGHT LOGS", 8.5, INK3, MONO, anchor="middle", ls="0.08em", weight=600))

    # Cross connection: TRAINED POLICY (from TRAINING left edge 640 to FLY AT THE EDGE right edge 524)
    # Wire at x=592, text at 592
    o.append(f'<path d="M640,394 H592 V329 H524" fill="none" stroke="{RED2}" stroke-width="1.2" marker-end="url(#{ns}-red)"/>')
    o.append(txt(592, 322, "TRAINED POLICY", 8.5, RED2, MONO, anchor="middle", weight=700, ls="0.08em"))

    # ── C · the compounding asset ─────────────────────────────────────
    o.append(band(608, "C", "THE COMPOUNDING ASSET — WHY THE SPEED REPEATS"))

    assets = ["ONE CODEBASE", "PHYSICS PACKAGE", "TRAINED POLICIES", "QUALIFICATION EVIDENCE", "TEST RIGS & PIPELINE"]
    for i, a in enumerate(assets):
        x = 40 + i * 187
        o.append(panel_box(x, 634, 172, 36, a, stroke=LINE2, fill="#090d14", size=8.0, tcol=INK2))

    gens = [
        ("NIGHTSHADE MK I", "PAYS FOR THE CORE", True),
        ("NIGHTSHADE MK II", "PAYS THE DELTA", False),
        ("NIGHTSHADE MK III", "+ EVIDENCE REUSED", False),
        ("HEMLOCK MK I", "PAYS THE DELTA", False),
        ("HEMLOCK MK II", "+ TERRAIN LAYER", False),
    ]
    for i, (g, sub, core) in enumerate(gens):
        x = 40 + i * 187
        stroke = RED if core else LINE2
        fill = RED_W if core else "#090d14"
        tcol = "#ffffff" if core else INK2
        scol = "#fca5a5" if core else INK3
        o.append(line(x + 86, 670, x + 86, 680, LINE2, 1))
        o.append(panel_box(x, 680, 172, 48, g, sub=sub, stroke=stroke, fill=fill, sw=1.3 if core else 1.0,
                           tcol=tcol, scol=scol, size=8.2, sub_size=7.2))

    o.append(txt(960, 764, "EACH PASS COSTS LESS · EACH GENERATION PAYS LESS · THE FRONTIER RISES", 9.2, INK2, MONO, anchor="end", ls="0.08em", weight=600))
    o.append("</svg>")
    return "".join(o)


# ══════════════════════════════════════════════════════════════════════
# 12 · THE VEHICLE AND ITS TWIN
# ══════════════════════════════════════════════════════════════════════
def eng_twin():
    W, H = 1000, 560
    ns = "et"
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="The flight vehicle and its simulation twin: measured flight data identifies the physics, the twin trains the policies, the hardware-in-the-loop harness clears them for flight">',
         defs_arrow(ns, {"ink": INK2, "red": RED2, "grey": LINE3})]

    def chip(x, y, w, h, label, size=7, tcol=INK2, stroke=LINE3):
        return panel_box(x, y, w, h, label, size=size, tcol=tcol, stroke=stroke)

    # vehicle
    o.append(txt(40, 40, "THE FLIGHT VEHICLE", 9.5, INK4, MONO, ls="0.13em"))
    o.append(rect(40, 56, 430, 400, stroke=LINE3, dash="4 4"))
    o.append(txt(56, 78, "ONE SHARED CORE, ONE PER-PLATFORM PACKAGE", 8.5, RED2, MONO, weight=700, ls="0.1em"))
    o.append(chip(56, 94, 398, 40, "NAVIGATION & SENSING", size=8.4, tcol=INK))
    for i, c in enumerate(["CRPA + GNSS", "INERTIAL", "SEEKER", "SCENE MATCH"]):
        o.append(chip(56 + i * 100, 140, 94, 34, c, size=6.8))
    o.append(chip(56, 186, 398, 40, "FLIGHT CONTROL", size=8.4, tcol=INK))
    for i, c in enumerate(["ESTIMATOR", "GUIDANCE", "CONTROL LAW", "ENVELOPE"]):
        o.append(chip(56 + i * 100, 232, 94, 34, c, size=6.8))
    o.append(chip(56, 278, 398, 40, "PROPULSION", size=8.4, tcol=INK))
    o.append(chip(56, 324, 190, 34, "ECU → TURBOJET", size=6.8))
    o.append(chip(264, 324, 190, 34, "FUEL → PUMP", size=6.8))
    o.append(chip(56, 366, 398, 40, "ACTUATION", size=8.4, tcol=INK))
    o.append(chip(56, 412, 398, 30, "POWER RAIL — ONE RAIL TO HARDEN", size=7.4, tcol=INK3))

    # twin
    o.append(txt(530, 40, "THE SIMULATION TWIN", 9.5, INK4, MONO, ls="0.13em"))
    o.append(rect(530, 56, 430, 400, stroke=LINE3, dash="4 4"))
    o.append(txt(546, 78, "IDENTIFIED FROM FLIGHT, NOT WRITTEN FROM A TEXTBOOK", 8.5, RED2, MONO, weight=700, ls="0.1em"))
    o.append(panel_box(546, 94, 398, 62, "IDENTIFICATION",
                       sub="FLIGHT LOGS → AERODYNAMICS · ACTUATOR CURVE · INERTIA", size=8.4, sub_size=6.8))
    o.append(panel_box(546, 168, 398, 76, "SHARED PHYSICS BACKBONE",
                       sub="ONE PACKAGE PER AIRFRAME · BOUNDARY LAYER · ROTOR WASH · THERMAL · VOLTAGE SAG · VIBRATION",
                       stroke=RED, fill=RED_W, sw=1.3, tcol=INK, size=9.4, sub_size=6.6))
    o.append(panel_box(546, 256, 398, 62, "TRAINING",
                       sub="RL + DOMAIN RANDOMISATION · BEHAVIOUR CLONING · WORLD MODEL", size=8.4, sub_size=6.8))
    o.append(panel_box(546, 330, 398, 58, "HIL VALIDATION",
                       sub="THE FIRST FLIGHT OF EVERY VERSION HAPPENS IN THE LAB", size=8.4, sub_size=6.8))
    o.append(panel_box(546, 400, 398, 42, "QUALIFICATION EVIDENCE",
                       sub="EVERY CAMPAIGN RETURNS EVIDENCE THAT TRAVELS", size=8, sub_size=6.6))

    o.append(arrow(470, 120, 530, 120, ns, "ink"))
    o.append(txt(500, 112, "FLIGHT LOGS", 8, INK3, MONO, anchor="middle", ls="0.08em"))
    o.append(arrow(530, 454, 470, 454, ns, "red"))
    o.append(txt(500, 446, "POLICIES", 8, RED2, MONO, anchor="middle", ls="0.08em"))

    o.append(txt(40, 500, "A CONTROL POLICY IS ONLY EVER AS GOOD AS THE PHYSICS IT GREW UP IN.", 12, INK, SANS, weight=600))
    o.append(txt(40, 522, "The twin is earned one real flight at a time. A new airframe is a new package on the same simulation architecture — not a new simulator.", 11, INK3, SANS))
    o.append("</svg>")
    return "".join(o)


# ══════════════════════════════════════════════════════════════════════
# 14 · LATENCY IS A DISTANCE
# ══════════════════════════════════════════════════════════════════════
def eng_latency():
    W, H = 1000, 460
    ns = "lt"
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="Distance flown while one control cycle runs: a conventional stack against the Apollyon stack">']

    L, R = 190, 940

    def X(m):
        return L + (m / 2.0) * (R - L)

    o.append(txt(L, 34, "DISTANCE FLOWN WHILE ONE CONTROL CYCLE RUNS", 9.5, INK4, MONO, ls="0.12em"))
    for v in (0, 0.5, 1.0, 1.5, 2.0):
        x = X(v)
        o.append(line(x, 52, x, 342, LINE))
        o.append(txt(x, 364, f"{v:.1f} m", 9.5, INK4, MONO, anchor="middle"))

    o.append(txt(180, 96, "A CONVENTIONAL STACK", 10, INK3, MONO, anchor="end", weight=700))
    segs = [(0, 0.48, "#161616"), (0.48, 0.86, "#1E1E1E"), (0.86, 1.34, "#282828"), (1.34, 1.60, "#333333")]
    for a, b, col in segs:
        o.append(rect(X(a), 76, X(b) - X(a), 44, stroke=LINE2, fill=col))
    o.append(rect(X(1.60), 76, X(1.90) - X(1.60), 44, stroke=RED_W, fill="none", dash="4 3"))
    for lbl, x in [("copies through user space", 0.24), ("runtime overhead", 0.67), ("inference", 1.10), ("actuate", 1.47)]:
        o.append(txt(X(x), 140, lbl, 9.5, INK4, MONO, anchor="middle"))
    o.append(txt(X(1.75), 140, "jitter — the cycle", 9.5, RED2, MONO, anchor="middle"))
    o.append(txt(X(1.75), 154, "that misses", 9.5, RED2, MONO, anchor="middle"))
    o.append(txt(X(1.90) - 6, 68, "1.9 m of flight", 11.5, RED2, MONO, anchor="end", weight=700))

    o.append(txt(180, 240, "OURS", 11, INK, MONO, anchor="end", weight=700))
    o.append(rect(X(0), 220, X(0.25) - X(0), 44, stroke=INK, fill=RED_W))
    o.append(txt(X(0.125), 292, "0.25 m", 11.5, INK, MONO, anchor="middle", weight=700))
    o.append(rect(X(0.25) + 4, 220, X(2.0) - X(0.25) - 4, 44, stroke=LINE2, fill="none", dash="4 4"))
    o.append(wrap(X(0.25) + 20, 238, "everything after this point is margin — time to react rather than time to compute",
                  X(2.0) - X(0.25) - 60, 11, INK3, SANS, lh=16))

    o.append(line(60, 400, 960, 400, LINE2))
    for i, (k, v) in enumerate([
        ("FUSED KERNELS", "no allocation, no launch overhead"),
        ("REAL-TIME KERNEL", "isolated cores, nothing preempts the loop"),
        ("ZERO-COPY PATH", "sensors write straight into GPU memory"),
    ]):
        x = 60 + i * 306
        o.append(rect(x, 416 - 7, 8, 8, stroke=RED, fill=RED_W))
        o.append(txt(x + 16, 420, k, 9.5, INK2, MONO, weight=700))
        o.append(txt(x + 16, 438, v, 9.5, INK4, MONO))
    o.append("</svg>")
    return "".join(o)


# ══════════════════════════════════════════════════════════════════════
# 15 · CONVERGENCE — the loop closes, and the pipeline transfers
# ══════════════════════════════════════════════════════════════════════
def eng_convergence():
    W, H = 1000, 500
    ns = "ec"
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="Learned control converging on the expert envelope, and the transfer chain by which the same loop packages the next airframe">',
         defs_arrow(ns, {"ink": INK2, "red": RED2, "grey": LINE3})]

    L, R, T, B = 70, 540, 104, 330
    o.append(txt(70, 40, "THE LOOP CLOSES", 9.5, INK4, MONO, ls="0.13em"))
    o.append(txt(70, 58, "FRACTION OF THE PHYSICAL ENVELOPE RECOVERED", 8.5, INK4, MONO, ls="0.08em"))
    o.append(line(L, T, L, B, LINE2))
    o.append(line(L, B, R, B, LINE2))
    o.append(txt((L + R) / 2, B + 42, "FLIGHT CAMPAIGNS", 9.5, INK4, MONO, anchor="middle", ls="0.12em"))

    ey = 132
    o.append(line(L, ey, R, ey, RED2, 1.4, dash="7 5"))
    o.append(txt(R, ey - 10, "expert envelope — what the aircraft can actually do", 10, RED2, MONO, anchor="end"))
    o.append(line(L + 10, 310, L + 190, 310, INK4, 1.4, dash="4 4"))
    o.append(txt(L + 200, 314, "conventional autonomy", 10, INK4, MONO))

    pts = [(70, 310), (150, 262), (230, 224), (310, 194), (390, 172), (470, 156), (540, 146)]
    o.append(poly(pts, INK2, sw=2))
    for x, y in pts:
        o.append(dot(x, y, 3.6, RED))
    o.append(txt(548, 158, "learned control", 10.5, INK2, MONO, anchor="end", weight=700))
    o.append(txt(70, 372, "Each mark is one flight campaign: one identification pass, one simulator correction, one retrain. The loop", 10, INK4, MONO))
    o.append(txt(70, 388, "closes when the policy matches the expert in reality and the twin predicts the flight.", 10, INK4, MONO))

    o.append(line(620, 30, 620, 430, LINE))

    o.append(txt(650, 40, "WHAT TRAVELS TO THE NEXT AIRFRAME", 9.5, INK4, MONO, ls="0.12em"))
    chain = [
        ("RESEARCH QUAD", "instrumented, cheap to fly, cheap to crash — where the loop is proven"),
        ("HIGH-SPEED PLATFORM", "a 500 km/h airframe flown autonomously at 300 km/h — new package, same loop"),
        ("PRODUCTION AIRCRAFT", "the same twin, policies and evidence, commissioned for the customer"),
    ]
    for i, (lbl, sub) in enumerate(chain):
        y = 58 + i * 84
        o.append(panel_box(650, y, 310, 62, lbl, sub=sub, size=8.8, sub_size=6.8,
                           stroke=RED if i == 1 else LINE3, fill=RED_W if i == 1 else BG,
                           sw=1.3 if i == 1 else 1, tcol=INK if i == 1 else INK2))
        if i < 2:
            o.append(arrow(805, y + 62, 805, y + 84, ns, "ink"))
    o.append(txt(650, 336, "WHAT TRAVELS WITH IT", 8.5, RED2, MONO, weight=700, ls="0.1em"))
    for i, c in enumerate(["IDENTIFICATION RIG", "TWIN ARCHITECTURE", "TRAINING PIPELINE", "EVIDENCE PACKAGES", "TEAM KNOWLEDGE"]):
        x = 650 + (i % 2) * 158
        y = 350 + (i // 2) * 34
        o.append(panel_box(x, y, 150, 28, c, size=6.6))
    o.append(txt(650, 462, "The network weights are per-airframe. The pipeline is permanent.", 10.5, INK3, SANS))
    o.append("</svg>")
    return "".join(o)


# ══════════════════════════════════════════════════════════════════════
# 10 · THE COMPOUNDING LOOPS, THE POSITION MAP, THE ROUTE MAP
# ══════════════════════════════════════════════════════════════════════
def compound_loops():
    W, H = 1000, 620
    ns = "cl"
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="The compounding loops: flight data and hardware feed engineering, industry and distribution, and each delivered programme returns more units, data and capital">',
         defs_arrow(ns, {"ink": INK4, "red": RED2, "grey": LINE3})]

    o.append(panel_box(260, 40, 480, 48, "FLIGHT DATA / HARDWARE",
                       "WHAT A DELIVERED PROGRAMME RETURNS", stroke=LINE3, tcol=INK2,
                       sub_size=8.0, scol=INK4))
    o.append(arrow(500, 88, 500, 124, ns, "ink"))

    loops = [
        (124, "ENGINEERING LOOP", "faster iteration · better models", "reusable autonomy · qualification"),
        (252, "INDUSTRIAL LOOP", "seekers · propulsion · suppliers", "tooling · production · integration"),
        (380, "DISTRIBUTION LOOP", "export approvals · customers", "partners · field deployments"),
    ]
    for y, label, s1, s2 in loops:
        o.append(rect(260, y, 480, 92, LINE3, BG, 1))
        o.append(txt(500, y + 33, label, 12, INK, MONO, anchor="middle", weight=700, ls="0.14em"))
        o.append(txt(500, y + 57, s1, 8.8, INK3, MONO, anchor="middle"))
        o.append(txt(500, y + 71, s2, 8.8, INK3, MONO, anchor="middle"))

    o.append(arrow(500, 216, 500, 252, ns, "red"))
    o.append(arrow(500, 344, 500, 380, ns, "red"))
    o.append(arrow(500, 472, 500, 508, ns, "red"))

    o.append(rect(260, 508, 480, 74, RED, RED_W, 1.4))
    o.append(txt(500, 538, "MORE UNITS · MORE DATA · MORE CAPITAL", 10.5, INK, MONO,
                 anchor="middle", weight=700, ls="0.1em"))
    o.append(txt(500, 558, "the next programme starts from a higher base", 8.4, INK3, MONO, anchor="middle"))

    o.append(f'<path d="M740,545 H880 V64 H740" fill="none" stroke="{RED2}" stroke-width="1.2" '
             f'stroke-dasharray="5 5" marker-end="url(#{ns}-red)"/>')
    o.append(txt(810, 56, "NEXT PROGRAMME", 8.5, RED2, MONO, anchor="middle", weight=700, ls="0.12em"))
    o.append("</svg>")
    return "".join(o)


def position_map():
    W, H = 1000, 620
    L, R, T, B = 120, 920, 80, 520
    midx, midy = (L + R) / 2, (T + B) / 2
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="Position map: development cadence against unit cost, bubble size showing system sophistication, with Apollyon in the high-cadence expendable quadrant">']

    o.append(f'<rect x="{L}" y="{T}" width="{midx - L}" height="{midy - T}" fill="{RED_W}" fill-opacity="0.5"/>')
    o.append(line(L, T, L, B, LINE2, 1.2))
    o.append(line(L, B, R, B, LINE2, 1.2))
    o.append(line(midx, T, midx, B, LINE, 1, dash="4 4"))
    o.append(line(L, midy, R, midy, LINE, 1, dash="4 4"))

    o.append(f'<text transform="translate({L - 58},{midy}) rotate(-90)" font-family="{MONO}" '
             f'font-size="9.5" fill="{INK4}" text-anchor="middle" letter-spacing="0.14em">DEVELOPMENT &amp; UPDATE CADENCE</text>')
    o.append(txt(L, B + 30, "LOW UNIT COST · EXPENDABLE", 9, INK4, MONO, ls="0.1em"))
    o.append(txt(R, B + 30, "HIGH UNIT COST · EXQUISITE", 9, INK4, MONO, anchor="end", ls="0.1em"))
    o.append(txt(midx, B + 52, "UNIT COST", 9.5, INK4, MONO, anchor="middle", ls="0.16em"))

    bubbles = [
        (300, 190, 46, "APOLLYON", "high cadence · expendable", True),
        (710, 210, 56, "WESTERN NEO-PRIMES", None, False),
        (300, 420, 44, "MASS PRODUCTION", "Geran · Peklo class", False),
        (710, 415, 66, "MBDA · KONGSBERG", None, False),
    ]
    for cx, cy, r, name, sub, hot in bubbles:
        if hot:
            o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{RED_W}" stroke="{RED}" stroke-width="1.6"/>')
            o.append(txt(cx, cy + r + 24, name, 11.5, RED2, MONO, anchor="middle", weight=700, ls="0.1em"))
        else:
            o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{BG}" stroke="{LINE3}" stroke-width="1.3"/>')
            o.append(txt(cx, cy + r + 22, name, 10.5, INK2, MONO, anchor="middle"))
        if sub:
            o.append(txt(cx, cy + r + 38, sub, 8.5, INK4, MONO, anchor="middle"))

    o.append(txt(L, 600, "BUBBLE SIZE = SYSTEM SOPHISTICATION · AXES ARE QUALITATIVE", 9, INK4, MONO, ls="0.08em"))
    o.append("</svg>")
    return "".join(o)


def tonbo_routes():
    W, H = 1000, 560
    ns = "tr"
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="Tonbo fielded markets reached from India: Armenia, Europe, North America, North Africa and Peru">',
         defs_arrow(ns, {"ink": INK4, "red": RED2, "grey": LINE3})]

    nodes = {
        "na": (60, 70, 200, 58, "NORTH AMERICA", "tier-one partnerships", False),
        "eu": (700, 70, 240, 58, "EUROPE", "tier-one partnerships", False),
        "in": (420, 268, 160, 58, "INDIA", "Tonbo · Apollyon", True),
        "am": (760, 210, 200, 58, "ARMENIA", "Volt · Spartan-S · thermal optics", False),
        "af": (660, 430, 250, 58, "NORTH AFRICA", "$25m border surveillance", False),
        "pe": (140, 430, 240, 58, "PERU", "army night-vision suites", False),
    }

    edges = [
        ((580, 292), (760, 245)),
        ((568, 268), (750, 128)),
        ((450, 268), (240, 128)),
        ((560, 326), (660, 455)),
        ((440, 326), (380, 450)),
    ]
    for (x1, y1), (x2, y2) in edges:
        o.append(arrow(x1, y1, x2, y2, ns, "grey"))

    for key, (x, y, w, h, label, sub, hot) in nodes.items():
        if hot:
            o.append(panel_box(x, y, w, h, label, sub, stroke=RED, fill=RED_W, sw=1.4,
                               tcol=INK, sub_size=8.0, scol=INK3))
        else:
            o.append(panel_box(x, y, w, h, label, sub, stroke=LINE3, fill=BG,
                               tcol=INK2, sub_size=8.0, scol=INK4))

    o.append(txt(40, 538, "FIELDED MARKETS · 15+ YEARS · 24 COUNTRIES", 9, INK4, MONO, ls="0.1em"))
    o.append("</svg>")
    return "".join(o)


VISUALS = {
    "war_inversions": war_inversions,
    "cost_curve": cost_curve,
    "strike_family": strike_family,
    "ahuti_speed": ahuti_speed,
    "india_production": india_production,
    "india_exports": india_exports,
    "arch_vehicle": arch_vehicle,
    "arch_software": arch_software,
    "cortex_stack": cortex_stack,
    "salvo_curve": salvo_curve,
    "eng_system": eng_system,
    "eng_twin": eng_twin,
    "eng_latency": eng_latency,
    "eng_convergence": eng_convergence,
    "compound_loops": compound_loops,
    "position_map": position_map,
    "tonbo_routes": tonbo_routes,
}


def main():
    os.makedirs(OUT, exist_ok=True)
    inline = {}
    for name, fn in VISUALS.items():
        svg = fn()
        open(os.path.join(OUT, f"{name}.svg"), "w", encoding="utf-8").write(svg)
        inline[name] = svg
        print(f"wrote assets/{name}.svg  ({len(svg):,} bytes)")
    json.dump(inline, open(os.path.join(OUT, "visuals.json"), "w", encoding="utf-8"))
    print("wrote assets/visuals.json")


if __name__ == "__main__":
    main()
