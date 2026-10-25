# glasspring

[English] · [简体中文](README.zh-CN.md)

**Glasspring is an installable Agent Skill for creating, restyling, and reviewing responsive web interfaces.** For a new page, it guides a coding agent to produce `tokens.css`, `preview.html`, and `design-notes.md`. It routes bundled reference cards by product type, industry, platform, and stack, and provides helpers for selected checks. The cards are static; the repository has no built-in pipeline that studies live products and turns observations into design guidance. Its default design voice is Apple-inspired; the user's brief and existing design system take priority, and glass is optional.

> Public source preview; not ready for a stable release. See the [current evidence and release gates](docs/RELEASE-GATES.md).

## Standalone coffee storefront preview

This fictional storefront is an independently authored visual demo, separate from the try prompt below and the public pilot protocol. It demonstrates local shopping-bag state only; it does not place orders or take payments. It is not a Glasspring run or evaluation result.

<p align='center'><img src='examples/coffee-storefront/assets/preview-desktop.png' alt='Full-page desktop screenshot of the fictional Morrow Coffee storefront.' width='100%'><br>Desktop page</p>

<p align='center'><img src='examples/coffee-storefront/interaction.gif' alt='Five-frame local interaction: add coffee to the bag, open it, update quantity, and remove the item.' width='100%'><br>Standalone example interaction; this browser capture is not a Glasspring session or evaluation.</p>

<details>
  <summary>View the mobile layout</summary>
  <p align='center'><img src='examples/coffee-storefront/assets/preview-mobile.png' alt='Full-page mobile screenshot of the fictional Morrow Coffee storefront.' width='320'></p>
</details>

Run the example from the repository root:

~~~sh
python -m http.server 8000 --directory examples/coffee-storefront
~~~

Then open http://127.0.0.1:8000/. See the [page source](examples/coffee-storefront/index.html) and [example notes](examples/coffee-storefront/README.md) for its fictional content and asset provenance.

## Task modes in the skill

| Request | Intended work |
|---|---|
| New web page | Create a responsive preview with tokens.css, preview.html, and design-notes.md |
| Full restyle | Change an existing web UI, then review the changed states and record decisions |
| Small UI edit | Preserve the current design system and check the affected area |
| Review | Report findings without editing files |

For native apps, games, and mini-programs, the current skill produces a web preview unless a separate platform implementation is available and tested.

## Workflow

Glasspring is instruction-led rather than a hosted generator. The agent selects relevant reference cards and helper commands for the task; a person still reviews the result and decides what to ship.

~~~mermaid
flowchart LR
    A['Brief and current design system'] --> B['Select relevant reference cards']
    B --> C['Coding agent builds, edits, or reviews the UI']
    C --> D['Selected local checks and screenshots']
    D --> E['Human review and delivery']
~~~

An optional stdio MCP server exposes some helper tools. Registration is manual, and integration inside a production host has not been verified.

The checks cover selected rules and behaviors. They do not certify design quality, every interaction, or complete WCAG conformance.

## Install and try

Clone the repository, then install into a disposable project. From the repository root, preview the copy operation with --dry-run:

~~~sh
git clone https://github.com/Rethymus/glasspring.git
cd glasspring
node skills/glasspring/scripts/install.mjs --target "PATH_TO_PROJECT" --host codex --dry-run
node skills/glasspring/scripts/install.mjs --target "PATH_TO_PROJECT" --host codex
~~~

For Claude Code, use --host claude. Replace PATH_TO_PROJECT with a project directory on your machine. See [installation and host verification](INSTALL.md), including backup and restore behavior.

The installer and checks have been run with Node.js 22 and Python 3.12. Browser probes also need Chromium and network access to fetch axe-core.

Start a new host session after installation. Check whether it lists Glasspring, ask it to use the skill for one small task, and record whether it reads the installed file and follows the instructions. A successful file copy alone does not prove discovery or task behavior.

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

These validate selected helper logic and package behavior; they do not run a model or establish that an agent will follow the skill.

For a generated run directory, you can also check the output structure and selected static rules:

~~~sh
python skills/glasspring/scripts/doctor.py --target "PATH_TO_RUN"
~~~

This check does not measure design quality or verify every interaction.

| Area | Recorded status |
|---|---|
| Main CI | **PASS** for the recorded Windows, macOS, and Ubuntu checks; this does not test an agent session. [Run details](https://github.com/Rethymus/glasspring/actions/runs/40198893762) |
| Last recorded sample suite | **FAIL**: 12 PASS, 1 contrast FAIL, 1 expected negative-control row, and 2 network SKIP; exit code 1. Sample projects are absent from the public tree, so a fresh replay is **INSUFFICIENT_EVIDENCE**. |
| Host behavior | **PARTIAL**: one Codex session listed skill metadata (**PASS**); reading the installed skill and task behavior remain **UNKNOWN**; Claude discovery and task behavior are **NOT_RUN**. |
| Independent efficacy | **NOT_RUN**. The public [protocol](evals/protocol.json) is incomplete and lacks referenced palette/component-library inputs and fixed host/model/budget values; replay is **INSUFFICIENT_EVIDENCE**. |
| Privacy review | **PARTIAL**; see [security notes](SECURITY.md). |
| Third-party rights | **BLOCKED** pending file-level source, license, and authority review; see [third-party notices](THIRD_PARTY_NOTICES.md). |
| Browser runtime dependency | **OPEN**: a probe fetches axe-core from a CDN without a pinned integrity value or offline policy. |

The full evidence and release criteria are in [release gates](docs/RELEASE-GATES.md), [evaluation notes](docs/EVALUATION.md), and [host verification](INSTALL.md).

## Safety and project files

The tools run with the invoking user's permissions; they are not a sandbox. Browser probes may execute target-page code and retrieve axe-core at runtime. Run them only against trusted projects and review [SECURITY.md](SECURITY.md).

- [Skill entrypoint and routed references](skills/glasspring/)
- [Design workflow and boundaries](docs/ARCHITECTURE.md)
- [Evaluation plan and benchmark context](docs/EVALUATION.md)
- Source and asset review: [PROVENANCE.md](PROVENANCE.md), [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)
- Installation, contribution, and security guidance: [INSTALL.md](INSTALL.md), [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md)

The root [MIT license](LICENSE) covers only project-authored material that contributors have authority to license. It does not clear third-party text, code, or assets.
