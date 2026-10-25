# glasspring

[English](README.md) | [简体中文](README.zh-CN.md)

**A workflow skill for coding agents that build or review responsive web interfaces.**

Glasspring guides an agent through a new web preview, a restyle, a small edit, or a review. The repository packages one skill entrypoint, static design reference cards, and local or browser checks that report limited observations. The references do not automatically inspect live products, and the repository has no versioned product-capture and research-validation pipeline.

> **Current status as of 2026-10-25: public source preview; stable release is NO-GO.** Host task behavior and independent efficacy remain unverified, the privacy review is partial, and third-party rights are blocked. See [release gates](docs/RELEASE-GATES.md).

## What Glasspring does

| Task | Workflow and deliverable |
|---|---|
| New preview | Create `tokens.css`, `preview.html`, and `design-notes.md`. |
| Full restyle | Work in the existing app and token entrypoint; provide before/after evidence and design notes. |
| Small edit | Preserve the existing system and check only the changed surface. |
| Review only | Report findings and evidence without editing project files. |

The user’s brief and existing design system take precedence. Glass and other style choices are optional. Native app, game, and mini-program requests produce web previews unless that platform is separately implemented and tested.

## Coffee storefront example

The repository includes a fictional storefront illustration inspired by the public coffee-shop pilot brief in [the evaluation protocol](evals/protocol.json). That brief refers to a supplied brand palette, but the palette is not included in the repository. These local Chromium screenshots show an illustration, **not** a reproducible evaluation input or output from a Glasspring agent run. They do not demonstrate improved design quality, skill discovery, or task success.

![Full-page desktop screenshot of the illustrative Morrow Coffee storefront](examples/coffee-storefront/assets/preview-desktop.png)

<details>
<summary>Mobile layout and local bag interaction</summary>

<p><img src="examples/coffee-storefront/assets/preview-mobile.png" width="320" alt="Full-page mobile screenshot of the illustrative Morrow Coffee storefront"></p>
<p><img src="examples/coffee-storefront/assets/preview-bag-open.png" width="100%" alt="The demo bag open with House Blend and an 18 dollar subtotal"></p>
</details>

The brand, products, copy, and prices are fictional. The bag changes local page state only; it does not place orders or collect payment. Run the page from the repository root:

~~~sh
python -m http.server 8000 --directory examples/coffee-storefront
~~~

Open `http://127.0.0.1:8000/`. See the [example notes](examples/coffee-storefront/README.md) for its source and evidence boundaries.

## Install and try the skill

Clone the repository and install into a disposable project:

~~~sh
git clone https://github.com/Rethymus/glasspring.git
cd glasspring
node skills/glasspring/scripts/install.mjs --target "PATH_TO_PROJECT" --host codex
~~~

Replace `PATH_TO_PROJECT` with a path valid for your shell. Use `--host claude` for the Claude Code directory layout. The installer copies files; it does not prove that a host discovers or follows the skill. Start a fresh host session, check that Glasspring is listed, then try a small task. See [installation details](INSTALL.md) for backups, dry runs, and the observed host matrix.

Example task:

> Use Glasspring to design a responsive incident dashboard for on-call engineers. Keep the existing brand tokens, make the severity filter and pause control work, and include useful loading and empty states.

The optional MCP server requires manual host configuration. Its self-test covers a local stdio handshake; production host integration has not been verified.

## Checks you can run

The current CI workflow runs:

~~~sh
python -m unittest discover -s tests -v
node skills/glasspring/scripts/install.mjs --selftest
python skills/glasspring/scripts/verify_output.py --selftest
python skills/glasspring/scripts/mcp_server.py --selftest
~~~

For a generated run directory, `python skills/glasspring/scripts/doctor.py --target "PATH_TO_RUN"` checks selected static rules and output structure. It does not establish design quality or verify every interaction.

Browser probes require Chromium. `probe_render.py` uses a local page URL and fetches axe-core 4.10.2 from cdnjs when available. Missing browser, axe, or click observations stay `UNKNOWN` or fail the relevant gate; they are not `PASS`. The probes do not establish full WCAG conformance.

~~~sh
# Terminal 1
python -m http.server 8000 --directory "PATH_TO_RUN"

# Terminal 2
python skills/glasspring/scripts/probe_render.py http://127.0.0.1:8000/preview.html
~~~

## Evidence and release status

| Area | Status and evidence |
|---|---|
| Mechanical CI on the published main snapshot | `PASS` on Windows, macOS, and Ubuntu on 2026-10-25. See the [run](https://github.com/Rethymus/glasspring/actions/runs/40198893762). This does not test a coding-agent host. |
| Last recorded full sample suite | `FAIL`: 12 `PASS`, 1 real contrast `FAIL`, 1 expected negative control, and 2 network-dependent `SKIP` across 16 rows; exit code 1. The sample pages are not in this repository, so replay is `INSUFFICIENT_EVIDENCE`. |
| Fresh-session host behavior | `PARTIAL`: one Codex session listed skill metadata (`PASS`); installed-file reading and task behavior are `UNKNOWN`; Claude Code discovery and task behavior are `NOT_RUN`. |
| Independent efficacy comparison | `NOT_RUN`: the public prompts are a pilot, not a hidden holdout. Two tasks also refer to missing source inputs, so replay is `INSUFFICIENT_EVIDENCE`. |
| First-party privacy review | `PARTIAL`: the heuristic scan found no common secret patterns in the initial source snapshot; the demo was reviewed separately. No complete binary, history, or dedicated secret-scanner review was run. |
| Third-party rights and attribution | `BLOCKED`: per-file origins, license obligations, and authority to license remain unresolved. |
| Runtime dependency integrity | `OPEN`: browser checks fetch axe-core from a public CDN; checksum and offline policy are unresolved. |

No evidence currently supports claims of improved design quality, compatibility with every agent, or full WCAG conformance. The root MIT license does not clear third-party prose, code, screenshots, or assets. See [evaluation notes](docs/EVALUATION.md), [provenance](PROVENANCE.md), [third-party notices](THIRD_PARTY_NOTICES.md), and [security and privacy](SECURITY.md).

## Security and repository map

The tools run with the host user’s filesystem and process permissions; the skill’s scope instructions are not a sandbox. Browser probes execute the supplied page code, and MCP path arguments are not restricted to a configured workspace. Review [security and privacy](SECURITY.md) before use.

| Path | Purpose |
|---|---|
| `skills/glasspring/SKILL.md` | Main workflow and reference router |
| `skills/glasspring/references/` | Static design guidance for domains, styles, platforms, types, and tokens |
| `skills/glasspring/scripts/` | Installer, selected checks, screenshots, and browser probes |
| `skills/glasspring/assets/` | Notes template, rubric, and visual references |
| `examples/coffee-storefront/` | Fictional local storefront example and screenshots |
| `tests/` | Automated regressions for selected failure boundaries |
| `evals/protocol.json` | Unexecuted pilot comparison protocol |
| `docs/` | Architecture, evaluation, and release evidence |

## License

See [LICENSE](LICENSE) and [third-party notices](THIRD_PARTY_NOTICES.md). The MIT license applies only to material contributors may license.
