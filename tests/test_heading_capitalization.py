"""
Test heading capitalization in markdown files.

Validates that all headings start with uppercase letters.
"""
import pytest
import re
from pathlib import Path


class TestHeadingCapitalization:
    """Test that all markdown headings start with uppercase letters."""
    
    def test_heading_capitalization_in_docs(self, docs_directory):
        """Test that all headings in docs/ start with uppercase letters."""
        # Import the validation logic from the script
        from scripts.validate_heading_capitalization import check_file
        
        # Find all markdown files in docs directory
        md_files = list(docs_directory.rglob('*.md'))
        
        assert len(md_files) > 0, "No markdown files found in docs directory"
        
        files_with_issues = []
        
        for md_file in md_files:
            issues = check_file(md_file)
            if issues:
                files_with_issues.append((md_file, issues))
        
        # Build detailed error message
        if files_with_issues:
            error_parts = ["\nHeadings starting with lowercase letters found:\n"]
            for file_path, issues in files_with_issues:
                rel_path = file_path.relative_to(docs_directory.parent)
                error_parts.append(f"\n📄 {rel_path}")
                for line_num, line in issues:
                    error_parts.append(f"  Line {line_num}: {line}")
            
            error_message = '\n'.join(error_parts)
            error_message += f"\n\nTotal: {sum(len(issues) for _, issues in files_with_issues)} issues in {len(files_with_issues)} file(s)"
            pytest.fail(error_message)
    
    def test_heading_validation_logic(self):
        """Test the heading validation logic with specific examples."""
        from scripts.validate_heading_capitalization import is_heading_properly_capitalized
        
        # Valid headings (should return True)
        assert is_heading_properly_capitalized("# Proper Heading")
        assert is_heading_properly_capitalized("## Another Proper Heading")
        assert is_heading_properly_capitalized("### Yet Another Heading")
        assert is_heading_properly_capitalized("# 123 Number starts are OK")
        assert is_heading_properly_capitalized("# @Special character starts are OK")
        assert is_heading_properly_capitalized("# `Code` at start is OK")
        assert is_heading_properly_capitalized("Not a heading")
        
        # Invalid headings (should return False)
        assert not is_heading_properly_capitalized("# lowercase heading")
        assert not is_heading_properly_capitalized("## another lowercase")
        assert not is_heading_properly_capitalized("### yet another lowercase")
    
    def test_code_block_filtering(self, tmp_path):
        """Test that code blocks are properly filtered out."""
        from scripts.validate_heading_capitalization import check_file
        
        # Create a test markdown file with code blocks
        test_file = tmp_path / "test.md"
        test_file.write_text("""# Valid Heading

Some content here.

```python
# this is a code comment, not a heading
def function():
    pass
```

## Another Valid Heading

```yaml
# another code comment
key: value
```

## invalid heading here

More content.
""", encoding='utf-8')
        
        issues = check_file(test_file)
        
        # Should only find one issue: the "invalid heading here"
        assert len(issues) == 1
        assert issues[0][1] == "## invalid heading here"
