"""Canonical navigation utilities shared across the publishing toolchain."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterator, Sequence

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
MKDOCS_CONFIG_PATH = REPO_ROOT / "mkdocs.yml"


class NavigationError(RuntimeError):
    """Raised when the canonical navigation cannot be resolved."""


def load_mkdocs_configuration(path: Path = MKDOCS_CONFIG_PATH) -> dict:
    """Load the MkDocs configuration file."""

    if not path.exists():
        raise NavigationError(f"MkDocs configuration not found at {path}.")

    try:
        with path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
    except yaml.YAMLError as exc:  # pragma: no cover - YAML failures are rare
        raise NavigationError("Failed to parse MkDocs configuration.") from exc

    if not isinstance(data, dict):
        raise NavigationError("Unexpected MkDocs configuration structure.")

    return data


def load_navigation(path: Path = MKDOCS_CONFIG_PATH) -> list:
    """Return the raw navigation structure from mkdocs.yml."""

    config = load_mkdocs_configuration(path)
    nav = config.get("nav")
    if not isinstance(nav, list):
        raise NavigationError("mkdocs.yml must define a top-level 'nav' list.")

    return nav


def _iter_targets(node: object) -> Iterator[str]:
    """Yield every file target referenced within a navigation subtree."""

    if isinstance(node, str):
        yield node
        return

    if isinstance(node, list):
        for item in node:
            yield from _iter_targets(item)
        return

    if isinstance(node, dict):
        for value in node.values():
            yield from _iter_targets(value)
        return


def _is_markdown(target: str) -> bool:
    """Return True when the navigation target refers to a markdown document."""

    return Path(target).suffix.lower() == ".md"


def _collect_section_markdown(section: Sequence[object]) -> list[str]:
    """Collect markdown files from a structured navigation section."""

    markdown_files: list[str] = []
    for target in _iter_targets(list(section)):
        if _is_markdown(target):
            markdown_files.append(target)
    return markdown_files


def get_book_build_files(nav: Sequence[object] | None = None) -> list[str]:
    """Return the ordered markdown files that form the full book build."""

    nav = list(nav) if nav is not None else load_navigation()

    ordered_files: list[str] = []
    for entry in nav:
        if not isinstance(entry, dict) or len(entry) != 1:
            continue

        title, children = next(iter(entry.items()))
        if not isinstance(children, (list, tuple)):
            continue

        if title.startswith("Part ") or title == "Appendices":
            ordered_files.extend(_collect_section_markdown(children))

    if not ordered_files:
        raise NavigationError("No book chapters resolved from navigation.")

    return ordered_files


def get_whitepaper_chapter_files(nav: Sequence[object] | None = None) -> list[str]:
    """Return ordered chapter files suitable for whitepaper exports."""

    book_files = get_book_build_files(nav)
    return [name for name in book_files if not Path(name).stem.startswith("part_")]


def get_all_navigation_targets(nav: Sequence[object] | None = None) -> list[str]:
    """Return every file target referenced anywhere in the navigation."""

    nav = list(nav) if nav is not None else load_navigation()
    return list(_iter_targets(nav))


def _parse_arguments(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inspect the canonical navigation for Architecture as Code."
    )
    parser.add_argument(
        "--book-build",
        action="store_true",
        help="Print the markdown files used for the full book build in order.",
    )
    parser.add_argument(
        "--chapters",
        action="store_true",
        help="Print the ordered chapter files excluding part introductions.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Print every file target referenced in the navigation.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_arguments(argv)

    try:
        if args.book_build:
            outputs = get_book_build_files()
        elif args.chapters:
            outputs = get_whitepaper_chapter_files()
        elif args.all:
            outputs = get_all_navigation_targets()
        else:
            outputs = []
    except NavigationError as exc:
        print(f"Error: {exc}")
        return 1

    for line in outputs:
        print(line)

    return 0


if __name__ == "__main__":  # pragma: no cover - exercised via CLI
    raise SystemExit(main())
