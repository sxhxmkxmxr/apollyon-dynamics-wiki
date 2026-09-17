import re
import os

WIKI_DIR = "/home/soham-kumar/soham/apollyon/deck/wiki"

# Files to update
replacements = [
    # (file_relative, old_str, new_str)
    ("subsystems/airframe-structures.html", 'href="physics-backbone.html"', 'href="near-envelope-control.html#backbone"'),
    ("doctrine/new-arsenal.html", 'href="../subsystems/physics-backbone.html"', 'href="../subsystems/near-envelope-control.html#backbone"'),
    ("products/ahuti.html", 'href="../subsystems/physics-backbone.html"', 'href="../subsystems/near-envelope-control.html#backbone"'),
    ("products/research-platforms.html", 'href="../subsystems/physics-backbone.html"', 'href="../subsystems/near-envelope-control.html#backbone"'),
    ("doctrine/missing-middle.html", 'href="../subsystems/anti-jam-gnss.html"', 'href="../subsystems/gnss-denied-navigation.html#crpa"'),
    ("products/hacm-350.html", 'href="../subsystems/anti-jam-gnss.html"', 'href="../subsystems/gnss-denied-navigation.html#crpa"'),
    ("products/nightshade-adx1.html", 'href="../subsystems/anti-jam-gnss.html"', 'href="../subsystems/gnss-denied-navigation.html#crpa"'),
    ("README.md", '`subsystems/physics-backbone.html`', '`subsystems/near-envelope-control.html`'),
]

for rel_path, old_s, new_s in replacements:
    full_path = os.path.join(WIKI_DIR, rel_path)
    if os.path.exists(full_path):
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if old_s in content:
            content = content.replace(old_s, new_s)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Replaced link in {rel_path}")
        else:
            print(f"Old string not found in {rel_path}")

