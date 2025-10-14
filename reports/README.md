# Reports Directory

This directory contains automated analysis reports for the Architecture as Code book.

## Available Reports

### Chapter Length Analysis

**Purpose**: Analyze the distribution of chapter lengths and identify chapters that exceed acceptable variance.

**Files**:
- `chapter_length_analysis.md` - Comprehensive statistical analysis of all chapters
- `chapter_length_action_plan.md` - Detailed action plan for chapters exceeding the 2x variance threshold

**How to Generate**:
```bash
python3 scripts/analyze_chapter_lengths.py
```

**Automated Testing**:
The chapter length variance is also validated in the test suite:
```bash
python -m pytest tests/test_consistency.py::TestConsistency::test_chapter_length_variance -v
```

**Threshold**: Chapters should not exceed 100% variance (2x) of the average chapter length.

**Current Status**: 
- 28 chapters analyzed
- Average: 1,373 words
- 2 chapters exceed threshold (Chapters 5 and 9)
- Action plans provided for both chapters

## Future Reports

Additional automated analysis reports can be added here for:
- Diagram distribution and usage
- Technical term consistency
- Cross-reference validation
- Sources and citations analysis
