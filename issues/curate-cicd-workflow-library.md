# Issue: Curate CI/CD workflow examples and lift into reference library

**Summary**
Appendix A contains several GitHub Actions/Jenkins pipeline examples (GDPR checks, testing, delivery). We should adopt these as a versioned “reference library” and wire them into our repositories as selectable templates.

**Why**
Accelerates team adoption, ensures compliance gates (GDPR/data residency), and standardises pipeline quality.

**Scope**
- Extract and parameterise workflows (environment, residency, cost-centre, etc.).
- Provide repository-scoped composite actions or reusable workflows.
- Documentation with when/why to use each template.

**References**
- Site: Appendix A → “CI/CD Pipelines and Architecture as Code Automation” (e.g., 05_CODE_1, 05_CODE_2), plus testing workflows.

**Acceptance Criteria**
- [ ] `/.github/workflows/` contains reusable workflows for compliance and testing.
- [ ] Jenkins examples mirrored (where applicable) or documented alternatives.
- [ ] Decision guide that maps scenario → workflow.

**Tasks**
- [ ] Import `05_CODE_1` (GDPR compliance GH Actions) and adapt variable names.
- [ ] Import `05_CODE_2` (Jenkins variant) or provide GH Actions parity.
- [ ] Add documentation page linking each template with usage notes.

Source: Appendix A.
