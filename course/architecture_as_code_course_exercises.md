# Architecture as Code Course Exercises

This companion guide provides detailed exercises, lab briefs, and extension pathways for each module of the *Architecture as Code* curriculum. Every exercise references the maturity radar prompts, specifies expected artefacts, and links to the templates in `course/templates/`. Facilitators should assign exercises during live sessions and track completion through the module workbooks.

## How to use this guide

1. Review the module overview and select the live and asynchronous exercises that align with participant goals.
2. Duplicate the Module Workbook template for the cohort and pre-populate each exercise table with due dates and facilitators.
3. During facilitation, remind teams to store evidence in version control and link commits, pipelines, and documentation to their workbook entries.
4. Use the Lab Submission Checklist to validate completion before granting sign-off.

---

## Module 0 – Orientation and radar benchmarking

**Book alignment:** Chapters 01 *Introduction to Architecture as Code*, 02 *Fundamental Principles of Architecture as Code*, 24 *Modern Best Practices and Lessons Learned*, and 27 *Conclusion*. Ensure workbook reflections summarise insights from these chapters before progressing to later modules.

| Exercise | Format | Objective | Key artefacts | Radar prompts |
| --- | --- | --- | --- | --- |
| Baseline radar survey | Individual | Establish initial maturity scores and supporting evidence across all disciplines. | Completed radar survey export, workbook baseline summary. | Entire radar checklist. |
| Evidence landscape mapping | Team workshop | Identify codified artefacts versus manual processes and highlight automation opportunities. | Workbook evidence map, repository links to existing artefacts. | Documentation, governance, automation readiness. |
| Improvement experiment charter | Individual self-study | Define a personal experiment aligned to the weakest radar discipline. | Reflection log entry, action plan canvas stub. | Target discipline chosen by participant. |

**Extension:** Produce a short loom-style video walkthrough of the organisation’s tooling landscape and upload the link to the workbook knowledge hub.

---

## Module 1 – Infrastructure as code foundations

**Book alignment:** Chapters 05 *Automation, DevOps and CI/CD for Architecture as Code*, 07 *Containerisation and Orchestration as Code*, and 13 *Testing Strategies for Architecture as Code*. Capture workbook entries that cite the patterns, gates, and testing approaches introduced in these chapters.

| Exercise | Format | Objective | Key artefacts | Radar prompts |
| --- | --- | --- | --- | --- |
| Declarative pipeline build | Live lab | Create an automated infrastructure delivery pipeline with validation gates. | Pipeline configuration, Terraform/Pulumi code, pipeline run link. | Version control, automated validation, drift detection. |
| Post-incident analysis clinic | Facilitated discussion | Distil lessons from manual deployment incidents and translate them into codified safeguards. | Workbook incident comparison notes, updated pull-request checklist. | Peer review, reusable modules, deployment automation. |
| Module testing sprint | Self-study | Implement module testing (e.g. Terratest) and document results. | Test code, pipeline evidence, reflection log update. | Automated validation, coverage monitoring. |

**Extension:** Introduce cost estimation tooling (Infracost or Terraform cost modules) and record findings under the action plan canvas experiment backlog.

---

## Module 2 – Architecture as Code modelling

**Book alignment:** Chapters 06 *Structurizr: Architecture Modeling as Code*, 23 *Soft as Code Interplay*, and Appendix B *Technical Architecture for Book Production*. Use workbook notes to demonstrate how the referenced chapters influence modelling decisions and traceability.

| Exercise | Format | Objective | Key artefacts | Radar prompts |
| --- | --- | --- | --- | --- |
| Structurizr workspace build | Workshop | Model system context, container, and component views from source-controlled definitions. | Structurizr DSL repository, generated diagrams, CI logs. | Model generation, change synchronisation, traceability. |
| Architecture review swap | Peer review | Critique another team’s models for clarity, traceability, and ADR linkage. | Review checklist, workbook peer review notes, follow-up issues. | Decision capture, automated validation, shared understanding. |
| ADR authoring | Self-study | Capture trade-offs and decisions related to modelling choices. | ADR markdown file, pull request, reviewer comments. | Decision capture, collaboration, documentation. |

**Extension:** Integrate automated conformance checks (e.g. Structurizr lint rules) and document outcomes in the workbook quality section.

---

## Module 3 – Containerisation and orchestration at scale

**Book alignment:** Chapters 07 *Containerisation and Orchestration as Code*, 08 *Microservices Architecture as Code*, and 14 *Architecture as Code in Practice*. Document workbook evidence that shows container workflows aligning with guidance from these chapters.

| Exercise | Format | Objective | Key artefacts | Radar prompts |
| --- | --- | --- | --- | --- |
| Broken manifest recovery | Simulation | Diagnose and resolve a failing deployment while implementing blue-green automation. | Corrected manifests, rollout scripts, smoke test results. | Declarative configuration, tested rollouts, runtime settings. |
| Container security drill | Lab | Run container scans and plan remediation actions linked to policy enforcement. | Scan reports, remediation backlog, workbook risk log. | Automated enforcement, alert surfacing, remediation feedback. |
| Secrets rotation lab | Self-study | Configure secrets management integration and document rotation cadence. | Secrets configuration code, rotation run evidence, action plan update. | Codified runtime settings, adaptive feedback, automated enforcement. |

**Extension:** Implement progressive delivery tooling (e.g. Argo Rollouts or Flagger) and capture telemetry dashboards within the workbook.

---

## Module 4 – Policy as code and security automation

**Book alignment:** Chapters 09 *Security Fundamentals for Architecture as Code*, 09b *Advanced Security Patterns and Implementation*, 09c *Risk as Code and Threat Handling as Code*, and 10 *Policy and Security as Code in Detail*. Reference workbook artefacts back to the control patterns, policy libraries, and response practices described in the book.

| Exercise | Format | Objective | Key artefacts | Radar prompts |
| --- | --- | --- | --- | --- |
| Governance requirement translation | Scenario workshop | Convert policy statements into executable OPA/Sentinel rules with automated tests. | Policy code, unit tests, pipeline integration screenshot. | Policy storage, automated enforcement, peer review. |
| Violation runbook rehearsal | Tabletop exercise | Practise incident response to policy breaches using predefined runbooks. | Completed runbook checklist, time-to-response metrics, workbook operations log. | Alert surfacing, feedback loops, escalation pathways. |
| Coverage metrics reflection | Self-study | Capture enforcement coverage metrics and identify manual approvals to codify. | Reflection log update, metrics dashboard link, action plan backlog item. | Automated enforcement, adaptive feedback. |

**Extension:** Pilot chat-based policy assistance (e.g. rule drafting bots) and evaluate ethical considerations in the workbook foresight section.

---

## Module 5 – Governance as code operations

**Book alignment:** Chapters 11 *Governance as Code*, 17 *Organisational Change and Team Structures*, and 19 *Management as Code*. Ensure workbook updates explicitly cite the governance, cultural, and leadership mechanisms explored in these chapters.

| Exercise | Format | Objective | Key artefacts | Radar prompts |
| --- | --- | --- | --- | --- |
| Workflow codification | Group workshop | Encode the existing governance workflow into repository configuration and automation scripts. | Workflow configuration, before/after diagrams, workbook governance matrix. | Codified approvals, decision history, accessible tooling. |
| Template accessibility clinic | Role-play | Adapt governance request templates for diverse stakeholder needs. | Updated templates, feedback notes, usability checklist. | Inclusive tooling, peer review, documentation updates. |
| Exception path rehearsal | Self-study | Test an automated exception process in a lower environment. | Evidence artefacts, exception log, action plan update. | Automated exception tracking, testing discipline. |

**Extension:** Establish a governance change advisory board run via pull requests and capture meeting cadences in the workbook communication plan.

---

## Module 6 – Compliance as code evidence flows

**Book alignment:** Chapters 12 *Compliance and Regulatory Adherence*, 15 *Evidence as Code*, and Appendix 34 *Control Mapping Matrix Template*. Workbook compliance notes should highlight how controls, evidence pipelines, and mapping templates relate to the book guidance.

| Exercise | Format | Objective | Key artefacts | Radar prompts |
| --- | --- | --- | --- | --- |
| Compliance pipeline implementation | Lab | Automate control execution, evidence storage, and remediation ticketing. | Pipeline definition, evidence repository links, remediation tickets. | Continuous control execution, automated evidence, integrated remediation. |
| Evidence analytics review | Workshop | Validate reporting outputs and trace controls to evidence and issues. | Analytics screenshots, traceability matrix, workbook summary. | Reporting cadences, traceability, reusable baselines. |
| Baseline alignment task | Self-study | Map two organisational controls to a reusable baseline. | Baseline document, mapping markdown, reflection log entry. | Reusable baselines, automated evidence. |

**Extension:** Integrate compliance findings with observability tooling (e.g. Grafana annotations) and record dashboards in the workbook analytics section.

---

## Module 7 – Testing as code for resilient platforms

**Book alignment:** Chapters 13 *Testing Strategies for Architecture as Code*, 05 *Automation, DevOps and CI/CD for Architecture as Code*, and 16 *Migration from Traditional Infrastructure*. Capture workbook experiments that demonstrate links to layered testing, automated delivery, and migration risk management from the book.

| Exercise | Format | Objective | Key artefacts | Radar prompts |
| --- | --- | --- | --- | --- |
| Chaos engineering lab | Simulation | Execute a failure injection experiment and analyse resilience metrics. | Experiment script, telemetry output, workbook experiment log. | Chaos testing, detection, recovery automation. |
| Data stewardship workshop | Clinic | Define governance for synthetic and production-like data in testing. | Data governance charter, access controls, workbook checklist. | Test data management, documentation, policy alignment. |
| Coverage gap analysis | Self-study | Assess test coverage gaps and propose automation improvements. | Updated test matrix, automation backlog, reflection log update. | Coverage monitoring, automated validation. |

**Extension:** Introduce resilience scoring dashboards and compare before/after metrics within the workbook scoreboard.

---

## Module 8 – Documentation, knowledge, and culture as code

**Book alignment:** Chapters 22 *Documentation as Code vs Architecture as Code*, 23 *Soft as Code Interplay*, 18 *Team Structure and Competency Development for Architecture as Code*, and 17 *Organisational Change and Team Structures*. Workbook outcomes should explicitly draw on documentation pipelines, knowledge codification, and cultural automation described in the book.

| Exercise | Format | Objective | Key artefacts | Radar prompts |
| --- | --- | --- | --- | --- |
| Documentation pipeline sprint | Lab | Build automated documentation pipelines with diagram regeneration. | Pipeline configuration, generated site artefacts, workbook publishing ledger. | Version-controlled documentation, automated builds, quality checks. |
| Playbook codification | Workshop | Create an onboarding playbook with automated reminders and review cadence. | Playbook markdown, scheduler configuration, workbook culture map. | Knowledge capture, onboarding playbooks, review cadences. |
| Knowledge cadence integration | Self-study | Define and document knowledge review cadences within tooling. | Calendar automation, workflow definition, reflection log entry. | Continuous retrospectives, cultural tooling, governance. |

**Extension:** Establish a contribution leaderboard and capture improvement metrics in the workbook learning log.

---

## Module 9 – Management as code and adaptive operating models

**Book alignment:** Chapters 19 *Management as Code*, 20 *AI Agent Team for the Architecture as Code Initiative*, 21 *Digital Transformation through Code-Based Infrastructure*, and Appendix B *Technical Architecture for Book Production*. Relate workbook dashboarding, operating model codification, and leadership playbooks to the practices detailed in the book.

| Exercise | Format | Objective | Key artefacts | Radar prompts |
| --- | --- | --- | --- | --- |
| Operating model codification | Lab | Encode leadership ceremonies and portfolio reviews into workflows. | Workflow files, approval matrices, workbook artefact index. | Documented operating models, codified resource allocation. |
| Metrics dashboard build | Workshop | Produce a dashboard powered by pipeline and radar data. | Dashboard configuration, data lineage notes, workbook registry. | Automated metrics, decision support, feedback loops. |
| Playbook iteration PR | Self-study | Submit updates to the management playbook via pull request. | Pull request link, reviewer feedback, reflection log entry. | Collaborative playbook iteration, governance automation. |

**Extension:** Prototype scenario-based staffing simulations with AI support and record results in the workbook foresight section.

---

## Module 10 – Optimisation, AI assistance, and future readiness

**Book alignment:** Chapters 20 *AI Agent Team for the Architecture as Code Initiative*, 25 *Future Trends and Development*, 26 *Anti-Patterns in Architecture as Code Programmes*, 26 *Prerequisites for Architecture as Code Adoption*, and 27 *Conclusion*. Use the workbook to evidence how foresight activities and capstone plans apply the strategic guidance from these chapters.

| Exercise | Format | Objective | Key artefacts | Radar prompts |
| --- | --- | --- | --- | --- |
| AI-enabled scenario planning | Workshop | Explore AI-assisted operating models and maturity trajectories. | Scenario canvas, AI tool configuration notes, workbook foresight log. | AI-assisted optimisation, self-healing, innovative governance. |
| Anti-pattern remediation lab | Clinic | Identify anti-patterns and design countermeasures linked to radar improvements. | Case study annotations, countermeasure backlog, action plan updates. | Anti-pattern recognition, innovation safeguards. |
| Capstone readiness review | Self-study | Validate the 90-day roadmap and presentation assets. | Workbook capstone checklist, presentation outline, reflection log summary. | Holistic radar review, strategic alignment. |

**Extension:** Compile a sustainability impact addendum evaluating the environmental footprint of automation choices, and store findings in the workbook closing notes.

---

## Facilitator tracking dashboard

Use the following checklist to monitor exercise completion across the cohort. Update it after each session and share progress with participants to maintain accountability.

| Module | Exercise | Status (Not started / In progress / Complete) | Evidence link | Radar delta observed |
| --- | --- | --- | --- | --- |
| 0 | Baseline radar survey |  |  |  |
| 0 | Evidence landscape mapping |  |  |  |
| 0 | Improvement experiment charter |  |  |  |
| 1 | Declarative pipeline build |  |  |  |
| 1 | Post-incident analysis clinic |  |  |  |
| 1 | Module testing sprint |  |  |  |
| 2 | Structurizr workspace build |  |  |  |
| 2 | Architecture review swap |  |  |  |
| 2 | ADR authoring |  |  |  |
| 3 | Broken manifest recovery |  |  |  |
| 3 | Container security drill |  |  |  |
| 3 | Secrets rotation lab |  |  |  |
| 4 | Governance requirement translation |  |  |  |
| 4 | Violation runbook rehearsal |  |  |  |
| 4 | Coverage metrics reflection |  |  |  |
| 5 | Workflow codification |  |  |  |
| 5 | Template accessibility clinic |  |  |  |
| 5 | Exception path rehearsal |  |  |  |
| 6 | Compliance pipeline implementation |  |  |  |
| 6 | Evidence analytics review |  |  |  |
| 6 | Baseline alignment task |  |  |  |
| 7 | Chaos engineering lab |  |  |  |
| 7 | Data stewardship workshop |  |  |  |
| 7 | Coverage gap analysis |  |  |  |
| 8 | Documentation pipeline sprint |  |  |  |
| 8 | Playbook codification |  |  |  |
| 8 | Knowledge cadence integration |  |  |  |
| 9 | Operating model codification |  |  |  |
| 9 | Metrics dashboard build |  |  |  |
| 9 | Playbook iteration PR |  |  |  |
| 10 | AI-enabled scenario planning |  |  |  |
| 10 | Anti-pattern remediation lab |  |  |  |
| 10 | Capstone readiness review |  |  |  |

> Maintain British English spelling throughout all artefacts and ensure that every exercise references evidence stored in version control.
