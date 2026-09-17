import os
import re

# Read CAD generators
from cad_diagrams import *

# 1. Update products/hacm-350.html to include FIG 02 CAD diagram
with open("/home/soham-kumar/soham/apollyon/deck/wiki/products/hacm-350.html", "r", encoding="utf-8") as f:
    hacm_html = f.read()

# Generate HACM CAD
hacm_cad = """<div class="blueprint-plate">
  <div class="blueprint-head">
    <div class="title">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/></svg>
      FIG. 02 &mdash; HACM-350 Structural Station Lines &amp; Internal Packaging
    </div>
    <span class="scale">Scale: 1:25 &middot; Dimensions in Millimetres</span>
  </div>
  <div class="blueprint-body">
    <svg viewBox="0 0 960 260" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="CAD schematic of HACM-350 cruise missile">
      <defs>
        <pattern id="cad_grid" width="20" height="20" patternUnits="userSpaceOnUse">
          <line x1="0" y1="0" x2="20" y2="0" stroke="rgba(56,189,248,0.06)" stroke-width="1"/>
          <line x1="0" y1="0" x2="0" y2="20" stroke="rgba(56,189,248,0.06)" stroke-width="1"/>
        </pattern>
        <pattern id="hatch_wh" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
          <line x1="0" y1="0" x2="0" y2="6" stroke="#f43f5e" stroke-width="1" opacity="0.4"/>
        </pattern>
        <pattern id="hatch_fuel" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(-45)">
          <line x1="0" y1="0" x2="0" y2="6" stroke="#38bdf8" stroke-width="1" opacity="0.3"/>
        </pattern>
        <pattern id="hatch_booster" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
          <line x1="0" y1="0" x2="0" y2="6" stroke="#94a3b8" stroke-width="1" opacity="0.35"/>
        </pattern>
      </defs>

      <rect width="960" height="260" fill="#0d1117"/>
      <rect width="960" height="260" fill="url(#cad_grid)"/>

      <!-- Centerline Datum -->
      <line x1="30" y1="125" x2="930" y2="125" stroke="#38bdf8" stroke-width="0.8" stroke-dasharray="12,4,2,4" opacity="0.6"/>
      <text x="35" y="120" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="8" opacity="0.7">DATUM &pound;</text>

      <!-- JETTISONABLE SOLID ROCKET BOOSTER (STA 750 to 900) -->
      <rect x="730" y="98" width="160" height="54" fill="url(#hatch_booster)" stroke="#cbd5e1" stroke-width="1.2"/>
      <polygon points="890,92 925,78 925,98 890,108" fill="#1e293b" stroke="#38bdf8" stroke-width="1.2"/>
      <polygon points="890,158 925,172 925,152 890,142" fill="#1e293b" stroke="#38bdf8" stroke-width="1.2"/>
      <path d="M 890 112 L 915 106 L 915 144 L 890 138 Z" fill="#334155" stroke="#94a3b8" stroke-width="1"/>
      <line x1="730" y1="88" x2="730" y2="162" stroke="#f43f5e" stroke-width="1" stroke-dasharray="3,3"/>
      <text x="810" y="129" fill="#e2e8f0" font-family="JetBrains Mono, monospace" font-size="8.5" font-weight="600" text-anchor="middle">SOLID BOOSTER (JETTISONABLE)</text>

      <!-- MAIN AIRFRAME BODY (STA 80 to 730) -->
      <path d="M 80 125 Q 140 98, 200 98 L 730 98 L 730 152 L 200 152 Q 140 152, 80 125 Z" fill="rgba(15,23,42,0.85)" stroke="#f8fafc" stroke-width="1.8"/>

      <!-- COMPARTMENT BULKHEADS -->
      <line x1="200" y1="98" x2="200" y2="152" stroke="#64748b" stroke-width="1.2"/>
      <line x1="330" y1="98" x2="330" y2="152" stroke="#64748b" stroke-width="1.2"/>
      <line x1="490" y1="98" x2="490" y2="152" stroke="#64748b" stroke-width="1.2"/>

      <!-- 1. AVIONICS & CRPA BAY (STA 80 - 200) -->
      <path d="M 88 125 Q 135 104, 185 104 L 185 146 Q 135 146, 88 125 Z" fill="rgba(56,189,248,0.08)" stroke="#38bdf8" stroke-width="0.8"/>
      <rect x="130" y="93" width="45" height="5" fill="#38bdf8" stroke="#f8fafc" stroke-width="0.8"/>
      <circle cx="138" cy="95.5" r="1.5" fill="#0d1117"/>
      <circle cx="148" cy="95.5" r="1.5" fill="#0d1117"/>
      <circle cx="158" cy="95.5" r="1.5" fill="#0d1117"/>
      <circle cx="168" cy="95.5" r="1.5" fill="#0d1117"/>
      <rect x="145" y="152" width="22" height="4" fill="#38bdf8" stroke="#38bdf8"/>
      <text x="140" y="122" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="8" font-weight="700" text-anchor="middle">AVIONICS / CRPA</text>
      <text x="140" y="133" fill="#94a3b8" font-family="JetBrains Mono, monospace" font-size="7" text-anchor="middle">AI-DSMAC Core</text>

      <!-- 2. PENETRATING WARHEAD BAY (STA 200 - 330) -->
      <rect x="205" y="103" width="120" height="44" fill="url(#hatch_wh)" stroke="#f43f5e" stroke-width="1.2"/>
      <text x="265" y="122" fill="#f43f5e" font-family="JetBrains Mono, monospace" font-size="8.5" font-weight="700" text-anchor="middle">WARHEAD 120-150 kg</text>
      <text x="265" y="133" fill="#fda4af" font-family="JetBrains Mono, monospace" font-size="7" text-anchor="middle">Forged Tungsten Penetr.</text>

      <!-- 3. JP-10 FUEL BLADDER (STA 330 - 490) -->
      <rect x="335" y="103" width="150" height="44" fill="url(#hatch_fuel)" stroke="#38bdf8" stroke-width="1"/>
      <text x="410" y="122" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="8.5" font-weight="600" text-anchor="middle">JP-10 FUEL CELL</text>
      <text x="410" y="133" fill="#94a3b8" font-family="JetBrains Mono, monospace" font-size="7" text-anchor="middle">~160 kg &middot; CG Balanced</text>

      <!-- 4. GTRE 350 TURBOJET BAY & S-DUCT (STA 490 - 730) -->
      <path d="M 480 98 Q 515 84, 550 84 L 590 84 Q 565 98, 540 106 L 515 106 Z" fill="#1e293b" stroke="#38bdf8" stroke-width="1"/>
      <rect x="520" y="104" width="195" height="42" fill="#1e293b" stroke="#f8fafc" stroke-width="1.2"/>
      <line x1="535" y1="104" x2="535" y2="146" stroke="#38bdf8" stroke-width="1"/>
      <line x1="550" y1="106" x2="550" y2="144" stroke="#64748b" stroke-width="1"/>
      <line x1="565" y1="108" x2="565" y2="142" stroke="#64748b" stroke-width="1"/>
      <rect x="580" y="109" width="60" height="32" fill="#0f172a" stroke="#f43f5e" stroke-width="0.8" stroke-dasharray="2,2"/>
      <circle cx="610" cy="125" r="6" fill="none" stroke="#f43f5e" stroke-width="0.8"/>
      <line x1="660" y1="106" x2="660" y2="144" stroke="#38bdf8" stroke-width="1.5"/>
      <path d="M 700 110 L 730 114 L 730 136 L 700 140 Z" fill="#334155" stroke="#f8fafc" stroke-width="1"/>
      <text x="620" y="123" fill="#f8fafc" font-family="JetBrains Mono, monospace" font-size="8.5" font-weight="700" text-anchor="middle">GTRE 350 kgf TURBOJET</text>
      <text x="620" y="134" fill="#94a3b8" font-family="JetBrains Mono, monospace" font-size="7" text-anchor="middle">Azad Eng &middot; Single-Shaft</text>

      <!-- FOLDED SCISSOR WINGS (STOWED) -->
      <polygon points="310,98 560,98 550,88 330,88" fill="rgba(56,189,248,0.15)" stroke="#38bdf8" stroke-width="1.2"/>
      <text x="435" y="81" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="7.5" font-weight="600" text-anchor="middle">FOLDED WINGS (Span: 2.6 m deployed)</text>

      <!-- TAIL CONTROL FINS -->
      <polygon points="680,98 722,62 730,62 724,98" fill="#1e293b" stroke="#f8fafc" stroke-width="1.2"/>
      <polygon points="680,152 722,188 730,188 724,152" fill="#1e293b" stroke="#f8fafc" stroke-width="1.2"/>

      <!-- DIMENSION RULES -->
      <line x1="80" y1="210" x2="730" y2="210" stroke="#94a3b8" stroke-width="1"/>
      <line x1="80" y1="204" x2="80" y2="216" stroke="#94a3b8" stroke-width="1"/>
      <line x1="730" y1="204" x2="730" y2="216" stroke="#94a3b8" stroke-width="1"/>
      <text x="405" y="222" fill="#f8fafc" font-family="JetBrains Mono, monospace" font-size="9" text-anchor="middle">Fuselage Length: 4,500 &ndash; 5,000 mm</text>

      <line x1="80" y1="238" x2="925" y2="238" stroke="#38bdf8" stroke-width="1"/>
      <line x1="80" y1="232" x2="80" y2="244" stroke="#38bdf8" stroke-width="1"/>
      <line x1="925" y1="232" x2="925" y2="244" stroke="#38bdf8" stroke-width="1"/>
      <text x="502" y="250" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="9" font-weight="600" text-anchor="middle">Total Launch Configuration with Booster: 5,500 &ndash; 6,000 mm</text>

      <line x1="50" y1="98" x2="50" y2="152" stroke="#94a3b8" stroke-width="1"/>
      <line x1="44" y1="98" x2="56" y2="98" stroke="#94a3b8" stroke-width="1"/>
      <line x1="44" y1="152" x2="56" y2="152" stroke="#94a3b8" stroke-width="1"/>
      <text x="40" y="128" fill="#94a3b8" font-family="JetBrains Mono, monospace" font-size="8" text-anchor="end">&Oslash; 380 mm</text>
    </svg>
  </div>
  <div class="blueprint-cap">
    <b>FIG. 02</b> Internal packaging, station divisions, and dimensional envelope of the HACM-350 sovereign strike missile. Sized around the GTRE 350 kgf engine for high-altitude launch at 4,500 m AMSL.
  </div>
</div>"""

if "FIG. 02 &mdash; HACM-350 Structural Station Lines" not in hacm_html:
    # Insert right before </section> of Section 1 specs
    insertion_target = """  <div class="note">
    <div class="t">Reading the numbers</div>
    <p>Every figure above is set by one of three constraints: the air at 4,500 m, the electronic-warfare environment along the northern frontier, or the requirement that Indian tier-1 industry can build the part at rate. Where a number looks conservative, it is usually buying margin in the first of those.</p>
  </div>
</section>"""

    new_section = """  <div class="note">
    <div class="t">Reading the numbers</div>
    <p>Every figure above is set by one of three constraints: the air at 4,500 m, the electronic-warfare environment along the northern frontier, or the requirement that Indian tier-1 industry can build the part at rate. Where a number looks conservative, it is usually buying margin in the first of those.</p>
  </div>

  """ + hacm_cad + """
</section>"""
    hacm_html = hacm_html.replace(insertion_target, new_section)
    with open("/home/soham-kumar/soham/apollyon/deck/wiki/products/hacm-350.html", "w", encoding="utf-8") as f:
        f.write(hacm_html)
    print("HACM-350 CAD diagram inserted!")

# 2. Update products/ahuti.html to include FIG 02 CAD diagram based on actual photo
with open("/home/soham-kumar/soham/apollyon/deck/wiki/products/ahuti.html", "r", encoding="utf-8") as f:
    ahuti_html = f.read()

ahuti_cad = """<div class="blueprint-plate">
  <div class="blueprint-head">
    <div class="title">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
      FIG. 02 &mdash; Ahuti High-Speed Interceptor UAV &middot; Tail-Sitter Station Diagram
    </div>
    <span class="scale">Scale: 1:10 &middot; Based on Engineering Prototype</span>
  </div>
  <div class="blueprint-body">
    <svg viewBox="0 0 960 300" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="CAD wireframe station diagram of Ahuti interceptor UAV">
      <defs>
        <pattern id="ahuti_grid" width="20" height="20" patternUnits="userSpaceOnUse">
          <line x1="0" y1="0" x2="20" y2="0" stroke="rgba(56,189,248,0.06)" stroke-width="1"/>
          <line x1="0" y1="0" x2="0" y2="20" stroke="rgba(56,189,248,0.06)" stroke-width="1"/>
        </pattern>
        <pattern id="hatch_warhead" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
          <line x1="0" y1="0" x2="0" y2="6" stroke="#f43f5e" stroke-width="1" opacity="0.4"/>
        </pattern>
        <pattern id="hatch_battery" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(-45)">
          <line x1="0" y1="0" x2="0" y2="6" stroke="#38bdf8" stroke-width="1" opacity="0.3"/>
        </pattern>
      </defs>

      <rect width="960" height="300" fill="#0d1117"/>
      <rect width="960" height="300" fill="url(#ahuti_grid)"/>

      <!-- Centerline Datum -->
      <line x1="40" y1="150" x2="920" y2="150" stroke="#38bdf8" stroke-width="0.8" stroke-dasharray="12,4,2,4" opacity="0.6"/>
      <text x="45" y="145" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="8" opacity="0.7">DATUM &pound;</text>

      <!-- 1. CLEAR HEMISPHERICAL SEEKER DOME (Nose STA 080 - 140) -->
      <path d="M 140 105 A 45 45 0 0 0 140 195 Z" fill="rgba(56,189,248,0.12)" stroke="#38bdf8" stroke-width="1.8"/>
      <circle cx="120" cy="150" r="14" fill="#1e293b" stroke="#f8fafc" stroke-width="1.2"/>
      <circle cx="120" cy="150" r="7" fill="#38bdf8"/>
      <line x1="120" y1="136" x2="120" y2="164" stroke="#f8fafc" stroke-width="0.8" stroke-dasharray="2,2"/>
      <line x1="106" y1="150" x2="134" y2="150" stroke="#f8fafc" stroke-width="0.8" stroke-dasharray="2,2"/>

      <!-- 2. MAIN FUSELAGE CONTOUR (Bullet / Torpedo Profile STA 140 to 650) -->
      <path d="M 140 105 Q 260 85, 420 85 L 560 85 Q 610 98, 670 150 Q 610 202, 560 215 L 420 215 Q 260 215, 140 195 Z" 
            fill="rgba(15,23,42,0.9)" stroke="#f8fafc" stroke-width="2"/>

      <!-- COMPARTMENT DIVIDERS -->
      <line x1="250" y1="92" x2="250" y2="208" stroke="#64748b" stroke-width="1" stroke-dasharray="3,3"/>
      <line x1="390" y1="86" x2="390" y2="214" stroke="#64748b" stroke-width="1" stroke-dasharray="3,3"/>
      <line x1="530" y1="87" x2="530" y2="213" stroke="#64748b" stroke-width="1" stroke-dasharray="3,3"/>

      <!-- 3. FORWARD AVIONICS & CORTEX EDGE COMPUTE (STA 140 - 250) -->
      <rect x="155" y="112" width="85" height="76" rx="4" fill="#1e293b" stroke="#38bdf8" stroke-width="1"/>
      <circle cx="175" cy="130" r="4" fill="#38bdf8"/>
      <rect x="190" y="122" width="40" height="16" fill="#0f172a" stroke="#64748b" stroke-width="0.8"/>
      <text x="197" y="160" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="8" font-weight="700" text-anchor="middle">CORTEX COMPUTE</text>
      <text x="197" y="172" fill="#94a3b8" font-family="JetBrains Mono, monospace" font-size="7" text-anchor="middle">200 Hz Optical &bull; IMU</text>

      <!-- 4. DIRECTIONAL FRAGMENTATION WARHEAD BAY (STA 250 - 390) -->
      <rect x="260" y="98" width="120" height="104" rx="3" fill="url(#hatch_warhead)" stroke="#f43f5e" stroke-width="1.2"/>
      <rect x="370" y="88" width="12" height="124" fill="#1e293b" stroke="#f43f5e" stroke-width="1"/>
      <circle cx="376" cy="100" r="2" fill="#f43f5e"/>
      <circle cx="376" cy="150" r="2" fill="#f43f5e"/>
      <circle cx="376" cy="200" r="2" fill="#f43f5e"/>
      <text x="315" y="145" fill="#f43f5e" font-family="JetBrains Mono, monospace" font-size="8.5" font-weight="700" text-anchor="middle">5.5 kg WARHEAD</text>
      <text x="315" y="158" fill="#fda4af" font-family="JetBrains Mono, monospace" font-size="7" text-anchor="middle">Focused Blast-Frag</text>

      <!-- 5. BATTERY & CAPACITOR POWER CORE (STA 390 - 530) -->
      <rect x="400" y="98" width="120" height="104" rx="3" fill="url(#hatch_battery)" stroke="#38bdf8" stroke-width="1"/>
      <text x="460" y="145" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="8.5" font-weight="600" text-anchor="middle">ENERGY CORE</text>
      <text x="460" y="158" fill="#94a3b8" font-family="JetBrains Mono, monospace" font-size="7" text-anchor="middle">High-C Discharge &bull; Boost</text>

      <!-- 6. NACA INLET CUTAWAYS ON BODY -->
      <polygon points="320,86 350,96 350,86" fill="#0d1117" stroke="#38bdf8" stroke-width="0.8"/>
      <polygon points="460,86 490,96 490,86" fill="#0d1117" stroke="#38bdf8" stroke-width="0.8"/>
      <polygon points="320,214 350,204 350,214" fill="#0d1117" stroke="#38bdf8" stroke-width="0.8"/>
      <polygon points="460,214 490,204 490,214" fill="#0d1117" stroke="#38bdf8" stroke-width="0.8"/>

      <!-- 7. SWEPT COMPOSITE TAIL-SITTER FINS & LANDING LEGS -->
      <path d="M 520 86 Q 590 55, 680 35 L 750 35 Q 670 75, 620 115 Z" fill="#1e293b" stroke="#f8fafc" stroke-width="1.5"/>
      <path d="M 520 214 Q 590 245, 680 265 L 750 265 Q 670 225, 620 185 Z" fill="#1e293b" stroke="#f8fafc" stroke-width="1.5"/>
      <path d="M 530 140 Q 600 120, 710 100 L 760 105 Q 660 135, 620 145 Z" fill="rgba(30,41,59,0.7)" stroke="#38bdf8" stroke-width="1"/>
      <path d="M 530 160 Q 600 180, 710 200 L 760 195 Q 660 165, 620 155 Z" fill="rgba(30,41,59,0.7)" stroke="#38bdf8" stroke-width="1"/>

      <!-- 8. MOTOR POD NACELLES AT FIN TIPS -->
      <rect x="730" y="24" width="55" height="22" rx="11" fill="#1e293b" stroke="#38bdf8" stroke-width="1.4"/>
      <polygon points="785,28 805,35 785,42" fill="#38bdf8"/>
      <line x1="800" y1="10" x2="800" y2="60" stroke="#f8fafc" stroke-width="1.5"/>

      <rect x="730" y="254" width="55" height="22" rx="11" fill="#1e293b" stroke="#38bdf8" stroke-width="1.4"/>
      <polygon points="785,258 805,265 785,272" fill="#38bdf8"/>
      <line x1="800" y1="240" x2="800" y2="290" stroke="#f8fafc" stroke-width="1.5"/>

      <rect x="740" y="96" width="45" height="18" rx="9" fill="#1e293b" stroke="#64748b" stroke-width="1"/>
      <rect x="740" y="186" width="45" height="18" rx="9" fill="#1e293b" stroke="#64748b" stroke-width="1"/>

      <!-- Conical Parabolic Tail Stinger -->
      <polygon points="610,135 670,150 610,165" fill="#334155" stroke="#f8fafc" stroke-width="1"/>

      <!-- CALLOUT LABELS & ARROWS -->
      <line x1="120" y1="130" x2="80" y2="70" stroke="#38bdf8" stroke-width="0.8"/>
      <text x="80" y="60" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="8" font-weight="600" text-anchor="end">HEMISPHERICAL DOME</text>
      <text x="80" y="70" fill="#94a3b8" font-family="JetBrains Mono, monospace" font-size="7" text-anchor="end">Day/Night Optical Head</text>

      <line x1="785" y1="35" x2="840" y2="20" stroke="#38bdf8" stroke-width="0.8"/>
      <text x="845" y="20" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="8" font-weight="600">BRUSHLESS MOTOR POD</text>
      <text x="845" y="30" fill="#94a3b8" font-family="JetBrains Mono, monospace" font-size="7">High-RPM &bull; Folding Propfan</text>

      <line x1="680" y1="265" x2="720" y2="285" stroke="#f8fafc" stroke-width="0.8"/>
      <text x="725" y="288" fill="#f8fafc" font-family="JetBrains Mono, monospace" font-size="8" font-weight="600">SWEPT LANDING STRUTS</text>
      <text x="725" y="297" fill="#94a3b8" font-family="JetBrains Mono, monospace" font-size="7">Tail-Sitter Launch/Recovery</text>

      <line x1="95" y1="275" x2="805" y2="275" stroke="#94a3b8" stroke-width="1"/>
      <line x1="95" y1="269" x2="95" y2="281" stroke="#94a3b8" stroke-width="1"/>
      <line x1="805" y1="269" x2="805" y2="281" stroke="#94a3b8" stroke-width="1"/>
      <text x="450" y="290" fill="#f8fafc" font-family="JetBrains Mono, monospace" font-size="8.5" text-anchor="middle">Total Airframe Length: ~950 mm</text>
    </svg>
  </div>
  <div class="blueprint-cap">
    <b>FIG. 03</b> Engineering station layout of the Ahuti interceptor UAV, modeled directly from the flight-test prototype. Illustrates the hemispherical optical seeker dome, forward Cortex compute, directional warhead sleeve, and the 4 swept tail-sitter landing legs with tip-mounted brushless propfan nacelles.
  </div>
</div>"""

if "FIG. 02 &mdash; Ahuti High-Speed Interceptor UAV" not in ahuti_html:
    # Insert right after the figure in Section 4 #aero
    ahuti_target = """  <figure class="dark">
    <img src="../assets/ahuti-front.jpg" alt="Ahuti interceptor front elevation">
    <figcaption><b>Fig. 02</b> Front elevation. The frontal area is the design variable that the entire configuration is arranged around.</figcaption>
  </figure>"""
    ahuti_html = ahuti_html.replace(ahuti_target, ahuti_target + "\n\n  " + ahuti_cad)
    with open("/home/soham-kumar/soham/apollyon/deck/wiki/products/ahuti.html", "w", encoding="utf-8") as f:
        f.write(ahuti_html)
    print("Ahuti CAD diagram inserted!")

# 3. Update products/nightshade-adx1.html to include FIG 02 CAD diagram based on brochures
with open("/home/soham-kumar/soham/apollyon/deck/wiki/products/nightshade-adx1.html", "r", encoding="utf-8") as f:
    ns_html = f.read()

ns_cad = """<div class="blueprint-plate">
  <div class="blueprint-head">
    <div class="title">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 12L2 2l4 10-4 10 20-10z"/></svg>
      FIG. 02 &mdash; Nightshade ADX-1 Jet Loitering Munition &middot; Planform &amp; Internal Cutaway
    </div>
    <span class="scale">Scale: 1:15 &middot; Dimensions in Millimetres</span>
  </div>
  <div class="blueprint-body">
    <svg viewBox="0 0 960 280" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="CAD cutaway schematic of Nightshade ADX-1 jet loitering munition">
      <defs>
        <pattern id="ns_grid" width="20" height="20" patternUnits="userSpaceOnUse">
          <line x1="0" y1="0" x2="20" y2="0" stroke="rgba(56,189,248,0.06)" stroke-width="1"/>
          <line x1="0" y1="0" x2="0" y2="20" stroke="rgba(56,189,248,0.06)" stroke-width="1"/>
        </pattern>
        <pattern id="hatch_ns_fuel" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
          <line x1="0" y1="0" x2="0" y2="6" stroke="#38bdf8" stroke-width="1" opacity="0.3"/>
        </pattern>
        <pattern id="hatch_ns_warhead" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(-45)">
          <line x1="0" y1="0" x2="0" y2="6" stroke="#f43f5e" stroke-width="1" opacity="0.35"/>
        </pattern>
      </defs>

      <rect width="960" height="280" fill="#0d1117"/>
      <rect width="960" height="280" fill="url(#ns_grid)"/>

      <!-- Centerline Datum -->
      <line x1="40" y1="140" x2="920" y2="140" stroke="#38bdf8" stroke-width="0.8" stroke-dasharray="12,4,2,4" opacity="0.6"/>
      <text x="45" y="135" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="8" opacity="0.7">DATUM &pound;</text>

      <!-- BLENDED DELTA WING PLANFORM -->
      <path d="M 80 140 Q 150 120, 240 100 L 640 25 L 720 25 L 720 70 L 660 140 Z" fill="rgba(15,23,42,0.85)" stroke="#f8fafc" stroke-width="1.8"/>
      <path d="M 80 140 Q 150 160, 240 180 L 640 255 L 720 255 L 720 210 L 660 140 Z" fill="rgba(15,23,42,0.85)" stroke="#f8fafc" stroke-width="1.8"/>

      <rect x="695" y="18" width="30" height="8" rx="2" fill="#38bdf8" stroke="#f8fafc" stroke-width="1"/>
      <rect x="695" y="254" width="30" height="8" rx="2" fill="#38bdf8" stroke="#f8fafc" stroke-width="1"/>

      <polygon points="560,50 635,32 635,46 560,62" fill="#1e293b" stroke="#38bdf8" stroke-width="1"/>
      <polygon points="560,230 635,248 635,234 560,218" fill="#1e293b" stroke="#38bdf8" stroke-width="1"/>

      <path d="M 80 140 Q 160 100, 280 100 L 650 100 L 690 120 L 720 128 L 720 152 L 690 160 L 650 180 L 280 180 Q 160 180, 80 140 Z" 
            fill="#0f172a" stroke="#38bdf8" stroke-width="1.5"/>

      <!-- 1. NOSE TONBO TRAP EO/IR GIMBAL (STA 80 - 150) -->
      <path d="M 80 140 Q 110 125, 145 125 L 145 155 Q 110 155, 80 140 Z" fill="#1e293b" stroke="#f8fafc" stroke-width="1.2"/>
      <circle cx="115" cy="140" r="10" fill="#0d1117" stroke="#38bdf8" stroke-width="1.2"/>
      <circle cx="115" cy="140" r="4" fill="#f43f5e"/>
      <text x="115" y="168" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="7.5" font-weight="700" text-anchor="middle">TONBO TRAP</text>
      <text x="115" y="177" fill="#94a3b8" font-family="JetBrains Mono, monospace" font-size="6.5" text-anchor="middle">Dual EO/IR</text>

      <!-- 2. MODULAR WARHEAD BAY (STA 150 - 270) -->
      <rect x="155" y="112" width="110" height="56" rx="2" fill="url(#hatch_ns_warhead)" stroke="#f43f5e" stroke-width="1.2"/>
      <text x="210" y="137" fill="#f43f5e" font-family="JetBrains Mono, monospace" font-size="8" font-weight="700" text-anchor="middle">15 kg WARHEAD</text>
      <text x="210" y="148" fill="#fda4af" font-family="JetBrains Mono, monospace" font-size="7" text-anchor="middle">HEAT / Pre-Frag</text>

      <!-- 3. CONFORMAL FUEL BLADDER (STA 270 - 430) -->
      <rect x="275" y="108" width="150" height="64" rx="3" fill="url(#hatch_ns_fuel)" stroke="#38bdf8" stroke-width="1"/>
      <text x="350" y="137" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="8.5" font-weight="600" text-anchor="middle">JP-8 FUEL TANK</text>
      <text x="350" y="148" fill="#94a3b8" font-family="JetBrains Mono, monospace" font-size="7" text-anchor="middle">Center of Gravity Trim</text>

      <!-- 4. DORSAL NACA AIR INTAKE SCOOP -->
      <polygon points="410,126 460,118 460,162 410,154" fill="#0d1117" stroke="#38bdf8" stroke-width="1.2"/>
      <line x1="435" y1="122" x2="435" y2="158" stroke="#38bdf8" stroke-width="0.8" stroke-dasharray="2,2"/>

      <!-- 5. MICRO-TURBOJET BAY (STA 460 - 680) -->
      <rect x="470" y="116" width="180" height="48" rx="2" fill="#1e293b" stroke="#f8fafc" stroke-width="1.2"/>
      <line x1="485" y1="116" x2="485" y2="164" stroke="#38bdf8" stroke-width="1.2"/>
      <line x1="500" y1="118" x2="500" y2="162" stroke="#64748b" stroke-width="1"/>
      <line x1="515" y1="120" x2="515" y2="160" stroke="#64748b" stroke-width="1"/>
      <rect x="530" y="122" width="60" height="36" fill="#0f172a" stroke="#f43f5e" stroke-width="0.8" stroke-dasharray="2,2"/>
      <line x1="610" y1="118" x2="610" y2="162" stroke="#38bdf8" stroke-width="1.5"/>
      <path d="M 650 122 L 690 128 L 690 152 L 650 158 Z" fill="#334155" stroke="#f8fafc" stroke-width="1"/>
      <text x="560" y="137" fill="#f8fafc" font-family="JetBrains Mono, monospace" font-size="8.5" font-weight="700" text-anchor="middle">MICRO-TURBOJET</text>
      <text x="560" y="148" fill="#94a3b8" font-family="JetBrains Mono, monospace" font-size="7" text-anchor="middle">40-60 kgf &bull; 650+ km/h</text>

      <!-- CATAPULT LAUNCH LUGS -->
      <rect x="330" y="96" width="12" height="4" fill="#f8fafc"/>
      <rect x="520" y="96" width="12" height="4" fill="#f8fafc"/>
      <rect x="330" y="180" width="12" height="4" fill="#f8fafc"/>
      <rect x="520" y="180" width="12" height="4" fill="#f8fafc"/>

      <!-- DIMENSION LABELS -->
      <line x1="80" y1="240" x2="690" y2="240" stroke="#94a3b8" stroke-width="1"/>
      <line x1="80" y1="234" x2="80" y2="246" stroke="#94a3b8" stroke-width="1"/>
      <line x1="690" y1="234" x2="690" y2="246" stroke="#94a3b8" stroke-width="1"/>
      <text x="385" y="254" fill="#f8fafc" font-family="JetBrains Mono, monospace" font-size="8.5" text-anchor="middle">Length: 1,150 mm (Mk I) / Up to 2,200 mm (Mk III)</text>

      <line x1="745" y1="25" x2="745" y2="255" stroke="#38bdf8" stroke-width="1"/>
      <line x1="739" y1="25" x2="751" y2="25" stroke="#38bdf8" stroke-width="1"/>
      <line x1="739" y1="255" x2="751" y2="255" stroke="#38bdf8" stroke-width="1"/>
      <text x="760" y="144" fill="#38bdf8" font-family="JetBrains Mono, monospace" font-size="8.5" font-weight="600" transform="rotate(90 760 144)" text-anchor="middle">Wingspan: 1,250 mm</text>
    </svg>
  </div>
  <div class="blueprint-cap">
    <b>FIG. 02</b> Planform and cutaway architecture of the Nightshade ADX-1 jet loitering munition. Shows the chin Tonbo TRAP sensor gimbal, 15 kg modular warhead, central fuel cell, dorsal flush intake, and micro-turbojet engine bay enabling sustained 650+ km/h dash speeds.
  </div>
</div>"""

if "FIG. 02 &mdash; Nightshade ADX-1 Jet Loitering Munition" not in ns_html:
    ns_target = """  <figure class="dark">
    <img src="../assets/nightshade-mk3.jpg" alt="Nightshade ADX-1 Mk III side profile render">
    <figcaption><b>Fig. 01</b> ADX-1 Mk III. Composite high-strength airframe, low-drag configuration, internal fuel with centre-of-gravity management as fuel burns off.</figcaption>
  </figure>"""
    ns_html = ns_html.replace(ns_target, ns_target + "\n\n  " + ns_cad)
    with open("/home/soham-kumar/soham/apollyon/deck/wiki/products/nightshade-adx1.html", "w", encoding="utf-8") as f:
        f.write(ns_html)
    print("Nightshade CAD diagram inserted!")

