Fix incorrect heading numbering in Appendix B (e.g., 27.1 → 31.1)

**Description**: The headings within Appendix B inherit numbering from earlier chapters, resulting in confusing section numbers such as “31.1” even though the content should be part of an appendix.

**Current Behavior**: Section headings display multi-level numeric prefixes tied to chapter numbering rather than appendix lettering.

**Expected Behavior**: Appendix sections should either use appendix lettering (e.g., “B.1”) or unnumbered headings, consistent with the overall style guide.

**Affected Files**:
- `docs/31_technical_architecture.md`
- Numbering configuration (e.g., `docs/pandoc.yaml`)

**Suggested Fix**:
1. Adjust heading levels or Pandoc configuration so numbering switches to appendix format.
2. Verify the table of contents reflects the desired appendix numbering.
