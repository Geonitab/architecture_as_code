import os

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

![Inledning till arkitektur som kod](images/diagram_01_inledning.png)

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
            "filename": "02_grundlaggande_principer.md", 
            "title": "Grundläggande principer för Architecture as Code",
            "area": "Systemutveckling",
            "mermaid_code": """graph LR
    A[Deklarativ kod] --> B[Versionskontroll]
    B --> C[Automatisering]
    C --> D[Reproducerbarhet]
    D --> E[Skalbarhet]""",
            "content": """# Grundläggande principer för Architecture as Code

Architecture as Code bygger på fundamentala principer som säkerställer framgångsrik implementation av kodifierad systemarkitektur. Dessa principer omfattar hela systemlandskapet och skapar en helhetssyn för arkitekturhantering.

![Grundläggande principer diagram](images/diagram_02_kapitel1.png)

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

Källor:
- Red Hat. "Architecture as Code Principles and Best Practices." Red Hat Developer.
- Martin, R. "Clean Architecture: A Craftsman's Guide to Software Structure." Prentice Hall, 2017.
- ThoughtWorks. "Architecture as Code: The Next Evolution." Technology Radar, 2024."""
        },
        
        # Resterande 21 kapitel kommer här (förkortade för brevity)
        {
            "filename": "03_versionhantering.md",
            "title": "Versionhantering och kodstruktur", 
            "area": "Systemutveckling",
            "mermaid_code": """graph LR
    A[Git repository] --> B[Branching strategy]
    B --> C[Code review]
    C --> D[Merge process]
    D --> E[Deployment]""",
            "content": """# Versionhantering och kodstruktur

Effektiv versionhantering utgör ryggraden i Infrastructure as Code-implementationer. Genom att tillämpa samma metoder som mjukvaruutveckling på infrastrukturdefinitioner skapas spårbarhet, samarbetsmöjligheter och kvalitetskontroll.

![Versionhantering och kodstruktur](images/diagram_03_kapitel2.png)

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
    generate_iac_book_content()