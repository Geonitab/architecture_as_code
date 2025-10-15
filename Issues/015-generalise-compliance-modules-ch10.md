# Generalise compliance modules in Chapter 10: Policy as Code

## Summary
Ensure Chapter 10 compliance modules use EU-wide regulators and regions without Swedish-specific references.

## Tasks
- [ ] Update the OPA compliance module to remove "msb" regulator references and parameterise region settings for EU deployment.
- [ ] Adjust the OSCAL financial profile to cite EU-wide standards such as PSD2 instead of Finansinspektionen requirements.
- [ ] Verify that all code examples operate correctly for general EU compliance scenarios.

## Acceptance Criteria
- Modules validate GDPR requirements using EU terminology and regional parameters.
- No Swedish abbreviations, regulators, or locations appear in Chapter 10 content.
- OSCAL examples align with recognised EU templates.

## Labels
- bug
- compliance

## Assignees
- @dev-team

## Milestone
- v1.1
