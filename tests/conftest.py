"""
Pytest configuration and shared fixtures for book content testing.
"""
import os
import yaml
from pathlib import Path
import pytest

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

@pytest.fixture(scope="session")
def requirements_config():
    """Load book requirements configuration."""
    requirements_file = TESTS_DIR / "requirements.yaml"
    with open(requirements_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

@pytest.fixture(scope="session")
def chapter_files(docs_directory):
    """List all markdown chapter files."""
    return list(docs_directory.glob("*.md"))

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

Källor:
- Test Reference 1
- Test Reference 2
"""