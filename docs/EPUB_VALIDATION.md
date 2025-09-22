# EPUB Validation Documentation

## Översikt

Detta projekt inkluderar automatisk validering av EPUB-filer med hjälp av EPUBCheck för att säkerställa att genererade EPUB-filer följer EPUB-standarden och fungerar korrekt i olika läsare.

## EPUBCheck

[EPUBCheck](https://github.com/w3c/epubcheck) är det officiella valideringsverktyget från W3C för EPUB-filer. Det kontrollerar att EPUB-filer följer EPUB-specifikationen och identifierar potentiella kompatibilitetsproblem.

### Installation

EPUBCheck installeras automatiskt i:
- GitHub Actions CI/CD-miljön
- Docker-byggningsmiljön
- Kan installeras lokalt med följande steg:

```bash
# Installera Java (krävs för EPUBCheck)
sudo apt-get install openjdk-11-jdk

# Ladda ner och installera EPUBCheck
wget https://github.com/w3c/epubcheck/releases/download/v5.1.0/epubcheck-5.1.0.zip
unzip epubcheck-5.1.0.zip
sudo mv epubcheck-5.1.0 /opt/
sudo ln -sf /opt/epubcheck-5.1.0/epubcheck.jar /usr/local/bin/

# Skapa wrapper-skript
echo '#!/bin/bash' | sudo tee /usr/local/bin/epubcheck
echo 'java -jar /opt/epubcheck-5.1.0/epubcheck.jar "$@"' | sudo tee -a /usr/local/bin/epubcheck
sudo chmod +x /usr/local/bin/epubcheck
```

## Automatisk Validering

### I Byggprocessen

EPUB-validering är integrerad i byggprocessen:

1. **`docs/build_book.sh`**: Validerar EPUB-fil efter generering
2. **`generate_book.py`**: Kontrollerar befintliga EPUB-filer
3. **GitHub Actions**: Automatisk validering i CI/CD-pipeline

### Valideringsutdata

Valideringen producerar följande typer av problem:

- **FATAL**: Kritiska fel som gör EPUB-filen oanvändbar
- **ERROR**: Fel som kan påverka kompatibilitet
- **WARNING**: Varningar för mindre problem
- **INFO**: Informationsmeddelanden

### Loggar

Valideringsresultat sparas i:
- `docs/epub-validation.log` - Detaljerad valideringslogg
- `releases/book/epub-validation.log` - Valideringslogg för release-version
- `docs/epub-validation-test.log` - Testvalideringslogg

## Testning

### Automatiska Tester

Ny testfil `tests/test_epub_validation.py` innehåller:

```python
# Grundläggande tester
test_epubcheck_available()           # EPUBCheck är tillgängligt
test_epub_file_exists()             # EPUB-fil finns
test_epub_file_validation()         # Komplett valideringstest
test_release_epub_validation()      # Release EPUB-validering
test_epub_metadata_present()        # Metadata är närvarande
test_epub_structure_integrity()     # Grundläggande strukturintegritet
```

### Köra Tester

```bash
# Kör alla tester inklusive EPUB-validering
python3 tests/run_tests.py --type all

# Kör endast EPUB-validering
python3 -m pytest tests/test_epub_validation.py -v
```

## Felsökning

### Vanliga Problem

#### 1. "Content is not allowed in prolog"
**Problem**: Ogiltiga tecken i början av XHTML-filer
**Lösning**: 
- Kontrollera att markdown-filer har UTF-8 kodning utan BOM
- Se till att Pandoc-konfiguration är korrekt

#### 2. "Fragment identifier is not defined"
**Problem**: Brutna interna länkar i EPUB
**Lösning**:
- Kontrollera att alla referenser i markdown är korrekta
- Se till att kapitelrubriker följer konsekvent format

#### 3. "Date value does not follow recommended syntax"
**Problem**: Felaktig datumformat i metadata
**Lösning**:
- Metadata date-fält bör vara i ISO 8601-format (YYYY-MM-DD)
- Konfigurerat i `pandoc.yaml`

### Debugging

För detaljerad felsökning:

```bash
# Manuell validering
epubcheck docs/arkitektur_som_kod.epub

# Verbose utdata
epubcheck -v docs/arkitektur_som_kod.epub

# Spara utdata till fil
epubcheck docs/arkitektur_som_kod.epub > validation-debug.log 2>&1
```

## Konfiguration

### Pandoc-konfiguration

`docs/pandoc.yaml` innehåller EPUB-specifika inställningar:

```yaml
# Metadata för korrekt EPUB-generering
metadata:
  title: "Arkitektur som kod"
  subtitle: "Infrastructure as Code i praktiken"
  author: "Kodarkitektur Bokverkstad"
  date: "2024"              # ISO-format för kompatibilitet
  language: sv
  lang: sv-SE

# EPUB-specifika inställningar
epub-chapter-level: 1        # Kapitelnivå för EPUB-struktur
```

### Byggskript-konfiguration

I `docs/build_book.sh`:

```bash
# Förbättrad EPUB-generering med validering
pandoc --defaults=pandoc.yaml "${CHAPTER_FILES[@]}" \
    -t epub \
    -o $OUTPUT_EPUB \
    --metadata date="$(date +'%Y-%m-%d')" \
    --metadata language=sv \
    --epub-cover-image="images/book-cover.png"

# Automatisk validering efter generering
validate_epub "$OUTPUT_EPUB"
```

## Kvalitetsstandarder

### Godkänd Validering

En EPUB-fil anses godkänd om:
- **0 fatala fel** (FATAL count = 0)
- **≤10 fel** (ERROR count ≤ 10)
- **Varningar accepterade** (WARNING count ignoreras)

### Kritiska Fel

EPUB-filen avvisas om:
- **>0 fatala fel** (förhindrar läsning)
- **>10 fel** (påverkar kompatibilitet avsevärt)

### Rapportering

Valideringsresultat rapporteras i:
- GitHub Actions workflow-loggar
- Test-rapporter
- Release-artefakter

## CI/CD Integration

### GitHub Actions

EPUB-validering är integrerad i `.github/workflows/unified-build-release.yml`:

1. **EPUBCheck-installation** under systemdependenser
2. **Automatisk validering** under byggprocessen
3. **Valideringsloggar** sparas som artefakter
4. **Testning** som en del av kvalitetskontroll

### Felhantering

- **Fatala fel**: Bygget rapporterar varning men fortsätter
- **Många fel**: Bygget rapporterar varning
- **Få fel/varningar**: Bygget lyckas normalt

## Framtida Förbättringar

### Planerade Funktioner

1. **Automatisk reparation** av vanliga EPUB-fel
2. **Anpassad EPUBCheck-konfiguration** för projektet
3. **Integration med fler EPUB-validatorer**
4. **Automatisk kompatibilitetstestning** med populära läsare

### Kvalitetsmål

- **0 fatala fel** i alla release-versioner
- **≤5 fel** i release-versioner
- **100% strukturintegritet** för alla EPUB-filer

## Support

För problem med EPUB-validering:

1. Kontrollera valideringsloggar
2. Kör manuell validering med `epubcheck`
3. Kontrollera Pandoc-konfiguration
4. Verifiera markdown-filernas kodning
5. Granska testresultat i `tests/test_epub_validation.py`

Valideringen hjälper till att säkerställa att EPUB-filer fungerar optimalt i alla e-läsare och följer industristandarder för digital bokpublicering.