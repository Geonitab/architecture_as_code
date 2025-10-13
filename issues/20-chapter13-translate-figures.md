Translate Swedish labels in Chapter 13 figures to English

**Description**: Figures 13.1 and 13.2 still contain Swedish terms within the diagrams, even though the chapter text has been localised to English. This creates a jarring language mix and makes the visuals harder to understand for English-speaking readers.

**Current Behavior**: The Mermaid sources for the Chapter 13 diagrams include Swedish words (e.g., "Planering", "Genomförande"). The generated PNGs therefore ship with Swedish labels in the published book.

**Expected Behavior**: Figures 13.1 and 13.2 should use English terminology consistent with the chapter narrative and glossary.

**Affected Files**:
- `docs/13_testing_strategies.md`
- `docs/images/diagram_13_test_pyramid.mmd`
- `docs/images/diagram_13_test_pyramid.png`
- `docs/images/diagram_13_testing_quadrant.mmd`
- `docs/images/diagram_13_testing_quadrant.png`

**Suggested Fix**:
1. Update the Mermaid diagram labels to English equivalents.
2. Regenerate the PNG assets with the standard light theme.
3. Review the chapter to ensure the captions and references still align with the updated terminology.
