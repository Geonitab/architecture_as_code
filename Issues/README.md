# GitHub Issues: Source Verification for Architecture as Code Narrative

This directory contains individual issue drafts for verifying external sources referenced in the Architecture as Code manuscript. Each issue file has been extracted from the consolidated proposal document to facilitate independent tracking and resolution.

## Purpose

These issues capture verification work to ensure the manuscript accurately represents cited sources and maintains rigorous academic standards. Each issue focuses on specific source materials and corresponding manuscript sections.

## Issue List

1. **[issue_01_confirm_aac_definition_and_traditional_architecture_critique.md](./issue_01_confirm_aac_definition_and_traditional_architecture_critique.md)**
   - Source IDs: [1]
   - Labels: `documentation`, `architecture`, `requirements`
   - Focus: AaC definition and traditional architecture critique validation

2. **[issue_02_validate_aac_core_principles_and_ssot_delivery_mechanisms.md](./issue_02_validate_aac_core_principles_and_ssot_delivery_mechanisms.md)**
   - Source IDs: [2], [9]
   - Labels: `documentation`, `architecture`
   - Focus: Core principles and SSOT delivery mechanisms verification

3. **[issue_03_substantiate_aac_self_definition_and_plugin_system.md](./issue_03_substantiate_aac_self_definition_and_plugin_system.md)**
   - Source IDs: [3]
   - Labels: `documentation`, `architecture`
   - Focus: Self-definition and plugin system validation

4. **[issue_04_clarify_aac_vs_iac_abstraction_and_opinionation.md](./issue_04_clarify_aac_vs_iac_abstraction_and_opinionation.md)**
   - Source IDs: [4], [14]
   - Labels: `documentation`, `architecture`
   - Focus: AaC vs IaC abstraction levels and opinionation verification

5. **[issue_05_verify_c4_model_level_definitions_and_anti_decay_guidance.md](./issue_05_verify_c4_model_level_definitions_and_anti_decay_guidance.md)**
   - Source IDs: [5], [6]
   - Labels: `documentation`, `architecture`, `qa`
   - Focus: C4 model definitions and anti-decay guidance validation

6. **[issue_06_confirm_industry_trend_data_driving_aac_adoption.md](./issue_06_confirm_industry_trend_data_driving_aac_adoption.md)**
   - Source IDs: [7]
   - Labels: `documentation`, `requirements`
   - Focus: Industry trend data and statistics verification

7. **[issue_07_review_historical_context_of_model_driven_development.md](./issue_07_review_historical_context_of_model_driven_development.md)**
   - Source IDs: [8]
   - Labels: `documentation`, `architecture`
   - Focus: Historical MDD context validation

8. **[issue_08_validate_iac_market_data_and_economic_rationale.md](./issue_08_validate_iac_market_data_and_economic_rationale.md)**
   - Source IDs: [10], [11], [12], [13]
   - Labels: `documentation`, `requirements`
   - Focus: IaC market data and economic rationale verification

9. **[issue_09_assess_iac_testability_claims_pulumi_vs_terraform.md](./issue_09_assess_iac_testability_claims_pulumi_vs_terraform.md)**
   - Source IDs: [15]
   - Labels: `documentation`, `qa`
   - Focus: IaC testability claims validation

10. **[issue_10_reinforce_iac_state_management_security_guidance.md](./issue_10_reinforce_iac_state_management_security_guidance.md)**
    - Source IDs: [16]
    - Labels: `documentation`, `security`
    - Focus: IaC state management security guidance verification

## Structure

Each issue file follows a consistent format:
- **Title**: Descriptive issue name
- **Source IDs**: Referenced source material identifiers
- **Relevant Manuscript Sections**: Specific sections requiring verification
- **Problem Statement**: Clear description of the verification task
- **Acceptance Criteria**: Measurable outcomes for issue completion
- **Recommended Labels**: Suggested GitHub labels for categorisation

## Usage

To create GitHub issues from these files:
1. Navigate to the [GitHub Issues page](https://github.com/Geonitab/architecture_as_code/issues)
2. Click "New issue"
3. Copy the content from the relevant issue file
4. Apply the recommended labels
5. Submit the issue

## Source Catalogue

The canonical list of verified sources lives in [`source_catalogue.json`](./source_catalogue.json).  
This catalogue maps each Source ID (1–16) to its bibliographic entry, citation URL, and the
manuscript chapters it supports. Automated validation uses this file to ensure:
- issues only reference published sources
- each source is tracked at least once
- cross-references to `docs/33_references.md` remain consistent

Update both the catalogue and the references chapter if new sources are introduced.

## Source Document

These issues were extracted from:
- **Original file**: `ISSUE_PROPOSALS_AAC_SOURCE_VALIDATION.md`
- **Source branch**: `codex/review-sources-for-aac-core-definitions-and-principles`
- **Date split**: 2025-10-16

---

*Prepared to maintain rigorous source alignment across the Architecture as Code manuscript.*
