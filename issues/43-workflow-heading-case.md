Create workflow to enforce uppercase initial letters in docs/ headings

**Description**: We need an automated workflow that scans every `.md` file in `docs/` to ensure that each heading starts with an uppercase letter. This prevents style regressions and keeps headings consistent.

**Current Behavior**: There is no automated validation, so headings starting with lowercase letters slip into the repository until manual review catches them.

**Expected Behavior**: A GitHub Actions workflow should run on pull requests and fail if any heading (lines starting with `#`, `##`, etc.) begins with a lowercase letter.

**Affected Files**:
- `.github/workflows/` (new workflow file)
- `docs/**/*.md`

**Suggested Fix**:
1. Implement a script (e.g., using Python or Bash) that checks heading lines for uppercase initial characters.
2. Add a GitHub Actions workflow invoking the script across all Markdown files in `docs/`.
3. Ensure the workflow runs on pushes and pull requests targeting main branches.
