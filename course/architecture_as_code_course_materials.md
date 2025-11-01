# Architecture as Code Course Working Materials

This pack equips facilitators and participants with structured agendas, artefact templates, and practice exercises that reinforce the maturity radar checkpoints introduced in the *Architecture as Code* curriculum. Every activity emphasises evidence capture in version control and reflective improvement tied to radar deltas. Use this pack alongside the module workbook template to capture outcomes, decisions, and improvement experiments in a consistent format.

## Facilitation guidance

- **Cohort readiness:** Circulate Module 0 pre-work one week in advance and confirm that all attendees have access to shared repositories, collaboration boards, and the radar survey tool.
- **Tooling expectations:** Encourage teams to provision lightweight sandboxes (e.g. Terraform Cloud trial, Kubernetes kind cluster) ahead of practice labs to minimise set-up time during sessions.
- **Evidence discipline:** Reinforce that every deliverable must reference artefacts in source control. Screenshots alone are insufficient; link to commits, pipelines, and generated documentation.
- **Reflection rhythm:** Allocate the final fifteen minutes of each live session to update radar scores, log blockers, and agree on one improvement experiment per participant.
- **Workbook usage:** Require every participant team to clone the module workbook template before the session begins and populate it collaboratively during each agenda block. Facilitators should review workbook entries during breaks to surface gaps or coaching needs.
- **Assessment mapping:** Connect every live task and asynchronous assignment to the capstone criteria so that learners understand how weekly outputs compound towards the final assessment.

## Module-by-module materials

### Module 0 – Orientation and radar benchmarking
- **Live session run sheet (2.5 hours):**
  1. Welcome circle and cohort norms (20 minutes).
  2. Radar walkthrough with exemplar evidence (40 minutes).
  3. Individual completion of the radar survey (35 minutes).
  4. Break (10 minutes).
  5. Small-group synthesis of weakest disciplines and current tooling (30 minutes).
  6. Plenary share-back with prioritised focus areas (30 minutes).
  7. Improvement experiment selection and next steps (15 minutes).
  8. Workbook wrap (10 minutes) – teams record commitments, backlog items, and evidence gaps in the module workbook.
- **Interactive exercise:** *Radar evidence map* – participants list existing artefacts, decide whether they are codified, and identify immediate automation opportunities. Capture the map as a markdown table within the workbook so that it can evolve during later modules.
- **Asynchronous reinforcement:** Provide a narrated walkthrough of the radar tool that participants can revisit. Encourage reflection log entries within 48 hours to reinforce baseline insights.
- **Self-study assignment:** Draft a personal learning goal statement connecting one radar weakness to expected organisational outcomes. Store the statement in the shared repository using the reflection log template and link it from the workbook.

### Module 1 – Infrastructure as code foundations
- **Live lab:** Build a declarative pipeline that provisions a repeatable environment.
  - Starter assets: repository skeleton with Terraform and Pulumi directories, GitHub Actions workflow stub, policy check placeholder.
  - Tasks: implement automated linting, plan/apply gates, drift detection job, and branch protection aligned to radar prompts; raise a pull request describing review expectations.
  - Workbook capture: document chosen tooling, pipeline screenshots, and evidence links in the lab section of the workbook.
- **Case discussion:** Compare two anonymised post-incident reports that highlight manual deployment anti-patterns. Learners tag each remediation with the relevant radar prompt and update the workbook with mitigation commitments.
- **Playground extension:** Provide an optional sandbox challenge to implement infrastructure testing using Terratest or Checkov with success criteria listed in the workbook.
- **Self-study challenge:** Extend the lab pipeline with automated module testing and submit evidence links plus a retrospective entry via the lab checklist. Update the reflection log with observed maturity shifts.

### Module 2 – Architecture as code modelling
- **Workshop focus:** Create and validate a Structurizr DSL workspace representing a shared platform.
  - Activities: model the system context, container, and component diagrams; set up automated diagram export in CI; link decision records to model elements.
  - Quality bar: linting pipeline passes, diagrams refresh automatically, ADR references resolve. Document evidence and outstanding actions inside the workbook quality checklist.
- **Peer review clinic:** Swap repositories to critique naming conventions, traceability, and documentation alignment using the provided checklist. Capture peer feedback and agreed remediations in the workbook review log.
- **Reference material:** Share a curated gallery of Structurizr examples mapped to maturity radar scores to inspire improvement experiments.
- **Self-study assignment:** Capture an ADR describing the modelling approach trade-offs and submit via pull request with reviewer sign-off. Log the ADR link in the reflection log and workbook.

### Module 3 – Containerisation and orchestration at scale
- **Simulation:** Teams receive a broken deployment manifest and must restore service whilst implementing blue-green release automation.
  - Deliverables: corrected manifests, rollout script, automated smoke tests, and a readme describing rollback triggers.
  - Workbook prompts: record failure symptoms, diagnostic steps, and recovery verification evidence.
- **Security drill:** Run container image scanning and map findings to radar prompts on policy enforcement and remediation. Log critical vulnerabilities, remediation owners, and pipeline updates in the workbook risk log.
- **Architecture roundtable:** Debate how container orchestration decisions influence the radar’s governance and compliance dimensions, noting cross-discipline dependencies in the workbook.
- **Self-study lab:** Configure secrets management integration (e.g. Sealed Secrets) and document rotation procedures in the action plan canvas. Update the reflection log with evidence of automated secrets validation.

### Module 4 – Policy as code and security automation
- **Scenario workshop:** Translate written governance requirements into Open Policy Agent rules enforced in CI.
  - Stages: policy authoring, unit testing, pipeline integration, and incident simulation.
  - Workbook documentation: capture policy snippets, test evidence, and residual manual controls.
- **Runbook rehearsal:** Practise responding to a policy violation alert using the predefined runbook template. Record timing metrics and improvement actions in the workbook operations log.
- **Game day extension:** Facilitate a tabletop exercise simulating concurrent policy breaches to stress-test escalation paths. Summarise lessons learned within the workbook retrospective section.
- **Self-study reflection:** Update the radar log with enforcement coverage metrics and identify any manual approvals that must be codified. Link metrics dashboards or alert outputs from the lab checklist.

### Module 5 – Governance as code operations
- **Process mapping exercise:** Visualise the current governance workflow, then encode it using repository-based configuration files. Store before-and-after artefacts and code snippets in the workbook attachments section.
- **Template clinic:** Customise governance request templates to support non-technical stakeholders, collecting feedback during role-play sessions. Log stakeholder quotes, accessibility adjustments, and backlog items in the workbook.
- **Facilitated debate:** Explore how governance automation interfaces with cultural change, referencing the maturity radar prompts. Capture alignment decisions and policy owners in the workbook governance matrix.
- **Self-study action:** Trial an exception path in a lower environment, capture automated evidence, and report findings using the lab checklist. Update the action plan canvas with required governance control updates.

### Module 6 – Compliance as code evidence flows
- **Hands-on lab:** Implement a compliance control pipeline that executes checks, stores evidence artefacts, and raises remediation tickets. Use the workbook pipeline tracker to log control status and evidence locations.
- **Analytics review:** Inspect reporting outputs and ensure traceability between controls, evidence, and issue management systems. Summarise findings in the workbook analytics summary, highlighting radar score implications.
- **Guest insight:** Invite compliance partners to review artefacts and comment on audit readiness. Capture their feedback verbatim in the workbook stakeholder feedback table.
- **Self-study assignment:** Align two organisational controls to a shared baseline and document the mapping using the action plan canvas. Reference the baseline within the reflection log and workbook.

### Module 7 – Testing as code for resilient platforms
- **Chaos experiment:** Design and run a failure injection scenario, then measure detection and recovery metrics. Record experiment hypotheses, telemetry outputs, and recovery time comparisons in the workbook experiment log.
- **Data management clinic:** Demonstrate synthetic data generation scripts and define governance for data refresh cycles. Populate the workbook data stewardship checklist with owners, controls, and review cadences.
- **Automation benchmarking:** Compare testing coverage across teams using the lab submission checklist as a scoring guide. Capture insights and improvement priorities in the workbook scoreboard.
- **Self-study activity:** Update the test matrix with coverage gaps, including proposed automation to close each gap. Provide evidence links in the reflection log and workbook.

### Module 8 – Documentation, knowledge, and culture as code
- **Publishing sprint:** Configure automated documentation builds, including diagram regeneration and quality checks. Log pipeline timings, quality gate results, and outstanding technical debt in the workbook publishing ledger.
- **Cultural codification exercise:** Author a playbook for onboarding a new team using markdown templates and scheduled reminders. Document rituals, communication channels, and playbook reviewers in the workbook culture map.
- **Knowledge exchange forum:** Host a lightning talk round where teams share documentation wins. Capture recording links and feedback in the workbook learning log.
- **Self-study deliverable:** Record a knowledge review cadence and integrate it into the cohort’s documentation pipeline. Note the cadence within both the reflection log and workbook.

### Module 9 – Management as code and adaptive operating models
- **Operating model lab:** Convert leadership ceremonies and reporting cadences into workflow definitions. Attach workflow definitions, automation scripts, and approval matrices within the workbook artefact index.
- **Dashboard practicum:** Build a lightweight metrics dashboard fed by pipeline outputs and radar data. Capture metric definitions, data lineage, and access controls in the workbook dashboard registry.
- **Leadership fishbowl:** Facilitate a conversation with senior stakeholders reviewing management artefacts. Record decisions, follow-up actions, and radar impacts in the workbook governance log.
- **Self-study brief:** Submit a pull request updating the management playbook with revised staffing models and review annotations. Link the pull request from the reflection log and workbook.

### Module 10 – Optimisation, AI assistance, and future readiness
- **Foresight workshop:** Facilitate scenario planning exercises combining AI-assisted operations with maturity radar trajectories. Document chosen scenarios, AI enablers, and ethical considerations in the workbook foresight log.
- **Anti-pattern clinic:** Analyse case studies to identify blockers, then formulate countermeasures logged in the action plan canvas. Summarise anti-pattern signals and countermeasures in the workbook improvement backlog.
- **Capstone preparation:** Finalise the 90-day roadmap, ensuring alignment with radar improvements and evidence captured across previous modules. Use the workbook capstone checklist to verify that success measures, ownership, and follow-up cadences are recorded.
- **Celebration circle:** Close the cohort with a facilitated retrospective and acknowledgement round. Capture appreciations, commitments, and planned community-of-practice rituals in the workbook closing notes.

## Cross-module artefacts

- **Radar reflection log:** Weekly entry capturing the updated score, supporting evidence, blockers, and planned experiments.
- **Lab submission checklist:** Consistent review gates covering version control hygiene, automated testing, policy enforcement, documentation, and sign-off.
- **Action plan canvas:** Shared template to articulate improvement experiments, expected outcomes, ownership, and integration with strategic objectives.
- **Module workbook:** Living document per team that records session notes, artefact links, feedback, and radar adjustments across all activities.
- **Facilitator debrief notes:** After each session, document observed trends, participant needs, and adjustments required for subsequent modules.

## Assessment alignment

| Assessment | Supporting artefacts | Evidence expectations |
| --- | --- | --- |
| Weekly reflection logs | Radar reflection log, lab submission checklist, module workbook | Updated radar scores, experiment summaries, evidence links |
| Lab artefacts | Repository branches, automated pipeline outputs, runbooks, workbook lab entries | Passing pipelines, peer review sign-off, documentation updates |
| Capstone action plan | Action plan canvas, roadmap presentation, workbook capstone checklist | Measurable 90-day objectives, traceability to radar deltas, executive-ready narrative |
| Final presentation | Slide deck sourced from repository, demo environment, workbook closing notes | Showcases improvements, lessons learned, and leadership engagement |

Ensure that every artefact is stored within the shared version-controlled workspace and tagged with the relevant module identifier to ease discovery and audit. Reference the module workbook in pull requests so that reviewers can trace context rapidly.
