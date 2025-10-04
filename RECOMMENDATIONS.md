# Code Quality Recommendations

This document provides ongoing recommendations for maintaining and improving code quality in the kodarkitektur-bokverkstad repository.

---

## Completed Improvements ✅

The following critical issues have been addressed:

1. **ESLint Errors Fixed** - All 3 critical errors resolved
2. **Bundle Size Optimized** - 25% reduction through code splitting
3. **Documentation Updated** - Security issues and requirements documented
4. **Repository Cleanup** - Removed 30MB build artifact from git

---

## Remaining Recommendations

### 1. Documentation Language Standardization (HIGH PRIORITY)

**Issue**: Mixed Swedish and English documentation creates confusion for international contributors.

**Current State**:
- README.md: ✅ English
- bot.md: ❌ Mixed Swedish/English ("Svengelska")
- CICD_SETUP.md: ❌ Swedish
- generate_book.py: ❌ Swedish comments
- Book content: ✅ English (per README claim)

**Recommendation**: Choose one approach:

#### Option A: Full English (Recommended for Open Source)

**Benefits**:
- Accessible to international contributors
- Consistent with open-source best practices
- Easier maintenance

**Steps**:
1. Translate bot.md to English
2. Translate CICD_SETUP.md to English  
3. Update Python script comments to English
4. Update print/log messages to English
5. Review all markdown files for consistency

**Estimated Effort**: 3-4 hours

#### Option B: Documented Hybrid

**Benefits**:
- Respects Swedish origin
- Reduces translation effort
- Keeps internal tooling in native language

**Steps**:
1. Add explicit language policy to README
2. Clarify which parts are Swedish vs English
3. Provide glossary of Swedish technical terms
4. Document rationale

**Estimated Effort**: 1 hour

**Recommendation**: Choose Option A for better long-term maintainability.

---

### 2. Frontend Testing Infrastructure (MEDIUM PRIORITY)

**Issue**: React application has no automated tests.

**Current State**:
- ✅ Python tests exist in `tests/`
- ❌ No React component tests
- ❌ No integration tests
- ❌ No E2E tests

**Recommendation**: Implement Vitest testing

**Setup**:
```bash
npm install -D vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom
```

**Add to package.json**:
```json
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage"
  }
}
```

**Create `vitest.config.ts`**:
```typescript
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react-swc';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts',
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
```

**Example Test** (`src/pages/__tests__/Index.test.tsx`):
```typescript
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Index from '../Index';

describe('Index Page', () => {
  it('renders dashboard title', () => {
    render(
      <BrowserRouter>
        <Index />
      </BrowserRouter>
    );
    
    expect(screen.getByText(/Architecture as Code/i)).toBeInTheDocument();
  });
});
```

**Estimated Effort**: 2-3 hours setup + ongoing test writing

---

### 3. Python Code Modernization (MEDIUM PRIORITY)

**Current Issues**:
- No type hints
- Using `os.path` instead of modern `pathlib`
- Print statements instead of proper logging
- Disabled main function creates confusion

**Recommendation**: Modernize Python code

**Example Refactor** for `generate_book.py`:

```python
"""Book generation and validation utilities.

This module handles EPUB validation for the Architecture as Code book.
Content generation has been migrated to manual English editing.
"""
import logging
from pathlib import Path
from typing import Tuple
import subprocess

logger = logging.getLogger(__name__)


def validate_epub_file(epub_path: Path) -> Tuple[bool, str]:
    """
    Validate EPUB file using EPUBCheck.
    
    Args:
        epub_path: Path to the EPUB file to validate
        
    Returns:
        Tuple of (success status, validation output log)
    """
    try:
        # Check if EPUBCheck is available
        result = subprocess.run(
            ['epubcheck', '--version'],
            capture_output=True,
            text=True,
            timeout=10,
            check=False
        )
        
        if result.returncode != 0:
            return False, "EPUBCheck is not available"
            
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False, "EPUBCheck is not installed or not available"
    
    try:
        logger.info(f"Validating EPUB file: {epub_path}")
        result = subprocess.run(
            ['epubcheck', str(epub_path)],
            capture_output=True,
            text=True,
            timeout=60,
            check=False
        )
        
        log_output = result.stdout + result.stderr
        
        if result.returncode == 0:
            logger.info("EPUB validation passed")
            return True, log_output
        else:
            logger.warning("EPUB validation revealed issues")
            fatal_count = log_output.count('FATAL')
            error_count = log_output.count('ERROR') - fatal_count
            warning_count = log_output.count('WARNING')
            
            logger.warning(f"Fatal errors: {fatal_count}")
            logger.warning(f"Errors: {error_count}")
            logger.warning(f"Warnings: {warning_count}")
            
            return False, log_output
            
    except subprocess.TimeoutExpired:
        return False, "EPUBCheck timeout - file may be too large or corrupted"
    except Exception as e:
        return False, f"Error during EPUB validation: {str(e)}"


def main() -> int:
    """Main entry point for EPUB validation."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    epub_path = Path("docs/arkitektur_som_kod.epub")
    
    if not epub_path.exists():
        logger.info("No EPUB file found to validate")
        return 0
    
    logger.info("Checking existing EPUB file...")
    success, log_output = validate_epub_file(epub_path)
    
    # Save validation log
    log_path = Path("docs/epub-validation.log")
    try:
        log_path.write_text(
            f"EPUB validation log for: {epub_path}\n"
            f"Status: {'APPROVED' if success else 'ERRORS FOUND'}\n"
            f"{'=' * 50}\n"
            f"{log_output}",
            encoding='utf-8'
        )
        logger.info(f"Validation log saved: {log_path}")
    except Exception as e:
        logger.error(f"Could not save validation log: {e}")
    
    return 0 if success else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
```

**Benefits**:
- Type safety and IDE support
- Better error handling
- Structured logging
- Modern Python patterns
- Clearer purpose

**Estimated Effort**: 4-6 hours for all Python scripts

---

### 4. CI/CD Optimization (LOW PRIORITY)

**Current Issue**: CI/CD pipeline takes 15+ minutes primarily due to dependency installation.

**Recommendation**: Optimize with caching and pre-built images

**Option A: GitHub Actions Caching**

Add to workflow:
```yaml
- name: Cache TeXLive
  uses: actions/cache@v3
  with:
    path: /usr/share/texlive
    key: ${{ runner.os }}-texlive-${{ hashFiles('**/build_book.sh') }}
    restore-keys: |
      ${{ runner.os }}-texlive-

- name: Cache npm dependencies
  uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
```

**Option B: Pre-built Docker Images**

1. Create and publish base image to GitHub Container Registry
2. Update Dockerfile.book-builder to use base image
3. Only install project-specific dependencies in CI

**Example**:
```dockerfile
# Base image (published separately)
FROM ubuntu:latest as base
RUN apt-get update && apt-get install -y \
    texlive-xetex \
    texlive-fonts-recommended \
    pandoc
# ... other stable dependencies

# Project image (built in CI)
FROM ghcr.io/geonitab/book-builder-base:latest
COPY . /workspace
RUN npm install --legacy-peer-deps
```

**Expected Improvement**: 
- Traditional build: 90 min → 30-40 min
- Docker build: 60 min → 15-20 min

**Estimated Effort**: 3-4 hours

---

### 5. Security Dependency Updates (MEDIUM PRIORITY)

**Issue**: Some dependencies have known vulnerabilities but can't be auto-fixed.

**Affected Packages**:
1. `@toast-ui/react-editor` (peer dependency conflict)
2. `markdown` (ReDoS vulnerability, no fix available)
3. `dompurify` (via @toast-ui/editor)

**Recommendations**:

#### For @toast-ui/react-editor:
1. **Check for updates**: Search for React 18 compatible alternatives
2. **Consider alternatives**:
   - `@tiptap/react` - Modern rich text editor
   - `react-quill` - Lightweight editor
   - `lexical` - Facebook's modern editor framework

#### For markdown package:
1. **Evaluate usage**: Determine if it's actually needed
2. **Consider alternatives**:
   - `marked` - Fast, lightweight markdown parser
   - `remark` - Pluggable markdown processor
   - Native browser rendering if only display needed

#### For dompurify:
- Upgrade `@toast-ui/editor` if newer version fixes it
- Or wait for upstream fix

**Estimated Effort**: 2-3 hours investigation + implementation time

---

### 6. Additional Improvements (LOW PRIORITY)

#### 6.1 Add Standard OSS Files

Create the following files to improve project professionalism:

**CONTRIBUTING.md**:
```markdown
# Contributing to Architecture as Code Book

Thank you for your interest in contributing!

## How to Contribute

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## Development Setup

See [README.md](README.md) for installation instructions.

## Code Standards

- ESLint must pass with 0 errors
- Follow existing code style
- Add tests for new features
- Update documentation as needed

## Commit Messages

Use clear, descriptive commit messages:
- `fix:` Bug fixes
- `feat:` New features
- `docs:` Documentation updates
- `refactor:` Code refactoring
```

**CODE_OF_CONDUCT.md**: Use standard Contributor Covenant

**SECURITY.md**:
```markdown
# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| Latest  | :white_check_mark: |

## Reporting a Vulnerability

Please report security vulnerabilities to [security email].
Do not open public issues for security vulnerabilities.
```

**Estimated Effort**: 1-2 hours

#### 6.2 Add Pre-commit Hooks

Install husky and lint-staged:
```bash
npm install -D husky lint-staged
npx husky install
npx husky add .husky/pre-commit "npx lint-staged"
```

**package.json**:
```json
{
  "lint-staged": {
    "*.{ts,tsx}": ["eslint --fix", "git add"],
    "*.{md,json}": ["prettier --write", "git add"]
  }
}
```

**Benefits**: Prevents committing code with linting errors

**Estimated Effort**: 30 minutes

#### 6.3 Add Prettier for Code Formatting

```bash
npm install -D prettier
```

**Create `.prettierrc`**:
```json
{
  "semi": true,
  "trailingComma": "all",
  "singleQuote": false,
  "printWidth": 100,
  "tabWidth": 2
}
```

**Estimated Effort**: 30 minutes

---

## Priority Order for Implementation

Based on impact and effort, recommended order:

1. **Fix Documentation Language** (Option B - 1 hour) - Quick win
2. **Add Frontend Tests** (2-3 hours) - High value
3. **Modernize Python Code** (4-6 hours) - Code quality
4. **Add OSS Standard Files** (1-2 hours) - Professional polish
5. **Security Dependency Updates** (2-3 hours) - Risk mitigation
6. **Add Pre-commit Hooks** (30 min) - Prevent future issues
7. **CI/CD Optimization** (3-4 hours) - Developer experience

**Total Estimated Effort**: 14-20 hours

---

## Maintenance Checklist

Regular maintenance tasks to keep code quality high:

### Weekly
- [ ] Run `npm audit` and review vulnerabilities
- [ ] Check for dependency updates with `npm outdated`
- [ ] Review open issues and PRs

### Monthly
- [ ] Update dependencies (patch versions)
- [ ] Review and update documentation
- [ ] Run full test suite
- [ ] Check bundle size metrics

### Quarterly
- [ ] Major dependency updates
- [ ] Security audit
- [ ] Performance review
- [ ] Documentation audit

---

## Metrics to Track

Monitor these metrics to ensure continued quality:

1. **Code Quality**
   - ESLint errors: 0 (current: ✅ 0)
   - ESLint warnings: < 10 (current: ✅ 7)
   - Test coverage: > 70% (current: ❌ No frontend tests)

2. **Performance**
   - Bundle size: < 500 KB gzipped (current: ⚠️ 299 KB main + vendors)
   - Build time: < 10 seconds (current: ✅ ~7-9 seconds)
   - Lighthouse score: > 90 (not yet measured)

3. **Security**
   - Critical vulnerabilities: 0 (current: ✅ 0)
   - High vulnerabilities: 0 (current: ✅ 0)
   - Moderate vulnerabilities: < 3 (current: ⚠️ 5)

4. **Documentation**
   - README up to date: Yes (current: ✅)
   - All features documented: Yes (current: ✅)
   - API docs coverage: 100% (current: N/A)

---

## Conclusion

The repository is in good shape with recent improvements. Focus on:

1. **Language standardization** for international collaboration
2. **Test coverage** for reliability
3. **Security updates** for safety
4. **Code modernization** for maintainability

All recommendations are achievable within 15-20 hours of focused work, which will significantly improve the project's long-term sustainability and contributor experience.

---

**Last Updated**: 2025-01-04  
**Next Review**: After implementing high-priority recommendations
