# Release gates

Status: **Public source preview published; NO-GO for a stable release**. The public preview is on `main` in [Rethymus/glasspring](https://github.com/Rethymus/glasspring). Its initial sanitized snapshot was published directly, without a contemporaneous pull request or release tag. No stable-release claim has been made.

| Gate | State | Evidence or closure requirement |
|---|---|---|
| Recoverable private source baseline | PASS | Complete archive, per-file SHA-256 manifest, archive CRC verification; original path excluded from public tree |
| Baseline source tests | PASS, bounded | Existing tool selftests passed on the audited Windows environment; this does not establish gate completeness |
| False-success regressions | PASS, bounded | 22 independent regression tests on candidate; original failures retained separately |
| Selected live browser checks | PASS, bounded | Multi-page sample: four pages at 390 and 1440, axe and click observations present; screenshot/DOM UX findings remain recorded |
| Full current sample suite | FAIL / INCOMPLETE | 12 PASS, 1 real color-contrast failure, 1 exact expected-negative control, and 2 SKIP across 16 rows; exit 1. The Kumo render-volume check now sees composed text; probe waits for DOM readiness; hidden responsive controls are excluded; controlled panels are observed. Both skips are remote-image checks blocked by `picsum.photos`; the contrast finding is not exempted |
| Dependency reproducibility | PASS, bounded | Three existing sample lockfiles installed with scripts disabled and built; official npm advisory audit reported zero known advisories |
| First-party privacy scan | PARTIAL | A follow-up scan removed internal sample identifiers and findings from the public skill tree; private screenshots and sample payloads are excluded. A 2026-10-25 heuristic scan found no common API-key, private-key, GitHub-token, AWS-key, or local absolute-path patterns in 78 tracked text files. No dedicated secret scanner or complete binary/history review was run; comprehensive asset review remains needed. |
| Rights and attribution | BLOCKED | Per-file origins, upstream license obligations and author authority unresolved. A 2026-10-25 source scan still found high-specificity research and competitor attributions in retained cards without claim-by-claim source revisions; see [PROVENANCE.md](../PROVENANCE.md) and [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md). |
| Independent efficacy | BLOCKED | No independent comparison has been run. The six prompts in evals/protocol.json are public pilot prompts, not a hidden holdout; a confirmatory study needs a separate task set, independent human judges, task outcomes, and uncertainty reporting. See docs/EVALUATION.md |
| Actual host compatibility | BLOCKED | Automated Codex and Claude directory-layout and file-copy checks pass on Windows, macOS, and Linux in CI. One isolated fresh Codex session listed skill metadata (`PASS`), but a local execution policy blocked reading the installed file, so invocation/task behavior is `UNKNOWN`. A Claude Code fresh session is `NOT_RUN`. This is insufficient to establish host compatibility. See INSTALL.md |
| Runtime dependency integrity | OPEN | Browser and fetched axe source are external dependencies; checksum/pinning and offline coverage policy need a decision |
| Public repository setup | PASS, bounded | Public `main` exists; GitHub private vulnerability reporting is enabled. This is repository setup only, not a stable-release approval. |

Before release, attach immutable evidence for each supported host/OS and each required evaluation. Report unsupported combinations as unsupported. A smaller prerelease may omit experimental adapters or extra examples, but must state its reduced scope and resolve rights for everything it still distributes.

Allowed claims today: “bundled design workflow and tools”, “tested on the stated Windows environment”, “selected sample behaviors observed”. Disallowed claims today: “works with every agent”, “all UX gates pass”, “proven better design”, “independent experiment count validated”, “fully WCAG compliant”, or “REA-powered research pipeline”.
