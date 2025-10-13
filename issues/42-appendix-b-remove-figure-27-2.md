Remove Figure 27.2 from Appendix B

**Description**: Figure 27.2 is redundant in Appendix B and should be removed to simplify the section.

**Current Behavior**: The appendix displays an additional architecture data model diagram that repeats information covered elsewhere.

**Expected Behavior**: Appendix B should rely on the primary technical architecture figure without the extra diagram.

**Affected Files**:
- `docs/31_technical_architecture.md`
- `docs/images/diagram_27_er_architecture.png`
- `docs/images/diagram_27_er_architecture.mmd`

**Suggested Fix**:
1. Delete the Markdown block referencing Figure 27.2.
2. Remove the PNG if it is unused elsewhere.
3. Rebuild the book to ensure no missing asset warnings.
