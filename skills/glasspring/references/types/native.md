# types/native.md — 原生移动/桌面类型包（平台习语与翻译层）

> When to read: 交付物是 iOS/Android 原生应用（SwiftUI/Compose），或原生桌面应用（macOS/Windows）——设计语言需要翻译成平台习语而非 Web 语法。
> Source status: The historical source ledger is not included in this public preview. Treat this card as project design guidance, not independently verified or universally applicable research.

## 1. 原生移动（iOS / Android）

### 触控与尺度
- 触控目标（官方表，HIG Accessibility Mobility 2026-10-18）：**iOS/iPadOS 默认 44×44pt、最低 28×28pt**；watchOS 44/28；macOS 28/20；Android ≥48dp（WCAG 最低 24 是地板不是标准）。本 skill 设计地板取 **44pt**（官方默认值，严于官方最低——glasspring 交付按此不变）。间距与尺寸同重：有边框元素约 **12pt** 环绕间距，无边框约 **24pt**（官方值）。
- 安全区：刘海/Home Indicator（`env(safe-area-inset-*)` 或 SwiftUI SafeArea）——底部导航与悬浮按钮必须避让。
- 字阶平台差：iOS Dynamic Type（11-34pt 语义档）；Android Material Type scale（sp，随系统字体缩放）。**用户系统字体缩放必须不破版**（这是无障碍法定要求级）。**缩放优先级（HIG Typography 2026-10-18）**：用户调大字号时优先放大其关心的内容（正文/对话），**非重点元素不跟着膨胀**（tab 标题、瞬态数值保持原尺寸）。

### 导航习语（平台差异即用户心智）
| 模式 | iOS | Android |
|---|---|---|
| 顶层导航 | 底部 Tab Bar | Bottom Navigation + FAB |
| 返回 | 左上返回箭头 + 右滑手势 | 系统返回键/手势 |
| 动作 | 工具栏图标/长按菜单 | 底部 Action Sheet/长按 |
| 开关 | iOS Switch | Material Switch |
- 混搭平台控件（Android 上画 iOS Switch）= 移植感即廉价感。

### 翻译层（Web 设计 → 原生）
- hover 态 → 长按/滑动动作（移动无 hover）；
- 玻璃 chrome → `UIVisualEffectView`/`Modifier.blur`/Compose `blur`（真材质而非假半透明）；
- tokens.md 的 OKLCH 色阶直接可用；间距 4pt 网格同构。

### 红线
- 系统手势区放可点控件（边缘返回手势冲突）；隐藏系统导航；字号不随系统缩放；Web 式弹窗轰炸。

## 2. 原生桌面（macOS / Windows）

### 交互习语
- 键盘一等公民：全流程 Tab/方向键可达、快捷键（⌘C/V/S、Esc 关弹层）、菜单栏完整（macOS）。
- 多窗口/多文档心智（macOS）；窗口尺寸自由拖拽 → 响应式必须真做。
- 右键上下文菜单是桌面高频习语（Web 端常忽略）。

### 主题机制
| 平台 | 主题入口 |
|---|---|
| macOS | NSAppearance（aqua/darkAqua）、系统 accent color |
| Windows | WinUI ThemeResources、系统 accent、Mica/Acrylic 材质 |
| Electron | nativeTheme.shouldUseDarkColors + CSS 变量桥 |
| Qt | QPA 主题插件/样式表 |
- 红线：自绘窗口铬（拖拽区/圆角/阴影）覆盖系统行为；不尊重系统深浅色设置；桌面端用移动端超大触控目标（浪费密度）。

## 3. 质量底线

- 无鼠标完成全部核心流程（桌面）；单手拇指热区完成高频操作（移动）。
- 系统深浅色/字号缩放/减弱动效全部尊重。
- 原生控件优先：能用系统组件就不自绘（日期选择器/分享/打印）。
