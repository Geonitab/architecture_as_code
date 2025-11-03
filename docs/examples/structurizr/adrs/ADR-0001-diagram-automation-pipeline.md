# ADR-0001: Automate Structurizr Diagram Rendering in CI

## Status
Accepted

## Context
The book pipeline encourages contributors to submit Structurizr DSL updates alongside manuscript changes. Reviewers require rendered diagrams to confirm the visual impact of each change and ensure nothing drifts from previously agreed layouts. Manual exports slow feedback cycles and frequently result in inconsistent artefacts.

## Decision
Introduce a repository automation job that validates the Structurizr workspace, exports diagram assets, and publishes them as pull request build artefacts. The job reuses the reference workspace so every contribution follows the same toolchain and layout defaults.

## Consequences
- Reviewers receive fresh PNG diagrams without waiting for local exports.
- Failing validations stop merges when the DSL becomes inconsistent or when exports lag behind workspace edits.
- Contributors use the shared automation command to replicate CI behaviour on their workstations, reducing "works on my machine" discrepancies.
