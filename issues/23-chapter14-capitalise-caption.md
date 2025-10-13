Capitalise the caption for Figure 14.4

**Description**: The caption under Figure 14.4 begins with a lowercase letter, breaking the book's style guide and the rest of the figure captions in Chapter 14.

**Current Behavior**: The italicised caption in Chapter 14 starts with a lowercase word ("figure"), which stands out against the surrounding captions that begin with uppercase letters.

**Expected Behavior**: Every figure caption should start with an uppercase "Figure" followed by the chapter-specific numbering.

**Affected Files**:
- `docs/14_practical_implementation.md`

**Suggested Fix**:
1. Update the italic caption text for Figure 14.4 so it begins with "Figure".
2. Review the chapter to ensure no other captions start with lowercase letters.
3. Rebuild the book to confirm the caption renders correctly.
