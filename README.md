# glasspring

[English](README.md) · [简体中文](README.zh-CN.md)

**Glasspring is a project-local Agent Skill for creating and reviewing responsive web interfaces.** It routes tasks to bundled design references, guides new-page work and in-place UI changes, and offers small local checks for selected implementation details.

The package follows the open [Agent Skills format](https://agentskills.io/specification); a valid package does not by itself prove that a host discovers or follows it.

> **Public source preview · stable release BLOCKED.** Third-party rights review is unresolved. Host task behavior and independent design efficacy have not been established. See the [release gates](docs/RELEASE-GATES.md) for evidence and closure requirements.

## Coffee storefront example

The fictional Morrow Coffee storefront below is a **manual example built with Glasspring's bundled guidance and checks**. It uses a coffee-storefront scenario, but it is not a recorded coding-agent output or an efficacy result. The [public pilot protocol](evals/protocol.json) refers to inputs, including a supplied brand palette, that are absent from this repository, so this page is not a reproducible benchmark run. The bag updates local page state and subtotal only; no order or payment service exists. Products, copy, and images are fictional.

<p align="center"><img src="examples/coffee-storefront/shots/coffee-storefront-desktop.png" alt="Full-page desktop screenshot of the fictional Morrow Coffee storefront." width="100%"><br>Desktop page at 1440px</p>

<p align="center"><img src="examples/coffee-storefront/interaction.gif" alt="Five-frame local interaction: initial page, add House Blend, open the bag, increase the quantity, then remove the item." width="100%"><br>Local shopping-bag interaction</p>

<details>
  <summary>View the mobile layout and open-bag state</summary>
  <p align="center"><img src="examples/coffee-storefront/shots/coffee-storefront-mobile.png" alt="Full-page mobile screenshot of the fictional Morrow Coffee storefront." width="320"></p>
  <p align="center"><img src="examples/coffee-storefront/shots/coffee-storefront-bag-open.png" alt="Open bag with two House Blend items, a $36 subtotal, and a local-demo disclaimer." width="100%"></p>
</details>

Start the example from the repository root:

~~~sh
python -m http.server 8000 --directory examples/coffee-storefront
~~~

Open http://127.0.0.1:8000/preview.html. Inspect the [preview source](examples/coffee-storefront/preview.html), [tokens](examples/coffee-storefront/tokens.css), and [design notes](examples/coffee-storefront/design-notes.md). The [example README](examples/coffee-storefront/README.md) records setup and limitations.

## What Glasspring guides

- **New standalone preview:** asks the agent to create `tokens.css`, `preview.html`, and `design-notes.md`, with narrow and desktop PNG captures in `shots/`.
- **Full restyle:** work in the existing app, preserve its entrypoints, and record before/after evidence.
- **Small UI edit:** keep the existing design system and check the changed area.
- **Review only:** report findings without editing files.

For new previews and restyles, references are routed by product type, domain or style pack, platform, and stack. The new-preview workflow asks the agent to propose three different directions before choosing one; this is a process instruction, not evidence of better results. The bundled default design language is Apple-inspired, while the user's brief and an existing design system take priority; glass is optional.

Available checks include selected text-contrast calculations, a heuristic style-pattern scan, the output contract for new standalone previews, and optional browser screenshots and interaction probes. Browser tools inspect a URL supplied for a specific task or check. An optional stdio MCP server exposes some checks; registration is manual, and production host integration has not been verified.

The design references are bundled guidance; Glasspring does not automatically turn live-product observations into new reference cards. Platform-specific references can inform responsive web previews, but this repository has no validated native-app, game, or mini-program code-output path.

## Install and try

Install into a disposable project first. Replace `PATH_TO_PROJECT` with that project's path. The audited toolchain used Node.js 22.14 and Python 3.12; these are tested versions, not minimum-version guarantees.

~~~sh
git clone https://github.com/Rethymus/glasspring.git
cd glasspring
node skills/glasspring/scripts/install.mjs --target "PATH_TO_PROJECT" --host codex --dry-run
node skills/glasspring/scripts/install.mjs --target "PATH_TO_PROJECT" --host codex
~~~

For Claude Code, use `--host claude`. The installer copies the Skill into the project's `.agents/skills/glasspring` or `.claude/skills/glasspring` directory. The installed folder includes its [scoped third-party notice](skills/glasspring/THIRD_PARTY_NOTICES.md); the broader [repository-level rights review](THIRD_PARTY_NOTICES.md) is not copied. Passing file-copy checks does not prove that a host discovers or follows the Skill. See [installation and host verification](INSTALL.md) for evidence, backup/restore, and removal steps.

After installation, try a task like this in a coding-agent session:

~~~text
Use Glasspring to create a responsive storefront for fictional Morrow Coffee. Use warm cream (#f8f3eb), espresso text (#35221b), and terracotta actions (#93432d). Include a hero, three product cards, and a keyboard-operable local bag that adds and removes products and updates the subtotal; do not add checkout or payment. Use assets already in the target project. If product imagery is missing, create simple CSS or inline SVG illustrations; do not download external assets. Deliver tokens.css, preview.html, and design-notes.md. Check the 390px and 1440px layouts, save narrow and desktop PNG captures in shots/, and report checks you cannot run.
~~~

This is a sample request, not a recorded Agent run or a recipe for reproducing the manual example above.

## Checks and evidence

Run repository checks from the root:

~~~sh
python -m unittest discover -s tests -v
node skills/glasspring/scripts/install.mjs --selftest
python skills/glasspring/scripts/verify_output.py --selftest
python skills/glasspring/scripts/mcp_server.py --selftest
~~~

These commands exercise repository code, not an Agent design task. The standalone-preview contract and browser checks need their required inputs and tools; browser probes need Chromium, and the optional axe check also needs network access. These checks do not score overall design quality, establish a benefit from using the Skill, or certify complete WCAG conformance.

The prior full audit recorded **FAIL / INCOMPLETE**: 12 **PASS**, one real color-contrast failure, one exact expected-negative control, and two **SKIP**; the contrast finding remains unresolved. See the [release gates](docs/RELEASE-GATES.md) for details.

Current host evidence is limited: one fresh Codex session listing the Skill metadata is **PASS**, but access to the installed Skill file remains **UNKNOWN**; Claude discovery and task behavior are **NOT_RUN**. Independent efficacy is **NOT_RUN**. The stable release remains **BLOCKED**. See [installation evidence](INSTALL.md), [evaluation and research](docs/EVALUATION.md), [release gates](docs/RELEASE-GATES.md), and [security notes](SECURITY.md).

## Safety, license, and project files

Tools run with the invoking user's permissions; they are not a sandbox. Browser probes may execute target-page code, and the optional axe check retrieves axe-core from a CDN. Run them only against trusted projects and review [SECURITY.md](SECURITY.md).

The repository includes an [MIT license file](LICENSE). Rights review for retained third-party text, code, and assets remains unresolved; the license file does not establish that those materials are cleared. See the [third-party review](THIRD_PARTY_NOTICES.md).

- [Installable Skill](skills/glasspring/): entrypoint, routed references, scripts, and templates.
- [Coffee storefront example](examples/coffee-storefront/): a manual example, not benchmark evidence.
- [Architecture](docs/ARCHITECTURE.md), [evaluation](docs/EVALUATION.md), and [release gates](docs/RELEASE-GATES.md): product boundary and evidence.
- [Provenance](PROVENANCE.md), [third-party notices](THIRD_PARTY_NOTICES.md), [contributing](CONTRIBUTING.md), and [security](SECURITY.md).
