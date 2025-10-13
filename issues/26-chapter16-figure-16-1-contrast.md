Improve text contrast for Figure 16.1

**Description**: In Chapter 16, the label "Leadership & People Ops" inside Figure 16.1 is rendered in a very light grey. Readers struggle to distinguish the text against the white background.

**Current Behavior**: The Mermaid diagram uses a light grey font color for the leadership node, resulting in poor contrast once exported to PNG.

**Expected Behavior**: Figure 16.1 should use the same high-contrast text color as other nodes so the label remains legible.

**Affected Files**:
- `docs/16_migration.md`
- `docs/images/diagram_18_team_collaboration.mmd`
- `docs/images/diagram_18_team_collaboration.png`

**Suggested Fix**:
1. Update the Mermaid class or style for the leadership node to use the standard dark text color.
2. Regenerate the PNG asset after adjusting the theme.
3. Verify the updated figure renders clearly in Chapter 16.
