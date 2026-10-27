#!/usr/bin/env python3
"""divergence_report.py — four-attribute divergence across generated pages.

Distinctiveness is a separate outcome from brief fit (Design Creativity Bench
finding) and agent-made pages collapse to one face by default. This tool
measures, per page: title font family, body font family, accent hue family,
background family — then reports how many of the four attributes each pair of
pages shares (agentskillshub test-based-ranking attributes; adapted with
per-file extraction instead of screenshots so it runs offline and in CI).

  python divergence_report.py run1/ run2/ run3/        # sample dirs with preview.html/tokens.css
  python divergence_report.py --selftest

Verdict per pair: 0-1 shared axes = distinct, 2 = borderline, 3-4 = same face.
Exit 0 always unless inputs are unreadable; this is a measurement, not a gate.
"""
from __future__ import annotations
import argparse
import math
import os
import re
import sys

HEX_RE = re.compile(r"#[0-9a-fA-F]{6}\b")
FONT_RE = re.compile(r"font-family\s*:\s*([^;}]+)")
SEL_FONT_BLOCK_RE = re.compile(r"(h1|body)\s*\{([^}]*)\}", re.I)
TOKEN_ACCENT_RE = re.compile(r"(--[\w-]*accent[\w-]*)\s*:\s*([^;]+)", re.I)
TOKEN_BG_RE = re.compile(r"(--(?:bg|background|surface)[\w-]*)\s*:\s*([^;]+)", re.I)
BG_CSS_RE = re.compile(r"body\s*\{[^}]*background(?:-color)?\s*:\s*([^;}]+)", re.I | re.S)

HUE_FAMILIES = [("neutral", 0, 0), ("red", 0, 25), ("orange", 25, 60), ("yellow", 60, 90),
                ("green", 90, 150), ("teal", 150, 200), ("blue", 200, 255), ("purple", 255, 300),
                ("pink", 300, 345), ("red", 345, 360)]


def _first_font(stack: str) -> str:
    for part in stack.split(","):
        f = part.strip().strip("\"'").lower()
        if f and f not in ("inherit", "initial", "var(--font-body)", "var(--font-display)"):
            return re.sub(r"\s+", " ", f)
    return stack.strip().lower() or "unspecified"


def _hex_to_rgb(h: str) -> tuple[int, int, int]:
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))  # type: ignore[return-value]


def _rgb_to_hsl(r: int, g: int, b: int) -> tuple[float, float, float]:
    rf, gf, bf = r / 255, g / 255, b / 255
    mx, mn = max(rf, gf, bf), min(rf, gf, bf)
    l = (mx + mn) / 2
    if mx == mn:
        return 0.0, 0.0, l
    d = mx - mn
    s = d / (2 - mx - mn) if l > 0.5 else d / (mx + mn)
    if mx == rf:
        h = ((gf - bf) / d + (6 if gf < bf else 0)) * 60
    elif mx == gf:
        h = ((bf - rf) / d + 2) * 60
    else:
        h = ((rf - gf) / d + 4) * 60
    return h, s, l


def hue_family(h: float, spread: float) -> str:
    # spread = max-min in 0..1; HSL s inflates near black/white, so neutrality
    # is judged by channel spread (a cream #f8f3eb is a near-neutral surface).
    if spread < 0.06:
        return "neutral"
    for name, lo, hi in HUE_FAMILIES:
        if name == "neutral":
            continue
        if lo <= h < hi:
            return name
    return "neutral"


def bg_family(h: float, spread: float, l: float) -> str:
    tone = "dark" if l < 0.3 else ("light" if l > 0.7 else "mid")
    fam = "neutral" if spread < 0.08 else hue_family(h, spread)
    return f"{tone}-{fam}"


def _color_tokens(css: str) -> tuple[dict[str, str], dict[str, str]]:
    return ({m.group(1): m.group(2) for m in TOKEN_ACCENT_RE.finditer(css)},
            {m.group(1): m.group(2) for m in TOKEN_BG_RE.finditer(css)})


def _resolve(css_vars: dict[str, str], value: str, depth: int = 0) -> str:
    v = value.strip()
    m = re.match(r"var\((--[\w-]+)\)", v)
    if m and depth < 6:
        return _resolve(css_vars, css_vars.get(m.group(1), v), depth + 1)
    return v


def _first_hex(value: str) -> str | None:
    m = HEX_RE.search(value)
    return m.group(0) if m else None


def page_attributes(sample_dir: str) -> dict:
    """Extract the four attributes from a run dir (preview.html + tokens.css)."""
    html_path = os.path.join(sample_dir, "preview.html")
    html = open(html_path, encoding="utf-8", errors="ignore").read() if os.path.isfile(html_path) else ""
    tokens_css = ""
    for cand in ("tokens.css",):
        p = os.path.join(sample_dir, cand)
        if os.path.isfile(p):
            tokens_css = open(p, encoding="utf-8", errors="ignore").read()
    inline = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", html, re.S | re.I))
    css = tokens_css + "\n" + inline

    title_font = body_font = "unspecified"
    for m in SEL_FONT_BLOCK_RE.finditer(inline + "\n" + tokens_css):
        fam = FONT_RE.search(m.group(2))
        if fam:
            if m.group(1).lower() == "h1":
                title_font = _first_font(fam.group(1))
            else:
                body_font = _first_font(fam.group(1))
    if title_font == "unspecified":
        dm = re.search(r"--font-display\s*:\s*([^;]+)", css)
        title_font = _first_font(dm.group(1)) if dm else "unspecified"
    if body_font == "unspecified":
        bm = re.search(r"--font-body\s*:\s*([^;]+)", css)
        body_font = _first_font(bm.group(1)) if bm else "unspecified"

    accent_var, bg_var = _color_tokens(css)
    accent_hex = _first_hex(_resolve(accent_var, next(iter(accent_var.values())) if accent_var else "")) \
        or next((h for h in HEX_RE.findall(css)), None)
    accent = "unspecified"
    if accent_hex:
        r, g, b = _hex_to_rgb(accent_hex)
        h, _s, _l = _rgb_to_hsl(r, g, b)
        accent = hue_family(h, (max(r, g, b) - min(r, g, b)) / 255)

    bg = "unspecified"
    bg_val = ""
    if bg_var:
        first = sorted(bg_var.items())[0][1]
        bg_val = _resolve(bg_var, first)
    if not bg_val:
        bm = BG_CSS_RE.search(inline)
        bg_val = bm.group(1) if bm else ""
    bg_hex = _first_hex(bg_val)
    if bg_hex:
        r, g, b = _hex_to_rgb(bg_hex)
        h, _s, l = _rgb_to_hsl(r, g, b)
        bg = bg_family(h, (max(r, g, b) - min(r, g, b)) / 255, l)

    return {"title_font": title_font, "body_font": body_font,
            "accent": accent, "background": bg}


def shared_axes(a: dict, b: dict) -> list[str]:
    return [k for k in a if a[k] == b[k]]


def selftest() -> int:
    import tempfile
    fails = []

    def check(name, ok, detail=""):
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f": {detail}" if detail else ""))
        if not ok:
            fails.append(name)

    tmp = tempfile.mkdtemp(prefix="divergence-selftest-")
    pages = {
        "warm-serif": ("Libre Caslon Text", "Libre Caslon Text", "#93432d", "#f8f3eb"),
        "cool-mono": ("IBM Plex Mono", "Inter", "#2563eb", "#0c0f14"),
        "same-as-warm": ("Libre Caslon Text", "Libre Caslon Text", "#93432d", "#f8f3eb"),
    }
    attrs = {}
    for name, (disp, body, accent, bg) in pages.items():
        d = os.path.join(tmp, name)
        os.makedirs(d)
        open(os.path.join(d, "tokens.css"), "w").write(
            f":root{{--font-display:'{disp}';--font-body:'{body}';"
            f"--color-accent:{accent};--bg:{bg};}}\n")
        open(os.path.join(d, "preview.html"), "w").write(
            f"<html><head><title>{name}</title></head><body style='background:{bg}'></body></html>")
        attrs[name] = page_attributes(d)

    check("warm-serif attributes extracted",
          attrs["warm-serif"] == {"title_font": "libre caslon text", "body_font": "libre caslon text",
                                  "accent": "red", "background": "light-neutral"}, str(attrs["warm-serif"]))
    check("cool-mono attributes extracted",
          attrs["cool-mono"] == {"title_font": "ibm plex mono", "body_font": "inter",
                                 "accent": "blue", "background": "dark-neutral"}, str(attrs["cool-mono"]))
    check("identical pages share all four axes",
          len(shared_axes(attrs["warm-serif"], attrs["same-as-warm"])) == 4)
    check("distinct pages share at most one axis",
          len(shared_axes(attrs["warm-serif"], attrs["cool-mono"])) <= 1,
          str(shared_axes(attrs["warm-serif"], attrs["cool-mono"])))
    import shutil
    shutil.rmtree(tmp, ignore_errors=True)
    print("SELFTEST " + ("PASSED" if not fails else f"FAILED ({len(fails)})"))
    return 0 if not fails else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="four-attribute divergence across generated pages")
    ap.add_argument("dirs", nargs="*", help="sample directories (preview.html + tokens.css)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if len(a.dirs) < 2:
        ap.error("give at least two sample directories (or --selftest)")
    attrs = {}
    for d in a.dirs:
        try:
            attrs[os.path.basename(d.rstrip('/\\')) or d] = page_attributes(d)
        except OSError as e:
            print(f"unreadable sample {d}: {e}", file=sys.stderr)
            return 2
    names = sorted(attrs)
    print(f"{'page':<24} {'title font':<22} {'body font':<22} {'accent':<10} background")
    for n in names:
        v = attrs[n]
        print(f"{n:<24} {v['title_font']:<22} {v['body_font']:<22} {v['accent']:<10} {v['background']}")
    print("\npairwise shared axes (0-1 distinct, 2 borderline, 3-4 same face):")
    worst = 0
    for i, n1 in enumerate(names):
        for n2 in names[i + 1:]:
            sh = shared_axes(attrs[n1], attrs[n2])
            worst = max(worst, len(sh))
            print(f"  {n1} × {n2}: {len(sh)} shared {sh if sh else '(fully distinct)'}")
    for k in ("title_font", "body_font", "accent", "background"):
        uniq = len({attrs[n][k] for n in names})
        print(f"attribute {k}: {uniq} distinct value(s) across {len(names)} pages")
    print(f"\nworst pair shares {worst}/4 axes — distinctiveness is a separate outcome from brief fit")
    return 0


if __name__ == "__main__":
    sys.exit(main())
