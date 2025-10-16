# Issue: Emphasise Testable IaC for Practical AaC Execution

**Priority:** High  
**Suggested Labels:** documentation, qa  
**Linked Finding:** #9 – IaC Testability

## Summary
Clarify that AaC's quality promise depends on adopting IaC tooling that supports unit and integration testing, highlighting Pulumi and AWS CDK as exemplars.

## Background
AaC extends beyond documentation; it demands executable, testable architectural artefacts. Tools such as Pulumi and AWS CDK enable infrastructure definitions in general-purpose languages, unlocking unit testing and CI-friendly validation. The practical implementation and testing chapters need explicit guidance that positions these tools over purely declarative options when test coverage is paramount.

## Acceptance Criteria
- [ ] Add a dedicated subsection to `docs/14_practical_implementation.md` (and reference `docs/13_testing_strategies.md` if necessary) that explains why AaC favours IaC platforms supporting unit tests.
- [ ] Provide concrete examples of how Pulumi or AWS CDK facilitate architectural testing workflows.
- [ ] Contrast this approach with declarative-only tools (e.g., Terraform) in terms of testability, whilst acknowledging their place within the ecosystem.
- [ ] Reference the relevant sources from the verified list (Source [16] or others) to substantiate claims about testing capability.

## Additional Notes
Coordinate with the testing strategies chapter so messaging is consistent and avoids duplication.
