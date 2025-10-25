---
title: generate-presentations: add concurrency to prevent overlaps
labels:
  - ci
  - actions
---

**File**: `.github/workflows/generate-presentations.yml`

### Acceptance criteria
- Add:
  ```yaml
  concurrency:
    group: presentations-${{ github.ref }}
    cancel-in-progress: true
  ```
- Confirm validation and artefact publication remain successful.
