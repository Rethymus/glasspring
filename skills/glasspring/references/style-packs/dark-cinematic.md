# Style Pack: 暗色电影级（Dark Cinematic）

> 第三张风格包 DNA 卡。语料：Vercel / elevenlabs / runwayml 公开界面观察 + Linear 交叉印证。AI/crypto/infra 的高戏剧暗面可以是合法原型；反 slop 规则禁止的是“暗色与霓虹堆叠”，不是暗色与戏剧感本身。
> provenance: basis=observation | 借鉴层级 L1 原则 + L2 结构 + L3 重推导值 | [Last verified: 2026-10-22]
> observed-target（FM-3）: 流派实践（非版本化产品），漂移风险低；参照为 2026-10 快照 | 适配：AI 产品 hero、crypto/infra 营销页、开发者工具品牌页 | 与 linear-instrument.md 的分界：instrument=工作表面（数据仪表、零戏剧），cinematic=营销表面（首屏戏剧、产品 hero）。同一产品的 dashboard 用 instrument，landing 用本卡。
> 信号色为**品牌变量**：本卡 demo 档用电蓝 hue 230，替换为品牌色时保持 C≥0.12 与「on-signal 用 void 黑字」两条不变。

## Philosophy

**"One light source in a dark room."** 整页只有一个光源时刻（glow/渐变/玻璃三选一），戏剧感来自亮度对比的落差而非彩色元素的堆叠。暗面是舞台，不是壁纸。
keywords: [void-layered, single-signal, one-glow, desaturated-support] · 性格轴：energy 6 / formality 6 / density 3 / playfulness 2

## 取舍链（Trigger → Decision → Reason → Evidence → 弃掉什么）

1. 暗底想要戏剧感 → 用**亮度落差**（L0.10 底 vs L0.94 文字 = 17.3:1）+ 唯一一次 glow → 暗面的高级感来自对比度预算花在一处 → Vercel 首屏纯黑白落差 + 一次白光；**弃掉**「多点位霓虹点缀」（那是 slop 清单点名的暗+霓虹堆叠）
2. 背景需要层次 → void L0.10 起三级分层（0.10/0.155/0.21），**刻意不用 #000** → 纯黑 kills 层次头顶空间（surface 无处可暗）且 glow 在 #000 上无溢出感；#030304 近黑但留 0.05 L 余量 → 三级实测全部 AAA；**弃掉** #000 底 + 灰字（灰字在纯黑上发闷，8.32 vs 更低）
3. AI/crypto 题材诱惑渐变 mesh → 渐变/glow/玻璃**预算各一次、永不堆叠** → 三种效果同时出现=「AI 生成的脸」（ slop 清单：渐变填充弱站 52% vs 高分 22%）→ runway 首屏单一光晕、elevenlabs 近单色；**弃掉** aurora/mesh 多彩渐变
4. 辅助色怎么配 → **desaturated 辅助**（C≤0.04）只用于分隔/底图，饱和度预算全部让给唯一信号色 → 信号色出现即事件 → elevenlabs 灰阶主导 + 稀释彩色；**弃掉**多彩语义色系（那是仪表盘的预算，本流派的页面几乎无数据）

## Seed & Tokens（引擎重推导，check_contrast 实测 2026-10-22）

- seed：中性冷相 hue 250 @ C≤0.012（void 分层底）；信号色 demo hue 230 @ C 0.15

```css
/* void 分层三级（palette oklch_to_hex 推导，#000 刻意弃用） */
--pr-void:    oklch(0.100 0.004 250);  /* #030304 页面底 */
--pr-surface: oklch(0.155 0.008 250);  /* #0A0D10 面板/卡 */
--pr-raised:  oklch(0.210 0.012 250);  /* #14191E 悬浮/hover */
/* 语义对（实测选定档） */
--color-text:   #E9EBEE;  /* oklch(0.94 0.004 250)，on void 17.26 AAA */
--color-muted:  #A1A5A9;  /* oklch(0.72 0.008 250)，on void 8.32 AA · on surface 7.86 AA */
--color-signal: #00AEE9;  /* oklch(0.70 0.15 230) demo 档，on void 8.08 AA(also AAA) */
--color-on-signal: #030304; /* void 黑字压信号色 8.08 AA——信号色上**永不用白字**（白字 3.43 FAIL 实测） */
/* 中性 ramp（引擎 --neutral 输出，用于浅色反相区/辅助 UI） */
--pr-neutral-300: #B9BEC4; --pr-neutral-500: #858A8F; --pr-neutral-700: #595E63;
```

- 密度：低（营销表面，一屏一事）；圆角：小（4-10px，锐利感）；阴影族：**glow 即阴影**（0 0 80px 信号色 @15-20% 单次），常规投影几乎不用；动效性格：慢入场（600-900ms ease-out，克制的 opacity/位移 8px）、hero 媒体允许一次 scroll 驱动视差
- 字族性格：display=高对比 grotesk 或衬线均可但**一个页面只一种**、正文=Inter/system；字重对比拉满（display 600+/正文 400），行文极短

## rules.always

- 效果预算制：glow / 渐变 / 玻璃全页**各至多一次**且不互相堆叠；glow 只属于唯一信号色
- 信号色出现即事件：全页 ≤3 处（CTA/一个关键词/数据高亮）；on-signal 文字一律 void 黑
- 辅助色 desaturated（C≤0.04）用于边框/分隔/底图纹理；正文永远 text/muted 两档灰阶
- 暗底文字对比自查把 glow 合成算进去：`check_contrast.py --tint "rgba(signal,0.15)" --composites void,surface` 取最坏

## rules.never

- 无 #000 大面积底（层次死区 + glow 无溢出）；无纯白段落文字（用 #E9EBEE）——SKILL §3 暗色条款
- 无多点位霓虹（信号色 >3 处即破预算）；无 aurora/mesh 渐变；无暗+酸绿组合（slop 清单点名）
- 无玻璃叠 glow（一次预算不能花两遍）；无彩色边框（边框属 desaturated 辅助）
- 无居中三行卡（icon+题+文 ×3 网格）——营销表面用 layout-baselines 锚线构图

## accessibility_floor（实测 2026-10-22）

text/void 17.26 AAA · muted/void 8.32 AA · muted/surface 7.86 AA · text/raised 14.81 AAA · signal/void 8.08 AA · on-signal(void黑) 8.08 AA；白字/signal 3.43 FAIL（已立法禁止）；glow 合成最坏情形未测（本卡页面默认零玻璃零大 glow 铺底，若用户点名 glow 底须补 --tint 实测）

## measured_final（实测终值回写——种子是意图，实测是事实）

- void 终值 **oklch(0.100 0.004 250) #030304**：种子只定了「近黑冷相」，L0.10 为层次头顶空间选档
- 信号色终值 #00AEE9 = oklch(0.70 0.15 230)：demo 档；替换品牌色时重测 signal/void 与 on-signal 两对并回写本段
- on-signal 立法：**void 黑字**（白字 3.43 FAIL 实测驱动）；后续迭代以本段终值为基线

## validation

黄金 prompt：「给一个 AI 视频生成产品做暗色 landing（hero + 三个能力点 + CTA）」→ 验证：void 分层/单一信号色 ≤3 处/唯一 glow/desaturated 辅助/极短文案 五线索命中 ≥3。已知限制：crypto 题材易滑向霓虹堆叠（预算制是唯一护栏，slop_scan 不计 glow 次数——需人工数）；浅色反相区（页脚/法规页）用 neutral ramp 反转时全部色对需重测。
Use this as a starting direction. Validate contrast, motion, and signal-color density against the actual content and target devices.
