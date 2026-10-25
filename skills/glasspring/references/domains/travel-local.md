# Domain pack — travel & local（OTA/酒店/地图网约车/房产/本地预约/宠物）

> When to read: booking and moving — OTA/hotels/airlines, maps/navigation/ride-hail, real estate, local appointments, pet services.
> Source status: The historical source ledger is not included in this public preview. Treat this card as project design guidance, not independently verified or universally applicable research.

## Surfaces

### 旅行 OTA / 酒店 / 航司
- **Two mutually exclusive IA modes**: inspiration (full-bleed imagery + white overlays, low density) vs comparison (cool-blue data density + filters). Never mix on one screen.
- Progressive disclosure beats full search forms (Hopper: two inputs > Kayak wall); permission requests AFTER the user felt the value; price-calendar heat colors inform, never alarm (Hopper criticized "alarming colors").
- Motion 3/5: date/destination spring transitions; list loads quiet.
- Glass: image price tags, map + listing float cards, booking step overlays; comparison tables never.
- Red lines: fees (cleaning/taxes) revealed late; first-screen permission bombardment; overloaded date pickers.

### 地图 / 导航 / 网约车
- **Map is the canvas, overlays are the UI** — nothing may occlude the forward road; one-glance readability (large type, bottom-anchored controls per Fitts).
- Realtime layer motion 4/5: vehicle interpolation, route draw, state springs — all <400ms (Doherty); menus quiet. Peak-End: arrival moment gets the celebration.
- **Glass: the canonical best-fit** — vehicle card, ETA capsule, bottom action panel float over map without blocking it; the route line itself never takes material.
- Red lines: overlays covering the direction of travel, multi-level taps while moving, blinding white overlays at night.

### 房产平台（Zillow/贝壳/Redfin 型）
- Marathon browsing (hundreds of image decisions) + wish-list-as-filter psychology; map+list dual pane on desktop, polygon draw search.
- Filters: never mutually resetting (tested failure); ~10 sub-categories max per block (Baymard).
- Motion 2/5: gallery inertia, map-list linked panning; decorative springs off.
- Glass: map price pins, detail float cards; listing cards solid.
- Red lines: hidden listing prices, expired/fake listings mixed in, photos materially diverging from reality.

### 本地生活预约（美容/家政/维修）
- Form-like transaction: Eliminate→Automate→Simplify (NN/g EAS; Marriott's manual card-type selection = named anti-pattern); Goal-Gradient step progress (pre-advanced progress bar legitimate).
- Motion 2/5: step transitions light; booking success = the Peak-End moment (one celebration).
- Components: time-slot grid, provider card (rating+distance+slots), cancellation policy shown BEFORE booking, calendar/service-notification subscribe.
- Red lines: fields beyond necessity, policy after payment, pre-checked add-ons.

### 宠物经济
- Family-member emotional register (Aesthetic-Usability amplified); pet profiles drive recommendations (species/weight/age); medical zones switch to clinical trust styling.
- Motion 3/5: photo walls, birthday moments; medical forms quiet.
- Red lines: monetizing illness moments, recommendation ignoring allergy/size constraints.
