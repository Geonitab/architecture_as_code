# GitHub Actions Workflows Documentation

## Overview

This repository uses a unified GitHub Actions workflow to handle all aspects of the book publication and release process. The unified workflow replaces multiple separate workflows with a single, optimized solution that supports both traditional and Docker-based builds.

### Workflow catalogue at a glance

| Workflow | File | Purpose | Typical triggers | Key outputs / actions |
|----------|------|---------|------------------|------------------------|
| Unified Build & Release | `.github/workflows/unified-build-release.yml` | Builds every deliverable (book formats, presentations, whitepapers, website) in one pass | Push or pull request touching book sources, scripts, or workflow; manual dispatch | Publishes multi-format artefacts, optional GitHub release |
| Build MkDocs Site | `.github/workflows/build-mkdocs.yml` | Builds and deploys the MkDocs site to `gh-pages` | Push or pull request affecting `docs/**` or `mkdocs.yml`; manual dispatch | Updates the documentation site via GitHub Pages |
| Generate Presentations | `.github/workflows/generate-presentations.yml` | Regenerates presentation materials from the manuscript | Push or pull request touching chapter markdown or the generator script; manual dispatch | Uploads PPTX deck, outline, and helper scripts as artefacts |
| Generate Whitepapers | `.github/workflows/generate-whitepapers.yml` | Produces standalone HTML whitepapers per chapter | Push or pull request touching chapter markdown or the generator script; manual dispatch | Uploads individual HTML files and a combined archive |
| Content Validation Tests | `.github/workflows/content-validation.yml` | Runs quality checks over generated content | Push or pull request touching docs, tests, or `generate_book.py`; manual dispatch | Pytest reports and a PR summary comment |
| Validate Heading Capitalisation | `.github/workflows/validate-heading-capitalization.yml` | Guard-rail to keep headings in sentence case | Push or pull request touching `docs/**/*.md`; manual dispatch | Fails fast if headings break the style guide |
| Validate Figure Captions | `.github/workflows/validate-figure-captions.yml` | Ensures figure captions follow the house style | Push or pull request touching `docs/**/*.md`; manual dispatch | Fails fast if captions fall outside the expected pattern |
| Auto draft PR from issue + Codex auto-fix | `.github/workflows/assign-codex.yml` | Seeds a draft PR for new issues and re-runs Codex on active PRs | Issue opened/reopened; pull request opened, reopened, synchronised, or marked ready | Keeps the `codex/issue-*` branches in sync and comments with Codex results |
| Cleanup Old Branches | `.github/workflows/clean-old-braches.yml` | Prunes remote branches that have gone stale | Scheduled daily run; manual dispatch | Deletes remote branches (excluding `main`/`gh-pages`) older than two days |
| Close conflicted pull requests | `.github/workflows/close-conflicted-pull-requests.yml` | Helps triage conflicted or empty PRs | Manual dispatch | Closes conflicted/empty PRs and opens explanatory issues |
| Create GitHub Issues from Markdown | `.github/workflows/create-issues.yml` | Raises issues from templates under `.github/scripts` | Manual dispatch | Uses `.github/scripts/create_issues.py` to file issues against the repo |
| Dependabot auto-merge | `.github/workflows/dependabot-automerge.yml` | Scaffold for automated Dependabot merges | Dependabot pull requests; manual dispatch | Placeholder step printing instructions for running the merge logic |

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

### 🔧 Supporting automation and maintenance workflows

The repository also relies on a handful of operational workflows that keep day-to-day housekeeping on track:

- **`assign-codex.yml`** – When an issue is opened or reopened the workflow spins up (or reuses) a `codex/issue-*` branch, opens a draft PR, and immediately runs the Codex assistant so that every issue starts life with a working draft. It also re-invokes Codex whenever a linked PR is updated, keeping the generated fixes fresh.
- **`clean-old-braches.yml`** – Runs nightly to prune remote branches whose last commit is older than forty-eight hours, excluding `main` and `gh-pages`. Use the manual dispatch if you need an ad-hoc sweep.
- **`close-conflicted-pull-requests.yml`** – A manual triage tool that inspects open PRs, closes those that are conflicted or contain no file changes, and raises an explanatory issue for each closure so context is not lost.
- **`create-issues.yml`** – Exposes a manual button that executes `.github/scripts/create_issues.py`, allowing bulk issue creation from curated markdown catalogues under source control.
- **`dependabot-automerge.yml`** – A starter workflow intended for automating Dependabot PR merges. It currently installs dependencies and echoes placeholders, ready for a future command that performs the actual merge step.

## Release Types

### Unified Release Tags
- `v{run_number}-unified` - Unified workflow release (all deliverables)

### Release Contents

**Unified Releases** include:
```
Assets:
├── architecture_as_code.pdf (PDF book)
├── architecture_as_code.epub (EPUB book)  
├── architecture_as_code.docx (Word book)
├── architecture_as_code_presentation.pptx (PowerPoint)
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
