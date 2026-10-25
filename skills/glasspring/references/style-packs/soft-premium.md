# Style Pack: 静奢柔和（Soft Premium · Editorial Luxury 档）

> 第四档风格卡。语料：taste-skill-classics soft-skill（high-end-visual-design）中的 Editorial Luxury 方向，经本项目重新组织。
> provenance: basis=observation（classics soft-skill 规则全读）| 借鉴层级 L1 原则 + L2 结构 + L3 重推导值（观察奶油 #FDFBF7 → hue 84.6 重推导，**不抄录**）| [Last verified: 2026-10-22]
> observed-target（FM-3）: 流派实践（非版本化产品），漂移风险低；参照为 2026-10 快照 | 适配：高端服务/酒店/私银行/律所/精品电商/作品集静奢面
> 与既有包分界：swiss=锐利冷、editorial-magazine=印刷正典（多栏/首字下沉/hairline 节奏）、organic=大地手作、warm-soft=游戏化——本卡=**静奢暖调+胶片颗粒+超软阴影**，无印刷多栏正典负担。同族另两原型（Ethereal Glass/Soft Structuralism）待后续建卡。

## Philosophy

**"Quiet luxury whispers in materials, not in features."** 预算全花在材质感上：暖奶油纸面、胶片颗粒、超软环境影、高反差衬线 display——没有一个元素在喊，但每个元素都被养过。
keywords: [quiet-luxury, film-grain, soft-depth, serif-contrast] · 性格轴：energy 3 / formality 7 / density 4 / playfulness 2

## 取舍链（Trigger → Decision → Reason → Evidence → 弃掉什么）

1. 高端感想靠视觉堆料 → 全部预算转投**材质**（grain 0.03/超软影/纸面暖白）→ 奢侈的信号是「被养过的表面」不是「更多的东西」→ soft-skill Editorial Luxury 原型；**弃掉**「高级=深色+玻璃」（那是 Ethereal Glass 原型的答案，本档不取）
2. 色彩怎么配 → **暖单色 + sage 单点缀**：奶油底/浓缩墨正文/sage 只作文本安全深档与装饰浅档双轨 → 静奢的克制=色相数 ≤3，情绪由明暖度承载 → sage L0.62 装饰档实测 3.43 仅大件、L0.48 文本档 6.13 AA 双轨立法；**弃掉**多彩 pastel 系（那是 warm-soft/notion 的语言）
3. 衬线 display 高反差 → 特大衬线细字重对极小 sans 正文（尺寸反差拉满）→ 静奢的张力来自字型反差而非色彩反差 → soft-skill "high-contrast serif headings"；**弃掉**超重 grotesk display（那是 swiss/soft-structuralism 的）
4. 阴影怎么用 → **超软超淡环境影**（大 blur 低 opacity <0.05）+ 颗粒统一表面 → 硬阴影破坏「被养过」的柔和感 → minimalist-ui ultra-diffuse 律同源互证；**弃掉** Double-Bezel 构造卡（那是 soft-structuralism 的语法，本档卡片平放+发丝边）

## Seed & Tokens（引擎重推导，check_contrast 实测 2026-10-22）

- seed：暖奶油 hue 84.6 @ C≤0.006（观察 #FDFBF7 归一化）；sage hue 155 @ C 0.05 双轨；espresso hue 55 @ C 0.035

```css
/* 暖奶油族（palette_from_oklch.py 从 hue 84.6 重推导） */
--pr-bg:     oklch(0.985 0.006 84.6);  /* #FCFAF6 暖奶油纸面 */
--pr-surface:#ffffff;                   /* 白卡（分离靠发丝边+grain，非底差） */
--pr-ink:    oklch(0.28 0.035 55);      /* #362418 浓缩墨 on bg 14.16 AAA */
--pr-muted:  oklch(0.55 0.015 60);      /* #787069 on bg 4.66 AA */
/* sage 双轨（单点缀色相） */
--pr-sage-deco: oklch(0.62 0.05 155);   /* #6F8F79 装饰/大件 3.43:1——禁文本 */
--pr-sage-text: oklch(0.48 0.05 155);   /* #476651 文本/链接 6.13 AA */
/* 反转面板（页脚/引言区） */
--pr-espresso-panel: oklch(0.28 0.035 55); /* 底，奶油字 14.16 AAA */
```

- 密度：中低；圆角：小（4-8px，静奢不要玩具感）；阴影族：**超软环境影**（如 `0 24px 60px rgba(54,36,24,0.06)`，opacity 永远 <0.05）+ **胶片颗粒** `position:fixed; pointer-events:none` 全局层 opacity 0.03；动效性格：极慢极轻（600-800ms ease-out，位移 ≤12px），spring 仅限微交互
- 字族性格：display=高反差衬线（PP Editorial New/Playfair 精神，字重 400-500 大尺寸），正文=中性 sans（Geist/Switzer）；**尺寸反差拉满**（display 4-7rem vs 正文 15-16px），tracking 衬线微负 -0.01~-0.02em

## rules.always

- 全局胶片颗粒层（fixed + pointer-events-none + opacity 0.03）统一所有表面质感；颗粒即本档的「材质签名」
- sage 双轨纪律：装饰档只上大件（分隔/大数字/图框），文本一律文本档
- 卡片平放 + 1px 发丝边（rgba 黑 6-8%）+ 超软影；分区靠 py-24+ 级大留白（soft-skill "Double your standard padding"）
- display 衬线 + sans 正文同屏反差 ≥3 倍字号；引言/页脚用 espresso 反转面板（奶油字）

## rules.never

- 无硬阴影、无饱和色块、无渐变（静奢的表面只有纸+颗粒+软影）
- 无玻璃（本档是 Editorial Luxury；Ethereal Glass 是同族另一原型，混用即两不纯粹）
- 无 pill 徽章、无 emoji、无居中三行卡；装饰 sage 档永不承文本
- 无致密 bento（那是 warm-soft 的）——本档版式是编辑式大留白

## accessibility_floor（实测 2026-10-22，bg #FCFAF6）

ink/底 14.16 AAA · muted/底 4.66 AA · sage文本/底 6.13 AA · sage装饰/底 3.43（大件）· 反转面板 14.16 AAA · espresso/白卡 14.76 AAA；颗粒层 0.03 不影响对比实测（远低于可感知阈值）

## measured_final（实测终值回写——种子是意图，终值是事实）

- 奶油底终值 **#FCFAF6 = oklch(0.985 0.006 84.6)**（观察值 #FDFBF7 归一化）；espresso 终值 #362418 = oklch(0.28 0.035 55)
- **sage 双轨立法**（实测驱动）：装饰 #6F8F79 L0.62（3.43 大件档）/ 文本 #476651 L0.48（6.13）——单档 sage 上文本是本卡头号误用点
- 后续迭代以本段终值为基线

## validation

黄金 prompt：「给一家私人律师/精品酒店做品牌首页（hero+服务+联系）」→ 验证：颗粒材质/衬线反差/sage 双轨/超软影/大留白 五线索命中 ≥3。已知限制：胶片颗粒在低分屏可能脏；衬线 web font 需自托管子集（系统衬线降级折损气质）；「静奢」误用于 youthful 题材会显老气——formality ≥6 才可用。
Use this as a starting direction. Validate the typography, textures, and level of formality against the actual brand, content, and display quality.
