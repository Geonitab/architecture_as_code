# issues/05_site_native_concurrency.md
---
title: "site (native): add concurrency to prevent overlapping builds"
labels: [ci, actions]
---

**File:** `.github/workflows/site.yml`

### Acceptance criteria
```yaml
concurrency:
  group: site-${{ github.ref }}
  cancel-in-progress: true
```

* Ensure artefacts still upload.

