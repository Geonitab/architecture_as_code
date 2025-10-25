# issues/01_orchestrator_concurrency_timeout.md
---
title: "Orchestrator: add top-level concurrency and finalise timeout"
labels: [ci, actions, release]
---

**File:** `.github/workflows/orchestrate-all.yml`

### Problems
- No top-level `concurrency` → overlapping runs can race on artefacts/releases.
- `finalise` job lacks explicit `timeout-minutes`.

### Acceptance criteria
```yaml
concurrency:
  group: orchestrate-all-${{ github.ref }}
  cancel-in-progress: true
```

* Add top-level concurrency block.
* Set `timeout-minutes: 20` on `finalise`.
* Keep `permissions: contents: write` and verify artefacts still publish.

