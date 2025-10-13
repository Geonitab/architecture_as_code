Correct Chapter 19 figure numbering referencing Chapter 21

**Description**: Figure captions in Chapter 19 incorrectly reference Chapter 21 (e.g., “Figure 21.1”) instead of using the proper Chapter 19 numbering. This leads to confusion and broken cross-references.

**Current Behavior**: Several captions are hardcoded with “21.x” values despite appearing in Chapter 19.

**Expected Behavior**: Captions should reference “Figure 19.x” and rely on Pandoc’s automatic numbering.

**Affected Files**:
- `docs/19_management_as_code.md`

**Suggested Fix**:
1. Replace any hardcoded “21.” prefixes in the captions with neutral text (e.g., “Figure 19.x”) or remove the numbering entirely to let Pandoc manage it.
2. Rebuild the book to confirm the captions increment correctly.
