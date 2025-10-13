Missing consistent Mermaid theme across diagrams

**Description**: There is currently no unified theme for Mermaid diagrams in the book, resulting in inconsistent visual presentation.

**Requirements**:
- **Consistent style** across all diagrams
- **Colour range** from light blue to dark blue
- **Accessibility** for colour blindness (e.g., using textures or contrast-friendly hues)

**Current State**: 
- A custom Kvadrat theme exists at `docs/mermaid-Kvadrat-theme.json`
- However, consistency and accessibility requirements may not be fully met

**Suggested Improvements**:
1. Review and update the Mermaid theme configuration for consistency
2. Ensure colour palette is accessible for colour-blind users
3. Apply the theme uniformly across all diagram generation
4. Consider adding patterns or textures in addition to colours for better accessibility
5. Document the theme guidelines in `VISUAL_ELEMENTS_GUIDE.md`

**References**:
- Existing theme: `docs/mermaid-Kvadrat-theme.json`
- Build script: `docs/build_book.sh`
- Documentation: `VISUAL_ELEMENTS_GUIDE.md`
