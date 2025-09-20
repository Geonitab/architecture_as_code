# Arkitektur som kod - Bokstruktur

Detta dokument beskriver den logiska strukturen för boken "Arkitektur som kod" som är organiserad i 25 kapitel som bygger på varandra för att ge en komplett förståelse av Architecture as Code och Infrastructure as Code för svenska organisationer.

## Kapitelstruktur

### Del 1: Grunder och fundamentala koncept (Kapitel 1-4)

| Kapitel | Fil | Titel | Beskrivning |
|---------|-----|-------|-------------|
| 1 | `01_inledning.md` | Inledning till arkitektur som kod | Introduktion till konceptet Architecture as Code och dess relation till Infrastructure as Code |
| 2 | `02_grundlaggande_principer.md` | Grundläggande principer för Architecture as Code | Fundamentala principer som deklarativ arkitekturdefinition och helhetsperspektiv |
| 3 | `03_versionhantering.md` | Versionhantering och kodstruktur | Best practices för versionshantering av arkitekturkod |
| 4 | `04_adr.md` | Architecture Decision Records (ADR) | Strukturerad dokumentation av arkitekturbeslut |

### Del 2: Kärnimplementering (Kapitel 5-9)

| Kapitel | Fil | Titel | Beskrivning |
|---------|-----|-------|-------------|
| 5 | `05_automatisering_cicd.md` | Automatisering och CI/CD-pipelines | Automation av arkitekturprocesser genom CI/CD |
| 6 | `06_devops_cicd.md` | DevOps och CI/CD för Infrastructure as Code | DevOps-praktiker specifikt för IaC |
| 7 | `07_molnarkitektur.md` | Molnarkitektur som kod | Cloudnativ arkitektur och IaC i molnmiljöer |
| 8 | `08_containerisering.md` | Containerisering och orkestrering som kod | Container-baserad arkitektur som kod |
| 9 | `09_microservices.md` | Microservices-arkitektur som kod | Microservices-mönster implementerat genom kod |

### Del 3: Säkerhet och compliance (Kapitel 10-12)

| Kapitel | Fil | Titel | Beskrivning |
|---------|-----|-------|-------------|
| 10 | `10_sakerhet.md` | Säkerhet i Architecture as Code | Säkerhetsaspekter och best practices |
| 11 | `11_policy_sakerhet.md` | Policy och säkerhet som kod i detalj | Detaljerad genomgång av policy-as-code |
| 12 | `12_compliance.md` | Compliance och regelefterlevnad | Regelefterlevnad i svenska organisationer |

### Del 4: Testning och kvalitetssäkring (Kapitel 13-14)

| Kapitel | Fil | Titel | Beskrivning |
|---------|-----|-------|-------------|
| 13 | `13_teststrategier.md` | Teststrategier för infrastruktukod | Testning av IaC och arkitekturkod |
| 14 | `14_praktisk_implementation.md` | Architecture as Code i praktiken | Praktiska implementeringsexempel |

### Del 5: Drift och hantering (Kapitel 15-16)

| Kapitel | Fil | Titel | Beskrivning |
|---------|-----|-------|-------------|
| 15 | `15_kostnadsoptimering.md` | Kostnadsoptimering och resurshantering | Ekonomisk optimering av resurser |
| 16 | `16_migration.md` | Migration från traditionell infrastruktur | Migrationstrategier och best practices |

### Del 6: Organisatoriska aspekter (Kapitel 17-19)

| Kapitel | Fil | Titel | Beskrivning |
|---------|-----|-------|-------------|
| 17 | `17_organisatorisk_forandring.md` | Organisatorisk förändring och teamstrukturer | Organisationsutveckling för IaC |
| 18 | `18_team_struktur.md` | Team-struktur och kompetensutveckling för IaC | Teamorganisation och kompetensutveckling |
| 19 | `19_digitalisering.md` | Digitalisering genom kodbaserad infrastruktur | Digital transformation genom IaC |

### Del 7: Avancerade ämnen och framtid (Kapitel 20-22)

| Kapitel | Fil | Titel | Beskrivning |
|---------|-----|-------|-------------|
| 20 | `20_lovable_mockups.md` | Använd Lovable för att skapa mockups för svenska organisationer | AI-driven utveckling och prototyping |
| 21 | `21_framtida_trender.md` | Framtida trender och teknologier | Kommande utvecklingar inom området |
| 22 | `22_best_practices.md` | Best practices och lärda läxor | Samlade erfarenheter och rekommendationer |

### Del 8: Avslutning (Kapitel 23-25)

| Kapitel | Fil | Titel | Beskrivning |
|---------|-----|-------|-------------|
| 23 | `23_slutsats.md` | Slutsats | Sammanfattning och framtidsperspektiv |
| 24 | `24_ordlista.md` | Ordlista | Definitioner av viktiga termer |
| 25 | `25_om_forfattarna.md` | Om författarna | Information om bokens författare |

## Diagram och bilder

Katalogen `images/` innehåller:
- **Mermaid-filer** (`.mmd`): Källkod för diagram som automatiskt konverteras till PNG
- **PNG-filer** (`.png`): Genererade diagrambilder som används i boken

Varje kapitel har associerade diagram som illustrerar viktiga koncept och processer.

## Byggprocess

Boken byggs automatiskt genom:

1. **Diagram-generering**: Mermaid-diagram konverteras till PNG-bilder
2. **PDF-generering**: Alla kapitel kombineras till en komplett PDF med Pandoc
3. **Versionskontroll**: Hela processen är versionshanterad via Git

### Lokalt byggande

```bash
# Bygg hela boken
cd docs
./build_book.sh
```

### CI/CD

Boken byggs automatiskt vid ändringar i `docs/` katalogen genom GitHub Actions.

## Kapitel navigation

Kapitlen är numrerade 01-25 och organiserade för att:
- **Bygga på varandra logiskt**: Varje kapitel förutsätter kunskap från tidigare kapitel
- **Gruppera relaterade ämnen**: Liknande ämnen behandlas tillsammans
- **Balansera teori och praktik**: Teoretiska grunder följs av praktiska implementationer
- **Anpassas för svenska förhållanden**: Specifika hänsyn till svenska regelkrav och organisationskultur

## Målgrupp

Boken riktar sig till:
- IT-arkitekter och systemdesigners
- DevOps-ingenjörer och infrastrukturspecialister
- Utvecklare som arbetar med molnteknologier
- Teknikledare och beslutsfattare
- Projektledare för digitaliseringsinitiativ

## Författare och bidragsgivare

Se `25_om_forfattarna.md` för detaljerad information om bokens författare och bidragsgivare.

---

*Denna dokumentation uppdaterades senast: 2024-09-20*