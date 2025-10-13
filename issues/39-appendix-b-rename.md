Rename Chapter 31 to “Appendix B”

**Description**: The technical architecture chapter at the end of the book should be presented as “Appendix B”, but it currently appears as “Chapter 31 – Technical Architecture for Book Production”.

**Current Behavior**: The heading and navigation label treat the appendix like a numbered chapter, causing confusion in the table of contents.

**Expected Behavior**: The section should be titled “Appendix B: Technical Architecture for Book Production” and listed among the appendices.

**Affected Files**:
- `docs/31_technical_architecture.md`
- Any navigation configuration referencing this file (e.g., `mkdocs.yml`, `docs/pandoc.yaml`)

**Suggested Fix**:
1. Update the top-level heading to “Appendix B: …”.
2. Adjust configuration so the appendix is grouped with other appendices rather than numbered chapters.
