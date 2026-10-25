# Domain pack — entertainment & games（活动票务/游戏 UI/体育竞猜）

> When to read: tickets/live events, game HUDs & menus, sports scores & (compliance-sensitive) betting.
> Source status: The historical source ledger is not included in this public preview. Treat this card as project design guidance, not independently verified or universally applicable research.

## 1. 活动/票务（Eventbrite/大麦/Ticketmaster 型）

- Psychology: peak arousal (queue anxiety) + Peak-End rule — **the confirmation page is the memory; craft it**.
- Grammar: interactive seat map (pan/zoom + zoned price legend), real-time inventory, 10-min cart countdown (honest: expiry must release), queue room with progress breathing, anti-bot verification, transfer/resale restrictions on the ticket.
- Motion 3/5: seat-select spring, countdown roll, confirmation celebration; seat-map zoom = smooth easing (precision, not spring).
- Glass: sticky bottom checkout bar; seat map & countdown never.
- Platform: mobile = countdown + one-page checkout; desktop = seat maps; ticket QR must work offline + adapt to brightness.
- Red lines: countdowns that don't release seats, junk fees revealed at the last step (UK CMA investigated dynamic pricing disclosure), queue pages without status (refresh avalanches).

## 2. 游戏 UI（按类型；HUD 语法与玻璃适用边界）

- **Glass HUD fit by genre** — fits: competitive shooters/MOBA *menus*, rosters, post-match screens ("Flat 2.0" glass layering); sim/management full panels; RPG dialogue/inventory. **Fails**: horror (glass highlights fight fog — go diegetic), hardcore competitive HUD center (translucency slows combat reads), children's games (cognitive load), burn-in risk on long-lived static HUDs.
- Genre palettes: team colors (blue/orange), rarity ladders (white→green→blue→purple→gold), low-sat single-hue for horror; enemies and allies never share a hue family.
- Numbers: tabular, mono-scaled; HUD = four corners (health/ammo/ability/minimap); damage numbers spring, ability CD sweep; **in-game persistent HUD has no idle animation** (60fps budget ≈ 16.6ms/frame — UI motion must not tax render).
- Gamepad: XY-focus navigation, focus ring unmistakable, ≤6 clicks to cross, ≥32epx targets, TV safe areas 27/48epx, TV-safe colors 16–235; nested interactive grids are the classic d-pad trap.
- Red lines: translucency on combat-critical info, cheerful flat-UI in horror, monetization dark patterns in kids' games.

## 3. 体育/竞猜（ESPN/Fantasy/DraftKings 型）

- Densest lawful surface: sticky score ticker + play-by-play stream + win-probability curves; tabular-nums, column-aligned; second-screen (TV + phone) is the primary posture.
- Motion 2.5/5: score-change flash (one pulse); celebration only for *your* team, restrained.
- **合规语法（不可协商）**: deposit limits, periodic reality-checks, self-exclusion, activity statements — visible, never buried; settlement/odds UI must never render losing states as celebrations; near-miss visual glorification is a documented dark pattern.
- Glass: score ticker/bottom tabs; odds lists & data tables solid.
- Red lines: color-only win/loss (add arrows — colorblind), gradient/low-contrast score strips (must read at 3m), minor-reachable betting aesthetics.
