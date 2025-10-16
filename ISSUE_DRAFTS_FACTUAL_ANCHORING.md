# GitHub Issue Drafts – Factual Anchoring of Documentation

This file captures the issue drafts required to implement the "Factual Anchoring of Documentation" action plan. Each draft includes context, priority, and acceptance criteria so the issues can be copied into GitHub with the correct labels.

## Issue: Highlight Microservice Complexity as AaC's Primary Driver

**Priority:** High  
**Suggested Labels:** documentation, architecture  
**Linked Finding:** #6 – Microservice Complexity

### Summary
Elevate the archived microservices rationale so the book's primary chapters immediately communicate that AaC addresses modern distributed system complexity.

### Background
The archived chapter `docs/archive/08_microservices.md` retains vital statistics and reasoning that explain why AaC emerged as a response to microservice sprawl. These insights currently sit outside the main narrative, diluting the opening argument. Reintegrating the most compelling evidence into the introduction and containerisation chapters will reinforce the urgency of AaC and combat the "slideware syndrome" critique.

### Acceptance Criteria
- [ ] Extract the most persuasive facts, statistics, and challenge statements from `docs/archive/08_microservices.md`.
- [ ] Update `docs/01_introduction.md` to reference microservice-induced complexity as the motivating problem statement, explicitly linking it to AaC adoption.
- [ ] Expand `docs/07_containerization.md` with a section explaining how container and microservice patterns necessitate AaC for coherence and governance.
- [ ] Ensure inserted content cites the appropriate sources already catalogued in `docs/33_references.md`.

### Additional Notes
Confirm that any references to historical anecdotes or statistics remain accurate and use British English terminology throughout.

---

## Issue: Emphasise Testable IaC for Practical AaC Execution

**Priority:** High  
**Suggested Labels:** documentation, qa  
**Linked Finding:** #9 – IaC Testability

### Summary
Clarify that AaC's quality promise depends on adopting IaC tooling that supports unit and integration testing, highlighting Pulumi and AWS CDK as exemplars.

### Background
AaC extends beyond documentation; it demands executable, testable architectural artefacts. Tools such as Pulumi and AWS CDK enable infrastructure definitions in general-purpose languages, unlocking unit testing and CI-friendly validation. The practical implementation and testing chapters need explicit guidance that positions these tools over purely declarative options when test coverage is paramount.

### Acceptance Criteria
- [ ] Add a dedicated subsection to `docs/14_practical_implementation.md` (and reference `docs/13_testing_strategies.md` if necessary) that explains why AaC favours IaC platforms supporting unit tests.
- [ ] Provide concrete examples of how Pulumi or AWS CDK facilitate architectural testing workflows.
- [ ] Contrast this approach with declarative-only tools (e.g., Terraform) in terms of testability, whilst acknowledging their place within the ecosystem.
- [ ] Reference the relevant sources from the verified list (Source [16] or others) to substantiate claims about testing capability.

### Additional Notes
Coordinate with the testing strategies chapter so messaging is consistent and avoids duplication.

---

## Issue: Clarify AaC versus IaC Abstraction Responsibilities

**Priority:** Medium  
**Suggested Labels:** documentation, architecture  
**Linked Finding:** #4 – Abstraction and Opinionation

### Summary
Strengthen the automation chapter with an explicit comparison between AaC and IaC abstraction layers, using visuals or call-out boxes to prevent reader confusion.

### Background
Readers must grasp that AaC specifies architectural intent and guardrails, while IaC implements the concrete infrastructure. Without a clear delineation, automation discussions risk conflating responsibilities. Introducing a visual diagram or structured explainer in `docs/05_automation_devops_cicd.md` will sharpen understanding and underline governance themes.

### Acceptance Criteria
- [ ] Review the current narrative in `docs/05_automation_devops_cicd.md` and identify where clarification is most impactful.
- [ ] Add a diagram (Mermaid or similar) or a visually distinct text box contrasting AaC and IaC roles.
- [ ] Emphasise how AaC embeds governance and standardisation, with IaC executing the specifics.
- [ ] Cite the relevant findings and sources so readers can trace the factual basis for the distinction.

### Additional Notes
Coordinate with existing diagrams to maintain stylistic consistency (fonts, colours, British English spellings).

---

## Issue: Anchor IaC State Security Guidance to Verified Sources

**Priority:** High  
**Suggested Labels:** documentation, security  
**Linked Finding:** #10 – State Management Security

### Summary
Ensure the security chapters explicitly cite Source [16] (and other relevant references) when discussing the protection of IaC state files.

### Background
Secure management of IaC state, including encryption, storage location, and access control, is a critical risk area. Although the chapters `docs/09a_security_fundamentals.md` and `docs/09b_security_patterns.md` describe best practices, they require precise source attribution to reinforce credibility and auditability.

### Acceptance Criteria
- [ ] Audit the sections covering IaC state storage and protection within `docs/09a_security_fundamentals.md` and `docs/09b_security_patterns.md`.
- [ ] Insert explicit citations to Source [16] (and any other corroborating sources) wherever these controls are described.
- [ ] Verify that citation formatting matches the repository standard and links correctly to `docs/33_references.md`.
- [ ] Update language as required to maintain alignment with the verified factual statements.

### Additional Notes
If any statements cannot be backed by the referenced sources, adjust or remove them accordingly.

---

## Issue: Complete Reference Chapter for Verified Sources

**Priority:** High  
**Suggested Labels:** documentation, qa  
**Linked Findings:** #1–#10 – Comprehensive Verification

### Summary
Confirm that the references chapter lists every source used in the verification effort and that cross-references throughout the book resolve correctly.

### Background
The documentation overhaul depends on 16 verified sources. To maintain traceability, `docs/33_references.md` must include each source in the agreed format, and internal citations throughout the chapters (including updated ones) must point back accurately.

### Acceptance Criteria
- [ ] Review `docs/33_references.md` and confirm all 16 verified sources are present, correctly formatted, and alphabetically or logically ordered per repository standards.
- [ ] Check chapters touched by recent factual updates (e.g., `docs/01_introduction.md`, `docs/02_fundamental_principles.md`, `docs/06_structurizr.md`, and any other affected files) to ensure their reference links resolve to entries in `docs/33_references.md`.
- [ ] Add or correct anchors, link identifiers, or numbering so citations remain consistent after new content is integrated.
- [ ] Document any discrepancies or missing sources for follow-up if they cannot be resolved immediately.

### Additional Notes
Consider producing a short changelog within the issue comments to track reference updates once completed.

