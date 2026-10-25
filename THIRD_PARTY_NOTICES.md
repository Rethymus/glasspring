# Third-party review — unresolved

This is a review ledger, not a completed license clearance. A URL citation is not a redistribution license. The project's MIT declaration applies only to material its authors may license.

| Source / component | Observed role | License evidence | Outstanding action |
|---|---|---|---|
| glasspring project | Local code, templates and references | Existing MIT file, copyright “glasspring contributors” | Maintainer must confirm authorship and authority to license retained material |
| morluto/rea | Method and distribution reference | MIT at pinned revision | No imported REA implementation was found; preserve upstream notices if code is later imported |
| shuding/liquid-glass | Refraction technique cited by the skill; no upstream code import identified | Upstream repository is MIT at pinned revision `a2d2e847f793430e3409a52927af815a23f4d372` | Keep the attribution; verify any future code or asset import separately |
| anthropics/skills frontend-design | Source-attributed rules and prose | Upstream skill LICENSE.txt is Apache-2.0 | Compare retained prose to pinned upstream, record copied or adapted portions and supply required notices/license if applicable |
| Leonxlnx/taste-skill | Direction and critique methodology | Upstream LICENSE is MIT | Trace retained wording and transformations; preserve notices for copied substantial portions |
| XIAS and other design skills | Probe methods and design rules mentioned by source comments | Not comprehensively verified | Pin each source, diff any borrowed implementation and preserve its actual license and notices |
| Apple HIG / WWDC; NN/g; Baymard | Research and reference claims | Public availability does not establish permission to republish text/assets | Replace long reproductions with original summaries, inspect terms and mark approximations explicitly |
| axe-core 4.10.2 via cdnjs | Downloaded at probe runtime; not bundled | No complete dependency notice review performed | Record upstream license and runtime supply-chain policy; checksum/cache design remains open |
| Demo photographs, fonts and product screenshots | Excluded with private examples from this candidate | Not cleared by this audit | Require per-asset provenance, redistribution permission and private-data review before adding examples |

References for verified upstream license files:

- [REA MIT license](https://github.com/morluto/rea/blob/41cf869949b82bd0f24d425f6557432ae3a63545/LICENSE).
- [shuding/liquid-glass MIT license](https://github.com/shuding/liquid-glass/blob/a2d2e847f793430e3409a52927af815a23f4d372/LICENSE).
- [Anthropic frontend-design license](https://github.com/anthropics/skills/blob/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/frontend-design/LICENSE.txt).
- [taste-skill license](https://github.com/Leonxlnx/taste-skill/blob/6010f91a9935f1c167dfc500fb1a475681892e6b/LICENSE).

The standalone skill package includes its own copy of the project MIT license and a scoped notice at [`skills/glasspring/THIRD_PARTY_NOTICES.md`](skills/glasspring/THIRD_PARTY_NOTICES.md). The project describes its glass recipe pages as authored examples; this audit did not independently compare every line against upstream sources. The project is not affiliated with Apple Inc.; “Apple-inspired” describes a design language and does not imply Apple endorsement.

Do not publish a badge claiming all third-party material is MIT. Do not infer that avoiding exact hex values clears rights in copied expression or assets. This audit records observed licensing evidence and gaps; unresolved rows block a rights-cleared stable release. The maintainer's decision to publish this source preview does not close those gaps or clear downstream redistribution.
