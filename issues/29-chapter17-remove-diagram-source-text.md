Remove inline “Diagram source” notes from Chapter 17

**Description**: Chapter 17 still contains inline strings such as “Diagram source: images/diagram_19_devops_management_loop.mmd”. These production notes should not appear in the published manuscript.

**Current Behavior**: After each figure description, the chapter includes a plain text line pointing to the Mermaid source file. The note renders in italics in the final PDF, distracting from the content and cluttering the layout.

**Expected Behavior**: Source references belong in the repository, not in the reader-facing narrative. The chapter should omit these notes and rely on standard captions.

**Affected Files**:
- `docs/17_organizational_change.md`

**Suggested Fix**:
1. Remove each “Diagram source” sentence following the Chapter 17 figures.
2. Verify that the remaining figure captions still provide enough context for readers.
3. Rebuild the chapter to confirm no residual production notes remain.
