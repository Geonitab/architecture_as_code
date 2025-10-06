# Architecture as Code – Repository Overview

This repository is the working space for the "Architecture as Code" publishing initiative. It combines long-form book content, presentation and whitepaper pipelines, and a React + TypeScript dashboard that showcases the material. The goal is to treat all deliverables as code: every artifact is generated, validated, and released automatically from this single source of truth.

## 📦 Core Deliverables
- **Book** – 27 chapter manuscript with diagrams and supporting assets located in `docs/`.
- **Presentation Pack** – Speaker-ready slide decks produced per release in `releases/presentation/` and `templates/`.
- **Whitepapers** – Chapter-specific HTML whitepapers rendered through the automation workflows in `releases/whitepapers/`.
- **Static Website** – React-powered documentation and dashboard bundled from the `src/` application and the `public/` assets directory.

## 🗂️ Repository Structure
| Path | Purpose |
| --- | --- |
| `docs/` | Markdown chapters, mermaid diagrams, and the LaTeX-friendly build scripts for the book PDF. |
| `releases/` | Canonical outputs for book, presentation, whitepaper, and website bundles grouped by release cycle. |
| `templates/` | Hand-crafted slide and document templates that seed new release assets. |
| `scripts/` | Python utilities for link validation, asset checks, and release automation. |
| `src/` | React + TypeScript dashboard built with Vite, Tailwind CSS, and shadcn/ui components. |
| `public/` | Static assets consumed by the dashboard (favicons, manifest, imagery). |
| `exports/` | Intermediate build artifacts shared across release steps. |
| `tests/` | Automated checks for documentation structure and dashboard behaviour. |
| Root guides (`*.md`) | Project playbooks, retrospectives, and status reports for content, localization, branding, and automation. |

## ⚙️ Automation & Tooling
- **GitHub Actions** (`.github/workflows/`) orchestrate unified build-and-release jobs, standalone whitepaper generation, presentation builds, and content validation.
- **Node.js Tooling** uses Vite for bundling, Tailwind for styling, and ESLint/TypeScript for quality gates defined in `package.json`, `tsconfig*.json`, and `eslint.config.js`.
- **Python Scripts** automate documentation health checks such as `scripts/verify_links.py` with configurable outputs.
- **Shell Utilities** like `build_release.sh` and `docs/build_book.sh` provide reproducible local builds mirroring CI behaviour.

## 🚀 Getting Started
### Install Dependencies
```bash
# Install JavaScript dependencies (React dashboard & tooling)
npm install --legacy-peer-deps

# Optional: global tools for diagram and document generation
npm install -g @mermaid-js/mermaid-cli
```

### Build the Manuscript
```bash
python3 generate_book.py      # Refresh markdown sources from templates
cd docs && ./build_book.sh    # Render PDF with diagrams via Pandoc + LaTeX
```

### Run the Dashboard
```bash
npm run dev    # Start Vite dev server
npm run build  # Create production bundle in dist/
```

### End-to-End Release
```bash
./build_release.sh            # Generate book, presentations, whitepapers, and web bundle
```

## 🧭 Documentation Map
The root directory holds curated guidance that documents the state of the project:
- `ANALYSIS_SUMMARY.md`, `CODEBASE_ANALYSIS.md`, and `REMAINING_WORK.md` outline technical findings and TODOs.
- `BRAND_GUIDELINES.md`, `VISUAL_ELEMENTS_GUIDE.md`, and `DESIGN_SYSTEM.md` define visual identity and UI standards.
- `TRANSLATION_PROJECT.md`, `ENGLISH_STATUS.md`, and related files track localization and editorial progress.
- `DOCS_PROTECTION.md`, `TEST_WORKFLOW.md`, and `CICD_SETUP.md` cover process governance and automation.

## 🤝 Contributing
1. Update the relevant markdown chapters or dashboard components.
2. Run local validation (`python3 scripts/verify_links.py` and/or project build commands above).
3. Commit changes with clear messages and open a pull request that references the release checklist in `WORKFLOWS.md`.

## 📄 License
The "Architecture as Code" materials are maintained and published by Geonit AB. Please consult project leads for licensing details prior to distribution.
