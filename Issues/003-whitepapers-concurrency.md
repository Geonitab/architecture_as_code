---
title: generate-whitepapers: add concurrency to prevent overlaps
labels:
  - ci
  - actions
---

**File**: `.github/workflows/generate-whitepapers.yml`

### Acceptance criteria
- Add:
  ```yaml
  concurrency:
    group: whitepapers-${{ github.ref }}
    cancel-in-progress: true
  ```
- Confirm artefact creation and validation remain successful.
