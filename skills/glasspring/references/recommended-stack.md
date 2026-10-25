# recommended-stack.md — 推荐栈组合（React/Next.js 生态）

> When to read: 目标栈为 **React/Next.js + Tailwind** 且用户未指定组件库时。非 React 项目跳过本文件。
> Source note: This card contains project guidance and changing library details. Its omitted research ledger is not available in this preview; verify current package versions, APIs, and vendor guidance before use.
> Last verified: 2026-10-24。

## 核心原则

**优先复用成熟库。严禁在已有依赖可以正确表达的情况下自行设计实现组件和行为。**

指定好库清单，即使 oneshot 也能出不错的前端——因为每个库都承载了一个复杂领域的已验证实现（a11y/键盘导航/焦点管理/ARIA），agent 从零实现这些几乎必然引入缺陷。

**内嵌文案本地化扫描**（2026-10-22，dnd-kit 查证升级为栈级律）：凡带内建文案的库（拖拽播报/空态/aria 指引），中文交付前必须扫一遍**库内英文串**——dnd-kit 已证实例（instructions/announcements 默认仅英文）；headless 库（cmdk/Radix 原语）天然免疫，styled 库（Kumo/Radix Themes/sonner）逐个过。检出即本地化或换 headless 层自管。

**路线选择判据**（复制型 vs 依赖型，2026-10-22 成文——两条构建样本路线的决策入口）：
- **复制型（shadcn）**：需要改组件内部源码 / 设计语言深度定制（glasspring 的默认搭档——token 层直写）/ 团队要审计每一行 UI 代码
- **依赖型（Kumo / Radix Themes）**：接受厂商语义 token 即可表达设计 / 求最快到 polish（升级靠 npm）/ 已在厂商生态（Cloudflare 项目→Kumo）
- **既有项目从其现状**（components.json→shadcn 路线；已装 @radix-ui/themes 或 @cloudflare/kumo→依赖型路线）——迁移仅在用户明示时启动（走官方 migrate 技能）
- 两条路线**不混装**（依赖去重第一查的推论）；glasspring 设计语言两条路线通吃（token 层各自映射）
- **三种接线机制**（三条构建样本实证）：shadcn=CSS 变量层（:root/.dark）+ components.json；Kumo=CSS @import（exports 路径+@source+顺序敏感）；Radix Themes=**运行时 Theme 上下文**（`<Theme accentColor grayColor radius>` props 供 token，换肤不改 CSS）。接 themed 库先清脚手架锅炉板 CSS（color-scheme/暗色字色与库冲突——axe h1 违规实证）

**依赖去重三查**（严格限制重复依赖，2026-10-22 成文）：①**同职责库不并存**——原语层 Base UI / Radix / React Aria 三选一（shadcn 默认 Base UI、老项目 Radix、Kumo 也是 Base UI——混装=三套焦点管理并存）；②**新增依赖前先查已装**（`npx shadcn@latest add` 前先查项目组件清单，shadcn 官方技能明令不导入未添加的组件、不重复添加已装的）；③**库能力覆盖时禁手写**（下反模式表）。

## 来源纪律（怎么用库——shadcn 官方技能对齐 2026-10-22）

1. **先用现成，再写自定义**：写任何 UI 前 `npx shadcn@latest search -q "<关键词>"` 查注册表；**"Compose, don't reinvent"**——设置页=Tabs+Card+表控件，仪表盘=Sidebar+Card+Chart+Table
2. **永远走 CLI 不抓源文件**："NEVER fetch raw files from GitHub manually — always use the CLI"；更新上游用 `add --dry-run --diff` 智能合并，**无用户明批永不 `--overwrite`**；preset 码永不手解
3. **registry 必须显式**："Never default to a registry on behalf of the user"——用户未指定注册表（@shadcn/@tailark…）就问（brief-wins 同构）
4. **className 只管布局不管样式**：禁覆写组件色/字型；语义色 only（禁 `bg-blue-500` 裸值）、禁手写 `dark:` 覆盖；等尺寸用 `size-10`，间距用 flex `gap-*` 禁 `space-x/y-*`
5. **内置组件优先于手写标记**：Alert（提示）/Empty（空态）/Separator（非 `<hr>`）/Skeleton（非 animate-pulse div）/Badge（非样式化 span）；Dialog/Sheet/Drawer 必有 Title、Avatar 必有 Fallback；overlay 禁手写 z-index
6. **第三方注册表组件入项目后过一遍**：修硬编码导入路径/补缺失子组件/图标导入换项目 `iconLibrary`
7. **迁移有官方技能**：shadcn 仓库自带 `skills/migrate-radix-to-base`——Radix 老项目升 Base UI 走它，不手搬

## 推荐栈

> **原语层已换代（2026-10-22 官方 changelog + base-ui.com 直读核实）**：shadcn/ui 自 2026-07 起 **Base UI 为默认原语层**（组件页移至 /docs/components/base/），现行官方 styles 为 Rhea/Sera/Luma（2026 年 4-5 月）；Radix 降为可选层。「Nova」是社区 Base UI preset 名（如 base-nova style），非官方 style——用户提「shadcn Nova」时按此对齐。原语层收敛大势：shadcn 默认 + Kumo 均基于 Base UI。**Base UI 地面真相**：Radix + Floating UI + Material UI 三生态原作者重建（七人全职——可持续性信号）；**原语层自带 W3C APG + WCAG 2.2 组件行为合规**——a11y 分工即此显式化：**行为合规归原语层，表面对比/材质/动效归 glasspring 门禁**；npm 包名 `@base-ui/react`；纯 headless（零 CSS 附带，Tailwind/Motion 皆容）。

| 职责 | 推荐 | 备选 | 选择理由 |
|---|---|---|---|
| **UI 组件** | shadcn/ui（**Base UI 原语**，2026-07 起默认；styles: Rhea/Sera/Luma） | Kumo（Cloudflare）/ Radix / React Aria | 源代码可控（复制进项目）；a11y 已内建；可定制不 lock-in。用户指定已有组件库时优先保留其系统。 |
| **Kumo 专项** | `@cloudflare/kumo`（Cloudflare projects） | — | Use the current official component and design guidance. Confirm installed version, required CSS imports, Tailwind content scanning, and icon dependencies in the target project before implementation; these details can change by release. |
| **图标** | Lucide | Phosphor / Tabler | currentColor 继承（单色语义，禁在图标内上多色）；具名导入 tree-shakeable；一致 stroke；MIT |
| **动画** | Motion（原 Framer Motion） | CSS transition / GSAP | React 原生；声明式；reduced-motion 内建。bundle 注意：固定元素用 `m` + `LazyMotion` 减包；组件内响应系统级降级用 `useReducedMotion()` 钩子而非散落 CSS 媒体查询 | **环境边界**（Sonnet 5 提示词 2026-10-23）：Motion 需构建管线，claude.ai artifact 白名单无此库——artifact 沙箱交付降级为 Tailwind core + 白名单库（lucide-react 0.383.0/recharts/d3/shadcn）；交付环境先问「有没有构建管线」 |
| **可调面板** | react-resizable-panels | — | 声明式 resize；键盘可达。Major versions may change exported names and props; check the installed package's documentation and exports before implementation. |
| **拖拽** | dnd-kit | @hello-pangea/dnd | 轻量；传感器抽象；a11y 内建。**查证 2026-10-22**：KeyboardSensor 默认启用（useSortable 自带箭头跳格增强）——真正必须手动的：①instructions/announcements **默认仅英文，中文项目必须本地化**（`announcements` prop + 文档本地化指引）②自定义播报用「位置」措辞非索引③拖拽把手用真 `<button>`。域名已漂 docs.dndkit.com→dndkit.com |
| **状态管理** | Zustand | Jotai / Valtio | 最小 API；无 boilerplate；中间件生态。重渲染纪律：组件内用 selector 订阅（`useStore(s => s.slice)`）而非解构整个 store——默认全等比较防多余重渲染 |
| **命令面板** | cmdk | — | ⌘K UI 原语；a11y 完整；headless 无内嵌文案（本地化扫描免疫）。库域法：可访问名走 `<Label>`；过滤逻辑用库的，禁自写输入过滤绕过其排序/高亮 |
| **Toast** | sonner | — | 堆叠/暂停/免配置；优雅动画；aria-live 内建。库域法：`<Toaster>` 全站挂载一次（多实例=多重 aria-live 竞争）；关键动作确认不靠 toast（cross-ref product.md 弹层焦点三件事） |
| **抽屉/底部面板** | vaul | — | 触摸友好；拖拽关闭。库域法：vaul 基于 Dialog 原语——与 Dialog **禁同屏叠开**（双遮罩双焦点陷阱）；把手（Handle）可点面积 ≥44px 命中区 |

## 选择标准

1. **a11y 内建**：键盘导航/焦点管理/ARIA 属性由库处理，agent 不用想
2. **源代码可控**：复制进项目或 MIT 开源——不 lock-in SaaS
3. **Tree-shakeable**：只打包用到的
4. **TypeScript 优先**：类型完整
5. **社区活跃**：维护活跃、文档齐全、Stack Overflow 有答案

## 反模式（禁止自行实现）

| 禁止 | 原因 | 用库 |
|---|---|---|
| 手写 Modal/Dialog | 焦点陷阱/Escape/aria-modal 极易遗漏 | Dialog（Radix/shadcn） |
| 手写 Dropdown | 键盘导航/typeahead/aria-activedescendant 极易遗漏 | DropdownMenu / Combobox |
| 手写 Tooltip | 定位/auto-flip/delay/aria-describedby 极易遗漏 | Tooltip |
| 手写 Toast 队列 | 堆叠/暂停/aria-live 极易遗漏 | sonner |
| 手写 DnD | 传感器抽象/碰撞检测/键盘替代极复杂 | dnd-kit |
| 手写 Resizable panel | 指针捕捉/键盘调整/持久化极复杂 | react-resizable-panels |
| 自制图标集 | 一致性/可访问性/maintenance 成本高 | Lucide |
| 手写动画缓动 | 物理感/一致性/性能极难调对 | Motion 内建 spring/easing |
| 手绘地图 SVG 路径 | 地理投影/边界精度/交互全错（v0 生产律 2026-10-23） | react-simple-maps / Leaflet / Mapbox |
| 浏览器原生弹窗 alert/confirm/prompt | 无焦点陷阱/无 aria/样式失控（Orchids 生产律 2026-10-23） | Dialog 组件 + sonner toast |
| AI 图像工具生成图标/Logo | 风格失控+锯齿+语义漂移（Orchids 生产律） | lucide-react 具名图标 |
| 资产生成写在代码内（内联 SVG 大段/生成调用混入组件） | 资产先于代码——生成→落盘→引用（Orchids 律） | 预生成资产文件 |

## 与 glasspring 的分工

| 层 | 谁负责 | 内容 |
|---|---|---|
| **设计语法** | glasspring | 什么看起来好/为什么（色彩比例/层级/间距节奏/动效语义） |
| **推荐栈** | 本文件 | 用什么库实现（组件/图标/动画/拖拽/状态） |
| **验证链** | glasspring | 证明结果不是 slop（对比度实测/slop 扫描/输出契约）。a11y 分层：组件**行为**合规（焦点/键盘/ARIA）由原语层（Base UI APG+WCAG 2.2）承担；glasspring 门禁验证**表面**（对比度实测/材质否决/动效语义）——两层各查各的，不重复测也不留空 |

推荐栈是设计语法的**实现载体**——glasspring 说"色彩在数据不在 chrome"（AF1），React Aria + Tailwind 确保实现时色彩 token 只出现在数据元素上。
