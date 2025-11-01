# Risk as Code and Threat Handling as Code {#chapter-risk-and-threat-modelling}

*Risk management is often treated as a paperwork exercise. When executed as code it becomes measurable, testable, and continuously enforceable across every environment.*

## Why risk and threat handling belong in the codebase

Architecture as Code programmes already encode infrastructure, policy, and security controls. Extending the repository to cover risk registers and threat playbooks makes the entire resilience posture transparent and repeatable.

- **Traceability:** Risk statements, controls, and compensating actions live alongside the architecture components they cover, enabling precise linkage during audits.
- **Consistency:** Automated pipelines evaluate risk criteria in the same way every time, removing subjective scoring and ensuring all platforms meet minimum thresholds.
- **Speed:** Codified playbooks trigger as soon as telemetry indicates a hazard, delivering sub-minute responses instead of waiting for manual coordination.
- **Learning loops:** Post-incident reviews generate pull requests that refine controls or playbooks, creating a living body of knowledge.

## Engineering a risk-as-code model

### Domain-driven risk definitions

Structure risk definitions as declarative YAML or JSON documents that capture context, probability, impact, and ownership. Version control provides historical records of changing assumptions and facilitates independent review. Treat the schema as a contract that automated tooling validates during pull requests.

```yaml
id: RISK-0047
category: platform-resilience
statement: "Loss of regional database cluster availability disrupts customer journeys"
likelihood: high
impact: critical
control_refs:
  - terraform://modules/database/ha_cluster
  - policy://runbooks/failover
risk_owner: payments-site-reliability
review_cadence: quarterly
```

Store the schema definition in the repository and validate each risk document through CI checks. Rejections for missing data, outdated review dates, or invalid owners prevent stale artefacts entering the main branch.

### Quantifying controls with metrics as code

Link each risk to observable metrics managed as code. Prometheus alerts, Azure Monitor queries, or AWS CloudWatch alarms can be generated from the same repository, providing consistent evidence of control health. A failing metric should fail the pipeline, forcing remediation before release.

### Automating approvals and exceptions

Embed governance logic within policy-as-code engines such as Open Policy Agent or HashiCorp Sentinel. For example, deployments may only proceed when every high or critical risk is either mitigated by automated controls or accompanied by a time-bound exception. Exceptions themselves become code artefacts with explicit expiry dates and approval chains, ensuring ongoing scrutiny.

## Threat handling as code

### Codified threat intelligence ingestion

Threat handling begins by ingesting intelligence feeds in structured formats like STIX/TAXII. Use scheduled pipelines to fetch indicators of compromise, normalise them, and publish curated sets to security tooling. Encoding this workflow ensures provenance is auditable and sanitisation routines are consistent.

### Automated threat modelling

Model systems with tools such as the Threat Modelling Manifesto or Microsoft Threat Modelling Tool, but generate the models directly from the codebase. Diagrams and attack trees stored as Mermaid or Structurizr files can be regenerated whenever architecture code changes. Automated validation checks for missing trust boundaries, unclassified data stores, or unmitigated STRIDE categories.

### Response playbooks expressed as state machines

Represent incident response actions as state machines or workflow definitions (for example AWS Step Functions, Azure Logic Apps, or Temporal workflows). Each state corresponds to a containment or eradication step, complete with guard conditions, rollback logic, and evidence capture. Playbooks should:

1. **Subscribe** to signals from SIEM platforms or anomaly detection pipelines.
2. **Assess** risk ratings automatically by referencing the risk-as-code repository.
3. **Act** by triggering infrastructure changes, such as revoking credentials, isolating workloads, or rotating keys.
4. **Document** activities by writing to immutable logs and creating collaboration tickets.

### Exercising playbooks continuously

Adopt security chaos engineering techniques—automated scenarios that inject simulated breaches or infrastructure failures. These drills run on schedules or in response to configuration changes, validating that playbooks execute correctly and risk tolerances remain aligned. Findings become new backlog items captured as code changes, closing the loop between detection and improvement.

## Integrating with the delivery pipeline

- **Pull request templates** require authors to link risk IDs and threat model references for each change, ensuring architectural adjustments consider their resilience impact.
- **Continuous integration** stages lint risk definitions, execute policy-as-code checks, and run synthetic attack simulations against ephemeral environments.
- **Continuous delivery** gates verify that all mitigations and response automations passed their most recent chaos drill, preventing regressions from reaching production.
- **Observability dashboards** pull directly from the code-defined risk catalogue, highlighting coverage gaps and upcoming review cadences.

## Operating model considerations

- **Ownership:** Assign product-aligned risk stewards who approve updates via code reviews, ensuring accountability remains close to the delivery teams.
- **Skills:** Upskill engineers in threat modelling, security automation, and regulatory expectations so they can interpret results and iterate safely.
- **Tooling alignment:** Integrate security platforms through APIs and infrastructure-as-code modules, avoiding manual portal configurations that drift from the source of truth.
- **Culture:** Celebrate the remediation pull request—not just the discovery. Treat risk and threat artefacts as first-class code assets subject to the same engineering rigour as application releases.

By encoding risk assessments and threat handling in the repository, organisations attain a defensible, adaptive security posture. Evidence of control effectiveness is generated continuously, response actions are reliable, and every change builds upon an auditable foundation of codified resilience.
