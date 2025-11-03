# ADR-0002: Link Diagram Elements to Knowledge Graph Records

## Status
Accepted

## Context
Knowledge graph enrichment relies on canonical identifiers so supporting services can stitch diagrams, ADRs, and telemetry together. Without explicit references, downstream analytics cannot determine which container or component implements a given decision.

## Decision
Embed canonical ADR identifiers within Structurizr elements via the `url` metadata field. The identifier points to the corresponding ADR markdown file stored in version control. Automated checks verify that every referenced ADR file exists and that identifiers remain stable.

## Consequences
- Editors can open the ADR directly from the diagram to review context before approving changes.
- Automated policy tooling can map architecture metadata to decision history without manual tagging.
- Future refactors retain traceability because ADR identifiers stay immutable even when filenames evolve.
