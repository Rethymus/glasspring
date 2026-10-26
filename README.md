# glasspring

[English](README.md) · [简体中文](README.zh-CN.md)

**Glasspring is a project-local Agent Skill package intended to guide coding agents through designing, restyling, or reviewing responsive web interfaces.** It contains a `SKILL.md`, curated static design references, and helper scripts. The instructions describe how an agent should choose references and run selected checks; live host behavior is incompletely verified, as shown below. A new standalone preview uses the three-file contract: `tokens.css`, `preview.html`, and `design-notes.md`.

The reference library is static. Glasspring does not automatically inspect live products and turn observations into new reference cards.

> This is a public source preview. A stable release is **BLOCKED** while third-party rights, independent efficacy, host behavior, and browser-runtime dependency controls remain unresolved. See the [release gates](docs/RELEASE-GATES.md).

## Coffee storefront example

This fictional storefront is a **manual example prepared with Glasspring's references and checks**. It follows the self-contained README task below, not the separate coffee task in the [public pilot protocol](evals/protocol.json): that pilot task's referenced palette input is absent from this repository. These images show the example, not an agent-host session or an efficacy result.

The page, products, and copy are fictional; its hero, product, and botanical images were generated for this example. The bag updates local page state and subtotal only. It does not place orders or take payments.

<p align='center'><img src='examples/coffee-storefront/shots/coffee-storefront-desktop.png' alt='Full-page desktop screenshot of the fictional Morrow Coffee storefront.' width='100%'><br>Desktop page at 1440px</p>

<p align='center'><img src='examples/coffee-storefront/interaction.gif' alt='Five-frame local interaction: initial page, add House Blend, open the bag, add the same product again, then remove it.' width='100%'><br>Local shopping-bag interaction</p>

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

## Workflows

| Request | Intended workflow |
|---|---|
| New standalone web preview | Select relevant references, build a page, and deliver `tokens.css`, `preview.html`, and `design-notes.md` |
| Full restyle | Work in the existing app and token entrypoint; record decisions and before/after evidence |
| Small UI edit | Preserve the current design system and check the affected area |
| Review only | Return findings without editing files |

## How the instructions work

- **Choose references:** The core routing budget is at most three craft references; a selected style pack replaces a domain pack. Task-specific guides and platform adapters may add reads when relevant.
- **Choose a direction:** For a new preview or full restyle, the instructions ask the agent to consider three distinct directions and commit to one before building. This is an instructed workflow, not an independently measured design-quality result.
- **Build and check:** New previews use the three-file contract. Restyles work in the existing app and token entrypoint. Helper scripts can check selected contrast pairs and static patterns, verify the output structure, and capture or probe selected browser states when the required browser tooling is available.
- **Respect the limits:** Browser helpers can capture or probe a supplied page. The default material and motion guidance is Apple-inspired, subject to the brief and existing design system; this describes a design direction and does not imply Apple affiliation. Glass is optional. Native apps, games, and mini-programs receive a web preview unless a separate platform implementation is available and tested. Checks do not rate overall design quality or certify full WCAG conformance. Optional MCP registration is manual, and production-host integration is unverified.

See [architecture notes](docs/ARCHITECTURE.md) for the product boundary, [provenance notes](PROVENANCE.md) and [third-party notices](THIRD_PARTY_NOTICES.md) for source and rights gaps.

## Install and try

Clone the repository and preview installation into a disposable project. Replace `PATH_TO_PROJECT` with a path valid for your shell:

~~~sh
git clone https://github.com/Rethymus/glasspring.git
cd glasspring
node skills/glasspring/scripts/install.mjs --target "PATH_TO_PROJECT" --host codex --dry-run
node skills/glasspring/scripts/install.mjs --target "PATH_TO_PROJECT" --host codex
~~~

Use `--host claude` for the Claude Code project directory. The installer copies files into `.agents/skills/glasspring` for Codex or `.claude/skills/glasspring` for Claude Code. These file-copy checks do not prove that a host discovers or follows the Skill. See [installation and host verification](INSTALL.md) for current evidence and backup/restore instructions.

Recorded project checks used Node.js 22 and Python 3.12. Browser probes require Chromium; the axe check also fetches axe-core from a CDN.

Try this task in a coding-agent session after installing:

~~~text
Use Glasspring to create a responsive storefront for fictional Morrow Coffee. Use warm cream (#f8f3eb), espresso text (#35221b), and terracotta actions (#93432d). Include a hero, three product cards, and a keyboard-operable local bag panel that adds and removes products and updates the subtotal; do not add checkout or payment. Use only assets already in the target project. If it has no product imagery, create simple CSS or inline SVG illustrations; do not download external assets. Deliver tokens.css, preview.html, and design-notes.md. Check the page at 390px and 1440px, and report any checks you cannot run.
~~~

## Checks and current evidence

Run the helper and package checks from the repository root:

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

These checks exercise selected helper logic and packaging. They do not run a coding agent or show that the Skill improves design. The axe check in `probe_render.py` needs Chromium and network access to fetch axe-core; if that coverage is unavailable or skipped, the result is `UNKNOWN` unless another observed failure makes it `FAIL`.

| Area | Recorded status |
|---|---|
| Public `main` CI | **PASS** on Windows, macOS, and Ubuntu. It tests the repository checks, not an agent session. [Run details](https://github.com/Rethymus/glasspring/actions/runs/40198893762) |
| Historical full audit suite | **FAIL**: 12 PASS, 1 contrast FAIL, 1 expected negative-control row, and 2 network SKIP across 16 rows; exit code 1. The contrast finding remains open, and the sample inputs are private. |
| Follow-up browser sample gate | **PASS, bounded** on 11 private sample directories at 390px and 1440px; 0 FAIL and 0 SKIP. Public replay is **INSUFFICIENT_EVIDENCE** because the inputs are not included. This does not close the historical contrast finding or establish design quality. |
| Host behavior | **PARTIAL**: one Codex session listed Skill metadata (**PASS**); installed-file reading and task behavior remain **UNKNOWN**; Claude discovery and task behavior are **NOT_RUN**. |
| Independent efficacy | **NOT_RUN**; the public pilot is not a holdout, and its referenced palette and component-library inputs are missing. See the [protocol](evals/protocol.json) and [evaluation notes](docs/EVALUATION.md). |
| Privacy / third-party rights / browser runtime | **PARTIAL / BLOCKED / OPEN**, respectively. See [security notes](SECURITY.md), [third-party notices](THIRD_PARTY_NOTICES.md), and the [release gates](docs/RELEASE-GATES.md). |

Do not infer support for every agent, improved design quality, or full WCAG conformance from these results. The [evaluation notes](docs/EVALUATION.md) explain the study plan and research context.

## Safety and project files

The tools run with the invoking user's permissions; they are not a sandbox. Browser probes may execute target-page code and retrieve axe-core at runtime. Run them only against trusted projects and review [SECURITY.md](SECURITY.md).

- [Skill entrypoint and routed references](skills/glasspring/)
- [Design workflow and boundaries](docs/ARCHITECTURE.md)
- [Evaluation plan and benchmark context](docs/EVALUATION.md)
- Source and asset review: [PROVENANCE.md](PROVENANCE.md), [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)
- Installation, contribution, and security guidance: [INSTALL.md](INSTALL.md), [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md)

The root [MIT license](LICENSE) covers only project-authored material that contributors have authority to license. It does not clear third-party text, code, or assets.
