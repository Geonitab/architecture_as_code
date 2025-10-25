---
title: Orchestrator: add top-level concurrency and finalise timeout
labels:
  - ci
  - actions
---

**File**: `.github/workflows/orchestrate-all.yml`

### Problems
- No top-level `concurrency`, so overlapping runs can race on artefacts and releases.
- The `finalise` job lacks an explicit `timeout-minutes` value.

### Acceptance criteria
- Add:
  ```yaml
  concurrency:
    group: orchestrate-all-${{ github.ref }}
    cancel-in-progress: true
  ```
- Set `timeout-minutes: 20` on `finalise`.
- Keep `permissions: contents: write` and confirm artefacts still publish.
