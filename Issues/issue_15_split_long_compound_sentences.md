# Issue 15: Split Long Compound Sentences

## Relevant Documentation Sections
Architecture as Code manuscript chapters, especially sections that describe workflows, tooling integrations, and governance frameworks.

## Problem Statement
Numerous passages use long compound sentences exceeding 60 words, packing multiple clauses into a single line. These constructions overwhelm readers and obscure the main message.

## Impact
- Readers must re-read sentences to extract key information.
- Dense wording reduces accessibility for practitioners seeking quick guidance.
- Overly long sentences diminish the authoritative, confident tone of the book.

## Recommended Remediation
- Limit sentences to 20–25 words where possible, with one core idea per sentence.
- Split lengthy sentences at natural breakpoints, introducing connective sentences to preserve flow.
- Ensure resulting prose maintains British English spelling and consistent terminology.

## Acceptance Criteria
- Highlighted examples are rewritten into shorter sequences of sentences without losing meaning.
- Editorial sampling across documentation confirms improved readability and pacing.
- Readability tooling (for example, Flesch-Kincaid) shows measurable improvement in affected sections.

## Recommended Labels
`documentation`
