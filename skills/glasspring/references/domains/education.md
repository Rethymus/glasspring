# Domain pack — education（K12/LMS · 高教 MOOC · 儿童 ⚠ · 语言学习）

> When to read: learning products — LMS/classroom tools, MOOC platforms, children's apps (COPPA ⚠), language learning.
> Source status: The historical source ledger is not included in this public preview. Treat this card as project design guidance, not independently verified or universally applicable research.

## Cross-domain rules

- Protect the learner's ownership: reduce "start" friction without manufacturing anxiety; progress motivates (Goal-Gradient) but streak-loss punishment conflicts with learning goals (Duolingo's main criticism: hearts/energy monetize anxiety — 6.8% paid conversion).
- Assignment deadlines (K12/LMS) and certificates (MOOC) are the task-center components; children's UI = huge icons + minimal text + voice guidance.
- Glass: **neutral-lean-negative** — learning products prioritise content clarity and reduced cognitive load; glass adds visual noise that competes with educational content. Use only if the brand already has a glass identity (then Tier 1 on media overlays only, never on text/quiz/navigation). Children's apps: never (COPPA simplicity compounds).

## Surfaces

### K12 / LMS（Canvas、Google Classroom 型）
- Teacher-efficiency first: SpeedGrader-style flows, to-do/deadline timeline as the home axis, parent-visible transparency. Procurement hard-gates accessibility (WCAG) — it's a sales requirement, not a value-add.
- Motion 1-2/5. Offline/low-end device tolerance (post-pandemic equity lesson).
- Red lines: teacher/student IA confusion, deadline surprises.

### 高教 / MOOC（Coursera 型）
- Credibility via institution partners; paid tier + free first-module preview (Coursera 2024 model). Progress % + certificate preview; cohort deadlines optional.
- Motion 1/5 (player controls only).

### 儿童教育 ⚠（COPPA 强监管）
- **Verifiable parental consent before collecting any personal data from under-13s** (FTC enforces; voice data + third-party SDKs are the prosecuted vectors). No behavioral ads to children — ever. Independent child mode, separated from social features.
- Design: oversized targets, audio instructions, no reading required, celebrations cute AND dismissible; purchase flows behind the parent gate.
- Motion: **1/5 基线**（与 LMS/K12 一致）；借 game.md 的 Peak-End 庆祝可作为**单次可关闭弹层**（非持续 idle 动画）；儿童动效红线：celebration 不可强制观看/不可跳过失败——答题错误不触发负面动画。
- Red lines: color/pressure inducing continuous consumption, ad placements in play flows.

### 语言学习（Duolingo 型）
- Daily low-friction loop: streak calendar, leagues (30-person tiers), lesson-length minimalism. Answer-correct spring feedback is the core reinforcement circuit (motion 4/5 — the one domain where game-motion IS the product).
- Red lines: heart/energy punishing wrong answers behind a paywall (documented criticism), guilt-driven streak restoration upsells.
