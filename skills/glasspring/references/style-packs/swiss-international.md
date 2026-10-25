# Style Pack: 瑞士国际主义（Swiss International）

> DNA 卡 · 提炼自瑞士平面设计（International Typographic Style）在 Web 端的当代实践（basis=observation + 设计史 L1）| [Last verified: 2026-10-16] | 适配：作品集/设计工作室/建筑/编辑刊物/品牌叙事站
> 色值由 `palette_from_oklch.py` 从 hue 14 重推导（瑞士红家族），实测对比度已验证。

## Philosophy

**"网格即秩序，留白即宣言。"** 不对称网格、无衬线字族、客观摄影、红黑纸三色、装饰归零——内容与网格承担全部表现力。
keywords: [grid, helvetica-lineage, objective, asymmetric, ink-on-paper] · 性格轴：energy 3 / formality 7 / density 5 / playfulness 0

## Seed & Tokens（引擎重推导 2026-10-16）

- seed：瑞士红 hue 14 @ C0.17-0.19（文字级红用 C0.13 深档保证对比）
- paper `#F9F7F2`（暖白 oklch 0.97 0.008 80）· ink `#111111`（on paper 17.64 AAA）
- accent red `#C0271B`（on paper 5.53 AA——文字可用）· 大标题纯黑 + 红仅做标点/编号/线条

## rules.always

- 非对称网格：栏宽不等、错位排版、大留白切分；12 列网格裸露使用（基线可见可选）
- 大字号无衬线（Helvetica 家族/Neue Haas/Inter Tight 重档）+ 小号 mono 图注（编号/日期/规格）
- 摄影：客观、黑白或去饱和、锐利裁切；红色元素与照片色域严格分离
- 悬浮层玻璃：可用（此风格的纸面需要材质对比）；正文/标题区禁用

## rules.never

- 居中对称 hero、渐变、装饰图标、圆角大于 2px（锐角是纪律）
- 阴影柔化（阴影模糊半径 >8px 即破坏纸面感）；动效弹跳（全站 ease 线性）

## accessibility_floor（实测 2026-10-16）

ink/paper 17.64 AAA · accent red 5.53 AA · 红色仅大字号/图形（小号正文用 ink）

## measured_final（实测终值——种子是意图，终值是事实）

瑞士红终值 `#C0271B` = oklch(0.51 0.17 **20**)——种子 hue 14 漂移至 20（文字级深档的合法调整，run 前未预见）；ink 纯黑无漂移。后续以终值为基线。


## validation

黄金 prompt：「做一个建筑事务所作品集首页」→ 验证：非对称网格/mono 图注/红黑纸三色/摄影客观性 四线索 ≥3。
