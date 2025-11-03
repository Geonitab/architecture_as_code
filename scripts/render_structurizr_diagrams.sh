#!/usr/bin/env bash
set -euo pipefail

WORKSPACE=${1:-docs/examples/structurizr/aac_reference_workspace.dsl}
OUTPUT_DIR=${STRUCTURIZR_OUTPUT_DIR:-build/structurizr}
FORMATS=${STRUCTURIZR_FORMATS:-png,structurizr}
MANIFEST=${STRUCTURIZR_MANIFEST:-docs/examples/structurizr/aac_reference_workspace.manifest.json}
CLI_IMAGE=${STRUCTURIZR_CLI_IMAGE:-structurizr/cli:2024.03.01}

if command -v docker >/dev/null 2>&1; then
  RUNTIME="docker"
elif command -v podman >/dev/null 2>&1; then
  RUNTIME="podman"
else
  cat >&2 <<'MSG'
Neither Docker nor Podman is available on this machine.
Install one of the container runtimes or run the Structurizr CLI manually:
  java -jar structurizr-cli.jar validate -w <workspace>
  java -jar structurizr-cli.jar export -w <workspace> -f png,structurizr -o <output>
MSG
  exit 3
fi

mkdir -p "${OUTPUT_DIR}"

${RUNTIME} run --rm -v "$(pwd)":/workspace "${CLI_IMAGE}" \
  validate -w "/workspace/${WORKSPACE}"

${RUNTIME} run --rm -v "$(pwd)":/workspace "${CLI_IMAGE}" \
  export -w "/workspace/${WORKSPACE}" -f "${FORMATS}" -o "/workspace/${OUTPUT_DIR}"

if [[ "${STRUCTURIZR_SKIP_MANIFEST_UPDATE:-0}" != "1" ]]; then
  python3 scripts/update_structurizr_manifest.py \
    --workspace "${WORKSPACE}" \
    --manifest "${MANIFEST}" \
    --formats "${FORMATS}" \
    --output-dir "${OUTPUT_DIR}"
  echo "Structurizr diagrams exported to ${OUTPUT_DIR} and manifest updated at ${MANIFEST}."
else
  echo "Structurizr diagrams exported to ${OUTPUT_DIR}. Manifest update skipped as requested."
fi
