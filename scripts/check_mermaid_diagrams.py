#!/usr/bin/env python3
"""Validate that committed Mermaid diagrams reflect their sources."""

from __future__ import annotations

import argparse
import filecmp
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List, Tuple


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


def _render_diagram(
    mmdc_path: Path, source: Path, target: Path, theme: Path | None
) -> Tuple[bool, str]:
    """Render a Mermaid source file to ``target`` using the configured CLI."""

    command = _build_command(mmdc_path, source, target, theme)

    result = subprocess.run(
        command,
        check=False,
        env=os.environ,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "").strip()
        return False, detail

    if not target.is_file() or target.stat().st_size == 0:
        return False, "Mermaid CLI did not produce output"

    return True, ""


def _prepare_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Validate committed Mermaid diagrams and optionally refresh missing "
            "or outdated PNG renderings."
        )
    )
    parser.add_argument(
        "--write-missing",
        action="store_true",
        help=(
            "Render PNG files for diagrams that are missing or diverge from their "
            "current Mermaid source definitions."
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = _prepare_arguments()
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
    generated: List[Path] = []
    refreshed: List[Path] = []

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        for source in sources:
            target = source.with_suffix(".png")

            if not target.is_file():
                if not args.write_missing:
                    failures.append(
                        "❌ Missing rendered diagram for "
                        f"{source.relative_to(repo_root)}"
                    )
                    continue

                success, detail = _render_diagram(mmdc_path, source, target, theme_file)
                if not success:
                    failures.append(
                        "❌ Failed to render missing diagram "
                        f"{source.relative_to(repo_root)} via Mermaid CLI: {detail}"
                    )
                    continue

                generated.append(target)

            candidate = tmp_path / target.name
            success, detail = _render_diagram(mmdc_path, source, candidate, theme_file)

            if not success:
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

            if not filecmp.cmp(candidate, target, shallow=False):
                if args.write_missing:
                    try:
                        shutil.copy2(candidate, target)
                    except OSError as err:
                        failures.append(
                            "❌ Unable to refresh diagram "
                            f"{target.relative_to(repo_root)}: {err}"
                        )
                        continue

                    refreshed.append(target)
                else:
                    failures.append(
                        "❌ Rendered output diverges from committed PNG: "
                        f"{target.relative_to(repo_root)}"
                    )

    if failures:
        print("Mermaid diagram validation failed:")
        for failure in failures:
            print(failure)
        return 1

    if args.write_missing:
        if generated:
            print(
                "🆕 Regenerated the following Mermaid diagrams:"  # pragma: no cover - output only
            )
            for target in sorted(generated):
                print(f"   • {target.relative_to(repo_root)}")

        if refreshed:
            print(
                "🔄 Updated the following Mermaid diagrams to match their sources:"  # pragma: no cover - output only
            )
            for target in sorted(refreshed):
                print(f"   • {target.relative_to(repo_root)}")

    print("✅ All Mermaid diagrams match their committed PNG counterparts.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
