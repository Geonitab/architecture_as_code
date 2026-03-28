#!/usr/bin/env python3
"""
Source Verification Script for Architecture as Code Book

This script verifies all cited sources throughout the manuscript:
- Checks URL accessibility (HTTP/HTTPS links)
- Validates ISBN format (for books)
- Identifies archive entries and other references
- Generates comprehensive reports

Usage:
    python3 scripts/verify_sources.py [--timeout 10] [--output reports/sources]
"""

import os
import re
import sys
import json
import time
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Set
from urllib.parse import urlparse
import urllib.request
from urllib.error import URLError, HTTPError
import socket

# Allow importing navigation from the same scripts/ directory.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from navigation import REPO_ROOT, get_book_build_files  # noqa: E402

# Configuration
DEFAULT_TIMEOUT = 10
DEFAULT_OUTPUT = "source-verification-report"
USER_AGENT = "Architecture-as-Code-Book-Source-Verifier/1.0"


class SourceVerifier:
    """Verify sources cited in book chapters."""
    
    def __init__(self, timeout: int = DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.verified_urls = {}  # Cache for URL verification results
        self.all_sources = []
        self.broken_sources = []
        self.valid_sources = []
        self.skipped_sources = []
        
    def extract_sources_from_file(self, file_path: Path) -> List[Dict]:
        """Extract all sources from a markdown file."""
        sources = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')
            
            in_sources_section = False
            source_section_indent = 0
            
            for line_num, line in enumerate(lines, 1):
                # Detect sources section
                if re.match(r'^(##\s+)?Sources?(\s+and\s+[Rr]eferences)?:?\s*$', line, re.IGNORECASE):
                    in_sources_section = True
                    source_section_indent = 0
                    continue
                    
                # Check for subsection headers within sources (like "### Academic sources")
                if in_sources_section and re.match(r'^###\s+', line):
                    continue
                
                # Exit sources section if we hit another main section
                if in_sources_section and re.match(r'^##\s+(?!.*[Ss]ources)', line):
                    in_sources_section = False
                    continue
                
                # Extract source entries
                if in_sources_section:
                    # Match list items (- or * prefix)
                    match = re.match(r'^[-*]\s+(.+)$', line)
                    if match:
                        source_text = match.group(1).strip()
                        
                        # Extract URLs from the source text
                        urls = self._extract_urls(source_text)
                        
                        # Extract ISBN if present
                        isbn = self._extract_isbn(source_text)
                        
                        source_entry = {
                            'file': file_path.name,
                            'line': line_num,
                            'text': source_text,
                            'urls': urls,
                            'isbn': isbn,
                            'type': self._classify_source(source_text, urls, isbn)
                        }
                        
                        sources.append(source_entry)
        
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
        
        return sources
    
    def _extract_urls(self, text: str) -> List[str]:
        """Extract all URLs from text."""
        urls = []
        
        # Match markdown links [text](url)
        markdown_links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', text)
        for _, url in markdown_links:
            if url.startswith('http://') or url.startswith('https://'):
                urls.append(url)
        
        # Match plain URLs
        plain_urls = re.findall(r'https?://[^\s\)\]]+', text)
        urls.extend(plain_urls)
        
        return list(set(urls))  # Remove duplicates
    
    def _extract_isbn(self, text: str) -> str:
        """Extract ISBN from text if present."""
        # Match ISBN-10 or ISBN-13
        isbn_match = re.search(r'ISBN(?:-1[03])?[:\s]*([\d-]{10,17})', text, re.IGNORECASE)
        if isbn_match:
            return isbn_match.group(1)
        return None
    
    def _classify_source(self, text: str, urls: List[str], isbn: str) -> str:
        """Classify the source type."""
        if urls:
            return 'url'
        elif isbn:
            return 'book'
        elif any(keyword in text.lower() for keyword in ['nist', 'iso', 'standard', 'specification']):
            return 'standard'
        elif any(keyword in text.lower() for keyword in ['arxiv', 'doi', 'journal', 'proceedings']):
            return 'academic'
        else:
            return 'other'
    
    def verify_url(self, url: str) -> Tuple[bool, str]:
        """Verify if a URL is accessible."""
        # Check cache first
        if url in self.verified_urls:
            return self.verified_urls[url]
        
        # Skip localhost and template variables
        if 'localhost' in url or '127.0.0.1' in url:
            result = (True, 'Skipped (localhost)')
            self.verified_urls[url] = result
            return result
        
        if '${' in url or '{{' in url:
            result = (True, 'Skipped (template variable)')
            self.verified_urls[url] = result
            return result
        
        try:
            # Create request with user agent
            req = urllib.request.Request(url)
            req.add_header('User-Agent', USER_AGENT)
            
            # Try HEAD request first (faster)
            req.get_method = lambda: 'HEAD'
            
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                status = response.status
                if status == 200:
                    result = (True, f'OK ({status})')
                else:
                    result = (True, f'Accessible ({status})')
                self.verified_urls[url] = result
                return result
                
        except HTTPError as e:
            # Some servers don't support HEAD, try GET
            if e.code == 405 or e.code == 501:
                try:
                    req = urllib.request.Request(url)
                    req.add_header('User-Agent', USER_AGENT)
                    
                    with urllib.request.urlopen(req, timeout=self.timeout) as response:
                        status = response.status
                        result = (True, f'OK ({status})')
                        self.verified_urls[url] = result
                        return result
                except Exception as e2:
                    result = (False, f'Error: {str(e2)}')
                    self.verified_urls[url] = result
                    return result
            
            # Treat 429 (rate limiting) as accessible but temporarily unavailable
            if e.code == 429:
                result = (True, f'Rate limited (429) - likely valid but temporarily unavailable')
                self.verified_urls[url] = result
                return result
            
            result = (False, f'HTTP {e.code}: {e.reason}')
            self.verified_urls[url] = result
            return result
            
        except URLError as e:
            if isinstance(e.reason, socket.timeout):
                result = (False, 'Timeout')
            else:
                result = (False, f'URL Error: {e.reason}')
            self.verified_urls[url] = result
            return result
            
        except socket.timeout:
            result = (False, 'Timeout')
            self.verified_urls[url] = result
            return result
            
        except Exception as e:
            result = (False, f'Error: {str(e)}')
            self.verified_urls[url] = result
            return result
    
    def verify_isbn(self, isbn: str) -> Tuple[bool, str]:
        """Validate ISBN format."""
        # Remove hyphens and spaces
        isbn_clean = re.sub(r'[-\s]', '', isbn)
        
        # Check ISBN-10
        if len(isbn_clean) == 10:
            if re.match(r'^\d{9}[\dX]$', isbn_clean):
                return (True, 'Valid ISBN-10 format')
            else:
                return (False, 'Invalid ISBN-10 format')
        
        # Check ISBN-13
        elif len(isbn_clean) == 13:
            if re.match(r'^\d{13}$', isbn_clean):
                return (True, 'Valid ISBN-13 format')
            else:
                return (False, 'Invalid ISBN-13 format')
        
        else:
            return (False, f'Invalid ISBN length: {len(isbn_clean)}')
    
    def verify_source(self, source: Dict) -> Dict:
        """Verify a single source entry."""
        result = {
            'source': source,
            'verified': False,
            'status': 'Unknown',
            'details': []
        }
        
        # Verify URLs
        if source['urls']:
            url_results = []
            for url in source['urls']:
                is_valid, status = self.verify_url(url)
                url_results.append({
                    'url': url,
                    'valid': is_valid,
                    'status': status
                })
                
                if not is_valid and 'Skipped' not in status:
                    result['details'].append(f"❌ URL broken: {url} - {status}")
                elif is_valid and 'Skipped' not in status:
                    result['details'].append(f"✅ URL accessible: {url}")
                else:
                    result['details'].append(f"⏭️  URL skipped: {url} - {status}")
            
            # Source is verified if at least one URL is valid
            result['verified'] = any(r['valid'] for r in url_results)
            result['url_results'] = url_results
        
        # Verify ISBN
        if source['isbn']:
            is_valid, status = self.verify_isbn(source['isbn'])
            result['details'].append(f"{'✅' if is_valid else '❌'} ISBN: {source['isbn']} - {status}")
            if is_valid:
                result['verified'] = True
        
        # For sources without URLs or ISBNs, mark as "needs manual verification"
        if not source['urls'] and not source['isbn']:
            result['verified'] = False
            result['status'] = 'No verifiable identifiers (manual check needed)'
            result['details'].append(f"⚠️  {result['status']}")
        else:
            if result['verified']:
                result['status'] = 'Verified'
            else:
                result['status'] = 'Broken or inaccessible'
        
        return result
    
    # ------------------------------------------------------------------
    # Reference-anchor helpers (new in #1761)
    # ------------------------------------------------------------------

    _ANCHOR_HTML_RE = re.compile(r'<a\s+id="source-(\d+)"')
    # Pandoc span: [anything]{#source-N} — matched via the closing ]{#source-N}
    # because the span text may contain nested brackets (e.g. [**Source [1]:**])
    _ANCHOR_PANDOC_RE = re.compile(r'\]\{#source-(\d+)\}')
    _STANDARD_SOURCES_HDR_RE = re.compile(r'^## Sources\s*$', re.MULTILINE)
    _INLINE_CITE_RE = re.compile(r'\[Source \[(\d+)\]\]\(33_references\.md#source-\d+\)')
    _ANY_SOURCE_BRACKET_RE = re.compile(r'\[Source \[')

    def load_reference_anchors(self, references_path: Path) -> Set[int]:
        """Return the set of source numbers declared as anchors in references.md."""
        if not references_path.exists():
            return set()
        text = references_path.read_text(encoding='utf-8')
        html_ids = {int(m) for m in self._ANCHOR_HTML_RE.findall(text)}
        pandoc_ids = {int(m) for m in self._ANCHOR_PANDOC_RE.findall(text)}
        return html_ids | pandoc_ids

    def validate_chapter_citations(
        self, chapter_path: Path, defined_anchors: Set[int]
    ) -> List[Dict]:
        """
        Find all [Source [N]] occurrences in *chapter_path* and report those
        whose number N has no corresponding anchor in docs/33_references.md.

        Returns a list of dicts with keys: file, line, text, source_number.
        """
        broken: List[Dict] = []
        if not chapter_path.exists():
            return broken
        try:
            text = chapter_path.read_text(encoding='utf-8')
        except Exception as exc:
            print(f"Warning: could not read {chapter_path}: {exc}")
            return broken

        for line_no, line in enumerate(text.splitlines(), start=1):
            for match in self._INLINE_CITE_RE.finditer(line):
                n = int(match.group(1))
                if n not in defined_anchors:
                    broken.append({
                        'file': chapter_path.name,
                        'line': line_no,
                        'text': match.group(0),
                        'source_number': n,
                    })
        return broken

    def validate_sources_header(self, chapter_path: Path) -> bool:
        """Return True when the chapter has a standard ``## Sources`` section."""
        if not chapter_path.exists():
            return False
        try:
            text = chapter_path.read_text(encoding='utf-8')
        except Exception:
            return False
        return bool(self._STANDARD_SOURCES_HDR_RE.search(text))

    # ------------------------------------------------------------------
    # End of new helpers
    # ------------------------------------------------------------------

    def scan_repository(self, docs_dir: Path) -> None:
        """Scan all canonical chapter files and verify sources."""
        print(f"Scanning {docs_dir} for sources...")

        # Use the canonical navigation to build the file list so that all
        # chapters (including appendices) are covered, not just 01_–27_ files.
        try:
            book_files = get_book_build_files()
        except Exception as exc:
            print(f"Warning: could not load navigation — falling back to glob. {exc}")
            book_files = None

        if book_files is not None:
            # Resolve to absolute paths; exclude part-introduction pages from
            # citation/header checks but keep them for URL scanning.
            chapter_files = [
                docs_dir / f
                for f in book_files
                if not Path(f).stem.startswith('part_')
            ]
        else:
            # Legacy fallback: two-digit-prefixed files only.
            chapter_files = sorted(
                f for f in docs_dir.glob("*.md")
                if re.match(r'^\d{2}_', f.name)
            )

        # Always include 33_references.md for URL verification.
        refs_file = docs_dir / "33_references.md"
        if refs_file.exists() and refs_file not in chapter_files:
            chapter_files.append(refs_file)

        print(f"Found {len(chapter_files)} chapter files\n")

        # Load reference anchors once for citation validation.
        defined_anchors = self.load_reference_anchors(refs_file)

        # Validate ## Sources headers and citation formats.
        self.missing_sources_headers: List[str] = []
        self.broken_citation_refs: List[Dict] = []

        refs_stem = refs_file.stem  # "33_references"
        for ch_file in chapter_files:
            # Skip the references file itself from header/citation checks.
            if ch_file.stem == refs_stem:
                continue
            if not self.validate_sources_header(ch_file):
                self.missing_sources_headers.append(ch_file.name)
            broken = self.validate_chapter_citations(ch_file, defined_anchors)
            self.broken_citation_refs.extend(broken)
        
        # Extract sources from all files
        for chapter_file in chapter_files:
            sources = self.extract_sources_from_file(chapter_file)
            self.all_sources.extend(sources)
        
        print(f"Extracted {len(self.all_sources)} source citations\n")
        
        # Verify each source
        print("Verifying sources...")
        for i, source in enumerate(self.all_sources, 1):
            if i % 10 == 0:
                print(f"  Processed {i}/{len(self.all_sources)} sources...")
            
            result = self.verify_source(source)
            
            if result['verified']:
                self.valid_sources.append(result)
            else:
                if result['status'] == 'No verifiable identifiers (manual check needed)':
                    self.skipped_sources.append(result)
                else:
                    self.broken_sources.append(result)
            
            # Rate limiting
            time.sleep(0.1)
        
        print(f"Verification complete! Processed {len(self.all_sources)} sources.\n")
    
    def generate_summary(self) -> str:
        """Generate summary statistics."""
        total = len(self.all_sources)
        valid = len(self.valid_sources)
        broken = len(self.broken_sources)
        skipped = len(self.skipped_sources)

        # New validation counts (default to 0 if scan_repository not yet called).
        missing_hdrs = len(getattr(self, 'missing_sources_headers', []))
        broken_cites = len(getattr(self, 'broken_citation_refs', []))

        summary = f"""
======================================================================
Source Verification Summary
======================================================================
Total sources cited: {total}
Verified and accessible: {valid}
Broken or inaccessible: {broken}
Needs manual verification: {skipped}
----------------------------------------------------------------------
Chapters missing ## Sources section: {missing_hdrs}
Broken citation references (anchor not in 33_references.md): {broken_cites}
======================================================================
"""
        return summary
    
    def generate_markdown_report(self, output_path: str) -> None:
        """Generate markdown report."""
        report_path = f"{output_path}.md"

        missing_hdrs = getattr(self, 'missing_sources_headers', [])
        broken_cites = getattr(self, 'broken_citation_refs', [])

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Source Verification Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            # Summary
            f.write("## Summary\n\n")
            f.write(f"- **Total sources cited:** {len(self.all_sources)}\n")
            f.write(f"- **Verified and accessible:** {len(self.valid_sources)}\n")
            f.write(f"- **Broken or inaccessible:** {len(self.broken_sources)}\n")
            f.write(f"- **Needs manual verification:** {len(self.skipped_sources)}\n")
            f.write(f"- **Chapters missing `## Sources` section:** {len(missing_hdrs)}\n")
            f.write(
                f"- **Broken citation references (anchor not in 33_references.md):**"
                f" {len(broken_cites)}\n\n"
            )

            # Missing ## Sources headers
            if missing_hdrs:
                f.write("## Chapters Missing `## Sources` Section\n\n")
                f.write(
                    "These chapters are in the canonical chapter list but do not have a "
                    "`## Sources` section:\n\n"
                )
                for name in missing_hdrs:
                    f.write(f"- `{name}`\n")
                f.write("\n")

            # Broken citation references
            if broken_cites:
                f.write("## Broken Citation References\n\n")
                f.write(
                    "These inline citations reference a source number that has no corresponding "
                    "anchor in `docs/33_references.md`:\n\n"
                )
                for item in broken_cites:
                    f.write(
                        f"- `{item['file']}` line {item['line']}: "
                        f"`{item['text']}` — Source [{item['source_number']}] not anchored\n"
                    )
                f.write("\n")
            
            # Broken sources
            if self.broken_sources:
                f.write("## ❌ Broken or Inaccessible Sources\n\n")
                f.write("These sources require updates or replacements:\n\n")
                
                for result in self.broken_sources:
                    source = result['source']
                    f.write(f"### {source['file']} (Line {source['line']})\n\n")
                    f.write(f"**Citation:** {source['text']}\n\n")
                    f.write(f"**Type:** {source['type']}\n\n")
                    f.write("**Details:**\n")
                    for detail in result['details']:
                        f.write(f"- {detail}\n")
                    f.write("\n")
            
            # Manual verification needed
            if self.skipped_sources:
                f.write("## ⚠️ Sources Requiring Manual Verification\n\n")
                f.write("These sources lack URLs or ISBNs and need manual checking:\n\n")
                
                for result in self.skipped_sources:
                    source = result['source']
                    f.write(f"### {source['file']} (Line {source['line']})\n\n")
                    f.write(f"**Citation:** {source['text']}\n\n")
                    f.write(f"**Type:** {source['type']}\n\n")
                    f.write("\n")
            
            # Valid sources
            f.write("## ✅ Verified Sources\n\n")
            f.write(f"Total: {len(self.valid_sources)} sources verified successfully.\n\n")
            
            f.write("<details>\n<summary>Click to expand verified sources list</summary>\n\n")
            
            current_file = None
            for result in self.valid_sources:
                source = result['source']
                if source['file'] != current_file:
                    if current_file is not None:
                        f.write("\n")
                    f.write(f"### {source['file']}\n\n")
                    current_file = source['file']
                
                f.write(f"- **Line {source['line']}:** {source['text']}\n")
            
            f.write("\n</details>\n\n")
            
            # Recommendations
            f.write("## Recommendations\n\n")
            if self.broken_sources:
                f.write(f"1. **Update or replace {len(self.broken_sources)} broken sources**\n")
                f.write("   - Review each broken source listed above\n")
                f.write("   - Find alternative sources or updated URLs\n")
                f.write("   - Update chapter files accordingly\n\n")
            
            if self.skipped_sources:
                f.write(f"2. **Manually verify {len(self.skipped_sources)} sources without URLs/ISBNs**\n")
                f.write("   - Check if books, standards, and reports are accessible\n")
                f.write("   - Consider adding URLs or ISBNs for future verification\n\n")
            
            f.write("3. **Regular verification**\n")
            f.write("   - Run this script periodically to catch new broken links\n")
            f.write("   - Integrate into CI/CD pipeline for automatic checks\n\n")
        
        print(f"✅ Markdown report: {report_path}")
    
    def generate_json_report(self, output_path: str) -> None:
        """Generate JSON report."""
        report_path = f"{output_path}.json"
        
        missing_hdrs = getattr(self, 'missing_sources_headers', [])
        broken_cites = getattr(self, 'broken_citation_refs', [])

        report = {
            'generated': datetime.now().isoformat(),
            'summary': {
                'total': len(self.all_sources),
                'verified': len(self.valid_sources),
                'broken': len(self.broken_sources),
                'manual_check': len(self.skipped_sources),
                'missing_sources_headers': len(missing_hdrs),
                'broken_citation_refs': len(broken_cites),
            },
            'missing_sources_headers': missing_hdrs,
            'broken_citation_refs': broken_cites,
            'broken_sources': [
                {
                    'file': r['source']['file'],
                    'line': r['source']['line'],
                    'text': r['source']['text'],
                    'type': r['source']['type'],
                    'status': r['status'],
                    'details': r['details']
                }
                for r in self.broken_sources
            ],
            'manual_verification_needed': [
                {
                    'file': r['source']['file'],
                    'line': r['source']['line'],
                    'text': r['source']['text'],
                    'type': r['source']['type']
                }
                for r in self.skipped_sources
            ],
            'verified_sources': [
                {
                    'file': r['source']['file'],
                    'line': r['source']['line'],
                    'text': r['source']['text'],
                    'type': r['source']['type']
                }
                for r in self.valid_sources
            ]
        }
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"✅ JSON report: {report_path}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Verify all cited sources in the Architecture as Code book'
    )
    parser.add_argument(
        '--timeout',
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f'Timeout for URL requests in seconds (default: {DEFAULT_TIMEOUT})'
    )
    parser.add_argument(
        '--output',
        type=str,
        default=DEFAULT_OUTPUT,
        help=f'Output file prefix (default: {DEFAULT_OUTPUT})'
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("Source Verification for Architecture as Code")
    print("=" * 70)
    print()
    
    # Find docs directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    docs_dir = project_root / "docs"
    
    if not docs_dir.exists():
        print(f"Error: docs directory not found at {docs_dir}")
        sys.exit(1)
    
    # Create verifier and scan
    verifier = SourceVerifier(timeout=args.timeout)
    verifier.scan_repository(docs_dir)
    
    # Print summary
    print(verifier.generate_summary())
    
    # Generate reports
    print("Generating reports...")
    verifier.generate_markdown_report(args.output)
    verifier.generate_json_report(args.output)
    
    print("\nDone!")
    
    # Exit with error code if broken sources or broken citation references found.
    broken_cites = getattr(verifier, 'broken_citation_refs', [])
    if verifier.broken_sources or broken_cites:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
