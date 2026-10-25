#!/usr/bin/env python3
"""deal_direction.py — direction dealer for the glasspring skill.

taste-skill draw.mjs mechanism, adapted (2026-10-22): for open-brief builds
the biggest failure mode is "the category default every time". The dealer
randomly deals THREE directions; you pick ONE and commit. Adopted commitment
laws (assets/design-notes-template.md §1):

  1  Choose the dealt one, not the most familiar — hold each against the
     subject inventory (8-12 things only this client has) before choosing.
  2  Adopt it. Do NOT blend it with the layout you would have made anyway.
  3  Redraw only for a reason you can state (brand conflict / missing asset),
     never for comfort — and record the redraw in design-notes.

The deck: the nine style packs plus one engine-led wildcard (no pack — pick
one of the nine creative engines and carry the whole page with it). This is
a random draw, so it fights familiarity by construction.

Usage:
  python deal_direction.py            # deal 3
  python deal_direction.py --seed 7   # reproducible deal (cite seed in notes)
  python deal_direction.py --prompt "为一家独立咖啡烘焙工作室做品牌页"
                                      # seed derived from the brief (deterministic
                                      # per brief — same brief, same deal, no manual
                                      # seed needed; gpt-taste seeded-RNG insight:
                                      # "LLMs are inherently lazy and always pick
                                      # the first layout option", so the deck must
                                      # be forced random, not preferred)
  python deal_direction.py --keep warm-soft-saas
                                      # brand locked: deal 2 + that pack
"""
from __future__ import annotations
import argparse, hashlib, random, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))

PACKS = {
    "linear-instrument": "devtools/B2B 深色仪表，键盘优先，mono 数据",
    "notion-paper": "块编辑器纸感，灰阶层级，克制链接绿",
    "swiss-international": "不对称网格，红作标点，字排即设计",
    "brutalist-web": "裸结构 2-3px 黑边，系统字，平面色块",
    "editorial-magazine": "印刷衬线正文，hairline 节奏，首字下沉",
    "dark-academia": "羊皮纸+oxblood，双线分隔，拉丁编号",
    "organic-natural": "低饱和陶土/植物，叶形角，留白 ≥40%",
    "warm-soft-saas": "chunky 触觉按钮，2px+ 实色边，游戏化单色区块",
    "dark-cinematic": "void 分层，单一信号色 ≤3 处，唯一 glow",
    "soft-premium": "静奢暖奶油，胶片颗粒，衬线反差，sage 双轨",
    "soft-structural": "瑞士骨柔和肤，巨型 grotesk，漫射影，近单色",
    "ethereal-glass": "OLED 深空，假玻璃卡三件套，单色相 mesh，发丝微光",
}
WILDCARD = ("engine-led（无包）",
            "不发风格包——从九创意引擎选一个（产品自证/页面即器物/名字即主角/单一 motif/装扮另一品类/场所承载/固定舞台/一节一色/极端克制），用它贯穿全页")
DEAL_N = 3


def main() -> int:
    ap = argparse.ArgumentParser(description="glasspring direction dealer (deal 3, commit to 1)")
    ap.add_argument("--seed", type=int, help="RNG seed for a reproducible deal (cite it in design-notes)")
    ap.add_argument("--prompt", help="the brief text — seed is derived from it (deterministic per brief)")
    ap.add_argument("--keep", choices=sorted(PACKS),
                    help="brand-locked pack: include it in the deal plus %d draws" % (DEAL_N - 1))
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        ok = (len(PACKS) == 12 and DEAL_N == 3
              and all("\n" not in v for v in PACKS.values())
              and len(WILDCARD) == 2)
        print(f"  [{'PASS' if ok else 'FAIL'}] deck: 9 packs + 1 wildcard, deal size 3")
        rng = random.Random(42)
        drawn = rng.sample(list(PACKS) + ["__wild__"], DEAL_N)
        print(f"  [{'PASS' if len(set(drawn)) == 3 else 'FAIL'}] seeded deal returns 3 distinct names")
        s1 = int(hashlib.sha256("咖啡烘焙".encode()).hexdigest()[:8], 16)
        s2 = int(hashlib.sha256("咖啡烘焙".encode()).hexdigest()[:8], 16)
        print(f"  [{'PASS' if s1 == s2 else 'FAIL'}] prompt-derived seed is deterministic")
        print("SELFTEST PASSED (offline anchors green)" if ok else "SELFTEST FAILED")
        return 0 if ok else 1

    if a.prompt:
        seed = int(hashlib.sha256(a.prompt.encode("utf-8")).hexdigest()[:8], 16)
        seed_note = f"（prompt 派生 seed {seed}）"
    elif a.seed is not None:
        seed = a.seed
        seed_note = f"（seed {seed}）"
    else:
        seed = None
        seed_note = ""
    rng = random.Random(seed)
    deck = dict(PACKS)
    deck["__wild__"] = WILDCARD[1]
    names = list(deck)
    keep = [a.keep] if a.keep else []
    pool = [n for n in names if n not in keep]
    dealt = keep + rng.sample(pool, DEAL_N - len(keep))
    print(f"== 发牌{seed_note}：三个方向，选一个并承诺 ==")
    for i, n in enumerate(dealt, 1):
        label = WILDCARD[0] if n == "__wild__" else n
        print(f"  [{i}] {label} — {deck[n]}")
        if n != "__wild__":
            print(f"      read: references/style-packs/{n}.md（rules.always/never 与 a11y floor 在卡内）")
    print()
    print("承诺三律（design-notes §1 记录）：")
    print("  ① 选发的不选熟的——先列 8-12 条题材独有清单，逐方向掂量后再选；")
    print("  ② 承诺它。禁止与「你本来就会做的那个布局」混血；")
    print("  ③ 重抽仅限可陈述理由（品牌冲突/素材缺失），重抽必记录。")
    print()
    print("选中后在 design-notes §1 写：选中方向 + 逐方向否决原因 + 第一直觉（已被处决的默认审美）。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
