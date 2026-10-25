# Style Pack: 暖软 SaaS（Warm-Soft SaaS）

> 第二张风格包 DNA 卡。语料：Duolingo 公开设计系统文档与 onboarding 型生产力应用界面观察；本卡重新推导配色，不复制品牌色值。
> provenance: basis=observation + official-docs（Duolingo 设计系统文档）| 借鉴层级 L1 原则 + L2 结构 + L3 重推导值（**不抄录 Duolingo 实际 hex**——引擎从种子 hue 137.6 重推导）| [Last verified: 2026-10-22]
> observed-target（FM-3）: Duolingo 2026-10 的设计语言（版本化产品，改版后需重观察）；流派面：friendly-consumer SaaS 原型，漂移风险中等 | 适配：onboarding 重的消费级生产力 app、教育/习惯养成/轻健康
> 与 organic-natural.md 的分界：本卡=数字化友好（高饱和品牌色块+游戏化机制感），organic=自然手作（低饱和陶土/植物+手作质感）。onboarding 重的 productivity 落本卡。

## Philosophy

**"Learning should feel like a game, not a task."** 高饱和品牌色块占据真实表面积、按钮厚得能"按进去"、边框永不细若发丝——一切都在邀请触摸，没有一样东西在装成熟。
keywords: [chunky, playful-mass, touchable, game-loop] · 性格轴：energy 8 / formality 2 / density 6 / playfulness 9

## 取舍链（Trigger → Decision → Reason → Evidence → 弃掉什么）

1. 品牌绿占表面积 30%+ → 让品牌色做**色块质量**而非文字颜色 → 游戏化产品需要情绪剂量，剂量=面积不是频率 → Duolingo owl green 大面积铺装；**弃掉**「accent 只做点缀」的经典纪律（那是 instrument 流派的纪律，不是本流派的）
2. 白字压亮绿实测 3.3:1 → 文本/按钮绿下潜至 #348400/#2B7000 → 4.5:1 是硬地板，品牌感靠色块面积补回 → 绿500 #50A02A 白字 FAIL 实测（Duolingo 生产环境同款配置是已知 a11y 批评）；**弃掉**「照抄观察值」（L3 纪律：实测不过就升档）
3. 按钮 4px 底阴影 + 全圆角 → 触觉隐喻（按下去物理下沉）→ chunky 是本流派的核心语法，阴影=按钮的"厚度" → Duolingo 按钮按压位移交互；**弃掉** hairline 边框与扁平阴影（那是 linear-instrument 的语法）
4. 吉祥物即角色（出现在 onboarding/错误页/streak）→ 用角色承载情绪而非用插画装饰 → 习惯养成需要情感锚点，角色=回访理由之一 → Duo 猫头鹰的系统性出场；**弃掉**抽象 hero 插画（无法跨场景承载情绪）

## Seed & Tokens（引擎重推导，check_contrast 实测 2026-10-22）

- seed：owl green → hue 137.6（亮绿），accent chroma 0.17-0.20；neutral = 暖相 hue 85 @ C≤0.012

```css
/* accent ramp（palette_from_oklch.py --seed #58cc02 输出，check-ramp PASS） */
--pr-accent-50:  oklch(0.97 0.02 137.6);  /* #EFF9EC */
--pr-accent-100: oklch(0.93 0.05 137.6);  /* #D8F0D0 */
--pr-accent-300: oklch(0.80 0.11 137.6);  /* #9BCF88 */
--pr-accent-500: oklch(0.63 0.17 137.6);  /* #50A02A ← 品牌/图标/表面专用，零文字 */
--pr-accent-700: oklch(0.48 0.15 137.6);  /* #2B7000 ← 文本/链接绿 */
/* 暖中性 + 语义终值（实测选定档） */
--pr-bg:          #FBFAF7;  /* 暖纸白 oklch(0.985 0.004 85) */
--color-text:     #35332E;  /* on bg 12.09 AAA */
--color-muted:    #75716A;  /* on bg 4.65 AA */
--color-btn:      #348400;  /* 按钮绿 oklch(0.54 0.17 137.6)，白字 4.72 AA */
--color-btn-shadow: #1E6400; /* 按钮底阴影绿 oklch(0.44 0.15 137.6)——4px 实色，非 blur */
--color-btn-text: #ffffff;
/* 次要游戏化色（非文本装饰填充专用：图标底/进度/streak，不承载文字） */
--pr-fun-orange: #ff9600; --pr-fun-pink: #ce82ff; --pr-fun-blue: #1cb0f6;
--pr-fun-red: #ff4b4b; --pr-fun-yellow: #ffc800;
```

- 密度：中高（bento 网格，格数学精确无死格）；圆角：卡片 16-20px、按钮全圆；阴影族：实色 offset 底阴影（0 4px 0 按钮色深档），**不用 blur 扩散影**；动效性格：弹簧 Q 弹（stiffness 中高/damping 低，overshoot 可见）、按压 scale(.97)+阴影压缩
- 字族性格：display=圆润人文 sans（Nunito/Feather Bold 精神，字重 800）、正文=Mona Sans/Inter；标题句号可省、微文案用「你」不用「您」

## rules.always

- 边框 ≥2px 实色（永不 hairline）；卡片圆角 16-20px、按钮全圆、图标容器圆角填充按类目着色
- 主按钮=btn 绿 + 白字 + 4px 实色底阴影，按压时 translateY(2px)+阴影缩至 2px（触觉下沉）
- 游戏化次要色每次**只用一种**于一个区块（多色并发即马戏团）；streak/进度类数字用 fun 色但 ≥18.66px bold（大文本 3:1 floor 自查）
- 吉祥物/角色出场必须绑定状态语义（欢迎/错误/连击），不做纯装饰漂浮

## rules.never

- 绿 500 上永远不放任何文字（白字 3.28 FAIL / 深墨 3.85 FAIL——纯表面色）
- 无 hairline（<1.5px）分隔——用 2-3px 实色边或整段色场分节
- 无 blur 扩散阴影（shadow glow 与本流派触觉隐喻冲突）；无 glass 面板（友好实体感与半透明材质互斥，用户点名转 glass.md Tier 1 并记录冲突）
- 无中性灰按钮（本流派的按钮必须有色；灰只属于禁用态）

## accessibility_floor（实测 2026-10-22）

text/bg 12.09 AAA · muted/bg 4.65 AA · 白字/btn绿 4.72 AA · 白字/绿700 6.14 AA · 文本绿/白 5.88 AA（AAA 差 1.1，链接可再下潜或接受 AA）；游戏化次要色限非文本装饰，白底 3:1 不达（#ff9600 2.1:1）——已知限制，靠形状双通道兜底

## measured_final（实测终值回写——种子是意图，实测是事实）

- 按钮绿终值 **#348400 = oklch(0.54 0.17 137.6)**：从种子亮绿下潜 3 档（对比度地板驱动），品牌亮感由绿 500 色块面积承接
- 文本绿终值 #2B7000 = oklch(0.48 0.15 137.6)；底阴影绿 #1E6400 = oklch(0.44 0.15 137.6)
- 暖中性族实测 hue 85（种子未指定，从「暖」定性推导）；后续迭代以本段终值为基线

## validation

黄金 prompt：「给一个番茄钟习惯养成 app 做 onboarding 三屏（含 streak 展示）」→ 验证：chunky 按钮/2px+ 边框/绿块面积/游戏化单色区块/角色状态出场 五线索命中 ≥3。已知限制：吉祥物需插画资产（本卡只管出场语法不管绘制）；教育外题材（如金融）误用本卡会轻佻化——formality ≤3 的产品才可用。
Validate mascot and progress-indicator contrast on every surface; same-hue colors can disappear when placed on matching backgrounds.
