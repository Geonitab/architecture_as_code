# Issue 22: Expand Compliance Requirement Examples Beyond Repeated Lists

## Priority
Medium

## Type
List repetition

## Component
Compliance sections across chapters

## Problem Statement
Compliance lists featuring “GDPR, PCI-DSS, and industry-specific regulations” recur across Chapters 2, 4, and 5, occasionally swapping in ISO27001 or SOC2. The repetition overemphasises a narrow subset of regulations and neglects sector-specific obligations.

## Evidence of Repetition
- Chapter 2 – Requirements as Code example: YAML snippet `compliance: ["GDPR", "ISO27001"]`.
- Chapter 4 – Compliance and Quality Standards: reiterates “GDPR, PCI-DSS, and industry-specific regulations”.
- Chapter 5 – Multiple references embedding the same trio of regulations into narrative passages.

## Impact
- Signals a limited understanding of broader regulatory landscapes (for example, NIS2, DORA, HIPAA, energy-sector rules).
- Reduces the perceived relevance of the book for organisations outside GDPR-focused contexts.
- Creates monotonous lists instead of targeted, scenario-specific guidance.

## Recommended Actions
1. Develop a compliance matrix or appendix mapping regulations to architectural concerns and industries.
2. Vary examples in each chapter to highlight different regulatory drivers (for example, DORA for financial services, NERC CIP for energy).
3. Reference the consolidated matrix instead of repeating the same short list in prose.

## Acceptance Criteria
- [ ] Compliance matrix or appendix created with cross-industry coverage.
- [ ] Chapters 2, 4, and 5 updated to reference the matrix and showcase diverse regulatory examples.
- [ ] Editorial review confirms elimination of repetitive regulation lists.

## Recommended Labels
`documentation`, `requirements`
