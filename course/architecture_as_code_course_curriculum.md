# Architecture as Code Course Curriculum

## Course purpose and structure
This instructor-led curriculum translates the *Architecture as Code* book into a practical learning journey for enterprise arc
hitects, platform engineers, security leads, and delivery managers. The course uses the Architecture as Code maturity radar ques
tions as continuous checkpoints so that participants can benchmark their organisations, surface gaps, and prioritise improvemen
ts after every module.

- **Format:** Blended delivery across workshops, labs, and asynchronous assignments.
- **Duration:** Ten modules delivered over ten weeks (2.5 hour live session + 1 hour self-study per module).
- **Cohort profile:** Cross-functional teams of six to twelve practitioners who influence architecture, governance, compliance, 
and platform delivery.
- **Primary artefacts:** Radar self-assessments, module workbooks, version-controlled exercises, and organisational action plans.

## Delivery approach grounded in the maturity radar
1. **Initial baseline (Module 0):** Each participant completes the full radar checklist and identifies a priority aspect in whic
h their organisation scores lowest. These findings shape personalised learning goals.
2. **Module cadence:** Every module revisits the radar questions for the featured discipline. Learners record their maturity stag
e, supporting evidence, and blockers.
3. **Progressive commitments:** Participants document one tangible improvement experiment per module that will raise the radar sc
ore by at least one point.
4. **Closing review:** The final session re-runs the full radar, analyses score deltas, and captures lessons learned alongside ac
tion plans for the next quarter.

## Module overview
Each module references the book chapters that provide core reading plus related maturity radar questions. Facilitators should st
art with the radar prompts to frame why the module matters, then explore the referenced chapters before moving into discussion a
nd hands-on practice.

### Module 0 – Orientation and radar benchmarking
- **Chapters:** 01 Introduction, 02 Fundamental Principles, 24 Best Practices, 27 Conclusion.
- **Learning objectives:**
  - Explain the Architecture as Code philosophy and the value of codifying architecture, policy, and culture.
  - Establish baseline maturity using the radar checklist across all aspects.
  - Prioritise target disciplines based on observed capability gaps.
- **Radar prompts:** Review the entire checklist to identify the two weakest disciplines and the evidence behind those ratings.
- **Activities:** Facilitate a guided radar completion workshop, capture current tools and processes, and agree on cohort norms f
or collaboration.

### Module 1 – Infrastructure as code foundations
- **Chapters:** 05 Automation, DevOps, and CI/CD; 07 Containerisation; 13 Testing Strategies.
- **Learning objectives:**
  - Design declarative infrastructure delivery pipelines with automated validation.
  - Map radar questions on version control, drift detection, and reusable modules to current IaC practices.
  - Plan iterative improvements for environments that still rely on manual deployment steps.
- **Radar prompts:** Focus on questions covering peer review, automated validation, declarative deployments, reusable modules, an
d drift detection.
- **Activities:** Compare Terraform and Pulumi workflows, review drift detection tooling, and draft a pull-request checklist that
 embeds radar expectations.

### Module 2 – Architecture as code modelling
- **Chapters:** 06 Structurizr, 23 Soft as Code Interplay, 31 Technical Architecture.
- **Learning objectives:**
  - Generate C4 or Structurizr DSL models from source-controlled definitions.
  - Maintain traceability between architecture models, owning teams, and decision records.
  - Automate model validation and synchronise diagrams with documentation outputs.
- **Radar prompts:** Examine questions on model generation, change synchronisation, traceability, decision capture, and automati
c validation.
- **Activities:** Build a Structurizr DSL workspace, integrate architecture decision records, and configure automated linting for
 model consistency.

### Module 3 – Containerisation and orchestration at scale
- **Chapters:** 07 Containerisation, 08 Microservices, 14 Practical Implementation.
- **Learning objectives:**
  - Codify container build pipelines, security scans, and publication workflows.
  - Define declarative orchestration manifests with tested rollout strategies.
  - Deliver runtime configuration and secrets through code-first mechanisms.
- **Radar prompts:** Address questions on version-controlled definitions, automated image pipelines, declarative cluster configu
ration, tested rollouts, and codified runtime settings.
- **Activities:** Run a Kubernetes deployment lab, compare blue-green vs canary rollouts, and automate secret rotation using tool
s such as Sealed Secrets or External Secrets Operator.

### Module 4 – Policy as code and security automation
- **Chapters:** 09a Security Fundamentals, 09b Security Patterns, 09c Risk and Threat as Code, 10 Policy and Security.
- **Learning objectives:**
  - Translate governance requirements into machine-readable policies enforced in CI/CD.
  - Integrate security telemetry to drive policy updates and automated remediation.
  - Apply radar prompts to evaluate policy peer review, enforcement, alerting, and feedback loops.
- **Radar prompts:** Review questions on policy storage in version control, automated enforcement, peer review, alert surfacing,
 and adaptive feedback.
- **Activities:** Create Open Policy Agent or Sentinel rules, implement pull-request checks, and simulate policy violation handli
ng with actionable runbooks.

### Module 5 – Governance as code operations
- **Chapters:** 11 Governance as Code, 19 Management as Code, 17 Organisational Change.
- **Learning objectives:**
  - Codify governance workflows, approval rules, and decision rationale in repositories.
  - Enable non-developers to interact with governance tooling through templates and guided interfaces.
  - Use radar prompts to identify gaps in testing, exception handling, and accessibility of governance automations.
- **Radar prompts:** Analyse questions on codified approvals, decision history capture, lower-environment testing, automated exce
ption tracking, and inclusive tooling.
- **Activities:** Configure repository protection policies, design governance templates for new initiatives, and rehearse excepti
on escalation paths.

### Module 6 – Compliance as code evidence flows
- **Chapters:** 12 Compliance, 15 Evidence as Code, 34 Control Mapping Matrix Template.
- **Learning objectives:**
  - Automate regulatory control execution and evidence capture.
  - Maintain reusable compliance baselines mapped to standards and frameworks.
  - Integrate issue tracking with compliance findings for traceable remediation.
- **Radar prompts:** Consider questions on continuous control execution, reusable baselines, automated evidence storage, integra
 ted remediation, and reporting cadences.
- **Activities:** Build a compliance-as-code pipeline using frameworks such as Conformity or AWS Audit Manager, and pilot an auto
mated evidence repository using version-controlled artefacts.

### Module 7 – Testing as code for resilient platforms
- **Chapters:** 13 Testing Strategies, 05 Automation, DevOps, and CI/CD, 16 Migration.
- **Learning objectives:**
  - Define multi-layered testing (unit, integration, security, compliance) for architecture-as-code artefacts.
  - Implement chaos and resilience testing aligned to radar prompts.
  - Manage synthetic and production-like test data using code-based pipelines.
- **Radar prompts:** Explore questions covering automated test definition, pipeline execution, coverage monitoring, chaos testing
, and test data management.
- **Activities:** Create a test matrix for architecture artefacts, configure automated chaos experiments, and build reusable data
 seeding scripts.

### Module 8 – Documentation, knowledge, and culture as code
- **Chapters:** 22 Documentation vs Architecture, 23 Soft as Code Interplay, 18 Team Structure, 17 Organisational Change.
- **Learning objectives:**
  - Publish living documentation using Markdown, diagram automation, and CI/CD builds.
  - Capture organisational knowledge, rituals, and onboarding journeys as code-backed playbooks.
  - Apply radar prompts to evaluate documentation pipelines, knowledge governance, and cultural automation.
- **Radar prompts:** Review questions on version-controlled documentation, automated builds, definition-of-done updates, automate
d diagram generation, quality checks, knowledge capture, onboarding playbooks, continuous retrospectives, cultural tooling, and 
review cadences.
- **Activities:** Build a documentation publishing pipeline, design an onboarding playbook, and configure automated reminders for
 knowledge reviews.

### Module 9 – Management as code and adaptive operating models
- **Chapters:** 19 Management as Code, 20 AI Agent Team, 21 Digitalisation, 31 Technical Architecture.
- **Learning objectives:**
  - Encode leadership ceremonies, portfolio reviews, and staffing models as automated workflows.
  - Instrument metrics and dashboards that provide timely decision support.
  - Iterate management playbooks through pull requests with leadership participation.
- **Radar prompts:** Focus on questions covering documented operating models, standardised ceremonies, automated metrics, codifie
d resource allocation, and collaborative playbook iteration.
- **Activities:** Prototype a management dashboard pipeline, create standard agendas generated from code, and rehearse leadership
 pull-request reviews.

### Module 10 – Optimisation, AI assistance, and future readiness
- **Chapters:** 20 AI Agent Team, 25 Future Trends, 26 AaC Anti-Patterns, 26 Prerequisites for AaC, 27 Conclusion.
- **Learning objectives:**
  - Evaluate how AI augments architecture and governance, and anticipate emerging practices.
  - Recognise anti-patterns that inhibit progression to levels four and five of the maturity model.
  - Formulate a 90-day roadmap aligned to radar improvements and strategic priorities.
- **Radar prompts:** Consolidate insights across all disciplines, emphasising AI-assisted optimisation, self-healing, and innovat
ive governance models.
- **Activities:** Conduct an AI-enabled scenario planning workshop, analyse anti-pattern case studies, and draft strategic object
ives for the next maturity level.

## Assessment strategy
- **Formative assessments:** Weekly reflection logs mapping radar scores to observed changes, plus peer reviews of lab artefacts.
- **Summative assessments:**
  1. A capstone action plan that details maturity improvements for the next quarter, referencing evidence for score changes.
  2. A live presentation in Module 10 summarising radar evolution, key experiments, and organisational impact.
- **Certification criteria:** Minimum 20% improvement in at least three radar disciplines, completion of all lab artefacts in ver
sion control, and facilitator sign-off on the capstone presentation.

## Facilitator guidance
- Start each module by reviewing the previous week’s radar deltas; celebrate quick wins and examine blockers.
- Encourage teams to store all coursework in a shared repository so that maturity evidence remains auditable.
- Use breakout sessions to compare maturity journeys across teams, sparking cross-pollination of practices.
- Monitor language for British English consistency in all submitted artefacts, aligning with the editorial style guide.
- Close the programme by co-authoring a shared retrospective that records lessons learned, next experiments, and ownership of f
ollow-up actions.

## Curriculum audit confirmation

- The module-to-chapter mapping was reconfirmed during the latest curriculum audit: every chapter listed in Modules 0–10 has an active counterpart in the `docs/` directory, including Module 0 readings (**01 Introduction**, **02 Fundamental Principles**, **24 Best Practices**, **27 Conclusion**) and Module 7 references (**05 Automation, DevOps, and CI/CD**, **13 Testing Strategies**, **16 Migration**).【F:docs/01_introduction.md†L1-L151】【F:docs/02_fundamental_principles.md†L1-L147】【F:docs/24_best_practices.md†L1-L133】【F:docs/27_conclusion.md†L1-L125】【F:docs/05_automation_devops_cicd.md†L1-L184】【F:docs/13_testing_strategies.md†L1-L203】【F:docs/16_migration.md†L1-L206】
- Continue to update the curriculum file in tandem with new or renamed chapters so that facilitators and learners can rely on a single source of truth for pre-reading assignments.【F:docs/05_automation_devops_cicd.md†L1-L184】【F:docs/13_testing_strategies.md†L1-L203】【F:docs/16_migration.md†L1-L206】
