# Style Pack: 有机自然（Organic Natural）

> DNA 卡 · 提炼自有机自然/陶土美学集群的公开实践（basis=observation + 流派 L1）| [Last verified: 2026-10-16] | 适配：可持续品牌/手作食品/护肤/生活方式/律所之外的人文品牌——**不适配**：硬科技/竞技/数据密集仪表盘
> 色值由引擎重推导 + 步进 L 实测（陶土初值 3.07 FAIL → 文字级 #8B4A2B 5.99；鼠尾草 #3E5A46 7.08 AAA——"升 L 不降门槛"实证）。

## Philosophy

**"自然的节奏，手作的温度。"** 有机曲线、陶土与植物色、大量呼吸留白、不完美即性格——把"可持续"从口号变成触感。
keywords: [organic, terracotta, sage, handmade, breathable] · 性格轴：energy 3 / formality 4 / density 3 / playfulness 3

## Seed & Tokens（实测 2026-10-16，check_contrast.py）

- warm white `#FAF6F0` · ink-green `#2E3B32`（**10.91 AAA**——绿调墨水是本风格的签名）
- terracotta `#8B4A2B`（**6.27 AA** 文字级；大面积图形可用浅档 #C67B4E 仅限非文本）
- sage `#43654C`（5.81 AA）/ deep sage `#3E5A46`（7.08 AAA）——双绿系统（冷绿+暖白）是松弛感来源
- 字体：人文无衬线（可变）或手写标题点缀（克制使用）；圆角 10-16px（有机曲线）

## rules.always

- 曲线语言：border-radius 不对称（如 24px 4px 24px 24px 的"叶片圆角"）、有机形状 SVG 分隔
- 留白率 ≥40%：呼吸感是本风格的第一触感；纸张纹理点缀（低透明度）
- 状态色走泥土系（成功=鼠尾草、警告=陶土、错误=深砖红）——拒绝纯红纯绿

## rules.never

- 玻璃/金属/霓虹（与本风格材质语义冲突）；高饱和促销色
- 硬几何图形（完美圆/正三角）；纯白 #FFFFFF 大面积（用暖白）

## accessibility_floor（实测 2026-10-16）

ink/white 10.91 AAA · terracotta 文字级 6.27 AA · sage 5.81 AA · 有机曲线不承载信息

## measured_final（实测终值回写——种子是意图，实测是事实）

GP19 实测（2026-10-17，主会话复核）回写：
- sage `#43654C` 实测 **6.09 AA**（本行以上卡载 5.81 为卡面初值）——合法漂移，**以 6.09 为基线**；deep sage `#3E5A46` 7.08 AAA 复现一致。
- terracotta `#8B4A2B` 文字级终值 **6.27 AA**（GP19 复测确认；本卡头部"5.99"为初版推导记录，最终以 6.27 为准）。
- ink-green 10.91 AAA、浅档 #C67B4E 3.07（仅非文本）均按卡载落位——零漂移。
- 规则：后续迭代以上述终值为基线，不再回到种子重推；若重推，更新本段并重测全部色对。

## validation

黄金 prompt：「做一个手工陶艺工作室的品牌首页」→ 验证：有机曲线/陶土鼠尾草双色/呼吸留白/手作质感 四线索 ≥3。
