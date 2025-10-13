Investigate why heading 14.6 renders as 14.6.1 when no body text precedes a subheading

**Description**: In Chapter 14, the section titled 14.6 unexpectedly appears as 14.6.1 whenever a subheading follows immediately without intervening body text. This disrupts the numbering sequence and suggests a Markdown structure issue.

**Current Behavior**: When the chapter is built, the heading that should read "14.6" is auto-numbered as "14.6.1" because the first element inside the section is another heading. Readers see an extra level in the table of contents.

**Expected Behavior**: Top-level sections should retain their numbering (e.g., 14.6) regardless of whether the content begins with text or a nested subheading.

**Affected Files**:
- `docs/14_practical_implementation.md`

**Suggested Fix**:
1. Insert a brief introductory sentence or paragraph immediately after the 14.6 heading so Pandoc recognises content before the subheading.
2. Alternatively, adjust the heading levels so the structure reflects the intended hierarchy.
3. Rebuild the book to ensure the table of contents and heading numbering remain correct.
