"""Rebuild all wiki visualizations in CFB / Cost-Curve brutalist language.
Black #060606, bone #F2EFE9, hairline #222, single red #D92323.
No gradients, no glow, no rounded cards.
"""
import math, os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
BONE = "#F2EFE9"
MUT = "#8A8781"
DIM = "#5A5854"
GRID = "#1E1E1E"
GREY = "#8f8f8f"
RED = "#D92323"
REDB = "#E83131"

MONO = "JetBrains Mono, monospace"
SANS = "Inter, sans-serif"


def cost_curve():
    W, H = 1200, 640
    pl, pr, pt, pb = 110, 60, 200, 90
    pw, ph = W - pl - pr, H - pt - pb
    # x linear 80..2150, y log 60..14000
    xmin, xmax = 80, 2150
    ymin_l, ymax_l = math.log10(60), math.log10(14000)

    def tx(v):
        return pl + (v - xmin) / (xmax - xmin) * pw
    def ty(v):
        return pt + ph - (math.log10(v) - ymin_l) / (ymax_l - ymin_l) * ph

    comp = [
        ("Berkut-BM", 150, 4500),
        ("Barracuda-250", 375, 3100),
        ("Barracuda-500", 950, 450),
        ("Tomahawk", 1600, 430),
    ]
    apol = [
        ("Nightshade Mk II", 300, 2700),
        ("Nightshade Mk III", 500, 1500),
        ("Hemlock Mk I", 1000, 320),
        ("Hemlock Mk II", 1500, 32),
    ]
    s = []
    s.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="auto">')
    s.append(f'<rect width="{W}" height="{H}" fill="#060606"/>')
    # kicker
    s.append(f'<text x="48" y="48" fill="{RED}" font-family="{MONO}" font-size="13" font-weight="700" letter-spacing="0.08em">THE COST CURVE</text>')
    s.append(f'<line x1="48" y1="60" x2="96" y2="60" stroke="{RED}" stroke-width="2.5"/>')
    s.append(f'<text x="48" y="112" fill="{BONE}" font-family="{SANS}" font-size="42" font-weight="800" letter-spacing="-0.02em">Cost per kg-km, by range.</text>')
    # formula box + note
    s.append(f'<rect x="48" y="132" width="560" height="48" fill="none" stroke="#2b2b2b" stroke-width="1"/>')
    s.append(f'<text x="66" y="161" fill="{MUT}" font-family="{SANS}" font-size="14">Cost per kg-km&#160;&#160;=</text>')
    s.append(f'<text x="238" y="153" fill="{BONE}" font-family="{SANS}" font-size="14" font-weight="600">unit cost (INR)</text>')
    s.append(f'<line x1="238" y1="159" x2="560" y2="159" stroke="{BONE}" stroke-width="1"/>')
    s.append(f'<text x="238" y="174" fill="{BONE}" font-family="{SANS}" font-size="14" font-weight="600">payload (kg) × range (km)</text>')
    s.append(f'<text x="660" y="153" fill="{MUT}" font-family="{SANS}" font-size="13">Both axes logarithmic on cost. Range linear.</text>')
    s.append(f'<text x="660" y="172" fill="{MUT}" font-family="{SANS}" font-size="13">Comparator prices from public sources.</text>')
    # grid: y log ticks
    for yv in [100, 200, 500, 1000, 2000, 5000, 10000]:
        py = ty(yv)
        major = yv in (100, 1000, 10000)
        s.append(f'<line x1="{pl}" y1="{py:.1f}" x2="{W-pr}" y2="{py:.1f}" stroke="{"#2b2b2b" if major else GRID}" stroke-width="1"/>')
        if major:
            s.append(f'<text x="{pl-12}" y="{py+4:.1f}" fill="{BONE}" font-family="{MONO}" font-size="12" text-anchor="end">{yv:,}</text>')
    for yv in [60, 80, 150, 300, 700, 1500, 3000, 7000, 14000]:
        py = ty(yv)
        s.append(f'<line x1="{pl}" y1="{py:.1f}" x2="{pl+8}" y2="{py:.1f}" stroke="#2b2b2b" stroke-width="1"/>')
    # x ticks
    for xv in [150, 300, 500, 1000, 1500, 2000]:
        px = tx(xv)
        s.append(f'<line x1="{px:.1f}" y1="{pt}" x2="{px:.1f}" y2="{pt+ph}" stroke="{GRID}" stroke-width="1"/>')
        s.append(f'<text x="{px:.1f}" y="{pt+ph+24}" fill="{MUT}" font-family="{MONO}" font-size="12" text-anchor="middle">{xv:,}</text>')
    s.append(f'<text x="{pl+pw/2}" y="{pt+ph+52}" fill="{BONE}" font-family="{SANS}" font-size="14" text-anchor="middle">Range (km)</text>')
    s.append(f'<text x="30" y="{pt+ph/2}" fill="{MUT}" font-family="{SANS}" font-size="14" text-anchor="middle" transform="rotate(-90 30 {pt+ph/2})">Cost per kg-km (INR)</text>')
    # lower-is-better arrow
    s.append(f'<line x1="{pl-52}" y1="{pt+60}" x2="{pl-52}" y2="{pt+ph-40}" stroke="{DIM}" stroke-width="1"/>')
    s.append(f'<text x="{pl-46}" y="{pt+ph-60}" fill="{DIM}" font-family="{MONO}" font-size="10" transform="rotate(-90 {pl-46} {pt+ph-60})" text-anchor="middle">lower is better ↓</text>')
    # comparator line
    pts = " ".join(f"{tx(x):.1f},{ty(y):.1f}" for _, x, y in comp)
    s.append(f'<polyline points="{pts}" fill="none" stroke="{GREY}" stroke-width="2"/>')
    for name, x, y in comp:
        px, py = tx(x), ty(y)
        s.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="6" fill="#060606" stroke="{GREY}" stroke-width="2"/>')
        # label above
        s.append(f'<text x="{px:.1f}" y="{py-18:.1f}" fill="{MUT}" font-family="{SANS}" font-size="13" text-anchor="middle">{name}</text>')
    # apollyon line
    apts = " ".join(f"{tx(x):.1f},{ty(y):.1f}" for _, x, y in apol)
    s.append(f'<polyline points="{apts}" fill="none" stroke="{RED}" stroke-width="2.5"/>')
    for name, x, y in apol:
        px, py = tx(x), ty(y)
        s.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="6.5" fill="{RED}" stroke="{RED}" stroke-width="2"/>')
    # apollyon labels (offset to avoid overlap, like reference)
    offs = {
        "Nightshade Mk II": (-128, 30),
        "Nightshade Mk III": (16, -14),
        "Hemlock Mk I": (18, -12),
        "Hemlock Mk II": (-132, -14),
    }
    for name, x, y in apol:
        dx, dy = offs[name]
        px, py = tx(x), ty(y)
        s.append(f'<text x="{px+dx:.1f}" y="{py+dy:.1f}" fill="{REDB}" font-family="{SANS}" font-size="14" font-weight="700">{name}</text>')
    # legend top right of plot
    lx, ly = W - pr - 330, pt + 8
    s.append(f'<line x1="{lx}" y1="{ly}" x2="{lx+28}" y2="{ly}" stroke="{GREY}" stroke-width="2"/>')
    s.append(f'<circle cx="{lx+14}" cy="{ly}" r="5" fill="#060606" stroke="{GREY}" stroke-width="2"/>')
    s.append(f'<text x="{lx+38}" y="{ly+5}" fill="{MUT}" font-family="{SANS}" font-size="13">Comparators in service</text>')
    s.append(f'<line x1="{lx}" y1="{ly+24}" x2="{lx+28}" y2="{ly+24}" stroke="{RED}" stroke-width="2.5"/>')
    s.append(f'<circle cx="{lx+14}" cy="{ly+24}" r="5.5" fill="{RED}"/>')
    s.append(f'<text x="{lx+38}" y="{ly+29}" fill="{REDB}" font-family="{SANS}" font-size="13" font-weight="700">Apollyon long-range strike family</text>')
    # footer hairline
    fy = H - 34
    s.append(f'<line x1="48" y1="{fy}" x2="{W-48}" y2="{fy}" stroke="{GRID}" stroke-width="1"/>')
    s.append(f'<text x="48" y="{fy+22}" fill="{DIM}" font-family="{MONO}" font-size="10">APOLLYON DYNAMICS&#160;&#160;|&#160;&#160;USD 1 = INR 95&#160;&#160;|&#160;&#160;Berkut-BM unit cost estimated; no public figure</text>')
    s.append(f'<text x="{W-48}" y="{fy+22}" fill="{DIM}" font-family="{MONO}" font-size="10" text-anchor="end">01</text>')
    s.append('</svg>')
    open(os.path.join(OUT, "apollyon_cost_curve_dark.svg"), "w").write("\n".join(s))
    print("cost curve ok")


def modern_warfare():
    W, H = 1200, 800
    s = []
    s.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="auto">')
    s.append(f'<rect width="{W}" height="{H}" fill="#060606"/>')
    s.append(f'<text x="48" y="52" fill="{RED}" font-family="{MONO}" font-size="13" font-weight="700" letter-spacing="0.08em">MODERN WARFARE</text>')
    s.append(f'<line x1="48" y1="64" x2="96" y2="64" stroke="{RED}" stroke-width="2.5"/>')
    s.append(f'<text x="48" y="118" fill="{BONE}" font-family="{SANS}" font-size="44" font-weight="800" letter-spacing="-0.025em">The war changed shape.</text>')
    s.append(f'<text x="48" y="148" fill="{MUT}" font-family="{SANS}" font-size="15">Three inversions observed in Ukraine, the Red Sea, and Nagorno-Karabakh. Each row reads past → present.</text>')
    # three shift rows
    rows = [
        ("01", "MANNED → TELE-OPERATED → AUTONOMOUS", "Pilots and $80M jets give way to RF-fragile FPVs, then to edge-AI weapons that fly with zero link.", "EDGE-AI"),
        ("02", "SCARCE → DISPOSABLE → ATTRITABLE", "18-month prime backlogs lose to automotive-cadence salvo production measured in thousands/month.", "MASS"),
        ("03", "PERMISSIVE → JAMMED → DENIED", "A jammer every ~10 km on the FLOT. >80% of GNSS denied. Only onboard autonomy reaches target.", "DENIED"),
    ]
    y = 190
    for num, big, detail, tag in rows:
        s.append(f'<line x1="48" y1="{y}" x2="{W-48}" y2="{y}" stroke="{GRID}" stroke-width="1"/>')
        s.append(f'<text x="48" y="{y+36}" fill="{DIM}" font-family="{MONO}" font-size="12">{num}</text>')
        s.append(f'<text x="48" y="{y+68}" fill="{BONE}" font-family="{SANS}" font-size="30" font-weight="800" letter-spacing="-0.02em">{big}</text>')
        s.append(f'<text x="48" y="{y+94}" fill="{MUT}" font-family="{SANS}" font-size="14">{detail}</text>')
        s.append(f'<text x="{W-48}" y="{y+36}" fill="{RED}" font-family="{MONO}" font-size="11" font-weight="700" text-anchor="end">{tag}</text>')
        y += 122
    # cost asymmetry block
    y += 6
    s.append(f'<line x1="48" y1="{y}" x2="{W-48}" y2="{y}" stroke="{GRID}" stroke-width="1"/>')
    s.append(f'<text x="48" y="{y+32}" fill="{RED}" font-family="{MONO}" font-size="11" font-weight="700">COST ASYMMETRY · THE 1:100 TRAP</text>')
    # two bars: attritable vs interceptor (log-ish widths)
    by = y + 52
    # attritable bar (short)
    s.append(f'<text x="48" y="{by}" fill="{MUT}" font-family="{MONO}" font-size="11">ATTRITABLE STRIKE · SHAHED / NIGHTSHADE CLASS</text>')
    s.append(f'<rect x="48" y="{by+10}" width="180" height="14" fill="{BONE}"/>')
    s.append(f'<text x="48" y="{by+52}" fill="{BONE}" font-family="{SANS}" font-size="30" font-weight="800">₹15–35 LAKH</text>')
    s.append(f'<text x="280" y="{by+52}" fill="{MUT}" font-family="{SANS}" font-size="14">$20–40k · 1,000s per month</text>')
    # interceptor bar (long)
    iy = by + 76
    s.append(f'<text x="48" y="{iy}" fill="{MUT}" font-family="{MONO}" font-size="11">LEGACY INTERCEPTOR · PATRIOT / SM-2 / ASTER CLASS</text>')
    s.append(f'<rect x="48" y="{iy+10}" width="880" height="14" fill="none" stroke="{RED}" stroke-width="1.5"/>')
    s.append(f'<rect x="48" y="{iy+10}" width="880" height="14" fill="{RED}" opacity="0.25"/>')
    s.append(f'<text x="48" y="{iy+52}" fill="{REDB}" font-family="{SANS}" font-size="30" font-weight="800">₹18–35 CRORE</text>')
    s.append(f'<text x="300" y="{iy+52}" fill="{MUT}" font-family="{SANS}" font-size="14">$2–4M · 18–36 month lead time</text>')
    s.append(f'<text x="{W-48}" y="{by+52}" fill="{DIM}" font-family="{MONO}" font-size="11" text-anchor="end">SOURCE: RUSI / CSIS · APOLLYON EST.</text>')
    s.append('</svg>')
    open(os.path.join(OUT, "modern_warfare_shifts_dark.svg"), "w").write("\n".join(s))
    print("modern warfare ok")


def india_chart(fname, kicker, title, big, suffix, data, callout1, callout2, footnote, num):
    W, H = 600, 400
    pl, pr, pt, pb = 64, 28, 108, 60
    pw, ph = W - pl - pr, H - pt - pb
    vals = [v for _, v, _ in data]
    mn, mx = 0, max(vals) * 1.12
    n = len(data)
    def tx(i): return pl + i * (pw / (n - 1))
    def ty(v): return pt + ph - (v - mn) / (mx - mn) * ph
    s = []
    s.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="auto">')
    s.append(f'<rect width="{W}" height="{H}" fill="#060606"/>')
    s.append(f'<text x="24" y="34" fill="{RED}" font-family="{MONO}" font-size="11" font-weight="700">{kicker}</text>')
    s.append(f'<text x="24" y="62" fill="{BONE}" font-family="{SANS}" font-size="21" font-weight="800" letter-spacing="-0.015em">{title}</text>')
    s.append(f'<text x="24" y="94" fill="{BONE}" font-family="{SANS}" font-size="34" font-weight="800" letter-spacing="-0.02em">{big}<tspan fill="{MUT}" font-size="14" font-weight="400">  {suffix}</tspan></text>')
    # gridlines: 3
    import math as m
    step = mx / 3
    mag = 10 ** m.floor(m.log10(step))
    step = mag * (1 if step / mag < 1.5 else (2 if step / mag < 3.5 else 5))
    v = step
    while v < mx:
        py = ty(v)
        s.append(f'<line x1="{pl}" y1="{py:.1f}" x2="{W-pr}" y2="{py:.1f}" stroke="{GRID}" stroke-width="1"/>')
        if v >= 1000:
            lab = f"₹{v/100000:.1f}L Cr" if v >= 100000 else f"₹{v/1000:.0f}k Cr" if v >= 10000 else f"₹{v:,.0f} Cr"
        else:
            lab = f"₹{v:,.0f} Cr"
        s.append(f'<text x="{pl-8}" y="{py+4:.1f}" fill="{DIM}" font-family="{MONO}" font-size="9" text-anchor="end">{lab}</text>')
        v += step
    pts = " ".join(f"{tx(i):.1f},{ty(v):.1f}" for i, (_, v, _) in enumerate(data))
    s.append(f'<polyline points="{pts}" fill="none" stroke="{BONE}" stroke-width="2"/>')
    for i, (yr, v, lab) in enumerate(data):
        px, py = tx(i), ty(v)
        last = i == n - 1
        s.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{5 if last else 3.5}" fill="{RED if last else "#060606"}" stroke="{RED if last else MUT}" stroke-width="1.5"/>')
        if last or i == 0:
            anchor = "end" if last else "start"
            xx = px - 8 if last else px + 8
            s.append(f'<text x="{xx:.1f}" y="{py-10:.1f}" fill="{BONE if last else MUT}" font-family="{MONO}" font-size="{"11" if last else "9"}" font-weight="{"700" if last else "400"}" text-anchor="{anchor}">{lab}</text>')
        s.append(f'<text x="{px:.1f}" y="{pt+ph+22}" fill="{DIM}" font-family="{MONO}" font-size="10" text-anchor="middle">{yr}</text>')
    s.append(f'<text x="24" y="{H-30}" fill="{MUT}" font-family="{SANS}" font-size="11">{callout1}</text>')
    s.append(f'<text x="24" y="{H-14}" fill="{DIM}" font-family="{SANS}" font-size="11">{callout2}</text>')
    s.append(f'<line x1="24" y1="{H-44}" x2="{W-24}" y2="{H-44}" stroke="{GRID}" stroke-width="1"/>')
    s.append('</svg>')
    open(os.path.join(OUT, fname), "w").write("\n".join(s))
    print(fname, "ok")


if __name__ == "__main__":
    cost_curve()
    modern_warfare()
    india_chart(
        "india_defence_production_dark.svg",
        "INDIA · DOMESTIC PRODUCTION",
        "Defence production, FY21 → FY26",
        "₹1.78 LAKH CR",
        "4.1× since FY14",
        [("FY21", 84643, "₹84.6k Cr"), ("FY22", 94845, ""), ("FY23", 108684, ""),
         ("FY24", 127435, ""), ("FY25", 151339, ""), ("FY26", 178000, "₹1,78,000 Cr")],
        "75% of FY27 capital (₹1.39L Cr) reserved for domestic industry.",
        "Source: MoD / DDP. FY14 base ₹43,746 Cr.",
        "02", 2,
    )
    india_chart(
        "india_defence_exports_dark.svg",
        "INDIA · EXPORT FOOTPRINT",
        "Defence exports, FY14 → FY26",
        "₹38,424 CR",
        "56× in 12 years",
        [("FY14", 686, "₹686 Cr"), ("FY18", 4682, ""), ("FY21", 8435, ""),
         ("FY23", 15918, ""), ("FY25", 23622, ""), ("FY26", 38424, "₹38,424 Cr")],
        "Private share 45.16% · 145 firms · 80+ nations.",
        "Source: DDP series, MoD April 2026.",
        "03", 3,
    )
