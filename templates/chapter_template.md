---
# ============================================================
# YAML FRONTMATTER
# Fill in every field before committing the chapter.
# ============================================================

# The full chapter title as it appears in the book.
title: "Chapter NN: Your Chapter Title Here"

# The chapter number. Use the format shown in book_index.json.
# Examples: 1, 9, 9B, 15A, 26B
chapter: NN

# The author's full name as it should appear in the published book.
author: "Gunnar Nordqvist"

# Publication or last-revised date in ISO 8601 format (YYYY-MM-DD).
date: "YYYY-MM-DD"

# A list of relevant topic tags used for indexing and navigation.
# Choose from existing tags in book_index.json and add new ones only if necessary.
tags:
  - architecture-as-code
  - your-topic-tag
  - another-tag
---

<!-- ============================================================
     CHAPTER FILE: docs/NN_your_chapter_title.md

     INSTRUCTIONS FOR CONTRIBUTORS
     ==============================
     1. Replace every placeholder marked with ALL_CAPS or angle
        brackets <like this>.
     2. Delete all comment blocks (<!-- ... -->) before submitting.
     3. Follow docs/STYLE_GUIDE.md: Oxford-standard British English
        throughout. Use "organisation" not "organization", etc.
     4. Refer to the discipline and book title as "Architecture as Code"
        (never "Architecture As Code" or "architecture as code").
     5. Run `python3 generate_book.py && docs/build_book.sh` to confirm
        the chapter compiles without errors.
     ============================================================ -->

# <Chapter Title> {#chapter-NN}

<!-- Provide a one- to three-sentence chapter abstract that will appear
     in the table of contents and in any auto-generated summaries.
     Keep it under 80 words. -->

<Brief abstract summarising the chapter's topic and why it matters
to practitioners of Architecture as Code.>

---

## Learning Objectives

<!-- List four to six concrete, measurable outcomes for the reader.
     Begin each objective with an action verb (e.g., "Explain",
     "Implement", "Evaluate", "Design", "Compare"). -->

By the end of this chapter, you will be able to:

- **Explain** <core concept introduced in this chapter>.
- **Identify** <key patterns, principles, or components covered>.
- **Design** <practical artefact or approach the reader can create>.
- **Implement** <tool, technique, or workflow demonstrated>.
- **Evaluate** <trade-offs or decision criteria discussed>.

---

## Introduction

<!-- Write 3–5 paragraphs that:
     - Contextualise the chapter within the broader Architecture as Code
       narrative and the book part it belongs to.
     - State the problem or opportunity the chapter addresses.
     - Outline what will be covered and how the sections connect.
     Reference the relevant part introduction (e.g., docs/part_a_foundations.md)
     where appropriate. -->

<Introduction text goes here. Set the scene, state the problem,
and briefly outline the chapter structure.>

---

## <Section 1 Title>

<!-- Replace with a descriptive heading for your first main topic.
     Aim for 400–800 words per section. Use sub-headings (###) to break
     up longer explanations. Include concrete examples wherever possible. -->

<Body text for section 1. Explain the concept, principle, or
practice being introduced. Use British English throughout.>

### <Subsection 1.1 Title>

<!-- Use subsections to organise complex topics. Not every section
     needs subsections; add them only when they improve clarity. -->

<Body text for subsection 1.1.>

### <Subsection 1.2 Title>

<Body text for subsection 1.2.>

---

## <Section 2 Title>

<Body text for section 2.>

---

## <Section 3 Title>

<!-- Add as many sections as the topic requires. Most chapters have
     between three and six main sections in addition to the standard
     ones that frame the chapter (Introduction, Code Examples,
     Diagrams, Summary, References). -->

<Body text for section 3.>

---

## Code Examples

<!-- Provide at least one complete, runnable code example relevant to
     the chapter's topic. Follow these rules:
     - Always include a language identifier on fenced code blocks.
     - Prefer YAML, Python, Bash, or HCL unless the chapter specifically
       covers another language.
     - Add inline comments to explain non-obvious lines.
     - Verify that every example is technically correct before committing. -->

The following example demonstrates <what the code achieves and
why it is relevant to this chapter's theme>.

```yaml
# Example: <descriptive title>
# Purpose: <one-line description of what this snippet does>

<your-code-here>:
  property: value  # British English comments throughout
  another-property: another-value
```

<!-- If the chapter warrants multiple examples, use sub-headings. -->

### <Additional Example Title>

<Brief explanation of the second example.>

```bash
# Example: <descriptive title>
<your-bash-snippet-here>
```

---

## Diagrams

<!-- Every diagram must have both a Mermaid source (.mmd) and a
     rendered PNG (.png) committed to docs/images/.
     Naming convention: diagram_NN_<short_description>.mmd / .png
     where NN matches the chapter number.

     Steps:
     1. Create docs/images/diagram_NN_<short_description>.mmd
     2. Render: npx mmdc -i docs/images/diagram_NN_<short_description>.mmd \
                         -o docs/images/diagram_NN_<short_description>.png \
                         -b transparent
     3. Validate: python3 scripts/check_mermaid_diagrams.py
     4. Reference the PNG below with a meaningful alt-text description. -->

![<Descriptive alt text explaining what the diagram shows>](images/diagram_NN_<short_description>.png)

*Figure NN.1: <Caption describing the diagram in one sentence.>*

<!-- Add further diagrams as required, incrementing the figure number. -->

---

## Summary

<!-- Write 3–5 sentences that:
     - Recap the key concepts, patterns, or practices introduced.
     - Highlight the most important takeaway for the reader.
     - Point forward to the next chapter or related chapters.
     Keep the summary concise: 150–250 words. -->

This chapter explored <key topic> and its role within Architecture as Code.
<Summarise the main points covered in two or three sentences.>
The following chapter, Chapter <NN+1>, builds on these foundations by
examining <brief preview of the next chapter's topic>.

---

## References

<!-- List all sources cited in this chapter using a consistent format.
     Prefer: Author Surname, Initials. (Year). *Title*. Publisher / URL.
     Include URLs for online sources and ISBNs for books where available.
     Verify every URL with: python3 scripts/verify_sources.py -->

- <Author Surname>, <Initials>. (<Year>). *<Title of Work>*. <Publisher>.
- <Author Surname>, <Initials>. (<Year>). "<Article or Chapter Title>". *<Journal or Book>*, <Volume>(<Issue>), <pp. Pages>. <URL or DOI if applicable>.
- <Organisation Name>. (<Year>). *<Report or Document Title>*. Retrieved from <URL>.

<!-- ============================================================
     END OF CHAPTER TEMPLATE
     Remove this comment block before submitting.
     ============================================================ -->
