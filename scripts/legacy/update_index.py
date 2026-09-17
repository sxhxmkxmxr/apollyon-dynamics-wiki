import re

with open("/home/soham-kumar/soham/apollyon/deck/wiki/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Remove "· wiki root · rev 1.0 · September 2026"
html = re.sub(
    r'<div class="mast-meta">Apollyon Dynamics <span>.*?</span></div>',
    r'<div class="mast-meta">Apollyon Dynamics</div>',
    html
)

# 2. Remove the specific stats and keep three boxes with "fill with appropriate stats or remove"
old_stats = """  <div class="stats">
    <div class="stat"><div class="n accent">07</div><div class="d">Fielded units across four theatres</div></div>
    <div class="stat"><div class="n">2025</div><div class="d">Founded · first Army order within months</div></div>
    <div class="stat"><div class="n">17+</div><div class="d">Engineering team</div></div>
    <div class="stat"><div class="n">03</div><div class="d">Concurrent product lines</div></div>
  </div>"""

new_stats = """  <div class="stats">
    <div class="stat"><div class="n">&mdash;</div><div class="d">fill with appropriate stats or remove</div></div>
    <div class="stat"><div class="n">&mdash;</div><div class="d">fill with appropriate stats or remove</div></div>
    <div class="stat"><div class="n">&mdash;</div><div class="d">fill with appropriate stats or remove</div></div>
  </div>"""

html = html.replace(old_stats, new_stats)

# Also check if stats exist in another whitespace variant
if "fill with appropriate stats or remove" not in html:
    html = re.sub(
        r'<div class="stats">\s*<div class="stat"><div class="n accent">07</div>.*?</div>\s*</div>',
        new_stats,
        html,
        flags=re.DOTALL
    )

# 3 & 4. Update Section 3 (Engineering Thesis & Compounding Loop, remove Fig 01)
old_thesis_pattern = r'<section id="thesis">.*?</section>'
new_thesis = """<section id="thesis">
  <div class="sec-tag">03 · Engineering thesis</div>
  <h2>Depth and speed are not a trade</h2>
  <p>The central organisational claim is that engineering depth and execution speed can coexist at scale, and that the apparent trade-off between them is an organisational problem to be solved rather than a law to be obeyed. The institution has to accumulate the technical memory of a mature prime while keeping the iteration velocity of a young engineering company.</p>
  <p>Mechanically, that is achieved by owning the layers where performance actually lives. Most of a vehicle can be bought; its performance cannot. Every bought layer arrives with someone else's limit attached &mdash; a supplier's safety throttle on the power system, a flight stack built around an operator, general-purpose compute with non-deterministic jitter in the control path, or somebody else's form factor. Owning the performance-critical layers &mdash; control, runtime, scheduling, and navigation &mdash; is what determines whether an airframe reaches its physical limits or remains throttled by third-party assumptions.</p>
  <div class="note key">
    <div class="t">The compounding loop</div>
    <p>Engineering efforts compound. As an organization, institutional velocity and execution speed increase with accumulated experience and iterative hardware campaigns. The instrumentation, ingest pipelines, and automated test harnesses are built once; thereafter, every campaign costs less and returns more. This foundation enables the firm to maintain speed even as organizational scale expands, delivering systems of substantially higher complexity in compressed timeframes &mdash; establishing an enduring engineering and institutional aim.</p>
  </div>
</section>"""

html = re.sub(old_thesis_pattern, new_thesis, html, flags=re.DOTALL)

# 5. Update Product Classes section (#classes)
old_classes_pattern = r'<section id="classes">.*?</section>'
new_classes = """<section id="classes">
  <div class="sec-tag">04 · Product classes</div>
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
</section>"""

html = re.sub(old_classes_pattern, new_classes, html, flags=re.DOTALL)

# 6. Update Product Register (#products)
old_products_pattern = r'<section id="products">.*?</section>'
new_products = """<section id="products">
  <div class="sec-tag">05 · Product register</div>
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
      <p>A short-range, high-speed interceptor for hostile reconnaissance drones and loitering munitions. Cued by ground radar in midcourse, handed to an onboard day/night seeker in the terminal phase. Carbon-fibre smart-infill airframe, clocked at 337 km/h and climbing. Kinetic and proximity-blast kill options. Tail-sitter vertical launch.</p>
      <div class="foot"><span class="pill dev">Mk-I flying · Mk-II in design</span><span>337 km/h</span></div>
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
      <p>The layer between every sensor a formation already receives and the people who need to act on it. Detect, analyse, assess, flag, escalate — then compose one assessment into the form each authorised user can act on. One operator supervises six to twenty ISR aircraft. 100% local processing, zero external dependency.</p>
      <div class="foot"><span class="pill dev">TRL 4–5 · development</span><span>6–20 aircraft / op</span></div>
    </div>
    <div class="card">
      <div class="kicker">Mobile command platform</div>
      <h3><a href="products/mdcc.html">Mobile Distributed Command Centre</a></h3>
      <p>Cortex as a platform you can drive to the edge of an operation. Compute, storage, networking and the whole intelligence stack on a vehicle, with every stage of processing running locally so the platform depends on nothing outside itself. Five deployment hosts, six primary mission roles.</p>
      <div class="foot"><span class="pill dev">TRL 4–5 · development</span><span>Zero external dep</span></div>
    </div>
  </div>
</section>"""

html = re.sub(old_products_pattern, new_products, html, flags=re.DOTALL)

# 7. Update Subsystems Register (#subsystems)
old_subsystems_pattern = r'<section id="subsystems">.*?</section>'
new_subsystems = """<section id="subsystems">
  <div class="sec-tag">06 · Subsystem register</div>
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
</section>"""

html = re.sub(old_subsystems_pattern, new_subsystems, html, flags=re.DOTALL)

# 8. Update Matrix (#matrix)
old_matrix_pattern = r'<section id="matrix">.*?</section>'
new_matrix = """<section id="matrix">
  <div class="sec-tag">07 · Commonality</div>
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
</section>"""

html = re.sub(old_matrix_pattern, new_matrix, html, flags=re.DOTALL)

# 9. Update Aside Navigation
old_aside_pattern = r'<aside class="aside">.*?</aside>'
new_aside = """<aside class="aside">
  <h4>This page</h4>
  <ul>
    <li><a href="#overview">Overview</a></li>
    <li><a href="#ethos">Ethos</a></li>
    <li><a href="#thesis">Engineering thesis</a></li>
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
</aside>"""

html = re.sub(old_aside_pattern, new_aside, html, flags=re.DOTALL)

with open("/home/soham-kumar/soham/apollyon/deck/wiki/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Updated wiki/index.html successfully!")
