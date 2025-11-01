#!/usr/bin/env python3
"""Validate that committed Mermaid diagrams reflect their sources."""

from __future__ import annotations

import filecmp
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List


def _resolve_mmdc(root: Path) -> Path:
    """Locate the Mermaid CLI executable."""

    local_mmdc = root / "node_modules" / ".bin" / "mmdc"
    if local_mmdc.is_file():
        return local_mmdc

    fallback = shutil.which("mmdc")
    if fallback:
        return Path(fallback)

    raise FileNotFoundError(
        "Mermaid CLI (mmdc) is unavailable. Run 'npm ci' before executing this check."
    )


def _build_command(
    mmdc_path: Path, source: Path, target: Path, theme: Path | None
) -> List[str]:
    command = [
        str(mmdc_path),
        "-i",
        str(source),
        "-o",
        str(target),
        "-t",
        "default",
        "-b",
        "transparent",
        "--width",
        "1400",
        "--height",
        "900",
    ]

    if theme and theme.is_file():
        command.extend(["-c", str(theme)])

    return command


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    images_dir = repo_root / "docs" / "images"
    theme_file = repo_root / "docs" / "mermaid-kvadrat-theme.json"

    if not images_dir.is_dir():
        print("No diagram directory found; nothing to validate.")
        return 0

    try:
        mmdc_path = _resolve_mmdc(repo_root)
    except FileNotFoundError as exc:  # pragma: no cover - direct exit path
        print(str(exc), file=sys.stderr)
        return 2

    sources = sorted(images_dir.glob("*.mmd"))
    if not sources:
        print("No Mermaid sources discovered; nothing to validate.")
        return 0

    failures: List[str] = []

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        for source in sources:
            target = source.with_suffix(".png")

            if not target.is_file():
                failures.append(
                    f"❌ Missing rendered diagram for {source.relative_to(repo_root)}"
                )
                continue

            candidate = tmp_path / target.name
            command = _build_command(mmdc_path, source, candidate, theme_file)

            result = subprocess.run(
                command,
                check=False,
                env=os.environ,
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:
                detail = (result.stderr or result.stdout or "").strip()
                if "libatk-1.0.so.0" in detail:
                    failures.append(
                        "❌ Mermaid CLI could not launch a headless browser. Install the "
                        "GTK/ATK runtime (e.g. libatk-1.0-0, libgtk-3-0, libnss3, libxss1) "
                        "or point PUPPETEER_EXECUTABLE_PATH to an existing Chrome binary "
                        "before running the check."
                    )
                    break

                failures.append(
                    "❌ Failed to render "
                    f"{source.relative_to(repo_root)} via Mermaid CLI: {detail}"
                )
                continue

            if not candidate.is_file() or candidate.stat().st_size == 0:
                failures.append(
                    f"❌ Mermaid CLI did not produce output for {source.relative_to(repo_root)}"
                )
                continue

            if not filecmp.cmp(candidate, target, shallow=False):
                failures.append(
                    "❌ Rendered output diverges from committed PNG: "
                    f"{target.relative_to(repo_root)}"
                )

    if failures:
        print("Mermaid diagram validation failed:")
        for failure in failures:
            print(failure)
        return 1

    print("✅ All Mermaid diagrams match their committed PNG counterparts.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
