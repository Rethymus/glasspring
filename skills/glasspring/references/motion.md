# motion.md — spring physics & motion semantics

> When to read: before adding any animation/transition. If the answer is "don't animate", that's a valid outcome.
> Targeted source checks updated 2026-10-26; this is not a full claim-by-claim audit. Inline links identify sources checked. Apple sources include its [Motion guidance](https://developer.apple.com/design/human-interface-guidelines/motion) and [SwiftUI Spring API](https://developer.apple.com/documentation/swiftui/spring); MDN covers [`prefers-reduced-motion`](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion). Web recommendations are project translations, not Apple platform requirements.

## 0. The three questions (answer before animating)

1. **Does this interaction happen frequently?** (scroll, typing, list updates) → default to no motion. Apple advises generally avoiding custom motion in frequently repeated app interactions ([HIG Motion](https://developer.apple.com/design/human-interface-guidelines/motion)). The bands below are project heuristics adapted from [Emil Kowalski's `animate` Skill at a pinned revision](https://github.com/emilkowalski/skills/blob/2d228630ba1446365f614a108cb8252f1feda202/skills/animate/SKILL.md#L31-L37), not measured user thresholds: **100+ times/day** (keyboard shortcuts/command palette) → no animation; **tens/day** (hover/list navigation) → near-imperceptible and fast, or none; **occasional** (modal/drawer/toast) → standard motion; **rare/first-time** (onboarding/celebration) → use sparingly. Keyboard-initiated actions are this project's default no-motion rule, not a platform requirement.
2. **Is it a data update?** Chart refresh, log line arrival, score tick → **replace in place, no animation.** Animating data changes causes misreading (devtools/BI/security consensus).
3. **Is motion the only signal?** Then add a text/state signal too — "Make motion optional" + `prefers-reduced-motion` must render the end state.

## 1. Presets (Apple official values — do not invent others without marking them as such)

| preset | SwiftUI params | feel | use for |
|---|---|---|---|
| smooth | `Spring(duration: 0.5, bounce: 0)` (critically damped) | settles, no overshoot | containers, navigation transitions, sheets |
| snappy | `Spring(duration: 0.5, bounce: 0.15)` | quick, tiny bounce | controls, toggles, small confirmations |
| bouncy | `Spring(duration: 0.5, bounce: 0.3)` | playful overshoot | appearing elements, delight moments (sparse!) |
| interactive | `interactiveSpring(response: 0.15, dampingFraction: 0.86)` | very fast | direct-manipulation follow-ups |

Bounce scale: 0 = critically damped, 1 = undamped oscillation, −1 = max overdamping. From the project root, generate actual curves with `python "<SKILL_ROOT>/scripts/spring_convert.py" --semantic bouncy --css`; replace `<SKILL_ROOT>` with the host-specific project install path listed in `SKILL.md`.

## 2. The interruptibility rule (web-specific, critical)

- **CSS `linear()` springs are time-certain but NOT interruptible and don't inherit gesture velocity.**
- Use CSS `linear()` for: state transitions, entrances, toggles — anything with a fixed start and end.
- Use a JS spring integrator (Motion library or ~20 lines of semi-implicit Euler) for: drag releases, swipe cards, pull-to-refresh — anything that must continue the gesture's velocity.
- Never fake a gesture with CSS: a drag-release that restarts from zero reads as broken.
- **Gesture-direction consistency**: keep dismissal motion consistent with the opening gesture when that helps preserve spatial expectations (a paraphrase of [Apple HIG Motion](https://developer.apple.com/design/human-interface-guidelines/motion)).
- **Do not rely on motion alone for important information**: keep a visible or textual state cue; add haptics or audio only when useful and available for the target platform ([Apple HIG Motion](https://developer.apple.com/design/human-interface-guidelines/motion)).

## 3. Duration guidance (NN/g; Apple gives parameter-based, not fixed-duration, guidance)

- Feedback: ~100ms. Small state changes: 150–250ms. Large panels/regions: 300ms. 500ms absolute ceiling.
- **Per-component duration references** (adapted from the pinned [animate Skill](https://github.com/emilkowalski/skills/blob/2d228630ba1446365f614a108cb8252f1feda202/skills/animate/SKILL.md#L101-L110), not universal or user-study thresholds): button press 100–160ms, tooltip/small popover 125–200ms, dropdown/select 150–250ms, and modal/drawer 200–500ms. The source gives a general <300ms UI recommendation while listing 200–500ms for modals/drawers; treat the longer timings as case-specific. Use a short stagger only when it supports reading order, and never block interaction; no fixed stagger band is claimed here.
- Entrances slightly longer than exits (300 in / 200–250 out). Fast start, gentle settle — spring curves do this naturally.
- "150ms micro-interaction" style folklore attributed to Apple is unverified — cite springs, not magic durations.
- **缓动方向按情境**（同源 2026-10-24）：入/出场 ease-out；屏上移动/形变 ease-in-out；hover/颜色变化 `ease`（即时跟随）；匀速运动（marquee/进度）linear；**ease-in 永不用于 UI 入场**——它推迟用户正注视的时刻（弹簧曲线自带此性质，勿再叠加 easing）。非弹簧过渡的参考曲线：`cubic-bezier(0.23, 1, 0.32, 1)`（自定义 ease-out——内置关键字曲线偏弱）。
- **最便宜工具阶梯**（同源）：CSS transition → `@starting-style` → CSS animation → WAAPI → JS 库（Motion）。快速重触发一律 transition（retarget 重定向）而非 keyframes（重启）。

## 4. Spring → CSS recipe

```css
:root { /* bouncy: Spring(duration:0.5, bounce:0.3); play over ~2.0s (4τ horizon) */
  --ease-spring-bouncy: linear(<output of spring_convert.py --css>);
}
.card-pop { animation: pop 2s var(--ease-spring-bouncy); }
@keyframes pop { from { transform: scale(.92); } to { transform: scale(1); } }
```

For practical UI, prefer `--duration 0.3 …` (plays over ~1.2s) — perceptual duration is what users feel.
Implementation notes: values outside [0,1] are allowed and can encode overshoot. MDN marks `linear()` widely available across browsers since December 2023 ([reference](https://developer.mozilla.org/en-US/docs/Web/CSS/easing-function/linear)). The Web Animations API's `easing` option accepts CSS easing functions ([MDN](https://developer.mozilla.org/en-US/docs/Web/API/KeyframeEffect/KeyframeEffect)), so the same function can be passed there.

## 4a. Start/end states & input-origin rules

- **Never animate from `scale(0)`** — an element growing from nothing reads as a system glitch, not a transition. Enter from `scale(.92)–.95` + opacity 0 (the pop recipe above is the canonical form).
- **fade-and-slide 入场 = generic 点名**（官方 frontend-design 2026-10-22）：无差别 fade+translateY 入场与卡片 hover 过渡是「模板默认动效」——入场动效要么语义化（§4b 分层/题材签名），要么不做；用户触发的动效永远欢迎
- Buttons/pressables get `:active { transform: scale(.97) }` — physical press depth, spring optional.
- **hover 禁色过渡**（kumo-design 厂商纪律 2026-10-22，与「hover/focus 指示即时出现」同源扩展）：hover 的**颜色变化必须即时**（`transition-colors` 禁）——动画化的颜色变化读作迟钝；transform/阴影类可以动，颜色不许拖。
- **Popovers scale from their trigger origin** (`transform-origin` at the anchor point); modals stay centered. Scaling a menu from screen-center breaks the spatial link to what opened it.
- **入场位移 ≤8–16px + fade**，永不从远屏外飞入（ux-ui motion-choreography 同款上限）；**Never animate keyboard-initiated actions**: keyboard users navigate by rhythm — animation between their keystroke and the result adds latency they must wait through on every Tab/Enter. Hover/focus indicators appear instantly; only pointer-driven reveals animate. (Cross-ref §2: interruptibility — keyboard actions are the extreme case of uninterruptible.)
- **降级平价律**（XIAS verify_reduced_motion 三信号之 C 深读 2026-10-24）：no-preference 态可见的元素在 reduce 态**不得消失**（"Reduced motion must never cost content"——降级永不以丢内容为代价）；对照实现：双渲染快照（no-preference/reduce 各一次）**可见集 diff**，no-preference 有而 reduce 无即 FAIL。互证补强：我方 Pass C 数 animationName≠none，XIAS 加了可见集平价面；**豁免谱**：opacity/色彩过渡不算 motion（只罚 transform/位移/尺寸/位置），阈值 0.1s
- **检查 JS 驱动动画的降级行为**：Motion/GSAP 可能通过 JS/WAAPI 驱动，`getComputedStyle().animationName` 不会覆盖所有此类动画；在库内使用 reduced-motion 钩子，并结合 `document.getAnimations()` 检查正在运行的动画。
- **动画不能控制内容是否可见**：打字机或揭示动画若让内容默认隐藏，慢设备、禁用动画的引擎和过早截图都可能看到空白。让基础态内容可见，并把动画作为增强；用渲染检查覆盖 natural、初始帧和 reduced-motion 状态。
- Use ease-out curves for enter/exit; `ease-in` on UI enter makes the interface feel sluggish to arrive. Springs encode their own curve — don't double-apply easing on top of a `linear()` spring.

## 5. Domain-appropriate motion (field-tested boundaries — full tables in domain packs)

- **High-bounce zones**: short-video interactions, dating card swipes (JS spring — gesture), project-management drag & drop, quiz answer feedback, map/realtime layers (interpolation, <400ms response).
- **Zero-bounce zones** (motion budget 0–1): government forms, medical records, legal docs, crypto signing, accounting tables, admin CRUD, agri/industrial control, kiosk. Motion = 100–200ms fades only.
- **Special cases**: mental-health/wellness — slow breathing motion (4–6s cycles), springs feel mechanical there; trading — zero celebratory motion (regulatory history: Robinhood $7.5M settlement); sports betting — settlement must never render as victory celebration.
- Peak-End rule: spend your best animation on the *end* moments (success confirmations, delivery arrival) — memory is written there.

- **motion-off 测试**（feitangyuan/motion-web 765★ 竞品研读 2026-10-20）：把动效全关后再看页面——**若布局会让人尴尬，动效就是借口不是优势**；"一个漂亮机制贴在没人设计的布局上 = 失败页"。与 type.md §5a 去饰回填律互为对偶（设计侧/动效侧）。

## 4b. Hero 分层深度纪律（scroll-craft hero-depth 竞品研读 2026-10-20）

- hero-led 营销页的**分层是基线不是抛光**：动工前命名四层——背景/焦点主体/前景/大气层，并写明**什么独立动、什么重叠、什么必须物理相连**。
- **分层必须改变感知深度**：多层元素同速移动不算分层——要用明显不同的位移/缩放速率、遮挡、远近关系。
- **接触点锚定**：人留在岩石上、产品留在底座、轮子留在路上——共享位移+共同接触点枢轴可支撑不同层缩放而不飘浮。
- 真 alpha 通道检查：生成棋盘格/白底不是透明；修光晕/毛边/裁切织物。
- **动工前写层契约表**（scroll-craft approved-collection）：平面 × 资产深度 × 独立运动 × 接触/遮挡规则，六列含 typography（稳定平面）；位移量级从远到近递增（远最小→近最强克制位移）；精细指针设备可加轻指针响应且必须可加性（触屏/键盘/reduced-motion 仍得完整构图）。
- 一个连贯镜头理念；**premium = 受控的运动与时机，不是处处运动**。工作表面（仪表盘）不需要发明的营销 hero。

## 5. 视图过渡语义表（vercel react-view-transitions 竞品研读 2026-10-20）

- **每个过渡必须说得出传达什么空间关系或连续性**——说不出就别加。
- 模式语义与优先级：共享元素（name）="同一物，深入一层" > Suspense 揭示="数据到了" > 列表重排（per-item key）="同物新排列" > 状态进出="出现/消失" > 路由="去新地方"。实现时能全做就按此序全做。

## 5a. 慢放审查法（make-interfaces-feel-better 竞品研读 2026-10-20）

- 自审动效时在浏览器 Animations 面板**以 10% 速回放**，逐态走查 hover/focus/active/loading/empty——**10% 速下"感觉不对"的，就是全速下微妙错误的东西**。
- 图标切换动画用 opacity+scale+blur 而非切换可见性（参考值 scale .25→1、opacity 0→1、blur 4px→0，spring bounce 恒 0）。

## 6. 性能纪律（ibelick/ui-skills 9892★ 竞品研读 2026-10-20）

- 合成层属性优先（transform/opacity）；绘制/布局动画仅限**小而孤立**的表面，大容器上禁。
- **先测量后动画**（measure once, then animate via transform/opacity）；DOM 读写不交错；类布局效果用 FLIP。
- 滚动驱动动效用 CSS Scroll/View Timelines 或 IntersectionObserver，**不轮询 scrollTop**；离屏暂停；rAF 循环必须有停止条件。
- 动画卡顿时的选择是**降级技术而非删除动效**（prefer downgrading technique over removing motion entirely）。

## 5b. CSS Scroll-Driven Animations (optional enhancement; support varies)

- `animation-timeline: view()` / `scroll()` 实现纯 CSS 滚动驱动——**零 JS、零 scroll 劫持、零轮询**。
- taste-skill motion.md 55k 的核心洞察：**"scroll-linked means linear"**——滚动就是缓动，14/18 个 scrub 站锁定滚动条（这正是 CSS scroll timelines 做的）。
- **Browser support checked 2026-10-26:** MDN marks `animation-timeline` as limited availability and not Baseline because some widely used browsers do not support it ([compatibility status](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/animation-timeline)). Keep the `@supports (animation-timeline: view())` gate and a static completed-state fallback; verify the target browser versions before relying on the enhancement.
- **glasspring 域**：落地页滚动叙事（layout-baselines.md §分段）应优先使用 CSS scroll timelines；仅当需要复杂时间轴编排时才用 GSAP ScrollTrigger（scroll-craft 引擎）。
- **四种已验证 scrub 模式**（gpt-taste GSAP 语汇 交叉 2026-10-22）：①钉住标题+下方画廊滚动 ②图像 scale 0.8→1.0 进场+退场压暗淡出 ③**逐词擦洗**（词 opacity 0.1→1.0 随滚动点亮——注意 0.1 不是 0：起点必须可读，这是「动画不守门」在 scrub 上的投影）④滚动驱动卡片堆叠。reduced-motion 一律塌缩到静态终态（gsap.matchMedia 门控）

## 6a. 获奖站实测动效纪律（taste-skill motion.md 55k 全读，99 SOTD 研究）

- **preloader 的实测死刑**：60/99 获奖站用 preloader——**一半的页 2.5s 后仍不可读，三分之一 4.5s**；25/29 的 3s 内加载完的页在 4.5s 仍什么都不显示。house：无 preloader；首屏 HTML 立即在，场景就绪后从背后淡入。
- **scroll-hijack 的可用性代价实测**：被劫持页 usability 6.01 vs 正常滚动 6.50——访客不知身在何处/还剩多少/如何离开，键盘与读屏一无所获。
- **入场揭示的量化限制**：触发于元素顶到视口 85-90% 处、只触发一次、rise 12-32px 或行 mask；**视内任何东西隐藏不超过 900ms；首屏内容永不等待滚动**。
- **无穷动效豁免制**（XIAS verify_screen_economy 同源）：无穷动画 FAIL 除非——`aria-busy` 容器内 / live region / 忙控件的 aria-hidden spinner 兄弟（转圈不算装饰）；**豁免走 HTML 注释登记**（`screen-economy: endless-motion <≥15 字理由>`）——"a bare switch gets flipped to quiet a gate"（裸开关会被翻过去静音门禁；书面理由才会被问责）；自动播放无控件视频同罪
- **8+ 运动元素 floor 的域分野仲裁**（taste-skill house rules 2026-10-22，FM-6 裁定）：获奖展示页低于 8 个运动元素判 fail、16 以下 warn——**该 floor 仅限获奖站/作品集展示域**（AE7 纪律的域内条款），不覆盖产品工作表面（SKILL §3 频繁交互域零动效不变）；两域同产品时 landing 给足 8+、dashboard 保持 0/5，即 linear-instrument/cinematic 分界律的动效面
- **可读性地板（经本工具 --pairs fg_alpha 实测仲裁 2026-10-20）**：taste-skill 的"变暗 ≥40%"**只对大字装饰性元素成立**——#111@40% on #fff 实测 2.62:1，不过 AA-large 3:1；正文变暗到 ~60% 才保 4.5:1。ink-fill 从 45% 起实测 3.04:1（大字线恰好通过，**仅限大字**）。blur ≤8px 且落定即消失；**没有任何东西穿过正在阅读的文字**。**a11y 地板恒高于风格地板（FM-6）**。
- **ease-exit 精细化（终结两源分歧）**：ease-in 退场**只用于永久离场**（被替换的幻灯/关闭的面板），短促、约为入场的 60-70%；访客在等待看到的东西永不 ease-in。其余退场仍 ease-out。
- **reduced-motion = 更少更温和，不是没有**：保留 opacity/颜色变化，去掉位移/缩放/视差/自动播放——reduced 态就是完成态。
- **签名动效按题材选**：作品集→索引+预览；餐厅→慢交叉淡化；产品→hero 快门；报告→滚动数字。动效说不出题材就别加。
- 生成动效 tell（带频次）：同款 fade-up 每块/hover 抬升每卡/无限循环无开关（脉冲点/微光字/旋转徽章）/自定义光标（28/99，仅 10 有 reduced-motion）/scramble 打字机（标题四秒不可读）。

## 7. Reduced motion

`@media (prefers-reduced-motion: reduce)`: preserve the content and render the completed state without unnecessary movement; opacity or color transitions may remain when they help communicate state. Treat this as a project accessibility requirement, and verify behavior in target browsers ([MDN reference](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion)).
