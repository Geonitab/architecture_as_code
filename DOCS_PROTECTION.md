# Docs Directory Protection

This directory contains protection mechanisms to ensure the integrity of the book content in the `docs/` directory, particularly preventing unwanted large-scale deletions or modifications to critical chapter files.

## Overview

The protection system was implemented to address concerns about PR #15, which contained massive deletions from core book chapters:
- `docs/01_inledning.md`: 236 lines deleted, only 4 added
- `docs/02_kapitel1.md`: 1267 lines deleted, only 4 added  
- `docs/03_kapitel2.md`: 953 lines deleted, only 4 added

These changes represented significant content loss that could impact the book's quality and completeness.

## Protection Mechanisms

### 1. GitHub Actions Workflow (`.github/workflows/docs-protection.yml`)

Automatically runs on pull requests that modify files in the `docs/` directory. The workflow:

- **Validates content changes**: Ensures no excessive deletions (max 10% deletion ratio)
- **Checks file integrity**: Verifies chapter files maintain minimum content length (100 lines)
- **Prevents critical file deletion**: Protects numbered chapter files from being deleted
- **Provides feedback**: Comments on PRs with validation results
- **Blocks merging**: Fails the check if validation doesn't pass

### 2. Manual Validation Script (`scripts/validate-docs-protection.sh`)

A standalone script that can be run locally to validate changes before pushing:

```bash
# Validate against main branch
./scripts/validate-docs-protection.sh

# Validate against a specific branch
./scripts/validate-docs-protection.sh develop
```

## Protection Rules

### Deletion Ratio Limit
- Maximum 10% of content can be deleted from any file
- Calculated as: `deleted_lines / (total_changes + deleted_lines)`
- Prevents massive content removal while allowing reasonable edits

### Minimum Content Length
- Chapter files (matching pattern `docs/[0-9]+_*.md`) must have at least 100 lines
- Ensures chapters maintain substantial content
- Prevents chapters from being reduced to stubs

### Critical File Protection
- Numbered chapter files cannot be deleted
- Includes files like `01_inledning.md`, `02_kapitel1.md`, etc.
- Maintains book structure integrity

## Usage

### For Developers

1. **Before making changes**: Run the validation script to check your current changes
2. **During development**: Keep the protection rules in mind when editing chapter files
3. **Before pushing**: Ensure your changes will pass the automated checks

### For Reviewers

1. **Automatic validation**: GitHub Actions will automatically check docs changes
2. **Review comments**: Look for protection check comments on PRs
3. **Manual verification**: Can run the script locally to double-check

### For Administrators

1. **Monitoring**: Review failed protection checks in GitHub Actions
2. **Rule adjustment**: Modify thresholds in workflow file if needed
3. **Emergency override**: Can temporarily disable checks if necessary

## Configuration

Both the GitHub Actions workflow and validation script use these configurable parameters:

- `MAX_DELETIONS_RATIO`: Maximum allowed deletion ratio (default: 0.1 = 10%)
- `MIN_CONTENT_LENGTH`: Minimum lines for chapter files (default: 100)

To adjust these values:
1. Edit `.github/workflows/docs-protection.yml` for automated checks
2. Edit `scripts/validate-docs-protection.sh` for manual validation

## Troubleshooting

### Validation Failed: Excessive Deletions
- **Cause**: Your changes delete more than 10% of a file's content
- **Solution**: Review if the deletions are necessary, or split into smaller changes

### Validation Failed: Content Too Short
- **Cause**: A chapter file has fewer than 100 lines after your changes
- **Solution**: Ensure chapter files maintain substantial content

### Validation Failed: Critical File Deleted
- **Cause**: You attempted to delete a numbered chapter file
- **Solution**: Restore the file or justify the deletion in the PR description

## Files

- `.github/workflows/docs-protection.yml` - GitHub Actions workflow for automated protection
- `scripts/validate-docs-protection.sh` - Manual validation script
- `DOCS_PROTECTION.md` - This documentation file

## Related

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Book Build Workflow](../.github/workflows/build-book.yml)
- [Repository Contributing Guidelines](../README.md)