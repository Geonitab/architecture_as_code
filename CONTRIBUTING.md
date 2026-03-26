# Contributing to Architecture as Code

Thank you for your interest in contributing to *Architecture as Code*. This guide covers everything you need to set up a local environment, contribute manuscript content or automation code, and submit a pull request that meets the project's quality standards.

---

## Table of Contents

1. [Development Setup](#development-setup)
2. [Repository Structure](#repository-structure)
3. [Chapter Contribution Workflow](#chapter-contribution-workflow)
4. [Diagram Creation Guidelines](#diagram-creation-guidelines)
5. [Code Style Guidelines](#code-style-guidelines)
6. [Testing Requirements](#testing-requirements)
7. [Building Locally](#building-locally)
8. [Commit Message Conventions](#commit-message-conventions)
9. [Pull Request Process](#pull-request-process)
10. [PR Checklist](#pr-checklist)

---

## Development Setup

### Prerequisites

The following tools must be installed at the exact versions listed. Use `make verify-env` after setup to confirm everything is correctly configured.

| Tool | Required Version | Purpose |
|------|-----------------|---------|
| Python | 3.12.3 | Content generation and validation scripts |
| Node.js | 20.11.1 | Mermaid CLI and helper scripts |
| Pandoc | 3.1.9 | Markdown → PDF / EPUB / DOCX conversion |
| XeLaTeX (TeXLive) | 2023+ | PDF rendering engine |
| Mermaid CLI (`mmdc`) | 10.7.0 | Diagram generation from `.mmd` sources |

### Step-by-step Installation

#### 1. Clone the repository

```bash
git clone <repository-url>
cd architecture_as_code
```

#### 2. Install Python dependencies

```bash
python3 -m pip install -r requirements.txt
```

#### 3. Install Node.js dependencies (Mermaid CLI)

```bash
npm ci
```

> Use `npm ci` rather than `npm install` to guarantee reproducible installs from the locked `package-lock.json`.

#### 4. Install Pandoc

Download Pandoc 3.1.9 from the [official releases page](https://github.com/jgm/pandoc/releases/tag/3.1.9) and follow the platform-specific instructions.

#### 5. Install TeXLive (XeLaTeX)

> **Important:** TeXLive installation takes 8 or more minutes. Do **not** cancel it mid-way.

```bash
# Debian / Ubuntu
sudo apt-get install texlive-xetex texlive-fonts-recommended texlive-latex-extra

# macOS (via Homebrew)
brew install --cask mactex
```

#### 6. Verify your environment

```bash
make verify-env
```

All tool versions should be reported as matching. Resolve any discrepancies before proceeding.

---

## Repository Structure

```
docs/                           # All manuscript content
├── [0-9]*.md                   # Numbered chapters (01_introduction.md, etc.)
├── part_*.md                   # Part introductions (part_a_foundations.md, etc.)
├── appendix_*.md               # Appendices
├── book_index.json             # Canonical chapter ordering (single source of truth)
├── images/                     # Mermaid sources (*.mmd) and generated PNGs
├── build_book.sh               # PDF / EPUB / DOCX build script
└── pandoc.yaml                 # Pandoc configuration

scripts/                        # Validation and automation utilities
├── check_mermaid_diagrams.py   # Verify diagram consistency
├── verify_links.py             # Link validation
├── verify_sources.py           # Source verification
├── verify_environment.py       # Toolchain validation
├── navigation.py               # Shared utilities for chapter ordering
└── translate_repo.py           # Translation helper

templates/                      # Reusable document templates
└── chapter_template.md         # Starting point for new chapters

tests/                          # Pytest test suites
├── test_completeness.py        # Content completeness validation
├── test_consistency.py         # Cross-chapter consistency checks
└── test_technical_accuracy.py  # Technical correctness checks

releases/                       # Git-ignored distribution bundles
```

### Canonical Source of Truth

`docs/book_index.json` defines the complete chapter ordering and metadata. All automation, build scripts, and quality checks consume this file. When adding a new chapter, update this file first.

---

## Chapter Contribution Workflow

### 1. Understand the book structure

Review `docs/book_structure.md` and `docs/book_index.json` to understand which part your contribution belongs to and how existing chapters are organised.

### 2. Use the chapter template

Copy `templates/chapter_template.md` as the starting point for a new chapter:

```bash
cp templates/chapter_template.md docs/NN_your_chapter_title.md
```

Replace `NN` with the chapter number and update the YAML frontmatter.

### 3. Write content following editorial standards

- Use Oxford-standard British English (see [Code Style Guidelines](#code-style-guidelines)).
- Follow the section structure defined in the template (Learning Objectives, Introduction, content sections, Code Examples, Diagrams, Summary, References).
- Keep all prose in Markdown; use fenced code blocks for code samples.
- Target a reading level appropriate for experienced practitioners and enterprise architects.

### 4. Add diagrams

See [Diagram Creation Guidelines](#diagram-creation-guidelines) for the full workflow. Every diagram must have both a `.mmd` source file and a corresponding rendered `.png` committed together.

### 5. Update `docs/book_index.json`

If you are adding a new chapter, add an entry in the correct position within `book_index.json`. Follow the existing schema exactly.

### 6. Regenerate and validate

```bash
# Regenerate manuscript output
python3 generate_book.py

# Build all formats
docs/build_book.sh

# Run content validation
python3 -m pytest tests/ -v

# Check links and sources
python3 scripts/verify_links.py
python3 scripts/verify_sources.py
```

### 7. Open a pull request

Follow the [Pull Request Process](#pull-request-process) and complete the [PR Checklist](#pr-checklist).

---

## Diagram Creation Guidelines

### Overview

Mermaid diagrams are the primary diagramming format. Both the `.mmd` source and the rendered `.png` must be committed together in `docs/images/`.

### Creating a new diagram

1. Create a `.mmd` file in `docs/images/`:

   ```bash
   # Example file: docs/images/diagram_NN_my_topic.mmd
   ```

2. Write valid Mermaid syntax. Include the approved theme block at the top of every file:

   ```mermaid
   %%{init: {'theme':'base', 'themeVariables': {
     'primaryColor': '#2563EB',
     'primaryTextColor': '#F8FAFC',
     'primaryBorderColor': '#1E3A8A',
     'lineColor': '#60A5FA',
     'background': '#F8FAFF'
   }}}%%
   ```

3. Render the PNG:

   ```bash
   npx mmdc -i docs/images/diagram_NN_my_topic.mmd \
            -o docs/images/diagram_NN_my_topic.png \
            -b transparent
   ```

4. Validate consistency across all diagrams:

   ```bash
   python3 scripts/check_mermaid_diagrams.py
   ```

5. Reference the diagram in your chapter Markdown:

   ```markdown
   ![Descriptive alt text](images/diagram_NN_my_topic.png)
   ```

### Gantt chart colour palette

When creating Gantt charts, use the Kvadrat colour palette defined in `docs/STYLE_GUIDE.md`:

- Done tasks: `#1E3A8A` with white text `#F8FAFC`
- Active tasks: `#2563EB` with white text `#F8FAFC`
- Future tasks: `#60A5FA` with dark text `#0F172A`

### Accessibility

All diagram text must meet WCAG AA contrast requirements (minimum 4.5:1 for normal text). Use the Inter font family to match the book's design system.

### Troubleshooting

If `mmdc` fails with a Chrome or Chromium error:

```bash
PUPPETEER_EXECUTABLE_PATH=$(which google-chrome) python3 scripts/check_mermaid_diagrams.py
```

---

## Code Style Guidelines

### British English

All manuscript prose must use Oxford-standard British English. The following table shows required conversions:

| American English | British English (required) |
|-----------------|---------------------------|
| organization | organisation |
| optimize | optimise |
| color | colour |
| center | centre |
| behavior | behaviour |
| digitization | digitisation |
| containerization | containerisation |
| modernization | modernisation |

> Exception: Spellings inside code samples, configuration files, CLI commands, API field names, and quoted third-party material must retain the original spelling. Update surrounding prose and inline comments to British English instead.

### Terminology

- Always write the book and discipline title as **Architecture as Code** — "as" is lower case, "Architecture" and "Code" are capitalised.
- Use "programme" for initiatives (not "program", unless referring to computer software).
- Refer to collective audiences as "teams", "practitioners", or "organisations".
- Apply the serial (Oxford) comma in lists.
- Write dates in ISO format (`2025-10-15`) or long-form British style (`15 October 2025`).

### Tone

Maintain a formal, instructional tone suitable for professional and academic readers. Avoid colloquialisms and region-specific idioms.

### Code examples

- Include language identifiers on every fenced code block (` ```bash `, ` ```yaml `, ` ```python `, etc.).
- Ensure every code example is correct, tested, and runnable where possible.
- Add inline comments to explain non-obvious steps.

### Automation scripts

Python scripts under `scripts/` and root-level generators follow PEP 8. Run `python3 -m pytest tests/test_technical_accuracy.py -v` to verify correctness after changes to automation code.

---

## Testing Requirements

All contributions must pass the full pytest test suite before submission.

### Running the test suite

```bash
# Full suite
python3 -m pytest tests/ -v

# Individual suites
python3 -m pytest tests/test_completeness.py -v
python3 -m pytest tests/test_consistency.py -v
python3 -m pytest tests/test_technical_accuracy.py -v
```

### What the tests cover

| Suite | Checks |
|-------|--------|
| `test_completeness.py` | Ensures all required sections exist in every chapter |
| `test_consistency.py` | Validates cross-chapter terminology and reference consistency |
| `test_technical_accuracy.py` | Verifies code examples and commands are technically correct |

### Additional validation

```bash
# Verify all internal and external links
python3 scripts/verify_links.py

# Verify cited sources (URLs and ISBNs)
python3 scripts/verify_sources.py

# Check document numbering consistency
python3 scripts/check_doc_numbering.py

# Validate diagram consistency
python3 scripts/check_mermaid_diagrams.py
```

---

## Building Locally

### Quick build (content only)

```bash
python3 generate_book.py
```

This completes in under one second and confirms that all chapter files referenced in `book_index.json` are present and parseable.

### Full book build (PDF, EPUB, DOCX)

```bash
docs/build_book.sh
```

This takes approximately 30 seconds and produces output files in `releases/book/`.

### Complete release build

```bash
python3 build_all_orchestrator.py --zip
```

This generates all deliverables: book formats, presentation deck, per-chapter HTML whitepapers, and the documentation website.

### Documentation site preview

```bash
mkdocs serve
```

Open `http://127.0.0.1:8000` in a browser to preview the site locally.

### Combined content and build

```bash
python3 generate_book.py && docs/build_book.sh
```

Run this after any manuscript change to verify the full publishing pipeline succeeds before committing.

---

## Commit Message Conventions

### Format

```
<type>(<scope>): <short summary> (#<issue-number>)

<optional body>
```

- **type**: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, or `ci`
- **scope**: component affected (e.g., `chapter-05`, `diagrams`, `build`, `scripts`, `tests`)
- **summary**: imperative mood, lower case, no trailing full stop, 72 characters or fewer
- **issue reference**: include the GitHub issue number when applicable

### Examples

```
docs(chapter-07): add containerisation security section (#1234)
fix(diagrams): regenerate PNG for diagram_15_pipeline after mmd update (#1250)
test(consistency): add cross-reference validation for Part C chapters (#1260)
chore(deps): update mermaid-cli to 10.7.0 (#1270)
```

### Body guidelines

Use the commit body to explain *why* a change was made rather than *what* changed (the diff shows what). Keep lines at 72 characters or fewer.

---

## Pull Request Process

### Before opening a PR

1. Ensure your branch is up to date with `main`:
   ```bash
   git pull --rebase origin main
   ```
2. Run the full validation suite (see [Testing Requirements](#testing-requirements)).
3. Build the book locally to confirm no compilation errors (see [Building Locally](#building-locally)).
4. Verify the environment matches locked versions:
   ```bash
   make verify-env
   ```

### Opening the PR

- Use a clear, descriptive title following the commit message convention.
- Reference related issues using `Closes #NNNN` or `Relates to #NNNN` in the PR description.
- Describe what changed, why it changed, and how reviewers can verify it.
- For manuscript changes, note which chapters are affected and which part they belong to.

### Review expectations

- Reviews typically focus on editorial quality (British English, terminology, tone) and technical correctness.
- Reviewers may request changes to align with the style guide or to fix broken links, outdated sources, or diagram inconsistencies.
- Address all review comments before requesting re-review.
- All CI checks must pass before a PR can be merged.

### Bot automation

Specialised bots respond to labelled issues. Apply the relevant label to trigger automated feedback:

| Label | Bot |
|-------|-----|
| `architecture` | Architect Bot |
| `dev` | Developer Bot |
| `design` | Designer Bot |
| `documentation` | Editor Bot |
| `qa` | QA Bot |
| `req` | Requirements Bot |

---

## PR Checklist

Complete this checklist before marking a PR as ready for review.

### Content

- [ ] All prose uses Oxford-standard British English spelling and grammar
- [ ] "Architecture as Code" is capitalised correctly throughout
- [ ] Terminology follows `docs/STYLE_GUIDE.md`
- [ ] All new sections include appropriate headings and are logically ordered
- [ ] Code examples have language identifiers and are technically correct
- [ ] References and citations are complete and verified (`python3 scripts/verify_sources.py`)

### Diagrams

- [ ] Every new or modified `.mmd` file has a corresponding regenerated `.png`
- [ ] `python3 scripts/check_mermaid_diagrams.py` passes with no errors
- [ ] Diagram alt text is descriptive and in British English
- [ ] Diagrams use the approved Kvadrat colour palette

### Structure and metadata

- [ ] `docs/book_index.json` is updated if a chapter was added or renamed
- [ ] Chapter YAML frontmatter is complete (title, chapter number, author, date, tags)
- [ ] All internal links resolve (`python3 scripts/verify_links.py`)

### Build and tests

- [ ] `python3 generate_book.py` completes without errors
- [ ] `docs/build_book.sh` completes without errors
- [ ] `python3 -m pytest tests/ -v` passes with no failures
- [ ] `make verify-env` reports all versions as matching

### General

- [ ] Commit messages follow the project conventions
- [ ] No unintended files are staged (binaries, personal configs, `releases/` output)
- [ ] PR description references the relevant GitHub issue(s)
