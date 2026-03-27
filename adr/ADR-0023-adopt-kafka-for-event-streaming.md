---
adr_id: ADR-0023
title: Adopt Kafka for Event Streaming
status: Accepted
date: "2024-02-15"
last_reviewed: "2025-01-10"
next_review_due: "2025-07-10"
deciders:
  - Architecture Steering Council
  - Platform Reliability Guild
reviewers:
  - Alice Patel
  - Gustav Lindström
  - Elena Kowalski
related_chapters:
  - docs/02_fundamental_principles.md
  - docs/05_automation_devops_cicd.md
  - docs/08_microservices.md
related_diagrams:
  - docs/images/diagram_08_chapter6.png
related_backlog_items:
  - AAC-1420
  - PLAT-882
summary: Apache Kafka standardises the event streaming layer across the Architecture as Code platform, enabling decoupled service communication and auditable change propagation.
automation_hooks:
  - Kafka topic provisioning is managed via Terraform modules committed to the architecture repository.
  - Consumer group lag alerts are wired into the governance-as-code pipeline to surface drift in real time.
change_notes:
  - 2025-01-10 – Review confirmed topic retention policies align with compliance evidence retention requirements; no successor ADR required.
---

# Decision

Adopt Apache Kafka as the standard event streaming platform for all asynchronous service communication within the Architecture as Code platform. Kafka topic definitions, retention policies, and consumer group configurations shall be declared as code in the architecture repository and reviewed under the same ADR governance process as infrastructure changes.

# Context

As the Architecture as Code platform grew to span multiple bounded contexts—CI/CD automation, governance pipelines, evidence collection, and whitepaper generation—point-to-point integrations became a source of fragility. Services coupling directly to one another made it difficult to reason about data flow, trace the origin of changes, or replay events for audit purposes.

The programme's guiding principle of treating all architectural decisions as versioned, auditable artefacts extends naturally to the event bus. An event streaming platform that is itself provisioned as code closes the gap between "infrastructure as code" and "communication topology as code".

# Key Considerations

## Decoupled service communication

Kafka's publish-subscribe model allows producers and consumers to evolve independently. New consumers can be added to existing topics without modifying upstream services, supporting the incremental adoption approach described in Chapter 2.

## Auditability and replay

Kafka's persistent log provides an ordered, replayable record of every event. This property is essential for the evidence pipeline described in the Evidence as Code chapter: policy evaluation results, configuration snapshots, and control attestations can be replayed to reconstruct the compliance posture at any point in time.

## Operational observability

Consumer group lag is a first-class operational metric. By surfacing lag data through the governance-as-code pipeline, teams receive early warning of processing bottlenecks before they affect downstream audit or reporting workflows.

## Code-defined topology

Topic schemas, retention periods, replication factors, and ACLs are expressed as Terraform resources committed to the architecture repository. Changes pass through the standard pull-request review process, ensuring that communication topology decisions receive the same scrutiny as infrastructure changes.

# Alternatives Considered

| Alternative | Reason Rejected |
|---|---|
| RabbitMQ | Lacks durable log replay; unsuitable for evidence archival requirements |
| AWS SQS/SNS | Cloud-vendor lock-in conflicts with the multi-cloud portability principle |
| gRPC streaming | Point-to-point coupling; does not support multiple independent consumers per event |
| Redis Streams | Limited retention guarantees and weaker operational tooling for long-term audit trails |

# Consequences

- All new inter-service integrations shall use Kafka topics rather than direct API calls where asynchronous delivery is acceptable.
- Topic schemas shall be registered in the schema registry and treated as versioned artefacts.
- Teams adopting this ADR must provision consumer group lag dashboards as part of their onboarding checklist.
- Existing point-to-point integrations shall be migrated to Kafka topics on a schedule agreed with the Architecture Steering Council.
