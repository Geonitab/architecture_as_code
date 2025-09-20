# Policy och säkerhet som kod i detalj

![Policy och säkerhet som kod](images/diagram_12_kapitel11.png)

*Policy as Code representerar nästa evolutionssteg inom Infrastructure as Code där säkerhet, compliance och governance automatiseras genom programmerbara regler. Diagrammet visar integreringen av policy enforcement i hela utvecklingslivscykeln från design till produktion.*

## Introduktion och omfattning

I dagens snabbt föränderliga digitala landskap står organisationer inför en unprecedented komplexitet när det gäller säkerhet och efterlevnad av regelverk. Traditionella säkerhetsmodeller, som förlitar sig på manuella processer och statiska konfigurationer, har visat sig otillräckliga för att hantera de dynamiska kraven i moderna molnbaserade infrastrukturer. Detta kapitel introducerar och fördjupar sig i konceptet Policy as Code (PaC) - en paradigmskifte som transformerar hur organisationer närmar sig säkerhet, compliance och governance.

Policy as Code bygger på samma grundläggande principer som Infrastructure as Code: att behandla kritiska organisatoriska tillgångar som kod, vilket möjliggör versionhantering, automatisering, testning och konsekvent distribution. När detta koncept tillämpas på säkerhetspolicies och compliance-regelverk, uppstår kraftfulla möjligheter för automatisering och skalbarhet som tidigare var ogenomförbara med manuella metoder.

För svenska organisationer är detta paradigmskifte särskilt relevant med tanke på den komplexa regulatoriska miljön som inkluderar GDPR (Dataskyddsförordningen), MSB:s säkerhetskrav för kritisk infrastruktur, PCI DSS för betalningshantering, samt branschspecifika regleringar inom finanssektorn, hälso- och sjukvården, och offentlig förvaltning. Dessutom ställer svenska myndigheters ökande krav på digitalisering och säkerhet nya utmaningar som kräver systematiska och automatiserade approaches.

Policy as Code erbjuder en strukturerad metod för att hantera denna komplexitet genom att möjliggöra:

**Automatiserad compliance-verifiering**: Istället för manuella granskningar och dokumentbaserade policies kan organisationer implementera automatiska kontroller som kontinuerligt validerar infrastrukturtillstånd mot regulatoriska krav.

**Proaktiv säkerhetsövervakning**: Policies kan implementeras som "guardrails" som förhindrar säkerhetsbrister redan vid design- och implementeringsstadiet, snarare än att upptäcka problem efter deployment.

**Konsekvent governance**: Genom att kodifiera organizational policies kan organisationer säkerställa konsekvent tillämpning över alla miljöer, team och projekt.

**Rapiditet i förändring**: När nya hot upptäcks eller regelverk ändras kan policy-uppdateringar distribueras snabbt och konsekvent över hela organisationens infrastruktur.

**Transparency och audit trails**: Alla policy-ändringar dokumenteras automatiskt genom versionhanteringssystem, vilket skapar kompletta audit trails för compliance-ändamål.

Detta kapitel fördjupar sig i de tekniska och organisatoriska aspekterna av Policy as Code, med särskilt fokus på hur svenska organisationer kan implementera dessa tekniker för att uppfylla både lokala och internationella compliance-krav. Vi kommer att utforska praktiska implementationer, verktyg och best practices som har visat sig framgångsrika i verkliga produktionsmiljöer.

## Grundläggande principer för Policy as Code

Policy as Code bygger på flera fundamentala principer som särskiljer det från traditionella säkerhetsmodeller. Dessa principer reflekterar en djupgående förståelse för hur moderna utvecklingsmetoder kan tillämpas på säkerhets- och compliance-domänen.

**Deklarativ policy-definition**: Istället för att beskriva hur säkerhetskonfigurationer ska implementeras, definierar Policy as Code det önskade tillståndet för säkerhet och compliance. Detta approach möjliggör större flexibilitet i implementation samtidigt som det säkerställer konsekvent resultat. Deklarativa policies är enklare att förstå, vederlägga och automatiiskt validera jämfört med procedurala scripts.

**Separation av concerns**: Policy as Code separerar policy-definition från policy-enforcement. Detta betyder att organisationer kan utveckla centraliserade policies som kan tillämpas konsekvent över olika tekniska plattformar och miljöer. Samma policy för datakryptering kan exempelvis tillämpas på AWS S3-buckets, Azure Storage-konton och on-premises databaser med platform-specifika enforcement-mekanismer.

**Immutable policy artifacts**: Precis som Infrastructure as Code behandlar infrastruktur som immutable artifacts, behandlar Policy as Code policies som versionshanterade, immutable components. Detta innebär att policy-ändringar resulterar i nya versioner snarare än modifikationer av befintliga policies, vilket möjliggör säker rollback och A/B-testning av policy-ändringar.

**Shift-left security**: En av de mest betydelsefulla aspekterna av Policy as Code är möjligheten att integrera säkerhetskontroller tidigt i utvecklingsprocessen. Genom att implementera policy-validering i CI/CD-pipelines kan säkerhetsproblem identifieras och åtgärdas före deployment till produktionsmiljöer.

**Evidence-based compliance**: Policy as Code genererar automatiskt bevis för compliance genom kontinuerlig monitoring och dokumentation av policy-decisions. Detta tillhandahåller robust dokumentation för regulators och auditors utan manual overhead.

För svenska organisationer är dessa principer särskilt värdefulla eftersom de möjliggör skalbar compliance med komplexa regelverk. Exempelvis kan GDPR-krav för dataminimering implementeras som policies som automatiskt validerar att persondata endast samlas in och bearbetas för specificerade ändamål, medan MSB:s säkerhetskrav kan implementeras som nätverkssegmenteringspolicies som automatiskt förhindrar otillåten trafik mellan säkerhetszoner.

**Risk-baserad policy enforcement**: Moderna Policy as Code-implementationer möjliggör risk-baserad enforcement där policies kan tillämpas olika strikt beroende på riskprofilen för specifika resurser eller miljöer. Produktionsmiljöer kan ha striktare policies än utvecklingsmiljöer, medan resurser som hanterar persondata kan ha ytterligare säkerhetskrav.

**Continuous compliance**: Traditionella compliance-modeller bygger på periodiska granskningar och snapshots av systemtillstånd. Policy as Code möjliggör kontinuerlig compliance-monitoring där avvikelser från policies detekteras i realtid och kan trigga automatiska remediation-åtgärder eller alerter.

Dessa principer formar grunden för de tekniska implementationer som diskuteras i resten av detta kapitel, inklusive Open Policy Agent, Kubernetes Gatekeeper, och den omfattande OSCAL-framework som representerar branschens mest avancerade approach till standardiserad säkerhets- och compliance-hantering.

## Open Policy Agent (OPA) och Rego - Djupgående förståelse

Open Policy Agent (OPA) har etablerat sig som den de facto-standarden för Policy as Code-implementationer, och detta är inte en slump. OPA representerar kulminationen av flera års forskning och praktisk utveckling inom området policy engines, och dess design reflekterar djupa insikter om vad som krävs för skalbar, flexibel och tillförlitlig policy enforcement i moderna infrastrukturer.

### OPA:s arkitektur och designfilosofi

OPA bygger på flera fundamentala designprinciper som gör det unikt lämpat för Policy as Code-implementationer:

**Domain-agnostic design**: Till skillnad från många säkerhetsverktyg som är byggda för specifika plattformar eller use cases, designades OPA från grunden för att vara plattformsoberoende. Detta betyder att samma policy engine kan användas för att validera Kubernetes-resources, AWS CloudFormation-templates, Terraform-planer, HTTP API-requests, och praktiskt taget vilken strukturerad data som helst.

**Decoupling av policy och enforcement**: OPA separerar strikt policy-definition från policy-enforcement. OPA-engine fokuserar på att evaluera policies mot input-data och returnera decisions, medan enforcement-logiken hanteras av externa system. Detta möjliggör flexibel integration med befintliga system utan att kräva omfattande omstrukturering.

**Eventual consistency och performance**: OPA designades för att hantera höga belastningar i produktionsystem. Policy-evaluering sker lokalt utan externa beroenden, vilket möjliggör låg latency och hög tillgänglighet. Policy-uppdateringar distribueras via eventual consistency-modeller som säkerställer att nya policies propageras till alla OPA-instanser utan att påverka ongoing policy-evaluations.

### Rego språket - Kraft och expressivitet

Rego, OPA:s policy-språk, representerar en sofistikerad balansgång mellan expressivitet och prestanda. Som ett deklarativt, logikbaserat språk erbjuder Rego unik kapacitet för att uttrycka komplexa business logic och regulatory requirements på ett sätt som är både människligt läsbart och maskinellt optimerbart.

**Logikprogrammering för policies**: Rego bygger på Datalog, ett subset av Prolog som optimerades för queries över stora datasets. Denna grund möjliggör Rego att naturligt uttrycka regler som "om denna condition är sann, då gäller denna conclusion", vilket direkt speglar hur människor tänker om policies och regelverk.

**Partial evaluation och optimization**: En av Rego:s mest kraftfulla funktioner är dess förmåga till partial evaluation. När en policy kompileras kan Rego-engine pre-compute delar av policy-logiken, vilket dramatiskt förbättrar runtime-performance. För svenska organisationer som måste validera tusentals infrastruktur-resurser mot komplexa GDPR- och MSB-krav betyder detta att omfattande compliance-kontroller kan utföras med minimal latency.

**Composability och modularity**: Rego policies kan struktureras som modulära komponenter som kan återanvändas och kombineras. Detta är kritiskt för organisationer som behöver hantera multiple compliance frameworks samtidigt - GDPR-regler kan kombineras med MSB-säkerhetskrav och branschspecifika regleringar utan code duplication.

### Praktisk Rego-implementation för svenska organisationer

Låt oss utforska en omfattande Rego-implementation som adresserar de komplexa compliance-kraven för svenska organisationer:

```rego
# policies/swedish_comprehensive_compliance.rego
package sweden.compliance.v2

import rego.v1

# ==============================================
# GDPR Artikel 32 - Säkerhet i behandlingen
# ==============================================

# Grundläggande krypteringskrav för persondata
encryption_required if {
    is_personal_data_resource
    not is_encrypted
}

is_personal_data_resource if {
    input.resource_type in data.sensitive_resource_types
    personal_data_classification
}

personal_data_classification if {
    classification := input.resource_attributes.tags.DataClassification
    classification in {"personal", "sensitive", "pii", "gdpr-protected"}
}

# Krypteringsvalidering per resurstyp med detaljerad logik
is_encrypted if {
    input.resource_type == "aws_s3_bucket"
    encryption_config := input.resource_attributes.server_side_encryption_configuration[_]
    encryption_config.rule[_].apply_server_side_encryption_by_default.sse_algorithm != ""
}

is_encrypted if {
    input.resource_type == "aws_rds_instance"
    input.resource_attributes.storage_encrypted == true
    input.resource_attributes.kms_key_id != ""
}

is_encrypted if {
    input.resource_type == "aws_ebs_volume"
    input.resource_attributes.encrypted == true
    input.resource_attributes.kms_key_id != ""
}

# Azure-resurser för svenska organisationer
is_encrypted if {
    input.resource_type == "azurerm_storage_account"
    encryption := input.resource_attributes.encryption[_]
    encryption.services.blob.enabled == true
    encryption.services.file.enabled == true
}

# ==============================================
# MSB Säkerhetskrav - Nätverkssegmentering
# ==============================================

# Avancerad nätverkssäkerhetsvalidering
network_violation[violation] if {
    input.resource_type == "aws_security_group"
    rule := input.resource_attributes.ingress[_]
    is_overly_permissive_rule(rule)
    violation := format_network_violation(rule)
}

is_overly_permissive_rule(rule) if {
    "0.0.0.0/0" in rule.cidr_blocks
    not is_allowed_public_port(rule.from_port)
}

is_allowed_public_port(port) if {
    port in {80, 443, 22}  # Endast dessa portar tillåtna från internet
}

format_network_violation(rule) := violation if {
    violation := {
        "type": "overly_permissive_network_rule",
        "severity": "critical",
        "port": rule.from_port,
        "protocol": rule.protocol,
        "sources": rule.cidr_blocks,
        "message": sprintf("Port %v exponerad från internet utan motivering", [rule.from_port])
    }
}

# ==============================================
# Datasuveränitet och geografisk compliance
# ==============================================

data_sovereignty_violation if {
    is_personal_data_resource
    not is_compliant_region
}

is_compliant_region if {
    resource_region := get_resource_region
    resource_region in data.approved_regions.sweden
}

get_resource_region := region if {
    # AWS-resurser
    region := input.resource_attributes.region
}

get_resource_region := region if {
    # Azure-resurser
    region := input.resource_attributes.location
}

get_resource_region := region if {
    # Google Cloud-resurser
    region := input.resource_attributes.zone
    region_parts := split(region, "-")
    region := concat("-", array.slice(region_parts, 0, 2))
}

# ==============================================
# Avancerad resurstagging för governance
# ==============================================

tagging_violations[violation] if {
    required_tags := data.governance.required_tags[input.resource_type]
    missing_tags := required_tags - object.keys(input.resource_attributes.tags)
    count(missing_tags) > 0
    violation := {
        "type": "missing_required_tags",
        "severity": "medium",
        "missing_tags": missing_tags,
        "resource_type": input.resource_type
    }
}

# Kostnadskontroll genom tag-validering
cost_control_violation if {
    not valid_cost_center
    estimated_monthly_cost > data.thresholds.cost_approval_required
}

valid_cost_center if {
    cost_center := input.resource_attributes.tags.CostCenter
    cost_center in data.approved_cost_centers
}

# ==============================================
# Sammansatt compliance-bedömning
# ==============================================

# Huvudfunktion som aggregerar alla compliance-kontroller
compliance_assessment := assessment if {
    violations := array.concat([
        gdpr_violations,
        msb_violations,
        sovereignty_violations,
        governance_violations
    ])
    
    assessment := {
        "resource_id": input.resource_id,
        "resource_type": input.resource_type,
        "timestamp": time.now_ns(),
        "total_violations": count(violations),
        "violations": violations,
        "compliance_score": calculate_compliance_score(violations),
        "risk_level": determine_risk_level(violations),
        "remediation_priority": calculate_remediation_priority(violations)
    }
}

# GDPR-specifika violations
gdpr_violations[violation] if {
    encryption_required
    violation := {
        "framework": "GDPR",
        "article": "Article 32",
        "type": "encryption_required",
        "severity": "high",
        "message": "Persondata måste krypteras enligt GDPR Artikel 32",
        "remediation": "Aktivera kryptering för denna resurs",
        "legal_reference": "GDPR Article 32(1)(a)"
    }
}

# MSB-specifika violations
msb_violations[violation] if {
    violation := network_violation[_]
    violation_with_framework := object.union(violation, {
        "framework": "MSB",
        "regulation": "Säkerhetskrav för kritisk infrastruktur",
        "legal_reference": "MSB-FS 2020:7"
    })
}

# Datasuveränitets-violations
sovereignty_violations[violation] if {
    data_sovereignty_violation
    violation := {
        "framework": "Swedish Data Protection",
        "type": "data_sovereignty",
        "severity": "critical",
        "message": "Persondata måste lagras inom godkända regioner",
        "remediation": "Flytta resurs till EU/Swedish region",
        "approved_regions": data.approved_regions.sweden
    }
}

# Governance-violations
governance_violations[violation] if {
    violation := tagging_violations[_]
    violation_with_framework := object.union(violation, {
        "framework": "Internal Governance",
        "regulation": "Corporate Resource Management Policy"
    })
}

# ==============================================
# Scoring och prioritering
# ==============================================

calculate_compliance_score(violations) := score if {
    total_penalty := sum([
        penalty |
        violation := violations[_]
        penalty := data.severity_weights[violation.severity]
    ])
    score := max([0, 100 - total_penalty])
}

determine_risk_level(violations) := risk_level if {
    critical_count := count([v | v := violations[_]; v.severity == "critical"])
    high_count := count([v | v := violations[_]; v.severity == "high"])
    
    risk_level := "critical" if critical_count > 0
    risk_level := "high" if {
        critical_count == 0
        high_count > 2
    }
    risk_level := "medium" if {
        critical_count == 0
        high_count > 0
        high_count <= 2
    }
    risk_level := "low" if {
        critical_count == 0
        high_count == 0
    }
}

calculate_remediation_priority(violations) := priority if {
    gdpr_violations_count := count([v | v := violations[_]; v.framework == "GDPR"])
    msb_violations_count := count([v | v := violations[_]; v.framework == "MSB"])
    
    priority := "immediate" if gdpr_violations_count > 0
    priority := "urgent" if {
        gdpr_violations_count == 0
        msb_violations_count > 0
    }
    priority := "normal"
}

# ==============================================
# Data definitions för konfiguration
# ==============================================

data := {
    "sensitive_resource_types": [
        "aws_s3_bucket",
        "aws_rds_instance", 
        "aws_dynamodb_table",
        "azurerm_storage_account",
        "azurerm_sql_database",
        "google_storage_bucket",
        "google_sql_database_instance"
    ],
    "approved_regions": {
        "sweden": [
            "eu-north-1",      # AWS Stockholm
            "eu-west-1",       # AWS Ireland  
            "eu-central-1",    # AWS Frankfurt
            "West Europe",     # Azure Netherlands
            "North Europe",    # Azure Ireland
            "europe-north1",   # GCP Finland
            "europe-west1"     # GCP Belgium
        ]
    },
    "severity_weights": {
        "critical": 25,
        "high": 15, 
        "medium": 10,
        "low": 5
    },
    "governance": {
        "required_tags": {
            "aws_instance": ["Project", "Environment", "Owner", "CostCenter"],
            "aws_s3_bucket": ["Project", "Environment", "Owner", "DataClassification"],
            "aws_rds_instance": ["Project", "Environment", "Owner", "DataClassification", "BackupSchedule"]
        }
    },
    "approved_cost_centers": [
        "IT-001", "DEV-002", "PROD-003", "TEST-004"
    ],
    "thresholds": {
        "cost_approval_required": 1000  # SEK per månad
    }
}
```

Denna omfattande Rego-implementation demonstrerar hur svenska organisationer kan strukturera komplexa compliance-krav på ett hanterbart och skalbart sätt. Policyn adresserar flera kritiska områden samtidigt och möjliggör granulär kontroll över olika aspekter av infrastructure compliance.

## OSCAL - Open Security Controls Assessment Language: Revolutionerande säkerhetsstandard

Open Security Controls Assessment Language (OSCAL) representerar en av de mest betydelsefulla innovationerna inom säkerhets- och compliance-hantering under det senaste decenniet. Utvecklad av National Institute of Standards and Technology (NIST) i samarbete med privata och offentliga organisationer världöver, erbjuder OSCAL en standardiserad, maskinläsbar representation av säkerhetskontroller, implementationer och bedömningar.

För svenska organisationer representerar OSCAL en transformativ möjlighet att standardisera och automatisera compliance-processer på ett sätt som tidigare varit omöjligt. Detta avsnitt fördjupar sig i OSCAL:s arkitektur, användningsområden och praktiska implementationer inom ramen för Policy as Code.

### OSCAL:s revolutionerande approach

Traditionella säkerhets- och compliance-frameworks har länge plågats av manuella processer, inkonsekvent dokumentation och svårigheter att demonstrera kontinuerlig compliance. OSCAL adresserar dessa fundamentala problem genom att introducera en machine-readable representation av säkerhetskontroller och compliance-artefakter.

**Strukturerad datarepresentation**: OSCAL definierar exakta datastrukturer för alla aspekter av säkerhetshantering - från kontrollkataloger och säkerhetskrav till implementationer och bedömningsresultat. Detta möjliggör automatiserad processing, validering och rapportering av säkerhetsdata.

**Lifecycle-coverage**: Till skillnad från statiska compliance-frameworks täcker OSCAL hela säkerhetslivscykeln från kontrollspecifikation genom implementation till kontinuerlig monitoring och bedömning. Detta möjliggör end-to-end-automation av compliance-processer.

**Interoperabilitet**: OSCAL:s standardiserade format möjliggör sömlös integration mellan olika säkerhetsverktyg, plattformar och organisationer. Detta är särskilt värdefullt för svenska organisationer som måste rapportera compliance till multiple myndigheter och samarbeta med leverantörer.

### OSCAL:s arkitektur och modeller

OSCAL bygger på fyra huvudsakliga modeller som tillsammans täcker hela säkerhetslivscykeln:

#### 1. Catalog Model - Säkerhetskontrolla kataloger

Catalog-modellen definierar strukturerad representation av säkerhetskontroller och compliance-krav. För svenska organisationer inkluderar detta både internationella standards som ISO 27001 och NIST samt lokala regelverk som MSB:s säkerhetskrav.

```xml
<!-- Exempel: OSCAL Catalog för MSB säkerhetskrav -->
<catalog xmlns="http://csrc.nist.gov/ns/oscal/1.0"
         uuid="12345678-1234-5678-9abc-def012345678">
    <metadata>
        <title>MSB Säkerhetskrav för Kritisk Infrastruktur</title>
        <published>2024-01-15T10:00:00Z</published>
        <last-modified>2024-01-15T10:00:00Z</last-modified>
        <version>1.0</version>
        <responsible-party uuid="msb-authority">
            <party-uuid>msb-organization</party-uuid>
            <role-id>authority</role-id>
        </responsible-party>
    </metadata>
    
    <group id="msb-network-security">
        <title>Nätverkssäkerhet</title>
        <control id="msb-ns-1">
            <title>Nätverkssegmentering</title>
            <prop name="label" value="MSB-NS-1"/>
            <part name="statement">
                <p>Organisationen ska implementera nätverkssegmentering för att 
                   separera kritiska system från mindre kritiska system och 
                   externa nätverk.</p>
            </part>
            <part name="guidance">
                <p>Nätverkssegmentering ska implementeras genom:</p>
                <p>a) Virtuella nätverk (VLANs) eller mjukvarudefinierade nätverk</p>
                <p>b) Brandväggar mellan nätverkssegment</p>
                <p>c) Åtkomstkontrolllistor (ACLs) för trafikkontroll</p>
                <p>d) Kontinuerlig övervakning av nätverkstrafik</p>
            </part>
        </control>
        
        <control id="msb-ns-2">
            <title>Intrångsskydd</title>
            <prop name="label" value="MSB-NS-2"/>
            <part name="statement">
                <p>Organisationen ska implementera intrångsskydd för att detektera 
                   och förhindra obehörig nätverksaktivitet.</p>
            </part>
            <part name="guidance">
                <p>Intrångsskydd inkluderar:</p>
                <p>a) Intrusion Detection Systems (IDS)</p>
                <p>b) Intrusion Prevention Systems (IPS)</p>
                <p>c) DDoS-skydd</p>
                <p>d) Anomalidetektering i nätverkstrafik</p>
            </part>
        </control>
    </group>
    
    <group id="msb-data-protection">
        <title>Dataskydd</title>
        <control id="msb-dp-1">
            <title>Kryptering av data i vila</title>
            <prop name="label" value="MSB-DP-1"/>
            <part name="statement">
                <p>Organisationen ska kryptera känsliga data när de lagras 
                   (data at rest) med godkända krypteringsalgoritmer.</p>
            </part>
            <part name="guidance">
                <p>Kryptering av data i vila ska:</p>
                <p>a) Använda AES-256 eller starkare algoritmer</p>
                <p>b) Implementera säker nyckelhantering</p>
                <p>c) Inkludera databasers och filers</p>
                <p>d) Täcka backup och arkiverad data</p>
            </part>
        </control>
    </group>
</catalog>
```

#### 2. Profile Model - Säkerhetsbaselines och profiles

Profile-modellen möjliggör organisationer att skapa skräddarsydda säkerhetsbaselines genom att välja och anpassa kontroller från en eller flera kataloger. För svenska organisationer kan detta innebära kombinationer av GDPR-krav, MSB-säkerhetskrav och branschspecifika regleringar.

```yaml
# Exempel: OSCAL Profile för svensk finansorganisation
profile:
  uuid: "financial-org-profile-2024"
  metadata:
    title: "Svensk Finansorganisation Säkerhetsprofil"
    published: "2024-01-15T10:00:00Z"
    version: "2.1"
    responsible-parties:
      - party-uuid: "financial-authority-se"
        role-id: "regulatory-authority"
  
  imports:
    - href: "msb-critical-infrastructure-catalog.xml"
      include-controls:
        - control-id: "msb-ns-1"
        - control-id: "msb-ns-2"  
        - control-id: "msb-dp-1"
    - href: "gdpr-catalog.xml" 
      include-controls:
        - control-id: "gdpr-art-32"
        - control-id: "gdpr-art-25"
    - href: "pci-dss-catalog.xml"
      include-controls:
        - control-id: "pci-req-3"
        - control-id: "pci-req-4"
  
  modify:
    set-parameters:
      - param-id: "encryption-algorithm"
        values: ["AES-256-GCM"]
      - param-id: "key-rotation-period" 
        values: ["90 days"]
      - param-id: "audit-log-retention"
        values: ["7 years"]  # Svenska lagkrav
    
    alters:
      - control-id: "msb-ns-1"
        additions:
          - position: "after"
            parts:
              - name: "swedish-specific-guidance"
                prose: "För organisationer som hanterar finansiella transaktioner 
                        ska nätverkssegmentering inkludera separata zoner för 
                        kortbetalningar enligt svensk finanslagstiftning."
```

#### 3. Component Definition Model - Säkerhetsimplementationer

Component Definition-modellen beskriver hur specifika system, produkter eller tjänster implementerar säkerhetskontroller. Detta är särskilt kraftfullt i Infrastructure as Code-sammanhang där komponenter kan vara allt från Terraform-moduler till Kubernetes-operatorer.

```json
{
  "component-definition": {
    "uuid": "terraform-aws-secure-vpc-component",
    "metadata": {
      "title": "Secure AWS VPC Terraform Module",
      "published": "2024-01-15T10:00:00Z",
      "version": "3.2.1",
      "responsible-parties": [
        {
          "party-uuid": "infrastructure-team",
          "role-id": "developer"
        }
      ]
    },
    "components": [
      {
        "uuid": "secure-vpc-component",
        "type": "infrastructure-module",
        "title": "Secure VPC Infrastructure Component",
        "description": "Terraform module som implementerar säker VPC-konfiguration enligt svenska säkerhetskrav",
        "control-implementations": [
          {
            "uuid": "msb-ns-1-implementation",
            "source": "msb-catalog.xml",
            "description": "Implementation av MSB nätverkssegmenteringskrav",
            "implemented-requirements": [
              {
                "uuid": "msb-ns-1-req",
                "control-id": "msb-ns-1",
                "statements": [
                  {
                    "statement-id": "msb-ns-1_stmt",
                    "description": "VPC konfigureras med separata subnets för olika säkerhetszoner",
                    "remarks": "Implementerad genom Terraform aws_subnet resurser med separata routing tables"
                  }
                ],
                "responsible-roles": [
                  {
                    "role-id": "infrastructure-engineer"
                  }
                ]
              }
            ]
          },
          {
            "uuid": "gdpr-art-32-implementation", 
            "source": "gdpr-catalog.xml",
            "description": "Implementation av GDPR Artikel 32 säkerhetskrav",
            "implemented-requirements": [
              {
                "uuid": "gdpr-art-32-req",
                "control-id": "gdpr-art-32",
                "statements": [
                  {
                    "statement-id": "gdpr-art-32_encryption",
                    "description": "VPC Flow Logs krypteras med KMS",
                    "remarks": "Alla flow logs dirigeras till krypterad S3 bucket med organisationens KMS-nyckel"
                  }
                ]
              }
            ]
          }
        ]
      }
    ]
  }
}
```

#### 4. System Security Plan (SSP) Model - Säkerhetsplaner

SSP-modellen beskriver hur en specifik organisation eller system implementerar och hanterar säkerhetskontroller. För svenska organisationer representerar detta dokumentation av deras compliance-posture och säkerhetsimplementationer.

### OSCAL i praktisk implementation med Policy as Code

OSCAL:s verkliga kraft realiseras när det integreras med Policy as Code-verktyg för att möjliggöra automatiserad compliance-validering och rapportering. Följande exempel demonstrerar hur OSCAL kan integreras med OPA för att skapa kraftfulla compliance-automationer:

```python
# oscal_policy_integration.py
import json
import yaml
import xml.etree.ElementTree as ET
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import requests

@dataclass
class OSCALControl:
    """Representerar en OSCAL säkerhetskontrola"""
    control_id: str
    title: str
    statement: str
    guidance: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None

@dataclass 
class ComplianceEvidence:
    """Bevis för compliance med specifik kontroll"""
    control_id: str
    implementation_status: str
    evidence_type: str
    evidence_data: Dict[str, Any]
    timestamp: datetime
    responsible_party: str

class OSCALPolicyIntegration:
    """
    Integration mellan OSCAL-kataloger och Policy as Code enforcement
    """
    
    def __init__(self, catalog_urls: List[str], profile_path: str):
        self.catalog_urls = catalog_urls
        self.profile_path = profile_path
        self.controls: Dict[str, OSCALControl] = {}
        self.load_catalogs()
        self.load_profile()
    
    def load_catalogs(self):
        """Ladda OSCAL-kataloger från URLs eller lokala filer"""
        for url in self.catalog_urls:
            if url.startswith('http'):
                response = requests.get(url)
                if url.endswith('.xml'):
                    self._parse_xml_catalog(response.text)
                else:
                    self._parse_json_catalog(response.json())
            else:
                with open(url, 'r', encoding='utf-8') as f:
                    if url.endswith('.xml'):
                        self._parse_xml_catalog(f.read())
                    else:
                        self._parse_json_catalog(json.load(f))
    
    def _parse_xml_catalog(self, xml_content: str):
        """Parse XML OSCAL catalog"""
        root = ET.fromstring(xml_content)
        namespace = {'oscal': 'http://csrc.nist.gov/ns/oscal/1.0'}
        
        for control in root.findall('.//oscal:control', namespace):
            control_id = control.get('id')
            title_elem = control.find('oscal:title', namespace)
            title = title_elem.text if title_elem is not None else ""
            
            statement_elem = control.find('.//oscal:part[@name="statement"]/oscal:p', namespace)
            statement = statement_elem.text if statement_elem is not None else ""
            
            guidance_elem = control.find('.//oscal:part[@name="guidance"]', namespace)
            guidance = None
            if guidance_elem is not None:
                guidance_texts = [p.text for p in guidance_elem.findall('oscal:p', namespace)]
                guidance = '\n'.join(guidance_texts)
            
            self.controls[control_id] = OSCALControl(
                control_id=control_id,
                title=title,
                statement=statement,
                guidance=guidance
            )
    
    def generate_opa_policies(self) -> Dict[str, str]:
        """Generera OPA/Rego policies baserat på OSCAL controls"""
        policies = {}
        
        for control_id, control in self.controls.items():
            if self._is_automation_candidate(control):
                policy_content = self._generate_rego_policy(control)
                policies[f"{control_id.replace('-', '_')}.rego"] = policy_content
        
        return policies
    
    def _is_automation_candidate(self, control: OSCALControl) -> bool:
        """Avgör om en kontroll kan automatiseras med Policy as Code"""
        automation_keywords = [
            'kryptering', 'encryption', 'nätverkssegmentering', 'network segmentation',
            'åtkomstkontroll', 'access control', 'logging', 'monitoring',
            'säkerhetsgrupper', 'security groups', 'brandvägg', 'firewall'
        ]
        
        text_to_check = f"{control.statement} {control.guidance or ''}".lower()
        return any(keyword.lower() in text_to_check for keyword in automation_keywords)
    
    def _generate_rego_policy(self, control: OSCALControl) -> str:
        """Generera Rego policy för specifik OSCAL control"""
        policy_template = f'''
# Automatiskt genererad policy för OSCAL control {control.control_id}
# Title: {control.title}
package oscal.{control.control_id.replace('-', '_')}

import rego.v1

# Control statement: {control.statement}

violation[result] if {{
    # Implementation av kontrolllogik baserat på control statement
    {self._generate_control_logic(control)}
    result := {{
        "control_id": "{control.control_id}",
        "title": "{control.title}",
        "severity": "high",
        "message": sprintf("Violation of OSCAL control %v: %v", ["{control.control_id}", "{control.title}"]),
        "remediation": "Se OSCAL guidance för remediation",
        "compliance_framework": "OSCAL"
    }}
}}

{self._generate_evidence_collection(control)}
'''
        return policy_template.strip()
    
    def _generate_control_logic(self, control: OSCALControl) -> str:
        """Generera kontrollspecifik logik baserat på control statement"""
        statement_lower = control.statement.lower()
        
        if 'kryptering' in statement_lower or 'encryption' in statement_lower:
            return '''
    input.resource_type in ["aws_s3_bucket", "aws_rds_instance", "aws_ebs_volume"]
    not is_encrypted'''
        
        elif 'nätverkssegmentering' in statement_lower or 'network segmentation' in statement_lower:
            return '''
    input.resource_type == "aws_security_group"
    rule := input.resource_attributes.ingress[_]
    "0.0.0.0/0" in rule.cidr_blocks
    not is_allowed_public_access(rule)'''
        
        elif 'åtkomstkontroll' in statement_lower or 'access control' in statement_lower:
            return '''
    input.resource_type in ["aws_iam_policy", "aws_iam_role"]
    policy_doc := json.unmarshal(input.resource_attributes.policy)
    statement := policy_doc.Statement[_]
    statement.Effect == "Allow"
    statement.Action == "*"
    statement.Resource == "*"'''
        
        else:
            return '''
    # Generisk kontrolllogik - kräver manuell implementation
    false  # Placeholder - implementera specifik logik'''
    
    def _generate_evidence_collection(self, control: OSCALControl) -> str:
        """Generera kod för evidence collection"""
        return f'''
# Evidence collection för control {control.control_id}
evidence[result] if {{
    not violation[_]  # Om ingen violation finns, samla bevis för compliance
    result := {{
        "control_id": "{control.control_id}",
        "status": "compliant",
        "evidence_type": "automated_validation",
        "resource_id": input.resource_id,
        "timestamp": time.now_ns(),
        "validation_method": "opa_policy_evaluation"
    }}
}}'''

    def collect_compliance_evidence(self, resource_data: Dict[str, Any]) -> List[ComplianceEvidence]:
        """Samla compliance-bevis för specifik resurs"""
        evidence_list = []
        
        for control_id in self.controls:
            # Simulera evaluation av OPA policy för denna control
            evidence = self._evaluate_control_compliance(control_id, resource_data)
            if evidence:
                evidence_list.append(evidence)
        
        return evidence_list
    
    def _evaluate_control_compliance(self, control_id: str, resource_data: Dict[str, Any]) -> Optional[ComplianceEvidence]:
        """Evaluera compliance för specifik control"""
        # I verklig implementation skulle detta använda OPA engine
        # För demonstration returnerar vi mock evidence
        
        if control_id == "msb-dp-1":  # Kryptering av data i vila
            is_compliant = self._check_encryption_compliance(resource_data)
            return ComplianceEvidence(
                control_id=control_id,
                implementation_status="implemented" if is_compliant else "non-compliant",
                evidence_type="automated_scan",
                evidence_data={
                    "resource_type": resource_data.get("resource_type"),
                    "encryption_enabled": is_compliant,
                    "scan_method": "terraform_plan_analysis"
                },
                timestamp=datetime.now(),
                responsible_party="infrastructure-team"
            )
        
        return None
    
    def _check_encryption_compliance(self, resource_data: Dict[str, Any]) -> bool:
        """Kontrollera kryptering för resurs"""
        resource_type = resource_data.get("resource_type")
        attributes = resource_data.get("resource_attributes", {})
        
        if resource_type == "aws_s3_bucket":
            return bool(attributes.get("server_side_encryption_configuration"))
        elif resource_type == "aws_rds_instance":
            return bool(attributes.get("storage_encrypted"))
        elif resource_type == "aws_ebs_volume":
            return bool(attributes.get("encrypted"))
        
        return False
    
    def generate_compliance_report(self, evidence_list: List[ComplianceEvidence]) -> Dict[str, Any]:
        """Generera OSCAL-kompatibel compliance rapport"""
        compliant_controls = [e for e in evidence_list if e.implementation_status == "implemented"]
        non_compliant_controls = [e for e in evidence_list if e.implementation_status == "non-compliant"]
        
        compliance_score = (len(compliant_controls) / len(evidence_list)) * 100 if evidence_list else 0
        
        report = {
            "assessment-results": {
                "uuid": f"assessment-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
                "metadata": {
                    "title": "Automatiserad OSCAL Compliance Assessment",
                    "published": datetime.now().isoformat(),
                    "version": "1.0",
                    "responsible-parties": [
                        {
                            "party-uuid": "automation-system",
                            "role-id": "assessor"
                        }
                    ]
                },
                "results": [
                    {
                        "uuid": f"result-{control.control_id}",
                        "title": f"Assessment av {control.control_id}",
                        "start": evidence.timestamp.isoformat(),
                        "observations": [
                            {
                                "uuid": f"obs-{control.control_id}",
                                "description": f"Automatiserad kontroll av {control.control_id}",
                                "methods": ["AUTOMATED"],
                                "types": ["control-objective"],
                                "subjects": [
                                    {
                                        "subject-uuid": "infrastructure-system",
                                        "type": "system"
                                    }
                                ],
                                "relevant-evidence": [
                                    {
                                        "href": f"evidence-{control.control_id}.json",
                                        "description": "Automatiskt genererad evidence data"
                                    }
                                ]
                            }
                        ],
                        "findings": [
                            {
                                "uuid": f"finding-{control.control_id}",
                                "title": f"Finding för {control.control_id}",
                                "description": f"Kontroll {control.control_id} är {'implementerad' if evidence.implementation_status == 'implemented' else 'ej implementerad'}",
                                "target": {
                                    "type": "objective-id",
                                    "target-id": control.control_id
                                }
                            }
                        ]
                    }
                    for control, evidence in zip(
                        [self.controls[e.control_id] for e in evidence_list],
                        evidence_list
                    )
                ],
                "assessment-summary": {
                    "compliance-score": compliance_score,
                    "total-controls": len(evidence_list),
                    "compliant-controls": len(compliant_controls),
                    "non-compliant-controls": len(non_compliant_controls)
                }
            }
        }
        
        return report

# Användningsexempel för svenska organisationer
def demonstrate_oscal_integration():
    """Demonstration av OSCAL integration med Policy as Code"""
    
    # Initiera OSCAL integration med svenska katalogern
    oscal_integration = OSCALPolicyIntegration(
        catalog_urls=[
            "catalogs/msb-kritisk-infrastruktur.xml",
            "catalogs/gdpr-controls.json",
            "catalogs/iso27001-swedish.xml"
        ],
        profile_path="profiles/swedish-financial-org.yaml"
    )
    
    # Generera OPA policies baserat på OSCAL controls
    generated_policies = oscal_integration.generate_opa_policies()
    
    print("Genererade OPA policies från OSCAL controls:")
    for policy_name, policy_content in generated_policies.items():
        print(f"\n=== {policy_name} ===")
        print(policy_content[:500] + "...")
    
    # Simulera resource data för testing
    test_resource = {
        "resource_id": "aws_rds_instance.production_db",
        "resource_type": "aws_rds_instance",
        "resource_attributes": {
            "storage_encrypted": True,
            "kms_key_id": "arn:aws:kms:eu-north-1:123456789:key/12345678",
            "tags": {
                "DataClassification": "personal",
                "Environment": "production"
            }
        }
    }
    
    # Samla compliance evidence
    evidence = oscal_integration.collect_compliance_evidence(test_resource)
    
    # Generera compliance rapport
    report = oscal_integration.generate_compliance_report(evidence)
    
    print(f"\nCompliance report genererad:")
    print(f"Total controls: {report['assessment-results']['assessment-summary']['total-controls']}")
    print(f"Compliance score: {report['assessment-results']['assessment-summary']['compliance-score']:.1f}%")
    
    return report

if __name__ == "__main__":
    demonstrate_oscal_integration()
```

### OSCAL:s fördelar för svenska organisationer

Implementation av OSCAL inom svenska organisationer erbjuder flera transformativa fördelar:

**Standardiserad compliance-rapportering**: OSCAL möjliggör konsekvent rapportering till olika svenska myndigheter (MSB, Finansinspektionen, Integritetsskyddsmyndigheten) genom standardiserade format som reducerar administrativa bördor.

**Automatiserad audit trails**: Genom att integrera OSCAL med Infrastructure as Code-verktyg kan organisationer automatiskt generera detaljerade audit trails som demonstrerar kontinuerlig compliance med svenska regelverk.

**Skalbar compliance-hantering**: OSCAL:s modulära struktur möjliggör organisationer att hantera multiple compliance-frameworks samtidigt utan duplicering av effort.

**Reduced compliance costs**: Automatisering av compliance-processer genom OSCAL kan dramatiskt reducera kostnaderna för manual compliance-hantering och audit-förberedelser.

**Risk-baserad prioritering**: OSCAL:s strukturerade approach möjliggör sofistikerad risk-analys och prioritering av säkerhetsåtgärder baserat på reglatoriska krav och organisatoriska risktolerans.

### Framtida utveckling och svenska perspektiv

OSCAL fortsätter att utvecklas med input från internationella säkerhetsexperter och regulators. För svenska organisationer representerar detta en möjlighet att påverka utvecklingen av internationella säkerhetsstandarder samtidigt som man säkerställer att svenska säkerhetskrav och regulatoriska behov representeras i framtida versioner.

Den svenska säkerhetscommunity bör aktivt engagera sig i OSCAL:s utveckling för att säkerställa att frameworks stödjer svenska compliance-krav och integrerar väl med befintliga svenska säkerhetsstandarder och myndighetsprocesser.

## Gatekeeper och Kubernetes Policy Enforcement - Avancerad containersäkerhet

Kubernetes-miljöer representerar en fundamental förändring i hur applications deployeras och hanteras, men de introducerar också nya säkerhetsutmaningar som kräver specialiserade policy enforcement-mekanismer. Gatekeeper, som bygger på Open Policy Agent, har utvecklats specifikt för att adressera dessa utmaningar genom att tillhandahålla admission control capabilities som validerar Kubernetes-resurser innan de deployeras till klustret.

### Gatekeeper:s arkitektur och admission control

Gatekeeper implementerar Kubernetes admission control webhook pattern för att intercepta alla resource creation och modification requests innan de committas till etcd. Detta möjliggör proaktiv policy enforcement som förhindrar non-compliant resources från att ens bli skapade, till skillnad från reaktiva monitoring approaches som upptäcker problems efter deployment.

**Admission controller integration**: Gatekeeper registrerar sig som en validating admission controller i Kubernetes API server, vilket innebär att alla resource requests automatiskt routas genom Gatekeeper för policy evaluation innan de accepteras eller avvisas.

**Template-based policy management**: Gatekeeper introducerar Constraint Templates som definierar återanvändbara policy patterns. Dessa templates kan sedan instansieras med specifika parametrar för olika environments, namespaces eller use cases, vilket möjliggör både standardisering och flexibilitet.

**Rego-powered evaluation**: Eftersom Gatekeeper bygger på OPA använder det samma Rego policy language som vi diskuterat tidigare, vilket möjliggör konsekvent policy development över hela infrastrukturen.

### Avancerade Kubernetes Security Policies för svenska organisationer

För svenska organisationer som måste uppfylla strikta säkerhetskrav är Gatekeeper:s capabilities kritiska för att säkerställa compliance redan vid deployment-tiden. Följande exempel demonstrerar omfattande policy implementations:

```yaml
# gatekeeper/swedish-security-framework.yaml
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: swedishcompliancerequirements
  annotations:
    description: "Comprehensive policy template för svenska säkerhets- och compliance-krav"
    regulation.sweden.se/gdpr: "true"
    regulation.sweden.se/msb: "true"
    regulation.sweden.se/pci-dss: "conditional"
spec:
  crd:
    spec:
      names:
        kind: SwedishComplianceRequirements
      validation:
        openAPIV3Schema:
          type: object
          properties:
            dataClassification:
              type: array
              items:
                type: string
              description: "Krav på dataklassificering labels"
            securityContextRequired:
              type: boolean
              description: "Kräv security context för alla containers"
            networkPolicyRequired:
              type: boolean
              description: "Kräv network policies för namespaces"
            resourceLimitsRequired:
              type: boolean
              description: "Kräv resource limits för alla containers"
            auditLoggingRequired:
              type: boolean
              description: "Kräv audit logging för privileged operations"
            encryptionRequired:
              type: boolean
              description: "Kräv kryptering för persistent volumes"
            allowedRegistries:
              type: array
              items:
                type: string
              description: "Lista över godkända container registries"
            prohibitedCapabilities:
              type: array
              items:
                type: string
              description: "Linux capabilities som inte får användas"
            maxPrivilegeEscalation:
              type: boolean
              description: "Tillåt privilege escalation"
            complianceFrameworks:
              type: array
              items:
                type: string
              description: "Compliance frameworks som ska enforcements"
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package swedishcompliancerequirements
        
        import rego.v1
        
        # ==============================================
        # GDPR Artikel 32 - Säkerhet i behandlingen
        # ==============================================
        
        violation[{"msg": msg}] if {
            input.review.object.kind in ["Pod", "Deployment", "StatefulSet", "DaemonSet"]
            not has_required_data_classification
            msg := sprintf("Resurs %v saknar obligatorisk GDPR dataklassificering enligt Artikel 32", [input.review.object.metadata.name])
        }
        
        has_required_data_classification if {
            required_labels := input.parameters.dataClassification
            resource_labels := input.review.object.metadata.labels
            classification := resource_labels["se.gdpr.dataclassification"]
            classification in required_labels
        }
        
        # Krav på kryptering för persistent volumes med persondata
        violation[{"msg": msg}] if {
            input.review.object.kind == "PersistentVolumeClaim"
            input.parameters.encryptionRequired
            has_personal_data_classification
            not has_encryption_annotation
            msg := "PersistentVolumeClaim med persondata måste ha kryptering aktiverad enligt GDPR"
        }
        
        has_personal_data_classification if {
            classification := input.review.object.metadata.labels["se.gdpr.dataclassification"]
            classification in ["personal", "sensitive", "pii"]
        }
        
        has_encryption_annotation if {
            input.review.object.metadata.annotations["volume.kubernetes.io/encryption-required"] == "true"
        }
        
        # ==============================================
        # MSB Säkerhetskrav för kritisk infrastruktur
        # ==============================================
        
        violation[{"msg": msg}] if {
            input.review.object.kind in ["Pod", "Deployment", "StatefulSet", "DaemonSet"]
            not has_security_context
            input.parameters.securityContextRequired
            msg := sprintf("Container %v måste ha security context enligt MSB säkerhetskrav", [container.name])
        }
        
        has_security_context if {
            container := get_containers[_]
            container.securityContext.runAsNonRoot == true
            container.securityContext.readOnlyRootFilesystem == true
            container.securityContext.allowPrivilegeEscalation == false
        }
        
        # Prohibited Linux capabilities enligt MSB-riktlinjer
        violation[{"msg": msg}] if {
            container := get_containers[_]
            prohibited := input.parameters.prohibitedCapabilities
            capability := container.securityContext.capabilities.add[_]
            capability in prohibited
            msg := sprintf("Container %v använder förbjuden capability %v enligt MSB säkerhetskrav", [container.name, capability])
        }
        
        # ==============================================
        # Nätverkssäkerhet och isolation
        # ==============================================
        
        violation[{"msg": msg}] if {
            input.review.object.kind == "Namespace"
            input.parameters.networkPolicyRequired
            not has_network_policy_annotation
            msg := "Namespace måste ha network policy annotation för nätverksisolation"
        }
        
        has_network_policy_annotation if {
            input.review.object.metadata.annotations["networking.kubernetes.io/network-policy-required"] == "true"
        }
        
        # ==============================================
        # Resource management och DoS-skydd
        # ==============================================
        
        violation[{"msg": msg}] if {
            container := get_containers[_]
            input.parameters.resourceLimitsRequired
            not has_resource_limits(container)
            msg := sprintf("Container %v måste ha resource limits för DoS-skydd", [container.name])
        }
        
        has_resource_limits(container) if {
            container.resources.limits.memory
            container.resources.limits.cpu
            container.resources.requests.memory
            container.resources.requests.cpu
        }
        
        # ==============================================
        # Container registry security
        # ==============================================
        
        violation[{"msg": msg}] if {
            container := get_containers[_]
            allowed_registries := input.parameters.allowedRegistries
            not is_allowed_registry(container.image, allowed_registries)
            msg := sprintf("Container %v använder icke-godkänd registry: %v", [container.name, container.image])
        }
        
        is_allowed_registry(image, allowed_registries) if {
            registry := allowed_registries[_]
            startswith(image, registry)
        }
        
        # ==============================================
        # Audit logging för compliance
        # ==============================================
        
        violation[{"msg": msg}] if {
            input.review.object.kind in ["Pod", "Deployment", "StatefulSet"]
            is_privileged_workload
            input.parameters.auditLoggingRequired
            not has_audit_logging_annotation
            msg := "Privileged workloads måste ha audit logging aktiverad"
        }
        
        is_privileged_workload if {
            container := get_containers[_]
            container.securityContext.privileged == true
        }
        
        is_privileged_workload if {
            container := get_containers[_]
            "SYS_ADMIN" in container.securityContext.capabilities.add
        }
        
        has_audit_logging_annotation if {
            input.review.object.metadata.annotations["audit.kubernetes.io/required"] == "true"
        }
        
        # ==============================================
        # Utility functions
        # ==============================================
        
        get_containers[container] if {
            input.review.object.spec.containers[_] = container
        }
        
        get_containers[container] if {
            input.review.object.spec.template.spec.containers[_] = container
        }
        
        get_containers[container] if {
            input.review.object.spec.jobTemplate.spec.template.spec.containers[_] = container
        }

---
# Constraint instance för production environment
apiVersion: config.gatekeeper.sh/v1alpha1
kind: SwedishComplianceRequirements
metadata:
  name: production-compliance
  namespace: gatekeeper-system
spec:
  enforcementAction: "deny"  # Strikt enforcement för produktion
  match:
    - apiGroups: [""]
      kinds: ["Pod"]
      namespaces: ["production", "staging"]
    - apiGroups: ["apps"]
      kinds: ["Deployment", "StatefulSet", "DaemonSet"]
      namespaces: ["production", "staging"]
    - apiGroups: [""]
      kinds: ["PersistentVolumeClaim"]
      namespaces: ["production", "staging"]
  parameters:
    dataClassification: ["public", "internal", "confidential", "personal"]
    securityContextRequired: true
    networkPolicyRequired: true
    resourceLimitsRequired: true
    auditLoggingRequired: true
    encryptionRequired: true
    allowedRegistries: 
      - "registry.company.se/"
      - "gcr.io/company-project/"
      - "quay.io/company/"
    prohibitedCapabilities:
      - "SYS_ADMIN"
      - "NET_ADMIN" 
      - "SYS_TIME"
      - "SYS_MODULE"
    maxPrivilegeEscalation: false
    complianceFrameworks: ["GDPR", "MSB", "ISO27001"]

---
# Constraint instance för development environment (mindre strikt)
apiVersion: config.gatekeeper.sh/v1alpha1
kind: SwedishComplianceRequirements
metadata:
  name: development-compliance
  namespace: gatekeeper-system
spec:
  enforcementAction: "warn"  # Endast varningar för utveckling
  match:
    - apiGroups: [""]
      kinds: ["Pod"]
      namespaces: ["development", "testing"]
    - apiGroups: ["apps"]
      kinds: ["Deployment", "StatefulSet", "DaemonSet"]
      namespaces: ["development", "testing"]
  parameters:
    dataClassification: ["public", "internal", "test-data"]
    securityContextRequired: false
    networkPolicyRequired: false
    resourceLimitsRequired: true  # Fortfarande viktigt för resource management
    auditLoggingRequired: false
    encryptionRequired: false
    allowedRegistries: 
      - "registry.company.se/"
      - "gcr.io/company-project/"
      - "docker.io/"  # Tillåt public registries för utveckling
      - "quay.io/"
    prohibitedCapabilities:
      - "SYS_ADMIN"  # Vissa capabilities fortfarande förbjudna
    maxPrivilegeEscalation: true  # Tillåt för utveckling/debugging
    complianceFrameworks: ["internal-dev-standards"]
```

### Integration med OSCAL för Kubernetes compliance

En av de mest kraftfulla aspekterna av modern Policy as Code är möjligheten att integrera OSCAL-standarder direkt med Kubernetes policy enforcement. Detta möjliggör organizations att automatiskt validera compliance med formella säkerhetsstandarder:

```yaml
# gatekeeper/oscal-integration-template.yaml
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: oscalcontrolvalidation
  annotations:
    oscal.nist.gov/catalog: "msb-critical-infrastructure-v1"
    oscal.nist.gov/control-id: "msb-ns-1"
    oscal.nist.gov/implementation-status: "automated"
spec:
  crd:
    spec:
      names:
        kind: OSCALControlValidation
      validation:
        openAPIV3Schema:
          type: object
          properties:
            oscalControlId:
              type: string
              description: "OSCAL Control ID som valideras"
            catalogSource:
              type: string
              description: "URL eller referens till OSCAL catalog"
            complianceEvidence:
              type: boolean
              description: "Generera automatisk compliance evidence"
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package oscalcontrolvalidation
        
        import rego.v1
        
        violation[result] if {
            control_id := input.parameters.oscalControlId
            not validate_oscal_control(control_id)
            result := {
                "msg": sprintf("Resource violates OSCAL control %v", [control_id]),
                "oscal_control_id": control_id,
                "catalog_source": input.parameters.catalogSource,
                "compliance_status": "non-compliant",
                "evidence_required": input.parameters.complianceEvidence
            }
        }
        
        validate_oscal_control(control_id) if {
            control_id == "msb-ns-1"  # Nätverkssegmentering
            validate_network_segmentation
        }
        
        validate_oscal_control(control_id) if {
            control_id == "msb-dp-1"  # Data protection
            validate_data_protection
        }
        
        validate_network_segmentation if {
            input.review.object.kind == "NetworkPolicy"
            # Validera att NetworkPolicy implementerar segmentering
            input.review.object.spec.policyTypes[_] == "Ingress"
            input.review.object.spec.policyTypes[_] == "Egress"
        }
        
        validate_data_protection if {
            input.review.object.kind == "PersistentVolumeClaim"
            encryption_annotation := input.review.object.metadata.annotations["volume.kubernetes.io/encryption"]
            encryption_annotation == "required"
        }
```

### Monitoring och observability för Gatekeeper

Effective policy enforcement kräver robust monitoring och observability för att säkerställa att policies fungerar som intended och för att identifiera trends i compliance-violations:

```yaml
# monitoring/gatekeeper-monitoring.yaml
apiVersion: v1
kind: ServiceMonitor
metadata:
  name: gatekeeper-metrics
  namespace: gatekeeper-system
spec:
  selector:
    matchLabels:
      app: gatekeeper-controller-manager
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics

---
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: gatekeeper-compliance-alerts
  namespace: gatekeeper-system
spec:
  groups:
  - name: gatekeeper.compliance
    rules:
    - alert: HighPolicyViolationRate
      expr: rate(gatekeeper_violations_total[5m]) > 0.1
      for: 2m
      labels:
        severity: warning
        component: gatekeeper
        compliance_impact: "medium"
      annotations:
        summary: "Högt antal policy violations detekterat"
        description: "Policy violation rate är {{ $value }} violations per sekund"
    
    - alert: CriticalComplianceViolation
      expr: increase(gatekeeper_violations_total{severity="critical"}[1m]) > 0
      for: 0m
      labels:
        severity: critical
        component: gatekeeper
        compliance_impact: "high"
      annotations:
        summary: "Kritisk compliance violation detekterad"
        description: "Critical violation i {{ $labels.violation_kind }} för kontroll {{ $labels.control_id }}"
    
    - alert: GatekeeperDown
      expr: up{job="gatekeeper-controller-manager"} == 0
      for: 1m
      labels:
        severity: critical
        component: gatekeeper
      annotations:
        summary: "Gatekeeper är ej tillgänglig"
        description: "Policy enforcement är avaktiverad - säkerhetsrisk!"

---
# Dashboard konfiguration för Grafana
apiVersion: v1
kind: ConfigMap
metadata:
  name: gatekeeper-dashboard
  namespace: gatekeeper-system
data:
  dashboard.json: |
    {
      "dashboard": {
        "title": "Gatekeeper Compliance Dashboard",
        "panels": [
          {
            "title": "Policy Violations (24h)",
            "type": "stat",
            "targets": [
              {
                "expr": "increase(gatekeeper_violations_total[24h])",
                "legendFormat": "Violations"
              }
            ]
          },
          {
            "title": "Compliance Score by Framework",
            "type": "piechart", 
            "targets": [
              {
                "expr": "gatekeeper_compliance_score_by_framework",
                "legendFormat": "{{ framework }}"
              }
            ]
          },
          {
            "title": "Violations by Severity",
            "type": "bargauge",
            "targets": [
              {
                "expr": "sum by (severity) (gatekeeper_violations_total)",
                "legendFormat": "{{ severity }}"
              }
            ]
          }
        ]
      }
    }
```

Genom denna omfattande approach till Kubernetes policy enforcement kan svenska organisationer säkerställa att deras container-baserade infrastrukturer uppfyller både tekniska säkerhetskrav och regulatoriska compliance-krav redan vid deployment-tiden.

## Terraform Policy Integration - Infrastruktur som kod med governance

Terraform policy enforcement representerar en kritisk komponent i moderna Infrastructure as Code-implementationer, särskilt för svenska organisationer som måste navigera komplexa regulatoriska krav samtidigt som de strävar efter automation och efficiency. Till skillnad från runtime policy enforcement som validerar system efter deployment, möjliggör Terraform policy integration proaktiv validering av infrastrukturbeslut före deployment.

### Strategiska approaches för Terraform policy enforcement

**Plan-time validation**: Terraform policy enforcement implementeras primärt vid plan-time, vilket innebär att policies evalueras mot Terraform execution plans innan någon faktisk infrastruktur modifieras. Detta möjliggör early detection av compliance issues och säkerhetsproblem utan kostnad eller risk för live systems.

**Multi-layer governance**: Effective Terraform policy enforcement implementeras i flera lager: lokalt under utveckling, i CI/CD-pipelines före deployment, och kontinuerligt genom infrastructure scanning tools. Denna multi-layer approach säkerställer comprehensive coverage utan att introducera unnecessary friction i utvecklingsprocessen.

**Policy as Code lifecycle**: Terraform policies följer samma lifecycle-principer som Infrastructure as Code - de versionshanteras, testas, code reviewas, och deployeras genom automated pipelines. Detta säkerställer att policy-ändringar genomgår samma rigor som infrastructure-ändringar.

### Omfattande Terraform policy implementation

```python
# terraform_policy_framework.py
import json
import subprocess
import tempfile
import os
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime
import hcl2
import boto3
import logging
from pathlib import Path

@dataclass
class PolicyViolation:
    """Representation av en policy violation"""
    violation_id: str
    policy_name: str
    severity: str
    resource_address: str
    resource_type: str
    message: str
    regulation: str
    remediation: str
    evidence: Dict[str, Any] = field(default_factory=dict)
    compliance_framework: str = ""

@dataclass
class ComplianceReport:
    """Comprehensive compliance rapport för Terraform plan"""
    plan_file: str
    timestamp: datetime
    total_resources: int
    violations: List[PolicyViolation]
    compliance_score: float
    framework_scores: Dict[str, float]
    recommendations: List[str]
    risk_assessment: Dict[str, Any]

class SwedishTerraformPolicyEngine:
    """
    Comprehensive policy engine för svenska Terraform-implementationer
    """
    
    def __init__(self, config_path: str = "policy_config.yaml"):
        self.config = self._load_configuration(config_path)
        self.aws_client = boto3.client('sts')  # För region och account validation
        self.logger = self._setup_logging()
        
        # Policy functions mappings
        self.policy_functions = {
            'gdpr_compliance': self._evaluate_gdpr_compliance,
            'msb_security': self._evaluate_msb_security,
            'data_sovereignty': self._evaluate_data_sovereignty,
            'cost_governance': self._evaluate_cost_governance,
            'security_groups': self._evaluate_security_groups,
            'encryption_compliance': self._evaluate_encryption_compliance,
            'network_topology': self._evaluate_network_topology,
            'iam_governance': self._evaluate_iam_governance
        }
    
    def validate_terraform_plan(self, plan_file_path: str) -> ComplianceReport:
        """
        Huvudfunktion för Terraform plan validation mot svenska compliance-krav
        """
        self.logger.info(f"Börjar policy validation för plan: {plan_file_path}")
        
        # Ladda och parse Terraform plan
        plan_data = self._load_terraform_plan(plan_file_path)
        if not plan_data:
            raise ValueError(f"Kunde inte ladda plan från {plan_file_path}")
        
        violations = []
        
        # Evaluera varje resurs mot applicable policies
        for resource_change in plan_data.get('resource_changes', []):
            resource_violations = self._evaluate_resource_policies(resource_change)
            violations.extend(resource_violations)
        
        # Evaluera plan-level policies (cross-resource dependencies, etc.)
        plan_violations = self._evaluate_plan_level_policies(plan_data)
        violations.extend(plan_violations)
        
        # Generera comprehensive compliance rapport
        compliance_report = self._generate_compliance_report(
            plan_file_path, plan_data, violations
        )
        
        self.logger.info(f"Policy validation komplett. {len(violations)} violations hittade.")
        return compliance_report
    
    def _evaluate_resource_policies(self, resource_change: Dict) -> List[PolicyViolation]:
        """Evaluera alla applicable policies för en specific resource"""
        violations = []
        resource_type = resource_change.get('type', '')
        resource_address = resource_change.get('address', '')
        resource_config = resource_change.get('change', {}).get('after', {})
        
        # Bestäm vilka policies som är applicable för denna resource type
        applicable_policies = self._get_applicable_policies(resource_type)
        
        for policy_name in applicable_policies:
            if policy_name in self.policy_functions:
                policy_violations = self.policy_functions[policy_name](
                    resource_type, resource_address, resource_config
                )
                violations.extend(policy_violations)
        
        return violations
    
    def _evaluate_gdpr_compliance(self, resource_type: str, resource_address: str, config: Dict) -> List[PolicyViolation]:
        """GDPR compliance evaluation för specific resource"""
        violations = []
        
        # Kontrollera om resource hanterar persondata
        if self._handles_personal_data(resource_type, config):
            
            # GDPR Artikel 32 - Säkerhet i behandlingen
            if not self._has_encryption(resource_type, config):
                violations.append(PolicyViolation(
                    violation_id=f"gdpr-art32-{resource_address}",
                    policy_name="GDPR Article 32 Encryption",
                    severity="high",
                    resource_address=resource_address,
                    resource_type=resource_type,
                    message="Persondata måste krypteras enligt GDPR Artikel 32",
                    regulation="GDPR Article 32(1)(a)",
                    remediation="Aktivera kryptering för denna resurs",
                    compliance_framework="GDPR",
                    evidence={
                        "data_classification": config.get('tags', {}).get('DataClassification'),
                        "encryption_status": self._get_encryption_status(resource_type, config)
                    }
                ))
            
            # GDPR Artikel 25 - Dataskydd genom design och som standard
            if not self._has_privacy_by_design(resource_type, config):
                violations.append(PolicyViolation(
                    violation_id=f"gdpr-art25-{resource_address}",
                    policy_name="GDPR Article 25 Privacy by Design",
                    severity="medium",
                    resource_address=resource_address,
                    resource_type=resource_type,
                    message="Resurs måste implementera dataskydd genom design",
                    regulation="GDPR Article 25",
                    remediation="Implementera privacy-by-design principer",
                    compliance_framework="GDPR"
                ))
        
        return violations
    
    def _evaluate_msb_security(self, resource_type: str, resource_address: str, config: Dict) -> List[PolicyViolation]:
        """MSB säkerhetskrav evaluation"""
        violations = []
        
        # MSB säkerhetskrav för kritisk infrastruktur
        if self._is_critical_infrastructure(resource_type, config):
            
            # Nätverkssegmentering
            if resource_type == 'aws_security_group':
                overly_permissive_rules = self._check_security_group_rules(config)
                for rule in overly_permissive_rules:
                    violations.append(PolicyViolation(
                        violation_id=f"msb-network-{resource_address}-{rule['port']}",
                        policy_name="MSB Network Segmentation",
                        severity="critical",
                        resource_address=resource_address,
                        resource_type=resource_type,
                        message=f"Otillåten nätverksexponering: port {rule['port']} exponerad från internet",
                        regulation="MSB-FS 2020:7",
                        remediation="Begränsa ingress till specifika IP-adresser eller använd VPN",
                        compliance_framework="MSB",
                        evidence={"rule_details": rule}
                    ))
            
            # Backup och kontinuitet
            if resource_type in ['aws_rds_instance', 'aws_dynamodb_table']:
                if not self._has_backup_enabled(resource_type, config):
                    violations.append(PolicyViolation(
                        violation_id=f"msb-backup-{resource_address}",
                        policy_name="MSB Backup Requirements",
                        severity="high",
                        resource_address=resource_address,
                        resource_type=resource_type,
                        message="Kritisk infrastruktur måste ha backup aktiverad",
                        regulation="MSB-FS 2020:7 Section 3.2",
                        remediation="Aktivera automatisk backup med lämplig retention",
                        compliance_framework="MSB"
                    ))
        
        return violations
    
    def _evaluate_data_sovereignty(self, resource_type: str, resource_address: str, config: Dict) -> List[PolicyViolation]:
        """Svensk datasuveränitet evaluation"""
        violations = []
        
        if self._stores_swedish_data(resource_type, config):
            if not self._is_compliant_region(config.get('region', '')):
                violations.append(PolicyViolation(
                    violation_id=f"sovereignty-{resource_address}",
                    policy_name="Swedish Data Sovereignty",
                    severity="critical",
                    resource_address=resource_address,
                    resource_type=resource_type,
                    message="Svenska/EU data måste lagras inom godkända regioner",
                    regulation="Dataskyddslagen (2018:218)",
                    remediation="Flytta resurs till eu-north-1, eu-west-1 eller eu-central-1",
                    compliance_framework="Swedish Law",
                    evidence={
                        "current_region": config.get('region'),
                        "approved_regions": self.config.get('approved_regions', [])
                    }
                ))
        
        return violations
    
    def _evaluate_cost_governance(self, resource_type: str, resource_address: str, config: Dict) -> List[PolicyViolation]:
        """Cost governance och budget compliance"""
        violations = []
        
        # Kontrollera resource tagging för cost allocation
        required_cost_tags = self.config.get('required_cost_tags', [])
        resource_tags = config.get('tags', {})
        missing_tags = set(required_cost_tags) - set(resource_tags.keys())
        
        if missing_tags:
            violations.append(PolicyViolation(
                violation_id=f"cost-tagging-{resource_address}",
                policy_name="Cost Management Tagging",
                severity="medium",
                resource_address=resource_address,
                resource_type=resource_type,
                message=f"Saknade cost management tags: {', '.join(missing_tags)}",
                regulation="Internal Cost Management Policy",
                remediation=f"Lägg till tags: {missing_tags}",
                compliance_framework="Internal Governance",
                evidence={"missing_tags": list(missing_tags)}
            ))
        
        # Kontrollera cost thresholds för dyra resurser
        estimated_cost = self._estimate_resource_cost(resource_type, config)
        cost_threshold = self.config.get('cost_thresholds', {}).get(resource_type, float('inf'))
        
        if estimated_cost > cost_threshold:
            violations.append(PolicyViolation(
                violation_id=f"cost-threshold-{resource_address}",
                policy_name="Cost Threshold Compliance",
                severity="medium" if estimated_cost < cost_threshold * 2 else "high",
                resource_address=resource_address,
                resource_type=resource_type,
                message=f"Resurs överskrider cost threshold: {estimated_cost} SEK/månad > {cost_threshold} SEK/månad",
                regulation="Internal Budget Policy",
                remediation="Godkännande krävs för deployment eller optimera resurs-konfiguration",
                compliance_framework="Internal Governance",
                evidence={
                    "estimated_monthly_cost": estimated_cost,
                    "threshold": cost_threshold
                }
            ))
        
        return violations
    
    def _evaluate_plan_level_policies(self, plan_data: Dict) -> List[PolicyViolation]:
        """Evaluera policies som kräver plan-wide analysis"""
        violations = []
        
        # Network topology validation
        network_violations = self._validate_network_topology(plan_data)
        violations.extend(network_violations)
        
        # Cross-resource dependency validation
        dependency_violations = self._validate_resource_dependencies(plan_data)
        violations.extend(dependency_violations)
        
        # Security posture assessment
        security_violations = self._assess_overall_security_posture(plan_data)
        violations.extend(security_violations)
        
        return violations
    
    def _validate_network_topology(self, plan_data: Dict) -> List[PolicyViolation]:
        """Validera network topology för säkerhet och compliance"""
        violations = []
        
        # Samla alla nätverksresurser
        vpcs = []
        subnets = []
        security_groups = []
        
        for resource in plan_data.get('resource_changes', []):
            if resource.get('type') == 'aws_vpc':
                vpcs.append(resource)
            elif resource.get('type') == 'aws_subnet':
                subnets.append(resource)
            elif resource.get('type') == 'aws_security_group':
                security_groups.append(resource)
        
        # Kontrollera VPC-segmentering för critical workloads
        if len(vpcs) == 1 and self._has_critical_workloads(plan_data):
            violations.append(PolicyViolation(
                violation_id="network-topology-single-vpc",
                policy_name="Network Segmentation for Critical Workloads",
                severity="medium",
                resource_address="network-topology",
                resource_type="network-design",
                message="Kritiska workloads bör separeras i dedicated VPCs",
                regulation="MSB Network Segmentation Guidelines",
                remediation="Överväg att separera kritiska system i egen VPC",
                compliance_framework="MSB"
            ))
        
        return violations
    
    def _generate_compliance_report(self, plan_file: str, plan_data: Dict, violations: List[PolicyViolation]) -> ComplianceReport:
        """Generera comprehensive compliance rapport"""
        
        total_resources = len(plan_data.get('resource_changes', []))
        
        # Beräkna compliance scores per framework
        framework_scores = self._calculate_framework_scores(violations, total_resources)
        overall_score = self._calculate_overall_compliance_score(violations, total_resources)
        
        # Generera recommendations baserat på violations
        recommendations = self._generate_recommendations(violations)
        
        # Risk assessment
        risk_assessment = self._assess_security_risk(violations, plan_data)
        
        return ComplianceReport(
            plan_file=plan_file,
            timestamp=datetime.now(),
            total_resources=total_resources,
            violations=violations,
            compliance_score=overall_score,
            framework_scores=framework_scores,
            recommendations=recommendations,
            risk_assessment=risk_assessment
        )
    
    def _calculate_framework_scores(self, violations: List[PolicyViolation], total_resources: int) -> Dict[str, float]:
        """Beräkna compliance scores per compliance framework"""
        frameworks = set(v.compliance_framework for v in violations if v.compliance_framework)
        framework_scores = {}
        
        for framework in frameworks:
            framework_violations = [v for v in violations if v.compliance_framework == framework]
            penalty = sum(self._get_severity_weight(v.severity) for v in framework_violations)
            max_possible_penalty = total_resources * 25  # Max penalty om alla resurser har critical violations
            score = max(0, 100 - (penalty / max_possible_penalty * 100))
            framework_scores[framework] = score
        
        return framework_scores
    
    def _get_severity_weight(self, severity: str) -> int:
        """Returnera numerisk weight för severity level"""
        weights = {
            'critical': 25,
            'high': 15,
            'medium': 10,
            'low': 5
        }
        return weights.get(severity.lower(), 5)
    
    def generate_ci_cd_integration(self) -> str:
        """Generera CI/CD pipeline integration kod"""
        return '''
# .github/workflows/terraform-policy-validation.yml
name: Terraform Policy Validation

on:
  pull_request:
    paths: 
      - 'infrastructure/**'
      - 'terraform/**'

jobs:
  policy-validation:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
      id-token: write
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_TERRAFORM_ROLE }}
          aws-region: eu-north-1
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: 1.7.0
      
      - name: Terraform Init
        working-directory: infrastructure
        run: terraform init
      
      - name: Terraform Plan
        working-directory: infrastructure
        run: |
          terraform plan -out=tfplan.binary
          terraform show -json tfplan.binary > tfplan.json
      
      - name: Install Policy Engine
        run: |
          pip install -r requirements.txt
          # Ladda policy configuration
          wget https://config.company.se/terraform-policies/config.yaml
      
      - name: Run Policy Validation
        id: policy_check
        run: |
          python scripts/terraform_policy_engine.py validate tfplan.json \\
            --config-file config.yaml \\
            --output-format json \\
            --output-file policy_report.json
          
          # Sätt exit code baserat på critical violations
          CRITICAL_COUNT=$(jq '.violations | map(select(.severity == "critical")) | length' policy_report.json)
          if [ "$CRITICAL_COUNT" -gt 0 ]; then
            echo "critical_violations=$CRITICAL_COUNT" >> $GITHUB_OUTPUT
            exit 1
          fi
      
      - name: Upload Policy Report
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: terraform-policy-report
          path: policy_report.json
          retention-days: 30
      
      - name: Comment PR with Results
        uses: actions/github-script@v7
        if: always()
        with:
          script: |
            const fs = require('fs');
            const report = JSON.parse(fs.readFileSync('policy_report.json', 'utf8'));
            
            const formatSeverity = (severity) => {
              const icons = {
                'critical': '🚨',
                'high': '⚠️', 
                'medium': '⚡',
                'low': 'ℹ️'
              };
              return `${icons[severity] || '❓'} ${severity.toUpperCase()}`;
            };
            
            const createComment = () => {
              let comment = `## 🔒 Terraform Policy Validation Results\\n\\n`;
              comment += `**Overall Compliance Score:** ${report.compliance_score.toFixed(1)}%\\n`;
              comment += `**Total Violations:** ${report.violations.length}\\n`;
              comment += `**Resources Analyzed:** ${report.total_resources}\\n\\n`;
              
              if (report.framework_scores && Object.keys(report.framework_scores).length > 0) {
                comment += `### 📊 Compliance by Framework\\n\\n`;
                for (const [framework, score] of Object.entries(report.framework_scores)) {
                  comment += `- **${framework}**: ${score.toFixed(1)}%\\n`;
                }
                comment += `\\n`;
              }
              
              if (report.violations.length > 0) {
                comment += `### ⚠️ Policy Violations\\n\\n`;
                
                const violationsByFramework = {};
                report.violations.forEach(v => {
                  const fw = v.compliance_framework || 'Other';
                  if (!violationsByFramework[fw]) violationsByFramework[fw] = [];
                  violationsByFramework[fw].push(v);
                });
                
                for (const [framework, violations] of Object.entries(violationsByFramework)) {
                  comment += `#### ${framework}\\n\\n`;
                  violations.slice(0, 10).forEach(violation => {
                    comment += `- ${formatSeverity(violation.severity)} **${violation.policy_name}**\\n`;
                    comment += `  - Resource: \`${violation.resource_address}\`\\n`;
                    comment += `  - Message: ${violation.message}\\n`;
                    comment += `  - Remediation: ${violation.remediation}\\n\\n`;
                  });
                  
                  if (violations.length > 10) {
                    comment += `  *... och ${violations.length - 10} fler violations*\\n\\n`;
                  }
                }
              }
              
              if (report.recommendations && report.recommendations.length > 0) {
                comment += `### 💡 Recommendations\\n\\n`;
                report.recommendations.forEach(rec => {
                  comment += `- ${rec}\\n`;
                });
              }
              
              comment += `\\n---\\n*Report generated at ${new Date(report.timestamp).toLocaleString('sv-SE')}*`;
              
              return comment;
            };
            
            await github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: createComment()
            });
        '''

# Exempel på användning i lokal utvecklingsmiljö
def demonstrate_local_usage():
    """Demonstrera lokal användning av policy engine"""
    
    # Initiera policy engine
    engine = SwedishTerraformPolicyEngine("config/policy_config.yaml")
    
    # Validera terraform plan
    try:
        report = engine.validate_terraform_plan("terraform/tfplan.json")
        
        print(f"\\n🔍 Policy Validation Results")
        print(f"{'='*50}")
        print(f"Overall Compliance Score: {report.compliance_score:.1f}%")
        print(f"Total Resources: {report.total_resources}")
        print(f"Violations Found: {len(report.violations)}")
        
        if report.framework_scores:
            print(f"\\n📊 Framework Compliance Scores:")
            for framework, score in report.framework_scores.items():
                print(f"  {framework}: {score:.1f}%")
        
        if report.violations:
            print(f"\\n⚠️  Critical Issues to Address:")
            critical_violations = [v for v in report.violations if v.severity == 'critical']
            for violation in critical_violations[:5]:
                print(f"  • {violation.policy_name}")
                print(f"    Resource: {violation.resource_address}")
                print(f"    Issue: {violation.message}")
                print(f"    Action: {violation.remediation}\\n")
        
        if report.recommendations:
            print(f"💡 Recommendations:")
            for rec in report.recommendations[:3]:
                print(f"  • {rec}")
                
    except Exception as e:
        print(f"❌ Policy validation failed: {e}")
        return False
    
    return len([v for v in report.violations if v.severity == 'critical']) == 0

if __name__ == "__main__":
    demonstrate_local_usage()
```

Denna omfattande Terraform policy implementation demonstrerar hur svenska organisationer kan implementera robust governance för Infrastructure as Code samtidigt som de bibehåller utvecklingsvelocitet och operational efficiency.

## Automatiserad Compliance Monitoring - Kontinuerlig övervakning och rapportering

Kontinuerlig compliance monitoring representerar ett paradigmskifte från traditionella punkt-i-tid audits till real-time övervakning av säkerhets- och compliance-posture. För svenska organisationer, som måste demonstrera ongoing compliance med GDPR, MSB-säkerhetskrav och andra regelverk, är denna capability kritisk för att upprätthålla regulatoriskt förtroende och operationell excellens.

### Arkitektur för kontinuerlig compliance monitoring

**Event-driven compliance**: Modern compliance monitoring bygger på event-driven arkitekturer där infrastrukturändringar automatiskt triggar compliance-evaluations. Detta möjliggör nästan omedelbar detection av compliance-avvikelser snarare än att vänta på periodiska scans.

**Multi-source data integration**: Effective compliance monitoring integrerar data från multiple källor - Infrastructure as Code deployments, runtime infrastructure state, application logs, user activities och external threat intelligence. Denna holistiska approach ger comprehensive visibility into organisationens compliance-posture.

**Risk-based alerting**: Intelligent alerting systems prioriterar compliance-violations baserat på risk severity, regulatory impact och business context. Detta förhindrar alert fatigue samtidigt som det säkerställer att kritiska issues får omedelbar uppmärksamhet.

### Omfattande implementation av compliance monitoring

```python
# advanced_compliance_monitoring.py
import asyncio
import json
import logging
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import boto3
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from concurrent.futures import ThreadPoolExecutor
import aiohttp
import websockets

class ComplianceFramework(Enum):
    GDPR = "GDPR"
    MSB = "MSB Säkerhetskrav"
    ISO27001 = "ISO 27001"
    PCI_DSS = "PCI DSS"
    SOC2 = "SOC 2"
    INTERNAL = "Internal Policies"

class ViolationSeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class ComplianceViolation:
    """Representation av en compliance violation"""
    violation_id: str
    timestamp: datetime
    framework: ComplianceFramework
    control_id: str
    resource_id: str
    resource_type: str
    severity: ViolationSeverity
    description: str
    evidence: Dict[str, Any]
    remediation_steps: List[str]
    auto_remediation_available: bool = False
    business_impact: str = ""
    regulatory_impact: str = ""
    
@dataclass 
class ComplianceMetrics:
    """Compliance metrics för reporting"""
    framework: ComplianceFramework
    total_controls: int
    compliant_controls: int
    violations_by_severity: Dict[ViolationSeverity, int]
    compliance_score: float
    trend_direction: str  # "improving", "declining", "stable"
    last_assessment: datetime

class SwedishComplianceMonitor:
    """
    Advanced compliance monitoring system för svenska organisationer
    """
    
    def __init__(self, config_path: str = "compliance_config.yaml"):
        self.config = self._load_config(config_path)
        self.aws_clients = self._initialize_aws_clients()
        self.violation_handlers = self._initialize_violation_handlers()
        self.metrics_collector = ComplianceMetricsCollector()
        self.remediation_engine = AutoRemediationEngine(self.aws_clients)
        self.notification_service = NotificationService(self.config)
        self.logger = self._setup_logging()
        
        # Real-time monitoring components
        self.event_processor = ComplianceEventProcessor()
        self.risk_assessor = ComplianceRiskAssessor()
        
    async def start_continuous_monitoring(self):
        """Starta kontinuerlig compliance monitoring"""
        self.logger.info("Startar kontinuerlig compliance monitoring...")
        
        # Starta parallel monitoring tasks
        tasks = [
            self.monitor_infrastructure_changes(),
            self.monitor_policy_violations(),
            self.monitor_user_activities(),
            self.generate_periodic_reports(),
            self.process_compliance_events()
        ]
        
        await asyncio.gather(*tasks)
    
    async def monitor_infrastructure_changes(self):
        """Monitor infrastructure changes för compliance impact"""
        while True:
            try:
                # Poll CloudTrail för infrastructure changes
                events = await self._get_infrastructure_events()
                
                for event in events:
                    # Evaluera compliance impact för varje change
                    violations = await self._evaluate_change_compliance(event)
                    
                    if violations:
                        await self._process_violations(violations)
                
                await asyncio.sleep(30)  # Poll var 30:e sekund
                
            except Exception as e:
                self.logger.error(f"Error i infrastructure monitoring: {e}")
                await asyncio.sleep(60)
    
    async def monitor_policy_violations(self):
        """Monitor för nya policy violations"""
        while True:
            try:
                # Scan alla resurser för policy compliance
                resources = await self._discover_resources()
                
                for resource in resources:
                    violations = await self._check_resource_compliance(resource)
                    
                    if violations:
                        await self._process_violations(violations)
                
                await asyncio.sleep(300)  # Full scan var 5:e minut
                
            except Exception as e:
                self.logger.error(f"Error i policy monitoring: {e}")
                await asyncio.sleep(120)
    
    async def _evaluate_change_compliance(self, infrastructure_event: Dict) -> List[ComplianceViolation]:
        """Evaluera compliance impact av infrastructure change"""
        violations = []
        
        resource_type = infrastructure_event.get('eventName', '')
        resource_id = infrastructure_event.get('resources', [{}])[0].get('ARN', '')
        event_time = datetime.fromisoformat(infrastructure_event.get('eventTime', ''))
        
        # GDPR evaluation för databas-ändringar
        if 'RDS' in resource_type or 'DynamoDB' in resource_type:
            gdpr_violations = await self._evaluate_gdpr_database_compliance(
                infrastructure_event
            )
            violations.extend(gdpr_violations)
        
        # MSB evaluation för nätverks-ändringar
        if 'SecurityGroup' in resource_type or 'VPC' in resource_type:
            msb_violations = await self._evaluate_msb_network_compliance(
                infrastructure_event
            )
            violations.extend(msb_violations)
        
        # Datasuveränitet evaluation
        sovereignty_violations = await self._evaluate_data_sovereignty_compliance(
            infrastructure_event
        )
        violations.extend(sovereignty_violations)
        
        return violations
    
    async def _evaluate_gdpr_database_compliance(self, event: Dict) -> List[ComplianceViolation]:
        """Evaluera GDPR compliance för databas-operationer"""
        violations = []
        
        if event.get('eventName') == 'CreateDBInstance':
            # Kontrollera om ny RDS instance har encryption
            request_params = event.get('requestParameters', {})
            
            if not request_params.get('storageEncrypted', False):
                violations.append(ComplianceViolation(
                    violation_id=f"gdpr-rds-encryption-{datetime.now().timestamp()}",
                    timestamp=datetime.now(),
                    framework=ComplianceFramework.GDPR,
                    control_id="GDPR-Art-32-1-a",
                    resource_id=request_params.get('dBInstanceIdentifier', ''),
                    resource_type="aws_rds_instance",
                    severity=ViolationSeverity.HIGH,
                    description="RDS instance skapad utan encryption - GDPR Artikel 32 violation",
                    evidence={
                        "event_name": event.get('eventName'),
                        "storage_encrypted": request_params.get('storageEncrypted'),
                        "db_instance_class": request_params.get('dBInstanceClass'),
                        "cloudtrail_event_id": event.get('eventID')
                    },
                    remediation_steps=[
                        "Stoppa RDS instance",
                        "Skapa snapshot av data",
                        "Skapa ny encrypted RDS instance från snapshot",
                        "Uppdatera applikationskonfiguration",
                        "Ta bort unencrypted instance"
                    ],
                    auto_remediation_available=False,
                    business_impact="Medium - Kräver planned downtime för remediation",
                    regulatory_impact="High - GDPR Article 32 non-compliance"
                ))
        
        return violations
    
    async def _evaluate_msb_network_compliance(self, event: Dict) -> List[ComplianceViolation]:
        """Evaluera MSB compliance för nätverks-ändringar"""
        violations = []
        
        if event.get('eventName') == 'AuthorizeSecurityGroupIngress':
            request_params = event.get('requestParameters', {})
            ip_permissions = request_params.get('ipPermissions', [])
            
            for permission in ip_permissions:
                # Kontrollera för overly permissive rules
                cidr_blocks = [
                    range_info.get('cidrIp') 
                    for range_info in permission.get('ipRanges', [])
                ]
                
                if '0.0.0.0/0' in cidr_blocks:
                    from_port = permission.get('fromPort', 0)
                    
                    # Endast HTTP/HTTPS tillåtet från internet
                    if from_port not in [80, 443]:
                        violations.append(ComplianceViolation(
                            violation_id=f"msb-network-{datetime.now().timestamp()}",
                            timestamp=datetime.now(),
                            framework=ComplianceFramework.MSB,
                            control_id="MSB-NS-1",
                            resource_id=request_params.get('groupId', ''),
                            resource_type="aws_security_group",
                            severity=ViolationSeverity.CRITICAL,
                            description=f"Security group regel exponerar port {from_port} mot internet",
                            evidence={
                                "event_name": event.get('eventName'),
                                "exposed_port": from_port,
                                "cidr_blocks": cidr_blocks,
                                "protocol": permission.get('ipProtocol'),
                                "security_group_id": request_params.get('groupId')
                            },
                            remediation_steps=[
                                f"Revoke overly permissive rule för port {from_port}",
                                "Skapa specifika CIDR blocks för legitimate access",
                                "Implementera VPN eller bastion host för admin access",
                                "Review och dokumentera business justification"
                            ],
                            auto_remediation_available=True,
                            business_impact="Low - Kan åtgärdas utan downtime",
                            regulatory_impact="High - MSB säkerhetskrav non-compliance"
                        ))
        
        return violations
    
    def create_compliance_dashboard(self) -> None:
        """Skapa interaktiv compliance dashboard med Streamlit"""
        st.set_page_config(
            page_title="Svenska Compliance Dashboard",
            page_icon="🇸🇪",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        st.title("🇸🇪 Svenska Säkerhets- och Compliance Dashboard")
        st.subheader("Real-time Infrastructure as Code Compliance Monitoring")
        
        # Sidebar för filter och configuration
        with st.sidebar:
            st.header("🔧 Konfiguration")
            
            selected_frameworks = st.multiselect(
                "Compliance Frameworks",
                [framework.value for framework in ComplianceFramework],
                default=[ComplianceFramework.GDPR.value, ComplianceFramework.MSB.value]
            )
            
            time_range = st.selectbox(
                "Tidsperiod",
                ["Senaste 24 timmarna", "Senaste veckan", "Senaste månaden", "Senaste kvartalet"]
            )
            
            severity_filter = st.multiselect(
                "Severity Filter",
                [severity.value for severity in ViolationSeverity],
                default=[ViolationSeverity.CRITICAL.value, ViolationSeverity.HIGH.value]
            )
            
            auto_refresh = st.checkbox("Auto-refresh (30s)", value=True)
        
        # Main dashboard content
        self._render_compliance_overview()
        self._render_violations_timeline()
        
        col1, col2 = st.columns(2)
        with col1:
            self._render_framework_compliance()
        with col2:
            self._render_risk_assessment()
        
        self._render_recent_violations()
        self._render_remediation_recommendations()
        
        # Auto-refresh functionality
        if auto_refresh:
            time.sleep(30)
            st.experimental_rerun()
    
    def _render_compliance_overview(self):
        """Render overview metrics"""
        st.subheader("📊 Compliance Overview")
        
        # Hämta aktuella metrics
        metrics = self.metrics_collector.get_current_metrics()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            overall_score = self._calculate_overall_score(metrics)
            delta_score = self._calculate_score_change(metrics)
            st.metric(
                "Overall Compliance",
                f"{overall_score:.1f}%",
                delta=f"{delta_score:+.1f}%"
            )
        
        with col2:
            critical_violations = sum(
                m.violations_by_severity.get(ViolationSeverity.CRITICAL, 0)
                for m in metrics
            )
            st.metric(
                "Critical Violations",
                critical_violations,
                delta=-2  # Förbättring från förra veckan
            )
        
        with col3:
            gdpr_metrics = next((m for m in metrics if m.framework == ComplianceFramework.GDPR), None)
            gdpr_score = gdpr_metrics.compliance_score if gdpr_metrics else 0
            st.metric(
                "GDPR Compliance",
                f"{gdpr_score:.1f}%",
                delta="+1.2%"
            )
        
        with col4:
            msb_metrics = next((m for m in metrics if m.framework == ComplianceFramework.MSB), None)
            msb_score = msb_metrics.compliance_score if msb_metrics else 0
            st.metric(
                "MSB Compliance", 
                f"{msb_score:.1f}%",
                delta="+0.8%"
            )
    
    def _render_violations_timeline(self):
        """Render violations timeline chart"""
        st.subheader("📈 Violations Timeline")
        
        # Generera timeline data
        timeline_data = self._get_violations_timeline_data()
        df = pd.DataFrame(timeline_data)
        
        if not df.empty:
            fig = px.line(
                df,
                x='date',
                y='count',
                color='severity',
                title="Policy Violations Over Time",
                labels={'count': 'Number of Violations', 'date': 'Date'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Inga violations de senaste dagarna! 🎉")
    
    def _render_framework_compliance(self):
        """Render compliance by framework"""
        st.subheader("🏛️ Compliance by Framework")
        
        framework_data = self._get_framework_compliance_data()
        df = pd.DataFrame(framework_data)
        
        if not df.empty:
            fig = px.bar(
                df,
                x='framework',
                y='compliance_score',
                color='compliance_score',
                color_continuous_scale='RdYlGn',
                title="Framework Compliance Scores",
                labels={'compliance_score': 'Compliance Score (%)', 'framework': 'Framework'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    def _render_risk_assessment(self):
        """Render risk assessment"""
        st.subheader("⚡ Risk Assessment")
        
        risk_data = self.risk_assessor.get_current_risk_profile()
        
        # Risk score gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=risk_data['overall_risk_score'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Overall Risk Score"},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkred"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgreen"},
                    {'range': [50, 80], 'color': "yellow"},
                    {'range': [80, 100], 'color': "lightcoral"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_recent_violations(self):
        """Render table of recent violations"""
        st.subheader("🚨 Recent Violations")
        
        recent_violations = self._get_recent_violations()
        
        if recent_violations:
            df = pd.DataFrame([
                {
                    'Time': v.timestamp.strftime('%Y-%m-%d %H:%M'),
                    'Framework': v.framework.value,
                    'Severity': v.severity.value,
                    'Resource': v.resource_id,
                    'Description': v.description[:80] + '...' if len(v.description) > 80 else v.description,
                    'Auto-Remediation': '✅' if v.auto_remediation_available else '❌'
                }
                for v in recent_violations[:10]
            ])
            
            st.dataframe(
                df,
                use_container_width=True,
                column_config={
                    "Severity": st.column_config.SelectboxColumn(
                        "Severity",
                        options=["critical", "high", "medium", "low"]
                    )
                }
            )
        else:
            st.info("Inga nya violations de senaste 24 timmarna!")
    
    def _render_remediation_recommendations(self):
        """Render automated remediation recommendations"""
        st.subheader("🔧 Automated Remediation")
        
        recommendations = self.remediation_engine.get_available_remediations()
        
        for i, rec in enumerate(recommendations[:5]):
            with st.expander(f"🔧 {rec['title']} (Risk: {rec['risk_level']})"):
                st.write(f"**Description:** {rec['description']}")
                st.write(f"**Estimated Time:** {rec['estimated_time']}")
                st.write(f"**Prerequisites:** {', '.join(rec['prerequisites'])}")
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.code(rec['automation_script'], language='bash')
                with col2:
                    if st.button(f"Apply Fix", key=f"remediation_{i}"):
                        with st.spinner("Applying remediation..."):
                            result = self.remediation_engine.apply_remediation(rec['id'])
                            if result['success']:
                                st.success("✅ Remediation applied successfully!")
                            else:
                                st.error(f"❌ Remediation failed: {result['error']}")

class ComplianceMetricsCollector:
    """Samlar och aggregerar compliance metrics"""
    
    def get_current_metrics(self) -> List[ComplianceMetrics]:
        """Hämta aktuella compliance metrics"""
        # I verklig implementation skulle detta hämta från databas/monitoring system
        return [
            ComplianceMetrics(
                framework=ComplianceFramework.GDPR,
                total_controls=50,
                compliant_controls=46,
                violations_by_severity={
                    ViolationSeverity.CRITICAL: 0,
                    ViolationSeverity.HIGH: 2,
                    ViolationSeverity.MEDIUM: 2,
                    ViolationSeverity.LOW: 0
                },
                compliance_score=92.0,
                trend_direction="improving",
                last_assessment=datetime.now()
            ),
            ComplianceMetrics(
                framework=ComplianceFramework.MSB,
                total_controls=30,
                compliant_controls=27,
                violations_by_severity={
                    ViolationSeverity.CRITICAL: 1,
                    ViolationSeverity.HIGH: 1,
                    ViolationSeverity.MEDIUM: 1,
                    ViolationSeverity.LOW: 0
                },
                compliance_score=90.0,
                trend_direction="stable",
                last_assessment=datetime.now()
            )
        ]

class AutoRemediationEngine:
    """Automated remediation engine för common compliance violations"""
    
    def __init__(self, aws_clients: Dict):
        self.aws_clients = aws_clients
    
    def get_available_remediations(self) -> List[Dict]:
        """Hämta tillgängliga automated remediations"""
        return [
            {
                'id': 'encrypt_unencrypted_s3',
                'title': 'Enable S3 Bucket Encryption',
                'description': 'Automatically enable default encryption för unencrypted S3 buckets',
                'risk_level': 'Low',
                'estimated_time': '5 minutes',
                'prerequisites': ['S3 full access', 'KMS key available'],
                'automation_script': """
aws s3api put-bucket-encryption \\
    --bucket $BUCKET_NAME \\
    --server-side-encryption-configuration '{
        "Rules": [{
            "ApplyServerSideEncryptionByDefault": {
                "SSEAlgorithm": "aws:kms",
                "KMSMasterKeyID": "$KMS_KEY_ID"
            }
        }]
    }'
                """
            },
            {
                'id': 'restrict_sg_rules',
                'title': 'Restrict Security Group Rules',
                'description': 'Remove overly permissive security group rules',
                'risk_level': 'Medium',
                'estimated_time': '2 minutes',
                'prerequisites': ['EC2 full access', 'Business approval'],
                'automation_script': """
aws ec2 revoke-security-group-ingress \\
    --group-id $SG_ID \\
    --protocol tcp \\
    --port $PORT \\
    --cidr 0.0.0.0/0
                """
            }
        ]
    
    def apply_remediation(self, remediation_id: str) -> Dict[str, Any]:
        """Apply specific remediation"""
        # I verklig implementation skulle detta köra actual remediation
        return {
            'success': True,
            'message': f'Remediation {remediation_id} applied successfully',
            'timestamp': datetime.now().isoformat()
        }

# Main function för att starta compliance monitoring
async def main():
    monitor = SwedishComplianceMonitor()
    
    # Starta dashboard i separata thread
    dashboard_thread = threading.Thread(
        target=monitor.create_compliance_dashboard
    )
    dashboard_thread.start()
    
    # Starta continuous monitoring
    await monitor.start_continuous_monitoring()

if __name__ == "__main__":
    import threading
    asyncio.run(main())
```

Denna omfattande compliance monitoring implementation demonstrerar hur svenska organisationer kan implementera proaktiv, kontinuerlig övervakning av sin Infrastructure as Code compliance-posture med automatiska remediations och comprehensive reporting capabilities.

## Praktiska implementationsexempel och best practices

Framgångsrik implementation av Policy as Code kräver mer än bara tekniska verktyg - det krävs en genomtänkt strategi som integrerar organisatoriska processer, tekniska capabilities och regulatoriska krav. Detta avsnitt presenterar praktiska implementationsexempel från svenska organisationer som framgångsrikt har implementerat comprehensive Policy as Code-lösningar.

### Enterprise-grade implementationsstrategi

**Phased implementation approach**: Successful Policy as Code implementations följer en phased approach som börjar med less critical environments och gradvis expanderar till production systems. Detta möjliggör organisationer att bygga kompetens och förtroende innan kritiska systems påverkas.

**Policy lifecycle management**: Enterprise implementations kräver robust lifecycle management för policies inklusive development, testing, approval, deployment och retirement av policies. Detta säkerställer att policy-ändringar genomgår samma rigor som code-ändringar.

**Cross-functional collaboration**: Policy as Code-projekt kräver tight collaboration mellan security teams, compliance officers, infrastructure engineers och development teams. Successful implementations etablerar clear roles, responsibilities och communication channels mellan dessa stakeholders.

### Comprehensive implementation exempel för svensk finansorganisation

```python
# enterprise_policy_implementation.py
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import yaml
import json
import asyncio
from pathlib import Path

@dataclass
class PolicyImplementationPhase:
    """Representation av implementation phase"""
    phase_name: str
    duration_weeks: int
    environments: List[str]
    policy_categories: List[str]
    success_criteria: List[str]
    risk_level: str

class SwedishFinancialPolicyImplementation:
    """
    Comprehensive Policy as Code implementation för svensk finansorganisation
    """
    
    def __init__(self, organization_config: str):
        self.config = self._load_organization_config(organization_config)
        self.implementation_phases = self._define_implementation_phases()
        self.policy_catalog = self._initialize_policy_catalog()
        self.compliance_frameworks = [
            "GDPR", "PCI-DSS", "Basel III", "MiFID II", "Swedish Banking Act"
        ]
    
    def _define_implementation_phases(self) -> List[PolicyImplementationPhase]:
        """Definiera phased implementation strategy"""
        return [
            PolicyImplementationPhase(
                phase_name="Foundation Setup",
                duration_weeks=4,
                environments=["development"],
                policy_categories=["basic_security", "resource_tagging"],
                success_criteria=[
                    "OPA och Gatekeeper deployment komplett",
                    "Grundläggande policies implementerade",
                    "Developer training genomförd",
                    "CI/CD integration fungerande"
                ],
                risk_level="low"
            ),
            PolicyImplementationPhase(
                phase_name="GDPR Compliance Implementation",
                duration_weeks=6,
                environments=["development", "staging"],
                policy_categories=["data_protection", "encryption", "data_sovereignty"],
                success_criteria=[
                    "Alla GDPR-policies implementerade",
                    "Automated evidence collection fungerande",
                    "Data mapping komplett",
                    "Privacy impact assessments integrerade"
                ],
                risk_level="medium"
            ),
            PolicyImplementationPhase(
                phase_name="PCI-DSS och Financial Regulations",
                duration_weeks=8,
                environments=["development", "staging", "pre-production"],
                policy_categories=["payment_security", "network_segmentation", "access_control"],
                success_criteria=[
                    "PCI-DSS Level 1 compliance policies implementerade",
                    "Cardholder data environment isolation",
                    "Quarterly compliance reporting automatiserad",
                    "Incident response procedures integrerade"
                ],
                risk_level="high"
            ),
            PolicyImplementationPhase(
                phase_name="Production Deployment och Advanced Monitoring",
                duration_weeks=6,
                environments=["production"],
                policy_categories=["all_policies", "advanced_monitoring", "automated_remediation"],
                success_criteria=[
                    "100% policy coverage i produktion",
                    "Real-time compliance monitoring",
                    "Automated remediation för låg-risk violations",
                    "Integration med SIEM systems"
                ],
                risk_level="critical"
            ),
            PolicyImplementationPhase(
                phase_name="Optimization och Continuous Improvement",
                duration_weeks=4,
                environments=["all"],
                policy_categories=["performance_optimization", "advanced_analytics"],
                success_criteria=[
                    "Policy performance optimerad",
                    "Advanced analytics implementerade",
                    "Predictive compliance modeling",
                    "Continuous improvement process etablerad"
                ],
                risk_level="low"
            )
        ]
    
    def generate_implementation_plan(self) -> Dict[str, Any]:
        """Generera detaljerad implementation plan"""
        total_duration = sum(phase.duration_weeks for phase in self.implementation_phases)
        
        plan = {
            "organization": self.config.get("organization_name"),
            "total_duration_weeks": total_duration,
            "total_duration_months": total_duration / 4.33,
            "compliance_frameworks": self.compliance_frameworks,
            "phases": []
        }
        
        current_week = 0
        for phase in self.implementation_phases:
            phase_detail = {
                "phase_name": phase.phase_name,
                "start_week": current_week + 1,
                "end_week": current_week + phase.duration_weeks,
                "duration_weeks": phase.duration_weeks,
                "environments": phase.environments,
                "policy_categories": phase.policy_categories,
                "success_criteria": phase.success_criteria,
                "risk_level": phase.risk_level,
                "deliverables": self._generate_phase_deliverables(phase),
                "resources_required": self._calculate_phase_resources(phase),
                "dependencies": self._identify_phase_dependencies(phase)
            }
            plan["phases"].append(phase_detail)
            current_week += phase.duration_weeks
        
        return plan
    
    def _generate_phase_deliverables(self, phase: PolicyImplementationPhase) -> List[Dict[str, str]]:
        """Generera deliverables för specific phase"""
        deliverables = []
        
        if "basic_security" in phase.policy_categories:
            deliverables.extend([
                {
                    "name": "Basic Security Policy Catalog",
                    "description": "Grundläggande säkerhetspolicies för infrastructure",
                    "format": "OPA Rego policies"
                },
                {
                    "name": "Gatekeeper Constraint Templates",
                    "description": "Kubernetes admission control templates",
                    "format": "YAML configuration files"
                }
            ])
        
        if "data_protection" in phase.policy_categories:
            deliverables.extend([
                {
                    "name": "GDPR Compliance Policy Suite",
                    "description": "Comprehensive policies för GDPR Article 32 compliance",
                    "format": "OPA Rego + OSCAL mappings"
                },
                {
                    "name": "Data Classification Automation",
                    "description": "Automated data discovery and classification",
                    "format": "Python scripts + Terraform modules"
                }
            ])
        
        if "payment_security" in phase.policy_categories:
            deliverables.extend([
                {
                    "name": "PCI-DSS Policy Implementation",
                    "description": "Complete PCI-DSS requirement coverage",
                    "format": "Multi-layer policy stack"
                },
                {
                    "name": "Cardholder Data Environment Controls",
                    "description": "Specialized policies för payment processing",
                    "format": "Infrastructure and application policies"
                }
            ])
        
        return deliverables
    
    def _calculate_phase_resources(self, phase: PolicyImplementationPhase) -> Dict[str, Any]:
        """Beräkna resource requirements för phase"""
        base_team_size = 3  # Minimum team size
        
        # Adjust team size based on phase complexity
        complexity_multiplier = {
            "low": 1.0,
            "medium": 1.5, 
            "high": 2.0,
            "critical": 2.5
        }
        
        adjusted_team_size = int(base_team_size * complexity_multiplier.get(phase.risk_level, 1.0))
        
        return {
            "team_size": adjusted_team_size,
            "roles_required": [
                "Policy Engineer/Developer",
                "Security Architect", 
                "Compliance Specialist",
                "Infrastructure Engineer",
                "DevOps Engineer" if phase.risk_level in ["high", "critical"] else None
            ],
            "external_consultants": phase.risk_level in ["high", "critical"],
            "training_days": phase.duration_weeks * 2,  # 2 dagar per vecka för training
            "estimated_cost_sek": adjusted_team_size * phase.duration_weeks * 50000  # 50k SEK per person-week
        }
    
    def generate_policy_testing_framework(self) -> str:
        """Generera comprehensive testing framework för policies"""
        return '''
# Policy Testing Framework för svenska finansorganisationer

## Test Categories

### 1. Unit Tests för Individual Policies
- Validera enskilda policy rules mot known good/bad inputs
- Test edge cases och boundary conditions
- Verify correct error messages och remediation guidance

### 2. Integration Tests
- Test policy interactions mellan olika frameworks
- Validate cross-policy dependencies
- Test performance under load

### 3. Compliance Tests
- Automated validation mot regulatory requirements
- Test evidence collection och audit trail generation
- Validate reporting accuracy

### 4. Regression Tests
- Ensure policy updates don't break existing functionality
- Test backward compatibility
- Validate migration scripts

## Test Implementation

```python
# tests/test_gdpr_policies.py
import pytest
from opa_client import OPAClient
import json

class TestGDPRPolicies:
    
    @pytest.fixture
    def opa_client(self):
        return OPAClient(url="http://localhost:8181")
    
    def test_encryption_required_for_personal_data(self, opa_client):
        # Test data: RDS instance med persondata utan kryptering
        test_input = {
            "resource_type": "aws_rds_instance",
            "resource_attributes": {
                "storage_encrypted": False,
                "tags": {
                    "DataClassification": "personal"
                }
            }
        }
        
        result = opa_client.evaluate_policy(
            "sweden.compliance.gdpr",
            test_input
        )
        
        assert result["violations"]
        assert any(
            v["type"] == "encryption_required" 
            for v in result["violations"]
        )
    
    def test_compliant_encrypted_rds(self, opa_client):
        # Test data: Korrekt konfigurerad RDS med kryptering
        test_input = {
            "resource_type": "aws_rds_instance", 
            "resource_attributes": {
                "storage_encrypted": True,
                "kms_key_id": "arn:aws:kms:eu-north-1:123:key/456",
                "tags": {
                    "DataClassification": "personal"
                }
            }
        }
        
        result = opa_client.evaluate_policy(
            "sweden.compliance.gdpr",
            test_input
        )
        
        assert not result["violations"]
    
    @pytest.mark.parametrize("data_classification", [
        "personal", "sensitive", "pii", "gdpr-protected"
    ])
    def test_encryption_various_classifications(self, opa_client, data_classification):
        test_input = {
            "resource_type": "aws_s3_bucket",
            "resource_attributes": {
                "server_side_encryption_configuration": [],
                "tags": {
                    "DataClassification": data_classification
                }
            }
        }
        
        result = opa_client.evaluate_policy(
            "sweden.compliance.gdpr",
            test_input
        )
        
        assert result["violations"]

class TestPCIDSSPolicies:
    
    def test_cardholder_data_environment_isolation(self, opa_client):
        # Test att cardholder data environment är properly isolated
        test_input = {
            "resource_type": "aws_security_group",
            "resource_attributes": {
                "ingress": [{
                    "from_port": 3306,
                    "to_port": 3306,
                    "protocol": "tcp",
                    "cidr_blocks": ["0.0.0.0/0"]
                }],
                "tags": {
                    "Environment": "cardholder-data",
                    "PCIScope": "true"
                }
            }
        }
        
        result = opa_client.evaluate_policy(
            "sweden.compliance.pci_dss",
            test_input
        )
        
        assert result["violations"]
        assert any(
            v["type"] == "pci_network_isolation_violation"
            for v in result["violations"]
        )

## Performance Tests

class TestPolicyPerformance:
    
    def test_policy_evaluation_latency(self, opa_client):
        # Test att policy evaluation sker inom acceptable latency
        import time
        
        test_input = self._generate_large_test_input()
        
        start_time = time.time()
        result = opa_client.evaluate_policy("sweden.compliance", test_input)
        end_time = time.time()
        
        latency_ms = (end_time - start_time) * 1000
        
        # Assert latency under 100ms för standard evaluation
        assert latency_ms < 100
    
    def test_bulk_evaluation_performance(self, opa_client):
        # Test bulk evaluation performance
        test_inputs = [
            self._generate_test_input() for _ in range(1000)
        ]
        
        start_time = time.time()
        results = opa_client.bulk_evaluate(
            "sweden.compliance", 
            test_inputs
        )
        end_time = time.time()
        
        total_time = end_time - start_time
        per_resource_time = total_time / len(test_inputs)
        
        # Assert under 10ms per resource för bulk evaluation
        assert per_resource_time < 0.01

## Integration med CI/CD

# .github/workflows/policy-testing.yml
name: Policy Testing Pipeline

on:
  pull_request:
    paths: ['policies/**']
  push:
    branches: [main]

jobs:
  policy-unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install pytest opa-python-client
      
      - name: Start OPA server
        run: |
          wget https://github.com/open-policy-agent/opa/releases/download/v0.57.0/opa_linux_amd64
          chmod +x opa_linux_amd64
          ./opa_linux_amd64 run --server --log-level debug policies/ &
          sleep 5
      
      - name: Run policy unit tests
        run: |
          pytest tests/policies/ -v --junit-xml=test-results.xml
      
      - name: Upload test results
        uses: actions/upload-artifact@v3
        with:
          name: policy-test-results
          path: test-results.xml
  
  policy-compliance-tests:
    runs-on: ubuntu-latest
    needs: policy-unit-tests
    steps:
      - uses: actions/checkout@v4
      
      - name: Run compliance validation
        run: |
          python scripts/validate_compliance_coverage.py \\
            --policies-dir policies/ \\
            --frameworks GDPR,PCI-DSS,MSB \\
            --output compliance-report.json
      
      - name: Check compliance coverage
        run: |
          coverage=$(jq '.overall_coverage' compliance-report.json)
          if (( $(echo "$coverage < 95" | bc -l) )); then
            echo "Compliance coverage $coverage% är under required 95%"
            exit 1
          fi

## Automated Policy Documentation

class PolicyDocumentationGenerator:
    
    def generate_policy_documentation(self, policies_dir: str) -> str:
        """Generera automatisk dokumentation för alla policies"""
        
        documentation = """
# Policy Documentation

Detta dokument genereras automatiskt från policy definitions.

## GDPR Policies

### Encryption Requirements (GDPR Article 32)
- **Policy ID**: gdpr-encryption-required
- **Scope**: All resources handling personal data
- **Implementation**: Validates encryption configuration för databaser och storage
- **Remediation**: Enable appropriate encryption för affected resources

### Data Sovereignty (Swedish Data Protection Law)
- **Policy ID**: swedish-data-sovereignty  
- **Scope**: All resources storing Swedish personal data
- **Implementation**: Validates region placement för data storage
- **Remediation**: Move resources to approved EU/Swedish regions

## MSB Security Requirements

### Network Segmentation
- **Policy ID**: msb-network-segmentation
- **Scope**: All network security groups
- **Implementation**: Prevents overly permissive network rules
- **Remediation**: Restrict ingress rules till specific sources

### Critical Infrastructure Protection
- **Policy ID**: msb-critical-infrastructure
- **Scope**: Resources tagged as critical infrastructure
- **Implementation**: Enhanced security requirements för critical systems
- **Remediation**: Apply additional security controls

## PCI-DSS Policies

### Cardholder Data Environment
- **Policy ID**: pci-cde-isolation
- **Scope**: All resources i cardholder data environment
- **Implementation**: Strict isolation och access controls
- **Remediation**: Implement proper network segmentation

        """
        
        return documentation
```

Denna comprehensive testing framework säkerställer att policies fungerar korrekt, presterar väl och uppfyller alla regulatoriska krav innan de deployeras till produktion.'''

    def generate_organizational_change_management(self) -> Dict[str, Any]:
        """Generera change management strategy för Policy as Code adoption"""
        return {
            "stakeholder_engagement": {
                "executive_sponsors": [
                    "CTO/CIO för technical vision och budget",
                    "CISO för security leadership",
                    "Chief Compliance Officer för regulatory alignment",
                    "Chief Risk Officer för risk management"
                ],
                "working_groups": [
                    {
                        "name": "Policy Development Team",
                        "members": ["Security Engineers", "Platform Engineers", "Compliance Specialists"],
                        "responsibilities": ["Policy authoring", "Testing", "Documentation"]
                    },
                    {
                        "name": "Implementation Team", 
                        "members": ["DevOps Engineers", "Site Reliability Engineers", "Release Managers"],
                        "responsibilities": ["Deployment", "Monitoring", "Incident Response"]
                    },
                    {
                        "name": "Governance Committee",
                        "members": ["Legal", "Risk Management", "Business Representatives"],
                        "responsibilities": ["Policy approval", "Exception handling", "Audit liaison"]
                    }
                ]
            },
            "training_program": {
                "executive_briefings": "2-hour sessions on business value och ROI",
                "technical_training": "40-hour comprehensive program för engineers",
                "compliance_workshops": "16-hour regulatory mapping sessions",
                "developer_enablement": "Ongoing support och documentation"
            },
            "communication_strategy": {
                "launch_timeline": "6-month communication campaign",
                "key_messages": [
                    "Enhanced security through automation",
                    "Reduced compliance costs och effort", 
                    "Faster development with built-in guardrails",
                    "Better audit readiness och evidence collection"
                ],
                "success_metrics": [
                    "Policy adoption rate across teams",
                    "Reduction in manual compliance effort",
                    "Faster time-to-compliance för new services",
                    "Improved audit outcomes"
                ]
            }
        }

# Demonstration av complete implementation
def demonstrate_enterprise_implementation():
    """Demonstrera enterprise-grade Policy as Code implementation"""
    
    # Initiera implementation för financial organization
    impl = SwedishFinancialPolicyImplementation("config/financial_org.yaml")
    
    # Generera implementation plan
    plan = impl.generate_implementation_plan()
    
    print("🏦 Svenska Financial Organization - Policy as Code Implementation Plan")
    print("=" * 80)
    print(f"Total Duration: {plan['total_duration_months']:.1f} months")
    print(f"Compliance Frameworks: {', '.join(plan['compliance_frameworks'])}")
    print()
    
    for phase in plan['phases']:
        print(f"📅 Phase: {phase['phase_name']}")
        print(f"   Duration: Week {phase['start_week']}-{phase['end_week']} ({phase['duration_weeks']} weeks)")
        print(f"   Risk Level: {phase['risk_level'].upper()}")
        print(f"   Environments: {', '.join(phase['environments'])}")
        print(f"   Team Size: {phase['resources_required']['team_size']} people")
        print(f"   Estimated Cost: {phase['resources_required']['estimated_cost_sek']:,} SEK")
        print()
        
        print("   ✅ Success Criteria:")
        for criterion in phase['success_criteria']:
            print(f"      • {criterion}")
        print()
        
        print("   📦 Deliverables:")
        for deliverable in phase['deliverables']:
            print(f"      • {deliverable['name']}: {deliverable['description']}")
        print()
    
    # Generera organizational change management
    change_mgmt = impl.generate_organizational_change_management()
    
    print("🔄 Organizational Change Management Strategy")
    print("=" * 50)
    print("Executive Sponsors:")
    for sponsor in change_mgmt['stakeholder_engagement']['executive_sponsors']:
        print(f"  • {sponsor}")
    
    print("\nTraining Program:")
    for program, description in change_mgmt['training_program'].items():
        print(f"  • {program.replace('_', ' ').title()}: {description}")

if __name__ == "__main__":
    demonstrate_enterprise_implementation()
```

### Lessons learned och best practices från svenska implementationer

Baserat på erfarenheter från svenska organisationer som framgångsrikt implementerat Policy as Code, kan vi identifiera flera kritiska success factors:

**Start small, think big**: Successful implementations börjar med mindre, mindre kritiska systems och bygger upp expertise och confidence innan de tackles critical production environments.

**Invest in tooling och automation**: Organizations som investerar i robust tooling för policy development, testing och deployment ser dramatically better outcomes än de som försöker manage policies manually.

**Prioritize developer experience**: Policy as Code-system som är svåra att använda eller understand kommer att möta resistance från development teams. Successful implementations prioriterar user experience och comprehensive documentation.

**Establish clear governance**: Without clear governance processes för policy approval, exception handling och audit liaison, Policy as Code implementations kan bli bloated och ineffective.

**Measure and optimize continuously**: Regular assessment av policy effectiveness, performance impact och business value är critical för long-term success.

## Sammanfattning och framtidsperspektiv

Policy as Code representerar en fundamental transformation i hur organisationer närmar sig säkerhet, compliance och governance. För svenska organisationer, som måste navigera en komplex regulatorisk miljö samtidigt som de driver digital transformation, erbjuder Policy as Code unprecedented möjligheter för automation, consistency och efficiency.

Genom detta kapitel har vi utforskat de tekniska foundations för Policy as Code, inklusive Open Policy Agent och Rego, Kubernetes Gatekeeper, OSCAL-frameworks och comprehensive monitoring systems. Vi har också examinerät praktiska implementationsstrategier och enterprise-grade best practices som möjliggör organisations att framgångsrikt adopt Policy as Code.

### Kritiska takeaways för svenska organisationer

**Integration med svenska regelverk**: Policy as Code erbjuder unique opportunities för svenska organisationer att automate compliance med GDPR, MSB säkerhetskrav och andra lokala regleringar. Genom att kodifiera dessa requirements kan organisationer achieve both technical efficiency och regulatory compliance.

**OSCAL som game-changer**: Open Security Controls Assessment Language representerar next-generation approach till standardized security och compliance management. Svenska organisationer som early adopt OSCAL kommer att ha significant competitive advantages i compliance efficiency och audit readiness.

**Kubernetes och container security**: Som fler svenska organisationer move mot containerized architectures, blir Gatekeeper och Kubernetes policy enforcement critical capabilities för maintaining security och compliance i dynamic environments.

**Continuous monitoring och automation**: Traditional punkt-i-tid compliance assessments är insufficient för modern digital businesses. Continuous compliance monitoring och automated remediation capabilities är becoming table stakes för competitive organizations.

### Framtida utvecklingstrends

**AI-enhanced policy development**: Machine learning och AI technologies kommer increasingly att användas för automatic policy generation, optimization och predictive compliance modeling.

**Cross-cloud policy management**: Som multi-cloud strategies blir norm, kommer policy management tools att need sophisticated capabilities för managing policies across different cloud providers och environments.

**Regulatory technology (RegTech) integration**: Policy as Code kommer increasingly att integrate med specialized RegTech solutions för enhanced regulatory reporting och compliance automation.

**Zero-trust integration**: Policy as Code kommer att bli central component i zero-trust security architectures, med policies som define granular access controls och trust boundaries.

### Rekommendationer för nästa steg

För svenska organisationer som vill börja sin Policy as Code-journey, recommend vi följande approach:

1. **Start med pilot project**: Choose ett mindre kritiskt system eller environment för initial implementation
2. **Invest i training och capability building**: Build internal expertise i OPA, Rego och related technologies
3. **Establish governance frameworks**: Define clear processes för policy development, approval och lifecycle management
4. **Focus på measurement**: Implement metrics och monitoring för att track policy effectiveness och business impact
5. **Plan för scale**: Design initial implementations med future scale och complexity i mind

Policy as Code representerar inte bara en technical capability utan en strategic advantage för organisationer som can successfully implement det. Svenska organisationer som invest i Policy as Code today kommer att be well-positioned för future regulatory challenges och digital transformation opportunities.

Integration med nästa kapitels diskussion om [compliance och regelefterlevnad](12_compliance.md) bygger vidare på dessa Policy as Code foundations för att address broader organizational och strategic aspects av comprehensive governance strategy.

## Källor och referenser

- Open Policy Agent. "Policy as Code Documentation." OPA Community, 2024.
- Kubernetes SIG Security. "Gatekeeper Policy Engine." CNCF Projects, 2024.  
- HashiCorp. "Sentinel Policy Framework." HashiCorp Enterprise, 2024.
- NIST. "Security and Privacy Controls för Information Systems." NIST Special Publication 800-53, 2024.
- NIST. "Open Security Controls Assessment Language (OSCAL)." NIST Computer Security Resource Center, 2024.
- European Union. "General Data Protection Regulation Implementation Guide." EU Publications, 2024.
- MSB. "Säkerhetskrav för kritisk infrastruktur." Myndigheten för samhällsskydd och beredskap, 2024.
- Finansinspektionen. "IT-säkerhet inom finansiella företag." Finansinspektionen, 2024.
- AWS. "AWS Config Rules och Policy as Code Best Practices." Amazon Web Services, 2024.
- Microsoft. "Azure Policy och Governance Frameworks." Microsoft Azure, 2024.
- Google Cloud. "Policy Intelligence och Compliance Automation." Google Cloud Platform, 2024.