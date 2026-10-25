# glass.md — glass/glassmorphism recipe library (3 performance tiers)

> When to read: whenever a surface might be translucent, before writing its CSS.
> Last verified: 2026-10-25. Apple’s [Materials guidance](https://developer.apple.com/design/human-interface-guidelines/materials) describes Liquid Glass for functional controls and navigation, with regular and clear variants; [MDN’s `backdrop-filter` reference](https://developer.mozilla.org/en-US/docs/Web/CSS/backdrop-filter) documents the web implementation. This skill translates those ideas to web interfaces; project-specific values below are approximations, not Apple constants.

## 0. Decision tree — run it BEFORE using any glass (all four must pass)

1. **Is this the navigation/control layer or a floating overlay** (toolbar, side panel, player controls, command palette, map info card)? If it's content (article body, table rows, forms, settings), **no glass**. Apple rule: "Don't use Liquid Glass in the content layer."
2. **Is glass-on-glass avoided?** Stacked translucent surfaces = clutter + backdrop-root breakage. Group one cluster behind ONE shared blur layer.
3. **Is the underlying content rich media / scrolling content** that justifies translucency? Over flat solid backgrounds, glass adds blur cost for no effect — use a solid surface.
4. **Trust/density zones veto**: prices, account balances, medical results, legal text, alert severity, checkout forms, log viewers, charts → opaque surfaces always (domain packs mark these).

## 1. Tier 1 — full glass (default; ~97% browser support)

```css
.glass {
  /* saturate 校准注记（apple liquid-glass 策展 2026-10-20）：Apple 实操区间 1.2–1.5×；
     180% 是 CSS 社区配方上限——追求官方观感降至 150%，追求信息密度下的克制降至 120% */
  -webkit-backdrop-filter: blur(var(--glass-blur, 20px)) saturate(var(--glass-saturate, 180%));
          backdrop-filter: blur(var(--glass-blur, 20px)) saturate(var(--glass-saturate, 180%));
  background: color-mix(in oklab, var(--glass-tint) 100%, transparent); /* tint has built-in alpha */
  border: 1px solid var(--glass-border);
  box-shadow: var(--glass-shadow), inset 0 1px 0 rgb(255 255 255 / 0.25); /* top-weighted inner highlight */
}
```

- Tint alpha floor **0.70** (light) with blur ≥ 20px — this is the guaranteed-text-contrast base. Raise alpha for bright worst-case backdrops.
- blur 20px is for bars/panels; small elements may go 40px+; **never** a full-viewport blur behind scrolling content (cost = area × radius).
- **blur 的元素级纪律**（soft-skill/classics 交叉验证 2026-10-22）：backdrop-filter 只上 **fixed/sticky 小面积件**（bars/浮动 pill）；**随页滚动的 in-flow 玻璃卡/玻璃分区 = 每帧位移触发全量模糊重算**，需要玻璃感的滚动内容改用「实底 + 内高光 + 发丝环」假玻璃（Double-Bezel 内核语法）；噪点/纹理覆盖层同理只放 `position:fixed; pointer-events:none` 层
- Include `-webkit-` prefix (older Safari).
- Recipe values in this project are *look approximations*, not official Apple values. The technique reference and license status are recorded in [the third-party notices](../../THIRD_PARTY_NOTICES.md).
- **Liquid garnish (optional Tier 1 enhancement)** — edge light that mimics refraction without displacement filters (Tier 3 hazards don't apply; all effects are plain paint):
  ```css
  .glass--liquid {
    border: 1px solid transparent;
    background:
      linear-gradient(var(--glass-tint), var(--glass-tint)) padding-box,
      conic-gradient(from 210deg,
        rgb(255 255 255 / .28), rgb(255 255 255 / .06) 90deg,
        rgb(255 255 255 / .02) 200deg, rgb(255 255 255 / .22)) border-box;
    box-shadow: var(--glass-shadow),
      inset 0 1px 0 rgb(255 255 255 / 0.28),   /* top specular */
      inset 0 -1px 0 rgb(255 255 255 / 0.10);  /* bottom bounce */
  }
  ```
  Budget: highlight alphas ≤ 0.30 combined; decoration only — removing the garnish must lose no information (same rule as Tier 3 displacement).

## 2. Tier 2 — opaque scrim fallback (always ship this path)

```css
@supports not ((backdrop-filter: blur(1px)) or (-webkit-backdrop-filter: blur(1px))) {
  .glass {
    background: color-mix(in oklab, var(--glass-tint-solid) 88%, transparent);
    background-image: linear-gradient(rgb(255 255 255 / .18), transparent 40%);
    box-shadow: var(--glass-shadow), inset 0 1px 0 rgb(255 255 255 / 0.2);
  }
}
```

Also force Tier 2 when: `prefers-reduced-transparency: reduce` (support is Chromium-only ~74% — detect it, but also respect it manually by offering a "reduce transparency" solid theme), `forced-colors: active`, or low-end device heuristics (`navigator.deviceMemory <= 2` / `hardwareConcurrency <= 4`).

## 3. Tier 3 — refraction enhancement (progressive, Chromium-leaning)

True edge refraction = SVG displacement map (rounded-rect SDF → `feImage` → `feDisplacementMap` on R/G channels) applied via `backdrop-filter: url(#lens) blur(20px) saturate(180%)`.

- **Tested hazard (glasspring N3, 2026-10-15)**: a data-URI `feImage` displacement map inside `backdrop-filter: url(#…)` **hung and blanked an embedded Chromium webview** (desktop in-app browser) — the whole document rendered empty. Rules: (1) Tier 3 lives behind a feature detect AND a device gate; (2) never in the critical render path — base Tier 1 must stand alone; (3) treat embedded webviews (Electron/WebView2, in-app browsers) as suspect; (4) ship a kill switch. Reference the technique from `assets/glass-recipes/refraction-experiment.html`, which is opt-in.
- Gate on: `CSS.supports('backdrop-filter','url(#x)')` + reduced-motion off + device heuristic pass. Safari/Firefox partially support it (displacement invisible).
- Experiment parameters used here: glass IOR 1.5, convex squircle profile `y = (1-(1-x)^4)^(1/4)`, 127-ray sampling, and RGBA encode `r=128+x·127`. These are project implementation choices, not Apple constants. Displacement is **decorative only**: removing it must lose no information.
- Technique reference: [shuding/liquid-glass](https://github.com/shuding/liquid-glass/tree/a2d2e847f793430e3409a52927af815a23f4d372) (MIT; no code imported). Never copy unlicensed code.

## 4. The backdrop-root trap (top cause of "glass suddenly invisible")

`backdrop-filter` blurs only up to the nearest **backdrop root**. Any ancestor with `opacity < 1`, `filter`, `mask/clip-path`, `mix-blend-mode`, another `backdrop-filter`, or `will-change` of those **truncates the blur** (element keeps its tint → looks like a flat colored box). Consequences:
- Don't animate parent opacity while children blur; animate `transform` or the glass element's own properties.
- For entrance animations use `@starting-style` + `transition` on the glass element itself, not opacity on an ancestor. The exit half needs `transition-behavior: allow-discrete` (Baseline 2024) with `display` and `overlay` in the transition list — otherwise the element vanishes before its fade-out plays. Both halves are plain CSS; the ancestor-opacity rule still applies.
- Audit on every change: if glass "went flat", check ancestors first.

## 5. Accessibility checklist (hard gate — all required)

- [ ] Text on glass ≥4.5:1 (≥3:1 large) measured against **worst-case backdrop**（为何必须实测：meodai color-expert 语料统计 2026-10-23——**仅 ~11.98% 的随机 hex 色对过 WCAG AA**，APCA 90 仅 0.08%——拍脑袋配色的通过率约 1/8）: run `python scripts/check_contrast.py --fg <text> --composites "<brightest>,<darkest>" --tint <glass tint>`; paste the output into design-notes.md. The tool also prints an informational APCA Lc value (Bronze: body ≥75 / other text ≥60 / large ≥45) — a second opinion that catches polarity asymmetry WCAG 2 cannot see; informational only, the gate stays WCAG 2.2. APCA 深读补注（2026-10-24）：**极性律**——浅字深底需比深字浅底**更多**对比（WCAG 两侧同权是它最大盲区）；换算桥 Bridge-PCA：Lc 58≈3:1 / 72≈4.5:1 / 85≈7:1（需 WCAG 2 向后兼容时用；WCAG 2 在深色上最易误判——浅色作背景输入）；Lc 15=不可见阈 / 30=图标与点读 / 90=久读推荐。
- [ ] Non-text (borders, focus rings, control boundaries) ≥3:1.
- [ ] **逐态对比度地板**（XIAS verify_states.mjs 深读 2026-10-24）：对比度须在 **default/hover/focus 三态各自模拟后分别实测**（hover 换底最容易塌对比；focus 用 el.focus()；disabled 跳过；测后 mouse.move(0,0)+blur 复位；透明底沿祖先链取效底）——阈值 graphical 3.0/大字 3.0/正文 4.5。注意：此门测**每态达地板**而非态间可辨（可辨由 hover 明度差 ≥8% 律承担——两门互补缺一不可：hover 与 default 相同会过地板门但挂可辨门）
- [ ] **装饰性低对比文字不豁免**：渐弱诗行、水印字等低对比文本仍会影响低视力用户，`role="img"`/`aria-hidden` 不改变其实际可读性。修复时逐档检查文字对比度；非文本装饰边框适用不同的 WCAG 判定范围。
- [ ] `prefers-reduced-motion`: no liquid wobble/displacement animation.
- [ ] **文本间距覆写生存（WCAG 1.4.12）**：用户改行高 1.5/段距 2×/字距 0.12em/词距 0.16em 时内容不得裁切（禁固定高度容器）；`rem` 排版、**不锁 `html { font-size }`**（尊重用户基准字号）。
- [ ] **Skip 导航链接**（2.4.1）：首焦点可直达主内容，跳过导航栏
- [ ] **焦点顺序=阅读顺序**（2.4.3）：Tab 次序遵循视觉布局，禁 `tabindex` > 0
- [ ] **Label in Name**（2.5.3）：可见标签文字包含在 accessible name 中
- [ ] **焦点不触发导航**（3.2.1）：focus 单独出现不触发上下文切换或页面跳转
- [ ] `prefers-reduced-transparency: reduce` → Tier 2.
- [ ] `prefers-contrast: more` → raise tint alpha + border contrast.
- [ ] `forced-colors: active` → glass falls back to `Canvas`/`CanvasText` system colors; focus indicator survives.
- [ ] Motion is never the only signal; glass never the only affordance.
- [ ] **界面底色适应律**（meodai colorandcontrast/color-vision 深读 2026-10-24）：整体带色的界面底（如蓝灰系）经**色适应**使界面中其他色被感知偏移（"can cause other colors in the interface to take on a different appearance"）——成对实测须在**真实界面底**上做，不能在纯白/纯黑底测完就移植；**高对比邻接色的振动**（chromostereopsis 色质立体视：不同波长焦深不同，散光/近视放大）——红蓝等对置高饱和邻接慎用
- [ ] **CVD 模拟器局限**（meodai colorandcontrast/accessibility 深读 2026-10-24）：模拟工具暗示每种视觉类型有**固定体验**，但异常三色视严重度谱广——**工具过+主观判 ≠ 安全认证**；多数工具对单色视模拟不当；混淆线独立不足为决策依据。正确姿势：CVD 模拟=参考输入，WCAG 合规+ΔE 加大=主要手段；H-K 效应（饱和度被感知为亮度增量）在暗模式对比评估中列干扰项
- [ ] **认证无障碍**（ux-guidelines 行 107）：密码框 `autocomplete="current-password"` 且**永不禁粘贴**（禁粘贴=认知测试，WCAG 3.3.8 违例；onpaste preventDefault=Critical 反例）
- [ ] WCAG 2.2 new criteria: focus never obscured by sticky/fixed chrome (2.4.11); dragging has a non-drag alternative or is single-pointer (2.5.7); consistent help entry across pages (3.2.6); no re-asking for same info in a process (3.3.7); authentication has a non-cognitive path or is avoided (3.3.8) — the latter four apply to all deliverables, not just glass surfaces.

## 5a. 跨平台玻璃差异（apple liquid-glass 翻译节 2026-10-20）

- **Android**：blur 昂贵且版本间不一致，平台设计语言本就不用玻璃——**优先不透明或轻透明**，不为模仿 iOS 而上玻璃。
- **Electron/Tauri 桌面**：优先**原生窗口材质**（Electron `vibrancy`/`backgroundMaterial`、Tauri `window-vibrancy` crate→NSVisualEffectView/Mica/Acrylic）——原生材质自动响应 Reduce Transparency，webview 内 CSS 玻璃不会。
- **reduced-transparency 平台矩阵**：`prefers-reduced-transparency` 仅 Chromium 系（Electron 全平台、Tauri 仅 Windows）；Tauri 的 WebKit（macOS/Linux）不认——原生读取（`NSWorkspace.accessibilityDisplayShouldReduceTransparency`）传入页面，或直接用原生材质。
- **glass 区域少而小**：动效内容之上的 backdrop-filter 昂贵（这也是 Apple 的规则）。

## 6. Apple semantics cheat-sheet (for cross-platform fidelity)

- Two variants: **regular** (blurs + luminance-adjusts for legibility; default — "use the regular variant when background content might create legibility issues, or when components have a significant amount of text") vs **clear** (highly translucent; only over visually rich media backgrounds). Clear + bright content → dark dimming layer at **35% opacity** (official value); if the underlying content is sufficiently dark (or media controls provide their own dimming), no dimming layer needed. Never mix variants in one interface.
- **Content-layer exception (official)**: controls in the content layer with a *transient interactive element* (sliders, toggles) may take on the Liquid Glass appearance **while activated**, to emphasize interactivity — this is the only sanctioned content-layer glass.
- **Vibrancy rule (official)**: "use vibrant colors on top of materials" — foreground on glass should adapt (currentColor / background-aware mixes), never fixed colors that may go illegible when the backdrop changes. For CSS this is the adaptive-tint-flip rule in this file plus `light-dark()`.
- **玻璃上单色默认（official Color §Liquid Glass 2025-12-16）**：Liquid Glass **无固有色**——取其背后内容的颜色；其上符号与文字默认单色（亮内容上用深、暗内容上用浅）。小元素（工具栏/tab bar）随底下内容在亮暗外观间自适应；大元素（sidebar）更不透明以保表面内容的可读。
- **主操作：着色背景而非符号/标签**（系统 Done 按钮的做法）；**勿给多个控件的背景着色**——彩背景只留给真正受益于强调的元素（状态指示/主操作）。
- **彩色背景上避免近似色的控件标签**——偏好单色工具栏/tab bar，或有足够区分度的一个 accent；内容大体单色的 app 可用品牌色作 accent。
- **品牌色远离多数控件**——留给主操作与状态（official Branding 2026-09-09）。**着色主操作每屏 1 个、至多 2 个，永不成排**（official review checklist #4）；品牌色想全局表达时，移入内容层让它从玻璃下滚过、被材质拾取。
- **静置可读性检查**：滚动容器**顶部静置态**就必须可读——彩色内容是后来滚到玻璃下面的，不能等它到了才失守（official Color）。
- **Background extension effect (official; SwiftUI `backgroundExtensionEffect()` 2026-10-18)**: full-screen background media should extend *underneath* sidebars/toolbars/tab bars — if a sidebar would cover an important part of the image, use the flip-and-blur variant (mirror the image beneath the chrome, blurred). CSS approximation: duplicate the media flipped vertically under the chrome region with `filter: blur()` + reduced opacity — decorative only.
- Controls/adaptations to emulate in CSS: adaptive tint flips with backdrop lightness (implement via `light-dark()` +, ideally, a JS luminance sampler on scroll containers); scroll-edge scrim under bars (`linear-gradient` fade matching surface color); "materialize" entrances (scale 0.96→1 + blur-out) instead of plain fades.
- Interactive glow / specular highlights: subtle inner top highlight (already in Tier 1) +, on hover/press, a faint radial light following the pointer — keep ≤ 0.15 alpha.
