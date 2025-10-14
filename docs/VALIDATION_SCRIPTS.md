# Content Validation Scripts

This document describes the automated validation scripts used to maintain content quality and consistency throughout the Architecture as Code book.

## Overview

The repository includes several validation scripts that run automatically via GitHub Actions to ensure content meets the book's style guide and quality standards.

## Validation Scripts

### 1. Heading Capitalization Validator

**Script**: `scripts/validate_heading_capitalization.py`  
**Workflow**: `.github/workflows/validate-heading-capitalization.yml`

**Purpose**: Ensures all markdown headings (lines starting with `#`, `##`, `###`, etc.) begin with uppercase letters.

**Usage**:
```bash
python3 scripts/validate_heading_capitalization.py
```

**Exit Codes**:
- `0`: All headings are properly capitalized
- `1`: One or more headings start with lowercase letters

**Example Output**:
```
Checking 54 markdown files for heading capitalization...
✅ All headings are properly capitalized!
```

### 2. Figure Caption Capitalization Validator

**Script**: `scripts/validate_figure_captions.py`  
**Workflow**: `.github/workflows/validate-figure-captions.yml`

**Purpose**: Ensures all figure captions (italic text after image references) begin with uppercase "Figure" followed by proper numbering.

**Usage**:
```bash
python3 scripts/validate_figure_captions.py
```

**Exit Codes**:
- `0`: All figure captions are properly capitalized
- `1`: One or more figure captions start with lowercase 'figure'

**Example Output**:
```
Checking 47 markdown files for figure caption capitalization...
✅ All figure captions are properly capitalized!
```

**What It Checks**:
- Figure captions must start with `*Figure` (uppercase F)
- Follows pattern: `*Figure X.Y – Caption text*`
- Example: `*Figure 14.1 – Architecture as Code relies on...*`

## CI/CD Integration

Both validation scripts run automatically on:
- **Pull Requests** to `main` branch
- **Pushes** to `main` branch
- **Manual Trigger** via workflow_dispatch

### Triggers

The workflows are triggered when:
```yaml
paths:
  - 'docs/**/*.md'
```

This ensures validations run only when documentation files change, optimizing CI/CD resources.

## Style Guide Compliance

### Heading Style
✅ **Correct**:
```markdown
# Architecture as Code in Practice
## Implementation roadmap and strategies
### Key considerations
```

❌ **Incorrect**:
```markdown
# architecture as Code in Practice
## implementation roadmap and strategies
### key considerations
```

### Figure Caption Style
✅ **Correct**:
```markdown
![Figure 14.1 – Capability landscape](images/diagram_08_chapter7.png)
*Figure 14.1 – Architecture as Code relies on coordinated governance...*
```

❌ **Incorrect**:
```markdown
![figure 14.1 – Capability landscape](images/diagram_08_chapter7.png)
*figure 14.1 – Architecture as Code relies on coordinated governance...*
```

## Development Workflow

When adding new content:

1. **Write Content**: Add markdown files to `docs/` directory
2. **Add Figures**: Include images with proper captions
3. **Local Validation**: Run validation scripts before committing
   ```bash
   python3 scripts/validate_heading_capitalization.py
   python3 scripts/validate_figure_captions.py
   ```
4. **Commit & Push**: CI/CD will automatically validate
5. **Fix Issues**: If validation fails, update content and push again

## Adding New Validations

To add a new validation script:

1. Create script in `scripts/` directory
2. Follow the same pattern as existing validators:
   - Return exit code 0 for success, 1 for failure
   - Provide clear, actionable error messages
   - Skip archive and generated content
3. Create corresponding workflow in `.github/workflows/`
4. Test locally before committing
5. Update this documentation

## Troubleshooting

### False Positives

If a validator flags content that is intentionally lowercase:

1. **Code blocks**: Already excluded from validation
2. **Special cases**: Add to validator's exception list
3. **Archive content**: Archived files are excluded

### Running Locally

All scripts can be run locally without any dependencies:
```bash
# From repository root
python3 scripts/validate_heading_capitalization.py
python3 scripts/validate_figure_captions.py
```

No additional Python packages are required - all scripts use only standard library modules.

## Maintenance

### Regular Updates

- Review validation rules quarterly
- Update to match evolving style guide
- Add new validators as needed
- Refactor for performance if needed

### Monitoring

- Check GitHub Actions for workflow success rates
- Review flagged issues in PRs
- Collect feedback from contributors

## References

- **Style Guide**: See book style guide for complete formatting rules
- **CI/CD Documentation**: `docs/31_technical_architecture.md` - Appendix B
- **Workflows**: `.github/workflows/` directory for all automation

---

*This documentation is maintained alongside the validation scripts. Update when adding or modifying validators.*
