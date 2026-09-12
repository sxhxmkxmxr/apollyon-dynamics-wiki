import re
import os

WIKI_DIR = "/home/soham-kumar/soham/apollyon/deck/wiki"

def update_subsystem_page(filepath, slug):
    with open(filepath, 'r') as f:
        content = f.read()

    subsystems = [
        ("near-envelope-control.html", "near-envelope-control", "Robust control for fast platforms"),
        ("gnss-denied-navigation.html", "gnss-denied-navigation", "High-speed GNSS-denied nav"),
        ("onboard-compute.html", "onboard-compute", "Edge compute &amp; inference"),
        ("flight-software.html", "flight-software", "Flight software stack"),
        ("seekers.html", "seekers", "Seekers &amp; terminal guidance"),
        ("propulsion.html", "propulsion", "Propulsion"),
        ("airframe-structures.html", "airframe-structures", "Airframe &amp; structures"),
        ("launch-systems.html", "launch-systems", "Launch &amp; ground systems"),
    ]
    sub_links = []
    for f_name, s, label in subsystems:
        cls = ' class="here"' if s == slug else ''
        sub_links.append(f'    <li><a href="{f_name}"{cls}>{label}</a></li>')
    subs_html = "  <h4>Subsystems</h4>\n  <ul>\n" + "\n".join(sub_links) + "\n  </ul>"

    prod_html = """  <h4>Products</h4>
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
  </ul>"""

    new_nav_block = f"{subs_html}\n{prod_html}"

    # Replace from <h4>Subsystems</h4> until </aside>
    pattern = re.compile(r'  <h4>Subsystems</h4>.*?  </ul>(\s*<h4>Products</h4>.*?  </ul>)?(\s*<h4>Doctrine</h4>.*?  </ul>)?', re.DOTALL)
    if pattern.search(content):
        new_content = pattern.sub(new_nav_block, content)
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Updated subsystem nav: {filepath}")
    else:
        print(f"Pattern not found in: {filepath}")

for slug, filename in [
    ("seekers", "subsystems/seekers.html"),
    ("propulsion", "subsystems/propulsion.html"),
    ("airframe-structures", "subsystems/airframe-structures.html"),
    ("launch-systems", "subsystems/launch-systems.html"),
]:
    p = os.path.join(WIKI_DIR, filename)
    if os.path.exists(p):
        update_subsystem_page(p, slug)
