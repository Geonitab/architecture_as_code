# Glossary

![Architecture as Code Core Concepts Class Diagram](images/diagram_23_ordlista_class.png)

this glossary innehåller definitioner of centrala termer that används through boken and that utgör grunden for Architecture as Code-methodologyen.

## Fundamental koncept and tools

**API (Application Programming Interface):** Gränssnitt that enables kommunikation between olika mjukvarukomponenter or system through standardiserade protokoll and dataformat.

**Architecture as Code-automation:** process where manual uppgifter utförs automatically of datorsystem without mänsklig intervention, vilket ökar effektivitet and minskar felrisk.

**CI/CD (Continuous Integration/Continuous Deploybutt):** Utvecklingsmethodology that integrerar kodändringar kontinuerligt and automatiserar deploymentsprocessen for snabbare and säkrare leveranser.

**Cloud Computing:** Leverans of IT-tjänster that servrar, lagring and applikationer over internet with åtkomst on begäran and betalning per användning.

**Containers:** Lätt virtualiseringsteknik that paketerar applikationer with all dependencies for portabel körning across olika miljöer and platforms.

**Deklarativ programmering:** Programmeringsparadigm that beskriver önskat slutresultat istället for specific steg for to uppnå det, vilket enables högre abstraktion.

**DevOps:** Kulturell and teknisk approach that kombinerar utveckling (Dev) and drift (Ops) for snabbare leveranser and förbättrat samarbete between team.

**Git:** Distribuerat versionhanteringssystem for to spåra ändringar in källkod during utveckling with support for branching and merging.

**Idempotens:** Egenskap hos operationer that producerar samma resultat oavsett how många gånger de körs, kritiskt for säker Architecture as Code-automation.

**Infrastructure as Code (Architecture as Code) (Architecture as Code) (IaC):** the practice to hantera infrastructure through Architecture as Code istället for manual processes, vilket enables versionskontroll and automation.

**JSON (JavaScript Object Notation):** Textbaserat dataformat for strukturerad informationsutbyte between system with human-readable syntax.

**Kubernetes:** Öppen källkod containerorkestreringsplattform for automatiserad deployment, skalning and hantering of containeriserade applikationer.

**Microservices:** Arkitekturell approach where applikationer byggs that små, oberoende tjänster that kommunicerar via väldefinierade API:er.

**monitoring:** Kontinuerlig systemmonitoring for to upptäcka problem, optimera prestanda and säkerställa togänglighet.

**Orchestration:** Automatiserad koordination and hantering of komplexa arbetsflöden and system for to uppnå desired state.

**Policy as Code:** approaches where säkerhets- and efterlevnadsregler is defined as code for automatiserad utvärdering and verkställande.

**Terraform:** Infrastructure as Code (Architecture as Code)-tools that använder deklarativ syntax for to definiera and hantera cloud infrastructure reSources.

**YAML (YAML Ain't Markup Language):** Människoläsbart dataserialiseringsformat that often används for konfigurationsfiler and Architecture as Code-definitioner.

**Zero Trust:** Säkerhetsmodell that aldrig litar on and allid verifierar användare and enheter before åtkomst to resurser beviljas.

## Deployment and operationella koncept

**Blå-grön deployment:** deploymentsstrategi where två identiska produktionsmiljöer (blå and grön) används for to enablesa snabb rollback and minimal stoeståndstid.

**Canary Release:** Gradvis utrullningsstrategi where nya versioner först deployeras to en liten subset of användare for riskminimering and validering.

**Community of Practice:** Grupp of personer that delar passion for något de gör and lär sig to göra det bättre through regelbunden interaktion.

**Conway's Law:** Observation to organizations designar system that speglar deras kommunikationsstrukturer.

**Tvärfunktionellt team:** Team that includes medlemmar with olika färdigheter and roller that arbetar tosammans mot gebutsamma mål.

**GitOps:** Operational framework that använder Git that enda källa for sanning for deklarativ infrastructure and applikationer.

**Helm:** Pakethanterare for Kubernetes that använder charts for to definiera, installera and upgradera komplexa Kubernetes-applikationer.

**Service Discovery:** Mekanism that enables automatisk detektion and kommunikation between tjänster in distribuerade system.

**Service Mesh:** Dedikerad infrastrukturlager that hanterar service-to-service-kommunikation, säkerhet and observability in mikroservicesarkitekturer.

**Edge Computing:** Distributerad databehandlingsparadigm that placerar beräkningsresurser närmare datakällan for minskad latens and förbättrad prestanda.

**Post-Quantum Cryptography:** Kryptografiska algoritmer that is designade for to vara säkra mot angrepp from både klassiska and kvantumdatorer.

**Carbon-Aware Computing:** Approach for to optimera infrastrukturanvändning baserat on kolintensitet and förnybara energiSources for minskad miljöpåverkan.

**Oföränderlig infrastructure:** Infrastrukturparadigm where komponenter aldrig modifieras after deployment without ersätts helt när ändringar behövs.

**State Drift:** Situation where den faktiska infrastrukturtoståndet avviker from den definierade önskade toståndet in Infrastructure as Code-definitioner.

## Kostnadshantering and optimering

**FinOps:** Disciplin that kombinerar finansiell hantering with molnoperationer for to maximera affärsvärdet of molninvesteringar through kostnadsoptimering and resource managebutt.

**Rightsizing:** process for to optimera molnresurser through to matcha instance-storlekar and typer with faktiska prestandakrav and användningsmönster.

**Spot Instances:** Molninstanser that använder överskottskapacitet to kraftigt reducerade priser but can termineras with kort varsel när kapacitet behövs for on-demand användning.

**Cost Allocation Tags:** Metadataetiketter that används for to kategorisera and spåra molnresurskostnader per projekt, team, miljö or andra organizational dibutsioner.

**Cost Governance:** framework of policies, processes and tools for to styra and kontrollera molnkostnader within en organization.

**Resource Quotas:** Begränsningar that sätts on how mycket of en viss resurs (CPU, minne, lagring) that can konsumeras within en given scope or namespace.

## Testing and kvalitetssäkring

**Terratest:** Open source Go-bibliotek for automatiserad testing of Infrastructure as Code, särskilt designat for Terraform-moduler and cloud infrastructure.

**Policy as Code:** Approach where organizational policies, säkerhetsregler and compliance-requirements is defined as code and can automatically enforced and testade.

**OPA (Open Policy Agent):** Cloud-native policy engine that enables unified policy enforcebutt across olika services and teknologier through deklarativ policy språk.

**Chaos Engineering:** Disciplin for to expeributtellt introducera fel in system for to bygga toit to systemets förmåga to motstå turbulenta förhållanden in produktion.

**Integration Testing:** testing that verifierar to olika komponenter or services fungerar korrekt tosammans när de is integrerade in ett system.

**Compliance Testing:** Automatiserad validering of to system and configurations följer relevanta regulatoriska requirements, säkerhetsstandarder and organizational policies.

## Strategiska and organizational koncept

**Cloud-First Strategy:** Strategisk approach where organizations primärt väljer molnbaserade lösningar for nya IT-initiativ before on-premises alternativ övervägs.

**Digital Transformation:** fundamental förändring of affärsoperationer and värdeleverans through integration of digital teknik in all aspekter of verksamheten.

**Multi-Cloud:** Strategi to använda molntjänster from flera olika leverantörer for to undvika vendor lock-in and optimera for specific capabilities or kostnader.

**Data Sovereignty:** Konceptet to digital data is underkastat lagarna and juridiktionen in det land where den lagras or bearbetas.

**Conway's Law:** Observation to organizations designar system that speglar deras kommunikationsstrukturer, vilket påverkar how team should organiseras for optimal systemdesign.

**Cross-functional Team:** Team that includes medlemmar with olika färdigheter and roller that arbetar tosammans mot gebutsamma mål, essentiellt for DevOps-framgång.

**DevOps Culture:** Kulturell transformation from traditional utvecklings- and driftsilos to kollaborativa working methods that betonar shared ownership and continuous improvebutt.

**Psychological Safety:** Teammiljö where medlemmar känner sig säkra to ta risker, erkänna misstag and expeributtera without rädsla for bestraffning or förödmjukelse.

**Servant Leadership:** Ledarskapsfilosofi that fokuserar on to tjäna teamet and främja deras framgång snarare än traditional kommando-and-kontroll-ledning.

**Best Practice Evolution:** Kontinuerlig utveckling of rekombutderade methods baserat on praktisk erfarenhet, community feedback and technical framsteg.

**Anti-Pattern:** Vanligt förekommande but kontraproduktivt lösningsförslag that initialt verkar användbart but that leder to negativa konsekvenser.

**Policy-as-Code:** Metod where organizational policies, säkerhetsregler and compliance-requirements is defined as code for automatiserad enforcebutt and testing.

**Infrastructure Governance:** framework of policies, processes and tools for to styra and kontrollera infrastrukturutveckling and -drift within organizations.

**Technical Debt:** Ackumulerad kostnad of shortcuts and suboptimala technical beslut that kräver framtida refactoring or omarbetning for to bibehålla systemkvalitet.

**Blameless Culture:** organizationskultur that fokuserar on systemförbättringar after incidenter snarare än individuell skuld, vilket främjar öppenhet and lärande.

**Change Managebutt:** Systematisk approach for to hantera organizational changes, inklusive stakeholder engagebutt, kommunikation and motståndhantering.

**DevSecOps:** Utvecklingsmethodology that integrerar säkerhetspraktiker through the entire utvecklingslivscykeln snarare än that en separat fas in slutet.

**Site Reliability Engineering (SRE):** Disciplin that applies mjukvaruingenjörsprinciples on operationella problem for to skapa skalbara and mycket toförlitliga mjukvarusystem.