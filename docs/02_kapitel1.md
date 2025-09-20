# Grundläggande principer för Infrastructure as Code

Infrastructure as Code bygger på flera fundamentala principer som säkerställer framgångsrik implementation och långsiktig hållbarhet. Dessa principer utgör grunden för hur organisationer bör tänka kring kodbaserad infrastruktur, och fördjupar de koncept som introducerades i [kapitel 1](01_inledning.md) om Infrastructure as Code som paradigm.

![Grundläggande principer diagram](images/diagram_02_kapitel1.png)

Diagrammet visar det naturliga flödet från deklarativ kod genom versionskontroll och automatisering till reproducerbarhet och skalbarhet - de fem grundpelarna inom IaC. Dessa principer kommer att vara centrala för alla tekniska implementationer som vi kommer att utforska i kommande kapitel, från [versionhantering](03_kapitel2.md) till [avancerad säkerhet](12_kapitel11.md).

## Deklarativ vs imperativ approach

Den deklarativa approachen innebär att beskriva önskat slutläge istället för stegen för att nå dit. Detta skiljer sig från imperativ programmering där varje steg måste specificeras explicit. Deklarativ IaC-kod fokuserar på "vad" istället för "hur", vilket möjliggör högre abstraktion och mindre felbenägenhet.

Exempel på deklarativ kod inkluderar Terraform HCL, CloudFormation YAML, eller Kubernetes manifests. Dessa verktyg tar ansvar för att beräkna och utföra nödvändiga förändringar för att uppnå det specificerade tillståndet, vilket reducerar komplexitet för utvecklaren.

## Idempotens och konvergens

Idempotens säkerställer att upprepade körningar av samma IaC-kod producerar identiska resultat, oavsett nuvarande systemtillstånd. Detta är kritiskt för tillförlitlighet och möjliggör säker automatisering utan risk för oavsiktliga förändringar.

Konvergens refererar till systemets förmåga att automatiskt korrigera avvikelser från önskat tillstånd. Modern IaC-verktyg implementerar kontinuerlig konvergens genom att regelbundet kontrollera och korrigera infrastrukturtillstånd enligt definierade specifikationer.

## Immutable infrastruktur

Principen om immutable infrastruktur innebär att infrastrukturkomponenter aldrig modifieras efter deployment. Istället ersätts hela komponenter när förändringar behövs. Detta eliminerar configuration drift och säkerställer konsistens mellan miljöer.

Immutable infrastruktur stödjs av containerteknologier och cloud-native tjänster som möjliggör snabb skapelse och förstörelse av infrastrukturresurser. Detta approach reducerar också säkerhetsrisker genom att minimera systemets attackyta över tid.

## Testbarhet och kvalitetssäkring

IaC-kod ska behandlas som vilken annan kod som helst, vilket innebär omfattande testning på flera nivåer. Unit-tester validerar enskilda moduler, integration-tester verifierar komponentinteraktion, och end-to-end-tester säkerställer hela systemets funktionalitet. Dessa teststrategier kommer att fördjupas betydligt i kommande kapitel om [CI/CD-pipelines](04_kapitel3.md) och [praktisk implementation](08_kapitel7.md).

Teststrategier inkluderar statisk kodanalys, policy validation, och infrastrukturtestning i isolerade miljöer. Automated testing pipelines säkerställer att förändringar valideras innan de når produktionsmiljöer, vilket minskar risken för störningar och säkerhetsbrister. Dessa koncept blir särskilt viktiga när vi utforskar [säkerhet i Infrastructure as Code](06_kapitel5.md) och [policy as code](12_kapitel11.md).

Policy-driven testing möjliggör automatisk validering av compliance-krav och säkerhetsstandarder som en integrerad del av utvecklingsprocessen. Detta skapar grunden för den governance-approach som vi kommer att se i [kapitel 14 om compliance](14_kapitel13.md).

Källor:
- Puppet Labs. "Infrastructure as Code: A Brief Introduction." Puppet Documentation.
- Red Hat. "Infrastructure as Code Principles and Best Practices." Red Hat Developer.
- Google Cloud. "Infrastructure as Code on Google Cloud." Google Cloud Architecture Center.