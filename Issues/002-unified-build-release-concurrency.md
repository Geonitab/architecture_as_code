---
title: unified-build-release: top-level concurrency and minimal permissions
labels:
  - ci
  - actions
  - performance
---

**File**: `.github/workflows/unified-build-release.yml`

### Problems
- There is no top-level `concurrency` block.
- Workflow permissions are not declared.

### Acceptance criteria
- Add:
  ```yaml
  concurrency:
    group: unified-${{ github.ref }}
    cancel-in-progress: true
  permissions:
    contents: write
  ```
- Verify the release process still succeeds.
