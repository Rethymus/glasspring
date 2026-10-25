# Domain pack — social & community（社交网络/即时通讯/论坛/约会/创作者）

> When to read: the product's core loop is people reacting to people — social feeds, messaging, communities/forums, dating, creator monetization.
> Source status: The historical source ledger is not included in this public preview. Treat this card as project design guidance, not independently verified or universally applicable research.

## Cross-domain rules

- Social feeds = infinite scroll's legitimate home (NN/g), but: preserve "way back" landmarks, keep footer reachable, never endless without a loading state.
- Preset image aspect ratios (1:1 / 4:5 / 16:9) — CLS from unpictured media is a defect.
- Spring = "someone is responding to you" (likes, follows, match moments). Feed scrolling itself: no decoration.

## Surfaces

### 社交网络（Instagram/微博/X 型）
- Story ring (unread gradient) is the consumable marker; publish→instant-feedback loop must never break (post confirmation animation).
- Motion 3/5: spring bursts on like/follow, pull-to-refresh elasticity.
- Glass: top nav/composer/input bar; image cards never.
- Red lines: no feedback after posting; aspect-ratio jank.

### 即时通讯（WhatsApp/微信/Telegram 型）
- Bubbles carry tone: mine = brand-solid, theirs = neutral; typing indicator (three dots breathing), read receipts, reaction bubbles, quote blocks, unread divider.
- Motion 2/5 — high-frequency surface, fatigue is fast: bubble entrance micro-spring, send-fail shake only.
- Glass: input bar/top panel/sticker tray; **bubbles never** (maximum legibility).
- Red lines: unbounded bubble width; search weaker than send; default-on read receipts with no off switch (social-pressure design).

### 兴趣社区/论坛（Reddit/Discord/豆瓣 型）
- Culture is load-bearing: pseudonymity, vote-visible ranking, volunteer moderation, nested threads (indent 16px/level, flatten after ~10), spoiler/NSFW blur patterns. Users "notoriously resist overt corporate marketing" — brand accent only on voting/tags.
- Night mode = off-black `#1A1A1B`, never pure black (long-read comfort).
- Motion 2/5; tool-feel over delight.
- Glass: floating compose button/side cards; nested comment areas never (translucency destroys indent legibility).
- Red lines: forced real names, staff posts disguised as users, visible commercial tampering with ranking.

### 约会交友（Tinder/Hinge 型）
- Safety is the first gate for the most vulnerable side: double opt-in, photo verification badge, report/unmatch ≤2 clicks from any match, panic features; never expose who rejected whom.
- Motion 3.5/5: swipe cards track the finger (JS spring — gesture velocity inheritance), release flies out/springs back; the match moment is the peak (big spring + double-photo overlay).
- Glass: card info gradient layer, match modal; photos never.
- Red lines: paywalled safety, discriminatory pricing (Tinder age-pricing: $60.5M settlement), deep-buried reporting.

### 创作者经济（Patreon/爱发电 型）
- Tiers are identity: 3-card price laddering, "most popular" center anchor, locked-content blur previews, progress funding goals, member badges.
- Motion 2.5/5: becoming-a-patron is the peak moment (one spring + badge unlock).
- **Pricing transparency is the survival line** (Patreon 2017 fee-structure reversal exodus).
- Red lines: mid-subscription fee changes, cancellation mazes, misleading perk promises.
