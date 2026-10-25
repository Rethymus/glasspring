# Style Pack: Linear 仪表盘（Linear Instrument）

> 第一个实证风格包：演示"逆向观察 → DNA 卡 → 引擎重推导 → 实测"完整链路。参照 Linear 产品文档与公开界面观察提炼；色值由引擎从 hue 238 重推导（非抄录 Linear 实际 hex——L3 合规）。
> provenance: basis=observation + Sequoia spotlight/Geist 交叉印证 | [Last verified: 2026-10-16] | observed-target: Linear.app 公开界面与文档（未版本化快照——产品改版后本卡描述的是"2026-10 的 Linear 风"，需当代版本时请重观察）| 适配：devtools/B2B SaaS 深色仪表盘（见 domains/devtech.md）

## Philosophy

**"Speed is the feature."** 快到没有感觉、有主见到不容配置、键盘到无需鼠标。克制的暗色仪表、单一 accent、等宽数据、一切为流状态服务。
keywords: [instrument, keyboard-first, opinionated, calm-dark] · 性格轴：energy 4 / formality 5 / density 8 / playfulness 1

## Seed & Tokens（引擎重推导，check_contrast 实测 2026-10-16）

- seed：hue 238（靛蓝），accent chroma ≤0.14；neutral = hue 238 @ C≤0.014

```css
/* accent ramp（palette_from_oklch.py --hue 238 --chroma 0.14 输出） */
--pr-accent-300: oklch(0.80 0.11 238);  /* #75C8FC */
--pr-accent-500: oklch(0.63 0.14 238);  /* #0093D3 */
--pr-accent-700: oklch(0.48 0.14 238);  /* #0065A2 */
/* tinted neutrals（背景三级） */
--pr-bg:       #101319;   /* 页面底 */
--pr-surface:  #161b24;   /* 面板 */
--pr-surface-up: #1d2430; /* 悬浮 */
/* 实测语义对 */
--color-text:  #e8eaf6;   /* on bg 15.52:1 AAA */
--color-accent: #8b93f8;  /* on bg 6.75:1 AA */
--color-on-accent: #0d0f16; /* on accent 6.95:1 AA */
```

## rules.always

- 数据/日志/ID/时间戳一律 mono + tabular-nums；键盘可达（⌘K 命令面板一等公民）
- 图表色：单一 accent 族 + 语义色分离（ok/warn/error 永不与 accent 混淆）
- 密度优先：行高紧凑档默认可切

## rules.never

- 无玻璃（此风格与玻璃互斥——若用户点名玻璃，转 glass.md Tier 1 但记录风格冲突）
- 无弹跳弹簧（120-200ms 纯 ease-out；手势释放除外）
- 无渐变 hero、无居中 hero、无装饰插画

## accessibility_floor（实测 2026-10-16）

text/bg 15.52 AAA · accent/bg 6.75 AA · on-accent 6.95 AA · 全对见 scripts/check_contrast.py 记录

## measured_final（实测终值回写——种子是意图，实测是事实）

对比度门禁会驱动语义色偏离种子（合法且必要），**最终值必须回写本卡**：
- Adjust the semantic accent to satisfy contrast and the product’s brand direction; record any deviation from the source seed in the design notes.
- 背景族终值实测 hue 261-264（同样偏离 238——着色中性随 L 变化的合法漂移）。
- 规则：后续迭代以本段实测终值为基线，不再回到种子重推；若重推，更新本段并重测全部色对。

## validation

黄金 prompt：「做一个 Linear 风格的 issue tracker 界面（深色）」→ 验证：键盘流/密度/mono 数据/accent 克制四线索命中 ≥3。
