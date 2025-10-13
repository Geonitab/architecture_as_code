Improve contrast for Figure 20.1

**Description**: Figure 20.1 uses white text on a light grey background, reducing legibility for readers and failing contrast guidelines.

**Current Behavior**: The Mermaid diagram renders with white font and pastel node fills, making the labels difficult to read.

**Expected Behavior**: Figure 20.1 should use high-contrast colors—preferably dark text on light backgrounds—to match the design system.

**Affected Files**:
- `docs/20_ai_agent_team.md`
- `docs/images/diagram_28_agent_team.mmd`
- `docs/images/diagram_28_agent_team.png`

**Suggested Fix**:
1. Update the Mermaid styling to use the shared light theme with dark text.
2. Regenerate the PNG asset.
3. Verify the figure renders clearly in Chapter 20.
