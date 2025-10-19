#!/usr/bin/env bash
# Shared helper for invoking the OpenAI Responses API from GitHub Actions workflows.
# Expects PROMPT and OPENAI_API_KEY to be present in the environment.
set -euo pipefail

FORMAT="${1:-text}"
PROMPT="${PROMPT:-}"
API_KEY="${OPENAI_API_KEY:-}"

if [[ -z "$PROMPT" ]]; then
  echo "PROMPT environment variable is required." >&2
  exit 1
fi

if [[ -z "$API_KEY" ]]; then
  echo "OPENAI_API_KEY environment variable is required." >&2
  exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
  sudo apt-get update >/dev/null
  sudo apt-get install -y jq >/dev/null
fi

REQUEST=$(jq -n --arg prompt "$PROMPT" '{
  model: "gpt-4o-mini",
  input: [{role: "user", content: $prompt}]
}')

RAW=$(curl -sS https://api.openai.com/v1/responses \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d "$REQUEST")

if [[ "${FORMAT}" == "raw" ]]; then
  printf '%s' "$RAW"
  exit 0
fi

TEXT=$(echo "$RAW" | jq -r '.output_text // .output[0].content[0].text // empty')

if [[ -z "$TEXT" ]]; then
  ERROR_MESSAGE=$(echo "$RAW" | jq -r '.error.message // empty')
  if [[ -n "$ERROR_MESSAGE" ]]; then
    echo "OpenAI error: ${ERROR_MESSAGE}" >&2
  else
    echo "OpenAI response did not contain any text." >&2
  fi
  exit 2
fi

case "$FORMAT" in
  text)
    printf '%s' "$TEXT"
    ;;
  json)
    JSON_BODY=$(printf '%s' "$TEXT" | awk 'BEGIN{capture=0}{if(index($0,"{"))capture=1;if(capture)print}')
    if [[ -z "$JSON_BODY" ]]; then
      echo "OpenAI response did not include a JSON payload." >&2
      exit 3
    fi
    echo "$JSON_BODY" | jq -c .
    ;;
  *)
    echo "Unsupported format: ${FORMAT}. Use text, json, or raw." >&2
    exit 4
    ;;
esac
