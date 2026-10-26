# glasspring

[English](README.md) · [简体中文](README.zh-CN.md)

**Glasspring is an opinionated, project-level Agent Skill for responsive web interface work.** It guides a coding agent through a new preview, a larger restyle, a small UI edit, or a read-only review. It routes to bundled design references and selected local checks. The default guidance has an Apple-inspired starting point; the user brief and existing design system take priority, and glass effects are optional.

The package follows the open [Agent Skills format](https://agentskills.io/specification); format compliance alone does not prove that a host discovers or follows the Skill.

> **Public source preview · stable release BLOCKED.** Third-party rights review is still open. See [release gates](docs/RELEASE-GATES.md).

## Coffee storefront example

This is a manually packaged Glasspring-guided example, not output from a fresh Agent host or evidence that the Skill improves results. It uses fictional products and a local-only shopping bag; no checkout or payment is implemented. The [design notes](examples/coffee-storefront/design-notes.md) record what was checked and what remains unverified.

<p align="center"><img src="examples/coffee-storefront/shots/coffee-storefront-desktop.png" alt="Full-page desktop screenshot of the fictional Morrow Coffee storefront." width="100%"><br>1440px desktop page</p>

<p align="center"><img src="examples/coffee-storefront/interaction.gif" alt="Local interaction: initial page, add House Blend, open the bag, increase quantity, then remove the item." width="100%"><br>Local shopping-bag interaction</p>

<details>
  <summary>Mobile layout and open-bag view</summary>
  <p align="center"><img src="examples/coffee-storefront/shots/coffee-storefront-mobile.png" alt="Full-page mobile screenshot of the fictional Morrow Coffee storefront." width="320"></p>
  <p align="center"><img src="examples/coffee-storefront/shots/coffee-storefront-bag-open.png" alt="Open shopping bag with two House Blend items, a 36 dollar subtotal, and a local-demo notice." width="100%"></p>
</details>

The example was captured at **390px and 1440px**. Its record reports **6/6 output-contract clauses PASS**, **0 scan findings**, **7 selected contrast pairs PASS**, and a **Playwright interaction smoke PASS**. The render probe with axe disabled is **UNKNOWN** (exit 2); automated axe coverage is **NOT_RUN**. These results apply to this example only.

To view the page locally from the repository root:

~~~sh
python -m http.server 8000 --directory examples/coffee-storefront
~~~

Open <http://127.0.0.1:8000/preview.html>. Browse the [preview source](examples/coffee-storefront/preview.html), [design tokens](examples/coffee-storefront/tokens.css), and [full check record](examples/coffee-storefront/design-notes.md).

## What the Skill guides

- **New preview:** creates `tokens.css`, `preview.html`, `design-notes.md`, and desktop/mobile PNGs under `shots/`. The workflow asks for three distinct directions before implementation.
- **Larger restyle:** works inside the existing app and records before/after evidence.
- **Small UI edit:** follows the existing design system and limits review to the changed area.
- **Read-only review:** reports findings without editing files.

For new previews and larger restyles, guidance routes by product type, domain or style, platform, and technology stack. The repository includes selected-contrast calculations, heuristic style scans, an output-contract checker, browser screenshots and interaction probes, and an optional stdio MCP server. MCP setup is manual; production-host integration has not been verified.

The references are bundled guidance for principles and patterns, not instructions to copy a product's UI or assets. Glasspring does not automatically turn observations of live products into new reference cards. Native apps, games, and mini-program code delivery are outside the validated scope.

## Install and try it

Start in a disposable project. Replace `PATH_TO_PROJECT` with its path. Node.js 22.14 and Python 3.12 are the versions used in the recorded checks; they are not declared minimums.

~~~sh
git clone https://github.com/Rethymus/glasspring.git
cd glasspring
node skills/glasspring/scripts/install.mjs --target "PATH_TO_PROJECT" --host codex --dry-run
node skills/glasspring/scripts/install.mjs --target "PATH_TO_PROJECT" --host codex
~~~

For a Claude Code project, use `--host claude`. The installer copies the Skill to `.agents/skills/glasspring` or `.claude/skills/glasspring`. Installation and file-copy checks do not prove host discovery or task behavior. See [installation and host verification](INSTALL.md) for limits, backup, and removal instructions.

After installation, start a new coding-agent session and try:

~~~text
Use Glasspring to make a responsive storefront for the fictional Morrow Coffee brand. Use warm cream (#f8f3eb), espresso text (#35221b), and terracotta buttons (#93432d). Include a hero, three product cards, and a keyboard-operable local shopping bag that updates quantity and subtotal when items are added or removed. Do not add checkout or payment. Use existing project assets; if product images are missing, draw simple illustrations with CSS or inline SVG instead of downloading assets. Deliver tokens.css, preview.html, and design-notes.md. Check the layout at 390px and 1440px, save mobile and desktop PNGs under shots/, and report checks you could not run.
~~~

This is a sample request, not a recorded host run or benchmark result.

## Checks and current evidence

Run the repository's local checks from its root:

~~~sh
python -m unittest discover -s tests -v
node skills/glasspring/scripts/install.mjs --selftest
python skills/glasspring/scripts/verify_output.py --selftest
python skills/glasspring/scripts/mcp_server.py --selftest
~~~

These check repository code; they do not evaluate an Agent's design output. The latest recorded project evidence remains bounded:

| Area | State |
|---|---|
| Historical full audit | **FAIL / INCOMPLETE**: 12 PASS, 1 real contrast failure, 1 expected-negative control, and 2 SKIP; the contrast issue remains open. |
| Privacy review | **PARTIAL**: heuristic text scan only; no dedicated secret scan or complete binary/history review. |
| Codex host | Skill metadata listing **PASS**; reading the installed file and task behavior **UNKNOWN**. |
| Claude Code host | Fresh-session discovery and task behavior **NOT_RUN**. |
| Independent efficacy | **NOT_RUN (DESIGNED_NOT_EXECUTED)**; the public pilot is not a hidden holdout, and its coffee task's supplied palette is absent from this repository. |
| Browser dependency integrity | **OPEN**: axe-core is fetched from a CDN without a pinned integrity value or offline coverage policy. |
| Stable release | **BLOCKED** until all open release gates are resolved. |

See [release gates](docs/RELEASE-GATES.md), [evaluation notes](docs/EVALUATION.md), [provenance](PROVENANCE.md), and [third-party notices](THIRD_PARTY_NOTICES.md) for evidence and closure requirements. No claim is made that the Skill improves design quality, works in every Agent host, or fully conforms to WCAG.

## Safety and license

Tools run with the caller's permissions and are not sandboxed. Browser probes may execute target-page code; the optional axe check downloads axe-core from a CDN. Use trusted projects and read the [security notes](SECURITY.md).

The repository includes an [MIT license](LICENSE), but retained third-party text, code, and assets still need rights review. The repository license does not resolve those source obligations.

## Project map

- [Installable Skill](skills/glasspring/): entry instructions, routed references, scripts, and templates.
- [Coffee storefront](examples/coffee-storefront/): manual example and its check record.
- [Architecture](docs/ARCHITECTURE.md), [evaluation](docs/EVALUATION.md), and [release gates](docs/RELEASE-GATES.md): scope and evidence.
- [Contributing](CONTRIBUTING.md), [security](SECURITY.md), [provenance](PROVENANCE.md), and [third-party notices](THIRD_PARTY_NOTICES.md).
