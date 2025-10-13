Rename Appendix A so it is not labelled as Chapter 26

**Description**: Appendix A currently appears as “Chapter 26” in the generated output, which misleads readers and breaks the appendix structure.

**Current Behavior**: The appendix file inherits automatic chapter numbering, resulting in headings such as “26 Appendix A”.

**Expected Behavior**: The appendix should display simply as “Appendix A” without a chapter number.

**Affected Files**:
- `docs/30_appendix_code_examples.md`
- Any configuration controlling numbering (e.g., `docs/pandoc.yaml`)

**Suggested Fix**:
1. Disable automatic numbering for the appendix heading (e.g., by using `number-sections: false` for appendices or adjusting heading levels).
2. Verify that the output shows “Appendix A” without a numeric prefix.
