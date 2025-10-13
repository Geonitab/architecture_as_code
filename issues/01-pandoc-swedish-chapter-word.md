Pandoc outputs Swedish word for "Chapter"

**Description**: Pandoc renders the word *"Kapitel"* instead of *"Chapter"* in the output. This affects the consistency of English language usage across the document.

**Current Behavior**: When generating the PDF, Pandoc uses Swedish language defaults, resulting in "Kapitel" appearing in the output instead of "Chapter".

**Expected Behavior**: The output should use English words consistently, displaying "Chapter" instead of "Kapitel".

**Affected Files**:
- `docs/pandoc.yaml` (configuration file)
- Likely related to metadata `language: sv` and `lang: sv-SE` settings

**Suggested Fix**: Update the Pandoc configuration to use English language settings when generating English versions of the book.
