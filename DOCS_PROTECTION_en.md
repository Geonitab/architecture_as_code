# Docs Directory Protection Guidelines

## Purpose
This file provides guidelines to prevent unintended modifications to the `docs/` directory, which contains the source content for the "Architecture as Code" book.

## Rules for Working with the Repository

### ✅ Allowed Operations
- **Reading** from `docs/` directory to generate presentations, analyses, or derived content
- **Adding new files** outside the `docs/` directory (e.g., `presentations/`, `scripts/`, etc.)
- **Modifying** files outside the `docs/` directory
- **Creating tools** that read from `docs/` to generate content elsewhere

### ❌ Restricted Operations  
- **Modifying** existing files in `docs/` directory without explicitly book content approval
- **Deleting** content from markdown files in `docs/`
- **Truncating** or reducing the substantial content in book chapters
- **Changing** the book's core content structure

## For Pull Requests Related to Presentations or External Features

When creating features that need book content (like presentations):

1. **Read Only**: Use `docs/` content as read-only source material
2. **Generate Elsewhere**: Create output files in appropriate directories:
   - `presentations/` for PowerPoint and presentation files
   - `scripts/` for automation tools
   - `exports/` for generated formats
3. **Preserve Source**: Never modify the source markdown files in `docs/`

## Example: Correct Approach for PR #16

The original intent of PR #16 was to create presentations. The correct approach is:

```bash
# ✅ Correct: Read from docs, generate in presentations/
python generate_presentation.py  # Reads docs/, writes to presentations/

# ❌ Incorrect: Modify files in docs/
# (This is what accidentally happened in the original PR #16)
```

## Validation

Before committing changes related to book features:

1. **Check file changes**: `git diff --name-only` should not show `docs/*.md` files
2. **Verify docs integrity**: Ensure book chapters maintain their full content
3. **Test read-only access**: Confirm your scripts only read from `docs/`, never write to it

## Emergency Recovery

If `docs/` files are accidentally modified:

```bash
# Reset docs files to last known good state
git checkout HEAD~1 -- docs/

# Or reset to main branch state
git checkout origin/main -- docs/
```

## Contact

For questions about modifying book content in `docs/`, please:
- Review this protection guide
- Check with repository maintainers
- Ensure changes align with book publication requirements