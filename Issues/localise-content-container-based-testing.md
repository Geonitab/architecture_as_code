```markdown
# Issue: Localise Content to British English – Container-Based Testing with Compliance

**Section:** 05_automation_devops_cicd/#container-based-testing-with-compliance  
**Summary:** The Docker configuration enforces an American locale, undermining British English consistency across the automation chapter.

## Observed Non-British Usage
- Dockerfile snippet sets `en_US.UTF-8` for `LANG`, `LANGUAGE`, and `LC_ALL`.
- Commentary references US-centric locale assumptions for compliance pipelines.
- Reinforces American spelling defaults during build processes.

## Proposed Corrections
- Replace locale generation and environment variables with `en_GB.UTF-8`.
- Update explanatory text to confirm British English locale enforcement.
- Validate that downstream scripts and templates inherit the British locale settings.

## Tasks
- [ ] Adjust the Docker example to generate and export `en_GB.UTF-8`.
- [ ] Review surrounding guidance to ensure British spelling and terminology.
- [ ] Document any compatibility considerations when adopting British locales in CI pipelines.
```
