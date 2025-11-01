# Architecture as Code - Book Project

This repository powers the publication workflow for the book *Architecture as Code*. It contains the complete manuscript alongside automation scripts for generating multi-format releases and distribution assets.

## 📚 About the Book

The book explores how to treat architecture and infrastructure work as software artefacts. More than thirty-five chapters are organised into Parts A–G with Part H delivering extended appendices that cover the entire lifecycle—from foundational principles and automation practices to organisational change and future outlooks. Each chapter is now framed for a global audience, combining conceptual guidance, practical templates, and illustrative diagrams without relying on region-specific assumptions.【F:docs/book_structure.md】【F:docs/part_a_foundations.md】【F:docs/part_h_appendices.md】

### Target Audience
- System and enterprise architects
- DevOps and platform engineers
- Software developers working with cloud-native stacks
- Technology leaders, managers, and programme owners
- Transformation teams driving digitalisation initiatives【F:docs/book_structure.md】

## 📖 Narrative Structure

### Seven Core Parts (Parts A–G)

| Part | Chapters | Focus |
| --- | --- | --- |
| Part A – Foundations | 1-4 | Core concepts, guiding principles, and documentation practices for Architecture as Code |
| Part B – Architecture Platform | 5-7 | Automation tooling, cloud environments, containerisation, and modelling foundations |
| Part C – Security & Governance | 9-12 | Security automation, policy enforcement, governance models, and compliance obligations |
| Part D – Delivery & Operations | 13-16 | Testing strategies, delivery pipelines, cost management, and migration playbooks |
| Part E – Organisation & Leadership | 17-21 | Organisational change, competency development, AI-assisted collaboration, and digital transformation |
| Part F – Experience & Best Practices | 22-24 | Product discovery techniques, interdisciplinary collaboration, and codified lessons learned |
| Part G – Future & Wrap-up | 25-27 | Strategic outlook, forward-looking development plans, and closing guidance |【F:docs/book_structure.md】【F:docs/part_a_foundations.md】

Each lettered part is introduced by a dedicated preface (`docs/part_[a-g]_*.md`) that frames the narrative for the chapters that follow.【F:docs/part_a_foundations.md】

### Appendices and Extended Material
- **Part H – Appendices and Reference:** Brings together reference material, technical enablers, and maturity guidance that support the core narrative.【F:docs/part_h_appendices.md】
- **Chapter 28 – Glossary:** Key terminology for Architecture as Code initiatives.【F:docs/28_glossary.md】
- **Chapter 29 – About the Author:** Profile of Gunnar Nordqvist and the expertise behind the book.【F:docs/29_about_the_authors.md】
- **Appendix A – Code Examples and Technical Implementations:** Reference implementations and automation templates.【F:docs/30_appendix_code_examples.md】
- **Appendix B – Technical Architecture for Book Production:** Tooling overview for the publishing platform.【F:docs/31_technical_architecture.md】
- **Appendix C – Templates and Tools Catalogue:** Curated set of maturity, governance, and automation artefacts, including the Control Mapping Matrix Template.【F:docs/appendix_templates_and_tools.md】
- **Appendix D – FINOS Project Blueprint:** Operational blueprint demonstrating governance as code alignment.【F:docs/32_finos_project_blueprint.md】
- **Appendix E – Architecture as Code Maturity Model:** Adoption guidance and progress measurement for “as code” disciplines.【F:docs/architecture_as_code_maturity_model.md】
- **Control Mapping Matrix Template:** Reusable compliance tooling referenced throughout the appendices.【F:docs/appendix_c_control_mapping_matrix_template.md】

### Archived Drafts
- **Former Chapter 32 – Advantages and Disadvantages of Working in a Code-Oriented Organisation:** Preserved in `docs/archive/32_code_oriented_organisations.md` for optional background reading and future revisions.【F:docs/book_structure.md】【F:docs/archive/README.md】

## 🧭 Repository Layout

```
docs/                     # Manuscript chapters, diagrams, and publishing assets
├── *.md                  # Numbered chapters and appendices (01_introduction.md … 31_technical_architecture.md)
├── archive/              # Retired chapter drafts kept for reference (e.g., former Chapter 32)
├── images/               # Mermaid sources (*.mmd) and generated PNG diagrams
├── build_book.sh         # Local helper for PDF/EPUB/DOCX generation
└── pandoc.yaml           # Shared Pandoc configuration

releases/                 # Git-ignored distribution bundles populated by build scripts
├── book/                 # architecture_as_code.{pdf,epub,docx}
├── presentation/         # architecture_as_code_presentation.pptx and supporting files
├── whitepapers/          # Per-chapter HTML exports
└── website/              # Static site build output

.github/workflows/        # Automation for builds, bot responses, and content validation
└── *.yml                 # Includes unified-build-release.yml, generate-presentations.yml, generate-whitepapers.yml, and specialised bot workflows
```

## 🚀 Build and Automation Workflow

### Prerequisites
- **Pandoc 3.1.9+** and **XeLaTeX** (`texlive-xetex`, `texlive-fonts-recommended`, `texlive-plain-generic`) for PDF output.
- **Mermaid CLI (`@mermaid-js/mermaid-cli`)** for diagram generation (requires a Node.js runtime for installation).
- **Python 3.12+** for content automation scripts.【F:docs/build_book.sh】【F:build_release.sh】

### Core Commands
```bash
# Regenerate chapter content from automation scripts
python3 generate_book.py

# Build PDF, EPUB, and DOCX (runs diagram export, copies cover art, and writes to releases/book/)
docs/build_book.sh

# Orchestrate every deliverable and create an optional release archive
python3 build_all_orchestrator.py --zip

# Create the full distribution bundle (book formats, presentation, whitepapers, website)
./build_release.sh

```

The GitHub Actions pipeline (`.github/workflows/unified-build-release.yml`) mirrors these commands to produce release artifacts whenever book content or automation scripts change.【F:build_release.sh】

### MkDocs Documentation Site

The MkDocs configuration in `mkdocs.yml` publishes every chapter and appendix as a browsable documentation site. Use the standard MkDocs commands to iterate locally:

```bash
mkdocs serve   # start local preview server
mkdocs build   # render static site into the site/ directory
```

Continuous integration enforces successful builds through the `Build MkDocs Site` workflow, which runs whenever `docs/` sources or the MkDocs configuration change.【F:mkdocs.yml】【F:.github/workflows/build-mkdocs.yml】

> **Live URL:** The GitHub Pages deployment uses the custom domain `https://aac.geon.se`, and GitHub automatically redirects the default `https://geonitab.github.io/architecture_as_code/` address to that hostname. Requests to `aac.github.com` will appear blank because that domain is not owned by this project and is therefore outside of the configured Pages setup.【F:CNAME】

## 📦 Release Deliverables
- **Book formats:** `architecture_as_code.pdf`, `.epub`, and `.docx` generated via Pandoc with the Eisvogel template.
- **Presentation materials:** `architecture_as_code_presentation.pptx` containing chapter summaries and speaker notes.
- **Whitepapers:** HTML exports for each chapter designed for responsive reading.
- **Static website:** Production-ready site mirroring the manuscript for web distribution.【F:releases/README.md】

## 🔄 CI/CD Workflows

GitHub Actions automate validation and publishing. The primary pipeline (`unified-build-release.yml`) runs the full release script, while companion workflows handle targeted tasks such as presentation generation, whitepaper exports, translation support, and specialised bot responses for architecture, development, design, editorial, QA, and requirements queries.【F:build_release.sh】【F:.github/workflows/architect-bot.yml】

Key workflows include:
- `unified-build-release.yml` – orchestrates book, presentation, whitepaper, and website builds, then prepares distribution assets.
- `generate-presentations.yml` and `generate-whitepapers.yml` – regenerate individual deliverables on demand.
- `content-validation.yml` – checks documentation quality and structural rules before merges.
- `architect-bot.yml`, `developer-bot.yml`, `designer-bot.yml`, `editor-bot.yml`, `qa-bot.yml`, and `requirements-bot.yml` – automation bots that respond to labelled GitHub issues.
- `issue-response.yml` and `translate.yml` – support triage messaging and localisation workflows.【F:.github/workflows/architect-bot.yml】【F:.github/workflows/unified-build-release.yml】

## 📝 Contributing

1. Review `docs/STYLE_GUIDE.md` alongside the unified Git workflow in
   `docs/documentation_workflow.md` to confirm spelling, tone, and review expectations.
2. Update the relevant markdown chapter(s) under `docs/`, ADR templates, or supporting
   automation scripts in line with the shared workflow.
3. Regenerate content and verify outputs:
   ```bash
   python3 generate_book.py
   docs/build_book.sh
   ```
4. If changes affect release collateral, run `./build_release.sh` to confirm presentation, whitepaper, and website builds succeed.
5. Commit changes with clear messages and submit a pull request following the shared
   Git-based review workflow so automation validates heading and link conventions.

## 🔍 Link Verification

Use `scripts/verify_links.py` to validate internal and external references across the manuscript and supporting docs. The script emits Markdown, HTML, and JSON reports to aid review and CI integration.【F:scripts/verify_links.py】【F:LINK_VERIFICATION.md】

```bash
python3 scripts/verify_links.py            # default run
python3 scripts/verify_links.py --timeout 20  # custom timeout for slow endpoints
python3 scripts/verify_links.py --output reports/links  # custom output location
```

## 📚 Source Verification

Use `scripts/verify_sources.py` to verify all cited sources throughout the manuscript. The script checks URL accessibility, validates ISBN formats, and identifies sources requiring manual verification. It generates comprehensive Markdown and JSON reports listing verified, broken, and manually-verifiable sources.【F:scripts/verify_sources.py】

```bash
python3 scripts/verify_sources.py            # default run
python3 scripts/verify_sources.py --timeout 15  # custom timeout for slow endpoints
python3 scripts/verify_sources.py --output reports/sources  # custom output location
```

## 📄 Governance

The Architecture as Code book workshop maintains the repository, coordinates releases, and ensures automation reliability. See `docs/29_about_the_authors.md` for author biography and book context.【F:docs/29_about_the_authors.md】

## 🌍 Language

Manuscript chapters and automation output are maintained in English to streamline translation workflows and international collaboration.【F:docs/book_structure.md】【F:AGENTS.md】
