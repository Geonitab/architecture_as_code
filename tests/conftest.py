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

def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--language",
        action="store",
        default="svenska",
        help="Language to test: svenska or english"
    )

@pytest.fixture(scope="session")
def language(request):
    """Get the language from command line option."""
    return request.config.getoption("--language")

@pytest.fixture(scope="session")
def requirements_config(language):
    """Load book requirements configuration based on language."""
    if language == "english":
        requirements_file = TESTS_DIR / "requirements_en.yaml"
    else:
        requirements_file = TESTS_DIR / "requirements.yaml"
    with open(requirements_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

@pytest.fixture(scope="session")
def chapter_files(docs_directory, language):
    """List all markdown chapter files for the specified language."""
    # Get all .md files but exclude README.md
    all_md_files = list(docs_directory.glob("*.md"))
    
    # List of non-chapter files to exclude
    non_chapter_files = {
        "README.md", "README_en.md",
        "TERMINOLOGI_JUSTERING.md", "TERMINOLOGI_JUSTERING_en.md",
        "SVENGELSKA_FIXES_SUMMARY.md", "SVENGELSKA_FIXES_SUMMARY_en.md",
        "ENGELSKA_UTTRYCK_SAMMANSTÄLLNING.md", "ENGELSKA_UTTRYCK_SAMMANSTÄLLNING_en.md",
        "language_deviations_issue.md", "language_deviations_issue_en.md",
        "BOOK_COVER_DESIGN.md", "BOOK_COVER_DESIGN_en.md",
        "EPUB_VALIDATION.md", "EPUB_VALIDATION_en.md"
    }
    
    if language == "english":
        # Filter for English files (those ending with _en.md)
        chapter_files = [f for f in all_md_files if f.name.endswith("_en.md") and f.name not in non_chapter_files]
    else:
        # Filter for Swedish files (those NOT ending with _en.md)
        chapter_files = [f for f in all_md_files if not f.name.endswith("_en.md") and f.name not in non_chapter_files]
    
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

Källor:
- Test Reference 1
- Test Reference 2
"""