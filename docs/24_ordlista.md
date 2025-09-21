# Ordlista

Denna ordlista innehåller definitioner av centrala termer som används genom boken.

## Grundläggande koncept och verktyg

**API (Application Programming Interface):** Gränssnitt som möjliggör kommunikation mellan olika mjukvarukomponenter eller system genom standardiserade protokoll och dataformat.

**Automatisering:** Process där manuella uppgifter utförs automatiskt av datorsystem utan mänsklig intervention, vilket ökar effektivitet och minskar felrisk.

**CI/CD (Continuous Integration/Continuous Deployment):** Utvecklingsmetodik som integrerar kodändringar kontinuerligt och automatiserar deployment-processen för snabbare och säkrare leveranser.

**Cloud Computing:** Leverans av IT-tjänster som servrar, lagring och applikationer över internet med on-demand access och pay-per-use modeller.

**Containers:** Lätt virtualiseringsteknik som paketerar applikationer med alla dependencies för portabel körning across olika miljöer och plattformar.

**Deklarativ programmering:** Programmeringsparadigm som beskriver önskat slutresultat istället för specifika steg för att uppnå det, vilket möjliggör högre abstraktion.

**DevOps:** Kulturell och teknisk approach som kombinerar utveckling (Dev) och drift (Ops) för snabbare leveranser och förbättrat samarbete mellan team.

**Git:** Distribuerat versionhanteringssystem för att spåra ändringar i källkod under utveckling med support för branching och merging.

**Idempotens:** Egenskap hos operationer som producerar samma resultat oavsett hur många gånger de körs, kritiskt för säker automatisering.

**Infrastructure as Code (IaC):** Praktiken att hantera infrastruktur genom kod istället för manuella processer, vilket möjliggör versionskontroll och automatisering.

**JSON (JavaScript Object Notation):** Textbaserat dataformat för strukturerad informationsutbyte mellan system med human-readable syntax.

**Kubernetes:** Open-source containerorkestreringsplattform för automatiserad deployment, scaling och hantering av containeriserade applikationer.

**Microservices:** Arkitekturell approach där applikationer byggs som små, oberoende tjänster som kommunicerar via väldefinierade API:er.

**Monitoring:** Kontinuerlig övervakning av system för att upptäcka problem, optimera prestanda och säkerställa tillgänglighet.

**Orchestration:** Automatiserad koordination och hantering av komplexa arbetsflöden och system för att uppnå desired state.

**Policy as Code:** Approach där säkerhets- och compliance-regler definieras som kod för automatiserad evaluering och enforcement.

**Terraform:** Infrastructure as Code-verktyg som använder deklarativ syntax för att definiera och hantera cloud infrastructure resources.

**YAML (YAML Ain't Markup Language):** Människoläsbart dataserialiseringsformat som ofta används för konfigurationsfiler och IaC-definitioner.

**Zero Trust:** Säkerhetsmodell som aldrig litar på och alltid verifierar användare och enheter innan access till resurser beviljas.

## Deployment och operationella koncept

**Blue-Green Deployment:** Deploymentstrategi där två identiska produktionsmiljöer (blå och grön) används för att möjliggöra snabb rollback och minimal downtime.

**Canary Release:** Gradvis utrullningsstrategi där nya versioner först deployeras till en liten subset av användare för riskminimering och validering.

**Community of Practice:** Grupp av personer som delar passion för något de gör och lär sig att göra det bättre genom regelbunden interaktion.

**Conway's Law:** Observation att organisationer designar system som speglar deras kommunikationsstrukturer.

**Cross-functional Team:** Team som inkluderar medlemmar med olika färdigheter och roller som arbetar tillsammans mot gemensamma mål.

**GitOps:** Operational framework som använder Git som enda källa för sanning för deklarativ infrastruktur och applikationer.

**Helm:** Pakethanterare för Kubernetes som använder charts för att definiera, installera och upgradera komplexa Kubernetes-applikationer.

**Service Discovery:** Mekanism som möjliggör automatisk detektion och kommunikation mellan tjänster i distribuerade system.

**Service Mesh:** Dedikerad infrastrukturlager som hanterar service-till-service-kommunikation, säkerhet och observability i mikroservicesarkitekturer.

**Edge Computing:** Distributerad databehandlingsparadigm som placerar beräkningsresurser närmare datakällan för minskad latens och förbättrad prestanda.

**Post-Quantum Cryptography:** Kryptografiska algoritmer som är designade för att vara säkra mot angrepp från både klassiska och kvantumdatorer.

**Carbon-Aware Computing:** Approach för att optimera infrastrukturanvändning baserat på kolintensitet och förnybara energikällor för minskad miljöpåverkan.

**Immutable Infrastructure:** Infrastrukturparadigm där komponenter aldrig modifieras efter deployment utan ersätts helt när ändringar behövs.

**State Drift:** Situation där den faktiska infrastrukturtillståndet avviker från den definierade önskade tillståndet i Infrastructure as Code-definitioner.

## Kostnadshantering och optimering

**FinOps:** Disciplin som kombinerar finansiell hantering med molnoperationer för att maximera affärsvärdet av molninvesteringar genom kostnadsoptimering och resource management.

**Rightsizing:** Process för att optimera molnresurser genom att matcha instance-storlekar och typer med faktiska prestandakrav och användningsmönster.

**Spot Instances:** Molninstanser som använder överskottskapacitet till kraftigt reducerade priser men kan termineras med kort varsel när kapacitet behövs för on-demand användning.

**Cost Allocation Tags:** Metadataetiketter som används för att kategorisera och spåra molnresurskostnader per projekt, team, miljö eller andra organisatoriska dimensioner.

**Cost Governance:** Ramverk av policies, processer och verktyg för att styra och kontrollera molnkostnader inom en organisation.

**Resource Quotas:** Begränsningar som sätts på hur mycket av en viss resurs (CPU, minne, lagring) som kan konsumeras inom en given scope eller namespace.

## Testning och kvalitetssäkring

**Terratest:** Open source Go-bibliotek för automatiserad testning av Infrastructure as Code, särskilt designat för Terraform-moduler och cloud infrastructure.

**Policy as Code:** Approach där organisatoriska policies, säkerhetsregler och compliance-krav definieras som kod och kan automatiskt enforced och testade.

**OPA (Open Policy Agent):** Cloud-native policy engine som möjliggör unified policy enforcement across olika services och teknologier genom deklarativ policy språk.

**Chaos Engineering:** Disciplin för att experimentellt introducera fel i system för att bygga tillit till systemets förmåga att motstå turbulenta förhållanden i produktion.

**Integration Testing:** Testning som verifierar att olika komponenter eller services fungerar korrekt tillsammans när de är integrerade i ett system.

**Compliance Testing:** Automatiserad validering av att system och konfigurationer följer relevanta regulatoriska krav, säkerhetsstandarder och organisatoriska policies.

## Strategiska och organisatoriska koncept

**Cloud-First Strategy:** Strategisk approach där organisationer primärt väljer molnbaserade lösningar för nya IT-initiativ innan on-premises alternativ övervägs.

**Digital Transformation:** Fundamental förändring av affärsoperationer och värdeleverans genom integration av digital teknik i alla aspekter av verksamheten.

**Multi-Cloud:** Strategi att använda molntjänster från flera olika leverantörer för att undvika vendor lock-in och optimera för specifika capabilities eller kostnader.

**Data Sovereignty:** Konceptet att digital data är underkastat lagarna och juridiktionen i det land där den lagras eller bearbetas.

**Conway's Law:** Observation att organisationer designar system som speglar deras kommunikationsstrukturer, vilket påverkar hur team bör organiseras för optimal systemdesign.

**Cross-functional Team:** Team som inkluderar medlemmar med olika färdigheter och roller som arbetar tillsammans mot gemensamma mål, essentiellt för DevOps-framgång.

**DevOps Culture:** Kulturell transformation från traditionella utvecklings- och driftsilos till kollaborativa arbetssätt som betonar shared ownership och continuous improvement.

**Psychological Safety:** Teammiljö där medlemmar känner sig säkra att ta risker, erkänna misstag och experimentera utan rädsla för bestraffning eller förödmjukelse.

**Servant Leadership:** Ledarskapsfilosofi som fokuserar på att tjäna teamet och främja deras framgång snarare än traditionell kommando-och-kontroll-ledning.

**Best Practice Evolution:** Kontinuerlig utveckling av rekommenderade metoder baserat på praktisk erfarenhet, community feedback och tekniska framsteg.

**Anti-Pattern:** Vanligt förekommande men kontraproduktivt lösningsförslag som initialt verkar användbart men som leder till negativa konsekvenser.

**Policy-as-Code:** Metod där organisatoriska policies, säkerhetsregler och compliance-krav definieras som kod för automatiserad enforcement och testing.

**Infrastructure Governance:** Ramverk av policies, processer och verktyg för att styra och kontrollera infrastrukturutveckling och -drift inom organisationer.

**Technical Debt:** Ackumulerad kostnad av shortcuts och suboptimala tekniska beslut som kräver framtida refactoring eller omarbetning för att bibehålla systemkvalitet.

**Blameless Culture:** Organisationskultur som fokuserar på systemförbättringar efter incidenter snarare än individuell skuld, vilket främjar öppenhet och lärande.

**Change Management:** Systematisk approach för att hantera organisatoriska förändringar, inklusive stakeholder engagement, kommunikation och motståndhantering.

**DevSecOps:** Utvecklingsmetodik som integrerar säkerhetspraktiker genom hela utvecklingslivscykeln snarare än som en separat fas i slutet.

**Site Reliability Engineering (SRE):** Disciplin som tillämpar mjukvaruingenjörsprinciper på operationella problem för att skapa skalbara och mycket tillförlitliga mjukvarusystem.