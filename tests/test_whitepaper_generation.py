#!/usr/bin/env python3
"""
Test whitepaper generation functionality.

These tests validate that the ``generate_whitepapers.py`` script correctly
reflects the current Architecture as Code manuscript and generates the expected
whitepaper outputs for every numbered chapter in ``docs/``.
"""

import unittest
import os
import sys
import tempfile
import shutil
from pathlib import Path

import yaml

# Add parent directory to path to import the script
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generate_whitepapers import (
    get_chapter_mapping, 
    get_book_overview, 
    read_chapter_content,
    generate_whitepapers
)

class TestWhitepaperGeneration(unittest.TestCase):
    """Test whitepaper generation functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.original_cwd = os.getcwd()
        # Change to repository root
        repo_root = Path(__file__).parent.parent
        os.chdir(repo_root)
    
    def tearDown(self):
        """Clean up test environment."""
        os.chdir(self.original_cwd)
    
    def _load_requirements_config(self):
        """Load requirements front matter as a dictionary."""
        requirements_path = Path("BOOK_REQUIREMENTS.md")

        if not requirements_path.exists():
            return {}

        lines = requirements_path.read_text(encoding="utf-8").splitlines()
        if not lines or lines[0].strip() != "---":
            return {}

        front_matter = []
        for line in lines[1:]:
            if line.strip() == "---":
                break
            front_matter.append(line)

        return yaml.safe_load("\n".join(front_matter)) or {}

    def _canonical_chapters(self):
        """Return the canonical chapter filenames defined in requirements."""
        config = self._load_requirements_config()
        return [
            chapter["filename"]
            for chapter in config.get("book", {}).get("chapters", [])
            if chapter.get("filename")
        ]

    def test_chapter_mapping_complete(self):
        """Test that the chapter mapping covers every numbered chapter file."""
        mapping = get_chapter_mapping()
        numbered_chapters = self._canonical_chapters()

        self.assertEqual(
            len(mapping),
            len(numbered_chapters),
            (
                "Chapter mapping should include all numbered chapters. "
                f"Expected {len(numbered_chapters)}, got {len(mapping)}"
            ),
        )

        missing = sorted(set(numbered_chapters) - set(mapping.keys()))
        extras = sorted(set(mapping.keys()) - set(numbered_chapters))

        self.assertFalse(missing, f"Mapping missing chapters: {missing}")
        self.assertFalse(extras, f"Mapping contains unexpected chapters: {extras}")

        for expected_file in numbered_chapters[:6]:
            self.assertIn(expected_file, mapping, f"Missing expected file: {expected_file}")
    
    def test_chapter_mapping_matches_actual_files(self):
        """Test that all files in mapping actually exist in docs/."""
        mapping = get_chapter_mapping()
        docs_dir = Path("docs")

        for filename in mapping.keys():
            file_path = docs_dir / filename
            self.assertTrue(file_path.exists(), f"Mapped file does not exist: {file_path}")
    
    def test_book_overview_updated(self):
        """Test that book overview has correct chapter count."""
        overview = get_book_overview()
        numbered_chapters = self._canonical_chapters()

        self.assertEqual(
            overview['chapters_count'],
            len(numbered_chapters),
            (
                "Book overview chapter count should match the number of "
                f"numbered chapters (expected {len(numbered_chapters)})"
            ),
        )
        self.assertIn('title', overview)
        self.assertIn('subtitle', overview)
        self.assertIn('description', overview)
    
    def test_read_chapter_content_handles_missing_title(self):
        """Test that read_chapter_content handles files without H1 titles."""
        # Create a temporary file without H1 title
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("This is a test chapter without H1 title.\n")
            f.write("## Section 1\n")
            f.write("Some content here.\n")
            temp_file = f.name
        
        try:
            result = read_chapter_content(temp_file)
            self.assertIsNotNone(result)
            self.assertIn('title', result)
            # Should generate title from filename
            self.assertTrue(len(result['title']) > 0)
            self.assertIn('condensed_content', result)
            self.assertIn('section_headers', result)
        finally:
            os.unlink(temp_file)
    
    def test_read_chapter_content_handles_minimal_content(self):
        """Test that read_chapter_content handles files with minimal content."""
        # Create a temporary file with minimal content
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("# Test Chapter\n")
            f.write("Short content.\n")
            temp_file = f.name
        
        try:
            result = read_chapter_content(temp_file)
            self.assertIsNotNone(result)
            self.assertEqual(result['title'], 'Test Chapter')
            # Should have fallback content and headers
            self.assertTrue(len(result['condensed_content']) > 0)
            self.assertTrue(len(result['section_headers']) > 0)
        finally:
            os.unlink(temp_file)
    
    def test_whitepaper_generation_creates_all_files(self):
        """Test that whitepaper generation creates files for all mapped chapters."""
        # Use a temporary directory for output
        with tempfile.TemporaryDirectory() as temp_dir:
            # Change the current working directory temporarily
            original_whitepapers_dir = Path("whitepapers")
            temp_whitepapers_dir = Path(temp_dir) / "whitepapers"
            
            # Backup existing whitepapers if they exist
            backup_dir = None
            if original_whitepapers_dir.exists():
                backup_dir = Path(temp_dir) / "backup_whitepapers"
                shutil.copytree(original_whitepapers_dir, backup_dir)
                shutil.rmtree(original_whitepapers_dir)
            
            try:
                # Generate whitepapers
                success = generate_whitepapers(release_mode=False)
                self.assertTrue(success, "Whitepaper generation should succeed")
                
                # Check that whitepapers directory was created
                self.assertTrue(original_whitepapers_dir.exists(), "Whitepapers directory should be created")
                
                # Count generated files
                generated_files = list(original_whitepapers_dir.glob("*.html"))
                mapping = get_chapter_mapping()
                
                self.assertEqual(len(generated_files), len(mapping), 
                               f"Should generate {len(mapping)} whitepapers, got {len(generated_files)}")
                
                # Check that each mapped chapter has a corresponding whitepaper
                for chapter_file in mapping.keys():
                    expected_whitepaper = chapter_file.replace('.md', '_whitepaper.html')
                    whitepaper_path = original_whitepapers_dir / expected_whitepaper
                    self.assertTrue(whitepaper_path.exists(), 
                                  f"Missing whitepaper for {chapter_file}: {whitepaper_path}")
                    
                    # Check that file is not empty
                    self.assertGreater(whitepaper_path.stat().st_size, 1000, 
                                     f"Whitepaper file should be substantial: {whitepaper_path}")
            
            finally:
                # Clean up and restore backup if needed
                if original_whitepapers_dir.exists():
                    shutil.rmtree(original_whitepapers_dir)
                if backup_dir and backup_dir.exists():
                    shutil.copytree(backup_dir, original_whitepapers_dir)


if __name__ == '__main__':
    unittest.main()