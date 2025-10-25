---
title: native build workflows: explicit minimal permissions across all
labels:
  - security
  - ci
---

**Files**: `book.yml`, `whitepapers.yml`, `site.yml`, `presentations.yml`

### Acceptance criteria
- Each workflow declares:
  ```yaml
  permissions:
    contents: read
  ```
- Verify that no job in these workflows requires elevated permissions.
