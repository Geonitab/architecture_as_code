# Generalise GDPR examples in Chapter 5: CI/CD Pipelines

## Summary
Align the Chapter 5 GDPR pipeline examples with EU-wide identifiers and compliance triggers instead of Swedish-specific patterns.

## Tasks
- [ ] Replace Swedish personal data patterns with general EU identifiers in pipeline documentation.
- [ ] Update GitHub Actions workflows and regex patterns to remove Swedish-specific data checks.
- [ ] Validate the workflow configuration using a representative European AWS region such as eu-west-1.

## Acceptance Criteria
- Pipeline triggers focus on general GDPR-compliant events and identifiers.
- No Swedish-specific strings, comments, or validation logic remain in the chapter examples.
- Workflow testing is confirmed for an EU region configuration.

## Labels
- enhancement
- compliance

## Assignees
- @dev-team

## Milestone
- v1.1
