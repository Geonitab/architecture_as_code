# Säkerhet i Infrastructure as Code

Säkerhet inom Infrastructure as Code kräver integration av säkerhetstänk genom hela utvecklings- och deployment-processen. Genom att behandla säkerhet som kod kan organisationer uppnå systematisk och skalbar säkerhetshantering som utvecklas tillsammans med infrastrukturen.

![Säkerhet i Infrastructure as Code](images/diagram_06_kapitel5.png)

Diagrammet visar det integrerade säkerhetsflödet från security policies genom secret management och access control till compliance scanning och threat modeling.

## Security as Code principles

Security as Code innebär att säkerhetskonfigurationer, policies, och controls definieras och hanteras som kod. Detta möjliggör version control, automated testing, och reproducible security implementations across miljöer och organisationer.

Policy as Code frameworks som Open Policy Agent (OPA) används för att definiera säkerhetsregler som kan evalueras automatiskt under CI/CD-processen. Detta säkerställer att säkerhetsstandarder upprätthålls konsekvent utan att sakta ner utvecklingsprocessen.

## Secret management strategier

Centraliserad secret management är kritisk för säker IaC-implementation. Secrets som API keys, passwords, och certificates ska aldrig lagras i kod utan hanteras genom dedikerade vault-lösningar som HashiCorp Vault, AWS Secrets Manager, eller Azure Key Vault.

Dynamic secret generation och automatic rotation minimerar exposure time och reducerar säkerhetsrisker. Integration mellan IaC-verktyg och secret management systems möjliggör secure access till credentials utan att kompromissa development workflow eller operational efficiency.

## Identity and Access Management

Granular IAM policies definieras som kod för att implementera principle of least privilege across infrastrukturresurser. Role-based access control (RBAC) och attribute-based access control (ABAC) används för att säkerställa appropriate access levels för olika användare och tjänster.

Cross-account och cross-subscription access patterns implementeras genom federated identity och trust relationships. Service accounts och managed identities används för application-level access, medan human users autentiseras genom corporate identity providers.

Källor:
- NIST. "Cybersecurity Framework for Infrastructure as Code." National Institute of Standards and Technology.
- OWASP. "Infrastructure as Code Security Top 10." Open Web Application Security Project.
- CIS. "Center for Internet Security IaC Benchmarks." Center for Internet Security.