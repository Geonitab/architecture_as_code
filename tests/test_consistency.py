"""
Consistency validator for book content.

Validates uniform tone, style, and formatting across all chapters.
"""
import pytest
import re
from collections import Counter


class TestConsistency:
    """Test consistency in formatting, style, and structure."""
    
    def test_title_format_consistency(self, chapter_files, requirements_config):
        """Test that all chapters have consistent H1 title format."""
        max_title_length = requirements_config["structure"]["maximum_title_length"]
        
        title_issues = []
        for chapter_file in chapter_files:
            content = chapter_file.read_text(encoding='utf-8')
            lines = content.split('\n')
            
            # Find H1 title (should be first non-empty line)
            h1_title = None
            for line in lines:
                line = line.strip()
                if not line:
                    continue

                if line.startswith('\\') or line.startswith('<!--'):
                    # Allow LaTeX directives or HTML comments before the H1 title
                    continue

                if line.startswith('# '):
                    h1_title = line[2:].strip()
                    break

                title_issues.append({
                    "file": chapter_file.name,
                    "issue": "First content line is not H1 title"
                })
                break
            
            if h1_title:
                # Check title length
                if len(h1_title) > max_title_length:
                    title_issues.append({
                        "file": chapter_file.name,
                        "issue": f"Title too long: {len(h1_title)} > {max_title_length} chars"
                    })
                
                # Check title format (no trailing punctuation)
                if h1_title.endswith('.') or h1_title.endswith('!'):
                    title_issues.append({
                        "file": chapter_file.name,
                        "issue": "Title should not end with punctuation"
                    })
        
        assert not title_issues, f"Title format issues: {title_issues}"
    
    def test_header_hierarchy_consistency(self, chapter_files, requirements_config):
        """Test that header hierarchy is consistent (H1 -> H2 -> H3 -> H4)."""
        valid_hierarchy = requirements_config["quality"]["consistency"]["header_hierarchy"]
        fail_on_consistency = requirements_config.get("testing", {}).get("fail_on_consistency_issues", True)
        
        hierarchy_issues = []
        for chapter_file in chapter_files:
            content = chapter_file.read_text(encoding='utf-8')
            lines = content.split('\n')
            
            headers = []
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                if re.match(r'^#{1,6}\s+', line):
                    level = len(line) - len(line.lstrip('#'))
                    headers.append((line_num, level, line))
            
            # Check hierarchy (no skipping levels)
            prev_level = 0
            for line_num, level, header_text in headers:
                if level > prev_level + 1:
                    hierarchy_issues.append({
                        "file": chapter_file.name,
                        "line": line_num,
                        "issue": f"Header level {level} skips level {prev_level + 1}",
                        "header": header_text
                    })
                prev_level = level
        
        if hierarchy_issues:
            if fail_on_consistency:
                assert not hierarchy_issues, f"Header hierarchy issues: {hierarchy_issues}"
            else:
                import warnings
                warnings.warn(
                    f"Header hierarchy issues detected in {len(hierarchy_issues)} cases. Consider restructuring headers to follow H1->H2->H3 flow.",
                    UserWarning
                )
    
    def test_diagram_reference_consistency(self, chapter_files):
        """Test that diagram references follow consistent format."""
        diagram_issues = []
        expected_pattern = re.compile(r'!\[.*?\]\(images/diagram_\d{2}[a-z]?_.*?\.png\)')
        
        for chapter_file in chapter_files:
            content = chapter_file.read_text(encoding='utf-8')
            
            # Find all image references
            image_refs = re.findall(r'!\[.*?\]\([^)]+\)', content)
            
            for ref in image_refs:
                if 'images/' in ref and 'diagram_' in ref:
                    if not expected_pattern.search(ref):
                        diagram_issues.append({
                            "file": chapter_file.name,
                            "issue": f"Invalid diagram reference format: {ref}",
                            "expected": "![description](images/diagram_XX_name.png)"
                        })
        
        assert not diagram_issues, f"Diagram reference issues: {diagram_issues}"
    
    def test_sources_section_consistency(self, chapter_files):
        """Test that sources sections follow consistent format."""
        sources_issues = []
        
        for chapter_file in chapter_files:
            content = chapter_file.read_text(encoding='utf-8')
            
            # Remove code blocks to avoid false positives
            content_no_code = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
            content_no_code = re.sub(r'`[^`]+`', '', content_no_code)
            
            # Find sources section (accept both "Sources:" and "Källor:")
            # Must be at the start of a line
            sources_match = re.search(
                r'^((?:Sources?|Källor?):.*?)(?=\n\n|\n#|\Z)', 
                content_no_code, 
                re.IGNORECASE | re.DOTALL | re.MULTILINE
            )
            
            if sources_match:
                sources_text = sources_match.group(1)
                
                # Check format: should be "Sources:" or "Källor:" followed by list items
                if not re.search(r'(?:Sources?|Källor?):\s*\n\s*-', sources_text, re.IGNORECASE):
                    sources_issues.append({
                        "file": chapter_file.name,
                        "issue": "Sources section should use bullet list format",
                        "found": sources_text[:100] + "..."
                    })
        
        assert not sources_issues, f"Sources section issues: {sources_issues}"
    
    def test_language_consistency(self, chapter_files, requirements_config):
        """Test that content is consistently in the expected language."""
        language = requirements_config["book"]["language"]
        
        if language == "english":
            # Common Swedish words that shouldn't appear in English text
            wrong_language_indicators = [
                r'\boch\b', r'\batt\b', r'\bför\b', r'\bsom\b', r'\bmed\b',
                r'\bav\b', r'\btill\b', r'\bär\b', r'\bdet\b', r'\bden\b',
                r'\bi\b', r'\bpå\b', r'\bhan\b', r'\bhar\b', r'\bvar\b'
            ]
            issue_prefix = "Possible Swedish text detected"
        else:
            pytest.skip(f"Language consistency test not configured for language: {language}")
        
        language_issues = []
        for chapter_file in chapter_files:
            content = chapter_file.read_text(encoding='utf-8')
            
            # Skip code blocks and inline code
            content_no_code = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
            content_no_code = re.sub(r'`[^`]+`', '', content_no_code)
            
            for pattern in wrong_language_indicators:
                matches = list(re.finditer(pattern, content_no_code, re.IGNORECASE))
                if matches:
                    for match in matches[:3]:  # Limit to first 3 matches
                        context_start = max(0, match.start() - 30)
                        context_end = min(len(content_no_code), match.end() + 30)
                        context = content_no_code[context_start:context_end].strip()
                        
                        language_issues.append({
                            "file": chapter_file.name,
                            "issue": f"{issue_prefix}: '{match.group()}'",
                            "context": context
                        })
        
        # Only warn about language issues, don't fail the test
        if language_issues:
            import warnings
            warnings.warn(
                f"Potential language consistency issues: {len(language_issues)} found",
                UserWarning
            )
    
    def test_consistent_terminology(self, chapter_files):
        """Test for consistent use of technical terminology."""
        # Define preferred terminology
        terminology_preferences = {
            r'\bInfrastructure as Code\b': 'Infrastructure as Code',  # Keep English
            r'\bCI/CD\b': 'CI/CD',                                   # Keep abbreviation
        }
        
        terminology_issues = []
        for chapter_file in chapter_files:
            content = chapter_file.read_text(encoding='utf-8')
            
            # Check for mixed terminology usage
            for pattern, preferred in terminology_preferences.items():
                # This is just a warning check, not enforcing strict rules
                matches = list(re.finditer(pattern, content, re.IGNORECASE))
                if len(matches) > 0:
                    # Count variations to detect inconsistency
                    variations = set(match.group() for match in matches)
                    if len(variations) > 1:
                        terminology_issues.append({
                            "file": chapter_file.name,
                            "term": preferred,
                            "variations": list(variations),
                            "count": len(matches)
                        })
        
        # Only warn about terminology issues
        if terminology_issues:
            import warnings
            warnings.warn(
                f"Terminology variations detected in {len(terminology_issues)} cases",
                UserWarning
            )
    
    def test_chapter_length(self, chapter_files, requirements_config):
        """Test that each chapter meets minimum word count requirement."""
        minimum_words = requirements_config["structure"]["minimum_word_count"]
        fail_on_consistency = requirements_config.get("testing", {}).get("fail_on_consistency_issues", True)
        
        # Special chapters that may have different word count requirements
        special_chapters = requirements_config["book"].get("special_chapters", {})
        special_filenames = [
            special_chapters.get("ordlista", {}).get("filename", ""),
            special_chapters.get("authors", {}).get("filename", ""),
        ]
        
        short_chapters = []
        for chapter_file in chapter_files:
            content = chapter_file.read_text(encoding='utf-8')
            
            # Skip special chapters that don't need to meet word count requirements
            if chapter_file.name in special_filenames:
                continue
            
            # Extract text content and count words
            word_count = self._count_content_words(content)
            
            if word_count < minimum_words:
                short_chapters.append({
                    "file": chapter_file.name,
                    "word_count": word_count,
                    "minimum_required": minimum_words
                })
        
        if short_chapters:
            if fail_on_consistency:
                assert not short_chapters, (
                    f"Chapters below minimum word count ({minimum_words} words): {short_chapters}"
                )
            else:
                import warnings
                warnings.warn(
                    f"Chapters below minimum word count detected: {len(short_chapters)} chapters under {minimum_words} words. Consider expanding content.",
                    UserWarning
                )
    
    def test_chapter_length_variance(self, chapter_files, requirements_config):
        """Test that no chapter exceeds 100% variance (2x) of the average chapter length."""
        fail_on_consistency = requirements_config.get("testing", {}).get("fail_on_consistency_issues", True)
        
        # Special chapters that may have different requirements
        special_chapters = requirements_config["book"].get("special_chapters", {})
        special_filenames = [
            special_chapters.get("ordlista", {}).get("filename", ""),
            special_chapters.get("authors", {}).get("filename", ""),
        ]
        
        # Collect word counts for all chapters (excluding special chapters)
        chapter_stats = []
        total_words = 0
        
        for chapter_file in chapter_files:
            # Skip special chapters
            if chapter_file.name in special_filenames:
                continue
            
            content = chapter_file.read_text(encoding='utf-8')
            word_count = self._count_content_words(content)
            
            chapter_stats.append({
                "file": chapter_file.name,
                "word_count": word_count,
            })
            total_words += word_count
        
        if not chapter_stats:
            pytest.skip("No regular chapters found to analyze")
        
        # Calculate average
        avg_words = total_words / len(chapter_stats)
        max_allowed = avg_words * 2  # 100% variance = 2x the mean
        
        # Find chapters that exceed the threshold
        excessive_chapters = []
        for stat in chapter_stats:
            if stat["word_count"] > max_allowed:
                variance_ratio = stat["word_count"] / avg_words
                stat["avg_words"] = avg_words
                stat["max_allowed"] = max_allowed
                stat["variance_ratio"] = variance_ratio
                excessive_chapters.append(stat)
        
        # Generate detailed message
        if excessive_chapters:
            msg_parts = [
                f"\nChapter length variance check failed:",
                f"Average chapter length: {avg_words:.0f} words",
                f"Maximum allowed (2x mean): {max_allowed:.0f} words",
                f"\nChapters exceeding threshold ({len(excessive_chapters)}):"
            ]
            
            for ch in excessive_chapters:
                msg_parts.append(
                    f"  - {ch['file']}: {ch['word_count']} words "
                    f"({ch['variance_ratio']:.2f}x the mean, "
                    f"{ch['word_count'] - max_allowed:.0f} words over limit)"
                )
            
            msg_parts.append("\nRecommended actions:")
            msg_parts.append("  1. Review content for potential split into multiple chapters")
            msg_parts.append("  2. Consider moving detailed examples to appendices")
            msg_parts.append("  3. Identify sections that could be condensed")
            msg_parts.append("  4. See reports/chapter_length_analysis.md for full analysis")
            
            error_msg = "\n".join(msg_parts)
            
            if fail_on_consistency:
                assert not excessive_chapters, error_msg
            else:
                import warnings
                warnings.warn(
                    f"Chapter length variance detected: {len(excessive_chapters)} chapter(s) exceed 2x mean length. {error_msg}",
                    UserWarning
                )
    
    def _count_content_words(self, content):
        """Count actual content words, excluding markdown formatting and code blocks."""
        # Remove code blocks (both fenced and indented)
        content_no_code = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
        content_no_code = re.sub(r'^ {4,}.*$', '', content_no_code, flags=re.MULTILINE)
        
        # Remove inline code
        content_no_code = re.sub(r'`[^`]*`', '', content_no_code)
        
        # Remove headers (they are structural, not content)
        content_no_code = re.sub(r'^#{1,6}\s+.*$', '', content_no_code, flags=re.MULTILINE)
        
        # Remove image references
        content_no_code = re.sub(r'!\[.*?\]\([^)]*\)', '', content_no_code)
        
        # Remove links but keep link text
        content_no_code = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', content_no_code)
        
        # Remove markdown formatting characters
        content_no_code = re.sub(r'[*_~`#\[\]()!-]', ' ', content_no_code)
        
        # Split into words and count non-empty words
        words = content_no_code.split()
        return len([word for word in words if word.strip()])