# Quick Reference: AaC/IaC Ratio Maintenance

## Current Status
- **Ratio**: 22.19:1 ✅ (Exceeds 20:1 requirement)
- **AaC mentions**: 710
- **IaC mentions**: 32

## How to Check Ratio

### Option 1: Automated Test (Recommended)
```bash
python3 tests/test_aac_iac_ratio.py
```
**Output**: Pass/Fail status with detailed counts

### Option 2: Analysis Script
```bash
python3 scripts/fix_aac_iac_ratio.py
```
**Output**: Detailed analysis, will auto-fix if ratio is below 20:1

## Integration with CI/CD

Add to your test workflow:
```yaml
- name: Validate AaC/IaC Ratio
  run: python3 tests/test_aac_iac_ratio.py
```

## What Gets Counted

### Architecture as Code (AaC)
- Case-insensitive matches of "Architecture as Code"
- Found in: Chapter content, descriptions, explanations

### Infrastructure as Code (IaC)
- Case-insensitive matches of "Infrastructure as Code"
- Case-sensitive matches of "IaC" abbreviation
- Preserved in: Code blocks, tool-specific documentation

## When to Run

✅ **Before committing changes** to chapter files (docs/[0-9]*.md)
✅ **After content updates** that might affect terminology
✅ **In CI/CD pipeline** to prevent regressions
✅ **When reviewing PRs** that modify book content

## Files That Matter

### Content Files
All chapter files in `docs/`:
- `01_introduction.md` through `27_technical_architecture.md`
- Only numbered markdown files are analyzed

### Tool Files
- `scripts/fix_aac_iac_ratio.py` - Analysis and fix tool
- `tests/test_aac_iac_ratio.py` - Validation test

### Documentation
- `IAC_AAC_RATIO_FIX.md` - Implementation details
- `SOLUTION_COMPLETE.md` - Summary and results
- This file - Quick reference

## Troubleshooting

### If Ratio Drops Below 20:1

1. **Run analysis**:
   ```bash
   python3 scripts/fix_aac_iac_ratio.py
   ```

2. **Review proposed changes** - Script shows what it will fix

3. **Apply automated fix** - Script runs automatically

4. **Verify result**:
   ```bash
   python3 tests/test_aac_iac_ratio.py
   ```

### If Manual Review Needed

Check file-by-file breakdown:
```bash
python3 << 'EOF'
import re
from pathlib import Path

for f in sorted(Path('docs').glob('[0-9]*.md')):
    content = f.read_text()
    aac = len(re.findall(r'\bArchitecture as Code\b', content, re.I))
    iac = len(re.findall(r'\bInfrastructure as Code\b|\bIaC\b', content, re.I))
    if iac > 0:
        print(f"{f.name:40} AaC:{aac:4} IaC:{iac:4} Ratio:{aac/iac:5.1f}:1")
EOF
```

## Best Practices

1. **Preserve technical context** - IaC mentions in code blocks and tool docs are appropriate
2. **Use full term** - Prefer "Architecture as Code" over "AaC" abbreviation
3. **Run tests early** - Catch ratio issues before they accumulate
4. **Document exceptions** - If preserving IaC, explain why in comments

## Contact

For questions or issues with the ratio tooling:
- Check documentation: `IAC_AAC_RATIO_FIX.md`
- Review implementation: `scripts/fix_aac_iac_ratio.py`
- Check test logic: `tests/test_aac_iac_ratio.py`

---

**Last Updated**: 2025-10-03
**Current Ratio**: 22.19:1 ✅
**Status**: Compliant
