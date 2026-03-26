# Translation Workflow {#translation-workflow}

This document describes how translations of *Architecture as Code* manuscript content are managed, how to add a new language, and the quality standards that all translated content must meet.

---

## Table of Contents

1. [Translation Infrastructure Overview](#translation-infrastructure-overview)
2. [Using `scripts/translate_repo.py`](#using-scriptstranslate_repopy)
3. [Adding a New Language](#adding-a-new-language)
4. [Translation Quality Standards](#translation-quality-standards)
5. [Testing Translated Content](#testing-translated-content)
6. [Maintaining Translations](#maintaining-translations)

---

## Translation Infrastructure Overview

### Approach

Translations of *Architecture as Code* are stored as separate Markdown files alongside the canonical English-language source. The primary tooling is a Python helper script (`scripts/translate_repo.py`) that uses the `translators` library to produce a machine-translated first draft. Human reviewers then refine each draft to meet editorial and technical standards before it is committed to the repository.

### File layout

Translated files follow the naming convention `<original_basename>_<language_code>.md` and are placed in the same directory as their English source, or within `docs/archive/` for drafts that are not yet part of the live build.

```
docs/
├── 01_introduction.md              # Canonical English source
├── 01_introduction_sv.md           # Swedish translation (example)
└── archive/
    ├── future_development_sv.md    # Archived Swedish draft
    └── microservices_architecture_en.md
```

The build pipeline currently compiles only the canonical English sources listed in `docs/book_index.json`. Translated files are maintained in the repository for reference and future multilingual editions but are not included in the default PDF, EPUB, or DOCX builds unless explicitly added to `book_index.json`.

### Dependencies

| Dependency | Purpose |
|-----------|---------|
| Python 3.12.3 | Required runtime for `translate_repo.py` |
| `translators` library | Machine translation via multiple provider back-ends |

Install the Python dependencies before running any translation commands:

```bash
python3 -m pip install -r requirements.txt
```

Confirm that `translators` is available:

```bash
python3 -c "import translators; print('translators available')"
```

---

## Using `scripts/translate_repo.py`

### What the script does

`scripts/translate_repo.py` walks the repository tree starting from the root, reads every non-binary file it encounters, calls the `translators` library to translate the content from English into the target language, and overwrites each file with the translated text.

The script skips the following paths to avoid corrupting automation and version-control metadata:

- `.git/`
- `.github/`
- `scripts/`

### Running a translation

> **Warning:** The script overwrites files in place. Always work on a dedicated Git branch and commit the English originals first so that changes can be reviewed and reverted if necessary.

```bash
# Create a branch for the translation
git checkout -b translation/<language-code>-<chapter-or-scope>

# Run translation for a specific file
python3 - <<'EOF'
from scripts.translate_repo import translate_file_content
translate_file_content("docs/01_introduction.md", target_language="sv")
EOF

# Or translate an entire directory subtree
python3 - <<'EOF'
from scripts.translate_repo import translate_directory
translate_directory("docs/", target_language="sv")
EOF
```

Alternatively, invoke the script directly to translate the entire repository (use with caution):

```bash
python3 scripts/translate_repo.py
```

The default target language is Swedish (`sv`). Pass a different [BCP 47 language tag](https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry) to the `target_language` parameter to translate into another language.

### Supported language codes

The `translators` library supports a wide range of language codes. Common examples:

| Language | Code |
|---------|------|
| Swedish | `sv` |
| German | `de` |
| French | `fr` |
| Spanish | `es` |
| Japanese | `ja` |
| Simplified Chinese | `zh` |
| Portuguese | `pt` |

Refer to the [translators library documentation](https://github.com/UlionTse/translators) for the full list of supported codes and provider availability.

### Output

The script prints progress to standard output:

```
Startar översättning för mappen: /path/to/architecture_as_code
Översatte filen: docs/01_introduction.md
...
Översättningen är klar!
```

Files that are empty or unreadable (binary assets) are skipped with an informational message.

---

## Adding a New Language

Follow these steps to introduce a language that has not been translated before.

### 1. Verify language support

Confirm that the target language code is supported by the `translators` library:

```python
python3 -c "
import translators as ts
# Attempt a short test translation
result = ts.translate_text('Architecture as Code', from_language='en', to_language='<code>')
print(result)
"
```

If this succeeds, proceed. If it raises an exception, check the library documentation for the correct code or an alternative provider.

### 2. Create a translation branch

```bash
git checkout -b translation/<language-code>-initial
```

### 3. Translate target files

Decide which files to translate. For a new language, start with a representative subset rather than attempting the entire repository at once:

```bash
python3 - <<'EOF'
from scripts.translate_repo import translate_file_content

# Translate the introduction chapter as a pilot
translate_file_content("docs/01_introduction.md", target_language="<code>")
EOF
```

After the machine translation completes, rename the output file to include the language suffix before the `.md` extension and move the original back to its canonical English path:

```bash
# The script overwrites the original file, so restore it from git
git checkout docs/01_introduction.md

# Rename the translated copy appropriately
mv docs/01_introduction.md docs/01_introduction_<code>.md
```

> **Tip:** Translate one file at a time for new languages so that quality can be assessed before translating the full manuscript.

### 4. Apply language-specific editorial review

Machine translation output must always be reviewed by a fluent speaker before being committed (see [Translation Quality Standards](#translation-quality-standards)).

### 5. Update documentation

Add the new language to this document's supported language table and, once a translation is considered complete enough for inclusion, update `docs/book_index.json` to reference the translated files in a separate build configuration.

### 6. Open a pull request

Submit the reviewed translations through the standard pull request process described in `CONTRIBUTING.md`. Use the `documentation` label to trigger the Editor Bot for automated feedback.

---

## Translation Quality Standards

Machine translation provides a useful starting draft but always requires human editorial refinement. The following standards must be met before any translated file is committed to a non-archive path.

### Technical terminology

Architecture and technology terms that are widely understood in English should generally be left untranslated or transliterated rather than adapted into potentially ambiguous local equivalents. Examples:

- "Architecture as Code" — retain the English title in all translations.
- "pipeline", "microservice", "container", "repository" — retain if the target language community uses the English term.
- Domain-specific terms defined in the book's glossary — use translations only where a well-established local equivalent exists.

### Structural fidelity

- All Markdown headings, YAML frontmatter fields, fenced code blocks, and internal link anchors must be preserved exactly as in the English source.
- Do **not** translate content inside fenced code blocks, inline code spans, or HTML attributes.
- Image references and diagram filenames must remain unchanged.

### Prose quality

- Translated prose must read naturally in the target language; literal word-for-word renditions are not acceptable.
- Maintain the formal, instructional tone of the English original.
- Avoid colloquialisms, region-specific idioms, or culturally specific metaphors unless they accurately convey the intended meaning.

### Consistency

- Use consistent terminology throughout all translated chapters. Maintain a glossary of preferred translations for technical terms specific to the target language.
- Where a term appears with varying translations in the machine output, standardise on one form during editorial review.

### Review sign-off

Every translated file requires sign-off from at least one fluent speaker of the target language who also has sufficient technical background to verify that architectural and engineering concepts are correctly conveyed.

---

## Testing Translated Content

### Structural validation

Run the standard link and source verification scripts against translated files:

```bash
# Check that all internal links resolve
python3 scripts/verify_links.py

# Verify cited sources
python3 scripts/verify_sources.py
```

These scripts check Markdown link syntax and URL availability regardless of the language of the surrounding prose.

### Build validation

Translated chapters that are added to `book_index.json` must pass the full build pipeline:

```bash
python3 generate_book.py && docs/build_book.sh
```

Check that Pandoc processes the translated Markdown without errors and that the resulting PDF, EPUB, and DOCX output is formatted correctly.

### Pytest suite

The content validation tests operate primarily on the English canonical sources. When a translation is added to the live build, extend the relevant test fixtures in `tests/` to include the translated files:

```bash
python3 -m pytest tests/ -v
```

Review any failures carefully; some checks (such as spell-checking for British English) may need language-specific configuration before they can be applied to non-English content.

### Manual review checklist

Before marking a translated PR as ready for merge, verify:

- [ ] Code blocks, CLI commands, and configuration examples are unchanged from the English source.
- [ ] Image references and diagram filenames are unchanged.
- [ ] YAML frontmatter is structurally valid and retains the correct `chapter` and `tags` values.
- [ ] The translated prose reads naturally and meets the quality standards above.
- [ ] A fluent speaker has reviewed and approved the content.

---

## Maintaining Translations

### Keeping translations in sync with the English source

The canonical English manuscript evolves continuously. Translated files must be updated whenever substantive changes are made to the corresponding English source. The recommended process is:

1. When a pull request modifies an English chapter file, check whether a translated version of that file exists.
2. If a translated version exists and the changes are substantive (new sections, revised technical content, updated examples), open a follow-up issue labelled `documentation` to request a translation update.
3. Re-run `translate_file_content` on the modified file to generate a new machine-translated draft, then apply editorial review as described above.

### Archiving outdated translations

Translated files that are no longer kept in sync with the English source should be moved to `docs/archive/` with a note in `docs/archive/README.md` recording the reason and date of archival. This preserves the historical content without creating confusion about its current status.

### Tracking translation coverage

Maintain a simple coverage table in this document (or in a dedicated `docs/translation_status.md` file) that shows which chapters have been translated, reviewed, and are currently up to date for each language.

#### Example coverage table

| Chapter | Swedish (`sv`) | German (`de`) | French (`fr`) |
|---------|:-------------:|:-------------:|:-------------:|
| 01 Introduction | Draft | — | — |
| 02 Fundamental Principles | Draft | — | — |
| … | … | … | … |

Status key: **—** = not started, **Draft** = machine translation only, **Review** = under human review, **Complete** = reviewed and up to date.

### Raising issues

To report a translation error, outdated content, or to volunteer as a reviewer for a specific language, open a GitHub issue with the `documentation` label and include the target language and chapter number in the title.
