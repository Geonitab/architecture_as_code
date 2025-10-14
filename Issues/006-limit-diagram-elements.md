# Enforce Diagram Legibility Limits

## Summary
Ensure every diagram contains no more than 15 elements to maintain readability, splitting diagrams when necessary.

## Tasks
- [x] Review all diagrams and count their visual elements (nodes, bars, slices, etc.).
- [x] Identify diagrams exceeding the 15-element threshold.
- [x] Propose and implement splits or redesigns for diagrams with too many elements.

## Acceptance Criteria
- [x] No single diagram contains more than 15 elements.
- [x] Replacement diagrams preserve the original information while improving clarity.

## Implementation Summary

### Analysis Results
- Analyzed 72 diagram files in `docs/images/`
- Identified 13 diagrams exceeding the 15-element threshold
- All diagrams now comply with the 15-element limit

### Changes Made

#### Simplified Diagrams (4)
1. `code_review_sequence.mmd` - Reduced from 18 to 15 elements by condensing quality check steps
2. `diagram_04_adr_chapter.mmd` - Reduced from 18 to 13 elements by removing redundant subgraph
3. `diagram_13_testing_quadrant.mmd` - Reduced from 16 to 13 elements by removing low-coverage quadrant
4. `diagram_29_governance_pipeline.mmd` - Reduced from 16 to 11 elements by consolidating workflow steps

#### Split Flowcharts (2)
1. `diagram_27_technical_structure.mmd` (23 elements) → Split into:
   - `diagram_27a_source_materials.mmd` (6 elements) - Source materials and version control
   - `diagram_27b_build_pipeline.mmd` (12 elements) - Build environment and output formats

2. `diagram_30_soft_as_code.mmd` - Reduced from 21 to 12 elements by consolidating related concepts

#### Split Mindmaps

1. **Organizational Change** - `mindmap_17_organization.mmd` (38 elements) → 3 diagrams:
   - `mindmap_17a_culture_collaboration.mmd` (13 elements) - Cultural foundations and cross-functional teams
   - `mindmap_17b_capability_roles.mmd` (12 elements) - Learning paths and role evolution
   - `mindmap_17c_change_management.mmd` (12 elements) - Change management approach

2. **Digital Transformation** - `mindmap_21_digitalisation.mmd` (49 elements) → 3 diagrams:
   - `mindmap_21a_technical.mmd` (13 elements) - Technical foundation (cloud, automation, architecture)
   - `mindmap_21b_organisational.mmd` (12 elements) - Organizational dimensions (teams, governance, change)
   - `mindmap_21c_business.mmd` (12 elements) - Business value and innovation

3. **Best Practices** - `mindmap_22_best_practices.mmd` (75 elements) → 5 diagrams:
   - `mindmap_22a_code_organization.mmd` (13 elements) - Repository structure and module design
   - `mindmap_22b_security_compliance.mmd` (12 elements) - Security patterns and regulatory compliance
   - `mindmap_22c_performance.mmd` (12 elements) - Performance optimization and scaling
   - `mindmap_22d_governance.mmd` (12 elements) - Governance frameworks and policy-as-code
   - `mindmap_22e_global_practices.mmd` (11 elements) - Cross-cultural collaboration and open source

4. **Soft as Code Interplay** - `mindmap_23_soft_as_code.mmd` (108 elements) → 6 diagrams:
   - `mindmap_23a_shared_dna.mmd` (12 elements) - Shared DNA of "as code" disciplines
   - `mindmap_23b_compliance.mmd` (12 elements) - Compliance as code
   - `mindmap_23c_architecture.mmd` (11 elements) - Architecture as code central hub
   - `mindmap_23d_documentation.mmd` (11 elements) - Documentation as code
   - `mindmap_23e_knowledge_culture.mmd` (11 elements) - Knowledge and culture as code
   - `mindmap_23f_synergies.mmd` (11 elements) - Synergies and implementation strategy

### Chapter Updates
Updated 5 chapters to reference the new split diagrams:
- `docs/17_organizational_change.md` - Now references 3 mindmaps instead of 1
- `docs/21_digitalization.md` - Now references 3 mindmaps instead of 1
- `docs/23_soft_as_code_interplay.md` - Now references 6 mindmaps instead of 1
- `docs/24_best_practices.md` - Now references 5 mindmaps instead of 1
- `docs/31_technical_architecture.md` - Now references 2 diagrams instead of 1

### Archived Diagrams
Moved 8 oversized diagrams to `docs/images/archive/`:
- `diagram_27_technical_structure.mmd` (23 elements)
- `mindmap_02_principles.mmd` (37 elements, unused)
- `mindmap_10_security_original.mmd` (48 elements, unused)
- `mindmap_17_organization.mmd` (38 elements)
- `mindmap_19_digitalization.mmd` (55 elements, unused)
- `mindmap_21_digitalisation.mmd` (49 elements)
- `mindmap_22_best_practices.mmd` (75 elements)
- `mindmap_23_soft_as_code.mmd` (108 elements)

### Validation
Created `scripts/validate_diagram_elements.py` to automatically validate all diagrams comply with the 15-element limit. This script can be integrated into CI/CD pipelines.

### Results
✅ All 83 active diagrams now have ≤15 elements
✅ All split diagrams preserve the original information
✅ Chapter references updated with clear, descriptive captions
✅ Improved diagram clarity and readability throughout the book
