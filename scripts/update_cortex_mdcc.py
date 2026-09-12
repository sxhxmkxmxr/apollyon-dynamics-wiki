with open("/home/soham-kumar/soham/apollyon/deck/wiki/products/cortex.html", "r") as f:
    c = f.read()

c = c.replace(
    '<span>· fielded · GSQR reference CORTEX-MDCC-25-1042-03 · v1.0</span>',
    '<span>· TRL 4–5 · development · GSQR reference CORTEX-MDCC-25-1042-03 · v1.0</span>'
)
c = c.replace(
    '<span class="right">Fielded · runs on MDCC, command post, ops room or edge server</span>',
    '<span class="right">TRL 4–5 · development · runs on MDCC, command post, ops room or edge server</span>'
)
with open("/home/soham-kumar/soham/apollyon/deck/wiki/products/cortex.html", "w") as f:
    f.write(c)

with open("/home/soham-kumar/soham/apollyon/deck/wiki/products/mdcc.html", "r") as f:
    m = f.read()

m = m.replace(
    '<span>· fielded · Cortex primary tactical host</span>',
    '<span>· TRL 4–5 · development · Cortex primary tactical host</span>'
)
m = m.replace(
    '<span class="right">Fielded · running Apollyon Cortex</span>',
    '<span class="right">TRL 4–5 · development · running Apollyon Cortex</span>'
)
with open("/home/soham-kumar/soham/apollyon/deck/wiki/products/mdcc.html", "w") as f:
    f.write(m)

print("Cortex and MDCC updated to TRL 4–5 development.")
