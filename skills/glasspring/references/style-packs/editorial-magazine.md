# Style Pack: 杂志编辑风（Editorial Magazine）

> DNA 卡 · 提炼自高端印刷杂志的 Web 实践（basis=observation + 编辑设计传统 L1）| [Last verified: 2026-10-16] | 适配：深度内容/评论刊物/品牌故事/文化机构
> 色值由 `palette_from_oklch.py` 从勃艮第 hue 350 重推导（accent-700 = #834765 深档），实测对比度已验证（ink 16.58 AAA / 勃艮第 9.03 AAA）。

## Philosophy

**"阅读的仪式感。"** 衬线显示字体、宽行距、首字下沉、细规则线、不对称双栏——每一屏都在说"这里的内容值得慢读"。
keywords: [serif, generous-leading, drop-cap, hairline-rules, unhurried] · 性格轴：energy 2 / formality 6 / density 4 / playfulness 1

## Seed & Tokens（引擎重推导 2026-10-16）

- paper `#FAF7F2`（暖米白）· ink `#1A1815`（16.58 AAA）· accent burgundy `#722F37`（9.03 AAA，标题/引言/细线）
- 显示字体：Fraunces/Playfair 类高对比衬线（OFL 可嵌）+ 正文衬线 1.7-1.8 行高
- 细规则线：0.5-1px `#D8D2C8`（非结构分隔，纯排版节奏）

## rules.always

- 首字下沉（drop-cap）用于每篇正文开头；pull quote 大号衬线斜体嵌排版
- 图注系统：mono 小号 + 编号（Fig. 01）；全宽图与文本栏交替节奏
- 章节编号语法（01/02/03 + 细线）；日期/作者/阅读时间的刊头排版

## rules.never

- 无衬线做正文（可用做图注/导航）；彩色底色块包正文；圆角卡片包内容（印刷品没有卡片）
- 渐变、玻璃、emoji 图标——印刷传统与这三者互斥

## accessibility_floor（实测 2026-10-16）

ink/paper 16.58 AAA · burgundy 9.03 AAA · 细线装饰 0.5px 不承载信息（纯节奏）

## measured_final（实测终值）

勃艮第终值 `#722F37` = oklch(0.34 0.07 **13**)——与种子 hue 350 吻合（深档自然收 chroma）；paper `#FAF7F2` = hue **91**（暖纸从中性分离——暖白固有色相端）。两色均无越界。

## validation

黄金 prompt：「做一个文学评论杂志的首页（含本期目录/精选文章/作者列表）」→ 验证：衬线体系/首字下沉/细线节奏/引言排版 四线索 ≥3。
