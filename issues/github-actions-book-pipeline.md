# Issue: Implement GitHub Actions CI/CD for book production

**Summary**
Appendix B details a GitHub Actions pipeline that builds the book from Markdown/diagrams with Pandoc and Mermaid, including caching and release artefacts. We should implement or align our pipeline with this reference.

**Why**
Provides reproducible builds, validates diagrams/config, and publishes artefacts with an auditable trail.

**Scope**
- Adopt `build-book.yml` (push/PR/dispatch), add caching, and artefact retention.
- Integrate diagram generation and quality checks.
- Automate releases on `main`.

**References**
- Site: Appendix B → “GitHub Actions: CI/CD Pipeline” and “Build Process and Automation”.

**Acceptance Criteria**
- [ ] Workflow triggers: push to `main`, PRs to `main`, manual dispatch.
- [ ] Steps: environment, dependencies, diagram conversion, Pandoc PDF/EPUB/DOCX.
- [ ] Artefacts uploaded; release on `main` with retention.
- [ ] Quality gates: template/config/image checks.

**Tasks**
- [ ] Port the sample `build-book.yml` and tune timeouts.
- [ ] Add caching for APT, pip, Node.
- [ ] Add validation steps (template, config, images).
- [ ] Configure Release publishing with notes.

Source: Appendix B.
