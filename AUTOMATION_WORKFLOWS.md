# Automation Workflows Documentation

This document describes the GitHub Actions workflows that automate the generation of presentations and whitepapers from the book content.

## Overview

Two new automation workflows have been added to the repository:

1. **Presentation Generation** (`generate-presentations.yml`) - Creates PowerPoint presentation materials
2. **Whitepaper Generation** (`generate-whitepapers.yml`) - Creates individual HTML whitepaper documents

Both workflows automatically trigger when relevant content changes and generate high-quality, professionally formatted output files.

## Presentation Generation Workflow

### Purpose
Automatically generates PowerPoint presentation materials from book chapters to create engaging presentations for conferences, workshops, and educational purposes.

### Trigger Conditions
The workflow runs when:
- Push or PR changes to `docs/**/*.md` (book chapters)
- Changes to `generate_presentation.py` script
- Changes to the workflow file itself
- Manual triggering via GitHub Actions UI

### Generated Outputs
- **`presentation_outline.md`** - Structured outline with key points from each chapter
- **`generate_pptx.py`** - Python script to create PowerPoint presentations
- **`requirements.txt`** - Dependencies needed for PowerPoint generation
- **`arkitektur_which_kod_presentation.pptx`** - Complete PowerPoint presentation file (ready to use)

### Workflow Steps
1. **Setup Environment** - Python 3.12 with required dependencies
2. **Install PowerPoint Dependencies** - Install python-pptx library
3. **Generate Materials** - Run `generate_presentation.py --create-pptx` script
4. **Validation** - Verify all expected files are created with correct structure
5. **Artifact Upload** - Store generated materials and PowerPoint file for download
6. **PR Comments** - Add summary comment on pull requests

### Usage
After the workflow completes, the PowerPoint presentation is ready for imwithiate use!

**Download from GitHub Actions artifacts:**
- `arkitektur_which_kod_presentation.pptx` - Complete presentation (28 slides)
- `presentation_outline.md` - Structured outline for reference
- `generate_pptx.py` - Script for local customization
- `requirements.txt` - Dependencies list

**For local generation or customization:**
```bash
# Download artifacts from GitHub Actions or clone repository
python3 generate_presentation.py --create-pptx
# Or with custom output name:
python3 generate_presentation.py --create-pptx --output my_presentation.pptx
```

This creates a professional PowerPoint presentation with:
- Title slides for each chapter
- Key bullet points and concepts
- Swedish-language content optimized for architecture as code topics
- Professional Kvadrat branding and styling

## Whitepaper Generation Workflow

### Purpose
Automatically generates individual HTML whitepaper documents from each book chapter, creating standalone documents suitable for distribution, sharing, and marketing.

### Trigger Conditions
The workflow runs when:
- Push or PR changes to `docs/**/*.md` (book chapters)
- Changes to `generate_whitepapers.py` script
- Changes to the workflow file itself
- Manual triggering via GitHub Actions UI

### Generated Outputs
- **26 HTML whitepaper files** - One for each book chapter (e.g., `01_inledning_whitepaper.html`)
- **Archive file** - ZIP collection of all whitepapers for easy distribution

### Workflow Steps
1. **Setup Environment** - Python 3.12 environment
2. **Generate Whitepapers** - Run `generate_whitepapers.py` script
3. **Validation** - Verify HTML structure and content quality
4. **Quality Checks** - Validate Swedish content and proper formatting
5. **Archive Creation** - Create ZIP file containing all whitepapers
6. **Artifact Upload** - Store individual files and archive
7. **Performance Metrics** - Track generation efficiency and file sizes

### Features
Each whitepaper includes:
- **Professional HTML design** - Modern, responsive layout with Kvadrat branding
- **Swedish Content** - Optimized for Swedish organizations and compliance requirements
- **Standalone Format** - Can be shared independently via email, web, or print
- **SEO Optimized** - Proper meta tags and structured content
- **Print-Ready** - CSS styling optimized for both screen and print media

## File Structure

```
.github/workflows/
├── generate-presentations.yml    # Presentation automation workflow
├── generate-whitepapers.yml     # Whitepaper automation workflow
├── build-book.yml               # Existing book PDF generation
└── content-validation.yml       # Existing content validation

presentations/                   # Generated presentation materials (ignored in git)
├── presentation_outline.md      # Chapter outlines and key points
├── generate_pptx.py             # PowerPoint generation script
├── requirements.txt             # Python dependencies
└── arkitektur_som_kod_presentation.pptx  # Generated PowerPoint file (ready to use)

whitepapers/                     # Generated whitepaper documents (ignored in git)
├── 01_inledning_whitepaper.html # Introduction whitepaper
├── 02_grundlaggande_principer_whitepaper.html
├── ...                         # One HTML file per chapter
└── 26_appendix_kodexempel_whitepaper.html
```

## Configuration

### Workflow Settings
Both workflows use these environment variables:
- `ARTIFACT_RETENTION_DAYS: 30` - How long to keep generated artifacts
- `timeout-minutes: 15` - Maximum runtime for each workflow

### Dependencies
- **Python 3.12** - Primary runtime environment
- **python-pptx** - PowerPoint generation library (presentations only)
- **Standard Library** - HTML generation uses built-in Python modules

### Triggers
Both workflows are optimized to run only when necessary:
- Changes to book chapters (`docs/**/*.md`)
- Changes to generation scripts
- Manual triggering for testing or special builds
- Excluded: changes to other parts of the repository

## Integration with Existing Workflows

### Book Building Pipeline
The new workflows complement the existing `build-book.yml`:
- **Book PDF**: Complete book as single PDF document
- **Presentations**: Chapter content as PowerPoint materials
- **Whitepapers**: Individual chapters as standalone HTML documents

### Content Validation
All workflows include docs protection validation using `scripts/validate_docs_protection.py` to ensure:
- No unauthorized changes to book content
- Proper separation of generated vs. source content
- Adherence to content management guidelines

### Artifact Management
Generated files are:
- **Excluded from Git** - Added to `.gitignore` to prevent repository bloat
- **Stored as Artifacts** - Available for download via GitHub Actions
- **Archived for Distribution** - ZIP files for easy sharing
- **Automatically Cleaned** - 30-day retention policy

## Debugging and Troubleshooting

### Common Issues

1. **Missing Dependencies**
   - Solution: Workflows automatically install required Python packages

2. **File Generation Failures**
   - Check: Source markdown files in `docs/` directory
   - Verify: Python script syntax using validation steps

3. **HTML Validation Errors**
   - Issue: Missing or malforwith HTML structure
   - Solution: Workflows include comprehensive validation steps

### Monitoring
Each workflow provides detailed logging:
- File generation progress
- Validation results
- Performance metrics
- Quality assurance checks

### Manual Testing
To test locally before pushing:
```bash
# Test presentation generation
python3 generate_presentation.py

# Test whitepaper generation  
python3 generate_whitepapers.py

# Validate generated files
ls -la presentations/
ls -la whitepapers/
```

## Security and Best Practices

### Docs Protection
- Workflows never modify source content in `docs/` directory
- Generated files are stored outside the docs directory
- Validation scripts ensure content integrity

### Access Control
- Workflows run with standard GitHub Actions permissions
- No external services or credentials required
- All operations are contained within the repository

### Performance Optimization
- Efficient triggering based on relevant file changes
- Caching not implemented (generation is fast enough)
- Parallel execution where possible

## Future Enhancements

Potential improvements for the workflows:
- **Multi-language Support** - Generate presentations/whitepapers in multiple languages
- **Custom Themes** - Configurable branding and styling options
- **Integration Testing** - Automated quality assurance for generated content
- **Deployment Integration** - Automatic publishing to websites or documentation platforms
- **Analytics Integration** - Track usage and performance of generated materials

## Support

For issues with the automation workflows:
1. Check the workflow logs in GitHub Actions tab
2. Verify the source scripts (`generate_presentation.py`, `generate_whitepapers.py`)
3. Review the artifact outputs for debugging information
4. Run the generation scripts locally to isolate issues

The workflows are designed to be robust and provide detailed error reporting to facilitate quick issue resolution.