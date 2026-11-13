# Triage of the April 2026 critical-review issues (epic #1937 and children)

Prepared for issue #1961. Status: **draft for the author's decision.** Nothing in this document cuts, merges, removes or renumbers a chapter. Evidence is taken from the manuscript on branch `claude/laughing-curie-k3kwvs` (13 November 2026), compared with the line counts and line ranges the issues assumed on 16 April 2026.

## Why the structural proposals are on hold

The epic proposes to remove or merge Chapters 9B, 9C, 14, 17/18/19, 21 and 23. Since April the book has become Book 1 of *The Transformed Architecture*. Later volumes cite this book by chapter number ("*Architecture as Code* (Chapter N)"), and the companion *Tools* inventories its artefacts by chapter. `CLAUDE.md` states that chapter numbers are fixed across the series. A merge or removal therefore changes text in other repositories and cannot be decided in this one alone. The recommendation for every structural item is **author decision required**; the only structural step this triage proposes is the non-breaking one: keep the chapter numbers and shorten or reorganise content inside a chapter.

## Line counts: assumed in April against the manuscript now

The manuscript did not shrink; it grew, mostly through the fact-check and consolidation work of October and November.

| File | Assumed in the issue | Now | Comment |
|---|---|---|---|
| `01_introduction.md` | 98 | 106 | |
| `02_fundamental_principles.md` | 604 | 661 | Requirements as Code still about 275 lines inside Chapter 2 |
| `04_adr.md` | 295 | 299 | |
| `05_automation_devops_cicd.md` | 593 | 604 | |
| `06_structurizr.md` | 1,278 | 1,304 | |
| `07_containerisation.md` | 311 | 317 | |
| `08_microservices.md` | 218 | 233 | |
| `09_security_fundamentals.md` | 295 | 196 | reduced by #1951 and the fact-check |
| `09b_security_patterns.md` | 647 | 622 | |
| `09c_risk_and_threat_as_code.md` | 91 | 92 | |
| `12_compliance.md` | 272 | 277 | |
| `13_testing_strategies.md` | 420 | 426 | |
| `14_practical_implementation.md` | 106 | 112 | |
| `16_migration.md` | 409 | 486 | CloudFormation AMI gone; one `NotImplementedError` stub remains |
| `17_organisational_change.md` | 105 | 111 | |
| `18_team_structure.md` | 279 | 285 | |
| `19_management_as_code.md` | 300 | 301 | |
| `21_digitalisation.md` | 393 | 415 | |
| `23_soft_as_code_interplay.md` | 262 | 269 | |
| `24_best_practices.md` | 232 | 229 | |
| `25_future_trends.md` | 304 | 326 | |
| `26a_prerequisites_for_aac.md` | 136 | 140 | |
| `26b_aac_anti_patterns.md` | 177 | 177 | |
| `27_conclusion.md` | 133 | 93 | paragraphs unwrapped in this branch (one paragraph per line), not cut |
| `28_glossary.md` | 119 | 127 | |
| `29_about_the_author.md` | 143 | 142 | |
| `30_appendix_code_examples.md` | 4,267 | 5,212 | larger, not smaller |
| `31_appendix_b_technical_architecture.md` | 335 | 399 | |
| `appendix_templates_and_tools.md` | 333 | 442 | |
| `32_finos_project_blueprint.md` | 92 | 99 | |
| `33_references.md` | 178 | 379 | bibliography grew with the fact-check |
| Whole manuscript (`docs/[0-9]*.md`) | about 14,965 | about 16,500 | |

The epic's headline (about 14,965 lines to about 5,208) does not describe the current book, and its per-chapter targets cannot be applied without re-measuring.

## Verdict per issue

Categories: **ALREADY DONE** (evidence shows the issue is resolved), **PARTIAL** (part done, remainder listed), **PLANNED** (still valid, needs an author decision or a separate piece of work), **RECOMMEND CLOSE** (premise no longer holds, or superseded).

| Issue | Proposal | Verdict | Evidence from the current manuscript |
|---|---|---|---|
| #1937 Epic | Cut 65 % of the book | **RECOMMEND CLOSE as written; replace by 3 to 4 scoped issues** (see below) | Premise (line counts, chapter structure, series independence) is out of date. The structural decisions it lists conflict with the fixed chapter numbers. |
| #1899 Cross-chapter duplication | One concept, one chapter | **PARTIAL** | Commit `a4755f4` (#1951, 2 Nov) moved state management to 9B, DORA metrics to 5, the Rego/OPA introduction to 10, Structurizr workspace types to 6, CALM to 22. Still present: AaC against IaC table in both Chapter 3 (line 23) and Chapter 5 (line 25); "assure once, comply many" in Chapters 10, 11, 12, 15A and 32 (9 mentions); `SEC-ID-001` in Chapters 10, 12 and 15A; Pulumi against Terraform in Chapter 13 only now (Chapter 14 copy gone); quantum material in 9B, 12, 24 and 25 (Chapter 25 holds 16 of 28 mentions); CNCF statistics in more than ten files. The "verbatim duplicate bibliography" of 9 and 9B is no longer verbatim (diff of the two `## Sources` blocks is 42 lines). Remaining work is editorial and does not touch chapter numbers: **PLANNED** as one issue "remaining duplicates" with the list above. |
| #1901 Marketing language, filler, fake case studies | Remove marketing vocabulary; remove or name case studies | **PARTIAL** | "robust", "powerful" and "seamless" removed on this branch (commit for #1852). The unsourced figures named in the issue ("£500 billion", "up to 70 %") are no longer in `21_digitalisation.md`; the Spotify and Capital One passages now cite a reference (entries in the chapter's own Sources section). The vague "prevented significant disruption" anecdote in Chapter 4 is gone. **Still present and reported, not deleted:** `19_management_as_code.md:287` ("Consider a global software company operating in regulated financial markets"), `26a_prerequisites_for_aac.md:104` ("A multinational financial services group offers a useful illustration"), and the unnamed "teams operating at scale across finance, public services, healthcare, media" sentence in `24_best_practices.md:3` and `part_f_practices.md:13`. These are illustrative composites without name or figure; **the author must decide** whether to label them explicitly as hypothetical scenarios, name and source a real case, or delete. |
| #1903 Appendix 30: move about 85 % of code to an external repo | Create `aac-examples` | **PLANNED, author decision** | The appendix is 5,212 lines, up from 4,267. No `aac-examples` repository is referenced anywhere in `docs/`. Moving code out changes the book's promise that listings are inline and referenced by `NN_CODE_x` keys from the chapters, and the *Tools* companion harvests the code blocks of Books 1 to 10 from this repository (`library/` in `Geonitab/Tools`). Needs the author's decision and a coordinated change in *Tools*. |
| #1905 Security track: remove 9B and 9C, cut 12 | Remove two chapters, cut about 1,050 lines | **PLANNED, author decision (chapter removal blocked by series numbering)** | 9B (622 lines, 492 of them in code blocks) and 9C (92 lines) still exist. Chapter 9 has shrunk from 295 to 196 lines. Chapter 12 is 277 lines of which 174 are code. Claims on `12_compliance.md` (wildcard `autoscaling:*`, ECDSA labelled post-quantum) not re-verified here. A non-renumbering alternative: keep 9B and 9C as chapters and shorten their code blocks. |
| #1906 Merge Chapters 17, 18, 19 | One chapter | **PLANNED, author decision (blocked by series numbering)** | 17 is 111 lines, 18 is 285 (169 in code blocks), 19 is 301. Overlaps listed in the issue (cross-functional teams, DORA, competency frameworks, communities of practice) still exist. Later volumes cite these chapter numbers. |
| #1908 Remove Chapter 23 | Delete chapter, add 25 lines to Chapter 22 | **PLANNED, author decision (blocked by series numbering)** | Chapter 23 is 269 lines. I numbered its figures in this branch (23.1 to 23.7) without changing content. Removal means renumbering Chapters 24 to 33 or leaving a gap. |
| #1911 Reconsider Chapter 21 | Shrink to about 80 lines or remove | **PARTIAL, then author decision** | 415 lines now. Verified against the issue: `from terraform_runner import TerraformRunner` still present (line 334); the unsourced "£500 billion" and "70 %" figures are gone; company anecdotes now carry references. The off-topic argument (digital transformation strategy rather than AaC) is editorial. Option A (re-frame to EU cloud sovereignty, keep the number) avoids renumbering and is the safer of the two options. |
| #1913 Chapters 1 and 2: trim, move Requirements as Code | Cut about 260 lines, new chapter | **PLANNED** | Chapter 1: 106 lines; the Adoptability/Extensibility/Productivity trio and "Companion workbook" section remain. Chapter 2: 661 lines; Requirements as Code still about 275 lines of it. A new chapter is a numbering change (blocked); shortening in place is possible. |
| #1914 Chapter 5: shorten YAML, Dockerfile, Prometheus | Cut about 335 lines | **PLANNED** | 604 lines, 261 in code blocks. Section-level cuts do not affect chapter numbers and could be done after the author confirms the target length. Note the AaC against IaC table (duplicate of Chapter 3) is still there. |
| #1916 Chapter 6: halve Structurizr | Cut about 640 lines, consider split | **PLANNED** | 1,304 lines, 768 in code blocks. Largest chapter in the body of the book. A split is a numbering change (blocked); an in-place cut is possible. |
| #1918 Chapters 7 and 8: merge | Cut about 250 lines | **PLANNED, merge blocked** | 317 and 233 lines. The CNCF statistics duplicate noted in the issue is still present (Chapters 1, 7, 8 and others). |
| #1921 Chapters 13 and 14: remove Vitest, merge 14 into 13 | Cut about 265 lines | **PLANNED, merge blocked** | The Vitest section is still there (from line 104; 19 mentions of Vitest). Chapter 14 is 112 lines, mostly cross-references to the appendix. Removing the Vitest section needs no renumbering and the appendix keys `13_CODE_A` to `13_CODE_L` would need review. |
| #1922 Chapter 16: move scripts out | Cut about 260 lines | **PARTIAL** | The outdated CloudFormation AMI `ami-0c94855bb95b03c2e` is gone and the template was rewritten as an import change set (line 62 onward). 385 of 486 lines are still code, and a `raise NotImplementedError` stub remains at line 389. |
| #1924 Chapter 24: halve best practices | Cut about 117 lines | **PARTIAL** | The "will be inserted in final production" text for Figure 24.1 is gone (the figure is in). Five mind maps (24.1 to 24.5) remain; the issue asks to delete them. 229 lines now. |
| #1926 Chapter 25: move carbon-aware code | Cut about 212 lines | **PLANNED** | 326 lines, 177 in code blocks; the carbon-aware section (line 55 onward) is still there. |
| #1929 Chapters 26A, 26B, 27: shorten | Cut about 208 lines | **PLANNED** | 26A 140, 26B 177, 27 93 (after unwrapping). The "Author's note" on numbering in 26A (line 3) and the composite financial-services case (line 104) remain. |
| #1930 Chapter 29: about the author to about 25 lines | Cut about 118 lines | **PLANNED, author decision** | 142 lines. The "Swedish terminology reference" (line 35), "Contributing to future editions" (line 94) and "Closing reflections" (line 131) remain. Choosing what goes in the author's own biography is the author's decision. |
| #1932 Chapter 31 and templates appendix: move the meta and the Python script | Cut about 585 lines | **PLANNED, author decision** | Chapter 31 is 399 lines; `appendix_templates_and_tools.md` is 442 lines, 414 of them code (the migration discovery Python). |
| #1935 Chapters 4, 28, 32, 33 and maturity model: trim | Cut about 216 lines | **PARTIAL** | Chapter 4 anecdote removed; two ADR examples remain. Glossary still has "How to use this glossary" (line 7), the five unused terms (Chaos Monkey, Runway Health Check, Digital Twin, Knowledge Graph, Access Federation) and the "Terms and relationship database" section (line 107). A Nordqvist self-citation remains in the bibliography (entry at line 355). Thoughtworks appears 6 times in `33_references.md`; not checked entry by entry. On this branch the glossary dropped its "VCS" abbreviation (#1863). |
| #1961 Triage | This document | **Delivered as a draft** | Needs the author's reading of the table above. |

## Proposed replacement for the epic

Close #1937 and the structural children with a comment pointing to this document, then open scoped issues with completion criteria:

1. **Remaining duplicates (from #1899).** Completion: the list above reduced to one authoritative chapter per concept, other chapters refer to it. No chapter numbers change.
2. **Code in the body of the book (from #1914, #1916, #1922, #1926, #1932).** Completion: for each chapter, the author sets a code-line ceiling; listings above it move to Appendix A, keeping the `NN_CODE_x` keys. Coordinate with *Tools*.
3. **Illustrative composites (from #1901).** Completion: each unnamed case study is labelled as a hypothetical scenario, replaced by a sourced case or deleted, as the author decides.
4. **Structural options needing series coordination (#1905, #1906, #1908, #1911, #1918, #1921).** Completion: the author states for each whether the chapter keeps its number; options that keep numbers (shorten in place, re-frame Chapter 21 to EU sovereignty) are specified separately from options that renumber.

## What was done in this branch for the cross-cutting issues

- #1852: "robust", "powerful" and "seamless" replaced with concrete wording in about a dozen files.
- #1858: about a third of "enables/enabling" replaced.
- #1861: translation artefacts and "Architecture as Code-based" removed.
- Nothing was deleted for #1899 or #1901.

## Needs human

- Decide the fate of the structural items (table above) and whether a companion `aac-examples` repository will exist.
- Decide the treatment of the unnamed composite case studies listed under #1901.
- Close or re-scope the issues according to the verdicts above; this branch does not edit issues.
