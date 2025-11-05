#!/usr/bin/env python3
"""
Diagram Complexity Analyzer

Analyzes Mermaid diagrams to identify overly complex diagrams that may be
difficult to read. Diagrams with more than 15 elements should be simplified
or split into multiple diagrams.

Usage:
    python3 scripts/analyze_diagram_complexity.py                    # Analyze all diagrams
    python3 scripts/analyze_diagram_complexity.py --threshold 15     # Custom threshold
    python3 scripts/analyze_diagram_complexity.py --verbose          # Show all diagrams
"""

import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple
import argparse
from collections import defaultdict


class DiagramComplexityAnalyzer:
    """Analyzes diagram complexity based on element count."""
    
    def __init__(self, threshold: int = 15):
        self.threshold = threshold
        self.results: Dict[str, Dict] = {}
    
    def count_elements(self, content: str, diagram_type: str) -> int:
        """Count elements in a diagram based on its type."""
        
        if diagram_type == 'graph' or diagram_type == 'flowchart':
            return self._count_graph_elements(content)
        elif diagram_type == 'sequenceDiagram':
            return self._count_sequence_elements(content)
        elif diagram_type == 'classDiagram':
            return self._count_class_elements(content)
        elif diagram_type == 'erDiagram':
            return self._count_er_elements(content)
        elif diagram_type == 'mindmap':
            return self._count_mindmap_elements(content)
        elif diagram_type == 'gantt':
            return self._count_gantt_elements(content)
        elif diagram_type == 'pie':
            return self._count_pie_elements(content)
        elif diagram_type == 'quadrantChart':
            return self._count_quadrant_elements(content)
        elif diagram_type == 'requirementDiagram':
            return self._count_requirement_elements(content)
        elif diagram_type == 'gitGraph':
            return self._count_git_elements(content)
        else:
            # Generic element counting
            return self._count_generic_elements(content)
    
    def _count_graph_elements(self, content: str) -> int:
        """Count nodes and subgraphs in flowcharts/graphs."""
        elements = 0
        
        # Count nodes (patterns like A[Label], B(Label), C{Label}, etc.)
        node_pattern = re.compile(r'\b[A-Z][A-Z0-9_]*\s*[\[\(\{<]')
        elements += len(node_pattern.findall(content))
        
        # Count subgraphs
        subgraph_pattern = re.compile(r'^\s*subgraph\s+', re.MULTILINE)
        elements += len(subgraph_pattern.findall(content))
        
        return elements
    
    def _count_sequence_elements(self, content: str) -> int:
        """Count participants and interactions in sequence diagrams."""
        elements = 0
        
        # Count participants
        participant_pattern = re.compile(r'^\s*participant\s+', re.MULTILINE)
        elements += len(participant_pattern.findall(content))
        
        # Count interactions (arrows: ->>, ->, -->>, -->)
        interaction_pattern = re.compile(r'-{1,2}>>{0,1}')
        elements += len(interaction_pattern.findall(content))
        
        return elements
    
    def _count_class_elements(self, content: str) -> int:
        """Count classes and relationships in class diagrams."""
        elements = 0
        
        # Count class definitions
        class_pattern = re.compile(r'^\s*class\s+\w+', re.MULTILINE)
        elements += len(class_pattern.findall(content))
        
        # Count relationships (-->, --|>, etc.)
        relationship_pattern = re.compile(r'--[>|ox*]|\.\.>')
        elements += len(relationship_pattern.findall(content))
        
        return elements
    
    def _count_er_elements(self, content: str) -> int:
        """Count entities and relationships in ER diagrams."""
        elements = 0
        
        # Count entities
        entity_pattern = re.compile(r'^\s*\w+\s*\{', re.MULTILINE)
        elements += len(entity_pattern.findall(content))
        
        # Count relationships
        relationship_pattern = re.compile(r'[|}][oO|][.|-]{1,2}[oO|][|{]')
        elements += len(relationship_pattern.findall(content))
        
        return elements
    
    def _count_mindmap_elements(self, content: str) -> int:
        """Count nodes in mindmap diagrams."""
        # Count indented lines (each represents a node)
        lines = content.split('\n')
        elements = 0
        
        for line in lines:
            stripped = line.strip()
            # Skip empty lines, comments, and the mindmap keyword
            if stripped and not stripped.startswith('%%') and stripped != 'mindmap':
                elements += 1
        
        return elements
    
    def _count_gantt_elements(self, content: str) -> int:
        """Count tasks and sections in Gantt charts."""
        elements = 0
        
        # Count sections
        section_pattern = re.compile(r'^\s*section\s+', re.MULTILINE)
        elements += len(section_pattern.findall(content))
        
        # Count tasks (lines with colons but not config lines)
        lines = content.split('\n')
        for line in lines:
            if ':' in line and not line.strip().startswith(('title', 'dateFormat', 'axisFormat', 'section', '%%')):
                elements += 1
        
        return elements
    
    def _count_pie_elements(self, content: str) -> int:
        """Count slices in pie charts."""
        # Count lines with colon (each is a slice)
        pie_pattern = re.compile(r'^\s*"[^"]+"\s*:', re.MULTILINE)
        return len(pie_pattern.findall(content))
    
    def _count_quadrant_elements(self, content: str) -> int:
        """Count data points in quadrant charts."""
        # Count lines with coordinates [x, y]
        point_pattern = re.compile(r':\s*\[\s*\d+\.?\d*\s*,\s*\d+\.?\d*\s*\]')
        return len(point_pattern.findall(content))
    
    def _count_requirement_elements(self, content: str) -> int:
        """Count requirements and elements in requirement diagrams."""
        elements = 0
        
        # Count requirements
        req_pattern = re.compile(r'^\s*(requirement|functionalRequirement|performanceRequirement)\s+', re.MULTILINE)
        elements += len(req_pattern.findall(content))
        
        # Count elements
        element_pattern = re.compile(r'^\s*element\s+', re.MULTILINE)
        elements += len(element_pattern.findall(content))
        
        # Count relationships
        relationship_pattern = re.compile(r'\s+-\s+(contains|copies|derives|satisfies|verifies|refines|traces)\s+->')
        elements += len(relationship_pattern.findall(content))
        
        return elements
    
    def _count_git_elements(self, content: str) -> int:
        """Count commits and branches in git graphs."""
        elements = 0
        
        # Count commits
        commit_pattern = re.compile(r'^\s*commit', re.MULTILINE)
        elements += len(commit_pattern.findall(content))
        
        # Count branches
        branch_pattern = re.compile(r'^\s*branch\s+', re.MULTILINE)
        elements += len(branch_pattern.findall(content))
        
        return elements
    
    def _count_generic_elements(self, content: str) -> int:
        """Generic element counting for unknown diagram types."""
        # Count non-empty, non-comment lines as approximate element count
        lines = content.split('\n')
        elements = 0
        
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith('%%') and not stripped.startswith('---'):
                elements += 1
        
        return max(0, elements - 3)  # Subtract a few for typical config lines
    
    def detect_diagram_type(self, content: str) -> str:
        """Detect the type of Mermaid diagram."""
        content_lower = content.lower().strip()
        
        # Check for diagram type keywords
        if content_lower.startswith('graph '):
            return 'graph'
        elif content_lower.startswith('flowchart '):
            return 'flowchart'
        elif content_lower.startswith('sequencediagram'):
            return 'sequenceDiagram'
        elif content_lower.startswith('classdiagram'):
            return 'classDiagram'
        elif content_lower.startswith('erdiagram'):
            return 'erDiagram'
        elif content_lower.startswith('mindmap'):
            return 'mindmap'
        elif content_lower.startswith('gantt'):
            return 'gantt'
        elif content_lower.startswith('pie'):
            return 'pie'
        elif content_lower.startswith('quadrantchart'):
            return 'quadrantChart'
        elif content_lower.startswith('requirementdiagram'):
            return 'requirementDiagram'
        elif content_lower.startswith('gitgraph'):
            return 'gitGraph'
        else:
            return 'unknown'
    
    def analyze_file(self, filepath: Path) -> Dict:
        """Analyze a single diagram file."""
        try:
            content = filepath.read_text(encoding='utf-8')
        except Exception as e:
            return {
                'error': f"Failed to read file: {e}",
                'elements': 0,
                'diagram_type': 'unknown'
            }
        
        # Skip empty files
        if not content.strip():
            return {
                'error': 'Empty file',
                'elements': 0,
                'diagram_type': 'unknown'
            }
        
        diagram_type = self.detect_diagram_type(content)
        element_count = self.count_elements(content, diagram_type)
        
        result = {
            'elements': element_count,
            'diagram_type': diagram_type,
            'is_complex': element_count > self.threshold,
            'filepath': str(filepath)
        }
        
        self.results[str(filepath)] = result
        return result
    
    def analyze_all_diagrams(self, diagram_dir: Path) -> None:
        """Analyze all diagram files in a directory."""
        diagram_files = sorted(diagram_dir.glob('*.mmd'))
        
        for filepath in diagram_files:
            self.analyze_file(filepath)
    
    def generate_report(self, verbose: bool = False) -> str:
        """Generate a complexity report."""
        if not self.results:
            return "No diagrams analyzed."
        
        # Categorize results
        complex_diagrams = {k: v for k, v in self.results.items() if v.get('is_complex', False)}
        simple_diagrams = {k: v for k, v in self.results.items() if not v.get('is_complex', False)}
        
        # Group by diagram type
        type_stats = defaultdict(lambda: {'count': 0, 'total_elements': 0, 'max_elements': 0})
        for result in self.results.values():
            dtype = result.get('diagram_type', 'unknown')
            type_stats[dtype]['count'] += 1
            type_stats[dtype]['total_elements'] += result.get('elements', 0)
            type_stats[dtype]['max_elements'] = max(type_stats[dtype]['max_elements'], result.get('elements', 0))
        
        # Build report
        lines = []
        lines.append("=" * 80)
        lines.append("DIAGRAM COMPLEXITY ANALYSIS REPORT")
        lines.append("=" * 80)
        lines.append(f"\nThreshold: {self.threshold} elements")
        lines.append(f"Total diagrams analyzed: {len(self.results)}")
        lines.append(f"Complex diagrams (>{self.threshold} elements): {len(complex_diagrams)} ⚠️")
        lines.append(f"Simple diagrams (≤{self.threshold} elements): {len(simple_diagrams)} ✅")
        
        # Type statistics
        lines.append("\n" + "-" * 80)
        lines.append("DIAGRAM TYPE STATISTICS")
        lines.append("-" * 80)
        lines.append(f"{'Type':<20} {'Count':<10} {'Avg Elements':<15} {'Max Elements':<15}")
        lines.append("-" * 80)
        
        for dtype, stats in sorted(type_stats.items()):
            avg = stats['total_elements'] / stats['count'] if stats['count'] > 0 else 0
            lines.append(f"{dtype:<20} {stats['count']:<10} {avg:<15.1f} {stats['max_elements']:<15}")
        
        # Complex diagrams details
        if complex_diagrams:
            lines.append("\n" + "=" * 80)
            lines.append("⚠️  COMPLEX DIAGRAMS REQUIRING REVIEW")
            lines.append("=" * 80)
            lines.append(f"{'File':<60} {'Type':<20} {'Elements':<10}")
            lines.append("-" * 80)
            
            # Sort by element count (descending)
            sorted_complex = sorted(complex_diagrams.items(), key=lambda x: x[1].get('elements', 0), reverse=True)
            
            for filepath, result in sorted_complex:
                filename = Path(filepath).name
                dtype = result.get('diagram_type', 'unknown')
                elements = result.get('elements', 0)
                lines.append(f"{filename:<60} {dtype:<20} {elements:<10}")
            
            lines.append("\n" + "=" * 80)
            lines.append("RECOMMENDATIONS")
            lines.append("=" * 80)
            lines.append("Complex diagrams (>15 elements) are difficult to read and should be:")
            lines.append("  1. Simplified by removing non-essential elements")
            lines.append("  2. Split into multiple focused diagrams")
            lines.append("  3. Reorganized using subgraphs to group related elements")
            lines.append("\nRefer to docs/DIAGRAM_STYLE_GUIDE.md for best practices.")
        
        # Verbose output: show all diagrams
        if verbose:
            lines.append("\n" + "=" * 80)
            lines.append("ALL DIAGRAMS")
            lines.append("=" * 80)
            lines.append(f"{'File':<60} {'Type':<20} {'Elements':<10} {'Status':<10}")
            lines.append("-" * 80)
            
            sorted_all = sorted(self.results.items(), key=lambda x: x[1].get('elements', 0), reverse=True)
            
            for filepath, result in sorted_all:
                filename = Path(filepath).name
                dtype = result.get('diagram_type', 'unknown')
                elements = result.get('elements', 0)
                status = "⚠️ Complex" if result.get('is_complex') else "✅ OK"
                lines.append(f"{filename:<60} {dtype:<20} {elements:<10} {status:<10}")
        
        return "\n".join(lines)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Analyze diagram complexity and identify overly complex diagrams',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 scripts/analyze_diagram_complexity.py
  python3 scripts/analyze_diagram_complexity.py --threshold 20
  python3 scripts/analyze_diagram_complexity.py --verbose

Diagrams with more than 15 elements are typically difficult to read and should
be simplified or split into multiple diagrams.
"""
    )
    
    parser.add_argument(
        '--threshold',
        type=int,
        default=15,
        help='Element count threshold for complexity (default: 15)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show all diagrams, not just complex ones'
    )
    
    parser.add_argument(
        '--dir',
        type=str,
        default='docs/images',
        help='Directory containing diagram files (default: docs/images)'
    )
    
    args = parser.parse_args()
    
    # Validate directory
    diagram_dir = Path(args.dir)
    if not diagram_dir.exists():
        print(f"Error: Directory not found: {diagram_dir}", file=sys.stderr)
        return 1
    
    # Run analysis
    analyzer = DiagramComplexityAnalyzer(threshold=args.threshold)
    analyzer.analyze_all_diagrams(diagram_dir)
    
    # Print report
    report = analyzer.generate_report(verbose=args.verbose)
    print(report)
    
    # Return exit code based on findings
    complex_count = sum(1 for r in analyzer.results.values() if r.get('is_complex', False))
    return 1 if complex_count > 0 else 0


if __name__ == '__main__':
    sys.exit(main())
