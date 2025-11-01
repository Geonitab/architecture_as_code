# Architecture as Code Course Working Materials

This pack equips facilitators and participants with structured agendas, artefact templates, and practice exercises that reinforce the maturity radar checkpoints introduced in the *Architecture as Code* curriculum. Every activity emphasises evidence capture in version control and reflective improvement tied to radar deltas.

## Facilitation guidance

- **Cohort readiness:** Circulate Module 0 pre-work one week in advance and confirm that all attendees have access to shared repositories, collaboration boards, and the radar survey tool.
- **Tooling expectations:** Encourage teams to provision lightweight sandboxes (e.g. Terraform Cloud trial, Kubernetes kind cluster) ahead of practice labs to minimise set-up time during sessions.
- **Evidence discipline:** Reinforce that every deliverable must reference artefacts in source control. Screenshots alone are insufficient; link to commits, pipelines, and generated documentation.
- **Reflection rhythm:** Allocate the final fifteen minutes of each live session to update radar scores, log blockers, and agree on one improvement experiment per participant.

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
- **Interactive exercise:** *Radar evidence map* – participants list existing artefacts, decide whether they are codified, and identify immediate automation opportunities.
- **Self-study assignment:** Draft a personal learning goal statement connecting one radar weakness to expected organisational outcomes. Store the statement in the shared repository using the reflection log template.

### Module 1 – Infrastructure as code foundations
- **Live lab:** Build a declarative pipeline that provisions a repeatable environment.
  - Starter assets: repository skeleton with Terraform and Pulumi directories, GitHub Actions workflow stub, policy check placeholder.
  - Tasks: implement automated linting, plan/apply gates, and drift detection job; raise a pull request describing review expectations.
- **Case discussion:** Compare two anonymised post-incident reports that highlight manual deployment anti-patterns. Learners tag each remediation with the relevant radar prompt.
- **Self-study challenge:** Extend the lab pipeline with automated module testing and submit evidence links plus a retrospective entry via the lab checklist.

### Module 2 – Architecture as code modelling
- **Workshop focus:** Create and validate a Structurizr DSL workspace representing a shared platform.
  - Activities: model the system context, container, and component diagrams; set up automated diagram export in CI; link decision records to model elements.
  - Quality bar: linting pipeline passes, diagrams refresh automatically, ADR references resolve.
- **Peer review clinic:** Swap repositories to critique naming conventions, traceability, and documentation alignment using the provided checklist.
- **Self-study assignment:** Capture an ADR describing the modelling approach trade-offs and submit via pull request with reviewer sign-off.

### Module 3 – Containerisation and orchestration at scale
- **Simulation:** Teams receive a broken deployment manifest and must restore service whilst implementing blue-green release automation.
  - Deliverables: corrected manifests, rollout script, automated smoke tests, and a readme describing rollback triggers.
- **Security drill:** Run container image scanning and map findings to radar prompts on policy enforcement and remediation.
- **Self-study lab:** Configure secrets management integration (e.g. Sealed Secrets) and document rotation procedures in the action plan canvas.

### Module 4 – Policy as code and security automation
- **Scenario workshop:** Translate written governance requirements into Open Policy Agent rules enforced in CI.
  - Stages: policy authoring, unit testing, pipeline integration, and incident simulation.
- **Runbook rehearsal:** Practise responding to a policy violation alert using the predefined runbook template.
- **Self-study reflection:** Update the radar log with enforcement coverage metrics and identify any manual approvals that must be codified.

### Module 5 – Governance as code operations
- **Process mapping exercise:** Visualise the current governance workflow, then encode it using repository-based configuration files.
- **Template clinic:** Customise governance request templates to support non-technical stakeholders, collecting feedback during role-play sessions.
- **Self-study action:** Trial an exception path in a lower environment, capture automated evidence, and report findings using the lab checklist.

### Module 6 – Compliance as code evidence flows
- **Hands-on lab:** Implement a compliance control pipeline that executes checks, stores evidence artefacts, and raises remediation tickets.
- **Analytics review:** Inspect reporting outputs and ensure traceability between controls, evidence, and issue management systems.
- **Self-study assignment:** Align two organisational controls to a shared baseline and document the mapping using the action plan canvas.

### Module 7 – Testing as code for resilient platforms
- **Chaos experiment:** Design and run a failure injection scenario, then measure detection and recovery metrics.
- **Data management clinic:** Demonstrate synthetic data generation scripts and define governance for data refresh cycles.
- **Self-study activity:** Update the test matrix with coverage gaps, including proposed automation to close each gap.

### Module 8 – Documentation, knowledge, and culture as code
- **Publishing sprint:** Configure automated documentation builds, including diagram regeneration and quality checks.
- **Cultural codification exercise:** Author a playbook for onboarding a new team using markdown templates and scheduled reminders.
- **Self-study deliverable:** Record a knowledge review cadence and integrate it into the cohort’s documentation pipeline.

### Module 9 – Management as code and adaptive operating models
- **Operating model lab:** Convert leadership ceremonies and reporting cadences into workflow definitions.
- **Dashboard practicum:** Build a lightweight metrics dashboard fed by pipeline outputs and radar data.
- **Self-study brief:** Submit a pull request updating the management playbook with revised staffing models and review annotations.

### Module 10 – Optimisation, AI assistance, and future readiness
- **Foresight workshop:** Facilitate scenario planning exercises combining AI-assisted operations with maturity radar trajectories.
- **Anti-pattern clinic:** Analyse case studies to identify blockers, then formulate countermeasures logged in the action plan canvas.
- **Capstone preparation:** Finalise the 90-day roadmap, ensuring alignment with radar improvements and evidence captured across previous modules.

## Cross-module artefacts

- **Radar reflection log:** Weekly entry capturing the updated score, supporting evidence, blockers, and planned experiments.
- **Lab submission checklist:** Consistent review gates covering version control hygiene, automated testing, policy enforcement, documentation, and sign-off.
- **Action plan canvas:** Shared template to articulate improvement experiments, expected outcomes, ownership, and integration with strategic objectives.
- **Facilitator debrief notes:** After each session, document observed trends, participant needs, and adjustments required for subsequent modules.

## Assessment alignment

| Assessment | Supporting artefacts | Evidence expectations |
| --- | --- | --- |
| Weekly reflection logs | Radar reflection log, lab submission checklist | Updated radar scores, experiment summaries, evidence links |
| Lab artefacts | Repository branches, automated pipeline outputs, runbooks | Passing pipelines, peer review sign-off, documentation updates |
| Capstone action plan | Action plan canvas, roadmap presentation | Measurable 90-day objectives, traceability to radar deltas, executive-ready narrative |
| Final presentation | Slide deck sourced from repository, demo environment | Showcases improvements, lessons learned, and leadership engagement |

Ensure that every artefact is stored within the shared version-controlled workspace and tagged with the relevant module identifier to ease discovery and audit.
