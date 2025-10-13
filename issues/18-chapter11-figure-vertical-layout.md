Figure 11.3 layout needs to be reworked into a vertical orientation

**Description**: Figure 11.3 in Chapter 11 currently uses a wide horizontal layout that becomes hard to read on standard PDF pages. The swim lanes compress text and require excessive horizontal scrolling when viewed on smaller screens.

**Current Behavior**: The governance workflow in Figure 11.3 is arranged horizontally with several parallel columns. Labels overlap and the diagram appears cramped when exported to PDF, causing accessibility issues for readers who rely on zooming.

**Expected Behavior**: Figure 11.3 should be redesigned with a vertical layout so that each step flows top-to-bottom, matching the reading direction and providing sufficient space for labels.

**Affected Files**:
- `docs/11_governance_as_code.md`
- `docs/images/diagram_29_governance_pipeline.mmd` (or the Mermaid source used for Figure 11.3)
- Corresponding PNG output for Figure 11.3

**Suggested Fix**:
1. Update the Mermaid (or source) diagram to arrange stages vertically.
2. Adjust node spacing and alignment to improve readability on A4/Letter page sizes.
3. Regenerate the PNG asset and confirm the updated layout renders correctly in Chapter 11.
