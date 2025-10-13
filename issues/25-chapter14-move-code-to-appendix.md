Relocate the lengthy Chapter 14 code example to Appendix A

**Description**: Chapter 14 currently embeds a very long code listing directly in the main narrative. The extended snippet disrupts the reading flow and duplicates material already curated in Appendix A.

**Current Behavior**: A multi-page code block appears inside Chapter 14, forcing readers to scroll past implementation details before continuing with the guidance content.

**Expected Behavior**: Chapter 14 should summarise the code example and link to Appendix A, where the full listing can live alongside other reusable assets.

**Affected Files**:
- `docs/14_practical_implementation.md`
- `docs/30_appendix_code_examples.md`

**Suggested Fix**:
1. Remove the in-chapter code block, leaving behind a brief summary and a reference link.
2. Add the full code listing to Appendix A if it is not already present, or cross-reference the existing entry.
3. Verify that internal links and headings still render correctly after the move.
