# Issue: Clarify AaC vs IaC repository boundaries and contracts via Git

**Summary**
Chapter 3 and the automation chapter highlight the layered responsibilities of AaC (guardrails, policies, models) vs IaC (execution artefacts). We should formalise the Git “contract”: separate repositories, versioned interfaces, and consumption patterns.

**Why**
Prevents drift, preserves governance signals, and lets IaC consume approved patterns cleanly.

**Scope**
- Define “published” AaC artefacts and their versioning scheme.
- Consumption pattern for IaC repositories (as modules/templates/blueprints).
- Validation gates: PR checks ensure IaC only uses approved versions.

**References**
- Chapter 3 (“Abstraction and governance responsibilities…”), and Chapter 5 cross-references to version control.

**Acceptance Criteria**
- [ ] Spec for AaC release process (tags, changelog, semver).
- [ ] Example IaC repository that imports a tagged AaC package.
- [ ] PR check that blocks unapproved/unstable AaC references.

Sources: Chapter 3; Chapter 5 (Automation) cross-reference to version control.
