with open('/home/soham-kumar/soham/apollyon/deck/wiki/scripts/build_all.py', 'r') as f:
    text = f.read()

# Cut off at # 7. wiki/subsystems/physics-backbone.html
if "# 7. wiki/subsystems/physics-backbone.html" in text:
    text = text[:text.index("# 7. wiki/subsystems/physics-backbone.html")]

with open('/home/soham-kumar/soham/apollyon/deck/wiki/scripts/build_all.py', 'w') as f:
    f.write(text)

print("build_all.py cleaned.")
