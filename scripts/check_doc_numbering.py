#!/usr/bin/env python3
"""Validate numbering of book chapter files in docs/ directory."""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path
import re

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"
PATTERN = re.compile(r"^(?P<number>\d+)(?P<suffix>[a-z]*)_.*\.md$", re.IGNORECASE)


def collect_numbered_files() -> dict[int, list[tuple[str, Path]]]:
    numbered: dict[int, list[tuple[str, Path]]] = defaultdict(list)

    for path in DOCS_DIR.glob("*.md"):
        match = PATTERN.match(path.name)
        if not match:
            continue

        number = int(match.group("number"))
        suffix = match.group("suffix").lower()
        numbered[number].append((suffix, path))

    return numbered


def find_numeric_gaps(sorted_numbers: list[int]) -> list[tuple[int, int]]:
    gaps: list[tuple[int, int]] = []
    for current, nxt in zip(sorted_numbers, sorted_numbers[1:]):
        if nxt - current > 1:
            gaps.append((current, nxt))
    return gaps


def find_numeric_duplicates(entries: dict[int, list[tuple[str, Path]]]) -> list[str]:
    duplicates: list[str] = []
    for number, suffixes in entries.items():
        seen: dict[str, Path] = {}
        for suffix, path in suffixes:
            key = f"{number}{suffix}"
            if key in seen:
                duplicates.append(
                    "Duplicate entry for "
                    f"{key}: {seen[key].name} and {path.name}"
                )
            else:
                seen[key] = path
    return duplicates


def check_suffix_sequences(number: int, suffix_entries: list[tuple[str, Path]]) -> list[str]:
    errors: list[str] = []

    base_present = any(suffix == "" for suffix, _ in suffix_entries)
    letters = sorted({suffix for suffix, _ in suffix_entries if suffix})

    if len(letters) != len([suffix for suffix, _ in suffix_entries if suffix]):
        errors.append(f"Duplicate appendix suffix detected for {number:02d}")

    if not letters:
        return errors

    expected_start = "a" if not base_present else letters[0]
    expected_ord = ord(expected_start)

    for letter in letters:
        if ord(letter) != expected_ord:
            expected_label = chr(expected_ord).upper()
            errors.append(
                "Missing appendix label for "
                f"{number:02d}: expected suffix '{expected_label}' before '{letter.upper()}'"
            )
            expected_ord = ord(letter)
        expected_ord += 1

    return errors


def main() -> int:
    numbered = collect_numbered_files()
    if not numbered:
        print("No numbered chapters found in docs/ directory.")
        return 0

    sorted_numbers = sorted(numbered)

    errors: list[str] = []

    gaps = find_numeric_gaps(sorted_numbers)
    for previous_number, next_number in gaps:
        errors.append(
            "Gap detected between numbered chapters: "
            f"{previous_number:02d} is followed by {next_number:02d}."
        )

    errors.extend(find_numeric_duplicates(numbered))

    for number, suffix_entries in numbered.items():
        errors.extend(check_suffix_sequences(number, suffix_entries))

    if errors:
        print("Numbering validation failed:")
        for message in errors:
            print(f" - {message}")
        return 1

    print("Numbering validation passed with no gaps or duplicates detected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
