# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository is a **book publishing platform** for "Architecture as Code", a comprehensive technical book covering architecture-as-code principles across 38 chapters and appendices. The project automates the generation of multiple publication formats (PDF, EPUB, DOCX), presentations, whitepapers, and a documentation website.

**Key principle:** This is primarily a publishing automation project. There is no React dashboard or front-end application (historical references in old configs may exist but can be ignored).

## Essential Commands

### Book Building
```bash
# Generate manuscript content from automation scripts
python3 generate_book.py

# Build all book formats (PDF, EPUB, DOCX) - runs from repo root
docs/build_book.sh

# Complete book workflow (content + build)
python3 generate_book.py && docs/build_book.sh

# Verify environment matches locked versions
make verify-env
```

### Diagram Management
```bash
# Install Mermaid CLI toolchain
npm ci

# Validate all Mermaid diagrams match their PNG exports
python3 scripts/check_mermaid_diagrams.py
```

### Complete Release Build
```bash
# Generate all deliverables (book, presentations, whitepapers)
python3 build_all_orchestrator.py --zip

# Full release pipeline (same as CI/CD)
./build_release.sh
```

### Documentation Site
```bash
# Local preview
mkdocs serve

# Build static site
mkdocs build
```

### Testing
```bash
# Run content validation tests
python3 -m pytest tests/ -v

# Run specific test suites
python3 -m pytest tests/test_completeness.py -v
python3 -m pytest tests/test_consistency.py -v
python3 -m pytest tests/test_technical_accuracy.py -v
```

### Validation Scripts
```bash
# Verify all internal and external links
python3 scripts/verify_links.py

# Verify cited sources (URLs and ISBNs)
python3 scripts/verify_sources.py

# Check document numbering consistency
python3 scripts/check_doc_numbering.py
```

## Architecture Overview

### Content Organization

The book is organized as **7 core parts (A-G) plus Part H (appendices)**:
- **Part A (Foundations):** Chapters 1-4 - Core concepts and principles
- **Part B (Architecture Platform):** Chapters 5-8 - Tooling and automation
- **Part C (Security & Governance):** Chapters 9-12 (including 9B, 9C) - Security and compliance
- **Part D (Delivery & Operations):** Chapters 13-16 (including 15A, 15B) - Testing and delivery
- **Part E (Organisation & Leadership):** Chapters 17-21 - Team structure and change management
- **Part F (Experience & Best Practices):** Chapters 22-24 - Collaboration and lessons learned
- **Part G (Future & Wrap-up):** Chapters 25-27 (including 26A, 26B) - Future trends and conclusion
- **Part H (Appendices):** Chapters 28-34 plus supplements - Reference materials and tools

**Canonical source of truth:** `docs/book_index.json` defines the complete chapter ordering and metadata. All automation and quality checks consume this file.

### Repository Structure
```
docs/                           # All manuscript content
├── [0-9]*.md                   # Numbered chapters (01_introduction.md, etc.)
├── part_*.md                   # Part introductions (part_a_foundations.md, etc.)
├── appendix_*.md               # Appendices
├── images/*.mmd                # Mermaid diagram sources (~100 files)
├── images/*.png                # Generated PNG diagrams (committed)
├── build_book.sh               # PDF/EPUB/DOCX build script
└── pandoc.yaml                 # Pandoc configuration

releases/                       # Generated deliverables (git-ignored)
├── book/                       # PDF, EPUB, DOCX
├── presentation/               # PowerPoint deck
├── whitepapers/                # HTML exports per chapter
└── website/                    # Static site output

scripts/                        # Validation and automation utilities
├── check_mermaid_diagrams.py   # Verify diagram consistency
├── verify_links.py             # Link validation
├── verify_sources.py           # Source verification
├── verify_environment.py       # Toolchain validation
└── navigation.py               # Shared utilities for chapter ordering

.github/workflows/              # CI/CD automation
├── unified-build-release.yml   # Main build pipeline
├── build-mkdocs.yml            # Website deployment
├── verify-mermaid-diagrams.yml # Diagram validation
├── content-validation.yml      # Quality checks
└── *-bot.yml                   # Specialized issue automation

tests/                          # Pytest test suites
├── test_completeness.py        # Content completeness validation
├── test_consistency.py         # Cross-chapter consistency
└── test_technical_accuracy.py  # Technical correctness
```

### Build Pipeline Architecture

1. **Content Generation:** `generate_book.py` reads `docs/book_index.json` and processes chapter files using the `scripts/navigation.py` module
2. **Diagram Export:** `docs/build_book.sh` uses Mermaid CLI to convert `.mmd` files to PNG (with fallback if Chromium unavailable)
3. **Book Compilation:** Pandoc converts Markdown → PDF/EPUB/DOCX using the Eisvogel LaTeX template
4. **Supplementary Formats:**
   - `generate_presentation.py` creates PowerPoint decks with chapter summaries
   - `generate_whitepapers.py` exports HTML versions of individual chapters
   - `mkdocs build` generates the browsable documentation site

### Diagram Workflow

**Critical principle:** Both `.mmd` source files and rendered `.png` files are committed to version control. This ensures offline readers and document reviewers have stable diagrams without regenerating assets.

- Mermaid sources live in `docs/images/*.mmd`
- PNG exports live in `docs/images/*.png`
- PNG files are marked as binary in `.gitattributes` to keep PRs readable
- CI enforces that every PNG matches its source via `scripts/check_mermaid_diagrams.py`
- If you modify a `.mmd` file, you must regenerate its PNG before committing

## Development Guidelines

### Editorial Standards

**Language:** Use Oxford-standard British English throughout all manuscript content
- "organisation" not "organization"
- "optimisation" not "optimization"
- "colour" not "color"
- "centre" not "center"

**Terminology:**
- Always capitalize as **"Architecture as Code"** (never "Architecture As Code" or "architecture as code")
- Use "programme" for initiatives (British usage)
- Refer to audiences as "teams", "practitioners", or "organisations"

**Reference:** See `docs/STYLE_GUIDE.md` for complete editorial rules.

### Making Changes

1. **For manuscript edits:**
   ```bash
   # Edit chapter files in docs/
   # Then regenerate and validate
   python3 generate_book.py && docs/build_book.sh
   ```

2. **For diagram changes:**
   ```bash
   # Edit .mmd file in docs/images/
   # Regenerate PNG
   npm ci  # if not already done
   python3 scripts/check_mermaid_diagrams.py
   ```

3. **For automation scripts:**
   ```bash
   # Edit Python files in scripts/ or root-level generators
   # Test with actual build
   python3 generate_book.py && docs/build_book.sh

   # Run relevant tests
   python3 -m pytest tests/test_completeness.py -v
   ```

### Critical Timing Notes (from AGENTS.md)

- **NEVER CANCEL** long-running dependency installs (TeXLive takes 8+ minutes)
- Always use adequate timeouts: 60+ minutes for installs, 5+ minutes for builds
- Book content generation: <1 second
- Complete book build with diagrams: ~30 seconds
- Full CI/CD pipeline: 15+ minutes (due to dependency installation)

### Common Validation Tasks

After making changes:
```bash
# Verify environment
make verify-env

# Check links
python3 scripts/verify_links.py

# Check sources
python3 scripts/verify_sources.py

# Check diagrams
python3 scripts/check_mermaid_diagrams.py

# Run content tests
python3 -m pytest tests/ -v

# Build everything
python3 build_all_orchestrator.py
```

## Technology Stack

**Core Publishing:**
- Python 3.12.3 - Content generation scripts
- Pandoc 3.1.9 - Markdown → PDF/EPUB/DOCX conversion
- XeLaTeX (TeXLive) - PDF rendering engine
- Mermaid CLI 10.7.0 (`@mermaid-js/mermaid-cli`) - Diagram generation
- MkDocs - Static documentation site

**Automation:**
- Node.js 20.11.1 - Mermaid CLI and helper scripts
- pytest - Content validation test framework
- GitHub Actions - CI/CD orchestration

**Version Locking:**
- `BOOK_REQUIREMENTS.md` - Canonical version declarations
- `requirements.txt` - Python dependencies
- `package.json` + `package-lock.json` - Node.js dependencies
- Use `make verify-env` to confirm all versions match

## CI/CD Workflows

### Main Workflows
- **unified-build-release.yml:** Orchestrates complete release build (book + presentation + whitepapers + website)
- **build-mkdocs.yml:** Builds and deploys documentation site to GitHub Pages (https://aac.geon.se)
- **verify-mermaid-diagrams.yml:** Validates diagram consistency on every push
- **content-validation.yml:** Runs pytest test suites for completeness, consistency, and technical accuracy

### Bot Workflows
Specialized automation bots respond to labeled GitHub issues:

| Bot | Workflow | Trigger Label |
|-----|----------|---------------|
| Architect Bot | `architect-bot.yml` | `architecture` |
| Developer Bot | `developer-bot.yml` | `dev` |
| Designer Bot | `designer-bot.yml` | `design` |
| Editor Bot | `editor-bot.yml` | `documentation` |
| QA Bot | `qa-bot.yml` | `qa` |
| Requirements Bot | `requirements-bot.yml` | `req` |

Apply the appropriate label to trigger the corresponding bot response.

## Website Deployment

- **Public URL:** https://aac.geon.se
- **Deployment:** GitHub Pages from `gh-pages` branch
- **Build trigger:** Pushes to `docs/` or `mkdocs.yml`
- **Local preview:** `mkdocs serve`

## Key Python Modules

When modifying automation scripts, understand these core modules:

- **generate_book.py:** Loads chapter list from `docs/book_index.json` via `scripts/navigation.py` and orchestrates content generation
- **build_all_orchestrator.py:** High-level coordinator calling individual generators
- **generate_presentation.py:** Creates PowerPoint deck with chapter summaries and speaker notes
- **generate_whitepapers.py:** Exports HTML versions of individual chapters
- **scripts/navigation.py:** Shared utilities for reading `book_index.json` and determining chapter ordering
- **scripts/check_mermaid_diagrams.py:** Validates that committed PNGs match their `.mmd` sources
- **scripts/verify_environment.py:** Ensures toolchain versions match `BOOK_REQUIREMENTS.md`

## Testing Strategy

The project uses pytest for content validation:

- **tests/test_completeness.py:** Ensures all required sections exist in chapters
- **tests/test_consistency.py:** Validates cross-chapter consistency (terminology, references)
- **tests/test_technical_accuracy.py:** Checks technical correctness of code examples and commands
- **tests/test_clarity.py:** Validates readability and clarity metrics

Run tests after manuscript changes to catch quality issues before CI/CD.

## Troubleshooting

### Mermaid CLI Chrome Error
If `mmdc` fails with a Chrome/Chromium error:
```bash
# Set explicit Chrome path
PUPPETEER_EXECUTABLE_PATH=$(which google-chrome) python3 scripts/check_mermaid_diagrams.py
```

### Pandoc Template Missing
```bash
mkdir -p ~/.local/share/pandoc/templates
pandoc --print-default-template=latex > ~/.local/share/pandoc/templates/eisvogel.latex
```

### Environment Version Mismatch
```bash
# Check discrepancies
make verify-env

# Fix Python packages
python3 -m pip install -r requirements.txt

# Fix Node.js packages
npm ci
```

## Additional Resources

- **README.md:** Project overview and contribution workflow
- **AGENTS.md:** Detailed development instructions for AI agents (includes critical timing notes)
- **BOOK_REQUIREMENTS.md:** Canonical version pins and installation instructions
- **docs/STYLE_GUIDE.md:** Complete editorial standards
- **docs/book_structure.md:** Detailed explanation of book organization
- **docs/documentation_workflow.md:** Git-based review workflow
