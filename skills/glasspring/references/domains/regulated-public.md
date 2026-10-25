# Domain pack — regulated & public（政务/非营利信仰/法律已单列；此处含政务公民服务与公共部门）

> When to read: government/civic services, public-sector forms and portals — the trust-through-consistency domain (法律/会计 see industrial-b2b.md §法律会计；非营利/宗教 content merged into this file)。
> Source status: The historical source ledger is not included in this public preview. Treat this card as project design guidance, not independently verified or universally applicable research.

## 政务/公民服务（gov.uk 为全球标杆）

- **Plainness is the feature**: consistency = trust; task completion = justice. GDS principles ("Start with user needs", "Do the hard work to make it simple"); black-on-white + single functional blue + focus yellow; no brand gradients, no marketing imagery.
- Statutory accessibility: WCAG 2.2 AA + accessibility statement legally required (public-sector bodies); error summary pattern top-of-page with field anchors; one-question-per-page with Continue (never "Next"); "I do not know" is a valid answer.
- Motion 0/5: focus states and loading are the only motion; Exit-this-page instant overlay is a sanctioned crisis exception.
- Glass: **principled mismatch** — focus visibility and predictability outrank material polish; do not import.
- Components: task-list service page (step + status), question pages, error summary, contact-channel choice, service status page (transparency = trust).
- Form a11y: skip-nav link mandatory（政务表单导航层级深）; focus order = reading order; error summary top-of-page + per-field anchor（已有）+ `aria-describedby`; label in name（可见标签=accessible name）。WCAG 2.2 AA 法定要求，government services 不可豁免。
- Red lines: marketing content, urgency A/B tests, breaking the browser back button (gov.uk explicitly forbids), progress bars where question order wasn't optimized first (their research: progress indicators optional).
