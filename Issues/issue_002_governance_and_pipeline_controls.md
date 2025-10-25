# Strengthen Governance and Pipeline Controls with Verified Sources

## Source IDs
- [5] GitLab. "Documentation as Code: Best Practices and Implementation." GitLab Documentation, 2024.
- [6] GitHub Docs. "About protected branches." https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/about-protected-branches.
- [7] Open Policy Agent. "Policy as Code Overview." https://www.openpolicyagent.org/docs/latest/.
- [8] HashiCorp. "Terraform Security Best Practices." HashiCorp Learning Resources, 2023. https://developer.hashicorp.com/terraform/cloud-docs/recommended-practices/security.

## Relevant Manuscript Sections
- `11_governance_as_code.md` – describe protected branch and policy-as-code enforcement patterns with direct citations.
- `23_soft_as_code_interplay.md` – connect software governance controls to Infrastructure as Code safeguards using the listed references.
- `09a_security_fundamentals.md` – reinforce security baselines derived from Terraform guidance.
- `09b_security_patterns.md` – expand the operational implications of the policy and security sources.

## Problem Statement
Current governance chapters reference these sources but fail to show how protected branches, policy evaluation, and Terraform hardening complement one another. Without this cross-link, the narrative underplays how Architecture as Code harmonises platform and security controls. Editors have requested clearer mapping between governance artefacts and the cited vendor practices.

## Acceptance Criteria
- Governance content explicitly links GitLab documentation to repository workflow controls.
- GitHub protected branch guidance is summarised within the governance as code chapter with a citation.
- OPA and HashiCorp security sources are used to illustrate automated guardrails across chapters 9 and 23.
- The prose clearly states how documentation-as-code practices interact with security automation in British English.

## Recommended Labels
- governance
- security
- dev
