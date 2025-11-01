from __future__ import annotations

import argparse
import datetime
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Sequence

from scripts.navigation import get_book_build_files

REPO_ROOT = Path(__file__).resolve().parent
DOCS_DIR = REPO_ROOT / "docs"
PANDOC_NON_LATEX_DEFAULTS = DOCS_DIR / "pandoc-nonlatex.yaml"
DEFAULT_DIST_DIR = REPO_ROOT / "dist"
DEFAULT_EPUB_OUTPUT = DEFAULT_DIST_DIR / "book.epub"
DEFAULT_SAMPLE_CHAPTERS: Sequence[str] = (
    "part_a_foundations.md",
    "01_introduction.md",
    "02_fundamental_principles.md",
    "03_version_control.md",
)
PART_FILE_PREFIX = "part_"
NON_LATEX_COVER_PAGE = "00_front_cover.md"
BOOK_COVER_IMAGE = DOCS_DIR / "images" / "book-cover.png"

_CHAPTER_LIST_CACHE: Sequence[str] | None = None


def load_full_chapter_filenames() -> list[str]:
    """Return the ordered list of chapter files defined in mkdocs.yml."""

    global _CHAPTER_LIST_CACHE

    if _CHAPTER_LIST_CACHE is None:
        _CHAPTER_LIST_CACHE = tuple(get_book_build_files())

    return list(_CHAPTER_LIST_CACHE)


def determine_chapter_list(
    *,
    build_all: bool,
    sample: bool,
    chapters: Sequence[str] | None,
) -> list[str]:
    """Resolve which chapter files should be included for a build."""

    if sum(bool(option) for option in (build_all, sample, bool(chapters))) > 1:
        raise ValueError("Choose only one of --all, --sample, or --chapters.")

    if chapters:
        return [chapter.strip() for chapter in chapters if chapter.strip()]

    if sample:
        return list(DEFAULT_SAMPLE_CHAPTERS)

    # When no explicit selection is provided we build the full book.
    _ = build_all  # Flag retained for clarity/intention.
    return load_full_chapter_filenames()


def resolve_chapter_paths(chapter_names: Sequence[str]) -> list[Path]:
    """Convert chapter names into absolute paths under docs/."""

    paths: list[Path] = []
    for name in chapter_names:
        candidate = DOCS_DIR / name
        if not candidate.exists():
            raise FileNotFoundError(
                f"Chapter '{name}' not found in {DOCS_DIR.relative_to(REPO_ROOT)}."
            )
        paths.append(candidate)
    return paths


def sanitise_part_markdown(content: str) -> str:
    """Remove LaTeX-only helpers from part introduction files."""

    skip_prefixes = ("\\cleardoublepage", "\\part{", "\\setbookpart")
    cleaned_lines: list[str] = []

    for line in content.splitlines():
        if any(line.startswith(prefix) for prefix in skip_prefixes):
            continue
        cleaned_lines.append(line)

    while cleaned_lines and not cleaned_lines[0].strip():
        cleaned_lines.pop(0)

    while cleaned_lines and not cleaned_lines[-1].strip():
        cleaned_lines.pop()

    return "\n".join(cleaned_lines)


def prepare_non_latex_chapter_paths(
    chapter_paths: Sequence[Path],
) -> tuple[list[Path], tempfile.TemporaryDirectory[str]]:
    """Prepare chapter paths for non-LaTeX formats such as EPUB."""

    temp_dir = tempfile.TemporaryDirectory()
    prepared: list[Path] = []

    for chapter_path in chapter_paths:
        if chapter_path.name.startswith(PART_FILE_PREFIX):
            sanitised = sanitise_part_markdown(
                chapter_path.read_text(encoding="utf-8")
            )
            if sanitised.strip():
                destination = Path(temp_dir.name) / chapter_path.name
                destination.write_text(sanitised + "\n", encoding="utf-8")
                prepared.append(destination)
        else:
            prepared.append(chapter_path)

    cover_path = DOCS_DIR / NON_LATEX_COVER_PAGE
    if cover_path.exists() and cover_path not in prepared:
        prepared.insert(0, cover_path)

    return prepared, temp_dir


def build_epub_from_chapters(chapter_paths: Sequence[Path], output_path: Path) -> None:
    """Combine the provided chapters into an EPUB using Pandoc."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    prepared_paths, temp_dir = prepare_non_latex_chapter_paths(chapter_paths)

    try:
        command: list[str] = ["pandoc"]
        if PANDOC_NON_LATEX_DEFAULTS.exists():
            command.extend(["--defaults", str(PANDOC_NON_LATEX_DEFAULTS)])

        command.extend(str(path) for path in prepared_paths)
        command.extend(
            [
                "-t",
                "epub",
                "-o",
                str(output_path),
                "--metadata",
                f"date={datetime.date.today():%Y-%m-%d}",
                "--metadata",
                "language=en-GB",
                "--metadata",
                "lang=en-GB",
                "--metadata=include-before=",
                "--metadata=header-includes=",
            ]
        )

        if BOOK_COVER_IMAGE.exists():
            command.extend(["--epub-cover-image", str(BOOK_COVER_IMAGE)])

        subprocess.run(command, check=True)
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            "Pandoc is required to build EPUB output but was not found in PATH."
        ) from exc
    finally:
        temp_dir.cleanup()

    if not output_path.exists() or output_path.stat().st_size == 0:
        raise RuntimeError(
            f"Expected EPUB output at {output_path} was not created or is empty."
        )


def create_argument_parser() -> argparse.ArgumentParser:
    """Build the command-line interface for the script."""

    parser = argparse.ArgumentParser(
        description="Generate Architecture as Code book artefacts.",
    )
    parser.add_argument(
        "--format",
        choices=["epub"],
        required=True,
        help="Output format to build.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_EPUB_OUTPUT,
        help=(
            "Destination file for the generated output. Paths are relative to "
            "the repository root unless absolute."
        ),
    )

    selection_group = parser.add_mutually_exclusive_group()
    selection_group.add_argument(
        "--all",
        action="store_true",
        help="Build the full manuscript (default).",
    )
    selection_group.add_argument(
        "--sample",
        action="store_true",
        help="Build the curated sample chapter set.",
    )
    selection_group.add_argument(
        "--chapters",
        nargs="+",
        metavar="CHAPTER",
        help="Explicit chapter filenames relative to docs/.",
    )

    parser.add_argument(
        "--validate",
        action="store_true",
        help="Run EPUBCheck after building the EPUB output.",
    )

    return parser


def run_cli(arguments: Sequence[str]) -> int:
    """Entry point for command-line execution."""

    parser = create_argument_parser()
    args = parser.parse_args(arguments)

    build_all = args.all or not (args.sample or args.chapters)
    chapter_names = determine_chapter_list(
        build_all=build_all,
        sample=args.sample,
        chapters=args.chapters,
    )
    chapter_paths = resolve_chapter_paths(chapter_names)

    output_path = args.output
    if not output_path.is_absolute():
        output_path = (REPO_ROOT / output_path).resolve()

    if args.format == "epub":
        try:
            display_path: Path | str = output_path.relative_to(REPO_ROOT)
        except ValueError:
            display_path = output_path

        print(
            f"📚 Building EPUB with {len(chapter_paths)} chapters → {display_path}"
        )
        build_epub_from_chapters(chapter_paths, output_path)

        if args.validate:
            success, log_output = validate_epub_file(str(output_path))
            if not success:
                print(log_output)
                return 1
        return 0

    raise NotImplementedError(f"Unsupported format requested: {args.format}")

def validate_epub_file(epub_path):
    """
    Validera EPUB-fil med EPUBCheck.
    
    Args:
        epub_path (str): Sökväg till EPUB-filen
        
    Returns:
        tuple: (success: bool, log_output: str)
    """
    try:
        # Check if EPUBCheck is available
        result = subprocess.run(['epubcheck', '--version'], 
                               capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            return False, "EPUBCheck är inte tillgängligt"
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False, "EPUBCheck är inte installerat eller inte tillgängligt"
    
    try:
        # Run EPUBCheck validation
        print(f"🔍 Validerar EPUB-fil: {epub_path}")
        result = subprocess.run(['epubcheck', epub_path], 
                               capture_output=True, text=True, timeout=60)
        
        # Log the validation output
        log_output = result.stdout + result.stderr
        
        if result.returncode == 0:
            print("✅ EPUB-validering godkänd")
            return True, log_output
        else:
            print("⚠️  EPUB-validering avslöjade problem")
            # Count different types of issues
            fatal_count = log_output.count('FATAL')
            error_count = log_output.count('ERROR') - fatal_count  # Subtract fatals from errors
            warning_count = log_output.count('WARNING')
            
            print(f"   - Fatala fel: {fatal_count}")
            print(f"   - Fel: {error_count}")
            print(f"   - Varningar: {warning_count}")
            
            return False, log_output
            
    except subprocess.TimeoutExpired:
        return False, "EPUBCheck timeout - filen kan vara för stor eller skadad"
    except Exception as e:
        return False, f"Fel vid EPUB-validering: {str(e)}"

def generate_iac_book_content():
    """
    Genererar alla markdown-filer för boken 'Arkitektur som kod'
    Fokus: Architecture as Code med Infrastructure as Code som praktiskt exempel
    """
    
    # Definiera mappar
    output_dir = "docs"
    images_dir = os.path.join(output_dir, "images")
    
    # Skapa mappar
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)
    
    # Bokens struktur med alla 23 filer
    book_structure = [
        {
            "filename": "01_inledning.md",
            "title": "Inledning till arkitektur som kod",
            "area": "Grundläggande koncept",
            "mermaid_code": """graph LR
    A[Traditionell arkitektur] --> B[Manuella processer]
    C[Architecture as Code] --> D[Automatiserade processer] 
    E[Infrastructure as Code] --> F[Praktiskt exempel]""",
            "content": """# Inledning till arkitektur som kod

Arkitektur som kod (Architecture as Code) representerar ett paradigmskifte inom systemutveckling där hela systemarkitekturen definieras, versionshanteras och hanteras genom kod. Detta approach möjliggör samma metodiker som traditionell mjukvaruutveckling för hela organisationens tekniska landskap.

![Inledning till arkitektur som kod](images/diagram_01_introduction.png)

Diagrammet illustrerar evolutionen från manuella processer till den omfattande visionen av Architecture as Code, där hela systemarkitekturen kodifieras.

## Evolution mot arkitektur som kod

Traditionella metoder för systemarkitektur har ofta varit manuella och dokumentbaserade. Architecture as Code bygger på etablerade principer från mjukvaruutveckling och tillämpar dessa på hela systemlandskapet.

Detta inkluderar inte bara infrastrukturkomponenter, utan även applikationsarkitektur, dataflöden, säkerhetspolicies, compliance-regler och organisatoriska strukturer - allt definierat som kod.

## Definition och omfattning

Architecture as Code definieras som praktiken att beskriva, versionhantera och automatisera hela systemarkitekturen genom maskinläsbar kod. Detta omfattar applikationskomponenter, integrationsmönster, dataarkitektur, infrastruktur och organisatoriska processer.

Denna holistiska approach möjliggör end-to-end automatisering där förändringar i krav automatiskt propagerar genom hela arkitekturen - från applikationslogik till deployment och monitering.

## Bokens syfte och målgrupp

Denna bok vänder sig till systemarkitekter, utvecklare, projektledare och IT-beslutsfattare som vill förstå och implementera Architecture as Code i sina organisationer. 

Läsaren kommer att få omfattande kunskap om hur hela systemarkitekturen kan kodifieras, från grundläggande principer till avancerade arkitekturmönster som omfattar hela organisationens digitala ekosystem.

Källor:
- ThoughtWorks. "Architecture as Code: The Next Evolution." Technology Radar, 2024.
- Martin, R. "Clean Architecture: A Craftsman's Guide to Software Structure." Prentice Hall, 2017."""
        },
        
        {
            "filename": "02_fundamental_principles.md", 
            "title": "Grundläggande principer för Architecture as Code",
            "area": "Systemutveckling",
            "mermaid_code": """graph LR
    A[Deklarativ kod] --> B[Versionskontroll]
    B --> C[Automatisering]
    C --> D[Reproducerbarhet]
    D --> E[Skalbarhet]""",
            "content": """# Grundläggande principer för Architecture as Code

Architecture as Code bygger på fundamentala principer som säkerställer framgångsrik implementation av kodifierad systemarkitektur. Dessa principer omfattar hela systemlandskapet och skapar en helhetssyn för arkitekturhantering.

![Grundläggande principer diagram](images/diagram_02_chapter1.png)

Diagrammet visar det naturliga flödet från deklarativ kod genom versionskontroll och automatisering till reproducerbarhet och skalbarhet - de fem grundpelarna inom Architecture as Code.

## Deklarativ arkitekturdefinition

Den deklarativa approachen inom Architecture as Code innebär att beskriva önskat systemtillstånd på alla nivåer - från applikationskomponenter till infrastruktur. Detta skiljer sig från imperativ programmering där varje steg måste specificeras explicit.

Deklarativ definition möjliggör att beskriva arkitekturens önskade tillstånd, vilket Architecture as Code utvidgar till att omfatta applikationsarkitektur, API-kontrakt och organisatoriska strukturer.

## Helhetsperspektiv på kodifiering

Architecture as Code omfattar hela systemekosystemet genom en holistisk approach. Detta inkluderar applikationslogik, dataflöden, säkerhetspolicies, compliance-regler och organisationsstrukturer.

Ett praktiskt exempel är hur en förändring i en applikations API automatiskt kan propagera genom hela arkitekturen - från säkerhetskonfigurationer till dokumentation - allt eftersom det är definierat som kod.

## Immutable architecture patterns

Principen om immutable arkitektur innebär att hela systemarkitekturen hanteras genom oföränderliga komponenter. Istället för att modifiera befintliga delar skapas nya versioner som ersätter gamla på alla nivåer.

Detta skapar förutsägbarhet och eliminerar architectural drift - där system gradvis divergerar från sin avsedda design över tid.

## Testbarhet på arkitekturnivå

Architecture as Code möjliggör testning av hela systemarkitekturen, inte bara enskilda komponenter. Detta inkluderar validering av arkitekturmönster, compliance med designprinciper och verifiering av end-to-end-flöden.

Arkitekturtester validerar designbeslut, systemkomplexitet och säkerställer att hela arkitekturen fungerar som avsett.

## Documentation as Code

Documentation as Code (DaC) representerar principen att behandla dokumentation som en integrerad del av kodbasen snarare än som ett separat artefakt. Detta innebär att dokumentation lagras tillsammans med koden, versionshanteras med samma verktyg och genomgår samma kvalitetssäkringsprocesser som applikationskoden.

### Fördelar med Documentation as Code

**Versionskontroll och historik**: Genom att lagra dokumentation i Git eller andra versionskontrollsystem får organisationer automatisk spårbarhet av förändringar, möjlighet att återställa tidigare versioner och full historik över dokumentationens utveckling.

**Kollaboration och granskning**: Pull requests och merge-processer säkerställer att dokumentationsändringar granskas innan de publiceras. Detta förbättrar kvaliteten och minskar risken för felaktig eller föråldrad information.

**CI/CD-integration**: Automatiserade pipelines kan generera, validera och publicera dokumentation automatiskt när kod förändras. Detta eliminerar manuella steg och säkerställer att dokumentationen alltid är uppdaterad.

### Praktisk implementation

```yaml
# .github/workflows/docs.yml
name: Documentation Build and Deploy
on:
  push:
    paths: ['docs/**', 'README.md']
  pull_request:
    paths: ['docs/**']

jobs:
  build-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          
      - name: Install dependencies
        run: npm install
        
      - name: Generate documentation
        run: |
          npm run docs:build
          npm run docs:lint
          
      - name: Deploy to GitHub Pages
        if: github.ref == 'refs/heads/main'
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs/dist
```

Moderna verktyg som GitBook, Gitiles och MkDocs möjliggör automatisk generering av webbdokumentation från Markdown-filer lagrade tillsammans med koden.

## Requirements as Code

Requirements as Code (RaC) transformerar traditionell kravspecifikation från textdokument till maskinläsbar kod som kan exekveras, valideras och automatiseras. Detta paradigmskifte möjliggör kontinuerlig verifiering av att systemet uppfyller sina krav genom hela utvecklingslivscykeln.

### Automatisering och traceability

**Automatiserad validering**: Krav uttryckta som kod kan exekveras automatiskt mot systemet för att verifiera compliance. Detta eliminerar manuell testning och säkerställer konsekvent validering.

**Direkt koppling mellan krav och kod**: Varje systemkomponent kan kopplas tillbaka till specifika krav, vilket skapar fullständig traceability från affärsbehov till teknisk implementation.

**Continuous compliance**: Förändringar i systemet valideras automatiskt mot alla definierade krav, vilket förhindrar regression och säkerställer ongoing compliance.

### Praktiskt exempel med Open Policy Agent (OPA)

```yaml
# requirements/security-requirements.yaml
apiVersion: policy/v1
kind: RequirementSet
metadata:
  name: svenska-sakerhetskrav
  version: "1.2"
spec:
  requirements:
    - id: SEC-001
      type: security
      description: "Alla S3 buckets måste ha kryptering aktiverad"
      priority: critical
      compliance: ["GDPR", "ISO27001"]
      policy: |
        package security.s3_encryption
        
        deny[msg] {
          input.resource_type == "aws_s3_bucket"
          not input.server_side_encryption_configuration
          msg := "S3 bucket måste ha server-side encryption"
        }
    
    - id: GDPR-001
      type: compliance  
      description: "Persondata måste lagras inom EU/EES"
      priority: critical
      compliance: ["GDPR"]
      policy: |
        package compliance.data_residency
        
        deny[msg] {
          input.resource_type == "aws_rds_instance"
          not contains(input.availability_zone, "eu-")
          msg := "RDS instans måste placeras i EU-region"
        }
```

### Validering och test-automation

Requirements as Code integreras naturligt med test-automation genom att krav blir executable specifications:

```python
# test/requirements_validation.py
import yaml
import opa

class RequirementsValidator:
    def __init__(self, requirements_file: str):
        with open(requirements_file, 'r') as f:
            self.requirements = yaml.safe_load(f)
    
    def validate_requirement(self, req_id: str, system_config: dict):
        requirement = self.find_requirement(req_id)
        policy_result = opa.evaluate(
            requirement['policy'], 
            system_config
        )
        return {
            'requirement_id': req_id,
            'status': 'passed' if not policy_result else 'failed',
            'violations': policy_result
        }
    
    def validate_all_requirements(self) -> dict:
        results = []
        for req in self.requirements['spec']['requirements']:
            result = self.validate_requirement(req['id'], self.system_config)
            results.append(result)
        
        return {
            'total_requirements': len(self.requirements['spec']['requirements']),
            'passed': len([r for r in results if r['status'] == 'passed']),
            'failed': len([r for r in results if r['status'] == 'failed']),
            'details': results
        }
```

Svenska organisationer drar särskild nytta av Requirements as Code för att automatiskt validera GDPR-compliance, finansiella regleringar och myndighetskrav som konstant måste uppfyllas.

Källor:
- Red Hat. "Architecture as Code Principles and Best Practices." Red Hat Developer.
- Martin, R. "Clean Architecture: A Craftsman's Guide to Software Structure." Prentice Hall, 2017.
- ThoughtWorks. "Architecture as Code: The Next Evolution." Technology Radar, 2024.
- GitLab. "Documentation as Code: Best Practices and Implementation." GitLab Documentation, 2024.
- Open Policy Agent. "Policy as Code: Expressing Requirements as Code." CNCF OPA Project, 2024.
- Atlassian. "Documentation as Code: Treating Docs as a First-Class Citizen." Atlassian Developer, 2023.
- NIST. "Requirements Engineering for Secure Systems." NIST Special Publication 800-160, 2023."""
        },
        
        # Resterande 21 kapitel kommer här (förkortade för brevity)
        {
            "filename": "03_version_control.md",
            "title": "Versionhantering och kodstruktur", 
            "area": "Systemutveckling",
            "mermaid_code": """graph LR
    A[Git repository] --> B[Branching strategy]
    B --> C[Code review]
    C --> D[Merge process]
    D --> E[Deployment]""",
            "content": """# Versionhantering och kodstruktur

Effektiv versionhantering utgör ryggraden i Infrastructure as Code-implementationer. Genom att tillämpa samma metoder som mjukvaruutveckling på infrastrukturdefinitioner skapas spårbarhet, samarbetsmöjligheter och kvalitetskontroll.

![Versionhantering och kodstruktur](images/diagram_03_chapter2.png)

Diagrammet illustrerar det typiska flödet från Git repository genom branching strategy och code review till slutlig deployment, vilket säkerställer kontrollerad och spårbar infrastrukturutveckling.

## Git-baserad arbetsflöde för infrastruktur

Git utgör standarden för versionhantering av IaC-kod och möjliggör distribuerat samarbete mellan team-medlemmar. Varje förändring dokumenteras med commit-meddelanden som beskriver vad som ändrats och varför, vilket skapar en komplett historik över infrastrukturutvecklingen.

## Kodorganisation och modulstruktur

Välorganiserad kodstruktur är avgörande för maintainability och collaboration i större IaC-projekt. Modulär design möjliggör återanvändning av infrastrukturkomponenter across olika projekt och miljöer.

Källor:
- Atlassian. "Git Workflows for Infrastructure as Code." Atlassian Git Documentation."""
        }
    ]
    
    # Skapa alla markdown-filer
    markdown_files = []
    mermaid_files = []
    
    for item_data in book_structure:
        filename = item_data["filename"]
        content = item_data["content"]
        mermaid_code = item_data.get("mermaid_code")
        
        print(f"Skapar {filename}...")
        
        # Hantera Mermaid-diagram om de finns
        if mermaid_code:
            image_name_base = f"diagram_{filename.split('.')[0]}"
            mermaid_file = os.path.join(images_dir, f"{image_name_base}.mmd")
            
            with open(mermaid_file, "w", encoding="utf-8") as f:
                f.write(mermaid_code.strip())
            
            mermaid_files.append(mermaid_file)
            print(f"Mermaid-diagram sparat till {mermaid_file}")
        
        # Skapa markdown-fil
        markdown_path = os.path.join(output_dir, filename)
        with open(markdown_path, "w", encoding="utf-8") as f:
            f.write(content.strip())
        
        os.chmod(markdown_path, 0o644)
        markdown_files.append(filename)
        print(f"Fil {filename} skapad framgångsrikt.")
    
    print(f"\n=== ITERATION 1 KOMPLETT ===")
    print(f"Totalt {len(markdown_files)} markdown-filer skapade")
    print(f"Totalt {len(mermaid_files)} mermaid-diagram skapade") 

if __name__ == "__main__":
    if len(sys.argv) > 1:
        sys.exit(run_cli(sys.argv[1:]))

    print("=" * 80)
    print("📚 generate_book.py – manual content notice")
    print("=" * 80)
    print()
    print(
        "Automated chapter generation remains disabled to safeguard the British English "
        "manuscript stored in docs/."
    )
    print(
        "Use the CLI to build distribution formats, for example:\n"
        "  python generate_book.py --format epub --output dist/book.epub --all"
    )
    print()
    print(
        "To regenerate markdown automatically, update generate_iac_book_content() with "
        "British English prose and uncomment the function call below."
    )
    print()
    print("=" * 80)
    print()

    # Content generation disabled - uncomment to regenerate
    # generate_iac_book_content()

    epub_path = DOCS_DIR / "architecture_as_code.epub"
    if epub_path.exists():
        print("📖 Checking existing EPUB file…")
        success, log_output = validate_epub_file(str(epub_path))

        log_path = DOCS_DIR / "epub-validation.log"
        try:
            with open(log_path, "w", encoding="utf-8") as handle:
                handle.write(f"EPUB validation log for: {epub_path}\n")
                handle.write(
                    f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                )
                handle.write(f"Status: {'APPROVED' if success else 'ERRORS FOUND'}\n")
                handle.write("=" * 50 + "\n")
                handle.write(log_output)
            print(f"📄 Validation log saved: {log_path}")
        except Exception as exc:  # pragma: no cover - defensive logging only
            print(f"⚠️  Could not save validation log: {exc}")
    else:
        print("ℹ️  No EPUB file found to validate")

    print()
    print("✅ Script completed")
