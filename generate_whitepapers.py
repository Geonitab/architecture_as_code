#!/usr/bin/env python3
"""
Generates whitepaper versions of each chapter in the book 'Arkitektur som kod'.
Each whitepaper includes:
1. The diagram from the respective chapter
2. Heavily condensed text summarizing the content
3. A reference to the full chapter
4. An overarching description of the book's content and purpose
"""

import os
import re

def get_book_overview():
    """Returns the overarching description of the book's content and purpose."""
    return """## Om boken "Arkitektur som kod"

**"Arkitektur som kod"** är en omfattande guide för svenska organisationer som vill implementera Infrastructure as Code (IaC). Boken täcker hela spektrumet från grundläggande principer till avancerade implementationsstrategier, organisatoriska förändringar och framtida teknologitrender.

**Målgrupp:** Systemarkitekter, utvecklare, DevOps-ingenjörer och projektledare
**Omfattning:** 23 kapitel organiserade i fyra huvudområden:
- **Grundläggande koncept** (Kapitel 1-4): Fundamental principles och basic workflows
- **Djupgående tekniska implementationer** (Kapitel 5-12): Security, scaling, compliance
- **Organisatoriska och strategiska aspekter** (Kapitel 13-18): Team dynamics, cost optimization
- **Avancerade ämnen och framtiden** (Kapitel 19-23): Emerging technologies och industry trends

Boken fokuserar särskilt på svenska compliance-krav, GDPR-efterlevnad och kostnadsoptimering för den svenska marknaden."""

def get_chapter_info():
    """Returns metadata for all 23 chapters."""
    return [
        {"id": "01", "file": "01_inledning.md", "title": "Inledning till arkitektur som kod", "area": "Grundläggande koncept"},
        {"id": "02", "file": "02_kapitel1.md", "title": "Grundläggande principer för Infrastructure as Code", "area": "Systemutveckling"},
        {"id": "03", "file": "03_kapitel2.md", "title": "Versionhantering och kodstruktur", "area": "Systemutveckling"},
        {"id": "04", "file": "04_kapitel3.md", "title": "Automatisering och CI/CD-pipelines", "area": "Systemutveckling"},
        {"id": "05", "file": "05_kapitel4.md", "title": "Molnarkitektur som kod", "area": "Arkitektur"},
        {"id": "06", "file": "06_kapitel5.md", "title": "Säkerhet i Infrastructure as Code", "area": "Säkerhet"},
        {"id": "07", "file": "07_kapitel6.md", "title": "Monitering och observabilitet", "area": "Systemutveckling"},
        {"id": "08", "file": "08_kapitel7.md", "title": "Skalbarhet och prestanda", "area": "Arkitektur"},
        {"id": "09", "file": "09_kapitel8.md", "title": "Digitalisering genom kodbaserad infrastruktur", "area": "Digitalisering"},
        {"id": "10", "file": "10_kapitel9.md", "title": "Organisatorisk förändring och teamstrukturer", "area": "Organisationsutveckling"},
        {"id": "11", "file": "11_kapitel10.md", "title": "Projektledning för IaC-initiativ", "area": "Projektledning"},
        {"id": "12", "file": "12_kapitel11.md", "title": "Innovation genom infrastrukturtransformation", "area": "Innovation"},
        {"id": "13", "file": "13_kapitel12.md", "title": "Produktutveckling med IaC-verktyg", "area": "Produkt- och tjänstutveckling"},
        {"id": "14", "file": "14_kapitel13.md", "title": "Compliance och regelefterlevnad", "area": "Säkerhet"},
        {"id": "15", "file": "15_kapitel14.md", "title": "Kostnadsoptimering och resurshantering", "area": "Arkitektur"},
        {"id": "16", "file": "16_kapitel15.md", "title": "Teststrategier för infrastrukturkod", "area": "Systemutveckling"},
        {"id": "17", "file": "17_kapitel16.md", "title": "Migration från traditionell infrastruktur", "area": "Digitalisering"},
        {"id": "18", "file": "18_kapitel17.md", "title": "Framtida trender och teknologier", "area": "Innovation"},
        {"id": "19", "file": "19_kapitel18.md", "title": "Best practices och lärda läxor", "area": "Styrning"},
        {"id": "20", "file": "20_kapitel19.md", "title": "Fallstudier och praktiska exempel", "area": "Systemutveckling"},
        {"id": "21", "file": "21_slutsats.md", "title": "Slutsats", "area": "Sammanfattning"},
        {"id": "22", "file": "22_ordlista.md", "title": "Ordlista", "area": "Referens"},
        {"id": "23", "file": "23_om_forfattarna.md", "title": "Om författarna", "area": "Biografi"}
    ]

def extract_chapter_summary(content, max_words=200):
    """Extract and condense the main content from a chapter."""
    # Remove the title line
    lines = content.split('\n')
    content_lines = []
    skip_next = False
    
    for line in lines[1:]:  # Skip the first title line
        line = line.strip()
        if not line:
            continue
        # Skip image references
        if line.startswith('!['):
            continue
        # Skip diagram descriptions that start with "Diagrammet"
        if line.startswith('Diagrammet '):
            continue
        # Skip section headers that are too long
        if line.startswith('##'):
            # Only include main section headers, not subsections
            if len(line.replace('#', '').strip()) < 50:
                content_lines.append(f"**{line.replace('##', '').strip()}**")
            continue
        # Skip source/reference sections
        if 'Källor' in line or 'Referenser' in line or line.startswith('- '):
            break
        # Add content lines
        if not line.startswith('#'):
            content_lines.append(line)
    
    # Join and limit words
    summary_text = ' '.join(content_lines)
    words = summary_text.split()
    if len(words) > max_words:
        summary_text = ' '.join(words[:max_words]) + '...'
    
    return summary_text

def get_diagram_reference(chapter_id, chapter_file):
    """Get the diagram filename for a chapter."""
    diagram_file = f"diagram_{chapter_id}_{chapter_file.replace('.md', '').replace('_', '_')}"
    # Handle special cases
    if chapter_file == "01_inledning.md":
        diagram_file = "diagram_01_inledning"
    elif chapter_file.startswith("02_"):
        diagram_file = "diagram_02_kapitel1"
    elif chapter_file.startswith("03_"):
        diagram_file = "diagram_03_kapitel2"
    else:
        # Extract chapter number for others
        chapter_num = chapter_file.split('_')[0]
        if chapter_file.startswith(f"{chapter_num}_kapitel"):
            kapitel_num = chapter_file.replace(f"{chapter_num}_kapitel", "").replace(".md", "")
            diagram_file = f"diagram_{chapter_num}_kapitel{kapitel_num}"
        else:
            # For special files like slutsats, ordlista, etc.
            base_name = chapter_file.replace('.md', '')
            diagram_file = f"diagram_{chapter_id}_{base_name}"
    
    return diagram_file

def generate_whitepaper(chapter_info, docs_dir, whitepapers_dir, book_overview):
    """Generate a whitepaper for a single chapter."""
    chapter_file = os.path.join(docs_dir, chapter_info["file"])
    
    # Read the full chapter content if it exists
    summary = ""
    if os.path.exists(chapter_file):
        with open(chapter_file, 'r', encoding='utf-8') as f:
            content = f.read()
            summary = extract_chapter_summary(content)
    else:
        summary = f"Kapitel {chapter_info['id']} behandlar {chapter_info['title'].lower()} inom området {chapter_info['area'].lower()}. Detta kapitel ger värdefulla insikter och praktisk vägledning för svenska organisationer som implementerar Infrastructure as Code."
    
    # Get diagram reference
    diagram_file = get_diagram_reference(chapter_info["id"], chapter_info["file"])
    
    # Create whitepaper content
    whitepaper_content = f"""# {chapter_info["title"]} - Whitepaper

## Sammanfattning

{summary}

## Visualisering

![{chapter_info["title"]} diagram](../docs/images/{diagram_file}.png)

*Diagrammet illustrerar nyckelkoncepten och flöden som behandlas i detta kapitel.*

## Läs mer

**För fullständig behandling av detta ämne, se Kapitel {chapter_info["id"]} i boken "Arkitektur som kod".**

Detta whitepaper ger en översikt av huvudkoncepten, men den fullständiga behandlingen inkluderar:
- Detaljerade tekniska implementationer
- Praktiska exempel och kodexempel
- Best practices för svenska organisationer
- Compliance-krav och säkerhetsaspekter
- Fallstudier och verkliga användningsfall

{book_overview}

---

*Detta whitepaper är en del av bokprojektet "Arkitektur som kod" - en omfattande guide för Infrastructure as Code på svenska.*
"""

    # Write whitepaper file
    whitepaper_filename = f"kapitel_{chapter_info['id']}_{chapter_info['title'].lower().replace(' ', '_').replace('å', 'a').replace('ä', 'a').replace('ö', 'o').replace('-', '_')}_whitepaper.md"
    # Clean filename
    whitepaper_filename = re.sub(r'[^a-zA-Z0-9_.]', '_', whitepaper_filename)
    whitepaper_filename = re.sub(r'_+', '_', whitepaper_filename)
    
    whitepaper_path = os.path.join(whitepapers_dir, whitepaper_filename)
    
    with open(whitepaper_path, 'w', encoding='utf-8') as f:
        f.write(whitepaper_content)
    
    print(f"Whitepaper skapad: {whitepaper_filename}")
    return whitepaper_filename

def generate_whitepapers_index(whitepapers_dir, whitepaper_files, book_overview):
    """Generate an index file for all whitepapers."""
    chapters = get_chapter_info()
    
    index_content = f"""# Whitepapers - Arkitektur som kod

Denna mapp innehåller korta whitepaper-versioner av varje kapitel i boken "Arkitektur som kod". Varje whitepaper ger en kondenserad översikt av kapitelets huvudinnehåll och hänvisar till det fullständiga kapitlet för fördjupning.

{book_overview}

## Tillgängliga whitepapers

"""
    
    for i, chapter in enumerate(chapters):
        if i < len(whitepaper_files):
            filename = whitepaper_files[i]
            index_content += f"- **[Kapitel {chapter['id']}: {chapter['title']}]({filename})**\n  *Område: {chapter['area']}*\n\n"
    
    index_content += """
## Hur man använder whitepapers

1. **Snabb översikt**: Läs whitepaper för att få en snabb förståelse av kapitelets innehåll
2. **Fördjupning**: Använd referensen för att läsa det fullständiga kapitlet
3. **Visuell förståelse**: Studera diagrammet för att förstå nyckelkoncepten
4. **Sammanhang**: Läs bokens övergripande beskrivning för att förstå hur kapitlet passar in i helheten

## Format och struktur

Varje whitepaper följer samma struktur:
- **Sammanfattning**: Kondenserad text som sammanfattar kapitelets innehåll
- **Visualisering**: Diagram från respektive kapitel
- **Läs mer**: Referens till det fullständiga kapitlet och dess innehåll
- **Om boken**: Övergripande beskrivning av bokens syfte och omfattning

---

*Whitepapers genererade automatiskt från bokprojektet "Arkitektur som kod"*
"""
    
    index_path = os.path.join(whitepapers_dir, "README.md")
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print("Index-fil skapad: README.md")

def main():
    """Generate all whitepapers."""
    # Setup directories
    docs_dir = "docs"
    whitepapers_dir = "whitepapers"
    
    # Create whitepapers directory
    os.makedirs(whitepapers_dir, exist_ok=True)
    print(f"Skapad mapp: {whitepapers_dir}")
    
    # Get book overview and chapter info
    book_overview = get_book_overview()
    chapters = get_chapter_info()
    
    # Generate whitepapers
    whitepaper_files = []
    for chapter in chapters:
        filename = generate_whitepaper(chapter, docs_dir, whitepapers_dir, book_overview)
        whitepaper_files.append(filename)
    
    # Generate index
    generate_whitepapers_index(whitepapers_dir, whitepaper_files, book_overview)
    
    print(f"\n=== WHITEPAPERS GENERERING KOMPLETT ===")
    print(f"Totalt {len(whitepaper_files)} whitepapers skapade")
    print(f"Alla filer sparade i: {whitepapers_dir}/")

if __name__ == "__main__":
    main()