# Issue: Standardise repository structure and module layout for AaC

**Summary**
Chapter 3 outlines expectations for code organisation and module structure to keep larger AaC projects maintainable. We need a standard layout (folders, naming, module boundaries) and a starter template.

**Why**
Consistent layout reduces cognitive load, speeds reviews, and supports reuse across environments.

**Scope**
- Define a top-level structure for AaC models, ADRs, governance policies, diagrams, and IaC consumers.
- Provide a template repository with examples and Makefile/tasks.

**References**
- Site: “Code organisation and module structure” section.

**Acceptance Criteria**
- [ ] Published repository template with folders for `aac/`, `adr/`, `governance/`, `docs/`, `images/`, `iac/consumers/`.
- [ ] README explains each folder and how it links to PR checks.
- [ ] Example module with inputs/outputs and versioning policy.

Source: Chapter 3.
