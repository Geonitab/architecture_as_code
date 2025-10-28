# Architecture as Code Structurizr Workspace Example

This curated workspace accompanies Chapter 06 and demonstrates how the book's C4 abstractions translate into Structurizr DSL. It models the end-to-end book production platform, including:

- A **System Context** view aligning with the collaboration model explained in the manuscript.
- A **Container** view showing the automation platform, diagram tooling, and supporting telemetry services.
- A **Component** view for the diagram automation service, highlighting where Structurizr-centric policy enforcement sits.
- A **Dynamic** view that tracks a diagram change from submission through automated review.
- A **Deployment** view for the production pipeline, enabling operational rehearsals and environment drift checks.

## Quick start

1. Install the Structurizr CLI (minimum version 2024.03.01 as referenced in the workspace configuration).
2. From the repository root, render the workspace using:
   ```bash
   structurizr.sh export \
     -workspace docs/examples/structurizr/aac_reference_workspace.dsl \
     -format plantuml,mermaid,structurizr
   ```
3. Open the generated diagrams (PNG/SVG) or the Structurizr Lite workspace to explore interactive tooling.

## Alignment with the book

- The workspace uses the **British English** nomenclature and tagging conventions described in `docs/06_structurizr.md`.
- Naming and relationship statements match the **Architecture as Code** pipeline introduced across Chapters 03, 05, and 31 so that newcomers can cross-reference narrative text with diagrams.
- Styles emphasise **governance, automation, and telemetry** pathways so platform and architecture teams can reason about evolution without redrawing diagrams from scratch.

## Extending the workspace

- Additional views may be appended in dedicated `views` blocks; align new view identifiers with chapter numbers for traceability.
- Reusable fragments (such as shared people or external systems) should be extracted into `!include` files. Keep those includes alongside the workspace file to simplify code review.
- All contributions should pass the Structurizr CLI validation (`structurizr.sh validate`) before opening a pull request.

