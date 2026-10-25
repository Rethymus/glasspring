# Domain pack — money (banking, investing, payments, insurance, lending, crypto)

> When to read: the product touches people's money or financial risk.
> Source status: The historical source ledger is not included in this public preview. Treat this card as project design guidance, not independently verified or universally applicable research.

## The one rule

**Trust outranks delight.** Design-look drives ≈46% of credibility judgments (Stanford Fogg) and first impressions form in ~50ms — but in money products, every decorative choice is read as either "bank-grade" or "scam". Money amounts, confirmation screens, risk disclosures: opaque, high-contrast, motion-light. Glass may frame these surfaces (chrome, headers); it never contains them.

## Surfaces

### Retail banking / neobank（Chime、Monzo 型）
- Psychology: payday anxiety; fear of balance being seen in public; inherited distrust of hidden fees.
- Design: balance = the page's only hero number; transactions as a "today/yesterday" timeline, not a table; balance hide/blur control is standard.
- Motion 2/5: spring count-up on incoming deposit ("money arrived" ritual); lists and charts use plain ease.
- Glass: asset-overview cards may use Tier 1; **balance digits and transaction rows opaque**.
- Components: balance reveal toggle, push-notify card, cash-flow timeline, early-direct-deposit badge.
- Red lines: red = "low balance" (punitive feel); calling yourself a "bank" without disclosing the partner-bank arrangement (regulatory action exists).

### Investing / trading（Robinhood、富途 型）— compliance-heavy
- Psychology: FOMO vs loss aversion; novices systematically underestimate risk.
- Regulatory facts that shape UX: gamification enforcement is real (Massachusetts v. Robinhood settled $7.5M with digital-engagement-practices reforms; FINRA $57M). Confetti celebrations are gone from the industry.
- Design: P&L always shown with % and time-window; risk disclosure on the same screen as the order button; red/green follows the exchange's convention (US: green up; A-share: red up — never invert).
- Motion 1/5: **zero celebratory animation.** Order confirmation = instant state change. Springs only on neutral chrome (sheet open/close).
- Glass: watchlist cards may frost lightly; order ticket and confirmation opaque.
- Red lines: casino-style push copy, levels/treasures/quests around trade frequency, default-on margin.

### Payments / checkout（Stripe Checkout 型）
- Psychology: the card-number seconds are the final trust trial; any visual discontinuity = fraud association.
- Design: Stripe's own answer is to *reduce customization*: hosted page, full order summary with fees upfront, local payment methods. Minimal funnel; biggest number = amount due; every fee itemized (48% abandonment link).
- Motion 1/5: deterministic progress for 3DS/redirects; one restrained checkmark spring on success, max.
- Glass: brand/logo area only; form region opaque.
- Components: card-number auto-formatting, inline per-field validation, soft-vs-hard decline recovery (retry vs change card), wallet one-tap.
- Red lines: unknown intermediary redirect pages, "payment failed" with no reason, clearing entered data on error, hijacking the back button.

### Insurance（Lemonade 型）
- Psychology: bored & skeptical when buying; anxious & fragile when claiming.
- Design: conversational quote flow (Lemonade: ~98% of policies sold via AI chatbot) proves the pattern; plain-language summary + full-terms disclosure as two layers.
- Motion 2/5: gentle chat-bubble entrances; **claims progress = deterministic easing (time = anxiety)**; spring only on "coverage active" reassurance moments.
- Glass: quote cards and coverage-comparison cards OK; terms text opaque.
- Red lines: rejection reasons buried in links, disclaimers in smaller-than-body type, "final interpretation rights" phrasing.

### Lending / mortgage（Rocket Mortgage 型）
- Psychology: biggest debt decision of a lifetime; fear of being locked in.
- Design: one-question-per-page progression (gov.uk pattern; note: their testing showed progress indicators optional once question order is good — optimize order first); auto-save with "continue later"; rate shown as monthly payment AND total cost of credit.
- Motion 2/5: light horizontal slide + spring between steps ("moving forward"); numeric tween on calculator updates. Rates/progress states opaque.
- Components: document upload with receipt confirmation, rate-lock countdown (honest), cross-device resume.
- Red lines: showing only the teaser rate, urgency countdowns to close, no save-and-resume.

### Crypto / Web3 wallets — irreversibility is the design brief
- Psychology: novelty excitement + catastrophically underestimated responsibility; scam exposure (approval phishing, fake support).
- Facts: seed phrase = unencrypted private key, no recovery exists; chain transactions are final.
- Design: **ceremony mode** for seed backup — full-screen, distraction-free, scrambled-word verification, screenshot warning; addresses truncated by default with full-verify tap; signing screens show human-readable intent + contract address.
- Motion 1/5: signing = zero decoration; spring forbidden on any asset-out button.
- Glass: portfolio dashboard background at most; signing modal and seed flow opaque, always.
- Red lines: smooth multi-step funnel for seed backup, confusing "approve token" with "send", rainbow-casino aesthetics.

## Chart grammar for money data（资金图表语法）

- **Composition / asset allocation: prefer the list-as-graph pattern — one row per holding with the ratio embedded in the row (color dot + % + amount + delta) — over stacked bars.** Proven finding (glasspring GP1 run): on dark surfaces a single-hue ramp mathematically cannot give 4 adjacent segments ≥3:1 non-text contrast; rows with textual ratios + color dots satisfy WCAG 1.4.1/1.4.11 with zero contrast debt. If a segmented bar is unavoidable: gaps between segments + a full text legend is the *minimum* mitigation, and the exemption must be written into design-notes.
- P&L deltas: always pair the absolute amount with % and its time window ("今日 +¥684.06 (+0.24%)"); direction = arrow + color, never color alone.
- Trends/sparklines: animate first paint only; refreshes replace in place (the domain-wide rule).
- Every chart number must drill to its source rows (the BI trust rule applies double for money).

## Glass chrome & scroll occlusion（玻璃底栏与滚动遮挡——二样本实证规则）

- **资金产品的悬浮（overlay）玻璃底栏，绝不允许遮挡任何一行金额**——金额被 chrome 瞬时遮住也不行。将其作为硬规则。二选一：
  1. **贴底非悬浮坞**：底栏为布局内的实底（或玻璃）元素，滚动视图 inset 让位，内容永不从栏下穿过；或
  2. 保留悬浮玻璃坞，但**给滚动容器预留底部让位**：`padding-bottom: calc(栏高 + env(safe-area-inset-bottom))`。
- 同规则适用于资金列表上方的 sticky 玻璃头。
- 验证方法：滚动到底后用 `scripts/preview_shot.py` 截图，逐条确认每个金额完整可见（静止截图里被裁掉 = 返工）。

## Domain-wide red lines
Decorative security chrome that implies guarantees (the padlock lesson: Chrome deprecated it); animation on any state transition involving money movement; hiding fees/rates behind interactions; treating risk disclosure as fine print.
