#!/usr/bin/env python3
"""Validate numbering of chapter files in docs/.

This script ensures that numbered markdown files in the docs directory follow
contiguous numbering rules and that any alphabetic suffixes form contiguous
series without duplicates. It is intended for CI use to catch accidental gaps
or duplicate identifiers when new chapters are added.
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List

ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"
NUMBERED_PATTERN = re.compile(r"^(\d+)([a-z]?)(?:_.*)?\.md$")


@dataclass(frozen=True)
class ChapterEntry:
    number: int
    suffix: str
    path: Path

    @property
    def identifier(self) -> str:
        """Return the chapter identifier such as 15 or 26b."""
        return f"{self.number}{self.suffix}" if self.suffix else str(self.number)


def find_numbered_chapters(paths: Iterable[Path]) -> List[ChapterEntry]:
    entries: List[ChapterEntry] = []
    for path in paths:
        if not path.is_file():
            continue
        match = NUMBERED_PATTERN.match(path.name)
        if match:
            number = int(match.group(1))
            suffix = match.group(2)
            entries.append(ChapterEntry(number=number, suffix=suffix, path=path))
    return entries


def check_contiguous_numbers(entries: List[ChapterEntry]) -> List[str]:
    issues: List[str] = []
    numbers = sorted({entry.number for entry in entries})
    if not numbers:
        issues.append("No numbered chapters were found in docs/.")
        return issues

    expected = numbers[0]
    for number in numbers:
        if number != expected:
            issues.append(
                f"Gap detected: expected chapter {expected:02d} but found {number:02d}."
            )
            expected = number
        expected += 1
    return issues


def check_suffix_rules(entries: List[ChapterEntry]) -> List[str]:
    issues: List[str] = []
    grouped: Dict[int, List[ChapterEntry]] = {}
    for entry in entries:
        grouped.setdefault(entry.number, []).append(entry)

    for number in sorted(grouped):
        group = grouped[number]
        suffixes = [entry.suffix for entry in group]
        base_count = suffixes.count("")
        if base_count > 1:
            files = ", ".join(str(entry.path.relative_to(ROOT)) for entry in group if entry.suffix == "")
            issues.append(
                f"Duplicate numeric chapter {number:02d} without suffix found in: {files}."
            )
            continue

        seen_letters = set()
        letter_indices: List[int] = []
        has_base = base_count == 1

        for entry in group:
            suffix = entry.suffix
            if not suffix:
                continue
            if len(suffix) != 1 or not suffix.isalpha() or not suffix.islower():
                issues.append(
                    f"Invalid suffix '{suffix}' on {entry.path.relative_to(ROOT)}; use a single lowercase letter."
                )
                continue
            if suffix in seen_letters:
                issues.append(
                    f"Duplicate suffix '{suffix}' for chapter {number:02d} in {entry.path.relative_to(ROOT)}."
                )
                continue
            if has_base and suffix == "a":
                issues.append(
                    f"Chapter {number:02d} already has a base file but also uses suffix 'a' in {entry.path.relative_to(ROOT)}."
                )
                continue
            seen_letters.add(suffix)
            letter_indices.append(ord(suffix) - ord("a"))

        sequence: List[int]
        if has_base:
            sequence = [0] + sorted(letter_indices)
        else:
            sequence = sorted(letter_indices)

        if sequence:
            expected_sequence = list(range(sequence[-1] + 1))
        else:
            expected_sequence = []
        if sequence != expected_sequence:
            missing_segments = []
            for expected_index in expected_sequence:
                if expected_index not in sequence:
                    if has_base and expected_index == 0:
                        # base missing is already covered by base_count == 0
                        continue
                    missing_letter = chr(expected_index + ord("a"))
                    missing_segments.append(missing_letter.upper())
            if missing_segments:
                issues.append(
                    f"Chapter {number:02d} is missing suffixes: {', '.join(missing_segments)}."
                )
            else:
                issues.append(
                    f"Chapter {number:02d} suffixes are not contiguous: {sequence} expected {expected_sequence}."
                )
    return issues


def main() -> int:
    if not DOCS_DIR.exists():
        print("docs/ directory not found", file=sys.stderr)
        return 1

    entries = find_numbered_chapters(DOCS_DIR.glob("*.md"))
    issues = []
    issues.extend(check_contiguous_numbers(entries))
    issues.extend(check_suffix_rules(entries))

    if issues:
        print("Numbering validation failed:")
        for issue in issues:
            print(f" - {issue}")
        return 1

    print("✅ Numbering validation passed: chapter files are contiguous and uniquely labelled.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
