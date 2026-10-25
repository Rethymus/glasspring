# platforms/mobile.md — 移动平台适配器（iOS/Android 习语与翻译层）

> When to read: 交付物是移动 App 页面（iOS/Android 原生，或以 HTML 预览呈现移动设计）。
> Source status: The historical source ledger is not included in this public preview. Treat this card as project design guidance, not independently verified or universally applicable research.

## 1. 触控与尺度

- 触控目标：iOS ≥44pt / Android ≥48dp（WCAG 24px 是地板）。
- 安全区：`env(safe-area-inset-top/bottom)`——刘海/状态栏/手势条必须避让；底部导航与悬浮 CTA 加让位。
- **iOS Safari 边缘取样怪癖**（Adamparishspok/safari-edge-colors 竞品研读 2026-10-20）：iPhone Safari 的状态栏/底栏颜色**取样自页面边缘的 fixed 元素**（每条 ≥5px 可见才被拾取）——`theme-color` meta 在浏览器内（非安装态）不可靠且上下只能同色。全出血 hero 被白条框住时：放两条与页缘同色的 fixed 细条（可随滚动 JS 变色），`html`/`body` 背景同步；满屏视口配合 `100dvh`（web.md §3）。
- 拇指热区：高频操作沉底（可达扇区）；顶部留给低频/状态。
- 手势：右滑返回（iOS）/预测性返回（Android 14+）——自绘侧滑菜单与系统手势冲突是经典坑。

## 2. 导航习语（平台差异即心智）

| 模式 | iOS | Android |
|---|---|---|
| 顶层导航 | Tab Bar（底部） | Bottom Navigation（+ 可选 FAB） |
| 层级深入 | Push（左入页）+ 返回箭头/右滑 | 前进堆叠 + 系统返回 |
| 模态 | Sheet（底部半屏，可拖拽关） | Bottom Sheet Dialog |
| 刷新 | 下拉 rubber-band | SwipeRefresh 指示器 |
- 混搭平台控件 = 移植感即廉价感；遵循各平台 Human Interface / Material 3 组件规范。

## 3. 响应式与自适应

- 窗口尺寸类（非设备型号）：compact（<600dp 单栏）→ medium（双栏/canonical list-detail）→ expanded（canonical 双栏）。
- 折叠屏/平板：同一 app 布局自适应（list-detail 展开），非放大版手机。**折叠双屏（iPhone Duo 型，2026-09 发布）一等布局**（apple-design-skill + iphone-duo-skills 竞品研读 2026-10-20）：折叠态与展开态都是完整布局而非缩放；展开态侧栏从 tab bar 转换（**沿系统顺序**）；竖排 dock/侧边工具条是 Duo 语法；双栏在展开屏是真并列不是分屏拼凑。
- 字号：随系统缩放（iOS Dynamic Type / Android fontScale）——**sp/语义字号而非固定 px**，缩放不破版。
- 横屏：游戏/视频外，多数 App 保持竖排优先但旋转不破版。

## 4. 主题与系统

- 深浅色：跟随系统（`prefers-color-scheme` / Configuration.update）+ 应用内覆盖（三态：跟随/浅/深）。
- 材质：iOS 系统材质（blur API）/ Android Material 3 surface containers——自绘假半透明不如系统 API。
- 触感反馈（Haptics）：关键确认轻触感（iOS UIImpactFeedback / Android HapticFeedback）——桌面 Web 没有的维度。
- 红线：拦截系统返回手势无出路；弹窗套弹窗；键盘弹起遮挡输入框（要 scroll-into-view）。

## 5. 质量底线

- 单手拇指完成高频操作；键盘弹起输入框可见；弱网/离线态有设计。
- 系统分享/钱包/通知/小部件等 OS 集成按平台习语接入。
- 动态字体缩放最大档不破版；深浅色 + 任意组合对比度实测通过。
