#!/usr/bin/env python3
"""
Link Verification Script for Kodarkitektur Bokverkstad Repository

This script iterates through all links in the repository to verify if they contain
relevant information. It outputs a comprehensive report summarizing which links are
valid and provide relevant content, as well as flagging any broken or irrelevant links.

Usage:
    python3 scripts/verify_links.py [--output report.md] [--timeout 10]

Features:
    - Extracts links from markdown, TypeScript/TSX, and Python files
    - Verifies HTTP/HTTPS links with HEAD/GET requests
    - Checks internal markdown file references
    - Categorizes links (external, internal, localhost, etc.)
    - Generates detailed HTML and Markdown reports
    - Respects rate limiting and handles network errors gracefully
"""

import os
import re
import sys
import argparse
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path
from typing import List, Dict, Set, Tuple
from collections import defaultdict
import json
import time
from html import escape

class LinkVerifier:
    """Main class for link verification."""
    
    def __init__(self, repo_path: Path, timeout: int = 10, verbose: bool = False):
        """
        Initialize the link verifier.
        
        Args:
            repo_path: Path to the repository root
            timeout: Timeout for HTTP requests in seconds
            verbose: Enable verbose output
        """
        self.repo_path = repo_path
        self.timeout = timeout
        self.verbose = verbose
        self.results = {
            'valid': [],
            'broken': [],
            'skipped': [],
            'internal_valid': [],
            'internal_broken': []
        }
        self.link_cache = {}
        
    def log(self, message: str):
        """Print message if verbose mode is enabled."""
        if self.verbose:
            print(message)
    
    def extract_links_from_file(self, file_path: Path) -> List[Tuple[str, int, str]]:
        """
        Extract all links from a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            List of tuples (url, line_number, context)
        """
        links = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
                
                for line_num, line in enumerate(lines, 1):
                    # Extract markdown links [text](url)
                    markdown_links = re.findall(r'\[([^\]]*)\]\(([^)]+)\)', line)
                    for text, url in markdown_links:
                        links.append((url.strip(), line_num, f"[{text}]({url})"))
                    
                    # Extract plain HTTP/HTTPS URLs
                    plain_urls = re.findall(r'https?://[^\s\)\]<>"\']+', line)
                    for url in plain_urls:
                        # Skip if already captured in markdown link
                        if not any(url in link[0] for link in links if link[1] == line_num):
                            links.append((url.strip(), line_num, url))
                    
                    # Extract relative file paths in markdown links
                    rel_paths = re.findall(r'\[([^\]]*)\]\(([^)]*\.md[^)]*)\)', line)
                    for text, path in rel_paths:
                        if not path.startswith('http'):
                            links.append((path.strip(), line_num, f"[{text}]({path})"))
        
        except Exception as e:
            self.log(f"Error reading {file_path}: {e}")
        
        return links
    
    def find_all_files(self) -> List[Path]:
        """
        Find all files to scan for links.
        
        Returns:
            List of file paths
        """
        patterns = ['**/*.md', '**/*.tsx', '**/*.ts', '**/*.py']
        exclude_dirs = {'node_modules', 'dist', '.git', 'releases', 'exports', '__pycache__'}
        
        files = []
        for pattern in patterns:
            for file_path in self.repo_path.glob(pattern):
                # Skip files in excluded directories
                if any(excluded in file_path.parts for excluded in exclude_dirs):
                    continue
                files.append(file_path)
        
        return sorted(files)
    
    def categorize_link(self, url: str) -> str:
        """
        Categorize a link.
        
        Args:
            url: The URL to categorize
            
        Returns:
            Category string
        """
        if url.startswith('http://localhost') or url.startswith('http://127.0.0.1'):
            return 'localhost'
        elif url.startswith('https://') or url.startswith('http://'):
            return 'external'
        elif url.endswith('.md') or '/' in url:
            return 'internal'
        else:
            return 'other'
    
    def verify_http_link(self, url: str) -> Tuple[bool, str, int]:
        """
        Verify an HTTP/HTTPS link.
        
        Args:
            url: The URL to verify
            
        Returns:
            Tuple of (is_valid, message, status_code)
        """
        # Check cache first
        if url in self.link_cache:
            return self.link_cache[url]
        
        try:
            # Clean up the URL
            url = url.rstrip('.,;:')
            
            # Create request with headers
            req = urllib.request.Request(
                url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (compatible; LinkVerifier/1.0)',
                    'Accept': '*/*'
                }
            )
            
            # Try HEAD request first (faster)
            req.get_method = lambda: 'HEAD'
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as response:
                    status_code = response.status
                    result = (True, 'OK', status_code)
                    self.link_cache[url] = result
                    return result
            except urllib.error.HTTPError as e:
                # If HEAD fails, try GET
                if e.code in [405, 403]:
                    req.get_method = lambda: 'GET'
                    with urllib.request.urlopen(req, timeout=self.timeout) as response:
                        status_code = response.status
                        result = (True, 'OK', status_code)
                        self.link_cache[url] = result
                        return result
                else:
                    result = (False, f'HTTP Error {e.code}', e.code)
                    self.link_cache[url] = result
                    return result
        
        except urllib.error.URLError as e:
            result = (False, f'URL Error: {e.reason}', 0)
            self.link_cache[url] = result
            return result
        except Exception as e:
            result = (False, f'Error: {str(e)}', 0)
            self.link_cache[url] = result
            return result
    
    def verify_internal_link(self, url: str, source_file: Path) -> Tuple[bool, str]:
        """
        Verify an internal file reference.
        
        Args:
            url: The relative path
            source_file: The file containing the reference
            
        Returns:
            Tuple of (is_valid, message)
        """
        # Remove anchor if present
        path_part = url.split('#')[0]
        
        if not path_part:
            return (True, 'Anchor only (valid)')
        
        # Try to resolve the path
        try:
            # First, try relative to the source file's directory
            abs_path = (source_file.parent / path_part).resolve()
            if abs_path.exists():
                return (True, f'Found: {abs_path.relative_to(self.repo_path)}')
            
            # Try relative to repo root
            abs_path = (self.repo_path / path_part).resolve()
            if abs_path.exists():
                return (True, f'Found: {abs_path.relative_to(self.repo_path)}')
            
            return (False, f'File not found: {path_part}')
        
        except Exception as e:
            return (False, f'Error resolving path: {e}')
    
    def verify_all_links(self):
        """Verify all links in the repository."""
        print("Scanning repository for links...")
        files = self.find_all_files()
        print(f"Found {len(files)} files to scan")
        
        all_links = defaultdict(list)
        
        # Extract all links
        print("\nExtracting links from files...")
        for file_path in files:
            links = self.extract_links_from_file(file_path)
            if links:
                all_links[file_path] = links
                self.log(f"  {file_path.relative_to(self.repo_path)}: {len(links)} links")
        
        total_links = sum(len(links) for links in all_links.values())
        print(f"\nTotal links found: {total_links}")
        
        # Verify links
        print("\nVerifying links...")
        processed = 0
        
        for file_path, links in all_links.items():
            rel_path = file_path.relative_to(self.repo_path)
            
            for url, line_num, context in links:
                processed += 1
                if processed % 50 == 0:
                    print(f"  Processed {processed}/{total_links} links...")
                
                category = self.categorize_link(url)
                
                link_info = {
                    'url': url,
                    'file': str(rel_path),
                    'line': line_num,
                    'context': context,
                    'category': category
                }
                
                if category == 'localhost':
                    link_info['status'] = 'Skipped (localhost)'
                    self.results['skipped'].append(link_info)
                
                elif category == 'external':
                    is_valid, message, status = self.verify_http_link(url)
                    link_info['status'] = message
                    link_info['http_status'] = status
                    
                    if is_valid:
                        self.results['valid'].append(link_info)
                    else:
                        self.results['broken'].append(link_info)
                    
                    # Rate limiting
                    time.sleep(0.1)
                
                elif category == 'internal':
                    is_valid, message = self.verify_internal_link(url, file_path)
                    link_info['status'] = message
                    
                    if is_valid:
                        self.results['internal_valid'].append(link_info)
                    else:
                        self.results['internal_broken'].append(link_info)
                
                else:
                    link_info['status'] = 'Skipped (other)'
                    self.results['skipped'].append(link_info)
        
        print(f"\nVerification complete! Processed {processed} links.")
    
    def generate_markdown_report(self, output_path: Path):
        """Generate a Markdown report."""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Link Verification Report\n\n")
            f.write(f"**Generated:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Summary
            f.write("## Summary\n\n")
            f.write(f"- ✅ **Valid External Links:** {len(self.results['valid'])}\n")
            f.write(f"- ❌ **Broken External Links:** {len(self.results['broken'])}\n")
            f.write(f"- ✅ **Valid Internal Links:** {len(self.results['internal_valid'])}\n")
            f.write(f"- ❌ **Broken Internal Links:** {len(self.results['internal_broken'])}\n")
            f.write(f"- ⏭️ **Skipped Links:** {len(self.results['skipped'])}\n\n")
            
            total = sum(len(v) for v in self.results.values())
            f.write(f"**Total Links Checked:** {total}\n\n")
            
            # Broken external links
            if self.results['broken']:
                f.write("## ❌ Broken External Links\n\n")
                f.write("These links need attention:\n\n")
                for link in sorted(self.results['broken'], key=lambda x: x['file']):
                    f.write(f"### {link['url']}\n")
                    f.write(f"- **File:** `{link['file']}:{link['line']}`\n")
                    f.write(f"- **Status:** {link['status']}\n")
                    f.write(f"- **Context:** `{link['context']}`\n\n")
            
            # Broken internal links
            if self.results['internal_broken']:
                f.write("## ❌ Broken Internal Links\n\n")
                f.write("These file references are broken:\n\n")
                for link in sorted(self.results['internal_broken'], key=lambda x: x['file']):
                    f.write(f"### {link['url']}\n")
                    f.write(f"- **File:** `{link['file']}:{link['line']}`\n")
                    f.write(f"- **Status:** {link['status']}\n")
                    f.write(f"- **Context:** `{link['context']}`\n\n")
            
            # Valid external links
            if self.results['valid']:
                f.write("## ✅ Valid External Links\n\n")
                f.write(f"Found {len(self.results['valid'])} working external links.\n\n")
                f.write("<details>\n<summary>Click to expand</summary>\n\n")
                for link in sorted(self.results['valid'], key=lambda x: x['url']):
                    f.write(f"- {link['url']} (in `{link['file']}:{link['line']}`)\n")
                f.write("\n</details>\n\n")
            
            # Valid internal links
            if self.results['internal_valid']:
                f.write("## ✅ Valid Internal Links\n\n")
                f.write(f"Found {len(self.results['internal_valid'])} working internal file references.\n\n")
                f.write("<details>\n<summary>Click to expand</summary>\n\n")
                for link in sorted(self.results['internal_valid'], key=lambda x: x['url']):
                    f.write(f"- {link['url']} (in `{link['file']}:{link['line']}`)\n")
                f.write("\n</details>\n\n")
            
            # Skipped links
            if self.results['skipped']:
                f.write("## ⏭️ Skipped Links\n\n")
                f.write(f"These links were skipped (localhost, templates, etc.): {len(self.results['skipped'])}\n\n")
                f.write("<details>\n<summary>Click to expand</summary>\n\n")
                for link in sorted(self.results['skipped'], key=lambda x: x['url']):
                    f.write(f"- {link['url']} - {link['status']} (in `{link['file']}:{link['line']}`)\n")
                f.write("\n</details>\n\n")
    
    def generate_html_report(self, output_path: Path):
        """Generate an HTML report."""
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Link Verification Report</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        h1 { color: #333; border-bottom: 3px solid #4CAF50; padding-bottom: 10px; }
        h2 { color: #555; margin-top: 30px; }
        .summary {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 20px 0;
        }
        .summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }
        .summary-item {
            padding: 15px;
            border-radius: 5px;
            text-align: center;
        }
        .summary-item.valid { background: #e8f5e9; }
        .summary-item.broken { background: #ffebee; }
        .summary-item.skipped { background: #e3f2fd; }
        .summary-item h3 { margin: 0 0 10px 0; font-size: 2em; }
        .summary-item p { margin: 0; color: #666; }
        .link-list {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 20px 0;
        }
        .link-item {
            border-left: 4px solid #ddd;
            padding: 15px;
            margin: 10px 0;
            background: #f9f9f9;
        }
        .link-item.broken { border-left-color: #f44336; }
        .link-item.valid { border-left-color: #4CAF50; }
        .link-url {
            font-weight: bold;
            color: #1976d2;
            word-break: break-all;
        }
        .link-meta {
            font-size: 0.9em;
            color: #666;
            margin-top: 5px;
        }
        .link-status {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 0.85em;
            margin-top: 5px;
        }
        .link-status.ok { background: #c8e6c9; color: #2e7d32; }
        .link-status.error { background: #ffcdd2; color: #c62828; }
        details { margin: 20px 0; }
        summary {
            cursor: pointer;
            padding: 10px;
            background: #e0e0e0;
            border-radius: 5px;
            font-weight: bold;
        }
        summary:hover { background: #d0d0d0; }
        code {
            background: #f5f5f5;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }
    </style>
</head>
<body>
"""
        
        html += f"<h1>🔗 Link Verification Report</h1>\n"
        html += f"<p><strong>Generated:</strong> {time.strftime('%Y-%m-%d %H:%M:%S')}</p>\n"
        
        # Summary
        html += '<div class="summary">\n<h2>Summary</h2>\n<div class="summary-grid">\n'
        
        total = sum(len(v) for v in self.results.values())
        
        html += f'''
        <div class="summary-item valid">
            <h3>{len(self.results['valid'])}</h3>
            <p>Valid External Links</p>
        </div>
        <div class="summary-item broken">
            <h3>{len(self.results['broken'])}</h3>
            <p>Broken External Links</p>
        </div>
        <div class="summary-item valid">
            <h3>{len(self.results['internal_valid'])}</h3>
            <p>Valid Internal Links</p>
        </div>
        <div class="summary-item broken">
            <h3>{len(self.results['internal_broken'])}</h3>
            <p>Broken Internal Links</p>
        </div>
        <div class="summary-item skipped">
            <h3>{len(self.results['skipped'])}</h3>
            <p>Skipped Links</p>
        </div>
        <div class="summary-item">
            <h3>{total}</h3>
            <p>Total Links</p>
        </div>
        '''
        
        html += '</div>\n</div>\n'
        
        # Broken links section
        if self.results['broken']:
            html += '<div class="link-list">\n<h2>❌ Broken External Links</h2>\n'
            html += '<p>These links need attention:</p>\n'
            for link in sorted(self.results['broken'], key=lambda x: x['file']):
                html += f'<div class="link-item broken">\n'
                html += f'<div class="link-url">{escape(link["url"])}</div>\n'
                html += f'<div class="link-meta">File: <code>{escape(link["file"])}:{link["line"]}</code></div>\n'
                html += f'<div class="link-status error">{escape(link["status"])}</div>\n'
                html += f'<div class="link-meta">Context: <code>{escape(link["context"][:100])}</code></div>\n'
                html += '</div>\n'
            html += '</div>\n'
        
        # Broken internal links
        if self.results['internal_broken']:
            html += '<div class="link-list">\n<h2>❌ Broken Internal Links</h2>\n'
            html += '<p>These file references are broken:</p>\n'
            for link in sorted(self.results['internal_broken'], key=lambda x: x['file']):
                html += f'<div class="link-item broken">\n'
                html += f'<div class="link-url">{escape(link["url"])}</div>\n'
                html += f'<div class="link-meta">File: <code>{escape(link["file"])}:{link["line"]}</code></div>\n'
                html += f'<div class="link-status error">{escape(link["status"])}</div>\n'
                html += '</div>\n'
            html += '</div>\n'
        
        # Valid external links (collapsible)
        if self.results['valid']:
            html += '<details>\n<summary>✅ Valid External Links '
            html += f'({len(self.results["valid"])} links)</summary>\n'
            html += '<div class="link-list">\n'
            for link in sorted(self.results['valid'], key=lambda x: x['url']):
                html += f'<div class="link-item valid">\n'
                html += f'<div class="link-url">{escape(link["url"])}</div>\n'
                html += f'<div class="link-meta">File: <code>{escape(link["file"])}:{link["line"]}</code></div>\n'
                html += f'<div class="link-status ok">{escape(link["status"])}</div>\n'
                html += '</div>\n'
            html += '</div>\n</details>\n'
        
        # Valid internal links (collapsible)
        if self.results['internal_valid']:
            html += '<details>\n<summary>✅ Valid Internal Links '
            html += f'({len(self.results["internal_valid"])} links)</summary>\n'
            html += '<div class="link-list">\n'
            for link in sorted(self.results['internal_valid'], key=lambda x: x['url']):
                html += f'<div class="link-item valid">\n'
                html += f'<div class="link-url">{escape(link["url"])}</div>\n'
                html += f'<div class="link-meta">File: <code>{escape(link["file"])}:{link["line"]}</code></div>\n'
                html += '</div>\n'
            html += '</div>\n</details>\n'
        
        # Skipped links (collapsible)
        if self.results['skipped']:
            html += '<details>\n<summary>⏭️ Skipped Links '
            html += f'({len(self.results["skipped"])} links)</summary>\n'
            html += '<div class="link-list">\n'
            for link in sorted(self.results['skipped'], key=lambda x: x['url']):
                html += f'<div class="link-item">\n'
                html += f'<div class="link-url">{escape(link["url"])}</div>\n'
                html += f'<div class="link-meta">File: <code>{escape(link["file"])}:{link["line"]}</code></div>\n'
                html += f'<div class="link-meta">Reason: {escape(link["status"])}</div>\n'
                html += '</div>\n'
            html += '</div>\n</details>\n'
        
        html += """
</body>
</html>
"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
    
    def generate_json_report(self, output_path: Path):
        """Generate a JSON report."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Verify all links in the repository',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  python3 scripts/verify_links.py
  
  # Custom output location
  python3 scripts/verify_links.py --output reports/links.md
  
  # Increase timeout for slow links
  python3 scripts/verify_links.py --timeout 20
  
  # Verbose mode
  python3 scripts/verify_links.py --verbose
        """
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='link-verification-report',
        help='Output file path (without extension, generates .md, .html, .json)'
    )
    
    parser.add_argument(
        '--timeout',
        type=int,
        default=10,
        help='Timeout for HTTP requests in seconds (default: 10)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Get repository root
    script_dir = Path(__file__).parent
    repo_path = script_dir.parent
    
    print("=" * 70)
    print("Link Verification for Kodarkitektur Bokverkstad")
    print("=" * 70)
    print()
    
    # Create verifier and run
    verifier = LinkVerifier(repo_path, timeout=args.timeout, verbose=args.verbose)
    verifier.verify_all_links()
    
    # Generate reports
    print("\nGenerating reports...")
    
    output_base = Path(args.output)
    
    md_path = output_base.with_suffix('.md')
    verifier.generate_markdown_report(md_path)
    print(f"  ✅ Markdown report: {md_path}")
    
    html_path = output_base.with_suffix('.html')
    verifier.generate_html_report(html_path)
    print(f"  ✅ HTML report: {html_path}")
    
    json_path = output_base.with_suffix('.json')
    verifier.generate_json_report(json_path)
    print(f"  ✅ JSON report: {json_path}")
    
    print()
    print("=" * 70)
    print("Verification Summary")
    print("=" * 70)
    print(f"✅ Valid external links: {len(verifier.results['valid'])}")
    print(f"❌ Broken external links: {len(verifier.results['broken'])}")
    print(f"✅ Valid internal links: {len(verifier.results['internal_valid'])}")
    print(f"❌ Broken internal links: {len(verifier.results['internal_broken'])}")
    print(f"⏭️  Skipped links: {len(verifier.results['skipped'])}")
    print("=" * 70)
    
    # Exit with error code if broken links found
    if verifier.results['broken'] or verifier.results['internal_broken']:
        print("\n⚠️  Warning: Broken links detected!")
        return 1
    else:
        print("\n✅ All verified links are working!")
        return 0


if __name__ == '__main__':
    sys.exit(main())
