#!/usr/bin/env python3
"""samples_gate.py — regression runner for an optional sample directory.

The repository does not ship client or historical benchmark projects. Point
this runner at samples you are authorized to use; it walks immediate child
directories of the supplied root:

  static sample  (preview.html, no package.json)
      -> slop_scan + probe_render on file://
  build sample   (package.json with a build script)
      -> npm run build -> vite preview (parsed port) -> probe_render on http
         (+ slop_scan over src/ when present)

One aggregate table, one exit code. Build samples are skipped with an honest
SKIP when node_modules is missing (run `npm i` first) — a missing install is a
skip, not a failure.

Usage:
  python samples_gate.py                       # all samples under examples/
  python samples_gate.py --root ../examples    # custom workspace root
  python samples_gate.py --only <sample-name> # one sample
"""
from __future__ import annotations
import argparse, http.client, os, re, subprocess, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
DEFAULT_ROOT = os.path.normpath(os.path.join(SKILL, "..", "..", "examples"))

sys.path.insert(0, HERE)
import probe_render  # noqa: E402

def run(cmd: list[str], cwd: str | None = None, timeout: int = 300) -> tuple[int, str]:
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=timeout,
                       shell=(os.name == "nt"))
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def slop_ok(path: str) -> tuple[bool, str]:
    rc, out = run([sys.executable, os.path.join(HERE, "slop_scan.py"), path], cwd=HERE)
    return rc == 0, out.strip().splitlines()[-1] if out.strip() else "no output"


def has_unreachable_remote_deps(path: str) -> str | None:
    """Return a reason string if the page references remote images and the
    network is down. Environmental
    dependency != page defect — per exit-code discipline that's a SKIP,
    not a FAIL (couldn't look, not found issues)."""
    import re as _re, urllib.request as _u
    try:
        html = open(path, encoding="utf-8", errors="ignore").read()
    except OSError:
        return None
    hosts = set()
    for m in _re.finditer(r'src="(https?://([^/"]+))', html):
        hosts.add(m.group(2))
    if not hosts:
        return None
    for h in sorted(hosts):
        try:
            _u.urlopen(f"https://{h}/", timeout=4)
        except Exception:
            return f"remote image host unreachable: {h}"
    return None


def probe(url: str, attempts: int = 2, width: int = 1440,
          expected_a11y: dict | None = None) -> tuple[bool, str]:
    """Two attempts: back-to-back multi-sample runs hit intermittent CDP/WS
    timeouts (same flakiness preview_shot's shoot_with_retry absorbs). The
    second attempt absorbs the transient; a real page failure fails twice."""
    last = None
    for i in range(1, attempts + 1):
        try:
            a, b, c, rac, a_ser, a_min, e_fail, vacuous, eco = probe_render.probe(url, width=width)
            status = probe_render.coverage_verdict(a, c, rac, a_ser, e_fail, vacuous,
                                                  expected_a11y=expected_a11y)
            detail = (f"{width}px {status['verdict']}: A {len(a)} / C {len(c)} / WAAPI {rac} "
                      f"/ axe {a_ser} / E {e_fail} / vacuous {vacuous}; "
                      f"expected-negative {status['expected_negative']}; missing {status['missing_checks']}")
            return status['ok'], detail
        except Exception as e:  # noqa: BLE001
            last = f"{type(e).__name__}: {e}"
            if i < attempts:
                time.sleep(1.0)
    return False, f"probe failed after {attempts} attempts: {last}"


def serve_and_probe_build(sample_dir: str) -> tuple[bool, str]:
    rc, out = run(["npm", "run", "build"], cwd=sample_dir, timeout=420)
    if rc != 0:
        return False, "npm run build failed: " + out.strip().splitlines()[-1][:120]
    port = free_port()
    log = os.path.join(sample_dir, ".preview.log")
    with open(log, "w", encoding="utf-8") as lf:
        proc = subprocess.Popen(["npx", "vite", "preview", "--port", str(port), "--strictPort"],
                                cwd=sample_dir, stdout=lf, stderr=lf, shell=(os.name == "nt"))
    try:
        url = f"http://localhost:{port}/"
        if not wait_for_preview(url):
            return False, "preview server never came up"
        r1, d1 = probe(url, width=390)
        r2, d2 = probe(url, width=1440)
        return r1 and r2, d1 + '; ' + d2
    finally:
        if os.name == "nt":
            subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"], capture_output=True)
        else:
            proc.terminate()


def wait_for_preview(url: str, attempts: int = 30, delay: float = 0.1) -> bool:
    """Wait through transient malformed responses while the preview starts.

    A BadStatusLine during startup is not a successful probe. Keep the existing
    bounded wait and require a later valid HTTP response before continuing.
    """
    for _ in range(attempts):
        try:
            with urllib.request.urlopen(url, timeout=1):
                return True
        except (OSError, http.client.HTTPException):
            time.sleep(delay)
    return False


def free_port() -> int:
    import socket
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def main() -> int:
    ap = argparse.ArgumentParser(description="sample interface regression runner")
    ap.add_argument("--root", default=DEFAULT_ROOT, help="directory containing authorized sample projects")
    ap.add_argument("--only", help="restrict to one sample directory name")
    ap.add_argument("--skip-builds", action="store_true", help="static samples only")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        ok = (callable(slop_ok) and callable(probe) and DEFAULT_ROOT.endswith("examples"))
        print(f"  [{'PASS' if ok else 'FAIL'}] default root resolves under examples/")
        print("SELFTEST PASSED (offline)" if ok else "SELFTEST FAILED")
        return 0 if ok else 1

    root = os.path.abspath(a.root)
    if not os.path.isdir(root):
        print(f"examples root not found: {root}")
        return 2
    samples = sorted(d for d in os.listdir(root)
                     if not d.startswith(".") and os.path.isdir(os.path.join(root, d))
                     and (os.path.isfile(os.path.join(root, d, "package.json"))
                          or os.path.isfile(os.path.join(root, d, "preview.html"))
                          or any(f.endswith(".html") for f in os.listdir(os.path.join(root, d)))))
    if a.only:
        samples = [s for s in samples if s == a.only]

    rows: list[tuple[str, str, str]] = []
    failures = 0
    for s in samples:
        d = os.path.join(root, s)
        has_pkg = os.path.isfile(os.path.join(d, "package.json"))
        entries = (["preview.html"] if os.path.isfile(os.path.join(d, "preview.html"))
                   else sorted(f for f in os.listdir(d) if f.endswith('.html')) if not has_pkg else [])
        has_html = bool(entries)
        net_reason = None
        try:
            if has_pkg and not has_html and not a.skip_builds:
                if not os.path.isdir(os.path.join(d, "node_modules")):
                    rows.append((s, "SKIP", "node_modules missing (npm i first)"))
                    continue
                ok, detail = serve_and_probe_build(d)
            elif has_html:
                net_reason = next((r for f in entries if (r := has_unreachable_remote_deps(os.path.join(d, f)))), None)
                if net_reason:
                    rows.append((s, "SKIP", net_reason))
                    continue
                from pathlib import Path
                checks = []
                for entry in entries:
                    ok_s, msg_s = slop_ok(os.path.join(d, entry))
                    checks.append((ok_s, f'{entry}: {msg_s}'))
                    for width in (390, 1440):
                        checks.append(probe(Path(d, entry).as_uri(), width=width))
                ok = all(c[0] for c in checks)
                detail = '; '.join(c[1] for c in checks)
            elif has_pkg:
                rows.append((s, "SKIP", "build sample (--skip-builds)"))
                continue
            else:
                rows.append((s, "SKIP", "no preview.html / package.json"))
                continue
        except Exception as e:  # noqa: BLE001
            ok, detail = False, f"{type(e).__name__}: {e}"
        rows.append((s, "PASS" if ok else "FAIL", detail))
        failures += 0 if ok else 1

    width = max((len(s) for s, _, _ in rows), default=0)
    print(f"== samples gate: {len(rows)} samples under {root} ==")
    for s, verdict, detail in rows:
        print(f"  [{verdict}] {s.ljust(width)}  {detail}")
    print(f"== {failures} failing ==")
    skipped = sum(v == 'SKIP' for _, v, _ in rows)
    print(f"coverage: {skipped} skipped; {len(rows)} rows")
    return 1 if failures else (2 if skipped or not rows else 0)


if __name__ == "__main__":
    sys.exit(main())
