#!/usr/bin/env python3
"""doctor.py — one-command health check for any glasspring engagement.

Run the packaged selftests, slop scan, and contract checks from one invocation
and return one report with a single exit code.

Checks, in order:
  1. tool selftests: check_contrast / spring_convert / slop_scan /
     verify_output (offline), preview_shot (--no-live unless --live)
  2. slop_scan over --target (default: current directory)
  3. verify_output over --target (output-contract clauses)

Usage:  python doctor.py [--target DIR] [--live] [--skip-selftest]
Exit:   0 = all green; 1 = any failure.
"""
from __future__ import annotations
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = ["check_contrast.py", "spring_convert.py", "slop_scan.py", "verify_output.py",
           "probe_render.py", "deal_direction.py", "token_emit.py", "run_init.py",
           "notes_draft.py", "visual_diff.py", "mcp_server.py",
           "divergence_report.py"]


def run(cmd: list[str]) -> tuple[int, str, float]:
    t0 = time.monotonic()
    p = subprocess.run([sys.executable, *cmd], capture_output=True, text=True,
                       encoding="utf-8", errors="ignore", timeout=180)
    tail = "\n".join((p.stdout + p.stderr).strip().splitlines()[-2:])
    return p.returncode, tail, time.monotonic() - t0


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(description="glasspring one-command health check")
    ap.add_argument("--target", default=".", help="directory to slop-scan and contract-verify")
    ap.add_argument("--live", action="store_true",
                    help="preview_shot selftest with live CDP capture (slower; default offline anchors only)")
    ap.add_argument("--skip-selftest", action="store_true",
                    help="skip tool selftests (run slop + contract checks only)")
    ap.add_argument("--selftest", action="store_true",
                    help="uniform-interface alias: run only the tool selftests (no target needed)")
    a = ap.parse_args()

    failures = 0
    elapsed = 0.0
    print("== glasspring doctor ==")

    print("-- tool selftests --")
    if not a.skip_selftest or a.selftest:
        for s in SCRIPTS:
            rc, tail, dt = run([os.path.join(HERE, s), "--selftest"])
            elapsed += dt
            print(f"  [{'OK' if rc == 0 else 'FAIL'}] {s}: {tail}")
            failures += rc != 0
        ps = [os.path.join(HERE, "preview_shot.py"), "--selftest"]
        if not a.live:
            ps.append("--no-live")
        rc, tail, dt = run(ps)
        elapsed += dt
        print(f"  [{'OK' if rc == 0 else 'FAIL'}] preview_shot.py ({'live' if a.live else 'offline'}): {tail}")
        failures += rc != 0
    else:
        print("  skipped (--skip-selftest)")

    if a.selftest:
        print(f"== doctor --selftest: {'ALL GREEN' if failures == 0 else f'{failures} failing'} ==")
        return 1 if failures else 0

    target_real = os.path.realpath(a.target)
    if target_real == HERE or target_real == os.path.dirname(HERE):
        print("  note: target is the skill root, not a run directory — slop hits in "
              "assets/glass-recipes are showcase fixtures (glass by design), and "
              "contract clauses expect a run dir (preview.html/tokens.css/design-notes.md/shots). "
              "Pass --target <run-dir> for a meaningful verdict.")

    print(f"-- slop scan: {a.target} --")
    rc, tail, dt = run([os.path.join(HERE, "slop_scan.py"), a.target])
    elapsed += dt
    print(f"  [{'OK' if rc == 0 else 'FAIL'}] {tail}")
    failures += rc != 0

    print(f"-- output contract: {a.target} --")
    rc, tail, dt = run([os.path.join(HERE, "verify_output.py"), a.target])
    elapsed += dt
    print(tail)
    failures += rc != 0

    print(f"== doctor mechanical checks: {'PASS' if failures == 0 else f'{failures} incomplete or failing check(s)'} ==")
    print(f"elapsed: {elapsed:.1f}s — record this and the run's token cost in design-notes §6 (cost observability)")
    print("This does not certify screenshot freshness, usability, WCAG conformance, or independent design improvement.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
