---
title: orchestrator release: tolerate optional artefacts gracefully
labels:
  - ci
  - release
---

**File**: `.github/workflows/orchestrate-all.yml`

### Acceptance criteria
- Keep `fail_on_unmatched_files: false` and add pre-flight logging of matched files.
- Ensure the release notes state which artefacts were present.
