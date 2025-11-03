# Architecture Decision Record Catalogue {#adr-catalogue}

This catalogue is generated from the structured ADR metadata committed to the repository. It keeps the documentation site, book manuscript, and automation backlog aligned by ensuring every referenced ADR includes links to chapters, diagrams, and delivery work items.

## Summary overview

| ADR | Title | Status | Linked chapters | Backlog items | Next review |
| --- | ----- | ------ | --------------- | ------------- | ----------- |
| ADR-0003 | Selection of Terraform for Architecture as Code | Accepted | docs/04_adr.md<br>docs/05_automation_devops_cicd.md<br>docs/06_structurizr.md | AAC-1182<br>AAC-1305 | 2025-05-15 |
| ADR-0007 | Selection of PostgreSQL for the Primary Database | Accepted | docs/04_adr.md<br>docs/08_microservices.md<br>docs/15_cost_optimization.md | AAC-1224<br>DATA-947 | 2025-04-02 |

## Detailed records

### ADR-0003 – Selection of Terraform for Architecture as Code

Terraform standardises multi-cloud infrastructure for the Architecture as Code platform whilst enabling British English compliant policy automation.

**Status:** Accepted — initial decision recorded on 2023-01-12.
**Review cadence:** Last reviewed on 2024-11-15; next review due 2025-05-15.

**Deciders:** Architecture Steering Council, Platform Reliability Guild
**Reviewers:** Alice Patel, Gustav Lindström, Priya Banerjee

**Linked chapters**
- `docs/04_adr.md`
- `docs/05_automation_devops_cicd.md`
- `docs/06_structurizr.md`

**Supporting diagrams**
- `docs/images/diagram_04_adr_process.png`
- `docs/images/diagram_04_adr_lifecycle.png`

**Backlog alignment**
- AAC-1182
- AAC-1305

**Automation hooks**
- Terraform plan enforcement integrated with the governance-as-code pipeline.
- Policy-as-code checks ensure mandatory tagging and remote state controls remain enabled.

**Change log**
- 2024-11-15 – Review confirmed remote state encryption controls are functioning and no successor ADR is required yet.

### ADR-0007 – Selection of PostgreSQL for the Primary Database

PostgreSQL anchors transactional workloads for the multi-tenant platform, aligning ADR guidance with resilience and cost optimisation chapters.

**Status:** Accepted — initial decision recorded on 2023-03-04.
**Review cadence:** Last reviewed on 2024-10-02; next review due 2025-04-02.

**Deciders:** Data Services Forum, Architecture Steering Council
**Reviewers:** Elena Kowalski, Michael Onwudiwe

**Linked chapters**
- `docs/04_adr.md`
- `docs/08_microservices.md`
- `docs/15_cost_optimization.md`

**Supporting diagrams**
- `docs/images/diagram_04_adr_structure.png`

**Backlog alignment**
- AAC-1224
- DATA-947

**Automation hooks**
- Database migration pipelines annotate change logs with the ADR identifier.
- Observability dashboards surface ADR review dates in the data platform status page.

**Change log**
- 2024-10-02 – Added operational readiness checklist and updated observability automation references.

---
*Generated automatically via `python3 scripts/generate_adr_catalogue.py`. Do not edit manually.*
