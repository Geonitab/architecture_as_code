# Security policy

## Reporting a problem

Report a security problem privately, not in a public issue: use the repository's
**Security** tab ("Report a vulnerability") or write to the repository owner
named in `.github/CODEOWNERS`.

The repository holds a manuscript and the automation that builds it; it holds no
production service and no personal data. Credentials, if one is ever committed
by mistake, are treated as exposed: revoke them first, then remove them from the
tree.

## What the repository does to stay safe

- `secret-scan.yml` runs `scripts/scan_secrets.py` on every pull request and
  every push to `main`.
- Dependabot proposes updates to pinned dependencies and to GitHub Actions
  (`.github/dependabot.yml`).
- Workflows that only read the repository declare `permissions: contents: read`.
- Every change reaches `main` through a pull request; `.github/CODEOWNERS` names
  the owner who reviews it.
