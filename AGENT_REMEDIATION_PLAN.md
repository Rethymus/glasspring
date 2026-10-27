# Agent Remediation Plan — versioned baseline (v2, 2026-10-27)

> The previous remediation plan was never committed to this repository
> (verified 2026-10-27 against every object in the full git history), so
> remediation status was `INSUFFICIENT_EVIDENCE`. This file is the new
> trackable baseline. Status vocabulary matches `docs/RELEASE-GATES.md`:
> PASS / FAIL / INCOMPLETE / NOT_RUN / UNKNOWN / BLOCKED / CLOSED.
> Update the tables in place; do not fork new plan files.

## Verified baseline (2026-10-27)

| Check | Status | Evidence |
|---|---|---|
| Unit suite (26 tests, three OS) | PASS | CI rollup SUCCESS on `196b563` (runs 40323454863 / 40323445013); local reruns ×2 |
| Output contract on the public example | PASS | `verify_output.py examples/coffee-storefront`: 0 FAIL / 0 UNKNOWN / 6 PASS (local rerun) |
| Style scan on the public example | PASS | `slop_scan.py`: 0 hard / 0 warn / 0 info (local rerun) |
| Tool selftests (installer, contract, MCP, probe) | PASS | local rerun on `196b563` tree |
| README consistency (EN/ZH, links, triggers) | PASS | PR #3 merged at `92c4975`; use-when section added in `f4e51d3` |
| axe-core runtime integrity | CLOSED | sha256 pin `b511cd9d…7b75e3` verified before running; mismatch skips pass D (`196b563`) |

## P0 — release blockers (must close before stable release)

| id | item | status | exit criteria |
|---|---|---|---|
| P0-1 | Rights review of retained third-party material | TRIAGED 2026-10-27: 8/9 rows CLOSED with evidence (docs/P0-1-TRIAGE-2026-10-27.md); XIAS upstream license fetched and pinned MIT; only narrow open item is the Apple HIG verbatim spot-check (host unreachable this session) | remaining: Apple spot-check, human sign-off on the triage record |
| P0-2 | Runtime dependency integrity | CLOSED for axe-core | re-audit whenever any new runtime fetch is added |

### P0-1 rights inventory and triage

Rows mirror `THIRD_PARTY_NOTICES.md`. For each: compare retained wording
against the pinned source, then either keep with the pinned notice or remove.

| source | pinned license | retained material | action |
|---|---|---|---|
| anthropics/skills frontend-design | Apache-2.0 (pinned) | cited design-guidance source; wording retained | diff wording vs source; keep-with-notice or rephrase |
| pbakaus/impeccable | Apache-2.0 (pinned) | one brief-priority rule in core skill | same |
| Leonxlnx/taste-skill | MIT (pinned) | direction/critique methodology; bounded content-replacement prompt adaptation | same |
| emilkowalski/skills `animate` | MIT (pinned) | frequency bands adapted in `references/motion.md` §0; MIT notice already embedded | diff bands wording vs source |
| XIAS and other named skills | unverified | names in research notes only | confirm no code/text retained; else pin license |
| Baymard / NN/g / Stanford | citation only | summarized findings, no source text | confirm no verbatim passages |
| Apple HIG / WWDC | summarized | paraphrased guidance (no Apple text/assets) | confirm paraphrase completeness |
| axe-core 4.10.2 | MPL-2.0 | runtime fetch only, sha256-pinned, not bundled | CLOSED — no MPL-covered files redistributed |
| omitted sample assets (photos/fonts/screenshots) | n/a | not part of the package | CLOSED — absent from tree |

## P1 — evidence completion (before any efficacy claim)

| id | item | status | exit criteria |
|---|---|---|---|
| P1-1 | Fresh-session host tests: discovery, invocation, following, boundary — separately per host | **Claude PASS** (2026-10-27: discovery + invocation + following + boundary, incl. 3-file routing budget held and honest disclosure of a permission-blocked helper; see docs/HOSTTEST-2026-10-27.md). Codex discovery indicator positive; task behavior account-blocked (`model_not_found` for ChatGPT-account Codex) — UNKNOWN | one recorded session per host with transcript + task output retained; Codex task run still owed once model access works |
| P1-2 | Confirmatory comparison on unseen holdout briefs (6×2×3, blind pairwise, distinctiveness scored separately, token/time recorded, all failures published) | NOT_RUN | results published per host/model with uncertainty; follow the seven implementation requirements in `docs/EVALUATION.md` |
| P1-3 | Cost observability (elapsed time and cost line in design notes §6) | NOT_RUN | template updated and used in the next generated run |

## P2 — distribution and maintenance (after P0-1 closes)

| id | item | status |
|---|---|---|
| P2-1 | skills.sh listing (`npx skills add Rethymus/glasspring`) | NOT_RUN |
| P2-2 | agentskillshub submission (third-party rating + security scan + ranking harness) | NOT_RUN |
| P2-3 | AGENTS.md / CLAUDE.md host pointers at repository root | NOT_RUN |
| P2-4 | installer prints the source commit for reproducible installs | NOT_RUN |
| P2-5 | quarterly ecosystem rescan and citation freshness review | recurring |
