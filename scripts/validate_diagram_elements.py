#!/usr/bin/env python3
"""
Validate that all Mermaid diagrams contain no more than 15 elements.

This script ensures diagram legibility by enforcing a maximum element count.
Exit codes:
  0 - All diagrams are within the 15-element limit
  1 - One or more diagrams exceed the limit
"""

import re
from pathlib import Path
from typing import Tuple, List
import sys


def count_diagram_elements(mmd_file: Path) -> Tuple[int, str, List[str]]:
    """
    Count visual elements in a Mermaid diagram.
    
    Returns:
        Tuple of (element_count, diagram_type, element_list)
    """
    try:
        content = mmd_file.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        # Filter out comments and front matter
        filtered_lines = []
        in_front_matter = False
        
        for line in lines:
            stripped = line.strip()
            
            if stripped == '---':
                in_front_matter = not in_front_matter
                continue
                
            if in_front_matter or stripped.startswith('%%'):
                continue
                
            if stripped:
                filtered_lines.append(stripped)
        
        # Detect diagram type
        diagram_type = 'unknown'
        if filtered_lines:
            first_line = filtered_lines[0].lower()
            if 'graph' in first_line or 'flowchart' in first_line:
                diagram_type = 'flowchart'
            elif 'sequencediagram' in first_line:
                diagram_type = 'sequence'
            elif 'classdiagram' in first_line:
                diagram_type = 'class'
            elif 'mindmap' in first_line:
                diagram_type = 'mindmap'
            elif 'pie' in first_line:
                diagram_type = 'pie'
            elif 'gantt' in first_line:
                diagram_type = 'gantt'
            elif 'quadrantchart' in first_line:
                diagram_type = 'quadrant'
            elif 'journey' in first_line:
                diagram_type = 'user_journey'
            elif 'statediagram' in first_line:
                diagram_type = 'state'
            elif 'erdiagram' in first_line:
                diagram_type = 'entity_relationship'
            elif 'timeline' in first_line:
                diagram_type = 'timeline'
        
        # Count elements based on diagram type
        elements = []
        
        if diagram_type == 'flowchart':
            # Count nodes (A[Text], B(Text), C{Text}, etc.)
            node_pattern = r'\b([A-Z][A-Za-z0-9_]*)\s*[\[\(\{]'
            for line in filtered_lines[1:]:  # Skip first line
                matches = re.findall(node_pattern, line)
                elements.extend(matches)
        
        elif diagram_type == 'mindmap':
            # Count nodes - each indented line is a node (excluding root and "mindmap")
            for line in filtered_lines[1:]:
                # Skip the root declaration
                if line.strip() and not line.strip().startswith('root'):
                    elements.append(line.strip())
        
        elif diagram_type == 'pie':
            # Count pie slices
            for line in filtered_lines:
                if ':' in line and not line.lower().startswith('pie'):
                    elements.append(line.strip())
        
        elif diagram_type == 'gantt':
            # Count gantt tasks
            for line in filtered_lines:
                stripped = line.strip()
                if stripped and not any(stripped.lower().startswith(x) for x in ['gantt', 'title', 'dateformat', 'section', 'axisformat']):
                    if ':' in stripped:
                        elements.append(stripped)
        
        elif diagram_type == 'quadrant':
            # Count quadrant points
            for line in filtered_lines:
                if ':' in line and '[' in line and ']' in line:
                    if not any(x in line.lower() for x in ['quadrant', 'title', 'x-axis', 'y-axis']):
                        elements.append(line.strip())
        
        elif diagram_type == 'sequence':
            # Count participants and messages
            for line in filtered_lines[1:]:
                stripped = line.strip()
                if stripped.startswith('participant '):
                    elements.append(stripped)
                elif '-->' in stripped or '->>' in stripped or '->' in stripped:
                    elements.append(stripped)
        
        elif diagram_type == 'class':
            # Count classes
            class_pattern = r'class\s+(\w+)'
            for line in filtered_lines:
                matches = re.findall(class_pattern, line)
                elements.extend(matches)
        
        # Remove duplicates but preserve count
        unique_elements = list(dict.fromkeys(elements))
        
        return len(unique_elements), diagram_type, unique_elements
        
    except Exception as e:
        print(f"Error analyzing {mmd_file}: {e}", file=sys.stderr)
        return 0, 'error', []


def main() -> int:
    """
    Validate all diagrams in docs/images/ directory.
    
    Returns:
        Exit code: 0 if all diagrams are valid, 1 if any exceed the limit
    """
    # Find the docs directory
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    images_dir = repo_root / 'docs' / 'images'
    
    if not images_dir.exists():
        print(f"Error: images directory not found at {images_dir}", file=sys.stderr)
        return 1
    
    # Find all mermaid files (excluding archive directory)
    mmd_files = sorted([f for f in images_dir.rglob('*.mmd') if 'archive' not in str(f)])
    
    if not mmd_files:
        print(f"Warning: No Mermaid files found in {images_dir}", file=sys.stderr)
        return 0
    
    print(f"Validating {len(mmd_files)} diagram files for 15-element limit...")
    
    exceeding_limit = []
    
    for mmd_file in mmd_files:
        count, diagram_type, elements = count_diagram_elements(mmd_file)
        
        if count > 15:
            exceeding_limit.append((mmd_file.name, count, diagram_type, elements))
    
    if exceeding_limit:
        print(f"\n❌ Found {len(exceeding_limit)} diagrams exceeding the 15-element limit:\n", file=sys.stderr)
        
        for filename, count, diagram_type, elements in exceeding_limit:
            print(f"  {filename} ({diagram_type}): {count} elements", file=sys.stderr)
        
        print(f"\nPlease split or simplify these diagrams to improve readability.", file=sys.stderr)
        return 1
    else:
        print(f"✅ All {len(mmd_files)} diagrams are within the 15-element limit!")
        return 0


if __name__ == '__main__':
    sys.exit(main())
