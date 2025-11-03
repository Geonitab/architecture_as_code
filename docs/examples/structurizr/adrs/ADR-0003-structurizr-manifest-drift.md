# ADR-0003: Detect Structurizr Drift via Workspace Manifests

## Status
Accepted

## Context
Contributors occasionally modify the Structurizr workspace without regenerating diagrams or updating documentation. Reviewers only spot the mismatch late in the release cycle, which delays approvals and undermines trust in the automation guidance described in the manuscript.

## Decision
Store a manifest alongside the reference workspace that records the SHA-256 digest of the DSL file and the export formats produced by the automation scripts. Continuous integration jobs calculate the current digest during pull requests and fail when it diverges from the stored value.

## Consequences
- Drift is detected immediately, prompting contributors to run the export helper before requesting review.
- The manifest doubles as lightweight documentation for reviewers who want to confirm which export formats the pipeline generates.
- Because the manifest lives next to the workspace, history diffing clearly shows when the DSL changed versus when exports were refreshed.
