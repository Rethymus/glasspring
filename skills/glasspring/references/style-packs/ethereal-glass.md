# Style Pack: 空灵玻璃（Ethereal Glass 档）

> soft-premium 同族第三原型。语料：taste-skill-classics soft-skill 的暗色层次与扩散光线建议，按本项目参数重新推导。
> provenance: basis=observation（classics soft-skill 规则）+ glass.md 全 tier 纪律约束 | 借鉴层级 L1 原则 + L2 结构 + L3 重推导值 | [Last verified: 2026-10-22]
> observed-target（FM-3）: 流派实践（非版本化产品），漂移风险低 | 适配：AI 产品/SaaS 暗色高级面/开发者品牌——玻璃材质本身是叙事的面
> 与 dark-cinematic 的分界：cinematic=平涂 void+唯一 glow+零玻璃零 mesh；本卡=**玻璃材质家族+mesh 氛围**——材质即叙事。两者同题材出现时按用户点名选，未点名默认 cinematic（更克制）。
> **三仲裁（本卡合法性根基，先于一切规则）**：①信任区恒实底（glass.md Tier 0 否决凌驾风格——价格/数据/代码/法务永不做玻璃）②Vantablack 卡为 in-flow 滚动件→**假玻璃语法**（实底+内高光+白/10 发丝环——读感即重玻璃，零逐帧重算，glass.md blur 元素级纪律）③真 backdrop-filter 仅 fixed 导航/模态（小面积）；Tier 2 实底回退必发。

## Philosophy

**"The interface is a pane of smoked glass over deep space."** 深空黑上浮着烟熏玻璃；mesh 光晕是唯一的宇宙背景辐射，材质本身在讲故事。
keywords: [oled-void, smoked-glass, mesh-atmosphere, hairline-luminescence] · 性格轴：energy 5 / formality 5 / density 4 / playfulness 3

## 取舍链（Trigger → Decision → Reason → Evidence → 弃掉了什么）

1. 重玻璃卡想直接 backdrop-filter → **in-flow 一律假玻璃**，真 blur 只上 fixed 导航 → 滚动件的 blur 每帧全量重算（成本=面积×半径），且卡底本是纯深色——blur 无信息增益 → glass.md blur 元素级纪律 + #0B0D11 实底实测；**弃掉**「全卡真 blur」的原型字面（视觉等价物已存在）
2. mesh 渐变与「渐变=弱站信号」冲突 → **单色相族低透明度层**（≤0.15/层、径向、至多两层）作为本档**唯一戏剧源**——cinematic 的效果预算制在此收拢为「mesh+发丝微光共占一份」→ 命名风格=预先申报的自由轴（typeui terracotta 案确立的 brief-wins 边界）；**弃掉**多彩 aurora mesh（那才是被 22% vs 52% 实证击毙的东西）
3. 白/10 发丝环想更亮 → **白/8-10 封顶**、内高光 ≤0.15 → 玻璃读感靠「边缘亮度对比」而非亮度本身 → 假玻璃三件套实测（卡 16.25 AAA 不受影响）；**弃掉**高亮描边（发光边框=AI 告示牌）
4. 零玻璃降级想只给 @supports → **Tier 2 实底回退必发**（粉底色 solid 88%+内高光），mesh 加 `@supports not` 平涂 void → 玻璃风格的可及性不是选项 → glass.md Tier 2 强制；**弃掉**「不支持就算了」

## Seed & Tokens（引擎重推导 + 玻璃最坏合成实测 2026-10-22）

- seed：OLED 黑（#050505，近无色相保留原值——achromatic 签名）；卡面 Vantablack hue 264 @ C0.009；mesh demo 单色相 hue 210（品牌可换）；玻璃 tint rgba(16,19,24,0.72)

```css
/* 深空族（引擎重推导） */
--pr-bg:      #050505;                 /* oklch(0.115 0 90) OLED 黑 */
--pr-card:    #0B0D11;                 /* oklch(0.159 0.009 264) Vantablack 卡 */
--pr-text:    oklch(0.93 0.008 250);   /* #E4E8EE on 底 17.03 AAA · 卡 16.25 AAA */
--pr-muted:   oklch(0.70 0.012 250);   /* #999FA6 on 底 9.12 AA */
--pr-hairline: rgb(255 255 255 / 0.09);/* 白/9 发丝环（8-10 封顶） */
--pr-tint:    rgba(16, 19, 24, 0.72);  /* 玻璃条 tint（alpha 内建 ≥0.70 floor） */
/* mesh：单色相 hue 210，两层径向 ≤0.15 opacity，radial at 20%/-10% 与 80%/110% */
/* 假玻璃卡三件套 */
--pr-fake-glass: background #0B0D11 + inset 0 1px 0 rgb(255 255 255 / 0.12) + 1px solid var(--pr-hairline);
```

- 密度：低；圆角：12-16px（玻璃的柔）；阴影几乎不用（深底上影不可见——分离靠发丝环+卡底差）；动效性格：极慢透明度呼吸（mesh 层 8-12s 交替 ≤0.05 摆动，reduced-motion 全停）、内容入场 700ms fade only
- 字族性格：display=轻至中字重 sans 大尺寸（玻璃世界观里粗黑字太「实」——300/400 weight 5-7rem）；正文=同族 400；mono 只作真数据

## rules.always

- **假玻璃三件套**上一切 in-flow 卡/面板：`#0B0D11 + inset 高光 ≤0.15 + 白/9 发丝环`
- **真 glass Tier 1 配方**只上 fixed 导航/模态：tint 0.72 + blur 20px + saturate 150%；Tier 2 实底回退必发
- mesh 单色相 ≤2 层径向、每层 opacity ≤0.15、`@supports not` 降平涂 void；信任区（价格/数据/代码/法务）恒实底 opaque——**风格不豁免否决**
- 文字全部落在实底或 tint 合成实测过的面上（glass 最坏合成已测 12.20 AAA）

## rules.never

- 无多彩 aurora mesh、无紫蓝 AI 渐变组合、无发光描边、无彩虹发丝
- 无 in-flow 真 backdrop-filter（滚动件 blur 禁令）；无玻璃叠玻璃（fixed 导航下内容面永不 glass）
- 信任区永不玻璃（Tier 0 否决凌驾本风格）——价格表/代码块/图表全实底
- 无纯白文字（#E4E8EE 上限）；无 #000 底（#050505 是签名但层次靠卡面差非纯黑）

## accessibility_floor（实测 2026-10-22，5/5 PASS 含玻璃最坏合成）

text/底 17.03 AAA · muted/底 9.12 AA · text/卡 16.25 AAA · muted/卡 8.70 AA · **奶油白/玻璃条 tint 0.72 最坏合成（过 OLED/卡/accent 三背板）12.20 AAA**；hairline 为非文本装饰（分离双通道：环+卡底差 4:1+）

## measured_final（实测终值回写——种子是意图，终值是事实）

- bg 终值 **#050505**（achromatic 签名保留原值）；卡 #0B0D11 = oklch(0.159 0.009 264)；tint 终值 rgba(16,19,24,0.72)
- mesh demo hue 210；换品牌色相时重测 glass 最坏合成一对并回写
- 后续迭代以本段终值为基线

## validation

黄金 prompt：「给一个 AI 数据平台做暗色 landing（hero+能力+定价）」→ 验证：OLED 深空/假玻璃卡三件套/fixed 真玻璃导航/单色相 mesh/信任区实底 五线索命中 ≥3（**定价区实底是硬性检查项**——风格在否决前低头的样子本身是线索）。已知限制：假玻璃在非 OLED 屏上材质感减半；mesh 降级路径的平涂 void 会让页面明显变素——接受（内容不依赖氛围）；与 cinematic 同题材同屏即违规。
**GP 转正待跑**（黄金 prompt 见上——定价实底是本档特有检查项）。
