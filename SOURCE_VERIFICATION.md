# Source Verification Documentation

This document describes the source verification script for the Architecture as Code book project.

## Overview

The `verify_sources.py` script verifies all cited sources throughout the manuscript to ensure they are accessible and properly documented. It scans markdown chapter files for source citations and validates their availability.

## Features

- ✅ **Comprehensive Source Extraction**: Finds all cited sources in chapter "Sources:" sections
- ✅ **URL Verification**: Makes HTTP HEAD/GET requests to verify external URLs are accessible
- ✅ **ISBN Validation**: Validates ISBN-10 and ISBN-13 format for book citations
- ✅ **Smart Classification**: Categorizes sources as URL, book, standard, academic, or other
- ✅ **Multiple Report Formats**: Generates Markdown and JSON reports
- ✅ **Rate Limiting**: Respects network resources with built-in delays
- ✅ **Caching**: Avoids duplicate checks for the same URL
- ✅ **Rate Limit Handling**: Treats HTTP 429 (rate limiting) as accessible but temporarily unavailable

## Usage

### Basic Usage

```bash
# Run from repository root
python3 scripts/verify_sources.py
```

This will:
1. Scan all numbered chapter files in the `docs/` directory
2. Extract all sources from "Sources:" sections
3. Verify URLs and validate ISBNs
4. Generate two report files:
   - `source-verification-report.md` - Human-readable markdown report
   - `source-verification-report.json` - Machine-readable JSON report

### Advanced Options

```bash
# Custom output location
python3 scripts/verify_sources.py --output reports/my-sources

# Increase timeout for slow links (default: 10 seconds)
python3 scripts/verify_sources.py --timeout 20

# Combine options
python3 scripts/verify_sources.py --timeout 15 --output custom-sources
```

## Report Contents

### Summary Section

The report includes:
- **Total sources cited**: Count of all source citations found
- **Verified and accessible**: Sources with working URLs or valid ISBNs
- **Broken or inaccessible**: Sources with broken URLs or connection errors
- **Needs manual verification**: Sources without URLs/ISBNs (books, standards, reports)

### Broken Sources Section

Each broken source includes:
- **File and line number**: Where the citation appears
- **Citation text**: Full source citation
- **Type**: Source classification (url, book, standard, academic, other)
- **Details**: Error messages and status codes

### Manual Verification Section

Sources that lack URLs or ISBNs are listed separately for manual verification. These typically include:
- Books without ISBNs
- Technical standards (NIST, ISO, etc.)
- Vendor documentation without specific URLs
- Generic references to organizations

### Verified Sources Section

A collapsible list of all successfully verified sources, organized by chapter file.

## Source Types

The script classifies sources into:

1. **URL Sources**: Citations with HTTP/HTTPS links
   - Verified with HTTP HEAD/GET requests
   - Follows redirects
   - Handles rate limiting gracefully

2. **Book Sources**: Citations with ISBN numbers
   - Validates ISBN-10 format (10 digits)
   - Validates ISBN-13 format (13 digits)
   - Accepts hyphens and spaces in ISBN

3. **Standard Sources**: Technical standards and specifications
   - Keywords: NIST, ISO, standard, specification
   - Typically require manual verification

4. **Academic Sources**: Research papers and journals
   - Keywords: arxiv, doi, journal, proceedings
   - Typically require manual verification

5. **Other Sources**: Everything else
   - Generic references
   - Organization documentation
   - Require manual verification

## Understanding Results

### Common Issues

1. **HTTP 404 Not Found**: The URL exists but the specific page doesn't
   - Action: Update link or find alternative source

2. **HTTP 429 Rate Limited**: Server temporarily limiting requests
   - Treated as accessible (not broken)
   - May indicate valid but high-traffic resource

3. **Timeout**: Server didn't respond within timeout period
   - May be temporary; rerun with `--timeout 20` to verify

4. **DNS Errors**: Domain doesn't exist or isn't accessible
   - Check if URL is misspelled or outdated

5. **No verifiable identifiers**: Source lacks URLs and ISBNs
   - Normal for many academic and standard references
   - Requires manual verification

### Exit Codes

- **0**: All sources verified or only manual verification needed
- **1**: One or more broken sources found

## Integration with CI/CD

The script can be integrated into GitHub Actions workflows:

```yaml
- name: Verify Sources
  run: |
    python3 scripts/verify_sources.py --timeout 15
  continue-on-error: true  # Don't fail build on broken sources
```

The script exits with code 1 if broken sources are found, making it suitable for CI validation.

## Examples

### Example Output (Console)

```
======================================================================
Source Verification for Architecture as Code
======================================================================

Scanning /path/to/docs for sources...
Found 28 chapter files

Extracted 95 source citations

Verifying sources...
  Processed 10/95 sources...
  Processed 20/95 sources...
  ...
Verification complete! Processed 95 sources.

======================================================================
Source Verification Summary
======================================================================
Total sources cited: 95
✅ Verified and accessible: 11
❌ Broken or inaccessible: 0
⚠️  Needs manual verification: 84
======================================================================

Generating reports...
✅ Markdown report: source-verification-report.md
✅ JSON report: source-verification-report.json

Done!
```

## Report Files

### Markdown Report (`*.md`)

- Human-readable format
- Suitable for GitHub viewing
- Includes expandable sections for verified sources
- Best for: Quick review, documentation

### JSON Report (`*.json`)

- Structured data format
- Programmatic access
- All source details included
- Best for: Automation, analysis, integration

## Maintenance

The generated reports are excluded from git (via `.gitignore`) as they can be regenerated at any time. Run the script:

- **Before releases**: To ensure all sources are accessible
- **After adding new chapters**: To verify new citations
- **Periodically**: To catch broken links over time
- **In CI/CD**: For automated quality checks

## Limitations

- **Rate Limiting**: Built-in 0.1s delay between requests; some servers may still rate-limit
- **Network Dependent**: Results may vary based on network conditions and server availability
- **Authentication**: Cannot verify links requiring login
- **Paywalled Content**: Cannot access subscriber-only resources
- **Manual Verification Required**: Books, standards, and many academic sources need manual checking

## Best Practices

### For Authors

1. **Include URLs when available**: Makes verification automatic
2. **Add ISBNs for books**: Enables format validation
3. **Use stable, permanent URLs**: Avoid temporary or dynamic links
4. **Prefer official sources**: Use vendor documentation over third-party sites

### For Reviewers

1. **Check broken sources first**: High priority to fix
2. **Manually verify standards**: NIST, ISO references typically need manual confirmation
3. **Validate book citations**: Confirm ISBNs and publication details
4. **Test alternative URLs**: If a URL is broken, search for the updated location

## Troubleshooting

### Script is slow

This is normal! The script makes HTTP requests to verify each URL. Speed improvements:
- Use `--timeout` to reduce wait time for unresponsive servers
- Script already includes caching to avoid duplicate checks
- Rate limiting delays are necessary to be respectful of external servers

### Too many timeouts

Increase timeout: `--timeout 20` or `--timeout 30`

### False positives for rate limiting

Some sites (like HashiCorp Developer Hub) aggressively rate-limit automated requests. The script now treats HTTP 429 as "accessible but rate-limited" rather than broken.

## Support

For issues or questions about the source verification script:
1. Check this documentation
2. Review the generated reports for context
3. Run tests: `python3 -m pytest tests/test_source_verification.py`
4. Open an issue in the repository with details about specific sources

---

**Last Updated**: 2025-10-14
