Replace product-specific terminology in Figure 13.4 with generic language

**Description**: Figure 13.4 in Chapter 13 references brand-specific features and proprietary product names. These labels make the diagram feel vendor-centric and reduce its usefulness for readers working in different environments.

**Current Behavior**: The Mermaid diagram for Figure 13.4 includes names of particular tools and internal systems. The published PNG therefore exposes terms that should remain anonymised or replaced with generic process descriptions.

**Expected Behavior**: Figure 13.4 should describe testing flows using neutral terminology (e.g., "CI pipeline", "Test orchestration service") so the content applies broadly across organisations.

**Affected Files**:
- `docs/13_testing_strategies.md`
- `docs/images/diagram_13_user_journey.mmd`
- `docs/images/diagram_13_user_journey.png`

**Suggested Fix**:
1. Review the Mermaid source for product or vendor references.
2. Replace those labels with role- or capability-based names.
3. Regenerate the PNG and confirm the new terminology is reflected in the chapter.
