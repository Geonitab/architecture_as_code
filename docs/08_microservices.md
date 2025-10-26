# Microservices Architecture as Code

## Introduction

Microservices architectures decompose business capabilities into independent services that can be planned, deployed, and evolved without synchronising every change across the entire estate. When coupled with Architecture as Code disciplines, microservices become observable, governable, and automatable. Source-controlled blueprints describe how services interact, how they are deployed, and which policies keep them trustworthy. This chapter explains how to weave Architecture as Code practices through microservice estates so that autonomy never undermines cohesion.

![Microservices operating model](images/diagram_08_chapter7.png)

## Architectural principles for federated teams

### Bounded contexts mapped to repositories

Treat each microservice as a bounded context with a clearly defined purpose, data contract, and operational envelope. Store the service's architecture definition beside its application code and IaC modules so that diagrams, infrastructure manifests, and compliance evidence travel together. Repository templates keep ownership information, on-call details, and dependency declarations consistent.

### Contract-first integration

Microservices thrive when interfaces are stable and well documented. Declare API specifications and event schemas as code (for example using OpenAPI or AsyncAPI) and register them in an architecture catalogue. Automated linting confirms that proposed changes respect backwards compatibility rules and alerts the owning teams when downstream consumers would break.

### Golden paths backed by reusable modules

Autonomous teams still need consistent guardrails. Provide shared Terraform modules, Kubernetes Helm charts, and service mesh policies that encode approved defaults for security, observability, and networking. Architecture as Code pipelines should verify that each service consumes the authorised modules and that deviations are reviewed through architecture decision records.

## Designing microservices with Architecture as Code assets

### Structuring repositories

A reference repository might include:

```text
./service
├── adr/                              # Architecture decision records
├── deployment/
│   ├── helm/
│   │   └── values.yaml               # Environment-specific overlays
│   ├── terraform/                    # Infrastructure definitions
│   └── policies/                     # OPA and service mesh policies
├── docs/
│   ├── context-diagram.mmd           # C4 diagrams under version control
│   └── runbooks/
│       └── resilience-playbook.md
├── service_contracts/
│   ├── api.yaml                      # OpenAPI definition
│   └── events/
│       └── order-created.json
└── src/
    └── ...
```

Architecture automation can parse this layout to build inventories, check dependency rules, and publish updated diagrams after every merge.

### Policy-aware delivery pipelines

CI/CD workflows should orchestrate both application tests and architectural conformance checks. A representative GitHub Actions job might combine security scans, contract validation, Terraform plan approval, and deployment orchestration:

```yaml
jobs:
  validate-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate architecture contracts
        run: |
          npm install -g @redocly/cli
          redocly lint service_contracts/api.yaml
      - name: Verify Terraform plan
        working-directory: deployment/terraform
        run: |
          terraform init -backend-config=env.tfbackend
          terraform plan -out=tfplan
      - name: Enforce policy guardrails
        run: |
          conftest test deployment/policies
      - name: Deploy via Helmfile
        run: |
          helmfile apply --environment=${{ github.ref_name }}
```

Such pipelines capture the architectural intent, flag drift immediately, and keep every service aligned with centrally defined guardrails.

### Runtime observability as code

Codify dashboards, alerting policies, and runbooks so that operability remains consistent across the fleet. Use tools such as Grafana configuration as code or Prometheus recording rules stored in Git. Tie alert routing to the ownership data held in each service repository so incidents reach the responsible team.

## Coordinating shared capabilities

### Service mesh and networking patterns

Architecture as Code enables platform teams to encode networking standards once and distribute them to every service. Istio, Linkerd, or AWS App Mesh policies can be generated from declarative manifests that specify identity requirements, mutual TLS expectations, and traffic routing rules. When services declare their intents, platform pipelines merge them with organisation-wide defaults to produce consistent yet flexible mesh configurations.

### Data management across domains

Avoid accidental monoliths by defining data ownership and access rules programmatically. Each microservice should publish read models or event streams that others consume through documented interfaces. Architecture as Code repositories can generate data lineage diagrams showing where authoritative data resides, who can access it, and how retention rules are enforced. Automated tests verify that only sanctioned services connect to sensitive datasets.

Establish the Structurizr-defined retention baseline as the shared starting
point: 90 days for active operational data and seven years for archived records.
Chapter&nbsp;6 codifies those values so that platform tooling, policy engines, and
service teams speak the same language. Domain teams may extend the retention
window when classifications such as "financial" or "health" demand stricter
handling, yet they must never reduce it without a formal exception reviewed by
the data governance council. Recording that decision within the service
repository keeps the automation story coherent.

```hcl
locals {
  retention_by_classification = {
    "baseline"   = { active_days = 90, archive_years = 7 }
    "financial"  = { active_days = 90, archive_years = 7 } # aligns with baseline, audit ready
    "confidential" = { active_days = 120, archive_years = 7 } # stricter due to classification
  }
}

module "order_storage" {
  source                 = "../modules/storage"
  classification         = var.data_classification
  default_retention      = local.retention_by_classification["baseline"]
  classification_override = lookup(local.retention_by_classification, var.data_classification, null)
}
```

Linking the local overrides back to the shared Structurizr configuration keeps
compliance automation consistent across the landscape and ensures auditors can
trace every microservice back to the canonical policy.

### Compliance by default

Regulatory expectations such as GDPR, PCI DSS, or sector-specific rules are easier to satisfy when encoded as reusable policies. Combine static analysis (for example, checking that logging excludes personal data) with dynamic controls (service mesh policies enforcing encryption in transit). Architecture guardrails should produce compliance reports automatically so stakeholders can evidence adherence without manual document assembly.

## Operating microservices estates sustainably

### Observability driven feedback loops

Collect metrics, traces, and logs into a shared telemetry platform. Architecture as Code ensures that each service exports consistent labels, making it straightforward to build cross-service dashboards. Feedback loops then inform capacity planning, resilience improvements, and disaster recovery rehearsals.

### Resilience testing as code

Define failure injection experiments alongside service definitions. Tools such as Chaos Mesh or Gremlin can be orchestrated via IaC pipelines to introduce latency, kill pods, or revoke permissions. Document expected outcomes and recovery steps within the same repository so that continuous verification becomes routine rather than exceptional.

### Cost and sustainability metrics

Automate reporting on resource consumption, carbon intensity, and idle workloads. When services codify budgets and scaling thresholds, platform automation can alert owners when utilisation deviates from expected norms. Embedding sustainability objectives into Architecture as Code keeps environmental considerations visible during design and runtime.

## Migration considerations

Many organisations evolve from monoliths or service-oriented architectures. Architecture as Code accelerates this journey by:

- Capturing target service boundaries as executable diagrams.
- Providing repeatable infrastructure templates for each new domain.
- Automating shadow traffic, data replication, and phased cut-overs.
- Documenting decommission plans for legacy components.

By treating migration playbooks as code, teams can rehearse transitions safely and roll back confidently when experiments expose new risks.

## Summary

Microservices amplify organisational agility when paired with disciplined automation. Architecture as Code gives leaders a shared source of truth for service contracts, platform guardrails, and operational posture. Investing in reusable templates, policy automation, and comprehensive observability enables teams to innovate quickly whilst preserving the resilience, compliance, and sustainability that modern enterprises demand.