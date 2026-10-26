# glasspring

[English](README.md) · [简体中文](README.zh-CN.md)

**Glasspring is a project-level Agent Skill for responsive web interface work.** It guides a coding agent through a new preview, a full restyle, a small UI edit, or a read-only review. For a new preview or restyle, it routes the brief by product type, domain or style, platform, and stack; then guides direction, tokens, implementation, viewport review, and selected checks. Its default material and motion guidance is Apple-inspired; the brief and existing design system take priority, and glass effects are optional.

The package follows the open [Agent Skills format](https://agentskills.io/specification). That format loads the full `SKILL.md` when a host activates a Skill; Glasspring then asks the agent to read no more than three core design references, with task-specific guides and platform adapters added when needed. This routing instruction is not a measured claim about token savings or better results, and host loading behavior has not been verified across hosts. References are static: Glasspring does not browse live products and turn observations into new reference cards. Native-app, game, and mini-program code delivery is outside the validated scope.

## When to use Glasspring

- "Make a responsive preview page / dashboard / landing page" — new preview.
- "Redesign this app's look" — full restyle that keeps your existing token system.
- "Small UI fix" — edit within the existing system.
- "Review this page's design" — read-only report.

Glasspring does not deliver native-app, game, or mini-program code; its platform references can inform a web preview only.

> **Public source preview · stable release BLOCKED.** Rights review for retained third-party material is incomplete. See the [release gates](docs/RELEASE-GATES.md) and [third-party notices](THIRD_PARTY_NOTICES.md) before redistributing the source or an installed copy.

## Coffee storefront example

This manually packaged example shows a responsive page and a local shopping-bag interaction. Its fictional brief pins the cream, espresso, and terracotta palette; the selected composition is a split hero with three product cards. It is not a fresh Agent-host run or evidence that Glasspring improves design outcomes. The [design notes](examples/coffee-storefront/design-notes.md) record its route and checks.

<p align="center"><img src="examples/coffee-storefront/shots/coffee-storefront-desktop.png" alt="Full-page desktop screenshot of the fictional Morrow Coffee storefront." width="100%"><br>1440px desktop page</p>

<p align="center"><img src="examples/coffee-storefront/interaction.gif" alt="Local interaction: initial page, add House Blend, open the bag, increase quantity, then remove the item." width="100%"><br>Local shopping-bag interaction</p>

<details>
  <summary>Mobile layout and open-bag view</summary>
  <p align="center"><img src="examples/coffee-storefront/shots/coffee-storefront-mobile.png" alt="Full-page mobile screenshot of the fictional Morrow Coffee storefront." width="320"></p>
  <p align="center"><img src="examples/coffee-storefront/shots/coffee-storefront-bag-open.png" alt="Open shopping bag with two House Blend items, a 36 dollar subtotal, and a local-demo notice." width="100%"></p>
</details>

For this example only, the output contract passed **6/6 clauses**, **7 selected contrast pairs** passed, the local Playwright bag flow passed, and the style scan found **0 findings**. The render probe was **UNKNOWN** (exit 2); axe coverage was **NOT_RUN**. These checks do not establish full WCAG conformance, visual quality, or Skill efficacy.

Run the page from the repository root:

~~~sh
python -m http.server 8000 --directory examples/coffee-storefront
~~~

Open <http://127.0.0.1:8000/preview.html>. See the [preview source](examples/coffee-storefront/preview.html), [tokens](examples/coffee-storefront/tokens.css), and [check record](examples/coffee-storefront/design-notes.md).

## Install and try Glasspring

Clone the repository and install into a disposable project. The installer runs on Node.js; helper tools use Python. The recorded checks used Node.js 22.14 and Python 3.12; these are tested versions, not declared minimums.

~~~sh
git clone https://github.com/Rethymus/glasspring.git
cd glasspring
node skills/glasspring/scripts/install.mjs --target "PATH_TO_PROJECT" --host codex --dry-run
node skills/glasspring/scripts/install.mjs --target "PATH_TO_PROJECT" --host codex
~~~

Replace `PATH_TO_PROJECT` with a path valid for your shell. For a Claude Code project, use `--host claude`. The installer copies the Skill and its references to `.agents/skills/glasspring` or `.claude/skills/glasspring`; file-copy success does not prove that a host discovers or follows it. See [installation and host verification](INSTALL.md) for backups, removal, and the current host evidence.

After installation, start a new coding-agent session and try:

~~~text
Use Glasspring to make a responsive storefront for the fictional Morrow Coffee brand. Use warm cream (#f8f3eb), espresso text (#35221b), and terracotta buttons (#93432d). Include a hero, three product cards, and a keyboard-operable local shopping bag that updates quantity and subtotal when items are added or removed. Do not add checkout or payment. Use existing project assets; if product images are missing, draw simple illustrations with CSS or inline SVG instead of downloading assets. Deliver tokens.css, preview.html, and design-notes.md. Check the layout at 390px and 1440px, save mobile and desktop PNGs under shots/, and report checks you could not run.
~~~

This is a sample request, not a recorded host run or benchmark result.

## Task modes and tools

| Task | What the Skill guides |
|---|---|
| New preview | Three design directions, semantic tokens, a standalone page, design notes, and narrow/desktop screenshots; selected checks apply to this new-preview output contract. |
| Full restyle | Work in the existing app and token system; capture before/after evidence. |
| Small UI edit | Preserve the existing system and use checks proportional to the changed area. |
| Read-only review | Inspect and report findings without editing project files. |

The package contains the `SKILL.md` workflow, static references, helper scripts, and an optional stdio MCP server. References are guidance, not instructions to copy a particular product's interface or assets. MCP setup is manual and production-host integration has not been verified. Browser probes need Chromium; the optional axe check fetches axe-core 4.10.2 from a CDN. Tools run with the caller's permissions and are not sandboxed; browser checks may execute target-page code. See [security notes](SECURITY.md).

## Current evidence and limits

Evidence snapshot: **2026-10-26**. Repository self-tests check the package and helper tools; they do not grade an Agent's design output.

~~~sh
python -m unittest discover -s tests -v
node skills/glasspring/scripts/install.mjs --selftest
python skills/glasspring/scripts/verify_output.py --selftest
python skills/glasspring/scripts/mcp_server.py --selftest
~~~

| Area | Recorded state |
|---|---|
| Installer file-copy checks | **PASS** in Windows, macOS, and Linux CI; host discovery and task behavior are separate and remain unverified. |
| Codex host | Skill metadata listing **PASS**; installed-file reading and task behavior **UNKNOWN**. |
| Claude Code host | Fresh-session discovery and task behavior **NOT_RUN**. Other hosts **NOT_RUN**. |
| Historical full sample audit | **FAIL / INCOMPLETE**: 12 `PASS`, 1 real contrast `FAIL`, 1 expected-negative control, and 2 `SKIP`; the historical inputs are not in this repository. |
| Independent efficacy comparison | **NOT_RUN**. The public pilot is not a hidden holdout; two task inputs are missing, and it does not separately measure distinctiveness, token cost, or Skill-use coverage. |
| Privacy review | **PARTIAL**: heuristic text scan only; no dedicated secret scan or complete binary/history review. |
| Browser dependency integrity | **OPEN**: axe-core is fetched from a CDN without a pinned integrity value or offline coverage policy. |
| Rights and attribution | **BLOCKED** until retained third-party sources and redistribution obligations are reviewed. |

See [release gates](docs/RELEASE-GATES.md), [evaluation notes](docs/EVALUATION.md), the [public pilot protocol](evals/protocol.json), [provenance](PROVENANCE.md), and [third-party notices](THIRD_PARTY_NOTICES.md) for details and closure criteria. No claim is made that Glasspring improves design quality, works in every Agent host, or fully conforms to WCAG.

## License and project map

The repository includes an [MIT license](LICENSE), but it does not grant rights to third-party material the contributors cannot license. Review the [third-party notices](THIRD_PARTY_NOTICES.md); stable release remains blocked until the rights gate is resolved. “Apple-inspired” describes a visual starting point and does not imply Apple affiliation.

- [Installable Skill](skills/glasspring/): workflow, routed references, scripts, and templates.
- [Coffee storefront](examples/coffee-storefront/): the manual example and its evidence record.
- [Architecture](docs/ARCHITECTURE.md), [evaluation](docs/EVALUATION.md), and [release gates](docs/RELEASE-GATES.md).
- [Contributing](CONTRIBUTING.md), [security](SECURITY.md), [provenance](PROVENANCE.md), and [third-party notices](THIRD_PARTY_NOTICES.md).
