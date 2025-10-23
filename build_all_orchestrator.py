#!/usr/bin/env python3
"""
High-level orchestrator for building all Architecture as Code deliverables locally.

This script coordinates the existing automation entry points to regenerate every
publication asset (book formats, whitepapers, presentations, and optionally the
static site) and, if requested, produces a consolidated archive of the results.

Usage examples:
    python3 build_all_orchestrator.py
    python3 build_all_orchestrator.py --include-site --zip
    python3 build_all_orchestrator.py --skip-presentations

The script is intentionally thin; the heavy lifting remains in:
    - generate_book.py
    - docs/build_book.sh
    - generate_whitepapers.py
    - generate_presentation.py
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent
RELEASE_ROOT = ROOT / "releases"
BOOK_RELEASE = RELEASE_ROOT / "book"
WHITEPAPER_RELEASE = RELEASE_ROOT / "whitepapers"
PRESENTATION_RELEASE = RELEASE_ROOT / "presentation"
WEBSITE_RELEASE = RELEASE_ROOT / "website"


def _timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log(message: str) -> None:
    print(f"[{_timestamp()}] {message}")


def log_success(message: str) -> None:
    log(f"✅ {message}")


def log_warning(message: str) -> None:
    log(f"⚠️  {message}")


def log_error(message: str) -> None:
    log(f"❌ {message}")


def run_command(command: Iterable[str | Path], *, cwd: Path | None = None) -> None:
    """Run a shell command and stream output, raising on failure."""
    command_as_str = [str(item) for item in command]
    working_dir = cwd or ROOT
    log(f"→ Running: {' '.join(command_as_str)} (cwd: {working_dir})")

    result = subprocess.run(command_as_str, cwd=working_dir, check=False)
    if result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, command_as_str, None, None)


def human_readable_size(path: Path) -> str:
    """Return a human-readable file size string."""
    size = path.stat().st_size
    units = ["B", "KB", "MB", "GB", "TB"]
    index = 0
    while size >= 1024 and index < len(units) - 1:
        size /= 1024.0
        index += 1
    return f"{size:.2f} {units[index]}"


def verify_file(path: Path, label: str, *, required: bool = True) -> None:
    """Validate that a file exists and is not empty."""
    if path.exists() and path.stat().st_size > 0:
        log_success(f"{label}: {path} ({human_readable_size(path)})")
    elif required:
        raise FileNotFoundError(f"Required file missing: {path}")
    else:
        log_warning(f"Optional file missing: {path}")


def verify_directory(path: Path, label: str) -> None:
    """Ensure a directory exists and contains at least one file."""
    if path.exists():
        file_count = sum(1 for file_path in path.rglob("*") if file_path.is_file())
        if file_count > 0:
            log_success(f"{label}: {path} ({file_count} files)")
            return
    raise FileNotFoundError(f"{label} not generated: {path}")


def ensure_release_structure(include_site: bool) -> None:
    """Create the standard release directory structure."""
    for directory in (BOOK_RELEASE, WHITEPAPER_RELEASE, PRESENTATION_RELEASE):
        directory.mkdir(parents=True, exist_ok=True)

    if include_site:
        WEBSITE_RELEASE.mkdir(parents=True, exist_ok=True)


def orchestrate_book() -> None:
    log("📚 Generating book content…")
    run_command([sys.executable, "generate_book.py"])

    log("📖 Building book formats via docs/build_book.sh …")
    run_command(["bash", "docs/build_book.sh", "--release"])

    verify_file(BOOK_RELEASE / "architecture_as_code.pdf", "Book PDF")
    verify_file(BOOK_RELEASE / "architecture_as_code.epub", "Book EPUB", required=False)
    verify_file(BOOK_RELEASE / "architecture_as_code.docx", "Book DOCX", required=False)


def orchestrate_whitepapers() -> None:
    log("📄 Generating whitepapers…")
    run_command([sys.executable, "generate_whitepapers.py", "--release"])
    verify_directory(WHITEPAPER_RELEASE, "Whitepapers")


def orchestrate_presentations() -> None:
    log("🎤 Generating presentation materials…")
    run_command(
        [
            sys.executable,
            "generate_presentation.py",
            "--release",
            "--create-pptx",
            "--output",
            "architecture_as_code_presentation.pptx",
        ]
    )
    verify_directory(PRESENTATION_RELEASE, "Presentation materials")


def orchestrate_site() -> None:
    if not (ROOT / "mkdocs.yml").exists():
        log_warning("mkdocs.yml not found – skipping site build.")
        return

    if not shutil.which("mkdocs"):
        log_warning("MkDocs not installed – skipping site build.")
        return

    log("🌐 Building MkDocs site…")
    run_command(["mkdocs", "build", "-d", "site"])

    WEBSITE_RELEASE.mkdir(parents=True, exist_ok=True)
    for entry in (ROOT / "site").iterdir():
        destination = WEBSITE_RELEASE / entry.name
        if entry.is_dir():
            shutil.copytree(entry, destination, dirs_exist_ok=True)
        else:
            shutil.copy2(entry, destination)
    verify_directory(WEBSITE_RELEASE, "Website")


def create_archive(output_path: Path) -> None:
    """Create a zip archive containing the entire releases/ directory."""
    if not RELEASE_ROOT.exists():
        raise FileNotFoundError("Releases directory not found; nothing to archive.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.exists():
        output_path.unlink()

    files = [path for path in RELEASE_ROOT.rglob("*") if path.is_file()]
    if not files:
        raise FileNotFoundError("No release files found to archive.")

    # Ensure we never include the archive itself in the payload
    files = [path for path in files if path != output_path]
    if not files:
        raise FileNotFoundError("No release files found to archive.")

    log(f"📦 Creating archive at {output_path} …")
    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for file_path in files:
            archive.write(file_path, file_path.relative_to(RELEASE_ROOT))

    log_success(f"Archive created: {output_path} ({human_readable_size(output_path)})")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build all Architecture as Code deliverables in one command."
    )
    parser.add_argument("--skip-book", action="store_true", help="Skip book generation.")
    parser.add_argument(
        "--skip-whitepapers", action="store_true", help="Skip whitepaper generation."
    )
    parser.add_argument(
        "--skip-presentations", action="store_true", help="Skip presentation generation."
    )
    parser.add_argument(
        "--include-site",
        action="store_true",
        help="Generate the MkDocs site (skipped by default).",
    )
    parser.add_argument(
        "--zip",
        dest="create_zip",
        action="store_true",
        help="Create a consolidated zip archive of the releases/ directory.",
    )
    parser.add_argument(
        "--archive-name",
        default="architecture_as_code_release.zip",
        help="Filename for the consolidated archive (default: architecture_as_code_release.zip).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ensure_release_structure(include_site=args.include_site)

    try:
        if args.skip_book:
            log_warning("Skipping book generation as requested.")
        else:
            orchestrate_book()

        if args.skip_whitepapers:
            log_warning("Skipping whitepaper generation as requested.")
        else:
            orchestrate_whitepapers()

        if args.skip_presentations:
            log_warning("Skipping presentation generation as requested.")
        else:
            orchestrate_presentations()

        if args.include_site:
            orchestrate_site()
        else:
            log("🌐 Site build skipped (enable with --include-site).")

        if args.create_zip:
            archive_path = RELEASE_ROOT / args.archive_name
            create_archive(archive_path)

        log_success("Build orchestrator completed successfully.")
        return 0

    except subprocess.CalledProcessError as exc:
        log_error(
            f"Command failed with exit code {exc.returncode}: {' '.join(exc.cmd)}"
        )
        return exc.returncode
    except FileNotFoundError as exc:
        log_error(str(exc))
        return 1
    except Exception as exc:  # pylint: disable=broad-except
        log_error(f"Unexpected error: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
