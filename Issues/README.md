# Architecture as Code Issue Catalogue

This directory curates ready-to-use GitHub issues that translate the book's guidance into actionable backlog items. Each issue references validated sources, links to the relevant manuscript chapters, and proposes labels to streamline triage.

## Issue Templates
- [issue_01_governance_and_security_alignment.md](issue_01_governance_and_security_alignment.md) – Establish cross-cloud governance, policy-as-code, and secure state backends.
- [issue_02_diagram_automation_enhancement.md](issue_02_diagram_automation_enhancement.md) – Automate Structurizr workflows and enforce diagram-review quality gates.
- [issue_03_documentation_and_adr_alignment.md](issue_03_documentation_and_adr_alignment.md) – Align ADR processes with documentation-as-code practices.
- [issue_04_testing_and_delivery_quality.md](issue_04_testing_and_delivery_quality.md) – Build comprehensive infrastructure testing pipelines and runbooks.

## Maintaining the Catalogue
- Keep `source_catalogue.json` updated whenever new authoritative references are added to docs/33_references.md.
- Ensure every issue template lists one or more Source IDs and that, in aggregate, the set covers every defined source.
- When adding a new issue file, update this README so the listing matches the files present in the directory.
