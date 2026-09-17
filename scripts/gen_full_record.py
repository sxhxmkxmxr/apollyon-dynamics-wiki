"""Generate wiki/strategic-dependency/full-record.html — all 70 episodes, one page, war by war."""
import json, os, html

HERE = os.path.dirname(os.path.abspath(__file__))
WIKI = os.path.dirname(HERE)
OUT = os.path.join(WIKI, "strategic-dependency")

raw = open(os.path.join(WIKI, "js", "dependency_corpus_data.js")).read()
raw = raw.split("=", 1)[1].strip().rstrip(";")
DATA = {d["ID"]: d for d in json.loads(raw)}

SECTIONS = [
 ("kashmir-1947", "First Kashmir War, 1947–48",
  "Two months after independence, India fought its first war with an imported arsenal — and met its first refusal.",
  ["D001", "D002"]),
 ("lean-years", "Rearmament on credit, 1950–61",
  "Between wars, rearmament ran on foreign credit: British jets hostage to NATO priorities, Shermans hostage to spares.",
  ["D003", "D004"]),
 ("war-1962", "Sino-Indian War, 1962",
  "The Himalayan war was also a logistics war, and nearly every link in the chain was foreign-held.",
  ["D005", "D006", "D007", "D008", "D009", "D010"]),
 ("war-1965", "Second Kashmir War, 1965 — and the rearmament freeze",
  "An embargo imposed mid-war, then a freeze that lingered in paperwork for years.",
  ["D011", "D012", "D013", "D014"]),
 ("war-1971", "Bangladesh War, 1971",
  "Readiness gaps found before the war, embargoes imposed during it.",
  ["D015", "D016", "D017", "D018", "D019"]),
 ("pokhran-1974", "Pokhran-I and the nuclear freeze, 1974–81",
  "After the 1974 test, Canada cut the Rajasthan reactors loose and Tarapur fuel became a pressure valve — the first sanctions regime India ever lived under.",
  ["D020", "D021", "D022"]),
 ("siachen-1984", "Siachen and the technology-control era, 1984–88",
  "The highest battlefield on earth, nearly lost to a kit list — while computers became a controlled substance.",
  ["D023", "D024"]),
 ("soviet-collapse", "The Soviet collapse, 1991–94",
  "In 1991 the supplier behind most Indian hardware simply vanished. Spares, engine kits and even gun barrels became archaeology overnight.",
  ["D025", "D026", "D027", "D028", "D029"]),
 ("pokhran-1998", "Pokhran-II sanctions, 1998",
  "The 1998 tests triggered the broadest American sanctions yet: defence sales, services and dual-use licences terminated together.",
  ["D030", "D031", "D032"]),
 ("kargil-1999", "Kargil War, 1999",
  "Seven denials in one short, high-altitude war — the densest case in the corpus.",
  ["D033", "D034", "D035", "D036", "D037", "D038", "D039"]),
 ("licence-decades", "The licensed-production decades, 2000–17",
  "The 2000s answer was licensed production — which too often meant assembling foreign kits while the critical designs, tools and software never transferred.",
  ["D040","D041","D042","D043","D044","D045","D046","D047","D048","D049",
   "D050","D051","D052","D053","D054","D055","D056","D057","D058","D059","D060"]),
 ("ladakh-2020", "Ladakh and the Ukraine rupture, 2019–26",
  "It started with winter clothing and ended with the entire Russian sustainment chain in question.",
  ["D061","D062","D063","D064","D065","D066","D067","D068","D069","D070"]),
]

total = sum(len(e) for _, _, _, e in SECTIONS)
assert total == 70, total
assert sorted(e for _, _, _, es in SECTIONS for e in es) == [f"D{i:03d}" for i in range(1, 71)]

def esc(s):
    return html.escape(s or "", quote=True)

def ep_block(d):
    url = (d.get("Primary URL") or "").strip()
    src = f'<div class="dep-src">SOURCE: <a href="{esc(url)}" target="_blank" rel="noopener noreferrer">{esc(url)}</a></div>' if url else ""
    sev = d.get("Severity", 3)
    sevlab = "SEV 5 · WARTIME DENIAL" if sev == 5 else ("SEV 4 · CRISIS EMBARGO" if sev == 4 else "SEV 3 · TECH CONTROL")
    sevcls = "sev-5" if sev == 5 else ("sev-4" if sev == 4 else "sev-3")
    return f"""<div class="dep-ep" id="{d['ID']}">
  <div class="dep-ep-head"><span>{esc(d.get('Date / period',''))} · {esc(d.get('Conflict / trigger',''))}</span><span class="dep-badge {sevcls}">{sevlab}</span></div>
  <h4>{esc(d.get('Episode',''))}</h4>
  <div class="dep-ep-meta">DENIED BY <strong>{esc(d.get('External actor / OEM',''))}</strong> &nbsp;·&nbsp; BOTTLENECK: <strong class="rb">{esc(d.get('Foreign-controlled bottleneck',''))}</strong></div>
  <p>{esc(d.get('Documented event',''))}</p>
  <p class="conseq">Consequence — {esc(d.get('Operational / strategic consequence',''))}</p>
  {src}
</div>"""

toc = "\n".join(
    f'    <li><a href="#{sid}">{title} ({len(eps)})</a></li>' for sid, title, _, eps in SECTIONS)

body = []
for idx, (sid, title, intro, eps) in enumerate(SECTIONS, 1):
    blocks = "\n".join(ep_block(DATA[e]) for e in eps)
    nxt = (f'<div style="margin-top:18px;"><a href="#{SECTIONS[idx][0]}" style="font-family:var(--mono);font-size:11px;">NEXT: {esc(SECTIONS[idx][1])} →</a></div>'
           if idx < len(SECTIONS) else "")
    body.append(f"""<section id="{sid}">
  <div class="sec-tag">{idx:02d} · {len(eps)} documented episodes</div>
  <h2>{esc(title)}</h2>
  <p class="lede">{esc(intro)}</p>
{blocks}{nxt}
</section>""")
body = "\n\n".join(body)

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Full Record — every denial, one by one — Apollyon Dynamics Wiki</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,wght@0,400;0,500;1,400&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../css/wiki.css">
</head>
<body>

<div class="rail">
  <div class="rail-inner">
    <a class="rail-brand" href="../index.html"><span class="glyph"></span>Apollyon Dynamics <em>&middot; Engineering Wiki</em></a>
    <nav class="rail-links">
      <a href="../index.html#strategic-dependency" class="on">Dependencies</a>
      <a href="../index.html#products">Products</a>
      <a href="../index.html#subsystems">Subsystems</a>
      <a href="../doctrine/new-arsenal.html">Doctrine</a>
    </nav>
  </div>
</div>

<div class="shell">
<div class="layout">

<aside class="aside">
  <h4>On this page</h4>
  <ul>
{toc}
  </ul>
  <h4>Wiki</h4>
  <ul>
    <li><a href="../index.html#strategic-dependency">← Dependency overview</a></li>
    <li><a href="../index.html#products">Products</a></li>
    <li><a href="../index.html#subsystems">Subsystems</a></li>
  </ul>
</aside>

<main class="main">

<div class="crumb"><a href="../index.html">Wiki</a><span>/</span><a href="../index.html#strategic-dependency">Strategic dependency</a><span>/</span>Full record</div>
<header class="masthead">
  <div class="mast-meta">Strategic dependency · 70 documented episodes · 1947–2026</div>
  <h1>The full record</h1>
  <p class="standfirst">Every denial in the corpus, explained one by one in chronological order — what was asked for, who refused, and what it cost. Each account carries its primary source. Start at the top, or jump to any era on the left.</p>
</header>

{body}

<section id="what-this-means">
  <div class="sec-tag">13 · What Apollyon takes from this</div>
  <h2>Build where the embargo cannot reach</h2>
  <div class="note key"><div class="t">Sovereign answer</div><p>Seventy episodes share one shape: the critical layer was foreign, and foreign means permissioned. Apollyon therefore owns the performance-determining layers first — aerodynamic modelling, flight runtime, GNSS-denied navigation, inference silicon integration — and manufactures on India's domestic industrial base at automotive cadence. No single foreign vote, file, or factory can pause a programme.</p></div>
</section>

<footer>
  <div>Apollyon Dynamics · Engineering Wiki · Strategic Dependency</div>
  <div><a href="../index.html#strategic-dependency">Overview</a> · <a href="../doctrine/new-arsenal.html">The New Arsenal</a></div>
</footer>

</main>
</div>
</div>

</body>
</html>
"""
open(os.path.join(OUT, "full-record.html"), "w").write(page)
print(f"full-record.html ({total} eps, {len(SECTIONS)} sections)")
