# Style Pack: 纸感极简（Notion Paper）

> DNA 卡 · 提炼自 Notion 公开界面观察（basis=observation，L3 重推导）| [Last verified: 2026-10-16] | observed-target: Notion 工作区界面（未版本化快照——产品改版后本卡描述的是"2026-10 的 Notion 纸感"，需当代版本时请重观察）| 适配：文档/知识库/笔记/Wiki（见 domains/productivity-b2b.md 文档面）
> 色值由 `palette_from_oklch.py` 从暖纸 hue 80 重推导，实测对比度已验证。

## Philosophy

**"工具退位给内容：界面是一张安静的白纸。"** 块（block）即组件；chrome hover 才浮现；层级靠灰阶底色差而非线框。
keywords: [paper, calm, neutral, block-editor, inline-first] · 性格轴：energy 2 / formality 4 / density 7 / playfulness 2

## Seed & Tokens（引擎重推导 2026-10-16）

- seed：暖纸中性 hue 80 @ C≤0.006（near-gray warmth）
- bg `#F7F6F3`（oklch 0.97 0.006 80）· surface `#FFFFFF` · ink `#37352F`（on bg 11.35 AAA）
- accent（链接/选中）：低饱和绿 `#20623D`（on bg 6.76 AA）——文档场景 accent 退后，仅链接/选中态

## rules.always

- 层级靠灰阶底色差（bg↔surface↔hover）+ 1px 描边；操作控件 hover 才浮现
- 块编辑语法：slash menu、拖拽句柄 hover 浮现、数据库 view 切换器
- 小圆角 4-6px；近零阴影（悬浮菜单允许一层微影；quantified：hover 影 ≤ `0 2px 8px rgba(0,0,0,0.04)` 200ms——**ultra-diffuse <0.05 律**，minimalist-ui 交叉验证 2026-10-22）
- **斑点粉彩配对单元**（minimalist-ui 交叉 2026-10-22，正文区彩底禁令的合法例外）：callout/高亮用「淡底+深字」**成对**发放——淡红 `#FDEBEC`/字 `#9F2F2D`、淡蓝 `#E1F3FE`/字 `#1F6C9F`、淡绿 `#EDF3EC`/字 `#346538`、淡黄 `#FBF3DB`/字 `#956400`；文字色永远取配对深色，不取默认 ink
- **仿 OS 窗铬用单色点**：document 风格页的假窗条三个点用浅灰单色；红黄绿彩色 traffic 点容易带出过时的桌面拟物感。
- 错峰入场公式：`animation-delay: calc(var(--index) * 80ms)`（minimalist-ui 交叉 2026-10-22）

## rules.never

- 卡片不用投影（上条量化档除外）；正文区彩色背景（斑点粉彩配对 callout 除外）；饱和度 >0.15 的色块大面积铺底
- 彩色图标铺满工具栏（emoji/单色图标是文化的一部分；**包内 emoji 页面图标是正典**——slop_scan emoji_icon_system 的 WARN 在本包按 design-notes §6 豁免论证处理，FM-6 包法胜，gp 样本需书面记录）

## accessibility_floor（实测 2026-10-16）

ink/paper 11.35 AAA · 链接绿 6.76 AA · hover 底差可辨（非颜色依赖）

## measured_final（实测终值——种子是意图，终值是事实）

ink 终值 `#37352F` = oklch(0.32 0.008 **80.6**)——与种子 hue 80 吻合（中性色不漂移）；链接绿终值 `#20623D` = hue **156**（由 AA 对比度驱动从暖纸系分离至绿系——合法漂移，已回写）。后续迭代以终值为基线。

## validation

黄金 prompt：「做一个团队知识库文档页（含侧栏树/正文/评论）」→ 验证：块编辑语法/灰阶层级/链接色克制三线索 ≥2。
