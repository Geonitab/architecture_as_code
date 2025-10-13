Restore missing Figure 14.1 image in Chapter 14

**Description**: Chapter 14 references Figure 14.1, but the intended diagram is missing or replaced with a placeholder. Readers see an empty space or the wrong image where the capability landscape should appear.

**Current Behavior**: The Markdown references `images/diagram_08_chapter7.png`, yet the exported PDF and site do not show the expected Figure 14.1 illustration. The asset likely references the wrong file or the image was removed during refactoring.

**Expected Behavior**: Figure 14.1 should display the capability landscape diagram that introduces the chapter's operating model.

**Affected Files**:
- `docs/14_practical_implementation.md`
- `docs/images/diagram_08_chapter7.png`

**Suggested Fix**:
1. Confirm which diagram should represent Figure 14.1.
2. Restore or recreate the correct image asset in `docs/images/`.
3. Update the Markdown reference if a new filename is required, and verify the figure renders in the generated PDF.
