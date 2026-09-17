with open('wiki/scripts/generate_infographics.py', 'r') as f:
    content = f.read()

# Fix the labels inside generate_cost_curve
content = content.replace(
    'svg.append(f\'<text x="{px - 14}" y="{py + 20}" fill="#cbd5e1" font-family="JetBrains Mono, monospace" font-size="10" text-anchor="end">₹2,700/kg·km · {env}</text>\')\n        elif "Hemlock Mk I"',
    'svg.append(f\'<text x="{px - 14}" y="{py + 20}" fill="#cbd5e1" font-family="JetBrains Mono, monospace" font-size="10" text-anchor="end">₹1,500/kg·km · {env}</text>\')\n        elif "Hemlock Mk I"'
)

content = content.replace(
    'svg.append(f\'<text x="{px - 14}" y="{py + 18}" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="10.5" font-weight="700" text-anchor="end">₹35/kg·km · 1.5M kg·km</text>\')',
    'svg.append(f\'<text x="{px - 14}" y="{py + 18}" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="10.5" font-weight="700" text-anchor="end">₹35/kg·km · 1,500,000 kg·km</text>\')'
)

# And make sure Hemlock Mk II is anchored properly
content = content.replace(
    'elif "Hemlock Mk II" in name:\n            svg.append(f\'<text x="{px - 14}" y="{py + 4}" fill="#ff453a"',
    'elif "Hemlock Mk II" in name:\n            svg.append(f\'<text x="{px - 14}" y="{py - 6}" fill="#ff453a"'
)

with open('wiki/scripts/generate_infographics.py', 'w') as f:
    f.write(content)

