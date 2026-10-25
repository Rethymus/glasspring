# glasspring

A frontend design workflow for coding agents, with semantic tokens, domain references, contrast calculations and browser inspection helpers.

**Publication status: public source preview; no stable release.** The maintainer has published this audited snapshot for review. The current evidence supports working tools and selected rendered examples, but does not establish an independently measured improvement in design quality. Third-party provenance review remains open, so the project MIT license must not be treated as clearing third-party material. See [release gates](docs/RELEASE-GATES.md) and [third-party notices](THIRD_PARTY_NOTICES.md).

See the [publication note](PUBLICATION-NOTE.md) for test evidence and remaining release gates.

## Scope

Use glasspring when creating or deliberately restyling a responsive web interface. It helps an agent choose a direction, preserve an existing design system, derive tokens, measure supplied color pairs and inspect rendered output. Domain and style cards provide optional guidance; they are not proofs of product suitability.

The primary supported deliverable is a web preview plus tokens and design notes. Native and mini-program adapters remain experimental until tested in their actual runtimes. The project has no bundled REA engine, binary analysis capability, backend or deployment service.

## Install into a test project

From this repository, with Node.js available:

```sh
node skills/glasspring/scripts/install.mjs --target /absolute/path/to/project --host codex
node skills/glasspring/scripts/install.mjs --target /absolute/path/to/project --host claude
```

Codex uses `.agents/skills/glasspring`; Claude Code uses `.claude/skills/glasspring`. Restart the host and verify that the skill appears. A successful copy verifies the file layout, not host discovery or model behavior. See [INSTALL.md](INSTALL.md).

The installer requires an explicit destination. Existing installations are preserved unless `--replace` is supplied; replacement retains a sibling backup. `--dry-run` previews the copy without writing the destination. It does not register an MCP server or modify global configuration.

## Use

Ask the host to use glasspring to design a specific interface for a specific audience. Provide an existing brand or design system when available. For example:

> Use glasspring to design a responsive incident dashboard for on-call engineers. Keep the existing brand tokens. Prioritize reading and filtering logs, keyboard navigation, and a useful loading and error state.

Keep changes proportional: a small edit should not trigger an entire redesign. Browser review should test user outcomes, such as changed billing amounts or working filters, as well as visual states.

## Verification

Python tools use the standard library and sibling modules. The audited machine ran Windows, Python 3.12.4 and Node.js 22.14.0. Broader compatibility is not yet established by this audit.

```sh
python -m unittest discover -s tests -v
python skills/glasspring/scripts/doctor.py --selftest
python skills/glasspring/scripts/doctor.py --target /absolute/path/to/deliverable
python skills/glasspring/scripts/probe_render.py http://127.0.0.1:8000/preview.html
```

`doctor --selftest` checks tooling. The normal doctor checks static rules and output structure. It does not run every helper, certify user experience, establish screenshot freshness, or prove contrast pairs cover the actual page. Its screenshot selftest is offline unless `--live` is requested; the render-probe selftest can still launch a browser and use the network.

The output verifier and render-probe CLI use `0 = checks passed`, `1 = failure`, `2 = incomplete evidence`. The sample runner also exits 2 for skipped required samples or an empty suite. Doctor aggregates any nonzero child result as an unsuccessful check.

Screenshots need a Chromium-family browser. The render probe downloads axe-core 4.10.2 from cdnjs at runtime. Missing axe or click observations remain UNKNOWN, and a hollow render fails its precondition. These probes cover selected checks, not full WCAG conformance or complete interaction semantics.

The screenshot coverage check currently expects encoded narrow images at 320–600px and desktop images at least 1000px wide. Use the default screenshot scale factor of 1 for that contract. Image dimensions alone cannot establish CSS viewport identity or capture freshness. The multi-page check compares declared token names; it does not verify all computed token values.

## Evidence and limitations

Historical development runs contain self-assessed scores and some paired outputs. They were used to improve the skill and are not a held-out, blinded efficacy study. The README's original before/after showcase intentionally used a weak “before” page; it is a demonstration, not a no-skill control.

The audit reproduced false acceptance of invalid screenshot files, lost coverage states in MCP responses and a multi-page checker exception. Candidate fixes and independent regression cases are included. The source workspace and its historical artifacts are preserved separately; private target projects, screenshots, dependency trees and internal research are excluded from this repository.

## Relationship to REA

[REA](https://github.com/morluto/rea) inspired evidence-oriented investigation and skill/tool distribution. This project does not call REA or implement its analysis workflows. Audit comparison was pinned to commit `41cf869949b82bd0f24d425f6557432ae3a63545`; see [PROVENANCE.md](PROVENANCE.md).

## License

The project declares MIT only for project-authored material its contributors may license. That declaration does not establish redistribution rights for third-party prose, code, screenshots or assets. This public source preview does not close the open provenance review or clear third-party material for downstream redistribution. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
