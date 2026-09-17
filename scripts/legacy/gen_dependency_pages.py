"""Generate wiki/strategic-dependency/ component pages from the corpus data file."""
import json, os, html, re

HERE = os.path.dirname(os.path.abspath(__file__))
WIKI = os.path.dirname(HERE)
OUT = os.path.join(WIKI, "strategic-dependency")
os.makedirs(OUT, exist_ok=True)

raw = open(os.path.join(WIKI, "js", "dependency_corpus_data.js")).read()
raw = raw.split("=", 1)[1].strip().rstrip(";")
DATA = {d["ID"]: d for d in json.loads(raw)}

COMPONENTS = [
 dict(slug="fighter-jet-engines", title="Fighter-jet engines",
      short="The single point of failure that grounds whole fleets — from AL-31s to today's Tejas GE F404 wait.",
      pattern=("Every Indian fighter generation has flown on imported hot sections. When the supplier stalls — "
               "Soviet collapse, Ukrainian overhaul lines, American supply chains — squadrons do not degrade gracefully, "
               "they stop flying. Five documented episodes, four of them wartime-critical, and the current one is unfolding now: "
               "finished Tejas Mk1A airframes parked for want of GE F404 engines."),
      counter=("Apollyon designs its strike systems around domestic expendable propulsion — the GTRE 350 kgf turbojet and "
               "Indian micro-jets — so no foreign engine OEM sits on the critical path of any programme."),
      eps=["D042","D046","D057","D068","D069"]),
 dict(slug="combat-aircraft-supply", title="Combat aircraft supply and spares",
      short="Embargoes that shrank the air force mid-war — 1965, the Soviet collapse, and the Ukraine-era spares shock.",
      pattern=("Aircraft are bought once and fed for forty years. Twice — 1965 and 1991 — the feeding stopped overnight: "
               "the American embargo, then the disappearance of the Soviet Union, which left the IAF burning war-reserve spares. "
               "The same film is playing again as Russian-origin sustainment seizes up and 44 emergency self-reliance projects "
               "try to cover the gap."),
      counter=("Apollyon manufactures out-of-autoclave composite airframes and stamped bulkheads on India's precision automotive "
              "base, and owns its flight software outright — no foreign airframe OEM, no black-box avionics to be switched off."),
      eps=["D001","D003","D011","D012","D013","D025","D026","D040","D041","D055","D066","D070"]),
 dict(slug="artillery-shells-fuses", title="Artillery guns, shells and fuses",
      short="The guns fell silent in Kargil for want of spares; the shell stockpile later fell to days.",
      pattern=("Artillery wins land wars and consumes ammunition faster than any peacetime planner admits. In Kargil, Bofors guns "
               "went out of action for spares while emergency precision rounds failed trials and imports arrived after the ceasefire. "
               "A decade later the War Wastage Reserve itself was down to critically low levels, and two successive foreign shell-plant "
               "partners were blacklisted or debarred mid-programme."),
      counter=("Apollyon replaces scarce foreign precision munitions with mass attritable strike weapons built at automotive cadence "
              "from domestic supply chains — salvo replenishment that does not depend on a single shell factory abroad."),
      eps=["D027","D035","D038","D039","D043","D044","D045","D060"]),
 dict(slug="radars-sensors-eyes", title="Radars, seekers and satellite eyes",
      short="Denied imagery over Kargil, blocked counter-battery radars, slipped S-400s — the sensor chain breaks first.",
      pattern=("Every denial regime in the corpus targets sensing first: tactical radios in 1962, the Peace Indigo network in 1971, "
               "weapon-locating radars strangled across three decades, satellite imagery that arrived 'mostly' useless over Kargil, "
               "and Mirage precision chains with foreign software in the loop. A blind battery is just expensive noise."),
      counter=("Apollyon fuses sovereign multi-spectral EO/IR seekers with domestic partners and runs its own neural edge inference "
              "on local silicon — plus a GNSS-denied navigation stack (CRPA nulling, optical scene matching) that never asks a "
              "foreign satellite for permission."),
      eps=["D007","D010","D018","D033","D034","D036","D037","D048","D053","D067"]),
 dict(slug="airlift-helicopters", title="Airlift and helicopters",
      short="The Himalayan air bridge ran on borrowed spares in 1962 — and Ladakh still depends on it.",
      pattern=("India's northern wars are won by airlift. In 1962 the C-119 fleet, the Caribous, and the radios that directed them "
               "were all foreign-held and all constrained mid-crisis. The pattern never left: Mi-4s grounded before 1971, An-12s flown "
               "back to the USSR for servicing, and C-119 spares embargoed twice in a decade."),
      counter=("Apollyon keeps its launch and sustainment footprint ground-mobile, containerised, and domestic — systems that deploy "
              "from Indian roads and rails with sub-30-minute readiness, not foreign depot pipelines."),
      eps=["D005","D006","D015","D016","D019"]),
 dict(slug="munitions-factories", title="Munitions factories and the powder chain",
      short="Licences for shell machinery cancelled in 1971; indigenous ammunition later declared unserviceable.",
      pattern=("It is not only finished rounds that were denied — it was the ability to make them. Washington cancelled licences for "
               "ammunition components and manufacturing machinery during the 1971 war; Israeli mortar rounds plugged 1965; and in 2012 "
               "indigenously produced ammunition was declared unserviceable, forcing replacement imports. A factory that cannot make "
               "powder is a museum."),
      counter=("Apollyon's strike family is specified from the start for Indian automotive-base production — stampable composites, "
              "domestic energetics chains, and 80–120 rounds a month of rate output, not boutique foreign lines."),
      eps=["D002","D008","D014","D017","D051"]),
 dict(slug="tanks-armour", title="Tanks, trucks and armoured spares",
      short="Shermans without spares in the 1950s, T-72 lines stopped in the 1990s, T-90s still 62% imported.",
      pattern=("Armour is a spares business wearing a tank's uniform. Shermans in the fifties, T-72 engine kits that stopped the "
               "assembly lines in 1992, Tatra trucks that never indigenised — and the T-90, licensed for decades, still carrying 62% "
               "imported cost in critical assemblies the supplier never transferred."),
      counter=("Apollyon avoids the licence-assembly trap entirely: clean-sheet designs, owned IP, and structures chosen so India's "
              "existing precision and automotive base can build them without a foreign drawing package."),
      eps=["D004","D028","D049","D050","D052"]),
 dict(slug="warships-naval", title="Warships and naval propulsion",
      short="Submarines delayed by foreign steel, frigates stranded by broken turbine chains, carriers without weapons.",
      pattern=("Sea power on installment plans: Scorpene boats delayed by foreign material packages, Project 11356 frigates caught "
               "when the Russian-Ukrainian turbine chain ruptured, Ukrainian-overhaul-dependent gas turbines with no domestic depot, "
               "Sea Kings blocked by American parts inside British airframes — and MiG-29Ks delivered to a carrier without working weapons."),
      counter=("Apollyon's kamikaze USV programme applies the same attritable logic at sea: low-observable hulls, autonomous "
              "non-satellite navigation and terminal optical homing, built to be lost in quantity rather than protected as crown jewels."),
      eps=["D032","D047","D054","D056","D058","D059","D064","D065"]),
 dict(slug="soldier-winter-kit", title="Soldier winter and high-altitude kit",
      short="Siachen was nearly lost for want of snow goggles; Ladakh 2020 meant emergency ECWCS from US stocks.",
      pattern=("The least glamorous denial in the corpus nearly decided the highest battlefield on earth: imported glacier kit reached "
               "Siachen hours before Operation Meghdoot in 1984. Thirty-six years later the Army told Parliament 80% of extreme-cold "
               "clothing was imported — and Ladakh's emergency sets came off American shelves while indigenous ECWCS took decades."),
      counter=("The lesson generalises: if the soldier's kit, the drone's airframe, or the missile's seeker cannot be sourced at home, "
              "it is a hostage, not an asset. Apollyon qualifies domestic sources before foreign ones, at every layer it controls."),
      eps=["D009","D023","D061","D062","D063"]),
 dict(slug="strategic-tech", title="Strategic tech: nuclear, cryogenic, compute, flight control",
      short="Sanctions that tried to freeze the bomb, the GSLV upper stage, the PARAM — and the Tejas flight laws.",
      pattern=("The longest-running denial campaign in the corpus: nuclear fuel and reactor support after Pokhran-I, supercomputers "
               "that forced PARAM into existence, cryogenic engines sanctioned off the GSLV, and the LCA's American flight-control "
               "partnership terminated after Pokhran-II. Each blockade eventually produced an Indian answer — decades late."),
      counter=("Apollyon inverts the sequence: own the performance-determining layers first — aerodynamic modelling, flight runtime, "
              "navigation, inference silicon integration — so no single foreign technology vote can pause a programme."),
      eps=["D020","D021","D022","D024","D029","D030","D031"]),
]

def esc(s):
    return html.escape(s or "", quote=True)

def ep_block(d):
    url = d.get("Primary URL", "").strip()
    src = f'<div class="dep-src">SOURCE: <a href="{esc(url)}" target="_blank" rel="noopener noreferrer">{esc(url)}</a></div>' if url else ""
    sev = d.get("Severity", 3)
    sevlab = "SEV 5 · WARTIME DENIAL" if sev == 5 else ("SEV 4 · CRISIS EMBARGO" if sev == 4 else "SEV 3 · TECH CONTROL")
    sevcls = "sev-5" if sev == 5 else ("sev-4" if sev == 4 else "sev-3")
    return f"""<div class="dep-ep">
  <div class="dep-ep-head"><span>{esc(d.get('Date / period',''))} · {esc(d.get('Conflict / trigger',''))}</span><span class="dep-badge {sevcls}">{sevlab}</span></div>
  <h4>{esc(d.get('Episode',''))}</h4>
  <div class="dep-ep-meta">DENIED BY <strong>{esc(d.get('External actor / OEM',''))}</strong> &nbsp;·&nbsp; BOTTLENECK: <strong class="rb">{esc(d.get('Foreign-controlled bottleneck',''))}</strong></div>
  <p>{esc(d.get('Documented event',''))}</p>
  <p class="conseq">Consequence — {esc(d.get('Operational / strategic consequence',''))}</p>
  {src}
</div>"""

sib_links = "\n".join(
    f'    <li><a href="{c["slug"]}.html">{i+1:02d} · {esc(c["title"])}</a></li>'
    for i, c in enumerate(COMPONENTS))

for i, c in enumerate(COMPONENTS):
    eps = [DATA[e] for e in c["eps"]]
    sev5 = sum(1 for d in eps if d.get("Severity") == 5)
    blocks = "\n".join(ep_block(d) for d in eps)
    toc = "\n".join(
        f'    <li><a href="#{d["ID"]}">{esc(d.get("Date / period",""))} — {esc(d.get("Episode",""))}</a></li>' for d in eps)
    # anchor ids
    titled = []
    for d in eps:
        b = ep_block(d).replace('<div class="dep-ep">', f'<div class="dep-ep" id="{d["ID"]}">')
        titled.append(b)
    blocks = "\n".join(titled)
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{i+1:02d} · {esc(c['title'])} — Strategic Dependency — Apollyon Dynamics Wiki</title>
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
  <h4>This page</h4>
  <ul>
    <li><a href="#pattern">The pattern</a></li>
    <li><a href="#episodes">Documented episodes ({len(eps)})</a></li>
    <li><a href="#counter">Apollyon countermeasure</a></li>
  </ul>
  <h4>Dependency index</h4>
  <ul>
{sib_links}
  </ul>
  <h4>Wiki</h4>
  <ul>
    <li><a href="../index.html#strategic-dependency">← Dependency overview</a></li>
    <li><a href="../index.html#products">Products</a></li>
    <li><a href="../index.html#subsystems">Subsystems</a></li>
  </ul>
</aside>

<main class="main">

<div class="crumb"><a href="../index.html">Wiki</a><span>/</span><a href="../index.html#strategic-dependency">Strategic dependency</a><span>/</span>{i+1:02d}</div>
<header class="masthead">
  <div class="mast-meta">Strategic dependency · {i+1:02d} of 10 · {len(eps)} documented episodes ({sev5} wartime-critical)</div>
  <h1>{esc(c['title'])}</h1>
  <p class="standfirst">{esc(c['short'])}</p>
</header>

<section id="pattern">
  <div class="sec-tag">01 · The pattern</div>
  <h2>What kept breaking</h2>
  <p class="lede">{esc(c['pattern'])}</p>
</section>

<section id="episodes">
  <div class="sec-tag">02 · Documented episodes</div>
  <h2>Short accounts, primary sources</h2>
  <p>Each entry below is drawn from official records, declassified cables, or parliamentary reports. Source links follow every account.</p>
{blocks}
</section>

<section id="counter">
  <div class="sec-tag">03 · Apollyon countermeasure</div>
  <h2>How this programme ends the pattern</h2>
  <div class="note key"><div class="t">Sovereign answer</div><p>{esc(c['counter'])}</p></div>
  <div class="synthesis-arrows" style="border: 1px solid var(--border-subtle);">
    <span>{"<a href='" + COMPONENTS[i-1]['slug'] + ".html'>← " + f"{i:02d}" + " · " + esc(COMPONENTS[i-1]['title']) + "</a>" if i > 0 else "<a href='../index.html#strategic-dependency'>← Index</a>"}</span>
    <span><a href="../index.html#strategic-dependency">Index</a></span>
    <span>{("<a href='" + COMPONENTS[i+1]['slug'] + ".html'>" + f"{i+2:02d}" + " · " + esc(COMPONENTS[i+1]['title']) + " →</a>") if i < len(COMPONENTS)-1 else "<a href='../index.html#strategic-dependency'>Index →</a>"}</span>
  </div>
</section>

<footer>
  <div>Apollyon Dynamics · Engineering Wiki · Strategic Dependency {i+1:02d}/10</div>
  <div><a href="../index.html#strategic-dependency">Overview</a> · <a href="../doctrine/new-arsenal.html">The New Arsenal</a></div>
</footer>

</main>
</div>
</div>

</body>
</html>
"""
    open(os.path.join(OUT, c["slug"] + ".html"), "w").write(page)
    print(f"{c['slug']}.html  ({len(eps)} eps)")

# emit mapping for index section
map_out = {c["slug"]: {"n": i+1, "title": c["title"], "short": c["short"],
                       "count": len(c["eps"]),
                       "sev5": sum(1 for e in c["eps"] if DATA[e].get("Severity")==5)}
           for i, c in enumerate(COMPONENTS)}
json.dump(map_out, open("/tmp/opencode/dep_components.json", "w"), indent=1)
print("mapping -> /tmp/opencode/dep_components.json")
