Remove Figure 26.1 from Appendix A

**Description**: Appendix A still includes Figure 26.1, which no longer adds value and should be removed along with its caption.

**Current Behavior**: The appendix renders the “Kodexempel appendix” figure at the top, consuming space without providing new information.

**Expected Behavior**: Appendix A should begin with the introductory text, omitting the redundant figure.

**Affected Files**:
- `docs/30_appendix_code_examples.md`
- `docs/images/diagram_26_appendix.png`

**Suggested Fix**:
1. Delete the Markdown block that inserts Figure 26.1 and its caption.
2. Remove the PNG asset if it is not used elsewhere.
3. Rebuild the book to confirm no references are broken.
