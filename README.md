# glasspring

[English](README.md) · [简体中文](README.zh-CN.md)

**Glasspring is a project-level Agent Skill for responsive web-interface work.** Its instructions guide an agent to choose static design references by product type, domain, platform, and stack, then select optional local or browser checks. A new standalone preview uses the three-file contract: `tokens.css`, `preview.html`, and `design-notes.md`.

> Public source preview. A stable release is **BLOCKED** while third-party rights, independent efficacy, host behavior, and browser-runtime dependency controls remain unresolved. See the [release gates](docs/RELEASE-GATES.md).

## Coffee storefront example

This fictional storefront is a **manual example prepared with Glasspring's reference and check workflow**. It follows the task brief below and includes the three-file preview contract. It is not a recorded agent-host session, an independent efficacy result, or a replay of the incomplete public pilot.

The page, products, and copy are fictional. The hero, product, and botanical images were generated for this example. The bag changes local page state and subtotal only; it does not place orders or take payments.

<p align='center'><img src='examples/coffee-storefront/shots/coffee-storefront-desktop.png' alt='Full-page desktop screenshot of the fictional Morrow Coffee storefront.' width='100%'><br>Desktop page at 1440px</p>

<p align='center'><img src='examples/coffee-storefront/interaction.gif' alt='Five-frame local interaction: add coffee, open the bag, increase quantity to two, and remove the item.' width='100%'><br>Local shopping-bag interaction, not evidence of agent discovery or efficacy.</p>

<details>
  <summary>View the mobile layout and open bag state</summary>
  <p align='center'><img src='examples/coffee-storefront/shots/coffee-storefront-mobile.png' alt='Full-page mobile screenshot of the fictional Morrow Coffee storefront.' width='320'></p>
  <p align='center'><img src='examples/coffee-storefront/shots/coffee-storefront-bag-open.png' alt='Open bag with two House Blend items, a $36 subtotal, and a local-demo disclaimer.' width='100%'></p>
</details>

Run the example from the repository root:

~~~sh
python -m http.server 8000 --directory examples/coffee-storefront
~~~

Then open http://127.0.0.1:8000/preview.html. The [example files](examples/coffee-storefront/) include the page, tokens, and asset provenance; [design notes](examples/coffee-storefront/design-notes.md) record the manual checks and their limits.

## What it does

| Request | Intended workflow |
|---|---|
| New standalone web preview | Select relevant references, build a page, and deliver `tokens.css`, `preview.html`, and `design-notes.md` |
| Full restyle | Change the existing app and token entrypoint, then record before/after evidence |
| Small UI edit | Preserve the current design system and check the affected area |
| Review only | Return findings without editing files |

For each task, the instructions call for at most three routed design references; platform adapters do not count toward that limit, and `glass.md` is required only when a translucent surface is used. Checks can measure selected contrast pairs, scan selected static patterns, verify deliverable structure, and capture or probe selected browser states when browser tooling is available.

The reference cards are static; Glasspring does not capture live products or turn research observations into design guidance. Its default material and motion guidance is Apple-inspired, subject to the brief and existing design system; glass effects are optional. “Apple-inspired” describes a design direction and does not imply Apple affiliation. The checks do not rate overall design quality or certify full WCAG conformance.

For native apps, games, and mini-programs, the current workflow produces a web preview unless a separate platform implementation is available and tested. An optional stdio MCP server exposes some helpers; registration is manual, and production-host integration is unverified.

## Install and try

Clone the repository and preview the install into a disposable project. Replace `PATH_TO_PROJECT` with a path valid for your shell:

~~~sh
git clone https://github.com/Rethymus/glasspring.git
cd glasspring
node skills/glasspring/scripts/install.mjs --target "PATH_TO_PROJECT" --host codex --dry-run
node skills/glasspring/scripts/install.mjs --target "PATH_TO_PROJECT" --host codex
~~~

Use `--host claude` for the Claude Code project directory. The installer writes to `.agents/skills/glasspring` for Codex and `.claude/skills/glasspring` for Claude Code. Project checks were run with Node.js 22 and Python 3.12; browser checks need Chromium. File copying alone does not prove host discovery or task behavior. See [installation and host verification](INSTALL.md) for backup, restore, and host evidence.

Try Glasspring with this task:

~~~text
Use Glasspring to create a responsive storefront for fictional Morrow Coffee. Use warm cream (#f8f3eb), espresso text (#35221b), and terracotta actions (#93432d). Include a hero, three product cards, and a keyboard-operable local bag panel that adds and removes products and updates the subtotal; do not add checkout or payment. Use only assets already in the target project. If it has no product imagery, create simple CSS or inline SVG illustrations; do not download external assets. Deliver tokens.css, preview.html, and design-notes.md. Check the page at 390px and 1440px, and report any checks you cannot run.
~~~

## Checks and current evidence

Run the local checks from the repository root:

~~~sh
python -m unittest discover -s tests -v
node skills/glasspring/scripts/install.mjs --selftest
python skills/glasspring/scripts/verify_output.py --selftest
python skills/glasspring/scripts/mcp_server.py --selftest
~~~

For a generated run directory, check its output structure and selected static rules:

~~~sh
python skills/glasspring/scripts/doctor.py --target "PATH_TO_RUN"
~~~

These commands validate selected helper logic and package behavior. They do not run an agent or establish that a host will discover and follow the skill. The axe check in `probe_render.py` needs Chromium and network access to fetch axe-core. If axe is unavailable or skipped, its coverage is recorded as unavailable and the overall verdict is `UNKNOWN` when no observed check fails (or `FAIL` if another check fails), never `PASS` on the basis of the omitted check.

| Area | Recorded status |
|---|---|
| Public `main` CI | **PASS** for recorded Windows, macOS, and Ubuntu checks; it does not test an agent session. [Run details](https://github.com/Rethymus/glasspring/actions/runs/40198893762) |
| Historical full audit suite | **FAIL**: 12 PASS, 1 contrast FAIL, 1 expected negative-control row, and 2 network SKIP across 16 rows; exit code 1. The contrast finding remains open, and the sample inputs are not in this repository. |
| Follow-up browser sample gate | **PASS, bounded** on 11 private sample directories at 390px and 1440px; 0 FAIL and 0 SKIP. A public replay is **INSUFFICIENT_EVIDENCE** because the inputs are not included. It does not close the historical contrast finding or establish design quality. |
| Host behavior | **PARTIAL**: one Codex session listed skill metadata (**PASS**); installed-file reading and task behavior remain **UNKNOWN**; Claude discovery and task behavior are **NOT_RUN**. |
| Independent efficacy | **NOT_RUN**; public replay is **INSUFFICIENT_EVIDENCE**. The public pilot lacks referenced palette/component-library inputs, fixed host/model/budget values, and a holdout task set. See the [protocol](evals/protocol.json). |
| Privacy / third-party rights / browser runtime | **PARTIAL / BLOCKED / OPEN**, respectively. See [security notes](SECURITY.md), [third-party notices](THIRD_PARTY_NOTICES.md), and the [release gates](docs/RELEASE-GATES.md). |

The evidence table distinguishes tool checks from host behavior and independent efficacy. Do not infer improved design quality, support for every agent, or full WCAG conformance from these results. See [evaluation notes](docs/EVALUATION.md) for the study plan and research context.

## Safety and project files

The tools run with the invoking user's permissions; they are not a sandbox. Browser probes may execute target-page code and retrieve axe-core at runtime. Run them only against trusted projects and review [SECURITY.md](SECURITY.md).

- [Skill entrypoint and routed references](skills/glasspring/)
- [Design workflow and boundaries](docs/ARCHITECTURE.md)
- [Evaluation plan and benchmark context](docs/EVALUATION.md)
- Source and asset review: [PROVENANCE.md](PROVENANCE.md), [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)
- Installation, contribution, and security guidance: [INSTALL.md](INSTALL.md), [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md)

The root [MIT license](LICENSE) covers only project-authored material that contributors have authority to license. It does not clear third-party text, code, or assets.
