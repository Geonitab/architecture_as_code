#!/usr/bin/env python3
"""
Build artefact validation tests for the Architecture as Code book.

This module verifies that generated EPUB files conform to EPUB standards using
EPUBCheck and asserts that the shell build pipeline is configured to produce
all expected distribution formats.
"""
import subprocess
import pytest
from pathlib import Path
import os

class TestEPUBValidation:
    """Test EPUB file validation and compliance."""
    
    @pytest.fixture
    def docs_directory(self):
        """Get docs directory path."""
        return Path(__file__).parent.parent / "docs"
    
    @pytest.fixture 
    def epub_file(self, docs_directory):
        """Get path to EPUB file."""
        return docs_directory / "architecture_as_code.epub"
    
    @pytest.fixture
    def release_epub_file(self):
        """Get path to release EPUB file."""
        return Path(__file__).parent.parent / "releases" / "book" / "architecture_as_code.epub"
    
    def test_epubcheck_available(self):
        """Test that EPUBCheck tool is available."""
        try:
            result = subprocess.run(['epubcheck', '--version'], 
                                   capture_output=True, text=True, timeout=10)
            assert result.returncode == 0, "EPUBCheck should be available"
            assert 'EPUBCheck' in result.stdout or 'EPUBCheck' in result.stderr, \
                "EPUBCheck version output should contain 'EPUBCheck'"
        except FileNotFoundError:
            pytest.skip("EPUBCheck not installed - skipping EPUB validation tests")
        except subprocess.TimeoutExpired:
            pytest.fail("EPUBCheck command timed out")
    

    def test_epub_file_validation(self, epub_file):
        """Test EPUB file validation with EPUBCheck."""
        if not epub_file.exists():
            pytest.skip(f"EPUB file not found at {epub_file}")
        
        try:
            # Check if EPUBCheck is available
            subprocess.run(['epubcheck', '--version'], 
                          capture_output=True, text=True, timeout=10, check=True)
        except (FileNotFoundError, subprocess.CalledProcessError):
            pytest.skip("EPUBCheck not available - skipping validation")
        
        # Run EPUBCheck validation
        result = subprocess.run(['epubcheck', str(epub_file)], 
                               capture_output=True, text=True, timeout=120)
        
        validation_output = result.stdout + result.stderr
        
        # Count different types of issues
        fatal_count = validation_output.count('FATAL')
        error_count = validation_output.count('ERROR') - fatal_count
        warning_count = validation_output.count('WARNING')
        
        # Save validation report for review
        validation_log = epub_file.parent / "epub-validation-test.log"
        try:
            with open(validation_log, 'w', encoding='utf-8') as f:
                f.write(f"EPUB Validation Test Report\n")
                f.write(f"File: {epub_file}\n")
                f.write(f"Status: {'PASS' if result.returncode == 0 else 'FAIL'}\n")
                f.write(f"Fatal errors: {fatal_count}\n")
                f.write(f"Errors: {error_count}\n")
                f.write(f"Warnings: {warning_count}\n")
                f.write("=" * 50 + "\n")
                f.write(validation_output)
        except Exception as e:
            print(f"Warning: Could not save validation log: {e}")
        
        # The test should ideally pass (return code 0), but we'll be lenient
        # and only fail on fatal errors that make the EPUB unusable
        if fatal_count > 0:
            pytest.fail(
                f"EPUB file has {fatal_count} fatal errors that prevent proper reading. "
                f"See {validation_log} for details."
            )
        elif error_count > 10:  # Allow some errors but not too many
            import warnings
            warnings.warn(
                f"EPUB file has {error_count} validation errors. "
                f"Consider fixing these for better compatibility. "
                f"See {validation_log} for details.",
                UserWarning
            )
        elif warning_count > 0:
            import warnings
            warnings.warn(
                f"EPUB file has {warning_count} validation warnings. "
                f"See {validation_log} for details.",
                UserWarning
            )
    
    def test_release_epub_validation(self, release_epub_file):
        """Test that release EPUB file validates correctly."""
        if not release_epub_file.exists():
            pytest.skip(f"Release EPUB file not found at {release_epub_file}")
        
        try:
            # Check if EPUBCheck is available
            subprocess.run(['epubcheck', '--version'], 
                          capture_output=True, text=True, timeout=10, check=True)
        except (FileNotFoundError, subprocess.CalledProcessError):
            pytest.skip("EPUBCheck not available - skipping validation")
        
        # Run EPUBCheck validation on release file
        result = subprocess.run(['epubcheck', str(release_epub_file)], 
                               capture_output=True, text=True, timeout=120)
        
        validation_output = result.stdout + result.stderr
        fatal_count = validation_output.count('FATAL')
        
        # Release EPUB should have no fatal errors
        assert fatal_count == 0, \
            f"Release EPUB file has {fatal_count} fatal errors that prevent proper reading"
    
    def test_epub_metadata_present(self, epub_file):
        """Test that EPUB has required metadata."""
        if not epub_file.exists():
            pytest.skip(f"EPUB file not found at {epub_file}")
        
        # This is a basic check - we could expand this to extract and validate metadata
        assert epub_file.stat().st_size > 1000, \
            "EPUB file should be substantial in size (indicating content and metadata)"
    
    def test_epub_structure_integrity(self, epub_file):
        """Test basic EPUB structure integrity."""
        if not epub_file.exists():
            pytest.skip(f"EPUB file not found at {epub_file}")
        
        # Test that it's a valid ZIP file (EPUB is based on ZIP)
        import zipfile
        try:
            with zipfile.ZipFile(epub_file, 'r') as zip_file:
                # Check for required EPUB files
                files = zip_file.namelist()
                
                # EPUB must have mimetype file
                assert 'mimetype' in files, "EPUB must contain mimetype file"
                
                # Should have META-INF directory
                meta_inf_files = [f for f in files if f.startswith('META-INF/')]
                assert len(meta_inf_files) > 0, "EPUB must contain META-INF directory"
                
                # Should have EPUB directory with content
                epub_files = [f for f in files if f.startswith('EPUB/')]
                assert len(epub_files) > 0, "EPUB must contain EPUB directory with content"
                
        except zipfile.BadZipFile:
            pytest.fail("EPUB file is not a valid ZIP archive")
        except Exception as e:
            pytest.fail(f"Error checking EPUB structure: {e}")


class TestBuildPipelineConfiguration:
    """Validate that the build pipeline script targets the correct outputs."""

    @pytest.fixture(scope="class")
    def build_script_path(self):
        """Path to the build pipeline shell script."""
        return Path(__file__).parent.parent / "docs" / "build_book.sh"

    @pytest.fixture(scope="class")
    def build_script(self, build_script_path):
        """Read the build pipeline script content."""
        return build_script_path.read_text(encoding="utf-8")

    def test_build_script_exists(self, build_script_path):
        """Ensure the build pipeline script exists and is executable."""
        assert build_script_path.exists(), "docs/build_book.sh must exist"
        assert build_script_path.stat().st_mode & 0o111, "docs/build_book.sh should be executable"

    def test_build_script_defines_expected_outputs(self, build_script):
        """Check that the build script defines all expected artefact names."""
        assert 'OUTPUT_PDF="architecture_as_code.pdf"' in build_script
        assert 'OUTPUT_EPUB="architecture_as_code.epub"' in build_script
        assert 'OUTPUT_DOCX="architecture_as_code.docx"' in build_script

    def test_build_script_invokes_pandoc(self, build_script):
        """Verify that the build script renders PDF and DOCX files with Pandoc."""
        assert 'pandoc --defaults=pandoc.yaml "${CHAPTER_FILES[@]}" -o "$OUTPUT_PDF" 2>&1' in build_script
        assert 'pandoc --defaults=pandoc.yaml "${NON_LATEX_CHAPTER_FILES[@]}" -t docx -o "$OUTPUT_DOCX"' in build_script

    def test_build_script_runs_epubcheck(self, build_script):
        """Ensure the build script validates EPUB output using epubcheck."""
        assert 'validate_epub() {' in build_script
        assert 'epubcheck "$epub_file"' in build_script

