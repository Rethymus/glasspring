# Domain pack — e-commerce & retail

> When to read: the product sells things — marketplace, D2C brand site, grocery/delivery, luxury, second-hand C2C, beauty, food delivery.
> Last verified: 2026-10-25. Sources: [Baymard cart-abandonment data](https://baymard.com/lists/cart-abandonment-rate), [Baymard online-grocery research](https://baymard.com/research/online-grocery), [NN/g luxury ecommerce study (2022)](https://www.nngroup.com/articles/luxury-principles-ecommerce-design/), and [Stanford's web-credibility report](https://credibility.stanford.edu/pdf/How_Do_People_Evaluate_a_Web_Site%27s_Credibility_v37.pdf). These studies support only the claims cited below; the remaining rules are project synthesis, not validated universal rules.

## Conversion anchors (why these rules exist)

- Baymard reports a **70.22%** average across 50 published cart-abandonment estimates. Its separate 2026 reasons study reports that 42% of US shoppers abandoned because they were “just browsing / not ready to buy”; among the remaining reasons it lists extra costs **40%**, slow delivery **20%**, card-information distrust **19%**, account creation **18%**, and inability to see total cost up front **12%**.
- Baymard reports an ideal checkout length of **12–14 form elements** and a 23.48-element average US checkout benchmark. These counts include more than just form fields.
- Stanford's web-credibility study reported that **46.1% of comments** addressed a site's design look. This is a share of comments, not a share of participants or credibility judgments.

## Surfaces

### Marketplace / 综合电商（Amazon、淘宝型）
- Psychology: task-driven, comparison anxiety, decision fatigue.
- Design: high density done well — desktop 4–5 column grids, mobile 2 columns; price/rating/shipping/fees scannable in one line; brand color only on primary CTA and selection states.
- Motion 2/5: skeleton screens; one spring pulse on add-to-cart success. Prices and checkout: no bounce.
- Glass: bottom sticky checkout bar and search bar may use Tier 1; **product cards never** (scannability first).
- Components: product card (image+price+list-price+rating+badge), faceted filters (never single-select-reset-others — tested failure), free-shipping progress bar, checkout stepper.
- Red lines: hiding fees to the last step, fake countdowns, filter互斥重置.

### D2C brand site（Allbirds、Gymshark 型）
- Psychology: browsing = planting desire; brand sincerity is the product.
- Design: brand color blocks + generous whitespace; editorial single-column scroll; customer is the hero, founder narrates (Shopify storytelling framework).
- Motion 3/5: hero parallax, scroll narrative, spring transitions between story sections; checkout stays quiet.
- Glass: Tier 1 on image overlays and lookbook layers; never on spec tables.
- Red lines: slow hero loads (luxury sites measurably bleed users), low-contrast gray smallcaps on photos, storytelling without a purchase path.

### Grocery / instant delivery（Instacart、美团闪购型）
- Psychology: restocking under time pressure; "in stock?" and "when?" uncertainty is the enemy.
- Design: freshness green base + status colors (red = out, amber = low); delivery slots and substitutions are first-class UI.
- Motion 2/5: ETA and courier progress interpolate continuously (<400ms response); stock changes get micro-feedback.
- Glass: delivery status capsule and slot picker overlay OK; product grid never.
- Red lines: orderable-but-out-of-stock items without a substitute prompt, vague "ASAP" ETAs.

### Luxury / fashion（Farfetch、SSENSE 型）
- Psychology: price anxiety + ritual; interruptions read as disrespect.
- Design: near black-and-white + one metallic accent; extreme whitespace; typography IS the brand. In-context usage photos drive purchase (NN/g luxury study: a Fendi shopper spent 12 minutes hunting size-reference images across 3 sites).
- Motion: content pages 4/5 (immersive scroll), **purchase flow 2/5** — zero decoration at payment.
- Glass: hero caption bars, showreel players, size-guide overlays; never price/size/checkout panels.
- Red lines: popups mid-scroll, countdown urgency, autoplay music, hidden prices without ranges, light-gray all-caps small text (documented readability failure).

### Second-hand / C2C（闲鱼、Vinted 型）
- Psychology: high vigilance — fear of misrepresentation and disputes.
- Design: trust stack visible (escrow states, seller rating, verification labels); authentic photos beat polish.
- Components: condition-grade card, negotiation chat, escrow state machine (paid→shipped→inspected→released), always-visible report entry.
- Motion 2/5: one spring celebration on escrow release.
- Glass: chat overlays and trade-status badges; no filters over real photos.
- Red lines: steering users off-platform, revealing dispute rules after purchase.

### Beauty（Sephora 型）
- Psychology: high trial cost (wrong shade), ingredient rationality + vibe-seeking.
- Design: clean neutral base; shade pickers and before/after comparisons are the heroes; in-context (on-face) photos convert (NN/g). "Get the basics right before AR" (NN/g on virtual try-on).
- Motion 3/5: try-on interactions <400ms; texture micro-animations; quiet checkout.
- Glass: shade floating panels, try-on viewfinder frames, ingredient cards — glass fits this domain unusually well; never over real skin-result photos.
- Red lines: AR over-smoothing that falsifies shades, marketing copy replacing ingredient facts.

### Food delivery（Uber Eats、DoorDash、美团外卖型）
- Psychology: hunger = zero patience; repeat orders are the business.
- Data: Baymard delivery benchmark 2026 (8 apps): none reached "decent" — top gaps: no reorder entry on home, missing dietary/customization filters, weak pickup-time/tipping info.
- Design: appetite palette only on CTA (food photography stays natural); category sticky nav; single-column big-image menus.
- Motion 3/5: live map interpolation; **delivery arrival is the Peak-End moment — put the one celebratory animation there.**
- Glass: courier card on map, "order in progress" capsule, dish half-sheet — glass showcase domain.
- Red lines: upsell inserted under countdown pressure, fake scarcity, menus without allergen/dietary filters.

## Domain-wide red lines
Fake urgency/countdowns; hidden costs until the last step; dark patterns in cancellation; product cards with any translucency; animating price changes.
