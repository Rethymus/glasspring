# glasspring

[English](README.md) | [简体中文](README.zh-CN.md)

Glasspring is a frontend design skill for coding agents, distributed as a folder. It guides an agent from a web brief to a responsive HTML preview, semantic CSS tokens, and design notes. Companion scripts check selected code and browser behavior.

> **Status as of 2026-10-25: public source preview; stable release is NO-GO.** File-copy checks pass, but fresh-host discovery, an independent efficacy study, and third-party rights clearance are not complete. See [release gates](docs/RELEASE-GATES.md).

## Product scope

Use Glasspring to explore a new responsive web page or dashboard, deliberately restyle an existing web interface, or review a generated preview. Existing project tokens and components remain the starting point unless the brief calls for a redesign.

Glasspring produces previews. It is not a production component library, deployment system, or automated external-product research and capture system. Its domain and style cards are static guidance, not a complete source catalog or independently validated design findings. Requests for native apps, games, and mini-programs receive web previews unless those platforms are separately implemented and tested.

The skill has an Apple-inspired visual bias. Follow it only where the brief and the existing design system leave room; translucent glass is optional and excluded from areas where trust is critical or data is dense.

## Expected output

- `preview.html` — responsive web preview.
- `tokens.css` — semantic tokens used by the preview.
- `design-notes.md` — brief interpretation, design choices, observed checks, and limitations.

## Install and try

Clone the repository and install into a disposable project first:

```sh
git clone https://github.com/Rethymus/glasspring.git
cd glasspring
node skills/glasspring/scripts/install.mjs --target "PATH_TO_PROJECT" --host codex
```

Replace `PATH_TO_PROJECT` with a path valid for your shell.

Use `--host claude` for the Claude Code directory layout. Installation copies files; it does not prove that a host discovers or follows the skill. Start a new session, confirm the skill is listed, and try a small task. See [installation details](INSTALL.md) for backups, dry runs, and the verified host matrix.

Example task:

> Use glasspring to design a responsive incident dashboard for incident response engineers. Keep the existing brand tokens, make the severity filter and pause control work, and include useful loading and empty states.

## Check the tools

The current CI workflow runs:

```sh
python -m unittest discover -s tests -v
node skills/glasspring/scripts/install.mjs --selftest
python skills/glasspring/scripts/verify_output.py --selftest
python skills/glasspring/scripts/mcp_server.py --selftest
```

For an actual generated run, use `python skills/glasspring/scripts/doctor.py --target "PATH_TO_RUN"`. Replace `PATH_TO_RUN` with the generated run directory. This checks selected static rules and output structure; it does not establish design quality or verify every interaction.

Browser probes require Chromium. `probe_render.py` uses a local page URL and fetches axe-core 4.10.2 from cdnjs when available. Missing browser, axe, or click observations stay `UNKNOWN` or fail the relevant gate; they are not counted as `PASS`. These checks do not establish full WCAG conformance.

```sh
# Terminal 1
python -m http.server 8000 --directory "PATH_TO_RUN"

# Terminal 2
python skills/glasspring/scripts/probe_render.py http://127.0.0.1:8000/preview.html
```

## Evidence and release gates

| Area | Recorded status |
|---|---|
| Installer layout and file copy checks | `PASS` in CI on Windows, macOS, and Linux as of 2026-10-25; host behavior is not covered |
| Last recorded full sample suite | `FAIL`: 12 `PASS`, 1 real contrast `FAIL`, 1 expected negative control, and 2 network dependent `SKIP` across 16 rows; aggregate exit code 1. Sample payloads are not included, so this run is not reproducible from this repository |
| Independent efficacy comparison | `NOT_RUN`; the public prompts are a pilot, not a hidden holdout |
| Fresh-host discovery and task behavior | `NOT_RUN` |
| Rights and attribution review | `BLOCKED` |

No claim of improved design quality, support for every agent, or full WCAG conformance is established. The root MIT license applies only to material contributors may license; it does not clear third-party prose, code, screenshots, or assets. See [evaluation notes](docs/EVALUATION.md), [release gates](docs/RELEASE-GATES.md), and [third-party notices](THIRD_PARTY_NOTICES.md).

## Repository map

| Path | Purpose |
|---|---|
| `skills/glasspring/SKILL.md` | Main workflow and reference router |
| `skills/glasspring/references/` | Static domain, style, platform, type, and token guidance |
| `skills/glasspring/scripts/` | Installer, selected checks, screenshots, and browser probes |
| `skills/glasspring/assets/` | Notes template, rubric, and visual references |
| `tests/` | Automated regressions for selected failure boundaries |
| `evals/protocol.json` | Unexecuted comparison protocol |
| `docs/` | Architecture, evaluation, provenance, and release status |

## License

See [LICENSE](LICENSE) and [third-party notices](THIRD_PARTY_NOTICES.md). The MIT file does not grant rights to material the contributors cannot license.
