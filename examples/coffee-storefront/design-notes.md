# Coffee storefront design notes

> Manual Glasspring-guided example, checked 2026-10-26 with skill version 2.1. This records the current public example packaging and checks; it does not claim a live Agent host run or benchmark result.

## §0 · Route and defaults

- Reading this as: a fictional D2C coffee storefront for people choosing a small-batch roast; warm, editorial brand language; desktop and mobile web preview.
- Route: marketing / brand page; e-commerce retail, D2C; plain web; static HTML, CSS, and vanilla JavaScript. No product type pack or platform adapter was needed.
- Core references counted toward the routing budget: `tokens.md` and `domains/ecommerce-retail.md`. No product-type pack or platform adapter was needed. Task-triggered guides: `type.md` for text styling and `motion.md` before adding the page's transitions and smooth scrolling. `glass.md` was not read because no translucent surface is used. The page follows the README task brief; its generated imagery was already present in the project when this packaging pass began.
- Deliverables: `tokens.css`, `preview.html`, `design-notes.md`, and local example assets. The one-page preview keeps its component CSS in `preview.html`, as the contract checker scans that entry file for token use.
- Scope: manually align and review the existing fictional example against the Skill contract. The visuals and local bag behavior were retained; these notes do not represent an invocation by an installed Codex or Claude host.

## §1 · Direction choice

- Considered in this packaging pass: **Roastery letter** (long-form origin story before product choice); **Market menu** (compact product-first list with comparison details); **Morning ritual** (split still-life hero, three roast cards, and a short sourcing note).
- Selected **Morning ritual** because the brief asks for a hero, three products, and a clear local bag action. The main differentiator is the split hero: a short editorial statement beside a coffee still life.
- First intuition was a generic warm café template. The brief explicitly names cream, espresso, and terracotta, so those colors stay; stamp badges and extra ornamental labels were left out.
- The directions share the required palette but vary in information order and layout. This selection records the current page choice; it is not a claim about the earlier image-generation session.

## §2 · E-commerce cues

- D2C brand page: generous whitespace and a short story section are used in the hero and “A more thoughtful roast” section.
- Visible purchase path: the hero links to coffee; all three product cards show a name, tasting note, price, and add action.
- Trust and price handling: prices are visible beside products; the bag and subtotal use an opaque surface; no countdown, hidden fee, checkout, or payment claim is present.
- Asset fit: locally generated, unbranded coffee imagery supports the fictional product and stays separate from real product claims.
- Self-check: 4 domain cues applied. These are design choices, not measured conversion outcomes.

## §3 · Glass and materials

- No glass or translucent component is used. There is no `backdrop-filter` or glass-on-glass surface.
- The shopping bag dialog is opaque. Product prices and subtotal stay on the opaque page/dialog surface, consistent with the money trust-zone rule.
- A translucent treatment and its fallback were not needed for this page.

## §4 · Contrast measurements

Measured with `skills/glasspring/scripts/check_contrast.py` using the listed foreground and background pairs. Each pair passed WCAG AA for the tested text or focus use; selected pairs also passed AAA. This is a selected-pair check, not complete WCAG conformance.

| Pair | Foreground | Background | Ratio | Result |
|---|---|---|---:|---|
| Body text / page | `#35221b` | `#f8f3eb` | 13.62:1 | PASS AA and AAA |
| Secondary text / page | `#65544a` | `#f8f3eb` | 6.51:1 | PASS AA |
| Button text / accent | `#fffaf3` | `#93432d` | 6.56:1 | PASS AA |
| Button text / hover | `#fffaf3` | `#71331f` | 9.21:1 | PASS AA and AAA |
| Focus ring / page | `#93432d` | `#f8f3eb` | 6.17:1 | PASS AA |
| Status text / page | `#71331f` | `#f8f3eb` | 8.66:1 | PASS AA and AAA |
| Skip-link text / dark surface | `#fffaf3` | `#35221b` | 14.48:1 | PASS AA and AAA |

`--color-on-accent` aliases the surface token; its real use was measured as button text against the accent fill. The shadow token is not a text/background pair and was not contrast-tested.

## §5 · Motion

- Motion budget: 1/5. The button has a 160ms hover transition and a 1px pressed-state shift; anchor scrolling is smooth. Bag quantity and subtotal update in place without animation.
- The dialog uses native `<dialog>` behavior. `prefers-reduced-motion: reduce` disables smooth scrolling and shortens transitions.
- No spring was needed or generated.

## §6 · Slop scan and visual review

- First `slop_scan.py examples/coffee-storefront`: exit 1, **1 hard / 1 warn**. The footer used middle-dot-separated metadata and the page title used an em-dash label.
- Minimal fix: turn the footer into three sentences and replace the title em dash with a colon. No scan rule or threshold changed.
- Final `slop_scan.py examples/coffee-storefront`: exit 0, **0 hard / 0 warn / 0 info**. No exemptions were needed; the cream, serif, and terracotta combination is explicitly required by the task brief.
- First `verify_output.py examples/coffee-storefront` after extracting CSS: exit 1, token-consumption **UNKNOWN** with three HTML token references; the helper checks `preview.html` and does not inspect an external stylesheet. Minimal packaging fix: keep the page-specific CSS inside `preview.html` and link the one source-of-truth `tokens.css`. Final result: exit 0, **0 FAIL / 0 UNKNOWN / 6 PASS**. The checker and its thresholds were not changed.
- Screenshot review intent: check the hero-to-product hierarchy, product price/action visibility, asset loading, mobile stacking, and horizontal overflow. The 1440px and 390px captures show the hero, all three products, story section, and footer; the mobile capture has no horizontal overflow.
- A separate visual critic was not available. A passing mechanical scan does not establish taste or task efficacy.

## §7 · Limits and remaining evidence

- **adds-friction — bounded viewport evidence:** checked at 390px and 1440px in Chrome only. Widths below 360px, 200% zoom, other browsers, and assistive-technology combinations were not tested.
- **blocks-conversion — demo scope:** bag state is in memory only; there is no inventory, persistence, checkout, order submission, or payment.
- **minor-polish — illustrative assets:** product names, prices, copy, and locally generated images are fictional, not evidence about a real coffee brand or retail outcome.
- Browser plugin was not available in this session. Visual and interaction checks used Python Playwright 1.53.0 with Chrome 155.0.8059.85. The local interaction smoke had no console warnings/errors or page exceptions.
- `probe_render.py --no-axe` returned **UNKNOWN**, Python process exit 2: coverage was partial because axe was disabled and click observation was unavailable. The separately run Playwright flow covers the listed bag actions; automated axe coverage is NOT_RUN here. No claim of full WCAG conformance is made.
- Host discovery and independent efficacy are NOT_RUN for this example. This work does not clear the repository's release blockers; see [`docs/RELEASE-GATES.md`](../../docs/RELEASE-GATES.md).

### Recorded checks (2026-10-26)

| Command or action | Result |
|---|---|
| `python -m unittest discover -s tests -v` | PASS, 24 tests, exit 0 |
| `node skills/glasspring/scripts/install.mjs --selftest` | PASS, exit 0 |
| `python skills/glasspring/scripts/verify_output.py --selftest` | PASS, exit 0 |
| `python skills/glasspring/scripts/mcp_server.py --selftest` | PASS, exit 0 |
| `python skills/glasspring/scripts/doctor.py --target examples/coffee-storefront` | PASS, exit 0; its offline `preview_shot` subcheck reports SKIP because live mode was not requested |
| `python skills/glasspring/scripts/verify_output.py examples/coffee-storefront` | PASS, 6 clauses, 0 FAIL / 0 UNKNOWN, exit 0 |
| `python skills/glasspring/scripts/slop_scan.py examples/coffee-storefront` | PASS, 0 findings, exit 0 |
| `python skills/glasspring/scripts/preview_shot.py <local URL> --out-dir <temp> --widths 390,1440 --expect-title "Morrow Coffee"` | PASS, exit 0; 390×844 and 1440×900 captures; temporary output directory |
| Playwright Python 1.53.0 with Chrome 155.0.8059.85 | PASS, exit 0; page and images loaded; 200 responses; no browser errors or overflow; add, subtotal, keyboard, Escape, remove, and empty states verified |
| `notes_draft.py` with the seven explicit pairs above | PASS, 7 pairs / 0 FAIL, 0 slop findings, 4 anchors, exit 0 |
| `python skills/glasspring/scripts/probe_render.py <local URL> --no-axe` | UNKNOWN, partial coverage, Python process exit 2; axe disabled and click observation unavailable |

## §8 · Reference anchors

- `skills/glasspring/SKILL.md` — version 2.1, read 2026-10-26.
- `references/tokens.md` — Last verified 2026-10-25.
- `references/type.md` — Last verified 2026-10-25.
- `references/domains/ecommerce-retail.md` — Last verified 2026-10-25.
- `references/motion.md` — Last verified 2026-10-25.
- No external performance or conversion statistic is used in these design notes.
