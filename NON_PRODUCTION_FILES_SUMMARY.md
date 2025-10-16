# Non-Production File Inventory

This inventory lists every tracked file that does **not** directly participate in generating the book manuscript, documentation site, or whitepapers. It is organised so maintainers can distinguish supportive reference material from the assets that power publication pipelines.

## Classification approach

- **Production scope** – Files and directories that drive `generate_book.py`, `generate_whitepapers.py`, `generate_presentation.py`, MkDocs site generation, or their shared templates are considered production assets and excluded here.
- **Supportive scope** – Operational documentation, analysis artefacts, validation utilities, and archived resources are included because they guide, validate, or contextualise the project without being required for generation.

## Root-level documentation

| File | Category | Purpose |
| --- | --- | --- |
| `AGENTS.md` | Governance | Repository-wide operating rules for anyone automating or editing the project, covering setup, validation, and British English expectations.【F:AGENTS.md†L1-L123】 |
| `ANALYSIS_INDEX.md` | Codebase analysis | Entry point into the January 2025 codebase review bundle, signposting the other analysis documents.【F:ANALYSIS_INDEX.md†L1-L37】 |
| `ANALYSIS_SUMMARY.md` | Codebase analysis | Executive summary of the hybrid repository review, including resolved issues and outstanding risks.【F:ANALYSIS_SUMMARY.md†L1-L37】 |
| `AUTOMATION_WORKFLOWS.md` | Automation reference | Describes presentation and whitepaper GitHub Actions plus specialised issue-response bots.【F:AUTOMATION_WORKFLOWS.md†L1-L35】 |
| `BOOK_REQUIREMENTS.md` | Test data | YAML specification of expected chapters and metadata consumed by validation tooling rather than publication scripts.【F:BOOK_REQUIREMENTS.md†L1-L32】 |
| `BRAND_GUIDELINES.md` | Design reference | Kvadrat brand palette, logo usage, and typography guidance for collateral design.【F:BRAND_GUIDELINES.md†L1-L30】 |
| `BRITISH_ENGLISH_CONVERSION.md` | Language audit | Records the switch of diagram source text from American to British English spelling across Mermaid files.【F:BRITISH_ENGLISH_CONVERSION.md†L1-L31】 |
| `CICD_SETUP.md` | Workflow notes | High-level description of the book-focused GitHub Actions pipeline and its triggers.【F:CICD_SETUP.md†L1-L29】 |
| `CODEBASE_ANALYSIS.md` | Codebase analysis | Full report on repository quality findings and remediation suggestions from January 2025.【F:CODEBASE_ANALYSIS.md†L1-L32】 |
| `CRITICAL_FIXES.md` | Remediation guide | Step-by-step fixes for the urgent issues identified by the analysis suite (e.g., ESLint failures).【F:CRITICAL_FIXES.md†L1-L28】 |
| `DESIGN_SYSTEM.md` | Design reference | Comprehensive graphic profile aligning collateral with Kvadrat’s colours, typography, and iconography.【F:DESIGN_SYSTEM.md†L1-L28】 |
| `DIAGRAM_INVENTORY.md` | Diagram tracking | Complete catalogue of Mermaid diagrams, their themes, and counts for auditing purposes.【F:DIAGRAM_INVENTORY.md†L1-L24】 |
| `DIAGRAM_LIMIT_COMPLETION.md` | Diagram tracking | Summary of enforcing the 15-element legibility limit across diagrams, including restructuring details.【F:DIAGRAM_LIMIT_COMPLETION.md†L1-L28】 |
| `DIAGRAM_THEME_STANDARD.md` | Design reference | Defines the Kvadrat diagram theme applied during builds and documents palette expectations.【F:DIAGRAM_THEME_STANDARD.md†L1-L30】 |
| `DIAGRAM_TRANSLATION_FIX.md` | Language audit | Documents the translation of lingering Swedish diagram text to English for the live site.【F:DIAGRAM_TRANSLATION_FIX.md†L1-L27】 |
| `DOCS_PROTECTION.md` | Governance | Rules that prevent accidental modification of book chapters and prescribe safe generation patterns.【F:DOCS_PROTECTION.md†L1-L33】 |
| `ENGLISH_CLEANUP_SUMMARY.md` | Language audit | Summarises the Svengelska cleanup campaign, including tooling and multi-pass approach.【F:ENGLISH_CLEANUP_SUMMARY.md†L1-L28】 |
| `ENGLISH_MIGRATION_SUMMARY.md` | Language audit | Provides corrected history of the English migration effort and associated tooling changes.【F:ENGLISH_MIGRATION_SUMMARY.md†L1-L32】 |
| `ENGLISH_STATUS.md` | Language audit | Snapshot of current language quality metrics and links to cleanup documentation.【F:ENGLISH_STATUS.md†L1-L29】 |
| `IAC_AAC_RATIO_FIX.md` | Content quality | Details the strategy that rebalanced IaC and AaC mentions to satisfy editorial ratios.【F:IAC_AAC_RATIO_FIX.md†L1-L30】 |
| `ISSUE_UPDATES_FROM_PR262.md` | Issue hygiene | Ready-to-use GitHub issue comments linking specific issues to PR #262.【F:ISSUE_UPDATES_FROM_PR262.md†L1-L26】 |
| `LINK_VERIFICATION.md` | Validation tooling | Instructions for running the repository-wide link verification script and interpreting outputs.【F:LINK_VERIFICATION.md†L1-L31】 |
| `NARRATIVE_COHESION_IMPROVEMENTS.md` | Content quality | Documents additions that improved part introductions and chapter transitions.【F:NARRATIVE_COHESION_IMPROVEMENTS.md†L1-L27】 |
| `PR262_GENOMGANG_SVENSKA.md` | Issue hygiene | Swedish-language summary of PR #262 and the issues it affects.【F:PR262_GENOMGANG_SVENSKA.md†L1-L25】 |
| `PR_262_REVIEW_SUMMARY.md` | Issue hygiene | English-language review of PR #262 and mapping to issue templates.【F:PR_262_REVIEW_SUMMARY.md†L1-L27】 |
| `QUICK_REFERENCE_AAC_IAC.md` | Validation tooling | Reference sheet for maintaining the AaC/IaC ratio via scripts and tests.【F:QUICK_REFERENCE_AAC_IAC.md†L1-L25】 |
| `README.md` | Project orientation | Main project guide outlining deliverables, build commands, and repository layout.【F:README.md†L1-L81】 |
| `README_ANALYSIS.md` | Codebase analysis | Quick-start companion to the broader analysis bundle.【F:README_ANALYSIS.md†L1-L33】 |
| `RECOMMENDATIONS.md` | Codebase analysis | Ongoing quality recommendations following the January 2025 review.【F:RECOMMENDATIONS.md†L1-L23】 |
| `REMAINING_WORK.md` | Language audit | Identifies residual translation issues after automated Svengelska cleanup.【F:REMAINING_WORK.md†L1-L25】 |
| `SINGLE_COVER_VERIFICATION.md` | Production assurance | Confirms the book now ships with a single front cover and documents related clean-up steps.【F:SINGLE_COVER_VERIFICATION.md†L1-L26】 |
| `SOURCE_VERIFICATION.md` | Validation tooling | Explains the source verification script that audits cited references.【F:SOURCE_VERIFICATION.md†L1-L31】 |
| `SWEDISH_REMOVAL_SUMMARY.md` | Language audit | Historical record of the six-pass Swedish content removal effort.【F:SWEDISH_REMOVAL_SUMMARY.md†L1-L29】 |
| `SYNTAX_HIGHLIGHTING.md` | Production support | Documents syntax highlighting choices for different deliverables without being required for generation itself.【F:SYNTAX_HIGHLIGHTING.md†L1-L27】 |
| `SYNTAX_HIGHLIGHTING_VALIDATION.md` | Production support | Validation log confirming the highlighting implementation across templates and pandoc config.【F:SYNTAX_HIGHLIGHTING_VALIDATION.md†L1-L25】 |
| `SOLUTION_COMPLETE.md` | Content quality | Final metrics and assurance for the AaC/IaC ratio remediation.【F:SOLUTION_COMPLETE.md†L1-L26】 |
| `SOLUTION_SUMMARY.md` | Governance | Clarifies the correct, read-only approach for presentation generation to protect book content.【F:SOLUTION_SUMMARY.md†L1-L27】 |
| `TASK_COMPLETION_SUMMARY.md` | Issue hygiene | Documents the fulfilment of the PR #262 review task, including artefacts produced.【F:TASK_COMPLETION_SUMMARY.md†L1-L27】 |
| `TEST_WORKFLOW.md` | Workflow notes | Marker file for exercising the enhanced `unified-build-release.yml` workflow logging.【F:TEST_WORKFLOW.md†L1-L23】 |
| `TRANSLATION_COMPLETION_SUMMARY.md` | Language audit | Historical wrap-up of the English translation project.【F:TRANSLATION_COMPLETION_SUMMARY.md†L1-L23】 |
| `TRANSLATION_PROJECT.md` | Language audit | Detailed record of the translation effort and artefacts generated during migration.【F:TRANSLATION_PROJECT.md†L1-L27】 |
| `VISUAL_ELEMENTS_GUIDE.md` | Design reference | Guidance on colours, accessible diagram theming, and brand alignment.【F:VISUAL_ELEMENTS_GUIDE.md†L1-L30】 |
| `WORKFLOWS.md` | Automation reference | Documentation for the unified GitHub Actions release pipeline and its triggers.【F:WORKFLOWS.md†L1-L30】 |

## Supporting directories and assets

| Path | Contents | Purpose |
| --- | --- | --- |
| `docs/archive/` | Archived drafts excluded from automated builds, retaining historical chapters for reference.【F:docs/archive/README.md†L1-L16】 | Preserve superseded manuscript material without impacting generation. |
| `exports/book-cover/` | Multi-format cover assets, editable sources, and brand collateral for design work.【F:exports/book-cover/README.md†L1-L36】 | Provide reusable design artefacts outside the automated build pipeline. |
| `references/` | Reference excerpts such as the CALM overview used for research context.【F:references/calm_what_is_excerpt.txt†L1-L20】 | Supplementary reading not consumed by generators. |
| `reports/` | Generated analysis reports on chapter metrics and action plans.【F:reports/README.md†L1-L25】 | Analytical insights supporting editorial decisions. |
| `releases/README.md` | Explanation of the release directory structure and deliverables produced by builds.【F:releases/README.md†L1-L32】 | Documentation of output packaging rather than an input to generation. |
| `scripts/` | Utilities for translation, analysis, and validation (e.g., repository translation helper).【F:scripts/translate_repo.py†L1-L15】 | Ancillary tooling that operates on content without being mandatory for builds. |
| `tests/` | Validation suite ensuring content quality, completeness, and ratio compliance.【F:tests/README.md†L1-L24】 | Automated checks that gate quality but do not generate deliverables. |
| `reports/chapter_length_analysis.md` & `reports/chapter_length_action_plan.md` | Word-count statistics and remediation plans derived from analysis tooling.【F:reports/README.md†L8-L24】 | Editorial planning artifacts beyond core generation. |
| `release_information_page.png` | Static PNG asset stored alongside documentation (size recorded in repository history).【417c70†L1-L2】 | Visual collateral separate from automated outputs. |

## Observations

- The non-production material is extensive yet thematically clustered into analysis, language quality, workflow governance, and design collateral, which simplifies audits of supporting artefacts.
- Several validation documents duplicate context across languages (for example, Swedish and English summaries of PR #262) to serve different stakeholder groups without touching generation code.【F:PR262_GENOMGANG_SVENSKA.md†L1-L25】【F:PR_262_REVIEW_SUMMARY.md†L1-L27】
- Archival and collateral directories (`docs/archive/`, `exports/book-cover/`, `references/`) demonstrate a deliberate separation between source manuscripts and historical or design resources, reducing the risk of unintended build side effects.【F:docs/archive/README.md†L1-L16】【F:exports/book-cover/README.md†L1-L32】
