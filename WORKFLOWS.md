# GitHub Actions Workflows Documentation

## Overview

This repository includes several GitHub Actions workflows to handle different aspects of the book publication and release process. Each workflow serves a specific purpose and creates different outputs.

## Workflow Files

### 🚀 Complete Release (`complete-release.yml`) - **RECOMMENDED**

**Purpose**: Creates comprehensive releases with all deliverable formats.

**Triggers**:
- Push to main branch with changes to:
  - `docs/**/*.md` (book chapters)
  - `docs/images/**/*.mmd` (diagrams)
  - Generation scripts (`generate_*.py`)
  - Build scripts (`build_release.sh`, `docs/build_book.sh`)
- Manual workflow dispatch with release option

**Dependencies Installed**:
- Python 3.12
- Node.js 18 with npm dependencies
- Pandoc 3.1.9
- TeXLive (full LaTeX distribution)
- Google Chrome + Mermaid CLI
- python-pptx for presentations

**Outputs**:
- 📖 **Book formats**: PDF, EPUB, DOCX
- 🎤 **Presentations**: PPTX with outline and scripts
- 📄 **Whitepapers**: Individual HTML files + combined PDF
- 🌐 **Website**: Complete static site build
- 📦 **Archive**: Complete release archive ZIP

**GitHub Release**: Creates comprehensive release with all files attached

**Duration**: ~90 minutes (includes full dependency installation)

---

### 🐳 Docker Complete Release (`build-book-fast.yml`)

**Purpose**: Docker-optimized version of complete release for faster builds.

**Triggers**:
- Same as complete-release.yml
- Additionally triggers on `Dockerfile.book-builder` changes

**Key Features**:
- Docker container with pre-installed dependencies
- GitHub Actions caching for Docker layers
- Parallel processing where possible
- Same outputs as complete-release.yml

**Outputs**: Identical to complete-release.yml

**GitHub Release**: Creates Docker-tagged comprehensive release

**Duration**: ~60 minutes (Docker caching reduces dependency installation time)

---

### 📖 Basic Book Build (`build-book.yml`) - **LEGACY**

**Purpose**: Simple PDF-only generation (original workflow).

**Triggers**:
- Push/PR to main branch with changes to:
  - `docs/**/*.md`
  - `docs/images/**/*.mmd`
  - `generate_book.py`
  - Workflow file itself

**Outputs**:
- PDF book only
- Generated diagram PNGs

**GitHub Release**: Simple release with PDF only

**Duration**: ~45 minutes

---

### 📄 Whitepaper Generation (`generate-whitepapers.yml`)

**Purpose**: Standalone whitepaper generation for individual chapter distribution.

**Triggers**:
- Changes to book chapters
- Changes to whitepaper generation script

**Outputs**:
- Individual HTML whitepapers
- Whitepaper archive ZIP
- Validation reports

**No GitHub Release**: Artifacts only

---

### 🎤 Presentation Generation (`generate-presentations.yml`)

**Purpose**: Standalone presentation material generation.

**Triggers**:
- Changes to book chapters
- Changes to presentation generation script

**Outputs**:
- PowerPoint presentation (PPTX)
- Presentation outline (Markdown)
- Generation scripts

**No GitHub Release**: Artifacts only

## Workflow Comparison

| Feature | Complete Release | Docker Complete | Basic Book | Whitepapers | Presentations |
|---------|------------------|-----------------|------------|-------------|---------------|
| **PDF Book** | ✅ | ✅ | ✅ | ❌ | ❌ |
| **EPUB/DOCX** | ✅ | ✅ | ❌ | ❌ | ❌ |
| **Presentations** | ✅ | ✅ | ❌ | ❌ | ✅ |
| **Whitepapers** | ✅ | ✅ | ❌ | ✅ | ❌ |
| **Website** | ✅ | ✅ | ❌ | ❌ | ❌ |
| **GitHub Release** | ✅ | ✅ | ✅ | ❌ | ❌ |
| **Docker** | ❌ | ✅ | ❌ | ❌ | ❌ |
| **Duration** | ~90min | ~60min | ~45min | ~15min | ~15min |

## Release Types

### Complete Release Tags
- `v{run_number}-complete` - Complete release workflow
- `v{run_number}-docker` - Docker complete release workflow  
- `v{run_number}` - Basic book workflow
- `v{run_number}-fast` - Legacy fast build (deprecated)

### Release Contents

**Complete Releases** include:
```
Assets:
├── arkitektur_som_kod.pdf (PDF book)
├── arkitektur_som_kod.epub (EPUB book)  
├── arkitektur_som_kod.docx (Word book)
├── arkitektur_som_kod_presentation.pptx (PowerPoint)
├── whitepapers_combined.pdf (All whitepapers)
└── complete-release-archive.zip (Everything)
```

**Basic Releases** include:
```
Assets:
└── arkitektur_som_kod.pdf (PDF book only)
```

## Workflow Artifacts

All workflows also upload artifacts with 30-day retention:

### Complete Release Artifacts
- `book-formats-complete` - All book formats (PDF, EPUB, DOCX)
- `presentation-materials-complete` - Presentation files
- `whitepapers-complete` - All whitepaper files
- `website-build-complete` - Static website build
- `complete-release-archive` - Complete archive ZIP

### Docker Release Artifacts
- Same as complete release but with `-docker` suffix

### Basic Book Artifacts
- `arkitektur-som-kod-pdf` - PDF file only
- `book-diagrams` - Generated PNG diagrams

## Usage Recommendations

### For Production Releases
- **Use**: `complete-release.yml` (comprehensive)
- **Alternative**: `build-book-fast.yml` (Docker-optimized)

### For Development/Testing
- **Use**: `build-book.yml` (quick PDF validation)
- **Use**: Individual component workflows for specific testing

### For Distribution
- **Book only**: Use basic workflow
- **Complete package**: Use complete release workflows
- **Individual components**: Use standalone component workflows

## Troubleshooting

### Common Issues

1. **Workflow timeout**: Increase timeout-minutes in workflow file
2. **Dependency installation failure**: Check cache keys and restore-keys
3. **Docker build failure**: Verify Dockerfile syntax and dependencies
4. **Release creation failure**: Check GITHUB_TOKEN permissions

### Debugging

1. Check workflow logs in GitHub Actions tab
2. Download artifacts to inspect intermediate files
3. Run individual steps locally using provided scripts
4. Use workflow_dispatch for manual triggering with custom parameters

## Manual Workflow Triggering

All workflows support manual triggering via GitHub UI:

1. Go to Actions tab in GitHub
2. Select desired workflow
3. Click "Run workflow"
4. Choose branch and parameters (if applicable)

The complete release workflows include an option to create GitHub releases when manually triggered.