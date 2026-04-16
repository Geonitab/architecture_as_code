# Cut Proposal: Halvera Architecture as Code

**Datum:** 2026-04-16
**Branch:** `claude/review-simplify-text-pe5y9`
**Premiss:** Hälften av all text ska bort utan substansförlust.
**Resultat av granskning:** ~65 % kan strykas (mer än målet).

---

## Sammanfattning

Fyra parallella kritiska granskningar (per bokdel) har gått igenom 38 manuskriptfiler om totalt **~14 955 rader**. Granskningarna identifierar **~9 760 rader (≈65 %)** som kan strykas utan att förlora pedagogiskt värde — i flera fall **förbättras** kvaliteten genom konsolidering, borttagna dubbletter och eliminerad fillertext.

| Bokdel | Rader nu | Rader efter | Reduktion |
|--------|----------|-------------|-----------|
| Part A & B (kap 1–8) | 3 494 | ~1 744 | **-50 %** |
| Part C & D (kap 9–16) | 2 986 | ~1 220 | **-59 %** |
| Part E & F (kap 17–24) | 2 027 | ~780 | **-61 %** |
| Part G & H (kap 25–34) | 6 458 | ~1 464 | **-77 %** |
| **Totalt** | **~14 965** | **~5 208** | **-65 %** |

---

## De fem strukturella huvudfynden

### 1. Appendix 30 är 28 % av hela boken (4 267 rader)

`30_appendix_code_examples.md` innehåller 25+ fullständiga produktionskod-filer i löpande text. I tryck/PDF går de inte att kopiera; i ett repo finns de redan. Förslag: flytta ~85 % till `aac-examples/`-repo, behåll fyra representativa listningar. **Besparing: ~3 700 rader.**

### 2. Säkerhetsspåret behandlar samma material 4 gånger

Kapitlen 9 / 9B / 9C / 10 / 11 / 12 (1 669 rader) upprepar OPA/Rego, "assure once, comply many", STRIDE, HashiCorp state-protection, kvantum-krypto och samma Rego-exempel i 3–5 olika kapitel. Kap 9B är 80 % kod-bloat (eller stub-Python som erkänner sig vara tom). Förslag: konsolidera till 4 kapitel om totalt ~620 rader. **Besparing: ~1 050 rader.**

### 3. Org-/ledarskapsspåret är generisk konsultjargong

Kap 17 (organisational change), 18 (team structure), 19 (management as code) säger samma sak om cross-functional teams, DORA, psychological safety och competency frameworks. Kap 23 (`soft_as_code_interplay`) är ett rent metakapitel som rekapitulerar tidigare innehåll. Kap 21 (`digitalisation`) är generisk McKinsey-prosa med trasig kod (Python-modulen `terraform_runner` finns inte) som hör hemma i en strategibok, inte i denna. **Besparing: ~1 250 rader.**

### 4. Bokens egen meta-dokumentation har spritt sig in i manuskriptet

Kap 29 (about the author, 143 rader) duplicerar kap 31 (publishing toolchain) som duplicerar `docs/STYLE_GUIDE.md`. Inkluderar dessutom uttalsguide för svenska vokaler. Kap 31 ägnar 200 rader åt hur denna bok byggdes. **Besparing: ~280 rader.**

### 5. Kritiska kvalitetsbuggar

* **4 brutna länkar i `33_references.md`** (`26a_future_trends.md`, `10_policy_as_code.md`, `32_index.md`, `20_team_structures.md` — inga av dessa filer finns).
* **Strukturell förvirring i 26A**: filen kallas sig "placerad i Part A" men numreras 26A.
* **Inkonsekvent ton**: endast kap 11 och 15A har "Learning Objectives" — antingen överallt eller ingenstans.
* **Vilseledande kod**: `12_compliance.md` har ECDSA P-384-tagg märkt "Post-Quantum"; `21_digitalisation.md` har Python-importer från fiktivt paket; `16_migration.md` har CloudFormation med utdaterad AMI från 2020.

---

## Topp-15 mest brutala kapsningar (per rader sparade)

| # | Plats | Åtgärd | Rader |
|---|-------|--------|-------|
| 1 | `30_appendix_code_examples.md:1006–1858` (12 testimplementationer) | Flytta till externt repo, behåll 1 | ~800 |
| 2 | `30_appendix_code_examples.md:1860–2438` (17_CODE_1–3) | DELETE — pseudo-pedagogisk YAML/Python | ~570 |
| 3 | `30_appendix_code_examples.md:3283–3734` (OSCAL 10_CODE_2–4) | Flytta till externt repo | ~400 |
| 4 | `30_appendix_code_examples.md:115–421` (Jenkinsfile) | DELETE — dublett till GitHub Actions | ~295 |
| 5 | `30_appendix_code_examples.md:3872–4259` (Structurizr workspace) | Flytta/trimma till 100 rader | ~290 |
| 6 | `appendix_templates_and_tools.md:23–333` (Migration Python) | Flytta till externt repo | ~305 |
| 7 | `30_appendix_code_examples.md:423–686` (Terratest VPC) | Flytta till externt repo | ~255 |
| 8 | `09b_security_patterns.md:312–586` (stub-Python) | DELETE | ~260 |
| 9 | `23_soft_as_code_interplay.md` (hela kapitlet) | STRYK kapitlet | ~240 |
| 10 | `09b_security_patterns.md:77–282` (Terraform-modul) | Flytta till appendix | ~190 |
| 11 | `12_compliance.md:67–252` (AI/serverless/quantum-kod) | DELETE — off-topic | ~180 |
| 12 | `16_migration.md:203–387` (bash/Python migration script) | Flytta till externt repo | ~170 |
| 13 | `19_management_as_code.md:72–251` (transparency-prosan) | DELETE — GitHub-reklam | ~140 |
| 14 | `13_testing_strategies.md:101–232` (Vitest-sektion) | DELETE — off-topic för AaC | ~120 |
| 15 | `06_structurizr.md:1050–1220` (challenges + Python validator) | KORTA 70 % | ~115 |

**Topp-15 ger ensamt ~4 330 rader bort.**

---

## Strukturella beslut som krävs

### A. Slå ihop / stryk dessa kapitel

| Kapitel | Beslut | Motivation |
|---------|--------|-----------|
| `09b_security_patterns.md` | **STRYK som eget kapitel** | 80 % kod-bloat eller stub-Python; rester flyttas till kap 9 + appendix |
| `09c_risk_and_threat_as_code.md` | **SLÅ IHOP med kap 9** | Stubb (91 rader) som duplicerar threat modelling och risk-tema |
| `14_practical_implementation.md` | **SLÅ IHOP med kap 13 eller Part D-intro** | Stubb (106 rader) som mest hänvisar till appendix |
| `17_organisational_change.md` + `18_team_structure.md` + `19_management_as_code.md` | **KONSOLIDERA till ett kapitel** | ~70 % överlapp i tema och i konkret formulering |
| `23_soft_as_code_interplay.md` | **STRYK kapitlet helt** | Rent metakapitel; ersätt med 25-radersavsnitt i kap 22 |
| `21_digitalisation.md` | **OMPRÖVA EXISTENS** | Off-topic strategiprosa + trasig kod; behåll endast EU-suveränitet, flytta till kap 11 eller 15 |

### B. Cross-cutting principbeslut

1. **Verktygs-introduktioner finns på exakt ett ställe.** OPA/Rego presenteras endast i kap 10. STRIDE endast i kap 9. "Assure once, comply many" endast i kap 11. Övriga kapitel refererar dit.
2. **Kod-block över 30 rader hör hemma i externt exempel-repo.** Inline endast representativa snutter.
3. **Inga "Learning Objectives"** — antingen överallt eller ingenstans. Förslag: ta bort de två som finns (kap 11, 15A).
4. **Inga "Sources"-listor som upprepar `33_references.md`.** En källa = en plats.
5. **Inga "Speculative"-/"Future"-sektioner i tekniska kapitel.** Hör i kap 25.
6. **Inga själv-referenser till bokens repo, byggprocess eller publishing toolchain** i manuskriptet. Hör i README/CONTRIBUTING.

### C. Tonkonsekvens

Stryk genomgående: *"comprehensive"*, *"sophisticated"*, *"mature"*, *"backbone"*, *"modern"*, *"pays dividends"*, *"transformation journey"*, *"mindset"* använt utan kontext. Ersätt EU-mantra-öppningar (`"European organisations face..."`) med direkt påstående.

---

## Genomförandeplan

### Fas 1 — Strukturella beslut (vecka 1)
1. Bekräfta att kap 9B, 9C, 14, 23 stryks/konsolideras (uppdatera `docs/book_index.json`).
2. Skapa exempel-repo `aac-examples/` (eller motsvarande) för flyttad kod.
3. Fixa de fyra brutna länkarna i `33_references.md`.

### Fas 2 — Stora kapsningar (vecka 2–3)
4. Tömma appendix 30 (största enskilda vinst, ~3 700 rader).
5. Konsolidera säkerhetsspåret 9/9b/9c/10/11/12.
6. Konsolidera org-spåret 17/18/19.
7. Stryk kap 23.

### Fas 3 — Per-kapitel-trim (vecka 4)
8. Korta kap 2, 5, 6, 13, 16 enligt findings-listor.
9. Korta kap 25, 27, 29, 31.
10. Stryk EU-buzzword-strofer och marknadsspråk.

### Fas 4 — Validering
11. Kör `python3 scripts/verify_links.py`.
12. Kör `python3 scripts/verify_sources.py`.
13. Kör `python3 -m pytest tests/ -v`.
14. Bygg boken: `python3 generate_book.py && docs/build_book.sh`.

---

## Issue-grupper

Alla findings spåras som GitHub-issues med label `documentation`, `simplify` (ny). Issues är grupperade per kapitel/spår — **inte** en issue per finding (det skulle vara ~80 issues). De största strukturella besluten har egna issues för diskussion.

Se issuelista i repo (filtrera på label `simplify`).

---

## Tre största risker med detta förslag

1. **Förlust av avsedd publik:** Boken är i nuvarande skick svår att navigera men *genomgripande*. Om man stryker 65 % riskerar man att förlora den läsare som vill ha en uttömmande referens. **Motåtgärd:** flyttad kod måste finnas i ett välorganiserat repo med tydliga länkar.
2. **EU-/sovereignty-vinkeln tunnar ut:** Många kapitel öppnar med EU-mantra. Stryker man det blir boken mindre tydligt riktad mot EU-arkitekter — vilket kan vara bokens marknadsdifferentiering. **Motåtgärd:** behåll EU-vinkeln i kap 10, 12, 25 där den är tekniskt motiverad.
3. **Strukturella ändringar bryter länkar och tester:** Stryker man kap 9B, 9C, 14, 23 bryts allt som refererar till dem (book_index.json, tester, references.md). **Motåtgärd:** Fas 1 behöver göras innan Fas 2 startar.

---

## Beslutspunkt

**Ska vi gå vidare med Fas 1 (strukturella beslut)?** Författaren behöver godkänna:
- Konsolidering 9B/9C/14/23.
- Att appendix 30 i huvudsak flyttas till externt repo.
- Att kap 21 antingen omarbetas till EU-cloud-fokus eller stryks.
