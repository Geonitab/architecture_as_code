# issues/06_assign_codex_triggers_permissions.md
---
title: "assign-codex.yml: enable triggers and define minimal permissions"
labels: [ci, automation]
---

**File:** `.github/workflows/assign-codex.yml`

### Problems
- `on:` is commented out (workflow will not run).
- Missing explicit permissions.

### Acceptance criteria
```yaml
on:
  issues:
    types: [opened, reopened]
  pull_request:
    types: [opened, reopened, ready_for_review, synchronize]
  workflow_dispatch: {}

permissions:
  contents: write
  pull-requests: write
  issues: write
```

* Match or document intentional differences versus `assign-codex2.yml`.

