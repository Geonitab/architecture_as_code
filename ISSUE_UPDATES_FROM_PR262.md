# GitHub Issue Updates Based on PR #262

This document provides the text that should be added to GitHub issues to document their linked pull requests, based on the information from PR #262.

## Issue #220 - Refresh Chapter 7

**Add this comment to the issue:**

```markdown
## Linked Pull Request

This issue has been addressed by:
- [#256 Refresh Chapter 7 for British English consistency](https://github.com/Geonitab/architecture_as_code/pull/256) — merged on 2025-10-12 at 18:38 UTC

Please review the PR to verify all tasks and acceptance criteria have been met.
```

## Issue #222 - Update Chapter 31

**Add this comment to the issue:**

```markdown
## Linked Pull Request

This issue has been addressed by:
- [#252 Translate and clarify Chapter 31 technical architecture](https://github.com/Geonitab/architecture_as_code/pull/252) — merged on 2025-10-12 at 18:39 UTC

Please review the PR to verify all tasks and acceptance criteria have been met.
```

## Issue #227 - Translate Chapter 9

**Add this comment to the issue:**

```markdown
## Linked Pull Requests

This issue has been addressed by:
- [#247 Translate Chapter 9 to British English](https://github.com/Geonitab/architecture_as_code/pull/247) — merged on 2025-10-12 at 18:36 UTC
- [#258 Translate Chapter 9 security content to English](https://github.com/Geonitab/architecture_as_code/pull/258) — merged on 2025-10-12 at 18:56 UTC

Please review these PRs to verify all tasks and acceptance criteria have been met.
```

## Issue #228 - Rewrite Chapter 20

**Add this comment to the issue:**

```markdown
## Linked Pull Request

This issue has been addressed by:
- [#251 Rewrite Chapter 20 AI agent team narrative](https://github.com/Geonitab/architecture_as_code/pull/251) — merged on 2025-10-12 at 18:31 UTC

Please review the PR to verify all tasks and acceptance criteria have been met.
```

## Issue #229 - Expand Chapter 28 Glossary

**Add this comment to the issue:**

```markdown
## Linked Pull Request

This issue has been addressed by:
- [#257 Update glossary language and expand terminology diagram](https://github.com/Geonitab/architecture_as_code/pull/257) — merged on 2025-10-12 at 18:54 UTC

Please review the PR to verify all tasks and acceptance criteria have been met.
```

## Issue #230 - Refresh Chapter 27

**Add this comment to the issue:**

```markdown
## Linked Pull Request

This issue has been addressed by:
- [#250 Refresh Chapter 27 conclusion](https://github.com/Geonitab/architecture_as_code/pull/250) — merged on 2025-10-12 at 18:43 UTC

Please review the PR to verify all tasks and acceptance criteria have been met.
```

## Issue #231 - Update Chapter 14

**Add this comment to the issue:**

```markdown
## Linked Pull Request

This issue has been addressed by:
- [#253 Revise Chapter 14 narrative and relocate code listings](https://github.com/Geonitab/architecture_as_code/pull/253) — merged on 2025-10-12 at 18:29 UTC

Please review the PR to verify all tasks and acceptance criteria have been met.
```

## Issue #232 - Balance Chapter 18

**Add this comment to the issue:**

```markdown
## Linked Pull Request

This issue has been addressed by:
- [#259 Remove generated Chapter 18 PNG outputs](https://github.com/Geonitab/architecture_as_code/pull/259) — merged on 2025-10-12 at 18:50 UTC

Please review the PR to verify all tasks and acceptance criteria have been met.
```

## Issue #237 - Complete Chapter 12 Diagrams

**Add this comment to the issue:**

```markdown
## Linked Pull Request

This issue has been addressed by:
- [#248 Add compliance chapter diagrams](https://github.com/Geonitab/architecture_as_code/pull/248) — merged on 2025-10-12 at 18:35 UTC

Please review the PR to verify all tasks and acceptance criteria have been met.
```

---

## Already Closed Issues

The following issues were already closed when this review was conducted:

- **Issue #234** - "Retire Chapter 6" → Linked PR: #254
- **Issue #235** - "Merge Chapters 25 And 26" → Linked PR: #249  
- **Issue #236** - "Retire Chapter 8" → Closed (no PR link found in templates)
- **Issue #238** - "Retire Chapter 22" → Closed (no PR link found in templates)

These closed issues should also have the PR information added to their history for completeness and traceability.

---

## Manual Update Instructions

Since GitHub API access is limited, these updates need to be added manually:

1. For each open issue listed above, navigate to the issue on GitHub
2. Add a new comment with the corresponding "Linked Pull Request(s)" text
3. Review the linked PR to verify if all tasks are complete
4. If all acceptance criteria are met, close the issue with a comment referencing the PR

Alternatively, you can use the GitHub CLI to automate these updates:

```bash
# Example for issue #220
gh issue comment 220 --body "## Linked Pull Request

This issue has been addressed by:
- [#256 Refresh Chapter 7 for British English consistency](https://github.com/Geonitab/architecture_as_code/pull/256) — merged on 2025-10-12 at 18:38 UTC

Please review the PR to verify all tasks and acceptance criteria have been met."
```
