# GitHub Issue Drafts: Source Verification for Architecture as Code Narrative

The following issue drafts capture the verification work requested for external sources. Each entry summarises the scope, required checks, and recommended labels to apply when creating the live GitHub Issue.

## Issue 1: Confirm AaC Definition and Traditional Architecture Critique
- **Source IDs**: [1]
- **Relevant Manuscript Sections**: Sections 1.1.1–1.1.2 of the Architecture as Code report draft (AaC definition and critique of traditional architecture).
- **Problem Statement**: Ensure the manuscript accurately represents AaC as "live, executable specifications" and faithfully conveys the source's critique of traditional architecture, including "slideware syndrome" and architectural entropy.
- **Acceptance Criteria**:
  - Cite the specific paragraphs in Sections 1.1.1–1.1.2 that describe AaC's definition and the failure modes of traditional approaches.
  - Confirm that the narrative links DevOps-driven change velocity with the need for AaC's embedded governance, as described in Source [1].
  - Document any discrepancies or missing arguments between the source and the manuscript, proposing corrective edits where necessary.
- **Recommended Labels**: `documentation`, `architecture`, `requirements`

## Issue 2: Validate AaC Core Principles and SSOT Delivery Mechanisms
- **Source IDs**: [2], [9]
- **Relevant Manuscript Sections**: Sections 1.2.1 and 2.2.2 covering Adoptability, Extensibility, and Productivity, plus the discussion of AaC as a Single Source of Truth (SSOT).
- **Problem Statement**: Verify that the manuscript's portrayal of AaC's core principles matches Source [2] and that Source [9] is correctly used to emphasise SSOT responsibilities and interfaces (CLI/API).
- **Acceptance Criteria**:
  - Cross-check each principle's description with the wording and nuance from Source [2].
  - Confirm that the SSOT section mentions both CLI and API interfaces when referencing Source [9].
  - Flag any missing attributes or misaligned terminology and suggest precise wording adjustments.
- **Recommended Labels**: `documentation`, `architecture`

## Issue 3: Substantiate AaC's Self-Definition and Plugin System
- **Source IDs**: [3]
- **Relevant Manuscript Sections**: Section 1.2.1 subsections discussing self-definition and extensibility via plugins.
- **Problem Statement**: Ensure the manuscript accurately reflects the GitHub project's emphasis on AaC being self-defining and powered by a robust plugin ecosystem.
- **Acceptance Criteria**:
  - Review the README and repository structure in Source [3] to confirm the prominence of self-definition and plugins.
  - Map repository evidence (e.g., `aac-spec`, plugin directories) to statements in the manuscript.
  - Record any gaps in the manuscript narrative and recommend supporting detail if the source highlights additional plugin capabilities.
- **Recommended Labels**: `documentation`, `architecture`

## Issue 4: Clarify AaC vs. IaC Abstraction and Opinionation
- **Source IDs**: [4], [14]
- **Relevant Manuscript Sections**: Section 3.1.2, including the comparison table contrasting AaC and IaC.
- **Problem Statement**: Validate that Source [4] supports the need for opinionated governance at the architectural level and that Source [14] substantiates the move toward higher-level abstractions (e.g., AWS CDK) bridging IaC and AaC.
- **Acceptance Criteria**:
  - Confirm the table's description of abstraction levels and governance aligns with Source [4]'s commentary on opinionated tooling.
  - Verify that Source [14] is cited where the manuscript discusses IaC tools adopting higher-level constructs akin to AaC.
  - Document any misinterpretations and supply corrected phrasing or additional citations if required.
- **Recommended Labels**: `documentation`, `architecture`

## Issue 5: Verify C4 Model Level Definitions and Anti-Decay Guidance
- **Source IDs**: [5], [6]
- **Relevant Manuscript Sections**: Sections 2.1.1 and 2.1.2, including the C4 hierarchy table and discussion of diagram automation.
- **Problem Statement**: Ensure the four C4 levels (Context, Container, Component, Code) are defined exactly as Source [5] specifies and that Source [6]'s guidance on automation and audience targeting is correctly represented.
- **Acceptance Criteria**:
  - Cross-reference each C4 level description in the manuscript with Source [5].
  - Validate the manuscript's discussion of "diagram decay" and automation best practices against Source [6].
  - Produce a summary table of any discrepancies and recommended edits.
- **Recommended Labels**: `documentation`, `architecture`, `qa`

## Issue 6: Confirm Industry Trend Data Driving AaC Adoption
- **Source IDs**: [7]
- **Relevant Manuscript Sections**: Section 4.1.2 covering microservices and event-driven architecture statistics.
- **Problem Statement**: Verify the percentages (e.g., 67% microservice adoption) and interpretative statements drawn from Source [7], ensuring they justify AaC's role in managing distributed complexity.
- **Acceptance Criteria**:
  - Extract exact figures from Source [7] and cross-check against the manuscript's claims.
  - Evaluate whether the manuscript's conclusion about formal boundary definition is substantiated by the source data.
  - Note any additional statistics from Source [7] that should be incorporated for completeness.
- **Recommended Labels**: `documentation`, `requirements`

## Issue 7: Review Historical Context of Model-Driven Development
- **Source IDs**: [8]
- **Relevant Manuscript Sections**: Section 2.2.1 discussing MDD shortcomings and AaC's modern positioning.
- **Problem Statement**: Ensure the manuscript accurately summarises historical criticisms of Model-Driven Development and the role of modern tooling (e.g., Structurizr) as highlighted in Source [8].
- **Acceptance Criteria**:
  - Compare the manuscript's depiction of MDD limitations with Source [8]'s account.
  - Confirm that references to modern MBSE-aligned tools reflect the source's examples and rationale.
  - Recommend refinements if key arguments from the source are missing or misrepresented.
- **Recommended Labels**: `documentation`, `architecture`

## Issue 8: Validate IaC Market Data and Economic Rationale
- **Source IDs**: [10], [11], [12], [13]
- **Relevant Manuscript Sections**: Sections 3.1.1 and 4.1.1 covering IaC definitions, market forecasts, and operational/economic benefits.
- **Problem Statement**: Confirm that the manuscript's market size figures (e.g., $3.75 billion forecast) and benefit statements align with the cited sources and support the argument that IaC paves the way for AaC.
- **Acceptance Criteria**:
  - Cross-check all quantitative data (market size, growth rates) against Source [11].
  - Ensure Source [10] underpins the definition of IaC used in the manuscript.
  - Validate that Sources [12] and [13] support the described operational and economic benefits.
  - Highlight any data gaps and suggest supplementary evidence if necessary.
- **Recommended Labels**: `documentation`, `requirements`

## Issue 9: Assess IaC Testability Claims (Pulumi vs Terraform)
- **Source IDs**: [15]
- **Relevant Manuscript Sections**: Section 3.2.1 focusing on testability and comparison between Pulumi and Terraform.
- **Problem Statement**: Ensure the manuscript accurately reflects Source [15]'s assessment of Pulumi's programmatic testing advantages over Terraform's declarative model.
- **Acceptance Criteria**:
  - Compare the manuscript's claims with the source's discussion of unit testing and developer workflows.
  - Verify that Pulumi's strengths and Terraform's limitations are presented in balance with the source material.
  - Document any areas where the manuscript extrapolates beyond the source and suggest corrective language.
- **Recommended Labels**: `documentation`, `qa`

## Issue 10: Reinforce IaC State Management Security Guidance
- **Source IDs**: [16]
- **Relevant Manuscript Sections**: Section 3.2.2 covering state file security requirements.
- **Problem Statement**: Confirm that the manuscript highlights remote storage, encryption at rest, and key management practices for IaC state files consistent with Source [16].
- **Acceptance Criteria**:
  - Cross-verify each security recommendation against the source.
  - Ensure the manuscript links these practices to AaC's governance posture.
  - Propose additional remediation steps if the source outlines further controls not yet captured in the manuscript.
- **Recommended Labels**: `documentation`, `security`

---

*Prepared for manual issue creation to maintain rigorous source alignment across the Architecture as Code manuscript.*
