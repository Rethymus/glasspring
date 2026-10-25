# Style Pack: 柔性结构（Soft Structuralism 档）

> soft-premium 同族第二原型。语料：taste-skill-classics soft-skill 的浅色背景、醒目排版与柔和阴影方向，按本项目参数重新推导。
> provenance: basis=observation（classics soft-skill 规则）| 借鉴层级 L1 原则 + L2 结构 + L3 重推导值 | [Last verified: 2026-10-22]
> observed-target（FM-3）: 流派实践（非版本化产品），漂移风险低 | 适配：设计工具/咨询/建筑事务所/企业品牌站——需要瑞士秩序但拒其冷峻的面
> 与 swiss-international 的分界（同骨架不同材质）：swiss=0-2px 直角+红色标点+linear 动效+锐利；本卡=同 grid 纪律 + **圆角 8-12px + 超软漫射影 + 无标点红**。一句话：swiss 的骨，soft-premium 的肤。

## Philosophy

**"Structure you can feel, edges you cannot."** 网格纪律全部保留——对齐、锚线、层级照旧；变的只是材质：每个硬边都被漫射软化，巨型 grotesk 承担全部戏剧性。
keywords: [soft-grid, massive-grotesk, diffused-depth, monochrome-forward] · 性格轴：energy 4 / formality 6 / density 5 / playfulness 2

## 取舍链（Trigger → Decision → Reason → Evidence → 弃掉什么）

1. 要瑞士的秩序不要它的冷 → 材质软化三件套（银灰底/圆角 8-12/超软影），结构纪律一条不减 → 冷感来自**边的硬度**而非网格本身 → soft-skill 原型定义；**弃掉**「放松对齐来换柔和」（对齐是骨架，软化只在表皮）
2. 戏剧性放哪 → **全部给巨型 grotesk display**（字重 800-900、尺寸跳 ≥3x）→ 无标点色无渐变时，字排是唯一乐器 → cookbook 反差极端律（100/200-800/900 权重对）；**弃掉**彩色大色场（那是 cinematic/organic 的乐器）
3. 阴影语法 → **漫射环境影**（大 blur 40-80px、opacity ≤0.06、永不偏移方向性）——影是「空气厚度」不是「投影光源」 → soft-skill "unbelievably soft, highly diffused"；**弃掉**方向性投影（那是 warm-soft chunky 底影的反面教材对位）
4. accent 要不要 → 单一冷蓝 demo 档、克制使用（链接/唯一 CTA），几乎单色前行 → 单色前行让 grotsk 和材质当主角 → 实测 accent/底 5.43 AA / 白字 5.99 AA；**弃掉**多 accent（swiss 的红色标点属 swiss 不外借）

## Seed & Tokens（引擎重推导 + 脚本直写实测 2026-10-22）

- seed：冷银灰 hue 250 @ C≤0.01（LIGHT 主题）；accent demo hue 250 @ C 0.12（品牌可换）

```css
/* 银灰族（palette_from_oklch.py 从 hue 250 重推导） */
--pr-bg:     oklch(0.965 0.005 250);  /* #F1F4F7 银灰底 */
--pr-surface:#ffffff;                  /* 白卡（超软影+发丝边分离） */
--pr-ink:    oklch(0.25 0.01 250);     /* #1E2226 on bg 14.50 AAA */
--pr-muted:  oklch(0.47 0.01 250);     /* #575B60 on bg 6.20 AA */
--pr-accent: oklch(0.50 0.12 250);     /* #2266A4 文本 5.43 AA · 白字 5.99 AA */
--pr-shadow: 0 40px 80px rgba(30, 34, 38, 0.06), 0 8px 24px rgba(30, 34, 38, 0.04); /* 漫射双层，无方向性 */
```

- 密度：中；圆角：8-12px（swiss 0-2px 的唯一结构偏离）；阴影族：见上，**永不偏移**；动效性格：缓入缓出 500-700ms，位移 ≤8px，无弹簧（弹簧属 warm-soft）
- 字族性格：display=巨型 grotesk 800-900（Archivo/General Sans/Switzer——**先过 Space Grotesk 陷阱自查**，type.md 第二阶收敛）；正文=同族 400；display/正文尺寸跳 ≥3x、字重极端对

## rules.always

- 超软漫射影 + 发丝边（rgba ink 6%）双通道分离；影永无方向偏移
- display 字重 800-900 + 尺寸跳 ≥3x——字排承担全部戏剧性
- 白卡在银灰底上分层；大量留白（密度 dial ≤5）
- accent 克制：链接/唯一 CTA/一个数据高亮，全页 ≤3 处

## rules.never

- 无方向性投影、无红色标点（swiss 专属）、无弹簧、无渐变
- 无 0-2px 直角（那是 swiss 的骨相记号——圆角 8-12px 是本卡的派别纹章）
- accent 不上大色块（本卡无彩色色场）
- display 禁 Inter/Roboto（XIAS/soft-skill 禁令）且**过第二阶收敛自查**

## accessibility_floor（实测 2026-10-22，bg #F1F4F7，hex 脚本直写配对）

ink/底 14.50 AAA · muted/底 6.20 AA · accent/底 5.43 AA · 白字/accent 5.99 AA · ink/白卡 16.01 AAA · muted/白卡 6.84 AA——6/6 全过

## measured_final（实测终值回写——种子是意图，终值是事实）

- bg 终值 **#F1F4F7 = oklch(0.965 0.005 250)**；ink #1E2226 / muted #575B60 / accent #2266A4 = oklch(0.50 0.12 250)
- 首轮三处 FAIL（muted L0.55 3.32 / accent L0.52 4.46）由重推导下潜至 L0.47/L0.50 修复——下潜即立法
- **流程入法**：色对 hex 由脚本从 OKLCH 直接生成配对文件，禁止人工转录（本轮两次转录错误教训）
- 后续迭代以本段终值为基线

## validation

黄金 prompt：「给一家建筑事务所做品牌首页（项目作品+方法+联系）」→ 验证：巨型 grotesk/漫射影/银灰白卡/grotesk 戏剧性/无标点色 五线索命中 ≥3。已知限制：银灰低饱和底在劣屏偏冷灰；grotesk 需自托管；与 swiss 的边界靠圆角与影维持——混用即两头不靠。
Use this as a starting direction. Confirm that the chosen type, materials, and image subjects fit the actual organization and project content.
