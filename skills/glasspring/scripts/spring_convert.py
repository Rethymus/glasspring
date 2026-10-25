#!/usr/bin/env python3
"""spring_convert.py — spring parameter translator for the glasspring skill.

Converts between three spring parameterizations:
  * SwiftUI  Spring(duration:bounce:) / spring(response:dampingFraction:)
  * Motion (JS)  { type:'spring', bounce, visualDuration } / { stiffness, damping, mass }
  * CSS  linear() easing curve (sampled damped harmonic oscillator)

Verified anchors from Apple's [SwiftUI Spring API](https://developer.apple.com/documentation/swiftui/spring):
  Spring(duration: 0.5, bounce: 0.3)          -> (mass 1.0, stiffness ~157.9, damping ~17.6)
  Spring(mass: 1, stiffness: 100, damping:10) -> (duration ~0.63, bounce ~0.5)
  SwiftUI default  spring(response:0.5, dampingFraction:0.825)

Usage:
  python spring_convert.py --selftest
  python spring_convert.py --semantic bouncy            # named preset -> all forms
  python spring_convert.py --duration 0.5 --bounce 0.3  # SwiftUI duration form
  python spring_convert.py --response 0.5 --damping 0.825
  python spring_convert.py --mass 1 --stiffness 100 --damping 10
  python spring_convert.py --visual-duration 0.3 --bounce 0.3   # Motion visualDuration form
  python spring_convert.py --duration 0.5 --bounce 0.3 --css   # include CSS linear() string
"""
from __future__ import annotations
import argparse, json, math, sys

TAU = 2.0 * math.pi
MIN_ZETA = 0.05  # Motion's clamp (motion-dom spring.ts)

PRESETS = {  # from Apple docs (duration 0.5 for the three named presets)
    "smooth":   dict(duration=0.5, bounce=0.0),
    "snappy":   dict(duration=0.5, bounce=0.15),
    "bouncy":   dict(duration=0.5, bounce=0.3),
    "default":  dict(response=0.5, damping=0.825),          # SwiftUI .spring default
    "interactive": dict(response=0.15, damping=0.86),       # .interactiveSpring default
}


def zeta_from_bounce(bounce: float) -> float:
    """Motion's mapping (motion-dom): bounce<0 -> overdamped side, else 1-bounce."""
    if bounce < 0:
        return min(1.0 / max(1.0 + bounce, MIN_ZETA), 1.0 / MIN_ZETA)
    return max(1.0 - bounce, MIN_ZETA)


def bounce_from_zeta(zeta: float) -> float:
    return 1.0 - zeta


def params_from_duration_bounce(duration: float, bounce: float, mass: float = 1.0) -> dict:
    """SwiftUI duration form: omega0 = 2*pi/duration  (anchor-verified)."""
    zeta = zeta_from_bounce(bounce)
    w0 = TAU / duration
    k = mass * w0 * w0
    c = 2.0 * zeta * math.sqrt(k * mass)
    return dict(mass=mass, stiffness=k, damping=c, zeta=zeta,
                duration=duration, bounce=bounce, omega0=w0)


def params_from_response_damping(response: float, damping_fraction: float, mass: float = 1.0) -> dict:
    """SwiftUI response form: response == tau (perceptual duration)."""
    zeta = damping_fraction
    w0 = TAU / response
    k = mass * w0 * w0
    c = 2.0 * zeta * math.sqrt(k * mass)
    return dict(mass=mass, stiffness=k, damping=c, zeta=zeta,
                duration=response, bounce=bounce_from_zeta(zeta), omega0=w0)


def params_from_visual_duration(visual_duration: float, bounce: float, mass: float = 1.0) -> dict:
    """Motion duration form: stiffness = (2*pi/(visualDuration*1.2))^2 (source-verified)."""
    zeta = zeta_from_bounce(bounce)
    w0 = TAU / (visual_duration * 1.2)
    k = mass * w0 * w0
    c = 2.0 * zeta * math.sqrt(k * mass)
    return dict(mass=mass, stiffness=k, damping=c, zeta=zeta,
                duration=visual_duration, bounce=bounce, omega0=w0)


def params_from_physical(mass: float, stiffness: float, damping: float) -> dict:
    w0 = math.sqrt(stiffness / mass)
    zeta = damping / (2.0 * math.sqrt(stiffness * mass))
    tau = TAU / w0
    return dict(mass=mass, stiffness=stiffness, damping=damping, zeta=zeta,
                duration=tau, bounce=bounce_from_zeta(zeta), omega0=w0)


def spring_x(t: float, w0: float, zeta: float) -> float:
    """Unit step response x(t) of the damped harmonic oscillator (starts 0 -> settles 1)."""
    if zeta < 1.0:
        wd = w0 * math.sqrt(1.0 - zeta * zeta)
        env = math.exp(-zeta * w0 * t)
        return 1.0 - env * (math.cos(wd * t) + (zeta * w0 / wd) * math.sin(wd * t))
    if abs(zeta - 1.0) < 1e-9:
        return 1.0 - (1.0 + w0 * t) * math.exp(-w0 * t)
    s = w0 * math.sqrt(zeta * zeta - 1.0)
    s1, s2 = -zeta * w0 + s, -zeta * w0 - s  # both negative; s2 more negative
    return 1.0 - (s2 * math.exp(s1 * t) - s1 * math.exp(s2 * t)) / (s2 - s1)


def css_linear(duration: float, bounce: float, points: int = 64, horizon: float = 4.0,
               decimals: int = 4) -> str:
    """Sample the spring into a CSS linear() string over [0, horizon*duration] seconds.

    The CSS animation duration should equal horizon*duration so the curve plays fully.
    """
    p = params_from_duration_bounce(duration, bounce)
    total = horizon * duration
    vals = [spring_x(total * i / (points - 1), p["omega0"], p["zeta"]) for i in range(points)]
    vals = [round(v, decimals) for v in vals]
    vals[-1] = 1.0
    body = ", ".join(f"{v:g}" for v in vals)
    return f"linear({body})"


def fmt(p: dict) -> str:
    return (f"SwiftUI   : spring(response: {p['duration']:.3g}, dampingFraction: {p['zeta']:.4g})  "
            f"== Spring(duration: {p['duration']:.3g}, bounce: {p['bounce']:.4g})\n"
            f"Motion JS : {{ type:'spring', mass: {p['mass']:.4g}, stiffness: {p['stiffness']:.6g}, "
            f"damping: {p['damping']:.6g} }}  (bounce {p['bounce']:.4g}, visualDuration {p['duration']:.3g})\n"
            f"CSS       : transition/animation duration ~{4*p['duration']:.3g}s, easing = css_linear() "
            f"(re-run with --css to emit)")


def selftest() -> int:
    fails = []

    def check(name, got, want, tol):
        ok = abs(got - want) <= tol
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}: got {got:.6g}, want {want:.6g} (+/-{tol:g})")
        if not ok:
            fails.append(name)

    print("selftest: Apple official anchors")
    p = params_from_duration_bounce(0.5, 0.3)
    check("duration=0.5,bounce=0.3 -> stiffness", p["stiffness"], 157.9, 0.1)
    check("duration=0.5,bounce=0.3 -> damping", p["damping"], 17.6, 0.1)
    q = params_from_physical(1.0, 100.0, 10.0)
    check("(m1,k100,c10) -> duration", q["duration"], 0.63, 0.01)
    check("(m1,k100,c10) -> bounce", q["bounce"], 0.5, 0.005)
    d = params_from_response_damping(0.5, 0.825)
    check("default preset zeta", d["zeta"], 0.825, 1e-9)

    print("selftest: CSS curve sanity")
    for name, dur, bnc, lo, hi in [("default(0.825)", 0.5, 0.175, 1.0, 1.20),
                                   ("bouncy(0.7)", 0.5, 0.3, 1.0, 1.35),
                                   ("smooth(zeta=1)", 0.5, 0.0, 0.999, 1.001)]:
        p = params_from_duration_bounce(dur, bnc)
        xs = [spring_x(4.0 * dur * i / 63.0, p["omega0"], p["zeta"]) for i in range(64)]
        peak = max(xs)
        ok = xs[0] <= 0.001 and abs(xs[-1] - 1.0) < 0.005 and lo <= peak <= hi
        print(f"  [{'PASS' if ok else 'FAIL'}] curve {name}: x0={xs[0]:.4g} peak={peak:.4g} x_end={xs[-1]:.4g}")
        if not ok:
            fails.append(f"curve {name}")

    print("selftest: css_linear string")
    s = css_linear(0.5, 0.3)
    ok = s.startswith("linear(0") and s.endswith(")") and "," in s
    print(f"  [{'PASS' if ok else 'FAIL'}] emits linear(...) [{len(s)} chars]")
    if not ok:
        fails.append("css_linear")

    if fails:
        print(f"SELFTEST FAILED: {fails}")
        return 1
    print("SELFTEST PASSED (all anchors green)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Spring parameter translator (SwiftUI <-> Motion <-> CSS linear())")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--semantic", choices=sorted(PRESETS), help="named preset")
    ap.add_argument("--duration", type=float, help="SwiftUI perceptual duration (s)")
    ap.add_argument("--bounce", type=float)
    ap.add_argument("--response", type=float, help="SwiftUI response (s)")
    ap.add_argument("--damping", type=float, help="SwiftUI dampingFraction (0..~1.3)")
    ap.add_argument("--mass", type=float)
    ap.add_argument("--stiffness", type=float)
    ap.add_argument("--physical-damping", type=float, help="Motion damping c")
    ap.add_argument("--visual-duration", type=float, help="Motion visualDuration (s)")
    ap.add_argument("--css", action="store_true", help="emit CSS linear() easing string")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        return selftest()

    if a.semantic:
        pr = PRESETS[a.semantic]
        if "response" in pr:
            p = params_from_response_damping(pr["response"], pr["damping"])
        else:
            p = params_from_duration_bounce(pr["duration"], pr["bounce"])
    elif a.mass is not None and a.stiffness is not None and a.physical_damping is not None:
        p = params_from_physical(a.mass, a.stiffness, a.physical_damping)
    elif a.visual_duration is not None and a.bounce is not None:
        p = params_from_visual_duration(a.visual_duration, a.bounce)
    elif a.response is not None and a.damping is not None:
        p = params_from_response_damping(a.response, a.damping)
    elif a.duration is not None and a.bounce is not None:
        p = params_from_duration_bounce(a.duration, a.bounce)
    else:
        ap.error("provide --semantic, or a parameter triple (see --help)")

    if a.json:
        out = dict(p)
        if a.css:
            out["css_easing"] = css_linear(p["duration"], p["bounce"])
            out["css_duration_s"] = 4 * p["duration"]
        print(json.dumps(out, indent=2))
    else:
        print(fmt(p))
        if a.css:
            print(f"CSS linear() ({64} pts, play over {4*p['duration']:.3g}s):\n  {css_linear(p['duration'], p['bounce'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
