# Issues

This directory contains curated GitHub issue drafts for the Architecture as Code manuscript. Each issue is backed by approved, peer-reviewed sources defined in the source catalogue.

## Source Catalogue

[`source_catalogue.json`](source_catalogue.json) — Defines Source IDs 1–16 with full bibliographic metadata, URLs, and chapter mappings. All issue templates must reference only Source IDs defined in this catalogue.

## Issue Templates

| File | Title | Source IDs |
|------|-------|-----------|
| [issue_001_architecture_foundations.md](issue_001_architecture_foundations.md) | Strengthen Architecture as Code Foundations with Current Industry Sources | 1, 3, 4, 5, 6, 9 |
| [issue_002_security_governance_compliance.md](issue_002_security_governance_compliance.md) | Align Security, Governance and Compliance Chapters with Authoritative Standards | 2, 7, 8, 10, 11, 12, 13, 14, 15, 16 |

## Structure

Each issue template follows this structure:

- **Problem Statement** – What content gap or quality issue is being addressed
- **Relevant Manuscript Sections** – Which chapter files are affected
- **Source IDs** – Catalogue entries that support the change (referenced as `[n]`)
- **Acceptance Criteria** – Checklist of testable conditions for completion
- **Recommended Labels** – GitHub label suggestions for routing to the appropriate bot

## Usage

1. Open the relevant issue template
2. Apply the recommended labels when creating the GitHub issue
3. The appropriate bot workflow will respond automatically (see `CLAUDE.md` for bot label mappings)
