# issues/07_native_workflows_minimal_permissions.md
---
title: "native build workflows: explicit minimal permissions across all"
labels: [ci, security]
---

**Files:**
- `.github/workflows/book.yml`
- `.github/workflows/whitepapers.yml`
- `.github/workflows/site.yml`
- `.github/workflows/presentations.yml`

### Acceptance criteria
Each declares:
```yaml
permissions:
  contents: read
```

* Verify none need elevated perms.

