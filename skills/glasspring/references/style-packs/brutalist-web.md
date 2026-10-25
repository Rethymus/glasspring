# Style Pack: 粗野主义网页（Brutalist Web）

> DNA 卡 · 提炼自 neo-brutalism Web 流派的公开实践（basis=observation + 流派 L1）| [Last verified: 2026-10-16] | 适配：设计师作品集/独立刊物/活动页/潮流品牌——**不适配**：企业官网/金融/医疗等信任敏感域
> 色值：经典蓝 #0000FF on 白 8.59 AAA、墨黑 18.88 AAA（实测 2026-10-16，check_contrast.py）

## Philosophy

**"诚实即风格：结构裸露，不加修饰。"** 系统字体、生硬黑边、零圆角零阴影、平面色块、刻意的不精致——反审美即审美，但它有严格的内部纪律（网格与层级依然存在）。
keywords: [raw, stark, systematic, anti-decoration, bold-flat] · 性格轴：energy 7 / formality 3 / density 6 / playfulness 4

## Seed & Tokens（经典三色 + 系统字体，实测 2026-10-16）

- paper `#FFFFFF` · ink `#111111`（18.88 AAA）· accent blue `#0000FF`（8.59 AAA——经典粗野蓝可作文字色，少数派）
- 圆角：**0px 全站**（纪律性的"无"）；阴影：**无**（分层全靠边框与色块）
- 字体：system-ui/monospace 混排（反精致的核心是拒绝字体炫技）

## rules.always

- 2-3px 纯黑实线边框勾全部结构（按钮/卡片/分隔）；hover = 反色（黑白互换）
- 平面色块分区（无渐变/无纹理/无模糊）；间距刻板遵循网格（粗野但有秩序）——元素**锚定网格轨不漂浮**（classics 互证 2026-10-22）；剃刀细线技法：`display:grid; gap:1px` + 反差底色
- 连接词/箭头/下划线直给（无含蓄交互暗示）
- **Macro/Micro 双尺度字型语法**（industrial-brutalist-ui 交叉验证 2026-10-22）：Macro 标题=超重 grotesk 全大写（clamp(4rem,10vw,15rem)、tracking -0.03~-0.06em、leading 0.85-0.95）；Micro 数据=等宽 10-14px 全大写宽 tracking（+0.05~+0.1em）担纲全部元数据/导航；衬线极少用且需 halftone/1-bit 降级处理
- **工业语义标签 + ASCII 符号学**（同源）：`<data> <samp> <kbd> <output> <dl>`；`[ 方括号节名 ]`、`>>>`、十字准星、对位标记、REV/UNIT 式字符串数据作装饰（属「自知是装饰的主题化内容」，符合 content-is-not-design）
- 纹理效果词表（同源，一次一种）：halftone/1-bit 抖动、CRT 扫描线（repeating-linear-gradient）、全局低透明度 SVG 噪点

## rules.never

- 任何圆角 >2px（classics 原文："All corners must be exactly 90 degrees"）、任何阴影、任何渐变、任何半透明（粗野主义与玻璃互斥——比 Linear 更绝对）
- 精致微交互（淡入/弹性——粗野主义的动效只有瞬时反色与位移）
- **双模式不混血**（同源原型律）：industrial（纸/墨/hazard 红）与 tactical-telemetry（暗底/磷光/终端绿单点）一项目选一种贯彻到底；终端绿 `#4AF626` 永不作正文色、仅限单一特定元件；暗底用 `#0A0A0A/#121212` 禁纯 #000

## accessibility_floor（实测 2026-10-16）

ink/paper 18.88 AAA · accent blue 8.59 AAA · 反色交互天然双通道

## measured_final（实测终值）

经典蓝 `#0000FF` 实测 oklch(0.42 0.26 **262**)——蓝到紫端（sRGB 蓝的固有位置，非漂移）；ink `#111111` 无漂移。零圆角零阴影纪律与实测一致。


## validation

黄金 prompt：「做一个独立设计工作室的作品集页（粗野主义）」→ 验证：黑边结构/零圆角/反色交互/平面色块 四线索 ≥3。
