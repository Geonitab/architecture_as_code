---
title: assign-codex.yml: enable triggers and define minimal permissions
labels:
  - ci
  - automation
---

**File**: `.github/workflows/assign-codex.yml`

### Problems
- The `on:` block is commented out, so the workflow never runs.
- Explicit permissions are not declared.

### Acceptance criteria
- Restore the triggers:
  ```yaml
  on:
    issues:
      types: [opened, reopened]
    pull_request:
      types: [opened, reopened, ready_for_review, synchronize]
    workflow_dispatch: {}
  ```
- Declare minimal permissions:
  ```yaml
  permissions:
    contents: write
    pull-requests: write
    issues: write
  ```
- Document any intentional differences versus `assign-codex2.yml`.
