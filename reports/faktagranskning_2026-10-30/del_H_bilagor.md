<!-- Delrapport från faktagranskningen 2026-10-30. Genererad av granskningsagent; sammanställd i README.md i samma katalog. -->

# Faktagranskning – Del H (bilagor och supplement)

Granskningsdatum: 2026-10-30. Granskare: Lead Researcher (faktagranskning, endast bedömning – inga filer i repot har ändrats).

## Omfattning

Lästa filer (varje rad, i sin helhet):

- docs/part_h_appendices.md (32 rader)
- docs/28_glossary.md (119 rader)
- docs/29_about_the_author.md (143 rader)
- docs/31_appendix_b_technical_architecture.md (335 rader)
- docs/32_finos_project_blueprint.md (92 rader)
- docs/appendix_templates_and_tools.md (333 rader)
- docs/architecture_as_code_maturity_model.md (222 rader)
- docs/appendix_d_control_mapping_matrix_template.md (19 rader)
- docs/maturity_model_radar.html (1 929 rader – skummad; dimensioner, frågor, referenslänkar, poängberäkning och CDN-beroenden kontrollerade programmatiskt)

Jämförelseunderlag i repot: docs/book_index.json, docs/33_references.md, BOOK_REQUIREMENTS.md, requirements.txt, package.json, Makefile, Dockerfile.book-builder, docs/build_book.sh, docs/pandoc.yaml, docs/pandoc-nonlatex.yaml, mkdocs.yml, .github/workflows/*.yml (14 st), scripts/, tests/, templates/, generate_book.py, generate_presentation.py, generate_whitepapers.py, build_all_orchestrator.py, references/glossary_terms_relationships.json, references/calm_what_is_excerpt.txt, docs/examples/structurizr/, docs/30_appendix_code_examples.md (listning 17_CODE_1), docs/images/*.mmd för de refererade diagrammen.

Inventering: cirka 190 påståenden (ordlistedefinitioner 58, biografi/källor ca 25, Appendix B ca 60, Appendix C ca 25, mognadsmodell/mallar/radar ca 25). Cirka 120 verifierade mot repot, cirka 35 externa URL:er/källor kontrollerade med curl/WebFetch (GitHub-API och github.com blockeras av proxyn; raw.githubusercontent.com och WebFetch fungerade). WebSearch-budgeten tog slut efter tre sökningar; resterande extern verifiering gjordes via direkta hämtningar av primärkällor.

## Sammanfattning

De interna supplementen (mognadsmodellen, radarverktyget, kontrollmappningsmallen) är i huvudsak konsistenta med varandra: tio discipliner, 50 identiska checklistfrågor, sex nivåer (0–5) och en poängskala 0–5 stämmer överens. De allvarliga problemen ligger i stället i källhänvisningar och i beskrivningar av verkligheten utanför repot. Appendix C beskriver ett "FINOS Project Blueprint" som ett arkitekturinitiativ byggt på CALM – i verkligheten är finos/project-blueprint en repositorymall med licens- och styrningsfiler, och det beskrivna initiativet (blueprint-paket, fyrfasutrullning, evidenspipelines) går inte att belägga någonstans. Appendix B tillskriver FINOS-projektet en beskrivning (YAML-definitioner, plugin-arkitektur, CLI) som i själva verket beskriver ett annat projekt (jondavid-black/AaC), och hänvisar till ett `aacplatform/aac` som inte finns. Källan "Thoughtworks (2024) Architecture as Code: The Next Evolution" (Source [1]) går inte att hitta hos Thoughtworks; den cirkulerar i både Om författaren och Appendix C. Författarbiografins enda primärkälla (Kvadrat-profilen) ger 404 och konsulten saknas i Kvadrats konsultsök; två av de övriga tre källorna är inte identifierbara dokument. Appendix B:s beskrivning av bygg-pipelinen är till stora delar föråldrad: `build-book.yml`, `generate-presentations.yml`, `generate-whitepapers.yml` och `exports/`-trädet finns inte längre, antalet filer och whitepapers stämmer inte, och licensuppgiften CC BY 4.0 i Om författaren motsägs av pandoc.yaml ("All rights reserved") och av att repot saknar LICENSE-fil.

## Fynd

### H-01 "FINOS Project Blueprint" beskrivs som ett arkitekturinitiativ som inte finns
- **Fil:rad:** docs/32_finos_project_blueprint.md:1-3, 9, 25, 29-37, 41-47, 69-74
- **Påstående:** "The FINOS Project Blueprint initiative exists to prove that open collaboration can harden architectural practice without adding bureaucracy. [...] By combining the automation foundations described in the book's technical chapters with the Common Architecture Language Model (CALM), the blueprint offers a reusable playbook for regulated financial organisations" samt "Each blueprint package ships with CALM definitions for baseline platform components, recommended relationships for service integration, and metadata schemas"
- **Bedömning:** FEL / FELCITERAT
- **Allvarlighet:** Hög
- **Evidens:** Repot https://github.com/finos/project-blueprint beskriver sig som "Project blueprint for Fintech Open Source Foundation hosted projects" – en GitHub-repositorymall ("Use this template") med LICENSE, CONTRIBUTING, SECURITY, NOTICE, MAINTAINERS och uppförandekod som implementerar FINOS öppna styrning. Den nämner inte CALM och innehåller inga blueprint-paket, pipelines, operativmodeller eller utrullningsfaser. FINOS Architecture as Code-projektet (https://github.com/finos/architecture-as-code, calm.finos.org) listar sina delprojekt (CLI, Shared, Models, CALM Hub, CALM Server, Docs, Learning Lab, VS Code-plugin, CALM Guard/Studio) – inget "Project Blueprint". Hela appendixets innehåll (sjupersonsteam, fyrfasutrullning, evidens-pipelines, leverantörsscorecards) härrör från bokens egna Appendix A (17_CODE_1) och kapitel 5/17/24, inte från något FINOS-dokument.
- **Förslag:** Skriv om appendixet som ett *förslag/tankeexperiment* från författaren ("a blueprint proposal inspired by FINOS CALM"), ta bort formuleringar som att initiativet "exists", att "FINOS members can accelerate…" och att "Project Blueprint recommends…", och lägg till en tydlig notis att "Project Blueprint" i FINOS-sammanhang avser en repositorymall. Alternativt byt namn på appendixet (t.ex. "A CALM-based Blueprint for Regulated Platforms") så att läsaren inte förväxlar det med ett FINOS-projekt.

### H-02 AaC-beskrivningen i Appendix B tillskrivs fel projekt; `aacplatform/aac` finns inte
- **Fil:rad:** docs/31_appendix_b_technical_architecture.md:69, 71, 75, 323
- **Påstående:** "The `aacplatform/aac` toolkit is a separate open-source project" / "The official Architecture-as-Code (AaC) repository describes the initiative as an open-source toolkit for capturing architecture definitions as YAML and turning them into validated, executable assets through a command-line interface [...] (AaC Open Source Project)" / "AaC emphasises that every capability is delivered through discoverable plugins" / Sources: "FINOS Architecture as Code Project. Architecture-as-Code Repository. https://github.com/finos/architecture-as-code"
- **Bedömning:** FELCITERAT
- **Allvarlighet:** Hög
- **Evidens:** https://github.com/aacplatform/aac ger 404 (kontrollerat 2026-10-30). Beskrivningen "define a system in simple yaml", plugin-system och CLI (`aac check …`, PyPI-paket `aac`) matchar repot https://github.com/jondavid-black/AaC ("Prototype Arch-as-Code", fork av DevOps-MBSE/AaC). FINOS-repot som anges som källa beskriver i stället CALM: "Architecture as Code (AasC) aims to devise and manage software architecture via a human and machine readable…", bygger på ett JSON Meta Schema och installeras med `npm install -g @finos/calm-cli` (calm.finos.org/introduction/what-is-calm). FINOS-README:n beskriver varken YAML-definitioner eller plugin-arkitektur. I docs/33_references.md:42 heter samma post dessutom "AaC Open Source Project", vilket inte stämmer med Appendix B:s "FINOS Architecture as Code Project".
- **Förslag:** Ersätt not och stycken med en korrekt beskrivning av FINOS CALM (JSON-schema, nodes/relationships/metadata, calm-cli) om det är FINOS som avses, eller byt källa till jondavid-black/AaC (DevOps-MBSE/AaC) om det YAML-/pluginbaserade verktyget avses. Ta bort referensen till `aacplatform/aac`. Harmonisera författarnamnet i 33_references.md.

### H-03 Source [1] "Thoughtworks (2024). Architecture as Code: The Next Evolution" går inte att belägga
- **Fil:rad:** docs/29_about_the_author.md:142; docs/32_finos_project_blueprint.md:91 (och docs/33_references.md:7, 144)
- **Påstående:** "**Thoughtworks (2024).** *Architecture as Code: The Next Evolution.* Technology Radar. [Source [1]]"
- **Bedömning:** FELCITERAT / EJ VERIFIERBART (sannolikt fantomkälla)
- **Allvarlighet:** Hög
- **Evidens:** Posten saknar URL i 33_references.md. https://www.thoughtworks.com/radar/techniques/architecture-as-code returnerar samma generiska sida "Techniques | Thoughtworks" som en påhittad slug (…/this-blip-does-not-exist-xyz), medan en verklig blip (…/infrastructure-as-code) returnerar en egen sida med titeln "Infrastructure as code | Technology Radar". Teknikkvadranten i Vol. 34 (april 2026) innehåller ingen blip "Architecture as Code" (närmast är "Architecture drift reduction with LLMs"). Frasen "The Next Evolution" förekommer inte. Blip-historiksidor kunde inte hämtas, så en äldre arkiverad blip kan inte helt uteslutas – men ingen Thoughtworks-publikation med den titeln har kunnat identifieras.
- **Förslag:** Ta bort eller ersätt Source [1] med en verifierbar källa (t.ex. FINOS CALM-dokumentationen, eller Thoughtworks faktiska blips "Diagrams as code"/"Infrastructure as code" med URL och volym). Eftersom Source [1] återanvänds i många kapitel bör åtgärden samordnas med granskningen av 33_references.md.

### H-04 Licensuppgiften CC BY 4.0 motsägs av repot
- **Fil:rad:** docs/29_about_the_author.md:119-128; docs/31_appendix_b_technical_architecture.md:333
- **Påstående:** "This work is licensed under the Creative Commons Attribution 4.0 International Licence (CC BY 4.0)." / "**Transparency**: Open-source code and a fully documented process."
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Hög
- **Evidens:** Repot innehåller ingen LICENSE-fil (ls LICENSE* → saknas; GitHub-API: `"license": null`; package.json säger "SEE LICENSE IN LICENSE"). docs/pandoc.yaml:73-75 trycker i varje PDF: "Copyright © … Architecture as Code Editorial Team … All rights reserved. This book is made available under open-source principles". README.md, CONTRIBUTING.md och docs/index.md nämner ingen licens. Utan licensfil är varken "CC BY 4.0" eller "open-source code" rättsligt belagt, och "All rights reserved" står i direkt konflikt med CC BY.
- **Förslag:** Besluta om licens, lägg till LICENSE (och ev. separat licens för kod respektive text), och uppdatera pandoc.yaml:s release-sida så att den anger samma licens som Om författaren.

### H-05 Beskrivna GitHub Actions-arbetsflöden finns inte längre
- **Fil:rad:** docs/31_appendix_b_technical_architecture.md:147-165, 192-194; docs/32_finos_project_blueprint.md:65
- **Påstående:** "`build-book.yml` automates the entire publication process" (med YAML `name: Build Book … timeout-minutes: 90`), "**Content Validation** (`content-validation.yml`): Markdown syntax checks, link validation, and language quality control", "**Presentation Generation** (`generate-presentations.yml`)", "**Whitepaper Generation** (`generate-whitepapers.yml`)", "Workflows derived from `build-book.yml`"
- **Bedömning:** FÖRÅLDRAT / FEL
- **Allvarlighet:** Hög
- **Evidens:** .github/workflows/ innehåller: assign-codex2.yml, build-mkdocs.yml, claude-code-review.yml, claude.yml, clean-fixed-issues.yml, clean-old-braches.yml, content-validation.yml, issue-create-draft-pr.yml, mermaid-designer-bot.yml, structurizr-diagrams.yml, unified-build-release.yml, validate-doc-numbering.yml, verify-mermaid-diagrams.yml. Varken build-book.yml, generate-presentations.yml eller generate-whitepapers.yml finns. unified-build-release.yml:4-6 säger uttryckligen att den "consolidates complete-release.yml, build-book-fast.yml, and build-book.yml"; den heter "Unified Build & Release", har `timeout-minutes: 60` och bygger via Docker-image (Dockerfile.book-builder) – inte 90 minuter och inte stegvis installation. content-validation.yml kör `tests/run_tests.py` och pytest-sviterna completeness/consistency/clarity/technical_accuracy – ingen Markdown-syntaxkontroll eller länkvalidering (scripts/verify_links.py som CLAUDE.md nämner finns för övrigt inte heller i scripts/).
- **Förslag:** Beskriv unified-build-release.yml (triggers på docs/**/*.md, *.mmd, generatorskript, templates, pandoc.yaml, Dockerfile; Docker-bygge med GHA-cache; release via softprops/action-gh-release) samt build-mkdocs.yml, verify-mermaid-diagrams.yml, validate-doc-numbering.yml och structurizr-diagrams.yml. Ändra content-validation-beskrivningen till "pytest-baserade innehållstester (fullständighet, konsekvens, läsbarhet, teknisk korrekthet)".

### H-06 Källorna till författarbiografin är döda eller oidentifierbara
- **Fil:rad:** docs/29_about_the_author.md:140-143 (och docs/33_references.md:84-97)
- **Påstående:** "**Kvadrat AB (2024).** *Gunnar Nordqvist – Chief Architect Profile.* … https://www.kvadrat.se/anlita-kvadrat/hitta-konsult/gunnar-nordqvist/" / "**Kvadrat AB (2024).** *Technology Consulting Excellence.* Company Profile. https://www.kvadrat.se/" / "**GitHub Open Source Community (2024).** *Collaborative Software Development.* Platform Documentation."
- **Bedömning:** FELCITERAT (död länk + fantomtitlar)
- **Allvarlighet:** Hög
- **Evidens:** Profil-URL:en ger HTTP 404 (curl och WebFetch, 2026-10-30). Kvadrats konsultsök har flyttat till https://anlita.kvadrat.se/ (302 från hitta-konsult-sidan); sökning på "Nordqvist" där ger "Ingen träff" bland 339 listade konsulter. Startsidan kvadrat.se innehåller inget dokument med titeln "Technology Consulting Excellence" – det är en påhittad rubrik för en hemsida. "GitHub Open Source Community – Collaborative Software Development – Platform Documentation" saknar URL och motsvarar inget identifierbart GitHub-dokument.
- **Förslag:** Ersätt källa 1 med en fungerande profil-URL (eller ta bort den om profilen är avpublicerad), byt källa 2 till "Kvadrat. *Om Kvadrat.* https://www.kvadrat.se/ (hämtad ÅÅÅÅ-MM-DD)" och stryk källa 4 (eller ersätt med konkret GitHub Docs-sida med URL). Uppdatera motsvarande poster i 33_references.md.

### H-07 Kodexemplet i Appendix D anropar åtta metoder som inte finns
- **Fil:rad:** docs/appendix_templates_and_tools.md:23-213 (särskilt 48-51, 59-61, 88-89)
- **Påstående:** Klassen `InfrastructureMigrationAssessment` presenteras under "Migration Assessment Automation" som en kanonisk tillgång "so that practitioners can embed them directly into their delivery workflows" (rad 3).
- **Bedömning:** FEL (koden kan inte köras)
- **Allvarlighet:** Medel
- **Evidens:** Följande metoder anropas men definieras aldrig: `_find_unmanaged_rds`, `_find_unmanaged_load_balancers`, `_find_unmanaged_security_groups`, `_assess_migration_complexity`, `_estimate_migration_effort`, `_assess_migration_risks`, `_calculate_migration_priority`, `_estimate_downtime` → `discover_unmanaged_resources()` kastar AttributeError. `import pandas as pd` används inte. Taggnycklarna `terraform:stack` och `pulumi:stack` (rad 99-100) är inga standardtaggar (varken Terraform eller Pulumi taggar resurser automatiskt); endast `aws:cloudformation:stack-name` är en verklig systemtagg. Kodblocket saknar dessutom inledande text och hör tematiskt till kapitel 16, inte till "Templates and Tools".
- **Förslag:** Komplettera med stubbar/implementationer eller märk blocket uttryckligen som utdrag ("excerpt – helper methods omitted"). Ta bort oanvänd import och de påhittade taggnycklarna (eller skriv "organisation-specific tags such as ManagedBy"). Överväg att flytta blocket till Appendix A/kapitel 16.

### H-08 Felaktigt antal manuskriptfiler och föråldrat filträd
- **Fil:rad:** docs/31_appendix_b_technical_architecture.md:15-32
- **Påstående:** "Book content is organised in 31 Markdown files within the `docs/` directory, where each file represents a chapter or appendix" följt av träd med "# Technical chapters (04–21)", 21, 23, 24, 25, 27, 28–31.
- **Bedömning:** FEL / FÖRÅLDRAT
- **Allvarlighet:** Medel
- **Evidens:** docs/ innehåller 37 numrerade kapitel-/bilagefiler (01–33 plus 09b, 09c, 15a, 26a, 26b) samt appendix_templates_and_tools.md, tre supplement, åtta delintroduktioner och 00_front_cover.md – totalt 63 .md-filer. book_index.json: 31 kapitel + 7 bilagor + 3 supplement; BOOK_REQUIREMENTS.md: `total_chapters: 38`. Siffran 31 motsvarar enbart kapitlen, men meningen säger "chapter or appendix". Trädet saknar 22, 26a, 26b, 32, 33, appendix_templates_and_tools.md, mognadsmodellen och part_*.md.
- **Förslag:** Skriv "38 numbered chapter and appendix files (plus part introductions, front cover and supplements)" och generera trädet från book_index.json.

### H-09 Kodutdrag för pandoc.yaml och mmdc stämmer inte med repot
- **Fil:rad:** docs/31_appendix_b_technical_architecture.md:83-100, 111-122
- **Påstående:** `subtitle: "Infrastructure as Code (Architecture as Code) in practice"`; `mmdc -in "$mmd_file" -o "$png_file" -t default -b transparent --width 1400 --height 900`
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Medel
- **Evidens:** docs/pandoc.yaml:28 har `subtitle: "A practical handbook for Infrastructure as Code"` och dessutom `from: markdown+bracketed_spans`, `highlight-style: tango`, `date`, `language: en-GB`. docs/build_book.sh:368-386 använder `mmdc -i … -t default -c mermaid-kvadrat-theme.json -b transparent --width 1400 --height 900 [--puppeteerConfigFile …]`; flaggan `-in` finns inte i Mermaid CLI (korrekt är `-i/--input`). EPUB/DOCX byggs med en separat defaults-fil docs/pandoc-nonlatex.yaml (build_book.sh:159, 553-592), vilket appendixet inte nämner ("pandoc.yaml … defines all format-specific settings").
- **Förslag:** Klistra in faktiska utdrag ur pandoc.yaml och build_book.sh; nämn pandoc-nonlatex.yaml och Kvadrat-temat.

### H-10 Beskrivningen av arbetsflödets steg och cachning motsvarar inte den faktiska pipelinen
- **Fil:rad:** docs/31_appendix_b_technical_architecture.md:169-179
- **Påstående:** "Environment setup (15 minutes): Install Python 3.12. Install TeX Live and XeLaTeX (8+ minutes). Install Pandoc 3.1.9. Install the Mermaid CLI with Chrome dependencies." / "Cache APT packages … Cache Python dependencies via pip. Cache Node.js modules."
- **Bedömning:** FÖRÅLDRAT
- **Allvarlighet:** Medel
- **Evidens:** unified-build-release.yml bygger Docker-imagen Dockerfile.book-builder (ubuntu:22.04, texlive, Pandoc 3.1.9 .deb, Node 20 + mermaid-cli 10.7.0, Google Chrome, Eisvogel) med `docker/build-push-action@v6` och `cache-from/cache-to: type=gha`. I arbetsflödet finns ingen APT- eller pip-cache; enda ytterligare cache är `actions/setup-node@v4` med `cache: 'npm'` (och Node **18**, rad 179). Installationsstegen ligger alltså i Dockerfilen, inte som jobbsteg.
- **Förslag:** Beskriv Docker-baserat bygge med lagercache; ta bort APT/pip-cache-påståendena eller ersätt med "Docker layer cache (GitHub Actions cache backend)".

### H-11 `exports/book-cover/`-trädet finns inte; CSS-utdraget kommer från presentationsmallen
- **Fil:rad:** docs/31_appendix_b_technical_architecture.md:244-281
- **Påstående:** "The book cover is produced through an HTML/CSS design system: templates/book-cover.svg … exports/book-cover/source/book-cover-final.html … BRAND_GUIDELINES.md … DESIGN_SYSTEM.md … pdf/ png/ jpg/ svg/" samt CSS ".title { font-size: 72px; font-weight: 800; line-height: 0.9; letter-spacing: -2px; }"
- **Bedömning:** FÖRÅLDRAT / INKONSEKVENT
- **Allvarlighet:** Medel
- **Evidens:** Katalogen exports/ finns inte; .gitignore:38-40 lyder "# Prevent legacy export directories from returning / exports/ / exports_old/". Filerna book-cover-final.html, book-cover.html, BRAND_GUIDELINES.md och DESIGN_SYSTEM.md ligger i docs/archive/book-cover/source/ (en arkivkatalog som mkdocs.yml exkluderar). Omslaget renderas i build_book.sh:297-314 från templates/book-cover.svg till images/book-cover.png. Variablerna `--kvadrat-blue: hsl(221, 67%, 32%)` m.fl. och `--success: hsl(160, 84%, 30%)` finns i templates/presentation-template.html:16-21 (inte i omslaget); där är `letter-spacing: -0.025em`, och "line-height: 0.9"/"letter-spacing: -2px" förekommer inte.
- **Förslag:** Beskriv den faktiska omslagskedjan (SVG → PNG i build_book.sh, pandoc `include-before`) och ange att designkällorna är arkiverade i docs/archive/book-cover/. Citera CSS från rätt fil eller stryk.

### H-12 Antal whitepapers och påstådda funktioner stämmer inte
- **Fil:rad:** docs/31_appendix_b_technical_architecture.md:285-291
- **Påstående:** "**Twenty-six whitepapers**: One per chapter." / "**Localisation**: Tuned for each target organisation's context." / "**Search optimisation**: Accurate metadata and structure."
- **Bedömning:** FÖRÅLDRAT / TVEKSAMT
- **Allvarlighet:** Medel
- **Evidens:** generate_whitepapers.py:242-269 hämtar kapitelmappningen från BOOK_REQUIREMENTS.md (38 kapitel) och varnar om `generated_count != len(chapter_mapping)` → 38 whitepapers, inte 26. Skriptet innehåller ingen lokaliserings-/översättningslogik (grep på locali/translat ger inga träffar). templates/whitepaper-template.html saknar `<meta name="description|keywords|author">`.
- **Förslag:** Skriv "one whitepaper per chapter (38 at the time of writing, driven by BOOK_REQUIREMENTS.md)"; stryk "Localisation" eller omformulera till "Context section per chapter"; verifiera eller stryk SEO-påståendet.

### H-13 generate_book.py och generate_presentation.py beskrivs/citeras felaktigt
- **Fil:rad:** docs/31_appendix_b_technical_architecture.md:60-65, 200-218
- **Påstående:** "The system uses `generate_book.py` to generate and update chapter content automatically: Iterative generation … Mermaid integration: Automatically generates diagram placeholders …" samt kodblocket `generate_presentation_outline()` med `glob.glob(str(docs_dir / "*.md"))`.
- **Bedömning:** FÖRÅLDRAT / INKONSEKVENT
- **Allvarlighet:** Medel
- **Evidens:** generate_book.py:170-260, 624-630: CLI:n kräver `--format epub` och bygger EPUB från kapitellistan i book_index.json via scripts/navigation.py; utan argument skrivs ett "manual content notice". Den äldre funktionen `generate_iac_book_content()` skriver ett fåtal .mmd-filer men ingen "iterativ batchgenerering" av kapitel. Den verkliga `generate_presentation_outline()` (generate_presentation.py:1352-1375) läser BOOK_REQUIREMENTS.md via `load_book_requirements()` och faller tillbaka på `_iter_primary_markdown_files()`; kodutdraget i appendixet är en förenklad äldre version.
- **Förslag:** Beskriv generate_book.py som "EPUB-bygge och kapitelurval (--all/--sample/--chapters) baserat på book_index.json"; märk kodutdrag som förenklade eller kopiera aktuell kod.

### H-14 Mognadsmodellens källor: odefinierad [13] och felattribuerad [1]
- **Fil:rad:** docs/architecture_as_code_maturity_model.md:30-31, 214-222
- **Påstående:** "Ch. 5 Automation & CI/CD [13]" / "Ch. 6 Structurizr [1]" / "[1]: https://github.com/dwmkerr/architecture-as-code "Architecture as Code GitHub Repository""
- **Bedömning:** FELCITERAT / INKONSEKVENT
- **Allvarlighet:** Medel
- **Evidens:** Källistan definierar endast [1]–[9]; [13] saknas. dwmkerr/architecture-as-code är "A project to help define architecture logically as code, and generate living, interactive diagrams" – ett YAML→diagram-verktyg (`aac-cli`) utan koppling till Structurizr (som bara nämns i dess "Alternatives"-lista) eller FINOS. Övriga källor [2]–[9] är rå-URL:er till bokens egna kapitel på raw.githubusercontent.com (alla svarar 200), dvs. självreferenser i stället för interna länkar.
- **Förslag:** Byt [13] till [1]/korrekt nummer; ersätt [1] med Structurizr-dokumentationen (https://docs.structurizr.com/dsl) eller kapitel 6; gör om [2]–[9] till relativa länkar (05_automation_devops_cicd.md etc.).

### H-15 Appendix D överdriver mognadsmodellens och radarverktygets funktioner
- **Fil:rad:** docs/appendix_templates_and_tools.md:7, 11
- **Påstående:** "describes six adoption levels … Each level contains assessment prompts, operating model guidance, and measurable outcomes" / "It enables leadership teams to capture current-state and target-state indicators, compare trajectories across business units, and export radar charts for strategy reviews."
- **Bedömning:** TVEKSAMT / INKONSEKVENT
- **Allvarlighet:** Medel
- **Evidens:** Nivåerna 0–5 (architecture_as_code_maturity_model.md:134-188) är korta punktlistor; checklistfrågorna är organiserade per disciplin, inte per nivå, och inga mätbara utfall anges per nivå. maturity_model_radar.html stöder endast ja/nej-svar för nuläge (rad 1086-1099), normaliserad poäng 0–5 (rad 1206-1207), Mermaid-radar, JSON-export/import (rad 1136-1163, 1651) och PDF-export av förbättringsförslag (jsPDF, rad 996-1005). Det finns inget målläge ("target state") och ingen jämförelse mellan affärsenheter.
- **Förslag:** "describes six maturity levels (0–5) and a per-discipline yes/no checklist" samt "captures current-state answers, plots a radar chart, lists prioritised improvement suggestions with chapter references, and exports JSON/PDF".

### H-16 Sju referenslänkar i radarverktyget pekar på ankare som inte finns
- **Fil:rad:** docs/maturity_model_radar.html (reference.url på raderna 400-949, bl.a. 422, 433, 687-720, 733, 755, 777, 858)
- **Påstående:** Länkar som `06_structurizr/#integration-with-ci-cd-pipelines`, `13_testing_strategies/#best-practices-for-infrastructure-testing-with-vitest`, `23_soft_as_code_interplay/#knowledge-and-culture-as-code`
- **Bedömning:** FEL (brutna interna länkar)
- **Allvarlighet:** Medel
- **Evidens:** Programmatisk kontroll av 37 unika referens-URL:er mot kapitelrubrikerna (MkDocs-slugifiering) visar 7 utan motsvarande ankare: 02_fundamental_principles/#the-declarative-approach-in-architecture-as-code; 06_structurizr/#integration-with-ci-cd-pipelines (faktiskt ankare: integration-with-cicd-pipelines); 06_structurizr/#structurizr-architecture-modeling-as-code (H1 har id "structurizr"); 12_compliance/#compliance-and-regulatory-adherence (H1-id "compliance"); 13_testing_strategies/#best-practices-for-infrastructure-testing-with-vitest (ingen sådan rubrik); 13_testing_strategies/#testing-strategies-for-infrastructure-as-code (H1-id "testing-strategies"); 23_soft_as_code_interplay/#knowledge-and-culture-as-code (faktiskt: knowledge-as-code-and-culture-as-code). Länkarna fungerar endast på MkDocs-sajten (use_directory_urls), inte i PDF/EPUB.
- **Förslag:** Rätta ankarna och lägg till en länkkontroll av radar-HTML:en i tests/ eller scripts/.

### H-17 Ordlistans "relationsdatabas" är ur synk och används inte av några pipelines
- **Fil:rad:** docs/28_glossary.md:107
- **Påstående:** "A structured dataset now lives at `references/glossary_terms_relationships.json` so automation can reason about how concepts reinforce one another. Pipelines use it to surface dependencies in pull requests, populate architecture decision templates, and keep presentation material aligned with the book's vocabulary."
- **Bedömning:** TVEKSAMT / INKONSEKVENT
- **Allvarlighet:** Medel
- **Evidens:** Enda konsument i repot är tests/test_glossary_dataset.py (grep över *.py/*.yml/*.sh/*.md). Inget arbetsflöde eller skript läser filen för PR-kommentarer, ADR-mallar eller presentationer. Datasetet (54 termer) saknar fem av ordlistans 58 termer – Continuous Improvement Loop, Anti-Pattern, Multi-Cloud Strategy, Edge Computing, CALM – och innehåller "Compliance Automation", som används i relationstabellen (rad 114-115) men inte definieras i ordlistan. Repots eget test `test_glossary_terms_match_dataset` skulle därmed falla. De fem relationerna i tabellen (documents, indexed_in, protects, validated_by, informed_by) finns däremot i JSON-filen.
- **Förslag:** Skriv "A structured dataset … is validated by the test suite and can be used by automation …" och synka JSON ↔ ordlista (lägg till de fem termerna, definiera Compliance Automation).

### H-18 Bildtexten "Blueprint governance spine" visar mognadstrappan
- **Fil:rad:** docs/32_finos_project_blueprint.md:5
- **Påstående:** "![Blueprint governance spine](images/diagram_32_maturity_model.png)"
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Medel
- **Evidens:** docs/images/diagram_32_maturity_model.mmd är en flowchart "Level 0 Initial / ad hoc → … → Level 5 Innovative / next-generation" – samma bild som mognadsmodellen använder (architecture_as_code_maturity_model.md:18 "Architecture as Code maturity staircase highlighting Levels 0 to 5"). Den har inget med en "governance spine" för blueprinten att göra.
- **Förslag:** Skapa ett eget diagram för Appendix C eller ändra bildtexten till "Maturity staircase reused as the blueprint's progression model".

### H-19 Motstridiga uppgifter om författarens relation till Kvadrat och om Kvadrat
- **Fil:rad:** docs/29_about_the_author.md:11, 31
- **Påstående:** "a self employed certified Chief Architect and IT Architect consultant associated with Kvadrat, a leading Swedish technology consultancy" (rad 11) kontra "Gunnar Nordqvist is a principal consultant at Kvadrat, a Scandinavian management and technology consultancy" (rad 31)
- **Bedömning:** INKONSEKVENT / TVEKSAMT
- **Allvarlighet:** Medel
- **Evidens:** kvadrat.se beskriver sig som "Sveriges största nätverk av egenföretagare" med 534 konsulter och kontor på elva orter i Sverige; ingen skandinavisk/nordisk verksamhet anges. Affärsmodellen (egenföretagare i nätverk) stödjer "self employed … associated with", men inte en anställningsliknande titel "principal consultant at Kvadrat". Titeln "principal consultant" förekommer inte i den (nu borttagna) profilen och kan inte verifieras.
- **Förslag:** Behåll en formulering: "an independent (self-employed) architect consultant in the Kvadrat network, a Swedish consultancy network of independent specialists". Stryk "Scandinavian" och "principal consultant".

### H-20 "Swedish Terminology Reference" förklarar institutioner som aldrig nämns
- **Fil:rad:** docs/29_about_the_author.md:35-40
- **Påstående:** "The Swedish organisations and institutions referenced here keep their native names … **KTH Royal Institute of Technology** … **Linköping University** … **Malmö University** …"
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Medel
- **Evidens:** grep över docs/*.md visar att KTH, Linköping och Malmö endast förekommer i just dessa rader – inget kapitel, ingen biografi och inget diagram (diagram_29_author_profile.mmd) refererar till dem. Avsnittet antyder utbildningsuppgifter som varken påstås eller kan verifieras.
- **Förslag:** Stryk de tre institutionsraderna (behåll Kvadrat AB och Nordqvist) eller lägg till den biografiska uppgift de ska förklara – om den är korrekt och verifierbar.

### H-21 Del H-introduktionen utelämnar Appendix C och Referenser; bilagebokstäver skiljer sig i repot
- **Fil:rad:** docs/part_h_appendices.md:9-21, 25-30
- **Påstående:** Beskriver Glossary, About the Author, Appendix A, Appendix B, Appendix D, Maturity Model och Control Mapping Matrix – men inte "Appendix C: FINOS Project Blueprint" (32) eller "References and Sources" (33).
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Medel
- **Evidens:** docs/book_index.json listar sju bilagor (28–34) inklusive 32 "Appendix C: FINOS Project Blueprint" och 33 "References and Sources". Beteckningarna är dessutom inkonsekventa i repot: book_index.json → appendix_templates_and_tools.md = Appendix D; BOOK_REQUIREMENTS.md → architecture_as_code_maturity_model.md = "Appendix D"; mkdocs.yml → mognadsmodellen = "Appendix E", radarverktyget = "Appendix F".
- **Förslag:** Lägg till stycken om Appendix C och Referenser i Del H; fastställ en bokstavsordning i book_index.json och spegla den i BOOK_REQUIREMENTS.md och mkdocs.yml.

### H-22 "structurizr.sh validate … on every pull request" stämmer inte med CI
- **Fil:rad:** docs/31_appendix_b_technical_architecture.md:135
- **Påstående:** "Run `structurizr.sh validate` against `docs/examples/structurizr/aac_reference_workspace.dsl` on every pull request."
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Låg
- **Evidens:** .github/workflows/structurizr-diagrams.yml triggas endast på pull requests som ändrar docs/examples/structurizr/**, de tre Structurizr-skripten eller arbetsflödet självt, och kör scripts/render_structurizr_diagrams.sh (Docker-image structurizr/cli:2024.03.01, `validate -w …` och `export`), inte `structurizr.sh`. Kommandot `validate` finns i Structurizr CLI (docs.structurizr.com/cli, kommandolista).
- **Förslag:** "validated in CI whenever the workspace or its tooling changes (structurizr-diagrams.yml, Structurizr CLI container)".

### H-23 Ordlistans CALM-post: fel kapitelhänvisning och oprecis karakterisering
- **Fil:rad:** docs/28_glossary.md:104
- **Påstående:** "The Common Architecture Language Model — a machine-readable, graph-based standard for describing architectural nodes, relationships, and metadata. (See [Chapter 32](32_finos_project_blueprint.md))"
- **Bedömning:** INKONSEKVENT / TVEKSAMT
- **Allvarlighet:** Låg
- **Evidens:** book_index.json betecknar 32 som "Appendix C", inte kapitel 32. CALM definieras officiellt som "an open-source specification developed by the Architecture as Code (AasC) community under FINOS … built on a JSON Meta Schema" (calm.finos.org/introduction/what-is-calm; identiskt med references/calm_what_is_excerpt.txt). "Graph-based standard" är en tolkning (noder/relationer bildar en graf) men inte FINOS egen beskrivning.
- **Förslag:** "an open-source FINOS specification (JSON Schema-based) describing architectures as nodes, relationships and metadata. (See Appendix C)".

### H-24 Chaos Monkey definieras som ett experiment i stället för Netflix verktyg
- **Fil:rad:** docs/28_glossary.md:63
- **Påstående:** "Chaos Monkey | A resilience experiment that deliberately terminates running resources to verify automated recovery, typically orchestrated through codified AaC workflows."
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Låg
- **Evidens:** Chaos Monkey är Netflix öppen källkods-verktyg som "randomly terminates virtual machine instances and containers that run inside of your production environment" (github.com/Netflix/chaosmonkey). Det är ett verktyg (en implementation av chaos engineering), inte "ett experiment", och det är inte "typically orchestrated through codified AaC workflows" – tillägget saknar stöd.
- **Förslag:** "Netflix's open-source tool that randomly terminates production instances to verify that services tolerate failure; an early, well-known chaos engineering implementation."

### H-25 Flera ordlistetermer används inte i boken trots löftet om spegling
- **Fil:rad:** docs/28_glossary.md:10, 39, 51, 52, 66, 75, 100, 101
- **Påstående:** "Each definition reflects the terminology used throughout the book." samt termerna Runbook Automation, Risk Assessment Matrix, Access Federation, Runway Health Check, Reserved and Spot Capacity, Digital Twin, AI for IT Operations/AIOps.
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Låg
- **Evidens:** grep (case-insensitive) över docs/[0-9]*.md och part_*.md exklusive ordlistan ger 0 träffar för var och en av dessa sju termer. "Access Federation" och "Runway Health Check" är dessutom icke-standardiserade begrepp (branschtermer: identity federation / federated identity; capacity or health review).
- **Förslag:** Stryk termer som inte används eller ändra meningen till "Definitions align with industry usage and, where applicable, with chapter usage"; byt "Access Federation" till "Identity Federation".

### H-26 GitOps-definitionen antyder push-modell
- **Fil:rad:** docs/28_glossary.md:32
- **Påstående:** "GitOps | Operating models that use a VCS as the single source of truth so that merges trigger automated reconciliation against live environments."
- **Bedömning:** TVEKSAMT
- **Allvarlighet:** Låg
- **Evidens:** OpenGitOps-principerna (CNCF, v1.0.0) är: Declarative, Versioned and Immutable, Pulled Automatically, Continuously Reconciled – dvs. agenter hämtar och avstämmer kontinuerligt; avstämningen "triggas" inte av merges.
- **Förslag:** "… where software agents continuously pull the declared state from version control and reconcile live environments against it (OpenGitOps principles)."

### H-27 Verktygskedjans versioner presenteras som aktuella men är tre år gamla / end-of-life
- **Fil:rad:** docs/29_about_the_author.md:50-53; docs/31_appendix_b_technical_architecture.md:170-173
- **Påstående:** "Python 3.12 … Pandoc 3.1.9 … XeLaTeX … Mermaid CLI" / "Install Pandoc 3.1.9. Install the Mermaid CLI with Chrome dependencies."
- **Bedömning:** FÖRÅLDRAT
- **Allvarlighet:** Låg
- **Evidens:** Pandoc 3.1.9 släpptes 2023-10-27; aktuell är 3.13 (2026-10-26) enligt pandoc.org/releases.html och changelog. Mermaid CLI 10.7.0 publicerades 2024-01-30; senaste är 12.0.0 (registry.npmjs.org). Node 20 (pinnad i BOOK_REQUIREMENTS.md/package.json: 20.11.1) nådde end-of-life 2026-04-30 och unified-build-release.yml använder Node 18 (EOL 2025-04-30) (endoflife.date). Pinningen är ett medvetet val, men texten bör datera den.
- **Förslag:** Skriv "pinned toolchain (as of release 2025.10): Pandoc 3.1.9, Mermaid CLI 10.7.0, Node 20.11.1" och överväg uppgradering (Node 22/24) i BOOK_REQUIREMENTS.md.

### H-28 Små källinkonsekvenser mellan bilagornas Sources och 33_references.md
- **Fil:rad:** docs/31_appendix_b_technical_architecture.md:323; docs/32_finos_project_blueprint.md:90-92
- **Påstående:** "FINOS Architecture as Code Project. Architecture-as-Code Repository." / "FINOS (2024). CALM …" / "Open Policy Agent (2024) … [Source [10]]"
- **Bedömning:** INKONSEKVENT
- **Allvarlighet:** Låg
- **Evidens:** 33_references.md:42 kallar samma post "AaC Open Source Project"; 33_references.md:66-67 anger att CALM-källan refereras i kapitel 22 men inte i Appendix C; Source [10] (rad 16) anger "[Chapter 32](32_index.md)" och Source [1] "[Chapter 26A](26a_future_trends.md)" – filerna 32_index.md, 26a_future_trends.md, 10_policy_as_code.md och 20_team_structures.md finns inte. Titel/år för Source [1] och [10] matchar däremot bilagornas Sources.
- **Förslag:** Harmonisera författarnamn och "Referenced in"-listor; rätta de fyra döda interna länkarna i 33_references.md (ligger utanför Del H men påverkar dess källor).

## Verifierat korrekt (urval)

- CALM:s definition och komponenter (nodes, relationships, metadata; JSON Meta Schema; `npm install -g @finos/calm-cli`) i Appendix C rad 19 och i references/calm_what_is_excerpt.txt stämmer med https://calm.finos.org/introduction/what-is-calm (hämtad 2026-10-30). https://calm.finos.org/ svarar 200.
- FINOS Architecture as Code-projektet är ett FINOS-projekt med lifecycle-badge "FINOS - Graduated" (raw README, finos/architecture-as-code); CALM v1.0 släpptes augusti 2025; 2026-roadmap lanserad (finos.org/community-spotlight/2026-matthew-bain). FINOS lifecycle-stadier: Forming, Labs, Incubating, Graduated, Archived (community.finos.org). Obs: calm.finos.org:s startsida visar fortfarande "FINOS incubating" – sajtens badge verkar inte uppdaterad. Appendix C påstår inget stadium, så detta är kontext.
- FINOS = Fintech Open Source Foundation, "an umbrella organization under the Linux Foundation" (finos.org/about-us). Påståendet (32:15) att FINOS underhåller specifikationer, referensimplementationer och datamodeller under öppen styrning är korrekt.
- Appendix C:s interna hänvisningar: "seven-person core team" = `size: 7` (1 lead + 2 senior infra + 1 security + 2 platform automation + 1 SRE) i docs/30_appendix_code_examples.md:1862-1975; "bi-weekly demos, monthly steering updates, quarterly business reviews" (rad 1958-1960); kapitel 5 (parallella spår, 05:145), kapitel 17 (psychological safety) och kapitel 24 (telemetry, distributed tracing, synthetic testing, sustainability indicators, 24:93) stämmer med book_index.json-titlarna.
- Om författaren: Python 3.12, Pandoc 3.1.9, XeLaTeX + Eisvogel, Mermaid CLI, GitHub Actions, PDF/EPUB/DOCX stämmer med BOOK_REQUIREMENTS.md, Dockerfile.book-builder, docs/pandoc.yaml (`pdf-engine: xelatex`, `template: eisvogel.latex`) och docs/build_book.sh. Eisvogel hämtas från Wandmalfarbe/pandoc-latex-template (build_book.sh:201; Dockerfile).
- GitHub-repot https://github.com/Geonitab/architecture_as_code är publikt och har Discussions aktiverat (GitHub-API `has_discussions: true`); https://creativecommons.org/licenses/by/4.0/ svarar 200.
- Appendix B: releaser skapas automatiskt vid push till main (softprops/action-gh-release@v2, unified-build-release.yml:586-641), artefakter sparas 30 dagar (`ARTIFACT_RETENTION_DAYS: 30`) och PDF/EPUB/DOCX/PPTX distribueras via GitHub Releases. Byggtid ~30 s och TeX Live 8+ min stämmer med CLAUDE.md/AGENTS.md. `cd presentations; pip install -r requirements.txt; python generate_pptx.py` motsvarar filerna som generate_presentation.py skriver (rad 1659-1684). templates/book-cover.svg finns. Kvadrat-färgtokens hsl(221,67%,32%), hsl(217,91%,60%), hsl(214,32%,18%), --success hsl(160,84%,30%) finns i templates/presentation-template.html:16-21.
- docs/examples/structurizr/aac_reference_workspace.dsl finns med taggarna "External Person", "Core System", "Operations", komponenten "Policy Evaluator" och containern "Observability Hub" (rad 7, 19, 53-54, 73-78). Structurizr CLI har kommandot `validate` (docs.structurizr.com/cli).
- Mognadsmodell ↔ radar: de tio disciplinerna och alla 50 checklistfrågor är identiska (programmatisk jämförelse); nivånamnen i texten (rad 134-188) matchar diagram_32_maturity_model.mmd; radarpoängen normaliseras till 0–5 (rad 1206-1207), konsekvent med Level 0–5 och Appendix D:s "six adoption levels". CDN-beroenden (picnic, mermaid@11.12.0, jspdf@2.5.1) resolvar; aac.geon.se, /maturity_model_radar.html och /architecture_as_code_maturity_model/ svarar 200.
- Mognadsmodellens rå-URL:er [2]–[9] till raw.githubusercontent.com svarar alla 200.
- Ordlistan: definitionerna av Zero Trust (i linje med NIST SP 800-207), SRE/SLO/SLI/Error Budget, Helm ("The package manager for Kubernetes"), Kubernetes, Terraform, Idempotence, Declarative Programming, Post-Quantum Cryptography, AIOps (Gartner-term), FinOps, Carbon-Aware Computing, Psychological Safety, Platform Team är sakligt korrekta om än förenklade. Kapitelhänvisningarna till kapitel 1, 3, 4, 5, 10, 25 och 26B matchar book_index.json. De fem relationerna i relationstabellen finns i references/glossary_terms_relationships.json.
- Kontrollmappningsmallen: ramverksnamnen (ISO 27001 Annex A, SOC 2 Trust Services Criteria, NIST 800-53, GDPR Articles) är korrekta på den generiska nivå de används; mallen anger inga specifika kontroll-ID:n. (Rekommendation: skriv "NIST SP 800-53 Rev. 5" och "ISO/IEC 27001:2022".)
- Svensk terminologi: Kvadrat = "square"; AB = aktiebolag; KTH = Kungliga Tekniska högskolan; "Linköpings universitet" (genitiv-s utan apostrof); Nordqvist = nord + qvist/kvist ("kvist" = twig) – korrekt.
- Kvadrat beskriver sig som ett svenskt nätverk av egenföretagande konsulter (534 konsulter, kontor på elva orter), vilket stödjer formuleringen "self employed … associated with Kvadrat" (29:11).

## Ej verifierbart

- Biografiska uppgifter om författaren (29:11-23): "certified Chief Architect", "IT Architect consultant", tidigare roller (IT architect, technical project manager, systems technician), kompetensområdena och "Kvadrat AB" som juridiskt bolagsnamn. Försök: den citerade Kvadrat-profilen (404), Kvadrats nya konsultportal anlita.kvadrat.se (sökning "Nordqvist" → "Ingen träff"), kvadrat.se/?s=Nordqvist (ingen träff), en allmän webbsökning (inga relevanta träffar). Inga privata källor har eftersökts. EJ VERIFIERBART – författaren bör själv bekräfta och ange en fungerande källa.
- Thoughtworks Source [1]: historiksidor för blips ("View blip history") kunde inte hämtas; sökbudgeten tog slut. Slug-beteendet (generisk sida för både "architecture-as-code" och nonsens-slug) talar starkt för att blippen inte finns, men en äldre arkiverad blip kan inte fullständigt uteslutas utan Thoughtworks arkiv-PDF:er.
- "GitHub Open Source Community (2024). Collaborative Software Development. Platform Documentation" – inget dokument med denna titel kunde identifieras (ingen URL angiven).
- Namnet på Structurizr CLI:s startskript (`structurizr.sh`, 31:135): README/doc-sidor för structurizr/cli kunde inte hämtas (404 på raw-sökvägar; installationssidan 404). Kommandot `validate` är bekräftat; skriptnamnet är i linje med CLI-distributionen men formellt obekräftat i denna granskning.
- Huruvida calm.finos.org:s "FINOS incubating"-badge är inaktuell (README säger "Graduated"): troligt men inte bekräftat av FINOS landscape (JS-sida, ej hämtad).
- Pandoc 3.1.9:s releasedatum bekräftat via changelog (2023-10-27); GitHub-releasesidan visar bara "28 Oct" (tidszonsskillnad).
