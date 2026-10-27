#!/usr/bin/env python3
"""observe_follow.py — constraint-following tracker for glassspring sessions.

Adapts the /observe idea (XIAS) with the Skill Coverage finding: benchmark
trajectories cover only ~38-45% of skill constraints on average, so a task
score alone cannot show the skill was followed. This tool reads a SESSION
TRANSCRIPT (any text export that shows tool calls and file writes in order)
and reports, per constraint, FOLLOWED / VIOLATED / NOT_OBSERVED plus a
coverage ratio. It measures following; it does not grade design quality.

Usage:
  python observe_follow.py --transcript session.log [--run-dir DIR] [--strict]
  python observe_follow.py --selftest

Exit 0 always, except --strict (exit 1 on any VIOLATED) or bad input.
"""
from __future__ import annotations
import argparse
import os
import re
import sys

REF_RE = re.compile(r"references/(?:domains|style-packs|platforms|types)/[\w-]+\.md"
                    r"|references/(?:tokens|type|layout-baselines|motion|glass|recommended-stack)\.md",
                    re.I)
CORE_RE = re.compile(r"references/(?:tokens|type|layout-baselines|motion|recommended-stack)\.md"
                     r"|references/domains/[\w-]+\.md|references/style-packs/[\w-]+\.md", re.I)
GATE_RE = re.compile(r"references/glass\.md", re.I)
PLATFORM_RE = re.compile(r"references/platforms/[\w-]+\.md", re.I)
TOOL_RES = {
    "check_contrast": re.compile(r"check_contrast\.py", re.I),
    "slop_scan": re.compile(r"slop_scan\.py", re.I),
    "render_probe": re.compile(r"probe_render\.py|preview_shot\.py", re.I),
    "contract": re.compile(r"verify_output\.py|doctor\.py", re.I),
}
DISCLOSE_RE = re.compile(r"could not run|无法运行|无法执行|not available|permission[- ]blocked|"
                         r"UNKNOWN|SKIP|不可用|未运行|无法执行", re.I)
WRITE_TOKENS = re.compile(r"(write|create|生成|写入|touch|open)\b.{0,60}\btokens\.css|tokens\.css.{0,40}(written|created|生成)", re.I)
WRITE_PREVIEW = re.compile(r"(write|create|生成|写入|touch|open)\b.{0,60}\bpreview\.html|preview\.html.{0,40}(written|created|生成)", re.I)
DELIVER_RE = {
    "tokens.css": re.compile(r"tokens\.css", re.I),
    "preview.html": re.compile(r"preview\.html", re.I),
    "design-notes.md": re.compile(r"design-notes\.md", re.I),
    "shots/": re.compile(r"shots/|\.png", re.I),
}
SKILL_READ = re.compile(r"SKILL\.md", re.I)


def analyse(transcript: str, run_dir: str | None = None) -> dict:
    t = transcript
    lines = t.splitlines()
    results: dict[str, dict] = {}

    def mark(name, status, why):
        results[name] = {"status": status, "why": why}

    # 1. skill loaded
    mark("skill_loaded", "FOLLOWED" if SKILL_READ.search(t) else "NOT_OBSERVED",
         "SKILL.md appears in the transcript" if SKILL_READ.search(t)
         else "no SKILL.md read observed — discovery/invocation unproven")

    # 2. routing budget (order of first mentions)
    seen: list[str] = []
    gate_reads = platform_reads = 0
    for m in REF_RE.finditer(t):
        p = m.group(0).lower()
        if GATE_RE.match(p):
            gate_reads += 1
            continue
        if PLATFORM_RE.match(p):
            platform_reads += 1
            continue
        if p not in seen:
            seen.append(p)
    core = [p for p in seen if CORE_RE.match(p)]
    over = len(core) - 3
    if not seen:
        mark("routing_budget", "NOT_OBSERVED", "no reference reads observed")
    elif over <= 0:
        mark("routing_budget", "FOLLOWED",
             f"{len(core)} core reference(s) read (budget <= 3); glass gate reads: {gate_reads}; "
             f"platform adapters: {platform_reads} (exempt)")
    else:
        mark("routing_budget", "VIOLATED",
             f"{len(core)} core references read exceeds the 3-file budget: {', '.join(core)}")

    # 3. tokens-first (first mention order)
    it, ip = WRITE_TOKENS.search(t), WRITE_PREVIEW.search(t)
    if it and ip:
        mark("tokens_first", "FOLLOWED" if it.start() < ip.start() else "VIOLATED",
             f"tokens.css write observed at offset {it.start()}, preview.html at {ip.start()}")
    elif run_dir and os.path.isdir(run_dir):
        mt = os.path.getmtime(os.path.join(run_dir, "tokens.css")) if os.path.isfile(os.path.join(run_dir, "tokens.css")) else None
        mp = os.path.getmtime(os.path.join(run_dir, "preview.html")) if os.path.isfile(os.path.join(run_dir, "preview.html")) else None
        if mt and mp:
            mark("tokens_first", "FOLLOWED" if mt <= mp else "VIOLATED",
                 "compared file mtimes in the run dir (transcript lacked ordered writes)")
        else:
            mark("tokens_first", "NOT_OBSERVED", "run dir incomplete")
    else:
        mark("tokens_first", "NOT_OBSERVED", "no ordered write evidence")

    # 4. tool invocations or honest disclosure
    for name, rx in TOOL_RES.items():
        if rx.search(t):
            mark(name, "FOLLOWED", "invoked in transcript")
        elif DISCLOSE_RE.search(t):
            mark(name, "FOLLOWED", "not invoked but an honest limitation is disclosed")
        else:
            mark(name, "NOT_OBSERVED", "neither invocation nor disclosure observed")

    # 5. deliverables
    for name, rx in DELIVER_RE.items():
        mark(f"deliverable:{name}", "FOLLOWED" if rx.search(t) else "NOT_OBSERVED",
             "mentioned" if rx.search(t) else "not observed in transcript")

    observable = [v for v in results.values() if v["status"] != "NOT_OBSERVED"]
    followed = [v for v in observable if v["status"] == "FOLLOWED"]
    results["_coverage"] = {
        "followed": len(followed), "observable": len(observable),
        "total": len(results),
        "ratio": (len(followed) / len(observable)) if observable else None,
    }
    return results


GOOD = """\
session: design task
read .claude/skills/glassspring/SKILL.md
read references/tokens.md
read references/domains/finance.md
read references/motion.md
write tokens.css seed ramp
python scripts/check_contrast.py --pairs ...
python scripts/slop_scan.py preview.html
python scripts/probe_render.py http://127.0.0.1:8000/preview.html
python scripts/doctor.py --target .
write preview.html with hero and cards
write design-notes.md sections 0-8
save shots/mobile.png shots/desktop.png
"""

BAD = """\
session: design task, no skill
read references/tokens.md references/type.md references/layout-baselines.md references/motion.md references/glass.md
write preview.html first
write tokens.css later
no checks were run at all
"""

HONEST = """\
session: tokens-only task
read SKILL.md, references/tokens.md, references/domains/ecommerce-retail.md
python scripts/slop_scan.py .
helper check_contrast.py could not run (execution policy) — manual OKLCH math substituted, pairs listed
write tokens.css
mention design-notes.md to fill
"""


def selftest() -> int:
    fails = []

    def check(name, ok, detail=""):
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f": {detail}" if detail else ""))
        if not ok:
            fails.append(name)

    g = analyse(GOOD)
    check("GOOD: skill loaded FOLLOWED", g["skill_loaded"]["status"] == "FOLLOWED")
    check("GOOD: routing budget FOLLOWED (3 core, glass=gate)",
          g["routing_budget"]["status"] == "FOLLOWED", g["routing_budget"]["why"])
    check("GOOD: tokens-first FOLLOWED", g["tokens_first"]["status"] == "FOLLOWED")
    check("GOOD: all four tools FOLLOWED",
          all(g[k]["status"] == "FOLLOWED" for k in ("check_contrast", "slop_scan", "render_probe", "contract")))
    check("GOOD: coverage 100% of observable",
          g["_coverage"]["ratio"] == 1.0, str(g["_coverage"]))

    b = analyse(BAD)
    check("BAD: routing budget VIOLATED (5 core reads)",
          b["routing_budget"]["status"] == "VIOLATED", b["routing_budget"]["why"])
    check("BAD: tokens-first VIOLATED", b["tokens_first"]["status"] == "VIOLATED")
    check("BAD: contrast NOT_OBSERVED (no invocation, no disclosure)",
          b["check_contrast"]["status"] == "NOT_OBSERVED")

    h = analyse(HONEST)
    check("HONEST: contrast counted FOLLOWED via disclosure",
          h["check_contrast"]["status"] == "FOLLOWED", h["check_contrast"]["why"])

    print("SELFTEST " + ("PASSED" if not fails else f"FAILED ({len(fails)})"))
    return 0 if not fails else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="constraint-following tracker for glassspring sessions")
    ap.add_argument("--transcript", help="session transcript (text export showing tool calls in order)")
    ap.add_argument("--run-dir", help="optional run dir for artifact-based checks")
    ap.add_argument("--strict", action="store_true", help="exit 1 on any VIOLATED constraint")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.transcript:
        ap.error("--transcript required (or --selftest)")
    try:
        t = open(a.transcript, encoding="utf-8", errors="replace").read()
    except OSError as e:
        print(f"cannot read transcript: {e}", file=sys.stderr)
        return 2
    res = analyse(t, a.run_dir)
    order = ["skill_loaded", "routing_budget", "tokens_first",
             "check_contrast", "slop_scan", "render_probe", "contract"]
    for k in order:
        v = res.get(k)
        if v:
            print(f"  [{v['status']:13s}] {k:16s} {v['why']}")
    for k in sorted(res):
        if k.startswith("deliverable:"):
            print(f"  [{res[k]['status']:13s}] {k:16s} {res[k]['why']}")
    c = res["_coverage"]
    ratio = f"{c['ratio']:.0%}" if c["ratio"] is not None else "n/a"
    print(f"\nfollowing coverage: {c['followed']}/{c['observable']} observable constraints "
          f"({ratio}); {c['total'] - c['observable']} NOT_OBSERVED")
    print("measures following, not design quality; NOT_OBSERVED is honest, never a pass")
    if a.strict and any(v["status"] == "VIOLATED" for k, v in res.items() if not k.startswith("_")):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
