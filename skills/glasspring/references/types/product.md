# types/product.md — software product pack (dashboards, admin, tools, data-dense screens)

> When to read: the deliverable is a software product surface — dashboard, admin/back-office, monitoring, editor, IDE-like tool, settings, any table-heavy or workflow-heavy screen. NOT for marketing/landing pages.
> Source status: The historical source ledger is not included in this public preview. Treat this card as project design guidance, not independently verified or universally applicable research.

## 0. The one rule

**Efficiency is the aesthetic.** Users live here 8 hours a day; delight comes from speed and predictability, not decoration. Perceived performance is a feature (Linear's core lesson).

## 1. Tables & data grammar

- Numbers: `font-variant-numeric: tabular-nums`, right-aligned, mono stack for IDs/hashes/timestamps/logs.
- Row heights: offer comfortable/compact toggle (Ant pattern); default compact for >20-row views.
- Money/danger columns never under translucent chrome; every cell content must survive `screenshot test`: nothing important hidden by chrome at rest or scrolled.
- Frozen header row; inline edit where workflow demands; batch-select with a contextual action bar (count + actions), not per-row buttons.
- Sorting/filtering: URL-synced state so views are shareable; filters never reset each other (Baymard-tested failure mode).
- Long lists: virtualize or paginate; never render 5,000 DOM rows.
- **实测基线：23 个真实产品屏的中位数**（taste-skill app-screens 85k 研究语料竞品研读 2026-10-20）：① **色彩花在数据不在 chrome**——着色像素占比中位约 3%（17/23 ≤5%），12/23 屏**无实心主按钮**；② **KPI 即文字非磁贴**——23 屏零例"图标圆底 + 迷你 sparkline 贴 KPI"；③ **表面扁平**——17/23 卡片无阴影，分离靠 1px 线或一个色阶；④ 仪表盘标题小（9 屏无 >16px 标题，有则中位 24px——**没有 hero 头**）；⑤ **表格 = 线与对齐**——无斑马纹、无表头色带、数字右对齐；⑥ **数据状态诚实**——零打印为零、缺失画灰杠、空区保留框架。
- **阴影=渐变照明边界律**（meodai briggs-colours-objects-light 深读 2026-10-24）：阴影/高光须读作**渐变的照明边界**，物体表面/边缘须读作**锐利的反射率边界**——投影用大 blur 渐变（照明语义），描边/分隔用 1px 锐线（反射语义），两者互换即「光照读作贴纸」的违和感来源；屏是发光体却被读作「照亮的页面」（UI 灰阶/层级线索正是利用这一解析）；像素统计≠感知色证词（照片曝光/白平衡按目的选——截图像素研究测的是「曝光良好的照片」非色觉）——截图对账须配成对实测
- A zero-offset, zero-blur shadow can create an outline without changing box layout. Use it only when that surface treatment fits the existing system; use a real border when users need a crisp divider or clear high-contrast edge.
- **图表 = graphical object**：有意义笔画/图形元素对比度按 **3:1**（WCAG 1.4.11 non-text）而非正文 4.5
- **Chart choice and alternatives**: choose a chart that fits the user question and data size, and include a readable text or table alternative for complex visualizations. Do not treat fixed point or series counts as universal prohibitions; validate them with the task and audience.
- **数据区形态变异**（nothing-design §2.9 + XIAS "three different shapes" 双源确认）：同屏 ≥3 个数据区必须**变异视觉形态**——hero 大数（唯一重量级）/分段进度条/同心环/迷你趋势线/条形排名……不做三张同形卡。形态选择跟数据语义走：单指标→hero 数，进度→分段条，多部分占比→环，趋势→sparkline。
- **Multi-series charts**: distinguish series with more than color alone. Combine labels, shapes, line styles, and sufficiently different colors, then check the chart in the actual viewing context.

## 2. Data updates NEVER animate

- Refreshed data replaces in place. Animate only first paint (≤300ms growth-in for charts).
- New rows/log lines appear immediately; a subtle background flash on the changed row is the maximum allowed emphasis.
- Live-tail/log streams scroll only when already at bottom (never yank the reader).

## 3. Glass budget: chrome layers only

Allowed glass surfaces: top nav, bottom dock, command palette (⌘K), detail drawers, floating toolbars. **Never**: table rows/cells, log viewers, code blocks, chart canvases, form regions, severity/status badges — any contrast reduction is an operational risk (devtools/security consensus).
Wiring: one shared blur layer per chrome cluster (no glass-on-glass); check the backdrop-root trap when animating drawers.

## 4. States are deliverables, not afterthoughts

Every list/table/panel ships: **empty** (with the one action that fills it), **loading** (skeleton matching final layout, then fade — no spinners for >1s waits), **error** (with recovery action), **partial/failed-sync** (visible staleness marker). A missing empty state is a defect.

Loading 细则（HIG Loading 2026-10-18）：**duration 已知 → determinate 进度条；未知 → indeterminate**（skeleton/spinner）——不混用假装确定；**加载不阻塞全局**——后台加载时用户可继续用其他区域（loading 是区域态不是页面态）；**不可避免的长载**给有趣的占位内容（提示/技巧），且**准确估剩余时间**来定占位内容时长（估太短占位内容没放完、太长会重复）。

## 4b. Forms & inputs grammar (HIG Text Fields, 2026-10-18)

- **Placeholder 不是标签**：placeholder 输入即消失——每个字段须有独立可见标签（或持久前缀/图标）；placeholder 只承担提示。占位符兼作唯一标签 = 无障碍缺陷 + 上下文丢失。
- **校验时机按上下文**（官方细则）：email 类在**切换字段时**校验（blur）；用户名/密码类在**切换前**即时校验（防提交后才发现）。错误就近显示并给修复动作（product.md §4 error 态）。
- **字段宽度即 affordance**：宽度匹配预期输入量（验证码窄、地址宽）；多字段纵向堆叠、同组同宽、组间分组。
- 私密数据走 secure 输入（`type="password"`，禁明文回显）；数字字段接输入格式器（千分位/小数位/百分比按 locale，勿假设呈现格式）。
- Tab 顺序 = 阅读顺序（系统默认已合理，仅必要时自定义）。

## 4c. Component grammar: nesting, stacking, states

- **嵌套卡片永远错误**（nested cards are always wrong）：卡片内再套卡片 = 层级失效 + 视觉噪音。分组用 divider/border/留白/背景色阶表达；卡片只在 elevation 传达真实层级时使用（"cards are the lazy answer"——先问空容器是否必要）。
- **同心圆角与光学对齐**（make-interfaces-feel-better 3736★ 竞品研读 2026-10-20）：嵌套元素的**外圆角 = 内圆角 + padding**——半径不匹配是界面"感觉不对"的头号原因；几何居中看着歪时按**光学**校正（带图标按钮/播放三角/非对称图标需手动微调）。
- **Double-Bezel 卡片语法**（soft-skill/classics 交叉验证 2026-10-22，同心圆角的构造化扩展）：卡片不平放——外壳（bg 黑/白 5% + 发丝环 + padding 1.5-2 + 大圆角）包内核（异色底 + inset 高光 `inset 0 1px 1px rgba(255,255,255,.15)` + `calc(外圆角-边距)` 内圆角）；按钮尾箭头必须住进圆形小屋（如 w-8 h-8 rounded-full），禁裸箭头贴字。注意与「嵌套卡片永远错误」的边界：bezel 是**材质分层**非信息嵌套，内层不承载独立分组语义
- **容器策略阶梯**（nothing-design 竞品研读 2026-10-20）：分组工具从轻到重 = **留白 > 单分隔线 > 细边框 > 面底卡**，用最轻够用的——每降一级加一层视觉重量。**最重要元素永不装箱**，让它浮在背景上。需要分隔线的时机多半是间距对比不足的症状（数据密集的结构同质列表除外）。
- **语义 z-index 标尺**：`--z-dropdown < --z-sticky < --z-drawer < --z-modal < --z-toast`，作为 token 发放并文档化；**禁止魔法值 999/9999**——每个叠加层取相邻语义档，新增层时插档而非抬顶。shadcn 桥下叠加层交组件库（cross-ref platforms/shadcn-tailwind.md）。
- **态可见律与死契约律**（XIAS verify_interactive.mjs 源码深读 2026-10-24）：①**死契约**——控件声明了 aria-pressed/expanded/checked/selected/sort 而点击后零 DOM 变更零焦点移动 = FAIL（声明了状态却什么都不做）；②**隐形态**——状态属性翻了但 computed-style/几何指纹完全不变 = FAIL（"读屏听得见，明眼人看不见"——状态翻转必须有可见指纹，等 ~260ms 过渡后再比对）；自验法：逐声明控件点击一次，问「屏阅读器听到的与眼睛看到的是否同步」
- **八态是交付清单**（design all eight states）：default / hover / focus / active / disabled / loading / error / success。键盘用户永远看不到 hover——focus 态独立存在，`outline: none` 必须有 `:focus-visible` 替代；disabled 附原因（title/aria-describedby）；交互组件缺任一适用态 = 缺陷（cross-ref §4 面板四态，那是容器级；本条是控件级）。**三源互证**（XIAS doctrine + typeui premium + 本条 2026-10-22）：每组件还需注明**键盘/指针/触摸**三输入行为
- **可逆动作用撤销，不用确认框**（undo beats confirmation）：常规可逆操作直接执行 + toast 撤销入口；确认框保留给 §5 的破坏性/不可逆动作。确认框是用户操作流的税。
- **感知阈值带出处**（pencilplaybook 竞品研读 2026-10-20）：hover 态**明度差 ≥8%**——低于此多数显示器上不可辨（WCAG 3:1 是地板，8% 是"可感知"的工艺值）；disabled 用 **40% 透明度**而非 50%（50% 与激活元素视觉竞争——MD3 与 Workday 用户测试收敛值）。状态值要么带出处要么实测，不拍脑袋。
- **键盘四查**（XIAS verify_keyboard.mjs 深读 2026-10-24）：①**Tab 可达**——可操作可见控件必须真被 Tab 到（预算 3n+20 次；常见 bug：**div 带交互 role 却无 tabindex**）；②**死键孪生**——自定义控件暴露 aria 状态必须在 **Enter/Space** 上翻转（Pass E 点击检查的键盘侧孪生，鼠标过而键盘死同样是死契约）；③**孤儿复合件**——tablist/listbox/tree/grid/menu/radiogroup 必须含至少一个可 Tab 项（`tabindex=-1` 子项豁免——箭头可达即算）；④**死箭头**——可达复合件须响应 ArrowDown/Right（roving tabindex 移动或 aria-activedescendant 变化）；弹层开着时 Tab 审计**限于弹层内**（正确陷阱的推论）
- **弹层焦点三件事的机械验证法**（XIAS verify_focustrap.mjs 深读 2026-10-24）：前置语义三件（role=dialog + aria-modal=true + 有可访问名——native dialog 由 showModal 隐含）；陷阱验证 = **Tab 循环 2n+2 次**焦点恒在弹层内（native 模态的 body 短暂停泊可容忍——真泄漏=焦点落到弹层后的可交互件）；关闭验证 = Escape 关闭后 `activeElement === 触发件`（开前给触发件打 id 以便回收比对）；**初始焦点位置未检测**（本条三件事律比它严——开层即入内仍需人工/探针把关）；CI 缺浏览器响亮失败
- **弹层焦点三件事**（ibelick fixing-accessibility 竞品研读 2026-10-20）：打开时初始焦点落在弹层内部、关闭时**焦点归还触发件**、开启期间焦点陷阱（focus trap）不漏到背景；Escape 可关；**toast 不得是关键信息的唯一通道**（aria-live 辅助而非替代）。
- **单侧彩条卡片禁令**（design-taste absolute bans + ux-ui design-doctrine 双源 2026-10-20）：card/alert/toast/callout 的**任意单侧** 3-4px 彩条（left/right/top/bottom 及 logical 形式全算——ux-ui design-taste 原文："in every direction, not just on the left"）是 AI 默认强调语法——强调用图标/背景色阶/字重承担；blockquote 的 border-left 引文约定除外（那是排版正典，且不与 border-radius 同框）。**不设扫描器规则**：正则无法可靠区分彩条卡片与引文块（v2 宁缺毋滥教训），由本条款+自审承担。
- **cursor 供职律**（ui-ux-pro-max 预交付清单 2026-10-23）：一切可点击元素 `cursor: pointer`；拖拽把手 `grab`/`grabbing`；禁用态 `not-allowed`——光标是零成本的供职性双通道（与 aria/视觉态并行的第三通道），自定义 cursor 图标禁（stitch 禁令互证）
- **长列表滚动律**（Z.ai 生产律 2026-10-23，中文市场产品）：数据长列表容器限高滚动（如 `max-h-96 overflow-y-auto`）+ **自定义滚动条样式**（原生滚动条破坏仪表盘质感）；分页 vs 无限滚动按数据更新频率定
- **意图-色彩契约**（XIAS lint_intent.mjs 源码深读 2026-10-24）：**删除/撤销/销毁类标签（delete/remove/discard/revoke/terminate…）永不穿主 accent**——「蓝色 Delete」是最常见的危险伪装；反向同样违规（confirm/save 穿 danger 色）；**同标签跨页 accent 必须一致**（填充实例比对）。验证走渲染 computed fill 对 --action-danger 令牌（"Source-grepping cannot prove this——类名说明不了它解析成什么色"）；纯中性描边式危险钮不违规（不标红 ≠ 穿错色）；裸 cancel 不算破坏性（它是全世界对话框的关闭钮，只有 cancel+宾语才算）
- **红色是中断不是层级**（同源）：红不在灰阶层级内——"没有急事就没有红色"；红色出现即宣告"看这里，现在"。数据状态色（成功绿/警告琥珀/危险红）豁免单 accent 规则，但只上在**值本身**，不上在标签或行背景。

## 5. Destructive & irreversible actions

- Never one-click: confirm popover for routine deletes; **type-the-resource-name** modal for account/resource destruction (cloud pattern).
- **破坏性动作永不获 primary/accent 突出样式**（HIG Buttons 2026-10-18："don't assign the primary role to a button that performs a destructive action, even if that action is the most likely choice"）——视觉突出导致未读误点；用系统红或次级样式承担破坏语义，确认流里的 primary role 永远给非破坏选择。
- Result of a destructive op = persistent state change with visible confirmation, never a toast that vanishes.
- Audit trail visible where compliance matters (who/when).

## 6. Navigation & layout grammar

- Record detail = right drawer or master-detail split (not full-page navigation away from the list).
- Header + tabs + related-lists three-part layout for record pages (Salesforce pattern).
- Command palette (⌘K) for power users + visible shortcut hints (`?` help layer).
- Breadcrumbs where hierarchy is >2 levels; back always works; view state in URL.
- 密度切换 (comfortable/compact) when tables are the core.

## 7. 中后台/CRUD 语法（Chinese enterprise back-office consensus — Ant/ProComponents patterns)

Query form + table as one unit; column settings + density switch in table toolbar; batch bar appears on selection; StepForm for multi-entity creation; Descriptions for read-only detail; Popconfirm for soft deletes + Modal double-confirm for hard deletes; import/export run async with progress; 面包屑 + 页签 navigation. Dark theme is an option (token-driven), rarely the default in operations contexts.

## 8. Copy & content

Clear, concise, conversational (Atlassian voice). No marketing language inside the product. Error messages: what happened + what to do next. Dates: relative ("3 min ago") with absolute on hover/title.

## 9. Quality floor for this type

Perceived first-paint < 1s on repeat visits; 交互件命中区 ≥44px 触屏/密集桌面 ≥40px 且**两个命中区不得重叠**；命中区口径含**标签并集**（包裹式或 for=id 关联的 label 计入命中面积——XIAS verify_target_size 深读 2026-10-24）与**间距豁免**（不足 24px 的目标若与其他目标圆心距均 ≥24px 则过 WCAG 2.5.8——独处的小目标不罚）；`will-change` 仅限 transform/opacity/filter 且只在首帧卡顿时加； `transition` 禁 `all`——显式列属性（防误动画布局属性，Vercel web-interface-guidelines 2026-10-20）；长文本容器必须可截断（`truncate`/`line-clamp`/`break-words`，flex 子项 `min-w-0`）；锚点标题加 `scroll-margin-top`（防 sticky 遮跳转目标）；zero layout shift on data refresh; keyboard-only completable core flows; focus-visible everywhere; every destructive action undoable OR confirmed; contrast verified including status colors on dark surfaces (`check_contrast.py`).
