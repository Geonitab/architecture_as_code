#!/usr/bin/env bash
# new_adr.sh - Architecture Decision Record template generator
#
# Usage: scripts/new_adr.sh "Title of the Architecture Decision"
#
# Calculates the next available ADR number, creates a new ADR file from
# template in docs/examples/structurizr/adrs/, and pre-populates metadata
# following the project's established ADR format.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
ADR_DIR="${REPO_ROOT}/docs/examples/structurizr/adrs"

# ── Argument validation ────────────────────────────────────────────────────────

if [[ $# -lt 1 || -z "${1// /}" ]]; then
    echo "Error: an ADR title is required." >&2
    echo "Usage: $(basename "$0") \"Title of the Architecture Decision\"" >&2
    exit 1
fi

ADR_TITLE="$1"

# ── Determine next ADR number ──────────────────────────────────────────────────

# Find the highest existing ADR number across all ADR-NNNN-*.md files.
HIGHEST=0
if compgen -G "${ADR_DIR}/ADR-*.md" > /dev/null 2>&1; then
    while IFS= read -r filepath; do
        filename="$(basename "${filepath}")"
        # Extract the four-digit number immediately after "ADR-"
        if [[ "${filename}" =~ ^ADR-([0-9]{4}) ]]; then
            num="${BASH_REMATCH[1]}"
            # Remove leading zeros for arithmetic comparison
            num_stripped="${num#"${num%%[!0]*}"}"
            num_stripped="${num_stripped:-0}"
            if (( num_stripped > HIGHEST )); then
                HIGHEST="${num_stripped}"
            fi
        fi
    done < <(find "${ADR_DIR}" -maxdepth 1 -name "ADR-*.md" | sort)
fi

NEXT_NUM=$(( HIGHEST + 1 ))
ADR_NUMBER=$(printf "%04d" "${NEXT_NUM}")

# ── Derive slug from title ─────────────────────────────────────────────────────

# Convert title to lowercase, replace spaces and non-alphanumeric chars with hyphens,
# collapse consecutive hyphens, strip leading/trailing hyphens.
ADR_SLUG="$(echo "${ADR_TITLE}" \
    | tr '[:upper:]' '[:lower:]' \
    | sed 's/[^a-z0-9]/-/g' \
    | sed 's/-\{2,\}/-/g' \
    | sed 's/^-//;s/-$//')"

ADR_ID="ADR-${ADR_NUMBER}"
ADR_FILENAME="${ADR_ID}-${ADR_SLUG}.md"
ADR_PATH="${ADR_DIR}/${ADR_FILENAME}"
TODAY="$(date +%Y-%m-%d)"

# ── Guard against accidental overwrite ────────────────────────────────────────

if [[ -f "${ADR_PATH}" ]]; then
    echo "Error: file already exists: ${ADR_PATH}" >&2
    exit 1
fi

# ── Write ADR template ─────────────────────────────────────────────────────────

cat > "${ADR_PATH}" << EOF
# ${ADR_ID}: ${ADR_TITLE}

## Status
Proposed

## Date
${TODAY}

## Context
<!-- Describe the forces at play and the problem that prompted this decision.
     Explain the technical and organisational constraints that are relevant. -->

## Decision
<!-- State the decision that was made. Use active voice: "We will…" -->

## Consequences
<!-- List the outcomes of the decision — both positive and negative.
     Include any follow-on actions required or trade-offs accepted. -->

## Alternatives Considered
<!-- Briefly describe other options that were evaluated and why they were not chosen. -->
EOF

echo "Created ${ADR_PATH}"
echo ""
echo "  ADR number : ${ADR_ID}"
echo "  Title      : ${ADR_TITLE}"
echo "  Status     : Proposed"
echo "  Date       : ${TODAY}"
echo ""
echo "Next steps:"
echo "  1. Fill in the Context, Decision, Consequences, and Alternatives sections."
echo "  2. Update the Status field as the ADR progresses (Proposed → Accepted)."
echo "  3. Run 'python3 scripts/validate_adrs.py' once full YAML front matter is added."
