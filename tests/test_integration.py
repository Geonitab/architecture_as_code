"""
Integration tests for end-to-end build process prerequisites.

These tests validate that all build prerequisites and configuration are in place
without actually running the build. They are designed to be fast.
"""
import importlib
import json
import os
import stat
import sys
from pathlib import Path

import pytest

# Project root is one level above tests/
PROJECT_ROOT = Path(__file__).parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"


class TestPythonScripts:
    """Validate that key Python scripts exist and are importable."""

    def test_generate_book_exists(self):
        """Test that generate_book.py exists in the project root."""
        script = PROJECT_ROOT / "generate_book.py"
        assert script.exists(), f"generate_book.py not found at {script}"

    def test_build_all_orchestrator_exists(self):
        """Test that build_all_orchestrator.py exists in the project root."""
        script = PROJECT_ROOT / "build_all_orchestrator.py"
        assert script.exists(), f"build_all_orchestrator.py not found at {script}"

    def test_generate_presentation_exists(self):
        """Test that generate_presentation.py exists in the project root."""
        script = PROJECT_ROOT / "generate_presentation.py"
        assert script.exists(), f"generate_presentation.py not found at {script}"

    def test_generate_whitepapers_exists(self):
        """Test that generate_whitepapers.py exists in the project root."""
        script = PROJECT_ROOT / "generate_whitepapers.py"
        assert script.exists(), f"generate_whitepapers.py not found at {script}"

    def test_generate_book_importable(self):
        """Test that generate_book.py can be imported without error."""
        if str(PROJECT_ROOT) not in sys.path:
            sys.path.insert(0, str(PROJECT_ROOT))
        try:
            import generate_book  # noqa: F401
        except ImportError as exc:
            pytest.fail(f"generate_book.py could not be imported: {exc}")

    def test_build_all_orchestrator_importable(self):
        """Test that build_all_orchestrator.py can be imported without error."""
        if str(PROJECT_ROOT) not in sys.path:
            sys.path.insert(0, str(PROJECT_ROOT))
        try:
            import build_all_orchestrator  # noqa: F401
        except ImportError as exc:
            pytest.fail(f"build_all_orchestrator.py could not be imported: {exc}")

    def test_navigation_module_importable(self):
        """Test that scripts/navigation.py can be imported without error."""
        scripts_dir = PROJECT_ROOT / "scripts"
        if str(scripts_dir) not in sys.path:
            sys.path.insert(0, str(scripts_dir))
        try:
            import navigation  # noqa: F401
        except ImportError as exc:
            pytest.fail(f"scripts/navigation.py could not be imported: {exc}")


class TestBuildScript:
    """Validate the shell build script."""

    def test_build_book_sh_exists(self):
        """Test that docs/build_book.sh exists."""
        script = DOCS_DIR / "build_book.sh"
        assert script.exists(), f"build_book.sh not found at {script}"

    def test_build_book_sh_is_executable(self):
        """Test that docs/build_book.sh is executable."""
        script = DOCS_DIR / "build_book.sh"
        assert script.exists(), f"build_book.sh not found at {script}"
        file_stat = script.stat()
        is_executable = bool(
            file_stat.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        )
        assert is_executable, (
            f"docs/build_book.sh is not executable. "
            f"Current mode: {oct(file_stat.st_mode)}"
        )

    def test_build_release_sh_exists(self):
        """Test that build_release.sh exists in the project root."""
        script = PROJECT_ROOT / "build_release.sh"
        assert script.exists(), f"build_release.sh not found at {script}"


class TestBookIndex:
    """Validate the canonical book index JSON."""

    def test_book_index_exists(self):
        """Test that docs/book_index.json exists."""
        index = DOCS_DIR / "book_index.json"
        assert index.exists(), f"book_index.json not found at {index}"

    def test_book_index_is_valid_json(self):
        """Test that docs/book_index.json is valid JSON."""
        index = DOCS_DIR / "book_index.json"
        assert index.exists(), f"book_index.json not found at {index}"
        with open(index, "r", encoding="utf-8") as fh:
            try:
                data = json.load(fh)
            except json.JSONDecodeError as exc:
                pytest.fail(f"docs/book_index.json is not valid JSON: {exc}")
        assert isinstance(data, dict), "book_index.json root must be a JSON object"

    def test_book_index_has_parts(self):
        """Test that book_index.json contains a 'parts' key with entries."""
        index = DOCS_DIR / "book_index.json"
        with open(index, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        assert "parts" in data, "book_index.json must contain a 'parts' key"
        assert len(data["parts"]) > 0, "book_index.json 'parts' must not be empty"

    def test_book_index_parts_have_chapters(self):
        """Test that each part in book_index.json contains chapters."""
        index = DOCS_DIR / "book_index.json"
        with open(index, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        for part in data.get("parts", []):
            assert "chapters" in part, (
                f"Part '{part.get('id', 'unknown')}' is missing 'chapters' key"
            )
            assert len(part["chapters"]) > 0, (
                f"Part '{part.get('id', 'unknown')}' has no chapters"
            )

    def test_book_index_chapter_files_exist(self):
        """Test that files referenced in book_index.json actually exist."""
        index = DOCS_DIR / "book_index.json"
        with open(index, "r", encoding="utf-8") as fh:
            data = json.load(fh)

        missing = []
        for part in data.get("parts", []):
            for chapter in part.get("chapters", []):
                file_path = PROJECT_ROOT / chapter.get("file", "")
                if not file_path.exists():
                    missing.append(chapter.get("file"))

        assert not missing, (
            f"The following files referenced in book_index.json do not exist: {missing}"
        )


class TestConfigurationFiles:
    """Validate that key configuration files are present."""

    def test_mkdocs_yml_exists(self):
        """Test that mkdocs.yml exists in the project root."""
        config = PROJECT_ROOT / "mkdocs.yml"
        assert config.exists(), f"mkdocs.yml not found at {config}"

    def test_pandoc_yaml_exists(self):
        """Test that docs/pandoc.yaml exists."""
        config = DOCS_DIR / "pandoc.yaml"
        assert config.exists(), f"docs/pandoc.yaml not found at {config}"

    def test_package_json_exists(self):
        """Test that package.json exists for Node.js tooling."""
        config = PROJECT_ROOT / "package.json"
        assert config.exists(), f"package.json not found at {config}"

    def test_package_json_is_valid(self):
        """Test that package.json is valid JSON."""
        config = PROJECT_ROOT / "package.json"
        with open(config, "r", encoding="utf-8") as fh:
            try:
                data = json.load(fh)
            except json.JSONDecodeError as exc:
                pytest.fail(f"package.json is not valid JSON: {exc}")
        assert isinstance(data, dict), "package.json root must be a JSON object"

    def test_requirements_txt_exists(self):
        """Test that requirements.txt exists."""
        req = PROJECT_ROOT / "requirements.txt"
        assert req.exists(), f"requirements.txt not found at {req}"

    def test_book_requirements_md_exists(self):
        """Test that BOOK_REQUIREMENTS.md exists."""
        req = PROJECT_ROOT / "BOOK_REQUIREMENTS.md"
        assert req.exists(), f"BOOK_REQUIREMENTS.md not found at {req}"

    def test_makefile_exists(self):
        """Test that Makefile exists in the project root."""
        makefile = PROJECT_ROOT / "Makefile"
        assert makefile.exists(), f"Makefile not found at {makefile}"


class TestBookRequirements:
    """Validate that BOOK_REQUIREMENTS.md mentions required tools."""

    REQUIRED_TOOLS = ["pandoc", "python", "mermaid", "node", "mkdocs"]

    def _read_requirements_lower(self) -> str:
        req = PROJECT_ROOT / "BOOK_REQUIREMENTS.md"
        with open(req, "r", encoding="utf-8") as fh:
            return fh.read().lower()

    @pytest.mark.parametrize("tool", REQUIRED_TOOLS)
    def test_tool_mentioned_in_requirements(self, tool):
        """Test that required tool is mentioned in BOOK_REQUIREMENTS.md."""
        content = self._read_requirements_lower()
        assert tool in content, (
            f"Tool '{tool}' is not mentioned in BOOK_REQUIREMENTS.md"
        )


class TestOutputDirectories:
    """Validate that required output directories can be created."""

    REQUIRED_OUTPUT_DIRS = [
        "releases/book",
        "releases/presentation",
        "releases/whitepapers",
        "releases/website",
    ]

    @pytest.mark.parametrize("rel_path", REQUIRED_OUTPUT_DIRS)
    def test_output_directory_creatable(self, tmp_path, rel_path):
        """Test that required output directory path can be created."""
        # We don't create them in the real project; we create in tmp to check
        target = tmp_path / rel_path
        target.mkdir(parents=True, exist_ok=True)
        assert target.is_dir(), f"Could not create directory {rel_path}"

    def test_scripts_directory_exists(self):
        """Test that scripts/ directory exists."""
        scripts = PROJECT_ROOT / "scripts"
        assert scripts.is_dir(), f"scripts/ directory not found at {scripts}"

    def test_docs_directory_exists(self):
        """Test that docs/ directory exists."""
        assert DOCS_DIR.is_dir(), f"docs/ directory not found at {DOCS_DIR}"

    def test_tests_directory_exists(self):
        """Test that tests/ directory exists."""
        tests = PROJECT_ROOT / "tests"
        assert tests.is_dir(), f"tests/ directory not found at {tests}"
