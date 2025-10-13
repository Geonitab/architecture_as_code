Figure 22.1 not rendering

**Description**: Figure 22.1 is missing or not being rendered in the final output.

**Current Behavior**: The figure reference exists in the document but the actual figure is not displayed in the generated PDF.

**Possible Causes**:
- Missing or incorrectly named image file
- Incorrect file path in markdown
- Mermaid diagram conversion failure
- Rendering settings issue

**Investigation Required**:
1. Check if the source `.mmd` file exists in `docs/images/`
2. Verify if the PNG conversion was successful
3. Review the markdown syntax for the figure reference
4. Check build logs for any conversion errors

**Suggested Fix**: Investigate the root cause and either fix the source file, file path, or rendering configuration as needed.
