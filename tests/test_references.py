"""
Test for comprehensive references compilation.

Validates that all sources cited in chapters are included in the references section.
"""
import pytest
import re
from pathlib import Path


class TestReferences:
    """Test comprehensive references compilation."""
    
    def test_references_file_exists(self):
        """Test that the references file exists."""
        references_file = Path("docs/33_references.md")
        assert references_file.exists(), "References file docs/33_references.md must exist"
    
    def test_all_chapter_sources_in_references(self):
        """Test that all sources cited in chapters are in the references section."""
        # Read all chapter sources
        chapters_dir = Path("docs")
        chapter_files = sorted([f for f in chapters_dir.glob('[0-9]*.md') 
                               if f.name not in ['33_references.md', '32_finos_project_blueprint.md']])
        
        # Extract all sources from chapters
        all_chapter_sources = set()
        sources_by_chapter = {}
        
        for chapter_file in chapter_files:
            content = chapter_file.read_text(encoding='utf-8')
            
            # Find Sources section
            sources_match = re.search(
                r'^(?:Sources?|Källor?):\s*\n((?:^\s*-\s+.+\n?)*)', 
                content, 
                re.MULTILINE
            )
            
            if sources_match:
                sources_text = sources_match.group(1)
                sources = []
                for line in sources_text.split('\n'):
                    line = line.strip()
                    if line.startswith('-'):
                        source = line[1:].strip()
                        # Normalize source text for comparison
                        normalized_source = self._normalize_source(source)
                        sources.append(normalized_source)
                        all_chapter_sources.add(normalized_source)
                
                if sources:
                    sources_by_chapter[chapter_file.name] = sources
        
        # Read references file
        references_file = Path("docs/33_references.md")
        references_content = references_file.read_text(encoding='utf-8')
        
        # Extract all references from the references section
        # Look for lines starting with ** (bold) which indicate source entries
        reference_entries = re.findall(
            r'^\*\*(.+?)\.\*\*\s+(.+?)$',
            references_content,
            re.MULTILINE
        )
        
        # Also look for simple entries (non-bold format)
        simple_entries = re.findall(
            r'^\*\*(.+?)\*\*$',
            references_content,
            re.MULTILINE
        )
        
        # Build set of all references
        all_references = set()
        for author, rest in reference_entries:
            # Reconstruct the full reference
            full_ref = f"{author}. {rest}"
            normalized_ref = self._normalize_source(full_ref)
            all_references.add(normalized_ref)
        
        for entry in simple_entries:
            normalized_ref = self._normalize_source(entry)
            all_references.add(normalized_ref)
        
        # Check that all chapter sources are in references
        missing_sources = []
        for chapter, sources in sources_by_chapter.items():
            for source in sources:
                # Check if this source is in the references
                found = False
                for ref in all_references:
                    if self._sources_match(source, ref):
                        found = True
                        break
                
                if not found:
                    missing_sources.append({
                        'chapter': chapter,
                        'source': source
                    })
        
        assert not missing_sources, (
            f"The following sources are cited in chapters but missing from references:\n" +
            "\n".join([f"  {m['chapter']}: {m['source']}" for m in missing_sources])
        )
    
    def test_references_format_consistency(self):
        """Test that references follow a consistent format."""
        references_file = Path("docs/33_references.md")
        content = references_file.read_text(encoding='utf-8')
        
        # Check that references have proper structure
        assert "# References and Sources" in content, "Must have main heading"
        assert "## Academic and Industry Publications" in content or "## Industry Research" in content, \
            "Must have section headings"
        
        # Check for cross-references
        cross_refs = re.findall(r'\*Referenced in:', content)
        assert len(cross_refs) > 0, "References must include cross-references to chapters"
    
    def _normalize_source(self, source):
        """Normalize source text for comparison."""
        # Remove markdown links but keep the text
        normalized = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', source)
        # Remove extra whitespace
        normalized = re.sub(r'\s+', ' ', normalized.strip())
        # Remove trailing periods
        normalized = normalized.rstrip('.')
        return normalized
    
    def _sources_match(self, source1, source2):
        """Check if two sources match (allowing for minor formatting differences)."""
        # Exact match
        if source1 == source2:
            return True
        
        # Check if one contains the other (for different formatting)
        if source1 in source2 or source2 in source1:
            return True
        
        # Extract key parts for comparison
        # For "GitHub Docs – About protected branches" vs "GitHub Docs. \"About protected branches.\""
        # Extract organization/author and main title
        
        # Split by common delimiters and compare first parts
        delimiters = r'[–—\-\.]'
        parts1 = re.split(delimiters, source1, maxsplit=1)
        parts2 = re.split(delimiters, source2, maxsplit=1)
        
        if len(parts1) > 0 and len(parts2) > 0:
            # Compare first parts (organization/author)
            first1 = parts1[0].strip().lower()
            first2 = parts2[0].strip().lower()
            
            if first1 == first2:
                # Same author/org, check if titles are similar
                if len(parts1) > 1 and len(parts2) > 1:
                    # Remove quotes and extra formatting from titles
                    title1 = re.sub(r'["\']', '', parts1[1]).strip().lower()
                    title2 = re.sub(r'["\']', '', parts2[1]).strip().lower()
                    
                    # Check if titles match or contain each other
                    if title1 in title2 or title2 in title1:
                        return True
                    
                    # Check first few words of title
                    words1 = title1.split()[:3]
                    words2 = title2.split()[:3]
                    if words1 and words2 and words1 == words2:
                        return True
        
        return False
