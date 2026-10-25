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

## Recent skill and generative-UI evidence

The following studies inform how to evaluate a skill; they are not results for Glasspring. The arXiv papers use different tasks, agents, and verifiers, so their effect sizes should not be transferred to this project.

- [SkillsBench](https://arxiv.org/abs/2602.12670) evaluated curated and self-generated skills across 11 domains and seven agent/model configurations. Curated skills improved average pass rate by 16.2 percentage points in the reported benchmark, but 16 of 84 evaluated tasks had negative deltas. Focused skills with two or three modules outperformed comprehensive documentation in that setup.
- [SWE-Skills-Bench](https://arxiv.org/abs/2603.15401) tested 49 skills on about 565 software-engineering task instances. 39 skills had zero pass-rate improvement and the average gain was 1.2%; some version-mismatched guidance reduced performance. This is a domain-specific result, not a general estimate for design skills.
- [Skill Coverage](https://arxiv.org/abs/2606.20659) found that the benchmark trajectories it analyzed covered only 38.66–45.51% of extracted skill constraints on average. A task score alone therefore cannot establish that a skill was discovered, invoked, or followed.
- [Design Theater](https://arxiv.org/abs/2607.22928) compared generated interfaces with their stated design rationales across 24 tasks and 120 interfaces. More than 25% of the rationales were not implemented, with a 34% failure rate for functional requirements. This supports checking design notes against rendered and interactive evidence.
- [UI-Bench](https://arxiv.org/abs/2508.20410) uses blinded expert pairwise judgments across 300 generated sites. It is a useful model for measuring visual preference separately from task completion, accessibility, and functional behavior.
- [OpenAI's skill-evaluation guide](https://developers.openai.com/blog/eval-skills) recommends checking whether the skill triggered, whether expected steps occurred, and whether outputs meet a small set of explicit criteria. That separation is relevant to this project's test design; it is not evidence of Glasspring's effectiveness.

These studies answer different questions. Screenshot reconstruction benchmarks assume a visual reference. Pairwise preference studies assess visual taste. Functional tasks test whether controls and flows work. A credible evaluation of glasspring must combine the evidence relevant to its claim and state its limits.

## Implications for this project

1. Treat the existing six briefs as a pilot. Create a separate, unseen brief set for a confirmatory comparison.
2. Keep no-skill and glasspring conditions matched for host, model revision, source assets, project state, time, and tool budget.
3. Ask independent human reviewers to compare anonymized outputs in randomized order. Automated or model based scores can supplement, but should not replace, those reviews.
4. Test visible behavior as well as screenshots: controls must produce the promised state changes, primary tasks must complete, and keyboard operation must work where required.
5. Report visual preference, task success, accessibility observations, elapsed time, failures, judge disagreement, and uncertainty separately. Do not award quality points merely for following glasspring's own rules.
6. For each run, record whether the host discovered and invoked the skill and whether its critical instructions were followed. If the host does not expose enough trace evidence to decide, report `UNKNOWN` rather than inferring compliance from the final page.
7. Compare each design-note claim with the rendered page, DOM, or interaction evidence. A rationale is not proof that the feature exists.

The current release gate remains blocked until an independent study with a genuinely separate task set is completed and its evidence is published.
