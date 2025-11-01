# Architecture as Code - Book Project

This repository powers the publication workflow for the book *Architecture as Code*. It contains the complete manuscript alongside automation scripts for generating multi-format releases and distribution assets.

## 📚 About the Book

The book explores how to treat architecture and infrastructure work as software artefacts. Thirty-eight chapters, appendices, and structured templates are organised into Parts A–G with Part H delivering extended appendices that cover the entire lifecycle—from foundational principles and automation practices to organisational change and future outlooks. Each chapter is now framed for a global audience, combining conceptual guidance, practical templates, and illustrative diagrams without relying on region-specific assumptions.【F:docs/book_structure.md】【F:docs/part_a_foundations.md】【F:docs/part_h_appendices.md】

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
| Part A – Foundations | 1–4 | Core concepts, guiding principles, and documentation practices for Architecture as Code |
| Part B – Architecture Platform | 5–8 | Automation tooling, Structurizr-based modelling, containerisation, and microservices foundations |
| Part C – Security & Governance | 9–12 (including 9B and 9C) | Security automation, policy enforcement, governance models, and compliance obligations |
| Part D – Delivery & Operations | 13–16 (including 15A and 15B) | Testing strategies, delivery pipelines, continuous assurance, cost management, and migration playbooks |
| Part E – Organisation & Leadership | 17–21 | Organisational change, competency development, AI-assisted collaboration, and digital transformation |
| Part F – Experience & Best Practices | 22–24 | Product discovery techniques, interdisciplinary collaboration, and codified lessons learned |
| Part G – Future & Wrap-up | 25–27 (including 26A and 26B) | Strategic outlook, adoption prerequisites, anti-pattern avoidance, and closing guidance |【F:docs/book_structure.md】【F:docs/part_a_foundations.md】

Each lettered part is introduced by a dedicated preface—`docs/part_a_foundations.md`, `docs/part_b_platform.md`, `docs/part_c_security.md`, `docs/part_d_delivery.md`, `docs/part_e_leadership.md`, `docs/part_f_practices.md`, and `docs/part_g_future.md`—that frames the narrative for the chapters that follow.【F:docs/part_a_foundations.md】【F:docs/part_b_platform.md】【F:docs/part_c_security.md】【F:docs/part_d_delivery.md】【F:docs/part_e_leadership.md】【F:docs/part_f_practices.md】【F:docs/part_g_future.md】

Lettered companion chapters (9B, 9C, 15A, 15B, 26A, and 26B) provide deeper dives into security, assurance, and adoption topics without breaking the overall numbering scheme.【F:docs/book_structure.md】

### Appendices and Extended Material
- **Part H – Appendices and Reference:** Brings together reference material, technical enablers, and maturity guidance that support the core narrative.
- **Glossary:** Key terminology for Architecture as Code initiatives.
- **About the Author:** Profile of Gunnar Nordqvist and the expertise behind the book.
- **Chapter 30 – Appendix A: Code Examples:** Reference implementations and automation templates.
- **Appendix B – Technical Architecture for Book Production (Chapter 31):** Tooling overview for the publishing platform.
- **Appendix C – FINOS Project Blueprint (Chapter 32):** Demonstration of governance-as-code alignment.
- **Supplement – Architecture as Code Maturity Model:** Progressive adoption guidance and assessment structure.
- **Supplement – Maturity Radar Tool:** Visual companion for the maturity model.
- **Chapter 33 – References and Sources:** Comprehensive bibliography and citations.
- **Chapter 34 – Control Mapping Matrix Template:** Compliance acceleration template that complements the maturity guidance.【F:docs/book_structure.md】【F:docs/part_h_appendices.md】【F:docs/34_control_mapping_matrix_template.md】

### Archived Drafts
- Retired drafts, translations, and case studies are catalogued in `docs/archive/README.md`, which records when and why each manuscript left the live build. Current entries cover Swedish-language drafts of Chapters 6, 8, 20, 25, and 26, along with guidance for handling the former Chapter 32 on code-oriented organisations.【F:docs/book_structure.md】【F:docs/archive/README.md】

## 🧭 Repository Layout

```
docs/                     # Manuscript chapters, diagrams, and publishing assets
├── *.md                  # Numbered chapters and appendices (01_introduction.md … 34_control_mapping_matrix_template.md)
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

The canonical ordering of these chapters is published in `docs/book_index.json`, enabling automation and quality checks to consume a single, machine-readable source of truth.【F:docs/book_index.json】

## 🖼️ Diagram Workflow

Mermaid diagrams live in `docs/images/` with the source (`*.mmd`) and the rendered PNG committed together. Keeping both artefacts in version control ensures offline readers, document reviewers, and downstream automations can rely on stable diagrams without regenerating assets. The PNG files are marked as binary in `.gitattributes` so pull requests stay tidy even when large diagrams change.【F:.gitattributes†L1-L2】

When you adjust or add diagrams:

- Run `npm ci` once per workspace to install the locked Mermaid CLI toolchain.
- Execute `python3 scripts/check_mermaid_diagrams.py` to confirm every committed PNG still matches its Mermaid source. The helper renders each diagram using the same parameters as the book build and fails fast if an image is missing or outdated.【F:scripts/check_mermaid_diagrams.py†L1-L138】
- If the check reports that Chromium cannot start, install the headless browser dependencies listed in the error output or point `PUPPETEER_EXECUTABLE_PATH` to an existing Chrome binary before rerunning the command.【F:scripts/check_mermaid_diagrams.py†L94-L138】

Continuous integration reinforces this policy via the **Verify Mermaid Diagrams** workflow, which installs the toolchain and runs the same check on every push or pull request that touches the diagram set.【F:.github/workflows/verify-mermaid-diagrams.yml†L1-L53】

## 🚀 Build and Automation Workflow

### Prerequisites
Canonical version pins live in the YAML front matter of `BOOK_REQUIREMENTS.md`. Install the accompanying manifests before running any build scripts:

- **Python 3.12.3** with the pip packages defined in `requirements.txt` (install via `python -m pip install -r requirements.txt`).
- **Pandoc 3.1.9** and **XeLaTeX** (`texlive-xetex`, `texlive-fonts-recommended`, `texlive-plain-generic`).
- **Node.js 20.11.1** with the pinned Mermaid CLI (`npm ci` installs `@mermaid-js/mermaid-cli@10.7.0` from `package-lock.json`).

Use `make verify-env` to confirm the local toolchain matches the locked versions and manifests. The check ensures `BOOK_REQUIREMENTS.md`, `requirements.txt`, `package.json`, and `package-lock.json` remain in sync.【F:BOOK_REQUIREMENTS.md†L1-L16】【F:requirements.txt†L1-L5】【F:package.json†L1-L12】【F:scripts/verify_environment.py†L1-L204】

### Core Commands
```bash
# Regenerate chapter content from automation scripts
python3 generate_book.py

# Build PDF, EPUB, and DOCX (runs diagram export, copies cover art, and writes to releases/book/)
docs/build_book.sh

# Generate the PowerPoint deck (writes to releases/presentation/ by default with --release)
python3 generate_presentation.py --release --create-pptx

# Orchestrate every deliverable and create an optional release archive
python3 build_all_orchestrator.py --zip

# Create the full distribution bundle (book formats, presentation, whitepapers, website)
./build_release.sh

```

> **Where is the build script?** The helper referenced above lives at `docs/build_book.sh`, is checked into source control, and ships with executable permissions so it can be invoked directly from the repository root (`./docs/build_book.sh`). The high-level orchestrator (`build_all_orchestrator.py`) calls the same entry point internally, keeping the README instructions and the automated workflow in lockstep.

The GitHub Actions pipeline (`.github/workflows/unified-build-release.yml`) mirrors these commands to produce release artifacts whenever book content or automation scripts change.【F:build_release.sh】

### MkDocs Documentation Site

The MkDocs configuration in `mkdocs.yml` publishes every chapter and appendix as a browsable documentation site. Use the standard MkDocs commands to iterate locally:

```bash
mkdocs serve   # start local preview server
mkdocs build   # render static site into the site/ directory
```

Continuous integration enforces successful builds through the `Build MkDocs Site` workflow, which runs whenever `docs/` sources or the MkDocs configuration change.【F:mkdocs.yml】【F:.github/workflows/build-mkdocs.yml】

## 🌐 Website

- **Public URL:** The documentation site is published at [https://aac.geon.se](https://aac.geon.se), matching the custom domain stored in the repository `CNAME` file to keep canonical links stable.【F:CNAME】【F:mkdocs.yml】
- **Deployment pipeline:** The `Build MkDocs Site` GitHub Actions workflow builds the site with `mkdocs build`, stages the generated artefacts (including `CNAME` and `.nojekyll`), and force-pushes the result to the `gh-pages` branch for GitHub Pages to serve.【F:.github/workflows/build-mkdocs.yml】
- **Local validation:** Run `mkdocs serve` for a preview or `mkdocs build` to recreate the static site locally before triggering a deployment, ensuring the hosted content mirrors the book manuscript.【F:mkdocs.yml】

## 📦 Release Deliverables
- **Book formats:** `architecture_as_code.pdf`, `.epub`, and `.docx` generated via Pandoc with the Eisvogel template.
- **Presentation materials:** `architecture_as_code_presentation.pptx` containing chapter summaries and speaker notes. The Python automation is the canonical source for the slide deck, and the retired Prezi prototype has been archived to avoid divergence.
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

## ✍️ Editorial Style

- Use the official casing **Architecture as Code** in all narrative copy, diagrams, navigation labels, and commit messages unless quoting external material with different styling.
- Follow the full editorial rules in `docs/STYLE_GUIDE.md`, including British English spelling, tone guidance, and terminology guardrails.

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

The Architecture as Code book workshop maintains the repository, coordinates releases, and ensures automation reliability. See `docs/about_the_author.md` for author biography and book context.【F:docs/about_the_author.md】

## 🌍 Language

Manuscript chapters and automation output are maintained in English to streamline translation workflows and international collaboration.【F:docs/book_structure.md】【F:AGENTS.md】
