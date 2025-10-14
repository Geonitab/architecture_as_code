# Translation Mapping: Swedish Requirements to English Issues

This document maps the original Swedish feedback to the corresponding English GitHub issues.

## Original Swedish Feedback → English Issues

### Introduction / Introduktion
| Swedish Requirement | English Issue | Status |
|---------------------|---------------|--------|
| Add management as code as one of the different aspects | Issue 1: Add Management as Code to Introduction Chapter | ✅ Created |

### ADR Chapter
| Swedish Requirement | English Issue | Status |
|---------------------|---------------|--------|
| Adr lifecycle bilden behöver vara vertikal (ADR lifecycle image needs to be vertical) | Issue 2: Make ADR Lifecycle Diagram Vertical | ✅ Created |
| Byt ut exempel 2 mot ett exempel som inte är sverigefokuserat (Replace example 2 with non-Sweden-focused example) | Issue 3: Replace Sweden-Focused ADR Example | ✅ Created |
| Ta bort infrastructure/ från exemplet på gitstruktur (Remove infrastructure/ from git structure example) | Issue 4: Remove infrastructure/ Prefix from ADR Git Structure Example | ✅ Created |
| Ta bort sverigefokus i kapitlet (Remove Sweden focus in the chapter) | Issue 5: Remove Sweden-Focused Content from ADR Chapter | ✅ Created |

### Automation, DevOps and CI/CD Chapter
| Swedish Requirement | English Issue | Status |
|---------------------|---------------|--------|
| Timeline-bilden måste bli högre för att den ska vara läslig (Timeline image must be taller to be readable) | Issue 6: Make Timeline Diagram Taller for Better Readability | ✅ Created |
| Dela upp kapitlet i mindre delar (Split chapter into smaller parts) | Issue 7: Split Automation Chapter into Smaller Focused Chapters | ✅ Created |
| Ta bort sverigefokus i kapitlet (Remove Sweden focus in the chapter) | Issue 8: Remove Sweden-Focused Content from Automation Chapter | ✅ Created |
| Ta bort avsnittet Swedish Architecture testing framework (Remove Swedish Architecture testing framework section) | Issue 9: Remove Swedish Architecture Testing Framework Section | ✅ Created |
| Flytta ut delarna om Governance as Code till ett eget kapitel (Move Governance as Code parts to separate chapter) | Issue 7 (part 1): Create New Chapter: Governance as Code | ✅ Created |
| Flytta ut delarna om GDPR till ett eget kapitel (Move GDPR parts to separate chapter) | Issue 7 (part 2): Create New Chapter: GDPR and Data Protection | ✅ Created |
| Flytta ut CI/CD pipelines for Architecture as Code till eget kapitel (Move CI/CD pipelines to separate chapter) | Issue 7 (part 3): Create New Chapter: CI/CD Pipelines for Architecture as Code | ✅ Created |
| Flytta Cost optimisation and budget control till kapitlet om FinOps och säkerställ att det inte är Sverigefokuserat längre (Move cost optimization to FinOps chapter and ensure it's not Sweden-focused) | Issue 10: Move Cost Optimization to FinOps Chapter | ✅ Created |

### Security in Architecture as Code Chapter
| Swedish Requirement | English Issue | Status |
|---------------------|---------------|--------|
| Dimensions of security architecture mindmap innehåller för mycket information för att kunna tillgodogöras (Mindmap contains too much information to be absorbed) | Issue 11: Split Security Mindmap into Multiple Diagrams | ✅ Created |
| Dela upp mindmap i fem nya mindmaps. En övergripande med fyra ben och fyra detaljerade för respektive ben (Split mindmap into five new mindmaps: one overview with four branches and four detailed ones for each branch) | Issue 11: Split Security Mindmap into Multiple Diagrams | ✅ Created |

## Issue Count Summary

- **Total Swedish Requirements**: 13 distinct requirements
- **Total English Issues Created**: 11 issues
- **Coverage**: 100% (some requirements combined into single issues where logical)

## Combined Requirements

Some Swedish requirements were logically combined into single issues:

1. **Issue 7** combines three related requirements:
   - Split the chapter into smaller parts
   - Move Governance as Code to separate chapter
   - Move GDPR to separate chapter
   - Move CI/CD pipelines to separate chapter

2. **Issue 11** combines two related requirements:
   - Mindmap contains too much information
   - Split into five mindmaps (one overview + four detailed)

## Issue Distribution by Type

### Content Changes (5 issues)
- Issue 1: Add Management as Code reference
- Issue 3: Replace Sweden-focused example
- Issue 5: Remove Sweden content from ADR
- Issue 8: Remove Sweden content from Automation
- Issue 9: Remove Swedish testing framework

### Restructuring (3 issues)
- Issue 7: Split Automation chapter (MAJOR)
- Issue 10: Move cost optimization content
- Issue 11: Split security mindmap (MAJOR)

### Visual/Design (2 issues)
- Issue 2: Vertical ADR lifecycle diagram
- Issue 6: Taller timeline diagram

### Organization/Structure (1 issue)
- Issue 4: Remove infrastructure/ prefix

## Next Steps

1. ✅ All Swedish requirements translated to English issues
2. ⏳ Create issues in GitHub repository
3. ⏳ Prioritize and assign issues
4. ⏳ Begin implementation

## Notes

- All issues maintain the intent and scope of the original Swedish requirements
- Issues are written with detailed context for implementers unfamiliar with the original feedback
- Acceptance criteria ensure requirements are fully met
- File references make implementation straightforward
