#!/usr/bin/env bash
set -euo pipefail

# Inputs via environment:
# - OPENAI_API_KEY (required)
# - SOURCE_TEXT     (required) the pasted free-form text
# - DRY_RUN         (optional) "true"/"false" (default: "true")
# - GITHUB_TOKEN    (provided by Actions) for gh cli
# - GITHUB_REPOSITORY (owner/repo), provided by Actions

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROMPT_FILE="${SCRIPT_DIR}/prompt.txt"

# Sanity checks
: "${OPENAI_API_KEY:?OPENAI_API_KEY is required}"
: "${SOURCE_TEXT:?SOURCE_TEXT is required}"

DRY_RUN="${DRY_RUN:-true}"

# Ensure tools
command -v jq >/dev/null || { echo "jq not found"; exit 1; }
command -v gh >/dev/null || { echo "gh CLI not found"; exit 1; }

# Ensure gh uses the token from Actions
export GH_TOKEN="${GH_TOKEN:-${GITHUB_TOKEN:-}}"

# 1) Save inputs
printf '%s' "$SOURCE_TEXT" > /tmp/source.txt

# 2) Verify prompt indentation (10 leading spaces on non-empty lines)
if ! awk 'NF && $0 !~ /^          /{exit 1}' "$PROMPT_FILE"; then
  echo "prompt.txt does not have the required 10-space indentation on all non-empty lines."
  exit 1
fi

# 3) Convert prompt to a safe JSON string
INSTRUCT="$(jq -Rs '.' "$PROMPT_FILE")"
CONTENT="$(cat /tmp/source.txt)"

# 4) Build OpenAI request safely
REQUEST="$(jq -n --arg instruct "$INSTRUCT" --arg content "$CONTENT" '{
  model: "gpt-4o-mini",
  input: [
    {role:"system", content:"Return JSON only. No explanations."},
    {role:"user", content: ($instruct | fromjson)},
    {role:"user", content: ("TEXT:\n" + $content)}
  ]
}')"

echo "::group::OpenAI API Request"
echo "$REQUEST" | jq .
echo "::endgroup::"

# 5) Call OpenAI with status capture
HTTP_CODE_FILE="$(mktemp)"
curl -sS https://api.openai.com/v1/responses \
  -H "Authorization: Bearer ${OPENAI_API_KEY}" \
  -H "Content-Type: application/json" \
  -o /tmp/response.json \
  -w "%{http_code}" \
  -d "$REQUEST" > "$HTTP_CODE_FILE" || true

STATUS="$(cat "$HTTP_CODE_FILE" || echo "000")"
echo "::group::OpenAI API Response"
cat /tmp/response.json || true
echo
echo "HTTP status: $STATUS"
echo "::endgroup::"

if [[ "$STATUS" != "200" ]]; then
  echo "Non-200 from OpenAI: $STATUS"
  if jq -e . >/dev/null 2>&1 < /tmp/response.json; then jq . /tmp/response.json; else cat /tmp/response.json; fi
  exit 1
fi

jq -e . >/dev/null < /tmp/response.json || { echo "Response not valid JSON"; exit 1; }
if jq -e '.error' >/dev/null < /tmp/response.json; then
  echo "OpenAI returned an error object:"; jq .error /tmp/response.json; exit 1
fi

RAW="$(
  jq -r '
    .output_text //
    (.output[]?.content[]? | select(.text != null) | .text) //
    (.content[]? | select(.text != null) | .text) //
    empty
  ' /tmp/response.json
)"

if [[ -z "$RAW" ]]; then
  echo "Model returned empty output_text/content."
  jq . /tmp/response.json || true
  exit 1
fi

# 6) Validate model-produced JSON
echo "$RAW" | jq -e '.issues and (.issues|type=="array")' > /tmp/issues.json
COUNT="$(jq '.issues|length' /tmp/issues.json)"
echo "Proposed issues: $COUNT"

# 7) Expose count to GitHub Actions (if running inside GA)
if [[ -n "${GITHUB_OUTPUT:-}" ]]; then
  echo "count=$COUNT" >> "$GITHUB_OUTPUT"
fi

# 8) Dry run preview
echo "::group::Preview"
jq -r '
  .issues
  | to_entries[]
  | "### \(.key + 1). \(.value.title_british)\n"
    + (.value.body_british // "") + "\n"
    + "Labels: " + ((.value.labels // []) | join(", ")) + "\n"
    + "Assignees: " + ((.value.assignees // []) | join(", ")) + "\n"
' /tmp/issues.json
echo "::endgroup::"

if [[ "${DRY_RUN,,}" == "true" ]]; then
  echo "Dry run enabled — no issues will be created."
  exit 0
fi

# 9) Create issues with gh, skipping duplicates by title
echo "Fetching existing open issues for duplicate detection…"
mapfile -t EXISTING_TITLES < <(gh issue list --state open --limit 200 --json title --jq '.[].title | ascii_downcase')

created=0
while IFS= read -r row; do
  title="$(jq -r '.title_british' <<<"$row")"
  body="$(jq -r '.body_british // ""' <<<"$row")"
  labels_json="$(jq -c '.labels // []' <<<"$row")"
  assignees_json="$(jq -c '.assignees // []' <<<"$row")"

  [[ -z "$title" || "$title" == "null" ]] && continue

  # duplicate check (case-insensitive)
  lower="$(printf '%s' "$title" | awk '{print tolower($0)}')"
  if printf '%s\n' "${EXISTING_TITLES[@]}" | grep -qx -- "$lower"; then
    echo "Skip duplicate: $title"
    continue
  fi

  # Build gh args
  args=(issue create --title "$title" --body "$body")
  # labels
  for lbl in $(jq -r '.[]' <<<"$labels_json"); do
    args+=(--label "$lbl")
  done
  # assignees
  for a in $(jq -r '.[]' <<<"$assignees_json"); do
    args+=(--assignee "$a")
  done

  # Create
  gh "${args[@]}"
  created=$((created+1))
done < <(jq -c '.issues[]' /tmp/issues.json)

echo "Created: $created issue(s)."