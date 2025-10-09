"""
Pytest configuration and shared fixtures for book content testing.
"""
import os
from pathlib import Path

import pytest
import yaml

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

def _load_markdown_front_matter(path: Path) -> dict:
    """Extract YAML front matter from a markdown file."""
    with open(path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    if not lines or lines[0].strip() != "---":
        raise ValueError(f"File {path} does not start with YAML front matter")

    front_matter_lines = []
    for line in lines[1:]:
        if line.strip() == "---":
            break
        front_matter_lines.append(line)
    else:
        raise ValueError(f"File {path} is missing closing YAML front matter delimiter")

    data = yaml.safe_load("".join(front_matter_lines))
    if not isinstance(data, dict):
        raise ValueError(f"Front matter in {path} did not produce a dictionary")
    return data


@pytest.fixture(scope="session")
def requirements_config(language):
    """Load book requirements configuration from the markdown requirements file."""
    requirements_file = PROJECT_ROOT / "BOOK_REQUIREMENTS.md"
    return _load_markdown_front_matter(requirements_file)

@pytest.fixture(scope="session")
def chapter_files(docs_directory, requirements_config):
    """List canonical chapter files defined in the requirements specification."""
    book_config = requirements_config.get("book", {})

    # Canonical chapters are the numbered entries in the requirements file
    canonical_filenames = {
        chapter["filename"]
        for chapter in book_config.get("chapters", [])
        if chapter.get("filename")
    }

    # Collect matching markdown files from docs/
    chapter_paths = [
        path
        for path in docs_directory.glob("*.md")
        if path.name in canonical_filenames
    ]

    # Sort for deterministic ordering across tests
    return sorted(chapter_paths, key=lambda path: path.name)

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