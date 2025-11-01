import json
from pathlib import Path

import yaml

BASE_DIR = Path(__file__).resolve().parents[1]
INDEX_PATH = BASE_DIR / "docs" / "book_index.json"
MKDOCS_PATH = BASE_DIR / "mkdocs.yml"


def _load_index():
    with INDEX_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def _iter_index_files(index_data):
    for part in index_data["parts"]:
        for chapter in part["chapters"]:
            yield chapter["file"], chapter["identifier"]
    for appendix in index_data["appendices"]:
        yield appendix["file"], appendix["identifier"]
    for supplement in index_data.get("supplements", []):
        yield supplement["file"], supplement["identifier"]


def test_book_index_counts_and_files_exist():
    index_data = _load_index()
    files = list(_iter_index_files(index_data))
    counted_units = sum(1 for _, identifier in files if not identifier.startswith("maturity_"))

    assert (
        index_data["total_units"] == counted_units
    ), f"Expected total_units={counted_units}, found {index_data['total_units']}"

    for file_path, identifier in files:
        target = BASE_DIR / file_path
        assert target.exists(), f"Missing file for identifier {identifier}: {file_path}"


def _extract_nav_entries(node):
    if isinstance(node, dict):
        for value in node.values():
            yield from _extract_nav_entries(value)
    elif isinstance(node, list):
        for item in node:
            yield from _extract_nav_entries(item)
    elif isinstance(node, str):
        yield node


def test_book_index_matches_mkdocs_navigation():
    index_data = _load_index()
    with MKDOCS_PATH.open(encoding="utf-8") as handle:
        mkdocs_config = yaml.safe_load(handle)

    nav_entries = {
        entry.replace("\\", "/") for entry in _extract_nav_entries(mkdocs_config.get("nav", []))
    }

    missing = []
    for file_path, identifier in _iter_index_files(index_data):
        relative_path = file_path.replace("\\", "/")
        if relative_path.startswith("docs/"):
            relative_path = relative_path[len("docs/") :]
        if identifier.startswith("maturity_"):
            # Supplements are optional in MkDocs navigation but must be accessible.
            continue
        if relative_path not in nav_entries:
            missing.append((identifier, relative_path))

    assert not missing, f"Entries missing from MkDocs navigation: {missing}"
