#!/usr/bin/env python3
"""check_contrast.py — WCAG 2.2 contrast checker for the glasspring skill.

Accepts hex (#RGB/#RRGGBB), rgb()/rgba() (alpha composites over the background
before measuring, which is what glass tints need), and oklch()/oklab().

Key rule for glass: text contrast must be computed against the WORST-CASE
composite background (tint composited over the brightest/darkest content that
can scroll underneath), not the average backdrop. Use --composites for that.

Reference anchors from [WCAG 2.2 contrast minimum](https://www.w3.org/TR/WCAG22/#contrast-minimum):
  #000 on #FFF -> 21.0 ; #767676 on #FFF -> ~4.54 ; large-text threshold 3.0.

Usage:
  python check_contrast.py --selftest
  python check_contrast.py --fg "#1a1a1a" --bg "#ffffff"
  python check_contrast.py --fg "#fff" --bg "#ffb8b8" --large        # 3.0 threshold
  python check_contrast.py --fg white --composites "#ffd400,#111111" --tint "rgba(20,22,30,0.72)"
      # composites the tint over each listed backdrop, takes worst case
"""
from __future__ import annotations
import argparse, math, os, re, sys

AA, AAA, AA_LARGE = 4.5, 7.0, 3.0

# ---------- parsing ----------
_HEX = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")
_FUNCT = re.compile(r"^(rgb|rgba|oklch|oklab|hsl)\(", re.I)
_NAMED = {"white": "#ffffff", "black": "#000000", "red": "#ff0000", "green": "#008000", "blue": "#0000ff",
          "yellow": "#ffff00", "orange": "#ffa500", "gray": "#808080", "grey": "#808080"}


def _hsl_to_rgb(h, s, l):
    def f(n):
        k = (n + h / 30.0) % 12
        a = s * min(l, 1 - l)
        return l - a * max(-1, min(k - 3, 9 - k, 1))
    return f(0), f(8), f(4)


def _oklab_to_linear_srgb(L, a, b):
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l_, m_, s_ = l_ ** 3, m_ ** 3, s_ ** 3
    return (+4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_,
            -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_,
            -0.0041960863 * l_ - 0.7034186147 * m_ + 1.7076147010 * s_)


def parse_color(spec: str) -> tuple[float, float, float, float]:
    """-> (r, g, b) each 0..1, plus alpha."""
    spec = spec.strip().lower()
    if spec in _NAMED:
        spec = _NAMED[spec]
    if _HEX.match(spec):
        h = spec[1:]
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        return (int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255, 1.0)
    if not _FUNCT.match(spec):
        raise ValueError(f"unsupported color: {spec!r}")
    inner = spec[spec.index("(") + 1: spec.rindex(")")]
    parts = [p.strip() for p in re.split(r"[,\s/]+", inner) if p.strip()]
    alpha = 1.0
    if len(parts) >= 4:
        a = parts[3]
        alpha = float(a[:-1]) / 100.0 if a.endswith("%") else float(a)
    fn = spec[: spec.index("(")]
    nums = []
    for p in parts[:3]:
        if p.endswith("%"):
            nums.append(float(p[:-1]) / 100.0)
        else:
            nums.append(float(p))
    if fn in ("rgb", "rgba"):
        vals = [n / 255.0 if n > 1 else n for n in nums]
        return vals[0], vals[1], vals[2], alpha
    if fn == "hsl":
        r, g, b = _hsl_to_rgb(nums[0], max(0.0, min(1.0, nums[1])), max(0.0, min(1.0, nums[2])))
        return r, g, b, alpha
    if fn == "oklch":
        h = math.radians(nums[2])
        r, g, b = _oklab_to_linear_srgb(nums[0], nums[1] * math.cos(h), nums[1] * math.sin(h))
    elif fn == "oklab":
        r, g, b = _oklab_to_linear_srgb(*nums)
    else:
        raise ValueError(f"unsupported function: {fn}")
    # _oklab_to_linear_srgb returns LINEAR sRGB; the rest of this module expects
    # gamma-encoded values. Encode here or luminance() would double-decode
    # Regression guard: convert linear channels to encoded sRGB exactly once.
    return (_enc(max(0.0, min(1.0, r))), _enc(max(0.0, min(1.0, g))),
            _enc(max(0.0, min(1.0, b))), alpha)


def composite(fg_rgba, bg_rgb01):
    """alpha-composite fg over bg -> opaque rgb 0..1"""
    (fr, fg_, fb, fa), (br, bgc, bb) = fg_rgba, bg_rgb01
    out = 1.0 - fa
    return (fr * fa + br * out, fg_ * fa + bgc * out, fb * fa + bb * out)


# ---------- M3-style closed-form tone solver (advisory) ----------
# Same closed form as material-color-utilities Contrast.lighter/darker
# (fetched 2026-10-18), expressed in WCAG relative-luminance space so it is
# exact against this script's ratio() — no cross-color-space error.
# Replaces the manual step-L search runs 14/19/30 all performed by hand.
def _lstar_from_y(y: float) -> float:
    """CIE Lab L* from normalized luminance (D65 white = 1.0)."""
    if y <= 0.008856:
        return max(0.0, 903.3 * y)
    return 116.0 * (y ** (1.0 / 3.0)) - 16.0


def tone_for_ratio(bg_lum: float, ratio_target: float, direction: str) -> float:
    """Lab L* (tone) the text needs against bg luminance to hit ratio_target.
    direction: 'darker' (text darker than bg, the usual light-theme case) or
    'lighter'. Exact algebra of (Yt + 0.05)/(Ybg + 0.05) = ratio; clamped 0-100."""
    if direction == "lighter":
        yt = ratio_target * (bg_lum + 0.05) - 0.05
    else:
        yt = (bg_lum + 0.05) / ratio_target - 0.05
    if yt <= 0:
        return 0.0
    return max(0.0, min(100.0, _lstar_from_y(yt)))


# ---------- WCAG math ----------
def _lin(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _enc(c: float) -> float:
    """gamma-encode a LINEAR value (inverse of _lin) — oklch/oklab paths need this."""
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def luminance(rgb01) -> float:
    r, g, b = (_lin(c) for c in rgb01)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(l1: float, l2: float) -> float:
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def ratio(fg_spec: str, bg_spec: str) -> float:
    f = parse_color(fg_spec)
    b = parse_color(bg_spec)
    f2 = composite(f, b[:3]) if f[3] < 1.0 else f[:3]
    return contrast(luminance(f2), luminance(b[:3]))


def judge(r: float, large: bool, aaa: bool) -> str:
    need = AA_LARGE if large else (AAA if aaa else AA)
    tag = "AAA" if aaa else ("AA-large" if large else "AA")
    if r >= need:
        extra = ""
        if not aaa and not large and r >= AAA:
            extra = " (also AAA)"
        return f"PASS {tag}{extra}"
    return f"FAIL {tag} (need {need}:1)"


# ---------- APCA (informational supplement; gate stays WCAG 2.2) ----------
# Port of APCA-W3 0.1.9 (apca-w3.js 0.0.98G-4g formula), constants transcribed
# from the reference source (Myndex/APCA-W3, fetched 2026-10-17) and verified
# against it by running the reference itself on the selftest pairs.
# Guideline: APCA Readability Criterion, Bronze Simple Mode thresholds —
# body text Lc >= 75 (preferred 90), other content text >= 60,
# large fluent (>36px) >= 45 (readtech.org/ARC, fetched 2026-10-17).
def apca_lc(txt_rgb_255: tuple, bg_rgb_255: tuple) -> float:
    main_trc = 2.4
    sco = (0.2126729, 0.7151522, 0.0721750)
    norm_bg, norm_txt, rev_txt, rev_bg = 0.56, 0.57, 0.62, 0.65
    blk_thrs, blk_clmp = 0.022, 1.414
    scale = 1.14
    lo_offset, lo_clip, dy_min = 0.027, 0.1, 0.0005

    def y(rgb):
        return sum(c * (v / 255.0) ** main_trc for c, v in zip(sco, rgb))

    def soft(v):
        return v if v > blk_thrs else v + (blk_thrs - v) ** blk_clmp

    ty, by = soft(y(txt_rgb_255)), soft(y(bg_rgb_255))
    if abs(by - ty) < dy_min:
        return 0.0
    if by > ty:  # BoW (normal polarity, positive)
        sapc = (by ** norm_bg - ty ** norm_txt) * scale
        return 0.0 if sapc < lo_clip else (sapc - lo_offset) * 100.0
    sapc = (by ** rev_bg - ty ** rev_txt) * scale
    return 0.0 if sapc > -lo_clip else (sapc + lo_offset) * 100.0


def apca_bronze(lc: float, large: bool = False) -> str:
    """Bronze Simple Mode mapping (body 75 / other 60 / large 45)."""
    need = 45.0 if large else 75.0
    label = "large-fluent" if large else "body"
    if abs(lc) >= need:
        return f"bronze-{label} PASS (|Lc|>={need:.0f})"
    return f"bronze-{label} below (|Lc|<={need:.0f} — {label} needs >= {need:.0f})"


# ---------- selftest ----------
def selftest() -> int:
    fails = []

    def check(name, got, want, tol):
        ok = abs(got - want) <= tol
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}: got {got:.4f}, want {want:.4f} (+/-{tol})")
        if not ok:
            fails.append(name)

    print("selftest: WCAG known anchors")
    check("#000 vs #fff", ratio("#000000", "#ffffff"), 21.0, 0.01)
    check("#767676 vs #fff", ratio("#767676", "#ffffff"), 4.54, 0.01)
    check("same color", ratio("#fff", "#fff"), 1.0, 0.001)
    check("named colors", ratio("white", "black"), 21.0, 0.01)
    print("selftest: formats")
    check("oklch white vs black", ratio("oklch(1 0 0)", "oklch(0 0 0)"), 21.0, 0.05)
    # Discriminating anchor: oklab L=0.5 gray == #636363
    # (oklab L is perceptual, NOT sRGB percentage); the double-gamma bug read it
    # as ~16.7:1 — this anchor fails if oklch paths decode luminance twice.
    check("oklch mid-gray == #636363 (gamma roundtrip)",
          ratio("oklch(0.5 0 0)", "#ffffff"), ratio("#636363", "#ffffff"), 0.05)
    check("rgba composite white/2 over black", ratio("rgba(255,255,255,0.5)", "#000000"),
          contrast(luminance((1.0, 1.0, 1.0) if False else composite((1, 1, 1, 0.5), (0, 0, 0))), 0.0), 0.001)
    check("hsl red vs white", ratio("hsl(0 100% 50%)", "#ffffff"), ratio("#ff0000", "#ffffff"), 0.01)
    print("selftest: thresholds")
    check("large threshold constant", AA_LARGE, 3.0, 0.0)

    print("selftest: APCA 0.0.98G-4g anchors (reference values from apca-w3 0.1.9 run)")
    hw = apca_lc((0, 0, 0), (255, 255, 255))
    check("APCA black on white", hw, 106.041, 0.2)
    check("APCA white on black", apca_lc((255, 255, 255), (0, 0, 0)), -107.885, 0.2)
    check("APCA #757575 on white", apca_lc((0x75, 0x75, 0x75), (255, 255, 255)), 72.032, 0.2)
    # polarity asymmetry: same pair reversed differs (WoB magnitude larger) —
    # the property WCAG 2 ratio cannot express and the reason APCA supplements it
    rev = abs(apca_lc((255, 255, 255), (0x75, 0x75, 0x75)))
    check("APCA polarity asymmetry", rev - apca_lc((0x75, 0x75, 0x75), (255, 255, 255)), 5.456, 0.3)
    print("selftest: APCA Bronze mapping constants")
    ok = (apca_bronze(76).startswith("bronze-body PASS")
          and apca_bronze(74).startswith("bronze-body below")
          and apca_bronze(46, large=True).startswith("bronze-large-fluent PASS")
          and apca_bronze(44, large=True).startswith("bronze-large-fluent below"))
    print(f"  [{'PASS' if ok else 'FAIL'}] bronze mapping (body 75 / large 45)")
    if not ok:
        fails.append("bronze-mapping")

    print("selftest: M3-style tone solver (advisory; formulas per material-color-utilities Contrast)")
    # anchor 1 (discriminating, known value): white bg @ 4.5 → darker-text tone ≈ 49.9
    # (the L* of #767676, the canonical "4.54:1 gray") — cross-validated against ratio()
    tone = tone_for_ratio(luminance((1.0, 1.0, 1.0)), 4.5, "darker")
    ok = abs(tone - 49.9) <= 0.3
    print(f"  [{'PASS' if ok else 'FAIL'}] tone for 4.5 on white ≈ 49.9: {tone:.2f}")
    if not ok:
        fails.append("tone-white")
    # anchor 2: solver round-trips through ratio() — the gray whose luminance
    # equals the solved Yt must measure exactly the requested ratio
    yt = (1.0 + 0.05) / 4.5 - 0.05  # exact Yt for 4.5 on white (darker text)
    hx = "#%02X%02X%02X" % tuple(round(_enc(yt) * 255) for _ in range(3))
    rt = ratio(hx, "#ffffff")
    ok = abs(rt - 4.5) <= 0.06  # 8-bit hex quantization noise at this luminance ≈ ±0.03
    print(f"  [{'PASS' if ok else 'FAIL'}] solver round-trip: gray at solved Yt measures 4.50:1: {rt:.3f}:1 ({hx})")
    if not ok:
        fails.append("tone-roundtrip")
    # anchor 3: lighter direction on black bg @ 4.5 → text luminance 0.175 → L* ≈ 48.9
    tone2 = tone_for_ratio(luminance((0.0, 0.0, 0.0)), 4.5, "lighter")
    ok = abs(tone2 - 48.9) <= 0.3
    print(f"  [{'PASS' if ok else 'FAIL'}] tone for 4.5 on black ≈ 48.9: {tone2:.2f}")
    if not ok:
        fails.append("tone-black")

    print("selftest: fg_alpha compositing (AD2 real-render gate)")
    import json as _json, tempfile as _tf, os as _os
    _pairs = [{"label": "ink-fill 45% start on white (large-text floor claim)",
               "fg": "#111111", "bg": "#ffffff", "fg_alpha": 0.45, "large": True}]
    _fd, _p = _tf.mkstemp(suffix=".json")
    _os.close(_fd)
    with open(_p, "w", encoding="utf-8") as _fh:
        _fh.write(_json.dumps(_pairs))
    import io as _io, contextlib as _cl
    _buf = _io.StringIO()
    with _cl.redirect_stdout(_buf):
        _rc = batch_pairs(_p)
    _out = _buf.getvalue()
    _os.remove(_p)
    # 45% ink on white ≈ 3:1 —— AE7/ink-fill "约 3:1，大字可读" 声称的机械验证
    _ok = _rc == 0 and "PASS" in _out and "fg @45%" in _out
    print(f"  [{'PASS' if _ok else 'FAIL'}] fg_alpha 45% ink on white passes large-text floor")
    if not _ok:
        fails.append("fg_alpha floor")
        print(_out)

    print("selftest: --pairs batch mode")
    import json as _json
    import tempfile
    with tempfile.TemporaryDirectory() as tdir:
        pf = os.path.join(tdir, "pairs.json")
        _json.dump([
            {"label": "ink/paper", "fg": "#111111", "bg": "#faf7f2"},
            {"label": "deliberate-fail", "fg": "#cccccc", "bg": "#ffffff"},
            {"label": "glass-nav", "fg": "#111111", "bg": "#000000",
             "tint": "rgba(255,255,255,0.72)", "composites": "#ffffff,#000000"},
        ], open(pf, "w", encoding="utf-8"))
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = batch_pairs(pf)
        out = buf.getvalue()
        ok = rc == 1 and "2/3 pass" in out and "deliberate-fail" in out and "glass-nav" in out
        print(f"  [{'PASS' if ok else 'FAIL'}] batch mixed verdicts -> exit 1 with failing label listed")
        if not ok:
            fails.append("batch-mixed")
        _json.dump([{"label": "ok", "fg": "#111111", "bg": "#faf7f2"}], open(pf, "w", encoding="utf-8"))
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = batch_pairs(pf)
        ok = rc == 0 and "1/1 pass" in buf.getvalue()
        print(f"  [{'PASS' if ok else 'FAIL'}] batch all-pass -> exit 0")
        if not ok:
            fails.append("batch-pass")

    if fails:
        print(f"SELFTEST FAILED: {fails}")
        return 1
    print("SELFTEST PASSED (all anchors green)")
    return 0


def _apca_note(fg_rgb, bg_rgb, large: bool) -> str:
    """Informational APCA line — never affects the WCAG gate exit code."""
    rgb255 = tuple(round(c * 255) for c in fg_rgb), tuple(round(c * 255) for c in bg_rgb)
    lc = apca_lc(*rgb255)
    if lc == 0.0:
        return "apca Lc 0 (below perceptual delta)"
    pol = "BoW" if lc > 0 else "WoB"
    return f"apca Lc {lc:.1f} ({pol}; {apca_bronze(abs(lc), large)}) — informational, gate stays WCAG 2.2"


def batch_pairs(path: str) -> int:
    """--pairs batch mode: one JSON file and one pass/fail summary. JSON schema:
    [ {"label":"ink/paper","fg":"...","bg":"...","large":false,"aaa":false,
       "tint":null,"composites":null} ]  — tint+composites = glass worst case."""
    import json
    try:
        with open(path, encoding="utf-8") as _pf:
            pairs = json.load(_pf)
    except (OSError, ValueError) as e:
        print(f"pairs file error: {e}")
        return 1
    fails = []
    for p in pairs:
        label = p.get("label", f'{p["fg"]} on {p["bg"]}')
        large, aaa = bool(p.get("large")), bool(p.get("aaa"))
        try:
            eff_bg = None
            if p.get("composites") and p.get("tint"):
                t = parse_color(p["tint"])
                worst_r = float("inf")
                for bg in p["composites"].split(","):
                    b = parse_color(bg)
                    eff = composite(t, b[:3])
                    worst_r = min(worst_r, contrast(luminance(composite(parse_color(p["fg"]), eff)),
                                                    luminance(eff)))
                r = worst_r
                eff_bg = eff  # APCA note measures the same worst-case backdrop
                note = f" (glass worst-case over {p['composites']})"
                eff_fg = p["fg"]
            else:
                r = ratio(p["fg"], p["bg"])
                eff_bg = parse_color(p["bg"])
                note = ""
            eff_fg = p["fg"]
        except Exception as e:  # noqa: BLE001 - a bad pair must not kill the batch
            print(f"  [ERROR] {label}: {e}")
            fails.append(label)
            continue
        if p.get("fg_alpha") is not None:
            # AD2 (ux-ui real-render gate 竞品研读 2026-10-20): 文字自身带透明度压在
            # （可能已合成的）背景上——ink-fill 45% 起步、变暗地板等规则的机械验证。
            a_f = float(p["fg_alpha"])
            frgb = parse_color(p["fg"])[:3]
            eff_fg_rgb = composite((frgb[0], frgb[1], frgb[2], a_f), eff_bg[:3])
            r = contrast(luminance(eff_fg_rgb), luminance(eff_bg[:3]))
            eff_fg = "rgb(" + ",".join(str(round(c * 255)) for c in eff_fg_rgb) + ")"
            note += f" (fg @{int(round(a_f * 100))}% over bg)"
        verdict = judge(r, large, aaa)
        need = AA_LARGE if large else (AAA if aaa else AA)
        ok = r >= need
        lc_line = ""
        try:
            lc = apca_lc(tuple(round(c * 255) for c in parse_color(eff_fg)),
                         tuple(round(c * 255) for c in eff_bg))
            lc_line = f" | Lc {lc:.0f}"
        except Exception:
            pass
        print(f"  [{'PASS' if ok else 'FAIL'}] {label}: {r:.2f}:1 {verdict}{note}{lc_line}")
        if not ok:
            fails.append(label)
    print(f"batch: {len(pairs) - len(fails)}/{len(pairs)} pass" +
          (f"; failing: {', '.join(fails)}" if fails else ""))
    return 1 if fails else 0


def main() -> int:
    ap = argparse.ArgumentParser(description="WCAG 2.2 contrast checker (hex/rgb/rgba/oklch/oklab/hsl)")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--fg", help="foreground color")
    ap.add_argument("--bg", help="background color")
    ap.add_argument("--composites", help="comma-separated backdrops; composites any translucent --tint over each and takes the WORST case (glass rule)")
    ap.add_argument("--tint", help="glass tint color, e.g. rgba(20,22,30,0.72)")
    ap.add_argument("--large", action="store_true", help="large text (>=24px or >=18.66px bold): 3.0")
    ap.add_argument("--aaa", action="store_true", help="AAA threshold (7.0)")
    ap.add_argument("--pairs", help='batch mode: JSON file — schema: [{"label":"ink/bg","fg":"#111","bg":"#fff","large":false,"aaa":false, "tint":"optional","composites":"#fff,#000"}] (top-level array)')
    ap.add_argument("--tone-for", type=float, metavar="RATIO",
                    help="advisory: with --bg, print the Lab tone (L*) text needs on that background to reach RATIO — replaces manual step-L search (M3-style closed form)")
    a = ap.parse_args()

    if a.selftest:
        return selftest()
    if a.pairs:
        return batch_pairs(a.pairs)
    if a.tone_for is not None:
        if not a.bg:
            ap.error("--tone-for requires --bg")
        bg_y = luminance(parse_color(a.bg)[:3])
        for direction in ("lighter", "darker"):
            t = tone_for_ratio(bg_y, a.tone_for, direction)
            print(f"  tone (L*) for {direction} text at {a.tone_for}:1 on {a.bg} -> {t:.1f}"
                  + ("  (oklch L ≈ this value, step L and re-measure to confirm)" if t > 0 else "  (unreachable on this bg)"))
        return 0
    if not a.fg:
        ap.error("--fg required (or --selftest)")

    if a.composites:
        if not a.tint:
            ap.error("--composites requires --tint (the glass surface tint)")
        t = parse_color(a.tint)
        worst_name, worst_r = None, float("inf")
        for bg in a.composites.split(","):
            b = parse_color(bg)
            eff = composite(t, b[:3])
            r = contrast(luminance(composite(parse_color(a.fg), eff)), luminance(eff))
            print(f"  backdrop {bg.strip():>9} -> effective bg #{''.join(f'{round(c*255):02X}' for c in eff)}  ratio {r:.2f}:1")
            if r < worst_r:
                worst_name, worst_r = bg.strip(), r
        verdict = judge(worst_r, a.large, a.aaa)
        print(f"WORST CASE: {worst_name} at {worst_r:.2f}:1 -> {verdict}")
        return 0 if worst_r >= (AA_LARGE if a.large else (AAA if a.aaa else AA)) else 1

    r = ratio(a.fg, a.bg)
    verdict = judge(r, a.large, a.aaa)
    print(f"contrast {a.fg} on {a.bg} = {r:.2f}:1 -> {verdict}")
    try:
        print(f"  {_apca_note(parse_color(a.fg), parse_color(a.bg), bool(a.large))}")
    except Exception:  # APCA note must never break the WCAG-gated CLI path
        pass
    return 0 if r >= (AA_LARGE if a.large else (AAA if a.aaa else AA)) else 1


if __name__ == "__main__":
    sys.exit(main())
