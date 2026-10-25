# Release gates

Status: **Public source preview published; NO-GO for a stable release**. The public repository is [Rethymus/glasspring](https://github.com/Rethymus/glasspring), with `main` as its only branch. No pull request, release tag, package-registry publication, or stable-release claim has been made.

| Gate | State | Evidence or closure requirement |
|---|---|---|
| Recoverable private source baseline | PASS | Complete archive, per-file SHA-256 manifest, archive CRC verification; original path excluded from public tree |
| Baseline source tests | PASS, bounded | Existing tool selftests passed on the audited Windows environment; this does not establish gate completeness |
| False-success regressions | PASS, bounded | 22 independent regression tests on candidate; original failures retained separately |
| Selected live browser checks | PASS, bounded | Multi-page sample: four pages at 390 and 1440, axe and click observations present; screenshot/DOM UX findings remain recorded |
| Full current sample suite | FAIL / INCOMPLETE | 12 PASS, 1 real color-contrast failure, 1 exact expected-negative control, and 2 SKIP across 16 rows; exit 1. The Kumo render-volume check now sees composed text; probe waits for DOM readiness; hidden responsive controls are excluded; controlled panels are observed. Both skips are remote-image checks blocked by `picsum.photos`; the contrast finding is not exempted |
| Dependency reproducibility | PASS, bounded | Three existing sample lockfiles installed with scripts disabled and built; official npm advisory audit reported zero known advisories |
| First-party privacy scan | PARTIAL | A follow-up scan removed internal sample identifiers and findings from the public skill tree; private screenshots and sample payloads are excluded. Comprehensive asset review remains needed. |
| Rights and attribution | BLOCKED | Per-file origins, upstream license obligations and author authority unresolved |
| Independent efficacy | BLOCKED | Historical scores are not blinded held-out results; execute evals/protocol.json with independent runs |
| Actual host compatibility | BLOCKED | Codex and Claude directory layouts tested with temporary projects; fresh agent sessions and supported OS matrix not executed |
| Runtime dependency integrity | OPEN | Browser and fetched axe source are external dependencies; checksum/pinning and offline coverage policy need a decision |
| Public repository setup | PASS, bounded | Public `main` exists; GitHub private vulnerability reporting is enabled. This is repository setup only, not a stable-release approval. |

Before release, attach immutable evidence for each supported host/OS and each required evaluation. Report unsupported combinations as unsupported. A smaller prerelease may omit experimental adapters or extra examples, but must state its reduced scope and resolve rights for everything it still distributes.

Allowed claims today: “bundled design workflow and tools”, “tested on the stated Windows environment”, “selected sample behaviors observed”. Disallowed claims today: “works with every agent”, “all UX gates pass”, “proven better design”, “independent experiment count validated”, “fully WCAG compliant”, or “REA-powered research pipeline”.
