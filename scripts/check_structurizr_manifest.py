"""Validate the Structurizr workspace manifest and ADR references."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import sys
from typing import Iterable


ADR_PATTERN = re.compile(r"ADR-\d{4}")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--workspace",
        default="docs/examples/structurizr/aac_reference_workspace.dsl",
        help="Path to the Structurizr DSL workspace file (default: %(default)s)",
    )
    parser.add_argument(
        "--manifest",
        default="docs/examples/structurizr/aac_reference_workspace.manifest.json",
        help="Path to the manifest JSON file (default: %(default)s)",
    )
    parser.add_argument(
        "--adr-root",
        default="docs/examples/structurizr/adrs",
        help="Directory containing ADR markdown files (default: %(default)s)",
    )
    return parser.parse_args()


def _sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def _load_manifest(manifest_path: pathlib.Path) -> dict:
    try:
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Manifest not found: {manifest_path}") from exc


def _collect_adr_ids(directory: pathlib.Path) -> set[str]:
    return {
        match.group(0)
        for path in directory.glob("ADR-*.md")
        for match in [ADR_PATTERN.search(path.name)]
        if match
    }


def _extract_workspace_adrs(workspace_path: pathlib.Path) -> Iterable[str]:
    text = workspace_path.read_text(encoding="utf-8")
    return ADR_PATTERN.findall(text)


def main() -> int:
    args = _parse_args()
    workspace = pathlib.Path(args.workspace)
    manifest_path = pathlib.Path(args.manifest)
    adr_root = pathlib.Path(args.adr_root)

    if not workspace.exists():
        raise FileNotFoundError(f"Workspace not found: {workspace}")

    manifest = _load_manifest(manifest_path)
    expected_hash = manifest.get("workspace_sha256")
    actual_hash = _sha256(workspace)

    exit_code = 0

    if expected_hash != actual_hash:
        print(
            "Structurizr workspace digest mismatch."
            f" Expected {expected_hash}, found {actual_hash}."
            " Run ./scripts/render_structurizr_diagrams.sh to refresh exports.",
            file=sys.stderr,
        )
        exit_code = 1

    declared_workspace = manifest.get("workspace_path")
    if declared_workspace and pathlib.Path(declared_workspace) != workspace:
        print(
            "Manifest workspace_path does not match the provided workspace argument.",
            file=sys.stderr,
        )
        exit_code = 1

    adr_root.mkdir(parents=True, exist_ok=True)
    available_adrs = _collect_adr_ids(adr_root)
    missing_files: set[str] = set()
    referenced_adrs = set(_extract_workspace_adrs(workspace))
    for adr_id in referenced_adrs:
        if not any(path.name.startswith(adr_id) for path in adr_root.glob(f"{adr_id}*.md")):
            missing_files.add(adr_id)

    if missing_files:
        print(
            "The workspace references ADR identifiers without matching markdown files: "
            + ", ".join(sorted(missing_files)),
            file=sys.stderr,
        )
        exit_code = 1

    unused_adrs = available_adrs - referenced_adrs
    if unused_adrs:
        print(
            "Warning: ADR files exist but are not linked from the workspace: "
            + ", ".join(sorted(unused_adrs)),
            file=sys.stderr,
        )

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
