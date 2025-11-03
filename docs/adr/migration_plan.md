# Legacy ADR Migration Plan {#adr-migration-plan}

Migrating historical Architecture Decision Records (ADRs) into the structured format introduced by issue #1305 requires a combination of metadata enrichment, automated verification, and collaborative review. This plan provides a reusable blueprint for transforming existing decision logs—whether stored in wikis, shared drives, or dated Markdown files—into the codified workflow that now powers the Architecture as Code documentation suite.

## Objectives

1. **Preserve historical intent** so design rationale remains discoverable alongside the automated Architecture as Code assets.
2. **Enrich legacy records with required metadata** (`adr_id`, review cadence, linked chapters, diagrams, and backlog references).
3. **Ensure continuous integration coverage** by validating that every migrated ADR passes `python3 scripts/validate_adrs.py`.
4. **Synchronise navigation and change logs** via `python3 scripts/generate_adr_catalogue.py` to keep MkDocs and book builds aligned.

## Migration Waves

| Wave | Scope | Activities | Exit Criteria |
| ---- | ----- | ---------- | -------------- |
| Wave 1 | Top 10 most-referenced ADRs | Inventory legacy files, assign canonical identifiers, capture missing metadata | ADR catalogue displays migrated entries with next review dates |
| Wave 2 | Compliance-critical decisions | Cross-link to policy diagrams, capture backlog remediation items, schedule reviews with governance teams | CI validation passes; automation dashboards ingest metadata |
| Wave 3 | Remaining historical records | Standardise tone, link to relevant chapters, and archive superseded entries with successor references | All references in `docs/` resolve to committed ADR files |

## Detailed Steps

1. **Catalogue existing material**
   - Export legacy ADRs from previous repositories, wiki spaces, or document stores.
   - Map each decision to the new identifier schema (`ADR-XXXX`) and track the source location for audit purposes.

2. **Enrich metadata**
   - Populate YAML front matter with review cadences, diagram links, and backlog identifiers.
   - Use British English for all narrative sections to stay consistent with the manuscript style.

3. **Peer review updates**
   - Raise a pull request per migration wave.
   - Include evidence that `python3 scripts/validate_adrs.py` and `python3 scripts/generate_adr_catalogue.py` have been executed.
   - Request reviewers from architecture, governance, and operations to confirm accuracy.

4. **Automate catalogue regeneration**
   - Run `python3 scripts/generate_adr_catalogue.py` after each merge to refresh `docs/adr/adr_catalogue.md`.
   - Confirm MkDocs navigation highlights the new entries and that change notes appear in the automatically generated table.

5. **Archive superseded artefacts**
   - Move deprecated or redundant ADRs into `docs/archive/` with cross-links to their successors.
   - Record the migration context within the `change_notes` list so future readers understand the rationale behind supersessions.

## Tooling Checklist

- `python3 scripts/validate_adrs.py` — confirms metadata completeness and cross-references manuscript mentions.
- `python3 scripts/generate_adr_catalogue.py` — regenerates the catalogue consumed by the documentation site and book build.
- `pytest tests/test_adr_metadata.py` — keeps the CI suite aligned with manual checks.

## Communication Plan

- Announce the migration schedule during the weekly Architecture as Code stand-up.
- Track progress against backlog items referenced within each ADR (`AAC-1182`, `AAC-1305`, `AAC-1224`, `DATA-947`).
- Share the regenerated catalogue with governance stakeholders to evidence continuous improvement.

By following this plan, teams can transition legacy architecture decisions into the automated, reviewable workflow without losing historical context or creating documentation drift.
