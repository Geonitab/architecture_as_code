from pathlib import Path
import re


def test_numbered_chapters_do_not_exceed_bounds() -> None:
    docs_dir = Path(__file__).resolve().parents[1] / "docs"
    max_allowed = 33
    offending = []

    for entry in docs_dir.iterdir():
        if not entry.is_file():
            continue
        match = re.match(r"^(\d+)_", entry.name)
        if match and int(match.group(1)) > max_allowed:
            offending.append(entry.name)

    assert not offending, (
        "Numbered chapter filenames must not exceed "
        f"{max_allowed:02d}_*. Found: {', '.join(sorted(offending))}"
    )
