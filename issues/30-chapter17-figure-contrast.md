Improve contrast for Figure 17.4

**Description**: Figure 17.4 displays white text on a light grey background, making the labels nearly illegible in printed and digital formats.

**Current Behavior**: The Mermaid diagram exports with light background fills and white font colors, leading to low-contrast nodes that fail accessibility standards.

**Expected Behavior**: Figure 17.4 should use dark text on light backgrounds (or vice versa) to maintain clear contrast across mediums.

**Affected Files**:
- `docs/17_organizational_change.md`
- `docs/images/diagram_19_devops_management_loop.mmd`
- `docs/images/diagram_19_devops_management_loop.png`

**Suggested Fix**:
1. Update the Mermaid theme or explicit styles for the nodes in Figure 17.4 to use dark text.
2. Regenerate the PNG asset.
3. Rebuild the book to confirm the figure is readable.
