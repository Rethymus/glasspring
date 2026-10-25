# Publication note

This repository's `main` branch is a **public source preview**, not a stable release. The preview was initially published as a sanitized root snapshot; earlier public history is held privately, and prior audit branch refs are preserved in local recovery bundles. That initial publication was direct, without a contemporaneous pull request or release tag.

## Scope and evidence

The repository contains the skill, its standalone installer, token and contrast utilities, render checks, and automated regression tests. The automated checks show that these tools run; they do not establish that agent output is better than a baseline.

Validation of the published source snapshot is recorded by [CI on commit `28adce6`](https://github.com/Rethymus/glasspring/actions/runs/40159018216) and local test results. Its Windows, macOS, and Ubuntu jobs passed the unit and installer layout checks with Python 3.12 and Node.js 22. Before the sample payloads were excluded from the public tree, the latest full audit suite reported 12 PASS, 1 FAIL, 1 EXPECTED-NEGATIVE control, and 2 SKIP across 16 rows. The remaining failure was insufficient contrast in visible moving text. Two rows skipped because their external image host was unavailable. That suite is not bundled here and cannot be rerun from this repository.

No independent comparison or fresh-host discovery/trigger study has been completed. The six prompts in `evals/protocol.json` are public and should be treated as a pilot, not a hidden holdout. A confirmatory study needs a separate task set kept out of skill development, blinded independent human review, functional outcomes, and uncertainty reporting. Manual file-copy installation checks do not prove that a coding-agent host discovers or follows the skill. See [evaluation notes](docs/EVALUATION.md).

## Rights and provenance

The root MIT license applies only to project-authored material that contributors may license. Third-party source tracing, excerpt review, and asset rights remain open; see [third-party notices](THIRD_PARTY_NOTICES.md) and [release gates](docs/RELEASE-GATES.md). Publication of this preview does not clear those questions or authorize reuse of omitted sample projects, images, fonts, or prompts.

## Before a stable release

- Complete the source-by-source rights and attribution review, including any adapted expression.
- Resolve the recorded contrast failure and rerun the complete visual and interaction suite with reproducible sample inputs.
- Run a confirmatory comparison against a no-skill baseline with a separate task set, independent human review, functional outcomes, and published uncertainty.
- Verify discovery and triggering in fresh supported host sessions.
- Keep private project inputs, prompts, screenshots, and identifying names out of the public repository unless their owners explicitly clear them.
