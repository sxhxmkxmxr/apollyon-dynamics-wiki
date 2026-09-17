import re
import os

WIKI_DIR = "/home/soham-kumar/soham/apollyon/deck/wiki"

def update_product_page(filepath, slug):
    with open(filepath, 'r') as f:
        content = f.read()

    # Determine "here" class
    products = [
        ("hacm-350.html", "hacm-350", "HACM-350"),
        ("nightshade-adx1.html", "nightshade-adx1", "Nightshade ADX-1"),
        ("usv-strike.html", "usv-strike", "Kamikaze USV"),
        ("ahuti.html", "ahuti", "Ahuti Interceptor"),
        ("mobile-drone-lab.html", "mobile-drone-lab", "Mobile Drone Lab"),
        ("cortex.html", "cortex", "Apollyon Cortex"),
        ("mdcc.html", "mdcc", "MDCC"),
    ]
    prod_links = []
    for f_name, s, label in products:
        cls = ' class="here"' if s == slug else ''
        prod_links.append(f'    <li><a href="{f_name}"{cls}>{label}</a></li>')
    prod_html = "  <h4>Products</h4>\n  <ul>\n" + "\n".join(prod_links) + "\n  </ul>"

    subs_html = """  <h4>Subsystems</h4>
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
  </ul>"""

    new_nav_block = f"{prod_html}\n{subs_html}"

    # Replace from <h4>Products</h4> until </aside>
    pattern = re.compile(r'  <h4>Products</h4>.*?  </ul>(\s*<h4>(?:Key subsystems|Subsystems)</h4>.*?  </ul>)?(\s*<h4>Doctrine</h4>.*?  </ul>)?', re.DOTALL)
    if pattern.search(content):
        new_content = pattern.sub(new_nav_block, content)
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Updated product nav: {filepath}")
    else:
        print(f"Pattern not found in: {filepath}")

# Update products
for slug, filename in [
    ("hacm-350", "products/hacm-350.html"),
    ("nightshade-adx1", "products/nightshade-adx1.html"),
    ("ahuti", "products/ahuti.html"),
    ("cortex", "products/cortex.html"),
    ("mdcc", "products/mdcc.html"),
    ("research-platforms", "products/research-platforms.html"),
]:
    p = os.path.join(WIKI_DIR, filename)
    if os.path.exists(p):
        update_product_page(p, slug)

