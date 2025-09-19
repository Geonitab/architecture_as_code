# Versionhantering och kodstruktur

Effektiv versionhantering utgör ryggraden i Infrastructure as Code-implementationer. Genom att tillämpa samma metoder som mjukvaruutveckling på infrastrukturdefinitioner skapas spårbarhet, samarbetsmöjligheter och kvalitetskontroll.

![Versionhantering och kodstruktur](images/diagram_03_kapitel2.png)

Diagrammet illustrerar det typiska flödet från Git repository genom branching strategy och code review till slutlig deployment, vilket säkerställer kontrollerad och spårbar infrastrukturutveckling.

## Git-baserad arbetsflöde för infrastruktur

Git utgör standarden för versionhantering av IaC-kod och möjliggör distribuerat samarbete mellan team-medlemmar. Varje förändring dokumenteras med commit-meddelanden som beskriver vad som ändrats och varför, vilket skapar en komplett historik över infrastrukturutvecklingen.

Branch-strategier som GitFlow eller GitHub Flow anpassas för infrastrukturkod genom att inkludera miljöspecifika branches. Feature branches används för utveckling av nya funktioner, medan release branches säkerställer stabilitet innan deployment till produktionsmiljöer.

## Kodorganisation och modulstruktur

Välorganiserad kodstruktur är avgörande för maintainability och collaboration i större IaC-projekt. Modulär design möjliggör återanvändning av infrastrukturkomponenter across olika projekt och miljöer, vilket reducerar dublering och förbättrar konsistens.

Directory structure bör reflektera både logisk och teknisk organisation, med tydlig separation mellan miljöer, regioner och tjänster. Naming conventions och dokumentation säkerställer att kod är självförklarande och tillgänglig för nya team-medlemmar.

## Tagging och release management

Semantic versioning appliceras på infrastrukturdefinitioner för att indikera omfattningen av förändringar. Major versions signalerar breaking changes, minor versions nya funktioner, och patch versions bugfixar eller mindre förbättringar.

Release branches och tags möjliggör reproducerbara deployments och rollback-funktionalitet. Automated tagging baserat på CI/CD-pipelines säkerställer konsistent versionering utan manuell intervention, vilket reducerar risk för mänskliga fel i release-processen.

## Branching strategies för infrastruktur

Infrastructure-specific branching strategies tar hänsyn till miljöspecifika krav och deployment patterns. Environment branches (dev, staging, prod) kan användas för att hantera miljöspecifika konfigurationer, medan feature branches fokuserar på funktionalitetsutveckling.

Merge strategies som rebase vs merge väljs baserat på önskad commit-historia och team-preferences. Squash merging kan användas för att minska commit-noise, medan preserve merging bibehåller fullständig utvecklingshistorik för debugging-ändamål.

## Code review processer

Systematiska code reviews säkerställer kvalitet och kunskapsdelning inom infrastrukturteam. Review-processer inkluderar kontroll av säkerhetsaspekter, kostnadsimplikationer, och alignment med organisatoriska standards och best practices.

Automated checks kombineras med manuell review för optimal effektivitet. Linting tools, security scanners, och cost estimators kan köras automatiskt, medan arkitekturell review och business logic kräver mänsklig bedömning och expertis.

Källor:
- Atlassian. "Git Workflows for Infrastructure as Code." Atlassian Git Documentation.
- GitLab. "Infrastructure as Code Best Practices." GitLab CI/CD Documentation.
- Microsoft. "Version Control for Infrastructure as Code." Azure DevOps Documentation.