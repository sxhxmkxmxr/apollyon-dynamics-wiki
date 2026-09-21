import os
import re
from urllib.parse import urlparse

WIKI_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
html_files = []
for root, dirs, files in os.walk(WIKI_DIR):
    for f in files:
        if f.endswith(".html"):
            html_files.append(os.path.join(root, f))

print(f"Total HTML files found: {len(html_files)}")

file_ids = {}
for hf in html_files:
    with open(hf, 'r', encoding='utf-8') as f:
        text = f.read()
    ids = set(re.findall(r'id=["\']([^"\']+)["\']', text))
    file_ids[hf] = ids

errors = []
total_links = 0

for hf in html_files:
    rel_path = os.path.relpath(hf, WIKI_DIR)
    with open(hf, 'r', encoding='utf-8') as f:
        raw_text = f.read()

    # Strip script blocks so JS template literals are not parsed as static HTML links
    cleaned_html = re.sub(r'<script\b[^>]*>.*?</script>', '', raw_text, flags=re.DOTALL | re.IGNORECASE)

    links = re.findall(r'(?:href|src)=["\']([^"\']+)["\']', cleaned_html)
    for link in links:
        total_links += 1
        if (link.startswith("http://") or link.startswith("https://") or link.startswith("mailto:")
                or link.startswith("tel:") or link.startswith("data:") or link.startswith("javascript:")):
            continue
        
        parsed = urlparse(link)
        target_path = parsed.path
        target_frag = parsed.fragment

        if not target_path:
            if target_frag:
                if target_frag not in file_ids[hf]:
                    errors.append(f"[{rel_path}] Broken internal anchor: #{target_frag}")
            continue

        resolved_file = os.path.normpath(os.path.join(os.path.dirname(hf), target_path))
        if not os.path.exists(resolved_file):
            errors.append(f"[{rel_path}] Broken file link: {link} -> {os.path.relpath(resolved_file, WIKI_DIR)}")
        else:
            if target_frag and resolved_file in file_ids:
                if target_frag not in file_ids[resolved_file]:
                    errors.append(f"[{rel_path}] Broken anchor in {os.path.relpath(resolved_file, WIKI_DIR)}: {link} (anchor #{target_frag})")

if errors:
    print(f"Found {len(errors)} broken links/anchors:")
    for err in errors:
        print(f"  - {err}")
    exit(1)
else:
    print(f"All {total_links} links and anchors verified successfully with 0 errors!")
