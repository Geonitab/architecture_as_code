# The Interplay Between Soft "as code" Disciplines

## Introduction

For years, the phrase "as code" has been tightly associated with hard, technically defined artifacts such as infrastructure, pipelines, and configurations. In recent years the same operating model has entered the softer domains of an organisation. When we speak about compliance as code, architecture as code, documentation as code, knowledge as code, and culture as code, we point to the same underlying ambition: describing complex, often human-dependent processes in machine-readable, version-controlled, and executable formats. This chapter explores how the disciplines overlap, the synergies they create, and how organisations can benefit from their combined strength.

![Soft as code ecosystem](images/diagram_23_soft_as_code.png)

The following mind maps illustrate the key concepts and relationships within the soft "as code" ecosystem. They visualise how the different disciplines connect through their shared DNA, each playing distinct roles while reinforcing one another to create organisational synergies.

![Shared DNA of "as code" disciplines](images/mindmap_23a_shared_dna.png)

*Figure 23.1 shows the foundational elements shared across all "as code" disciplines: structured representation, version control, and automatability.*

![Compliance as Code](images/mindmap_23b_compliance.png)

*Figure 23.2 illustrates how compliance as code provides quality engines, codified controls, and integration benefits.*

![Architecture as Code as central hub](images/mindmap_23c_architecture.png)

*Figure 23.3 demonstrates architecture as code serving as the central hub connecting technical implementation, policy, and documentation.*

![Documentation as Code](images/mindmap_23d_documentation.png)

*Figure 23.4 shows documentation as code providing communication layers, toolchain integration, and feedback loops.*

![Knowledge and Culture as Code](images/mindmap_23e_knowledge_culture.png)

*Figure 23.5 presents how knowledge and culture can be codified to enable structured onboarding and experience preservation.*

![Synergies and implementation strategy](images/mindmap_23f_synergies.png)

*Figure 23.6 highlights the synergies created through cross-pollination and the implementation strategy for adopting these practices.*

**Key takeaways from the mind map:**

- **Shared DNA at the core:** All soft "as code" disciplines are unified by structured representation, version control, and automatability—fundamental principles that enable collaboration across domains.
- **Compliance as Code acts as the quality engine:** By codifying rules and policies, it provides continuous validation and transparency, ensuring that architectural and documentation artifacts remain within approved boundaries.
- **Architecture as Code serves as the central hub:** It connects technical implementations with policy and documentation layers, providing traceability and enabling real-time synchronization across the ecosystem.
- **Documentation as Code forms the communication layer:** It translates technical and policy concepts into accessible narratives, enabling self-service knowledge and fostering collective ownership through structured feedback loops.
- **Knowledge and Culture as Code preserve organisational memory:** Formalizing lessons learned and cultural values ensures consistency, supports onboarding, and enables rapid iteration without losing core principles.
- **Synergies multiply value:** When these disciplines integrate, they create cross-functional collaboration spaces, unified validation pipelines, and enhanced traceability—accelerating the pace of change while managing risk.
- **Implementation requires strategy:** Success depends on shared principles, compatible tooling, cross-functional training, iterative building, and clear governance frameworks.

This visualisation reinforces the chapter's central message: soft "as code" disciplines are more powerful together than in isolation, creating an ecosystem where human creativity is amplified by the precision and reliability of code.

## A Shared DNA

Even though the disciplines address different problem spaces, they share a common DNA. The goal is to take soft artifacts—policies, architectural principles, design descriptions, documentation, governance models—and convert them into:

1. **Structured representation.** Machine-readable formats such as YAML, JSON, Markdown, domain-specific languages, or models within code libraries make it possible to validate, test, and connect information to automation.
2. **Version control.** Git or similar systems provide history, traceability, and the ability to collaborate through pull requests, code reviews, and release processes.
3. **Automatability.** When soft artifacts are expressed as code they can feed tools that generate reports, verify compliance, update dashboards, or trigger workflows.

This combination opens the door to a shared way of working across disciplines. Once an organisation has established a culture of version control, code review, and automated testing, it becomes natural to let compliance rules, architectural guidelines, and documentation structures live in the same ecosystem.

## Compliance as Code as the Quality Engine

Compliance as code focuses on translating regulations, standards, and internal policies into codified controls. Tools such as Open Policy Agent, HashiCorp Sentinel, or custom rule frameworks can ingest policy definitions and evaluate them against system configurations, CI/CD pipelines, or infrastructure definitions. When the discipline is connected to other soft areas several effects emerge:

- **Rule reuse.** Documentation and architectural principles can directly reference policy definitions, reducing the risk of diverging interpretations. An architect writing a blueprint can link to the same policy files the security team uses in their controls.
- **Continuous validation.** Documentation as code makes it possible to describe which controls exist and how they are executed, while automations from architecture as code can trigger compliance checks for every change. The result is an unbroken chain between intent and verification.
- **Transparency and education.** When the rule set is versioned and open to inspection, teams can teach themselves what is required. Pull requests on policy code become educational moments where lawyers, security experts, and developers meet and explain their reasoning.

Compliance as code thus becomes a quality engine that reinforces the other disciplines. When architectural or documentation artifacts are updated, automated controls can ensure that changes still fall within approved boundaries. If a rule changes, the update propagates to every system that uses it—from architectural diagrams to external reports.

## Architecture as Code as the Hub

Architecture as code means expressing architectural decisions, reference architectures, and target architectures in code. This might take the form of models in DSLs such as Structurizr, C4 models generated from Markdown, or Terraform/CloudFormation modules representing architectural patterns. Once the architecture exists in code, a natural hub for the other disciplines emerges:

- **Traceability to compliance.** The architecture can reference compliance rules that explain why a given pattern must include logging, encryption, or redundancy. By linking to rule definitions it becomes clear how design decisions support adherence.
- **Real-time documentation.** Documentation as code can be generated directly from architectural models and provide up-to-date manuals, diagrams, and guides. Documentation stays in sync with the "living" architecture.
- **Automated quality gates.** When architectural models are versioned, compliance and quality checks can run automatically before an architectural change is approved. This offers objective support for architecture boards and decision forums.

The hub metaphor is powerful: architecture as code connects technical implementations with policy and documentation layers. It becomes easier to facilitate dialogue across expert roles when everyone looks at the same source of truth.

## Documentation as Code as the Communication Layer

Documentation as code is about writing, storing, and publishing documentation with the same toolchain used for other code. Markdown files are versioned in Git, generated via static site generators, and distributed through CI/CD pipelines. In the interplay between soft "as code" disciplines, documentation as code is the glue that binds the ecosystem together:

- **Narratives around rules and architecture.** Documentation does not only describe "how" but also "why." By referencing compliance rules and architectural models, documentation explains the relationships and helps teams understand the bigger picture.
- **Self-service.** When documentation is easily accessible and up to date, teams can find answers themselves. That reduces the need for manual handovers and accelerates onboarding.
- **Feedback loops.** Pull requests on documentation create space for review, discussion, and improvement. Knowledge no longer gets stuck with a single individual; it becomes collectively owned.

Documentation as code also acts as a layer of visibility. Architectural principles, compliance rules, and process descriptions become transparent and can be discussed in a structured way. Learning and improvement are therefore strengthened across the organisation.

## Knowledge as Code and Culture as Code

To capture the full spectrum of soft artifacts we can also include knowledge as code and culture as code. Knowledge as code formalizes knowledge bases and lessons learned in code or semi-structured formats, while culture as code expresses values, decision-making practices, and ways of working in versioned playbooks. When experiences, norms, and policies can be linked to architectural models and documentation, insights become reusable, tracking adherence to working norms becomes easier, and onboarding grows more structured. The organisation can iterate quickly while still preserving its experience and values.

## Synergies and Cross-Pollination

Introducing several soft "as code" disciplines in parallel generates effects that exceed the value of any single initiative. Shared tools and processes turn pull requests into meeting places for architects, developers, lawyers, and communicators, and the same pipelines can validate code, policy, and documentation. Traceability improves when commit hashes, issues, and policy identifiers are cross-linked, giving revisions and incident investigations a clear history. Pace and appetite for experimentation increase because soft artifacts can be updated as fast as code while automated controls temper risk. Cross-functional collaborations emerge where legal experts learn technical details and developers appreciate the rationale behind regulations, creating shared ownership of the whole system.

## Challenges and Counterforces

The interplay between soft "as code" disciplines is powerful but also demanding. Common challenges include:

- **Differences in terminology and mindset.** Lawyers, architects, and documentation specialists use different vocabularies, which requires translation and extra onboarding.
- **Tooling barriers.** Not everyone is comfortable with Git, pull requests, or CI/CD, so training is needed to avoid creating new hierarchies.
- **Automation debt.** Codified rules do not capture every interpretation, so manual controls and clear governance remain necessary.
- **Information overload.** When everything is versioned and logged, metadata and structure are required to keep information navigable.

By addressing these challenges openly, investing in joint training initiatives, and establishing clear roles, organisations can maximize the value of the interplay.

## Practical Applications

To make the interplay more tangible, consider a few practical scenarios:

### Scenario 1: Policy Change

The compliance team updates a data retention rule in code, after which the architectural models flag components lacking encryption. Documentation as code generates a new section about the requirement, and dashboards notify teams so remedial actions can be planned without delay.

### Scenario 2: New Product Launch

A new product is defined as code, which simultaneously creates diagrams and triggers compliance checks in CI/CD. Documentation is enriched with onboarding guides and API descriptions, while the knowledge base links to lessons learned from earlier launches.

These scenarios illustrate how the interplay creates a dynamic chain in which each discipline amplifies the others.

## Strategies for Adoption

Organisations seeking to establish a cohesive ecosystem of soft "as code" disciplines can follow these strategies:

1. **Start with shared principles.** Clarify the objectives of the initiative and the outcomes it should deliver.
2. **Choose compatible tools.** Ensure that compliance, architecture, and documentation tooling can integrate and share version control.
3. **Invest in cross-functional training.** Teach lawyers Git, help architects understand policy DSLs, and make documentation specialists comfortable with automated publishing.
4. **Build iteratively.** Begin with a pilot area and measure effects such as time savings or improved audit readiness.
5. **Establish governance.** Define roles for code owners and review processes as well as forums for discussing policy and architecture changes.

## Future Perspectives

Technologies such as AI and semantic search engines expand the potential of soft "as code" disciplines. By combining codified regulations with language models, organisations can receive real-time advice, automated explanations, and proactive recommendations. Architecture as code can be connected to simulations that reveal the impact of design decisions before implementation, and documentation can be generated dynamically.

At the same time, data governance, security, and ethics become even more important. The more of an organisation’s soft fabric that is codified, the greater the demands on access control, privacy protection, and accountability.

## Conclusion

The interplay between soft "as code" disciplines is about building an ecosystem where compliance, architecture, documentation, knowledge, and culture move in unison. By applying the same tools, processes, and mindset to these artifacts as to traditional code, organisations become adaptive, transparent, and continuously learning. Compliance as code operates as the quality engine, architecture as code serves as the hub, documentation as code forms the communication layer, and knowledge/culture as code act as the collective memory and compass.

When these disciplines integrate, change ceases to be a threat and becomes a natural part of daily work. Teams can adapt rapidly to new requirements, experiment with new ideas, and still maintain a stable core of shared principles. The result is an organisation that dares to combine softness and structure—where human creativity is supported by the precision of code.

## Sources

Sources:
- [Open Policy Agent – Policy as Code Overview](https://www.openpolicyagent.org/docs/latest/)
- [HashiCorp – Policy as Code Overview](https://developer.hashicorp.com/terraform/cloud-docs/policy-enforcement)
- [GitHub Docs – About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
