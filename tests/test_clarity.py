"""
Clarity validator for book content.

Identifies ambiguities, unclear content, and readability issues.
"""
import pytest
import re
from pathlib import Path


class TestClarity:
    """Test content clarity and readability."""
    
    def test_minimum_content_length(self, chapter_files, requirements_config):
        """Test that chapters meet minimum content length requirements."""
        min_length = requirements_config["structure"]["minimum_content_length"]
        
        short_chapters = []
        for chapter_file in chapter_files:
            content = chapter_file.read_text(encoding='utf-8')
            
            # Remove whitespace and count actual content
            content_cleaned = re.sub(r'\s+', ' ', content).strip()
            # Remove markdown formatting for character count
            content_text = re.sub(r'[#*`\[\]()!-]', '', content_cleaned)
            
            actual_length = len(content_text)
            if actual_length < min_length:
                short_chapters.append({
                    "file": chapter_file.name,
                    "length": actual_length,
                    "minimum": min_length
                })
        
        assert not short_chapters, (
            f"Chapters below minimum length: {short_chapters}"
        )
    
    def test_minimum_paragraphs(self, chapter_files, requirements_config):
        """Test that chapters have sufficient paragraph structure."""
        min_paragraphs = requirements_config["quality"]["clarity"]["min_paragraphs"]
        
        insufficient_chapters = []
        for chapter_file in chapter_files:
            content = chapter_file.read_text(encoding='utf-8')
            
            # Split by double newlines to find paragraphs
            paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
            
            # Filter out headers, code blocks, and very short paragraphs
            content_paragraphs = []
            for p in paragraphs:
                # Skip headers
                if p.startswith('#'):
                    continue
                # Skip code blocks
                if p.startswith('```') or p.startswith('!['):
                    continue
                # Skip very short paragraphs (likely lists or metadata)
                if len(p.split()) < 10:
                    continue
                content_paragraphs.append(p)
            
            if len(content_paragraphs) < min_paragraphs:
                insufficient_chapters.append({
                    "file": chapter_file.name,
                    "paragraphs": len(content_paragraphs),
                    "minimum": min_paragraphs
                })
        
        assert not insufficient_chapters, (
            f"Chapters with insufficient paragraphs: {insufficient_chapters}"
        )
    
    def test_minimum_subsections(self, chapter_files, requirements_config):
        """Test that chapters have sufficient subsection structure."""
        min_subsections = requirements_config["quality"]["clarity"]["required_subsections"]
        
        insufficient_chapters = []
        for chapter_file in chapter_files:
            content = chapter_file.read_text(encoding='utf-8')
            
            # Count H2 headers (## Section)
            h2_headers = re.findall(r'^## .+', content, re.MULTILINE)
            
            if len(h2_headers) < min_subsections:
                insufficient_chapters.append({
                    "file": chapter_file.name,
                    "subsections": len(h2_headers),
                    "minimum": min_subsections
                })
        
        assert not insufficient_chapters, (
            f"Chapters with insufficient subsections: {insufficient_chapters}"
        )
    
    def test_sentence_length_readability(self, chapter_files, requirements_config):
        """Test for overly long sentences that hurt readability."""
        max_sentence_length = requirements_config["quality"]["clarity"]["max_sentence_length"]
        
        long_sentence_issues = []
        for chapter_file in chapter_files:
            content = chapter_file.read_text(encoding='utf-8')
            
            # Extract text content (remove headers, code blocks, etc.)
            text_content = content
            # Remove headers
            text_content = re.sub(r'^#+ .+$', '', text_content, flags=re.MULTILINE)
            # Remove code blocks
            text_content = re.sub(r'```.*?```', '', text_content, flags=re.DOTALL)
            # Remove inline code
            text_content = re.sub(r'`[^`]+`', '', text_content)
            # Remove image references
            text_content = re.sub(r'!\[.*?\]\([^)]+\)', '', text_content)
            
            # Split into sentences (simple approach)
            sentences = re.split(r'[.!?]+\s+', text_content)
            
            long_sentences = []
            for sentence in sentences:
                sentence = sentence.strip()
                if len(sentence) > max_sentence_length:
                    long_sentences.append({
                        "length": len(sentence),
                        "text": sentence[:100] + "..." if len(sentence) > 100 else sentence
                    })
            
            if long_sentences:
                long_sentence_issues.append({
                    "file": chapter_file.name,
                    "count": len(long_sentences),
                    "examples": long_sentences[:2]  # Show first 2 examples
                })
        
        # This is a warning, not a failure
        if long_sentence_issues:
            import warnings
            warnings.warn(
                f"Long sentences detected in {len(long_sentence_issues)} chapters",
                UserWarning
            )
    
    def test_unclear_terminology_usage(self, chapter_files):
        """Test for potentially unclear or inconsistent terminology."""
        # Common unclear phrases that should be clarified
        unclear_phrases = [
            r'\bdet\b(?!\s+(?:är|var|blir|kan|ska|kommer|skulle))',  # Vague "det"
            r'\bsådana?\b(?!\s+(?:som|här|där))',  # Vague "sådana"
            r'\bandra\b(?!\s+(?:ord|sidan|delen))',  # Vague "andra"
            r'\betc\.?$',  # Avoid "etc" - be specific
            r'\boch så vidare\b',  # Avoid "och så vidare" - be specific
        ]
        
        clarity_issues = []
        for chapter_file in chapter_files:
            content = chapter_file.read_text(encoding='utf-8')
            
            # Remove code blocks to avoid false positives
            content_no_code = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
            content_no_code = re.sub(r'`[^`]+`', '', content_no_code)
            
            for pattern in unclear_phrases:
                matches = list(re.finditer(pattern, content_no_code, re.IGNORECASE))
                if matches:
                    for match in matches[:2]:  # Limit examples
                        context_start = max(0, match.start() - 40)
                        context_end = min(len(content_no_code), match.end() + 40)
                        context = content_no_code[context_start:context_end].strip()
                        
                        clarity_issues.append({
                            "file": chapter_file.name,
                            "issue": "Potentially unclear terminology",
                            "term": match.group(),
                            "context": context
                        })
        
        # Only warn about clarity issues
        if clarity_issues:
            import warnings
            warnings.warn(
                f"Potentially unclear terminology in {len(clarity_issues)} cases",
                UserWarning
            )
    
    def test_chapter_flow_indicators(self, chapter_files):
        """Test for flow indicators and transitions between sections."""
        flow_indicators = [
            r'\bdärför\b', r'\bsåledes\b', r'\bmed andra ord\b',
            r'\bexempelvis\b', r'\btill exempel\b', r'\bdet vill säga\b',
            r'\bsamtidigt\b', r'\bdessutom\b', r'\bå andra sidan\b'
        ]
        
        chapters_without_flow = []
        for chapter_file in chapter_files:
            content = chapter_file.read_text(encoding='utf-8')
            
            # Count flow indicators
            flow_count = 0
            for pattern in flow_indicators:
                flow_count += len(re.findall(pattern, content, re.IGNORECASE))
            
            # Check if chapter has sufficient flow indicators relative to length
            word_count = len(content.split())
            expected_flow_ratio = 0.005  # ~1 indicator per 200 words
            
            if word_count > 300 and flow_count / word_count < expected_flow_ratio:
                chapters_without_flow.append({
                    "file": chapter_file.name,
                    "flow_indicators": flow_count,
                    "word_count": word_count,
                    "ratio": flow_count / word_count
                })
        
        # This is informational, not a hard failure
        if chapters_without_flow:
            import warnings
            warnings.warn(
                f"Chapters with limited flow indicators: {len(chapters_without_flow)}",
                UserWarning
            )