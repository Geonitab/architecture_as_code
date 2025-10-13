Chapter 12 figures show incorrect numbering from Chapter 14

**Description**: The captions in Chapter 12 reference figures as "Figure 14.1", "Figure 14.2", etc., instead of the correct Chapter 12 numbering. This confuses readers and breaks cross-references throughout the document.

**Current Behavior**: The Markdown captions beneath the Chapter 12 diagrams hardcode "Figure 14.x" even though the surrounding text discusses Chapter 12 content. Pandoc therefore renders mismatched numbering in the compiled PDF.

**Expected Behavior**: Captions in Chapter 12 should reference "Figure 12.x" so the numbering matches the chapter sequence and Pandoc can auto-generate the correct labels.

**Affected Files**:
- `docs/12_compliance.md`

**Suggested Fix**:
1. Update the figure captions in Chapter 12 to remove any hardcoded "14." prefixes.
2. Ensure captions rely on Pandoc's automatic numbering (e.g., italic text beneath the image) with the correct chapter number.
3. Rebuild the book to verify that the figure numbers now appear as 12.1, 12.2, etc.
