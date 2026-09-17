import os

print("Building Apollyon wiki pages...")

# 1. wiki/products/usv-strike.html
usv_html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Kamikaze USV · Standoff Maritime Strike — Apollyon Dynamics Wiki</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,wght@0,400;0,500;1,400&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../css/wiki.css">
</head>
<body>

<div class="rail">
  <div class="rail-inner">
    <a class="rail-brand" href="../index.html"><span class="glyph"></span>Apollyon Dynamics <em>· Engineering Wiki</em></a>
    <nav class="rail-links">
      <a href="../index.html#products" class="on">Products</a>
      <a href="../index.html#subsystems">Subsystems</a>
      <a href="../doctrine/new-arsenal.html">Doctrine</a>
      <a href="../about/history.html">History</a>
    </nav>
  </div>
</div>

<div class="shell">
<div class="layout">

<aside class="aside">
  <h4>This page</h4>
  <ul>
    <li><a href="#specs">Specifications</a></li>
    <li><a href="#blueprint">CAD schematic</a></li>
    <li><a href="#usecases">Operational usecases</a></li>
    <li><a href="#specifics">Engineering specifics</a></li>
    <li><a href="#marine-nav">Non-satellite nav</a></li>
    <li><a href="#hydrodynamics">Sea-state control</a></li>
    <li><a href="#warhead">Shaped-charge warhead</a></li>
    <li><a href="#subsystems">Shared subsystems</a></li>
  </ul>
  <h4>Products</h4>
  <ul>
    <li><a href="hacm-350.html">HACM-350</a></li>
    <li><a href="nightshade-adx1.html">Nightshade ADX-1</a></li>
    <li><a href="usv-strike.html" class="here">Kamikaze USV</a></li>
    <li><a href="ahuti.html">Ahuti Interceptor</a></li>
    <li><a href="mobile-drone-lab.html">Mobile Drone Lab</a></li>
    <li><a href="cortex.html">Apollyon Cortex</a></li>
    <li><a href="mdcc.html">MDCC</a></li>
  </ul>
  <h4>Subsystems</h4>
  <ul>
    <li><a href="../subsystems/near-envelope-control.html">Robust control for fast platforms</a></li>
    <li><a href="../subsystems/gnss-denied-navigation.html">High-speed GNSS-denied nav</a></li>
    <li><a href="../subsystems/onboard-compute.html">Edge compute &amp; inference</a></li>
    <li><a href="../subsystems/flight-software.html">Flight software stack</a></li>
    <li><a href="../subsystems/seekers.html">Seekers &amp; terminal guidance</a></li>
    <li><a href="../subsystems/propulsion.html">Propulsion</a></li>
    <li><a href="../subsystems/airframe-structures.html">Airframe &amp; structures</a></li>
    <li><a href="../subsystems/launch-systems.html">Launch &amp; ground systems</a></li>
  </ul>
  <h4>Doctrine</h4>
  <ul>
    <li><a href="../doctrine/new-arsenal.html">The New Arsenal</a></li>
    <li><a href="../doctrine/precision-is-mercy.html">Precision is Mercy</a></li>
    <li><a href="../doctrine/missing-middle.html">The missing middle</a></li>
  </ul>
</aside>

<main class="main">

<div class="crumb"><a href="../index.html">Wiki</a><span>/</span><a href="../index.html#products">Products</a><span>/</span>Class A · Standoff strike<span>/</span>Kamikaze USV</div>

<header class="masthead">
  <div class="mast-meta">Maritime standoff strike · Unmanned Surface Vehicle <span>· Class A · development programme · rev 1.2</span></div>
  <h1>Kamikaze USV <span class="sub">Maritime Strike Vessel</span></h1>
  <p class="standfirst">An attritable, low-observable unmanned surface vessel designed for littoral standoff strike, maritime swarm saturation, and port/shipping denial. Delivers a heavy penetrating shaped-charge warhead over 800+ km with autonomous non-satellite sea-surface navigation and terminal optical homing.</p>
</header>

<section id="specs">
  <div class="sec-tag">01 · Specification</div>
  <h2>Primary engineering baseline</h2>

  <div class="spec-card">
    <div class="spec-topbar"><span>Kamikaze USV · at a glance</span><span class="right">Class A Standoff Strike · Littoral Interdiction · Sovereign Design</span></div>
    <div class="spec-grid">
      <div class="spec-col">
        <div class="spec-col-title">Hull &amp; vessel</div>
        <div class="row"><div class="lbl">Displacement (full load)</div><div class="val">1,150 kg</div></div>
        <div class="row"><div class="lbl">Dry weight</div><div class="val">580 kg</div></div>
        <div class="row"><div class="lbl">Length overall (LOA)</div><div class="val">5.80 m</div></div>
        <div class="row"><div class="lbl">Beam overall (BOA)</div><div class="val">1.40 m</div></div>
        <div class="row"><div class="lbl">Draft (static / planning)</div><div class="val">0.38 m / 0.18 m</div></div>
        <div class="row"><div class="lbl">Radar cross section (X-band)</div><div class="val accent">&lt; 0.05 m² (stealth faceted)</div></div>
      </div>
      <div class="spec-col">
        <div class="spec-col-title">Propulsion &amp; kinematics</div>
        <div class="row"><div class="lbl">Engine type</div><div class="val">High-output marine turbo-diesel</div></div>
        <div class="row"><div class="lbl">Power output</div><div class="val">260 hp (194 kW)</div></div>
        <div class="row"><div class="lbl">Drive mechanism</div><div class="val">Twin steerable waterjets</div></div>
        <div class="row"><div class="lbl">Sprint speed (calm sea)</div><div class="val accent">48+ knots (88+ km/h)</div></div>
        <div class="row"><div class="lbl">Economical cruise speed</div><div class="val">28–32 knots</div></div>
        <div class="row"><div class="lbl">Operational range</div><div class="val accent">800+ km (430+ nm)</div></div>
      </div>
      <div class="spec-col">
        <div class="spec-col-title">Lethality &amp; payload</div>
        <div class="row"><div class="lbl">Primary warhead</div><div class="val accent">250–300 kg HE shaped charge</div></div>
        <div class="row"><div class="lbl">Penetration capability</div><div class="val">&gt; 80 mm naval steel RHA</div></div>
        <div class="row"><div class="lbl">Fuse mechanism</div><div class="val">Tri-mode: impact, delayed, optical</div></div>
        <div class="row"><div class="lbl">Target classes</div><div class="val">Corvettes, frigates, LSTs, piers</div></div>
        <div class="row"><div class="lbl">Sea state rating</div><div class="val">Operates SS-4 · Survives SS-5</div></div>
        <div class="row"><div class="lbl">Swarm coordination</div><div class="val">Apollyon Mesh P2P link</div></div>
      </div>
      <div class="spec-col">
        <div class="spec-col-title">Guidance &amp; autonomy</div>
        <div class="row"><div class="lbl">Anti-jam GNSS</div><div class="val">NavIC L5/S + GPS (CRPA nulling)</div></div>
        <div class="row"><div class="lbl">GNSS-denied navigation</div><div class="val">Coastline DSMAC + visual INS</div></div>
        <div class="row"><div class="lbl">Terminal seeker</div><div class="val">Stabilised dual EO/MWIR sensor</div></div>
        <div class="row"><div class="lbl">Terminal guidance</div><div class="val">Waterline tracking AI correlator</div></div>
        <div class="row"><div class="lbl">Unit production target</div><div class="val">₹45–65 Lakh per unit</div></div>
        <div class="row"><div class="lbl">Build methodology</div><div class="val">Infused carbon-aramid composite</div></div>
      </div>
    </div>
  </div>

  <div class="note">
    <div class="t">Doctrine alignment</div>
    <p>Naval surface combatants cost hundreds to thousands of crores and take half a decade to construct. The Kamikaze USV costs under a crore, can be built at rate by civilian boatbuilders using out-of-autoclave resin infusion, and forces hostile naval forces to expend multi-crore surface-to-air or anti-ship missiles to defend their hulls. At 800+ km range, it projects offensive sovereign power deep into littoral choke points.</p>
  </div>
</section>

<section id="blueprint">
  <div class="sec-tag">02 · Schematic</div>
  <h2>Internal architecture &amp; CAD layout</h2>

  <div class="blueprint-plate">
    <div class="blueprint-head">
      <div class="title">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/></svg>
        FIG. 01 &mdash; Kamikaze USV Planform &amp; Internal Equipment Packaging
      </div>
      <span class="scale">Scale: 1:30 · Length: 5,800 mm · Dimensions in Millimetres</span>
    </div>
    <div class="blueprint-body">
      <svg viewBox="0 0 960 300" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="CAD schematic of Kamikaze USV">
        <defs>
          <pattern id="cad_grid_usv" width="20" height="20" patternUnits="userSpaceOnUse">
            <line x1="0" y1="0" x2="20" y2="0" stroke="rgba(56,189,248,0.06)" stroke-width="1"/>
            <line x1="0" y1="0" x2="0" y2="20" stroke="rgba(56,189,248,0.06)" stroke-width="1"/>
          </pattern>
          <pattern id="hatch_wh_usv" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
            <line x1="0" y1="0" x2="0" y2="6" stroke="#f43f5e" stroke-width="1" opacity="0.4"/>
          </pattern>
          <pattern id="hatch_fuel_usv" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(-45)">
            <line x1="0" y1="0" x2="0" y2="6" stroke="#38bdf8" stroke-width="1" opacity="0.3"/>
          </pattern>
        </defs>

        <rect width="960" height="300" fill="#0d1117"/>
        <rect width="960" height="300" fill="url(#cad_grid_usv)"/>

        <!-- Centerline Datum -->
        <line x1="40" y1="150" x2="920" y2="150" stroke="#38bdf8" stroke-width="0.8" stroke-dasharray="12,4,2,4" opacity="0.6"/>
        <text x="45" y="142" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="8" opacity="0.7">DATUM £ / KEEL CENTERLINE</text>

        <!-- Hull Contour (Stealth Faceted Wave-Piercing Monohull) -->
        <path d="M 80 150 L 140 100 L 320 85 L 680 90 L 880 105 L 880 195 L 680 210 L 320 215 L 140 200 Z" fill="none" stroke="#f8fafc" stroke-width="1.8"/>

        <!-- Internal Chine & Deck Facets -->
        <path d="M 80 150 L 160 120 L 340 105 L 680 108 L 870 120" fill="none" stroke="#94a3b8" stroke-width="0.9" stroke-dasharray="3,2"/>
        <path d="M 80 150 L 160 180 L 340 195 L 680 192 L 870 180" fill="none" stroke="#94a3b8" stroke-width="0.9" stroke-dasharray="3,2"/>

        <!-- Transom Flat -->
        <line x1="880" y1="105" x2="880" y2="195" stroke="#38bdf8" stroke-width="2"/>

        <!-- Bulkhead Lines (Watertight Subdivisions) -->
        <line x1="130" y1="102" x2="130" y2="198" stroke="#38bdf8" stroke-width="1.2" stroke-dasharray="2,2"/>
        
        <!-- Warhead Compartment: STA 0500-1800 (x=130 to x=320) -->
        <rect x="135" y="105" width="180" height="90" fill="url(#hatch_wh_usv)" stroke="#f43f5e" stroke-width="1.2" rx="4"/>
        <text x="225" y="146" fill="#f43f5e" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" text-anchor="middle">280 kg HE WARHEAD</text>
        <text x="225" y="160" fill="#f43f5e" font-family="JetBrains Mono, monospace" font-size="7.5" text-anchor="middle">COPPER SHAPED-CHARGE LINER</text>

        <!-- Midship Bulkhead: x=320 -->
        <line x1="320" y1="85" x2="320" y2="215" stroke="#38bdf8" stroke-width="1.5"/>

        <!-- Avionics, Compute & Optical Mast Bay: STA 1800-2800 (x=320 to x=460) -->
        <rect x="325" y="100" width="130" height="100" fill="rgba(56,189,248,0.06)" stroke="#38bdf8" stroke-width="1"/>
        <!-- EO/MWIR Mast -->
        <circle cx="370" cy="150" r="14" fill="#0d1117" stroke="#38bdf8" stroke-width="1.5"/>
        <circle cx="370" cy="150" r="8" fill="#38bdf8" opacity="0.4"/>
        <text x="370" y="153" fill="#ffffff" font-family="JetBrains Mono, monospace" font-size="7" font-weight="700" text-anchor="middle">EO/IR</text>
        <!-- Edge Compute Unit -->
        <rect x="400" y="130" width="45" height="40" fill="none" stroke="#22c55e" stroke-width="1"/>
        <text x="422" y="153" fill="#22c55e" font-family="JetBrains Mono, monospace" font-size="6.5" font-weight="700" text-anchor="middle">EDGE AI</text>

        <!-- Fuel Bay (Baffled Self-Sealing Diesel Cells): STA 2800-4200 (x=460 to x=640) -->
        <line x1="460" y1="88" x2="460" y2="212" stroke="#38bdf8" stroke-width="1.5"/>
        <rect x="465" y="94" width="170" height="112" fill="url(#hatch_fuel_usv)" stroke="#38bdf8" stroke-width="1.2" rx="3"/>
        <line x1="550" y1="94" x2="550" y2="206" stroke="#38bdf8" stroke-width="0.8" stroke-dasharray="4,2"/>
        <text x="550" y="146" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="9" font-weight="700" text-anchor="middle">DIESEL FUEL CELL (480 L)</text>
        <text x="550" y="160" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="7.5" text-anchor="middle">RANGE &gt; 800 KM @ 30 KTS</text>

        <!-- Engine Room Bulkhead: x=640 -->
        <line x1="640" y1="90" x2="640" y2="210" stroke="#38bdf8" stroke-width="1.5"/>

        <!-- Turbo-Diesel Engine: STA 4200-5200 (x=640 to x=790) -->
        <rect x="650" y="115" width="135" height="70" fill="rgba(245,158,11,0.08)" stroke="#f59e0b" stroke-width="1.2" rx="2"/>
        <text x="717" y="146" fill="#f59e0b" font-family="JetBrains Mono, monospace" font-size="9" font-weight="700" text-anchor="middle">260 HP TURBO-DIESEL</text>
        <text x="717" y="160" fill="#f59e0b" font-family="JetBrains Mono, monospace" font-size="7.5" text-anchor="middle">ACOUSTIC DAMPED ENCLOSURE</text>

        <!-- Driveshaft & Waterjet Bay: STA 5200-5800 (x=790 to x=880) -->
        <line x1="790" y1="95" x2="790" y2="205" stroke="#38bdf8" stroke-width="1.2"/>
        <!-- Waterjets -->
        <rect x="840" y="118" width="50" height="26" fill="#1e293b" stroke="#38bdf8" stroke-width="1.2"/>
        <rect x="840" y="156" width="50" height="26" fill="#1e293b" stroke="#38bdf8" stroke-width="1.2"/>
        <path d="M 890 120 L 920 124 L 920 138 L 890 142 Z" fill="rgba(56,189,248,0.2)" stroke="#38bdf8" stroke-width="1"/>
        <path d="M 890 158 L 920 162 L 920 176 L 890 180 Z" fill="rgba(56,189,248,0.2)" stroke="#38bdf8" stroke-width="1"/>
        <text x="895" y="110" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="7.5">TWIN WATERJETS</text>

        <!-- Station Lines & Callouts -->
        <g stroke="#38bdf8" stroke-width="0.7" opacity="0.6">
          <line x1="80" y1="40" x2="80" y2="85"/>
          <line x1="130" y1="40" x2="130" y2="85"/>
          <line x1="320" y1="40" x2="320" y2="85"/>
          <line x1="460" y1="40" x2="460" y2="85"/>
          <line x1="640" y1="40" x2="640" y2="85"/>
          <line x1="880" y1="40" x2="880" y2="85"/>
        </g>
        <g fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="7.5" opacity="0.8">
          <text x="80" y="35" text-anchor="middle">STA 0000</text>
          <text x="130" y="35" text-anchor="middle">STA 0500</text>
          <text x="320" y="35" text-anchor="middle">STA 1800</text>
          <text x="460" y="35" text-anchor="middle">STA 2800</text>
          <text x="640" y="35" text-anchor="middle">STA 4200</text>
          <text x="880" y="35" text-anchor="middle">STA 5800</text>
        </g>

        <!-- Dimension arrows below -->
        <g stroke="#94a3b8" stroke-width="0.8">
          <line x1="80" y1="260" x2="880" y2="260"/>
          <line x1="80" y1="255" x2="80" y2="265"/>
          <line x1="880" y1="255" x2="880" y2="265"/>
        </g>
        <text x="480" y="275" fill="#f8fafc" font-family="JetBrains Mono, monospace" font-size="9" text-anchor="middle">OVERALL LENGTH: 5,800 MM · BEAM: 1,400 MM · DEPTH: 980 MM</text>
      </svg>
    </div>
    <div class="blueprint-cap">
      <b>CAD Station Reference</b> &mdash; Structural arrangement of the Kamikaze USV. From left: wave-piercing bow impact sensor (STA 0000–0500), 280 kg shaped-charge warhead cavity (STA 0500–1800), stabilised optical mast and isolated edge compute core (STA 1800–2800), baffled 480 L diesel tank (STA 2800–4200), turbocharged marine diesel (STA 4200–5200), and dual vectored waterjets with hydraulic trim tabs (STA 5200–5800).
    </div>
  </div>
</section>

<section id="usecases">
  <div class="sec-tag">03 · Operational roles</div>
  <h2>Primary usecases &amp; doctrine</h2>
  <p class="lede">The Kamikaze USV is engineered to project lethal asymmetric power across disputed littoral zones, island chains, and hostile anchorages where conventional naval vessels cannot operate without excessive risk.</p>

  <div class="tw">
    <table>
      <caption>Operational mission sets</caption>
      <thead><tr><th>Mission</th><th>Operational problem</th><th>USV solution</th></tr></thead>
      <tbody>
        <tr>
          <td><strong>Littoral interdiction</strong></td>
          <td>Hostile amphibious task forces and surface combatants operating within sovereign Exclusive Economic Zones (EEZ) and island territories.</td>
          <td>Continuous semi-submerged patrol; radar cross-section under 0.05 m² delays radar detection until within 2–3 km, enabling high-speed 48-knot interception.</td>
        </tr>
        <tr>
          <td><strong>Swarm saturation strike</strong></td>
          <td>Modern multi-function naval radars and Close-In Weapon Systems (CIWS) engage isolated surface targets with high kill probability.</td>
          <td>Salvos of 8–16 USVs coordinate arrival via mesh radio; multiple craft converge simultaneously from dispersed 360° bearings to overwhelm tracking channels.</td>
        </tr>
        <tr>
          <td><strong>Port &amp; anchorage denial</strong></td>
          <td>Heavily defended enemy naval bases, submarine pens, and ammunition loading jetties shielded by GPS jammers and surface booms.</td>
          <td>Autonomous non-satellite navigation using shoreline DSMAC matching; sneaks through harbour mouths and strikes high-value moored combatants at the waterline.</td>
        </tr>
        <tr>
          <td><strong>Choke point interdiction</strong></td>
          <td>Strategic maritime straits where commercial and naval transit can be selectively blockaded or contested during heightened conflict.</td>
          <td>Silent low-speed loitering (under 6 knots on auxiliary electric drive) for up to 36 hours before spooling main diesel for sprint attack.</td>
        </tr>
      </tbody>
    </table>
  </div>
</section>

<section id="specifics">
  <div class="sec-tag">04 · Engineering specifics</div>
  <h2>Deep technical architecture</h2>

  <h3 id="marine-nav">A · Non-satellite sea-surface navigation</h3>
  <p>Satellite denial over open water presents unique challenges: unlike land terrain, the open sea has no static topographic features for elevation correlation. The Kamikaze USV employs a layered navigation stack built specifically for marine environments:</p>
  <ul>
    <li><strong>CRPA Anti-Jam GNSS:</strong> Indigenous multi-element antenna suppresses coastal jammers by &gt;45 dB, maintaining NavIC/GPS lock during initial transit.</li>
    <li><strong>Hydro-Inertial Dead Reckoning:</strong> High-grade tactical IMUs fused with Doppler Velocity Logs (DVL) measuring acoustic speed over seabed, filtering out surface current drift.</li>
    <li><strong>Coastline DSMAC:</strong> As the vessel nears target archipelagos, ports, or coastlines, high-resolution optical cameras match shoreline profiles, headlands, and navigation marks against pre-loaded commercial satellite maps.</li>
    <li><strong>Optical Waterline Tracking:</strong> In the terminal 3 km run, dual daylight/MWIR stabilised cameras lock onto ship hull silhouettes, ignoring decoys, chaff, and smoke screens.</li>
  </ul>

  <h3 id="hydrodynamics">B · Sea-state 4 hydrodynamic stability &amp; waterjet control</h3>
  <p>Transiting at 45+ knots in rough seas induces extreme wave-slamming forces, propeller cavitation, and hull broaching. Apollyon's robust control stack solves these dynamics in real time:</p>
  <ul>
    <li><strong>Wave-Piercing Faceted Monohull:</strong> Sharp knife-bow pierces oncoming waves rather than riding over them, significantly reducing vertical G-loads on internal components.</li>
    <li><strong>Dynamic Waterjet Vectoring:</strong> Twin steerable waterjets eliminate exposed rudders and propellers, preventing damage from debris, nets, or shallow shoals.</li>
    <li><strong>Active Trim Control:</strong> High-speed hydraulic interceptor tabs respond at 100 Hz via the onboard edge compute core, continuously trimming pitch and roll to prevent porpoising at sprint speeds.</li>
  </ul>

  <h3 id="warhead">C · Heavy shaped-charge penetrating warhead</h3>
  <p>Unlike blast-only drone boats that produce superficial topside damage, the Kamikaze USV integrates a custom-engineered 250–300 kg shaped-charge warhead designed to compromise naval structural integrity:</p>
  <ul>
    <li><strong>Waterline &amp; Sub-Surface Impact:</strong> The vessel trims down immediately prior to impact, detonating against the target's hull right at or below the waterline.</li>
    <li><strong>Copper Jet Penetration:</strong> The precision-machined conical copper liner generates a hyper-velocity metal jet capable of penetrating over 80 mm of hardened naval steel armor, flooding critical boiler rooms and magazine bays.</li>
    <li><strong>Tri-Mode Fuse Architecture:</strong> Redundant piezoelectric bow contact switches, delayed penetrator inertia sensors, and an optical standoff trigger ensure lethal detonation even during glancing blows.</li>
  </ul>
</section>

<section id="subsystems">
  <div class="sec-tag">05 · Shared subsystems</div>
  <h2>Subsystems powering this vessel</h2>
  <div class="cards">
    <div class="card">
      <div class="kicker">Guidance &amp; control</div>
      <h3><a href="../subsystems/near-envelope-control.html">Robust Control for Fast Platforms</a></h3>
      <p>Adapted from our flight dynamics core to manage high-speed hydrodynamic surface stability, wave-slamming rejection, and active waterjet trim.</p>
    </div>
    <div class="card">
      <div class="kicker">Navigation</div>
      <h3><a href="../subsystems/gnss-denied-navigation.html">High-Speed GNSS-Denied Navigation</a></h3>
      <p>Fuses anti-jam CRPA NavIC/GPS with coastline DSMAC scene correlation and hydro-inertial odometry for long-range sea transit.</p>
    </div>
    <div class="card">
      <div class="kicker">Compute</div>
      <h3><a href="../subsystems/onboard-compute.html">Edge Compute &amp; Custom Inference Engine</a></h3>
      <p>Runs sub-millisecond waterline tracking, obstacle avoidance, and peer-to-peer swarm mesh coordination on ruggedized isolated cores.</p>
    </div>
    <div class="card">
      <div class="kicker">Software</div>
      <h3><a href="../subsystems/flight-software.html">Flight Software Stack</a></h3>
      <p>Deterministic runtime and telemetry logging engine adapted for mission-critical marine strike execution.</p>
    </div>
  </div>
</section>

<footer>
  <div>Kamikaze USV · Standoff Maritime Strike · Class A · Rev 1.2</div>
  <div><a href="../index.html">Wiki root</a> · <a href="../index.html#matrix">Commonality matrix</a> · apollyondynamics.com</div>
</footer>

</main>
</div>
</div>
</body>
</html>
"""

with open('/home/soham-kumar/soham/apollyon/deck/wiki/products/usv-strike.html', 'w') as f:
    f.write(usv_html)

print("Kamikaze USV page written successfully.")

# 2. wiki/products/mobile-drone-lab.html
lab_html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Mobile Drone Lab · Tactical Expeditionary Infrastructure — Apollyon Dynamics Wiki</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,wght@0,400;0,500;1,400&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../css/wiki.css">
</head>
<body>

<div class="rail">
  <div class="rail-inner">
    <a class="rail-brand" href="../index.html"><span class="glyph"></span>Apollyon Dynamics <em>· Engineering Wiki</em></a>
    <nav class="rail-links">
      <a href="../index.html#products" class="on">Products</a>
      <a href="../index.html#subsystems">Subsystems</a>
      <a href="../doctrine/new-arsenal.html">Doctrine</a>
      <a href="../about/history.html">History</a>
    </nav>
  </div>
</div>

<div class="shell">
<div class="layout">

<aside class="aside">
  <h4>This page</h4>
  <ul>
    <li><a href="#specs">Specifications</a></li>
    <li><a href="#blueprint">CAD schematic</a></li>
    <li><a href="#usecases">Operational usecases</a></li>
    <li><a href="#specifics">Engineering specifics</a></li>
    <li><a href="#hil-harness">HIL diagnostic suite</a></li>
    <li><a href="#mission-prep">Edge mission planning</a></li>
    <li><a href="#shelter-eng">Ruggedized shelter</a></li>
    <li><a href="#subsystems">Shared subsystems</a></li>
  </ul>
  <h4>Products</h4>
  <ul>
    <li><a href="hacm-350.html">HACM-350</a></li>
    <li><a href="nightshade-adx1.html">Nightshade ADX-1</a></li>
    <li><a href="usv-strike.html">Kamikaze USV</a></li>
    <li><a href="ahuti.html">Ahuti Interceptor</a></li>
    <li><a href="mobile-drone-lab.html" class="here">Mobile Drone Lab</a></li>
    <li><a href="cortex.html">Apollyon Cortex</a></li>
    <li><a href="mdcc.html">MDCC</a></li>
  </ul>
  <h4>Subsystems</h4>
  <ul>
    <li><a href="../subsystems/near-envelope-control.html">Robust control for fast platforms</a></li>
    <li><a href="../subsystems/gnss-denied-navigation.html">High-speed GNSS-denied nav</a></li>
    <li><a href="../subsystems/onboard-compute.html">Edge compute &amp; inference</a></li>
    <li><a href="../subsystems/flight-software.html">Flight software stack</a></li>
    <li><a href="../subsystems/seekers.html">Seekers &amp; terminal guidance</a></li>
    <li><a href="../subsystems/propulsion.html">Propulsion</a></li>
    <li><a href="../subsystems/airframe-structures.html">Airframe &amp; structures</a></li>
    <li><a href="../subsystems/launch-systems.html">Launch &amp; ground systems</a></li>
  </ul>
  <h4>Doctrine</h4>
  <ul>
    <li><a href="../doctrine/new-arsenal.html">The New Arsenal</a></li>
    <li><a href="../doctrine/precision-is-mercy.html">Precision is Mercy</a></li>
    <li><a href="../doctrine/missing-middle.html">The missing middle</a></li>
  </ul>
</aside>

<main class="main">

<div class="crumb"><a href="../index.html">Wiki</a><span>/</span><a href="../index.html#products">Products</a><span>/</span>Class C · Battlefield intelligence<span>/</span>Mobile Drone Lab</div>

<header class="masthead">
  <div class="mast-meta">Expeditionary maintenance &amp; mission planning <span>· Class C · Fielded operational system · rev 1.4</span></div>
  <h1>Mobile Drone Lab <span class="sub">Tactical Expeditionary Facility</span></h1>
  <p class="standfirst">A containerised, high-mobility expeditionary technical facility providing rapid field maintenance, diagnostic telemetry analysis, automated hardware-in-the-loop validation, and offline mission data generation directly at the tactical edge.</p>
</header>

<section id="specs">
  <div class="sec-tag">01 · Specification</div>
  <h2>Primary engineering baseline</h2>

  <div class="spec-card">
    <div class="spec-topbar"><span>Mobile Drone Lab · at a glance</span><span class="right">Class C Battlefield Intelligence · Forward Deployed · Fielded</span></div>
    <div class="spec-grid">
      <div class="spec-col">
        <div class="spec-col-title">Shelter &amp; mobility</div>
        <div class="row"><div class="lbl">Form factor</div><div class="val">20-ft ISO 1CC container</div></div>
        <div class="row"><div class="lbl">Deployment host</div><div class="val">6x6 tactical truck (TATRA / Leyland)</div></div>
        <div class="row"><div class="lbl">Dimensions (transit)</div><div class="val">6.05 m × 2.44 m × 2.59 m</div></div>
        <div class="row"><div class="lbl">Expanded workspace</div><div class="val accent">14.8 m² (bilateral gull-wings)</div></div>
        <div class="row"><div class="lbl">Setup / tear-down time</div><div class="val accent">&le; 20 minutes (2 operators)</div></div>
        <div class="row"><div class="lbl">Air transportability</div><div class="val">C-130J, Il-76, C-17 roll-on</div></div>
      </div>
      <div class="spec-col">
        <div class="spec-col-title">Turnaround &amp; diagnostics</div>
        <div class="row"><div class="lbl">Turnaround capacity</div><div class="val accent">12–16 airframes / 8-hr shift</div></div>
        <div class="row"><div class="lbl">Pre-flight checkout time</div><div class="val accent">&lt; 6 minutes / airframe</div></div>
        <div class="row"><div class="lbl">HIL simulation rate</div><div class="val">1,000 Hz real-time closed-loop</div></div>
        <div class="row"><div class="lbl">Rate table axes</div><div class="val">3-axis servo rate table (&plusmn;200°/s)</div></div>
        <div class="row"><div class="lbl">Seeker collimator</div><div class="val">Dual visible / LWIR collimator</div></div>
        <div class="row"><div class="lbl">Composite repair</div><div class="val">Vacuum debulk + hot-bonder curing</div></div>
      </div>
      <div class="spec-col">
        <div class="spec-col-title">Edge compute &amp; networking</div>
        <div class="row"><div class="lbl">Processing core</div><div class="val">Dual ruggedized Cortex GPU nodes</div></div>
        <div class="row"><div class="lbl">Local storage</div><div class="val accent">128 TB NVMe encrypted store</div></div>
        <div class="row"><div class="lbl">Terrain route compile</div><div class="val">&lt; 90 seconds (DEM + DSMAC)</div></div>
        <div class="row"><div class="lbl">Cryptographic provisioning</div><div class="val">Air-gapped zero-trace zeroizer</div></div>
        <div class="row"><div class="lbl">Comms tether</div><div class="val">Mil-spec tactical optical fiber</div></div>
        <div class="row"><div class="lbl">Wireless link</div><div class="val">Auto-pointing Ku/Ka SATCOM + mesh</div></div>
      </div>
      <div class="spec-col">
        <div class="spec-col-title">Power &amp; environment</div>
        <div class="row"><div class="lbl">Tactical generator</div><div class="val">15 kVA silent diesel (&lt;55 dBA)</div></div>
        <div class="row"><div class="lbl">Silent battery buffer</div><div class="val">48V 24 kWh LiFePO4 (6 hr silent)</div></div>
        <div class="row"><div class="lbl">Solar array</div><div class="val">2.4 kW folding monocrystalline</div></div>
        <div class="row"><div class="lbl">Operating temperature</div><div class="val">-30°C to +55°C</div></div>
        <div class="row"><div class="lbl">Filtration &amp; shielding</div><div class="val accent">CBRN overpressure · Tempest EMI</div></div>
        <div class="row"><div class="lbl">Field status</div><div class="val accent">Fielded · active Army orders</div></div>
      </div>
    </div>
  </div>

  <div class="note">
    <div class="t">The operational reality</div>
    <p>Autonomous strike weapons and interceptors cannot function as pristine laboratory prototypes in a high-intensity mountain or desert war. They arrive in crates on rough trails, undergo rapid re-tasking, suffer handling wear, and operate under complete satellite denial. The Mobile Drone Lab brings prime-grade diagnostic and integration capability straight to the battalion tactical operations center.</p>
  </div>
</section>

<section id="blueprint">
  <div class="sec-tag">02 · Schematic</div>
  <h2>Expeditionary container layout &amp; CAD blueprint</h2>

  <div class="blueprint-plate">
    <div class="blueprint-head">
      <div class="title">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/></svg>
        FIG. 01 &mdash; Mobile Drone Lab 20-Ft Shelter Internal Station Layout
      </div>
      <span class="scale">Scale: 1:35 · Dimensions in Millimetres · Length: 6,058 mm</span>
    </div>
    <div class="blueprint-body">
      <svg viewBox="0 0 960 300" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="CAD layout schematic of Mobile Drone Lab">
        <defs>
          <pattern id="cad_grid_lab" width="20" height="20" patternUnits="userSpaceOnUse">
            <line x1="0" y1="0" x2="20" y2="0" stroke="rgba(56,189,248,0.06)" stroke-width="1"/>
            <line x1="0" y1="0" x2="0" y2="20" stroke="rgba(56,189,248,0.06)" stroke-width="1"/>
          </pattern>
          <pattern id="hatch_power_lab" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
            <line x1="0" y1="0" x2="0" y2="6" stroke="#f59e0b" stroke-width="1" opacity="0.35"/>
          </pattern>
          <pattern id="hatch_compute_lab" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(-45)">
            <line x1="0" y1="0" x2="0" y2="6" stroke="#22c55e" stroke-width="1" opacity="0.35"/>
          </pattern>
        </defs>

        <rect width="960" height="300" fill="#0d1117"/>
        <rect width="960" height="300" fill="url(#cad_grid_lab)"/>

        <!-- Datum centerline -->
        <line x1="40" y1="150" x2="920" y2="150" stroke="#38bdf8" stroke-width="0.8" stroke-dasharray="12,4,2,4" opacity="0.5"/>
        <text x="45" y="142" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="8" opacity="0.7">DATUM £ / SHELTER AXIS</text>

        <!-- Container Outer Walls (20-ft ISO: x=80 to x=880, y=70 to y=230) -->
        <rect x="80" y="70" width="800" height="160" fill="none" stroke="#f8fafc" stroke-width="2" rx="2"/>

        <!-- Corner Castings (ISO standard) -->
        <rect x="80" y="70" width="16" height="16" fill="#1e293b" stroke="#38bdf8" stroke-width="1.2"/>
        <rect x="864" y="70" width="16" height="16" fill="#1e293b" stroke="#38bdf8" stroke-width="1.2"/>
        <rect x="80" y="214" width="16" height="16" fill="#1e293b" stroke="#38bdf8" stroke-width="1.2"/>
        <rect x="864" y="214" width="16" height="16" fill="#1e293b" stroke="#38bdf8" stroke-width="1.2"/>

        <!-- Expandable Gull-Wing Bay Outlines (dotted) -->
        <path d="M 220 70 L 220 40 L 740 40 L 740 70" fill="none" stroke="#38bdf8" stroke-width="1" stroke-dasharray="4,3"/>
        <path d="M 220 230 L 220 260 L 740 260 L 740 230" fill="none" stroke="#38bdf8" stroke-width="1" stroke-dasharray="4,3"/>
        <text x="480" y="52" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="7.5" text-anchor="middle">EXPANDABLE GULL-WING WORKSPACE BAY (PORT)</text>
        <text x="480" y="254" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="7.5" text-anchor="middle">EXPANDABLE GULL-WING WORKSPACE BAY (STBD)</text>

        <!-- Partition 1: Power & HVAC Bay (STA 0000-1200: x=80 to x=220) -->
        <line x1="220" y1="70" x2="220" y2="230" stroke="#38bdf8" stroke-width="1.5"/>
        <rect x="96" y="80" width="114" height="140" fill="url(#hatch_power_lab)" stroke="#f59e0b" stroke-width="1.2" rx="3"/>
        <text x="153" y="135" fill="#f59e0b" font-family="JetBrains Mono, monospace" font-size="8.5" font-weight="700" text-anchor="middle">15 kVA SILENT</text>
        <text x="153" y="148" fill="#f59e0b" font-family="JetBrains Mono, monospace" font-size="8.5" font-weight="700" text-anchor="middle">DIESEL + HVAC</text>
        <text x="153" y="165" fill="#f59e0b" font-family="JetBrains Mono, monospace" font-size="7" text-anchor="middle">24 kWh LiFePO4</text>
        <text x="153" y="177" fill="#f59e0b" font-family="JetBrains Mono, monospace" font-size="7" text-anchor="middle">CBRN FILTER</text>

        <!-- Partition 2: Avionics Umbilical Checkout (STA 1200-2600: x=220 to x=380) -->
        <line x1="380" y1="70" x2="380" y2="230" stroke="#38bdf8" stroke-width="1.5"/>
        <rect x="230" y="80" width="140" height="60" fill="rgba(56,189,248,0.08)" stroke="#38bdf8" stroke-width="1"/>
        <text x="300" y="105" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="8" font-weight="700" text-anchor="middle">AVIONICS DIAGNOSTIC</text>
        <text x="300" y="118" fill="#94a3b8" font-family="JetBrains Mono, monospace" font-size="7" text-anchor="middle">AUTONOMOUS HARNESS JIG</text>

        <rect x="230" y="160" width="140" height="60" fill="rgba(56,189,248,0.08)" stroke="#38bdf8" stroke-width="1"/>
        <text x="300" y="185" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="8" font-weight="700" text-anchor="middle">BATTERY CYCLER</text>
        <text x="300" y="198" fill="#94a3b8" font-family="JetBrains Mono, monospace" font-size="7" text-anchor="middle">RAPID CELL BALANCING</text>

        <!-- Partition 3: HIL 3-Axis Table & Seeker Bay (STA 2600-4200: x=380 to x=560) -->
        <line x1="560" y1="70" x2="560" y2="230" stroke="#38bdf8" stroke-width="1.5"/>
        <!-- 3-Axis Rate Table -->
        <circle cx="470" cy="150" r="32" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5"/>
        <circle cx="470" cy="150" r="18" fill="rgba(56,189,248,0.2)" stroke="#38bdf8" stroke-width="1"/>
        <text x="470" y="147" fill="#ffffff" font-family="JetBrains Mono, monospace" font-size="7.5" font-weight="700" text-anchor="middle">3-AXIS HIL</text>
        <text x="470" y="159" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="6.5" text-anchor="middle">RATE TABLE</text>
        <!-- Seeker Collimator Bench -->
        <rect x="390" y="80" width="80" height="36" fill="#1e293b" stroke="#38bdf8" stroke-width="1"/>
        <text x="430" y="102" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="6.5" text-anchor="middle">COLLIMATOR</text>
        <!-- Synthetic RF Emitter -->
        <rect x="390" y="184" width="80" height="36" fill="#1e293b" stroke="#38bdf8" stroke-width="1"/>
        <text x="430" y="206" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="6.5" text-anchor="middle">RF EMITTER</text>

        <!-- Partition 4: Apollyon Cortex Server Rack (STA 4200-5200: x=560 to x=700) -->
        <line x1="700" y1="70" x2="700" y2="230" stroke="#38bdf8" stroke-width="1.5"/>
        <rect x="575" y="80" width="110" height="140" fill="url(#hatch_compute_lab)" stroke="#22c55e" stroke-width="1.2" rx="3"/>
        <text x="630" y="135" fill="#22c55e" font-family="JetBrains Mono, monospace" font-size="8.5" font-weight="700" text-anchor="middle">CORTEX EDGE</text>
        <text x="630" y="148" fill="#22c55e" font-family="JetBrains Mono, monospace" font-size="8.5" font-weight="700" text-anchor="middle">SERVER RACK</text>
        <text x="630" y="165" fill="#22c55e" font-family="JetBrains Mono, monospace" font-size="7" text-anchor="middle">DUAL GPU NODES</text>
        <text x="630" y="177" fill="#22c55e" font-family="JetBrains Mono, monospace" font-size="7" text-anchor="middle">128 TB NVMe REPO</text>

        <!-- Partition 5: Composite Repair & Modular Airframe Racks (STA 5200-6058: x=700 to x=880) -->
        <rect x="715" y="80" width="145" height="60" fill="rgba(56,189,248,0.08)" stroke="#38bdf8" stroke-width="1"/>
        <text x="787" y="105" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="8" font-weight="700" text-anchor="middle">COMPOSITE HOT-BONDER</text>
        <text x="787" y="118" fill="#94a3b8" font-family="JetBrains Mono, monospace" font-size="7" text-anchor="middle">VACUUM PATCH JIG</text>

        <rect x="715" y="160" width="145" height="60" fill="rgba(56,189,248,0.08)" stroke="#38bdf8" stroke-width="1"/>
        <text x="787" y="185" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="8" font-weight="700" text-anchor="middle">MODULAR AIRFRAME RACKS</text>
        <text x="787" y="198" fill="#94a3b8" font-family="JetBrains Mono, monospace" font-size="7" text-anchor="middle">NIGHTSHADE · AHUTI SPARES</text>

        <!-- Station indicators above -->
        <g stroke="#38bdf8" stroke-width="0.7" opacity="0.6">
          <line x1="80" y1="20" x2="80" y2="70"/>
          <line x1="220" y1="20" x2="220" y2="70"/>
          <line x1="380" y1="20" x2="380" y2="70"/>
          <line x1="560" y1="20" x2="560" y2="70"/>
          <line x1="700" y1="20" x2="700" y2="70"/>
          <line x1="880" y1="20" x2="880" y2="70"/>
        </g>
        <g fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="7.5" opacity="0.8">
          <text x="80" y="15" text-anchor="middle">STA 0000</text>
          <text x="220" y="15" text-anchor="middle">STA 1200</text>
          <text x="380" y="15" text-anchor="middle">STA 2600</text>
          <text x="560" y="15" text-anchor="middle">STA 4200</text>
          <text x="700" y="15" text-anchor="middle">STA 5200</text>
          <text x="880" y="15" text-anchor="middle">STA 6058</text>
        </g>

        <!-- Dimension indicator below -->
        <g stroke="#94a3b8" stroke-width="0.8">
          <line x1="80" y1="280" x2="880" y2="280"/>
          <line x1="80" y1="275" x2="80" y2="285"/>
          <line x1="880" y1="275" x2="880" y2="285"/>
        </g>
        <text x="480" y="294" fill="#f8fafc" font-family="JetBrains Mono, monospace" font-size="9" text-anchor="middle">20-FT ISO CONTAINER LENGTH: 6,058 MM · WIDTH: 2,438 MM · HEIGHT: 2,591 MM</text>
      </svg>
    </div>
    <div class="blueprint-cap">
      <b>CAD Station Reference</b> &mdash; Internal equipment layout of the Mobile Drone Lab 20-ft tactical shelter. From left: quiet 15 kVA diesel generator, LiFePO4 battery bank, and CBRN/HVAC filtration (STA 0000–1200); automated avionics diagnostic and battery cycler benches (STA 1200–2600); 3-axis rate table and optical collimator bay (STA 2600–4200); Apollyon Cortex dual-GPU server rack and 128 TB NVMe mission store (STA 4200–5200); and vacuum composite repair jigs with modular airframe spare racks (STA 5200–6058).
    </div>
  </div>
</section>

<section id="usecases">
  <div class="sec-tag">03 · Operational roles</div>
  <h2>Primary usecases &amp; doctrine</h2>
  <p class="lede">The Mobile Drone Lab transforms rough tactical perimeters into self-sufficient aerospace integration nodes, removing reliance on distant rear-echelon depots.</p>

  <div class="tw">
    <table>
      <caption>Mission usecases</caption>
      <thead><tr><th>Role</th><th>Field challenge</th><th>Mobile Drone Lab solution</th></tr></thead>
      <tbody>
        <tr>
          <td><strong>Forward expeditionary staging</strong></td>
          <td>Delivering precision weapons and loitering munitions to front-line battalions requires final wing assembly and pre-flight validation.</td>
          <td>Deploys on a 6x6 truck within 20 minutes; unpacks, mates wings, performs automated umbilical checks, and readies 12–16 airframes per shift.</td>
        </tr>
        <tr>
          <td><strong>Battle-damage quick turnaround</strong></td>
          <td>Tactical drones and reusable interceptors sustain landing fractures, motor overheating, or shrapnel gouges during operational sorties.</td>
          <td>Onboard composite hot-bonder cures carbon-fiber structural patches in under 45 minutes; rapid motor and ESC balancing returns aircraft to combat service immediately.</td>
        </tr>
        <tr>
          <td><strong>Offline mission data ingestion</strong></td>
          <td>Cloud connectivity and commercial internet are severed under intense electronic warfare and sovereign operational security protocols.</td>
          <td>128 TB onboard NVMe stores continental DEM and multispectral satellite maps; generates mission routes and AI-DSMAC packages in under 90 seconds.</td>
        </tr>
        <tr>
          <td><strong>Cryptographic key zeroization</strong></td>
          <td>Weapons captured in unexploded states risk compromising national tactical datalinks and frequency hopsets.</td>
          <td>Air-gapped crypto console loads time-delimited sovereign mission keys directly into weapon secure enclaves prior to rail launch.</td>
        </tr>
      </tbody>
    </table>
  </div>
</section>

<section id="specifics">
  <div class="sec-tag">04 · Engineering specifics</div>
  <h2>Deep technical architecture</h2>

  <h3 id="hil-harness">A · Hardware-in-the-Loop (HIL) diagnostic suite</h3>
  <p>Rather than relying on basic continuity checks, the Mobile Drone Lab connects every weapon to a high-rate Hardware-in-the-Loop harness before flight:</p>
  <ul>
    <li><strong>3-Axis Dynamic Rate Table:</strong> Mounts the weapon's IMU on a high-precision servo table, simulating aggressive turns (&plusmn;200°/s) and measuring sensor output fidelity.</li>
    <li><strong>Synthetic Sensor Injection:</strong> Directly streams synthetic optical frames and radio frequency signatures into the weapon's guidance computer, verifying lock-on algorithms against target models.</li>
    <li><strong>Full Sortie Simulation:</strong> The weapon's flight software flies an entire 800 km simulated trajectory in the lab, verifying that control loops, bus latencies, and thermal margins remain strictly within specification.</li>
  </ul>

  <h3 id="mission-prep">B · Edge mission planning &amp; AI-DSMAC packet compilation</h3>
  <p>Weapons operating in GNSS-denied environments depend on precise pre-loaded terrain profiles. The lab's integrated Cortex server processes these packets locally:</p>
  <ul>
    <li><strong>Digital Elevation Model (DEM) Slicing:</strong> Sub-meter elevation contours along the intended flight path are extracted and compressed into under 150 MB mission footprints.</li>
    <li><strong>Topological Feature Rendering:</strong> Satellite imagery is processed to generate multi-angle lighting profiles, ensuring the weapon's onboard correlator recognizes ridgelines and infrastructure under varying sun conditions.</li>
    <li><strong>Waypoint &amp; No-Fly Deconfliction:</strong> Route planners automatically trace low-altitude terrain-masking paths through mountain valleys, keeping radar exposure below detection thresholds.</li>
  </ul>

  <h3 id="shelter-eng">C · Ruggedized all-weather shelter engineering</h3>
  <p>Engineered to operate in high-altitude Ladakh winters, Thar desert dust storms, and monsoon humidity:</p>
  <ul>
    <li><strong>CBRN Overpressure &amp; Dust Filtration:</strong> Positive internal pressure prevents chemical contaminants and fine abrasive dust from entering optical calibration rooms.</li>
    <li><strong>Tempest EMI Shielding:</strong> Attenuates electromagnetic radiation by &gt;60 dB, preventing enemy electronic surveillance units from detecting shelter operations.</li>
    <li><strong>Vibration Isolation:</strong> The rate table and optical benches sit on isolated pneumatic floor dampeners, maintaining sub-milliradian precision even when external diesel engines run.</li>
  </ul>
</section>

<section id="subsystems">
  <div class="sec-tag">05 · Shared subsystems</div>
  <h2>Subsystems hosted &amp; maintained</h2>
  <div class="cards">
    <div class="card">
      <div class="kicker">Compute platform</div>
      <h3><a href="cortex.html">Apollyon Cortex</a></h3>
      <p>Acts as the forward edge server node running localized situational awareness, sensor fusion, and multi-UAV supervision.</p>
    </div>
    <div class="card">
      <div class="kicker">Command node</div>
      <h3><a href="mdcc.html">Mobile Distributed Command Centre</a></h3>
      <p>Directly interfaces with MDCC tactical vehicles, sharing real-time diagnostic health and mission readiness data.</p>
    </div>
    <div class="card">
      <div class="kicker">Simulation core</div>
      <h3><a href="../subsystems/near-envelope-control.html">Robust Control for Fast Platforms</a></h3>
      <p>Validates vehicle neural policies on the HIL rate table before release to operational flight lines.</p>
    </div>
    <div class="card">
      <div class="kicker">Navigation</div>
      <h3><a href="../subsystems/gnss-denied-navigation.html">High-Speed GNSS-Denied Navigation</a></h3>
      <p>Compiles and uploads AI-DSMAC terrain packages and elevation grids directly into missile onboard flash memory.</p>
    </div>
  </div>
</section>

<footer>
  <div>Mobile Drone Lab · Class C · Fielded · Rev 1.4</div>
  <div><a href="../index.html">Wiki root</a> · <a href="../index.html#matrix">Commonality matrix</a> · apollyondynamics.com</div>
</footer>

</main>
</div>
</div>
</body>
</html>
"""

with open('/home/soham-kumar/soham/apollyon/deck/wiki/products/mobile-drone-lab.html', 'w') as f:
    f.write(lab_html)

print("Mobile Drone Lab page written successfully.")

# 3. wiki/subsystems/near-envelope-control.html
control_html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Robust Control for Fast Air Platforms — Apollyon Dynamics Wiki</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,wght@0,400;0,500;1,400&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../css/wiki.css">
</head>
<body>

<div class="rail">
  <div class="rail-inner">
    <a class="rail-brand" href="../index.html"><span class="glyph"></span>Apollyon Dynamics <em>· Engineering Wiki</em></a>
    <nav class="rail-links">
      <a href="../index.html#products">Products</a>
      <a href="../index.html#subsystems" class="on">Subsystems</a>
      <a href="../doctrine/new-arsenal.html">Doctrine</a>
      <a href="../about/history.html">History</a>
    </nav>
  </div>
</div>

<div class="shell">
<div class="layout">

<aside class="aside">
  <h4>This page</h4>
  <ul>
    <li><a href="#problem">Physical envelope</a></li>
    <li><a href="#why">Limits of linear control</a></li>
    <li><a href="#backbone">Physics backbone</a></li>
    <li><a href="#architecture">Direct-actuator policy</a></li>
    <li><a href="#generalisation">Fleet generalisation</a></li>
    <li><a href="#usedby">Used by</a></li>
  </ul>
  <h4>Subsystems</h4>
  <ul>
    <li><a href="near-envelope-control.html" class="here">Robust control for fast platforms</a></li>
    <li><a href="gnss-denied-navigation.html">High-speed GNSS-denied nav</a></li>
    <li><a href="onboard-compute.html">Edge compute &amp; inference</a></li>
    <li><a href="flight-software.html">Flight software stack</a></li>
    <li><a href="seekers.html">Seekers &amp; terminal guidance</a></li>
    <li><a href="propulsion.html">Propulsion</a></li>
    <li><a href="airframe-structures.html">Airframe &amp; structures</a></li>
    <li><a href="launch-systems.html">Launch &amp; ground systems</a></li>
  </ul>
  <h4>Products</h4>
  <ul>
    <li><a href="../products/hacm-350.html">HACM-350</a></li>
    <li><a href="../products/nightshade-adx1.html">Nightshade ADX-1</a></li>
    <li><a href="../products/usv-strike.html">Kamikaze USV</a></li>
    <li><a href="../products/ahuti.html">Ahuti Interceptor</a></li>
    <li><a href="../products/mobile-drone-lab.html">Mobile Drone Lab</a></li>
    <li><a href="../products/cortex.html">Apollyon Cortex</a></li>
    <li><a href="../products/mdcc.html">MDCC</a></li>
  </ul>
  <h4>Doctrine</h4>
  <ul>
    <li><a href="../doctrine/new-arsenal.html">The New Arsenal</a></li>
    <li><a href="../doctrine/precision-is-mercy.html">Precision is Mercy</a></li>
    <li><a href="../doctrine/missing-middle.html">The missing middle</a></li>
  </ul>
</aside>

<main class="main">

<div class="crumb"><a href="../index.html">Wiki</a><span>/</span><a href="../index.html#subsystems">Subsystems</a><span>/</span>Guidance &amp; control / Robust Control</div>
<header class="masthead">
  <div class="mast-meta">Guidance &amp; control · high-rate direct-actuator policy and sim-to-real physics backbone <span>· core subsystem</span></div>
  <h1>Robust Control for <span class="sub">Fast Air Platforms</span></h1>
  <p class="standfirst">High-rate closed-loop flight control and physics-grounded modeling engineered for extreme dynamic pressures, high-G transitions, and actuator saturation. Integrates our physics backbone and simulation-to-real workflow to guarantee aerodynamic stability where standard linear models fail.</p>
</header>

<section id="problem">
  <div class="sec-tag">01 · Physical envelope</div>
  <h2>Flying where nominal aerodynamic assumptions collapse</h2>
  <p>Standard autopilots are tuned for benign flight regimes: low-speed cruise, gentle hover, and mild turns where aerodynamic forces are linear, control axes are decoupled, and actuators operate with comfortable margin. At speeds exceeding 300 to 650 km/h, during 7G terminal maneuvers, and in the trans-subsonic envelope, every nominal assumption breaks down simultaneously.</p>

  <div class="tw">
    <table>
      <caption>Aerodynamic and actuator behavior at the limit</caption>
      <thead><tr><th>Parameter</th><th>Nominal autopilot model</th><th>Observed high-speed reality</th></tr></thead>
      <tbody>
        <tr><td><strong>Dynamic pressure (q)</strong></td><td>Assumed constant or slow-varying</td><td>Quadratically spikes by orders of magnitude, dramatically amplifying control surface effectiveness and aerodynamic loads.</td></tr>
        <tr><td><strong>Thrust &amp; torque</strong></td><td>Linear relationship with RPM / throttle</td><td>Severe rotor slip, blade stall, and compressor backpressure non-linearities at high Mach/airspeeds.</td></tr>
        <tr><td><strong>Cross-axis coupling</strong></td><td>Roll, pitch, and yaw are independent</td><td>Aerodynamic downwash and high angular rates produce strong, non-separable gyroscopic and aerodynamic cross-coupling.</td></tr>
        <tr><td><strong>Actuator authority</strong></td><td>Proportional reserve margin available</td><td>Control surfaces and propulsion sit on 100% saturation rails; no margin remains for classical error rejection.</td></tr>
        <tr><td><strong>Structural dynamics</strong></td><td>Rigid airframe assumption</td><td>High aeroelastic flex and airframe vibration inject high-frequency noise into inertial rate gyros.</td></tr>
        <tr><td><strong>Sensor integrity</strong></td><td>Unbiased linear accelerometer signals</td><td>Multi-axis sustained high-G loads combined with airframe resonance risk sensor clipping and filter divergence.</td></tr>
      </tbody>
    </table>
  </div>

  <figure>
    <img src="../assets/slides/near-envelope-1.jpg" alt="Charts showing what changes at the edge of physical performance">
    <figcaption><b>Fig. 01</b> At low speeds, dynamics are decoupled and linear. Near the envelope boundary, control surfaces saturate and the vehicle enters coupled, non-linear aerodynamics.</figcaption>
  </figure>
</section>

<section id="why">
  <div class="sec-tag">02 · Limits of linear control</div>
  <h2>Why classical cascades and online solvers break down</h2>

  <h3>A · The cascaded PID architecture</h3>
  <p>Standard open-source and commercial autopilots employ cascaded loops: position feeds attitude, attitude feeds angular rate, and angular rate feeds an actuator mixer. Each tier operates under the implicit assumption that the subsequent tier possesses sufficient actuation bandwidth and torque to fulfill its demand. When a high-speed interceptor or cruise missile executes a violent terminal dive at maximum dynamic pressure, control surfaces reach mechanical deflection limits. Under saturation, the cascaded integrator winds up, forcing the mixer to arbitrarily sacrifice control on one axis to preserve another—often culminating in catastrophic departure from controlled flight.</p>

  <h3>B · Advanced model-predictive control (MPC)</h3>
  <p>Online numerical optimization (MPC) represents a theoretical improvement by explicitly incorporating state and actuator constraints. However, online solvers require closed-form aerodynamic equations and consistent convergence times. Under aggressive transonic maneuvers and turbulent atmospheric shear, online optimization suffers from severe computational latency jitter, demanding excessive power-hungry compute that cannot reliably meet hard real-time deadlines.</p>

  <figure>
    <img src="../assets/slides/near-envelope-2.jpg" alt="Comparison of cascaded PID, model-based MPC, and direct-actuator learned control">
    <figcaption><b>Fig. 02</b> Comparison of control architectures. Cascaded loops diverge under saturation; direct-actuator neural policies evaluate deterministically in sub-millisecond cycles.</figcaption>
  </figure>
</section>

<section id="backbone">
  <div class="sec-tag">03 · Physics backbone &amp; sim-to-real</div>
  <h2>The physics-grounded simulation backbone</h2>
  <p class="lede">A control policy is only ever as dependable as the fidelity of the physical environment in which it was formed. Rather than relying on generic synthetic simulators, Apollyon builds an uncompromising, flight-validated physics foundation.</p>

  <p>The core methodology enforces rigorous calibration: every flight sortie is instrumented densely with high-rate black-box logging. Following recovery, the exact real-world command sequences are replayed through the simulator. Any divergence between the physical flight telemetry and simulated prediction is treated not as statistical noise, but as an unmodeled physical phenomenon that must be identified and explicitly incorporated into the aerodynamic and mechanical core.</p>

  <div class="tw">
    <table>
      <caption>Physical phenomena captured in the simulation core</caption>
      <thead><tr><th>Physical domain</th><th>Specific modeled phenomenon</th><th>Consequence if omitted</th></tr></thead>
      <tbody>
        <tr><td><strong>Aerodynamics</strong></td><td>Boundary layer separation, shock-induced flow detachment, and non-linear downwash interactions between tandem lifting surfaces.</td><td>Unpredictable stall during high-angle-of-attack evasive pull-outs.</td></tr>
        <tr><td><strong>Propulsion &amp; thermal</strong></td><td>Transient motor coil heating, ESC thermal throttling, back-EMF saturation, and battery cell internal resistance voltage drop under peak current.</td><td>Unmodeled thrust decay leading to altitude drop during sustained high-G terminal dives.</td></tr>
        <tr><td><strong>Aeroelastics</strong></td><td>Fuselage flex, fin flutter, and structural harmonic vibration transmission into the IMU mounting plate.</td><td>High-frequency control surface oscillation and servo motor overheating.</td></tr>
        <tr><td><strong>Actuation physics</strong></td><td>Servo gearbox backlash, rate limits under dynamic air loads, and deadband non-linearities.</td><td>Phase lag and pilot-induced-oscillation (PIO) during transonic transit.</td></tr>
      </tbody>
    </table>
  </div>

  <div class="note key">
    <div class="t">One backbone, modular airframe packages</div>
    <p>Apollyon maintains a single unified physics backbone. Each airframe—the Ahuti interceptor, the Nightshade jet munition, the HACM-350 cruise missile, or the Kamikaze USV—exists as a parameterized aerodynamic package residing on the identical simulation substrate. When a flight-test campaign improves our high-rate aerodynamic damping model, that fidelity immediately propagates to every program across the company.</p>
  </div>

  <figure>
    <img src="../assets/slides/apollyon-eng-2.jpg" alt="Flight data comparison against simulator prediction">
    <figcaption><b>Fig. 03</b> Telemetry replayed through the simulation backbone. Observed mismatches drive iterative refinement of physical terms, creating a hardened sim-to-real loop.</figcaption>
  </figure>
</section>

<section id="architecture">
  <div class="sec-tag">04 · Direct-actuator policy</div>
  <h2>High-rate closed-loop neural execution</h2>
  <p>The deployed flight policy evaluates at approximately <strong>500 Hz</strong> directly within the onboard compute core. The system bypasses intermediate PID stages entirely, mapping current aircraft state, measured dynamics, and target path coordinates straight to individual actuator commands.</p>

  <div class="cards">
    <div class="card">
      <div class="kicker">Execution module 01</div>
      <h3>Direct-actuator neural policy</h3>
      <p>Computes direct surface deflections and motor throttle targets at 500 Hz. Because the policy was conditioned on non-linear aerodynamics and full actuator saturation inside the simulation backbone, it operates naturally at the mechanical limits of the vehicle without integrator windup.</p>
      <div class="foot"><span>~500 Hz</span><span>Direct to actuators</span></div>
    </div>
    <div class="card">
      <div class="kicker">Execution module 02</div>
      <h3>High-rate adaptive state representation</h3>
      <p>A fast online diagnostic representation continually analyzes recent flight history to infer changing flight conditions—including crosswinds, air density variations, asymmetric battle damage, or structural payload shifts—supplying instant contextual conditioning to the primary policy.</p>
      <div class="foot"><span>Real-time</span><span>Contextual adaptation</span></div>
    </div>
  </div>

  <p>The resulting controller demonstrates exceptional robustness against unmodeled turbulence, sudden control surface clipping, and extreme dynamic pressure shifts, maintaining razor-sharp trajectory adherence throughout the entire terminal engagement.</p>
</section>

<section id="generalisation">
  <div class="sec-tag">05 · Fleet generalisation</div>
  <h2>Cross-platform deployment &amp; compounding velocity</h2>
  <p>While the specific policy weights are optimized for each individual vehicle geometry, the identification methodology, the high-fidelity physics core, and the simulation-to-real pipeline are completely shared. When developing a new platform, engineering teams do not write new flight control logic from scratch; they execute a parameterized training campaign within the proven pipeline.</p>

  <div class="tw">
    <table>
      <caption>Cross-platform control deployment</caption>
      <thead><tr><th>Platform</th><th>Speed regime</th><th>Primary control challenge</th><th>Execution rate</th></tr></thead>
      <tbody>
        <tr><td><a href="../products/ahuti.html">Ahuti Interceptor</a></td><td>337+ km/h</td><td>Tail-sitter vertical launch transition and high-speed terminal collision homing.</td><td>500 Hz direct actuator</td></tr>
        <tr><td><a href="../products/nightshade-adx1.html">Nightshade ADX-1</a></td><td>650+ km/h</td><td>Turbojet loiter-to-dash transition and steep 380+ km/h terminal dive guidance.</td><td>400 Hz elevon / throttle</td></tr>
        <tr><td><a href="../products/hacm-350.html">HACM-350</a></td><td>Mach 0.7–0.8</td><td>Trans-subsonic high dynamic pressure sea-skimming and 80° terminal dive onto fortified targets.</td><td>500 Hz fin actuation</td></tr>
        <tr><td><a href="../products/usv-strike.html">Kamikaze USV</a></td><td>48+ knots</td><td>Rough sea-state hydrodynamic stability, wave-slamming mitigation, and dynamic waterjet trim.</td><td>100 Hz hydraulic trim</td></tr>
      </tbody>
    </table>
  </div>

  <figure>
    <img src="../assets/slides/near-envelope-3.jpg" alt="Data flywheel from instrumented flight to validated control policy">
    <figcaption><b>Fig. 04</b> The hardware data flywheel: dense instrumented flight data reinforces the physics core, accelerating development for subsequent airframe programs.</figcaption>
  </figure>
</section>

<section id="usedby">
  <div class="sec-tag">06 · Used by</div>
  <h2>Platforms carrying this subsystem</h2>
  <div class="xref">
    <div class="t">Integrated into</div>
    <div class="items">
      <a href="../products/ahuti.html">Ahuti Interceptor — primary consumer, high-speed interception</a>
      <a href="../products/nightshade-adx1.html">Nightshade ADX-1 — terminal dive and loiter stability</a>
      <a href="../products/hacm-350.html">HACM-350 — high-subsonic Mach 0.8 cruise and terminal dive</a>
      <a href="../products/usv-strike.html">Kamikaze USV — sea-state hydrodynamic surface control</a>
      <a href="../products/mobile-drone-lab.html">Mobile Drone Lab — pre-flight HIL rate-table validation</a>
    </div>
  </div>
  <p>Depends on: <a href="onboard-compute.html">Edge Compute &amp; Custom Inference Engine</a>, <a href="flight-software.html">Flight Software Stack</a>.</p>
</section>

<footer>
  <div>Robust Control for Fast Air Platforms · Subsystem · Rev 2.0</div>
  <div><a href="../index.html">Wiki root</a> · <a href="../index.html#matrix">Commonality matrix</a> · apollyondynamics.com</div>
</footer>

</main>
</div>
</div>
</body>
</html>
"""

with open('/home/soham-kumar/soham/apollyon/deck/wiki/subsystems/near-envelope-control.html', 'w') as f:
    f.write(control_html)

print("Robust Control page written successfully.")

# 4. wiki/subsystems/gnss-denied-navigation.html
nav_html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>High-Speed GNSS-Denied Navigation — Apollyon Dynamics Wiki</title>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,wght@0,400;0,500;1,400&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../css/wiki.css">
</head>
<body>

<div class="rail">
  <div class="rail-inner">
    <a class="rail-brand" href="../index.html"><span class="glyph"></span>Apollyon Dynamics <em>· Engineering Wiki</em></a>
    <nav class="rail-links">
      <a href="../index.html#products">Products</a>
      <a href="../index.html#subsystems" class="on">Subsystems</a>
      <a href="../doctrine/new-arsenal.html">Doctrine</a>
      <a href="../about/history.html">History</a>
    </nav>
  </div>
</div>

<div class="shell">
<div class="layout">

<aside class="aside">
  <h4>This page</h4>
  <ul>
    <li><a href="#mach-regime">Mach 0.8 regime</a></li>
    <li><a href="#crpa">Anti-jam CRPA nulling</a></li>
    <li><a href="#dsmac">AI-DSMAC scene match</a></li>
    <li><a href="#fusion">Kalman sensor fusion</a></li>
    <li><a href="#platforms">Platform configs</a></li>
    <li><a href="#usedby">Used by</a></li>
  </ul>
  <h4>Subsystems</h4>
  <ul>
    <li><a href="near-envelope-control.html">Robust control for fast platforms</a></li>
    <li><a href="gnss-denied-navigation.html" class="here">High-speed GNSS-denied nav</a></li>
    <li><a href="onboard-compute.html">Edge compute &amp; inference</a></li>
    <li><a href="flight-software.html">Flight software stack</a></li>
    <li><a href="seekers.html">Seekers &amp; terminal guidance</a></li>
    <li><a href="propulsion.html">Propulsion</a></li>
    <li><a href="airframe-structures.html">Airframe &amp; structures</a></li>
    <li><a href="launch-systems.html">Launch &amp; ground systems</a></li>
  </ul>
  <h4>Products</h4>
  <ul>
    <li><a href="../products/hacm-350.html">HACM-350</a></li>
    <li><a href="../products/nightshade-adx1.html">Nightshade ADX-1</a></li>
    <li><a href="../products/usv-strike.html">Kamikaze USV</a></li>
    <li><a href="../products/ahuti.html">Ahuti Interceptor</a></li>
    <li><a href="../products/mobile-drone-lab.html">Mobile Drone Lab</a></li>
    <li><a href="../products/cortex.html">Apollyon Cortex</a></li>
    <li><a href="../products/mdcc.html">MDCC</a></li>
  </ul>
  <h4>Doctrine</h4>
  <ul>
    <li><a href="../doctrine/new-arsenal.html">The New Arsenal</a></li>
    <li><a href="../doctrine/precision-is-mercy.html">Precision is Mercy</a></li>
    <li><a href="../doctrine/missing-middle.html">The missing middle</a></li>
  </ul>
</aside>

<main class="main">

<div class="crumb"><a href="../index.html">Wiki</a><span>/</span><a href="../index.html#subsystems">Subsystems</a><span>/</span>Navigation / High-Speed GNSS-Denied Nav</div>
<header class="masthead">
  <div class="mast-meta">Navigation · anti-jam CRPA nulling and high-speed AI-DSMAC scene correlation <span>· core subsystem</span></div>
  <h1>High-Speed <span class="sub">GNSS-Denied Navigation</span></h1>
  <p class="standfirst">The satellite signal is the most vulnerable link in modern warfare. Engineered for Mach 0.8 cruise missiles traversing 250+ metres every second—a physics regime entirely beyond 200 km/h commercial drones or slow bomb-droppers—this subsystem integrates multi-element anti-jam CRPA nulling with real-time terrain contour referencing and AI-DSMAC scene correlation.</p>
</header>

<section id="mach-regime">
  <div class="sec-tag">01 · High-speed regime</div>
  <h2>Why Mach 0.8 at 250+ m/s breaks commercial drone navigation</h2>
  <p class="lede">Low-speed commercial drones, ISR quadcopters, and 150–200 km/h bomb-droppers operate in benign kinematic envelopes. At 40–50 m/s, cameras can integrate light over relatively long exposure times, optical flow algorithms have dozens of frames to track gentle feature drift, and latency in a map-matching pipeline is largely inconsequential. In contrast, a standoff strike missile operating at <strong>Mach 0.7–0.8 (240–270 m/s)</strong> fundamentally alters the physics of navigational sensing.</p>

  <div class="tw">
    <table>
      <caption>Kinematic constraints: 200 km/h drone versus Mach 0.8 cruise missile</caption>
      <thead><tr><th>Engineering parameter</th><th>Commercial / ISR drone (55 m/s)</th><th>HACM-350 cruise missile (250+ m/s)</th></tr></thead>
      <tbody>
        <tr><td><strong>Velocity / traverse rate</strong></td><td>~55 m/s (~200 km/h)</td><td><strong>250–270 m/s (Mach 0.8)</strong></td></tr>
        <tr><td><strong>Latency sensitivity</strong></td><td>100 ms compute latency = 5.5 m drift</td><td><strong>10 ms compute latency = 2.55 m unguided transit</strong></td></tr>
        <tr><td><strong>Ground motion blur</strong></td><td>Standard 1/500s exposure acceptable</td><td>Requires &le;1/4000s global shutter + forward motion compensation</td></tr>
        <tr><td><strong>Terrain swath coverage</strong></td><td>Slow, uniform nadir pass</td><td>High-rate swath: hundreds of square kilometres ingested per hour</td></tr>
        <tr><td><strong>Altitude variations</strong></td><td>Nominal flat-ground AGL clearance</td><td>Himalayan valley contouring: thousands of metres relief in seconds</td></tr>
        <tr><td><strong>Inertial drift rate</strong></td><td>Short 20–45 min sorties; &lt;100 m total drift</td><td>800–1,000 km transit (70+ min); tactical IMU drift exceeds 1.5 km</td></tr>
      </tbody>
    </table>
  </div>

  <p>At 250+ m/s, there is no margin for delayed frame ingestion or non-deterministic compute pauses. If an optical correlator takes 50 milliseconds to evaluate a terrain match, the missile has flown 12.5 metres past the calculated fix point. Apollyon's navigation architecture is engineered from the silicon up to guarantee sub-millisecond tensor processing and deterministic position updates at high subsonic velocities.</p>

  <figure>
    <img src="../assets/slides/gnss-denied-1.jpg" alt="Position error growth over time comparing GPS-guided, unassisted inertial, and terrain-referenced fixes">
    <figcaption><b>Fig. 01</b> Inertial drift compounds quadratically over long transit distances. Periodic terrain correlation fixes continuously collapse the uncertainty corridor back to zero.</figcaption>
  </figure>
</section>

<section id="crpa">
  <div class="sec-tag">02 · Electronic warfare defence</div>
  <h2>7-Element Controlled Reception Pattern Antenna (CRPA)</h2>
  <p>Satellite signals originating from 20,000 km orbital altitudes arrive at the earth's surface with extremely faint power levels (approx. -160 dBW). Ground-based electronic countermeasure complexes deploy vehicle-mounted multi-kilowatt broadband jammers designed to blanket battlefields across hundreds of kilometres.</p>

  <div class="tw">
    <table class="spec">
      <caption>CRPA anti-jam baseline</caption>
      <tbody>
        <tr><td><strong>Array configuration</strong></td><td>7-element conformal circular microstrip array</td></tr>
        <tr><td><strong>Frequency bands</strong></td><td>NavIC L5 / S-band · GPS L1 / L2 · GLONASS L1 / L2 · Galileo E1 / E5</td></tr>
        <tr><td><strong>Spatial null depth</strong></td><td><strong>&gt; 45 dB</strong> attenuation toward ground emitters</td></tr>
        <tr><td><strong>Degrees of freedom</strong></td><td>Up to 6 simultaneous independent jamming emitters suppressed</td></tr>
        <tr><td><strong>Threat envelope</strong></td><td>Counters 200–250 km radius EW complexes (HQ IDS TPCR 2025 #33)</td></tr>
        <tr><td><strong>Spoofing rejection</strong></td><td>Spatial coherence verification: isolates single-point false emitters</td></tr>
      </tbody>
    </table>
  </div>

  <h3>Radio-frequency spatial null steering</h3>
  <p>Rather than relying on passive RF filtering, the digital signal processor performs real-time adaptive beamforming. The processor continuously steers spatial nulls—zones of extreme radio insensitivity exceeding 45 dB—directly toward the elevation and azimuth of hostile ground jammers, while simultaneously preserving synthesized high-gain beams aimed at genuine orbital satellites overhead. Because ground jammers sit at negative or near-zero elevation angles while satellites orbit high in the sky, spatial geometry provides a massive discrimination advantage.</p>

  <div class="note key">
    <div class="t">Spoofing detection through spatial coherence</div>
    <p>A sophisticated adversary attempts subtle clock drift injection or false constellation spoofing. A conventional single-element receiver cannot differentiate forged signals from valid satellite broadcasts. The 7-element array measures the angle-of-arrival of each incoming satellite signal: if all constellation channels arrive from the identical bearing (a ground transmitter truck), the system instantly flags spoofing and rejects the radio fix, seamlessly handing navigation over to passive optical scene correlation.</p>
  </div>
</section>

<section id="dsmac">
  <div class="sec-tag">03 · Passive terrain referencing</div>
  <h2>High-speed AI-DSMAC scene correlation</h2>
  <p class="lede">When jamming saturation exceeds even CRPA nulling capacity, the weapon transitions to completely silent, unjammable passive vision: matching the real-time visual appearance and elevation of the earth against stored pre-mission topological maps.</p>

  <div class="cards">
    <div class="card">
      <div class="kicker">Modality 01</div>
      <h3>TERCOM (Terrain Contour Matching)</h3>
      <p>A high-rate radar or narrow-beam laser altimeter samples ground clearance directly beneath the airframe. The resulting 1D elevation profile trace is correlated against an onboard digital elevation model (DEM), yielding coarse horizontal coordinates independent of daylight or weather.</p>
      <div class="foot"><span>Active / silent options</span><span>Elevation profile</span></div>
    </div>
    <div class="card">
      <div class="kicker">Modality 02</div>
      <h3>AI-DSMAC (Scene Area Correlator)</h3>
      <p>A forward-canted high-speed CMOS camera captures 2D imagery of terrain ahead of the weapon. A neural embedding network extracts structural topological features, matching them against satellite reference maps in under 15 milliseconds.</p>
      <div class="foot"><span>Passive optical</span><span>Sub-metre precision</span></div>
    </div>
  </div>

  <h3>Invariant topological embeddings vs legacy brightness correlation</h3>
  <p>First-generation DSMAC systems relied on raw pixel brightness correlation. They failed consistently when seasons changed, when snow dusted mountain passes, or when the sun cast long afternoon shadows across ridgelines. Apollyon's AI-DSMAC operates entirely in feature space:</p>
  <ul>
    <li><strong>Topological Priors:</strong> Neural networks are trained on multi-temporal satellite imagery, learning to detect permanent geographic structure—ravines, cliff lines, ridgelines, road junctions, riverbeds, and permanent civil infrastructure—while ignoring transient surface noise (snow cover, agricultural variations, cloud shadows).</li>
    <li><strong>Multi-Sensor Cross-Matching:</strong> Daylight satellite imagery stored prior to launch matches reliably against live night-time thermal (LWIR) or forward-looking visible camera feeds during flight.</li>
    <li><strong>Lightweight Storage:</strong> Entire 1,000 km flight corridors across the Himalayas occupy less than 150 MB of encrypted onboard solid-state memory, allowing rapid field loading via the <a href="../products/mobile-drone-lab.html">Mobile Drone Lab</a> in under 90 seconds.</li>
  </ul>

  <figure>
    <img src="../assets/slides/gnss-denied-4.jpg" alt="Learned topological description versus legacy brightness correlation">
    <figcaption><b>Fig. 02</b> Legacy brightness correlation fails under seasonal changes or shadows. Apollyon's learned topological descriptors remain stable across snow, darkness, and oblique viewing angles.</figcaption>
  </figure>
</section>

<section id="fusion">
  <div class="sec-tag">04 · Sensor fusion &amp; corridor</div>
  <h2>Real-time Kalman filtering &amp; information-driven routing</h2>
  <p>The weapon runs a high-rate tightly-coupled Unscented Kalman Filter (UKF) integrating high-frequency tactical IMU accelerometer/gyro rates (~1,000 Hz), barometric altimetry, CRPA satellite fixes, and intermittent optical scene correlations.</p>

  <div class="tw">
    <table>
      <caption>Sensor characteristics in the navigation stack</caption>
      <thead><tr><th>Sensor</th><th>Measurement</th><th>Update rate</th><th>Operational role</th></tr></thead>
      <tbody>
        <tr><td><strong>Tactical IMU</strong></td><td>Body rates &amp; accelerations</td><td>1,000 Hz</td><td>High-rate short-term propagation; smooths between optical fixes.</td></tr>
        <tr><td><strong>CRPA Array</strong></td><td>NavIC / GPS pseudorange</td><td>10–20 Hz</td><td>Primary absolute reference until electronic warfare saturation.</td></tr>
        <tr><td><strong>Altimeter (Laser / Radar)</strong></td><td>Terrain clearance (AGL)</td><td>50 Hz</td><td>Altitude verification and coarse TERCOM elevation tracing.</td></tr>
        <tr><td><strong>AI-DSMAC Camera</strong></td><td>Topological ground imagery</td><td>10–30 Hz</td><td>Absolute horizontal position and yaw heading reset; zero drift.</td></tr>
        <tr><td><strong>Air Data Computer</strong></td><td>Indicated &amp; true airspeed</td><td>50 Hz</td><td>Wind vector estimation and aerodynamic dynamic pressure validation.</td></tr>
      </tbody>
    </table>
  </div>

  <h3>Information-density flight routing</h3>
  <p>Because optical fixes occur against geographic landmarks, route planning is an active navigation discipline. Over featureless expanses—such as large lakes, wide deserts, or smooth plains—inertial drift grows steadily. Mission planners lay waypoints intentionally along mountain ridgelines, highway corridors, or distinct terrain contours. Every time the weapon traverses a prominent landmark, the Kalman error corridor pinches down to under 1.5 metres, guaranteeing surgical accuracy at terminal impact.</p>

  <figure>
    <img src="../assets/slides/gnss-denied-5.jpg" alt="Dynamic error corridor along a planned flight route">
    <figcaption><b>Fig. 03</b> Navigational uncertainty corridor: error expands during featureless stretches and collapses to near-zero whenever the weapon matches a verified geographic checkpoint.</figcaption>
  </figure>
</section>

<section id="platforms">
  <div class="sec-tag">05 · Platform configurations</div>
  <h2>Cross-platform deployment specifications</h2>
  <div class="tw">
    <table>
      <caption>Subsystem implementation by platform</caption>
      <thead><tr><th>Platform</th><th>Speed &amp; flight regime</th><th>Navigation configuration</th><th>Terminal CEP</th></tr></thead>
      <tbody>
        <tr>
          <td><a href="../products/hacm-350.html"><strong>HACM-350</strong></a></td>
          <td>Mach 0.7–0.8 (250+ m/s) · 800–1,000 km</td>
          <td>7-element CRPA (NavIC/GPS) + AI-DSMAC against 30 m DEM; under 150 MB route storage; terminal LWIR silhouette match.</td>
          <td><strong>&lt; 1.5 m</strong></td>
        </tr>
        <tr>
          <td><a href="../products/nightshade-adx1.html"><strong>Nightshade ADX-1</strong></a></td>
          <td>650+ km/h · 300 km (Mk II)</td>
          <td>Multi-constellation anti-jam receiver + continuous optical odometry; autonomous terminal EO/IR homing independent of GNSS.</td>
          <td><strong>&lt; 1.0 m</strong></td>
        </tr>
        <tr>
          <td><a href="../products/usv-strike.html"><strong>Kamikaze USV</strong></a></td>
          <td>48+ knots · 800+ km sea transit</td>
          <td>CRPA satellite receiver + coastline topological DSMAC matching + hydro-inertial dead reckoning.</td>
          <td><strong>&lt; 2.0 m</strong></td>
        </tr>
        <tr>
          <td><a href="../products/ahuti.html"><strong>Ahuti Interceptor</strong></a></td>
          <td>337+ km/h · Short flyout</td>
          <td>High-G tactical IMU coasting with ground-radar uplink correction; autonomous visual seeker terminal lock.</td>
          <td>Direct collision</td>
        </tr>
      </tbody>
    </table>
  </div>
</section>

<section id="usedby">
  <div class="sec-tag">06 · Used by</div>
  <h2>Platforms carrying this subsystem</h2>
  <div class="xref">
    <div class="t">Integrated into</div>
    <div class="items">
      <a href="../products/hacm-350.html">HACM-350 — 7-element CRPA, AI-DSMAC, Mach 0.8 transit</a>
      <a href="../products/nightshade-adx1.html">Nightshade ADX-1 — anti-jam multi-GNSS and optical scene matching</a>
      <a href="../products/usv-strike.html">Kamikaze USV — coastline DSMAC and marine dead reckoning</a>
      <a href="../products/ahuti.html">Ahuti Interceptor — tactical IMU flyout and terminal lock</a>
      <a href="../products/mobile-drone-lab.html">Mobile Drone Lab — pre-flight DEM packet compilation</a>
    </div>
  </div>
  <p>Supported by: <a href="onboard-compute.html">Edge Compute &amp; Custom Inference Engine</a>, <a href="seekers.html">Seekers &amp; Terminal Guidance</a>.</p>
</section>

<footer>
  <div>High-Speed GNSS-Denied Navigation · Subsystem · Rev 2.0</div>
  <div><a href="../index.html">Wiki root</a> · <a href="../index.html#matrix">Commonality matrix</a> · apollyondynamics.com</div>
</footer>

</main>
</div>
</div>
</body>
</html>
"""

with open('/home/soham-kumar/soham/apollyon/deck/wiki/subsystems/gnss-denied-navigation.html', 'w') as f:
    f.write(nav_html)

print("High-Speed GNSS-Denied Navigation page written successfully.")

# 5. wiki/subsystems/onboard-compute.html
compute_html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Edge Compute &amp; Custom Inference Engine — Apollyon Dynamics Wiki</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,wght@0,400;0,500;1,400&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../css/wiki.css">
</head>
<body>

<div class="rail">
  <div class="rail-inner">
    <a class="rail-brand" href="../index.html"><span class="glyph"></span>Apollyon Dynamics <em>· Engineering Wiki</em></a>
    <nav class="rail-links">
      <a href="../index.html#products">Products</a>
      <a href="../index.html#subsystems" class="on">Subsystems</a>
      <a href="../doctrine/new-arsenal.html">Doctrine</a>
      <a href="../about/history.html">History</a>
    </nav>
  </div>
</div>

<div class="shell">
<div class="layout">

<aside class="aside">
  <h4>This page</h4>
  <ul>
    <li><a href="#framing">Latency as distance</a></li>
    <li><a href="#why-custom">Limits of generic runtimes</a></li>
    <li><a href="#engine">Proprietary inference core</a></li>
    <li><a href="#design-rules">Worst-case engineering</a></li>
    <li><a href="#workloads">Fleet workloads</a></li>
    <li><a href="#usedby">Used by</a></li>
  </ul>
  <h4>Subsystems</h4>
  <ul>
    <li><a href="near-envelope-control.html">Robust control for fast platforms</a></li>
    <li><a href="gnss-denied-navigation.html">High-speed GNSS-denied nav</a></li>
    <li><a href="onboard-compute.html" class="here">Edge compute &amp; inference</a></li>
    <li><a href="flight-software.html">Flight software stack</a></li>
    <li><a href="seekers.html">Seekers &amp; terminal guidance</a></li>
    <li><a href="propulsion.html">Propulsion</a></li>
    <li><a href="airframe-structures.html">Airframe &amp; structures</a></li>
    <li><a href="launch-systems.html">Launch &amp; ground systems</a></li>
  </ul>
  <h4>Products</h4>
  <ul>
    <li><a href="../products/hacm-350.html">HACM-350</a></li>
    <li><a href="../products/nightshade-adx1.html">Nightshade ADX-1</a></li>
    <li><a href="../products/usv-strike.html">Kamikaze USV</a></li>
    <li><a href="../products/ahuti.html">Ahuti Interceptor</a></li>
    <li><a href="../products/mobile-drone-lab.html">Mobile Drone Lab</a></li>
    <li><a href="../products/cortex.html">Apollyon Cortex</a></li>
    <li><a href="../products/mdcc.html">MDCC</a></li>
  </ul>
  <h4>Doctrine</h4>
  <ul>
    <li><a href="../doctrine/new-arsenal.html">The New Arsenal</a></li>
    <li><a href="../doctrine/precision-is-mercy.html">Precision is Mercy</a></li>
    <li><a href="../doctrine/missing-middle.html">The missing middle</a></li>
  </ul>
</aside>

<main class="main">

<div class="crumb"><a href="../index.html">Wiki</a><span>/</span><a href="../index.html#subsystems">Subsystems</a><span>/</span>Compute / Edge Compute &amp; Custom Inference</div>
<header class="masthead">
  <div class="mast-meta">Compute · hardware-software co-design &amp; custom inference runtime <span>· core subsystem</span></div>
  <h1>Edge Compute &amp; <span class="sub">Custom Inference Engine</span></h1>
  <p class="standfirst">At 100 to 250 metres per second, latency is not an abstract benchmark—it is a physical distance committed to an outdated decision. This subsystem delivers deterministic sub-millisecond execution through hardware-software co-design, isolated CPU/GPU cores, custom hand-tuned CUDA kernels, and a proprietary custom-built edge inference engine tailored for extreme compute efficiency per watt.</p>
</header>

<section id="framing">
  <div class="sec-tag">01 · Physical framing</div>
  <h2>Translating milliseconds into metres of unguided flight</h2>
  <p class="lede">In high-speed autonomous systems, the only meaningful unit of computation latency is distance. A flight controller or vision processor running on generic software spends its cycle bouncing between user space, kernel context switches, dynamic memory allocations, and framework jitter.</p>

  <div class="stats">
    <div class="stat"><div class="n">1.9 m</div><div class="d">Distance flown per cycle on a conventional stack (100 m/s with jitter)</div></div>
    <div class="stat"><div class="n accent">0.25 m</div><div class="d">Distance flown per cycle on Apollyon's co-designed execution core</div></div>
    <div class="stat"><div class="n">~7.6×</div><div class="d">Reduction in committed distance per control evaluation</div></div>
    <div class="stat"><div class="n">&lt; 1 ms</div><div class="d">Hard deterministic execution ceiling across all operational cycles</div></div>
  </div>

  <p>At Mach 0.8 (250+ m/s), the problem becomes extreme: a 15-millisecond delay represents nearly <strong>4 metres of blind flight</strong>. Everything saved in computation latency becomes physical aerodynamic margin—precious milliseconds spent actuating fins, adjusting thrust, or refining terminal lock rather than waiting for an inference runtime to return a tensor.</p>

  <figure>
    <img src="../assets/slides/apollyon-eng-3.jpg" alt="Control cycle end to end: conventional stack versus Apollyon custom execution core">
    <figcaption><b>Fig. 01</b> Control cycle timing. The red block on the conventional stack represents non-deterministic jitter—the occasional cycle that misses its deadline and commits the vehicle to blind flight.</figcaption>
  </figure>
</section>

<section id="why-custom">
  <div class="sec-tag">02 · The limit of generic runtimes</div>
  <h2>Why off-the-shelf deep learning frameworks fail in flight</h2>
  <p>Standard inference runtimes—including TensorRT, ONNX Runtime, and PyTorch Mobile—were engineered for enterprise servers, cloud clusters, or consumer devices. They prioritize batch throughput, broad operator compatibility, and automated model parsing over hard real-time determinism. In an expendable high-subsonic weapon, these assumptions become critical failure points:</p>

  <div class="tw">
    <table>
      <caption>Generic runtimes versus Apollyon custom inference engine</caption>
      <thead><tr><th>System attribute</th><th>Generic runtime (TensorRT / ONNX)</th><th>Apollyon custom inference engine</th></tr></thead>
      <tbody>
        <tr><td><strong>Memory management</strong></td><td>Dynamic heap allocation (<code>malloc</code>/<code>free</code>); risks heap fragmentation and page faults.</td><td><strong>100% static allocation</strong>; all tensor buffers pre-allocated and pinned at boot.</td></tr>
        <tr><td><strong>Kernel launch overhead</strong></td><td>Generic driver queueing; separate launches for activations, normalization, and bias.</td><td><strong>Fused custom CUDA kernels</strong>; single-kernel unrolled execution per neural block.</td></tr>
        <tr><td><strong>Operating system preemption</strong></td><td>Cooperative multithreading subject to OS context switches and thread interrupts.</td><td><strong>Isolated core affinity</strong>; dedicated CPU cores with interrupts completely masked.</td></tr>
        <tr><td><strong>Sensor-to-memory transfer</strong></td><td>Camera/IMU data copies through OS kernel space into host RAM, then to GPU VRAM.</td><td><strong>Zero-copy direct DMA</strong>; sensors write directly into unified GPU address space.</td></tr>
        <tr><td><strong>Latency profile</strong></td><td>Low average latency, but high tail jitter (99.9th percentile exceeds 25 ms).</td><td><strong>Zero tail jitter</strong>; worst-case execution time equals average execution time.</td></tr>
      </tbody>
    </table>
  </div>
</section>

<section id="engine">
  <div class="sec-tag">03 · Architectural mechanism</div>
  <h2>The proprietary Apollyon execution core</h2>
  <p class="lede">Apollyon builds a proprietary, custom-built inference runtime tightly co-designed with our onboard embedded silicon. Three core innovations provide deterministic sub-millisecond execution:</p>

  <div class="cards">
    <div class="card">
      <div class="kicker">Innovation 01</div>
      <h3>Hand-tuned fused CUDA kernels</h3>
      <p>Every neural network architecture in our guidance and navigation stack is compiled into hand-written CUDA and SIMD kernels. Operations such as LayerNorm, SiLU activation, matrix-vector multiplication, and sensor feature unpacking are merged into single monolithic kernel launches. Intermediate activations never leave fast GPU register and shared memory, eliminating high-latency VRAM round-trips.</p>
      <div class="foot"><span>Zero intermediate VRAM</span><span>Fused execution</span></div>
    </div>
    <div class="card">
      <div class="kicker">Innovation 02</div>
      <h3>Strict real-time core isolation</h3>
      <p>The compute module partitions physical silicon. Flight-critical guidance and direct-actuator neural loops run on dedicated, isolated CPU cores configured with Linux PREEMPT_RT. Non-critical tasks (telemetry compression, health monitoring) run on separate cores. Interrupts are redirected, ensuring the control thread is never preempted.</p>
      <div class="foot"><span>Isolated cores</span><span>No preemption</span></div>
    </div>
    <div class="card">
      <div class="kicker">Innovation 03</div>
      <h3>Zero-copy direct-to-GPU DMA</h3>
      <p>High-rate sensors—including high-speed CMOS global-shutter cameras, tactical IMUs, and radar altimeters—stream data directly into pinned unified GPU memory via PCIe Direct Memory Access (DMA). The standard triple-copy penalty across Linux kernel buffers is eliminated entirely.</p>
      <div class="foot"><span>Sensor direct to GPU</span><span>Zero-copy bus</span></div>
    </div>
  </div>

  <div class="note key">
    <div class="t">Thermal and power efficiency at the edge</div>
    <p>Expendable weapons and high-speed interceptors operate inside sealed composite airframes without heavy fans or liquid radiators. By eliminating redundant memory copies and optimizing kernel instruction pipelines, our custom engine reduces compute power consumption by over 40% compared to generic frameworks, keeping silicon junction temperatures well within operating limits during sustained high-speed sorties.</p>
  </div>
</section>

<section id="design-rules">
  <div class="sec-tag">04 · Engineering discipline</div>
  <h2>Design against the worst case, not the average</h2>
  <p>In aerospace software, average latency is a vanity metric. An inference stack that averages 2 milliseconds but suffers an 18-millisecond tail spike once every five hundred cycles is a system that will experience catastrophic failure during the exact high-G evasive maneuver or terminal intercept where compute load peaks.</p>
  <p>Every kernel, DMA pipeline, and memory access in Apollyon's compute core is profiled against its theoretical worst-case execution time (WCET). Bus latency is monitored in real time during flight tests, and any detected latency spike is treated as a flight-critical defect requiring kernel optimization.</p>
</section>

<section id="workloads">
  <div class="sec-tag">05 · Fleet workloads</div>
  <h2>What runs on the edge inference engine</h2>
  <div class="tw">
    <table>
      <caption>Onboard workloads across the fleet</caption>
      <thead><tr><th>Platform</th><th>Workload pipeline</th><th>Execution rate</th><th>Compute constraint</th></tr></thead>
      <tbody>
        <tr>
          <td><a href="../products/ahuti.html"><strong>Ahuti Interceptor</strong></a></td>
          <td>Direct-actuator flight control policy, adaptive world model, terminal optical target tracking.</td>
          <td>~500 Hz control / 60 Hz vision</td>
          <td>Extreme low-latency loop (<1 ms); zero preemption tolerated.</td>
        </tr>
        <tr>
          <td><a href="../products/nightshade-adx1.html"><strong>Nightshade ADX-1</strong></a></td>
          <td>Multi-spectral EO/IR object detection, visual odometry, autonomous terminal dive homing.</td>
          <td>400 Hz control / 30 Hz AI-vision</td>
          <td>Passive conduction cooling inside sealed carbon-fiber fuselage.</td>
        </tr>
        <tr>
          <td><a href="../products/hacm-350.html"><strong>HACM-350</strong></a></td>
          <td>High-speed AI-DSMAC terrain scene matching, optical horizon reference, terminal LWIR silhouette correlation.</td>
          <td>500 Hz fin control / 20 Hz DSMAC</td>
          <td>Mach 0.8 shock-resistant embedded compute module; 150 MB DEM cache.</td>
        </tr>
        <tr>
          <td><a href="../products/usv-strike.html"><strong>Kamikaze USV</strong></a></td>
          <td>Hydrodynamic active trim regulation, shoreline DSMAC correlation, optical waterline tracking, peer mesh.</td>
          <td>100 Hz trim / 30 Hz waterline AI</td>
          <td>Salt-mist sealed enclosure, high shock-load dampening.</td>
        </tr>
        <tr>
          <td><a href="../products/cortex.html"><strong>Apollyon Cortex / MDCC</strong></a></td>
          <td>Multi-stream battlefield sensor fusion, automated target recognition (ATR), edge tactical tracking.</td>
          <td>Multi-stream 30–60 fps</td>
          <td>Dual GPU cluster; 100% local processing at the tactical edge.</td>
        </tr>
      </tbody>
    </table>
  </div>
</section>

<section id="usedby">
  <div class="sec-tag">06 · Used by</div>
  <h2>Platforms carrying this subsystem</h2>
  <div class="xref">
    <div class="t">Integrated into</div>
    <div class="items">
      <a href="../products/ahuti.html">Ahuti Interceptor — primary consumer, sub-millisecond control loop</a>
      <a href="../products/nightshade-adx1.html">Nightshade ADX-1 — EO/IR terminal homing and flight control</a>
      <a href="../products/hacm-350.html">HACM-350 — AI-DSMAC edge terrain correlator</a>
      <a href="../products/usv-strike.html">Kamikaze USV — waterline tracking and waterjet vectoring</a>
      <a href="../products/mobile-drone-lab.html">Mobile Drone Lab — forward mission compilation server</a>
      <a href="../products/cortex.html">Apollyon Cortex / MDCC — distributed tactical intelligence nodes</a>
    </div>
  </div>
  <p>Enables: <a href="near-envelope-control.html">Robust Control for Fast Platforms</a>, <a href="gnss-denied-navigation.html">High-Speed GNSS-Denied Navigation</a>.</p>
</section>

<footer>
  <div>Edge Compute &amp; Custom Inference Engine · Subsystem · Rev 2.0</div>
  <div><a href="../index.html">Wiki root</a> · <a href="../index.html#matrix">Commonality matrix</a> · apollyondynamics.com</div>
</footer>

</main>
</div>
</div>
</body>
</html>
"""

with open('/home/soham-kumar/soham/apollyon/deck/wiki/subsystems/onboard-compute.html', 'w') as f:
    f.write(compute_html)

print("Edge Compute & Custom Inference Engine page written successfully.")

# 6. wiki/subsystems/flight-software.html
fsw_html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Flight Software Stack — Apollyon Dynamics Wiki</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,wght@0,400;0,500;1,400&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../css/wiki.css">
</head>
<body>

<div class="rail">
  <div class="rail-inner">
    <a class="rail-brand" href="../index.html"><span class="glyph"></span>Apollyon Dynamics <em>· Engineering Wiki</em></a>
    <nav class="rail-links">
      <a href="../index.html#products">Products</a>
      <a href="../index.html#subsystems" class="on">Subsystems</a>
      <a href="../doctrine/new-arsenal.html">Doctrine</a>
      <a href="../about/history.html">History</a>
    </nav>
  </div>
</div>

<div class="shell">
<div class="layout">

<aside class="aside">
  <h4>This page</h4>
  <ul>
    <li><a href="#heritage">Open-source heritage</a></li>
    <li><a href="#limits">Why open stacks fail</a></li>
    <li><a href="#core">Re-engineered core</a></li>
    <li><a href="#hil">HIL verification harness</a></li>
    <li><a href="#ownership">Owned layers</a></li>
    <li><a href="#usedby">Used by</a></li>
  </ul>
  <h4>Subsystems</h4>
  <ul>
    <li><a href="near-envelope-control.html">Robust control for fast platforms</a></li>
    <li><a href="gnss-denied-navigation.html">High-speed GNSS-denied nav</a></li>
    <li><a href="onboard-compute.html">Edge compute &amp; inference</a></li>
    <li><a href="flight-software.html" class="here">Flight software stack</a></li>
    <li><a href="seekers.html">Seekers &amp; terminal guidance</a></li>
    <li><a href="propulsion.html">Propulsion</a></li>
    <li><a href="airframe-structures.html">Airframe &amp; structures</a></li>
    <li><a href="launch-systems.html">Launch &amp; ground systems</a></li>
  </ul>
  <h4>Products</h4>
  <ul>
    <li><a href="../products/hacm-350.html">HACM-350</a></li>
    <li><a href="../products/nightshade-adx1.html">Nightshade ADX-1</a></li>
    <li><a href="../products/usv-strike.html">Kamikaze USV</a></li>
    <li><a href="../products/ahuti.html">Ahuti Interceptor</a></li>
    <li><a href="../products/mobile-drone-lab.html">Mobile Drone Lab</a></li>
    <li><a href="../products/cortex.html">Apollyon Cortex</a></li>
    <li><a href="../products/mdcc.html">MDCC</a></li>
  </ul>
  <h4>Doctrine</h4>
  <ul>
    <li><a href="../doctrine/new-arsenal.html">The New Arsenal</a></li>
    <li><a href="../doctrine/precision-is-mercy.html">Precision is Mercy</a></li>
    <li><a href="../doctrine/missing-middle.html">The missing middle</a></li>
  </ul>
</aside>

<main class="main">

<div class="crumb"><a href="../index.html">Wiki</a><span>/</span><a href="../index.html#subsystems">Subsystems</a><span>/</span>Software / Flight Software Stack</div>
<header class="masthead">
  <div class="mast-meta">Software · real-time execution core, high-rate logging &amp; HIL harness <span>· core subsystem</span></div>
  <h1>Flight Software <span class="sub">Stack</span></h1>
  <p class="standfirst">Built upon nearly two decades of global open-source autopilot maturity (PX4, ArduPilot), re-engineered for natively autonomous, high-subsonic strike weapons requiring direct-actuator neural control, microsecond deterministic scheduling, and extreme flight envelopes.</p>
</header>

<section id="heritage">
  <div class="sec-tag">01 · Foundation</div>
  <h2>Honouring two decades of open-source flight maturity</h2>
  <p class="lede">The global open-source autopilot community—anchored by ArduPilot since 2009 and the PX4 Autopilot project since 2011—revolutionized unmanned aviation. Over nearly twenty years of relentless community engineering, these codebases accumulated millions of operational flight hours, establishing the foundational standards of the modern drone industry.</p>

  <p>The achievements of this ecosystem are monumental:</p>
  <ul>
    <li><strong>Universal Device Driver Abstraction:</strong> Robust, battle-tested communication drivers across I2C, SPI, CAN, and UART interfaces for hundreds of commercial sensors and peripheral chips.</li>
    <li><strong>Standardized Telemetry:</strong> The MAVLink protocol, providing a universal lingua franca for command, control, and state broadcasting.</li>
    <li><strong>Advanced State Estimation:</strong> Sophisticated Extended Kalman Filter implementations (EKF2 and EKF3) fusing multiconstellation GNSS, barometers, magnetometers, and optical flow for stable commercial flight.</li>
    <li><strong>Democratization of Flight:</strong> Proving that autonomous robotic flight could be realized on low-cost microcontrollers, spawning entire commercial, agricultural, and academic industries.</li>
  </ul>

  <p>Apollyon Dynamics acknowledges and builds upon this extraordinary heritage. We retain the community's robust low-level hardware communication drivers and bus abstractions. However, when transitioning from commercial utility quadcopters to natively autonomous, high-subsonic strike weapons, the fundamental architectural assumptions of open-source firmware break down completely.</p>
</section>

<section id="limits">
  <div class="sec-tag">02 · Structural limitations</div>
  <h2>Why open firmware cannot be used out-of-the-box for strike weapons</h2>
  <p>Open-source flight stacks were architected around specific operational paradigms that directly conflict with the physics and operational realities of sovereign strike weapons:</p>

  <div class="tw">
    <table>
      <caption>Core architectural divergences</caption>
      <thead><tr><th>Domain</th><th>Open-source firmware assumption (PX4 / ArduPilot)</th><th>Autonomous high-speed strike weapon reality</th></tr></thead>
      <tbody>
        <tr>
          <td><strong>Operator presence</strong></td>
          <td>Assumes an RC transmitter, ground control station, and safety pilot with manual override modes (Manual, Acro, AltHold, Loiter, RTL).</td>
          <td><strong>Natively autonomous:</strong> Zero pilot in the loop, zero manual override, no RC link, and no return-to-launch logic from rail launch to target impact.</td>
        </tr>
        <tr>
          <td><strong>Control architecture</strong></td>
          <td>Decoupled cascaded PID loops (Position &rarr; Attitude &rarr; Angular Rate &rarr; Mixer) assuming linear dynamics at &lt;30 m/s.</td>
          <td><strong>Coupled non-linear dynamics:</strong> At Mach 0.8 (250+ m/s) and high dynamic pressure, cross-coupling and surface reversal require direct-actuator neural control.</td>
        </tr>
        <tr>
          <td><strong>Actuator saturation</strong></td>
          <td>Mixer sacrifices secondary axis authority when motor/servo channels hit 100% saturation rails.</td>
          <td><strong>Hard saturation operation:</strong> Weapon spends substantial terminal dive time on actuator rails; requires direct coupled control allocation.</td>
        </tr>
        <tr>
          <td><strong>Scheduling &amp; determinism</strong></td>
          <td>Cooperative workqueue threads subject to 5–15 ms latency jitter and dynamic OS scheduling overhead.</td>
          <td><strong>Microsecond hard real-time:</strong> 500 Hz direct control policy and high-speed optical correlation demand deterministic sub-millisecond execution.</td>
        </tr>
        <tr>
          <td><strong>High-G dynamics &amp; shock</strong></td>
          <td>EKF tuned for low-vibration commercial airframes; clips or resets under severe shock or sustained 7G turns.</td>
          <td><strong>High-G resilient estimation:</strong> Must maintain uninterrupted state tracking under rocket booster launch and violent evasive maneuvers.</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="note key">
    <div class="t">The fallacy of the "simple" unmanned vehicle</div>
    <p>Removing the human pilot does not simplify the flight software—it vastly increases the demands placed upon it. In an open-source drone, when an estimator drifts or a motor saturates, the software triggers a failsafe or prompts the human operator to take manual stick control. In an expendable cruise missile or high-speed interceptor traveling at hundreds of metres per second, no human intervention is possible. The software must resolve aerodynamic non-linearities autonomously and instantaneously.</p>
  </div>

  <figure>
    <img src="../assets/slides/apollyon-eng-4.jpg" alt="Apollyon flight stack architecture showing kept, rewritten, and added layers">
    <figcaption><b>Fig. 01</b> Architecture of the Apollyon flight software stack. Low-level sensor drivers are retained; the control laws, scheduling core, and state estimator are entirely re-engineered for high-speed autonomy.</figcaption>
  </figure>
</section>

<section id="core">
  <div class="sec-tag">03 · The re-engineered stack</div>
  <h2>What was kept, what was rewritten, and what was added</h2>
  <p class="lede">Apollyon preserves the battle-tested physical device drivers of the open-source community while completely replacing the control and scheduling layers with a hardened sovereign execution core.</p>

  <div class="tw">
    <table>
      <caption>Layer-by-layer architectural breakdown</caption>
      <thead><tr><th>Layer</th><th>Status</th><th>Engineering rationale</th></tr></thead>
      <tbody>
        <tr><td><strong>Sensor device drivers</strong></td><td><span class="pill core">Kept &amp; hardened</span></td><td>Physical bus communication (SPI, I2C, CAN FD) was never the failure point; retained and vetted for memory safety.</td></tr>
        <tr><td><strong>High-G state estimation</strong></td><td><span class="pill dev">Rewritten</span></td><td>Replaced with a tightly coupled UKF engineered to withstand high vibration, booster shock, and multi-axis 7G sustained turns without filter divergence.</td></tr>
        <tr><td><strong>Guidance &amp; control core</strong></td><td><span class="pill dev">Rewritten</span></td><td>Discarded PID cascade; replaced with a 500 Hz direct-actuator neural policy conditioned on our flight-validated <a href="near-envelope-control.html">physics backbone</a>.</td></tr>
        <tr><td><strong>Actuator allocation</strong></td><td><span class="pill dev">Rewritten</span></td><td>Direct multi-axis torque allocation that operates deterministically when elevons, rudders, or thrusters are fully saturated.</td></tr>
        <tr><td><strong>Deterministic scheduler</strong></td><td><span class="pill dev">Rewritten</span></td><td>Hard real-time static schedule with zero dynamic heap allocation and isolated CPU core affinity—see <a href="onboard-compute.html">Edge Compute &amp; Custom Inference Engine</a>.</td></tr>
        <tr><td><strong>Microsecond black-box logging</strong></td><td><span class="pill core">Added</span></td><td>Lossless microsecond-stamped logging capturing raw register states, bus timings, and actuator current for post-sortie simulation mismatch analysis.</td></tr>
        <tr><td><strong>Hardware-in-the-Loop (HIL) harness</strong></td><td><span class="pill core">Added</span></td><td>Integrated digital-analog testing harness executing the exact production flight binary against simulated real-time aerodynamics.</td></tr>
      </tbody>
    </table>
  </div>
</section>

<section id="hil">
  <div class="sec-tag">04 · Verification harness</div>
  <h2>Hardware-in-the-Loop (HIL) testing pipeline</h2>
  <p>Software is never qualified in the air. Every firmware build undergoes thousands of simulated sorties inside our Hardware-in-the-Loop testing harness before a weapon ever reaches the launch rail:</p>
  <ul>
    <li><strong>Identical Production Binaries:</strong> The flight computer running on the HIL bench executes the exact, bit-for-bit compiled binary deployed to the field. No special "simulation flags" or altered timing paths are permitted.</li>
    <li><strong>Full-Flight Sortie Emulation:</strong> The HIL bench injects synthetic high-rate IMU signals, barometric pressure profiles, radar altimeter returns, and optical scene feeds, verifying complete 800 km missions from booster ignition to terminal dive.</li>
    <li><strong>Automated Fault Injection:</strong> The test harness programmatically introduces jammed control surfaces, motor failures, electronic warfare RF interference, and sensor dropouts, ensuring the flight software executes robust fail-operational contingencies.</li>
  </ul>
</section>

<section id="ownership">
  <div class="sec-tag">05 · Ownership thesis</div>
  <h2>Why owning the execution core compounds velocity</h2>
  <p>Most of an airframe can be purchased from tier-1 suppliers, but vehicle performance cannot. Third-party commercial stacks arrive with foreign constraints: conservative safety throttles, non-deterministic latency jitter, and architectures designed around remote pilots.</p>
  <div class="tw">
    <table>
      <caption>Bought limits versus owned layers</caption>
      <thead><tr><th>System layer</th><th>Limit imposed by commercial / off-the-shelf software</th><th>What Apollyon builds &amp; owns</th></tr></thead>
      <tbody>
        <tr><td><strong>Mission autonomy</strong></td><td>Rigid waypoint state machines requiring manual GCS overrides.</td><td>End-to-end sovereign mission logic with autonomous target re-acquisition.</td></tr>
        <tr><td><strong>Flight control</strong></td><td>Conservative PID gains unable to stabilize transonic transitions.</td><td>Direct-actuator neural policies operating up to dynamic physical boundaries.</td></tr>
        <tr><td><strong>Compute runtime</strong></td><td>Generic OS scheduling with unpredictable latency spikes.</td><td>Deterministic sub-millisecond execution with isolated core affinity.</td></tr>
        <tr><td><strong>Test infrastructure</strong></td><td>Manual bench testing relying on post-crash guesswork.</td><td>Lossless microsecond logging feeding our closed-loop physics backbone.</td></tr>
      </tbody>
    </table>
  </div>

  <figure>
    <img src="../assets/slides/apollyon-eng-1.jpg" alt="Layer diagram showing limits that come with purchased components versus Apollyon owned layers">
    <figcaption><b>Fig. 02</b> Depth and speed are not a trade. Owning the performance-critical flight software layer allows Apollyon to iterate new vehicle configurations in days rather than quarters.</figcaption>
  </figure>
</section>

<section id="usedby">
  <div class="sec-tag">06 · Used by</div>
  <h2>Platforms carrying this subsystem</h2>
  <div class="xref">
    <div class="t">Integrated into</div>
    <div class="items">
      <a href="../products/hacm-350.html">HACM-350 — high-subsonic cruise missile guidance core</a>
      <a href="../products/nightshade-adx1.html">Nightshade ADX-1 — jet loitering munition autonomous flight stack</a>
      <a href="../products/ahuti.html">Ahuti Interceptor — direct-actuator high-speed intercept logic</a>
      <a href="../products/usv-strike.html">Kamikaze USV — marine surface strike execution engine</a>
      <a href="../products/mobile-drone-lab.html">Mobile Drone Lab — forward pre-flight HIL diagnostic harness</a>
    </div>
  </div>
  <p>Interfaces with: <a href="near-envelope-control.html">Robust Control for Fast Platforms</a>, <a href="onboard-compute.html">Edge Compute &amp; Custom Inference Engine</a>, <a href="gnss-denied-navigation.html">High-Speed GNSS-Denied Navigation</a>.</p>
</section>

<footer>
  <div>Flight Software Stack · Subsystem · Rev 2.0</div>
  <div><a href="../index.html">Wiki root</a> · <a href="../index.html#matrix">Commonality matrix</a> · apollyondynamics.com</div>
</footer>

</main>
</div>
</div>
</body>
</html>
"""

with open('/home/soham-kumar/soham/apollyon/deck/wiki/subsystems/flight-software.html', 'w') as f:
    f.write(fsw_html)

print("Flight Software Stack page written successfully.")

