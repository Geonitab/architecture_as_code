# Architecture as Code Structurizr Workspace Example

This curated workspace accompanies Chapter 06 and demonstrates how the book's C4 abstractions translate into Structurizr DSL. It models the end-to-end book production platform, including:

- A **System Context** view aligning with the collaboration model explained in the manuscript.
- A **Container** view showing the automation platform, diagram tooling, and supporting telemetry services.
- A **Component** view for the diagram automation service, highlighting where Structurizr-centric policy enforcement sits.
- A **Dynamic** view that tracks a diagram change from submission through automated review.
- A **Deployment** view for the production pipeline, enabling operational rehearsals and environment drift checks.

## Quick start

1. Install Docker or Podman; the helper pulls the consolidated `structurizr/structurizr` image (release 2026.09.19, recorded as a free-form property in the workspace configuration). The standalone Structurizr CLI has reached end of life, see [docs.structurizr.com/cli](https://docs.structurizr.com/cli).
2. From the repository root, execute the helper that mirrors the CI workflow:
   ```bash
   ./scripts/render_structurizr_diagrams.sh
   ```
   The script validates the workspace, exports Structurizr JSON and PlantUML artefacts into `build/structurizr/`, and refreshes the manifest hash recorded next to the DSL. It requires either Docker or Podman; if neither runtime is available the script prints manual `java -jar structurizr.war` alternatives so developers can still regenerate diagrams.
3. Render the PlantUML exports with PlantUML, or copy the DSL into a directory as `workspace.dsl` and start `structurizr local` there to explore the interactive tooling.

## Alignment with the book

- The workspace uses the **British English** nomenclature and tagging conventions described in `docs/06_structurizr.md`.
- Naming and relationship statements match the **Architecture as Code** pipeline introduced across Chapters 03, 05, and 31 so that newcomers can cross-reference narrative text with diagrams.
- Styles emphasise **governance, automation, and telemetry** pathways so platform and architecture teams can reason about evolution without redrawing diagrams from scratch.

## Extending the workspace

- Additional views may be appended in dedicated `views` blocks; align new view identifiers with chapter numbers for traceability.
- Reusable fragments (such as shared people or external systems) should be extracted into `!include` files. Keep those includes alongside the workspace file to simplify code review.
- All contributions should pass Structurizr validation (`./scripts/render_structurizr_diagrams.sh`) before opening a pull request.
- If the helper script reports a digest mismatch, rerun it to update `aac_reference_workspace.manifest.json` so the CI job recognises that diagrams and Markdown remain in sync.

