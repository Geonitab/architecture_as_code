# EPUB Validation Documentation

## Overview

This projekt includes automatisk validation of EPUB-filer with hjälp of EPUBCheck to säkerställa to genererade EPUB-filer följer EPUB-standarden and functions korrekt in olika läsare.

## EPUBCheck

[EPUBCheck](https://github.com/w3c/epubcheck) is the officiella valideringsverktyget from W3C för EPUB-filer. the kontrollerar to EPUB-filer följer EPUB-specifikationen och identifierar potentiella kompatibilitetsproblem.

### Installation

EPUBCheck installeras automatically in:
- GitHub Actions CI/CD-miljön
- Docker-byggningsmiljön
- can installeras lokalt with följande step:

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

## Automatisk validation

### in Byggprocessen

EPUB-validation is integrated in byggprocessen:

1. **`docs/build_book.sh`**: Validates EPUB-File efter generering
2. **`generate_book.py`**: Kontrollerar existing EPUB-filer
3. **GitHub Actions**: Automatisk validation in CI/CD-pipeline

### Valideringsutdata

Valideringen producerar följande typer of problem:

- **FATAL**: Kritiska fel as gör EPUB-filen oanvändbar
- **ERROR**: Fel as can påverka kompatibilitet
- **WARNING**: Varningar for mindre problem
- **INFO**: Informationswithdelanden

### Loggar

Valideringsresultat sparas in:
- `docs/epub-validation.log` - Detaljerad valideringslogg
- `releases/book/epub-validation.log` - Valideringslogg for release-version
- `docs/epub-validation-test.log` - Testvalideringslogg

## testing

### Automatiska Tester

Ny testfil `tests/test_epub_validation.py` Contentser:

```python
# Fundamental tester
test_epubcheck_available()           # EPUBCheck is tillgängligt
test_epub_file_exists()             # EPUB-File finns
test_epub_file_validation()         # Komplett valideringstest
test_release_epub_validation()      # Release EPUB-validation
test_epub_metadata_present()        # Metadata is närvarande
test_epub_structure_integrity()     # Fundamental strukturintegritet
```

### Köra Tester

```bash
# Kör all tester including EPUB-validation
python3 tests/run_tests.py --type all

# Kör endast EPUB-validation
python3 -m pytest tests/test_epub_validation.py -v
```

## Felsökning

### Vanliga Problem

#### 1. "Content is not allowed in prolog"
**Problem**: Ogiltiga tecken in början of XHTML-filer
**Lösning**: 
- Kontrollera to markdown-filer har UTF-8 kodning utan BOM
- Se to to Pandoc-konfiguration is korrekt

#### 2. "Fragment identifier is not defined"
**Problem**: Brutna interna länkar in EPUB
**Lösning**:
- Kontrollera to all References in markdown is korrekta
- Se to to kapitelrubriker följer konsekvent format

#### 3. "Date value does not follow recommended syntax"
**Problem**: Incorrect datumformat in metadata
**Lösning**:
- Metadata date-fält bör vara in ISO 8601-format (YYYY-MM-DD)
- Konfigurerat in `pandoc.yaml`

### Debugging

For detaljerad felsökning:

```bash
# Manuell validation
epubcheck docs/arkitektur_som_kod.epub

# Verbose utdata
epubcheck -v docs/arkitektur_som_kod.epub

# Spara utdata till File
epubcheck docs/arkitektur_som_kod.epub > validation-debug.log 2>&1
```

## Konfiguration

### Pandoc-konfiguration

`docs/pandoc.yaml` Contentser EPUB-specifika inställningar:

```yaml
# Metadata för korrekt EPUB-generering
metadata:
  title: "architecture as code"
  subtitle: "Infrastructure as Code in praktiken"
  author: "Kodarkitektur Bokverkstad"
  date: "2024"              # ISO-format för kompatibilitet
  language: sv
  lang: sv-SE

# EPUB-specifika inställningar
epub-chapter-level: 1        # Kapitelnivå för EPUB-struktur
```

### Byggskript-konfiguration

in `docs/build_book.sh`:

```bash
# Förbättrad EPUB-generering med validation
pandoc --defaults=pandoc.yaml "${CHAPTER_FILES[@]}" \
    -t epub \
    -o $OUTPUT_EPUB \
    --metadata date="$(date +'%Y-%m-%d')" \
    --metadata language=sv \
    --epub-cover-image="images/book-cover.png"

# Automatisk validation efter generering
validate_epub "$OUTPUT_EPUB"
```

## Kvalitetsstandarder

### Godkänd validation

a EPUB-File anses godkänd about:
- **0 fatala fel** (FATAL count = 0)
- **≤10 fel** (ERROR count ≤ 10)
- **Varningar accepterade** (WARNING count ignoreras)

### Kritiska Fel

EPUB-filen avvisas about:
- **>0 fatala fel** (forhindrar läsning)
- **>10 fel** (påverkar kompatibilitet avsevärt)

### Rapportering

Valideringsresultat rapporteras in:
- GitHub Actions workflow-loggar
- Test-rapporter
- Release-artefakter

## CI/CD Integration

### GitHub Actions

EPUB-validation is integrated in `.github/workflows/unified-build-release.yml`:

1. **EPUBCheck-installation** under systemdependenser
2. **Automatisk validation** under byggprocessen
3. **Valideringsloggar** sparas as artefakter
4. **testing** as a del of kvalitetskontroll

### Felhantering

- **Fatala fel**: Bygget rapporterar varning men fortsätter
- **Många fel**: Bygget rapporterar varning
- **Få fel/varningar**: Bygget lyckas normalt

## Framtida Förbättringar

### Planerade Funktioner

1. **Automatisk reparation** of vanliga EPUB-fel
2. **Anpassad EPUBCheck-konfiguration** for projektet
3. **Integration with fler EPUB-validatorer**
4. **Automatisk kompatibilitetstestning** with populära läsare

### Kvalitetsmål

- **0 fatala fel** in all release-versions
- **≤5 fel** in release-versions
- **100% Structureintegritet** for all EPUB-filer

## Support

For problem with EPUB-validation:

1. Kontrollera valideringsloggar
2. Kör manuell validation with `epubcheck`
3. Kontrollera Pandoc-konfiguration
4. Verifiera markdown-filernas kodning
5. Granska testresultat in `tests/test_epub_validation.py`

Valideringen hjälper to to säkerställa to EPUB-filer functions optimalt in all e-läsare and följer industristandarder for digital bokpublicering.