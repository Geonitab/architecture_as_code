---
title: site (native): add concurrency to prevent overlapping builds
labels:
  - ci
  - actions
---

**File**: `.github/workflows/site.yml`

### Acceptance criteria
- Add:
  ```yaml
  concurrency:
    group: site-${{ github.ref }}
    cancel-in-progress: true
  ```
- Ensure artefacts still upload successfully.
