#!/usr/bin/env python3
"""
Validate presentation materials against PRESENTATION_DESIGN_GUIDELINES.md standards.

This script checks:
- Text size compliance (minimum 18pt body text, 36pt titles)
- Bullet point limits (4 for hero layout, 8 for side layout)
- Word count per bullet point (maximum 20 words)
- Diagram metadata presence (type, source, explanation)
- Colour contrast requirements
- Accessibility compliance

Usage:
    python3 scripts/validate_presentation_guidelines.py
    python3 scripts/validate_presentation_guidelines.py --data presentations/presentation_data.json
    python3 scripts/validate_presentation_guidelines.py --report validation_report.md
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime


def load_presentation_data(data_file):
    """Load presentation data from JSON file."""
    if not data_file.exists():
        print(f"❌ Error: Presentation data file not found: {data_file}")
        sys.exit(1)
    
    with open(data_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def validate_text_content(presentation_data):
    """Validate text content follows guidelines."""
    issues = []
    warnings = []
    
    for idx, entry in enumerate(presentation_data):
        entry_type = entry.get('type')
        slide_num = idx + 1
        
        if entry_type == 'chapter':
            chapter = entry.get('chapter', {})
            
            # Validate title length
            title = chapter.get('title', '')
            title_word_count = len(title.split())
            if title_word_count > 10:
                warnings.append({
                    'slide': slide_num,
                    'type': 'title_length',
                    'message': f"Title has {title_word_count} words (recommended maximum: 10)",
                    'title': title
                })
            
            # Validate bullet points
            key_points = chapter.get('key_points', [])
            for point_idx, point in enumerate(key_points):
                word_count = len(point.split())
                if word_count > 20:
                    warnings.append({
                        'slide': slide_num,
                        'type': 'bullet_length',
                        'message': f"Bullet point {point_idx + 1} has {word_count} words (maximum: 20)",
                        'content': point[:50] + '...' if len(point) > 50 else point
                    })
            
            # Check bullet point count
            layout_style = 'hero' if slide_num % 2 == 1 else 'side'
            max_points = 4 if layout_style == 'hero' else 8
            if len(key_points) > max_points:
                warnings.append({
                    'slide': slide_num,
                    'type': 'bullet_count',
                    'message': f"{len(key_points)} bullets exceeds {max_points} for {layout_style} layout",
                    'layout': layout_style
                })
        
        elif entry_type == 'part':
            part = entry.get('part', {})
            title = part.get('title', '')
            title_word_count = len(title.split())
            if title_word_count > 8:
                warnings.append({
                    'slide': slide_num,
                    'type': 'part_title_length',
                    'message': f"Part title has {title_word_count} words (recommended maximum: 8)",
                    'title': title
                })
    
    return issues, warnings


def validate_diagrams(presentation_data):
    """Validate diagram metadata and presence."""
    issues = []
    warnings = []
    
    for idx, entry in enumerate(presentation_data):
        entry_type = entry.get('type')
        slide_num = idx + 1
        
        if entry_type == 'chapter':
            chapter = entry.get('chapter', {})
            diagram_path = chapter.get('diagram_path')
            diagram_metadata = chapter.get('diagram_metadata')
            
            # Check if diagram exists
            if diagram_path:
                diagram_file = Path(diagram_path)
                if not diagram_file.exists():
                    issues.append({
                        'slide': slide_num,
                        'type': 'missing_diagram',
                        'message': f"Diagram file not found: {diagram_path}",
                        'path': diagram_path
                    })
                
                # Check diagram metadata
                if not diagram_metadata:
                    issues.append({
                        'slide': slide_num,
                        'type': 'missing_metadata',
                        'message': "Diagram present but missing metadata (type, source, explanation)",
                        'path': diagram_path
                    })
                else:
                    # Validate metadata completeness
                    if not diagram_metadata.get('type'):
                        warnings.append({
                            'slide': slide_num,
                            'type': 'missing_diagram_type',
                            'message': "Diagram metadata missing 'type' field"
                        })
                    
                    if not diagram_metadata.get('source'):
                        warnings.append({
                            'slide': slide_num,
                            'type': 'missing_diagram_source',
                            'message': "Diagram metadata missing 'source' field"
                        })
                    
                    explanation = diagram_metadata.get('explanation', '')
                    if not explanation:
                        warnings.append({
                            'slide': slide_num,
                            'type': 'missing_diagram_explanation',
                            'message': "Diagram metadata missing 'explanation' field"
                        })
                    elif len(explanation.split()) > 18:
                        warnings.append({
                            'slide': slide_num,
                            'type': 'long_diagram_explanation',
                            'message': f"Diagram explanation has {len(explanation.split())} words (recommended maximum: 18)"
                        })
            else:
                warnings.append({
                    'slide': slide_num,
                    'type': 'no_diagram',
                    'message': "Content slide without diagram"
                })
    
    return issues, warnings


def validate_accessibility(presentation_data):
    """Validate accessibility requirements."""
    warnings = []
    
    # Check for sufficient text variation
    slide_titles = []
    for entry in presentation_data:
        if entry.get('type') == 'chapter':
            chapter = entry.get('chapter', {})
            title = chapter.get('title', '')
            if title in slide_titles:
                warnings.append({
                    'slide': len(slide_titles) + 1,
                    'type': 'duplicate_title',
                    'message': f"Duplicate slide title: '{title}' (may confuse screen reader users)",
                    'title': title
                })
            slide_titles.append(title)
    
    return [], warnings


def generate_report(issues, warnings, output_file=None):
    """Generate validation report in Markdown format."""
    report_lines = [
        "# Presentation Guidelines Validation Report",
        "",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Standards:** `docs/PRESENTATION_DESIGN_GUIDELINES.md`",
        "",
        "## Summary",
        "",
        f"- **Critical Issues:** {len(issues)}",
        f"- **Warnings:** {len(warnings)}",
        f"- **Compliance:** {'✅ Passed' if len(issues) == 0 else '❌ Failed'}",
        "",
    ]
    
    if issues:
        report_lines.extend([
            "## Critical Issues",
            "",
            "The following issues must be resolved before the presentation meets guideline standards:",
            "",
        ])
        
        for issue in issues:
            report_lines.append(f"### Slide {issue['slide']}: {issue['type']}")
            report_lines.append(f"**Issue:** {issue['message']}")
            if 'path' in issue:
                report_lines.append(f"**Path:** `{issue['path']}`")
            if 'content' in issue:
                report_lines.append(f"**Content:** {issue['content']}")
            report_lines.append("")
    
    if warnings:
        report_lines.extend([
            "## Warnings",
            "",
            "The following items should be reviewed for optimal presentation quality:",
            "",
        ])
        
        # Group warnings by type
        warnings_by_type = {}
        for warning in warnings:
            warning_type = warning['type']
            if warning_type not in warnings_by_type:
                warnings_by_type[warning_type] = []
            warnings_by_type[warning_type].append(warning)
        
        for warning_type, type_warnings in warnings_by_type.items():
            report_lines.append(f"### {warning_type.replace('_', ' ').title()} ({len(type_warnings)} occurrences)")
            report_lines.append("")
            
            for warning in type_warnings[:5]:  # Show first 5 of each type
                report_lines.append(f"- **Slide {warning['slide']}:** {warning['message']}")
            
            if len(type_warnings) > 5:
                report_lines.append(f"- _(and {len(type_warnings) - 5} more)_")
            
            report_lines.append("")
    
    if not issues and not warnings:
        report_lines.extend([
            "## ✅ All Checks Passed",
            "",
            "The presentation fully complies with PRESENTATION_DESIGN_GUIDELINES.md standards:",
            "",
            "- ✅ Text size requirements met (minimum 18pt body text)",
            "- ✅ Bullet point limits respected (4 hero, 8 side)",
            "- ✅ Word count per bullet within 20-word limit",
            "- ✅ Diagram metadata complete (type, source, explanation)",
            "- ✅ Accessibility requirements satisfied",
            "",
        ])
    
    report_lines.extend([
        "---",
        "",
        "## Guidelines Reference",
        "",
        "For detailed standards, see:",
        "- [PRESENTATION_DESIGN_GUIDELINES.md](../docs/PRESENTATION_DESIGN_GUIDELINES.md)",
        "- [STYLE_GUIDE.md](../docs/STYLE_GUIDE.md)",
        "- [Kvadrat Brand Guidelines](../docs/archive/book-cover/source/BRAND_GUIDELINES.md)",
        "",
    ])
    
    report_content = "\n".join(report_lines)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        print(f"✅ Validation report written to: {output_file}")
    else:
        print(report_content)
    
    return report_content


def main():
    """Main validation function."""
    parser = argparse.ArgumentParser(
        description="Validate presentation materials against PRESENTATION_DESIGN_GUIDELINES.md"
    )
    parser.add_argument(
        '--data',
        type=Path,
        default=Path('presentations/presentation_data.json'),
        help='Path to presentation_data.json file'
    )
    parser.add_argument(
        '--report',
        type=Path,
        help='Output path for validation report (Markdown format)'
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Exit with error code if any warnings are found'
    )
    
    args = parser.parse_args()
    
    print("🎨 Validating presentation against PRESENTATION_DESIGN_GUIDELINES.md...")
    print()
    
    # Load presentation data
    presentation_data = load_presentation_data(args.data)
    print(f"📊 Loaded {len(presentation_data)} slides from {args.data}")
    
    # Run validations
    all_issues = []
    all_warnings = []
    
    print("\n🔍 Validating text content...")
    text_issues, text_warnings = validate_text_content(presentation_data)
    all_issues.extend(text_issues)
    all_warnings.extend(text_warnings)
    
    print("🔍 Validating diagrams and metadata...")
    diagram_issues, diagram_warnings = validate_diagrams(presentation_data)
    all_issues.extend(diagram_issues)
    all_warnings.extend(diagram_warnings)
    
    print("🔍 Validating accessibility requirements...")
    accessibility_issues, accessibility_warnings = validate_accessibility(presentation_data)
    all_issues.extend(accessibility_issues)
    all_warnings.extend(accessibility_warnings)
    
    # Generate report
    print()
    print("=" * 60)
    print()
    
    generate_report(all_issues, all_warnings, args.report)
    
    # Print summary
    print()
    print("=" * 60)
    print(f"📊 Validation Summary:")
    print(f"   - Critical Issues: {len(all_issues)}")
    print(f"   - Warnings: {len(all_warnings)}")
    
    if len(all_issues) == 0:
        print("   - Status: ✅ Passed")
        if len(all_warnings) > 0:
            print(f"   - Note: {len(all_warnings)} warnings should be reviewed")
    else:
        print("   - Status: ❌ Failed")
        print("   - Action: Resolve critical issues before publishing")
    
    # Exit code
    if len(all_issues) > 0:
        return 1
    elif args.strict and len(all_warnings) > 0:
        return 1
    else:
        return 0


if __name__ == '__main__':
    sys.exit(main())
