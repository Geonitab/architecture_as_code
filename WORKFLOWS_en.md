# GitHub Actions Workflows Documentation

## Overview

This repository uses a unified GitHub Actions workflow to handle all aspects of the book publication and release process. The unified workflow replaces multiple separate workflows with a single, optimized solution that supports both traditional and Docker-based builds.

## Workflow Files

### 🎯 **Unified Build & Release (`unified-build-release.yml`) - RECOMMENDED**

**Purpose**: Single comprehensive workflow that consolidates all build and release functionality.

**Triggers**:
- Push to main branch with changes to:
  - `docs/**/*.md` (book chapters)
  - `docs/images/**/*.mmd` (diagrams)
  - Generation scripts (`generate_*.py`)
  - Build scripts (`build_release.sh`, `docs/build_book.sh`)
  - `Dockerfile.book-builder`
- Pull request validation
- Manual workflow dispatch with customizable options:
  - Build type: `traditional`, `docker`, or `both`
  - Deliverables: `all`, `book-only`, `presentations-only`, `whitepapers-only`, `website-only`
  - GitHub release creation: `true`/`false`

**Build Strategies**:
- **Traditional Build**: Full dependency installation (~90 minutes) for maximum compatibility
- **Docker Build**: Optimized with layer caching (~60 minutes) for faster builds
- **Both**: Runs both strategies with fallback support

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
- 📦 **Archive**: Complete unified release archive ZIP

**GitHub Release**: Creates comprehensive release with all files attached (tag: `v{run_number}-unified`)

**Duration**: 
- Traditional only: ~90 minutes
- Docker only: ~60 minutes  
- Both strategies: ~90 minutes (runs in parallel)

---

## Legacy Workflows (Removed)

The following workflows have been consolidated into the unified workflow:

### ~~🚀 Complete Release (`complete-release.yml`)~~ - **REPLACED**
### ~~🐳 Docker Complete Release (`build-book-fast.yml`)~~ - **REPLACED**  
### ~~📖 Basic Book Build (`build-book.yml`)~~ - **REPLACED**

All functionality from these workflows is now available in the unified workflow with improved features and flexibility.

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

---

### 🔍 Content Validation (`content-validation.yml`)

**Purpose**: Validates repository content and structure.

**Triggers**:
- Changes to various repository files
- Manual workflow dispatch

**Outputs**:
- Validation reports
- Content structure analysis

**No GitHub Release**: Validation only

---

## Workflow Comparison

| Feature | Unified Workflow | Whitepapers | Presentations | Content Validation |
|---------|------------------|-------------|---------------|-------------------|
| **PDF Book** | ✅ | ❌ | ❌ | ❌ |
| **EPUB/DOCX** | ✅ | ❌ | ❌ | ❌ |
| **Presentations** | ✅ | ❌ | ✅ | ❌ |
| **Whitepapers** | ✅ | ✅ | ❌ | ❌ |
| **Website** | ✅ | ❌ | ❌ | ❌ |
| **GitHub Release** | ✅ | ❌ | ❌ | ❌ |
| **Docker Optimization** | ✅ | ❌ | ❌ | ❌ |
| **Traditional Build** | ✅ | ❌ | ❌ | ❌ |
| **Selective Building** | ✅ | ❌ | ❌ | ❌ |
| **Duration** | 60-90min | ~15min | ~15min | ~5min |

## Release Types

### Unified Release Tags
- `v{run_number}-unified` - Unified workflow release (all deliverables)

### Release Contents

**Unified Releases** include:
```
Assets:
├── arkitektur_som_kod.pdf (PDF book)
├── arkitektur_som_kod.epub (EPUB book)  
├── arkitektur_som_kod.docx (Word book)
├── arkitektur_som_kod_presentation.pptx (PowerPoint)
├── whitepapers_combined.pdf (All whitepapers)
└── unified-release-archive.zip (Everything)
```

## Workflow Artifacts

All workflows upload artifacts with 30-day retention:

### Unified Workflow Artifacts
- `book-formats-unified` - All book formats (PDF, EPUB, DOCX)
- `presentation-materials-unified` - Presentation files
- `whitepapers-unified` - All whitepaper files
- `website-build-unified` - Static website build
- `unified-release-archive` - Complete archive ZIP
- `unified-traditional-build` - Traditional build results
- `unified-docker-build` - Docker build results

### Standalone Workflow Artifacts
- `presentation-materials` - Standalone presentation generation
- `whitepaper-documents` - Standalone whitepaper generation
- `whitepapers-archive` - Whitepaper collection ZIP

## Usage Recommendations

### For Production Releases
- **Use**: `unified-build-release.yml` (comprehensive, all deliverables)
- **Manual trigger options**: Choose build strategy and deliverables as needed

### For Development/Testing
- **Use**: `unified-build-release.yml` with `book-only` or specific deliverable types
- **Use**: Individual component workflows for quick standalone testing

### For Distribution
- **Complete package**: Use unified workflow with `all` deliverables
- **Individual components**: Use unified workflow with specific deliverable selection
- **Standalone testing**: Use `generate-presentations.yml` or `generate-whitepapers.yml`

## Troubleshooting

### Common Issues

1. **Workflow timeout**: Both traditional and Docker builds have appropriate timeouts
2. **Dependency installation failure**: Check cache keys and restore-keys in unified workflow
3. **Docker build failure**: Verify Dockerfile.book-builder syntax and dependencies  
4. **Release creation failure**: Check GITHUB_TOKEN permissions
5. **Build strategy conflicts**: Use workflow_dispatch to specify build type manually

### Debugging

1. Check workflow logs in GitHub Actions tab
2. Download artifacts to inspect interwithiate files from both build strategies
3. Run individual steps locally using provided scripts
4. Use workflow_dispatch for manual triggering with custom parameters

## Manual Workflow Triggering

### Unified Workflow Manual Triggering

The unified workflow supports comprehensive manual triggering via GitHub UI:

1. Go to Actions tab in GitHub
2. Select "Unified Build & Release" workflow
3. Click "Run workflow"
4. Configure options:
   - **Build Type**: `traditional`, `docker`, or `both`
   - **Deliverables**: `all`, `book-only`, `presentations-only`, `whitepapers-only`, `website-only`
   - **Create Release**: `true` or `false`
5. Choose branch (typically `main`)

### Standalone Workflow Triggering

Other workflows support basic manual triggering:
- **Generate Presentations**: No parameters, creates presentation materials
- **Generate Whitepapers**: No parameters, creates whitepaper documents
- **Content Validation**: No parameters, validates repository structure

The unified workflow includes comprehensive GitHub release creation when manually triggered with the release option enabled.