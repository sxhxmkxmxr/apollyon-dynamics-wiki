import os
import re

WIKI_DIR = "/home/soham-kumar/soham/apollyon/deck/wiki"

# Specific targeted replacements to ensure grammatical correctness and high fidelity
replacements = [
    ("an Indian defence prime", "an Indian neo-prime"),
    ("An Indian defence prime", "An Indian neo-prime"),
    ("Indian defence prime", "Indian neo-prime"),
    ("the new defence prime", "the sovereign neo-prime"),
    ("The new defence prime", "The sovereign neo-prime"),
    ("new defence prime", "neo-prime"),
    ("New defence prime", "Neo-prime"),
    ("New Defence Prime", "Neo-Prime"),
    ("new defense prime", "neo-prime"),
    ("New defense prime", "Neo-prime"),
    ("New Defense Prime", "Neo-Prime"),
    ("The defence prime can again be built from the bottom up", "A neo-prime can again be built from the bottom up"),
    ("defence prime can be built from the bottom up", "neo-prime can be built from the bottom up"),
]

count = 0
for root, dirs, files in os.walk(WIKI_DIR):
    for f in files:
        if f.endswith(".html") or f.endswith(".md") or f.endswith(".txt"):
            filepath = os.path.join(root, f)
            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()
            
            orig = content
            for old_s, new_s in replacements:
                content = content.replace(old_s, new_s)
            
            if content != orig:
                with open(filepath, "w", encoding="utf-8") as file:
                    file.write(content)
                print(f"Updated neo-prime narrative in: {os.path.relpath(filepath, WIKI_DIR)}")
                count += 1

print(f"Total files updated for neo-prime narrative: {count}")
