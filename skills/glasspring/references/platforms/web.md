# web.md — Web platform adapter

> When to read: targets that are NOT plain responsive web (Electron/Tauri/Qt/native/game — for the progressive-enhancement mindset before translating), OR plain web needing the support matrix, performance budgets, or device heuristics for glass gating. Plain responsive web pages: the essentials (reduced-motion, contrast, touch targets, dark mode) already live in SKILL.md §3 and the craft files — skip this file and spend the budget on a craft file instead.
> Last verified: 2026-10-25. See the [CSS `backdrop-filter` specification](https://drafts.fxtf.org/filter-effects-2/#BackdropFilterProperty) and [MDN support notes](https://developer.mozilla.org/en-US/docs/Web/CSS/backdrop-filter); verify support in the target browser matrix.

## 1. Baseline assumptions (what you may use freely, 2026)

Ship without polyfill: `oklch()`, `color-mix()`, `light-dark()` (set `color-scheme`), `@property`, container queries + `cqw`, `:has()`, `text-wrap: balance`, `popover` + `::backdrop`, `@starting-style`, `transition-behavior: allow-discrete` (with `overlay` in the transition list — exit animations for `display:none` toggles and top-layer elements; pairs with `@starting-style` which covers the entry half), `prefers-*` media queries.
Enhance-only (feature-detect, must degrade): View Transitions (`document.startViewTransition`), scroll-driven animations, anchor positioning, SVG-displacement glass refraction (Chromium-leaning).

## 2. Feature-detect patterns

```css
/* glass: base uses Tier 1; unsupported browsers get Tier 2 automatically */
@supports not ((backdrop-filter: blur(1px)) or (-webkit-backdrop-filter: blur(1px))) { /* Tier 2 */ }
@media (prefers-reduced-transparency: reduce) { /* Tier 2 — note: Chromium-only, don't rely on it alone */ }
@media (prefers-reduced-motion: reduce)   { /* springs render end-state */ }
@media (prefers-contrast: more)           { /* raise tint alpha, border contrast */ }
@media (forced-colors: active)            { /* Canvas/CanvasText system colors */ }
```

```js
// refraction gate (Tier 3)
const canRefract = CSS.supports('backdrop-filter','url(#x)')
  && !matchMedia('(prefers-reduced-motion: reduce)').matches
  && (navigator.deviceMemory ?? 8) > 4;
```

## 3. Responsive & input

- **移动端单独艺术指导**（scroll-craft 3725★ 竞品研读 2026-10-20）：滚动叙事/沉浸页的移动端不是响应式收尾——**单独构图**（深度平面/触点锚/开场中段退场态各自重排），并验证**真实滚动帧**与降级路径（不支持时静默退化为静态构图）。
- **满屏视口用 `100dvh` 不用 `100vh`**（baseline-ui 竞品研读 2026-10-20）：iOS Safari 地址栏收缩会让 100vh 页面底部被裁——动态视口单位 `dvh`/`svh` 按场景选（dvh 随地址栏变、svh 恒为最小）；fixed 元素吃满 `env(safe-area-inset-*)`（刘海/底部横条）。

- **内容不得死于容器**（XIAS verify_overflow.mjs 深读 2026-10-24）：文字被 `overflow:hidden` 裁掉而无 ellipsis = FAIL（1px 容差；**ellipsis 豁免**=有意截断；sr-only 跳过=有意裁剪）；控件**部分重叠 >25%（较小者口径）**=布局塌陷信号——嵌套不算重叠、小件全含于大件不算（输入框内清除钮合法）、换行链接**逐行 client rects 比对**（整框跨行误报）；修法=允许换行/ellipsis+tooltip/`flex-wrap`+`min-width:0`；多宽度跑（320/414/1280）
- **RTL 镜像律**（XIAS verify_rtl.mjs 深读 2026-10-24）：`dir="rtl"` 翻转后**不得引入 LTR 没有的横向溢出**（2px 容差；测法=翻转→等 120ms→比对 scrollWidth-clientWidth 与越界元素）；镜像破碎的根治=**逻辑属性**（`margin-inline-*`/`inset-inline-*`/`text-align: start` 替代物理 left/right）
- **基层剥离测试**（XIAS verify_mobile_first.mjs 同源）：**剥掉全部 @media/@container 查询后以 320px 渲染基层**（保留 reduced-motion/print/forced-colors/contrast 等可访问性查询）——基层溢出 = 桌面优先写法的自白（"without its patches the wide base overflows"）；mobile-first 的定义性测试：**基础样式无补丁即应在手机上成立**；越界元素排除横向滚动容器内（那是合法滚动非溢出）
- **固定列网格的 `1fr` 消失陷阱**：当固定列总宽和间隙超过窄屏内容区时，`1fr` 列可能缩到 0 宽，常使文本列消失。窄屏应切换布局（例如让消息列跨满网格并允许换行）；若窄屏检查报 zero box 而桌面正常，先核对固定列总宽和间隙。
- Breakpoints: derive from content, common anchors 390 / 768 / 1440. Test all three (golden rule: screenshot at each).门禁宽度可加 **280/320 下探档**（XIAS verify_responsive 深读 2026-10-24：280 是 Android 最窄档，专抓固定 px 宽/未重置 list padding/不换行 flex/超宽 minmax 下限）；`--scale` 放大根字号压测——"A layout that only fits at exactly 16px is fitting by luck"（恰好装下=运气装下；字体回退与用户字号会破）。
- **中庸混合识别**（meodai hexaflexagon 深读 2026-10-24）：两色等量混合若**弯向灰**（chroma 流失）→ 产出闷褐/灰紫——设计意图需要中间色时**不靠两端等混**，改直接选中间色或 oklab 混合后补 chroma；"哪色是原色"不如"chroma 得失的几何"重要。
- Touch targets: ≥44×44px primary (Apple/HIG convention), WCAG 2.5.8 minimum 24×24px with spacing — pick 44 as the design floor.
- Hover is absent on touch: `@media (hover: hover)` gate all hover-only affordances; never hide critical actions behind hover.
- Dark mode: `color-scheme: light dark` + `light-dark()` semantic tokens; honor system setting by default, offer explicit 3-state toggle (system/light/dark).
- `:focus-visible` styles always; never `outline: none` without replacement; focus ring ≥3:1 against adjacent colors.

## 4. Performance budget (glass pages)

- Each `backdrop-filter` layer costs area × blur-radius per frame. Budget: blurred area < 25% of viewport on mobile; ≤ 2 blur clusters visible per screen (share one layer per cluster).
- Animate `transform`/`opacity` only; animating blur values re-renders the backdrop — avoid, or gate to Tier 3 with reduced-motion off.
- Target: Lighthouse mobile perf ≥ 90 on marketing pages; **LCP ≤ 2.5s、INP ≤ 200ms（Core Web Vitals 标准值，ux-ui performance.md 同域判例 2026-10-20）**; CLS < 0.02 (predefine image aspect ratios — slop reviews fail pages with layout shift).
- Ship Tier 2 automatically when `navigator.deviceMemory <= 2` or `hardwareConcurrency <= 4`.

## 5. Deliverable preview requirements

Any web deliverable must open as a static page (no build step) or one-command dev server, so the reviewer (human or agent) can screenshot it at 390/768/1440. Include a `<!-- VERIFY: run the installed Glasspring skill's check_contrast.py via its SKILL_ROOT path on the pairs listed in design-notes.md -->` comment in preview.html.

## 6. 2026 新增能力（research cycle 2026-10-16 更新，web.dev Baseline 2026 全清单 + MDN 逐条核实）

### Baseline 2026 Newly Available 全清单（31 项，16 CSS/HTML + 15 JS/Web API）

**对 glasspring 直接有影响的 4 项：**

| 特性 | 影响 | glasspring 应用 |
|---|---|---|
| **`contrast-color()`** | 玻璃可访问性自动化——浏览器按背景自动选黑/白文字，替代手动对比度计算 | `color: contrast-color(var(--glass-bg))` 一行解决玻璃最坏合成问题；检查目标浏览器支持并保留手动对比度验证 |
| **Style container queries** | 风格包继承——style 容器内按父级计算样式选择子级样式，**style-pack 替换机制的原生解** | `@container style(--glass-enabled: true) { … }` |
| **`:open`** | `details`/`dialog` 打开态选择器——折叠面板打开态样式无需 JS 类切换 | 技术规格折叠区/对比模块的展开态 |
| **View transition active types** | 同页多区域独立过渡控制（`view-transition-class` 分组） | scroll-telling 章节独立过渡 + 产品演示多区域联动 |

**其他相关（按需采用）：**
- `crisp-edges`：Brutalist 风格包的锐利渲染原语
- `text-decoration-skip-ink: all`：Editorial 风格包的衬线下划线精修
- `text-indent: each-line / hanging`：Editorial 风格包的首行缩进
- `baseline-shift`：数据/mono 排版的基线精调
- `rcap/rch/rex/ric`：root-relative 单位（跨风格一致的缩放）
- `Math.sumPrecise()`：JS 浮点精确求和（data 准确性）
- Custom highlights：搜索/阅读 app 的自定义高亮

**已逐条核实：** `text-box-trim` = Baseline 2026 Newly Available（2026-08 起，MDN 逐字确认）
**待核实（下轮窗口）：** `field-sizing`、`if()`、`anchor positioning`、`popover=hint`、`@scope`（2025 已可用，非 2026 新增）

### 用法纪律
以上全部按 §1"增强专用"纪律接入——@supports 门控 + 基线退化路径，绝不作为布局依赖。

- **`text-box`（text-box-trim + text-box-edge）——Baseline 2026 Newly Available（2026-08 起）**：裁切文字块上下 inherent half-leading，实现按钮/胶囊/标题的**精确垂直居中**（`text-box: trim-both cap alphabetic`）——玻璃胶囊按钮的老大难问题有了原生解；glasspring 的胶囊 CTA/章节大标题默认可用，老浏览器自动退化为常规 line-height（增强非依赖）。
- **`shape()`**：clip-path 的可读/可动画形状函数（Baseline 2025）——玻璃边缘异形/切角可用，@supports 门控。
- **`field-sizing: content`**：输入框随内容自适应（表单场景）——增强项，@supports 门控。
- **`interest-invoker`/`interesttarget`**（Chromium 133+，Chromium-only）：hover 意图延迟显示——桌面增强专用，Safari/Firefox 无。

> 用法纪律：以上全部按 §1"增强专用"纪律接入——@supports 门控 + 基线退化路径，绝不作为布局依赖。
