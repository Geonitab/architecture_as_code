"""Update the Structurizr workspace manifest with the latest digest and formats."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import pathlib
from typing import Sequence


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
        help="Path to the manifest file that will be written (default: %(default)s)",
    )
    parser.add_argument(
        "--formats",
        default="png,structurizr",
        help="Comma-separated list of export formats captured in the manifest",
    )
    parser.add_argument(
        "--output-dir",
        default="build/structurizr",
        help="Directory used for Structurizr exports (default: %(default)s)",
    )
    return parser.parse_args()


def _normalise_formats(raw: str) -> Sequence[str]:
    return sorted({fragment.strip() for fragment in raw.split(",") if fragment.strip()})


def _sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    args = _parse_args()
    workspace = pathlib.Path(args.workspace)
    manifest_path = pathlib.Path(args.manifest)

    if not workspace.exists():
        raise FileNotFoundError(f"Workspace file not found: {workspace}")

    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    manifest = {
        "workspace_path": str(workspace.as_posix()),
        "workspace_sha256": _sha256(workspace),
        "export_formats": list(_normalise_formats(args.formats)),
        "export_directory": str(pathlib.Path(args.output_dir).as_posix()),
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
    }

    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
