# Domain pack — developer & infrastructure tools (devtools, cloud consoles, security, data/BI, B2B SaaS)

> When to read: the user is a professional operating software — terminals, observability, CI logs, cloud consoles, SOC dashboards, BI, CRM/admin back-ends.
> Source status: The historical source ledger is not included in this public preview. Treat this card as project design guidance, not independently verified or universally applicable research.

## The one rule

**Information fidelity over aesthetics.** Numbers, logs, code, timestamps must be trustworthy character-for-character. Users here are either in flow (coding) or in an incident (oncall) — "pretty but slower" and "formatting that breaks copy-paste" are rage features.

## Shared grammar

- Mono for all data: log lines, IDs, hashes, timestamps, diffs. `tabular-nums` right-aligned in tables.
- Dark theme is the default mental model (Grafana tradition); semantic colors ONLY for severity (error red / warn amber / ok green / info gray) — never rainbow syntax or gradient severity.
- Copy buttons on every code/command/ID block with a "copied" confirmation — omission is a defect.
- Keyboard-first: command palette (⌘K), visible shortcuts, `?` help layer.
- Density: compact rows, stable line rhythm; list pages denser than detail pages.
- **Data updates never animate.** New log lines appear; chart refreshes replace in place; animate only first paint (≤300ms growth-in).

## Surfaces

### Devtools deep water（终端 / 可观测性 / API 文档 / CI）
- Psychology: incident responders need a stable reference frame; decoration reads as noise.
- Motion 1/5: allowed — log auto-scroll, copy feedback pop, diff expand. Everything else static.
- Glass: top nav and settings panels at most. **Never** on terminal/log viewer/code blocks/chart canvas — any contrast reduction is an incident risk.
- Components: time-range picker (relative: last 5m/1h), severity filter chips, collapsible log cascade, status badges.

### Cloud consoles（AWS / Cloudflare / Vercel 型）
- Psychology: responsibility (deleting prod = incident), bill shock, multi-service cognitive overload.
- Design: resource tree left, breadcrumbs top; region/AZ pickers are first-class; cost visualization with labels; semantic token colors strictly (success/warning/critical/info).
- Motion 1.5/5: tree expand, region cross-fade; **destructive-confirmation dialogs enter with damping, not bounce** (weight matters); destroy flows move step-by-step, static and explicit.
- Components: type-the-resource-name confirm, quota bars, activity/audit streams, tag system.
- Red lines: one-click deletes, toast as the only record of a destructive action, visually hidden billing items.

### Security products（CrowdStrike / Wiz / 1Password 型）
- Psychology: alert fatigue vs adrenaline; the UI is an operations console, not a horror movie.
- Design: severity ladder strictly five levels (critical red / orange / medium yellow / low blue / info gray); attack-path graphs with blast-radius highlight; every number drills down to evidence.
- Motion 2/5: one attention pulse (≤2 loops) for critical alerts; graph expand spring; scan progress = deterministic bar, never spinner. Otherwise still.
- Glass: marketing hero and empty states only. **Never behind severity badges or alert rows** — translucency corrupts the color semantics.
- Red lines: cute animations on attack events, unexplained score changes, hiding the evidence chain ("why is this a threat").

#### Security product marketing（安全产品自己的营销页）
安全产品的**营销页**与**运营控制台**是不同面——营销页靠证明自己不会被攻破来传达信任，而非靠 alert 语义。四个补充规则：
- **审计标识 = 可调阅文件而非徽章**：编号、覆盖期、复审日期、核验出口——绿锁/盾牌贴纸是安全剧场（cliché），evidence-first 档案语法才是信任信号。
- **营销演示的数据必须与产品同一口径**：强度计/破解时长等演示数字须印出估算假设（硬件假设/平均命中/KDF 增益），并保证页面内部自洽——光谱表与演示卡对同一密码的估算差一个数量级 = 信任毁灭。
- **零请求声明的可验证形式**："本地运行零请求"须配套可验证提示（Network 面板提示/无 fetch 代码），不是无来源的自称。
- **绿锁 cliché 无条目也是红线**：反 slop 清单的 dark+acid-green 只间接覆盖；安全营销的典型翻车（荧光盾牌/锁头/矩阵雨）需单独识别并拒绝。

### Data / BI（Tableau / Looker / Metabase 型）
- Psychology: verification mindset — "the chart is pretty but how was it computed" kills trust.
- Design: big chart, small chrome; category palettes 6–8 colors colorblind-safe; filters as chip row above; exports (CSV/image/PDF) expected by default.
- Motion 1.5/5: first-paint growth only; **filter changes swap data instantly** (comparison reading); drill-through = level push transition.
- Glass: dashboard header/share modal at most; never chart containers (gridlines and data-ink must stay clean).
- Red lines: truncated y-axes unmarked, hidden query logic, front-end animation over large datasets.

### B2B SaaS / admin back-office（Salesforce / HubSpot / 中后台）
- Psychology: high-pressure operators; every extra click is tax; delight comes from speed, not surprise.
- Design: neutral gray scale + one brand color for primary actions; row-height density switcher (comfortable/compact); detail = header + tabs + related lists; batch toolbar appears on selection.
- Motion 2/5: skeleton→fade; drawer slide-in spring; everything else ≤150ms. Glass: nav bar, ⌘K palette, record detail drawer — never table rows/cells.
- Components: frozen-column tables with inline edit, kanban pipeline, saved views, bulk actions.
- Red lines: importing marketing-site styling into the back office, hiding operations for aesthetics, hover popovers covering the next row.

## Domain-wide red lines
Non-mono data text; animating data updates; more than one accent color in severity systems; translucency anywhere evidence/logs/numbers live; slow first paint on dashboards (perceived perf is a feature — Linear's core lesson).
