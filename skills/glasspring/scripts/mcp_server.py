#!/usr/bin/env python3
"""mcp_server.py — expose glasspring gates as MCP tools over stdio (JSON-RPC 2.0).

Why: agents in MCP-native hosts (Claude Desktop, ZCode, Cursor) can call the
gates as first-class tools — structured JSON back, no shell quoting, no "did
it actually run?" ambiguity. The verify loop becomes: edit → slop_scan →
check_contrast → verify_output → probe_render, each one round trip.

Transport: stdio, newline-delimited JSON-RPC 2.0 (MCP spec baseline
2025-06-18; newer clients' _meta fields are tolerated silently). stdout
carries protocol frames ONLY — all logging goes to stderr. In-process calls
to the sibling gate modules; subprocess only where no programmatic API exists
(doctor, deal_direction). 10 tools:

  slop_scan        static anti-slop scan (29 rules) — findings as JSON
  check_contrast   WCAG 2.2 + APCA batch pair check — per-pair verdicts
  verify_output    output-contract mechanical check — clause rows as JSON
  probe_render     6-pass render probe (spawns a browser; seconds)
  visual_diff      pixel PNG diff — fix-loop / drift gates
  notes_draft      auto-draft design-notes mechanical sections (§4/§6/§8)
  spring_convert   spring params → CSS linear() / Motion params
  palette_from_oklch  brand seed → OKLCH ramp CSS (rederived, not copied)
  deal_direction   direction dealer (subprocess; prompt-seeded deal text)
  doctor           aggregate health check (subprocess; stdout tail)

Register in an MCP client:
  {"command": "python", "args": [".agents/skills/glasspring/scripts/mcp_server.py"]}

Usage:
  python mcp_server.py            # serve on stdio
  python mcp_server.py --selftest # spawn self, full handshake + tool calls
"""
from __future__ import annotations
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import check_contrast as cc  # noqa: E402
import slop_scan as ss  # noqa: E402
import verify_output as vo  # noqa: E402
import visual_diff as vd  # noqa: E402
import spring_convert as sc  # noqa: E402
import notes_draft as nd  # noqa: E402

PROTOCOL_VERSION = "2025-06-18"
SERVER_INFO = {"name": "glasspring", "version": "2.1"}


def _abs(p: str) -> str:
    return p if os.path.isabs(p) else os.path.abspath(p)


# ---------- tool handlers: (arguments) -> (structured, text) ----------

def t_slop_scan(a: dict):
    path = _abs(a["path"])
    min_sev = a.get("min_severity", "info")
    findings = ss.scan_path(path)
    floor = {"info": 0, "warn": 1, "hard": 2}[min_sev]
    rows = [{"severity": s, "rule": r, "where": w, "hint": h}
            for s, r, w, h in findings if {"info": 0, "warn": 1, "hard": 2}[s] >= floor]
    counts = {"hard": sum(1 for f in rows if f["severity"] == "hard"),
              "warn": sum(1 for f in rows if f["severity"] == "warn"),
              "info": sum(1 for f in rows if f["severity"] == "info")}
    return {"ok": counts["hard"] == 0, "counts": counts, "findings": rows}, None


def t_check_contrast(a: dict):
    pairs, out, fails = a.get("pairs") or [], [], []
    if not pairs:
        return {"ok": False, "verdict": "UNKNOWN", "pass": 0, "total": 0,
                "failing": [], "pairs": [], "reason": "No color pairs supplied"}, None
    for i, p in enumerate(pairs):
        label = p.get("label", f'pair{i}:{p["fg"]} on {p["bg"]}')
        large, aaa = bool(p.get("large")), bool(p.get("aaa"))
        try:
            r = cc.ratio(p["fg"], p["bg"])
            need = cc.AA_LARGE if large else (cc.AAA if aaa else cc.AA)
            row = {"label": label, "fg": p["fg"], "bg": p["bg"], "ratio": round(r, 2),
                   "verdict": cc.judge(r, large, aaa), "ok": r >= need,
                   "apca_lc": round(cc.apca_lc(tuple(round(c * 255) for c in cc.parse_color(p["fg"])),
                                               tuple(round(c * 255) for c in cc.parse_color(p["bg"]))), 1)}
        except Exception as e:  # noqa: BLE001 — a bad pair must not kill the batch
            row = {"label": label, "fg": p.get("fg"), "bg": p.get("bg"), "error": str(e), "ok": False}
        out.append(row)
        fails.extend([row["label"]] if not row["ok"] else [])
    return {"ok": not fails, "pass": len(out) - len(fails), "total": len(out),
            "failing": fails, "pairs": out}, None


def t_verify_output(a: dict):
    results = vo.check_run(_abs(a["directory"]))
    rows = [{"name": n, "status": s, "detail": d} for n, s, d in results]
    fails = [r for r in rows if r["status"] == "FAIL"]
    unknown = [r for r in rows if r["status"] == "UNKNOWN"]
    return {"ok": not fails and not unknown, "verdict": "FAIL" if fails else ("UNKNOWN" if unknown else "PASS"),
            "counts": {"pass": len(rows) - len(fails) - len(unknown), "fail": len(fails), "unknown": len(unknown)},
            "clauses": rows}, None


def t_probe_render(a: dict):
    import probe_render as pr
    nat, froz, red, rac, a_ser, a_min, e_fail, vacuous, eco = pr.probe(
        a["url"], settle=float(a.get("settle", 0.8)), width=int(a.get("width", 1440)),
        with_axe=bool(a.get("axe", True)))
    status = pr.coverage_verdict(nat, red, rac, a_ser, e_fail, vacuous,
                                 axe_requested=bool(a.get("axe", True)))
    return {**status, "width": int(a.get("width", 1440)),
            "pass_a_gatekeeper": nat, "pass_b_frozen_extra": froz, "pass_c_reduce_hidden": red,
            "waapi_animating_under_reduce": rac, "axe_serious": a_ser,
            "axe_minimserious": a_min, "pass_e_click_violations": e_fail,
            "economy": eco}, None


def t_visual_diff(a: dict):
    r = vd.diff(_abs(a["png_a"]), _abs(a["png_b"]), tol=int(a.get("tol", 0)))
    verdict, why = "pass", ""
    mn, mx = a.get("min_diff"), a.get("max_diff")
    if mx is not None and r["ratio"] > float(mx):
        verdict, why = "fail", f"ratio {r['ratio']:.5f} > max {mx} (drift / unwanted change)"
    elif mn is not None and r["ratio"] < float(mn):
        verdict, why = "fail", f"ratio {r['ratio']:.5f} < min {mn} — no visible change: the fix changed nothing"
    return {"ok": verdict == "pass", "verdict": verdict, "why": why,
            "changed": r["changed"], "total": r["total"], "ratio": r["ratio"], "bbox": r["bbox"]}, None


def t_notes_draft(a: dict):
    run_dir = _abs(a["run_dir"])
    tokens = nd.parse_tokens(os.path.join(run_dir, "tokens.css")) if os.path.isfile(os.path.join(run_dir, "tokens.css")) else {}
    pairs, skipped = (nd.derive_pairs(tokens) if tokens else ([], ["tokens.css not found — fill §4 by hand"]))
    if a.get("pairs"):
        for item in a["pairs"].split(","):
            label, _, spec = item.partition("=")
            fg, _, bg = spec.partition(":")
            if fg and bg:
                pairs = [p for p in pairs if p["label"] != label] + [
                    {"label": label, "fg": fg, "bg": bg, "source": "EXPLICIT"}]
    nd.measure(pairs)
    slop = ss.scan_path(run_dir) or []
    refs = a.get("refs") or ["tokens.md", "type.md", "layout-baselines.md", "motion.md"]
    draft = nd.build_draft(run_dir, pairs, skipped, slop, refs, a.get("pack"),
                           f"mcp: notes_draft {run_dir}")
    result = {"draft": draft, "pairs_measured": len(pairs), "pairs_fail": sum(1 for p in pairs if not p.get("ok")),
              "slop_findings": len(slop)}
    if a.get("write", True):
        out = os.path.join(run_dir, "design-notes-DRAFT.md")
        if os.path.exists(out) and not a.get("force"):
            result["written"] = False
            result["note"] = f"refusing to overwrite {out} (force=true to overwrite)"
        else:
            with open(out, "w", encoding="utf-8") as f:
                f.write(draft)
            result["written"], result["out_path"] = True, out
    return result, None


def t_spring_convert(a: dict):
    if a.get("physical"):
        p = sc.params_from_physical(**a["physical"])
    elif a.get("response") is not None:
        p = sc.params_from_response_damping(float(a["response"]), float(a.get("damping_fraction", 1.0)))
    else:
        p = sc.params_from_duration_bounce(float(a["duration"]), float(a.get("bounce", 0.0)))
    css = sc.css_linear(float(a.get("duration", p.get("duration", 0.5))), float(a.get("bounce", 0.0)),
                        points=int(a.get("points", 64)))
    return {"params": p, "css_linear": css, "human": sc.fmt(p)}, None


def t_palette(a: dict):
    import palette_from_oklch as pf
    if a.get("seed"):
        ramps = pf.derive(a["seed"], neutral=bool(a.get("neutral")))
        return {"css": pf.emit_css(ramps), "neutral": bool(a.get("neutral"))}, None
    if a.get("hue") is not None:
        ramps = pf.derive_from_hue(float(a["hue"]), float(a.get("chroma", 0.14)), bool(a.get("neutral")))
        return {"css": pf.emit_css(ramps), "neutral": bool(a.get("neutral"))}, None
    raise ValueError("--seed or --hue required")


def _run_py(script: str, args: list[str], timeout: int = 300):
    p = subprocess.run([sys.executable, os.path.join(HERE, script), *args],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    return p.returncode, (p.stdout + p.stderr).strip()


def t_deal_direction(a: dict):
    args = []
    if a.get("prompt"):
        args += ["--prompt", a["prompt"]]
    if a.get("seed"):
        args += ["--seed", str(a["seed"])]
    if a.get("keep"):
        args += ["--keep", a["keep"]]
    rc, out = _run_py("deal_direction.py", args)
    return {"ok": rc == 0, "deal": out}, None


def t_doctor(a: dict):
    args = []
    if a.get("target"):
        args += ["--target", _abs(a["target"])]
    if a.get("skip_selftest"):
        args.append("--skip-selftest")
    rc, out = _run_py("doctor.py", args, timeout=600)
    tail = "\n".join(out.splitlines()[-12:])
    return {"ok": rc == 0, "exit_code": rc, "tail": tail}, None


# ---------- tool registry ----------

def _obj(props: dict, required: list[str] | None = None) -> dict:
    s = {"type": "object", "properties": props, "additionalProperties": False}
    if required:
        s["required"] = required
    return s


TOOLS = [
    {"name": "slop_scan", "title": "Anti-slop scan",
     "description": "Static scan of HTML/CSS for documented AI-slop tells (29 rules: cream/terracotta/rich-black hex, purple gradients, middle-dot meta, em-dash labels, arrow links, Inter identity, fade-up cards, uniform radius/shadow...). hard=CI gate, warn=fix or justify in design-notes.",
     "inputSchema": _obj({"path": {"type": "string", "description": "file or directory (*.html/*.css)"},
                          "min_severity": {"type": "string", "enum": ["info", "warn", "hard"]}},
                         ["path"]),
     "handler": t_slop_scan},
    {"name": "check_contrast", "title": "Contrast batch check",
     "description": "WCAG 2.2 contrast + APCA Lc for a batch of fg/bg pairs (hex/rgb/oklch). AA=4.5, AAA=7, large=3. Shipped guesses are defects — every text/background pair must be measured.",
     "inputSchema": _obj({"pairs": {"type": "array", "items": {"type": "object", "properties": {
         "label": {"type": "string"}, "fg": {"type": "string"}, "bg": {"type": "string"},
         "large": {"type": "boolean"}, "aaa": {"type": "boolean"}}, "required": ["fg", "bg"]}}},
                         ["pairs"]),
     "handler": t_check_contrast},
    {"name": "verify_output", "title": "Output contract check",
     "description": "Mechanical delivery-contract check of a run directory (tokens.css + preview.html + design-notes.md §0-§8, scope hygiene). FAIL = do not deliver.",
     "inputSchema": _obj({"directory": {"type": "string"}}, ["directory"]),
     "handler": t_verify_output},
    {"name": "probe_render", "title": "6-pass render probe",
     "description": "Live render probe via CDP (spawns a browser; takes seconds): A animation-gated content, B t=0 frozen window, C reduced-motion contract, D axe a11y, E click fingerprint (dead contract / invisible state, subtree-aware), F economy signals (flat spacing / one-sided accent).",
     "inputSchema": _obj({"url": {"type": "string", "description": "http(s) URL or file:/// path"},
                          "width": {"type": "integer"}, "settle": {"type": "number"}, "axe": {"type": "boolean"}},
                         ["url"]),
     "handler": t_probe_render},
    {"name": "visual_diff", "title": "Pixel screenshot diff",
     "description": "Pure-stdlib pixel diff of two PNGs of the same size. Gate modes: min_diff (fix-loop: a fix must change visible pixels — 无像素差=没修) and max_diff (drift: re-runs must match).",
     "inputSchema": _obj({"png_a": {"type": "string"}, "png_b": {"type": "string"}, "tol": {"type": "integer"},
                          "min_diff": {"type": "number"}, "max_diff": {"type": "number"}},
                         ["png_a", "png_b"]),
     "handler": t_visual_diff},
    {"name": "notes_draft", "title": "Design-notes auto-drafter",
     "description": "Auto-draft design-notes mechanical sections from live gates: §4 measured contrast (token auto-pairing; CANDIDATE rows need role confirmation), §6 first slop scan, §8 Last-verified anchors. Judgment sections stay TODO — finalize as design-notes.md yourself.",
     "inputSchema": _obj({"run_dir": {"type": "string"}, "pack": {"type": "string"},
                          "refs": {"type": "array", "items": {"type": "string"}},
                          "pairs": {"type": "string", "description": 'explicit pairs "label=fg:bg,..." '},
                          "write": {"type": "boolean"}, "force": {"type": "boolean"}},
                         ["run_dir"]),
     "handler": t_notes_draft},
    {"name": "spring_convert", "title": "Spring converter",
     "description": "SwiftUI spring params → CSS linear() + Motion params (Apple-official anchored). Inputs: duration+bounce, response+damping_fraction, or physical {mass, stiffness, damping}.",
     "inputSchema": _obj({"duration": {"type": "number"}, "bounce": {"type": "number"},
                          "response": {"type": "number"}, "damping_fraction": {"type": "number"},
                          "physical": {"type": "object", "properties": {"mass": {"type": "number"}, "stiffness": {"type": "number"}, "damping": {"type": "number"}}},
                          "points": {"type": "integer"}}),
     "handler": t_spring_convert},
    {"name": "palette_from_oklch", "title": "Seed → OKLCH ramp",
     "description": "Brand seed hex → rederived OKLCH ramp CSS (L3: rederived from the seed, never copied). neutral=true derives the tinted-neutral ramp instead.",
     "inputSchema": _obj({"seed": {"type": "string"}, "hue": {"type": "number"}, "chroma": {"type": "number"},
                          "neutral": {"type": "boolean"}}),
     "handler": t_palette},
    {"name": "deal_direction", "title": "Direction dealer",
     "description": "Open-brief builds: deal 3 directions from a 12-pack deck (prompt-derived deterministic seed), commit to 1. Commitment laws print with the deal: pick the unobvious, no default-layout blending, re-deal only with stated reason.",
     "inputSchema": _obj({"prompt": {"type": "string"}, "seed": {"type": "integer"}, "keep": {"type": "string"}}),
     "handler": t_deal_direction},
    {"name": "doctor", "title": "Skill health check",
     "description": "One-shot aggregate: every tool selftest + slop scan + output contract on a target directory. ALL GREEN = toolchain ready.",
     "inputSchema": _obj({"target": {"type": "string"}, "skip_selftest": {"type": "boolean"}}),
     "handler": t_doctor},
]

BY_NAME = {t["name"]: t for t in TOOLS}


# ---------- JSON-RPC loop ----------

def _write(obj: dict):
    sys.stdout.write(json.dumps(obj, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def handle(msg: dict):
    method = msg.get("method", "")
    mid = msg.get("id")
    if method == "initialize":
        _write({"jsonrpc": "2.0", "id": mid, "result": {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": SERVER_INFO}})
    elif method == "tools/list":
        _write({"jsonrpc": "2.0", "id": mid, "result": {
            "tools": [{k: t[k] for k in ("name", "title", "description", "inputSchema")}
                      for t in sorted(TOOLS, key=lambda t: t["name"])]}})
    elif method == "tools/call":
        params = msg.get("params") or {}
        tool = BY_NAME.get(params.get("name"))
        if tool is None:
            _write({"jsonrpc": "2.0", "id": mid, "error": {"code": -32602,
                    "message": f"Unknown tool: {params.get('name')!r}"}})
            return
        try:
            structured, text = tool["handler"](params.get("arguments") or {})
        except Exception as e:  # noqa: BLE001 — execution errors are model-recoverable
            _write({"jsonrpc": "2.0", "id": mid, "result": {
                "content": [{"type": "text", "text": f"{type(e).__name__}: {e}"}], "isError": True}})
            return
        payload = json.dumps(structured, ensure_ascii=False)
        _write({"jsonrpc": "2.0", "id": mid, "result": {
            "content": [{"type": "text", "text": text or payload}],
            "structuredContent": structured, "isError": False}})
    elif method == "ping":
        _write({"jsonrpc": "2.0", "id": mid, "result": {}})
    elif method.startswith("notifications/"):
        pass
    elif mid is not None:
        _write({"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": f"Method not found: {method}"}})


def serve():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except ValueError:
            continue
        try:
            handle(msg)
        except Exception as e:  # noqa: BLE001 — the server must survive handler bugs
            if msg.get("id") is not None:
                _write({"jsonrpc": "2.0", "id": msg["id"],
                        "error": {"code": -32603, "message": f"internal error: {type(e).__name__}: {e}"}})


def selftest() -> int:
    """Spawn self, drive the full handshake + representative tool calls."""
    import tempfile, time
    fails = []

    def check(name, ok, detail=""):
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f": {detail}" if detail else ""))
        if not ok:
            fails.append(name)

    with tempfile.TemporaryDirectory() as td:
        # fixture: slop-tell page + contrast-safe pairs + two diffable PNGs
        html = os.path.join(td, "page.html")
        with open(html, "w", encoding="utf-8") as f:
            f.write("<h1>x — y</h1><p style='background:#f4f1ea'>z</p>")
        def chunk(typ, data):
            import struct, zlib
            return struct.pack(">I", len(data)) + typ + data + struct.pack(">I", zlib.crc32(typ + data))
        import struct, zlib
        px = bytes((10, 20, 30)) * 16
        def png(path, flip=False):
            p = bytearray(px)
            if flip:
                p[15] = 200
            ihdr = struct.pack(">IIBBBBB", 4, 4, 8, 2, 0, 0, 0)
            raw = b"".join(b"\x00" + bytes(p[y * 12:(y + 1) * 12]) for y in range(4))
            with open(path, "wb") as f:
                f.write(vd.SIG + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))
        pa, pb = os.path.join(td, "a.png"), os.path.join(td, "b.png")
        png(pa); png(pb, flip=True)

        proc = subprocess.Popen([sys.executable, os.path.abspath(__file__)],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                stderr=subprocess.DEVNULL, text=True, encoding="utf-8")
        try:
            def rpc(method, params=None, mid=[0]):
                mid[0] += 1
                proc.stdin.write(json.dumps({"jsonrpc": "2.0", "id": mid[0], "method": method,
                                             "params": params or {}}) + "\n")
                proc.stdin.flush()
                line = proc.stdout.readline()
                return json.loads(line)

            r = rpc("initialize", {"protocolVersion": PROTOCOL_VERSION,
                                   "capabilities": {}, "clientInfo": {"name": "selftest", "version": "0"}})
            check("initialize handshake", r["result"]["serverInfo"]["name"] == "glasspring"
                  and "tools" in r["result"]["capabilities"], str(r.get("result", r))[:80])
            proc.stdin.write(json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}) + "\n")
            proc.stdin.flush()

            r = rpc("tools/list")
            names = [t["name"] for t in r["result"]["tools"]]
            check("tools/list: 10 tools, deterministic", len(names) == 10 and names == sorted(names), str(names))

            r = rpc("tools/call", {"name": "slop_scan", "arguments": {"path": html}})
            sc_ = r["result"]["structuredContent"]
            check("slop_scan: cream_hex + em-dash caught, ok=false",
                  sc_["ok"] is False and any(f["rule"] == "cream_hex" for f in sc_["findings"]), str(sc_["counts"]))

            r = rpc("tools/call", {"name": "check_contrast", "arguments": {"pairs": [
                {"label": "ink/paper", "fg": "#1a1a1a", "bg": "#ffffff"},
                {"label": "fail-pair", "fg": "#888888", "bg": "#ffffff"}]}})
            sc_ = r["result"]["structuredContent"]
            check("check_contrast: 1 pass 1 fail", sc_["pass"] == 1 and sc_["failing"] == ["fail-pair"],
                  f'{sc_["pass"]}/{sc_["total"]}')

            r = rpc("tools/call", {"name": "visual_diff", "arguments": {"png_a": pa, "png_b": pb, "min_diff": 0.01}})
            sc_ = r["result"]["structuredContent"]
            check("visual_diff: flip detected, min_diff gate passes",
                  sc_["changed"] == 1 and sc_["ok"], str(sc_))

            r = rpc("tools/call", {"name": "visual_diff", "arguments": {"png_a": pa, "png_b": pa, "min_diff": 0.01}})
            check("visual_diff: no-change caught as fix-loop fail", r["result"]["isError"] is False
                  and r["result"]["structuredContent"]["ok"] is False, "")

            r = rpc("tools/call", {"name": "check_contrast", "arguments": {"pairs": [{"fg": "not-a-color", "bg": "#fff"}]}})
            sc_ = r["result"]["structuredContent"]
            check("bad pair: contained per-pair error row, batch survives",
                  r["result"]["isError"] is False and not sc_["pairs"][0]["ok"] and "error" in sc_["pairs"][0], "")

            r = rpc("tools/call", {"name": "visual_diff", "arguments": {"png_a": "Z:/nope.png", "png_b": "Z:/nope2.png"}})
            check("tool execution error -> isError:true", r["result"]["isError"] is True, "")

            r = rpc("tools/call", {"name": "no_such_tool"})
            check("unknown tool -> JSON-RPC error -32602", r.get("error", {}).get("code") == -32602, "")

            r = rpc("spring_convert/x", {})
            check("unknown method -> -32601", r.get("error", {}).get("code") == -32601, "")

            r = rpc("tools/call", {"name": "spring_convert", "arguments": {"duration": 0.5, "bounce": 0.3}})
            sc_ = r["result"]["structuredContent"]
            check("spring_convert: Apple anchor 0.5/0.3 -> stiffness 157.9",
                  abs(sc_["params"]["stiffness"] - 157.9) < 0.5, str(sc_["params"])[:80])

            r = rpc("tools/call", {"name": "palette_from_oklch", "arguments": {"seed": "#58cc02"}})
            sc_ = r["result"]["structuredContent"]
            check("palette: emits :root block", "--" in sc_["css"] and "oklch" in sc_["css"], sc_["css"][:60])
        finally:
            try:
                proc.stdin.close()
            except OSError:
                pass
            proc.wait(timeout=10)
    print("mcp_server selftest:", "ALL PASS" if not fails else f"FAILED: {fails}")
    return 0 if not fails else 1


def main() -> int:
    if "--selftest" in sys.argv:
        return selftest()
    try:  # Windows consoles default to cp1252 — protocol is UTF-8
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stdin.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass
    print(f"glasspring MCP server ({SERVER_INFO['version']}): {len(TOOLS)} tools on stdio", file=sys.stderr)
    serve()
    return 0


if __name__ == "__main__":
    sys.exit(main())
