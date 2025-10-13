Move Chapter 18 to the end of the book

**Description**: Chapter 18 appears before later chapters even though it should be positioned at the end of the manuscript. The current placement disrupts the intended narrative flow.

**Current Behavior**: The MkDocs/Pandoc build sequence renders Chapter 18 before Chapters 19–27, contradicting the desired order where Chapter 18 should serve as the concluding chapter before the appendices.

**Expected Behavior**: Chapter 18 should appear after Chapter 20 and before the appendices, aligning with the new outline.

**Affected Files**:
- `docs/18_team_structure.md`
- `docs/mkdocs.yml` or other build ordering configuration (if applicable)
- Any navigation indices referencing Chapter 18

**Suggested Fix**:
1. Update the chapter ordering configuration so Chapter 18 is moved to the end of the main content.
2. Adjust cross-references or transitions if they assume the old position.
3. Rebuild the book to confirm the chapter appears in the correct location.
