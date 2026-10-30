#!/usr/bin/env bash
set -euo pipefail

# Renders the reference Structurizr workspace with the consolidated structurizr/structurizr
# distribution (https://docs.structurizr.com/binaries). The standalone structurizr/cli image
# that earlier versions of this script used has reached end of life.
WORKSPACE=${1:-docs/examples/structurizr/aac_reference_workspace.dsl}
OUTPUT_DIR=${STRUCTURIZR_OUTPUT_DIR:-build/structurizr}
# Formats accepted by `structurizr export`: plantuml, plantuml/c4plantuml, mermaid,
# websequencediagrams, static, json, theme (png/svg additionally need the -playwright image).
FORMATS=${STRUCTURIZR_FORMATS:-json,plantuml}
MANIFEST=${STRUCTURIZR_MANIFEST:-docs/examples/structurizr/aac_reference_workspace.manifest.json}
# The -noble tag is the non-hardened variant recommended for CI environments.
STRUCTURIZR_IMAGE=${STRUCTURIZR_IMAGE:-${STRUCTURIZR_CLI_IMAGE:-structurizr/structurizr:2026.09.19-noble}}

if command -v docker >/dev/null 2>&1; then
  RUNTIME="docker"
elif command -v podman >/dev/null 2>&1; then
  RUNTIME="podman"
else
  cat >&2 <<'MSG'
Neither Docker nor Podman is available on this machine.
Install one of the container runtimes, or download structurizr.war
(https://docs.structurizr.com/binaries, requires Java 21) and run the commands manually:
  java -jar structurizr.war validate -workspace <workspace>
  java -jar structurizr.war export -workspace <workspace> -format json -output <output>
  java -jar structurizr.war export -workspace <workspace> -format plantuml -output <output>
MSG
  exit 3
fi

mkdir -p "${OUTPUT_DIR}"

# The image uses /usr/local/structurizr as its working directory, so repository-relative
# paths work unchanged inside the container.
run_structurizr() {
  ${RUNTIME} run --rm -v "$(pwd)":/usr/local/structurizr "${STRUCTURIZR_IMAGE}" "$@"
}

run_structurizr validate -workspace "${WORKSPACE}"

# `structurizr export` takes a single -format per invocation.
IFS=',' read -r -a FORMAT_LIST <<< "${FORMATS}"
for format in "${FORMAT_LIST[@]}"; do
  format="${format// /}"
  [[ -z "${format}" ]] && continue
  run_structurizr export -workspace "${WORKSPACE}" -format "${format}" -output "${OUTPUT_DIR}"
done

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
