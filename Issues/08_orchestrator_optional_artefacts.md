# issues/08_orchestrator_optional_artefacts.md
---
title: "orchestrator release: tolerate optional artefacts gracefully"
labels: [ci, release]
---

**File:** `.github/workflows/orchestrate-all.yml`

### Problems
- Release step can fail when artefacts (e.g. `*.docx`) are missing.

### Acceptance criteria
- Keep `fail_on_unmatched_files: false`.
- Add a pre-flight step that logs which release patterns matched.
- Release notes explicitly mention which artefacts were present.

