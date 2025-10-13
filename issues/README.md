# GitHub Issues for Architecture as Code Book

This directory contains markdown files that will be automatically converted into GitHub issues using the workflow defined in `.github/workflows/create-issues.yml`.

## How It Works

1. Each `.md` file in this directory represents one GitHub issue
2. The first line of each file is used as the issue title
3. The remaining content becomes the issue body
4. The workflow can be manually triggered to create all issues at once

## Issue Categories

### Technical and Formatting Issues (6 issues)

1. **01-pandoc-swedish-chapter-word.md** - Pandoc outputs Swedish word for "Chapter"
2. **02-figure-21-caption-error.md** - Incorrect figure caption rendering in Figure 21.1
3. **03-chapter-18-hardcoded-numbering.md** - Hardcoded heading numbering in Chapter 18
4. **04-figure-22-not-rendering.md** - Figure 22.1 not rendering
5. **05-consistent-mermaid-theme.md** - Missing consistent Mermaid theme across diagrams
6. **06-rework-title-pages-british-english.md** - Rework the title pages from scratch in British English

### Translation Tasks (10 issues)

7. **07-translate-chapter-01-british-english.md** - Translate Chapter 1 to British English
8. **08-translate-chapter-02-british-english.md** - Translate Chapter 2 to British English
9. **09-translate-chapter-03-british-english.md** - Translate Chapter 3 to British English
10. **10-translate-chapter-04-british-english.md** - Translate Chapter 4 to British English
11. **11-translate-chapter-05-british-english.md** - Translate Chapter 5 to British English
12. **12-translate-chapter-06-british-english.md** - Translate Chapter 6 to British English
13. **13-translate-chapter-07-british-english.md** - Translate Chapter 7 to British English
14. **14-translate-chapter-08-british-english.md** - Translate Chapter 8 to British English
15. **15-translate-chapter-09-british-english.md** - Translate Chapter 9 to British English
16. **16-translate-chapter-10-british-english.md** - Translate Chapter 10 to British English

## Creating the Issues

To create these issues on GitHub:

1. Go to the repository's Actions tab
2. Select the "Create GitHub Issues from Markdown" workflow
3. Click "Run workflow"
4. Wait for the workflow to complete

All issues will be created automatically based on the content of these markdown files.

## Adding New Issues

To add a new issue:

1. Create a new `.md` file in this directory
2. Put the issue title as the first line
3. Add the issue description in the remaining lines
4. Run the workflow to create the issue

## Note

After the issues have been created, you may want to delete or archive this directory to avoid creating duplicate issues if the workflow is run again.
