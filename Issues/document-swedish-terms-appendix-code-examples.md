# Issue: Document Swedish Terminology in Appendix Code Examples

**Priority:** Low
**Suggested Labels:** documentation, localisation, appendix
**Linked Finding:** Swedish localisation audit – Appendix Code Examples

## Summary
Catalogue and address Swedish terminology within the Appendix Code Examples to ensure localisation is intentional and British English guidance remains clear.

## Background
Chapter 30 (`docs/30_appendix_code_examples/30_appendix_code_examples.md`) contains code snippets with Swedish words embedded in variables, comments, and outputs. Examples include references to MSB (Swedish Civil Contingencies Agency), Finansinspektionen, Integritetsskyddsmyndigheten (IMY), and numerous Swedish terms within Jenkins pipelines such as `kostnadscenter`, `säkerhetsskanning`, and phrases like `KRITISKA säkerhetsproblem funna`. Without documentation, these terms may confuse readers expecting British English context.

## Acceptance Criteria
- [ ] Inventory all Swedish words and phrases across the appendix code examples, noting their purpose and regulatory relevance.
- [ ] Decide whether to translate, annotate, or retain each term based on its necessity for illustrating localisation patterns.
- [ ] Update accompanying text or comments to clarify meaning for readers unfamiliar with Swedish terminology.
- [ ] Confirm that localisation decisions align with the overall British English standard for the book.

## Additional Notes
Coordinate with compliance editors to ensure references to Swedish regulators remain accurate and meaningful after any adjustments.
