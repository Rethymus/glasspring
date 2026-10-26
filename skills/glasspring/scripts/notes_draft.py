#!/usr/bin/env python3
"""notes_draft.py — auto-draft the mechanical sections of design-notes.md.

Runs the gates live (slop_scan + check_contrast math) and pre-fills §4
(measured contrast), §6 (slop scan), §8 (Last-verified anchors). Judgment
sections (§0-§3, §5, §7) become TODO slots — the draft bootstraps the
notes, it never replaces the agent's judgment. Final notes must be written
to design-notes.md by the agent; verify_output only accepts that name, and
deliberately NOT this draft.

Token pair derivation: text-role tokens (--ink/--muted/--text/...) measured
against --bg; button/accent tokens get a white-on-X CANDIDATE row (confirm
the real text color). Non-parseable values (color-mix/var/fonts) are skipped
with an honest note — measure after resolution, never guess.

Usage:
  python notes_draft.py <run_dir>
  python notes_draft.py <run_dir> --pairs "ink/paper=#1a1a1a:#ffffff,btn=#348400:#ffffff"
  python notes_draft.py <run_dir> --refs tokens.md,type.md,style-packs/warm-soft-saas.md
  python notes_draft.py --selftest
"""
from __future__ import annotations
import argparse, datetime, os, re, sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_contrast as cc  # noqa: E402
import slop_scan as ss  # noqa: E402

REFS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "references")
BG_NAMES = ("--bg", "--background", "--paper", "--page", "--surface", "--color-background")
TEXT_RE = re.compile(r"(ink|fg|-text|text-|foreground|muted|secondary|tertiary|heading|body|subtitle)")
CTA_RE = re.compile(r"(btn|button|accent|primary|cta|action|brand|-500|-600)")
COLOR_RE = re.compile(r"^(#[0-9a-fA-F]{3,8}\b|rgb|rgba|oklch|oklab|hsl)")
SKIP_RE = re.compile(r"(var\(|color-mix|linear-gradient|radial-gradient|\"|')")
NOTE_RE = re.compile(r"(var\(|color-mix|linear-gradient|radial-gradient)")


def parse_tokens(css_path: str) -> dict[str, str]:
    """--name: value from any :root-level declaration (comments stripped)."""
    try:
        text = Path(css_path).read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return {}
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    out = {}
    for m in re.finditer(r"(--[\w-]+)\s*:\s*([^;}]+)", text):
        out[m.group(1)] = m.group(2).strip()
    return out


def derive_pairs(tokens: dict[str, str]) -> tuple[list[dict], list[str]]:
    """(pairs, skipped notes). Auto rows marked source=AUTO/CANDIDATE."""
    bg = next((tokens[n] for n in BG_NAMES if n in tokens and COLOR_RE.match(tokens[n])
               and not SKIP_RE.search(tokens[n])), None)
    pairs, skipped = [], []
    if bg is None:
        skipped.append("no parseable --bg token — add pairs via --pairs or fill §4 by hand")
        bg = "#ffffff"
    for name, val in sorted(tokens.items()):
        if not COLOR_RE.match(val) or SKIP_RE.search(val):
            if NOTE_RE.search(val):
                skipped.append(f"{name}: value not directly parseable ({val[:32]}…) — measure after resolution")
            continue
        if TEXT_RE.search(name) and name not in BG_NAMES:
            pairs.append({"label": f"{name}/bg", "fg": val, "bg": bg, "source": "AUTO"})
        elif CTA_RE.search(name):
            pairs.append({"label": f"white/{name}", "fg": "#ffffff", "bg": val, "source": "CANDIDATE"})
    return pairs, skipped


def measure(pairs: list[dict]) -> list[dict]:
    for p in pairs:
        try:
            r = cc.ratio(p["fg"], p["bg"])
            p["ratio"], p["verdict"], p["ok"] = r, cc.judge(r, False, False), r >= 4.5
            p["apca"] = cc.apca_lc(tuple(round(c * 255) for c in cc.parse_color(p["fg"])),
                                   tuple(round(c * 255) for c in cc.parse_color(p["bg"])))
        except Exception as e:  # noqa: BLE001 — one bad pair must not kill the draft
            p["ratio"], p["verdict"], p["ok"], p["error"] = None, None, False, str(e)
    return pairs


def ref_anchor(ref: str) -> tuple[str, str]:
    """(resolved path or None, 'Last verified YYYY-MM-DD' | absent note)."""
    path = os.path.normpath(os.path.join(REFS_DIR, ref))
    if not os.path.isfile(path):
        return None, "（references/ 下未找到此文件——核对文件名）"
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            head = f.read(2000)
    except OSError:
        return path, "（无法读取文件头）"
    m = re.search(r"Last verified:\s*(\d{4}-\d{2}-\d{2})", head)
    return path, (f"Last verified {m.group(1)}" if m else "（文件头未标 Last-verified——打开确认）")


def build_draft(run_dir: str, pairs: list[dict], skipped: list[str],
                slop: list, refs: list[str], pack: str | None, argv: str) -> str:
    now = datetime.date.today().isoformat()
    L: list[str] = []
    L.append("# design-notes.md（草稿 — notes_draft.py 机械预填）\n")
    L.append(f"> 生成：{now} · 命令：`notes_draft.py {argv}`")
    L.append("> 本稿只预填机械节（§4/§6/§8）；判断节为待填槽。终稿补充判断后另存 design-notes.md")
    L.append("> （verify_output 只认 design-notes.md，且终稿数字必须来自最后一轮门禁——终检复跑律）。\n")
    L.append("## §0 · 路由与默认值\n\n> 待填：四维路由（类型×领域×平台×栈）；未指定维度默认值声明；参考文件读取清单与预算取舍理由。\n")
    L.append("## §1 · 方向取舍\n\n> 待填：发牌方向清单与逐方向否决原因；选中方向；第一直觉记录；编码前泛化审查结论（\"换成隔壁同行也成立吗？\"）。\n")
    L.append("## §2 · 领域线索\n\n> 待填：域包线索逐条实现方式；自验命中数 ≥3；无条款覆盖的自行决定标 judgment，引用条款标 文件名›节名（只引实际读过的）。\n")
    L.append("## §3 · 玻璃与材质\n\n> 待填：决策树四查结果；Tier 1/2/3 使用位置；信任区否决清单。（未用玻璃则写明\"未使用\"。）\n")
    # §4
    L.append("## §4 · 对比度实测（机械生成 — notes_draft.py）\n")
    L.append("| 对 | fg | bg | 比值 | 判定 | 来源 |")
    L.append("|---|---|---|---|---|---|")
    npass = nfail = 0
    for p in pairs:
        if p.get("error"):
            L.append(f"| {p['label']} | {p['fg']} | {p['bg']} | ERROR | {p['error'][:40]} | {p['source']} |")
            nfail += 1
            continue
        npass, nfail = (npass + 1, nfail) if p["ok"] else (npass, nfail + 1)
        L.append(f"| {p['label']} | {p['fg']} | {p['bg']} | {p['ratio']:.2f}:1 | "
                 f"{p['verdict']} (Lc {p['apca']:.0f}) | {p['source']} |")
    L.append(f"\n共 {len(pairs)} 对：PASS {npass} / FAIL {nfail}。CANDIDATE 行是自动推导（白字压底色）——确认该底色上的真实文字色后改写。")
    if skipped:
        L.append("\n跳过未测：")
        L.extend(f"- {s}" for s in skipped)
    if nfail:
        L.append("\n### FAIL → 修复 → 复测\n\n> 待填：逐对修复动作与复测数字（数值回填 tokens.css 头注，格式见现有样本）。\n")
    else:
        L.append("\n### tokens.css 头注回填\n\n> 待填：把实测数值回填 tokens.css 头注（`contrast/实测: 见 design-notes §4` 格式）。\n")
    L.append("## §5 · 动效语义\n\n> 待填：动效预算 Motion N/5；哪些动/哪些不动/为什么；spring 来源（脚本生成/手造）。\n")
    # §6
    hard = [f for f in slop if f[0] == ss.HARD]
    warn = [f for f in slop if f[0] == ss.WARN]
    info = [f for f in slop if f[0] == ss.INFO]
    L.append("## §6 · slop 扫描（机械生成 — notes_draft.py）\n")
    L.append(f"生成时扫描快照（notes_draft.py，{now}）：**{len(hard)} hard / {len(warn)} warn / {len(info)} info**")
    if slop:
        L.append("")
        for sev, rid, where, hint in slop:
            L.append(f"- **[{sev}]** `{rid}` — {where} — {hint}")
    else:
        L.append("（本次快照为零命中。终稿应记录最后一次扫描结果；不要把本快照误写成修复前的首扫结果。）")
    L.append("\n### 修复 → 终扫\n\n> 待填：修复动作 + 终扫数字；截图至上律：门禁过 ≠ 页面好，交付前目检全部截图。\n")
    L.append("### warn 豁免\n\n> 待填：逐条论证（无豁免则写\"无豁免\"）。\n")
    L.append("## §7 · 已知限制\n\n> 待填：诚实清单，每条标影响类（blocks-conversion / adds-friction / reduces-trust / minor-polish）与可辩护/需迭代。\n")
    # §8
    L.append("## §8 · 依赖的 Last-verified 锚点（机械生成 — notes_draft.py）\n")
    for ref in refs:
        path, note = ref_anchor(ref)
        shown = f"references/{ref}" if path else f"references/{ref}"
        L.append(f"- {shown} — {note}")
    if pack:
        path, note = ref_anchor(f"style-packs/{pack}.md")
        L.append(f"- references/style-packs/{pack}.md — {note if path else '（未找到该包文件——核对包名）'}")
    L.append("\n> 待填：主张漂移自查——本页引用的一切数字（星数/百分比/实测值）必须带来源日期；核对引用条款确实读过。\n")
    return "\n".join(L) + "\n"


def gather_slop(run_dir: str) -> list | None:
    try:
        return ss.scan_path(run_dir)
    except Exception as e:  # noqa: BLE001
        print(f"slop scan error: {e}", file=sys.stderr)
        return None


def selftest() -> int:
    import tempfile
    ok = True

    def check(cond, msg):
        nonlocal ok
        print(f"  [{'PASS' if cond else 'FAIL'}] {msg}")
        ok = ok and cond

    with tempfile.TemporaryDirectory() as td:
        css = ":root{--bg:#FBFAF7;--ink:#35332E;--muted:#75716A;--btn:#348400;--font-body:system-ui;--line:var(--ink)}"
        Path(os.path.join(td, "tokens.css")).write_text(css, encoding="utf-8")
        Path(os.path.join(td, "preview.html")).write_text(
            "<html><body style='background:#f4f1ea'><h1>x — y</h1></body></html>", encoding="utf-8")
        tokens = parse_tokens(os.path.join(td, "tokens.css"))
        pairs, skipped = derive_pairs(tokens)
        labels = {p["label"] for p in pairs}
        check({"--ink/bg", "--muted/bg", "white/--btn"} <= labels, f"derive: text+CTA pairs {sorted(labels)}")
        check(all("--font" not in l and "--line" not in l for l in labels), "derive: fonts & var() skipped")
        check(any("var(" in s for s in skipped), f"derive: var() noted in skipped ({skipped})")
        measure(pairs)
        ink = next(p for p in pairs if p["label"] == "--ink/bg")
        check(ink["ok"] and ink["ratio"] > 10, f"measure: ink on warm paper = {ink['ratio']:.2f} PASS")
        slop = gather_slop(td)
        check(slop is not None and any(f[1] == "cream_hex" for f in slop), "slop: cream_hex caught in temp run")
        draft = build_draft(td, pairs, skipped, slop, ["tokens.md", "motion.md"], None, "selftest")
        secs = re.findall(r"^## §(\d)", draft, re.M)
        check(secs == [str(i) for i in range(9)], f"draft: §0-§8 ordered ({secs})")
        check("机械生成" in draft and "cream_hex" in draft and "Last verified" in draft,
              "draft: measured §4 + live §6 + dated §8 all present")
        check("待填" in draft, "draft: judgment slots present")
        path, note = ref_anchor("motion.md")
        check(path and note.startswith("Last verified"), f"anchor: motion.md → {note}")
    print("notes_draft selftest:", "ALL PASS" if ok else "FAILED")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="auto-draft design-notes mechanical sections (§4/§6/§8)")
    ap.add_argument("run_dir", nargs="?", help="run directory containing preview.html/tokens.css")
    ap.add_argument("--pairs", help='explicit pairs: "label=fg:bg,label2=fg:bg" (overrides auto for those labels)')
    ap.add_argument("--refs", default="tokens.md,type.md,layout-baselines.md,motion.md",
                    help="comma list relative to references/ (default: the four routing anchors)")
    ap.add_argument("--pack", help="style-pack name → references/style-packs/<name>.md anchor")
    ap.add_argument("--out", help="output path (default <run_dir>/design-notes-DRAFT.md)")
    ap.add_argument("--force", action="store_true", help="overwrite existing draft")
    ap.add_argument("--stdout", action="store_true", help="print draft instead of writing")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.run_dir:
        ap.error("run_dir required (or --selftest)")
    tokens, pairs, skipped = {}, [], []
    css = os.path.join(a.run_dir, "tokens.css")
    if os.path.isfile(css):
        tokens = parse_tokens(css)
        pairs, skipped = derive_pairs(tokens)
    else:
        skipped.append("tokens.css not found — §4 needs explicit --pairs or manual fill")
    if a.pairs:
        for item in a.pairs.split(","):
            label, _, spec = item.partition("=")
            fg, _, bg = spec.partition(":")
            if fg and bg:
                pairs = [p for p in pairs if p["label"] != label] + [
                    {"label": label, "fg": fg, "bg": bg, "source": "EXPLICIT"}]
    measure(pairs)
    slop = gather_slop(a.run_dir) or []
    draft = build_draft(a.run_dir, pairs, skipped, slop, a.refs.split(","), a.pack,
                        " ".join(x for x in [a.run_dir, a.pairs and "--pairs …", a.pack and f"--pack {a.pack}"] if x))
    if a.stdout:
        # Drafts contain Unicode punctuation and CJK text. In particular,
        # Windows pipes can inherit a legacy code page that cannot encode it.
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        sys.stdout.write(draft)
        return 0
    out = a.out or os.path.join(a.run_dir, "design-notes-DRAFT.md")
    if os.path.exists(out) and not a.force:
        print(f"refusing to overwrite {out} (use --force)")
        return 1
    with open(out, "w", encoding="utf-8") as f:
        f.write(draft)
    nfail = sum(1 for p in pairs if not p.get("ok"))
    print(f"draft written: {out}")
    print(f"  §4 {len(pairs)} pairs ({nfail} FAIL) · §6 {len(slop)} findings · §8 {len(a.refs.split(',')) + bool(a.pack)} anchors")
    print("  next: fill 待填 slots, finalize as design-notes.md, then run doctor.py --target <run_dir> --skip-selftest")
    return 0


if __name__ == "__main__":
    sys.exit(main())
