from __future__ import annotations

"""Verify that local tooling matches the pinned versions for the book build."""

import json
import platform
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, Iterable, Tuple

try:
    import yaml
except ImportError as exc:  # pragma: no cover - guidance for missing dependency
    message = (
        "PyYAML is required to parse BOOK_REQUIREMENTS.md. "
        "Install the pinned Python dependencies with 'pip install -r requirements.txt' "
        "and rerun this check."
    )
    raise SystemExit(message) from exc

from packaging.version import InvalidVersion, Version

REPO_ROOT = Path(__file__).resolve().parents[1]
BOOK_REQUIREMENTS = REPO_ROOT / "BOOK_REQUIREMENTS.md"
REQUIREMENTS_TXT = REPO_ROOT / "requirements.txt"
PACKAGE_JSON = REPO_ROOT / "package.json"
PACKAGE_LOCK = REPO_ROOT / "package-lock.json"


class VerificationError(Exception):
    """Raised when one or more environment checks fail."""


def _load_front_matter() -> dict:
    if not BOOK_REQUIREMENTS.exists():
        raise VerificationError("BOOK_REQUIREMENTS.md is missing.")

    lines = BOOK_REQUIREMENTS.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise VerificationError("BOOK_REQUIREMENTS.md does not contain YAML front matter.")

    front_matter_lines = []
    for line in lines[1:]:
        if line.strip() == "---":
            break
        front_matter_lines.append(line)

    if not front_matter_lines:
        raise VerificationError("BOOK_REQUIREMENTS.md front matter is empty.")

    return yaml.safe_load("\n".join(front_matter_lines)) or {}


def _parse_version(raw: str) -> Version:
    normalised = raw.strip().lstrip("v")
    try:
        return Version(normalised)
    except InvalidVersion as exc:
        raise VerificationError(f"Cannot parse version '{raw}'.") from exc


def _run_version_command(command: Iterable[str], pattern: str | None = None) -> str:
    try:
        completed = subprocess.run(
            list(command),
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except FileNotFoundError:
        return ""
    except subprocess.CalledProcessError:
        return ""

    output = (completed.stdout or "") + (completed.stderr or "")
    output = output.strip()

    if not pattern:
        inline_match = re.search(r"\d+(?:\.\d+)+", output)
        return inline_match.group(0) if inline_match else output

    match = re.search(pattern, output)
    return match.group(1) if match else ""


def _compare_versions(label: str, expected: str, actual: str) -> Tuple[bool, str]:
    if not actual:
        return False, f"{label}: expected {expected}, but the command was not found."

    expected_version = _parse_version(expected)
    actual_version = _parse_version(actual)

    if actual_version != expected_version:
        return (
            False,
            f"{label}: expected {expected_version}, found {actual_version}.",
        )

    return True, f"{label}: {actual_version} (matched)."


def _load_requirements_versions() -> Dict[str, str]:
    if not REQUIREMENTS_TXT.exists():
        raise VerificationError("requirements.txt is missing.")

    versions: Dict[str, str] = {}
    for line in REQUIREMENTS_TXT.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if "==" not in stripped:
            raise VerificationError(
                f"requirements.txt entry '{stripped}' is not pinned with '=='."
            )
        name, version = stripped.split("==", 1)
        versions[name.strip()] = version.strip()

    return versions


def _load_package_json_versions() -> Dict[str, str]:
    if not PACKAGE_JSON.exists():
        raise VerificationError("package.json is missing.")

    data = json.loads(PACKAGE_JSON.read_text(encoding="utf-8"))
    deps = data.get("devDependencies", {})
    return {name: value for name, value in deps.items()}


def _load_package_lock_version(package_name: str) -> str:
    if not PACKAGE_LOCK.exists():
        raise VerificationError("package-lock.json is missing.")

    data = json.loads(PACKAGE_LOCK.read_text(encoding="utf-8"))
    packages = data.get("packages", {})
    package_key = f"node_modules/{package_name}"
    if package_key not in packages:
        raise VerificationError(
            f"package-lock.json is missing the '{package_name}' entry."
        )
    return str(packages[package_key].get("version", "")).strip()


def verify_tool_versions(metadata: dict) -> list[str]:
    toolchain = metadata.get("toolchain") or {}
    issues: list[str] = []

    checks = [
        (
            "Python",
            toolchain.get("python"),
            platform.python_version(),
        ),
        (
            "Pandoc",
            toolchain.get("pandoc"),
            _run_version_command(["pandoc", "--version"], r"pandoc\s+(\S+)")
            if toolchain.get("pandoc")
            else "",
        ),
        (
            "Node.js",
            toolchain.get("node"),
            _run_version_command(["node", "--version"]),
        ),
        (
            "Mermaid CLI",
            toolchain.get("mermaid_cli"),
            _run_version_command(["npx", "mmdc", "-V"]),
        ),
    ]

    for label, expected, actual in checks:
        if not expected:
            issues.append(f"{label}: no expected version declared in BOOK_REQUIREMENTS.md.")
            continue

        success, message = _compare_versions(label, expected, actual)
        if not success:
            issues.append(message)
        else:
            print(message)

    return issues


def verify_python_dependencies(metadata: dict) -> list[str]:
    expected = metadata.get("python_dependencies") or {}
    if not expected:
        return ["No python_dependencies declared in BOOK_REQUIREMENTS.md."]

    actual = _load_requirements_versions()
    issues: list[str] = []

    for name, version in expected.items():
        recorded = actual.get(name)
        if recorded is None:
            issues.append(
                f"requirements.txt is missing '{name}=={version}'."
            )
            continue
        if recorded != version:
            issues.append(
                f"requirements.txt pins '{name}=={recorded}' but BOOK_REQUIREMENTS.md expects {version}."
            )

    extra_packages = sorted(set(actual).difference(expected))
    if extra_packages:
        extras = ", ".join(extra_packages)
        issues.append(
            f"requirements.txt contains packages not listed in BOOK_REQUIREMENTS.md: {extras}."
        )

    return issues


def verify_node_dependencies(metadata: dict) -> list[str]:
    expected = metadata.get("node_dependencies") or {}
    if not expected:
        return ["No node_dependencies declared in BOOK_REQUIREMENTS.md."]

    package_versions = _load_package_json_versions()
    issues: list[str] = []

    for name, version in expected.items():
        recorded = package_versions.get(name)
        if recorded is None:
            issues.append(
                f"package.json is missing '{name}' with version {version}."
            )
            continue
        if recorded != version:
            issues.append(
                f"package.json pins '{name}@{recorded}' but BOOK_REQUIREMENTS.md expects {version}."
            )
            continue

        lock_version = _load_package_lock_version(name)
        if lock_version != version:
            issues.append(
                f"package-lock.json records '{name}' as {lock_version} instead of {version}."
            )

    extra_packages = sorted(set(package_versions).difference(expected))
    if extra_packages:
        extras = ", ".join(extra_packages)
        issues.append(
            f"package.json contains additional devDependencies not listed in BOOK_REQUIREMENTS.md: {extras}."
        )

    return issues


def main() -> None:
    metadata = _load_front_matter()
    failures: list[str] = []

    failures.extend(verify_tool_versions(metadata))
    failures.extend(verify_python_dependencies(metadata))
    failures.extend(verify_node_dependencies(metadata))

    if failures:
        print("\nEnvironment verification failed:")
        for issue in failures:
            print(f" - {issue}")
        raise VerificationError("Toolchain versions are not aligned.")

    print("\nAll declared toolchain versions are aligned.")


if __name__ == "__main__":
    try:
        main()
    except VerificationError as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
