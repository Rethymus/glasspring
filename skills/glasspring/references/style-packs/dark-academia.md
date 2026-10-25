# Style Pack: 暗色学院（Dark Academia）

> DNA 卡 · 提炼自暗色学院美学集群的公开实践（basis=observation + 美学运动 L1）| [Last verified: 2026-10-16] | 适配：独立书店/出版/文创/课程产品/文学品牌——**不适配**：科技 SaaS/金融交易/儿童产品
> 色值由引擎重推导 + 步进 L 实测（金色初值 4.30 FAIL → #6E5629 6.16 AA，"升 L 不降门槛"实证）。

## Philosophy

**"知识是有重量的——让界面承载它。"** 羊皮纸、油墨、哥特衬线、旧书质感、古典学院符号——怀旧不是装饰而是叙事本体。
keywords: [parchment, oxblood, gothic-serif, scholarly, candlelit] · 性格轴：energy 2 / formality 8 / density 5 / playfulness 0

## Seed & Tokens（实测 2026-10-16，check_contrast.py）

- parchment `#F5F1E8` · ink `#2C2418`（**13.57 AAA**）· oxblood `#6D2E2E`（**8.95 AAA**——标题/细线/引言符）
- antique gold `#6E5629`（6.16 AA——文字级；更大面积装饰可用 #8A6D3B 仅限图形）
- 字体：哥特/老式衬线（Playfair/Fraunces/EB Garamond，OFL 可嵌）+ 小号 mono 目录编号

## rules.always

- 衬线统治排版；细双线框（double rule）做分区；藏书纹/纸纹理点缀（低透明度）
- 章节用拉丁/希腊语编号系统（Vol. I、§2）；引文用 oxblood 竖线式
- 深色模式：墨黑 `#1A1712` + 羊皮纸字（同映射反转，对比度需重测）

## rules.never

- 霓虹色/饱和现代色（破坏烛光语境）；无衬线大标题；玻璃材质（羊皮纸吸光，与玻璃光学互斥）
- 现代科技图标（用版画/雕版线条 SVG）

## accessibility_floor（实测 2026-10-16）

ink/parchment 13.57 AAA · oxblood 8.95 AAA · gold 文字级 6.16 AA（升 L 后） · 双线装饰不承载信息

## measured_final（实测终值回写——种子是意图，实测是事实）

GP14 实测（2026-10-17，主会话复核）回写：16 组色对复测**全部与卡载一致，零漂移**——ink/parchment 13.57、oxblood 8.95、gold 6.16（升 L 后）即为终值基线。后续迭代以卡载值为基线；若重推色板，更新本段并重测全部色对。

## validation

黄金 prompt：「做一个独立书店的秋季书单页」→ 验证：哥特衬线/双线框/oxblood 引言/怀旧符号 四线索 ≥3。
