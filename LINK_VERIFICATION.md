# Link Verification

This document describes the link verification script for the Kodarkitektur Bokverkstad repository.

## Overview

The `verify_links.py` script iterates through all links in the repository to verify if they contain relevant information. It scans markdown, TypeScript/TSX, and Python files for links and verifies their validity.

## Features

- ✅ **Comprehensive Link Extraction**: Finds all HTTP/HTTPS URLs and internal file references
- ✅ **Multiple File Types**: Scans `.md`, `.tsx`, `.ts`, and `.py` files
- ✅ **Smart Categorization**: Categorizes links as external, internal, localhost, or other
- ✅ **HTTP Verification**: Makes HEAD/GET requests to verify external URLs
- ✅ **Internal Path Verification**: Checks that referenced files exist
- ✅ **Multiple Report Formats**: Generates Markdown, HTML, and JSON reports
- ✅ **Rate Limiting**: Respects network resources with built-in delays
- ✅ **Caching**: Avoids duplicate checks for the same URL

## Usage

### Basic Usage

```bash
# Run from repository root
python3 scripts/verify_links.py
```

This will:
1. Scan all relevant files in the repository
2. Extract and verify all links
3. Generate three report files:
   - `link-verification-report.md` - Human-readable markdown report
   - `link-verification-report.html` - Interactive HTML report with styling
   - `link-verification-report.json` - Machine-readable JSON report

### Advanced Options

```bash
# Custom output location
python3 scripts/verify_links.py --output reports/my-report

# Increase timeout for slow links (default: 10 seconds)
python3 scripts/verify_links.py --timeout 20

# Enable verbose output for debugging
python3 scripts/verify_links.py --verbose

# Combine options
python3 scripts/verify_links.py --timeout 15 --output custom-report --verbose
```

## Report Contents

### Summary Section

The report includes:
- Number of valid external links (HTTP/HTTPS URLs that are accessible)
- Number of broken external links (HTTP errors, timeouts, DNS failures)
- Number of valid internal links (markdown file references that exist)
- Number of broken internal links (file references that don't exist)
- Number of skipped links (localhost URLs, template variables, etc.)

### Broken Links Section

Each broken link includes:
- **URL**: The actual link that failed
- **File**: Source file and line number where the link appears
- **Status**: Error message (HTTP status, timeout, DNS error, etc.)
- **Context**: The surrounding text/markdown for context

### Valid Links Section

Collapsible sections listing all working links for reference and documentation purposes.

## Link Categories

The script categorizes links into:

1. **External Links**: HTTP/HTTPS URLs pointing to external websites
   - Verified with HTTP HEAD/GET requests
   - Follows redirects
   - Respects timeouts

2. **Internal Links**: References to files within the repository
   - Checks file existence relative to source file
   - Also checks relative to repository root
   - Handles anchor references (#section)

3. **Localhost Links**: URLs pointing to localhost or 127.0.0.1
   - Skipped as they are development/example URLs
   - Not applicable for verification

4. **Template Variables**: URLs containing template syntax
   - Examples: `https://${hostname}`, `${TERRAFORM_VERSION}`
   - Skipped as they are placeholders

## Understanding Results

### Common Broken Link Issues

1. **404 Not Found**: The URL exists but the specific page doesn't
   - Action: Update link or remove if no longer relevant

2. **Timeout**: Server didn't respond within timeout period
   - May be temporary; rerun with `--timeout 20` to verify

3. **DNS Errors**: Domain doesn't exist or isn't accessible
   - Check if domain is internal/private or if URL is misspelled

4. **401/403 Errors**: Authentication/permission required
   - May be valid but requires login; verify manually

5. **Internal URLs**: Links to company-specific internal domains
   - Normal for documentation; mark as expected in review

### Interpreting Internal Link Errors

Broken internal links usually indicate:
- Renamed or moved files that need link updates
- Deleted files that need link removal
- Incorrect relative paths

## Integration with CI/CD

The script can be integrated into GitHub Actions workflows:

```yaml
- name: Verify Links
  run: |
    python3 scripts/verify_links.py --timeout 15
  continue-on-error: true  # Don't fail build on broken links
```

The script exits with code 1 if broken links are found, making it suitable for CI validation.

## Examples

### Example Output (Console)

```
======================================================================
Link Verification for Kodarkitektur Bokverkstad
======================================================================

Scanning repository for links...
Found 147 files to scan

Extracting links from files...

Total links found: 290

Verifying links...
  Processed 50/290 links...
  Processed 100/290 links...
  Processed 150/290 links...
  Processed 200/290 links...
  Processed 250/290 links...

Verification complete! Processed 290 links.

Generating reports...
  ✅ Markdown report: link-verification-report.md
  ✅ HTML report: link-verification-report.html
  ✅ JSON report: link-verification-report.json

======================================================================
Verification Summary
======================================================================
✅ Valid external links: 31
❌ Broken external links: 42
✅ Valid internal links: 53
❌ Broken internal links: 140
⏭️  Skipped links: 24
======================================================================
```

## Report Files

### Markdown Report (`*.md`)

- Human-readable format
- Suitable for GitHub viewing
- Includes expandable sections for valid links
- Best for: Quick review, documentation

### HTML Report (`*.html`)

- Styled, interactive interface
- Color-coded sections
- Responsive design
- Collapsible sections
- Best for: Detailed review, presentations

### JSON Report (`*.json`)

- Structured data format
- Programmatic access
- All link details included
- Best for: Automation, analysis, integration

## Maintenance

The generated reports are excluded from git (via `.gitignore`) as they can be regenerated at any time. Run the script periodically to:

- Verify new links in recent changes
- Check if previously broken links are fixed
- Ensure documentation stays up-to-date

## Limitations

- **Rate Limiting**: Built-in 0.1s delay between requests to be respectful of external servers
- **Network Dependent**: Results may vary based on network conditions
- **Authentication**: Cannot verify links requiring login
- **Dynamic Content**: Cannot verify JavaScript-rendered content
- **False Positives**: Some valid links may fail due to bot protection or rate limiting

## Troubleshooting

### Script is slow

This is normal! The script makes HTTP requests to verify each external link. Speed improvements:
- Use `--timeout` to reduce wait time for unresponsive servers
- Script already includes caching to avoid duplicate checks

### Too many timeouts

Increase timeout: `--timeout 20` or `--timeout 30`

### False positives

Some websites block automated requests. Verify manually in a browser and note as expected behavior.

## Support

For issues or questions about the link verification script:
1. Check this documentation
2. Review the generated reports for context
3. Open an issue in the repository with details about the specific links

---

**Last Updated**: 2025-10-03
