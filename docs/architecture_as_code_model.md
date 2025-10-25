# Architecture as Code Model

## Maturity model for implementing architecture as code

Modern organisations are increasingly turning to **architecture as code (AaC)** to keep systems design, security and governance aligned with rapid delivery.  
The *Architecture as Code* book describes how codified representations of architecture, policy, governance and even cultural knowledge share common traits:  
they use machine-readable formats, live in version control and are automatically validated.  

This maturity model synthesises those insights into staged levels of adoption.  
It recognises that organisations progress from ad-hoc scripting and isolated diagrams to integrated, self-optimising systems that manage compliance, governance and knowledge via code.

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
