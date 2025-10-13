Lighten and reposition Figure 27.1 in Appendix B

**Description**: Figure 27.1 is too dark and appears mid-way through a code block in Appendix B, making it difficult to see and disrupting the layout.

**Current Behavior**: The technical architecture diagram uses a dark palette that blends into the background. Additionally, its Markdown placement causes the figure to render inside a surrounding code listing.

**Expected Behavior**: Figure 27.1 should use the standard light theme and sit outside any code blocks so the layout remains consistent.

**Affected Files**:
- `docs/31_technical_architecture.md`
- `docs/images/diagram_27_technical_structure.mmd`
- `docs/images/diagram_27_technical_structure.png`

**Suggested Fix**:
1. Update the Mermaid source to use the shared light theme with high-contrast text.
2. Move the image reference outside of any fenced code blocks.
3. Regenerate the PNG and verify the figure renders correctly in Appendix B.
