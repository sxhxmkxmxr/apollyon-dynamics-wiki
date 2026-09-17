import os

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Apollyon Dynamics — Engineering Wiki</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,wght@0,400;0,500;1,400&family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/wiki.css">
</head>
<body>

<div class="rail">
  <div class="rail-inner">
    <a class="rail-brand" href="index.html"><span class="glyph"></span>Apollyon Dynamics <em>· Engineering Wiki</em></a>
    <nav class="rail-links">
      <a href="#investment-thesis">Thesis</a>
      <a href="#modern-warfare">Modern Warfare</a>
      <a href="#problem-solution">Synthesis</a>
      <a href="#indias-window">India's Window</a>
      <a href="#strategic-dependency">Dependencies</a>
      <a href="#products">Products</a>
      <a href="#subsystems">Subsystems</a>
      <a href="doctrine/new-arsenal.html">Doctrine</a>
      <a href="about/history.html">History</a>
    </nav>
  </div>
</div>

<div class="shell">
<div class="layout">

<aside class="aside">
  <h4>This page</h4>
  <ul>
    <li><a href="#overview">Overview</a></li>
    <li><a href="#ethos">Ethos</a></li>
    <li><a href="#investment-thesis">Investment Thesis</a></li>
    <li><a href="#modern-warfare">Modern Warfare &amp; Cost Curve</a></li>
    <li><a href="#problem-solution">Problem &amp; Solution</a></li>
    <li><a href="#indias-window">India's Strategic Window</a></li>
    <li><a href="#strategic-dependency">Strategic Dependency (1947–2026)</a></li>
    <li><a href="#classes">Product classes</a></li>
    <li><a href="#products">Product register</a></li>
    <li><a href="#subsystems">Subsystem register</a></li>
    <li><a href="#matrix">Subsystem × product</a></li>
    <li><a href="#record">Record &amp; deployment</a></li>
  </ul>
  <h4>Products</h4>
  <ul>
    <li><a href="products/hacm-350.html">HACM-350</a></li>
    <li><a href="products/nightshade-adx1.html">Nightshade ADX-1</a></li>
    <li><a href="products/usv-strike.html">Kamikaze USV</a></li>
    <li><a href="products/ahuti.html">Ahuti Interceptor</a></li>
    <li><a href="products/mobile-drone-lab.html">Mobile Drone Lab</a></li>
    <li><a href="products/cortex.html">Apollyon Cortex</a></li>
    <li><a href="products/mdcc.html">MDCC</a></li>
  </ul>
  <h4>Subsystems</h4>
  <ul>
    <li><a href="subsystems/near-envelope-control.html">Robust control for fast platforms</a></li>
    <li><a href="subsystems/gnss-denied-navigation.html">High-speed GNSS-denied nav</a></li>
    <li><a href="subsystems/onboard-compute.html">Edge compute &amp; inference</a></li>
    <li><a href="subsystems/flight-software.html">Flight software stack</a></li>
    <li><a href="subsystems/seekers.html">Seekers &amp; terminal guidance</a></li>
    <li><a href="subsystems/propulsion.html">Propulsion</a></li>
    <li><a href="subsystems/airframe-structures.html">Airframe &amp; structures</a></li>
    <li><a href="subsystems/launch-systems.html">Launch &amp; ground systems</a></li>
  </ul>
  <h4>Doctrine</h4>
  <ul>
    <li><a href="doctrine/new-arsenal.html">The New Arsenal</a></li>
    <li><a href="doctrine/precision-is-mercy.html">Precision is Mercy</a></li>
    <li><a href="doctrine/missing-middle.html">The missing middle</a></li>
  </ul>
</aside>

<main class="main">

<header class="masthead">
  <div class="mast-meta">Apollyon Dynamics · Neo-Prime Knowledge Base</div>
  <h1>An Indian neo-prime, <span class="sub">built from the bottom up</span></h1>
  <p class="standfirst">Apollyon Dynamics designs and manufactures autonomous strike, interception, and battlefield-intelligence systems. This wiki is the company's internal reference: what each system is, what it is specified to do, and which shared subsystems it is built from.</p>
</header>

<section id="overview">
  <div class="sec-tag">01 · Overview</div>
  <h2>What the company is</h2>
  <p class="lede">Apollyon Dynamics is being built as an Indian neo-prime &mdash; an agile engineering institution that repeatedly converts difficult military operational requirements into reliable hardware, and that expands the class of problems it can solve with every programme.</p>
  <p>The company was founded by <strong>Jayant Khatri</strong> and <strong>Sourya Choudhury</strong> out of a hostel room at BITS Pilani, Hyderabad. Within two months of formally incorporating, hardware was shipping to active frontline units. It now operates across four theatres with seven fielded units, running three concurrent development lines: jet-propelled standoff strike, high-speed interception, and the edge command software layer that fuses multi-domain tactical intelligence.</p>
  <p>The core capability being accumulated is not any single vehicle. It is the engineering substrate underneath them &mdash; the physics simulation corrected against flight telemetry, the neural control policies trained within it, the navigation stack that functions under complete GNSS denial, the deterministic flight software runtime, and the domestic manufacturing ecosystem that lets all of it be built in India at rate. Each programme leaves that substrate deeper than it found it. That is the moat, and it is the reason the next machine is harder than the last.</p>

  <div class="stats">
    <div class="stat"><div class="n accent">07</div><div class="d">Fielded formations<span class="muted">Active across 4 military theatres</span></div></div>
    <div class="stat"><div class="n">&lt;2 mo</div><div class="d">Hostel to frontline<span class="muted">First unit delivery from inception</span></div></div>
    <div class="stat"><div class="n accent">03</div><div class="d">Concurrent product lines<span class="muted">Standoff strike · C-UAS · Edge C2</span></div></div>
  </div>
</section>

<section id="ethos">
  <div class="sec-tag">02 · Ethos</div>
  <h2>Precision is Mercy</h2>
  <p>A defence company should be comfortable with the fact that its products are weapons. Apollyon takes pride in the fact that its products are weapons, are meant to be lethal, and are built to make the prospect of waging war against India prohibitively expensive. A system that cannot produce decisive effect against the military target it was designed for is a weak instrument of deterrence.</p>
  <p>The ethical question begins after accepting that fact. Precision in striking a legitimate military target is an act of mercy toward the civilian population. Lethality provides certainty of military effect; precision confines that effect to where it is intended. The desired weapon is the one that maximises the probability of achieving the legitimate military objective while minimising collateral damage beyond it.</p>

  <blockquote>
    क्षमा शोभती उस भुजंग को, जिसके पास गरल हो<br>
    उसको क्या जो दंतहीन, विषरहित, विनीत, सरल हो।
    <cite>Ramdhari Singh Dinkar · Restraint has value only when a state possesses alternatives</cite>
  </blockquote>

  <p>Two load-bearing commitments govern how every system in this wiki is architected:</p>
  <ul>
    <li><strong>The machine goes first, always.</strong> The first moments of contact are the most dangerous, and they should be borne by a machine rather than a soldier. If something must be lost, it must not be a human life. This is why our strike systems are attritable by design, and why our interceptor is specified to be cheap enough to actually fire in quantity.</li>
    <li><strong>Sovereignty rests on an industrial substratum.</strong> A state that depends on foreign suppliers for the weapons required for its defence possesses less strategic freedom than one which can design, manufacture, replenish, and improve them domestically. Every design decision in this wiki is checked against whether India can build it, at rate, without a multi-year foreign export licence.</li>
  </ul>

  <figure class="dark">
    <img src="assets/precision-is-mercy.jpg" alt="Precision is Mercy — company ethos plate">
    <figcaption><b>Ethos</b> The company's governing principle. Discriminate force is the higher engineering standard, not the softer one. See <a href="doctrine/precision-is-mercy.html">Precision is Mercy</a>.</figcaption>
  </figure>
</section>

<section id="investment-thesis">
  <div class="sec-tag">03 · Investment Thesis</div>
  <h2>The Neo-Prime Inflection</h2>
  <p class="lede">The character of warfare has undergone an irreversible structural transition. Decades of peace-time procurement optimized for exquisite, multi-million-dollar platforms have collided with high-attrition, electronically dense battlefields. Apollyon Dynamics is architected to be the sovereign neo-prime that captures this structural transition.</p>

  <div class="cards" style="margin-top: 24px;">
    <div class="card">
      <div class="kicker">Pillar 01</div>
      <h3>Why Apollyon</h3>
      <p>We are not a systems integrator assembling foreign subsystems, nor an academic skunkworks. Apollyon is a vertically integrated neo-prime that owns the critical performance-determining layers: aerodynamic modeling, flight runtime, high-speed GNSS-denied navigation, and custom inference silicon integration. In less than 18 months, Apollyon designed, built, and flight-tested two clean-sheet jet platforms and deployed operational units across four military theatres.</p>
    </div>

    <div class="card">
      <div class="kicker">Pillar 02</div>
      <h3>Why This Category</h3>
      <p>Modern combat has revealed a catastrophic operational gap: the <a href="doctrine/missing-middle.html">missing middle</a>. Tactical quadcopters ($5k) have 10 km range and zero high-Mach penetration; legacy cruise missiles ($2M–$5M) and manned strike aircraft ($80M+) are too scarce and costly to fire in salvo. High-subsonic attritable strike (HACM-350, Nightshade) and high-speed interception (Ahuti) occupy this decisive space: deep standoff range, Mach 0.7–0.8 speed, and extreme EW survivability at 1/10th traditional prime cost.</p>
    </div>

    <div class="card">
      <div class="kicker">Pillar 03</div>
      <h3>Why Now · Core Architecture</h3>
      <p>Technological convergence enables neo-primes today: domestic expendable turbojets, low-cost high-density edge compute, and neural simulation-to-real flight control pipelines. Apollyon turns this convergence into a compounding architectural moat. Navigate directly to our <a href="#subsystems">core architecture register</a> to inspect our shared subsystems: <a href="subsystems/near-envelope-control.html">Robust Near-Envelope Control</a>, <a href="subsystems/gnss-denied-navigation.html">High-Speed GNSS-Denied Navigation</a>, <a href="subsystems/onboard-compute.html">Edge Compute Silicon</a>, and our <a href="subsystems/flight-software.html">Flight Software Stack</a>. The core is written once, qualified once, and amortized across every airframe.</p>
    </div>

    <div class="card">
      <div class="kicker">Pillar 04</div>
      <h3>Why India</h3>
      <p>India represents the most demanding military environment on Earth: an active 3,488 km high-altitude Himalayan frontier (LAC) with China, a contested western border (LoC), and vast Indian Ocean SLOCs. Structurally, the Indian Ministry of Defence has enacted decisive policies: reserving 75% of the capital acquisition budget (₹1.39 lakh crore in FY27) for domestic industry, banning 5,521+ items under Positive Indigenisation Lists, and accelerating procurement through iDEX Prime. India also provides the world's most competitive aerospace engineering talent and precision automotive base.</p>
    </div>

    <div class="card">
      <div class="kicker">Pillar 05</div>
      <h3>Why Autonomous Defense</h3>
      <p>Permissive skies are obsolete. In modern frontline operations, electronic warfare systems are stationed every 10 km along the FLOT, jamming over 80% of GNSS frequencies and severing RF command links within seconds. A weapon that depends on a human pilot or satellite tether cannot reach its target. True sovereign deterrence requires complete edge autonomy: onboard physics-grounded inertial estimation, topological terrain scene matching (AI-DSMAC), and terminal optical seeker homing executing deterministically on the vehicle with zero external connectivity.</p>
    </div>

    <div class="card">
      <div class="kicker">Pillar 06</div>
      <h3>Why Expendable Systems</h3>
      <p>The arithmetic of industrial attrition is brutal. A war of attrition cannot be fought with weapons that take two years to build and cost more than the targets they destroy. Firing a ₹25 crore ($3M) Patriot or SM-2 missile against a ₹20 lakh ($25k) loitering munition represents an economic exchange trap that exhausts the defender. Expendable, attritable weapons enable commanders to launch saturation salvos at automotive production cadences, overwhelming enemy integrated air defence systems without depleting treasury reserves.</p>
    </div>

    <div class="card" style="grid-column: 1 / -1;">
      <div class="kicker">Pillar 07 · Strategic Moat</div>
      <h3>Why Apollyon Can Become a Neo-Prime</h3>
      <p>Apollyon holds a structural advantage against all three traditional peer classes:</p>
      <ul>
        <li><strong>vs. Indian Incumbents (Tata, Adani, Solar):</strong> Legacy conglomerates move at bureaucratic multi-year programme speed and act largely as licensed assemblers of foreign IP. Apollyon iterates clean-sheet jet airframes in months and owns the underlying guidance, runtime, and control IP.</li>
        <li><strong>vs. Foreign Cheap-Mass Startups (Anduril, European makers):</strong> Foreign startups operate with high Western cost structures ($300k+/engineer), face severe ITAR export hurdles, and lack native sovereign trust with the Indian military. Apollyon operates on an Indian rupee cost base while maintaining complete sovereign alignment.</li>
        <li><strong>vs. Foreign Legacy Primes (MBDA, Kongsberg, Raytheon):</strong> Traditional primes maximize capability per unit regardless of cost. Apollyon maximizes strike envelope per rupee (₹/kg-km). Different objective function, not a cheaper copy.</li>
      </ul>
      <p>By decoupling the guidance and navigation software from the physical packaging, each new airframe costs less to develop and reaches flight qualification faster than the last. That compounding velocity is how Apollyon scales into the enduring neo-prime of the Indo-Pacific.</p>
    </div>
  </div>
</section>

<section id="modern-warfare">
  <div class="sec-tag">04 · Modern Warfare &amp; Cost Asymmetry</div>
  <h2>The Economics of Contemporary Combat</h2>
  <p class="lede">Recent high-intensity conflicts in Ukraine, the Red Sea, and Nagorno-Karabakh have fundamentally inverted military doctrine. Exquisite platforms are being neutralized by mass attritable systems, and electronic warfare has rendered satellite navigation a liability rather than an asset.</p>

  <div class="blueprint-plate">
    <div class="blueprint-head">
      <div class="title"><span class="glyph"></span>TACTICAL SHIFTS · AIR COMBAT &amp; COST DYNAMICS</div>
      <div class="scale">SOURCE: RUSI / CSIS / APOLLYON STRATEGY</div>
    </div>
    <div class="blueprint-body" style="padding: 10px;">
      <img src="assets/modern_warfare_shifts_dark.svg" alt="Modern Warfare Architectural Shifts and Cost Exchange Asymmetry Infographic" style="width: 100%; height: auto; display: block;">
    </div>
    <div class="blueprint-cap">
      <b>Fig. 01</b> The modern combat inversion: operational shifts across domains, replenishment cadences, and electromagnetic contestation. Bottom panel details the 1:100 cost-exchange asymmetry trap between attritable munitions and legacy surface-to-air interceptors.
    </div>
  </div>

  <h3>The Payload-Range Frontier (Cost per kg·km)</h3>
  <p>To quantify true economic asymmetry in standoff strike, Apollyon measures weapons by <strong>cost per kg-km</strong> &mdash; the unit acquisition cost divided by the product of payload mass (kg) and operational range (km). Firing an exquisite cruise missile to deliver 200 kg over 1,000 km at ₹20 crore costs ₹1,000 per kg-km. Apollyon's family of turbojet strike systems drives this metric from ₹2,700/kg-km down to ₹35/kg-km across generations.</p>

  <div class="blueprint-plate">
    <div class="blueprint-head">
      <div class="title"><span class="glyph"></span>LOG-LOG COST CURVE · STRIKE ENVELOPE METRIC</div>
      <div class="scale">UNIT COST / [PAYLOAD × RANGE] · USD 1 = INR 95</div>
    </div>
    <div class="blueprint-body" style="padding: 10px;">
      <img src="assets/apollyon_cost_curve_dark.svg" alt="Apollyon Cost Curve vs Global Comparators in Service" style="width: 100%; height: auto; display: block;">
    </div>
    <div class="blueprint-cap">
      <b>Fig. 02</b> Logarithmic cost curve comparing legacy Western and Russian standoff munitions (Berkut-BM, Barracuda-250, Barracuda-500, Tomahawk Block V) against the Apollyon long-range strike family (Nightshade Mk II, Nightshade Mk III, Hemlock Mk I, Hemlock Mk II). Each generation inherits the shared core and amortizes guidance R&amp;D over expanding envelopes.
    </div>
  </div>
</section>

<section id="problem-solution">
  <div class="sec-tag">05 · Problem &amp; Solution</div>
  <h2>The Synthesis Architecture</h2>
  <p class="lede">Traditional defense models are trapped between prohibitive replacement costs and multi-decade procurement paralysis. Apollyon resolves this dual failure through software-driven hardware iteration and mass attritability.</p>

  <div class="synthesis-container">
    <div class="synthesis-card problem">
      <div class="sec-tag" style="color: var(--accent-red);">The Problem</div>
      <h3 style="color: #f87171; margin-top: 8px;">The Dual Crisis of Legacy Defence</h3>
      
      <h4 style="margin-top: 14px; font-size: 13.5px; color: var(--text-primary);">1. The Attrition Trap</h4>
      <p style="font-size: 13px; color: var(--text-muted); line-height: 1.5;">Modern peer conflicts consume precision munitions at staggering rates &mdash; 10,000+ drones per month and hundreds of strike rounds daily. Traditional primes build exquisite systems with 18-to-36 month production backlogs. When war begins, stockpiles are depleted within weeks, leaving armed forces unarmed before production can react.</p>
      
      <h4 style="margin-top: 14px; font-size: 13.5px; color: var(--text-primary);">2. Procurement Paralysis</h4>
      <p style="font-size: 13px; color: var(--text-muted); line-height: 1.5;">Legacy prime development cycles span 7 to 15 years. Cost-plus contracting disincentivizes cost reduction. By the time an exquisite platform reaches operational units, its electronic warfare profiles are obsolete, its compute hardware is two generations behind commercial silicon, and its unit cost prevents commanders from ever risking it in combat.</p>
    </div>

    <div class="synthesis-center">
      <div style="font-family: var(--mono); font-size: 10px; letter-spacing: 0.14em; color: var(--accent-cyan); text-transform: uppercase; margin-bottom: 6px;">The Neo-Prime Synthesis</div>
      <div style="font-family: var(--sans); font-weight: 800; font-size: 18px; line-height: 1.25; color: #ffffff; margin-bottom: 10px;">MASS ATTRITABLE PRECISION AT SOFTWARE VELOCITY</div>
      <div style="font-size: 12px; color: var(--text-secondary); line-height: 1.45;">Automotive-cadence production, sovereign edge guidance autonomy, and continuous software deployment: deterrence through volume that cannot be depleted and intelligence that cannot be jammed.</div>
    </div>

    <div class="synthesis-card solution">
      <div class="sec-tag" style="color: var(--accent-cyan);">The Solution</div>
      <h3 style="color: var(--accent-cyan); margin-top: 8px;">The Apollyon Neo-Prime Model</h3>
      
      <h4 style="margin-top: 14px; font-size: 13.5px; color: var(--text-primary);">1. ₹/kg-km Cost Asymmetry</h4>
      <p style="font-size: 13px; color: var(--text-muted); line-height: 1.5;">Re-engineering aerospace fabrication using out-of-autoclave resin-transfer composites, domestic turbojet propulsion (GTRE 350 kgf, indigenous micro-jets), and unburdened mechanical architectures. We deliver deep standoff strike for ₹35 to ₹300 per kg-km &mdash; a 10× to 100× economic advantage that makes salvo replenishment sustainable.</p>
      
      <h4 style="margin-top: 14px; font-size: 13.5px; color: var(--text-primary);">2. Continuous Software Cadence</h4>
      <p style="font-size: 13px; color: var(--text-muted); line-height: 1.5;">One shared flight software and navigation repository across all platforms. Sensor integration, guidance law revisions, and electronic counter-countermeasures (ECCM) deploy in days through high-fidelity hardware-in-the-loop simulation, keeping systems ahead of adversary EW adaptations.</p>
    </div>
  </div>
</section>

<section id="indias-window">
  <div class="sec-tag">06 · India's Strategic Window</div>
  <h2>The Macro Inflection: Built in India, Sold to the World</h2>
  <p class="lede">Between FY2020–21 and FY2025–26, India's defence market turned permanently inward. Capital reservations, indigenous production volumes, and private export mandates have aligned to create a unique generational window for an Indian neo-prime.</p>

  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: 16px; margin: 24px 0;">
    <div class="blueprint-plate" style="margin: 0;">
      <div class="blueprint-head">
        <div class="title"><span class="glyph"></span>DOMESTIC DEFENCE PRODUCTION</div>
        <div class="scale">MoD / DDP OFFICIAL DATA</div>
      </div>
      <div class="blueprint-body" style="padding: 8px;">
        <img src="assets/india_defence_production_dark.svg" alt="India Annual Defence Production Surge FY21 to FY26" style="width: 100%; height: auto; display: block;">
      </div>
      <div class="blueprint-cap">
        <b>Production</b> Output rose 4.1× from ₹43,746 Cr (FY14) to ₹1,78,000 Cr (FY26), with private industry contributing 24%. ₹1.39 lakh crore is earmarked exclusively for domestic industry in FY27 under the 75% capital reservation mandate.
      </div>
    </div>

    <div class="blueprint-plate" style="margin: 0;">
      <div class="blueprint-head">
        <div class="title"><span class="glyph"></span>DEFENCE EXPORT FOOTPRINT</div>
        <div class="scale">DDP SERIES · MoD RELEASES</div>
      </div>
      <div class="blueprint-body" style="padding: 8px;">
        <img src="assets/india_defence_exports_dark.svg" alt="India Defence Exports 56-Fold Expansion FY14 to FY26" style="width: 100%; height: auto; display: block;">
      </div>
      <div class="blueprint-cap">
        <b>Exports</b> Annual defence exports expanded 56-fold from ₹686 Cr (FY14) to ₹38,424 Cr (FY26). Private industry accounts for 45.16% (₹17,353 Cr), with 145 licensed firms exporting sovereign equipment across 80+ partner nations.
      </div>
    </div>
  </div>

  <p>The inflection point is structural, driven by three intersecting realities:</p>
  <ul>
    <li><strong>Geopolitical Necessity:</strong> India faces active confrontation on both continental borders &mdash; the high-altitude Himalayan LAC and the Western LoC &mdash; while expanding its maritime presence across the Indian Ocean Region. Conventional imported platforms cannot be replenished in the quantities a multi-front conflict consumes.</li>
    <li><strong>Policy Realignment:</strong> The Ministry of Defence's Defence Acquisition Procedure (DAP 2020) and successive Positive Indigenisation Lists (5,521+ items barred from import) have locked foreign primes out of domestic tenders where Indian solutions exist. Fast-track pathways like iDEX Prime and Make-II have compressed development cycle times from 104 weeks to under 22 weeks.</li>
    <li><strong>The Sovereign Global Export Market:</strong> Sovereign democracies throughout the Global South and Indo-Pacific face the identical dilemma: they cannot afford $3M Western interceptors, yet cannot accept politically conditioned weapons from autocratic regimes. Apollyon's posture is dual-engine: <em>engineered for sovereign resilience on India's frontiers, and exported to non-aligned democratic allies worldwide.</em></li>
  </ul>
</section>

<section id="strategic-dependency">
  <div class="sec-tag">07 · Strategic Dependency Corpus</div>
  <h2>Eight Decades of Strategic Impairment (1947–2026)</h2>
  <p class="lede">From 1947 to 2026, India's military operational effectiveness has been repeatedly impaired by foreign supplier refusals, wartime arms embargoes, spares blockades, and export-control denials. True sovereign deterrence cannot exist without eliminating these single-point vulnerabilities.</p>
  <p>The interactive corpus below catalogues <strong>70 documented historical episodes</strong> drawn from official records, declassified cables, and parliamentary reports across air, land, sea, propulsion, sensors, and electronic warfare. Click any card to inspect the foreign bottleneck, documented event, strategic consequence, and <strong>Apollyon's architectural countermeasure</strong>.</p>

  <div class="dep-controls">
    <div style="font-family: var(--mono); font-size: 11px; color: var(--text-muted); margin-right: 8px;">FILTER DOMAIN:</div>
    <button class="dep-btn active" data-filter="domain" data-val="all">All (70)</button>
    <button class="dep-btn" data-filter="domain" data-val="air">Air &amp; Strike</button>
    <button class="dep-btn" data-filter="domain" data-val="propulsion">Propulsion</button>
    <button class="dep-btn" data-filter="domain" data-val="sensors">Sensors &amp; EW</button>
    <button class="dep-btn" data-filter="domain" data-val="land">Land &amp; Munitions</button>
    <button class="dep-btn" data-filter="domain" data-val="naval">Naval &amp; Sea</button>
  </div>

  <div class="dep-controls" style="margin-top: -10px;">
    <div style="font-family: var(--mono); font-size: 11px; color: var(--text-muted); margin-right: 8px;">FILTER ERA:</div>
    <button class="dep-btn active" data-filter="era" data-val="all">All Eras</button>
    <button class="dep-btn" data-filter="era" data-val="1947–61">1947–1961</button>
    <button class="dep-btn" data-filter="era" data-val="1962–73">1962–1973</button>
    <button class="dep-btn" data-filter="era" data-val="1974–89">1974–1989</button>
    <button class="dep-btn" data-filter="era" data-val="1990–97">1990–1997</button>
    <button class="dep-btn" data-filter="era" data-val="1998–2003">1998–2003</button>
    <button class="dep-btn" data-filter="era" data-val="2004–13">2004–2013</button>
    <button class="dep-btn" data-filter="era" data-val="2014–19">2014–2019</button>
    <button class="dep-btn" data-filter="era" data-val="2020–26">2020–2026</button>
  </div>

  <div style="display: flex; justify-content: space-between; align-items: center; margin: 16px 0 12px; font-family: var(--mono); font-size: 11.5px;">
    <div id="dep-count" style="color: var(--accent-cyan);">Showing 70 of 70 documented episodes</div>
    <input id="dep-search" type="text" placeholder="Search episodes, platforms, OEMs (e.g. Kargil, LCA, GE F404, GPS)..." style="background: var(--bg-surface); border: 1px solid var(--border-subtle); color: var(--text-primary); font-family: var(--mono); font-size: 11px; padding: 6px 12px; border-radius: 4px; width: 320px; max-width: 100%;">
  </div>

  <div id="dep-grid" class="dep-grid">
    <!-- Populated dynamically via JavaScript -->
  </div>

  <div id="dep-modal-backdrop" class="dep-modal-backdrop">
    <div class="dep-modal">
      <button id="dep-modal-close" class="dep-modal-close" aria-label="Close modal">&times;</button>
      <div id="dep-modal-content">
        <!-- Injected via JavaScript -->
      </div>
    </div>
  </div>
</section>

<section id="classes">
  <div class="sec-tag">08 · Product classes</div>
  <h2>Three classes of product</h2>
  <p>The portfolio is organised by what a system does to the problem, not by what it looks like. Each class is a different answer to a different part of the military problem space, and each one develops capability that stays inside the organisation and becomes available to the next programme.</p>

  <div class="tw">
    <table>
      <caption>Class register</caption>
      <thead><tr><th>Class</th><th>Problem it answers</th><th>Systems</th></tr></thead>
      <tbody>
        <tr>
          <td>A · Standoff strike</td>
          <td>Deliver decisive, precise effect against defended and time-critical targets at operational and strategic depth, in salvo quantities a real campaign consumes.</td>
          <td><a href="products/hacm-350.html">HACM-350</a>, <a href="products/nightshade-adx1.html">Nightshade ADX-1</a>, <a href="products/usv-strike.html">Kamikaze USV</a></td>
        </tr>
        <tr>
          <td>B · Air defence &amp; counter-UAS</td>
          <td>Deny hostile reconnaissance drones and loitering munitions a hard kill at a cost that makes firing the round a rational decision.</td>
          <td><a href="products/ahuti.html">Ahuti Interceptor UAV</a></td>
        </tr>
        <tr>
          <td>C · Battlefield intelligence</td>
          <td>Mobile command, edge intelligence, and operational drone infrastructure for high-tempo tactical formations.</td>
          <td><a href="products/mobile-drone-lab.html">Mobile Drone Lab</a>, <a href="products/cortex.html">Apollyon Cortex</a>, <a href="products/mdcc.html">MDCC</a></td>
        </tr>
      </tbody>
    </table>
  </div>

  <p>Classes A and B share nearly their whole software stack; class C is the layer that coordinates, deploys, and sharpens what classes A and B can achieve in theatre.</p>
</section>

<section id="products">
  <div class="sec-tag">09 · Product register</div>
  <h2>Systems</h2>

  <h3>Class A · Standoff strike</h3>
  <div class="cards">
    <div class="card">
      <div class="kicker">Standoff cruise missile</div>
      <h3><a href="products/hacm-350.html">HACM-350</a></h3>
      <p>A 500–600 kg high-subsonic cruise missile built around the GTRE 350 kgf expendable turbojet, specified for ground launch from 4,500 m Himalayan elevations. 800–1,000 km at Mach 0.7–0.8 with a 120–150 kg penetrator, at ₹1.5–1.8 crore a round and 80–120 rounds a month. This is the system that occupies the <a href="doctrine/missing-middle.html">sovereign middle</a>.</p>
      <div class="foot"><span class="pill dev">TRL 4–8 · development</span><span>800–1,000 km</span></div>
    </div>
    <div class="card">
      <div class="kicker">Jet loitering munition</div>
      <h3><a href="products/nightshade-adx1.html">Nightshade ADX-1</a></h3>
      <p>A turbojet-powered loitering munition built to bridge the gap between expendable drones and cruise missiles. 650+ km/h cruise against a conventional 100–200 km/h loitering munition, a terminal dive over 380 km/h, swappable EO/IR and anti-radiation seekers, and navigation that survives GNSS denial. Three marks: Mk I (50 km), Mk II (300 km), Mk III (120–150 km).</p>
      <div class="foot"><span class="pill fielded">Flown · Mk I</span><span>650+ km/h</span></div>
    </div>
    <div class="card">
      <div class="kicker">Unmanned surface strike</div>
      <h3><a href="products/usv-strike.html">Kamikaze USV</a></h3>
      <p>An attritable, low-observable unmanned surface vessel designed for littoral standoff strike, maritime swarm attacks, and port/shipping denial. Delivers a heavy penetrating explosive warhead over maritime distances with autonomous non-satellite sea-surface navigation and terminal optical homing.</p>
      <div class="foot"><span class="pill dev">Development</span><span>Maritime Standoff</span></div>
    </div>
  </div>

  <h3>Class B · Air defence &amp; counter-UAS</h3>
  <div class="cards">
    <div class="card">
      <div class="kicker">High-speed interceptor</div>
      <h3><a href="products/ahuti.html">Ahuti Interceptor UAV</a></h3>
      <p>A short-range, high-speed interceptor for hostile reconnaissance drones and loitering munitions. Cued by ground radar in midcourse, handed to an onboard day/night seeker in the terminal phase. Carbon-fibre smart-infill airframe, clocked at 337 km/h and climbing (flown to 498 km/h). Kinetic and proximity-blast kill options. Tail-sitter vertical launch.</p>
      <div class="foot"><span class="pill dev">Mk-I flying · Mk-II in design</span><span>337–498 km/h</span></div>
    </div>
  </div>

  <h3>Class C · Battlefield intelligence</h3>
  <div class="cards">
    <div class="card">
      <div class="kicker">Field deployable infrastructure</div>
      <h3><a href="products/mobile-drone-lab.html">Mobile Drone Lab</a></h3>
      <p>A containerised, expeditionary technical facility providing rapid field maintenance, payload integration, diagnostic telemetry analysis, and mission configuration directly at the tactical edge.</p>
      <div class="foot"><span class="pill fielded">Fielded</span><span>Tactical edge</span></div>
    </div>
    <div class="card">
      <div class="kicker">Software platform</div>
      <h3><a href="products/cortex.html">Apollyon Cortex</a></h3>
      <p>The layer between every sensor a formation already receives and the people who need to act on it. Detect, analyse, assess, flag, escalate &mdash; then compose one assessment into the form each authorised user can act on. One operator supervises six to twenty ISR aircraft. 100% local processing, zero external dependency.</p>
      <div class="foot"><span class="pill dev">TRL 4–5 · development</span><span>6–20 aircraft / op</span></div>
    </div>
    <div class="card">
      <div class="kicker">Mobile command platform</div>
      <h3><a href="products/mdcc.html">Mobile Distributed Command Centre</a></h3>
      <p>Cortex as a platform you can drive to the edge of an operation. Compute, storage, networking and the whole intelligence stack on a vehicle, with every stage of processing running locally so the platform depends on nothing outside itself. Five deployment hosts, six primary mission roles.</p>
      <div class="foot"><span class="pill dev">TRL 4–5 · development</span><span>Zero external dep</span></div>
    </div>
  </div>
</section>

<section id="subsystems">
  <div class="sec-tag">10 · Subsystem register</div>
  <h2>Shared subsystems</h2>
  <p>Subsystems are the unit in which capability is actually accumulated. A subsystem page is the authority for that technology; product pages state their configuration of it and link here rather than restating it. Every drone-class vehicle in the portfolio carries the same control stack; every strike vehicle carries the same navigation philosophy.</p>

  <div class="cards">
    <div class="card">
      <div class="kicker">Guidance &amp; control</div>
      <h3><a href="subsystems/near-envelope-control.html">Robust Control for Fast Air Platforms</a></h3>
      <p>High-rate closed-loop flight control and physics-grounded modeling engineered for extreme dynamic pressures, high-G transitions, and actuator saturation. Integrates our physics backbone and simulation-to-real workflow to guarantee aerodynamic stability where standard linear models fail.</p>
      <div class="foot"><span class="pill core">Core</span><span>Ahuti · Nightshade · HACM-350</span></div>
    </div>
    <div class="card">
      <div class="kicker">High-mach navigation</div>
      <h3><a href="subsystems/gnss-denied-navigation.html">High-Speed GNSS-Denied Navigation</a></h3>
      <p>Engineered for Mach 0.8 cruise missiles and high-subsonic strike airframes penetrating heavily contested electronic warfare theaters &mdash; far beyond low-speed 200 km/h drones. Fuses multi-element CRPA spatial nulling (&gt;45 dB) with high-speed optical odometry and topological terrain scene correlation.</p>
      <div class="foot"><span class="pill core">Core</span><span>HACM-350 · Nightshade · USV</span></div>
    </div>
    <div class="card">
      <div class="kicker">Edge compute &amp; silicon</div>
      <h3><a href="subsystems/onboard-compute.html">Edge Compute &amp; Custom Inference Engine</a></h3>
      <p>Hardware-software co-design delivering deterministic real-time scheduling on isolated cores, hand-tuned custom CUDA kernels for sensor and tensor bottlenecks, and a proprietary custom-built edge inference engine tailored for extreme compute efficiency per watt.</p>
      <div class="foot"><span class="pill core">Core</span><span>Sub-millisecond loop</span></div>
    </div>
    <div class="card">
      <div class="kicker">Flight software</div>
      <h3><a href="subsystems/flight-software.html">Flight Software Stack</a></h3>
      <p>Built upon nearly two decades of global open-source autopilot maturity (PX4, ArduPilot), re-engineered for natively autonomous, high-subsonic strike weapons requiring direct-actuator neural control, custom low-latency scheduling, and high-rate logging.</p>
      <div class="foot"><span class="pill core">Core</span><span>All flying systems</span></div>
    </div>
    <div class="card">
      <div class="kicker">Terminal guidance</div>
      <h3><a href="subsystems/seekers.html">Seekers &amp; terminal guidance</a></h3>
      <p>One airframe, swappable seekers. Passive EO/IR imaging for point targets independent of satellite navigation; passive anti-radiation homing for SEAD; automatic scene matching for the terminal dive.</p>
      <div class="foot"><span class="pill core">Core</span><span>Nightshade · HACM-350 · Ahuti</span></div>
    </div>
    <div class="card">
      <div class="kicker">Propulsion</div>
      <h3><a href="subsystems/propulsion.html">Propulsion</a></h3>
      <p>The turbojet line from small expendable jet-class engines up to the GTRE 350 kgf, and the high-altitude thrust derate that governs every Himalayan-launched design. Thrust margin is what buys a steep terminal dive.</p>
      <div class="foot"><span class="pill core">Core</span><span>HACM-350 · Nightshade</span></div>
    </div>
    <div class="card">
      <div class="kicker">Structures</div>
      <h3><a href="subsystems/airframe-structures.html">Airframe &amp; structures</a></h3>
      <p>Fully composite low-drag bodies, carbon-fibre smart-infill, stamped bulkheads and out-of-autoclave resin transfer moulding &mdash; chosen so that the structure can be produced by India's existing precision and automotive base rather than by an aerospace autoclave queue.</p>
      <div class="foot"><span class="pill core">Core</span><span>All airframes</span></div>
    </div>
    <div class="card">
      <div class="kicker">Ground segment</div>
      <h3><a href="subsystems/launch-systems.html">Launch &amp; ground systems</a></h3>
      <p>Ground-mobile launchers with &le;30 minute deployment readiness, catapult, vehicular rail and hand launch for the small vehicles, and containerised zero-length rail with solid booster for the heavy round.</p>
      <div class="foot"><span class="pill core">Core</span><span>&le;30 min ready</span></div>
    </div>
  </div>
</section>

<section id="matrix">
  <div class="sec-tag">11 · Commonality</div>
  <h2>Which product carries which subsystem</h2>
  <p>The point of the table below is the vertical reading. A subsystem that appears in three columns is a subsystem whose next improvement lands in three products at once.</p>
  <div class="tw">
    <table>
      <caption>Subsystem × product matrix</caption>
      <thead><tr>
        <th>Subsystem</th><th>HACM-350</th><th>Nightshade</th><th>Ahuti</th><th>Kamikaze USV</th><th>Cortex / MDCC / Lab</th>
      </tr></thead>
      <tbody>
        <tr><td><a href="subsystems/near-envelope-control.html">Robust Control for Fast Platforms</a></td><td>High-Mach dive</td><td>Terminal dive</td><td>Primary</td><td>Sea-state trim</td><td>—</td></tr>
        <tr><td><a href="subsystems/gnss-denied-navigation.html">High-Speed GNSS-Denied Nav (CRPA + Scene)</a></td><td>AI-DSMAC + CRPA</td><td>Scene match + CRPA</td><td>Optical / INS</td><td>Coastline match</td><td>—</td></tr>
        <tr><td><a href="subsystems/onboard-compute.html">Edge Compute &amp; Custom Inference</a></td><td>Edge correlator</td><td>Cortex edge</td><td>Cortex edge</td><td>Edge guidance</td><td>Inference core</td></tr>
        <tr><td><a href="subsystems/flight-software.html">Flight Software Stack</a></td><td>High-rate core</td><td>Autonomous core</td><td>Direct control</td><td>Maritime stack</td><td>Diagnostic link</td></tr>
        <tr><td><a href="subsystems/seekers.html">Seekers &amp; Terminal Guidance</a></td><td>LWIR / visible</td><td>EO/IR · ARH</td><td>Day/night optical</td><td>Thermal seeker</td><td>—</td></tr>
        <tr><td><a href="subsystems/propulsion.html">Propulsion</a></td><td>GTRE 350 kgf</td><td>Micro-turbojet</td><td>High-RPM propfan</td><td>High-speed marine</td><td>—</td></tr>
        <tr><td><a href="subsystems/airframe-structures.html">Airframe &amp; structures</a></td><td>Composite / stamped</td><td>Composite delta</td><td>CF smart-infill</td><td>Low-RCS hull</td><td>Shelter / van</td></tr>
        <tr><td><a href="subsystems/launch-systems.html">Launch &amp; ground</a></td><td>Rail + booster</td><td>Mobile launcher</td><td>Tail-sitter vertical</td><td>Cradle launch</td><td>Field lab &amp; MDCC</td></tr>
      </tbody>
    </table>
  </div>
</section>

<section id="record">
  <div class="sec-tag">12 · Record</div>
  <h2>Proof, not pitch decks</h2>
  <p>Progress is measured through validated performance, reliability, production yield, qualification, field acceptance, test maturity and the speed with which each generation improves on the last. The full chronology is on the <a href="about/history.html">history page</a>; the short version is that the company had no connections in the defence establishment, wrote to colonels, drove hardware to Chandigarh, and flew it in front of people who had seen a hundred pitches.</p>

  <figure>
    <img src="assets/deployed-locations.jpg" alt="Map of deployed locations across India — seven units, four theatres">
    <figcaption><b>Fig. 03</b> Seven operational units across four military theatres: Jammu and Udhampur (J&amp;K), Chandimandir (Chandigarh), Arunachal Pradesh, and Bengaluru (Karnataka).</figcaption>
  </figure>

  <div class="tags">
    <span>First Army order · ₹2,68,000</span>
    <span>15 Guards · letter</span>
    <span>181 Mountain Brigade · Lohitpur</span>
    <span>MOU with BSF · Dec 2025</span>
    <span>Coast Guard · 88 ACV</span>
    <span>Nightshade launch day · Jun 2026</span>
  </div>
</section>

<footer>
  <div>Apollyon Dynamics · Engineering Wiki · Rev 2.0 (Neo-Prime)</div>
  <div><a href="doctrine/new-arsenal.html">The New Arsenal</a> · <a href="about/history.html">History</a> · apollyondynamics.com</div>
</footer>

</main>
</div>
</div>

<!-- Load Dependency Corpus Data -->
<script src="js/dependency_corpus_data.js"></script>

<!-- Interactive Dependency Corpus Logic -->
<script>
(function() {
  const data = window.DEPENDENCY_CORPUS || [];
  const grid = document.getElementById('dep-grid');
  const countEl = document.getElementById('dep-count');
  const searchInput = document.getElementById('dep-search');
  const modalBackdrop = document.getElementById('dep-modal-backdrop');
  const modalClose = document.getElementById('dep-modal-close');
  const modalContent = document.getElementById('dep-modal-content');

  let activeDomain = 'all';
  let activeEra = 'all';
  let searchTerm = '';

  function getApollyonResponse(item) {
    const domain = (item.Domain || '').toLowerCase();
    const episode = (item.Episode || '').toLowerCase();
    const bottleneck = (item['Foreign-controlled bottleneck'] || '').toLowerCase();

    if (domain.includes('propulsion') || bottleneck.includes('engine') || bottleneck.includes('turbofan') || episode.includes('engine')) {
      return "Apollyon architects all jet strike systems around indigenous domestic propulsion — specifically the GTRE 350 kgf turbojet and Indian micro-jets — eliminating reliance on foreign ITAR/MTCR controlled engines (e.g. GE F404, Rolls-Royce Adour).";
    }
    if (episode.includes('gps') || bottleneck.includes('gps') || bottleneck.includes('satellite') || domain.includes('space')) {
      return "Apollyon permanently solves satellite vulnerability through a unified GNSS-denied navigation stack: 4-element CRPA spatial nulling (>45 dB suppression) fused with high-speed topological optical scene odometry (AI-DSMAC) and drift-bounded INS that never depends on foreign constellations.";
    }
    if (domain.includes('air') && (bottleneck.includes('aircraft') || bottleneck.includes('spares') || episode.includes('airframe'))) {
      return "Apollyon manufactures out-of-autoclave composite airframes and stamped bulkheads using India's vast precision automotive base, enabling rate-production of 80–120 strike rounds/month without foreign airframe dependencies.";
    }
    if (domain.includes('sensor') || domain.includes('c4isr') || bottleneck.includes('seeker') || bottleneck.includes('radar')) {
      return "Apollyon integrates sovereign multi-spectral EO/IR seekers with domestic strategic partners (Tonbo Imaging) and runs proprietary neural edge inference models directly on local silicon, keeping seeker software entirely sovereign.";
    }
    if (domain.includes('land') || domain.includes('munitions') || bottleneck.includes('ammunition')) {
      return "Apollyon replaces scarce foreign precision munitions with mass attritable strike weapons designed for automotive run-rate manufacturing, allowing continuous salvo replenishment from domestic Indian supply chains.";
    }
    if (domain.includes('flight') || domain.includes('software') || bottleneck.includes('fly-by-wire') || bottleneck.includes('avionics')) {
      return "Apollyon completely owns its flight software stack and guidance algorithms, derived from hardened deterministic cores with direct neural actuator control, eliminating foreign black-box avionics.";
    }
    return "Apollyon's vertically integrated neo-prime model replaces imported high-cost platforms with mass attritable, software-defined systems engineered entirely within India's industrial and sovereign software base.";
  }

  function filterItems() {
    return data.filter(item => {
      // Domain filter
      if (activeDomain !== 'all') {
        const d = (item.Domain || '').toLowerCase();
        if (activeDomain === 'air' && !d.includes('air')) return false;
        if (activeDomain === 'propulsion' && !d.includes('propulsion')) return false;
        if (activeDomain === 'sensors' && !(d.includes('sensor') || d.includes('c4isr') || d.includes('space') || d.includes('ew') || d.includes('computing'))) return false;
        if (activeDomain === 'land' && !d.includes('land') && !d.includes('munitions')) return false;
        if (activeDomain === 'naval' && !d.includes('naval') && !d.includes('sea')) return false;
      }
      // Era filter
      if (activeEra !== 'all' && item.Era !== activeEra) {
        return false;
      }
      // Search filter
      if (searchTerm) {
        const q = searchTerm.toLowerCase();
        const text = [
          item.Episode,
          item.Domain,
          item['External actor / OEM'],
          item['Foreign-controlled bottleneck'],
          item['Documented event'],
          item['Conflict / trigger']
        ].join(' ').toLowerCase();
        if (!text.includes(q)) return false;
      }
      return true;
    });
  }

  function render() {
    const items = filterItems();
    countEl.textContent = `Showing ${items.length} of ${data.length} documented episodes`;

    if (items.length === 0) {
      grid.innerHTML = '<div style="grid-column: 1/-1; padding: 32px; text-align: center; color: var(--text-muted); font-family: var(--mono); font-size: 13px;">No documented dependency episodes match your filter criteria.</div>';
      return;
    }

    grid.innerHTML = items.map(item => {
      const sevClass = item.Severity === 5 ? 'sev-5' : (item.Severity === 4 ? 'sev-4' : 'sev-3');
      const sevLabel = item.Severity === 5 ? 'SEV 5 · WARTIME DENIAL' : (item.Severity === 4 ? 'SEV 4 · CRISIS EMBARGO' : 'SEV 3 · TECH CONTROL');
      return `
        <div class="dep-card" data-id="${item.ID}">
          <div class="dep-card-head">
            <span style="color: var(--accent-cyan); font-weight: 700;">${item['Date / period']} · ${item.Domain}</span>
            <span class="dep-badge ${sevClass}">${sevLabel}</span>
          </div>
          <div style="font-weight: 600; font-size: 14px; color: var(--text-primary); margin-bottom: 6px; line-height: 1.35;">${item.Episode}</div>
          <div style="font-size: 11px; font-family: var(--mono); color: var(--text-muted); margin-bottom: 8px;">Actor: <strong style="color: var(--text-secondary);">${item['External actor / OEM']}</strong></div>
          <div style="font-size: 12.5px; color: var(--text-muted); line-height: 1.45; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;">${item['Documented event']}</div>
          <div style="margin-top: 10px; font-family: var(--mono); font-size: 10.5px; color: var(--accent-cyan); display: flex; align-items: center; gap: 4px;">Inspect episode &amp; countermeasure &rarr;</div>
        </div>
      `;
    }).join('');
  }

  // Filter click handlers
  document.querySelectorAll('.dep-btn').forEach(btn => {
    btn.addEventListener('click', function() {
      const type = this.getAttribute('data-filter');
      const val = this.getAttribute('data-val');

      document.querySelectorAll(`.dep-btn[data-filter="${type}"]`).forEach(b => b.classList.remove('active'));
      this.classList.add('active');

      if (type === 'domain') activeDomain = val;
      if (type === 'era') activeEra = val;
      render();
    });
  });

  // Search handler
  searchInput.addEventListener('input', function(e) {
    searchTerm = e.target.value.trim();
    render();
  });

  // Card click -> modal
  grid.addEventListener('click', function(e) {
    const card = e.target.closest('.dep-card');
    if (!card) return;
    const id = card.getAttribute('data-id');
    const item = data.find(x => x.ID === id);
    if (!item) return;

    const sevClass = item.Severity === 5 ? 'sev-5' : (item.Severity === 4 ? 'sev-4' : 'sev-3');
    const sevDesc = item.Severity === 5 ? 'Severity 5: Direct Wartime Denial / Embargo during Active Hostilities' : (item.Severity === 4 ? 'Severity 4: Crisis Impairment / Pre-War Sanctions' : 'Severity 3: Peacetime MTCR & Non-Proliferation Technology Denial');
    const countermeasure = getApollyonResponse(item);

    modalContent.innerHTML = `
      <div style="font-family: var(--mono); font-size: 11px; color: var(--accent-cyan); text-transform: uppercase; margin-bottom: 6px;">EPISODE ${item.ID} · ${item['Date / period']} · ${item.Domain}</div>
      <h2 style="font-size: 20px; line-height: 1.3; margin-bottom: 12px; color: #ffffff;">${item.Episode}</h2>
      
      <div style="margin-bottom: 18px;">
        <span class="dep-badge ${sevClass}" style="font-size: 11px; padding: 4px 8px;">${sevDesc}</span>
      </div>

      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; background: rgba(14, 20, 32, 0.8); border: 1px solid var(--border-subtle); border-radius: 4px; padding: 12px 16px; margin-bottom: 18px; font-size: 12px; font-family: var(--mono);">
        <div><span style="color: var(--text-muted);">External Actor:</span> <strong style="color: var(--text-primary);">${item['External actor / OEM']}</strong></div>
        <div><span style="color: var(--text-muted);">Conflict / Trigger:</span> <strong style="color: var(--text-primary);">${item['Conflict / trigger'] || 'N/A'}</strong></div>
        <div style="grid-column: 1 / -1;"><span style="color: var(--text-muted);">Foreign Bottleneck:</span> <strong style="color: #f87171;">${item['Foreign-controlled bottleneck']}</strong></div>
      </div>

      <div style="margin-bottom: 16px;">
        <h4 style="font-size: 12px; font-family: var(--mono); text-transform: uppercase; color: var(--text-muted); margin-bottom: 4px;">Documented Historical Event</h4>
        <p style="font-size: 13.5px; line-height: 1.55; color: var(--text-primary); margin: 0;">${item['Documented event']}</p>
      </div>

      <div style="margin-bottom: 16px;">
        <h4 style="font-size: 12px; font-family: var(--mono); text-transform: uppercase; color: var(--text-muted); margin-bottom: 4px;">Operational &amp; Strategic Consequence</h4>
        <p style="font-size: 13.5px; line-height: 1.55; color: #fbbf24; margin: 0;">${item['Operational / strategic consequence']}</p>
      </div>

      <div style="margin-bottom: 18px; padding-left: 14px; border-left: 2px solid var(--border-medium);">
        <h4 style="font-size: 11px; font-family: var(--mono); text-transform: uppercase; color: var(--text-muted); margin-bottom: 2px;">The Strategic Lesson</h4>
        <p style="font-size: 13px; font-style: italic; color: var(--text-secondary); margin: 0;">&ldquo;${item['Strategic lesson']}&rdquo;</p>
      </div>

      <div style="background: rgba(10, 132, 255, 0.08); border: 1px solid rgba(10, 132, 255, 0.3); border-radius: 4px; padding: 14px 16px; margin-bottom: 16px;">
        <div style="font-family: var(--mono); font-size: 11px; font-weight: 700; color: var(--accent-cyan); text-transform: uppercase; margin-bottom: 6px; display: flex; align-items: center; gap: 6px;">
          <span style="display:inline-block; width:6px; height:6px; background:var(--accent-cyan); border-radius:50%;"></span>
          Apollyon Sovereign Countermeasure
        </div>
        <p style="font-size: 13px; line-height: 1.5; color: var(--text-primary); margin: 0;">${countermeasure}</p>
      </div>

      ${item['Primary URL'] ? `
        <div style="font-family: var(--mono); font-size: 10.5px; color: var(--text-muted); border-top: 1px solid var(--border-subtle); padding-top: 12px;">
          Verified Primary Source: <a href="${item['Primary URL']}" target="_blank" rel="noopener noreferrer" style="color: var(--accent-cyan); word-break: break-all;">${item['Primary URL']}</a>
        </div>
      ` : ''}
    `;

    modalBackdrop.style.display = 'grid';
    document.body.style.overflow = 'hidden';
  });

  // Modal close handlers
  function closeModal() {
    modalBackdrop.style.display = 'none';
    document.body.style.overflow = '';
  }
  modalClose.addEventListener('click', closeModal);
  modalBackdrop.addEventListener('click', function(e) {
    if (e.target === modalBackdrop) closeModal();
  });
  window.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') closeModal();
  });

  // Initial render
  render();
})();
</script>

</body>
</html>
"""

with open('wiki/index.html', 'w') as f:
    f.write(html_content.strip() + '\n')

print("Successfully wrote wiki/index.html")
