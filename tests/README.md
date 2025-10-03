# Content Validation Test Suite

This directory contains a comprehensive test suite for validating the "Arkitektur som Kod" book content. The tests ensure that all content meets quality requirements for completeness, consistency, clarity, and technical accuracy.

## 🧪 Test Suite Overview

### Test Modules

1. **`test_completeness.py`** - Validates structural completeness
   - All required chapters exist
   - Proper file naming conventions
   - Required sections present (title, diagrams, sources)
   - Images and diagrams availability

2. **`test_consistency.py`** - Ensures uniform formatting and style
   - Header hierarchy consistency
   - Title format standardization
   - Diagram reference format
   - Language consistency (Swedish or English based on `--language` flag)
   - Terminology usage patterns

3. **`test_clarity.py`** - Checks content quality and readability
   - Minimum content length requirements
   - Adequate paragraph structure
   - Sufficient subsections
   - Sentence length analysis
   - Flow indicators and transitions

4. **`test_technical_accuracy.py`** - Validates technical content
   - YAML/JSON syntax validation
   - Code block syntax highlighting
   - Terraform/HCL syntax checks
   - Bash script safety analysis
   - Diagram reference validation
   - URL format compliance

## 📋 Requirements Configuration

The test suite uses `requirements.yaml` for Swedish content and `requirements_en.yaml` for English content to define:
- Expected book structure (27 chapters)
- Content quality standards
- Technical validation rules
- Special chapter exceptions (glossary, authors, etc.)

## 🌍 Language Support

The test suite supports testing both Swedish and English content:

### Testing Swedish Content (Default)
```bash
# Run all tests on Swedish content (default behavior)
python3 -m pytest tests/ -v

# Explicitly specify Swedish
python3 -m pytest tests/ -v --language=svenska
```

### Testing English Content
```bash
# Run all tests on English content
python3 -m pytest tests/ -v --language=english

# Run specific test categories on English content
python3 -m pytest tests/test_consistency.py -v --language=english
python3 -m pytest tests/test_completeness.py -v --language=english
```

### Language-Specific Behavior

- **Swedish tests** (`--language=svenska`):
  - Use `requirements.yaml` configuration
  - Test files without `_en.md` suffix
  - Check for English words in Swedish content
  
- **English tests** (`--language=english`):
  - Use `requirements_en.yaml` configuration
  - Test files with `_en.md` suffix
  - Check for Swedish words in English content

Both language configurations support the same test categories: completeness, consistency, clarity, and technical accuracy.

## 🚀 Running Tests

### Using npm scripts:
```bash
# Run all content validation tests
npm run test:content

# Generate HTML reports
npm run test:content:report

# Run specific test categories
npm run test:completeness
npm run test:consistency
npm run test:clarity
npm run test:technical
```

### Using the test runner directly:
```bash
# Install dependencies and run all tests
python3 tests/run_tests.py --install-deps

# Run specific test types
python3 tests/run_tests.py --type completeness
python3 tests/run_tests.py --type consistency
python3 tests/run_tests.py --type clarity
python3 tests/run_tests.py --type technical

# Skip HTML report generation
python3 tests/run_tests.py --no-report

# Quiet mode
python3 tests/run_tests.py --quiet
```

### Using pytest directly:
```bash
# Run all tests with verbose output
python3 -m pytest tests/ -v

# Run with HTML report
python3 -m pytest tests/ -v --html=test-reports/report.html --self-contained-html

# Run specific test file
python3 -m pytest tests/test_completeness.py -v
```

### Manual mobile responsiveness testing:
```bash
# Generate a report and apply mobile styles manually
python3 tests/run_tests.py --type technical
# Or apply mobile styles to existing report
python3 tests/make_mobile_responsive.py test-reports/content-validation-technical.html
```

## 🔄 CI/CD Integration

The test suite is integrated into the GitHub Actions workflow:

- **Triggers**: On pull requests and pushes to main that modify content
- **Automatic execution**: Runs all validation tests
- **Report generation**: Creates HTML reports for each test category
- **Artifact storage**: Saves test reports for 30 days
- **PR comments**: Automatically comments test results on pull requests

### GitHub Actions Workflow

The content validation runs as part of `.github/workflows/content-validation.yml`:

1. Sets up Python 3.12 environment
2. Installs test dependencies
3. Generates book content
4. Runs all validation tests
5. Creates detailed HTML reports
6. Uploads test artifacts
7. Comments results on PRs

## 📊 Test Reports

Test reports are generated in `test-reports/` directory:
- `content-validation-all.html` - Complete test suite results
- `completeness-report.html` - Structural completeness results
- `consistency-report.html` - Formatting consistency results
- `clarity-report.html` - Content clarity results
- `technical-report.html` - Technical accuracy results

### 📱 Mobile Compatibility

All test reports are automatically optimized for mobile devices, including iPhone:
- **Responsive design**: Tables convert to mobile-friendly card layouts on small screens
- **Touch-friendly**: Properly sized buttons and interactive elements
- **Readable text**: Optimized font sizes for mobile reading
- **Viewport optimization**: Includes proper viewport meta tags for mobile browsers

The mobile optimization is automatically applied when reports are generated using `run_tests.py`.

## ⚙️ Configuration

### Test Behavior

Tests are configured to be practical for an evolving book:
- **Hard failures**: Missing chapters, invalid file names, broken code syntax
- **Warnings only**: Missing sources sections, style issues, unclear terminology
- **Flexible validation**: Special chapters (glossary, authors) have different requirements

### Customization

Modify `requirements.yaml` to adjust:
- Content quality thresholds
- Required section patterns
- Special chapter rules
- Technical validation settings

## 🔧 Dependencies

The test suite requires:
- `pytest>=7.0.0` - Test framework
- `pytest-html>=3.1.0` - HTML report generation
- `pyyaml>=6.0.0` - YAML configuration parsing

Install with:
```bash
python3 tests/run_tests.py --install-deps
```

### Mobile Responsiveness Tools

The test suite includes mobile optimization tools:
- `tests/mobile-responsive.css` - Mobile-friendly CSS overrides
- `tests/make_mobile_responsive.py` - Post-processor for adding mobile styles

These are automatically applied when generating reports with `run_tests.py`.

## 🚨 Common Test Failures

### Completeness Issues
- **Missing chapters**: Ensure all 23 expected chapter files exist
- **Invalid naming**: Use `XX_name.md` format (e.g., `01_inledning.md`)
- **Missing sections**: Add H1 title, diagram reference, and sources section

### Consistency Issues
- **Header hierarchy**: Don't skip header levels (H1 → H2 → H3)
- **Title format**: Keep titles under 80 characters, no trailing punctuation
- **Diagram references**: Use `![description](images/diagram_XX_name.png)` format

### Clarity Issues
- **Content length**: Ensure chapters have sufficient content (500+ characters)
- **Structure**: Include at least 3 paragraphs and 2 subsections (H2)
- **Flow**: Add transition words and connecting phrases

### Technical Issues
- **YAML syntax**: Validate YAML code blocks for proper syntax
- **Code highlighting**: Specify language for code blocks (```yaml, ```bash, etc.)
- **Terraform syntax**: Ensure balanced braces and valid resource syntax

## 📈 Future Enhancements

Planned improvements:
- Link validation for external references
- Terminology consistency enforcement
- Automated content suggestions
- Integration with writing style guides
- Performance benchmarking for content generation

## 🤝 Contributing

When adding new tests:
1. Follow the existing test structure and naming conventions
2. Update `requirements.yaml` for new validation rules
3. Add appropriate fixtures in `conftest.py`
4. Include both positive and negative test cases
5. Document the purpose and expected behavior
6. Consider warnings vs. failures for different severity levels

The test suite is designed to be modular and extensible to support the evolving needs of the book project.