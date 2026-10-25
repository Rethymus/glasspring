# platforms/desktop.md — 桌面平台适配器（Electron/Tauri/Qt/WinUI/macOS）

> When to read: 交付物运行在桌面操作系统（Windows/macOS/Linux）——无论 Electron/Tauri/Qt/WinUI 还是 Web 应用套壳。
> Source status: The historical source ledger is not included in this public preview. Treat this card as project design guidance, not independently verified or universally applicable research.

## 1. 桌面交互习语（与 Web 的关键差异）

- **窗口是自由尺寸**：320px 到超宽都可能——真响应式（非断点假响应）；记住窗口尺寸与位置（下次打开还原）。
- **键盘一等公民**：全流程 Tab 可达；标准快捷键（⌘C/V/S/N/W、Esc 关弹层、⌘, 设置）；菜单栏完整（macOS 菜单栏 + Windows 顶栏菜单）；快捷键助记面板（? 唤起）。
- **右键上下文菜单**是高频习语（Web 端常缺）。
- 多窗口/多标签：状态按窗口隔离；拖拽文件进窗口（OS 集成）。
- 系统集成：深浅色跟随系统（nativeTheme）、系统通知、托盘/菜单栏图标、文件关联、开机启动（用户可选）。

## 2. 主题机制（按框架）

| 框架 | 深浅色与系统桥接 | 材质 |
|---|---|---|
| **Electron** | `nativeTheme.shouldUseDarkColors` → CSS 变量桥；`themeSource` 三态 | 振动/背景色自管；`vibrance`（macOS） |
| **Tauri** | 同 Electron 模式；Rust 侧窗口配置 | 依 OS（acrylic/macos-vibrancy 插件） |
| **Qt/QML** | QPA 风格（Fusion/macOS/Windows）+ 样式表 | Materia 风格插件 |
| **WinUI 3** | ThemeResources + 系统 accent + Mica/Acrylic 材质一等公民 | 系统 API 直接给 |
- 红线：自绘假窗口铬（假红绿灯按钮）；不监听系统主题切换事件（只初始化一次）；托盘/菜单行为与主窗口状态脱节。

## 3. 布局与密度

- 桌面密度 > 移动：行高更紧、信息更多、字号略小（13-14px 正文常见）。
- 侧栏导航（可折叠）+ 内容区 master-detail 是生产力应用默认骨架。
- 悬浮面板/抽屉承载二级操作；右键菜单承载三级。
- 红线：移动端底部 Tab Bar 搬上桌面；超大字号触控目标（浪费桌面密度）。

## 4. 质量底线

- 深浅色切换实时生效（不重启）；系统主题事件监听。
- 窗口最小尺寸可用（非假最小）；全键盘无死区。
- 原生菜单/托盘/通知与界面状态一致。
- 自动更新提示不阻塞工作流（后台下载+重启邀请）。
