# Publication note

This repository's `main` branch is a **public source preview**, not a stable release. It is published as a sanitized root snapshot; earlier public history is held privately, and prior audit branch refs are preserved in local recovery bundles. No release tag or pull request accompanies this direct publication.

## Scope and evidence

The repository contains the skill, its standalone installer, token and contrast utilities, render checks, and automated regression tests. The automated checks show that these tools run; they do not establish that agent output is better than a baseline.

Validation of this publication snapshot is recorded by the current CI run and local test results. Before the sample payloads were excluded from the public tree, the latest full audit suite reported 12 PASS, 1 FAIL, 1 EXPECTED-NEGATIVE control, and 2 SKIP across 16 rows. The remaining failure was insufficient contrast in visible moving text. Two rows skipped because their external image host was unavailable. That suite is not bundled here and cannot be rerun from this repository.

No independent held-out efficacy experiment or fresh-host discovery/trigger study has been completed. Manual file-copy installation checks do not prove that a coding-agent host discovers or follows the skill.

## Rights and provenance

The root MIT license applies only to project-authored material that contributors may license. Third-party source tracing, excerpt review, and asset rights remain open; see [third-party notices](THIRD_PARTY_NOTICES.md) and [release gates](docs/RELEASE-GATES.md). Publication of this preview does not clear those questions or authorize reuse of omitted sample projects, images, fonts, or prompts.

## Before a stable release

- Complete the source-by-source rights and attribution review, including any adapted expression.
- Resolve the recorded contrast failure and rerun the complete visual and interaction suite with reproducible sample inputs.
- Run an independent held-out comparison against a no-skill baseline.
- Verify discovery and triggering in fresh supported host sessions.
- Keep private project inputs, prompts, screenshots, and identifying names out of the public repository unless their owners explicitly clear them.
