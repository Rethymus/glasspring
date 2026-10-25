# glasspring

A frontend design skill and local review tools for coding agents.

glasspring guides an agent from a web brief to a responsive HTML preview, semantic CSS tokens, and design notes. Its local tools measure supplied color pairs, check output structure, capture screenshots, and inspect selected browser behavior.

> **Status: public source preview, not a stable release.** Selected tools have automated checks, but no independent study has shown that glasspring improves design or task outcomes. Third-party provenance review is also open. See the [publication note](PUBLICATION-NOTE.md) and [release gates](docs/RELEASE-GATES.md).

## What this project does

The skill routes a brief through product type, domain, platform, and technology references. It asks the agent to explore design directions, build a web preview, preserve or deliberately adapt an existing design system, and review the rendered result. The expected handoff is:

- `preview.html` — the responsive web preview.
- `tokens.css` — semantic design tokens used by that preview.
- `design-notes.md` — brief interpretation, choices, measured checks, and limitations.

The primary supported result is a preview and its design decisions. This repository does not promise production ready components in every framework, deployment, or native application code.

The bundled `SKILL.md` has a strong visual point of view: it uses an Apple inspired material and motion vocabulary and asks for a distinctive design choice. This is guidance, not an objective quality result. Use that point of view only where the brief and an existing design system leave room for it; translucent glass is optional and is prohibited in high trust or data dense areas.

## What is not included

- No automatic research, capture, indexing, or reverse engineering of external products. Domain and style cards are static project guidance; they do not contain complete source records or independently validated design findings.
- No bundled analysis engine, backend, or deployment service. The project does not call REA or implement its analysis workflow.
- No guarantee that a coding agent discovers or follows the skill. Copying files verifies the layout only.
- No claim of full accessibility conformance or measurable design improvement. Mechanical checks cover selected conditions and cannot judge whether an interface is useful.

The intended research to design workflow remains incomplete. The current implementation lacks a versioned product capture pipeline and evidence records that connect observations to design cards. See [maintainable scope](docs/ARCHITECTURE.md) and the [evaluation notes](docs/EVALUATION.md).

## Install into a test project

Clone this repository, then run the installer from its root. Use a disposable project directory for the first install.

```sh
git clone https://github.com/Rethymus/glasspring.git
cd glasspring
```

Install into a disposable project directory first. Use the path syntax for your shell:

```sh
# macOS or Linux
node skills/glasspring/scripts/install.mjs --target "/path/to/project" --host codex
```

```powershell
# Windows PowerShell
node skills/glasspring/scripts/install.mjs --target "C:\work\project" --host codex
```

For Claude Code, replace `codex` with `claude`. The installer copies the skill to `.agents/skills/glasspring` for Codex or `.claude/skills/glasspring` for Claude Code. It creates the target path if it is missing. Existing installations are preserved unless `--replace` is supplied; replacement keeps a sibling backup. `--dry-run` previews the copy. It does not register an MCP server or change global configuration.

Open a new host session in the target project, confirm the skill appears, and ask it to perform a small task. For example:

> Use glasspring to design a responsive incident dashboard for on call engineers. Keep the existing brand tokens. Make the severity filter and pause control work, and include useful loading and empty states.

File copy tests pass on Windows, macOS, and Linux in CI. Fresh host discovery and model behavior have not been verified. See [installation details](INSTALL.md) before using a host or operating system outside that evidence.

## Verify the tools

The current CI workflow runs these checks with Python 3.12 and Node.js 22 on Windows, macOS, and Linux:

```sh
python -m unittest discover -s tests -v
node skills/glasspring/scripts/install.mjs --selftest
python skills/glasspring/scripts/verify_output.py --selftest
python skills/glasspring/scripts/mcp_server.py --selftest
```

For an actual generated run, use `python skills/glasspring/scripts/doctor.py --target "PATH_TO_RUN"` to check static rules and output structure. Replace `PATH_TO_RUN` with the output directory using your shell's path syntax. It does not verify every interaction or establish design quality.

The screenshot and render probes require Chromium. `probe_render.py` needs a local page URL and downloads axe-core 4.10.2 from cdnjs when that check is available. Start a local server in one terminal and run the probe from this repository in another:

```sh
python -m http.server 8000 --directory "PATH_TO_RUN"
```

```sh
python skills/glasspring/scripts/probe_render.py http://127.0.0.1:8000/preview.html
```

Missing browser, axe, or click observations remain unknown or fail the relevant gate; they are not treated as passing. These selected probes do not establish full WCAG conformance, complete interaction behavior, or screenshot freshness.

## Evidence and open gates

The public [evaluation protocol](evals/protocol.json) is designed but has not been run. Its prompts are already public, so treat it as a pilot plan, not a hidden holdout set. A confirmatory comparison needs a new task set that was kept out of skill development, blinded independent review, and both visual and task outcome evidence. See [evaluation notes](docs/EVALUATION.md).

The last recorded full sample suite had one real contrast failure and two network dependent skips. Its sample payloads are not included here, so that run cannot be reproduced from this repository. The [release gates](docs/RELEASE-GATES.md) record the remaining status.

The root MIT license applies only to material the contributors have the right to license. It does not clear third-party prose, code, screenshots, or assets. Source by source provenance review remains open; see [third-party notices](THIRD_PARTY_NOTICES.md).

## Project map

| Path | Purpose |
|---|---|
| `skills/glasspring/SKILL.md` | Main agent workflow and file router |
| `skills/glasspring/references/` | Static domain, style, platform, type, and token guidance |
| `skills/glasspring/scripts/` | Installer, token and contrast tools, output checks, screenshot and browser probes |
| `skills/glasspring/assets/` | Notes template, rubric, and visual reference pages |
| `tests/` | Automated regression tests for selected failure boundaries |
| `evals/protocol.json` | Unexecuted comparison plan, not results |
| `docs/` | Architecture, evaluation, provenance, and release status |

## Background

[REA](https://github.com/morluto/rea) informed the project's interest in evidence oriented investigation and skill distribution. glasspring does not depend on REA; the comparison used commit `41cf869949b82bd0f24d425f6557432ae3a63545`. See [provenance](PROVENANCE.md).
