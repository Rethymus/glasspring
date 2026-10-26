# glasspring

[English](README.md) · [简体中文](README.zh-CN.md)

**Glasspring is a project-local Agent Skill for coding agents working on responsive web interfaces.** It supports new previews, full restyles, small edits, and read-only reviews. It selects static references for each task and includes scripts for selected local and browser checks. The reference library is maintained in the repository; it does not automatically inspect live products and create new reference cards.

## Coffee storefront example

This fictional storefront is a **manual example guided by Glasspring's references and checks**. It shows a responsive page and a local shopping-bag interaction; the page, products, and copy are fictional, and the images were generated for this example. The bag updates page state and subtotal only, with no order or payment service. These captures describe the example, not an installed-host run or a comparative efficacy study.

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

> **Release status:** public source preview. A stable release remains **BLOCKED** by unresolved third-party rights, independent efficacy, host behavior, and browser-runtime dependency gates. See the [release gates](docs/RELEASE-GATES.md).

## Task modes

| Task | Workflow |
|---|---|
| New standalone web preview | Select relevant references, build a page, and deliver `tokens.css`, `preview.html`, and `design-notes.md` |
| Full restyle | Keep the existing app and token entrypoint; record decisions and before/after evidence |
| Small UI edit | Preserve the current design system and check the affected area |
| Review only | Return findings without editing files |

## Routing and boundaries

- References route by product type, domain or style pack, platform, and applicable stack. The core craft budget is at most three references; a style pack replaces a domain pack. Relevant guides and platform adapters may add reads.
- For a new preview or full restyle, the instructions ask the agent to consider three distinct directions before building. This describes the workflow, not a measured quality result.
- The default design language is Apple-inspired; the brief and existing design system take precedence, and glass is optional.
- New previews use the three-file contract. Full restyles keep the existing app paths. Checks cover selected contrast pairs and static patterns; browser captures and probes require the relevant local tooling. They do not score overall design quality or certify full WCAG conformance.
- Native apps, games, and mini-programs receive web previews unless a separate platform implementation has been built and tested. MCP registration is manual. See the status table and [installation notes](INSTALL.md) for host evidence.

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

For a new-preview run directory, check its output structure and selected static rules:

~~~sh
python skills/glasspring/scripts/doctor.py --target "PATH_TO_RUN" --skip-selftest
~~~

The package commands exercise selected helper logic; they do not run an agent task. The `doctor.py --skip-selftest` command runs a static scan and the new-preview output contract, so use it only for a standalone preview. The axe check in `probe_render.py` requires Chromium and network access to fetch axe-core; missing or skipped coverage is `UNKNOWN` unless another observed failure makes the result `FAIL`.

| Area | Recorded status |
|---|---|
| Published `main` snapshot CI (`2ce478c`) | **PASS** on Windows, macOS, and Ubuntu. It tests the repository checks, not an agent session. [Run details](https://github.com/Rethymus/glasspring/actions/runs/40198893762) |
| Historical full audit suite | **FAIL**: 12 PASS, 1 contrast FAIL, 1 expected negative-control row, and 2 network SKIP across 16 rows; exit code 1. The contrast finding remains open, and the sample inputs are private. |
| Follow-up browser sample gate | **PASS, bounded** on 11 private sample directories at 390px and 1440px; 0 FAIL and 0 SKIP. Public replay is **INSUFFICIENT_EVIDENCE** because the inputs are not included. This does not close the historical contrast finding or establish design quality. |
| Host behavior | **PARTIAL**: one Codex session listed Skill metadata (**PASS**); installed-file reading and task behavior remain **UNKNOWN**; Claude discovery and task behavior are **NOT_RUN**. |
| Independent efficacy | **NOT_RUN**; the public pilot is not a holdout, and its referenced palette and component-library inputs are missing. See the [protocol](evals/protocol.json) and [evaluation notes](docs/EVALUATION.md). |
| Privacy / third-party rights / browser runtime | **PARTIAL / BLOCKED / OPEN**, respectively. See [security notes](SECURITY.md), [third-party notices](THIRD_PARTY_NOTICES.md), and the [release gates](docs/RELEASE-GATES.md). |

These results are limited to the cited runs; they do not establish broad host compatibility, independent design improvement, or full WCAG conformance. See the [evaluation notes](docs/EVALUATION.md) for the study plan and research context.

## Safety and project files

The tools run with the invoking user's permissions; they are not a sandbox. Browser probes may execute target-page code and retrieve axe-core at runtime. Run them only against trusted projects and review [SECURITY.md](SECURITY.md).

- [Skill entrypoint and routed references](skills/glasspring/)
- [Design workflow and boundaries](docs/ARCHITECTURE.md)
- [Evaluation plan and benchmark context](docs/EVALUATION.md)
- Source and asset review: [PROVENANCE.md](PROVENANCE.md), [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)
- Installation, contribution, and security guidance: [INSTALL.md](INSTALL.md), [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md)

The root [MIT license](LICENSE) covers only project-authored material that contributors have authority to license. It does not clear third-party text, code, or assets.
