# Appendix D: Templates and Tools {.unnumbered}

Architecture as Code initiatives rely on reusable templates and interactive tools to keep governance, maturity assessments, and compliance evidence consistent. This appendix curates the canonical assets published alongside the book so that practitioners can embed them directly into their delivery workflows.

## Architecture as Code Maturity Model

The [Architecture as Code Maturity Model](architecture_as_code_maturity_model.md) describes six adoption levels spanning foundational automation through to fully codified enterprise governance. Each level contains assessment prompts, operating model guidance, and measurable outcomes that help teams benchmark their progress.

## Architecture as Code Maturity Radar Tool

The [Maturity Radar Tool](maturity_model_radar.html) offers an interactive visualisation of the maturity model. It enables leadership teams to capture current-state and target-state indicators, compare trajectories across business units, and export radar charts for strategy reviews.

## Control Mapping Matrix Template

The [Control Mapping Matrix Template](appendix_d_control_mapping_matrix_template.md) provides a reusable table for expressing "assure once, comply many" evidence flows. Use it to link automated assurance artefacts to ISO 27001, SOC 2, NIST 800-53, GDPR, and internal policies so that governance teams can reuse validated outputs without bespoke reporting.

## Implementation Guidance

1. **Version the artefacts:** Store local copies of the templates in version control so changes trigger peer review and automated validation.
2. **Integrate with pipelines:** Reference the templates from CI/CD jobs to keep evidence manifests, maturity assessments, and control mappings synchronised with production systems.
3. **Tailor for context:** Extend the templates with sector-specific obligations or additional metrics, but retain the canonical structure to preserve comparability across programmes.
