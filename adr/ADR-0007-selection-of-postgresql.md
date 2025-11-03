---
adr_id: ADR-0007
title: Selection of PostgreSQL for the Primary Database
status: Accepted
date: "2023-03-04"
last_reviewed: "2024-10-02"
next_review_due: "2025-04-02"
deciders:
  - Data Services Forum
  - Architecture Steering Council
reviewers:
  - Elena Kowalski
  - Michael Onwudiwe
related_chapters:
  - docs/04_adr.md
  - docs/08_microservices.md
  - docs/15_cost_optimization.md
related_diagrams:
  - docs/images/diagram_04_adr_structure.png
related_backlog_items:
  - AAC-1224
  - DATA-947
summary: PostgreSQL anchors transactional workloads for the multi-tenant platform, aligning ADR guidance with resilience and cost optimisation chapters.
automation_hooks:
  - Database migration pipelines annotate change logs with the ADR identifier.
  - Observability dashboards surface ADR review dates in the data platform status page.
change_notes:
  - 2024-10-02 – Added operational readiness checklist and updated observability automation references.
---

# Decision

Standardise on managed PostgreSQL services for all primary transactional workloads within the Architecture as Code platform. PostgreSQL’s extensibility, replication options, and community tooling provide a balance between reliability and flexibility whilst integrating smoothly with the automated governance controls mandated across the estate.

# Context

The programme previously relied on a mixture of MySQL, SQL Server, and ad-hoc document stores. The inconsistency complicated cross-domain reporting and created unnecessary operational risk. The Architecture as Code principles require a coherent data backbone that can be managed, versioned, and observed as code alongside infrastructure modules and ADR metadata.

# Key Considerations

- Native support for JSON, geospatial data, and advanced indexing to cover diverse product requirements.
- Compatibility with managed services (Amazon RDS, Azure Database for PostgreSQL) for automated patching and backups.
- Alignment with cost optimisation narratives in Chapter 15 through storage tiering and read replica strategies.
- Strong ecosystem for migration tooling, including Sqitch and Liquibase integrations with CI pipelines.

# Consequences

- **Positive**
  - Simplified operational model with standard backup, retention, and encryption controls.
  - Unified observability dashboards referencing ADR-0007 to contextualise latency or failover alerts.
  - Easier data governance audits because schema migrations are linked to ADR metadata.
- **Negative**
  - Specialist teams using niche database features require exceptions backed by successor ADRs.
  - Training investment required for squads transitioning from SQL Server stored procedure heavy workloads.

# Mitigations

- Provide migration runbooks that map SQL Server constructs to PostgreSQL equivalents.
- Extend the cost modelling accelerators in Chapter 15 to include PostgreSQL reserved instance guidance.
- Capture exceptions in backlog item DATA-947 so review cadences align with `docs/adr/adr_catalogue.md` and the automation dashboards.
