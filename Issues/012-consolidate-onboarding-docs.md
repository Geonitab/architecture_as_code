# Consolidate Introductory and Onboarding Documentation

## Summary
Essential onboarding guidance is fragmented across multiple markdown files (`README.md`, `WORKFLOWS.md`, `AUTOMATION_WORKFLOWS.md`, `TEST_WORKFLOW.md`, and various docs/* chapters). New contributors must cross-reference several long-form documents to understand the project's purpose, required tooling, and validation steps. This creates avoidable friction for first-time collaborators.

## Tasks
- Inventory the current onboarding touchpoints (repository root files plus introductory chapters such as `docs/01_introduction.md` and `docs/book_structure.md`) to map overlapping information.
- Draft a unified `docs/getting-started.md` that walks readers through project context, prerequisite installations, core commands, and validation expectations in a concise, sequential format.
- Refactor `README.md` so the opening section remains a high-level overview and links prominently to the new getting started guide, book structure, and workflow documentation.
- Update supporting files (e.g., `WORKFLOWS.md`, `AUTOMATION_WORKFLOWS.md`) to remove duplicated narrative and point to the single source of truth for onboarding instructions.
- Ensure MkDocs navigation includes the new guide so it appears in published documentation, and verify build pipelines succeed with the updated structure.

## Acceptance Criteria
- A clearly scoped `docs/getting-started.md` exists, covering context, setup, key commands, and validation checks without requiring readers to consult multiple files.
- `README.md` links to the getting started guide and other foundational references while avoiding duplicated setup content.
- Automation documentation references the new guide for onboarding steps, with redundant text removed or summarised.
- MkDocs site navigation reflects the new guide and all automated builds succeed after the documentation restructuring.
