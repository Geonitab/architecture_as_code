"""
Tests for source verification functionality.

This test suite validates that:
1. The source verification script can be run successfully
2. Sources are properly extracted from chapter files
3. URLs are verified correctly
4. ISBN validation works as expected
5. Reports are generated correctly
"""

import pytest
import json
from pathlib import Path
import sys
import subprocess

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "scripts"))

from verify_sources import SourceVerifier


class TestSourceVerification:
    """Test source verification functionality."""
    
    @pytest.fixture
    def docs_directory(self):
        """Get docs directory."""
        return project_root / "docs"
    
    @pytest.fixture
    def verifier(self):
        """Create a SourceVerifier instance."""
        return SourceVerifier(timeout=5)
    
    def test_source_extraction(self, verifier, docs_directory):
        """Test that sources can be extracted from chapter files."""
        # Test with a specific chapter file
        chapter_file = docs_directory / "01_introduction.md"
        
        if not chapter_file.exists():
            pytest.skip(f"Chapter file not found: {chapter_file}")
        
        sources = verifier.extract_sources_from_file(chapter_file)
        
        # Should extract at least some sources
        assert len(sources) > 0, "No sources found in 01_introduction.md"
        
        # Check source structure
        for source in sources:
            assert 'file' in source
            assert 'line' in source
            assert 'text' in source
            assert 'urls' in source
            assert 'isbn' in source
            assert 'type' in source
    
    def test_url_extraction(self, verifier):
        """Test URL extraction from source text."""
        # Test markdown link
        text1 = "[Example Link](https://example.com/page)"
        urls1 = verifier._extract_urls(text1)
        assert "https://example.com/page" in urls1
        
        # Test plain URL
        text2 = "See https://example.org for more info"
        urls2 = verifier._extract_urls(text2)
        assert "https://example.org" in urls2
        
        # Test mixed
        text3 = "[Link](https://site.com) and https://another.site/path"
        urls3 = verifier._extract_urls(text3)
        assert len(urls3) == 2
        assert "https://site.com" in urls3
        assert "https://another.site/path" in urls3
    
    def test_isbn_extraction(self, verifier):
        """Test ISBN extraction from source text."""
        # Test ISBN-10
        text1 = "Book Title. Publisher, 2020. ISBN: 0-123-45678-9"
        isbn1 = verifier._extract_isbn(text1)
        assert isbn1 == "0-123-45678-9"
        
        # Test ISBN-13
        text2 = "Another Book. ISBN-13: 978-0-123-45678-9"
        isbn2 = verifier._extract_isbn(text2)
        assert isbn2 == "978-0-123-45678-9"
        
        # Test no ISBN
        text3 = "Article without ISBN"
        isbn3 = verifier._extract_isbn(text3)
        assert isbn3 is None
    
    def test_isbn_validation(self, verifier):
        """Test ISBN format validation."""
        # Valid ISBN-10
        valid, msg = verifier.verify_isbn("0-123-45678-9")
        assert valid is True
        assert "ISBN-10" in msg
        
        # Valid ISBN-13
        valid, msg = verifier.verify_isbn("978-0-123-45678-9")
        assert valid is True
        assert "ISBN-13" in msg
        
        # Invalid ISBN (wrong length)
        valid, msg = verifier.verify_isbn("123-456")
        assert valid is False
        assert "Invalid" in msg
    
    def test_source_classification(self, verifier):
        """Test source type classification."""
        # URL source
        type1 = verifier._classify_source(
            "Example",
            ["https://example.com"],
            None
        )
        assert type1 == 'url'
        
        # Book source
        type2 = verifier._classify_source(
            "Book Title",
            [],
            "978-0-123-45678-9"
        )
        assert type2 == 'book'
        
        # Standard source
        type3 = verifier._classify_source(
            "NIST Special Publication 800-53",
            [],
            None
        )
        assert type3 == 'standard'
        
        # Other source
        type4 = verifier._classify_source(
            "Generic Reference",
            [],
            None
        )
        assert type4 == 'other'
    
    def test_url_verification_caching(self, verifier):
        """Test that URL verification results are cached."""
        url = "https://www.openpolicyagent.org/docs/latest/"
        
        # First verification
        result1 = verifier.verify_url(url)
        
        # Second verification should use cache
        result2 = verifier.verify_url(url)
        
        # Results should be identical
        assert result1 == result2
        
        # Should be in cache
        assert url in verifier.verified_urls
    
    def test_localhost_urls_skipped(self, verifier):
        """Test that localhost URLs are skipped."""
        url = "http://localhost:8080/test"
        valid, status = verifier.verify_url(url)
        
        assert valid is True
        assert "Skipped" in status
        assert "localhost" in status
    
    def test_template_variables_skipped(self, verifier):
        """Test that template variable URLs are skipped."""
        url = "https://${HOSTNAME}/path"
        valid, status = verifier.verify_url(url)
        
        assert valid is True
        assert "Skipped" in status
        assert "template" in status.lower()
    
    def test_script_runs_successfully(self, docs_directory):
        """Test that the verification script can be run."""
        script_path = project_root / "scripts" / "verify_sources.py"
        
        # Run with very short timeout and custom output to not interfere with main report
        result = subprocess.run(
            [
                sys.executable,
                str(script_path),
                "--timeout", "2",
                "--output", "/tmp/test-source-verification"
            ],
            capture_output=True,
            text=True
        )
        
        # Script should run (may exit with 1 if broken sources found)
        assert result.returncode in [0, 1], f"Script failed: {result.stderr}"
        
        # Should generate reports
        assert Path("/tmp/test-source-verification.md").exists()
        assert Path("/tmp/test-source-verification.json").exists()
    
    def test_report_json_structure(self):
        """Test that the JSON report has the correct structure."""
        # Use the test report if it exists
        report_path = Path("/tmp/test-source-verification.json")
        
        if not report_path.exists():
            pytest.skip("JSON report not found (run test_script_runs_successfully first)")
        
        with open(report_path, 'r', encoding='utf-8') as f:
            report = json.load(f)
        
        # Check top-level structure
        assert 'generated' in report
        assert 'summary' in report
        assert 'broken_sources' in report
        assert 'manual_verification_needed' in report
        assert 'verified_sources' in report
        
        # Check summary structure
        summary = report['summary']
        assert 'total' in summary
        assert 'verified' in summary
        assert 'broken' in summary
        assert 'manual_check' in summary
        
        # Check that totals make sense
        assert summary['total'] == (
            summary['verified'] + 
            summary['broken'] + 
            summary['manual_check']
        )
    
    def test_all_chapters_have_sources_or_exemption(self, docs_directory):
        """Test that all chapters have sources or are explicitly exempted."""
        # Chapters that don't require sources
        exempt_chapters = {
            'appendix_a_glossary.md',
            'appendix_b_about_the_authors.md',
            'appendix_c_code_examples.md',
            'appendix_d_technical_architecture.md'
        }
        
        verifier = SourceVerifier()
        
        # Get all numbered chapter files
        chapter_files = sorted(docs_directory.glob("*.md"))
        chapter_files = [f for f in chapter_files if f.name[0].isdigit()]
        
        chapters_without_sources = []
        
        for chapter_file in chapter_files:
            if chapter_file.name in exempt_chapters:
                continue
            
            sources = verifier.extract_sources_from_file(chapter_file)
            
            if len(sources) == 0:
                chapters_without_sources.append(chapter_file.name)
        
        # Warn if chapters are missing sources, but don't fail
        # (This is a soft requirement as content is still being developed)
        if chapters_without_sources:
            import warnings
            warnings.warn(
                f"Chapters missing sources sections: {chapters_without_sources}",
                UserWarning
            )
    
    def test_source_verification_comprehensive(self, verifier, docs_directory):
        """Test comprehensive source verification across all chapters."""
        # This is an integration test that scans the whole repository
        verifier.scan_repository(docs_directory)
        
        # Should find sources
        assert len(verifier.all_sources) > 0, "No sources found in any chapter"
        
        # Should categorize all sources
        total_categorized = (
            len(verifier.valid_sources) + 
            len(verifier.broken_sources) + 
            len(verifier.skipped_sources)
        )
        
        assert total_categorized == len(verifier.all_sources), \
            "Not all sources were categorized"
        
        # Report statistics for informational purposes
        print(f"\nSource Verification Statistics:")
        print(f"  Total sources: {len(verifier.all_sources)}")
        print(f"  Verified: {len(verifier.valid_sources)}")
        print(f"  Broken: {len(verifier.broken_sources)}")
        print(f"  Manual check needed: {len(verifier.skipped_sources)}")
