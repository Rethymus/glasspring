#!/usr/bin/env python3
"""verify_output.py — mechanical output-contract checker for glasspring runs.

Why: prompt instructions alone do not prove that an output meets its contract.
This script turns the output
CONTRACT (not the design judgment) into machine-checkable clauses, rea
mcp-contracts style: every clause reports PASS / FAIL / UNKNOWN, and any
FAIL exits 1. UNKNOWN means incomplete evidence and exits 2.
File structure and declarations never prove visual quality or measurement execution.

Clauses (SKILL.md output contract):
  1. tokens.css exists, header declares seed + measured-contrast provenance
  2. preview.html exists and consumes tokens (var( references present)
  3. design-notes.md exists with §0-§8 sections present and in order
  4. shots/ contains >= 2 viewport PNG captures
  5. no stray temp artifacts (http.server logs, probe scratch files)

Usage:  python verify_output.py <run-directory>   |   --selftest
"""
from __future__ import annotations
import glob
import os
import re
import sys
from visual_diff import decode_png

PASS, FAIL, UNKNOWN = "PASS", "FAIL", "UNKNOWN"
NOTES_SECTIONS = ["§0", "§1", "§2", "§3", "§4", "§5", "§6", "§7", "§8"]


def clause(name: str, status: str, detail: str) -> tuple[str, str, str]:
    return name, status, detail


def check_run(directory: str) -> list[tuple[str, str, str]]:
    out: list[tuple[str, str, str]] = []
    directory = os.path.abspath(directory)
    if not os.path.isdir(directory):
        return [clause("run-directory", FAIL, f"not a directory: {directory}")]

    # 1. tokens deliverable + provenance header. In a shadcn bridge project
    #    (components.json present — run root or fixture/) the deliverable form
    #    is theme-additions.css (shadcn-tailwind.md §1), not a parallel
    #    tokens.css — tool gap closed here.
    has_bridge = (os.path.isfile(os.path.join(directory, "components.json"))
                  or os.path.isfile(os.path.join(directory, "fixture", "components.json")))
    tokens = os.path.join(directory, "tokens.css")
    bridge_form = False
    if has_bridge and os.path.isfile(os.path.join(directory, "theme-additions.css")):
        tokens = os.path.join(directory, "theme-additions.css")
        bridge_form = True
    if not os.path.isfile(tokens):
        out.append(clause("tokens-first", FAIL,
                          "tokens.css missing" + (" (bridge project: also no theme-additions.css)" if has_bridge else "")))
    else:
        head = open(tokens, encoding="utf-8", errors="ignore").read(3000).lower()
        missing = []
        if not re.search(r"seed|种子", head):
            missing.append("seed/种子")
        if not re.search(r"contrast|对比|实测", head):
            missing.append("contrast/实测")
        if missing:
            out.append(clause("tokens-provenance", FAIL,
                              f"header lacks {missing} provenance marker(s)"))
        else:
            out.append(clause("tokens-provenance", PASS, "header contains provenance markers; measurement execution not verified"
                             + (" (bridge form: theme-additions.css)" if bridge_form else "")))

    # 2. entry page(s) consume tokens — preview.html OR a multi-page site
    #    (the contract hard-required a
    #    single preview.html, which made 3-page deliverables unverifiable even
    #    though the multi-page-consistency clause below already supported them)
    preview = os.path.join(directory, "preview.html")
    pages = []
    if os.path.isfile(preview):
        pages = [preview]
    else:
        pages = sorted(p for p in glob.glob(os.path.join(directory, "*.html")))
    if not pages:
        out.append(clause("preview-exists", FAIL, "no preview.html and no *.html pages"))
    else:
        if len(pages) == 1 and pages[0].endswith("preview.html"):
            out.append(clause("preview-exists", PASS, "preview.html present"))
        else:
            out.append(clause("preview-exists", PASS,
                              f"multi-page deliverable: {len(pages)} pages ({', '.join(os.path.basename(p) for p in pages)})"))
        total_var = sum(len(re.findall(r"var\(--", open(p, encoding="utf-8", errors="ignore").read())) for p in pages)
        min_var = min(len(re.findall(r"var\(--", open(p, encoding="utf-8", errors="ignore").read())) for p in pages)
        if total_var >= 10 and min_var >= 3:
            out.append(clause("token-consumption", PASS,
                              f"{total_var} var(--) references across {len(pages)} page(s) (min per page {min_var})"))
        elif total_var == 0:
            out.append(clause("token-consumption", FAIL, "no var(--) references — tokens may not drive the pages"))
        else:
            out.append(clause("token-consumption", UNKNOWN,
                              f"thin token use: total {total_var}, min per page {min_var}"))

    # 3. design-notes §0-§8 as headings, in order (cross-references mid-line
    #    like "product.md §4" must not count — heading shape only)
    notes = os.path.join(directory, "design-notes.md")
    if not os.path.isfile(notes):
        out.append(clause("design-notes", FAIL, "design-notes.md missing"))
    else:
        text = open(notes, encoding="utf-8", errors="ignore").read()
        pos, ordered, absent = -1, True, []
        for i in range(9):
            m = re.search(rf"^\s*#{{1,6}}\s*§?\s*{i}(?!\d)", text, re.M)
            if not m:
                absent.append(f"§{i}")
            elif m.start() < pos:
                ordered = False
            else:
                pos = m.start()
        if absent:
            out.append(clause("notes-sections", FAIL, f"missing section headings: {', '.join(absent)}"))
        elif not ordered:
            out.append(clause("notes-sections", FAIL, "§0-§8 headings present but out of order"))
        else:
            out.append(clause("notes-sections", PASS, "§0-§8 headings present and ordered"))

    # 4. shots coverage
    shots = os.path.join(directory, "shots")
    pngs = []
    if os.path.isdir(shots):
        for root, _, fs in os.walk(shots):
            pngs += [os.path.join(root, f) for f in fs if f.lower().endswith(".png")]
    import struct, zlib
    sizes, invalid = [], []
    for path in pngs:
        try:
            w, h, _, _ = decode_png(path)
            sizes.append((w, h))
        except (ValueError, KeyError, IndexError, OSError, struct.error, zlib.error):
            invalid.append(os.path.basename(path))
    mobile = any(320 <= w <= 600 and h >= 400 for w, h in sizes)
    desktop = any(w >= 1000 and h >= 600 for w, h in sizes)
    if invalid:
        out.append(clause("shots-coverage", FAIL, f"invalid PNG(s): {invalid}"))
    elif mobile and desktop:
        out.append(clause("shots-coverage", PASS, f"decoded narrow + desktop PNGs: {sizes}; freshness and identity require review"))
    else:
        out.append(clause("shots-coverage", FAIL, f"need narrow (320-600px) + desktop (>=1000px) PNGs, got {sizes}"))

    # 5. stray temp artifacts (scope hygiene)
    strays = [f for f in os.listdir(directory)
              if re.fullmatch(r"(server\.log|nohup\.out|_dbg.*|.*\.tmp)", f, re.I)]
    if strays:
        out.append(clause("scope-hygiene", FAIL, f"stray artifacts: {', '.join(strays)}"))
    else:
        out.append(clause("scope-hygiene", PASS, "no stray temp artifacts"))

    # 6. multi-page consistency (AD3-adjacent: token drift check across HTML files)
    html_files = [f for f in os.listdir(directory) if f.lower().endswith(".html") and f != "preview.html"]
    if html_files:
        token_sets = {}
        for hf in html_files:
            html_path = os.path.join(directory, hf)
            content = open(html_path, encoding="utf-8", errors="ignore").read()
            # extract CSS custom property names
            vars_used = set(re.findall(r"--[\w-]+(?=\s*:)", content))
            token_sets[hf] = vars_used
        all_files = [hf for hf in html_files] + (["preview.html"] if os.path.exists(os.path.join(directory, "preview.html")) else [])
        if len(all_files) >= 2:
            main_vars = set(re.findall(r"--[\w-]+(?=\s*:)", open(os.path.join(directory, "preview.html"), encoding="utf-8", errors="ignore").read())) if os.path.exists(os.path.join(directory, "preview.html")) else set()
            drift = []
            for hf in all_files:
                hp = os.path.join(directory, hf)
                hv = set(re.findall(r"--[\w-]+(?=\s*:)", open(hp, encoding="utf-8", errors="ignore").read()))
                if main_vars and hv != main_vars:
                    diff = hv.symmetric_difference(main_vars)
                    if diff:
                        drift.append(f"{hf}: {sorted(diff)[:3]}")
            if drift:
                out.append(clause("multi-page-consistency", FAIL,
                                  f"token drift across pages: {'; '.join(drift)}"))
            else:
                out.append(clause("multi-page-consistency", PASS, "token sets aligned across pages"))
        else:
            out.append(clause("multi-page-consistency", PASS, "single-page deliverable"))
    return out


def _build_fixture(root: str):
    """Good/bad fixture for selftest (created under caller-supplied temp root)."""
    good = os.path.join(root, "good-run")
    os.makedirs(os.path.join(good, "shots"), exist_ok=True)
    open(os.path.join(good, "tokens.css"), "w", encoding="utf-8").write(
        "/* seed: demo brand oklch(0.6 0.14 250) | contrast: measured pairs below */\n"
        ":root{--color-accent:oklch(0.6 0.14 250)}")
    open(os.path.join(good, "preview.html"), "w", encoding="utf-8").write(
        '<!doctype html><meta charset="utf-8"><title>t</title>'
        + '<p style="color:var(--color-accent)">x</p>' * 12)
    open(os.path.join(good, "design-notes.md"), "w", encoding="utf-8").write(
        "\n".join(f"## {s} section" for s in NOTES_SECTIONS))
    import struct, zlib
    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))
    for i, (w, h) in enumerate(((390, 844), (1440, 900))):
        raw = (b'\0' + b'\xff\xff\xff' * w) * h
        data = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0))
        data += chunk(b'IDAT', zlib.compress(raw)) + chunk(b'IEND', b'')
        open(os.path.join(good, "shots", f"shot-{i}.png"), "wb").write(data)

    bad = os.path.join(root, "bad-run")
    os.makedirs(bad, exist_ok=True)
    open(os.path.join(bad, "tokens.css"), "w", encoding="utf-8").write(":root{}")
    open(os.path.join(bad, "preview.html"), "w", encoding="utf-8").write("<p>no tokens</p>")
    open(os.path.join(bad, "design-notes.md"), "w", encoding="utf-8").write("## §3 only")
    open(os.path.join(bad, "server.log"), "w", encoding="utf-8").write("stray")
    return good, bad


def selftest() -> int:
    import tempfile
    fails = []
    with tempfile.TemporaryDirectory() as tmp:
        good, bad = _build_fixture(tmp)
        good_res = {n: s for n, s, _ in check_run(good)}
        for cid in ("tokens-provenance", "token-consumption", "notes-sections", "shots-coverage", "scope-hygiene"):
            ok = good_res.get(cid) == PASS
            print(f"  [{'PASS' if ok else 'FAIL'}] good fixture {cid}==PASS (got {good_res.get(cid)})")
            if not ok:
                fails.append(cid)
        bad_res = {n: s for n, s, _ in check_run(bad)}
        for cid, want in (("tokens-provenance", FAIL), ("token-consumption", FAIL),
                          ("notes-sections", FAIL), ("shots-coverage", FAIL), ("scope-hygiene", FAIL)):
            ok = bad_res.get(cid) == want
            print(f"  [{'PASS' if ok else 'FAIL'}] bad fixture {cid}=={want} (got {bad_res.get(cid)})")
            if not ok:
                fails.append(cid)
        missing = check_run(os.path.join(tmp, "nope"))
        ok = missing[0][1] == FAIL
        print(f"  [{'PASS' if ok else 'FAIL'}] missing directory == FAIL (got {missing[0][1]})")
        if not ok:
            fails.append("missing-directory")
        # bridge-aware clause 1: components.json project
        # delivers theme-additions.css, not a parallel tokens.css
        bridge = os.path.join(tmp, "bridge-run")
        os.makedirs(bridge, exist_ok=True)
        open(os.path.join(bridge, "components.json"), "w", encoding="utf-8").write("{}")
        open(os.path.join(bridge, "theme-additions.css"), "w", encoding="utf-8").write(
            "/* seed: #4F46E5 | contrast: measured via check_contrast --pairs */\n:root{}")
        b_res = {n: (s, d) for n, s, d in check_run(bridge)}
        s1, d1 = b_res.get("tokens-provenance", (None, ""))
        ok = s1 == PASS and "bridge form" in d1
        print(f"  [{'PASS' if ok else 'FAIL'}] bridge fixture: theme-additions.css satisfies clause 1 (got {s1})")
        if not ok:
            fails.append("bridge-clause1")
        os.remove(os.path.join(bridge, "theme-additions.css"))
        b_res2 = {n: (s, d) for n, s, d in check_run(bridge)}
        s2, d2 = b_res2.get("tokens-first", (None, ""))
        ok2 = s2 == FAIL and "theme-additions" in d2
        print(f"  [{'PASS' if ok2 else 'FAIL'}] bridge fixture without deliverable -> FAIL naming theme-additions.css")
        if not ok2:
            fails.append("bridge-missing")
    if fails:
        print(f"SELFTEST FAILED: {fails}")
        return 1
    print("SELFTEST PASSED (all anchors green)")
    return 0


def render_html(directory: str, results: list) -> str:
    """Single-file acceptance report: clause table + embedded
    screenshots + pointers. Shareable as one .html attachment."""
    import base64
    import datetime
    import html as h

    shots = []
    sdir = os.path.join(directory, "shots")
    if os.path.isdir(sdir):
        for root, _, fs in os.walk(sdir):
            for f in sorted(fs):
                if f.lower().endswith(".png"):
                    p = os.path.join(root, f)
                    b64 = base64.b64encode(open(p, "rb").read()).decode()
                    rel = os.path.relpath(p, directory).replace("\\", "/")
                    shots.append((rel, b64))

    def row(name, status, detail):
        color = {"PASS": "#1a7f37", "FAIL": "#c62828", "UNKNOWN": "#b26a00"}[status]
        return (f"<tr><td><code>{h.escape(name)}</code></td>"
                f"<td style='color:{color};font-weight:700'>{status}</td>"
                f"<td>{h.escape(detail)}</td></tr>")

    now = datetime.date.today().isoformat()
    hard = sum(1 for _, s, _ in results if s == FAIL)
    soft = sum(1 for _, s, _ in results if s == UNKNOWN)
    verdict = "ALL GREEN" if hard == 0 else f"{hard} FAILING"
    parts = [f"""<!doctype html><meta charset="utf-8"><title>glasspring acceptance — {h.escape(os.path.basename(directory))}</title>
<body style="font:15px/1.6 system-ui,sans-serif;margin:32px auto;max-width:960px;color:#1c1c1c">
<h1 style="font-size:22px">glasspring acceptance report — <code>{h.escape(os.path.basename(directory))}</code></h1>
<p>generated {now} by verify_output.py · contract v2026-10 (5 clauses) ·
<b style="color:{'#1a7f37' if hard == 0 else '#c62828'}">{verdict}</b>
({len(results) - hard - soft} pass / {hard} fail / {soft} unknown)</p>
<p style="color:#555">UNKNOWN = cannot judge from files alone — gaps are stated, never silent.
Design-judgment gates (glass decision tree, motion semantics, rubric) live in design-notes.md §3/§7/§11 — this report covers the mechanical contract only.</p>
<table style="border-collapse:collapse;width:100%">"""
    ]
    parts.append("".join(row(*r) for r in results))
    parts.append("</table>")
    if shots:
        parts.append("<h2 style='font-size:18px'>captured viewports</h2>")
        for rel, b64 in shots:
            parts.append(f"<figure style='margin:16px 0'><figcaption><code>{h.escape(rel)}</code></figcaption>"
                         f"<img style='max-width:100%;border:1px solid #ddd;border-radius:8px' "
                         f"src='data:image/png;base64,{b64}' alt='{h.escape(rel)}'></figure>")
    parts.append("</body>")
    return "\n".join(parts)


def selftest_html() -> tuple[bool, str]:
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        good, _ = _build_fixture(tmp)
        out_path = os.path.join(tmp, "report.html")
        results = check_run(good)
        open(out_path, "w", encoding="utf-8").write(render_html(good, results))
        doc = open(out_path, encoding="utf-8").read()
        ok = ("ALL GREEN" in doc and "data:image/png;base64," in doc
              and "tokens-provenance" in doc and doc.count("<tr>") >= 5)
        return ok, out_path


def main() -> int:
    ap = __import__("argparse").ArgumentParser(
        description="glasspring output-contract checker (PASS/FAIL/UNKNOWN clauses)")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("directory", nargs="?", help="run directory to verify")
    ap.add_argument("--html", metavar="OUT", help="also write a single-file acceptance report (clauses + embedded screenshots)")
    a = ap.parse_args()
    if a.selftest:
        fails = []
        base = selftest()
        if base:
            fails.append("base")
        ok, path = selftest_html()
        print(f"  [{'PASS' if ok else 'FAIL'}] --html report (verdict + embedded shots + clause rows) -> {path}")
        if not ok:
            fails.append("html")
        if fails:
            print(f"SELFTEST FAILED: {fails}")
            return 1
        return 0
    if not a.directory:
        ap.error("give a run directory or --selftest")
    results = check_run(a.directory)
    for name, status, detail in results:
        print(f"[{status:7}] {name}: {detail}")
    hard = [r for r in results if r[1] == FAIL]
    soft = [r for r in results if r[1] == UNKNOWN]
    print(f"summary: {len(hard)} fail, {len(soft)} unknown, "
          f"{len(results) - len(hard) - len(soft)} pass")
    if a.html:
        open(a.html, "w", encoding="utf-8").write(render_html(a.directory, results))
        print(f"acceptance report -> {a.html}")
    return 1 if hard else (2 if soft else 0)


if __name__ == "__main__":
    sys.exit(main())
