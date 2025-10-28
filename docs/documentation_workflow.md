# Documentation and Architecture Contribution Workflow

Documentation and architecture assets in this repository follow the same Git-based
review cadence. Treating words, diagrams, and architectural models as code keeps
knowledge traceable and guarantees that reviewers see the complete change in one
pull request.

## End-to-end workflow

1. **Create a feature branch.** Group documentation, ADR updates, Structurizr or
   CALM model changes, and supporting automation tweaks into a single branch so the
   history clearly states why the change exists.
2. **Update the relevant artefacts.** Edit the Markdown chapter, ADR, diagram source
   (`.mmd`), or automation script inside the `docs/` directory. Provide context in the
   commit message that links the change back to the decision or issue.
3. **Run local validation.** Execute `python3 generate_book.py` followed by
   `docs/build_book.sh` to regenerate outputs. The command chain exercises diagram
   rendering and ensures MkDocs, Pandoc, and Eisvogel templates all parse the update.
4. **Submit a pull request for review.** Push the branch and open a pull request so the
   Git history captures discussion, inline comments, and approvals. Reference the
   architecture or documentation issue to maintain traceability.
5. **Address review feedback.** Refine the change set based on reviewer comments and
   ensure follow-up commits remain on the same branch so the timeline stays coherent.
6. **Verify automation status.** Confirm the `Content Validation Tests` workflow passes.
   It enforces heading capitalisation, link formatting, and structural rules for Markdown
   chapters alongside technical accuracy checks.
7. **Merge with confidence.** Once approvals are recorded and automation is green, merge
   the pull request. The unified workflow keeps ADRs, diagrams, and narrative content
   aligned without relying on ad-hoc wikis.

## Referencing the workflow in ADRs

Architecture Decision Records must link to this workflow in their **Review and
Documentation Workflow** section. Doing so reminds contributors that every decision
is captured through Git-based discussions and automation-backed validation before it
becomes part of the canonical architecture history.

## Contribution checklist

- [ ] Branch created from `main` with a descriptive name (for example,
      `docs/adr-observability-2025`).
- [ ] Markdown, diagrams, and configuration files updated together in the branch.
- [ ] Local validation run: `python3 generate_book.py && docs/build_book.sh`.
- [ ] Pull request references the originating issue or ADR.
- [ ] Content Validation workflow reports success (no heading or link formatting
      violations).
- [ ] ADRs and contribution notes link back to this document to reinforce the
      shared workflow.
