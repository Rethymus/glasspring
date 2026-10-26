# Third-party notices for the standalone skill

The MIT license in this directory applies only to project-authored material its contributors may license. It does not grant rights to third-party content.

- [shuding/liquid-glass](https://github.com/shuding/liquid-glass/tree/a2d2e847f793430e3409a52927af815a23f4d372) is cited as a refraction-technique reference. The project reports that no code from that repository is included; its upstream license is MIT at the pinned revision.
- [Anthropic's frontend-design skill](https://github.com/anthropics/skills/tree/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/frontend-design) is a cited source for design guidance; its pinned upstream `LICENSE.txt` is Apache-2.0. Retained wording and adaptations still need source comparison.
- [pbakaus/impeccable](https://github.com/pbakaus/impeccable/blob/9fa16a06d8957fde5687984629fd028c9f2abf10/.agents/skills/impeccable/SKILL.md) is explicitly attributed for one brief-priority rule in the core skill. Its `LICENSE` at that pinned commit is Apache-2.0. The retained expression and any adaptation still need comparison and rights review.
- [taste-skill](https://github.com/Leonxlnx/taste-skill/tree/6010f91a9935f1c167dfc500fb1a475681892e6b) is a source for direction and critique methodology; its pinned upstream license is MIT. Glasspring's bounded content-replacement prompt is an adaptation of the upstream skill's iteration note. The source's [test summary](https://github.com/Leonxlnx/taste-skill/blob/6010f91a9935f1c167dfc500fb1a475681892e6b/skills/taste-skill/references/research.md#L248-L273) describes six briefs, model jurors, one juror per brief per round, and reused briefs. This is not independent or human-user efficacy evidence. Retained wording and transformations still need a complete comparison and rights review.
- [Emil Kowalski's `animate` Skill](https://github.com/emilkowalski/skills/tree/2d228630ba1446365f614a108cb8252f1feda202/skills/animate) is the source for the frequency bands adapted in `references/motion.md` §0. The pinned repository license is MIT. The observed use is text guidance only; a full code/assets similarity audit is not complete. The bands are source-skill heuristics, not measured user thresholds. The notice below preserves the pinned source's MIT license text.
- XIAS and other design skills are named in some research notes. Their source revisions, licenses, and any adapted implementation have not been comprehensively checked.
- Domain references cite Baymard, NN/g and Stanford research. The skill summarizes selected findings and design implications; citations do not grant rights to republish source text or assets.
- Apple HIG and WWDC material is summarized as design guidance. Public availability is not permission to redistribute Apple text or assets; the project is not affiliated with Apple Inc.
- axe-core is fetched from cdnjs at probe runtime and is not bundled. The fetched artifact is pinned to sha256 b511cd9dec01c76f4b2ad1723b66b6db37d4c2eb4ed199076e1829d9ee7b75e3 (measured 2026-10-27 from the cdnjs 4.10.2 file); a mismatch skips the accessibility pass instead of running unverified code. axe-core is licensed MPL-2.0 by Deque Systems (verified against the npm registry, 2026-10-27). It is not redistributed in this repository and no MPL-covered files are bundled; runtime supply-chain policy: pinned version, pinned hash, honest skip on mismatch.
- Photos, fonts, and product screenshots from omitted sample projects are not part of this package and have not been cleared for redistribution.

This notice is not a complete provenance record or rights clearance. The repository clone contains a broader review in its root `THIRD_PARTY_NOTICES.md`; a standalone skill installation does not include that repository-level file.

### MIT license notice for the adapted `animate` guidance

The following notice is from the pinned `emilkowalski/skills` revision cited above:

```text
MIT License

Copyright (c) 2026 Emil Kowalski

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
