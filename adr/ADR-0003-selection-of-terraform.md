---
adr_id: ADR-0003
title: Selection of Terraform for Architecture as Code
status: Accepted
date: "2023-01-12"
last_reviewed: "2024-11-15"
next_review_due: "2025-05-15"
deciders:
  - Architecture Steering Council
  - Platform Reliability Guild
reviewers:
  - Alice Patel
  - Gustav Lindström
  - Priya Banerjee
related_chapters:
  - docs/04_adr.md
  - docs/05_automation_devops_cicd.md
  - docs/06_structurizr.md
related_diagrams:
  - docs/images/diagram_04_adr_process.png
  - docs/images/diagram_04_adr_lifecycle.png
related_backlog_items:
  - AAC-1182
  - AAC-1305
summary: Terraform standardises multi-cloud infrastructure for the Architecture as Code platform whilst enabling British English compliant policy automation.
automation_hooks:
  - Terraform plan enforcement integrated with the governance-as-code pipeline.
  - Policy-as-code checks ensure mandatory tagging and remote state controls remain enabled.
change_notes:
  - 2024-11-15 – Review confirmed remote state encryption controls are functioning and no successor ADR is required yet.
---

# Decision

Adopt HashiCorp Terraform as the strategic Infrastructure as Code tool for implementing the Architecture as Code operating model. Terraform’s provider ecosystem, mature state handling, and compatibility with policy enforcement frameworks allow the platform teams to codify infrastructure, compliance, and security standards without diverging across cloud estates.

# Context

Prior to this decision, teams managed AWS and Azure workloads through bespoke scripts and ad-hoc console operations. The inconsistency produced fragile environments, limited observability, and protracted audit preparation. Multiple delivery squads experimented with different IaC frameworks, increasing the risk of knowledge silos and inconsistent governance. The Architecture as Code initiative required a common foundation that respected existing investments whilst raising the automation baseline.

# Decision Drivers

- Multi-cloud parity to support both AWS and Azure product lines.
- First-class policy integration so architectural guardrails are enforced automatically.
- Strong ecosystem support for Terragrunt, Atlantis, and automated change approvals.
- Ability to integrate with Structurizr diagrams to document platform topology changes alongside ADRs.

# Consequences

- **Positive**
  - Consistent remote state encryption and versioned state back-ups across environments.
  - Shared module registry reduces duplicated infrastructure patterns.
  - Terraform plans provide audit-ready change evidence that links directly to ADR metadata.
- **Negative**
  - Teams must invest in Terraform training and migrate away from home-grown scripts.
  - Upgrade cadence needs central coordination to avoid provider drift.

# Follow-up Actions

- Align backlog items AAC-1182 and AAC-1305 with the migration plan outlined in `docs/adr/migration_plan.md`.
- Extend the Structurizr workspace example in Chapter 6 to reference Terraform modules tagged with this ADR identifier.
- Monitor the policy-as-code checks recorded in the automation pipeline to ensure exceptions are documented through successor ADRs when required.
