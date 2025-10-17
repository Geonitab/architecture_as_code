```markdown
# Issue: Localise Content to British English – Monitoring and Alerting

**Section:** 05_automation_devops_cicd/#monitoring-and-alerting  
**Summary:** Monitoring guidance inherits American locale assumptions from preceding pipeline configuration, risking inconsistent British English coverage.

## Observed Non-British Usage
- Prometheus configuration references pipelines configured with `en_US` locales.
- Commentary assumes American default metrics naming conventions.
- Lack of explicit British English terminology in explanatory notes.

## Proposed Corrections
- Clarify that monitoring jobs operate within an `en_GB`-configured environment following updates to the Docker pipeline.
- Adjust narrative to use British spelling and cite British operational tooling where helpful.
- Ensure metric labels and documentation align with British English phrasing.

## Tasks
- [ ] Update prose to reference British locale settings applied earlier in the chapter.
- [ ] Review metric descriptions and comments for American spellings.
- [ ] Add guidance on aligning monitoring terminology with British standards.
```
