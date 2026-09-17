import math
import os

os.makedirs('wiki/assets', exist_ok=True)

def generate_cost_curve():
    w, h = 920, 520
    pad_l, pad_r, pad_t, pad_b = 90, 40, 60, 70
    plot_w = w - pad_l - pad_r
    plot_h = h - pad_t - pad_b
    
    min_x, max_x = math.log10(100), math.log10(2500)
    min_y, max_y = math.log10(20), math.log10(12000)
    
    def tx(val):
        return pad_l + (math.log10(val) - min_x) / (max_x - min_x) * plot_w
    def ty(val):
        return pad_t + plot_h - (math.log10(val) - min_y) / (max_y - min_y) * plot_h

    comparators = [
        ("Berkut-BM", 150, 4500, "150 km · ~₹4,500"),
        ("Barracuda-250", 375, 3100, "375 km · ~₹3,100"),
        ("Barracuda-500", 950, 450, "950 km · ~₹450"),
        ("Tomahawk", 1600, 430, "1,600 km · ~₹430")
    ]
    
    apollyon = [
        ("Nightshade Mk II", 300, 2700, "₹2,700/kg·km", "4,500 kg·km"),
        ("Nightshade Mk III", 500, 1500, "₹1,500/kg·km", "12,500 kg·km"),
        ("Hemlock Mk I", 1000, 300, "₹300/kg·km", "75,000 kg·km"),
        ("Hemlock Mk II", 1500, 35, "₹35/kg·km", "1.5M kg·km")
    ]
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="auto">')
    svg.append('<defs>')
    svg.append('''
      <linearGradient id="bg-grad" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#090d16"/>
        <stop offset="100%" stop-color="#05070a"/>
      </linearGradient>
      <linearGradient id="apol-line" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0%" stop-color="#ff453a"/>
        <stop offset="100%" stop-color="#ff3b30"/>
      </linearGradient>
      <linearGradient id="apol-glow" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="rgba(255, 59, 48, 0.25)"/>
        <stop offset="100%" stop-color="rgba(255, 59, 48, 0.0)"/>
      </linearGradient>
      <filter id="glow-red" x="-20%" y="-20%" width="140%" height="140%">
        <feGaussianBlur stdDeviation="3" result="blur" />
        <feComposite in="SourceGraphic" in2="blur" operator="over" />
      </filter>
    ''')
    svg.append('</defs>')
    
    svg.append(f'<rect width="{w}" height="{h}" rx="8" fill="url(#bg-grad)" stroke="#151c2a" stroke-width="1"/>')
    svg.append('<text x="36" y="34" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="11" font-weight="700" letter-spacing="0.12em">THE COST CURVE · STRIKE ENVELOPE METRIC</text>')
    svg.append('<text x="36" y="52" fill="#e9edf2" font-family="Inter, sans-serif" font-size="16" font-weight="700">Cost per kg-km by Range (Log-Log Scale)</text>')
    
    svg.append(f'<g transform="translate({w - 380}, 20)">')
    svg.append('<rect width="344" height="42" rx="4" fill="#0c121e" stroke="#1f293d" stroke-width="1"/>')
    svg.append('<text x="14" y="26" fill="#8e9aa8" font-family="JetBrains Mono, monospace" font-size="11">Cost per kg·km = </text>')
    svg.append('<text x="140" y="19" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="11" font-weight="600">unit cost (INR)</text>')
    svg.append('<line x1="140" y1="24" x2="330" y2="24" stroke="#38bdf8" stroke-width="1"/>')
    svg.append('<text x="140" y="36" fill="#8e9aa8" font-family="JetBrains Mono, monospace" font-size="10.5">payload (kg) × range (km)</text>')
    svg.append('</g>')
    
    x_ticks = [100, 150, 300, 500, 1000, 1500, 2000]
    for xt in x_ticks:
        px = tx(xt)
        svg.append(f'<line x1="{px}" y1="{pad_t}" x2="{px}" y2="{pad_t + plot_h}" stroke="#141a27" stroke-width="1" stroke-dasharray="3,3"/>')
        svg.append(f'<text x="{px}" y="{pad_t + plot_h + 20}" fill="#8e9aa8" font-family="JetBrains Mono, monospace" font-size="10.5" text-anchor="middle">{xt:,}</text>')
    svg.append(f'<text x="{pad_l + plot_w/2}" y="{pad_t + plot_h + 46}" fill="#64748b" font-family="JetBrains Mono, monospace" font-size="11" text-anchor="middle">Operational Range (km) &rarr;</text>')

    y_ticks = [20, 50, 100, 300, 1000, 3000, 10000]
    for yt in y_ticks:
        py = ty(yt)
        svg.append(f'<line x1="{pad_l}" y1="{py}" x2="{pad_l + plot_w}" y2="{py}" stroke="#141a27" stroke-width="1"/>')
        if yt in [100, 1000, 10000]:
            svg.append(f'<text x="{pad_l - 12}" y="{py + 4}" fill="#e9edf2" font-family="JetBrains Mono, monospace" font-size="10.5" font-weight="600" text-anchor="end">₹{yt:,}</text>')
        else:
            svg.append(f'<text x="{pad_l - 12}" y="{py + 4}" fill="#64748b" font-family="JetBrains Mono, monospace" font-size="9.5" text-anchor="end">{yt:,}</text>')
    
    svg.append(f'<g transform="translate(24, {pad_t + plot_h/2}) rotate(-90)">')
    svg.append('<text x="0" y="0" fill="#8e9aa8" font-family="JetBrains Mono, monospace" font-size="11" text-anchor="middle">Cost per kg·km (INR) &larr;</text>')
    svg.append('</g>')
    
    svg.append(f'<g transform="translate({pad_l + 16}, {pad_t + plot_h - 100})">')
    svg.append('<line x1="0" y1="0" x2="0" y2="70" stroke="#38bdf8" stroke-width="1.5"/>')
    svg.append('<path d="M -4 64 L 0 72 L 4 64 Z" fill="#38bdf8"/>')
    svg.append('<text x="8" y="40" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="10" font-weight="600" transform="rotate(-90 8 40)">LOWER IS BETTER</text>')
    svg.append('</g>')
    
    comp_pts = [f"{tx(x):.1f},{ty(y):.1f}" for _, x, y, _ in comparators]
    svg.append(f'<polyline points="{" ".join(comp_pts)}" fill="none" stroke="#64748b" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>')
    for name, x, y, note in comparators:
        px, py = tx(x), ty(y)
        svg.append(f'<circle cx="{px}" cy="{py}" r="5" fill="#1e293b" stroke="#94a3b8" stroke-width="2"/>')
        dy = -14
        dx = -10 if name == "Berkut-BM" else (10 if name == "Tomahawk" else 0)
        ha = "end" if name == "Berkut-BM" else ("start" if name == "Tomahawk" else "middle")
        svg.append(f'<text x="{px + dx}" y="{py + dy}" fill="#94a3b8" font-family="Inter, sans-serif" font-size="11" font-weight="600" text-anchor="{ha}">{name}</text>')
        svg.append(f'<text x="{px + dx}" y="{py + dy + 12}" fill="#64748b" font-family="JetBrains Mono, monospace" font-size="9.5" text-anchor="{ha}">{note}</text>')
    
    apol_pts = [f"{tx(x):.1f},{ty(y):.1f}" for _, x, y, _, _ in apollyon]
    area_pts = [f"{tx(apollyon[0][1]):.1f},{pad_t + plot_h}"] + apol_pts + [f"{tx(apollyon[-1][1]):.1f},{pad_t + plot_h}"]
    svg.append(f'<polygon points="{" ".join(area_pts)}" fill="url(#apol-glow)"/>')
    svg.append(f'<polyline points="{" ".join(apol_pts)}" fill="none" stroke="url(#apol-line)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')
    
    for name, x, y, note, env in apollyon:
        px, py = tx(x), ty(y)
        svg.append(f'<circle cx="{px}" cy="{py}" r="6.5" fill="#ff3b30" stroke="#ffffff" stroke-width="2" filter="url(#glow-red)"/>')
        
        if name == "Nightshade Mk II":
            svg.append(f'<text x="{px - 14}" y="{py + 6}" fill="#ff453a" font-family="Inter, sans-serif" font-size="12" font-weight="700" text-anchor="end">{name}</text>')
            svg.append(f'<text x="{px - 14}" y="{py + 20}" fill="#cbd5e1" font-family="JetBrains Mono, monospace" font-size="10" text-anchor="end">₹2,700/kg·km · {env}</text>')
        elif name == "Nightshade Mk III":
            svg.append(f'<text x="{px - 14}" y="{py + 6}" fill="#ff453a" font-family="Inter, sans-serif" font-size="12" font-weight="700" text-anchor="end">{name}</text>')
            svg.append(f'<text x="{px - 14}" y="{py + 20}" fill="#cbd5e1" font-family="JetBrains Mono, monospace" font-size="10" text-anchor="end">₹1,500/kg·km · {env}</text>')
        elif name == "Hemlock Mk I":
            svg.append(f'<text x="{px + 14}" y="{py - 6}" fill="#ff453a" font-family="Inter, sans-serif" font-size="12" font-weight="700" text-anchor="start">{name}</text>')
            svg.append(f'<text x="{px + 14}" y="{py + 8}" fill="#cbd5e1" font-family="JetBrains Mono, monospace" font-size="10" text-anchor="start">₹300/kg·km · {env}</text>')
        elif name == "Hemlock Mk II":
            svg.append(f'<text x="{px - 14}" y="{py - 6}" fill="#ff453a" font-family="Inter, sans-serif" font-size="12" font-weight="700" text-anchor="end">{name}</text>')
            svg.append(f'<text x="{px - 14}" y="{py + 8}" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="10.5" font-weight="700" text-anchor="end">₹35/kg·km · 1.5M kg·km</text>')
            
    leg_x = pad_l + plot_w - 240
    leg_y = pad_t + 30
    svg.append(f'<g transform="translate({leg_x}, {leg_y})">')
    svg.append('<rect width="230" height="60" rx="4" fill="#0c121e" stroke="#1f293d" opacity="0.95"/>')
    svg.append('<line x1="14" y1="18" x2="38" y2="18" stroke="#64748b" stroke-width="2"/>')
    svg.append('<circle cx="26" cy="18" r="4" fill="#1e293b" stroke="#94a3b8" stroke-width="1.5"/>')
    svg.append('<text x="48" y="22" fill="#94a3b8" font-family="Inter, sans-serif" font-size="11">Comparators in service</text>')
    svg.append('<line x1="14" y1="42" x2="38" y2="42" stroke="#ff3b30" stroke-width="2.5"/>')
    svg.append('<circle cx="26" cy="42" r="5" fill="#ff3b30" stroke="#ffffff" stroke-width="1.5"/>')
    svg.append('<text x="48" y="46" fill="#ff453a" font-family="Inter, sans-serif" font-size="11" font-weight="700">Apollyon Strike Family</text>')
    svg.append('</g>')

    svg.append(f'<text x="{pad_l}" y="{h - 16}" fill="#475569" font-family="JetBrains Mono, monospace" font-size="9.5">APOLLYON DYNAMICS INTERNAL REGISTER · USD 1 = INR 95 · COMPARATOR PRICING VIA PUBLIC ACQUISITION RECORDS · BERKUT-BM ESTIMATED</text>')
    svg.append('</svg>')
    
    with open('wiki/assets/apollyon_cost_curve_dark.svg', 'w') as f:
        f.write("\n".join(svg))
    print("Generated wiki/assets/apollyon_cost_curve_dark.svg")

def generate_modern_warfare_shifts():
    w, h = 920, 480
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="auto">')
    svg.append('<defs>')
    svg.append('''
      <linearGradient id="mw-bg" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#090d16"/>
        <stop offset="100%" stop-color="#05070a"/>
      </linearGradient>
      <linearGradient id="red-card" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#190e12"/>
        <stop offset="100%" stop-color="#0d080a"/>
      </linearGradient>
      <linearGradient id="cyan-card" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#0c1724"/>
        <stop offset="100%" stop-color="#060b12"/>
      </linearGradient>
    ''')
    svg.append('</defs>')
    
    svg.append(f'<rect width="{w}" height="{h}" rx="8" fill="url(#mw-bg)" stroke="#151c2a" stroke-width="1"/>')
    
    svg.append('<text x="36" y="34" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="11" font-weight="700" letter-spacing="0.12em">TACTICAL INFOGRAPHIC · DOCTRINE INFLECTION</text>')
    svg.append('<text x="36" y="54" fill="#e9edf2" font-family="Inter, sans-serif" font-size="17" font-weight="700">The Modern Warfare Inversion: Autonomous Attrition vs Legacy Exquisiteness</text>')
    
    shifts = [
        ("01 · PLATFORM DOMAIN", "Manned Aircraft", "Tele-Operated UAS", "Autonomous Edge-AI", 
         "Exquisite pilots & jets ($80M+)", "Fragile RF datalinks & FPVs", "Independent optical & scene nav"),
        ("02 · REPLENISHMENT", "Exquisite / Scarce", "Semi-Disposable", "Mass Attritable",
         "Years to produce single units", "Vulnerable to supply shock", "Automotive-cadence production"),
        ("03 · ELECTROMAGNETIC", "Permissive Skies", "Occasional Jamming", "100% Contested FLOT",
         "Uninhibited GNSS & telemetry", "Spot EW interference", "Jammer every 10 km, >80% GNSS denial")
    ]
    
    card_w = 268
    for i, (tag, s1, s2, s3, d1, d2, d3) in enumerate(shifts):
        cx = 36 + i * (card_w + 22)
        cy = 78
        svg.append(f'<g transform="translate({cx}, {cy})">')
        svg.append(f'<rect width="{card_w}" height="185" rx="6" fill="#0b0f19" stroke="#1c2538" stroke-width="1"/>')
        svg.append(f'<text x="14" y="24" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700">{tag}</text>')
        
        svg.append('<circle cx="20" cy="54" r="4" fill="#64748b"/>')
        svg.append(f'<text x="32" y="52" fill="#94a3b8" font-family="Inter, sans-serif" font-size="11.5" font-weight="500">{s1}</text>')
        svg.append(f'<text x="32" y="65" fill="#64748b" font-family="JetBrains Mono, monospace" font-size="9">{d1}</text>')
        svg.append('<line x1="20" y1="62" x2="20" y2="86" stroke="#1e293b" stroke-width="1.5"/>')
        
        svg.append('<circle cx="20" cy="98" r="4" fill="#94a3b8"/>')
        svg.append(f'<text x="32" y="96" fill="#cbd5e1" font-family="Inter, sans-serif" font-size="11.5" font-weight="500">{s2}</text>')
        svg.append(f'<text x="32" y="109" fill="#64748b" font-family="JetBrains Mono, monospace" font-size="9">{d2}</text>')
        svg.append('<line x1="20" y1="106" x2="20" y2="130" stroke="#1e293b" stroke-width="1.5"/>')
        
        svg.append('<circle cx="20" cy="144" r="5" fill="#0a84ff" stroke="#38bdf8" stroke-width="1.5"/>')
        svg.append(f'<text x="32" y="142" fill="#38bdf8" font-family="Inter, sans-serif" font-size="12" font-weight="700">{s3}</text>')
        svg.append(f'<text x="32" y="156" fill="#94a3b8" font-family="JetBrains Mono, monospace" font-size="9.5">{d3}</text>')
        svg.append('</g>')
        
    bottom_y = 282
    bw = w - 72
    svg.append(f'<g transform="translate(36, {bottom_y})">')
    svg.append(f'<rect width="{bw}" height="165" rx="6" fill="#090d16" stroke="#1e293b" stroke-width="1"/>')
    
    svg.append('<rect x="16" y="16" width="370" height="132" rx="4" fill="url(#red-card)" stroke="#ef4444" stroke-opacity="0.3" stroke-width="1"/>')
    svg.append('<text x="32" y="38" fill="#f87171" font-family="JetBrains Mono, monospace" font-size="10.5" font-weight="700">ATTRITABLE STRIKE MUNITION (SHAHED / NIGHTSHADE Mk II)</text>')
    svg.append('<text x="32" y="74" fill="#ffffff" font-family="Inter, sans-serif" font-size="28" font-weight="800">₹15 – 35 Lakh <tspan font-size="15" font-weight="500" fill="#94a3b8">($20k – $40k USD)</tspan></text>')
    svg.append('<text x="32" y="98" fill="#cbd5e1" font-family="Inter, sans-serif" font-size="11.5">Commercial engines, stampable composites, COTS sensors.</text>')
    svg.append('<text x="32" y="116" fill="#f87171" font-family="JetBrains Mono, monospace" font-size="10.5">Manufacturable in batches of 1,000s / month · Salvo exhaustion weapon</text>')
    
    svg.append('<rect x="402" y="44" width="76" height="76" rx="38" fill="#141a27" stroke="#38bdf8" stroke-width="1.5"/>')
    svg.append('<text x="440" y="80" fill="#38bdf8" font-family="Inter, sans-serif" font-size="18" font-weight="800" text-anchor="middle">1 : 100</text>')
    svg.append('<text x="440" y="96" fill="#64748b" font-family="JetBrains Mono, monospace" font-size="8.5" text-anchor="middle">EXCHANGE RATIO</text>')
    
    svg.append('<rect x="494" y="16" width="338" height="132" rx="4" fill="url(#cyan-card)" stroke="#38bdf8" stroke-opacity="0.3" stroke-width="1"/>')
    svg.append('<text x="510" y="38" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="10.5" font-weight="700">LEGACY AIR DEFENCE INTERCEPTOR (PATRIOT / SM-2 / ASTER)</text>')
    svg.append('<text x="510" y="74" fill="#ffffff" font-family="Inter, sans-serif" font-size="28" font-weight="800">₹18 – 35 Crore <tspan font-size="15" font-weight="500" fill="#94a3b8">($2M – $4M USD)</tspan></text>')
    svg.append('<text x="510" y="98" fill="#cbd5e1" font-family="Inter, sans-serif" font-size="11.5">Exquisite aerospace mil-spec, 18-to-36 month production lead times.</text>')
    svg.append('<text x="510" y="116" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="10.5">The defender exhausts interceptor magazines before enemy exhausts strike drones</text>')
    svg.append('</g>')
    
    svg.append(f'<text x="36" y="{h - 10}" fill="#475569" font-family="JetBrains Mono, monospace" font-size="9">SOURCE: FRONT-LINE UKRAINE &amp; RED SEA COMBAT OBSERVATIONS (RUSI / CSIS) · APOLLYON TACTICAL ESTIMATES</text>')
    svg.append('</svg>')
    
    with open('wiki/assets/modern_warfare_shifts_dark.svg', 'w') as f:
        f.write("\n".join(svg))
    print("Generated wiki/assets/modern_warfare_shifts_dark.svg")

def generate_production_graph():
    w, h = 480, 320
    pad_l, pad_r, pad_t, pad_b = 60, 24, 64, 50
    plot_w = w - pad_l - pad_r
    plot_h = h - pad_t - pad_b
    
    data = [
        ("FY21", 84643, "₹84.6k Cr"),
        ("FY22", 94845, "₹94.8k Cr"),
        ("FY23", 108684, "₹108.7k Cr"),
        ("FY24", 127435, "₹127.4k Cr"),
        ("FY25", 151339, "₹151.3k Cr"),
        ("FY26", 178000, "₹1.78 Lakh Cr")
    ]
    
    min_val, max_val = 60000, 195000
    n = len(data)
    
    def tx(i):
        return pad_l + i * (plot_w / (n - 1))
    def ty(val):
        return pad_t + plot_h - (val - min_val) / (max_val - min_val) * plot_h
        
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="auto">')
    svg.append('<defs>')
    svg.append('''
      <linearGradient id="prod-bg" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#0b101c"/>
        <stop offset="100%" stop-color="#05070a"/>
      </linearGradient>
      <linearGradient id="prod-area" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="rgba(10, 132, 255, 0.35)"/>
        <stop offset="100%" stop-color="rgba(10, 132, 255, 0.0)"/>
      </linearGradient>
    ''')
    svg.append('</defs>')
    svg.append(f'<rect width="{w}" height="{h}" rx="6" fill="url(#prod-bg)" stroke="#151c2a" stroke-width="1"/>')
    
    svg.append('<text x="20" y="24" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="9.5" font-weight="700">INDIA INDIGENOUS SURGE · PRODUCTION</text>')
    svg.append('<text x="20" y="42" fill="#e9edf2" font-family="Inter, sans-serif" font-size="13" font-weight="700">Annual Defence Production (+110% in 5 Yrs)</text>')
    
    for val in [80000, 120000, 160000]:
        py = ty(val)
        svg.append(f'<line x1="{pad_l}" y1="{py}" x2="{pad_l + plot_w}" y2="{py}" stroke="#141a27" stroke-width="1"/>')
        svg.append(f'<text x="{pad_l - 8}" y="{py + 3}" fill="#64748b" font-family="JetBrains Mono, monospace" font-size="8.5" text-anchor="end">₹{val//1000}k Cr</text>')
        
    pts = [f"{tx(i):.1f},{ty(v):.1f}" for i, (_, v, _) in enumerate(data)]
    area = [f"{tx(0):.1f},{pad_t + plot_h}"] + pts + [f"{tx(n-1):.1f},{pad_t + plot_h}"]
    
    svg.append(f'<polygon points="{" ".join(area)}" fill="url(#prod-area)"/>')
    svg.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="#0a84ff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>')
    
    for i, (yr, val, label) in enumerate(data):
        px, py = tx(i), ty(val)
        is_last = (i == n - 1)
        c_fill = "#38bdf8" if is_last else "#0a84ff"
        r = 5 if is_last else 3.5
        svg.append(f'<circle cx="{px}" cy="{py}" r="{r}" fill="{c_fill}" stroke="#ffffff" stroke-width="1.5"/>')
        dy = -10 if not is_last else -12
        ha = "center" if not is_last else "end"
        color = "#e9edf2" if is_last else "#94a3b8"
        fw = "700" if is_last else "500"
        svg.append(f'<text x="{px}" y="{py + dy}" fill="{color}" font-family="JetBrains Mono, monospace" font-size="9" font-weight="{fw}" text-anchor="{ha}">{label}</text>')
        svg.append(f'<text x="{px}" y="{pad_t + plot_h + 16}" fill="#64748b" font-family="JetBrains Mono, monospace" font-size="9" text-anchor="middle">{yr}</text>')
        
    svg.append(f'<g transform="translate({pad_l + 10}, {pad_t + 16})">')
    svg.append('<rect width="180" height="34" rx="3" fill="#090d16" stroke="#1f293d" stroke-width="1"/>')
    svg.append('<text x="8" y="14" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="8" font-weight="700">75% CAPITAL EARMARK MANDATE</text>')
    svg.append('<text x="8" y="26" fill="#94a3b8" font-family="Inter, sans-serif" font-size="8.5">₹1.39 Lakh Cr reserved for domestic</text>')
    svg.append('</g>')
    
    svg.append(f'<text x="20" y="{h - 10}" fill="#475569" font-family="JetBrains Mono, monospace" font-size="8">SOURCE: MoD / PIB RELEASES · FY14 BASE: ₹43,746 Cr (4.1× EXPANSION)</text>')
    svg.append('</svg>')
    
    with open('wiki/assets/india_defence_production_dark.svg', 'w') as f:
        f.write("\n".join(svg))
    print("Generated wiki/assets/india_defence_production_dark.svg")

def generate_exports_graph():
    w, h = 480, 320
    pad_l, pad_r, pad_t, pad_b = 60, 24, 64, 50
    plot_w = w - pad_l - pad_r
    plot_h = h - pad_t - pad_b
    
    data = [
        ("FY14", 686, "₹686 Cr"),
        ("FY18", 4682, "₹4.6k"),
        ("FY21", 8435, "₹8.4k"),
        ("FY23", 15918, "₹15.9k"),
        ("FY25", 23622, "₹23.6k"),
        ("FY26", 38424, "₹38,424 Cr")
    ]
    
    min_val, max_val = 0, 42000
    n = len(data)
    
    def tx(i):
        return pad_l + i * (plot_w / (n - 1))
    def ty(val):
        return pad_t + plot_h - (val - min_val) / (max_val - min_val) * plot_h
        
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="auto">')
    svg.append('<defs>')
    svg.append('''
      <linearGradient id="exp-bg" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#0b101c"/>
        <stop offset="100%" stop-color="#05070a"/>
      </linearGradient>
      <linearGradient id="exp-area" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="rgba(56, 189, 248, 0.35)"/>
        <stop offset="100%" stop-color="rgba(56, 189, 248, 0.0)"/>
      </linearGradient>
    ''')
    svg.append('</defs>')
    svg.append(f'<rect width="{w}" height="{h}" rx="6" fill="url(#exp-bg)" stroke="#151c2a" stroke-width="1"/>')
    
    svg.append('<text x="20" y="24" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="9.5" font-weight="700">INDIA GLOBAL FOOTHOLD · EXPORTS</text>')
    svg.append('<text x="20" y="42" fill="#e9edf2" font-family="Inter, sans-serif" font-size="13" font-weight="700">Annual Defence Exports (56× in 12 Yrs)</text>')
    
    for val in [10000, 20000, 30000]:
        py = ty(val)
        svg.append(f'<line x1="{pad_l}" y1="{py}" x2="{pad_l + plot_w}" y2="{py}" stroke="#141a27" stroke-width="1"/>')
        svg.append(f'<text x="{pad_l - 8}" y="{py + 3}" fill="#64748b" font-family="JetBrains Mono, monospace" font-size="8.5" text-anchor="end">₹{val//1000}k Cr</text>')
        
    pts = [f"{tx(i):.1f},{ty(v):.1f}" for i, (_, v, _) in enumerate(data)]
    area = [f"{tx(0):.1f},{pad_t + plot_h}"] + pts + [f"{tx(n-1):.1f},{pad_t + plot_h}"]
    
    svg.append(f'<polygon points="{" ".join(area)}" fill="url(#exp-area)"/>')
    svg.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="#38bdf8" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>')
    
    for i, (yr, val, label) in enumerate(data):
        px, py = tx(i), ty(val)
        is_last = (i == n - 1)
        c_fill = "#38bdf8" if is_last else "#0a84ff"
        r = 5 if is_last else 3.5
        svg.append(f'<circle cx="{px}" cy="{py}" r="{r}" fill="{c_fill}" stroke="#ffffff" stroke-width="1.5"/>')
        dy = -10 if not is_last else -12
        ha = "center" if not is_last else "end"
        color = "#e9edf2" if is_last else "#94a3b8"
        fw = "700" if is_last else "500"
        svg.append(f'<text x="{px}" y="{py + dy}" fill="{color}" font-family="JetBrains Mono, monospace" font-size="9" font-weight="{fw}" text-anchor="{ha}">{label}</text>')
        svg.append(f'<text x="{px}" y="{pad_t + plot_h + 16}" fill="#64748b" font-family="JetBrains Mono, monospace" font-size="9" text-anchor="middle">{yr}</text>')
        
    svg.append(f'<g transform="translate({pad_l + 10}, {pad_t + 16})">')
    svg.append('<rect width="180" height="34" rx="3" fill="#090d16" stroke="#1f293d" stroke-width="1"/>')
    svg.append('<text x="8" y="14" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="8" font-weight="700">PRIVATE SHARE: 45.16% (₹17,353 Cr)</text>')
    svg.append('<text x="8" y="26" fill="#94a3b8" font-family="Inter, sans-serif" font-size="8.5">Reaching 80+ nations · 145 exporters</text>')
    svg.append('</g>')
    
    svg.append(f'<text x="20" y="{h - 10}" fill="#475569" font-family="JetBrains Mono, monospace" font-size="8">SOURCE: DDP HISTORICAL SERIES · MoD APRIL 2026</text>')
    svg.append('</svg>')
    
    with open('wiki/assets/india_defence_exports_dark.svg', 'w') as f:
        f.write("\n".join(svg))
    print("Generated wiki/assets/india_defence_exports_dark.svg")

if __name__ == '__main__':
    generate_cost_curve()
    generate_modern_warfare_shifts()
    generate_production_graph()
    generate_exports_graph()
