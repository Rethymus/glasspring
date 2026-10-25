#!/usr/bin/env python3
"""slop_scan.py — anti-slop static scanner for the glasspring skill.

Scans HTML/CSS/MD for the AI-slop tells listed in SKILL.md §3. Some calibration
ideas were informed by anthropics/skills frontend-design; see the repository's
third-party notice for source and license review status. Findings are warnings with suggested
alternatives — a finding is a prompt to reconsider, not always a defect.

Severity:
  hard  — exact documented tells; exit 1 (CI gate)
  warn  — strong patterns; fix or justify in design-notes
  info  — statistical hints (counts, combos)

Usage:
  python slop_scan.py --selftest
  python slop_scan.py preview.html
  python slop_scan.py src/            # scans *.html, *.css, *.htm
  python slop_scan.py preview.html --min-severity warn   # report warn+, exit on hard only
"""
from __future__ import annotations
import argparse, os, re, sys
from collections import Counter

HARD, WARN, INFO = "hard", "warn", "info"
SEV_ORDER = {INFO: 0, WARN: 1, HARD: 2}

# ---------- rule table ----------
# (rule_id, severity, compiled regex or callable, hint)
HEX_RULES = [
    ("cream_hex", HARD, r"#f4f1ea\b",
     "Claude-tell cream background. Pick a surface from the brand's own OKLCH ramp instead."),
    ("terracotta_hex", HARD, r"#d97757\b",
     "Terracotta accent (official calibration tell). Derive an accent from the brand seed."),
    ("rich_black_hex", HARD, r"#0b0b0b\b",
     "Documented slop black. Use a tinted dark surface (e.g. oklch 0.14-0.20 with brand hue, chroma <=0.03)."),
    ("neon_lime_hex", WARN, r"#(a3e635|84cc16|39ff14|00ff41|ccff00)\b",
     "Acid/neon green — on dark this is the 'dark + acid green' tell. If it's the brand, verify contrast and note it."),
]

def _purple_gradient(text: str):
    grad = re.findall(r"linear-gradient\([^)]*\)", text, re.I)
    purple = re.compile(r"#(7c3aed|8b5cf6|a855f7|6d28d9|9333ea|7e22ce)|\b(purple|violet)\b", re.I)
    hits = [g for g in grad if len(set(purple.findall(g))) >= 2]
    return len(hits)

def _middle_dot(text: str):
    n = 0
    for line in text.splitlines():
        if line.count(" · ") >= 2:
            # 期刊/仪器编号语法（含数字、§、№、Vol.、No.）是家族正典，不是 slop 标语
            if re.search(r"(?i)(\d|§|№|\bvol\.|\bno\.\s*\d)", line):
                continue
            n += 1
    return n

def _strip_comments(text: str) -> str:
    """Comments are not shipped UI — strip CSS/HTML comments before scanning."""
    text = re.sub(r"/\*.*?\*/", " ", text, flags=re.S)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    return text

def _em_dash(text: str):
    # The tell is LABEL chrome ("Essays — long form" lists), not prose em-dashes.
    # Count only short, label-like lines; prose lines are long and exempt.
    return sum(1 for line in text.splitlines()
               if len(line.strip()) <= 60 and re.search(r"\w — \w", line))

def _uniform_radius(text: str):
    c = Counter(m.lower() for m in re.findall(r"border-radius\s*:\s*(\d+)px", text))
    return {k: v for k, v in c.items() if v >= 6}

def _uniform_shadow(text: str):
    n = len(re.findall(r"rgba?\(\s*0\s*,\s*0\s*,\s*0\s*,\s*0\.1\s*\)", text))
    n += len(re.findall(r"rgb\(\s*0\s+0\s+0\s*/\s*0\.1\s*\)", text))
    return n

RULES = [
    ("purple_gradient", WARN, _purple_gradient,
     "Purple gradient hero (two+ purple stops) — the default AI hero. Use the brand ramp, or no gradient at all."),
    ("middle_dot_meta", HARD, _middle_dot,
     "Middle-dot meta strings ('Design · Systems · Journal'). Replace with real hierarchy."),
    ("em_dash_labels", WARN, _em_dash,
     "Repeated 'word — word' em-dash label pairs. Use real labels or punctuation."),
    ("arrow_link", WARN, lambda t: len(re.findall(r"→\s*</a>|(?<!hidden=\"true\")>\s*→", t)),
     "Decorative '→' glued to links (slop chrome). Let labels carry meaning. (aria-hidden arrow spans exempt)"),
    ("space_grotesk", WARN, lambda t: len(re.findall(r"(?i)space grotesk", t)),
     "Space Grotesk has become the 'distinctive font' tell. Choose from the project's voice, not the default-alt list."),
    ("inter_as_identity", WARN, lambda t: len(re.findall(r"(?im)font-family\s*:\s*[\"']?Inter[\"']?\s*[,;]", t)),
     "Inter as the first font = default identity. Keep Inter only as fallback after system-ui (licensing-safe stack)."),
    ("fade_up_stagger", WARN,
     lambda t: (1 if re.search(r"(?im)animation\s*:[^;]*fade", t)
                and (re.search(r"(?i)animation-delay\s*:[^;]*(var\(--|calc\()", t)
                     or re.search(r":nth-child\(", t)) else 0),
     "Per-card fade-up with stagger — documented motion slop. Motion budget: one orchestrated moment."),
    ("uniform_radius", WARN, _uniform_radius,
     "One literal border-radius value used 6+ times — the uniform-radius slop. Use radius tokens with 2-3 steps (var() tokens don't count)."),
    ("uniform_shadow", WARN, _uniform_shadow,
     "rgba(0,0,0,.1) shadow repeated 3+ times — single-shadow-kit slop. Define one elevation family token and reference it."),
    ("uppercase_eyebrow", INFO, lambda t: len(re.findall(r"(?i)text-transform\s*:\s*uppercase[^}]*letter-spacing\s*:\s*0\.[2-9]", t))
                                    + len(re.findall(r"(?i)letter-spacing\s*:\s*0\.[2-9][^}]*text-transform\s*:\s*uppercase", t)),
     "Wide-tracked ALL-CAPS eyebrow — official typography tell. Consider sentence-case labels."),
    # v2 additions
    ("emoji_icon_system", WARN, lambda t: len(re.findall(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]", t)),
     "Emoji used as UI icons (📚 ⚙ 📖...) — screenshot-fragile, platform-inconsistent, screen-reader-hostile. Use SVG icons."),
    ("glass_on_trust", HARD,
     lambda t: sum(1 for m in re.finditer(r"(?i)(?<![\w-])(backdrop-filter)\s*:", t)
                   if re.search(r"(?i)\b(price|amount|total|balance|severity|code|log)\b|图表|data-table",
                                t[max(0, m.start()-200):m.end()+200])),
     "Glass/blur on trust zones (prices/data/code) — domain pack red line. Trust zones must be opaque."),
    ("color_only_status", WARN,
     lambda t: sum(1 for m in re.finditer(r"(?i)\b(status|state|severity|priority)[\w-]*\s*[{:][^;}]{0,120}", t)
                   if re.search(r"(?i)(?<![\w-])(color|background)\s*:|(?<![\w-])bg\s*:", m.group(0))
                   and not re.search(r"(?i)(icon|text|label|badge|arrow|prefix|content|::before|::after)",
                                     t[max(0, m.start()-200):m.end()+200])),
     "Status indicated by color alone — WCAG 1.4.1. Add text label, icon, or shape."),
    ("gradient_area_large", WARN,
     lambda t: (len(re.findall(r"(?i)linear-gradient\([^)]*(?:100vh|100vw)[^)]*\)", t))
                + len(re.findall(r"(?is)(?:min-height|height)\s*:\s*100v[hw][^}]*linear-gradient", t))
                + len(re.findall(r"(?is)linear-gradient[^;}]*[;}][^}]*(?:min-height|height)\s*:\s*100v[hw]", t))),
     "Full-viewport gradient hero (gradient sized to 100vh/100vw) — the default AI hero at scale. Use brand ramp, no gradient, or scroll-bound partial gradient."),
    ("glass_text_readability", HARD,
     lambda t: sum(1 for m in re.finditer(r"(?i)(?<![\w-])(backdrop-filter)\s*:", t)
                   if not (re.search(r"(?i)(nav|header|toolbar|menubar|topbar|app-?bar|sidebar|banner|hud)\b",
                                     t[max(0, m.start()-300):m.start()])
                           or re.search(r"(?i)(nav|header|toolbar|menubar|topbar|app-?bar|sidebar|banner|hud)\b",
                                        t[m.end():m.end()+150]))
                   and re.search(r"(?i)(font-size|<p[ >]|<article|prose|body-text|paragraph|reading)",
                                 t[m.end():m.end()+200])),
     "Glass/blur under body text or prose — readability killer. Trust zones and reading areas must be opaque. (nav exemption window: 300ch lookbehind + 150ch lookahead — real nav blocks carry property clusters, and @supports conditions name their selector AFTER the query; covered by a regression fixture)"),
    # v3 batch: seven mechanically testable rules.
    ("decorative_numbering", WARN,
     lambda t: (lambda hits: len(hits) if len(hits) >= 2 else 0)(
         [m.group(0) for m in re.finditer(r">\s*0[1-9][)\].]?\s*<|[\"'`]\s*0[1-9]\s*[\"'`]|>\s*(?:Step|Phase|No\.?|Chapter)\s*0?\d\s*<", t, re.I)
         if not re.search(r"(?:19|20)\d\d", m.group(0))]),
     "Decorative index numbering (01 / 02 / 03, two or more) — numbering must be data (a rank, a sequence). types/product.md §4c."),
    ("generic_cta", WARN,
     lambda t: len(re.findall(r">\s*(?:learn more|get started|click here|read more|discover more|submit)\s*<", t, re.I)),
     "Generic button label (Learn more / Get started / Submit) — name the action or the thing ('Book a table', 'See the plans')."),
    ("generic_hero_words", WARN,
     lambda t: len(re.findall(r">\s*(?:unleash|elevate|supercharge|empower|revolutioniz|game.chang|seamless(?:ly)?|take.{0,12}to the next level)\b", t, re.I)),
     "Generic AI-hero vocabulary leading a headline ('Unleash/Elevate/Seamless…') — say what the thing does, in the subject's own words."),
    ("transition_all", WARN,
     lambda t: len(re.findall(r"transition\s*:\s*all\b|\btransition-all\b", t, re.I)),
     "transition: all — name the properties (transform, opacity); layout props must never ride along."),
    ("scale_zero", WARN,
     lambda t: len(re.findall(r"scale\(\s*0\s*\)|\bscale-0\b", t)),
     "Entering from scale(0) — start at 0.92-0.98 with opacity 0 (motion.md §4a)."),
    ("organic_blob", WARN,
     lambda t: len(re.findall(r"border-radius\s*:\s*(?:\d{1,3}%\s+){1,3}\d{1,3}%", t)),
     "Organic blob shape (multi-percentage border-radius) — the AI-gradient-companion tell. Ambient depth belongs to ultra-low-opacity fixed layers (<0.05, minimalist-ui 仲裁), not visible morphing shapes."),
    ("h_screen", WARN,
     lambda t: len(re.findall(r"\bh-screen\b|height\s*:\s*100vh\b|min-height\s*:\s*100vh\b", t, re.I)),
     "100vh jumps on mobile (address-bar crop) — use 100svh/100dvh (platforms/web.md §3). Desktop-only sheets: state it."),
    ("lorem_placeholder", HARD,
     lambda t: len(re.findall(r"lorem ipsum|dolor sit amet", t, re.I)),
     "Placeholder copy shipped (type.md §5a content-is-not-design). Real content or honest samples listed in the report."),
    ("placeholder_names", WARN,
     lambda t: len(re.findall(r"\b(?:John Doe|Jane Doe|John Smith|Foo Bar)\b|foo@bar\.com|test@test\.com|example@example\.com", t)),
     "Placeholder name/email shipped (agentskillshub 'nothing invented' page check 2026-10-24) — write real, brief-appropriate copy."),
    ("console_log_leak", WARN,
     lambda t: len(re.findall(r"\bconsole\.(?:log|debug|info)\s*\(", t)),
     "Debug console output shipped to the page (ux-skill console-log-leak 2026-10-24) — strip debug logs from deliverables."),
    ("bounce_loop", WARN,
     lambda t: len(re.findall(r"\banimate-(?:bounce|ping|pulse)\b|animation\s*:[^;]*\b(?:bounce|ping|pulse)\b", t, re.I)),
     "Looping attention animation (bounce/ping/pulse dot) — loops need an off switch and a reason (motion.md §6a)."),
    ("z_index_magic", WARN,
     lambda t: [m.group(1) for m in re.finditer(r"(?i)z-index\s*:\s*(\d{3,})", t) if int(m.group(1)) >= 999],
     "Magic z-index (999/9999 'top of everything') — replace with the semantic stack scale (--z-dropdown < --z-sticky < --z-drawer < --z-modal < --z-toast; types/product.md §4c)."),
]

def scan_text(text: str):
    """Yield (severity, rule, count/detail, hint). Only non-zero findings."""
    text = _strip_comments(text)
    for rid, sev, pattern, hint in HEX_RULES:
        n = len(re.findall(pattern, text, re.I))
        if n:
            yield sev, rid, n, hint
    for rid, sev, fn, hint in RULES:
        try:
            detail = fn(text)
        except Exception as e:  # a broken rule must not kill the scan
            yield INFO, f"{rid}_error", str(e), "rule raised; fix slop_scan.py"
            continue
        if detail:
            yield sev, rid, detail, hint

def scan_path(path: str):
    if os.path.isfile(path):
        files = [path]
    else:
        files = [os.path.join(root, f) for root, _, fs in os.walk(path) for f in fs
                 if f.lower().endswith((".html", ".htm", ".css"))]
    findings = []
    for f in files:
        try:
            text = open(f, encoding="utf-8", errors="ignore").read()
        except OSError as e:
            findings.append((HARD, "unreadable", f, str(e)))
            continue
        for sev, rid, detail, hint in scan_text(text):
            loc = _line_numbers(text, rid)
            where = f"L{','.join(map(str, loc[:5]))}" + ("…" if len(loc) > 5 else "") if loc else str(detail)
            findings.append((sev, rid, f"{f}:{where}", hint))
    return findings

# 单行可判规则的行定位提示（gogh 引述 Vercel 审计层 "file:line findings" 机制，2026-10-20）。
# 命中即报行号让修复直接跳行；聚合规则（跨行/需上下文窗）不在表内，保持计数格式。语义与 scan_text 一致。
LINE_HINTS = {
    "cream_hex": lambda ln: re.search(r"#f4f1ea\b", ln, re.I),
    "terracotta_hex": lambda ln: re.search(r"#d97757\b", ln, re.I),
    "rich_black_hex": lambda ln: re.search(r"#0b0b0b\b", ln, re.I),
    "neon_lime_hex": lambda ln: re.search(r"#(a3e635|84cc16|39ff14|00ff41|ccff00)\b", ln, re.I),
    "purple_gradient": lambda ln: any(len(set(re.findall(r"#(7c3aed|8b5cf6|a855f7|6d28d9|9333ea|7e22ce)|(?:\bpurple\b|\bviolet\b)", g, re.I))) >= 2
                                       for g in re.findall(r"linear-gradient\([^)]*\)", ln, re.I)),
    "middle_dot_meta": lambda ln: ln.count(" · ") >= 2 and not re.search(r"(?i)(\d|§|№|\bvol\.|\bno\.\s*\d)", ln),
    "em_dash_labels": lambda ln: len(ln.strip()) <= 60 and re.search(r"\w — \w", ln),
    "arrow_link": lambda ln: re.search(r"→\s*</a>|(?<!hidden=\"true\")>\s*→", ln),
    "space_grotesk": lambda ln: re.search(r"(?i)space grotesk", ln),
    "inter_as_identity": lambda ln: re.search(r"font-family\s*:\s*[\"']?Inter[\"']?\s*[,;]", ln, re.I),
    "uppercase_eyebrow": lambda ln: re.search(r"text-transform\s*:\s*uppercase[^}]*letter-spacing\s*:\s*0\.[2-9]", ln, re.I)
                                     or re.search(r"letter-spacing\s*:\s*0\.[2-9][^}]*text-transform\s*:\s*uppercase", ln, re.I),
    "emoji_icon_system": lambda ln: re.search(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]", ln),
    "z_index_magic": lambda ln: any(int(m.group(1)) >= 999 for m in re.finditer(r"z-index\s*:\s*(\d{3,})", ln, re.I)),
}

def _line_numbers(text: str, rid: str):
    """Return 1-based line numbers hitting the rule, or None (aggregate rule / no line found)."""
    hint = LINE_HINTS.get(rid)
    if hint is None:
        return None
    hits = [i for i, ln in enumerate(text.splitlines(), 1) if hint(ln)]
    return hits or None

# ---------- selftest ----------
SLOP_SAMPLES = [  # (expected_rule, sample)
    ("cream_hex", "body { background: #F4F1EA; }"),
    ("terracotta_hex", "a { color: #D97757; }"),
    ("rich_black_hex", "html { background-color:#0B0B0B; }"),
    ("neon_lime_hex", ".glow { color: #a3e635; }"),
    ("purple_gradient", ".hero { background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%); }"),
    ("middle_dot_meta", "<p>Design · Systems · Journal</p>"),
    ("em_dash_labels", "<li>Essays — long form</li>\n<li>Notes — short form</li>"),
    ("arrow_link", '<a class="link" href="/x">Read the essay →</a>'),
    ("space_grotesk", 'h1 { font-family: "Space Grotesk", sans-serif; }'),
    ("inter_as_identity", "body { font-family: Inter, sans-serif; }"),
    ("fade_up_stagger", "@keyframes fadeUp{from{opacity:0}}.card{animation:fadeUp .6s ease;animation-delay:calc(var(--i)*80ms)}"),
    ("uniform_radius", ".a{border-radius:16px}.b{border-radius:16px}.c{border-radius:16px}.d{border-radius:16px}"
                       ".e{border-radius:16px}.f{border-radius:16px}.g{border-radius:16px}"),
    ("uniform_shadow", ".a{box-shadow:0 4px 12px rgba(0, 0, 0, 0.1)}.b{box-shadow:0 4px 12px rgba(0, 0, 0, 0.1)}"
                       ".c{box-shadow:0 4px 12px rgba(0, 0, 0, 0.1)}"),
    ("uppercase_eyebrow", ".eyebrow{text-transform:uppercase;letter-spacing:0.25em}"),
    # v2 rules — each new rule must have a regression fixture.
    ("emoji_icon_system", "<button>📚 Library</button><button>⚙ Settings</button>"),
    ("glass_on_trust", '<table class="data-table"><td class="total">¥128.00</td></table>'
                       '<div style="backdrop-filter: blur(12px)"></div>'),
    ("color_only_status", '.status{color:var(--red)}'),
    ("gradient_area_large", ".hero{min-height:100vh;background:linear-gradient(180deg,#0f172a,#1e293b)}"),
    ("glass_text_readability", '<section class="panel" style="backdrop-filter: blur(20px)"></section>'
                               "<article><p>Body text sitting on glass.</p></article>"),
    ("z_index_magic", ".modal{z-index:9999}"),
    ("z_index_magic", '<div class="toast" style="z-index: 999">Saved</div>'),
    # v3 batch anchor — each rule has a regression fixture.
    ("decorative_numbering", '<section><h3>Features</h3><span>01</span><p>Fast</p><span>02</span><p>Light</p><span>03</span><p>Small</p></section>'),
    ("generic_cta", '<a class="btn" href="/x">Learn more</a>'),
    ("generic_hero_words", "<h1>Unleash your potential</h1>"),
    ("transition_all", ".card { transition: all 300ms ease; }"),
    ("scale_zero", ".modal { transform: scale(0); opacity: 0; }"),
    ("organic_blob", ".blob { border-radius: 58% 42% 55% 45% / 52% 48% 60% 40%; }"),
    ("h_screen", ".hero { height: 100vh; }"),
    ("lorem_placeholder", "<p>Lorem ipsum dolor sit amet</p>"),
    ("bounce_loop", '<div class="dot animate-pulse"></div>'),
]

CLEAN_SAMPLES = [  # must produce zero hard/warn findings
    ":root{--surface:#171a21;--accent:#4f8cff}.btn{border-radius:12px;transition:transform 200ms var(--ease-out)}",
    "<p>阅读设计 · 第 1 期</p>",  # single middle dot: fine
    ".a{border-radius:16px}.b{border-radius:16px}",  # below threshold
    'body{font-family:system-ui,-apple-system,"Segoe UI",Inter,sans-serif}',  # Inter as fallback only
    "h2{color:#8b5cf6}",  # single purple hex, not a gradient
    "<p>Backdrop stripes simulate worst-case bright content scrolling under glass — a teaching case for contrast floors.</p>",  # prose em-dash, long line: exempt
    "<!-- background: #F4F1EA -->",  # commented-out slop is not shipped slop
    # v2 false-positive guards
    '<nav class="site-nav" style="backdrop-filter: blur(20px)"><a>选集</a></nav><p>正文</p>',  # control-layer glass: exempt
    "<style>.nav{position:fixed;display:flex;justify-content:space-between;align-items:center;"
    "padding:0.8rem clamp(1.25rem, 4vw, 3rem);background:var(--tint);"
    "backdrop-filter:blur(20px) saturate(150%)}</style><p>正文</p>",  # long-property navigation cluster regression fixture
    '<span class="status-badge" style="background:var(--red)">已售罄</span>',  # badge = shape+text dual encoding
    "linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.6) 100%)",  # 100% is a stop position, not viewport size
    '.status-dot{background:var(--c-warn)}<span class="status-label">Live</span>',  # aria-dot + text sibling = dual encoding
    ".status-pill:hover { border-color: var(--color-border-strong); }",  # hover affordance, not status encoding
    "<p>VOL. II · §1 · ANNO MMXXVI</p>",  # numbered colophon = genre grammar, not slop tagline
    ".drawer{z-index:40}.toast{z-index:var(--z-toast)}",  # small tiered scale + semantic token: legitimate
    ".cta { transition: transform 200ms var(--ease-out), opacity 200ms; }",  # named properties: fine
    "<button>Book a table</button><span>Rank 1</span>",  # real CTA + single rank numeral as data: fine
    ".modal { transform: scale(0.96); opacity: 0; }",  # enters from 0.96 (motion.md §4a)
    ".hero { height: 100dvh; }",  # dynamic viewport unit
    "<p>六 stalks of wheat, cut at dawn</p>",  # real copy
    ".dot { animation: none; }",  # no loop
]

def selftest() -> int:
    fails = []
    print("selftest: slop samples must HIT their rule (any severity)")
    for expected, sample in SLOP_SAMPLES:
        hits = [(sev, rid) for sev, rid, _, _ in scan_text(sample)]
        rules = {rid for _, rid in hits}
        ok = expected in rules
        print(f"  [{'PASS' if ok else 'FAIL'}] {expected}: hit={hits}")
        if not ok:
            fails.append(expected)
    print("selftest: clean samples must produce NO hard/warn findings")
    for i, sample in enumerate(CLEAN_SAMPLES):
        found = [(sev, rid) for sev, rid, _, _ in scan_text(sample) if sev in (HARD, WARN)]
        ok = not found
        print(f"  [{'PASS' if ok else 'FAIL'}] clean#{i}: {found if found else 'no findings'}")
        if not ok:
            fails.append(f"clean#{i}")
    print("selftest: line-number locating (single-line rules report L<n>, aggregates keep counts)")
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        probe = os.path.join(td, "probe.html")
        open(probe, "w", encoding="utf-8").write(
            "<!DOCTYPE html>\n<html><head><style>\n"
            ".a{border-radius:16px}.b{border-radius:16px}.c{border-radius:16px}"  # radius ×3: below threshold
            "\nbody { background: #F4F1EA; }\n"                                     # line 4: cream_hex → expect L4
            ".m{z-index:9999}\n"                                                     # line 5: z_index_magic → expect L5
            "</style></head><body><p>Design · Systems · Journal · More</p></body></html>\n")  # line 7: middle_dot_meta → expect L7
        located = scan_path(probe)
        got = {rid: where for _, rid, where, _ in located}
        for rid, want in (("cream_hex", "L4"), ("z_index_magic", "L5"), ("middle_dot_meta", "L6")):
            ok = rid in got and want in got[rid]
            print(f"  [{'PASS' if ok else 'FAIL'}] locate {rid}: {got.get(rid)}")
            if not ok:
                fails.append(f"locate-{rid}")
    if fails:
        print(f"SELFTEST FAILED: {fails}")
        return 1
    print("SELFTEST PASSED (all anchors green)")
    return 0

def main() -> int:
    ap = argparse.ArgumentParser(description="glasspring anti-slop scanner")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("path", nargs="?", help="file or directory (*.html/*.htm/*.css)")
    ap.add_argument("--min-severity", choices=[INFO, WARN, HARD], default=INFO)
    a = ap.parse_args()

    if a.selftest:
        return selftest()
    if not a.path:
        ap.error("give a file/directory or --selftest")

    findings = scan_path(a.path)
    findings.sort(key=lambda x: -SEV_ORDER[x[0]])
    shown = [f for f in findings if SEV_ORDER[f[0]] >= SEV_ORDER[a.min_severity]]
    if not shown:
        print(f"no findings at >= {a.min_severity} in {a.path}")
    for sev, rid, where, hint in shown:
        print(f"[{sev.upper():4}] {rid}: {where}\n       -> {hint}")
    hard = [f for f in shown if f[0] == HARD]
    print(f"summary: {len(hard)} hard, "
          f"{sum(1 for f in shown if f[0]==WARN)} warn, "
          f"{sum(1 for f in shown if f[0]==INFO)} info")
    return 1 if hard else 0

if __name__ == "__main__":
    sys.exit(main())
