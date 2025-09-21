# Grundläggande principer för Architecture as Code

Architecture as Code bygger på fundamentala principer som säkerställer framgångsrik implementation av kodifierad systemarkitektur. Dessa principer omfattar och bygger vidare på Infrastructure as Code (IaC) men sträcker sig till hela systemlandskapet.

![Grundläggande principer diagram](images/diagram_02_kapitel1.png)

Diagrammet visar det naturliga flödet från deklarativ kod genom versionskontroll och automatisering till reproducerbarhet och skalbarhet - de fem grundpelarna inom Architecture as Code.

## Deklarativ arkitekturdefinition

Den deklarativa approachen inom Architecture as Code innebär att beskriva önskat systemtillstånd på alla nivåer - från applikationskomponenter till infrastruktur. Detta skiljer sig från imperativ programmering där varje steg måste specificeras explicit.

Infrastructure as Code är ett praktiskt exempel på deklarativ definition, där verktyg som Terraform eller CloudFormation beskriver infrastrukturens önskade tillstånd. Architecture as Code utvidgar detta till att omfatta applikationsarkitektur, API-kontrakt och organisatoriska strukturer.

## Helhetsperspektiv på kodifiering

Medan Infrastructure as Code fokuserar på infrastrukturresurser, omfattar Architecture as Code hela systemekosystemet. Detta inkluderar applikationslogik, dataflöden, säkerhetspolicies, compliance-regler och till och med organisationsstrukturer.

Ett praktiskt exempel är hur en förändring i en applikations API automatiskt kan propagera genom infrastrukturdefinitioner, säkerhetskonfigurationer och dokumentation - allt eftersom det är definierat som kod.

## Immutable architecture patterns

Principen om immutable arkitektur bygger vidare på Infrastructure as Code:s immutable infrastruktur men applicerar det på hela systemarkitekturen. Istället för att modifiera befintliga komponenter skapas nya versioner som ersätter gamla på alla nivåer.

Detta skapar förutsägbarhet och eliminerar architectural drift - där system gradvis divergerar från sin avsedda design över tid.

## Testbarhet på arkitekturnivå

Architecture as Code möjliggör testning av hela systemarkitekturen, inte bara enskilda komponenter. Detta inkluderar validering av arkitekturmönster, compliance med designprinciper och verifiering av end-to-end-flöden.

Infrastructure as Code-testning utgör en viktig del av denna helhetssyn, men kompletteras med arkitekturtester som validerar designbeslut och systemkomplexitet.

Källor:
- Fowler, M. "Infrastructure as Code: Patterns and Practices." Martin Fowler Blog.
- Red Hat. "Architecture as Code Principles and Best Practices." Red Hat Developer.
- Google Cloud. "Infrastructure as Code on Google Cloud." Google Cloud Architecture Center.