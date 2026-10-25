#!/usr/bin/env python3
"""palette_from_oklch.py — brand-DNA color engine for the glasspring skill.

The L3-compliance re-derivation engine (charter §2.1): given a brand seed it
REDERIVES a full OKLCH ramp — values are computed, never copied — and emits
CSS custom properties with hex fallbacks plus contrast-verification hints.

Usage:
  python palette_from_oklch.py --selftest
  python palette_from_oklch.py --seed "#4f8cff"            # derive everything
  python palette_from_oklch.py --seed "#4f8cff" --css      # emit :root block
  python palette_from_oklch.py --hue 152 --chroma 0.12     # explicit OKLCH seed

Selftest anchors (verified against the oklab standard, Björn Ottosson):
  oklch(0.5, 0, 0)  -> #636363   (a discriminating conversion anchor)
  #4f8cff           -> roundtrip through oklch and back, same hex
"""
from __future__ import annotations
import argparse, colorsys, math, sys

# ---- sRGB <-> linear ----
def _lin(c): return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
def _enc(c): return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055

# ---- oklab standard ----
def srgb_to_oklab(r, g, b):
    r, g, b = _lin(r), _lin(g), _lin(b)
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = l ** (1 / 3), m ** (1 / 3), s ** (1 / 3)
    return (0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
            1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
            0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_)

def oklab_to_linear_srgb(L, a, b):
    l_ = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m_ = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s_ = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    return (+4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_,
            -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_,
            -0.0041960863 * l_ - 0.7034186147 * m_ + 1.7076147010 * s_)

def hex_to_rgb(h):
    h = h.lstrip("#")
    if len(h) == 3: h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return "#" + "".join(f"{round(max(0, min(1, c)) * 255):02X}" for c in rgb)

def oklch_to_hex(L, C, H_deg):
    h = math.radians(H_deg)
    r, g, b = oklab_to_linear_srgb(L, C * math.cos(h), C * math.sin(h))
    return rgb_to_hex(tuple(_enc(max(0.0, min(1.0, c))) for c in (r, g, b)))

def hex_to_oklch(h):
    L, a, b = srgb_to_oklab(*hex_to_rgb(h))
    return L, math.hypot(a, b), math.degrees(math.atan2(b, a)) % 360

# ---- ramp construction (tokens.md §2 L-steps) ----
RAMP = [  # (step, L, chroma) — chroma tapers toward the extremes (gamut + taste)
    ("50", 0.97, 0.02), ("100", 0.93, 0.05), ("300", 0.80, 0.11),
    ("500", 0.63, 0.17), ("700", 0.48, 0.15), ("900", 0.32, 0.09),
]
NEUTRAL_CHROMA_MAX = 0.015

def derive(seed_hex: str, neutral: bool = False):
    L0, C0, H0 = hex_to_oklch(seed_hex)
    chroma = min(C0, 0.30) if not neutral else min(C0, NEUTRAL_CHROMA_MAX)
    name = "neutral" if neutral else "accent"
    out = []
    for step, L, C in RAMP:
        c = min(C, chroma) if not neutral else min(NEUTRAL_CHROMA_MAX, chroma)
        out.append((f"--pr-{name}-{step}", L, round(c, 3), round(H0, 1), oklch_to_hex(L, c, H0)))
    return out

def emit_css(ramps):
    lines = [":root {"]
    for var, L, C, H, hx in ramps:
        lines.append(f"  {var}: oklch({L} {C} {H});  /* {hx} */")
    lines.append("}")
    return "\n".join(lines)

# ---- style-pack scaffold table ----
# Facts below are quoted from references/style-packs/<name>.md — re-verified
# against the cards on 2026-10-17. The emitted file is a STARTER: the agent
# must still read the pack (provenance, rules, a11y floors live there, not here).
SCAFFOLDS = {
    "linear-instrument": dict(hue=238.0, chroma=0.14, neutral_hue=238.0,
        glass="none — style excludes glass (never); if user insists use Tier 1 and log the conflict",
        radius=None, notes=["dark instrument dashboard", "single accent", "mono/tabular data"]),
    "notion-paper": dict(hue=80.0, chroma=0.006, neutral_hue=80.0,
        glass="none (never)",
        radius="4-6px; near-zero shadows — one micro shadow only for floating menus",
        notes=["block editor grammar", "gray-fill hierarchy (no borders)", "restrained link green"]),
    "swiss-international": dict(hue=14.0, chroma=0.17,
        glass="floating layers only; body/headline zones never",
        radius="0-2px sharp; shadow blur <= 8px; motion linear, no bounce",
        notes=["asymmetric grid", "red as punctuation only", "mono captions"]),
    "brutalist-web": dict(seed="#0000FF",
        glass="none — absolute mutual exclusion",
        radius="0px site-wide; no shadows/gradients/translucency; motion = instant invert only",
        notes=["raw structure with 2-3px black borders", "system fonts", "flat color blocks"]),
    "editorial-magazine": dict(seed="#722F37",
        glass="none (mutually exclusive with print tradition)",
        radius="no rounded cards — print has none",
        notes=["serif body mandatory", "hairline rules rhythm", "drop caps"],
        measured_final="burgundy final oklch(0.34 0.07 13) — seed here IS the measured final"),
    "dark-academia": dict(seed="#6D2E2E",
        glass="none (parchment absorbs light — optically incompatible)",
        radius=None, notes=["serif rule + double-rule dividers", "oxblood quotes", "latin section numbering"]),
    "organic-natural": dict(seed="#8B4A2B",
        glass="none (material semantics conflict)",
        radius="10-16px organic; asymmetric leaf corners e.g. 24px 4px 24px 24px",
        notes=["dual green system", "whitespace >= 40%", "earthy status colors — never pure red/green"]),
    "warm-soft-saas": dict(seed="#58cc02", neutral_hue=85.0,
        glass="none (never — friendly-solid and translucent conflict)",
        radius="cards 16-20px; buttons fully round; icon tiles rounded fills",
        notes=["green 500 = surface/icon only, ZERO text on it (3.28 FAIL)", "buttons #348400 + white 4.72 AA",
               "2px+ solid borders, never hairline; 4px solid offset button shadow, no blur"],
        measured_final="btn green oklch(0.54 0.17 137.6) #348400; text green oklch(0.48 0.15 137.6) #2B7000"),
    "dark-cinematic": dict(hue=250.0, chroma=0.15, neutral_hue=250.0,
        glass="at most once per page, never stacked with glow/gradient (one-effect budget)",
        radius="4-10px sharp; glow-as-shadow single use 0 0 80px signal @15-20%",
        notes=["void layering L0.10/0.155/0.21 — never #000", "signal <= 3 occurrences, on-signal text = void black",
               "support colors desaturated C<=0.04; signal is brand-variable (demo hue 230)"],
        measured_final="void oklch(0.100 0.004 250) #030304; text #E9EBEE 17.26 AAA; demo signal #00AEE9 8.08 AA"),
    "soft-premium": dict(hue=155.0, chroma=0.05, neutral_hue=84.6,
        glass="none (Editorial Luxury archetype — glass belongs to the Ethereal sibling, never mixed)",
        radius="4-8px; ultra-soft ambient shadows only (opacity <0.05); film-grain fixed layer 0.03",
        notes=["sage dual-track: deco L0.62 large-elements-only, text L0.48 6.13 AA",
               "serif display vs sans body size contrast >=3x", "sections separated by py-24+ whitespace"],
        measured_final="bg oklch(0.985 0.006 84.6) #FCFAF6; ink espresso oklch(0.28 0.035 55) #362418 14.16 AAA"),
    "soft-structural": dict(hue=250.0, chroma=0.12, neutral_hue=250.0,
        glass="none (soft edge comes from diffused shadow, not translucency)",
        radius="8-12px; diffused non-directional double shadow 40/80px @0.04-0.06, never offset",
        notes=["swiss grid discipline kept, edges softened — radius 8-12px is the clan mark",
               "massive grotesk 800-900 carries all drama, size jump >=3x, second-order-convergence check",
               "accent <=3 occurrences; no punctuating red (swiss-only)"],
        measured_final="bg oklch(0.965 0.005 250) #F1F4F7; ink oklch(0.25 0.01 250) #1E2226 14.50 AAA; accent #2266A4 5.43 AA"),
    "ethereal-glass": dict(hue=210.0, chroma=0.10, neutral_hue=250.0,
        glass="the material IS the style — but Tier-0 veto supersedes: trust zones stay opaque; real blur on fixed chrome only, in-flow cards use fake-glass triplet",
        radius="12-16px; no shadows (invisible on void) — separation via white/9 hairline + card step",
        notes=["OLED #050505 signature; Vantablack cards #0B0D11 fake-glass triplet",
               "mesh: single hue family, <=2 radial layers @<=0.15 opacity, @supports flat-void fallback",
               "glass tint rgba(16,19,24,0.72); worst-case composite 12.20 AAA measured"],
        measured_final="text #E4E8EE 17.03 AAA; glass composite 12.20 AAA; card #0B0D11 16.25 AAA"),
}

def scaffold(name: str) -> int:
    if name not in SCAFFOLDS:
        print(f"unknown style '{name}'. known: {', '.join(sorted(SCAFFOLDS))}")
        return 1
    s = SCAFFOLDS[name]
    if "seed" in s:
        ramps = derive(s["seed"])
        seed_desc = f"seed {s['seed']}"
    else:
        ramps = derive_from_hue(s["hue"], s["chroma"])
        seed_desc = f"hue {s['hue']} C{s['chroma']}"
    if s.get("neutral_hue") is not None:
        ramps = ramps + derive_from_hue(s["neutral_hue"], NEUTRAL_CHROMA_MAX, neutral=True)
    print(f"/* ============================================================")
    print(f"   tokens.css STARTER — style pack '{name}' (scaffold, not final)")
    print(f"   seed: {seed_desc} | engine-rederived, not copied (L3)")
    print(f"   facts as of 2026-10-17 from references/style-packs/{name}.md —")
    print(f"   READ THE PACK before shipping: provenance, rules.always/never,")
    print(f"   a11y floors and typography live there, not in this file.")
    print(f"   ============================================================ */")
    print(emit_css(ramps))
    print(f"/* glass verdict : {s['glass']} */")
    if s.get("radius"):
        print(f"/* radius/shadow : {s['radius']} */")
    for n in s.get("notes", []):
        print(f"/* note          : {n} */")
    if s.get("measured_final"):
        print(f"/* measured_final: {s['measured_final']} */")
    print(f"/* next: verify text pairs -> check_contrast.py (--pairs batch), then read the pack */")
    return 0

# ---- ramp perceptual-uniformity check (meodai/skill.color-expert 617★ criterion, 2026-10-20) ----
def check_ramp(ramps, tol_hi=1.4, tol_lo=0.6):
    """顺序色阶的平坦感知导数测试：相邻步的 OKLab ΔE 应接近平坦——凸包 = 色阶夸大了数据中
    不存在的变差（jet 的本质失败）。灰度视图（仅 L 通道差）随每步一并列出供复核。
    返回被标记的 (step_index, dE_oklab, dL) 列表；空列表 = 平坦通过。"""
    pts = []
    for _n, L, C, H, _hx in ramps:
        a, b = C * math.cos(math.radians(H)), C * math.sin(math.radians(H))
        pts.append((L, a, b))
    des = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    dls = [abs(pts[i + 1][0] - pts[i][0]) for i in range(len(pts) - 1)]
    if not des:
        return []
    med = sorted(des)[len(des) // 2]
    if med <= 0:
        return []
    # bump = 过陡（夸大战差，meodai 原文语义）；dip = 过缓（浅端锥形是 UI 色阶常规，仅提示）
    return [("bump" if de > med * tol_hi else "dip", i, round(de, 4), round(dl, 4))
            for i, (de, dl) in enumerate(zip(des, dls))
            if de > med * tol_hi or de < med * tol_lo]

# ---- selftest ----
def selftest() -> int:
    fails = []
    def check(name, ok, detail=""):
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f": {detail}" if detail else ""))
        if not ok: fails.append(name)

    print("selftest: oklab conversion anchors")
    check("oklch(0.5,0,0) -> #636363", oklch_to_hex(0.5, 0, 0) == "#636363",
          oklch_to_hex(0.5, 0, 0))
    check("oklch(1,0,0) -> #ffffff", oklch_to_hex(1, 0, 0) == "#FFFFFF")
    check("oklch(0,0,0) -> #000000", oklch_to_hex(0, 0, 0) == "#000000")

    print("selftest: seed roundtrips (in-gamut)")
    for seed in ("#4f8cff", "#22c55e", "#f59e0b"):
        L, C, H = hex_to_oklch(seed)
        back = oklch_to_hex(L, C, H)
        ok = back == seed.upper()
        check(f"roundtrip {seed}", ok, back)
        if not ok: fails.append(f"roundtrip {seed}")

    print("selftest: ramp structure")
    ramps = derive("#4f8cff")
    Ls = [L for _, L, _, _, _ in ramps]
    check("ramp has 6 steps", len(ramps) == 6)
    check("ramp lightness monotonic desc", all(Ls[i] > Ls[i+1] for i in range(len(Ls)-1)), str(Ls))
    check("all hex valid", all(re_hex(hx) for _, _, _, _, hx in ramps))
    neutrals = derive("#4f8cff", neutral=True)
    check("neutral chroma clamped", all(C <= NEUTRAL_CHROMA_MAX + 1e-9 for _, _, C, _, _ in neutrals))

    print("selftest: check_ramp perceptual flatness (meodai criterion)")
    smooth = [(f"-{i}00", 0.90 - i * 0.10, 0.12, 250.0, "#000000") for i in range(6)]
    check("check_ramp: even-L ramp is flat", check_ramp(smooth) == [], str(check_ramp(smooth)))
    tapered = [(f"-{i}00", L, 0.12, 250.0, "#000000") for i, L in enumerate([0.97, 0.94, 0.88, 0.72, 0.55, 0.42])]
    check("check_ramp: light-end taper is not a defect", all(k != "bump" for k, *_ in check_ramp(tapered)), str(check_ramp(tapered)))
    bumpy = [(f"-{i}00", L, 0.12, 250.0, "#000000") for i, L in enumerate([0.90, 0.80, 0.70, 0.40, 0.30, 0.20])]
    flagged = check_ramp(bumpy)
    check("check_ramp: mid-ramp L jump flagged as bump", any(k == "bump" and i == 2 for k, i, *_ in flagged), str(flagged))

    print("selftest: --scaffold table")
    check("scaffold covers 12 packs", set(SCAFFOLDS) == {
        "linear-instrument", "notion-paper", "swiss-international", "brutalist-web",
        "editorial-magazine", "dark-academia", "organic-natural",
        "warm-soft-saas", "dark-cinematic", "soft-premium", "soft-structural",
        "ethereal-glass"}, str(sorted(SCAFFOLDS)))
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = scaffold("brutalist-web")
    out = buf.getvalue()
    ok = (rc == 0 and "--pr-accent-50" in out and "absolute mutual exclusion" in out
          and "STARTER" in out and "references/style-packs/brutalist-web.md" in out)
    check("scaffold brutalist emits ramp + glass verdict + pack pointer", ok)
    with contextlib.redirect_stdout(buf):
        rc2 = scaffold("no-such-style")
    check("scaffold unknown name -> exit 1", rc2 == 1)

    if fails:
        print(f"SELFTEST FAILED: {fails}"); return 1
    print("SELFTEST PASSED (all anchors green)"); return 0

import re
def re_hex(s): return bool(re.match(r"^#[0-9A-F]{6}$", s))

def main() -> int:
    ap = argparse.ArgumentParser(description="brand seed -> OKLCH ramp re-derivation")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--seed", help="brand color hex")
    ap.add_argument("--hue", type=float, help="explicit OKLCH hue (deg)")
    ap.add_argument("--chroma", type=float, help="explicit OKLCH chroma")
    ap.add_argument("--css", action="store_true", help="emit :root block")
    ap.add_argument("--scaffold", metavar="STYLE", help="emit a tokens.css STARTER from a style pack (names: " + ", ".join(sorted(SCAFFOLDS)) + ")")
    ap.add_argument("--neutral", action="store_true", help="derive tinted-neutral ramp instead")
    ap.add_argument("--check-ramp", action="store_true", help="flat perceptual-derivative test on the derived ramp (OKLab dE steps; exit 1 on bumps)")
    a = ap.parse_args()

    if a.selftest: return selftest()
    if a.scaffold: return scaffold(a.scaffold)
    if a.seed:
        L0, C0, H0 = hex_to_oklch(a.seed)
        H0, C0 = (a.hue if a.hue is not None else H0), (a.chroma if a.chroma is not None else C0)
    elif a.hue is not None:
        H0, C0 = a.hue, (a.chroma if a.chroma is not None else 0.14)
    else:
        ap.error("--seed or --hue required (or --selftest)")

    ramps = derive(a.seed, neutral=a.neutral) if a.seed else derive_from_hue(H0, C0, a.neutral)
    print(f"seed hue {H0:.1f}° — derived {'neutral' if a.neutral else 'accent'} ramp (rederived, not copied):")
    print(emit_css(ramps))
    if a.check_ramp:
        flagged = check_ramp(ramps)
        bumps = [f for f in flagged if f[0] == "bump"]
        for k, i, de, dl in flagged:
            if k == "bump":
                print(f"RAMP BUMP at step {i}: dE_oklab={de} dL={dl} — 色阶在此夸大了数据中不存在的变差（tokens.md §2 平坦导数测试）")
            else:
                print(f"ramp taper at step {i}: dE_oklab={de} dL={dl} — 浅端锥形（UI 常规，非缺陷；顺序/数据色阶须消锥）")
        if bumps:
            print("exit 1: fix the ramp L spacing before shipping.")
            return 1
        print("ramp check: no perceptual bumps — PASS")
    print("\nnext: verify text pairs with check_contrast.py before shipping (tokens.md §2).")
    return 0

def derive_from_hue(H, C, neutral=False):
    chroma = min(C, 0.30)
    out = []
    for step, L, c in RAMP:
        c = min(c, chroma) if not neutral else min(NEUTRAL_CHROMA_MAX, chroma)
        out.append((f"--pr-{'neutral' if neutral else 'accent'}-{step}", L, round(c, 3), round(H, 1), oklch_to_hex(L, c, H)))
    return out

if __name__ == "__main__":
    sys.exit(main())
