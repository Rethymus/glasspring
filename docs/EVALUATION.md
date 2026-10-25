# Evaluation status and research context

## Current status

No independent comparison of glasspring against a no-skill baseline has been run. The repository's [protocol](../evals/protocol.json) describes a small pilot: six briefs, three attempts per condition, and two conditions, for 36 output attempts. It fixes the host, model revision, brief, project, and time budget; it also calls for blinded review and functional outcome checks.

The prompts are published in this repository. They are therefore a public pilot set, not a hidden holdout. A confirmatory study needs new briefs that were kept out of skill development until generation is complete. If a fresh task set cannot be kept separate, report the result as exploratory.

The pilot is small. It can reveal large task specific effects and failure modes, but it cannot support broad claims across models, hosts, languages, or product domains. Publish all outputs and failures, report paired differences and uncertainty, and avoid collapsing visual preference, usability, and task completion into one score.

## What recent benchmarks contribute

- [UI-Bench](https://arxiv.org/abs/2508.20410) compares generated sites with blinded expert pairwise judgments across ten tools and thirty prompts, reporting calibrated uncertainty. It does not use automated image proxies as its primary measure in that setting. This supports pairwise review as one useful measure of visual quality; its scale is much larger than the glasspring pilot.
- [Design2Code](https://aclanthology.org/2025.naacl-long.199/) evaluates 484 real web pages using automatic visual metrics and human evaluation. It studies screenshot to code reconstruction, so its metrics do not directly measure whether an open ended design brief is useful.
- [DesignBench](https://arxiv.org/abs/2506.06251) evaluates generation, editing, and repair across HTML/CSS, React, Vue, and Angular. It highlights the value of testing more than initial page generation and separating results by task and framework. It is an arXiv benchmark paper, not evidence that glasspring works.
- [FrontCoder](https://aclanthology.org/2026.findings-acl.220/) reports that visual faithfulness and complex layouts remain difficult for base code models. It is a model training study; it does not test agent skills or prove a workflow benefit.

These studies answer different questions. Screenshot reconstruction benchmarks assume a visual reference. Pairwise preference studies assess visual taste. Functional tasks test whether controls and flows work. A credible evaluation of glasspring must combine the evidence relevant to its claim and state its limits.

## Implications for this project

1. Treat the existing six briefs as a pilot. Create a separate, unseen brief set for a confirmatory comparison.
2. Keep no-skill and glasspring conditions matched for host, model revision, source assets, project state, time, and tool budget.
3. Ask independent human reviewers to compare anonymized outputs in randomized order. Automated or model based scores can supplement, but should not replace, those reviews.
4. Test visible behavior as well as screenshots: controls must produce the promised state changes, primary tasks must complete, and keyboard operation must work where required.
5. Report visual preference, task success, accessibility observations, elapsed time, failures, judge disagreement, and uncertainty separately. Do not award quality points merely for following glasspring's own rules.

The current release gate remains blocked until an independent study with a genuinely separate task set is completed and its evidence is published.
