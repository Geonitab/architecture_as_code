Improve text contrast for Figure 16.2

**Description**: Figure 16.2 includes the label "Leadership Support" rendered in a light grey that blends into the white background. The text is difficult to read in both the PDF and HTML outputs.

**Current Behavior**: The Mermaid definition styles the leadership node with a light font color, creating poor contrast after export.

**Expected Behavior**: The label should use the same dark text color as the other nodes in the diagram to satisfy accessibility guidelines.

**Affected Files**:
- `docs/16_migration.md`
- `docs/images/diagram_18_competency_cycle.mmd`
- `docs/images/diagram_18_competency_cycle.png`

**Suggested Fix**:
1. Update the Mermaid styling for the leadership node to use the standard text color.
2. Regenerate the PNG asset.
3. Confirm the updated figure is legible in Chapter 16.
