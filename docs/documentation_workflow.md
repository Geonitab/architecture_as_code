# Documentation Workflow Guide {#documentation-workflow}

## Purpose

This workflow ensures that documentation, diagrams, and executable architecture models evolve together. By treating every inform
ation artefact as code, teams maintain consistent narratives, review history, and traceability across the repository.

## Branching and Reviews

1. **Create a feature branch** for every documentation improvement. Align naming with the associated issue or change request.
2. **Edit Markdown, diagrams, and models together.** Keep Structurizr, CALM, Mermaid, and narrative updates within the same chan
ge set to avoid divergence.
3. **Preview locally.** Render diagrams or generate the book preview to confirm formatting, spellings, and references.
4. **Open a pull request** with a concise summary, detailed testing notes, and links to related issues.
5. **Request peer review.** At least one reviewer validates technical accuracy, adherence to British English, and consistency wit
h established terminology.

## Automation and Checks

- **Continuous integration** executes `python3 generate_book.py && docs/build_book.sh` to rebuild the book, regenerate diagrams,
  and surface linting feedback.
- **ADR validation** runs `python3 scripts/validate_adrs.py` followed by `python3 scripts/generate_adr_catalogue.py` so that new
  decisions automatically populate the MkDocs navigation and change-log-friendly catalogue.
- **Link validation** ensures Markdown references resolve correctly. Update links or add redirect stubs whenever file paths chan
ge.
- **Diagram generation** leverages Mermaid CLI during the build to refresh PNG artefacts. Never commit outdated diagram renders.
- **Spell checking and style** checks enforce British English spellings and repository style conventions.

## Merging and Maintenance

- Merge only after all automated checks pass and reviewers approve.
- Keep the workflow documented—update this file whenever the process evolves.
- Periodically audit the documentation tree to remove dead links, regenerate diagrams, and validate that reference material remai
ns accurate.

## Incident Response

When link checkers or reviewers discover gaps:

1. **Reproduce the issue** locally using the documented commands.
2. **Patch the affected artefacts** (Markdown, diagrams, or models) within a dedicated branch.
3. **Extend tests or checks** if the gap was not caught automatically.
4. **Document lessons learnt** in the pull request or relevant chapter to prevent recurrence.
