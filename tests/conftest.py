"""Pytest configuration and shared fixtures for book content testing."""
import json
import os
from pathlib import Path
import pytest

try:  # pragma: no cover - exercised indirectly by the tests
    import yaml  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - triggered in CI environment
    yaml = None

from .utils.simple_yaml import safe_load as fallback_yaml_load

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
TESTS_DIR = PROJECT_ROOT / "tests"

@pytest.fixture(scope="session")
def project_root():
    """Project root directory."""
    return PROJECT_ROOT

@pytest.fixture(scope="session")
def docs_directory():
    """Docs directory containing markdown files."""
    return DOCS_DIR

def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--language",
        action="store",
        default="english",
        help="Language to test (default: english)"
    )

@pytest.fixture(scope="session")
def language(request):
    """Get the language from command line option."""
    return request.config.getoption("--language")

def _load_structured_file(path: Path):
    """Load a structured configuration file with graceful YAML fallback."""
    text = path.read_text(encoding="utf-8")
    if path.suffix in {".yaml", ".yml"}:
        if yaml is not None:
            return yaml.safe_load(text)
        return fallback_yaml_load(text)
    if path.suffix == ".json":
        return json.loads(text)
    raise ValueError(f"Unsupported configuration format: {path}")


@pytest.fixture(scope="session")
def requirements_config(language):
    """Load book requirements configuration based on language."""
    candidate_files = [
        TESTS_DIR / "requirements_en.yaml",
        TESTS_DIR / "requirements_en.yml",
        TESTS_DIR / "requirements_en.json",
        TESTS_DIR / "requirements.yaml",
        TESTS_DIR / "requirements.yml",
        TESTS_DIR / "requirements.json",
    ]

    for candidate in candidate_files:
        if candidate.exists():
            return _load_structured_file(candidate)

    raise FileNotFoundError("No requirements configuration file found")

@pytest.fixture(scope="session")
def chapter_files(docs_directory, language):
    """List all markdown chapter files for the specified language."""
    # Get all .md files but exclude README.md
    all_md_files = list(docs_directory.glob("*.md"))
    
    # List of non-chapter files to exclude
    non_chapter_files = {
        "README.md",
        "BOOK_COVER_DESIGN.md",
    }
    
    # Filter out non-chapter files
    chapter_files = [f for f in all_md_files if f.name not in non_chapter_files]
    
    return chapter_files

@pytest.fixture(scope="session")
def mermaid_files(docs_directory):
    """List all mermaid diagram files."""
    images_dir = docs_directory / "images"
    if images_dir.exists():
        return list(images_dir.glob("*.mmd"))
    return []

@pytest.fixture
def sample_chapter_content():
    """Sample valid chapter content for testing."""
    return """# Test Chapter Title

This is a sample chapter for testing purposes.

![Test Diagram](images/diagram_01_test.png)

This chapter contains multiple paragraphs to demonstrate the expected structure and content quality requirements.

## Section One

This is the first section with sufficient content to meet minimum requirements. The content should be clear and well-structured.

## Section Two

This is the second section that provides additional depth and ensures we meet the minimum subsection requirements.

Sources:
- Test Reference 1
- Test Reference 2
"""