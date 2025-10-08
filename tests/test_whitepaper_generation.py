#!/usr/bin/env python3
"""
Test whitepaper generation functionality.

This test validates that the generate_whitepapers.py script correctly processes
all chapter files and generates the expected number of whitepaper HTML files.
"""

import unittest
import os
import sys
import tempfile
import shutil
from pathlib import Path

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
    
    def test_chapter_mapping_complete(self):
        """Test that chapter mapping includes all expected files."""
        mapping = get_chapter_mapping()
        
        # Should have 31 chapters
        self.assertEqual(len(mapping), 31, f"Expected 31 chapters, got {len(mapping)}")
        
        # Check for key chapters
        expected_files = [
            '01_introduction.md',
            '05_automation_devops_cicd.md',
            '11_governance_as_code.md',
            '20_ai_agent_team.md',
            '23_soft_as_code_interplay.md',
            '31_technical_architecture.md'
        ]
        
        for expected_file in expected_files:
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
        
        self.assertEqual(overview['chapters_count'], 31, "Book overview should reflect 31 chapters")
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