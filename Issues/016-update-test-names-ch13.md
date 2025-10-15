# Update test names in Chapter 13: Testing Strategies

## Summary
Rename Chapter 13 testing artefacts and configurations to use EU-wide terminology and regions.

## Tasks
- [ ] Rename automated tests such as `TestSvenskaVPCGDPRCompliance` to European equivalents.
- [ ] Update Terraform generator configurations to use generic EU regions (e.g., eu-central-1) and neutral compliance tags.
- [ ] Ensure any GDPR flags or metadata are aligned with EU standards rather than national labels.

## Acceptance Criteria
- All tests execute and pass in CI/CD pipelines configured for EU regions.
- No localisation-specific names or strings remain in testing assets.
- Generated configurations support multiple EU regions without modification.

## Labels
- test
- enhancement

## Assignees
- @qa-team

## Milestone
- v1.1
