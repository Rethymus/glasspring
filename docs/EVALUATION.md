# Evaluation status and research context

## Current status

No independent comparison of glasspring against a no-skill baseline has been run. The repository's [protocol](../evals/protocol.json) describes a small pilot: six briefs, three attempts per condition, and two conditions, for 36 output attempts. It fixes the host, model revision, brief, project, and time budget; it also calls for blinded review and functional outcome checks.

The prompts are published in this repository. They are therefore a public pilot set, not a hidden holdout. A confirmatory study needs new briefs that were kept out of skill development until generation is complete. If a fresh task set cannot be kept separate, report the result as exploratory.

The pilot is small. It can reveal large task specific effects and failure modes, but it cannot support broad claims across models, hosts, languages, or product domains. Publish all outputs and failures, report paired differences and uncertainty, and avoid collapsing visual preference, usability, and task completion into one score.

The public protocol is also incomplete as a runnable task set: the coffee task refers to a supplied brand palette and the existing-project task refers to a supplied component library, but `evals/protocol.json` is the only tracked file under `evals/`. Those inputs are absent. Keep the current protocol unchanged; recover and record the intended inputs, or revise and version the briefs before any generation. Until then, reproducing those tasks is `INSUFFICIENT_EVIDENCE`.

## What recent benchmarks contribute

- [UI-Bench](https://arxiv.org/abs/2508.20410) compares ten tools across 30 prompts, producing 300 generated sites and more than 4,000 expert pairwise judgments with calibrated uncertainty. It does not use automated image proxies as its primary measure in that setting. This supports pairwise review as one useful measure of visual quality; its scale is much larger than the glasspring pilot.
- [Design2Code](https://aclanthology.org/2025.naacl-long.199/) evaluates 484 real web pages using automatic visual metrics and human evaluation. It studies screenshot to code reconstruction, so its metrics do not directly measure whether an open ended design brief is useful.
- [DesignBench](https://arxiv.org/abs/2506.06251) evaluates generation, editing, and repair across HTML/CSS, React, Vue, and Angular. It highlights the value of testing more than initial page generation and separating results by task and framework. It is an arXiv benchmark paper, not evidence that glasspring works.
- [FrontCoder](https://aclanthology.org/2026.findings-acl.220/) reports that visual faithfulness and complex layouts remain difficult for base code models. It is a model training study; it does not test agent skills or prove a workflow benefit.

## Recent skill and generative-UI evidence

The following studies inform how to evaluate a skill; they are not results for Glasspring. They use different tasks, agents, and verifiers, so their effect sizes should not be transferred to this project. Their results differ: curated skills help in one broad benchmark, while public web-development skills often hurt or add cost in another.

- [SkillsBench 1.1](https://arxiv.org/abs/2602.12670) evaluates 87 tasks across eight domains over 18 model-harness configurations. Its latest aggregate reports an increase in mean pass rate from 33.9% to 50.5% (+16.6 percentage points), with configuration-level gains from +4.1 to +25.7 points. The authors report that focused skills with at most three modules outperform larger bundles in this benchmark. These are curated skills on expertise-heavy tasks, not web-design results.
- [SWE-Skills-Bench](https://arxiv.org/abs/2603.15401) tested 49 skills on about 565 software-engineering task instances. 39 skills had zero pass-rate improvement and the average gain was 1.2%; some version-mismatched guidance reduced performance. This is a domain-specific result, not a general estimate for design skills.
- [WebDev-Skills-Bench](https://arxiv.org/abs/2608.23067) is an arXiv preprint submitted on 24 August 2026. It evaluates 31 public web-development skills on 50 projects and 1,000 ordered tasks using four matched conditions, including no-skill and length-matched irrelevant-skill controls. Across four models, target-skill injection lowered mean Pass@2 by 1.3–4.2 percentage points and increased token use by 72–394%; only 17–36% of skill/project pairs gained. The result concerns code-task completion in that setup, not visual quality or all design skills.
- [Asuka-Bench](https://arxiv.org/abs/2606.05920) is an arXiv preprint under review. It evaluates 50 web tasks with 784 criteria and 2,402 expected outcomes using browser-grounded tests and up to three feedback rounds. The strongest reported model completes only 52% of projects after three rounds. It does not test whether a skill helps; it shows why rendered behavior and repair from feedback should be measured separately from one-shot appearance.
- [Skill Coverage](https://arxiv.org/abs/2606.20659) found that the benchmark trajectories it analyzed covered only 38.66–45.51% of extracted skill constraints on average. A task score alone therefore cannot establish that a skill was discovered, invoked, or followed.
- [Design Theater](https://arxiv.org/abs/2607.22928) compared generated interfaces with their stated design rationales across 24 tasks and 120 interfaces. More than 25% of the rationales were not implemented, with a 34% failure rate for functional requirements. This supports checking design notes against rendered and interactive evidence.
- [OpenAI's skill-evaluation guide](https://developers.openai.com/blog/eval-skills) recommends checking whether the skill triggered, whether expected steps occurred, and whether outputs meet a small set of explicit criteria. That separation is relevant to this project's test design; it is not evidence of Glasspring's effectiveness.

These studies answer different questions. Screenshot reconstruction benchmarks assume a visual reference. Pairwise preference studies assess visual taste. Functional tasks test whether controls and flows work. A credible evaluation of glasspring must combine the evidence relevant to its claim and state its limits.

## Recent related work outside efficacy benchmarks

- [WebXSkill](https://aclanthology.org/2026.findings-emnlp.561/) is a Findings of EMNLP 2026 paper about autonomous browser agents. It pairs parameterized action programs with step-level natural-language guidance, organizes skills for URL-based retrieval, and reports results on WebArena, WebVoyager, and Online-Mind2Web. Its executable browser-workflow architecture differs from Glasspring's coding-agent instructions and local checks; its results do not transfer as evidence of Glasspring efficacy.
- [Skill Constellations](https://arxiv.org/abs/2610.11169) is an October 2026 arXiv preprint that traces skill-copy relationships through Git history. It reports that copied skills rarely change with their source and recommends versioned references to improve provenance and fix propagation. This is supply-chain research, not an efficacy result. **Inference for this repository:** recording the checked-out commit makes a copied installation more reproducible, but does not prove the installed host loaded or followed it.

## Implications for this project

1. Treat the existing six briefs as a pilot. Create a separate, unseen brief set for a confirmatory comparison.
2. Keep no-skill and Glasspring conditions matched for host, model revision, brief, project state, time, and tool budget. If the study aims to separate content effects from prompt-length effects, add a length-matched irrelevant-skill condition.
3. Evaluate routing per host, model, task, and project. Record whether the skill was discovered, invoked, and followed; do not assume a result transfers across models or task types.
4. Ask independent human reviewers to compare anonymized outputs in randomized order. Automated or model-based scores can supplement, but should not replace, those reviews.
5. Test visible behavior as well as screenshots: controls must produce the promised state changes, primary tasks must complete, and keyboard operation must work where required. Include a feedback-and-repair round when users would normally refine the brief after seeing a preview.
6. Report visual preference, task success, accessibility observations, elapsed time, token use, failures, judge disagreement, and uncertainty separately. Do not award quality points merely for following Glasspring's own rules.
7. Compare each design-note claim with the rendered page, DOM, or interaction evidence. A rationale is not proof that the feature exists.

The current release gate remains blocked until an independent study with a genuinely separate task set is completed and its evidence is published.
