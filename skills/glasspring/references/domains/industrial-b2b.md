# Domain pack — industrial & B2B（制造/物流/建筑/农业/能源电信 + 法律会计/专业服务）

> When to read: industrial commerce & operations — manufacturing configurators, logistics tracking, AEC/construction, agtech, energy/utilities/telecom; plus professional-services rigor (legal, accounting).
> Source status: The historical source ledger is not included in this public preview. Treat this card as project design guidance, not independently verified or universally applicable research.

## Surfaces

### 制造/工业 B2B（西门子型）
- Spec tables are the crown jewels: multi-column comparators (Carbon data-table pattern), strict units (kW/A/IP67), Excel export mandatory; warning yellow reserved for REAL safety semantics.
- Configurator: stepwise filter + compatibility check, 300ms damped updates; EOL products must visibly link successors.
- Hidden scenes: shop-floor tablets (gloves → big targets), NOC walls (3m readable).
- Red lines: gating specs behind lead forms, safety semantics drowned by brand color.

### 物流/供应链（Flexport 型）
- One tracking number = one lifecycle timeline (booking→departure→transshipment→customs→delivery); **ETA as confidence interval with update time, never a fake-precise date**; anomalies push proactively with action options.
- Motion 2.5/5: milestone lighting, position pulse, map-follow easing — value motion; tables quiet.
- Glass: map shipment card, sticky status strip; customs/document tables solid.
- Components: document vault (B/L, invoices), multi-currency cost breakdown, #bottom-state emptiness with format example.

### 建筑/AEC（Procore/Autodesk CC 型）
- Office+field dual-scene: drawings always white-bg black-line (field print habit); drawing revision metadata (Rev A, C-101) in bold mono; offline-first mobile (no-signal sites are normal, sync state explicit).
- Red lines: wrong drawing version = worst-case incident — version-compare entry must be prominent; silent conflict overwrite forbidden.

### 农业/AgTech（Climate FieldView 型）
- Sunlight-beaten operability: high-saturation palette, ≥48px targets, **zero hover dependency** (cab has no mouse), season-time (not calendar) axes, offline capture with return-to-yard sync, explainable agronomy cards ("why spray now").
- Motion 1/5 — the most restrained domain: glare + vibration make motion unreadable and costly.
- Glass: **explicitly avoided** (contrast loss in sun, misreads in cabs).
- Red lines: undated map layers (last year's data used as this year's), Wi-Fi assumptions.

### 能源/公用事业 + 电信（Octopus 型 vs 传统型）
- Bill page = inverted pyramid: total largest, expandable detail; usage charts daily/weekly/monthly; GOV.UK-style explicit labels not footnotes; estimated readings flagged (estimated reading must be explicit).
- Consumer motion 3/5 (usage ring growth, live-meter pulse, achievement badge spring — the rare gamifiable utility); billing/switching forms 1/5 static.
- Senior-heavy audience: WCAG AA floor, large-type mode, bill as email+PDF trust artifact, complaint/aid entries not in FAQ.
- Red lines: red on bill amounts (red = overdue only), dark-mode bills, lost switching progress.

### 法律/会计（MyCase/Xero 型 — 严谨迁移自专业服务）
- Legal: serif document typography, 6-minute-unit timers in mono, trust-account balance visible, conflict-check prompts; motion 1/5 (signature checkmark spring only). Accounting: 2-decimal exact display (no rounding drift), bank-reconciliation match = the one dopamine spring, period selectors, filing-deadline reminders uncollapsible.
- Red lines: client-visible opposing-party leakage, display-rounded money, tax deadlines folded into notification centers.
