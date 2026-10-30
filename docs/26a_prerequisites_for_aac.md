# Prerequisites for Architecture as Code Adoption {#prerequisites-for-aac}

> **Author’s note:** This chapter is numbered 26A in the overall book sequence but is placed here at the opening of Part A as a readiness guide. Its purpose is to help teams assess whether their organisation has the cultural, technical, and economic foundations needed before embarking on an Architecture as Code programme. Readers who are already familiar with the prerequisites may proceed directly to Chapter 2; those who prefer a comprehensive readiness review will find the frameworks and case studies in this chapter a practical starting point.

Successful Architecture as Code (AaC) programmes are never accidents. They emerge when an organisation’s cultural habits, technical capabilities, and economic discipline align with the philosophy set out in Chapter 2 on fundamental principles and explored in depth throughout this book. This chapter distils the readiness signals covered later in this book—from the organisational narratives in Chapters 17 to 19, to the delivery mechanics described in Chapters 5, 13, and 14, and the financial guardrails covered in Chapter 15 (Cost Optimisation and Resource Management). Readiness is not a gate to appease governance; it is evidence that the organisation can wield AaC responsibly.

## Why Readiness Matters

![Prerequisites transformation journey](images/diagram_17_transformation_journey.png)

The lesson from Chapter 14 (covered later in this book) still stands: organisations that front-load stakeholder alignment avoid the most common integration problems, because automation without alignment merely amplifies disorder. A readiness review slows the rush to tool selection. Leaders can then prove, rather than assume, that the organisation can absorb executable architecture. This review prevents brittle deployments that clash with the operational expectations described in Chapter 5 (covered later in this book). It also protects the psychological safety emphasised in Chapter 17 (covered later in this book)—the generative culture that Forsgren, Humble & Kim (2018) [Source [31]](33_references.md#source-31) show predicts software delivery performance—and keeps investment decisions honest in line with Chapter 15 (covered later in this book). Readiness is therefore a contract—when the prerequisites are visible, teams earn the right to automate architectural intent.

## Cultural Foundations

AaC flourishes where experimentation and shared ownership are routine. The cultural preparation described in Chapters 17 to 19 (covered later in this book) is essential: retrospectives must be regular, blameless reviews must be normal, and communities of practice must already exist. Without those habits the `as code` mindset from Chapter 3 becomes adversarial, with review comments interpreted as personal attacks.

Leaders must also tell a compelling story that links AaC to mission, customer outcomes, and professional growth, because narratives anchor change even when management intent is codified in the way Chapter 19 describes. When every engineer can articulate the “why”, the team structures from Chapter 18 feel like empowerment rather than intrusion.

Cultural readiness also involves aligning reward systems and career frameworks with the balanced scorecards described in Chapter 18, which combine delivery indicators with knowledge sharing and cross-team collaboration; promotions and recognition must celebrate shared delivery outcomes instead of isolated heroics.

Practitioners should already experience leaders acting as coaches, echoing the behavioural commitments in Chapter 17, so that AaC feels like a natural extension of existing norms rather than an abrupt revolution.
## Technical Maturity Baselines

AaC assumes mastery of core delivery disciplines. The continuous pipelines covered in Chapter 5, the testing depth covered in Chapter 13, and the Structurizr patterns covered in Chapter 6 must already be routine. Otherwise, architecture models drift from runtime reality. Such maturity cannot be assumed: the *State of Cloud Native Development Q3 2025* report by SlashData for the Cloud Native Computing Foundation ([Source [7]](33_references.md#source-7)) records that use of internal developer platforms among the developers surveyed rose only from 23 per cent in Q3 2024 to 27 per cent in Q3 2025.

Security and compliance practices from Chapters 9, 9B, and 10 also need to be embedded so that codified architecture does not introduce blind spots.

Governance automation, as described in Chapter 11, provides the scaffolding that lets architectural code flow through the same delivery channels as application code.

Technical readiness further demands disciplined environment strategies—golden paths, reference stacks, and service catalogues—that make reuse effortless and align with the platform guidance in Chapter 24.

Data quality expectations must be explicit so that telemetry, cost analytics, and resilience signals inform architectural decisions in the spirit of the observability and feedback loops described in Chapter 24.
## Knowledge and Information Management

Readiness depends on how knowledge is curated. The distinction between documentation and architecture covered in Chapter 22 only holds when both are discoverable. Teams need version-controlled architecture decision records, reusable component catalogues, and glossaries such as the Glossary in Chapter 28. These artefacts shorten onboarding time and anchor architectural intent in narrative context, echoing the measurement guidance from Chapter 17. Telemetry and feedback channels—highlighted in Chapters 5 and 24—must already feed insights into design discussions; otherwise AaC becomes detached from operational reality.

## Economic Preconditions

Financial discipline underpins sustainable automation. Chapter 15 shows how cost allocation tags and chargeback models make cloud spending transparent across teams; without that transparency, automation quickly becomes an expensive hobby. Readiness therefore requires funding models that reward incremental value, cost telemetry that is trusted across finance and engineering, and procurement practices flexible enough to support the pilot-based, iterative adoption described in Chapter 14. Budgeting as Code from Chapter 19—budget envelopes defined per product, platform, or team and adjusted through pull requests—lets teams reinvest savings rather than lose them to annual budget resets, while governance controls from Chapter 11 keep spending aligned with strategic guardrails. Organisations should also establish value-tracking rituals—quarterly benefit reviews, reuse inventories, and scenario planning—that echo the continuous improvement loops in Chapter 24. These forums allow finance, security, and engineering to recalibrate investment together, preventing the surprise budget cuts that have destabilised many digital initiatives.

## Skills, Roles, and Capacity

AaC expands rather than replaces existing responsibilities. The cross-functional roles mapped in [Chapter 18](18_team_structure.md)—platform product owners, site reliability engineers, security partners—must already collaborate effectively, with the team interaction modes that Skelton & Pais (2019) [Source [30]](33_references.md#source-30) describe in *Team Topologies* made explicit. Career pathways should recognise hybrid skill sets so practitioners can grow without abandoning technical leadership, reflecting the advice from [Chapter 19](19_management_as_code.md). Capacity planning matters too: reviewing architecture pull requests, maintaining models, and curating knowledge bases all consume time. Organisations that ignore this guidance risk burning out their people instead of building sustainable capability—the failure mode that the measurement guidance in [Chapter 17](17_organisational_change.md) warns against.

## Platform and Toolchain Alignment

The technology landscape must be coherent before AaC can thrive. Pipelines, modelling tools, and knowledge repositories need to integrate cleanly, as illustrated in [Chapters 05 and 06](05_automation_devops_cicd.md). Fragmented tooling multiplies cognitive load and complicates compliance checks referenced in [Chapter 12](12_compliance.md). Readiness reviews should also confirm the availability of safe experimentation environments—sandboxes and simulation frameworks that align with the testing ethos of [Chapter 13](13_testing_strategies.md). If experimentation is slow or expensive, architecture code will stagnate.

## Governance and Compliance Preparedness

AaC codifies governance rather than bypassing it. Policies, standards, and risk tolerances must already be expressed as automated controls—the *security policy as code* practice that the Thoughtworks Technology Radar moved to Adopt in 2020 ([Source [2]](33_references.md#source-2))—building on [Chapter 11](11_governance_as_code.md). Compliance partners should participate in pull request reviews, and audit trails should be generated automatically. Organisations also need agile decision forums reminiscent of the collaborative guardrails in [Chapter 23](23_soft_as_code_interplay.md). If governance is still a periodic toll booth, AaC will either stall or erode trust by appearing to sidestep controls.

## Change Management Infrastructure

Transformation succeeds when change is treated as a service. The communication patterns, sponsorship behaviours, and learning pathways described in [Chapter 17](17_organisational_change.md) must already be active. Town halls, asynchronous updates, and leadership blogs keep stakeholders aligned; mentorship schemes from [Chapter 18](18_team_structure.md) sustain knowledge transfer; migration playbooks from [Chapter 16](16_migration.md) prevent disruption. Organisations that rely on heroics or one-off training courses find AaC enthusiasm fading as soon as the early champions move on. Mature change programmes pair formal training with peer coaching, playbooks, and the iterative adoption journey described in [Chapter 14](14_practical_implementation.md), ensuring new behaviours are reinforced long after the initial launch.

## Readiness Assessment Framework

A structured readiness assessment keeps preparation honest. Borrowing from the measurement practices in [Chapter 17](17_organisational_change.md) and the continuous improvement routines in [Chapter 24](24_best_practices.md), a pragmatic framework comprises four loops:

1. **Contextual Discovery** – Map stakeholder expectations using the techniques from [Chapter 11](11_governance_as_code.md) so that finance, security, and delivery voices are heard.
2. **Capability Baseline** – Evaluate automation, testing, modelling, and knowledge management against benchmarks from [Chapters 05, 06, and 22](05_automation_devops_cicd.md).
3. **Cultural and Economic Diagnostics** – Measure psychological safety, leadership engagement, and funding flexibility, drawing on [Chapters 17 and 15](17_organisational_change.md).
4. **Remediation Roadmap** – Sequence improvements with explicit links to the chapters above so that cultural, technical, and financial gaps close together.

Treating readiness as an iterative loop mirrors the delivery cadence promoted in [Chapter 14](14_practical_implementation.md) and the adaptive mindset in [Chapter 25](25_future_trends.md).

## Readiness Scorecard Template

Use this scorecard to assess your organisation's readiness for Architecture as Code adoption. Rate each dimension 1 (not started) to 5 (fully implemented).

| Dimension | Assessment Criteria | Score (1–5) | Notes / Evidence |
|-----------|---------------------|-------------|-----------------|
| **Contextual Discovery** | | | |
| Stakeholder alignment | Key stakeholders identified and engaged | | |
| Current-state documentation | Existing architecture documented to C4 Level 2 | | |
| Tool inventory | Current toolchain catalogued (IaC, CI/CD, monitoring) | | |
| **Capability Baseline** | | | |
| Version control maturity | Infrastructure code in version control with branching strategy | | |
| Automation coverage | ≥50% of infrastructure provisioned via code | | |
| Skills availability | Team members trained in at least one IaC tool | | |
| **Cultural Readiness** | | | |
| Change appetite | Leadership support for code-first approach confirmed | | |
| Collaboration practices | Team uses pull-request-based review workflows | | |
| Learning culture | Team participates in internal knowledge-sharing sessions | | |
| **Economic Viability** | | | |
| Budget allocated | Budget confirmed for tooling, training, and migration effort | | |
| ROI baseline | Current cost-of-manual-change quantified for comparison | | |
| Risk tolerance | Acceptable risk threshold defined for incremental rollout | | |
| **Remediation Roadmap** | | | |
| Gap prioritisation | Top three capability gaps identified and ranked | | |
| Quick wins defined | At least one low-effort, high-visibility pilot scoped | | |
| Milestones agreed | 90-day and 12-month milestones documented | | |

**Scoring guidance:**
- 60–75 points: Ready to proceed — begin with a focused pilot
- 40–59 points: Partial readiness — address critical gaps before scaling
- Below 40 points: Foundation work needed — follow the Remediation Roadmap first

## Case Study: Preparing a Global Enterprise

A multinational financial services group offers a useful illustration. Automation maturity is high—CI/CD pipelines mirror [Chapter 05](05_automation_devops_cicd.md)—yet architecture still relies on static review boards. A readiness assessment uncovers three gaps. Knowledge artefacts live in static slide decks, contradicting the practices in [Chapter 22](22_documentation_vs_architecture.md). Psychological safety varies across regions, highlighting the cultural work described in [Chapter 17](17_organisational_change.md). Funding remains tied to annual projects, conflicting with the Budgeting as Code model from [Chapter 19](19_management_as_code.md).

The remediation roadmap tackles each issue. The architecture office pilots version-controlled decision records using [Chapter 04](04_adr.md) templates. Communities of practice connect regional teams, mirroring the design from [Chapter 18](18_team_structure.md). Finance introduces FinOps cost governance guided by [Chapter 15](15_cost_optimization.md). Six months later the organisation launches AaC pilots confident that culture, tooling, and funding can sustain the change.

## Common Readiness Anti-patterns

Organisations that struggle with AaC usually repeat familiar mistakes:

- **Tool-first enthusiasm** – Buying modelling platforms without addressing the cultural foundations in [Chapter 17](17_organisational_change.md) produces shelfware.
- **Heroic ownership** – Concentrating responsibility in a few experts defies the distributed leadership model in [Chapter 18](18_team_structure.md).
- **Budget whiplash** – Treating AaC as a one-off project contradicts the continuous optimisation message from [Chapter 15](15_cost_optimization.md).
- **Governance bypass** – Sidestepping compliance partners undermines the trust built through [Chapter 11](11_governance_as_code.md).
- **Metrics myopia** – Tracking deployment speed whilst ignoring culture repeats the caution from [Chapter 17](17_organisational_change.md).

Recognising these anti-patterns early enables corrective action before momentum is lost.

## Sequencing Readiness Investments

Perfection is unnecessary, but sequencing matters. Following the migration mindset in [Chapter 16](16_migration.md), organisations should start with a narrow architectural domain backed by supportive stakeholders. Establish cultural and governance guardrails first, stabilise tooling second, and adjust funding models alongside early wins. Each slice mirrors the pilot-first, incrementally expanding adoption journey from [Chapter 14](14_practical_implementation.md), proving both capability and organisational resilience.

## Measuring Ongoing Readiness

Readiness is not a one-off audit. Dashboards should blend the DORA indicators used in [Chapter 05](05_automation_devops_cicd.md)—deployment frequency, lead time for changes, change failure rate, failed deployment recovery time, and rework rate ([Source [49]](33_references.md#source-49))—with cultural metrics from [Chapter 17](17_organisational_change.md) and cost signals from [Chapter 15](15_cost_optimization.md). Governance measures—policy drift, exception frequency, audit findings—confirm whether the codified controls in [Chapter 11](11_governance_as_code.md) still operate. Quarterly reviews keep AaC aligned with reality and feed continuous improvement loops described in [Chapter 24](24_best_practices.md) and [Chapter 25](25_future_trends.md).

## Conclusion

AaC readiness is a deliberate synthesis of culture, technology, and economics. Organisations that honour these prerequisites create the conditions for disciplined adoption of the practices introduced in the chapters that follow. Those that skip the groundwork rediscover the failure modes catalogued throughout the book. By grounding adoption in readiness, teams respect the complexity of their sociotechnical systems and earn the right to begin the Architecture as Code journey described from [Chapter 2](02_fundamental_principles.md) onward.

[Chapter 2: Fundamental Principles](02_fundamental_principles.md) is the natural next step: it establishes the declarative, immutable, and testable patterns that readiness prepares teams to absorb. For anti-patterns to avoid during adoption, see [Chapter 26B: Anti-Patterns in Architecture as Code Programmes](26b_aac_anti_patterns.md).

## Sources

1. **SlashData for the Cloud Native Computing Foundation (2025).** *State of Cloud Native Development Q3 2025.* CNCF, November 2025. Available at: [https://www.cncf.io/reports/state-of-cloud-native-development/](https://www.cncf.io/reports/state-of-cloud-native-development/). [Source [7]](33_references.md#source-7)
2. **Thoughtworks (2019–2020).** *Security policy as code.* Technology Radar, Techniques: Trial (Vol. 21, November 2019), Adopt (Vol. 23, October 2020). Available at: [https://www.thoughtworks.com/radar/techniques/security-policy-as-code](https://www.thoughtworks.com/radar/techniques/security-policy-as-code). [Source [2]](33_references.md#source-2)
3. **Skelton, M. & Pais, M. (2019).** *Team Topologies: Organizing Business and Technology Teams for Fast Flow.* IT Revolution Press. ISBN 978-1-942788-81-2. [Source [30]](33_references.md#source-30)
4. **Forsgren, N., Humble, J. & Kim, G. (2018).** *Accelerate: The Science of Lean Software and DevOps.* IT Revolution Press. ISBN 978-1-942788-33-1. [Source [31]](33_references.md#source-31)
5. **DORA (2024).** *Accelerate State of DevOps Report 2024.* Google Cloud / DORA. Available at: [https://dora.dev/research/2024/dora-report/](https://dora.dev/research/2024/dora-report/). [Source [49]](33_references.md#source-49)
