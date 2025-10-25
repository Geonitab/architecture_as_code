# issues/04_generate_presentations_concurrency.md
---
title: "generate-presentations: add concurrency to prevent overlaps"
labels: [ci, actions]
---

**File:** `.github/workflows/generate-presentations.yml`

### Acceptance criteria
```yaml
concurrency:
  group: presentations-${{ github.ref }}
  cancel-in-progress: true
```

* Ensure validation & artefacts OK.

