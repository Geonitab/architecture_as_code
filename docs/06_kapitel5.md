### Säkerhet som kodprinciper

- **Definition**: Säkerhet som kod integrerar säkerhetspraxis i mjukvaruutvecklingscykeln.
- **Exempel**:
  - **Automatiserad säkerhetstestning**: Implementering av enhetstester som validerar säkerhetskontroller.
  - **Konfiguration som kod**: Att lagra säkerhetskonfigurationer i versionshanterade arkiv, vilket möjliggör granskning och spårbarhet.

### Hemlig hantering strategier

- **Översikt**: Effektiva strategier för att hantera känslig information på ett säkert sätt.
- **Praktisk hantering**:
  - **Miljövariabler**: Använda miljövariabler för att säkert lagra hemligheter.
  - **Verktyg för hemlighetsförvaltning**: Implementera verktyg som HashiCorp Vault eller AWS Secrets Manager för centraliserad hantering av hemligheter.

### Identitet och åtkomsthantering (IAM)

- **IAM Översikt**: Hantera användaridentiteter och kontrollera åtkomst till resurser.
- **IAM Policy Exempel**:
  - **Rollbaserad åtkomstkontroll (RBAC)**: Definiera roller och behörigheter för användare.
  - **Policy Exempel**: Ett exempel på en JSON IAM-policy som begränsar åtkomst till specifika AWS-resurser baserat på användarroller.