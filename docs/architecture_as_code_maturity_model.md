# Architecture as Code Maturity Model {#appendix-maturity-model}

## Maturity model for implementing architecture as code

Modern organisations are increasingly turning to **architecture as code (AaC)** to keep systems design, security and governance aligned with rapid delivery.  
The *Architecture as Code* book describes how codified representations of architecture, policy, governance and even cultural knowledge share common traits:  
they use machine-readable formats, live in version control and are automatically validated.  

This maturity model synthesises those insights into staged levels of adoption.
It recognises that organisations progress from ad-hoc scripting and isolated diagrams to integrated, self-optimising systems that manage compliance, governance and knowledge via code.

## Interactive radar assessment

For an interactive experience that mirrors the full questionnaire and generates a downloadable radar chart, use the [Architecture as Code maturity radar tool](maturity_model_radar.html). The tool captures every checklist question from this appendix, visualises the current capabilities and produces prioritised improvement guidance that can be shared across teams.

## Staircase overview of maturity progression

![Architecture as Code maturity staircase highlighting Levels 0 to 5](images/diagram_32_maturity_model.png)

The staircase presents the progression from manually curated architecture artefacts to adaptive, AI-supported operating models. Each step emphasises the primary enabler that unlocks the next maturity level.

---

## Dimensions and “as code” aspects

The maturity model includes the key “as code” disciplines discussed in the book:

| Aspect (discipline) | Description | References |
|----------------------|-------------|-------------|
| **Infrastructure as code (IaC)** | Declarative templates and programmatic frameworks (e.g. Terraform, Pulumi, AWS CDK) used to define, provision and manage infrastructure; test strategies include unit, integration and compliance tests. | Ch. 5 Automation & CI/CD [13], Ch. 13 Testing Strategies [2] |
| **Architecture as code (AaC)** | Models such as the C4 model or Structurizr DSL used to encode architecture. AaC becomes the hub that links policies, compliance rules and documentation. | Ch. 6 Structurizr [1], Ch. 23 Soft as Code Interplay [3] |
| **Containerisation & orchestration as code** | Definition of container images, Kubernetes manifests, Compose files and Helm charts; supports repeatable, portable deployments. | Ch. 7 Containerisation & Orchestration as Code [4] |
| **Policy as code (PaC) & Security as code** | Translation of governance and security requirements into executable rules using tools such as Open Policy Agent; reduces manual approvals, provides continuous validation and integrates with CI/CD pipelines. | Ch. 10 Policy & Security [5] |
| **Governance as code** | Codifying approval flows, branch protection rules and decision policies so that governance artefacts live in repositories with transparent review workflows. | Ch. 11 Governance as Code [6] |
| **Compliance as code** | Automating regulatory adherence through policy templates, continuous scanning, evidence collection and feedback loops. | Ch. 12 Compliance [7] |
| **Testing as code** | Multi-layered testing for codified architecture, including unit tests, policy compliance checks, cost forecasting and end-to-end validation. | Ch. 13 Testing Strategies [2] |
| **Documentation as code** | Using Markdown or AsciiDoc with version control to generate living documentation and diagrams; ensures architecture descriptions stay current and accessible. | Ch. 22 Documentation vs Architecture [8] |
| **Knowledge & culture as code** | Capturing organisational knowledge and cultural practices in structured repositories to preserve institutional memory and support onboarding. | Ch. 23 Soft as Code Interplay [3] |
| **Management as code** | Encoding leadership practices, team structures and decision processes into templates and bots (e.g. GitHub issues, pull-request workflows) to support repeatable governance. | Ch. 19 Management as Code [9] |

Each discipline contributes to the overall maturity.
Organisations rarely adopt all aspects at once; instead, they progressively expand the scope of codification.

---

## Assessment checklist for radar visualisation

Use the following yes/no questions to evaluate each discipline before plotting the results on a radar diagram. A "yes" response indicates that the preferred maturity-aligned practice is in place.

### Infrastructure as code (IaC)

- [ ] Are all infrastructure definitions stored in version control with peer review required prior to merge?
- [ ] Is automated validation or linting run on every infrastructure code change before deployment?
- [ ] Do environment deployments rely solely on declarative templates rather than manual changes?
- [ ] Are infrastructure modules reusable and parameterised to promote consistency across environments?
- [ ] Is drift detection automated and reviewed regularly to ensure infrastructure matches the declared state?

### Architecture as code (AaC)

- [ ] Are architecture models generated from source-controlled code or domain-specific language definitions?
- [ ] Do teams update architecture models as part of the same change when system behaviour evolves?
- [ ] Is traceability maintained between architecture components and the owning teams or repositories?
- [ ] Are architecture decisions captured as code-backed records that undergo pull-request review?
- [ ] Is automated validation applied to architecture models to detect inconsistencies or missing relationships?

### Containerisation & orchestration as code

- [ ] Are container images and orchestration manifests generated from version-controlled definitions reviewed by the owning team?
- [ ] Do pipelines automatically build, scan and publish container images before release?
- [ ] Is cluster configuration managed declaratively with automated reconciliation to enforce desired state?
- [ ] Are rollout strategies (such as blue-green or canary) codified and repeatedly tested in non-production environments?
- [ ] Is runtime configuration (including secrets and policies) delivered through code rather than manual console changes?

### Policy as code (PaC) & Security as code

- [ ] Are governance and security requirements expressed in machine-readable policies stored in version control?
- [ ] Do automated checks enforce policy compliance in CI/CD pipelines before promotion to higher environments?
- [ ] Is policy code peer reviewed alongside the application or infrastructure change it governs?
- [ ] Are policy violations surfaced through automated alerts with actionable remediation guidance?
- [ ] Is there a feedback loop that updates policies based on new threats, incidents or regulatory changes?

### Governance as code

- [ ] Are approval workflows, branch protections and role definitions codified and version controlled?
- [ ] Do governance automations capture decision history and rationale as part of the workflow output?
- [ ] Is governance code tested in lower environments before it is applied to production repositories?
- [ ] Are exceptions to governance policies time-bound, tracked and reviewed automatically?
- [ ] Is governance tooling accessible to non-developers through templates or guided interfaces sourced from the same codebase?

### Compliance as code

- [ ] Are regulatory controls translated into executable checks that run continuously against live environments?
- [ ] Does the organisation maintain reusable compliance baselines or templates for common regulations?
- [ ] Is evidence collection automated and stored alongside compliance code for audit readiness?
- [ ] Are compliance findings integrated with issue tracking to ensure timely remediation and verification?
- [ ] Do compliance automations generate dashboards or reports that stakeholders review on a scheduled cadence?

### Testing as code

- [ ] Are automated tests defined for every codified artefact, including infrastructure, policies and architecture models?
- [ ] Do pipelines execute the full testing suite on every merge or release candidate?
- [ ] Is test coverage monitored and improved through targeted backlog items when gaps emerge?
- [ ] Are failure scenarios rehearsed with automated chaos or resilience tests to validate recovery procedures?
- [ ] Is test data managed as code with repeatable seeding and sanitisation routines?

### Documentation as code

- [ ] Is documentation authored in version-controlled markup languages with enforced review workflows?
- [ ] Do automated builds publish documentation outputs (web, PDF, diagrams) from the same source repository?
- [ ] Are documentation updates included in the definition of done for relevant product or platform changes?
- [ ] Is diagram generation automated from code or structured data to eliminate manual drawing efforts?
- [ ] Are documentation quality checks (such as link validation and style linting) automated in CI/CD pipelines?

### Knowledge & culture as code

- [ ] Is organisational knowledge captured in structured repositories with clear ownership and contribution guidelines?
- [ ] Do onboarding and learning journeys exist as code-based playbooks or scripts executed during induction?
- [ ] Are retrospectives and continuous improvement actions tracked in version-controlled artefacts with follow-up automation?
- [ ] Is cultural guidance (values, rituals, ceremonies) embedded into tooling such as bots, templates or workflow prompts?
- [ ] Are knowledge repositories regularly reviewed through automated reminders to ensure relevance and accuracy?

### Management as code

- [ ] Are operating models, team topologies and responsibilities documented through code-driven templates?
- [ ] Do leadership ceremonies (such as portfolio reviews) run from standardised agendas or dashboards generated from code?
- [ ] Are performance and delivery metrics collected automatically and surfaced through shared management dashboards?
- [ ] Is resource allocation or staffing managed through codified workflows with automated approvals and audit trails?
- [ ] Are management playbooks iterated through pull requests with participation from the leadership community?

---

## Maturity levels

### Level 0 – Initial / ad hoc
Architecture is documented in slide decks or static diagrams; infrastructure is provisioned manually.  
Policies and governance documents are written as PDFs or intranet pages.  
Compliance is enforced through periodic audits.  
Testing is limited to manual checks.  

---

### Level 1 – Repeatable and version-controlled
- Teams start using declarative IaC templates (e.g. Terraform) to provision environments stored in Git.  
- Architectural diagrams are maintained in version control.  
- Security checks are performed through ad-hoc scripts; manual approvals predominate.  
- Basic syntax validation for IaC introduced.  
- Markdown begins to replace Word documents.

---

### Level 2 – Defined and automated
- Declarative IaC and container definitions become standard. CI/CD pipelines build and deploy infrastructure; integration tests and policy checks run automatically.  
- Organisations adopt DSLs like Structurizr to model systems and generate diagrams.  
- Governance requirements are expressed in policy languages like Rego.  
- Pull-request templates and branch rules codify approvals.  
- Tools such as Terratest and Checkov enforce compliance.  
- Documentation generated from code and published automatically.

---

### Level 3 – Managed and integrated
- AaC links policies, compliance controls and documentation; traceability between design and rules.  
- Policy engines enforce guardrails; zero-trust and threat modelling embedded.  
- Governance workflows are fully codified; non-developers use low-code policy editors.  
- Compliance requirements translated into templates with automated control execution.  
- Continuous compliance scanning integrated into operations.  
- Testing covers unit, integration, security and compliance.  
- Documentation remains in sync; knowledge and culture version-controlled.  
- Leadership practices encoded into templates and bots.

---

### Level 4 – Optimised and AI-assisted
- Architecture as code becomes dynamic and adaptive with telemetry feedback.  
- Machine learning predicts risks and remediates drift automatically.  
- Self-healing infrastructure scales proactively.  
- Governance as code spans enterprise portfolios with automated audit trails.  
- Carbon-aware deployment practices codified; AI optimises resource use.  
- Conversational agents automate knowledge discovery and onboarding.

---

### Level 5 – Innovative / next-generation
- Architecture integrates generative AI to explore alternatives; digital twins simulate systems.  
- Policies expressed in intent languages; AI agents synthesise granular rules.  
- Models incorporate quantum-safe cryptography and quantum-assisted optimisation.  
- Cultural values codified to guide AI behaviour and collaboration.  
- Organisation-wide management-as-code practices enable transparent, merit-based governance.

---

## Using the maturity model

1. **Assess current position** – Evaluate practices across each discipline; take the lowest common level as baseline.  
2. **Identify gaps and priorities** – Determine which disciplines need advancement.  
3. **Plan incremental improvements** – Move up one level at a time.  
4. **Invest in people and culture** – Prioritise training and collaboration.  
5. **Leverage automation** – Automate validation, testing and evidence collection early.  
6. **Prepare for AI augmentation** – Build telemetry pipelines and AI skills.

---

## Conclusion

Architecture as code is more than diagrams — it is a holistic approach that unifies infrastructure, policy, governance, documentation and culture through codified representations.  
By progressing through this maturity model, organisations can evolve from manual, error‑prone processes to adaptive systems that embed governance and leverage AI for continuous improvement.  

“As code” disciplines must reinforce one another rather than exist in silos.

---

## References

[1]: https://github.com/dwmkerr/architecture-as-code "Architecture as Code GitHub Repository"  
[2]: https://raw.githubusercontent.com/Geonitab/architecture_as_code/main/docs/13_testing_strategies.md "Testing Strategies Chapter"  
[3]: https://raw.githubusercontent.com/Geonitab/architecture_as_code/main/docs/23_soft_as_code_interplay.md "Soft as Code Interplay Chapter"  
[4]: https://raw.githubusercontent.com/Geonitab/architecture_as_code/main/docs/07_containerisation_and_orchestration.md "Containerisation and Orchestration Chapter"  
[5]: https://raw.githubusercontent.com/Geonitab/architecture_as_code/main/docs/10_policy_and_security.md "Policy and Security Chapter"  
[6]: https://raw.githubusercontent.com/Geonitab/architecture_as_code/main/docs/11_governance_as_code.md "Governance as Code Chapter"  
[7]: https://raw.githubusercontent.com/Geonitab/architecture_as_code/main/docs/12_compliance.md "Compliance Chapter"  
[8]: https://raw.githubusercontent.com/Geonitab/architecture_as_code/main/docs/22_documentation_vs_architecture.md "Documentation vs Architecture Chapter"  
[9]: https://raw.githubusercontent.com/Geonitab/architecture_as_code/main/docs/19_management_as_code.md "Management as Code Chapter"  
