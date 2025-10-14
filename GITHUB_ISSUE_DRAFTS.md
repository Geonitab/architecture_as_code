# GitHub Issue Drafts – Architecture as Code Content Updates

The following issue drafts convert recent Swedish-language feedback into actionable GitHub issues. Each draft includes a proposed title, summary, scope, task list, acceptance criteria, and suggested labels so they can be copied directly into the repository issue tracker.

## Issue: Highlight Management as Code in the Introduction Overview
**Summary:** Ensure the introduction chapter explicitly lists Management as Code as one of the core Architecture as Code dimensions and refresh supporting visuals if necessary.
**Scope:** `docs/01_introduction.md`, `docs/images/diagram_01_aac_flow.mmd`
**Tasks:**
- Update the textual description of interconnected “as Code” practices to include Management as Code alongside existing aspects.
- Review accompanying diagrams or captions to confirm Management as Code appears with equal prominence.
- Validate that the change keeps the prose consistent in tone and tense with the rest of the chapter.
**Acceptance Criteria:**
- The introduction explicitly references Management as Code in the list of Architecture as Code dimensions.
- Any related diagram or caption reflects the additional aspect without layout issues.
- Language remains fully English and aligns with the book’s editorial style guide.
**Suggested Labels:** documentation, requirements

## Issue: Reformat the ADR Lifecycle Diagram into a Vertical Layout
**Summary:** Adjust the ADR lifecycle illustration so that it uses a vertical orientation, improving readability when rendered in the book.
**Scope:** `docs/images/diagram_04_adr_lifecycle.mmd`, `docs/images/diagram_04_adr_lifecycle.png`
**Tasks:**
- Update the Mermaid source to draw the lifecycle steps vertically (top-to-bottom) with consistent spacing.
- Regenerate the PNG asset using the updated diagram definition.
- Verify that references inside `docs/04_adr.md` still align with the new visual proportions.
**Acceptance Criteria:**
- The lifecycle diagram displays vertically when the book is built, with labels remaining legible on standard page widths.
- Generated PNG passes existing build scripts without additional warnings.
- Chapter text accurately describes the updated layout.
**Suggested Labels:** design, documentation

## Issue: Replace ADR Example 2 with a Globally Relevant Scenario
**Summary:** Substitute the Sweden-centric ADR example in Chapter 4 with a scenario that applies to an international audience.
**Scope:** `docs/04_adr.md`
**Tasks:**
- Draft a new Example 2 that focuses on a universal security or architecture challenge without referencing Swedish regulations.
- Ensure the structure follows the ADR template and remains technically accurate.
- Remove residual Swedish terminology or localisation references within the section.
**Acceptance Criteria:**
- Example 2 presents a globally applicable case study with neutral terminology.
- Markdown formatting for the ADR example renders correctly in previews and PDF output.
- No explicit references to Sweden or Swedish-specific regulations remain in the example.
**Suggested Labels:** documentation, architecture

## Issue: Update ADR Repository Structure Example
**Summary:** Remove the `infrastructure/` directory from the ADR Git structure example to align with the desired repository layout.
**Scope:** `docs/04_adr.md`
**Tasks:**
- Edit the repository tree snippet so it no longer includes the `infrastructure/` folder.
- Confirm surrounding explanatory text still makes sense without the removed entry.
- Proofread the section for consistent indentation and code-block styling.
**Acceptance Criteria:**
- The Git tree example shows the revised directory structure without `infrastructure/`.
- Markdown renders the snippet as a correctly formatted code block.
- Adjacent prose requires no further clarifications about the removed folder.
**Suggested Labels:** documentation

## Issue: Remove Sweden-Specific Positioning from the ADR Chapter
**Summary:** Rework Chapter 4 to eliminate Swedish localisation, ensuring terminology and guidance apply to a broad international readership.
**Scope:** `docs/04_adr.md`
**Tasks:**
- Replace Swedish references (regulations, agencies, currency, geography) with globally relevant equivalents or neutral language.
- Review the chapter introduction, compliance sections, and summary for localisation cues.
- Maintain factual accuracy while preserving the instructional intent of each paragraph.
**Acceptance Criteria:**
- Chapter 4 contains no Sweden-specific mentions unless they are explicitly required as optional examples.
- Revised text remains grammatically correct and stylistically aligned with other chapters.
- Links and citations continue to reference authoritative, globally applicable sources.
**Suggested Labels:** documentation, editorial

## Issue: Break Chapter 5 into Smaller Automation and DevOps Sections
**Summary:** Refactor “Automation, DevOps and CI/CD for Architecture as Code” into a set of shorter, focused chapters or subsections for improved readability.
**Scope:** `docs/05_automation_devops_cicd.md`, potential new chapter files, `docs/book_structure.md`
**Tasks:**
- Identify logical groupings (e.g., automation fundamentals, governance, compliance, pipelines) and outline the new structure.
- Split the existing content into separate markdown files or well-defined subsections, updating navigation metadata as needed.
- Refresh `docs/book_structure.md` (and any table of contents files) to reflect the new organisation.
**Acceptance Criteria:**
- Chapter 5 no longer exists as a single monolithic file; content is modularised according to the approved outline.
- Internal links and references continue to work after the reorganisation.
- Book structure documentation reflects the updated chapter breakdown.
**Suggested Labels:** documentation, architecture

## Issue: Increase Readability of the Automation Timeline Diagram
**Summary:** Adjust the implementation timeline illustration so that it is taller and easier to read in the exported PDF.
**Scope:** `docs/images/diagram_05_gantt_timeline.mmd`, `docs/images/diagram_05_gantt_timeline.png`
**Tasks:**
- Modify the Mermaid configuration to increase vertical spacing, font size, or aspect ratio.
- Regenerate the PNG asset and confirm clarity when embedded in Chapter 5.
- Verify that the surrounding caption and text still describe the updated visual accurately.
**Acceptance Criteria:**
- The regenerated timeline diagram is legible without zooming in the PDF output.
- Build scripts regenerate the PNG without errors.
- Chapter content aligns with the adjusted timeline layout.
**Suggested Labels:** design, documentation

## Issue: Generalise Chapter 5 Content Beyond Sweden
**Summary:** Remove Sweden-centric references from the automation and DevOps chapter so the guidance applies globally.
**Scope:** `docs/05_automation_devops_cicd.md`
**Tasks:**
- Replace mentions of Swedish regulations, agencies, and currency with international or neutral equivalents.
- Rephrase localisation-dependent examples to address a global audience.
- Conduct a language pass to ensure consistent English prose after the edits.
**Acceptance Criteria:**
- Chapter 5 contains no Sweden-specific focus unless retained as optional callouts explicitly marked as such.
- Revised text reads fluently in English and matches editorial standards.
- Regulatory references, if any, cite international frameworks or clearly indicate regional variability.
**Suggested Labels:** documentation, editorial

## Issue: Move Governance as Code Guidance into a Dedicated Chapter
**Summary:** Extract the Governance as Code material from the automation chapter and integrate it into the standalone governance chapter (or create a new one if required).
**Scope:** `docs/05_automation_devops_cicd.md`, `docs/11_governance_as_code.md`
**Tasks:**
- Identify all Governance as Code sections currently embedded in Chapter 5.
- Relocate and adapt the content within `docs/11_governance_as_code.md` (or a new chapter) to avoid duplication.
- Ensure cross-references between chapters point to the consolidated governance content.
**Acceptance Criteria:**
- Chapter 5 no longer contains lengthy Governance as Code subsections.
- Governance concepts appear in the dedicated chapter with cohesive flow and updated context.
- Internal links and references resolve correctly after the move.
**Suggested Labels:** documentation, architecture

## Issue: Relocate GDPR Coverage to the Compliance Chapter
**Summary:** Move the GDPR-specific automation guidance into the compliance chapter to centralise regulatory material.
**Scope:** `docs/05_automation_devops_cicd.md`, `docs/12_compliance.md`
**Tasks:**
- Extract GDPR subsections and supporting examples from Chapter 5.
- Integrate the content into `docs/12_compliance.md`, updating headings, transitions, and citations as needed.
- Replace the original sections with concise cross-references back to the compliance chapter.
**Acceptance Criteria:**
- GDPR content resides primarily within the compliance-focused chapter.
- Chapter 5 retains only high-level pointers to compliance considerations, avoiding duplication.
- All moved sections maintain fully English language and correct formatting.
**Suggested Labels:** documentation, compliance

## Issue: Spin Off CI/CD Pipeline Details into Their Own Chapter
**Summary:** Create a dedicated chapter for Architecture as Code CI/CD pipeline patterns and remove the deep-dive section from Chapter 5.
**Scope:** `docs/05_automation_devops_cicd.md`, new chapter file (e.g., `docs/06_architecture_pipelines.md`), `docs/book_structure.md`
**Tasks:**
- Draft an outline for the standalone pipeline chapter, covering architecture tracks, YAML examples, and operational guidance.
- Move existing pipeline narratives, diagrams, and examples into the new file, updating references accordingly.
- Update the book structure documentation and any navigation elements to include the new chapter.
**Acceptance Criteria:**
- Chapter 5 references the dedicated pipeline chapter instead of containing the full text.
- The new chapter compiles without linting or build issues and maintains consistent tone.
- Links from other chapters resolve correctly to the new pipeline content.
**Suggested Labels:** documentation, architecture

## Issue: Remove the “Swedish Architecture Testing Framework” Section
**Summary:** Delete the localised testing framework section from Chapter 5 and, if necessary, replace it with globally relevant testing practices.
**Scope:** `docs/05_automation_devops_cicd.md`
**Tasks:**
- Remove the subsection titled “Swedish Architecture testing framework” and any Sweden-specific references within it.
- Decide whether a replacement subsection is needed (e.g., general architecture testing guidance) and draft it if applicable.
- Proof the surrounding content for flow and heading hierarchy after the removal.
**Acceptance Criteria:**
- Chapter 5 no longer contains the Sweden-specific testing framework section.
- Optional replacement content, if added, applies to a global audience and follows house style.
- Markdown headings remain sequential and correctly nested.
**Suggested Labels:** documentation, editorial

## Issue: Relocate Cost Optimisation Guidance to the FinOps Chapter
**Summary:** Move “Cost optimisation and budget control” from the automation chapter into the FinOps-focused chapter, removing localisation references.
**Scope:** `docs/05_automation_devops_cicd.md`, `docs/15_cost_optimization.md`
**Tasks:**
- Extract the cost optimisation section from Chapter 5 and integrate the material into `docs/15_cost_optimization.md`.
- Update the prose to remove Sweden-specific currency and regulatory references, ensuring global applicability.
- Insert cross-references so readers can still discover the material from Chapter 5.
**Acceptance Criteria:**
- Cost optimisation guidance resides in the FinOps chapter with coherent flow and headings.
- Chapter 5 no longer duplicates the same content, instead pointing to the FinOps chapter.
- Revised text avoids Sweden-specific terminology while remaining accurate.
**Suggested Labels:** documentation, finance

## Issue: Globalise the “Security in Architecture as Code” Chapter
**Summary:** Rewrite Chapter 9 to remove Sweden-specific framing and emphasise international security practices suitable for Architecture as Code.
**Scope:** `docs/09_security.md`
**Tasks:**
- Audit the chapter for Swedish regulatory references, agency names, or localisation-dependent examples and replace them with global perspectives.
- Ensure terminology, citations, and narratives remain accurate after the rewrite.
- Perform a style and grammar check to maintain consistency across the chapter.
**Acceptance Criteria:**
- Chapter 9 reads as globally relevant guidance with no unnecessary Sweden-specific focus.
- Updated content remains technically rigorous and aligned with the rest of the book’s security messaging.
- Citations and references support the broadened viewpoint.
**Suggested Labels:** documentation, security

## Issue: Split the Security Architecture Mind Map into Multiple Diagrams
**Summary:** Redesign the “Dimensions of security architecture” mind map into an overview diagram with four branches and four detailed mind maps—one for each branch.
**Scope:** `docs/09_security.md`, `docs/images/mindmap_10_security.mmd`, new diagram assets
**Tasks:**
- Define the four primary branches (e.g., threat management, policy automation, operational resilience, compliance) for the overview mind map.
- Create four additional Mermaid mind maps that deep-dive into each branch’s details.
- Update Chapter 9 to embed the new diagrams with appropriate captions and explanatory text.
**Acceptance Criteria:**
- The original monolithic mind map is replaced by five diagrams: one overview plus four detailed views.
- All diagrams render legibly in the generated PDF and pass build tooling.
- Chapter narrative references the new visuals and explains how readers should interpret them.
**Suggested Labels:** design, documentation, security
