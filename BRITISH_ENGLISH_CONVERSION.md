# British English Conversion - Diagram Files

## Overview

All Mermaid diagram source files (.mmd) in the `docs/images/` directory have been converted from American English to British English to ensure consistency throughout the documentation.

## Changes Made

### Spelling Conversions

The following American English spellings were converted to British English:

| American English | British English |
|-----------------|-----------------|
| optimization | optimisation |
| organization | organisation |
| organizational | organisational |
| utilization | utilisation |
| formalization | formalisation |
| minimization | minimisation |
| color | colour |

### Files Updated

**Active Diagram Files (11 files):**
1. `docs/images/diagram_04_adr_lifecycle.mmd` - ADR lifecycle diagram
2. `docs/images/diagram_05_gantt_timeline.mmd` - Gantt timeline
3. `docs/images/diagram_12_requirements_testing.mmd` - Requirements testing diagram
4. `docs/images/diagram_16_chapter15.mmd` - Cost optimization cycle
5. `docs/images/diagram_16_finops_cycle.mmd` - FinOps cycle
6. `docs/images/diagram_16_monitoring_stack.mmd` - Monitoring stack
7. `docs/images/diagram_22_conclusion.mmd` - Success factors pie chart
8. `docs/images/diagram_29_governance_pipeline.mmd` - Governance pipeline
9. `docs/images/mindmap_22a_code_organization.mmd` - Code organization mindmap
10. `docs/images/mindmap_22c_performance.mmd` - Performance mindmap
11. `docs/images/mindmap_22d_governance.mmd` - Governance mindmap

**Archived Diagram Files (3 files):**
1. `docs/images/archive/mindmap_02_principles.mmd` - Principles mindmap
2. `docs/images/archive/mindmap_22_best_practices.mmd` - Best practices mindmap
3. `docs/images/archive/mindmap_23_soft_as_code.mmd` - Soft as Code mindmap

**Additional Files:**
- `docs/images/mindmap_23e_knowledge_culture.mmd` - Knowledge culture mindmap

### Statistics

- **Total files updated:** 15
- **Total changes:** 26 replacements
- **Lines modified:** 26 insertions(+), 26 deletions(-)

## Verification

### Syntax Verification
✅ All modified .mmd files maintain valid Mermaid diagram syntax
✅ No breaking changes to diagram structure
✅ All diagram types preserved correctly

### Remaining English Variants

The following words that appear in some .mmd files are correctly spelled the same in both American and British English:
- "Analysis" (same in both variants)
- "Rightsizing" (technical term, no British variant)

## Impact

This conversion ensures that:
- All diagram source files use British English spelling
- PNG images regenerated from these sources will display British English text
- Documentation maintains consistent British English throughout
- Website (aac.geon.se), PDF, EPUB, and all other deliverables will use British English

## Related Documentation

- `DIAGRAM_TRANSLATION_FIX.md` - Previous Swedish to English translation work
- `VISUAL_ELEMENTS_GUIDE.md` - Visual elements and diagram theming guidelines
- `docs/images/README.md` - Diagram asset guidelines

## Notes

- This conversion complements the earlier Swedish to English translation work
- All changes are backward compatible with the Mermaid syntax
- The conversion script can be reused if new diagrams are added with American English spelling
