<div align="center">

# 🎨 glasspring

**A measurement-first design gate for AI coding agents — every color pair contrast-tested, 31 anti-slop rules scanned, six render probes, zero hits before anything ships**

*Give your coding agent a pair of "design eyes."*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](LICENSE)
[![Dependencies](https://img.shields.io/badge/Dependencies-0_stdlib_only-2ea44f.svg?style=flat-square)](#-security)
[![Validated](https://img.shields.io/badge/Validated-34_runs-blueviolet.svg?style=flat-square)](#-validation-evidence)
[![For](https://img.shields.io/badge/For-AI_Coding_Agents-8957e5.svg?style=flat-square)](#-install--quickstart)

**English** | [简体中文](README.zh-CN.md)

*Why does every AI-built page wear the same face — a capability limit, or untaught taste?*

**The 30-second path**: [Install](#-install--quickstart) → [Before / after](#-see-it-in-five-seconds) → [What it can do](#-what-it-can-do) → [Validation evidence](#-validation-evidence)

</div>

> [!IMPORTANT]
> **glasspring is a design knowledge layer, not a design answer.** It gives any AI coding agent that can read `.agents/skills/` four things: routing, derivation, measurement, and gating. It is **not a UI component library**, it does not replace human designers, and it does not promise the output "looks good." What it promises is **verifiability**: every color pair actually contrast-tested (WCAG + APCA second opinion), zero hits across 31 anti-slop rules, and all six render probes passing. The gates are a necessary condition, not a sufficient one.

> [!NOTE]
> This is the English README; [README.zh-CN.md](README.zh-CN.md) is the Chinese original. The two are kept semantically equivalent. The skill's reference files and tool output are Chinese-first. If the two versions ever drift, **the Chinese version is the source of truth**.

---

## Contents

1. [Why you need it](#-why-you-need-it)
2. [See it in five seconds](#-see-it-in-five-seconds)
3. [Install & quickstart](#-install--quickstart)
4. [What it can do](#-what-it-can-do)
5. [Built-in tools](#-built-in-tools)
6. [How it works](#-how-it-works)
7. [Design philosophy](#-design-philosophy)
8. [Managing it after install](#-managing-it-after-install)
9. [What it does not do](#-what-it-does-not-do)
10. [Validation evidence](#-validation-evidence)
11. [Security](#-security)
12. [Why it earns a star](#-why-it-earns-a-star)
13. [FAQ](#-faq)
14. [Contributing](#-contributing)
15. [License](#-license)

---

## 🤷 Why you need it

AI coding agents can already write front-end code that runs — but ask one for "a nice-looking page" and you always get the same face back:

- 🎨 "Make me a landing page" → **cream background + terracotta + purple-gradient hero**, identical to the last AI-built page you saw
- 🌓 "Add dark mode" → **naive inversion**: pure white text slapped on pure black, three minutes of eye pain
- 📊 "Build a dashboard" → proportional digits misaligning table columns, the whole page jumping on data refresh
- 💰 "The payment page too" → **translucent amounts**, users leave because they can't read what they're about to pay
- 📱 "Also the mini program" → web glass recipe copied over, **renders blank in the WeChat webview**
- ♿ "Mind accessibility" → cites WCAG clauses, but **not a single color pair was ever actually tested**
- 🈶 "Polish the Chinese typography" → line-height 1.5 crammed together, no CJK/Latin spacing
- ✨ "Add some micro-interactions" → **scroll fade-up on every card**, springs bouncing everywhere

None of this is a capability problem — **nobody ever taught the agent what "right" is**. It doesn't know 0.72 is the readability floor for a glass tint, that dark mode isn't inversion, that destructive buttons never use the primary color.

**glasspring turns this into one sentence.** Paste the line below to your agent — it works from any project, because the agent fetches the install guide itself; no local paths, no prior clone:

```
Install glasspring: https://raw.githubusercontent.com/Rethymus/glasspring/main/INSTALL.md
```

Once installed, you say "make a landing page" and the agent runs the four-question routing, derives tokens, contrast-tests colors, and verifies screenshots on its own — you never have to shout "watch the quality."

### ✅ Before you use it, you may want to know

| | |
|---|---|
| 📏 **Measured, not claimed** | Every color pair runs a WCAG contrast check (glass measured at worst-case compositing) plus an APCA Lc second opinion; every number has a source ledger |
| 🚫 **Anti-slop built in** | 31 detection rules: cream + terracotta, purple gradients, midpoint metadata, uniform radii + same shadow, AI buzzword filler, organic blobs…… zero hard hits before delivery |
| 🔬 **Six render probes** | `probe_render.py`: animation gating / t=0 freeze / reduced-motion contract / axe accessibility / **click fingerprints** (dead contracts & hidden states) / **economy signals** (uniform spacing / one-sided emphasis) — what static scans can't see, rendering sees |
| 🧪 **34 validated runs** | 14 domain packs + 12 style packs (5 packs promoted via GP end-to-end) + shadcn bridge + real mini-program dogfooding + cold-start isolation tests |
| 🆚 **Controlled experiments** | With/without-skill, four paired runs: **+6/+5/+6/+4** (the baseline is no straw man) |
| 🤖 **Works with every agent** | Any coding agent that reads `.agents/skills/` — Claude Code, ZCode, Codex CLI…… install once, use across the project |
| 🩺 **Self-diagnosing** | `doctor.py`, one command: all script self-tests + slop scan + output contract check |
| ⚖️ **Legal red lines built in** | No SF fonts bundled, no hand-drawn SF Symbols, no "Liquid Glass" branding — the borrowing ladder is written into the constitution |

---

## ⚡ See it in five seconds

Same brief, built twice. [examples/before.html](examples/before.html) is the **deliberate** AI-default take — purple-gradient hero, three identical cards, emoji icons, unmeasured low-contrast grays (the scanner finds 10 warns + 1 info). [examples/after.html](examples/after.html) is the same brief through the full pipeline — contrast 11/11 measured-pass, scan 0 hits, dual-viewport visual check. Open both in a browser and judge for yourself:

| Default AI take | glasspring take |
|---|---|
| ![before](docs-img/shot-pulse-before-desktop-1440x900.png) | ![after](docs-img/shot-pulse-after-desktop-1440x900.png) |

---

## 📦 Install & quickstart

Paste this line to your AI agent (Claude Code, ZCode, Codex, etc.):

```
Install glasspring: https://raw.githubusercontent.com/Rethymus/glasspring/main/INSTALL.md
```

中文触发语：`帮我安装 glasspring：https://raw.githubusercontent.com/Rethymus/glasspring/main/INSTALL.md`

That's the whole step. The URL points at the install guide; the agent fetches it and does the rest — **you never need to clone this repo first, and you never need to know a single path**.

**Only three prerequisites:**

- An AI coding agent that can read a skills directory (Claude Code, ZCode, Codex CLI……)
- Permission for the agent to run commands (copy files, run the installer and self-tests)
- Python 3 (pure stdlib, zero pip dependencies); Node only for the installer

**Upgrading is the same sentence** — send it again; the installer replaces the old directory via `--replace` and keeps an automatic backup.

<details>
<summary>What will it do? (click to expand)</summary>

1. **Fetch the install guide** — reads INSTALL.md at the URL above (installer usage + per-host directory conventions)
2. **Confirm the install location** — asks which project and which host: Claude Code installs to `.claude/skills/`, Codex / generic Agent Skills to `.agents/skills/`; user-level global install is also possible
3. **Run the installer** — `install.mjs` copies the skill directory wholesale (SKILL.md, 14 domain packs, 12 style packs, mature-stack guidance, shadcn bridge, 15 self-tested tools), verifying copied bytes for integrity; `--dry-run` previews first
4. **Run self-tests** — once `doctor.py` is all green, it tells you how to use it: just say "make me a landing page"

After install, `doctor.py --target <dir>` re-checks every tool in one command; to verify the experience item by item, walk through [USER-CHECKLIST.md](USER-CHECKLIST.md).
</details>

<details>
<summary>Agent already inside a cloned copy of this repo? (local fallback)</summary>

If your agent is already working inside a clone of this repository, you can also say:

```
帮我安装 glasspring：读取当前仓库根目录的 INSTALL.md 并按步骤完成安装
```

Both are equivalent; the URL version never depends on local paths and works everywhere.
</details>

### Manual install (no agent involved)

```bash
git clone https://github.com/Rethymus/glasspring
node glasspring/skills/glasspring/scripts/install.mjs --target /path/to/your/project --host claude
```

`--host` accepts `claude` (installs to `.claude/skills/`) or `codex` (installs to `.agents/skills/`); omit it for a generic install. `--dry-run` previews; `--replace` upgrades in place with an automatic backup.

---

## 🎯 What it can do

**14 domain packs**, each a validated DNA card — not a style description, an executable engineering constraint:

| Domain pack | Highlight rules | GP validated |
|------|---------|--------|
| 🛒 E-commerce / retail | Opaque price-trust zone / Baymard cost-up-front / restrained promos | ✅ 14/14 |
| 💰 Fintech / payments | Tabular-nums amounts / red only for overdue / crisis-safe entry | ✅ 14/14 |
| 💻 Developer tools | Mono data / glass never over code / copy button per block | ✅ 14/14 |
| 📚 Education | COPPA strict-regulation / kid touch targets ≥56px / motion 1-of-5 | ✅ 14/14 |
| 📺 Media / content | Dark playback surface by default / body text never translucent / F-pattern | ✅ 14/14 |
| 👥 Social / community | No forced real-name / visible vote sorting / rankings never for sale | ✅ 14/14 |
| 🎮 Games / entertainment | 60fps budget / four-corner HUD / five rarity tiers | ✅ 14/14 |
| ✈️ Travel / local | ETA with confidence interval / fees disclosed no later / Peak-End | ✅ 14/14 |
| 🏥 Health / fitness | Never celebrate "normal" / persistent crisis entry / pharma ISI | ✅ 14/14 |
| 🏛️ Government / public | Glass categorically mismatched / motion 0-of-5 / statutory accessibility | ✅ 14/14 |
| 🏭 Industrial B2B | Drawing-revision red line / zero hover dependence / readable at 3 m | ✅ 14/14 |
| 🔬 Academic / research | Charts are content / clickable DOIs / citations non-negotiable | ✅ 14/14 |
| 🏢 Enterprise / demo | Real photography / sticky scroll-telling / no fabrication | ✅ 14/14 |
| 📋 Productivity B2B | Visible WIP / multiple views, one data source / HR dignity constraints | ✅ 14/14 |

**12 style packs** (switch by naming one; ★ = promoted via GP end-to-end):

| Style pack | In one line | Fits |
|---|---|---|
| ★ Linear instrument | Keyboard-first, mono data, zero glass | devtools / dark B2B |
| Notion paper | Gray-scale hierarchy, block-editing syntax | docs / knowledge bases |
| Swiss International | Asymmetric grid, red as punctuation | portfolios / editorial |
| Brutalism | 2-3px black borders, zero radius zero shadow | indie zines / event pages |
| Magazine editorial | Serif body, hairline rhythm | long-form content |
| Dark academia | Parchment + oxblood, double-rule dividers | vintage academic |
| Organic natural | Terracotta / botanical, leaf-shaped corners | handmade / lifestyle |
| ★ Warm soft SaaS | chunky tactile buttons, 2px+ borders | habit-forming / onboarding |
| ★ Dark cinematic | void layering, ≤3 signal colors, one glow | AI / infra marketing |
| ★ Quiet luxury | film grain, serif contrast, sage two-track | law firms / boutique hotels |
| ★ Soft structural | giant grotesk, diffuse shadows | design tools / architecture studios |
| ★ Ethereal glass | OLED deep space, fake-glass trio | AI data platforms |

See the twelve-pack, same-content comparison gallery at [assets/style-gallery.html](skills/glasspring/assets/style-gallery.html) (opens in any browser). Every style pack's glass verdict, radius discipline, and motion budget are audited for cross-pack consistency. There is also a **shadcn/ui bridge** (Base UI primitives layer, default since 2026-07) and a **mature-library-first stack** (shadcn + Lucide + Motion + dnd-kit + Zustand…… 11 libraries each with a domain rule + triple dependency-dedup check — rolling your own when an existing dependency suffices is forbidden).

---

## 🔧 Built-in tools

| Tool | In one line | Highlights |
|---|---|---|
| 🩺 `doctor.py` | One-command health check: all script self-tests + slop scan + output contract | Single entry point |
| 📊 `check_contrast.py` | WCAG contrast + APCA Lc second opinion | `--pairs` batching / `--tone-for` closed-form solve |
| 🌈 `palette_from_oklch.py` | Brand color → OKLCH scale re-derivation | `--scaffold` emits a starter file from a DNA card |
| 📸 `preview_shot.py` | True 390px-viewport screenshots + interaction evidence | `--click` / `--probe` / `--scroll-to` / `--label` |
| 🚫 `slop_scan.py` | 31 anti-slop rules, programmatic scan | Dual-anchor self-test against dead rules |
| 🌗 `token_emit.py` | DTCG tokens → CSS/Swift/Kotlin/wxss | `--wxss` auto rpx conversion for mini programs |
| ✅ `verify_output.py` | Mechanical contract check + `--html` acceptance report | PASS/FAIL/UNKNOWN tri-state |
| 🔧 `spring_convert.py` | SwiftUI springs ↔ CSS `linear()` conversion | Anchored to Apple's official parameter values |
| 🔬 `probe_render.py` | Six render probes (A-F + empty-render guard) | Click fingerprints for dead contracts / axe a11y / reduced-motion contract / economy signals |
| 🎴 `deal_direction.py` | Direction dealer (9+2 pick-1 commitment) | `--prompt` derives a reproducible seed |
| 🚀 `run_init.py` | One-command scaffold: skeleton + token placeholders + notes template | Skeleton intentionally not green (honest starting point) |
| 📝 `notes_draft.py` | Design-notes first draft: measured §4 + first scan §6 + anchors §8 auto-filled | Judgment slots left open; final draft still requires them |
| 🔍 `visual_diff.py` | Pixel-level screenshot diff (pure-stdlib PNG decode) | Fix needs `--min-diff` > 0 (no diff = no fix) / drift `--max-diff` |
| 🔌 `mcp_server.py` | Gates as MCP: 10 tools registered into Claude Desktop/ZCode/Cursor | stdio JSON-RPC, structured JSON returns, no shell quoting |
| 📸 `samples_gate.py` | Full-sample regression in one command (13+5 entries, dual widths) | Exemption-aware / network-dependent steps honestly SKIP |
| 🖥️ `install.mjs` | Installer + file-map integrity check | Excludes __pycache__ |

---

## 📐 How it works

```
You say: "build a landing page for a coffee e-commerce brand"
        │
        ▼
Four-question routing: what type? what domain? what platform? what stack?
(reads ≤3 reference files — context economics; long context degrades adherence)
        │
        ▼
Tokens first: re-derive an OKLCH scale from your brand color (no copied values)
        │
        ▼
Build to recipe: graded glass recipes / spring semantic presets / CJK type rules / domain red lines
        │
        ▼
Verify by measurement: contrast batching + anti-slop scan + six render probes
(with click fingerprints) + true-viewport screenshots + output contract
        │
        ▼
Deliver: tokens.css + preview.html + design-notes.md + screenshots
```

After reading SKILL.md, the agent knows which tools to call and which references to read. **No commands to memorize.**

---

## 🧠 Design philosophy

**glasspring is a design knowledge layer, not yet another UI template.**

It sits one level above any concrete implementation — responsible for **routing, derivation, verification, refusal** — not for the underlying design itself. Design is done by the agent following the reference rules; there is no wrapper layer.

Every time you set up a fresh agent environment, you spend time teaching it what "right" is — how to measure contrast? when to use glass? what color for destructive buttons? The same lesson, over and over. glasspring does one simple thing: **the most reliable design rules of the moment, validated, anchored, and written into references by us. When rules age, we update them — you don't think about it.**

### Reference file layout

```
references/
├── tokens.md          → token system (OKLCH scales / dark re-derivation ladder)
├── type.md            → typography (scale / CJK rules / RTL / microcopy / image discipline)
├── layout-baselines.md → quantified landing-page baselines (composition/color/type/motion/imagery — measured from 99 SOTD)
├── motion.md          → spring physics (semantic presets / interruptible / gesture coaxial)
├── glass.md           → glass recipes (three-tier fallback / decision tree / HIG-anchored)
├── domains/           → 14 domain packs (glass verdicts / motion budgets / red lines each)
├── recommended-stack.md → mature-library-first stack (11 library domain rules + dedup triple-check + route criteria)
├── style-packs/       → 12 style DNA cards (re-derived values / rules / measured contrast)
├── platforms/         → platform adaptation (shadcn bridge / TV / desktop / mobile)
└── types/             → product types (admin syntax / native idioms / game HUDs)
```

---

## 💬 Managing it after install

Just talk to the agent in plain language — no commands to remember. *Natural-language triggers currently work best in Chinese; the exact phrases below are what the skill expects:*

| You say (中文) | The agent will |
|---|---|
| "帮我做个落地页 / 后台 / 小程序页面" | Trigger glasspring: route → derive → build → gate → deliver |
| "检查一下这个页面的设计质量" | Scanner + six render probes + contrast batching, with a report |
| "用 Linear 的风格做" | Read the linear-instrument style pack, replace the base tone |
| "glasspring 更新了吗？" | Re-run `doctor.py --selftest`; all green means in place |
| "新起一个页面工程" | `run_init.py <dir>` scaffolds the skeleton in one command (tokens/notes/screenshot dirs + next steps) |
| "卸载 glasspring" | List the directories to delete (.agents/skills/glasspring/ + gp-* samples per project), delete after confirmation, touch nothing else |

---

## 🚫 What it does not do

> [!WARNING]
> **What glasspring will never do:**
> - **Generate design answers** — it measures and gates; the design itself still comes from your brief and the model
> - **Certify "good looks"** — passing every gate only means the verifiable floor was met, not that the page wins awards (see the [FAQ](#-faq))
> - **Phone home** — every script is stdlib-only and runs locally; screenshots and reports never leave your machine
> - **Ship Apple's proprietary assets** — no SF fonts, no SF Symbols, no "Liquid Glass" branding, none of it, ever

---

## 📊 Validation evidence

| Evidence | Where |
|---|---|
| 34-run validation index (per-run RUBRIC + known limits; runs 1-30 indexed, run31-34 are dogfood/isolation/stress/multi-page extensions) | `evals/RESULTS-INDEX.md` |
| With/without-skill controlled experiments (+6/+5/+6/+4) | `evals/results/run6-9/` |
| Real mini-program dogfood (v2 vs v3, quantified) | `evals/results/run30/` |
| Cold-start isolation test (installed copy runs standalone) | `evals/results/run31/` |
| Security-product dogfood (audit-archive syntax) | `evals/results/run32/` |
| Cross-pack conflict stress test (FM-6 verified in the field) | `evals/results/run33/` |
| Full stability matrix (30/30 zero drift) | `evals/results/n6-audit.md` |
| External corroboration: StyleSeed's BENCH-V1 measured bare-rule inconsistency (Codex +1.6 / Claude Code −3.7); only forced render→score→revise gating reached +5.3 — same conclusion as glasspring's "measure, don't lecture" architecture | [bitjaru/styleseed](https://github.com/bitjaru/styleseed) |
| 12-pack style gallery (same content, opens in a browser) | [assets/style-gallery.html](skills/glasspring/assets/style-gallery.html) |
| Multi-page site, three laws measured (MASTER layering / variance / token consistency) | `examples/gp-multipage-site/` |
| Agent-friendly doc index (a repo map for agents) | `llms.txt` |
| Full source ledger | `docs/SOURCES.md` |

> Note: evidence paths shown as code spans live in the development archive and are not part of the published snapshot yet.


### Project status

| | |
|---|---|
| Validation | 34 RUBRIC-measured runs; full stability matrix 30/30 zero drift |
| Tools | 16, of which 15 ship with `--selftest` |
| Runtime | Python stdlib (zero deps) + Node (installer only) |
| Doc language | Chinese-first; this English translation available |
| License | MIT |

---

## 🔒 Security

glasspring is designed with security in mind:

| Measure | Detail |
|------|------|
| 🔒 **Local-only** | Every script is stdlib-only (zero external deps); no data leaves your machine |
| 🛡️ **Safe by default** | `install.mjs` only copies files, touches no system config; no executable binaries |
| 👀 **Fully open source** | Transparent code, auditable at any time; all tools are stdlib Python |
| 🔍 **Self-test coverage** | Every tool ships `--selftest` (hit anchors + anti-false-positive anchors); dual-anchor architecture keeps rules honest |
| 🧩 **Modular** | Don't trust a component? Delete that script file; the rest keeps working |

### Script security audit

Core scripts passed a three-front security review: JSON injection (stdlib `json.load` parses safely, no eval), HTML XSS (uniform `html.escape()` escaping, zero hits), Python code injection ($value handled as a string, no eval). **Zero vulnerabilities.**

---

## ⭐ Why it earns a star

- **Verifiable**: every rule either carries a source anchor or can be re-derived by a script — citations are acknowledgements, not dependencies
- **A culture of measurement**: 34 RUBRIC runs + with/without-skill controlled experiments (+6/+5/+6/+4) + cold-start isolation tests, all on disk and inspectable
- **Maintainable by one person**: 16 tools, 15 self-tested, all stdlib, one `doctor` command checks everything — when rules age, we update them; you don't worry

---

## ❓ FAQ

**Q: With glasspring installed, will the agent's pages definitely "look good"?**

No. glasspring guards a **verifiable floor**, not an aesthetic ceiling: contrast gets measured, slop gets blocked, renders get probed. Whether the result looks good still depends on your brief and the model — but it guarantees you'll never again receive a "seems to run" phoned-in page.

**Q: Can't the agent just cite the WCAG / HIG docs? Why this?**

Citing is not measuring. A model will fluently cite WCAG 1.4.3 and then hand back a gray-on-gray pair nobody ever computed. glasspring turns "citing the clause" into "running the numbers and emitting a report": every rule either carries a source anchor or is re-derivable by script — citations are acknowledgements, not dependencies.

**Q: If every gate passes, is the design correct?**

PASS is a **necessary condition, not a sufficient one**. The gates block unacceptable delivery; they cannot block mediocrity — a zero-slop page can still be boring. In the other direction, a FAIL is always a real problem: a genuine defect or drift that needs fixing; the dual-anchor self-tests (hit anchors + anti-false-positive anchors) exist precisely to prevent dead rules and false alarms.

**Q: Does it slow the agent down? Does it conflict with my existing shadcn / component libraries?**

No conflicts — glasspring itself is **not a component library**; the mature-library-first stack actually forbids rolling your own when an existing dependency already covers the need. All tools are stdlib-only and run locally, adding zero runtime dependencies; the agent calls tools on demand and never touches your build chain.

---

## 🌱 Contributing

- **Rule disputes / false positives / misses**: open an issue with the `doctor.py` output attached; pinpointing the exact rule ID is even better
- **PR red line**: **never loosen a rule's threshold to make a scan pass**; new rules must ship with dual-anchor self-tests (hit anchor + anti-false-positive anchor)
- **Translation**: improvements to this file are welcome via PR; the Chinese README is the source of truth

---

> [!WARNING]
> **Anti-impersonation notice**: glasspring's only distribution channel is this GitHub repository — any package named "glasspring" on npm / PyPI / file hosts is not this project. There is no official token, points system, paid group, or paid edition; the code is MIT-licensed open source. Any paid service, fundraising, or operation conducted in the name of glasspring is unrelated to this project; please report it directly.

## 📄 License

[MIT](LICENSE) — use the design rules and tooling freely; Apple's fonts, symbols, and trademarks are not included and never will be. See the source & acknowledgement ledger at `docs/SOURCES.md`.
