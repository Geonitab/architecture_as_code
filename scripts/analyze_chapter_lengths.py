#!/usr/bin/env python3
"""
Analyze Chapter Length Distribution

This script measures the length of every chapter and identifies any that exceed
the allowed variance relative to the average chapter length.

Tasks:
- Calculate the average chapter length based on word counts
- Compare each chapter against the average and highlight any that are more than 
  100% longer (over 2x the mean)
- Provide recommended edits or splits for any chapters breaching the threshold
"""

import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple


def count_content_words(content: str) -> int:
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


def extract_chapter_title(content: str) -> str:
    """Extract the chapter title from markdown content."""
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('# '):
            return line[2:].strip()
    return "Untitled"


def analyze_chapters(docs_dir: Path) -> Tuple[List[Dict], Dict]:
    """
    Analyze all chapter files and return statistics.
    
    Returns:
        Tuple of (chapter_stats, summary_stats)
    """
    # Get all numbered chapter files
    chapter_files = sorted([f for f in docs_dir.glob('[0-9]*.md') if f.is_file()])
    
    if not chapter_files:
        print("ERROR: No chapter files found in docs directory!")
        sys.exit(1)
    
    chapter_stats = []
    total_words = 0
    
    # Collect word counts for all chapters
    for chapter_file in chapter_files:
        content = chapter_file.read_text(encoding='utf-8')
        word_count = count_content_words(content)
        title = extract_chapter_title(content)
        
        chapter_stats.append({
            'filename': chapter_file.name,
            'title': title,
            'word_count': word_count,
        })
        total_words += word_count
    
    # Calculate statistics
    num_chapters = len(chapter_stats)
    avg_words = total_words / num_chapters if num_chapters > 0 else 0
    max_allowed = avg_words * 2  # 100% variance = 2x the mean
    
    # Identify outliers
    for stat in chapter_stats:
        stat['percentage_of_avg'] = (stat['word_count'] / avg_words * 100) if avg_words > 0 else 0
        stat['exceeds_threshold'] = stat['word_count'] > max_allowed
        stat['variance_ratio'] = stat['word_count'] / avg_words if avg_words > 0 else 0
    
    summary_stats = {
        'total_chapters': num_chapters,
        'total_words': total_words,
        'average_words': avg_words,
        'max_allowed_words': max_allowed,
        'outliers': [s for s in chapter_stats if s['exceeds_threshold']],
    }
    
    return chapter_stats, summary_stats


def generate_recommendations(chapter_stats: List[Dict], avg_words: float) -> List[str]:
    """Generate recommendations for chapters that exceed the threshold."""
    recommendations = []
    
    for stat in chapter_stats:
        if stat['exceeds_threshold']:
            ratio = stat['variance_ratio']
            excess_words = stat['word_count'] - (avg_words * 2)
            
            recommendations.append(f"""
**{stat['filename']} - {stat['title']}**
- Current length: {stat['word_count']} words ({stat['percentage_of_avg']:.1f}% of average)
- Variance ratio: {ratio:.2f}x the mean (exceeds 2x threshold)
- Excess words: {excess_words:.0f} words over the limit

Recommended actions:
1. Review content for potential split into multiple chapters
2. Consider moving detailed examples to appendices or separate documents
3. Identify sections that could be condensed without losing key information
4. Evaluate if some technical details could be referenced rather than fully explained
""")
    
    return recommendations


def print_report(chapter_stats: List[Dict], summary_stats: Dict, recommendations: List[str]):
    """Print a comprehensive report to console."""
    print("=" * 80)
    print("CHAPTER LENGTH DISTRIBUTION ANALYSIS")
    print("=" * 80)
    print()
    
    print("SUMMARY STATISTICS")
    print("-" * 80)
    print(f"Total chapters analyzed: {summary_stats['total_chapters']}")
    print(f"Total word count: {summary_stats['total_words']:,} words")
    print(f"Average chapter length: {summary_stats['average_words']:.0f} words")
    print(f"Maximum allowed (2x mean): {summary_stats['max_allowed_words']:.0f} words")
    print(f"Chapters exceeding threshold: {len(summary_stats['outliers'])}")
    print()
    
    print("DETAILED CHAPTER BREAKDOWN")
    print("-" * 80)
    print(f"{'Filename':<35} {'Words':>8} {'% of Avg':>10} {'Status':<15}")
    print("-" * 80)
    
    for stat in chapter_stats:
        status = "⚠️  EXCEEDS 2x" if stat['exceeds_threshold'] else "✓ OK"
        print(f"{stat['filename']:<35} {stat['word_count']:>8,} {stat['percentage_of_avg']:>9.1f}% {status:<15}")
    
    print()
    
    if recommendations:
        print("RECOMMENDATIONS FOR CHAPTERS EXCEEDING THRESHOLD")
        print("=" * 80)
        for rec in recommendations:
            print(rec)
    else:
        print("✓ All chapters are within acceptable length variance (≤2x mean)")
        print()
    
    print("=" * 80)


def save_report(chapter_stats: List[Dict], summary_stats: Dict, recommendations: List[str], output_file: Path):
    """Save the report to a markdown file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Chapter Length Distribution Analysis\n\n")
        f.write("*This report was automatically generated to analyze chapter length variance*\n\n")
        
        f.write("## Summary Statistics\n\n")
        f.write(f"- **Total chapters analyzed**: {summary_stats['total_chapters']}\n")
        f.write(f"- **Total word count**: {summary_stats['total_words']:,} words\n")
        f.write(f"- **Average chapter length**: {summary_stats['average_words']:.0f} words\n")
        f.write(f"- **Maximum allowed (2x mean)**: {summary_stats['max_allowed_words']:.0f} words\n")
        f.write(f"- **Chapters exceeding threshold**: {len(summary_stats['outliers'])}\n\n")
        
        f.write("## Detailed Chapter Breakdown\n\n")
        f.write("| Filename | Title | Words | % of Avg | Status |\n")
        f.write("|----------|-------|------:|----------:|--------|\n")
        
        for stat in chapter_stats:
            status = "⚠️ EXCEEDS 2x" if stat['exceeds_threshold'] else "✓ OK"
            title_short = stat['title'][:50] + "..." if len(stat['title']) > 50 else stat['title']
            f.write(f"| {stat['filename']} | {title_short} | {stat['word_count']:,} | {stat['percentage_of_avg']:.1f}% | {status} |\n")
        
        f.write("\n")
        
        if recommendations:
            f.write("## Recommendations for Chapters Exceeding Threshold\n\n")
            for rec in recommendations:
                f.write(rec)
                f.write("\n")
        else:
            f.write("## ✓ Compliance Status\n\n")
            f.write("All chapters are within acceptable length variance (≤2x mean).\n\n")
        
        f.write("---\n\n")
        f.write("*Note: Word counts exclude code blocks, markdown formatting, and structural elements.*\n")


def main():
    """Main entry point."""
    # Determine project root and docs directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    docs_dir = project_root / "docs"
    
    if not docs_dir.exists():
        print(f"ERROR: Docs directory not found at {docs_dir}")
        sys.exit(1)
    
    # Analyze chapters
    chapter_stats, summary_stats = analyze_chapters(docs_dir)
    
    # Generate recommendations for outliers
    recommendations = generate_recommendations(chapter_stats, summary_stats['average_words'])
    
    # Print report to console
    print_report(chapter_stats, summary_stats, recommendations)
    
    # Save report to file
    output_file = project_root / "reports" / "chapter_length_analysis.md"
    output_file.parent.mkdir(exist_ok=True)
    save_report(chapter_stats, summary_stats, recommendations, output_file)
    
    print(f"\n📄 Report saved to: {output_file}")
    
    # Exit with error code if there are outliers
    if summary_stats['outliers']:
        print(f"\n❌ Analysis complete: {len(summary_stats['outliers'])} chapter(s) exceed the 2x variance threshold")
        sys.exit(1)
    else:
        print("\n✓ Analysis complete: All chapters within acceptable variance")
        sys.exit(0)


if __name__ == "__main__":
    main()
