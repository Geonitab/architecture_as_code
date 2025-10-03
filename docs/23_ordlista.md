# Glossary

![Architecture as Code Core Concepts Class Diagram](images/diagram_23_ordlista_class.png)

This Glossary contains definitioner of centrala termer as används genAbout the Book and as forms the foundation for Architecture as Code methodology.

## Fundamental Concepts and verktyg

**API (Application Programming Interface):** Gränssnitt as enables kommunikation between different mjukvarukomponenter or systems through standardized protokoll and dataformat.

**Architecture as Code-automation:** Process where manuella uppgifter utfors automatically of datorsystem without mänsklig intervention, that ökar effektivitet and reduces felrisk.

**CI/CD (Continuous Integration/Continuous Deployment):** Utvecklingsmetodik as integrerar kodändringar kontinuerligt and automatiserar driftsättningsprocessen for snabbare and säkrare leveranser.

**Cloud Computing:** Leverans of IT-tjänster as servrar, lagring and applications over internet with åtkomst at begäran and betalning per use.

**Containers:** Lätt virtualiseringsteknik as paketerar applications with all dependencies for portabel körning across different environments and plattformar.

**Declarative programming:** Programmeringsparadigm that describes desired slutresultat instead for specific step to uppnå the, which enables högre abstraktion.

**DevOps:** cultural and technical approach as kombinerar development (Dev) and drift (Ops) for snabbare leveranser and forbättrat samarbete between team.

**Git:** Distribuerat versionhanteringssystem to spåra ändringar in källkod under development with support for branching and merging.

**Idempotens:** Egenskap at operationer as producerar same resultat oavsett how many gånger the körs, kritiskt for säker Architecture as Code-automation.

**Infrastructure as Code (Architecture as Code) (Architecture as Code) (IaC):** Praktiken to handle infrastructure through Architecture as Code instead for manuella processes, which enables version control and automation.

**JSON (JavaScript Object Notation):** Textbaserat dataformat for Structured informationsutbyte between systems with human-readable syntax.

**Kubernetes:** Öppen källkod containerorkestreringsplattform for automatiserad driftsättning, skalning and handling of containeriserade applications.

**Microservices:** Arkitekturell approach where applications byggs as stemplate, oberoende tjänster as kommunicerar via väldefinierade API:er.

**Övervakning:** Kontinuerlig systemövervakning to upptäcka problem, optimera performance and ensure togänglighet.

**Orchestration:** Automatiserad koordination and handling of komplexa arbetsflöden and systems to uppnå desired state.

**Policy as Code:** Tovägagångssätt where säkerhets- and efterlevnadsregler are defined as code for automatiserad utvärdering and verkställande.

**Terraform:** Infrastructure as Code (Architecture as Code)-verktyg as uses declarative syntax to definiera and handle cloud infrastructure resources.

**YAML (YAML Ain't Markup Language):** Människoläsbart dataserialiseringsformat as often används for konfigurationsfiler and Architecture as Code-definitioner.

**Zero Trust:** Säkerhetsmodell as aldrig litar at and always verifierar user and enheter innan åtkomst to resurser beviljas.

## Driftsättning and operational concepts

**Blå-grön driftsättning:** Driftsättningsstrategi where två identiska produktionsenvironments (blå and grön) används to enable snabb återställning and minimal stoeståndstid.

**Canary Release:** gradually utrullningsstrategi where new versions forst deployeras to a liten subset of user for riskminimering and validation.

**Community of Practice:** Grupp of personer as parts passion for något the gör and lär itself to göra the bättre through regelbunden interaktion.

**Conway's Law:** Observation to organisationer designar systems as speglar their kommunikationsStructureer.

**Tvärfunktionellt team:** Team as includes withlemmar with different färdigheter and roller as arbetar tosammans mot gemensamma mål.

**GitOps:** Operational framework as uses Git as enda källa for sanning for declarative infrastructure and applications.

**Helm:** Pakethanterare for Kubernetes as uses charts to definiera, installera and upgradera komplexa Kubernetes-applications.

**Service Discovery:** Mekanism as enables automatisk detektion and kommunikation between tjänster in distribuerade systems.

**Service Mesh:** Dedikerad infrastructurelager as handles service-to-service-kommunikation, säkerhet and observability in mikroservicesarkitekturer.

**Edge Computing:** Distributerad databehandlingsparadigm as placerar beräkningsresurser whenmare datakällan for minskad latens and forbättrad performance.

**Post-Quantum Cryptography:** Kryptografiska algoritmer as is designade to vara säkra mot angrepp from both klassiska and kvantumdatorer.

**Carbon-Aware Computing:** Approach to optimera infrastructureanvändning baserat at kolintensitet and fornybara energiSources for minskad miljöpåverkan.

**Oforänderlig infrastructure:** InfraStructureparadigm where components aldrig modifieras efter driftsättning without ersätts helt when ändringar behövs.

**State Drift:** Situation where The faktiska infrastructuretoståndet avviker from The definierade desired toståndet in Infrastructure as Code-definitioner.

## Kostnadshantering and optimering

**FinOps:** Disciplin as kombinerar finansiell handling with molnoperationer to maximera affärsvärdet of molninvesteringar through kostnadsoptimering and resource management.

**Rightsizing:** Process to optimera molnresurser by matcha instance-storlekar and typer with faktiska performancerequirements and användningsmönster.

**Spot Instances:** Molninstanser as uses överskottcreatecitet to kraftigt reducerade priser but can termineras with kort varsel when kapacitet behövs for on-demand use.

**Cost Allocation Tags:** Metadataetiketter as används to kategorisera and spåra molnresurskostnader per projekt, team, miljö or andra organizational dimensioner.

**Cost Governance:** Ramverk of policies, processes and verktyg to styra and kontrollera molnkostnader within a organisation.

**Resource Quotas:** Begränsningar as sätts at how very of a viss resurs (CPU, minne, lagring) which can konsumeras within a given scope or namespace.

## testing and kvalitetssäkring

**Terratest:** Open source Go-bibliotek for automatiserad testing of Infrastructure as Code, particularly designat for Terraform-moduler and cloud infrastructure.

**Policy as Code:** Approach where organizational policies, säkerhetsregler and compliance-requirements are defined as code and can automatically enforced and testade.

**OPA (Open Policy Agent):** Cloud-native policy engine as enables unified policy enforcement across different services and technologies through declarative policy språk.

**Chaos Engineering:** Disciplin to experimentellt introducera fel in systems to bygga toit to system's formåga to motstå turbulenta forhållanden in produktion.

**Integration Testing:** testing as verifierar to different components or services functions korrekt tosammans when the is integrerade in A systems.

**Compliance Testing:** Automatiserad validation of to systems and konfigurationer follows relevanta regulatoriska requirements, säkerhetsstandarder and organizational policies.

## Strategiska and organizational concepts

**Cloud-First Strategy:** Strategisk approach where organisationer primärt väljer molnbaserade lösningar for new IT-initiativ innan on-premises alternatives övervägs.

**Digital Transformation:** Fundamental change of affärsoperationer and värdeleverans through integration of digital teknik in all aspekter of verksamheten.

**Multi-Cloud:** Strategi to use molntjänster from flera different leverantörer to undvika vendor lock-in and optimera for specific capabilities or kostnader.

**Data Sovereignty:** Konceptet to digital data is underkastat lagarna and juridiktionen in the land where The lagras or bearbetas.

**Conway's Law:** Observation to organisationer designar systems as speglar their kommunikationsStructureer, which affect how team bör organiseras for optimal systemdesign.

**Cross-functional Team:** Team as includes withlemmar with different färdigheter and roller as arbetar tosammans mot gemensamma mål, essentiellt for DevOps-success.

**DevOps Culture:** cultural transformation from traditionella utvecklings- and driftsilos to kollaborativa arbetssätt as emphasizes shared ownership and continuous improvement.

**Psychological Safety:** Teammiljö where withlemmar känner itself säkra to ta risker, erkänna misstag and experimentera without rädsla for bestraffning or forödmjukelse.

**Servant Leadership:** Ledarskapsfilosofi as fokuserar at to tjäna teamet and främja their success rather than traditionell kommando-and-kontroll-ledning.

**Best Practice Evolution:** Kontinuerlig development of rekommenderade metoder baserat at praktisk erfarenhet, community feedback and technical framsteg.

**Anti-Pattern:** Vanligt forekommande but kontraproduktivt lösningsforslag as initialt verkar användbart but as leder to negative consequences.

**Policy-as-Code:** Metod where organizational policies, säkerhetsregler and compliance-requirements are defined as code for automatiserad enforcement and testing.

**Infrastructure Governance:** Ramverk of policies, processes and verktyg to styra and kontrollera infrastructure development and -drift within organisationer.

**Technical Debt:** Ackumulerad kostnad of shortcuts and suboptimala technical decisions as requires framtida refactoring or omarbetning to bibehålla systemkvalitet.

**Blameless Culture:** Organisationskultur as fokuserar at systemforbättringar efter incidenter rather than individuell skuld, which främjar öppenhet and lärande.

**Change Management:** Systematisk approach to handle organizational changes, including stakeholder engagement, kommunikation and motståndhantering.

**DevSecOps:** Utvecklingsmetodik as integrerar säkerhetspraktiker through entire utvecklingslivscykeln rather than as a separat fas in slutet.

**Site Reliability Engineering (SRE):** Disciplin as toämpar mjukvaruingenjörsprinciper at operational problem to create skalbara and very toforlitliga mjukvarusystem.