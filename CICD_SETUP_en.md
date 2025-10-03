# CI/CD Setup komplett

GitHub Actions konfiguration for automatisk bokbygge har skapats.

## Filer skapade:
- `.github/workflows/build-book.yml` - GitHub Actions workflow
- `README.md` - Uppdaterad projektdokumentation
- Uppdaterad interface with CI/CD status

## Next Steps:

1. **Anslut to GitHub**:
   - Klicka GitHub-knappen in Lovable
   - Auktorisera Lovable GitHub App
   - Skapa repository

2. **Automatisk byggprocess startar when**:
   - Markdown-filer ändras in `docs/`
   - Mermaid diagrams uppdateras
   - Push to main branch

3. **Workflow bygger**:
   - Konverterar .mmd → .png
   - creates PDF with Pandoc
   - Sparar that GitHub Release
   - Artifacts for nedladdning

## Byggprocessen includes:
- Pandoc with Eisvogel LaTeX-template
- Mermaid CLI for diagramkonvertering
- TeXLive for PDF-rendering
- Automatiska releases with versionsnummer

**Status: CI/CD pipeline redo for deployment!**