#!/usr/bin/env python3
"""run_init.py — scaffold a fresh glasspring run directory in one command.

The one-shot onboarding: instead of hand-creating the four deliverable
artifacts, `python run_init.py <dir> [--scaffold <pack>] [--seed <hex>]` makes

    <dir>/preview.html      — honest skeleton (tokens wired, real headings,
                              one focus element; no lorem, no slop defaults)
    <dir>/tokens.css        — starter from the chosen style pack (engine-
                              rederived via palette scaffold semantics) or a
                              neutral seed placeholder to be replaced
    <dir>/design-notes.md   — the §0-§8 template, pre-filled with the route
    <dir>/shots/            — empty, ready for preview_shot.py

then prints the exact next commands (design → build → gates). Exit 1 if the
target exists non-empty (never clobber a real run); --force to override.

The skeleton preview deliberately ships UNGREEN: it is a starting frame, not
a finished deliverable — the gates it prints are the ones that will initially
fail until real design work happens. That is the point.
"""
from __future__ import annotations
import argparse, os, shutil, sys
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)

NOTES_TEMPLATE = os.path.join(SKILL, "assets", "design-notes-template.md")

PREVIEW_SKELETON = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
@import url("tokens.css");
/* 页偏差（仅 deviations from tokens.css）写在这里 */
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: var(--font, system-ui); background: var(--bg, #ffffff);
       color: var(--ink, #111111); line-height: 1.8; font-size: 16px; }}
a:focus-visible, button:focus-visible {{ outline: 2px solid currentColor; outline-offset: 3px; }}
.wrap {{ padding: clamp(1.25rem, 4vw, 4rem); }}
h1 {{ font-size: clamp(2rem, 6vw, 4rem); line-height: 1.2; text-wrap: balance; max-width: 14em; }}
.lede {{ margin-top: 1rem; max-width: 32em; color: var(--muted, #555555); }}
/* TODO(design): 按 Design Read 选定的方向重写本页——这是骨架不是交付物 */
</style>
</head>
<body>
<div class="wrap">
  <h1>{title}</h1>
  <p class="lede">一句话说清这个页面为谁解决什么。</p>
</div>
</body>
</html>
"""

TOKENS_PLACEHOLDER = """/* seed/种子: <在此填品牌种子 hex，删除本占位后由 palette_from_oklch.py --seed 推导>;
   contrast/实测: <建 token 后用 check_contrast.py --pairs 实测并回写> */
:root {{
  --bg: #ffffff;
  --ink: #111111;   /* 占位——替换为推导值 */
  --muted: #555555; /* 占位——须实测 ≥4.5:1 */
  --font: system-ui, -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif;
}}
"""

NEXT_STEPS = """
下一步（按 SKILL.md 工作流）:
  1. 读 references/  路由四问 → 选风格包或发牌: python scripts/deal_direction.py --prompt "<简报>"
  2. 推导色板:        python scripts/palette_from_oklch.py --seed <hex> --css  (或 --scaffold {scaffold_flag})
  3. 替换 tokens.css 占位 → 实测: python scripts/check_contrast.py --fg ... --bg ...
  4. 重写 preview.html 为真实页面（当前是骨架, 门禁会红——这是设计起点）
  5. 截图:            python scripts/preview_shot.py "file:///{abs}/preview.html" --out-dir "{abs}/shots" --widths 390,1440
  6. 终门禁:          python scripts/doctor.py --target "{abs}"
  7. 填写 design-notes.md（§0-§8 逐节, 判断性决定与豁免论证写在对应节）
"""


def main() -> int:
    ap = argparse.ArgumentParser(description="glasspring run scaffold (one command to a gated run)")
    ap.add_argument("target", nargs="?", help="run directory to create (e.g. examples/my-page)")
    ap.add_argument("--title", default="未命名页面", help="page title for the skeleton preview")
    ap.add_argument("--scaffold", default=None,
                    help="style pack id for the tokens starter hint (e.g. soft-premium)")
    ap.add_argument("--force", action="store_true", help="scaffold into a non-empty directory (files are still never overwritten)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        import subprocess, tempfile
        fails = []
        me = os.path.abspath(__file__)
        def run_cmd(*args):
            return subprocess.run([sys.executable, me, *args],
                                  capture_output=True, text=True).returncode
        def check(name, ok):
            print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
            if not ok: fails.append(name)
        with tempfile.TemporaryDirectory() as td:
            run = os.path.join(td, "my-run")
            rc = run_cmd(run, "--title", "测试页")
            check("scaffold creates run", rc == 0 and os.path.isfile(os.path.join(run, "preview.html")))
            check("tokens.css present", os.path.isfile(os.path.join(run, "tokens.css")))
            check("design-notes template copied", os.path.isfile(os.path.join(run, "design-notes.md")))
            check("shots/ present", os.path.isdir(os.path.join(run, "shots")))
            rc2 = run_cmd(run)
            check("refuses non-empty without --force", rc2 != 0)
            before = Path(os.path.join(run, "preview.html")).read_text(encoding="utf-8")
            run_cmd(run, "--force")
            after = Path(os.path.join(run, "preview.html")).read_text(encoding="utf-8")
            check("--force never overwrites existing files", before == after)
        print("SELFTEST PASSED" if not fails else f"SELFTEST FAILED: {fails}")
        return 0 if not fails else 1


    if os.path.exists(a.target) and os.listdir(a.target) and not a.force:
        print(f"refusing: {a.target} exists and is non-empty (pass --force to add alongside)")
        return 1
    os.makedirs(os.path.join(a.target, "shots"), exist_ok=True)

    wrote = []
    preview = os.path.join(a.target, "preview.html")
    if not os.path.exists(preview):
        Path(preview).write_text(PREVIEW_SKELETON.format(title=a.title), encoding="utf-8")
        wrote.append("preview.html")
    tokens = os.path.join(a.target, "tokens.css")
    if not os.path.exists(tokens):
        Path(tokens).write_text(TOKENS_PLACEHOLDER, encoding="utf-8")
        wrote.append("tokens.css")
    notes = os.path.join(a.target, "design-notes.md")
    if not os.path.exists(notes) and os.path.isfile(NOTES_TEMPLATE):
        shutil.copyfile(NOTES_TEMPLATE, notes)
        wrote.append("design-notes.md (template)")

    abs_target = os.path.abspath(a.target)
    print(f"glasspring run scaffold → {abs_target}")
    for w in wrote:
        print(f"  + {w}")
    print(f"  + shots/ (empty)")
    print(NEXT_STEPS.format(abs=abs_target, scaffold_flag=a.scaffold or "<pack>"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
