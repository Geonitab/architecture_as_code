GitHub Issue: Governance Source Alignment

## Source IDs
- [1] AaC Open Source Project. – Architecture-as-Code Repository
- [10] GitHub Docs. – About protected branches
- [11] HashiCorp. – Policy as Code Overview
- [12] HashiCorp. – Securing Terraform State

## Relevant Manuscript Sections
- docs/11_governance_as_code.md
- docs/23_soft_as_code_interplay.md
- docs/09a_security_fundamentals.md

## Problem Statement
The governance narrative references protected branches and policy enforcement, yet the supporting guidance is scattered across chapters and misses a cohesive example that ties repository controls to Terraform policy enforcement. Without a curated update, readers cannot trace how governance tooling, IaC state security, and architectural guardrails reinforce each other.

## Acceptance Criteria
- [ ] Expand the governance chapter to link branch protection guidance with policy-as-code guardrails and Terraform state handling.
- [ ] Provide cross-references that guide readers from governance controls to the infrastructure security appendix.
- [ ] Add a short worked example demonstrating how repository policies trigger Terraform policy checks before merge.

## Recommended Labels
- documentation
- enhancement
