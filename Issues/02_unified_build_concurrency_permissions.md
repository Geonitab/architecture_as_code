# issues/02_unified_build_concurrency_permissions.md
---
title: "unified-build-release: top-level concurrency, minimal permissions"
labels: [ci, actions, performance]
---

**File:** `.github/workflows/unified-build-release.yml`

### Problems
- No top-level `concurrency`.
- Missing explicit `permissions`.

### Acceptance criteria
```yaml
concurrency:
  group: unified-${{ github.ref }}
  cancel-in-progress: true
permissions:
  contents: write
```

* Verify release still works.

