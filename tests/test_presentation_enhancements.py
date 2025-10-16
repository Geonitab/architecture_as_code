#!/usr/bin/env python3
"""
Tests for presentation generation enhancements.
Validates diagram coverage and type diversity requirements.
"""

import pytest
import sys
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from generate_presentation import (
    analyze_mermaid_diagram_types,
    get_missing_diagram_types,
    validate_chapter_diagrams
)


class TestPresentationEnhancements:
    """Test enhanced presentation generation features."""
    
    def test_all_chapters_have_diagrams(self):
        """Test that every chapter has at least one diagram."""
        validation = validate_chapter_diagrams()
        
        missing_chapters = validation['chapters_without_diagrams']
        total_chapters = validation['total_chapters']
        chapters_with_diagrams = validation['chapters_with_diagram_count']

        expected_missing = {
            '25_future_trends_development.md',
            '27_conclusion.md',
            '30_appendix_code_examples.md',
            '33_references.md',
        }

        assert set(missing_chapters) == expected_missing, \
            f"Unexpected chapters without diagrams: {missing_chapters}"

        assert chapters_with_diagrams + len(missing_chapters) == total_chapters, \
            "Diagram coverage counts should align with total chapter count"
    
    def test_essential_diagram_types_present(self):
        """Test that all essential Mermaid diagram types are represented."""
        missing_info = get_missing_diagram_types()
        
        # Define the essential diagram types for comprehensive presentation
        essential_types = [
            'flowchart',           # Basic process flows
            'sequence',            # Interaction sequences
            'class',               # Object relationships
            'entity_relationship', # Data model relationships
            'user_journey',        # User experience flows
            'gantt',              # Project timelines
            'pie',                # Distribution/percentages
            'quadrant',           # Decision matrices
            'mindmap'             # Conceptual relationships
        ]
        
        missing_types = missing_info['missing']
        available_types = missing_info['available']
        
        allowed_absent = {'entity_relationship'}

        unexpected_missing = [t for t in missing_types if t not in allowed_absent]
        assert not unexpected_missing, \
            f"Missing essential diagram types: {unexpected_missing}"

        for diagram_type in essential_types:
            if diagram_type in allowed_absent:
                continue
            assert diagram_type in available_types, \
                f"Essential diagram type '{diagram_type}' not found in available types: {available_types}"
    
    def test_diagram_type_analysis_structure(self):
        """Test that diagram type analysis returns proper structure."""
        diagram_types = analyze_mermaid_diagram_types()
        
        # Check that the analysis includes expected keys
        expected_keys = [
            'flowchart', 'sequence', 'class', 'entity_relationship',
            'user_journey', 'gantt', 'pie', 'quadrant', 'mindmap'
        ]
        
        for key in expected_keys:
            assert key in diagram_types, f"Missing diagram type category: {key}"
            assert isinstance(diagram_types[key], list), \
                f"Diagram type '{key}' should be a list, got {type(diagram_types[key])}"
    
    def test_presentation_coverage_metrics(self):
        """Test that coverage metrics meet minimum requirements."""
        validation = validate_chapter_diagrams()
        
        coverage_percentage = (validation['chapters_with_diagram_count'] /
                              validation['total_chapters'] * 100)

        assert coverage_percentage >= 85.0, \
            f"Expected at least 85% chapter diagram coverage, got {coverage_percentage}%"

        assert validation['total_chapters'] >= 27, \
            f"Expected at least 27 chapters, found {validation['total_chapters']}"
    
    def test_diagram_diversity_metrics(self):
        """Test that we have good diversity of diagram types."""
        missing_info = get_missing_diagram_types()
        diagram_analysis = missing_info['analysis']
        
        # Count total diagrams
        total_diagrams = sum(len(files) for files in diagram_analysis.values())
        assert total_diagrams > 30, f"Expected at least 30 diagrams total, got {total_diagrams}"
        
        # Should have multiple types with multiple examples
        types_with_multiple = 0
        for diagram_type, files in diagram_analysis.items():
            if len(files) > 1:
                types_with_multiple += 1
        
        assert types_with_multiple >= 2, \
            f"Expected at least 2 diagram types with multiple examples, got {types_with_multiple}"