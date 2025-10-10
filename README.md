# Architecture as Code - Book Project

This repository powers the publication workflow for the book *Architecture as Code*. It contains the complete manuscript alongside automation scripts for generating multi-format releases and distribution assets.

## 📚 About the Book

The book explores how to treat architecture and infrastructure work as software artifacts. Thirty-one chapters are organised into a seven-part narrative with extended appendices that cover the entire lifecycle—from foundational principles and automation practices to organisational change and future outlooks. Each chapter is written with Swedish public-sector and enterprise contexts in mind, combining conceptual guidance, practical templates, and illustrative diagrams.【F:docs/book_structure.md†L1-L139】

### Target Audience
- System and enterprise architects
- DevOps and platform engineers
- Software developers working with cloud-native stacks
- Technology leaders, managers, and programme owners
- Transformation teams driving digitalisation initiatives【F:docs/book_structure.md†L146-L159】

## 📖 Narrative Structure

### Seven Core Parts

| Part | Chapters | Focus |
| --- | --- | --- |
| Part 1 – Foundations | 1-4 | Core concepts, guiding principles, and documentation practices for Architecture as Code |
| Part 2 – Architecture Platform | 5-8 | Automation tooling, cloud environments, containerisation, and microservices foundations |
| Part 3 – Security & Governance | 9-12 | Security automation, policy enforcement, governance models, and compliance obligations |
| Part 4 – Delivery & Operations | 13-16 | Testing strategies, delivery pipelines, cost management, and migration playbooks |
| Part 5 – Organization & Leadership | 17-21 | Organisational change, competency development, AI-assisted collaboration, and digital transformation |
| Part 6 – Experience & Best Practices | 22-24 | Product discovery techniques, interdisciplinary collaboration, and codified lessons learned |
| Part 7 – Future & Wrap-up | 25-27 | Strategic outlook, forward-looking development plans, and closing guidance |【F:docs/book_structure.md†L7-L120】

### Appendices and Extended Material
- **Chapter 28 – Glossary:** Key terminology for Architecture as Code initiatives.
- **Chapter 29 – About the Authors:** Contributor biographies and acknowledgements.
- **Chapter 30 – Appendix A: Code Examples:** Reference implementations and automation templates.
- **Chapter 31 – Technical Structure for Book Production:** Tooling overview for the publishing platform.【F:docs/book_structure.md†L97-L139】

### Archived Drafts
- **Former Chapter 32 – Advantages and Disadvantages of Working in a Code-Oriented Organisation:** Preserved in `docs/archive/32_code_oriented_organisations.md` for optional background reading and future revisions.【F:docs/book_structure.md†L81-L108】【F:docs/archive/README.md†L1-L9】

## 🧭 Repository Layout

```
docs/                     # Manuscript chapters, diagrams, and publishing assets
├── *.md                  # Numbered chapters and appendices (01_introduction.md … 31_technical_architecture.md)
├── archive/              # Retired chapter drafts kept for reference (e.g., former Chapter 32)
├── images/               # Mermaid sources (*.mmd) and generated PNG diagrams
├── build_book.sh         # Local helper for PDF/EPUB/DOCX generation
└── pandoc.yaml           # Shared Pandoc configuration

releases/                 # Git-ignored distribution bundles populated by build scripts
├── book/                 # arkitektur_som_kod.{pdf,epub,docx}
├── presentation/         # arkitektur_som_kod_presentation.pptx and supporting files
├── whitepapers/          # Per-chapter HTML exports
└── website/              # Static site build output

.github/workflows/        # Automation for builds, bot responses, and content validation
└── *.yml                 # Includes unified-build-release.yml, generate-presentations.yml, generate-whitepapers.yml, and specialised bot workflows
```

## 🚀 Build and Automation Workflow

### Prerequisites
- **Pandoc 3.1.9+** and **XeLaTeX** (`texlive-xetex`, `texlive-fonts-recommended`, `texlive-plain-generic`) for PDF output.
- **Mermaid CLI (`@mermaid-js/mermaid-cli`)** for diagram generation.
- **Node.js & npm** for running JavaScript-based helper scripts (no front-end assets are currently included).
- **Python 3.12+** for content automation scripts.【F:docs/build_book.sh†L1-L171】【F:build_release.sh†L1-L59】

### Core Commands
```bash
# Regenerate chapter content from automation scripts
python3 generate_book.py

# Build PDF, EPUB, and DOCX (runs diagram export, copies cover art, and writes to releases/book/)
cd docs && ./build_book.sh

# Create the full distribution bundle (book formats, presentation, whitepapers, website)
./build_release.sh

```

The GitHub Actions pipeline (`.github/workflows/unified-build-release.yml`) mirrors these commands to produce release artifacts whenever book content or automation scripts change.【F:build_release.sh†L1-L212】

### MkDocs Documentation Site

The MkDocs configuration in `mkdocs.yml` publishes every chapter and appendix as a browsable documentation site. Use the standard MkDocs commands to iterate locally:

```bash
mkdocs serve   # start local preview server
mkdocs build   # render static site into the site/ directory
```

Continuous integration enforces successful builds through the `Build MkDocs Site` workflow, which runs whenever `docs/` sources or the MkDocs configuration change.【F:mkdocs.yml†L1-L53】【F:.github/workflows/build-mkdocs.yml†L1-L35】

## 📦 Release Deliverables
- **Book formats:** `arkitektur_som_kod.pdf`, `.epub`, and `.docx` generated via Pandoc with the Eisvogel template.
- **Presentation materials:** `arkitektur_som_kod_presentation.pptx` containing chapter summaries and speaker notes.
- **Whitepapers:** HTML exports for each chapter designed for responsive reading.
- **Static website:** Production-ready site mirroring the manuscript for web distribution.【F:releases/README.md†L1-L48】

## 🔄 CI/CD Workflows

GitHub Actions automate validation and publishing. The primary pipeline (`unified-build-release.yml`) runs the full release script, while companion workflows handle targeted tasks such as presentation generation, whitepaper exports, translation support, and specialised bot responses for architecture, development, design, editorial, QA, and requirements queries.【F:build_release.sh†L1-L212】【F:.github/workflows/architect-bot.yml†L1-L7】

Key workflows include:
- `unified-build-release.yml` – orchestrates book, presentation, whitepaper, and website builds, then prepares distribution assets.
- `generate-presentations.yml` and `generate-whitepapers.yml` – regenerate individual deliverables on demand.
- `content-validation.yml` – checks documentation quality and structural rules before merges.
- `architect-bot.yml`, `developer-bot.yml`, `designer-bot.yml`, `editor-bot.yml`, `qa-bot.yml`, and `requirements-bot.yml` – automation bots that respond to labelled GitHub issues.
- `issue-response.yml` and `translate.yml` – support triage messaging and localisation workflows.【F:.github/workflows/architect-bot.yml†L1-L7】【F:.github/workflows/unified-build-release.yml†L1-L15】

## 📝 Contributing

1. Update the relevant markdown chapter(s) under `docs/` or supporting automation scripts.
2. Regenerate content and verify outputs:
   ```bash
   python3 generate_book.py
   cd docs && ./build_book.sh
   ```
3. If changes affect release collateral, run `./build_release.sh` to confirm presentation, whitepaper, and website builds succeed.
4. Commit changes with clear messages and submit a pull request following repository guidelines.

## 🔍 Link Verification

Use `scripts/verify_links.py` to validate internal and external references across the manuscript and supporting docs. The script emits Markdown, HTML, and JSON reports to aid review and CI integration.【F:scripts/verify_links.py†L1-L160】【F:LINK_VERIFICATION.md†L1-L120】

```bash
python3 scripts/verify_links.py            # default run
python3 scripts/verify_links.py --timeout 20  # custom timeout for slow endpoints
python3 scripts/verify_links.py --output reports/links  # custom output location
```

## 📄 Governance

The Architecture as Code book workshop maintains the repository, coordinates releases, and ensures automation reliability. See `docs/29_about_the_authors.md` for contributor biographies and ownership details.【F:docs/29_about_the_authors.md†L1-L200】

## 🌍 Language

Manuscript chapters and automation output are maintained in English to streamline translation workflows and international collaboration.【F:docs/book_structure.md†L1-L159】【F:AGENTS.md†L115-L123】

