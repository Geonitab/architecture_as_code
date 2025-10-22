# Update test pipeline for code examples

## Summary
Audit and enhance the automated test pipeline so that every code example in the manuscript runs during continuous integration, with clear reporting that highlights failing snippets and tracks regressions.

## Background
The code examples underpin the book's credibility. Some snippets are currently untested or rely on manual verification, increasing the risk of drift as the content evolves. Strengthening the pipeline will provide fast feedback and protect against broken examples.

## Objectives
- Inventory all executable examples and determine how they are currently validated.
- Extend the pipeline to execute every example on each push, covering different runtimes or dependencies as needed.
- Improve reporting so contributors can trace failures back to the relevant manuscript sections.

## Proposed Approach
1. Review the existing test workflows and scripts to understand their coverage and limitations.
2. Design a mechanism to extract or package code examples for automated execution, taking into account language-specific requirements.
3. Update or add workflows that run the expanded test suite on each push and pull request.
4. Publish test results in an easily consumable format, such as annotated logs or summary comments.
5. Document the updated process so contributors know how to run the checks locally before raising pull requests.

## Acceptance Criteria
- Comprehensive mapping of every code example to an automated test or execution step.
- GitHub Actions (or equivalent) workflows updated to run the expanded coverage on each push and pull request.
- Clear pass/fail reporting that links failures to the corresponding manuscript sections.
- Contributor documentation refreshed with instructions for running the tests locally.

## Suggested Labels
- `dev`
- `ci`
- `qa`

