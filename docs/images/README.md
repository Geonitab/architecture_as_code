# Diagram Asset Guidelines

- Store Mermaid source diagrams as `.mmd` files in this directory.
- **Both `.mmd` source files and rendered `.png` files must be committed** to version
  control. This ensures offline readers and document reviewers have stable diagrams
  without needing to regenerate assets locally.
- PNG files are marked as binary in `.gitattributes` to keep diffs readable.
- If you modify a `.mmd` file, regenerate its PNG before committing:
  ```bash
  PUPPETEER_EXECUTABLE_PATH=$(which google-chrome) \
    npx mmdc -i docs/images/<diagram>.mmd -o docs/images/<diagram>.png
  ```
- CI enforces that every committed PNG matches its source via
  `scripts/check_mermaid_diagrams.py`.
