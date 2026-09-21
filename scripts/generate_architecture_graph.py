import os, math
from PIL import Image, ImageDraw, ImageFont

W = 3800
H = 2400
im = Image.new('RGBA', (W, H), (8, 10, 14, 255))
draw = ImageDraw.Draw(im)

# Fonts
font_title = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 38)
font_subtitle = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 20)
font_meta = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf', 15)
font_grp_title = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 21)
font_grp_sub = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 13)
font_card_title = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 17)
font_card_path = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 12)
font_card_desc = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12.5)
font_tag = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf', 11)

# Colors
BG_DARK = (8, 10, 14, 255)
CARD_BG = (16, 20, 28, 255)
CARD_BORDER = (34, 42, 58, 255)
TEXT_WHITE = (248, 250, 252, 255)
TEXT_GRAY = (148, 163, 184, 255)
TEXT_MUTED = (100, 116, 139, 255)

RED = (239, 68, 68, 255)
AMBER = (245, 158, 11, 255)
CYAN = (6, 182, 212, 255)
BLUE = (59, 130, 246, 255)
GREEN = (16, 185, 129, 255)
PURPLE = (168, 85, 247, 255)
LINE_DIM = (40, 50, 68, 180)

# Subtle background grid
for x in range(0, W, 80):
    draw.line([(x, 0), (x, H)], fill=(18, 22, 32, 120), width=1)
for y in range(0, H, 80):
    draw.line([(0, y), (W, y)], fill=(18, 22, 32, 120), width=1)

# Top Masthead
draw.rectangle([(0, 0), (W, 140)], fill=(12, 15, 21, 255))
draw.line([(0, 140), (W, 140)], fill=(28, 36, 50, 255), width=2)
draw.text((80, 32), "APOLLYON DYNAMICS  //  ENGINEERING WIKI ARCHITECTURAL GRAPH", fill=TEXT_WHITE, font=font_title)
draw.text((80, 85), "Complete topology & traversal paths from index.html across 24 pages, 6 functional pillars, and 1,507 verified cross-links", fill=TEXT_GRAY, font=font_subtitle)

# Meta Badges
badges = [
    ("24 HTML PAGES", GREEN),
    ("1,507 LINKS VERIFIED", CYAN),
    ("ZERO BROKEN ANCHORS", BLUE),
    ("REV 3.0", RED)
]
bx = W - 80
for btext, bcolor in reversed(badges):
    bbox = font_meta.getbbox(btext)
    bw = bbox[2] - bbox[0] + 24
    bx -= bw
    draw.rounded_rectangle([(bx, 48), (bx + bw - 10, 88)], radius=6, fill=(22, 28, 40, 255), outline=bcolor, width=1)
    draw.text((bx + 8, 60), btext, fill=bcolor, font=font_meta)
    bx -= 10

def draw_group_backdrop(x1, y1, x2, y2, title, subtitle, color):
    draw.rounded_rectangle([(x1, y1), (x2, y2)], radius=12, fill=(12, 15, 21, 220), outline=color, width=1)
    draw.rounded_rectangle([(x1, y1), (x2, y1 + 50)], radius=12, fill=(18, 23, 33, 255))
    draw.line([(x1, y1 + 50), (x2, y1 + 50)], fill=color, width=1)
    draw.text((x1 + 20, y1 + 14), title, fill=TEXT_WHITE, font=font_grp_title)
    if subtitle:
        draw.text((x1 + 24 + font_grp_title.getbbox(title)[2], y1 + 18), f"·  {subtitle}", fill=color, font=font_grp_sub)

cards = {}

def draw_node(key, x, y, w, h, title, path, desc, tag, tag_color, border_color=CARD_BORDER):
    cards[key] = {
        'rect': (x, y, x + w, y + h),
        'center': (x + w // 2, y + h // 2),
        'left': (x, y + h // 2),
        'right': (x + w, y + h // 2),
        'top': (x + w // 2, y),
        'bottom': (x + w // 2, y + h),
        'title': title
    }
    draw.rounded_rectangle([(x, y), (x + w, y + h)], radius=8, fill=CARD_BG, outline=border_color, width=2)
    t_box = font_tag.getbbox(tag)
    tw = t_box[2] - t_box[0] + 16
    draw.rounded_rectangle([(x + w - tw - 12, y + 10), (x + w - 12, y + 30)], radius=4, fill=(24, 30, 42, 255), outline=tag_color, width=1)
    draw.text((x + w - tw - 4, y + 13), tag, fill=tag_color, font=font_tag)
    draw.text((x + 16, y + 14), title, fill=TEXT_WHITE, font=font_card_title)
    draw.text((x + 16, y + 38), path, fill=tag_color, font=font_card_path)
    draw.text((x + 16, y + 62), desc, fill=TEXT_GRAY, font=font_card_desc)

# ═══════════════════════════════════════════════════════════════════════════
# 1. ROOT PORTAL: index.html
# ═══════════════════════════════════════════════════════════════════════════
draw_group_backdrop(60, 170, 560, 1720, "ROOT PORTAL", "THE MASTER BRIEFING & MANIFESTO", RED)
root_x, root_y, root_w, root_h = 80, 240, 460, 1450
cards['index.html'] = {
    'rect': (root_x, root_y, root_x + root_w, root_y + root_h),
    'center': (root_x + root_w // 2, root_y + root_h // 2),
    'left': (root_x, root_y + root_h // 2),
    'right': (root_x + root_w, root_y + root_h // 2),
    'top': (root_x + root_w // 2, root_y),
    'bottom': (root_x + root_w // 2, root_y + root_h),
    'title': 'Master Brief'
}
draw.rounded_rectangle([(root_x, root_y), (root_x + root_w, root_y + root_h)], radius=10, fill=(20, 24, 34, 255), outline=RED, width=2)
draw.rounded_rectangle([(root_x + root_w - 120, root_y + 14), (root_x + root_w - 16, root_y + 40)], radius=4, fill=(40, 16, 16, 255), outline=RED, width=1)
draw.text((root_x + root_w - 110, root_y + 18), "ENTRYPOINT", fill=RED, font=font_tag)
draw.text((root_x + 20, root_y + 18), "index.html", fill=TEXT_WHITE, font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 24))
draw.text((root_x + 20, root_y + 54), "An Indian neo-prime, built from the bottom up", fill=TEXT_GRAY, font=font_subtitle)

sec_items = [
    ("01 · Origin", "BITS Pilani hostel to Ladakh proving ground", 115),
    ("02 · Doctrine", "Precision is Mercy · New Arsenal · Missing Middle", 225),
    ("03 · The War", "Attrition arithmetic & daily drone consumption", 355),
    ("04 · Strategic Dependency", "70-year record of denial & sovereign mandate", 485),
    ("05 · The Ten-Year Window", "Capital reservation (75%) & structural reforms", 615),
    ("06 · The Plan", "Strike per Rupee · kg·km logarithmic envelope", 745),
    ("07 · Architecture", "The Invariant Core & Hardware/Software loop", 875),
    ("08 · Products", "Ahuti, Nightshade, Hemlock, Piranha", 1005),
    ("09 · The Business", "Revenue now (tactical) → compounding later", 1135),
    ("10 · Moats", "Demonstrated velocity & Tonbo unaligned corridor", 1265)
]
for snum, sdesc, sy in sec_items:
    draw.rounded_rectangle([(root_x + 16, root_y + sy), (root_x + root_w - 16, root_y + sy + 95)], radius=6, fill=(16, 20, 28, 255), outline=(32, 40, 56, 255), width=1)
    draw.text((root_x + 30, root_y + sy + 14), snum, fill=RED, font=font_tag)
    draw.text((root_x + 30, root_y + sy + 38), sdesc, fill=TEXT_GRAY, font=font_card_desc)

# ═══════════════════════════════════════════════════════════════════════════
# 2. PILLAR 1: DOCTRINE & FOUNDATIONAL THESIS (x: 640, y: 170, w: 620, h: 560)
# ═══════════════════════════════════════════════════════════════════════════
draw_group_backdrop(640, 170, 1260, 730, "01 · DOCTRINE & ETHOS", "ETHICAL & INDUSTRIAL THESIS", RED)
dx = 660
draw_node('precision-is-mercy.html', dx, 235, 580, 105, "Precision is Mercy", "wiki/doctrine/precision-is-mercy.html", "Ethical basis of strike: force without discrimination is barbarism;\nrestraint without lethality is impotence. Eliminates legitimate targets.", "ETHICAL", RED)
draw_node('new-arsenal.html', dx, 355, 580, 105, "The New Arsenal", "wiki/doctrine/new-arsenal.html", "Sovereign autonomy: an arsenal is not a stored stockpile, but the\nactive domestic capacity to build and modify weapons during war.", "INDUSTRIAL", RED)
draw_node('missing-middle.html', dx, 475, 580, 105, "The Missing Middle", "wiki/doctrine/missing-middle.html", "The barbell deficit: ordnance volume at base vs exquisite strategic apex.\nThe missing middle is attritable, software-defined mass built at rate.", "TEMPO THESIS", RED)
draw_node('strike-design-space.html', dx, 595, 580, 105, "Strike Design Space", "wiki/doctrine/strike-design-space.html", "Worked engineering case: Flamingo vs Barracuda vs Apollyon trade space;\nthree-axis salvo arithmetic across trans-Himalayan theatres.", "WORKED EXAMPLE", RED)

# ═══════════════════════════════════════════════════════════════════════════
# 3. PILLAR 2: STRATEGY & ECONOMICS (x: 640, y: 760, w: 620, h: 480)
# ═══════════════════════════════════════════════════════════════════════════
draw_group_backdrop(640, 760, 1260, 1240, "02 · STRATEGY & ECONOMICS", "COST ARITHMETIC & GO-TO-MARKET", AMBER)
sx = 660
draw_node('trajectory.html', sx, 825, 580, 115, "The Trajectory: Strike per Rupee", "wiki/strategy/trajectory.html", "The objective function: cost per kg·km. Nightshade Mk II (₹3,333/kg·km)\ndown to Hemlock Mk II (₹35/kg·km) — 14× below Tomahawk.", "METRIC", AMBER)
draw_node('competitive.html', sx, 955, 580, 115, "The Competitive Field", "wiki/strategy/competitive.html", "Honest benchmarking: cadence advantage vs Indian legacy primes;\ncapital efficiency & fabrication cost advantage vs Western neo-primes.", "BENCHMARK", AMBER)
draw_node('supply-chain.html', sx, 1085, 580, 115, "The Sovereign Supply Chain", "wiki/strategy/supply-chain.html", "Multi-sourced by design: dual domestic and neutral foreign suppliers;\nTonbo TRAP-1 seeker alliance; zero ITAR or single-source foreign veto.", "RESILIENCE", AMBER)

# ═══════════════════════════════════════════════════════════════════════════
# 4. PILLAR 3: STRATEGIC DEPENDENCY & RECORD (x: 640, y: 1270, w: 620, h: 450)
# ═══════════════════════════════════════════════════════════════════════════
draw_group_backdrop(640, 1270, 1260, 1720, "03 · DEPENDENCY & ORIGINS", "HISTORICAL EVIDENCE & PEDIGREE", PURPLE)
hx = 660
draw_node('full-record.html', hx, 1335, 580, 160, "The Full Record", "wiki/strategic-dependency/full-record.html", "70-year chronicle of foreign technology denials (1947–2024):\nKashmir, 1965, 1971, Pokhran-I/II, GPS denial in Kargil.\nThe historical proof of why strategic autonomy demands sovereign code.", "70 EPISODES", PURPLE)
draw_node('history.html', hx, 1515, 580, 160, "Hostel Room to Frontline", "wiki/about/history.html", "Founding history from BITS Pilani Hyderabad (May 2025) to Ladakh trials,\nproving grounds across 5 stations, national flight record (498 km/h),\nand rapid transformation into India's leading defence neo-prime.", "ORIGIN STORY", PURPLE)

# ═══════════════════════════════════════════════════════════════════════════
# 5. PILLAR 4: ARCHITECTURE & SUBSYSTEMS (x: 1340, y: 170, w: 1040, h: 1550)
# ═══════════════════════════════════════════════════════════════════════════
draw_group_backdrop(1340, 170, 2380, 1720, "04 · ARCHITECTURE & THE SHARED CORE", "INVARIANT KERNEL & MODULAR SUBSYSTEMS", CYAN)
draw_node('architecture/index.html', 1360, 235, 1000, 125, "The Shared Core: Hardware, Software & Method", "wiki/architecture/index.html", "Invariant guidance, navigation & state estimation stack reusable across airframes.\nSeparates vehicle physics from mission autonomy; digital twin HIL telemetry loop.", "SHARED CORE", CYAN, border_color=CYAN)

sub_w = 485
sub_h = 135
sub_nodes = [
    ('near-envelope-control.html', 1360, 385, "Robust Flight Control", "wiki/subsystems/near-envelope-control.html", "Gain-scheduled optimal observers & dynamic inversion\noperating at dynamic pressure boundaries & high-G pull-up.", "CONTROL", BLUE),
    ('gnss-denied-navigation.html', 1875, 385, "High-Speed GNSS-Denied Nav", "wiki/subsystems/gnss-denied-navigation.html", "CRPA multi-element anti-jam, visual odometry, DSMAC\nscene matching & strapdown inertial drift bounds.", "NAVIGATION", BLUE),
    ('onboard-compute.html', 1360, 545, "Edge Compute & Custom Inference", "wiki/subsystems/onboard-compute.html", "Deterministic microsecond deadline execution (WCET);\nbare-metal automotive silicon; sensor-to-actuator loop.", "COMPUTE", BLUE),
    ('flight-software.html', 1875, 545, "Flight Software Stack", "wiki/subsystems/flight-software.html", "Hardened deterministic RTOS kernel, zero dynamic\nallocation in flight loop, SIL/HIL test harnesses.", "SOFTWARE", BLUE),
    ('seekers.html', 1360, 705, "Seekers & Terminal Guidance", "wiki/subsystems/seekers.html", "Tonbo TRAP-1 dual-band EO/IR & active radar seekers;\ncloses terminal guidance independently without RF link.", "SEEKERS", BLUE),
    ('propulsion.html', 1875, 705, "Propulsion & Thrust Margin", "wiki/subsystems/propulsion.html", "Micro-turbojets (30–350 kgf) & high-RPM brushless\nmotors; high-altitude derating curves for Ladakh.", "PROPULSION", BLUE),
    ('airframe-structures.html', 1360, 865, "Airframe & Structures", "wiki/subsystems/airframe-structures.html", "Carbon composite vacuum-infusion, stamped metal\nbulkheads, standard fasteners, automotive-rate tooling.", "STRUCTURES", BLUE),
    ('launch-systems.html', 1875, 865, "Launch & Ground Systems", "wiki/subsystems/launch-systems.html", "Runway-independent pneumatic catapults & vehicle-\nmounted dynamic jet launch; 120-second scramble time.", "LAUNCH", BLUE),
]
for sn in sub_nodes:
    draw_node(sn[0], sn[1], sn[2], sub_w, sub_h, sn[3], sn[4], sn[5], sn[6], sn[7])

draw_node('research-platforms.html', 1360, 1025, 1000, 115, "Research Platforms (Testbeds A & B)", "wiki/products/research-platforms.html", "Dedicated non-commercial flight testbeds: dense telemetry instrumentation extracting\nparameter residuals, training adaptive models, and proving kernels before weapon integration.", "TESTBEDS", CYAN)

# Explanatory Callout inside Architecture
draw.rounded_rectangle([(1360, 1165), (2360, 1690)], radius=8, fill=(16, 20, 28, 255), outline=(34, 44, 62, 255), width=1)
draw.text((1385, 1185), "THE TWO OPERATIONAL REGISTERS OF THE SHARED CORE", fill=CYAN, font=font_card_title)
arch_desc_lines = [
    "A · THE MACHINE — WHAT FLIES:",
    "   Every vehicle runs an identical invariant autonomy stack: state estimation, UKF sensor",
    "   fusion, deterministic RTOS, and guidance laws. Per-platform deltas are strictly isolated",
    "   to mission sensors, propulsion, and structural actuation.",
    "",
    "B · THE LOOP — SUBSYSTEM ITERATION CADENCE:",
    "   Boundary flight sorties generate high-rate IMU and sensor discrepancy logs. Flight",
    "   discrepancies do not trigger ad-hoc tuning; they isolate parameter residuals that update",
    "   the high-fidelity 6-DOF digital twin within hours.",
    "",
    "C · REUSABILITY ACROSS GENERATIONS:",
    "   When a new airframe is designed (e.g. Hemlock), 80%+ of the guidance, navigation, and",
    "   flight-control software is inherited without recertification. The airframe is packaging;",
    "   the software stack is the compounding sovereign product."
]
ay = 1225
for line in arch_desc_lines:
    color = TEXT_WHITE if line.startswith(("A", "B", "C")) else TEXT_GRAY
    draw.text((1385, ay), line, fill=color, font=font_card_desc)
    ay += 28

# ═══════════════════════════════════════════════════════════════════════════
# 6. PILLAR 5: OPERATIONAL PRODUCTS (x: 2460, y: 170, w: 1260, h: 1550)
# ═══════════════════════════════════════════════════════════════════════════
draw_group_backdrop(2460, 170, 3720, 1720, "05 · PRODUCTS & OPERATIONAL ARSENAL", "TACTICAL CASH ENGINES & STRATEGIC STRIKE", GREEN)
prod_w = 600
prod_h = 160
px1 = 2480
px2 = 3100

# Row 1: Tactical Cash Engines (y=235)
draw_node('ahuti.html', px1, 235, prod_w, prod_h, "Ahuti C-UAS Interceptor", "wiki/products/ahuti.html", "High-speed multirotor kinetic interceptor (498 km/h national record).\nConsumable air-defence effector for DKS / Make-II; defeats jet loitering\nmunitions in the 400 km/h threat band. Unit cost ₹10–15 Lakh.", "REVENUE ENGINE", GREEN, border_color=GREEN)
draw_node('nightshade-adx1.html', px2, 235, prod_w, prod_h, "Nightshade Mk II", "wiki/products/nightshade-adx1.html", "Jet-powered one-way effector & aerial target (700 km/h, 300 km, 15 kg warhead).\nPlanning price ₹1.5 Cr (~₹3,333/kg·km). Dual-role target drone captures\nrecurring peacetime training contracts (AADC) into steady operating cash.", "REVENUE ENGINE", GREEN, border_color=GREEN)

# Row 2: Deep Standoff Strike & Maritime (y=425)
draw_node('hemlock.html', px1, 425, prod_w, prod_h, "Hemlock Family (Mk I / Mk II)", "wiki/products/hemlock.html", "Long-range deep-strike cruise missiles:\n• Mk I: 75 kg warhead, 1,000 km range, 900 km/h, ₹350/kg·km target.\n• Mk II: 1,000 kg warhead, 1,500 km range, terrain-following, ₹35/kg·km floor.", "STRATEGIC STRIKE", GREEN, border_color=GREEN)
draw_node('usv-strike.html', px2, 425, prod_w, prod_h, "Piranha USV", "wiki/products/usv-strike.html", "Low-observable autonomous surface vessel for maritime interdiction,\nport protection, and coastal surveillance. Shared sovereign navigation stack;\nattritable kinetic strike without risking naval personnel.", "MARITIME STRIKE", GREEN)

# Large Product Summary Box in Pillar 5 (y=615 to 1690)
draw.rounded_rectangle([(px1, 615), (px2 + prod_w, 1690)], radius=8, fill=(16, 20, 28, 255), outline=(34, 44, 62, 255), width=1)
draw.text((px1 + 25, 640), "ARSENAL ROADMAP & FLIGHT ENVELOPE TRAJECTORY", fill=GREEN, font=font_card_title)
prod_summary_lines = [
    "• FLIGHT-PROVEN HARDWARE (2025–2026):",
    "   - Ahuti Mk II: Certified at 498 km/h by India Book of Records (1 Sep 2026); defeats",
    "     jet loitering munitions in the 400 km/h threat band within a 10 km engagement radius.",
    "   - Nightshade Mk I: Flown 2026; validated dynamic vehicle-mounted jet catapult launch at 650 km/h.",
    "",
    "• NEAR-TERM SERIAL PRODUCTION (2027–2028):",
    "   - Nightshade Mk II: 15 kg warhead, 300 km range, 700 km/h terminal dive (4,500 kg·km).",
    "     Planning price near ₹1.5 crore (~₹3,333 / kg·km). Dual-role configuration captures recurring",
    "     peacetime live-fire training (AADC) while logging thousands of flight hours on serial tooling.",
    "   - Nightshade Mk III: 25 kg warhead, 500 km range, 800 km/h dive (12,500 kg·km, ₹1,700/kg·km).",
    "",
    "• STRATEGIC DEEP STRIKE (2029–2031):",
    "   - Hemlock Mk I: 75 kg warhead, 1,000 km range, 900 km/h cruise (75,000 kg·km, ₹350/kg·km).",
    "   - Hemlock Mk II: 1,000 kg warhead, 1,500 km range, terrain-following (1.5M kg·km, ₹35/kg·km).",
    "     Brings sovereign heavy standoff strike to ~14× below Tomahawk cost floor.",
    "",
    "• PROVING GROUNDS & USER EVALUATIONS FOOTPRINT:",
    "   - Verified operational evaluations and field trials across active service formations:",
    "     15 Guards (Jammu), BSF Academy (Gwalior), 181 Mountain Brigade (Lohitpur),",
    "     Army Air Defence College (Gopalpur), and Babina Field Firing Ranges."
]
py = 685
for line in prod_summary_lines:
    color = TEXT_WHITE if line.startswith("•") else TEXT_GRAY
    draw.text((px1 + 25, py), line, fill=color, font=font_card_desc)
    py += 30

# ═══════════════════════════════════════════════════════════════════════════
# 7. BOTTOM STRATEGIC BRIDGE
# ═══════════════════════════════════════════════════════════════════════════
draw_group_backdrop(60, 1760, 3720, 2340, "GOVERNING COMMERCIAL & TECHNICAL SYNTHESIS", "REVENUE NOW · COMPOUNDING CAPABILITY LATER", AMBER)

box_w = 1180
by = 1830
bh = 470

# Col 1
draw.rounded_rectangle([(80, by), (80 + box_w, by + bh)], radius=8, fill=CARD_BG, outline=AMBER, width=1)
draw.text((105, by + 20), "01 · PROCUREMENT VELOCITY INVERSION", fill=AMBER, font=font_card_title)
p1_text = [
    "• Capital Gestation Trap (DAP 2020):",
    "   - Strategic missiles (Hemlock) cost crores, requiring Tri-Service GSQR,",
    "     DAC Acceptance of Necessity (AoN), and 4–6 years of multi-season field trials.",
    "   - Startups relying solely on capital tenders burn venture equity on binary risks.",
    "",
    "• Delegated Revenue Expenditure (DFPDS):",
    "   - Tactical effectors (Ahuti) priced under ₹15L utilize delegated spending (Corps up to ₹25–50 Cr, Commands up to ₹100–500 Cr).",
    "   - Field corps and air-defence directorates procure on 6–12 month timelines.",
    "",
    "• Frontline Consumption Scale:",
    "   - Strategic missiles are stocked in hundreds; tactical interceptors are consumed in thousands.",
    "   - Ahuti delivers high gross margin per engineering month, creating positive operating cash flow."
]
py = by + 65
for line in p1_text:
    color = TEXT_WHITE if line.startswith("•") else TEXT_GRAY
    draw.text((105, py), line, fill=color, font=font_card_desc)
    py += 26

# Col 2
draw.rounded_rectangle([(1300, by), (1300 + box_w, by + bh)], radius=8, fill=CARD_BG, outline=GREEN, width=1)
draw.text((1325, by + 20), "02 · DUAL CASH ENGINES & SOVEREIGN COMPOUNDING", fill=GREEN, font=font_card_title)
p2_text = [
    "• Ahuti (Consumable Tactical C-UAS):",
    "   - High-rate multi-thousand unit revenue tranches into active air-defence networks",
    "     (Indian Army DKS / DGAAD / Raphe mPhibr).",
    "",
    "• Nightshade Mk II (Peacetime Training OpEx):",
    "   - Converted to target drone via Luneburg reflectors & miss-distance optics.",
    "   - Captures recurring peacetime training grants (Army Air Defence College / AADC),",
    "     logging thousands of flight hours on shared tooling and software.",
    "",
    "• Compounding into Hemlock & Heavy Deep Strike:",
    "   - Tactical cash flow directly finances high-tonnage tooling, wind-tunnel time, and turbofans.",
    "   - Hemlock enters production backed by an industrialized, self-funding neo-prime."
]
py = by + 65
for line in p2_text:
    color = TEXT_WHITE if line.startswith("•") else TEXT_GRAY
    draw.text((1325, py), line, fill=color, font=font_card_desc)
    py += 26

# Col 3
draw.rounded_rectangle([(2520, by), (2520 + box_w, by + bh)], radius=8, fill=CARD_BG, outline=CYAN, width=1)
draw.text((2545, by + 20), "03 · THE INVARIANT CODEBASE & SOVEREIGN SUPPLY CHAIN", fill=CYAN, font=font_card_title)
p3_text = [
    "• Invariant Guidance Stack (The Guidance is the Product):",
    "   - Every vehicle runs identical state estimation, CRPA anti-jam, and flight control.",
    "   - New airframe is purely packaging (engine class, structural volume, launch mode).",
    "",
    "• Empirical Sortie Flywheel:",
    "   - Proving ground sorties across five military stations feed telemetry back into digital twin.",
    "   - Gain schedules and adaptive policies patch over-the-air in 48 hours without redesign.",
    "",
    "• Zero Foreign Veto & The Tonbo Export Corridor:",
    "   - Strategic partnership with Tonbo Imaging secures domestic TRAP-1 seekers.",
    "   - Established 15-year footprint across 24+ non-aligned nations (Armenia, LatAm, Africa),",
    "     opening massive export markets immune to ITAR and Western/Russian embargoes."
]
py = by + 65
for line in p3_text:
    color = TEXT_WHITE if line.startswith("•") else TEXT_GRAY
    draw.text((2545, py), line, fill=color, font=font_card_desc)
    py += 26

# ═══════════════════════════════════════════════════════════════════════════
# 8. CLEAN ROUTED CONNECTORS
# ═══════════════════════════════════════════════════════════════════════════

def draw_clean_wire(p1, p2, color=LINE_DIM, width=2, dashed=False, arrow=True):
    x1, y1 = p1
    x2, y2 = p2
    mid_x = (x1 + x2) // 2
    points = [(x1, y1), (mid_x, y1), (mid_x, y2), (x2, y2)]
    if dashed:
        for i in range(len(points) - 1):
            xa, ya = points[i]
            xb, yb = points[i+1]
            dist = math.hypot(xb - xa, yb - ya)
            steps = int(dist // 12)
            for s in range(0, steps, 2):
                t1 = s / max(1, steps)
                t2 = min(1.0, (s + 1) / max(1, steps))
                draw.line([(xa + (xb - xa) * t1, ya + (yb - ya) * t1),
                           (xa + (xb - xa) * t2, ya + (yb - ya) * t2)], fill=color, width=width)
    else:
        draw.line(points, fill=color, width=width)
    if arrow:
        arr_size = 6
        draw.polygon([(x2, y2), (x2 - arr_size * 2, y2 - arr_size), (x2 - arr_size * 2, y2 + arr_size)], fill=color)

# Wire from index.html right edge to pillars
draw_clean_wire((540, 465), cards['missing-middle.html']['left'], color=RED, width=3)
draw_clean_wire((540, 985), cards['trajectory.html']['left'], color=AMBER, width=3)
draw_clean_wire((540, 1415), cards['full-record.html']['left'], color=PURPLE, width=3)
draw_clean_wire((540, 1595), cards['history.html']['left'], color=PURPLE, width=2)

# Wire from missing-middle.html to strike-design-space.html
draw_clean_wire(cards['missing-middle.html']['bottom'], cards['strike-design-space.html']['top'], color=RED, width=2)

# Wire from Architecture index.html to subsystems
draw.line([(1860, 360), (1860, 1000)], fill=CYAN, width=2)
for sn in sub_nodes:
    card_info = cards[sn[0]]
    if card_info['center'][0] < 1860:
        draw.line([(1860, card_info['center'][1]), (card_info['right'][0], card_info['center'][1])], fill=CYAN, width=2)
    else:
        draw.line([(1860, card_info['center'][1]), (card_info['left'][0], card_info['center'][1])], fill=CYAN, width=2)

# Wire from Architecture to Products (Shared Core Inheritance)
draw_clean_wire((2360, 290), cards['ahuti.html']['left'], color=CYAN, width=2)
draw_clean_wire((2360, 450), cards['hemlock.html']['left'], color=CYAN, width=2)
draw_clean_wire((2360, 490), cards['usv-strike.html']['left'], color=CYAN, width=2)

# Cash Engine Flow: Ahuti & Nightshade → Hemlock
# Ahuti (down to Hemlock)
draw_clean_wire(cards['ahuti.html']['bottom'], cards['hemlock.html']['top'], color=AMBER, width=3, dashed=True)
# Nightshade (down around to Hemlock)
ns_pt = cards['nightshade-adx1.html']['bottom']
hem_rt = cards['hemlock.html']['right']
draw.line([ns_pt, (ns_pt[0], ns_pt[1] + 25)], fill=AMBER, width=3)
draw.line([(ns_pt[0], ns_pt[1] + 25), (hem_rt[0] + 30, ns_pt[1] + 25)], fill=AMBER, width=3)
draw.line([(hem_rt[0] + 30, ns_pt[1] + 25), (hem_rt[0] + 30, hem_rt[1])], fill=AMBER, width=3)
draw.line([(hem_rt[0] + 30, hem_rt[1]), hem_rt], fill=AMBER, width=3)
draw.polygon([(hem_rt[0], hem_rt[1]), (hem_rt[0] + 12, hem_rt[1] - 6), (hem_rt[0] + 12, hem_rt[1] + 6)], fill=AMBER)

# Save image in artifact directory and in workspace
artifact_path = '/home/soham-kumar/.gemini/antigravity-cli/brain/a8d10e0e-dcd7-4728-a0f7-50377890e9ab/wiki_architecture_graph.png'
workspace_path = 'wiki/assets/wiki_architecture_graph.png'

im.save(artifact_path, 'PNG')
im.save(workspace_path, 'PNG')
print('Successfully saved v3 graph image to:')
print('  Artifact:', artifact_path)
print('  Workspace:', workspace_path)
