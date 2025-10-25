# issues/03_generate_whitepapers_concurrency.md
---
title: "generate-whitepapers: add concurrency to prevent overlaps"
labels: [ci, actions]
---

**File:** `.github/workflows/generate-whitepapers.yml`

### Acceptance criteria
```yaml
concurrency:
  group: whitepapers-${{ github.ref }}
  cancel-in-progress: true
```

* Confirm artefacts upload and validation passes.

