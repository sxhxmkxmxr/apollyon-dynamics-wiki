css_content = """/* ══════════════════════════════════════════════════════════════════════
   APOLLYON DYNAMICS · NEO-PRIME ENGINEERING & INVESTMENT WIKI
   Visual system derived from apollyondynamics.com & CFB pitch decks:
   Deep obsidian background (#05070a), high-contrast tactical typography,
   stealth surface cards, electric blue/cyan accents, and technical linework.
   ══════════════════════════════════════════════════════════════════════ */

:root {
  --bg-primary: #05070a;
  --bg-surface: #0a0e17;
  --bg-surface-2: #101522;
  --bg-surface-elevated: #131b2c;
  --bg-surface-hover: #172136;
  
  --text-primary: #f8fafc;
  --text-secondary: #cbd5e1;
  --text-muted: #8292a4;
  --text-dim: #475569;
  
  --border-subtle: rgba(255, 255, 255, 0.08);
  --border-medium: rgba(255, 255, 255, 0.15);
  --border-cyan: rgba(56, 189, 248, 0.35);
  --border-blue: rgba(10, 132, 255, 0.4);

  --accent-cyan: #38bdf8;
  --accent-blue: #0a84ff;
  --accent-red: #ef4444;
  --accent-rose: #f43f5e;
  --accent-emerald: #10b981;
  --accent-amber: #f59e0b;

  --accent: var(--accent-cyan);
  --accent-wash: rgba(56, 189, 248, 0.08);

  --sans: "Inter", "Helvetica Neue", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --mono: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, Monaco, monospace;
  --serif: "Newsreader", Georgia, "Times New Roman", serif;

  --maxw: 1200px;
  --measure: 76ch;
  --sidebar: 250px;
}

*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html {
  scroll-behavior: smooth;
  -webkit-text-size-adjust: 100%;
  overflow-x: clip;
  background-color: var(--bg-primary);
}

::selection {
  background: rgba(56, 189, 248, 0.25);
  color: #ffffff;
}

body {
  background-color: var(--bg-primary);
  color: var(--text-secondary);
  font-family: var(--sans);
  font-size: 15px;
  line-height: 1.68;
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
  overflow-x: clip;
  background-image: 
    radial-gradient(circle at 50% 0%, rgba(10, 132, 255, 0.05) 0%, transparent 60%),
    linear-gradient(rgba(255, 255, 255, 0.015) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.015) 1px, transparent 1px);
  background-size: 100% 100%, 40px 40px, 40px 40px;
}

img, svg, table {
  max-width: 100%;
}

.mono { font-family: var(--mono); }
.serif { font-family: var(--serif); }
.accent { color: var(--accent-cyan); }
.muted { color: var(--text-muted); }

/* ── Top rail ───────────────────────────────────────────────────────── */
.rail {
  border-bottom: 1px solid var(--border-subtle);
  background: rgba(5, 7, 10, 0.88);
  backdrop-filter: blur(14px);
  position: sticky;
  top: 0;
  z-index: 100;
}
.rail-inner {
  max-width: var(--maxw);
  margin: 0 auto;
  padding: 12px 28px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
  font-family: var(--mono);
  font-size: 11px;
  letter-spacing: .08em;
  text-transform: uppercase;
}
.rail-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  color: var(--text-primary);
  font-weight: 700;
  letter-spacing: -0.01em;
  white-space: nowrap;
}
.rail-brand .glyph {
  width: 15px;
  height: 15px;
  flex: 0 0 auto;
  background: var(--accent-cyan);
  clip-path: polygon(0 78%, 46% 8%, 72% 44%, 100% 34%, 66% 92%, 38% 56%);
  box-shadow: 0 0 10px rgba(56, 189, 248, 0.6);
}
.rail-brand em {
  font-style: normal;
  color: var(--text-muted);
  font-weight: 400;
  margin-left: 4px;
}
.rail-links {
  display: flex;
  align-items: center;
  flex-shrink: 0;
}
.rail-links a {
  color: var(--text-muted);
  text-decoration: none;
  margin-left: 20px;
  padding: 4px 0;
  border-bottom: 1px solid transparent;
  white-space: nowrap;
  transition: color 0.18s ease, border-color 0.18s ease;
}
.rail-links a:hover, .rail-links a.on {
  color: var(--accent-cyan);
  border-bottom-color: var(--accent-cyan);
}
@media (max-width: 820px) {
  .rail-inner {
    overflow-x: auto;
    scrollbar-width: none;
    justify-content: flex-start;
    padding: 10px 16px;
  }
  .rail-inner::-webkit-scrollbar { display: none; }
  .rail-brand em { display: none; }
}

/* ── Shell & layout ─────────────────────────────────────────────────── */
.shell {
  max-width: var(--maxw);
  margin: 0 auto;
  padding: 0 28px;
  width: 100%;
}
@media (max-width: 620px) {
  .shell { padding: 0 16px; }
}

.layout {
  display: grid;
  grid-template-columns: var(--sidebar) minmax(0, 1fr);
  gap: 56px;
  align-items: start;
}
@media (max-width: 980px) {
  .layout {
    grid-template-columns: minmax(0, 1fr);
    gap: 0;
  }
}

/* ── Aside Navigation ───────────────────────────────────────────────── */
.aside {
  position: sticky;
  top: 74px;
  padding: 40px 0;
  font-size: 13px;
  max-height: calc(100vh - 90px);
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.1) transparent;
}
.aside::-webkit-scrollbar { width: 4px; }
.aside::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.1); border-radius: 4px; }

@media (max-width: 980px) {
  .aside {
    position: static;
    max-height: none;
    padding: 16px 0 6px;
    border-bottom: 1px solid var(--border-subtle);
    margin-bottom: 16px;
  }
  .aside h4 { margin-bottom: 7px; }
  .aside ul {
    display: flex;
    gap: 8px;
    overflow-x: auto;
    margin: 0 0 16px;
    padding-bottom: 5px;
    scrollbar-width: none;
    -webkit-overflow-scrolling: touch;
  }
  .aside ul::-webkit-scrollbar { display: none; }
  .aside li { margin: 0; flex-shrink: 0; }
  .aside li a {
    display: inline-block;
    padding: 3px 9px;
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 3px;
    font-size: 12px;
  }
}

.aside h4 {
  font-family: var(--mono);
  font-size: 10px;
  letter-spacing: .16em;
  text-transform: uppercase;
  color: var(--accent-cyan);
  margin: 0 0 10px 0;
  font-weight: 600;
}
.aside h4:not(:first-child) {
  margin-top: 28px;
}
.aside ul {
  list-style: none;
  margin: 0;
  padding: 0;
}
.aside li {
  margin: 0 0 4px 0;
}
.aside a {
  color: var(--text-muted);
  text-decoration: none;
  display: block;
  padding: 3px 6px;
  border-left: 2px solid transparent;
  transition: all 0.16s ease;
  border-radius: 0 2px 2px 0;
}
.aside a:hover {
  color: var(--text-primary);
  background: var(--bg-surface);
  border-left-color: var(--accent-blue);
}
.aside a.here {
  color: var(--accent-cyan);
  font-weight: 600;
  background: rgba(56, 189, 248, 0.07);
  border-left-color: var(--accent-cyan);
}

/* ── Main content column ────────────────────────────────────────────── */
.main {
  min-width: 0;
  padding: 40px 0 80px;
  max-width: var(--measure);
}
@media (max-width: 980px) {
  .main {
    max-width: 100%;
    padding: 20px 0 60px;
  }
}

/* ── Masthead ───────────────────────────────────────────────────────── */
.masthead {
  border-bottom: 1px solid var(--border-subtle);
  padding-bottom: 32px;
  margin-bottom: 40px;
}
.mast-meta {
  font-family: var(--mono);
  font-size: 11px;
  letter-spacing: .12em;
  text-transform: uppercase;
  color: var(--accent-cyan);
  margin-bottom: 14px;
  display: flex;
  align-items: center;
  gap: 12px;
}
.mast-meta span {
  color: var(--text-muted);
  text-transform: none;
  letter-spacing: normal;
  font-size: 11px;
}
.masthead h1 {
  font-family: var(--sans);
  font-weight: 800;
  font-size: clamp(32px, 5vw, 44px);
  line-height: 1.12;
  letter-spacing: -0.03em;
  color: var(--text-primary);
  margin-bottom: 16px;
}
.masthead h1 .sub {
  font-weight: 400;
  color: var(--text-muted);
  display: block;
  font-size: clamp(20px, 3.2vw, 26px);
  letter-spacing: -0.015em;
  margin-top: 4px;
}
.standfirst {
  font-size: 17px;
  line-height: 1.58;
  color: var(--text-secondary);
  margin: 0;
  max-width: 68ch;
}

/* ── Breadcrumb ─────────────────────────────────────────────────────── */
.crumb {
  font-family: var(--mono);
  font-size: 10.5px;
  letter-spacing: .1em;
  text-transform: uppercase;
  color: var(--text-muted);
  margin-bottom: 16px;
}
.crumb a {
  color: var(--text-muted);
  text-decoration: none;
  transition: color 0.15s ease;
}
.crumb a:hover {
  color: var(--accent-cyan);
}
.crumb span {
  margin: 0 7px;
  color: var(--border-medium);
}

/* ── Typography & sections ──────────────────────────────────────────── */
section {
  margin-bottom: 48px;
}
.sec-tag {
  font-family: var(--mono);
  font-size: 11px;
  letter-spacing: .14em;
  text-transform: uppercase;
  color: var(--accent-cyan);
  margin-bottom: 6px;
  font-weight: 600;
}
h2 {
  font-family: var(--sans);
  font-weight: 750;
  font-size: 24px;
  line-height: 1.25;
  letter-spacing: -0.025em;
  color: var(--text-primary);
  margin: 0 0 16px 0;
}
h3 {
  font-family: var(--sans);
  font-weight: 650;
  font-size: 17px;
  line-height: 1.35;
  letter-spacing: -0.015em;
  color: var(--text-primary);
  margin: 24px 0 10px 0;
}
h4 {
  font-family: var(--sans);
  font-weight: 600;
  font-size: 14px;
  color: var(--text-primary);
  margin: 18px 0 8px 0;
}
p {
  margin: 0 0 14px 0;
}
p.lede {
  font-size: 16.5px;
  line-height: 1.62;
  color: var(--text-primary);
}
strong, b {
  color: var(--text-primary);
  font-weight: 600;
}
ul, ol {
  margin: 0 0 16px 20px;
}
li {
  margin-bottom: 6px;
}
a {
  color: var(--accent-cyan);
  text-decoration: none;
  transition: color 0.15s ease;
}
a:hover {
  text-decoration: underline;
}
blockquote {
  border-left: 2px solid var(--accent-blue);
  background: var(--bg-surface);
  padding: 16px 22px;
  margin: 24px 0;
  color: var(--text-primary);
  border-radius: 0 4px 4px 0;
  font-size: 15px;
}
blockquote cite {
  display: block;
  font-style: normal;
  font-family: var(--mono);
  font-size: 11px;
  color: var(--accent-cyan);
  margin-top: 10px;
  letter-spacing: .06em;
  text-transform: uppercase;
}

/* ── Stat tiles ─────────────────────────────────────────────────────── */
.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
  margin: 24px 0;
}
.stat {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: 4px;
  padding: 16px 18px;
  position: relative;
  overflow: hidden;
  transition: border-color 0.2s ease, transform 0.2s ease;
}
.stat:hover {
  border-color: var(--border-medium);
  transform: translateY(-2px);
}
.stat .n {
  font-family: var(--sans);
  font-weight: 800;
  font-size: 28px;
  line-height: 1.1;
  color: var(--text-primary);
  letter-spacing: -0.03em;
  margin-bottom: 6px;
}
.stat .n.accent {
  color: var(--accent-cyan);
}
.stat .d {
  font-family: var(--mono);
  font-size: 11px;
  line-height: 1.45;
  color: var(--text-muted);
}
.stat .d .muted {
  display: block;
  margin-top: 4px;
  font-size: 10px;
  color: var(--text-dim);
}

/* ── Cards Grid ─────────────────────────────────────────────────────── */
.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
  margin: 24px 0;
}
.card {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: 4px;
  padding: 22px;
  display: flex;
  flex-direction: column;
  position: relative;
  transition: border-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
}
.card:hover {
  border-color: var(--border-cyan);
  transform: translateY(-3px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);
}
.card .kicker {
  font-family: var(--mono);
  font-size: 10px;
  letter-spacing: .12em;
  text-transform: uppercase;
  color: var(--accent-cyan);
  margin-bottom: 8px;
}
.card h3 {
  font-size: 18px;
  margin: 0 0 10px 0;
}
.card h3 a {
  color: var(--text-primary);
  text-decoration: none;
}
.card h3 a:hover {
  color: var(--accent-cyan);
}
.card p {
  font-size: 14px;
  line-height: 1.55;
  color: var(--text-secondary);
  flex-grow: 1;
  margin-bottom: 16px;
}
.card .foot {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 14px;
  border-top: 1px solid var(--border-subtle);
  font-family: var(--mono);
  font-size: 11px;
  color: var(--text-muted);
}

/* ── Status Pills ───────────────────────────────────────────────────── */
.pill {
  display: inline-block;
  padding: 2px 7px;
  border-radius: 3px;
  font-family: var(--mono);
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: .06em;
}
.pill.dev {
  background: rgba(245, 158, 11, 0.12);
  color: #fbbf24;
  border: 1px solid rgba(245, 158, 11, 0.3);
}
.pill.fielded {
  background: rgba(16, 185, 129, 0.12);
  color: #34d399;
  border: 1px solid rgba(16, 185, 129, 0.3);
}
.pill.core {
  background: rgba(56, 189, 248, 0.12);
  color: #38bdf8;
  border: 1px solid rgba(56, 189, 248, 0.3);
}

/* ── Tables ─────────────────────────────────────────────────────────── */
.tw {
  width: 100%;
  overflow-x: auto;
  margin: 24px 0;
  border: 1px solid var(--border-subtle);
  border-radius: 4px;
  background: var(--bg-surface);
}
table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13.5px;
  line-height: 1.5;
  text-align: left;
}
caption {
  font-family: var(--mono);
  font-size: 10.5px;
  letter-spacing: .12em;
  text-transform: uppercase;
  color: var(--text-muted);
  text-align: left;
  padding: 12px 16px;
  border-bottom: 1px solid var(--border-subtle);
  background: var(--bg-surface-2);
}
th {
  font-family: var(--mono);
  font-size: 11px;
  letter-spacing: .08em;
  text-transform: uppercase;
  color: var(--text-primary);
  background: var(--bg-surface-2);
  padding: 10px 16px;
  border-bottom: 1px solid var(--border-subtle);
  font-weight: 600;
}
th.num, td.num {
  text-align: right;
}
td {
  padding: 11px 16px;
  border-bottom: 1px solid var(--border-subtle);
  color: var(--text-secondary);
}
tr:last-child td {
  border-bottom: none;
}
tr:hover td {
  background: rgba(255, 255, 255, 0.02);
}

/* ── Spec Cards (Matrix layout on product pages) ─────────────────────── */
.spec-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: 4px;
  overflow: hidden;
  margin: 24px 0;
}
.spec-topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 16px;
  background: var(--bg-surface-2);
  border-bottom: 1px solid var(--border-subtle);
  font-family: var(--mono);
  font-size: 11px;
  letter-spacing: .08em;
  text-transform: uppercase;
  color: var(--accent-cyan);
}
.spec-topbar .right {
  color: var(--text-muted);
  text-transform: none;
}
.spec-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 0;
}
.spec-col {
  padding: 16px 18px;
  border-right: 1px solid var(--border-subtle);
}
.spec-col:last-child {
  border-right: none;
}
@media (max-width: 768px) {
  .spec-col {
    border-right: none;
    border-bottom: 1px solid var(--border-subtle);
  }
}
.spec-col-title {
  font-family: var(--mono);
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: .08em;
  color: var(--text-primary);
  margin-bottom: 14px;
  padding-bottom: 6px;
  border-bottom: 1px solid var(--border-subtle);
}
.spec-col .row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 9px;
  font-size: 12.5px;
  line-height: 1.4;
}
.spec-col .lbl {
  color: var(--text-muted);
  padding-right: 8px;
}
.spec-col .val {
  font-family: var(--mono);
  color: var(--text-primary);
  font-weight: 500;
  text-align: right;
  font-size: 12px;
}
.spec-col .val.accent {
  color: var(--accent-cyan);
  font-weight: 700;
}

/* ── Notes and Alert Boxes ──────────────────────────────────────────── */
.note {
  background: var(--bg-surface);
  border-left: 3px solid var(--border-medium);
  border-radius: 0 4px 4px 0;
  padding: 16px 20px;
  margin: 24px 0;
  font-size: 14px;
  line-height: 1.6;
}
.note.key {
  border-left-color: var(--accent-cyan);
  background: rgba(56, 189, 248, 0.04);
}
.note .t {
  font-family: var(--mono);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: .1em;
  text-transform: uppercase;
  color: var(--text-primary);
  margin-bottom: 6px;
}
.note.key .t {
  color: var(--accent-cyan);
}
.note p:last-child {
  margin-bottom: 0;
}

/* ── Figures and Media ──────────────────────────────────────────────── */
figure {
  margin: 28px 0;
  border: 1px solid var(--border-subtle);
  border-radius: 4px;
  overflow: hidden;
  background: var(--bg-surface);
}
figure img {
  display: block;
  width: 100%;
  height: auto;
}
figcaption {
  padding: 10px 16px;
  font-size: 12.5px;
  color: var(--text-muted);
  background: var(--bg-surface-2);
  border-top: 1px solid var(--border-subtle);
}
figcaption b {
  font-family: var(--mono);
  font-size: 11px;
  text-transform: uppercase;
  color: var(--text-primary);
  margin-right: 6px;
}

/* ── CAD Blueprint Plates ───────────────────────────────────────────── */
.blueprint-plate {
  margin: 28px 0;
  border: 1px solid rgba(56, 189, 248, 0.2);
  background: #070a0f;
  border-radius: 4px;
  overflow: hidden;
  position: relative;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
}
.blueprint-plate::before {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  background-image:
    linear-gradient(to right, rgba(56, 189, 248, 0.035) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(56, 189, 248, 0.035) 1px, transparent 1px);
  background-size: 20px 20px;
}
.blueprint-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 16px;
  background: #0d121c;
  border-bottom: 1px solid rgba(56, 189, 248, 0.18);
  font-family: var(--mono);
  font-size: 10.5px;
  letter-spacing: .08em;
  text-transform: uppercase;
}
.blueprint-head .title {
  color: var(--accent-cyan);
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 10px;
}
.blueprint-head .scale {
  color: var(--text-muted);
}
.blueprint-body {
  padding: 20px 16px 16px;
  overflow-x: auto;
  position: relative;
}
.blueprint-body svg {
  display: block;
  width: 100%;
  height: auto;
  min-width: 680px;
}
.blueprint-cap {
  padding: 10px 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
  background: #090c13;
  font-size: 12px;
  color: var(--text-muted);
  line-height: 1.5;
}
.blueprint-cap b {
  color: var(--text-primary);
  font-family: var(--mono);
  font-size: 10px;
  text-transform: uppercase;
  margin-right: 6px;
}

/* ── Cross-reference list ───────────────────────────────────────────── */
.xref {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: 4px;
  padding: 16px 20px;
  margin: 20px 0;
}
.xref .t {
  font-family: var(--mono);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: .08em;
  text-transform: uppercase;
  color: var(--accent-cyan);
  margin-bottom: 8px;
}
.xref .items a {
  display: block;
  color: var(--text-primary);
  text-decoration: none;
  font-size: 13.5px;
  margin-bottom: 6px;
}
.xref .items a:hover {
  color: var(--accent-cyan);
  text-decoration: underline;
}

/* ── Timeline items ─────────────────────────────────────────────────── */
.timeline {
  position: relative;
  padding-left: 24px;
  margin: 24px 0;
  border-left: 1px solid var(--border-medium);
}
.tl-item {
  position: relative;
  margin-bottom: 24px;
}
.tl-item::before {
  content: "";
  position: absolute;
  left: -29px;
  top: 4px;
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: var(--accent-cyan);
  box-shadow: 0 0 8px rgba(56, 189, 248, 0.8);
}
.tl-when {
  font-family: var(--mono);
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: .08em;
  color: var(--accent-cyan);
  margin-bottom: 3px;
}
.tl-what {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
}
.tl-note {
  font-size: 13.5px;
  color: var(--text-muted);
  line-height: 1.5;
}

/* ── Tags / Badges ──────────────────────────────────────────────────── */
.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 20px 0;
}
.tags span {
  font-family: var(--mono);
  font-size: 11px;
  padding: 4px 10px;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: 3px;
  color: var(--text-secondary);
}

/* ── Interactive Infographics & Problem/Solution Components ──────────── */
.infographic-box {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: 6px;
  padding: 24px;
  margin: 28px 0;
  position: relative;
  overflow: hidden;
}
.infographic-box::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--accent-blue), var(--accent-cyan), transparent);
}

.synthesis-container {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 16px;
  align-items: center;
  margin: 28px 0;
}
@media (max-width: 900px) {
  .synthesis-container {
    grid-template-columns: 1fr;
    gap: 20px;
  }
}
.synthesis-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: 4px;
  padding: 20px;
}
.synthesis-card.problem {
  border-left: 3px solid var(--accent-red);
}
.synthesis-card.solution {
  border-right: 3px solid var(--accent-cyan);
}
.synthesis-center {
  background: linear-gradient(135deg, rgba(16, 21, 34, 0.9), rgba(10, 14, 23, 0.95));
  border: 1px solid var(--accent-blue);
  border-radius: 6px;
  padding: 22px;
  text-align: center;
  box-shadow: 0 0 25px rgba(10, 132, 255, 0.15);
  min-width: 200px;
}

/* ── Dependency Timeline & Interactive Corpus ───────────────────────── */
.dep-controls {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 20px;
  align-items: center;
}
.dep-btn {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  color: var(--text-muted);
  font-family: var(--mono);
  font-size: 11px;
  padding: 5px 12px;
  border-radius: 3px;
  cursor: pointer;
  transition: all 0.15s ease;
}
.dep-btn:hover {
  background: var(--bg-surface-2);
  color: var(--text-primary);
  border-color: var(--border-medium);
}
.dep-btn.active {
  background: rgba(56, 189, 248, 0.12);
  color: var(--accent-cyan);
  border-color: var(--accent-cyan);
  font-weight: 600;
}

.dep-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 14px;
  max-height: 600px;
  overflow-y: auto;
  padding-right: 6px;
}
.dep-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: 4px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.18s ease;
  position: relative;
}
.dep-card:hover {
  border-color: var(--accent-cyan);
  background: var(--bg-surface-2);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
}
.dep-card-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  font-family: var(--mono);
  font-size: 10px;
}
.dep-badge {
  padding: 2px 6px;
  border-radius: 2px;
  font-weight: 600;
  text-transform: uppercase;
}
.dep-badge.sev-5 {
  background: rgba(239, 68, 68, 0.15);
  color: #f87171;
  border: 1px solid rgba(239, 68, 68, 0.4);
}
.dep-badge.sev-4 {
  background: rgba(245, 158, 11, 0.15);
  color: #fbbf24;
  border: 1px solid rgba(245, 158, 11, 0.4);
}
.dep-badge.sev-3 {
  background: rgba(56, 189, 248, 0.15);
  color: #38bdf8;
  border: 1px solid rgba(56, 189, 248, 0.4);
}

.dep-modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(8px);
  display: none;
  place-items: center;
  z-index: 1000;
  padding: 20px;
}
.dep-modal {
  background: #0c101a;
  border: 1px solid var(--accent-cyan);
  box-shadow: 0 0 40px rgba(56, 189, 248, 0.2);
  border-radius: 6px;
  max-width: 650px;
  width: 100%;
  max-height: 85vh;
  overflow-y: auto;
  padding: 28px;
  position: relative;
}
.dep-modal-close {
  position: absolute;
  top: 18px;
  right: 18px;
  background: none;
  border: none;
  color: var(--text-muted);
  font-size: 20px;
  cursor: pointer;
  padding: 4px 8px;
}
.dep-modal-close:hover {
  color: var(--text-primary);
}

/* ── Footer ─────────────────────────────────────────────────────────── */
footer {
  border-top: 1px solid var(--border-subtle);
  padding: 32px 0 60px;
  margin-top: 60px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
  font-family: var(--mono);
  font-size: 11px;
  color: var(--text-muted);
}
footer a {
  color: var(--text-muted);
  text-decoration: none;
}
footer a:hover {
  color: var(--accent-cyan);
}
@media (max-width: 640px) {
  footer {
    flex-direction: column;
    align-items: flex-start;
  }
}
"""

with open('/home/soham-kumar/soham/apollyon/deck/wiki/css/wiki.css', 'w') as f:
    f.write(css_content)

print("Revamped wiki.css written successfully.")
