# Policy och säkerhet som kod i detalj

![Policy och säkerhet som kod](images/diagram_12_kapitel11.png)

*Policy as Code representerar nästa evolutionssteg inom Infrastructure as Code där säkerhet, compliance och governance automatiseras genom programmerbara regler. Diagrammet visar integreringen av policy enforcement i hela utvecklingslivscykeln från design till produktion.*

## Introduktion och kontextualisering

I en värld där svenska organisationer hanterar allt mer komplexa digitala infrastrukturer samtidigt som regulatoriska krav skärps kontinuerligt, har Policy as Code (PaC) framträtt som en oumbärlig disciplin inom Infrastructure as Code. Medan [kapitel 10 om säkerhet](10_sakerhet.md) introducerade grundläggande säkerhetsprinciper, tar detta kapitel ett djupt dyk i den avancerade implementeringen av policy-drivna säkerhetslösningar och introducerar läsaren till Open Security Controls Assessment Language (OSCAL) - en revolutionerande standard för säkerhetshantering.

Det traditionella paradigmet för säkerhets- och compliance-hantering kännetecknas av manuella processer, statiska dokumentation och reaktiva strategier. Denna approach skapar flaskhalsar i moderna utvecklingscykler där infrastrukturändringar sker flera gånger dagligen genom automated CI/CD-pipelines. Svenska organisationer, som traditionellt varit föregångare inom säkerhet och regelefterlevnad, står nu inför utmaningen att digitalisera och automatisera dessa processer utan att kompromissa med säkerhetsnivån.

Policy as Code adresserar denna utmaning genom att transformera säkerhet från en extern kontrollmekanism till en integrerad del av utvecklingsprocessen. Genom att uttrycka säkerhetskrav, compliance-regler och governance-policies som kod uppnås samma fördelar som Infrastructure as Code erbjuder: versionskontroll, testbarhet, återanvändbarhet, och konsistent deployment över miljöer och team.

I den svenska kontexten möter organisationer en komplex regulatorisk miljö som inkluderar EU:s allmänna dataskyddsförordning (GDPR), Myndigheten för samhällsskydd och beredskaps (MSB) säkerhetskrav för kritisk infrastruktur, NIS2-direktivet, och branschspecifika regleringar inom finansiella tjänster, vård och offentlig sektor. Traditionella compliance-approaches baserade på manuella kontroller och dokumentbaserade policies är inte bara ineffektiva utan också riskfyllda i dynamiska molnmiljöer.

Detta kapitel utforskar hur Policy as Code, förstärkt med OSCAL-standarder, möjliggör för svenska organisationer att uppnå unprecedented nivåer av säkerhetsautomatisering och compliance-övervakning. Vi kommer att undersöka verkliga implementationspattern, analysera case studies från svenska organisationer, och ge läsaren konkreta verktyg för att implementera enterprise-grade policy management.

## Evolutionen av säkerhetshantering inom Infrastructure as Code

Säkerhetshantering inom Infrastructure as Code har genomgått en betydande evolution från ad-hoc skript och manuella checklistor till sofistikerade policy engines och automated compliance frameworks. Denna evolution kan delas in i fyra distinkta faser, var och en med sina egna karakteristiska utmaningar och möjligheter.

**Fas 1: Manual Säkerhetsvalidering (2010-2015)**

I infrastrukturens barndom utfördes säkerhetsvalidering primärt genom manuella processer. Säkerhetsteam granskade infrastrukturkonfigurationer efter deployment, ofta veckор eller månader efter att resurserna blev produktiva. Denna reaktiva approach ledde till upptäckten av säkerhetsproblem långt efter att de kunde orsaka skada. Svenska organisationer, med sina strikta säkerhetskrav, var särskilt utsatta för de ineffektiviteter som denna approach medförde.

Utmaningarna var många: inkonsistent tillämpning av säkerhetspolicies, långa feedback-loopar mellan utveckling och säkerhet, och begränsad skalbarhet när organisationer växte och antalet infrastrukturresurser ökade exponentiellt. Dokumentation blev snabbt föråldrad, och kunskapsöverföring mellan team var problematisk.

**Fas 2: Scriptbaserad Automatisering (2015-2018)**

När organisationer började inse begränsningarna med manuella processer började de utveckla skript för att automatisera säkerhetsvalidering. Python-skript, Bash-scripts och powershell-moduler utvecklades för att kontrollera infrastrukturkonfigurationer mot företagspolicies. Denna approach möjliggjorde snabbare validering men saknade standardisering och var svår att underhålla.

Svenska utvecklingsteam började experimentera med custom security validation scripts som integrerades i CI/CD-pipelines. Dessa early adopters upptäckte både möjligheterna och begränsningarna med scriptbaserad automatisering: medan automation förbättrade hastigheten betydligt, blev maintenance av hundratals specialiserade scripts en börda i sig själv.

**Fas 3: Policy Engine Integration (2018-2021)**

Introduktionen av dedikerade policy engines som Open Policy Agent (OPA) markerade en vändpunkt i utvecklingen av säkerhetsautomatisering. Dessa verktyg erbjöd standardiserade sätt att uttrycka och utvärdera policies, vilket möjliggjorde separation av policy logic från implementation details.

Kubernetes adoption i svenska organisationer drev utvecklingen av sofistikerade admission controllers och policy enforcement points. Gatekeeper, baserat på OPA, blev snabbt de facto standarden för Kubernetes policy enforcement. Svenska enterprise-organisationer började utveckla comprehensive policy libraries som täckte allt från basic security hygiene till complex compliance requirements.

**Fas 4: Comprehensive Policy Frameworks (2021-nu)**

Dagens generation av policy as code platforms integrerar djupt med hela utvecklingslivscykeln, från design-time validation till runtime monitoring och automated remediation. OSCAL (Open Security Controls Assessment Language) har framträtt som en game-changing standard som möjliggör interoperabilitet mellan olika säkerhetsverktyg och standardiserad representation av säkerhetskontroller.

Svenska organisationer är nu i förfronten av att adoptера comprehensive policy frameworks som kombinerar policy as code med continuous compliance monitoring, automated risk assessment och adaptive security controls. Denna evolution har möjliggjort för organisationer att uppnå regulatory compliance med unprecedented precision och effektivitet.

## Open Policy Agent (OPA) och Rego: Grunden för policy-driven säkerhet

Open Policy Agent har etablerats som de facto standarden för policy as code implementation genom sin flexibla arkitektur och kraftfulla deklarativa policy-språk Rego. OPA:s framgång ligger i dess förmåga att separera policy logic från application logic, vilket möjliggör centraliserad policy management samtidigt som utvecklingsteam behåller autonomi över sina applikationer och infrastrukturer.

Rego-språket representerar en paradigm shift från imperativ till deklarativ policy definition. Istället för att specificera "hur" något ska göras, fokuserar Rego på "vad" som ska uppnås. Denna approach resulterar i policies som är mer läsbara, testbara och underhållbara jämfört med traditionella script-baserade lösningar.

För svenska organisationer som måste navigera komplex regulatorisk miljö, erbjuder OPA och Rego en kraftfull plattform för att implementera allt från basic säkerhetshygien till sophisticated compliance frameworks. Policy-utvecklare kan skapa modulära, återanvändbara bibliotek som täcker common säkerhetspatterns, regulatory requirements och organizational standards.

### Arkitekturell foundation för enterprise policy management

OPA:s arkitektur bygger på flera nyckelprinciper som gör det särskilt lämpat för enterprise-environments:

**Decouplad Policy Evaluation**: OPA agerar som en policy evaluation engine som tar emot data och policies som input och producerar decisions som output. Denna separation tillåter samma policy logic att appliceras över olika systems och environments utan modification.

**Pull vs Push Policy Distribution**: OPA stödjer både pull-baserad policy distribution (där agents hämtar policies från centrala repositories) och push-baserad distribution (där policies distribueras aktivt till agents). Svenska organisationer med strikta säkerhetskrav föredrar ofta pull-baserade approaches för bättre auditability och control.

**Bundle-baserad Policy Packaging**: Policies och data kan paketeras som bundles som inkluderar dependencies, metadata och signatures. Detta möjliggör atomic policy updates och rollback capabilities som är kritiska för production environments.

### Avancerad Rego-programmering för svenska compliance-krav

```rego
# policies/advanced_swedish_compliance.rego
package sweden.enterprise.security

import rego.v1

# ========================================
# GDPR Article 32 - Advanced Implementation
# ========================================

# Komprehensiv krypteringsvalidering som hanterar olika AWS-services
encryption_compliant[resource] {
    resource := input.resources[_]
    resource.type in encryption_required_services
    encryption_methods := get_encryption_status(resource)
    encryption_validation := validate_encryption_strength(encryption_methods)
    encryption_validation.compliant == true
}

encryption_required_services := {
    "aws_s3_bucket",
    "aws_rds_instance", 
    "aws_rds_cluster",
    "aws_ebs_volume",
    "aws_efs_file_system",
    "aws_dynamodb_table",
    "aws_redshift_cluster",
    "aws_elasticsearch_domain",
    "aws_kinesis_stream",
    "aws_sqs_queue",
    "aws_sns_topic"
}

# Avancerad krypteringsvalidering med stöd för olika encryption methods
get_encryption_status(resource) := result {
    resource.type == "aws_s3_bucket"
    result := {
        "at_rest": has_s3_encryption(resource),
        "in_transit": has_s3_ssl_policy(resource),
        "key_management": get_s3_key_management(resource)
    }
}

get_encryption_status(resource) := result {
    resource.type == "aws_rds_instance"
    result := {
        "at_rest": resource.attributes.storage_encrypted,
        "in_transit": resource.attributes.force_ssl,
        "key_management": get_rds_kms_config(resource)
    }
}

# Validera krypteringsstyrka enligt svenska säkerhetskrav
validate_encryption_strength(encryption) := result {
    # Kontrollera att både at-rest och in-transit encryption är aktiverat
    encryption.at_rest == true
    encryption.in_transit == true
    
    # Validera key management practices
    key_validation := validate_key_management(encryption.key_management)
    
    result := {
        "compliant": key_validation.approved,
        "strength_level": key_validation.strength,
        "recommendations": key_validation.recommendations
    }
}

validate_key_management(kms_config) := result {
    # AWS KMS Customer Managed Keys rekommenderas för svenska organisationer
    kms_config.type == "customer_managed"
    kms_config.key_rotation_enabled == true
    kms_config.multi_region_key == false  # Datasuveränitet
    
    result := {
        "approved": true,
        "strength": "high",
        "recommendations": []
    }
}

validate_key_management(kms_config) := result {
    # AWS Managed Keys acceptabelt men med rekommendationer
    kms_config.type == "aws_managed"
    
    result := {
        "approved": true,
        "strength": "medium", 
        "recommendations": [
            "Överväg customer managed keys för förbättrad kontroll",
            "Implementera key rotation policies"
        ]
    }
}

# ========================================
# MSB Säkerhetskrav - Nätverkssegmentering
# ========================================

# Sofistikerad nätverksvalidering som hanterar complex network topologies
network_security_compliant[violation] {
    resource := input.resources[_]
    resource.type == "aws_security_group"
    
    violations := evaluate_network_security(resource)
    violation := violations[_]
    violation.severity in ["critical", "high"]
}

evaluate_network_security(security_group) := violations {
    violations := array.concat(
        evaluate_ingress_rules(security_group),
        evaluate_egress_rules(security_group)
    )
}

evaluate_ingress_rules(sg) := violations {
    violations := [v |
        rule := sg.attributes.ingress[_]
        violation := check_ingress_rule(rule, sg.attributes.name)
        violation != null
        v := violation
    ]
}

check_ingress_rule(rule, sg_name) := violation {
    # Kritisk violation för öppna administrativa portar
    rule.cidr_blocks[_] == "0.0.0.0/0"
    rule.from_port in administrative_ports
    
    violation := {
        "type": "critical_port_exposure",
        "severity": "critical",
        "port": rule.from_port,
        "security_group": sg_name,
        "message": sprintf("Administrativ port %v exponerad mot internet", [rule.from_port]),
        "remediation": "Begränsa access till specifika management networks",
        "msb_requirement": "Säkerhetskrav 3.2.1 - Nätverkssegmentering"
    }
}

check_ingress_rule(rule, sg_name) := violation {
    # High violation för icke-standard portar öppna mot internet
    rule.cidr_blocks[_] == "0.0.0.0/0"
    not rule.from_port in allowed_public_ports
    not rule.from_port in administrative_ports
    
    violation := {
        "type": "non_standard_port_exposure", 
        "severity": "high",
        "port": rule.from_port,
        "security_group": sg_name,
        "message": sprintf("Icke-standard port %v exponerad mot internet", [rule.from_port]),
        "remediation": "Validera business requirement och begränsa access",
        "msb_requirement": "Säkerhetskrav 3.2.2 - Minimal exponering"
    }
}

administrative_ports := {22, 3389, 5432, 3306, 1433, 27017, 6379, 9200, 5601}
allowed_public_ports := {80, 443}

# ========================================
# Datasuveränitet och GDPR Compliance
# ========================================

data_sovereignty_compliant[resource] {
    resource := input.resources[_]
    resource.type in data_storage_services
    
    # Kontrollera dataklassificering
    classification := get_data_classification(resource)
    
    # Validera region placement baserat på dataklassificering
    region_compliance := validate_region_placement(resource, classification)
    region_compliance.compliant == true
}

data_storage_services := {
    "aws_s3_bucket", "aws_rds_instance", "aws_rds_cluster",
    "aws_dynamodb_table", "aws_elasticsearch_domain", 
    "aws_redshift_cluster", "aws_efs_file_system"
}

get_data_classification(resource) := classification {
    # Prioritera explicit tagging
    classification := resource.attributes.tags["DataClassification"]
    classification != null
}

get_data_classification(resource) := "personal" {
    # Infer från resource naming patterns
    contains(lower(resource.attributes.name), "personal")
}

get_data_classification(resource) := "personal" {
    # Infer från database patterns
    resource.type in ["aws_rds_instance", "aws_rds_cluster"]
    database_indicators := {"user", "customer", "personal", "gdpr", "pii"}
    some indicator in database_indicators
    contains(lower(resource.attributes.identifier), indicator)
}

get_data_classification(resource) := "internal" {
    # Default för oklassificerad data
    true
}

validate_region_placement(resource, classification) := result {
    # Persondata måste lagras inom EU
    classification == "personal"
    resource_region := get_resource_region(resource)
    eu_regions := {"eu-north-1", "eu-west-1", "eu-west-2", "eu-west-3", "eu-central-1", "eu-south-1"}
    
    resource_region in eu_regions
    
    result := {
        "compliant": true,
        "region": resource_region,
        "classification": classification,
        "requirement": "GDPR Artikel 44-49 - Överföringar till tredje land"
    }
}

validate_region_placement(resource, classification) := result {
    # Persondata i icke-EU region
    classification == "personal"
    resource_region := get_resource_region(resource)
    eu_regions := {"eu-north-1", "eu-west-1", "eu-west-2", "eu-west-3", "eu-central-1", "eu-south-1"}
    
    not resource_region in eu_regions
    
    result := {
        "compliant": false,
        "region": resource_region, 
        "classification": classification,
        "violation_type": "data_sovereignty",
        "severity": "critical",
        "message": sprintf("Persondata lagras i region %v utanför EU", [resource_region]),
        "remediation": "Flytta resurs till EU-region eller implementera adequacy decision framework",
        "requirement": "GDPR Artikel 44-49 - Överföringar till tredje land"
    }
}

get_resource_region(resource) := region {
    # Explicit region setting
    region := resource.attributes.region
    region != null
}

get_resource_region(resource) := region {
    # Infer från availability zone
    az := resource.attributes.availability_zone
    region := substring(az, 0, count(az) - 1)
}

get_resource_region(resource) := "unknown" {
    # Fallback för resources utan explicit region
    true
}

# ========================================
# Comprehensive Compliance Assessment
# ========================================

compliance_assessment := result {
    # Samla alla compliance violations
    encryption_violations := [v | 
        resource := input.resources[_]
        not encryption_compliant[resource]
        v := create_encryption_violation(resource)
    ]
    
    network_violations := [v |
        violation := network_security_compliant[_]
        v := violation
    ]
    
    sovereignty_violations := [v |
        resource := input.resources[_]
        not data_sovereignty_compliant[resource]
        v := create_sovereignty_violation(resource)
    ]
    
    all_violations := array.concat(
        array.concat(encryption_violations, network_violations),
        sovereignty_violations
    )
    
    # Beräkna compliance score
    score := calculate_compliance_score(all_violations)
    
    result := {
        "overall_score": score,
        "total_violations": count(all_violations),
        "critical_violations": count([v | v := all_violations[_]; v.severity == "critical"]),
        "high_violations": count([v | v := all_violations[_]; v.severity == "high"]),
        "medium_violations": count([v | v := all_violations[_]; v.severity == "medium"]),
        "violations": all_violations,
        "recommendations": generate_recommendations(all_violations),
        "regulatory_compliance": {
            "gdpr": assess_gdpr_compliance(all_violations),
            "msb": assess_msb_compliance(all_violations), 
            "iso27001": assess_iso_compliance(all_violations)
        }
    }
}

calculate_compliance_score(violations) := score {
    violation_penalty := sum([penalty |
        violation := violations[_]
        penalty := severity_penalty[violation.severity]
    ])
    
    max_score := 100
    score := math.max(0, max_score - violation_penalty)
}

severity_penalty := {
    "critical": 25,
    "high": 15, 
    "medium": 10,
    "low": 5
}

generate_recommendations(violations) := recommendations {
    violation_types := {v.type | v := violations[_]}
    
    recommendations := [rec |
        violation_type := violation_types[_]
        rec := recommendation_mapping[violation_type]
    ]
}

recommendation_mapping := {
    "encryption_required": "Implementera enterprise encryption standards med customer managed KMS keys",
    "critical_port_exposure": "Implementera bastion hosts eller AWS Systems Manager för administrativ access",
    "data_sovereignty": "Skapa region-specifika Terraform providers för automatisk compliance",
    "resource_tagging": "Implementera obligatorisk tagging genom resource policies"
}
```

### Integration med svenska enterprise-miljöer

För svenska organisationer som opererar inom regulated industries kräver OPA-implementation ofta integration med befintliga säkerhetssystem och compliance frameworks. Detta inkluderar integration med SIEM-system för audit logging, identity providers för policy authorization och enterprise monitoring systems för real-time alerting.

Enterprise-grade OPA deployments kräver också considerations kring high availability, performance optimization och secure policy distribution. Svenska organisationer med kritisk infrastruktur måste säkerställa att policy evaluation inte blir en single point of failure som kan påverka business operations.

## OSCAL: Open Security Controls Assessment Language - Revolutionerande säkerhetsstandardisering

Open Security Controls Assessment Language (OSCAL) representerar en paradigmskifte inom säkerhetshantering och compliance-automation. Utvecklad av NIST (National Institute of Standards and Technology), erbjuder OSCAL en standardiserad approach för att representera, hantera och automatisera säkerhetskontroller och assessment-processer. För svenska organisationer som måste navigera komplex regulatorisk miljö samtidigt som de implementerar Infrastructure as Code, utgör OSCAL en game-changing teknik som möjliggör unprecedented automation och interoperabilitet.

OSCAL adresserar en fundamental utmaning inom enterprise säkerhetshantering: fragmenteringen av säkerhetskontroller, assessment-processer och compliance-frameworks. Traditionellt har organisationer varit tvungna att hantera múltipla, inkompatibla säkerhetsstandarder (ISO 27001, NIST Cybersecurity Framework, SOC 2, GDPR, etc.) genom separata system och processer. OSCAL möjliggör en unified approach där säkerhetskontroller kan uttryckas, mappas och automatiseras genom en gemensam meta-language.

För Infrastructure as Code-practitioners representerar OSCAL möjligheten att integrera säkerhetskontroller direkt i utvecklingsprocessen genom machine-readable formats som kan valideras, testats och deployeras tillsammans med infrastrukturkod. Detta skapar en seamless integration mellan security governance och infrastructure automation som tidigare varit tekniskt omöjlig att uppnå.

### OSCAL-arkitektur och komponenter

OSCAL-arkitekturen bygger på en hierarkisk struktur av sammanlänkade modeller som tillsammans representerar hela lifecycle för säkerhetskontroller från definition till implementation och assessment. Varje OSCAL-modell tjänar ett specifikt syfte men är designad för seamless interoperabilitet med andra modeller i ekosystemet.

**Catalog Model**: Utgör foundation för OSCAL-ekosystemet genom att definiera collections av säkerhetskontroller. Catalog-modellen möjliggör standardiserad representation av kontrollers från olika frameworks (NIST SP 800-53, ISO 27001, CIS Controls, etc.) i ett unified format. För svenska organisationer möjliggör detta representation av MSB:s säkerhetskrav, GDPR-kontroller och branschspecifika regleringar i samma tekniska framework.

**Profile Model**: Representerar customized selections och configurations av säkerhetskontroller från en eller flera catalogs. Profiles möjliggör organizations att skapa tailored säkerhetskrav baserat på risk tolerance, regulatory requirements och business context. Svenska finansiella institutioner kan exempelvis skapa profiles som kombinerar GDPR-requirements med Finansinspektionens säkerhetskrav och PCI DSS-standards.

**Component Definition Model**: Dokumenterar hur specifika system komponenter (software, hardware, services) implementerar säkerhetskontroller. Denna modell skapar critical linking mellan abstrakt kontrolldefinitioner och konkret implementation details. I Infrastructure as Code-kontexten representerar component definitions hur specific Terraform modules, Kubernetes deployments eller AWS services implementerar required säkerhetskontroller.

**System Security Plan (SSP) Model**: Beskriver comprehensive säkerhetsimplementation för ett specifikt system, inklusive how säkerhetskontroller är implementerade, who ansvarar för varje kontroll och how kontrollers monitoras och maintainas. SSP-modellen möjliggör automated generation av säkerhetsdokumentation direkt från Infrastructure as Code definitions.

**Assessment Plan och Assessment Results Models**: Definierar how säkerhetskontroller ska assessas och dokumenterar resultaten av dessa assessments. Dessa modeller möjliggör automated compliance testing och continuous monitoring av säkerhetskontroller genom integration med CI/CD pipelines.

**Plan of Action and Milestones (POA&M) Model**: Hanterar remediation planning och tracking för identified säkerhetsgap. POA&M-modellen möjliggör systematic approach till säkerhetsförbättringar och kan integreras med project management tools för comprehensive risk management.

### Praktisk OSCAL-implementation för svenska organisationer

Implementation av OSCAL i svenska enterprise-miljöer kräver careful planning och systematic approach som respekterar befintliga säkerhetsprocesser samtidigt som moderna automation capabilities introduceras gradvist.

```json
{
  "catalog": {
    "uuid": "12345678-1234-5678-9abc-123456789012",
    "metadata": {
      "title": "Svenska Enterprise Säkerhetskontroller",
      "published": "2024-01-15T10:00:00Z",
      "last-modified": "2024-01-15T10:00:00Z",
      "version": "1.0",
      "oscal-version": "1.1.2",
      "props": [
        {
          "name": "organization",
          "value": "Svenska Myndigheten för Samhällsskydd och Beredskap"
        },
        {
          "name": "jurisdiction", 
          "value": "Sweden"
        }
      ]
    },
    "groups": [
      {
        "id": "gdpr-controls",
        "title": "GDPR Säkerhetskontroller",
        "props": [
          {
            "name": "label",
            "value": "GDPR"
          }
        ],
        "controls": [
          {
            "id": "gdpr-art32-1",
            "title": "Säkerhet i behandlingen - Kryptering",
            "params": [
              {
                "id": "gdpr-art32-1_prm1",
                "label": "Krypteringsstandard",
                "values": ["AES-256", "RSA-2048"]
              },
              {
                "id": "gdpr-art32-1_prm2", 
                "label": "Nyckelhantering",
                "values": ["HSM", "AWS KMS Customer Managed"]
              }
            ],
            "props": [
              {
                "name": "label",
                "value": "GDPR-32.1"
              },
              {
                "name": "sort-id",
                "value": "gdpr-32-01"
              }
            ],
            "parts": [
              {
                "id": "gdpr-art32-1_smt",
                "name": "statement",
                "prose": "Den registeransvarige och personuppgiftsbiträdet ska, med beaktande av den senaste utvecklingen, genomförandekostnaderna och behandlingens art, omfattning, sammanhang och ändamål samt riskerna, av varierande sannolikhetsgrad och allvar, för fysiska personers rättigheter och friheter, genomföra lämpliga tekniska och organisatoriska åtgärder för att säkerställa en säkerhetsnivå som är lämplig i förhållande till risken, inbegripet pseudonymisering och kryptering av personuppgifter."
              },
              {
                "id": "gdpr-art32-1_gdn",
                "name": "guidance",
                "prose": "För svenska organisationer rekommenderas implementation av kryptering för alla persondata både i vila och under överföring. Krypteringsnycklar ska hanteras enligt svenska säkerhetskrav och preferably genom Hardware Security Modules (HSM) eller motsvarande säkra nyckelhanteringssystem."
              }
            ],
            "controls": [
              {
                "id": "gdpr-art32-1.1",
                "title": "Kryptering i vila",
                "props": [
                  {
                    "name": "label", 
                    "value": "GDPR-32.1.1"
                  }
                ],
                "parts": [
                  {
                    "id": "gdpr-art32-1.1_smt",
                    "name": "statement", 
                    "prose": "Alla databaser och storage systems som innehåller persondata ska krypteras i vila med godkända krypteringsalgoritmer."
                  }
                ]
              },
              {
                "id": "gdpr-art32-1.2",
                "title": "Kryptering under överföring",
                "props": [
                  {
                    "name": "label",
                    "value": "GDPR-32.1.2"  
                  }
                ],
                "parts": [
                  {
                    "id": "gdpr-art32-1.2_smt",
                    "name": "statement",
                    "prose": "All kommunikation som överför persondata ska ske över krypterade kanaler med minimum TLS 1.2."
                  }
                ]
              }
            ]
          }
        ]
      },
      {
        "id": "msb-controls",
        "title": "MSB Säkerhetskrav för Kritisk Infrastruktur", 
        "props": [
          {
            "name": "label",
            "value": "MSB"
          }
        ],
        "controls": [
          {
            "id": "msb-3.2.1",
            "title": "Nätverkssegmentering",
            "props": [
              {
                "name": "label",
                "value": "MSB-3.2.1"
              }
            ],
            "parts": [
              {
                "id": "msb-3.2.1_smt",
                "name": "statement",
                "prose": "Kritiska system ska skyddas genom nätverkssegmentering som begränsar potentiell lateral movement av angripare och minimerar attack surface."
              },
              {
                "id": "msb-3.2.1_gdn", 
                "name": "guidance",
                "prose": "Implementation ska inkludera micro-segmentation på application layer, network access control lists och zero-trust network principles. För molnmiljöer rekommenderas implementation genom Virtual Private Clouds (VPC), Security Groups och Network Access Control Lists (NACLs)."
              }
            ],
            "controls": [
              {
                "id": "msb-3.2.1.1",
                "title": "Micro-segmentation",
                "parts": [
                  {
                    "id": "msb-3.2.1.1_smt",
                    "name": "statement",
                    "prose": "Applikationer ska segmenteras på network layer för att begränsa lateral movement."
                  }
                ]
              },
              {
                "id": "msb-3.2.1.2", 
                "title": "Zero Trust Network Access",
                "parts": [
                  {
                    "id": "msb-3.2.1.2_smt",
                    "name": "statement",
                    "prose": "Alla network access requests ska verifieras och authoriseras oavsett source location."
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

### OSCAL Profile utveckling för svenska företag

OSCAL Profiles möjliggör svenska organisationer att skapa customized säkerhetskrav som kombinerar múltipla regulatory frameworks i en coherent, implementable standard. Denna capability är särskilt värdefull för svenska multinationals som måste balansera lokala regulatory requirements med global enterprise standards.

```json
{
  "profile": {
    "uuid": "87654321-4321-8765-4321-876543218765",
    "metadata": {
      "title": "Svenska Finansiella Institutioner Säkerhetsprofil",
      "published": "2024-01-15T11:00:00Z",
      "last-modified": "2024-01-15T11:00:00Z", 
      "version": "2.1",
      "oscal-version": "1.1.2",
      "props": [
        {
          "name": "organization",
          "value": "Svenska Finansiella Sektorn"
        },
        {
          "name": "sector",
          "value": "Financial Services"
        }
      ]
    },
    "imports": [
      {
        "href": "https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json",
        "include-controls": [
          {
            "matching": [
              {
                "pattern": "ac-.*"
              },
              {
                "pattern": "au-.*"
              },
              {
                "pattern": "sc-.*"
              }
            ]
          }
        ]
      },
      {
        "href": "svenska-enterprise-catalog.json",
        "include-controls": [
          {
            "matching": [
              {
                "pattern": "gdpr-.*"
              },
              {
                "pattern": "msb-.*"
              }
            ]
          }
        ]
      }
    ],
    "merge": {
      "combine": {
        "method": "merge"
      }
    },
    "modify": {
      "set-parameters": [
        {
          "param-id": "ac-1_prm_1",
          "values": ["Svenska Finansiella Säkerhetspolicies"]
        },
        {
          "param-id": "gdpr-art32-1_prm1",
          "values": ["AES-256-GCM"]
        },
        {
          "param-id": "gdpr-art32-1_prm2",
          "values": ["AWS KMS Customer Managed med HSM backing"]
        }
      ],
      "alters": [
        {
          "control-id": "gdpr-art32-1",
          "adds": [
            {
              "position": "after",
              "by-id": "gdpr-art32-1_gdn",
              "parts": [
                {
                  "id": "gdpr-art32-1_fi-gdn",
                  "name": "guidance",
                  "title": "Finansinspektionens Tilläggskrav",
                  "prose": "Finansiella institutioner ska dessutom implementera kryptering enligt Finansinspektionens föreskrifter om informationssäkerhet (FFFS 2017:7) vilket inkluderar krav på certified cryptographic modules och regular key rotation."
                }
              ]
            }
          ]
        },
        {
          "control-id": "msb-3.2.1",
          "adds": [
            {
              "position": "after", 
              "by-id": "msb-3.2.1_gdn",
              "parts": [
                {
                  "id": "msb-3.2.1_fi-req",
                  "name": "requirement",
                  "title": "Finansiella Tilläggskrav", 
                  "prose": "Finansiella transaktionssystem ska implementera additional network isolation och encrypted communication channels för alla customer data flows enligt PCI DSS Level 1 requirements."
                }
              ]
            }
          ]
        }
      ]
    }
  }
}
```

### Component Definition för Infrastructure as Code

En av OSCAL:s mest kraftfulla capabilities är möjligheten att dokumentera how specific technology components implementerar säkerhetskontroller. För Infrastructure as Code-practitioners möjliggör detta automatic generation av säkerhetsdokumentation och compliance validation directly från infrastructure definitions.

```json
{
  "component-definition": {
    "uuid": "11223344-5566-7788-99aa-bbccddeeff00",
    "metadata": {
      "title": "AWS Infrastructure Components för Svenska Organisationer",
      "published": "2024-01-15T12:00:00Z",
      "last-modified": "2024-01-15T12:00:00Z",
      "version": "1.5",
      "oscal-version": "1.1.2"
    },
    "components": [
      {
        "uuid": "comp-aws-rds-mysql",
        "type": "software",
        "title": "AWS RDS MySQL Database Instance",
        "description": "Managed MySQL database service med svenska compliance konfiguration",
        "props": [
          {
            "name": "version",
            "value": "8.0"
          },
          {
            "name": "provider",
            "value": "AWS"
          }
        ],
        "control-implementations": [
          {
            "uuid": "impl-rds-mysql-gdpr",
            "source": "svenska-enterprise-catalog.json",
            "description": "GDPR compliance implementation för RDS MySQL",
            "implemented-requirements": [
              {
                "uuid": "req-gdpr-encryption",
                "control-id": "gdpr-art32-1.1",
                "description": "RDS encryption at rest implementation",
                "statements": [
                  {
                    "statement-id": "gdpr-art32-1.1_smt",
                    "uuid": "stmt-rds-encryption",
                    "description": "Encryption konfigurerad genom storage_encrypted parameter",
                    "implementation-status": {
                      "state": "implemented"
                    }
                  }
                ],
                "props": [
                  {
                    "name": "implementation-point",
                    "value": "Terraform aws_db_instance resource"
                  }
                ]
              },
              {
                "uuid": "req-gdpr-transit-encryption", 
                "control-id": "gdpr-art32-1.2",
                "description": "RDS encryption in transit implementation",
                "statements": [
                  {
                    "statement-id": "gdpr-art32-1.2_smt",
                    "uuid": "stmt-rds-ssl",
                    "description": "TLS enforced genom DB parameter groups",
                    "implementation-status": {
                      "state": "implemented"
                    }
                  }
                ]
              }
            ]
          },
          {
            "uuid": "impl-rds-mysql-msb",
            "source": "svenska-enterprise-catalog.json",
            "description": "MSB compliance implementation för RDS MySQL",
            "implemented-requirements": [
              {
                "uuid": "req-msb-network-isolation",
                "control-id": "msb-3.2.1.1",
                "description": "Network segmentation genom VPC och Security Groups",
                "statements": [
                  {
                    "statement-id": "msb-3.2.1.1_smt",
                    "uuid": "stmt-rds-vpc",
                    "description": "RDS deployed i private subnets med restricted Security Groups",
                    "implementation-status": {
                      "state": "implemented"
                    }
                  }
                ]
              }
            ]
          }
        ]
      },
      {
        "uuid": "comp-aws-s3-bucket",
        "type": "software", 
        "title": "AWS S3 Storage Bucket",
        "description": "Object storage med svenska compliance och säkerhetskonfiguration",
        "control-implementations": [
          {
            "uuid": "impl-s3-gdpr",
            "source": "svenska-enterprise-catalog.json", 
            "description": "S3 GDPR compliance implementation",
            "implemented-requirements": [
              {
                "uuid": "req-s3-encryption",
                "control-id": "gdpr-art32-1.1",
                "description": "S3 encryption at rest med Customer Managed KMS",
                "statements": [
                  {
                    "statement-id": "gdpr-art32-1.1_smt",
                    "uuid": "stmt-s3-kms",
                    "description": "Default encryption configured med AES-256 och Customer Managed KMS keys",
                    "implementation-status": {
                      "state": "implemented"
                    }
                  }
                ],
                "props": [
                  {
                    "name": "encryption-algorithm",
                    "value": "AES-256"
                  },
                  {
                    "name": "key-management",
                    "value": "AWS KMS Customer Managed"
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

### System Security Plan automation med OSCAL

En av OSCAL:s mest transformativa capabilities är möjligheten att automatically generera comprehensive System Security Plans (SSP) från Infrastructure as Code definitions kombinerat med component definitions. Detta revolutionerar säkerhetsdokumentation från static, manually maintained documents till dynamic, continuously updated representations av actual system state.

```python
# oscal_ssp_generator.py
import json
import yaml
from typing import Dict, List, Any
from datetime import datetime
import hcl2
import boto3

class OSCALSystemSecurityPlanGenerator:
    """
    Automated generation av OSCAL System Security Plans från Infrastructure as Code
    """
    
    def __init__(self, terraform_directory: str, component_definitions: List[str]):
        self.terraform_directory = terraform_directory
        self.component_definitions = component_definitions
        self.aws_client = boto3.client('sts')
        
    def generate_ssp(self, profile_href: str, system_name: str) -> Dict[str, Any]:
        """Generera comprehensive SSP från IaC definitions"""
        
        # Parse Terraform configurations
        terraform_resources = self._parse_terraform_resources()
        
        # Load component definitions
        components = self._load_component_definitions()
        
        # Match resources till components
        resource_mappings = self._map_resources_to_components(terraform_resources, components)
        
        # Generate control implementations
        control_implementations = self._generate_control_implementations(resource_mappings)
        
        # Create SSP structure
        ssp = {
            "system-security-plan": {
                "uuid": self._generate_uuid(),
                "metadata": {
                    "title": f"System Security Plan - {system_name}",
                    "published": datetime.now().isoformat() + "Z",
                    "last-modified": datetime.now().isoformat() + "Z",
                    "version": "1.0",
                    "oscal-version": "1.1.2",
                    "props": [
                        {
                            "name": "organization", 
                            "value": "Svenska Enterprise Organization"
                        },
                        {
                            "name": "system-name",
                            "value": system_name
                        }
                    ]
                },
                "import-profile": {
                    "href": profile_href
                },
                "system-characteristics": {
                    "system-ids": [
                        {
                            "identifier-type": "https://ietf.org/rfc/rfc4122",
                            "id": self._get_aws_account_id()
                        }
                    ],
                    "system-name": system_name,
                    "description": f"Automated System Security Plan för {system_name} genererad från Infrastructure as Code",
                    "security-sensitivity-level": "moderate",
                    "system-information": {
                        "information-types": [
                            {
                                "uuid": self._generate_uuid(),
                                "title": "Persondata enligt GDPR",
                                "description": "Personuppgifter som behandlas enligt GDPR",
                                "categorizations": [
                                    {
                                        "system": "https://doi.org/10.6028/NIST.SP.800-60v1r1",
                                        "information-type-ids": ["C.3.5.8"]
                                    }
                                ],
                                "confidentiality-impact": {
                                    "base": "moderate",
                                    "selected": "high",
                                    "adjustment-justification": "Svenska GDPR-krav kräver högt skydd"
                                },
                                "integrity-impact": {
                                    "base": "moderate", 
                                    "selected": "high"
                                },
                                "availability-impact": {
                                    "base": "low",
                                    "selected": "moderate"
                                }
                            }
                        ]
                    },
                    "security-impact-level": {
                        "security-objective-confidentiality": "high",
                        "security-objective-integrity": "high", 
                        "security-objective-availability": "moderate"
                    },
                    "status": {
                        "state": "operational"
                    },
                    "authorization-boundary": {
                        "description": "AWS Account boundary inkluderande alla IaC-managed resources"
                    }
                },
                "system-implementation": {
                    "users": [
                        {
                            "uuid": self._generate_uuid(),
                            "title": "Svenska System Administrators",
                            "description": "Administratörer med privileged access till system components",
                            "props": [
                                {
                                    "name": "type",
                                    "value": "internal"
                                }
                            ],
                            "role-ids": ["admin-role"]
                        },
                        {
                            "uuid": self._generate_uuid(),
                            "title": "Svenska End Users",
                            "description": "Standard användare med begränsad access",
                            "props": [
                                {
                                    "name": "type", 
                                    "value": "internal"
                                }
                            ],
                            "role-ids": ["user-role"]
                        }
                    ],
                    "components": self._generate_ssp_components(resource_mappings)
                },
                "control-implementation": {
                    "description": "Control implementation för svenska compliance requirements",
                    "implemented-requirements": control_implementations
                }
            }
        }
        
        return ssp
    
    def _parse_terraform_resources(self) -> List[Dict]:
        """Parse Terraform configurations och extrahera resource definitions"""
        resources = []
        
        for tf_file in self._find_terraform_files():
            with open(tf_file, 'r') as f:
                try:
                    tf_content = hcl2.loads(f.read())
                    
                    for resource_type, resource_configs in tf_content.get('resource', {}).items():
                        for resource_name, resource_config in resource_configs.items():
                            resources.append({
                                "type": resource_type,
                                "name": resource_name,
                                "config": resource_config,
                                "file": tf_file
                            })
                except Exception as e:
                    print(f"Error parsing {tf_file}: {e}")
                    
        return resources
    
    def _map_resources_to_components(self, resources: List[Dict], components: List[Dict]) -> Dict:
        """Mappa Terraform resources till OSCAL components"""
        mappings = {}
        
        for resource in resources:
            for component in components:
                if self._resource_matches_component(resource, component):
                    mappings[f"{resource['type']}.{resource['name']}"] = {
                        "resource": resource,
                        "component": component
                    }
                    
        return mappings
    
    def _resource_matches_component(self, resource: Dict, component: Dict) -> bool:
        """Kontrollera om en Terraform resource matchar en OSCAL component"""
        
        # AWS RDS mapping
        if resource['type'] == 'aws_db_instance' and 'rds' in component.get('title', '').lower():
            return True
            
        # AWS S3 mapping  
        if resource['type'] == 'aws_s3_bucket' and 's3' in component.get('title', '').lower():
            return True
            
        # AWS EC2 mapping
        if resource['type'] == 'aws_instance' and 'ec2' in component.get('title', '').lower():
            return True
            
        return False
    
    def _generate_control_implementations(self, mappings: Dict) -> List[Dict]:
        """Generera control implementations baserat på resource mappings"""
        implementations = []
        
        for resource_id, mapping in mappings.items():
            resource = mapping['resource']
            component = mapping['component']
            
            for impl in component.get('control-implementations', []):
                for req in impl.get('implemented-requirements', []):
                    # Validera att resource faktiskt implementerar kontrollen
                    validation_result = self._validate_control_implementation(resource, req)
                    
                    implementations.append({
                        "uuid": self._generate_uuid(),
                        "control-id": req['control-id'],
                        "description": f"Implementation genom {resource_id}",
                        "statements": [
                            {
                                "statement-id": stmt.get('statement-id'),
                                "uuid": self._generate_uuid(),
                                "description": f"{stmt.get('description')} - Status: {validation_result['status']}",
                                "implementation-status": {
                                    "state": validation_result['status']
                                }
                            }
                            for stmt in req.get('statements', [])
                        ],
                        "props": [
                            {
                                "name": "implementation-point",
                                "value": resource_id
                            },
                            {
                                "name": "validation-timestamp",
                                "value": datetime.now().isoformat() + "Z"
                            }
                        ]
                    })
                    
        return implementations
    
    def _validate_control_implementation(self, resource: Dict, requirement: Dict) -> Dict:
        """Validera att en resource faktiskt implementerar en säkerhetskontroll"""
        
        control_id = requirement['control-id']
        resource_config = resource['config']
        
        # GDPR encryption validation
        if 'gdpr-art32-1.1' in control_id:  # Encryption at rest
            if resource['type'] == 'aws_db_instance':
                encrypted = resource_config.get('storage_encrypted', False)
                return {
                    "status": "implemented" if encrypted else "planned",
                    "details": f"Storage encryption: {encrypted}"
                }
            elif resource['type'] == 'aws_s3_bucket':
                # Check för server_side_encryption_configuration
                encryption_config = resource_config.get('server_side_encryption_configuration')
                return {
                    "status": "implemented" if encryption_config else "planned",
                    "details": f"Encryption configuration present: {bool(encryption_config)}"
                }
        
        # MSB network segmentation validation
        elif 'msb-3.2.1' in control_id:
            if resource['type'] == 'aws_db_instance':
                vpc_sg = resource_config.get('vpc_security_group_ids', [])
                db_subnet_group = resource_config.get('db_subnet_group_name')
                return {
                    "status": "implemented" if vpc_sg and db_subnet_group else "planned",
                    "details": f"VPC security: {bool(vpc_sg)}, Subnet group: {bool(db_subnet_group)}"
                }
        
        return {"status": "planned", "details": "Validation not implemented för denna kontroll"}
    
    def _generate_ssp_components(self, mappings: Dict) -> List[Dict]:
        """Generera SSP component definitions"""
        components = []
        
        for resource_id, mapping in mappings.items():
            resource = mapping['resource']
            component = mapping['component']
            
            components.append({
                "uuid": self._generate_uuid(),
                "type": "software",
                "title": f"{resource['type']} - {resource['name']}",
                "description": f"IaC-managed {resource['type']} implementation",
                "status": {
                    "state": "operational"
                },
                "props": [
                    {
                        "name": "terraform-resource",
                        "value": resource_id
                    },
                    {
                        "name": "deployment-status", 
                        "value": "active"
                    }
                ]
            })
            
        return components
    
    def _generate_uuid(self) -> str:
        """Generera UUID för OSCAL elements"""
        import uuid
        return str(uuid.uuid4())
    
    def _get_aws_account_id(self) -> str:
        """Hämta AWS account ID för system identification"""
        try:
            return self.aws_client.get_caller_identity()['Account']
        except Exception:
            return "unknown-account"
    
    def _find_terraform_files(self) -> List[str]:
        """Hitta alla Terraform-filer i directory"""
        import glob
        import os
        
        tf_files = []
        for root, dirs, files in os.walk(self.terraform_directory):
            for file in files:
                if file.endswith('.tf'):
                    tf_files.append(os.path.join(root, file))
                    
        return tf_files
    
    def _load_component_definitions(self) -> List[Dict]:
        """Ladda OSCAL component definitions"""
        components = []
        
        for comp_def_file in self.component_definitions:
            with open(comp_def_file, 'r') as f:
                comp_def = json.load(f)
                components.extend(comp_def.get('component-definition', {}).get('components', []))
                
        return components

# Användning för svenska organisationer
def generate_swedish_enterprise_ssp():
    """Exempel på SSP generation för svenska enterprise-miljö"""
    
    generator = OSCALSystemSecurityPlanGenerator(
        terraform_directory="/path/to/terraform",
        component_definitions=[
            "svenska-aws-components.json",
            "kubernetes-components.json"
        ]
    )
    
    ssp = generator.generate_ssp(
        profile_href="svenska-finansiella-profil.json",
        system_name="Svenska Enterprise Production Environment"
    )
    
    # Spara SSP
    with open("svenska-enterprise-ssp.json", "w") as f:
        json.dump(ssp, f, indent=2, ensure_ascii=False)
    
    print("System Security Plan genererad för svenska enterprise-miljö")
    
    return ssp
```

### OSCAL Assessment och Continuous Compliance

En av OSCAL:s mest kraftfulla features är möjligheten att automatisera security assessments och implementera continuous compliance monitoring. För svenska organisationer som måste demonstrera ongoing compliance med GDPR, MSB-krav och andra regulatoriska frameworks, möjliggör OSCAL assessment automation unprecedented precision och efficiency.

```python
# oscal_assessment_automation.py
import json
import boto3
from typing import Dict, List, Any
from datetime import datetime, timedelta
import subprocess

class OSCALAssessmentEngine:
    """
    Automated OSCAL assessment engine för svenska compliance requirements
    """
    
    def __init__(self, ssp_file: str, assessment_plan_file: str):
        self.ssp_file = ssp_file
        self.assessment_plan_file = assessment_plan_file
        self.aws_config = boto3.client('config')
        self.aws_inspector = boto3.client('inspector2')
        
    def execute_assessment(self) -> Dict[str, Any]:
        """Kör comprehensive OSCAL assessment"""
        
        # Ladda SSP och assessment plan
        with open(self.ssp_file, 'r') as f:
            ssp = json.load(f)
            
        with open(self.assessment_plan_file, 'r') as f:
            assessment_plan = json.load(f)
        
        # Kör automated tests för varje kontroll
        assessment_results = {
            "assessment-results": {
                "uuid": self._generate_uuid(),
                "metadata": {
                    "title": "Automated OSCAL Assessment - Svenska Enterprise",
                    "published": datetime.now().isoformat() + "Z",
                    "last-modified": datetime.now().isoformat() + "Z",
                    "version": "1.0",
                    "oscal-version": "1.1.2"
                },
                "import-ssp": {
                    "href": self.ssp_file
                },
                "assessment-activities": [],
                "results": []
            }
        }
        
        # Kör assessments för implemented requirements
        for impl_req in ssp['system-security-plan']['control-implementation']['implemented-requirements']:
            control_id = impl_req['control-id']
            assessment_result = self._assess_control(control_id, impl_req, ssp)
            assessment_results['assessment-results']['results'].append(assessment_result)
        
        # Generera overall compliance score
        compliance_score = self._calculate_compliance_score(assessment_results['assessment-results']['results'])
        assessment_results['assessment-results']['compliance-score'] = compliance_score
        
        return assessment_results
    
    def _assess_control(self, control_id: str, implementation: Dict, ssp: Dict) -> Dict:
        """Assess en specifik säkerhetskontroll"""
        
        if 'gdpr-art32-1' in control_id:
            return self._assess_gdpr_encryption(control_id, implementation, ssp)
        elif 'msb-3.2.1' in control_id:
            return self._assess_msb_network_segmentation(control_id, implementation, ssp)
        else:
            return self._assess_generic_control(control_id, implementation)
    
    def _assess_gdpr_encryption(self, control_id: str, implementation: Dict, ssp: Dict) -> Dict:
        """Assess GDPR encryption requirements"""
        
        findings = []
        
        # Kontrollera AWS Config rules för encryption compliance
        config_rules = [
            'rds-storage-encrypted',
            's3-bucket-server-side-encryption-enabled',
            'ebs-encrypted-volumes'
        ]
        
        for rule_name in config_rules:
            try:
                response = self.aws_config.get_compliance_details_by_config_rule(
                    ConfigRuleName=rule_name
                )
                
                non_compliant_resources = [
                    r for r in response.get('EvaluationResults', [])
                    if r['ComplianceType'] == 'NON_COMPLIANT'
                ]
                
                if non_compliant_resources:
                    findings.append({
                        "uuid": self._generate_uuid(),
                        "title": f"Non-compliant resources för {rule_name}",
                        "description": f"Hittade {len(non_compliant_resources)} non-compliant resources",
                        "severity": "high",
                        "implementation-statement-uuid": implementation['statements'][0]['uuid'],
                        "related-observations": [
                            {
                                "observation-uuid": self._generate_uuid(),
                                "description": f"Resource {r['EvaluationResultIdentifier']['EvaluationResultQualifier']['ResourceId']} är non-compliant"
                            }
                            for r in non_compliant_resources[:5]  # Begränsa till 5 för readability
                        ]
                    })
                else:
                    findings.append({
                        "uuid": self._generate_uuid(),
                        "title": f"Compliant encryption för {rule_name}",
                        "description": "Alla resurser följer encryption requirements",
                        "severity": "info",
                        "implementation-statement-uuid": implementation['statements'][0]['uuid']
                    })
                    
            except Exception as e:
                findings.append({
                    "uuid": self._generate_uuid(),
                    "title": f"Assessment error för {rule_name}",
                    "description": f"Kunde inte köra assessment: {str(e)}",
                    "severity": "medium"
                })
        
        # Sammanställ assessment result
        has_high_findings = any(f.get('severity') == 'high' for f in findings)
        
        return {
            "uuid": self._generate_uuid(),
            "title": f"GDPR Encryption Assessment - {control_id}",
            "description": "Automated assessment av GDPR encryption requirements",
            "start": (datetime.now() - timedelta(minutes=5)).isoformat() + "Z",
            "end": datetime.now().isoformat() + "Z",
            "props": [
                {
                    "name": "assessment-method",
                    "value": "automated"
                },
                {
                    "name": "assessor",
                    "value": "OSCAL Assessment Engine"
                }
            ],
            "findings": findings,
            "status": "non-compliant" if has_high_findings else "compliant"
        }
    
    def _assess_msb_network_segmentation(self, control_id: str, implementation: Dict, ssp: Dict) -> Dict:
        """Assess MSB network segmentation requirements"""
        
        findings = []
        
        # Kontrollera Security Groups för improper network access
        ec2_client = boto3.client('ec2')
        
        try:
            security_groups = ec2_client.describe_security_groups()['SecurityGroups']
            
            for sg in security_groups:
                # Kontrollera för overly permissive ingress rules
                for rule in sg.get('IpPermissions', []):
                    for ip_range in rule.get('IpRanges', []):
                        if ip_range.get('CidrIp') == '0.0.0.0/0':
                            # Kontrollera om det är administrative ports
                            from_port = rule.get('FromPort', 0)
                            to_port = rule.get('ToPort', 65535)
                            
                            admin_ports = {22, 3389, 5432, 3306, 1433, 27017}
                            
                            if any(port in range(from_port, to_port + 1) for port in admin_ports):
                                findings.append({
                                    "uuid": self._generate_uuid(),
                                    "title": "Otillåten administrativ port exponering",
                                    "description": f"Security Group {sg['GroupId']} exponerar administrativa portar {from_port}-{to_port} mot internet",
                                    "severity": "critical",
                                    "target": {
                                        "type": "resource",
                                        "target-id": sg['GroupId']
                                    }
                                })
            
            # Kontrollera för VPC flow logs
            flow_logs = ec2_client.describe_flow_logs()['FlowLogs']
            active_flow_logs = [fl for fl in flow_logs if fl['FlowLogStatus'] == 'ACTIVE']
            
            if not active_flow_logs:
                findings.append({
                    "uuid": self._generate_uuid(),
                    "title": "VPC Flow Logs inte aktiverade",
                    "description": "VPC Flow Logs krävs för network monitoring enligt MSB-krav",
                    "severity": "high"
                })
            
        except Exception as e:
            findings.append({
                "uuid": self._generate_uuid(),
                "title": "Network assessment error",
                "description": f"Kunde inte köra network assessment: {str(e)}",
                "severity": "medium"
            })
        
        has_critical_findings = any(f.get('severity') == 'critical' for f in findings)
        has_high_findings = any(f.get('severity') == 'high' for f in findings)
        
        return {
            "uuid": self._generate_uuid(),
            "title": f"MSB Network Segmentation Assessment - {control_id}",
            "description": "Automated assessment av MSB network segmentation requirements",
            "start": (datetime.now() - timedelta(minutes=3)).isoformat() + "Z",
            "end": datetime.now().isoformat() + "Z",
            "findings": findings,
            "status": "non-compliant" if (has_critical_findings or has_high_findings) else "compliant"
        }
    
    def _assess_generic_control(self, control_id: str, implementation: Dict) -> Dict:
        """Generic assessment för controls utan specific automated tests"""
        
        return {
            "uuid": self._generate_uuid(),
            "title": f"Manual Assessment Required - {control_id}",
            "description": "Denna kontroll kräver manual assessment",
            "start": datetime.now().isoformat() + "Z",
            "end": datetime.now().isoformat() + "Z",
            "findings": [
                {
                    "uuid": self._generate_uuid(),
                    "title": "Manual review required",
                    "description": f"Control {control_id} kräver manual validation av implementation",
                    "severity": "info"
                }
            ],
            "status": "unknown"
        }
    
    def _calculate_compliance_score(self, results: List[Dict]) -> Dict:
        """Beräkna overall compliance score"""
        
        total_controls = len(results)
        compliant_controls = len([r for r in results if r.get('status') == 'compliant'])
        non_compliant_controls = len([r for r in results if r.get('status') == 'non-compliant'])
        unknown_controls = len([r for r in results if r.get('status') == 'unknown'])
        
        compliance_percentage = (compliant_controls / total_controls * 100) if total_controls > 0 else 0
        
        return {
            "overall_percentage": round(compliance_percentage, 1),
            "total_controls": total_controls,
            "compliant_controls": compliant_controls,
            "non_compliant_controls": non_compliant_controls,
            "unknown_controls": unknown_controls,
            "assessment_timestamp": datetime.now().isoformat() + "Z"
        }
    
    def _generate_uuid(self) -> str:
        """Generera UUID för OSCAL elements"""
        import uuid
        return str(uuid.uuid4())

# Continuous Compliance Monitoring
class OSCALContinuousCompliance:
    """
    Continuous compliance monitoring med OSCAL integration
    """
    
    def __init__(self, ssp_file: str):
        self.ssp_file = ssp_file
        self.assessment_engine = OSCALAssessmentEngine(ssp_file, "assessment-plan.json")
        
    def run_daily_compliance_check(self):
        """Daglig compliance check"""
        
        print("Kör daglig OSCAL compliance assessment...")
        
        assessment_results = self.assessment_engine.execute_assessment()
        
        # Spara results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"assessment-results-{timestamp}.json"
        
        with open(results_file, 'w') as f:
            json.dump(assessment_results, f, indent=2, ensure_ascii=False)
        
        # Analysera results och skicka notifications
        self._analyze_and_notify(assessment_results)
        
        return assessment_results
    
    def _analyze_and_notify(self, assessment_results: Dict):
        """Analysera assessment results och skicka notifications"""
        
        compliance_score = assessment_results['assessment-results']['compliance-score']
        
        critical_findings = []
        high_findings = []
        
        for result in assessment_results['assessment-results']['results']:
            for finding in result.get('findings', []):
                if finding.get('severity') == 'critical':
                    critical_findings.append(finding)
                elif finding.get('severity') == 'high':
                    high_findings.append(finding)
        
        # Notification logic
        if critical_findings:
            self._send_critical_alert(critical_findings, compliance_score)
        elif high_findings:
            self._send_high_severity_alert(high_findings, compliance_score)
        elif compliance_score['overall_percentage'] < 95:
            self._send_compliance_warning(compliance_score)
        else:
            self._send_compliance_ok(compliance_score)
    
    def _send_critical_alert(self, findings: List[Dict], score: Dict):
        """Skicka critical security alert"""
        print(f"🚨 CRITICAL SECURITY ALERT: {len(findings)} critical findings detected!")
        print(f"Overall compliance: {score['overall_percentage']}%")
        
    def _send_high_severity_alert(self, findings: List[Dict], score: Dict):
        """Skicka high severity alert"""
        print(f"⚠️ HIGH SEVERITY ALERT: {len(findings)} high severity findings detected!")
        print(f"Overall compliance: {score['overall_percentage']}%")
        
    def _send_compliance_warning(self, score: Dict):
        """Skicka compliance warning"""
        print(f"⚠️ COMPLIANCE WARNING: Overall compliance {score['overall_percentage']}% below threshold")
        
    def _send_compliance_ok(self, score: Dict):
        """Skicka compliance OK notification"""
        print(f"✅ COMPLIANCE OK: Overall compliance {score['overall_percentage']}%")
```

### OSCAL-integration med CI/CD pipelines

För att maximera värdet av OSCAL-implementation måste security assessments och compliance validation integreras seamlessly i development workflows. Detta möjliggör shift-left security practices där säkerhetsproblem upptäcks och addresseras tidigt i utvecklingscykeln.

```yaml
# .github/workflows/oscal-compliance-pipeline.yml
name: OSCAL Compliance Pipeline

on:
  push:
    branches: [main, develop]
    paths: ['infrastructure/**', 'oscal/**']
  pull_request:
    branches: [main]
    paths: ['infrastructure/**', 'oscal/**']

jobs:
  oscal-validation:
    runs-on: ubuntu-latest
    name: OSCAL Document Validation
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          
      - name: Install OSCAL CLI Tools
        run: |
          pip install oscal-tools
          wget https://github.com/usnistgov/oscal-cli/releases/latest/download/oscal-cli.jar
          
      - name: Validate OSCAL Documents
        run: |
          # Validera alla OSCAL JSON-dokument
          for file in oscal/*.json; do
            echo "Validating $file..."
            java -jar oscal-cli.jar validate "$file"
          done
          
      - name: Generate Assessment Plan
        run: |
          python scripts/generate_assessment_plan.py \
            --profile oscal/svenska-enterprise-profile.json \
            --output oscal/assessment-plan.json

  infrastructure-compliance:
    runs-on: ubuntu-latest
    name: Infrastructure Compliance Assessment
    needs: oscal-validation
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: eu-north-1
          
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: 1.6.0
          
      - name: Terraform Plan
        working-directory: infrastructure
        run: |
          terraform init
          terraform plan -out=tfplan.binary
          terraform show -json tfplan.binary > tfplan.json
          
      - name: Generate OSCAL SSP
        run: |
          python scripts/oscal_ssp_generator.py \
            --terraform-dir infrastructure \
            --component-definitions oscal/components \
            --profile oscal/svenska-enterprise-profile.json \
            --output oscal/system-security-plan.json
            
      - name: Run OSCAL Assessment
        run: |
          python scripts/oscal_assessment_automation.py \
            --ssp oscal/system-security-plan.json \
            --assessment-plan oscal/assessment-plan.json \
            --output oscal/assessment-results.json
            
      - name: Analyze Compliance Results
        run: |
          python scripts/analyze_compliance.py \
            --results oscal/assessment-results.json \
            --threshold 95 \
            --output compliance-report.json
            
      - name: Upload OSCAL Artifacts
        uses: actions/upload-artifact@v3
        with:
          name: oscal-artifacts
          path: |
            oscal/system-security-plan.json
            oscal/assessment-results.json
            compliance-report.json
            
      - name: Comment PR with Compliance Results
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const complianceReport = JSON.parse(fs.readFileSync('compliance-report.json'));
            
            const compliance = complianceReport.compliance_score;
            const criticalFindings = complianceReport.critical_findings || [];
            const highFindings = complianceReport.high_findings || [];
            
            let statusEmoji = '✅';
            let statusText = 'COMPLIANT';
            
            if (criticalFindings.length > 0) {
              statusEmoji = '🚨';
              statusText = 'CRITICAL ISSUES';
            } else if (highFindings.length > 0) {
              statusEmoji = '⚠️';
              statusText = 'HIGH SEVERITY ISSUES';
            } else if (compliance.overall_percentage < 95) {
              statusEmoji = '⚠️';  
              statusText = 'BELOW THRESHOLD';
            }
            
            const comment = `
            ## ${statusEmoji} OSCAL Compliance Assessment
            
            **Overall Status:** ${statusText}  
            **Compliance Score:** ${compliance.overall_percentage}%
            
            ### Summary
            - **Total Controls:** ${compliance.total_controls}
            - **Compliant:** ${compliance.compliant_controls}
            - **Non-Compliant:** ${compliance.non_compliant_controls}
            - **Unknown:** ${compliance.unknown_controls}
            
            ${criticalFindings.length > 0 ? `
            ### 🚨 Critical Findings (${criticalFindings.length})
            ${criticalFindings.slice(0, 5).map(f => `- **${f.title}**: ${f.description}`).join('\n')}
            ${criticalFindings.length > 5 ? `\n*... och ${criticalFindings.length - 5} fler critical findings*` : ''}
            ` : ''}
            
            ${highFindings.length > 0 ? `
            ### ⚠️ High Severity Findings (${highFindings.length})
            ${highFindings.slice(0, 3).map(f => `- **${f.title}**: ${f.description}`).join('\n')}
            ${highFindings.length > 3 ? `\n*... och ${highFindings.length - 3} fler high severity findings*` : ''}
            ` : ''}
            
            ### 📋 Regulatory Compliance
            - **GDPR:** ${complianceReport.regulatory_compliance?.gdpr || 'Unknown'}
            - **MSB:** ${complianceReport.regulatory_compliance?.msb || 'Unknown'}
            - **ISO 27001:** ${complianceReport.regulatory_compliance?.iso27001 || 'Unknown'}
            
            ---
            
            *Assessment performed using OSCAL automation at ${new Date().toISOString()}*
            `;
            
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: comment
            });
            
      - name: Fail on Critical Issues
        run: |
          python -c "
          import json
          with open('compliance-report.json') as f:
              report = json.load(f)
          critical_count = len(report.get('critical_findings', []))
          if critical_count > 0:
              print(f'❌ Found {critical_count} critical security findings. Failing build.')
              exit(1)
          else:
              print('✅ No critical security findings detected.')
          "

  continuous-monitoring:
    runs-on: ubuntu-latest
    name: Setup Continuous Monitoring
    if: github.ref == 'refs/heads/main'
    needs: [infrastructure-compliance]
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy Compliance Monitoring
        run: |
          # Deploy CloudWatch dashboard för compliance monitoring
          aws cloudformation deploy \
            --template-file monitoring/oscal-compliance-dashboard.yaml \
            --stack-name oscal-compliance-monitoring \
            --capabilities CAPABILITY_IAM \
            --region eu-north-1
            
      - name: Schedule Daily Assessments
        run: |
          # Skapa EventBridge rule för dagliga assessments
          aws events put-rule \
            --name daily-oscal-assessment \
            --schedule-expression "cron(0 6 * * ? *)" \
            --description "Daily OSCAL compliance assessment"
```

OSCAL representerar framtiden för säkerhetsautomatisering och compliance management inom Infrastructure as Code. För svenska organisationer som måste balansera regulatory compliance med innovation velocity erbjuder OSCAL en path forward som möjliggör både enhanced security och operational efficiency.

## Gatekeeper och Kubernetes Policy Enforcement: Enterprise-grade implementationer

Kubernetes-miljöer representerar en unik utmaning för policy enforcement på grund av deras dynamiska natur och complex orchestration patterns. Gatekeeper, baserat på OPA, har framträtt som den ledande lösningen för Kubernetes admission control, möjliggör comprehensive policy enforcement som integreras seamlessly med Kubernetes-native workflows.

För svenska organisationer som adopterar containerisering och Kubernetes som central del av sin Infrastructure as Code-strategi, representerar Gatekeeper en critical capability för att säkerställa att säkerhetspolicies enforcement automatiskt över alla deployments, oavsett development team eller application complexity.

Gatekeeper's admission controller architecture möjliggör policy evaluation vid deployment-time, vilket förhindrar non-compliant workloads från att någonsin nå production. Denna proactive approach är fundamental för svenska organisationer som måste demonstrera preventive controls till regulators och maintain continuous compliance.

### Enterprise Constraint Template design

Constraint Templates i Gatekeeper fungerar som reusable policy definitions som kan konfigureras med parametrar för different environments och use cases. För svenska enterprise-miljöer kräver constraint templates sophisticated logic som kan hantera complex regulatory requirements samtidigt som de ger development teams tillräcklig flexibilitet för innovation.

```yaml
# gatekeeper/swedish-enterprise-constraints.yaml
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: swedishenterprisesecurity
  annotations:
    description: "Comprehensive svenska enterprise säkerhetskrav för Kubernetes workloads"
    compliance.frameworks: "GDPR,MSB,ISO27001"
spec:
  crd:
    spec:
      names:
        kind: SwedishEnterpriseSecurity
      validation:
        openAPIV3Schema:
          type: object
          properties:
            gdprDataClassification:
              type: object
              properties:
                required:
                  type: boolean
                  default: true
                allowedValues:
                  type: array
                  items:
                    type: string
                  default: ["public", "internal", "confidential", "personal"]
            resourceLimits:
              type: object
              properties:
                enforceMemoryLimits:
                  type: boolean
                  default: true
                enforceCPULimits:
                  type: boolean  
                  default: true
                maxMemoryPerContainer:
                  type: string
                  default: "2Gi"
                maxCPUPerContainer:
                  type: string
                  default: "1000m"
            networkSecurity:
              type: object
              properties:
                requireNetworkPolicies:
                  type: boolean
                  default: true
                allowedRegistries:
                  type: array
                  items:
                    type: string
                prohibitedPorts:
                  type: array
                  items:
                    type: integer
                  default: [22, 23, 135, 445, 1433, 3306, 3389, 5432, 6379, 27017]
            auditLogging:
              type: object
              properties:
                requireAuditAnnotations:
                  type: boolean
                  default: true
                requiredAnnotations:
                  type: array
                  items:
                    type: string
                  default: ["se.audit.owner", "se.audit.purpose", "se.audit.dataflow"]
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package swedishenterprisesecurity
        
        import rego.v1
        
        # GDPR Data Classification Enforcement
        violation[{"msg": msg}] {
          input.review.object.kind in ["Pod", "Deployment", "StatefulSet", "DaemonSet"]
          input.parameters.gdprDataClassification.required
          object_meta := get_object_metadata(input.review.object)
          not object_meta.labels["se.gdpr.dataclassification"]
          msg := "Workload måste ha GDPR dataklassificering label enligt svenska regelverk"
        }
        
        violation[{"msg": msg}] {
          input.review.object.kind in ["Pod", "Deployment", "StatefulSet", "DaemonSet"]
          input.parameters.gdprDataClassification.required
          object_meta := get_object_metadata(input.review.object)
          classification := object_meta.labels["se.gdpr.dataclassification"]
          not classification in input.parameters.gdprDataClassification.allowedValues
          msg := sprintf("GDPR dataklassificering '%v' är inte tillåten. Tillåtna värden: %v", [classification, input.parameters.gdprDataClassification.allowedValues])
        }
        
        # Resource Limits enligt svenska säkerhetspraxis
        violation[{"msg": msg}] {
          input.review.object.kind == "Pod"
          input.parameters.resourceLimits.enforceMemoryLimits
          container := input.review.object.spec.containers[_]
          not container.resources.limits.memory
          msg := sprintf("Container '%v' måste ha memory limits för säker resurshantering", [container.name])
        }
        
        violation[{"msg": msg}] {
          input.review.object.kind == "Pod"
          input.parameters.resourceLimits.enforceCPULimits
          container := input.review.object.spec.containers[_]
          not container.resources.limits.cpu
          msg := sprintf("Container '%v' måste ha CPU limits för säker resurshantering", [container.name])
        }
        
        # Excessive Resource Usage Prevention
        violation[{"msg": msg}] {
          input.review.object.kind == "Pod"
          container := input.review.object.spec.containers[_]
          memory_limit := container.resources.limits.memory
          memory_limit
          exceeds_memory_limit(memory_limit, input.parameters.resourceLimits.maxMemoryPerContainer)
          msg := sprintf("Container '%v' memory limit %v överskrider tillåtet maximum %v", [container.name, memory_limit, input.parameters.resourceLimits.maxMemoryPerContainer])
        }
        
        # Container Security Context Enforcement
        violation[{"msg": msg}] {
          input.review.object.kind == "Pod"
          container := input.review.object.spec.containers[_]
          not container.securityContext.runAsNonRoot
          msg := sprintf("Container '%v' måste köras som non-root användare enligt MSB säkerhetskrav", [container.name])
        }
        
        violation[{"msg": msg}] {
          input.review.object.kind == "Pod"
          container := input.review.object.spec.containers[_]
          not container.securityContext.readOnlyRootFilesystem
          msg := sprintf("Container '%v' måste använda read-only root filesystem för förbättrad säkerhet", [container.name])
        }
        
        violation[{"msg": msg}] {
          input.review.object.kind == "Pod"
          container := input.review.object.spec.containers[_]
          container.securityContext.privileged
          msg := sprintf("Container '%v' får inte köras i privileged mode enligt säkerhetspolicy", [container.name])
        }
        
        # Network Security Enforcement
        violation[{"msg": msg}] {
          input.review.object.kind == "Pod"
          container := input.review.object.spec.containers[_]
          port := container.ports[_]
          port.containerPort in input.parameters.networkSecurity.prohibitedPorts
          msg := sprintf("Container '%v' försöker exponera prohibited port %v", [container.name, port.containerPort])
        }
        
        # Image Registry Validation
        violation[{"msg": msg}] {
          input.review.object.kind == "Pod"
          container := input.review.object.spec.containers[_]
          image := container.image
          not allowed_registry(image, input.parameters.networkSecurity.allowedRegistries)
          msg := sprintf("Container '%v' använder image från otillåten registry: %v", [container.name, image])
        }
        
        # Audit Annotation Requirements
        violation[{"msg": msg}] {
          input.review.object.kind in ["Pod", "Deployment", "StatefulSet", "DaemonSet"]
          input.parameters.auditLogging.requireAuditAnnotations
          object_meta := get_object_metadata(input.review.object)
          required_annotation := input.parameters.auditLogging.requiredAnnotations[_]
          not object_meta.annotations[required_annotation]
          msg := sprintf("Workload måste ha audit annotation '%v' för compliance tracking", [required_annotation])
        }
        
        # Service Account Security
        violation[{"msg": msg}] {
          input.review.object.kind == "Pod"
          input.review.object.spec.serviceAccountName == "default"
          msg := "Pod får inte använda default service account - skapa dedicated service account"
        }
        
        violation[{"msg": msg}] {
          input.review.object.kind == "Pod"
          input.review.object.spec.automountServiceAccountToken != false
          not input.review.object.spec.serviceAccountName
          msg := "Pod måste explicit disable automountServiceAccountToken eller använda named service account"
        }
        
        # Helper functions
        get_object_metadata(obj) := obj.metadata {
          obj.kind == "Pod"
        }
        
        get_object_metadata(obj) := obj.spec.template.metadata {
          obj.kind in ["Deployment", "StatefulSet", "DaemonSet"]
        }
        
        exceeds_memory_limit(actual, max_allowed) {
          actual_bytes := parse_memory(actual)
          max_bytes := parse_memory(max_allowed)
          actual_bytes > max_bytes
        }
        
        parse_memory(mem_str) := bytes {
          # Simplified memory parsing - production should handle all units
          endswith(mem_str, "Gi")
          gb := to_number(trim_suffix(mem_str, "Gi"))
          bytes := gb * 1024 * 1024 * 1024
        }
        
        parse_memory(mem_str) := bytes {
          endswith(mem_str, "Mi")
          mb := to_number(trim_suffix(mem_str, "Mi"))
          bytes := mb * 1024 * 1024
        }
        
        allowed_registry(image, allowed_registries) {
          registry := allowed_registries[_]
          startswith(image, registry)
        }

---
# Production Constraint Instance för svenska enterprise miljöer
apiVersion: config.gatekeeper.sh/v1alpha1
kind: SwedishEnterpriseSecurity
metadata:
  name: production-security-policy
  namespace: gatekeeper-system
spec:
  enforcementAction: deny  # Strict enforcement för production
  match:
    - apiGroups: [""]
      kinds: ["Pod"]
      namespaces: ["production", "staging"]
    - apiGroups: ["apps"]
      kinds: ["Deployment", "StatefulSet", "DaemonSet"]
      namespaces: ["production", "staging"]
  parameters:
    gdprDataClassification:
      required: true
      allowedValues: ["internal", "confidential", "personal"]
    resourceLimits:
      enforceMemoryLimits: true
      enforceCPULimits: true
      maxMemoryPerContainer: "8Gi"
      maxCPUPerContainer: "4000m"
    networkSecurity:
      requireNetworkPolicies: true
      allowedRegistries: 
        - "harbor.company.se/"
        - "gcr.io/company-project/"
        - "eu.gcr.io/company-project/"
      prohibitedPorts: [22, 23, 135, 445, 1433, 3306, 3389, 5432, 6379, 27017]
    auditLogging:
      requireAuditAnnotations: true
      requiredAnnotations: 
        - "se.audit.owner"
        - "se.audit.purpose" 
        - "se.audit.dataflow"
        - "se.compliance.framework"

---
# Development Environment Constraint (mindre strikt)
apiVersion: config.gatekeeper.sh/v1alpha1
kind: SwedishEnterpriseSecurity
metadata:
  name: development-security-policy
  namespace: gatekeeper-system
spec:
  enforcementAction: warn  # Warning mode för development
  match:
    - apiGroups: [""]
      kinds: ["Pod"]
      namespaces: ["development", "test"]
    - apiGroups: ["apps"]
      kinds: ["Deployment", "StatefulSet", "DaemonSet"]
      namespaces: ["development", "test"]
  parameters:
    gdprDataClassification:
      required: true
      allowedValues: ["public", "internal", "confidential", "personal"]
    resourceLimits:
      enforceMemoryLimits: true
      enforceCPULimits: false  # Mindre strikt för development
      maxMemoryPerContainer: "16Gi"
      maxCPUPerContainer: "8000m"
    networkSecurity:
      requireNetworkPolicies: false
      allowedRegistries: 
        - "harbor.company.se/"
        - "gcr.io/company-project/"
        - "docker.io/"  # Tillåt public images för development
      prohibitedPorts: [22, 23, 135, 445]  # Endast kritiska portar
    auditLogging:
      requireAuditAnnotations: false  # Optional för development
```

### Network Policy automation och enforcement

Kubernetes Network Policies utgör en fundamental säkerhetskomponent för micro-segmentation, men their manual configuration är error-prone och svår att maintain i large-scale environments. Svenska organisationer kräver automated network policy generation och enforcement som säkerställer proper network segmentation samtidigt som den ger development teams flexibility.

```yaml
# gatekeeper/network-policy-constraint.yaml
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: swedishnetworkpolicyenforcement
spec:
  crd:
    spec:
      names:
        kind: SwedishNetworkPolicyEnforcement
      validation:
        openAPIV3Schema:
          type: object
          properties:
            requireNetworkPolicy:
              type: boolean
              default: true
            allowedNamespaces:
              type: array
              items:
                type: string
            blockedCommunication:
              type: array
              items:
                type: object
                properties:
                  from:
                    type: string
                  to:
                    type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package swedishnetworkpolicyenforcement
        
        import rego.v1
        
        # Kräv NetworkPolicy för alla namespaces med känslig data
        violation[{"msg": msg}] {
          input.review.object.kind == "Namespace"
          namespace_name := input.review.object.metadata.name
          classification := input.review.object.metadata.labels["se.gdpr.dataclassification"]
          classification in ["confidential", "personal"]
          input.parameters.requireNetworkPolicy
          not has_network_policy(namespace_name)
          msg := sprintf("Namespace '%v' med dataklassificering '%v' måste ha NetworkPolicy", [namespace_name, classification])
        }
        
        # Förhindra workloads i namespaces utan NetworkPolicies
        violation[{"msg": msg}] {
          input.review.object.kind in ["Pod", "Deployment", "StatefulSet"]
          namespace_name := input.review.object.metadata.namespace
          input.parameters.requireNetworkPolicy
          not namespace_excluded(namespace_name)
          not has_network_policy(namespace_name)
          msg := sprintf("Workloads kan inte deployeras i namespace '%v' utan NetworkPolicy", [namespace_name])
        }
        
        has_network_policy(namespace) {
          # Detta skulle behöva kompletteras med actual NetworkPolicy lookup
          # För demonstration antar vi att namespaces med vissa labels har policies
          data.kubernetes.networkpolicies[namespace]
        }
        
        namespace_excluded(namespace) {
          excluded_namespaces := {"kube-system", "kube-public", "gatekeeper-system", "monitoring"}
          namespace in excluded_namespaces
        }

---
# Automated NetworkPolicy generation för svenska organisationer
apiVersion: v1
kind: ConfigMap
metadata:
  name: network-policy-templates
  namespace: gatekeeper-system
data:
  default-deny-all.yaml: |
    apiVersion: networking.k8s.io/v1
    kind: NetworkPolicy
    metadata:
      name: default-deny-all
      namespace: {{.Namespace}}
      labels:
        se.policy.type: "default-deny"
        se.compliance.framework: "MSB"
    spec:
      podSelector: {}
      policyTypes:
      - Ingress
      - Egress
      
  allow-same-namespace.yaml: |
    apiVersion: networking.k8s.io/v1
    kind: NetworkPolicy
    metadata:
      name: allow-same-namespace
      namespace: {{.Namespace}}
      labels:
        se.policy.type: "namespace-isolation"
    spec:
      podSelector: {}
      policyTypes:
      - Ingress
      - Egress
      ingress:
      - from:
        - namespaceSelector:
            matchLabels:
              name: {{.Namespace}}
      egress:
      - to:
        - namespaceSelector:
            matchLabels:
              name: {{.Namespace}}
              
  allow-dns.yaml: |
    apiVersion: networking.k8s.io/v1
    kind: NetworkPolicy
    metadata:
      name: allow-dns
      namespace: {{.Namespace}}
    spec:
      podSelector: {}
      policyTypes:
      - Egress
      egress:
      - to: []
        ports:
        - protocol: UDP
          port: 53
```

### Gatekeeper monitoring och observability

För svenska enterprise-miljöer är comprehensive monitoring av policy enforcement critical för både security operations och compliance demonstrering. Gatekeeper måste integreras med existing monitoring infrastructure för real-time alerting och audit trail generation.

```yaml
# monitoring/gatekeeper-monitoring.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: gatekeeper-controller-manager
  namespace: gatekeeper-system
  labels:
    app: gatekeeper
    se.monitoring.team: "security"
spec:
  selector:
    matchLabels:
      control-plane: controller-manager
      gatekeeper.sh/operation: webhook
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics
    
---
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: gatekeeper-security-alerts
  namespace: gatekeeper-system
  labels:
    se.alerting.severity: "critical"
spec:
  groups:
  - name: gatekeeper.security
    rules:
    - alert: GatekeeperPolicyViolationHigh
      expr: increase(gatekeeper_violations_total[5m]) > 10
      for: 2m
      labels:
        severity: warning
        team: security
        compliance: "GDPR,MSB"
      annotations:
        summary: "Hög frekvens av Gatekeeper policy violations"
        description: "{{ $value }} policy violations de senaste 5 minuterna"
        runbook_url: "https://wiki.company.se/gatekeeper-violations"
        
    - alert: GatekeeperWebhookDown
      expr: up{job="gatekeeper-webhook"} == 0
      for: 1m
      labels:
        severity: critical
        team: security
      annotations:
        summary: "Gatekeeper webhook är inte tillgänglig"
        description: "Gatekeeper admission webhook är ned - säkerhetspolicies enforces inte"
        action: "Kontrollera Gatekeeper controller status omedelbart"
        
    - alert: GatekeeperConstraintViolations
      expr: |
        increase(gatekeeper_violations_total{
          violation_kind="SwedishEnterpriseSecurity"
        }[10m]) > 5
      for: 5m
      labels:
        severity: high
        team: security
        regulation: "svenska-compliance"
      annotations:
        summary: "Svenska säkerhetskrav violations upptäckta"
        description: "{{ $value }} violations av svenska enterprise säkerhetskrav"
        compliance_impact: "Potentiell GDPR/MSB compliance risk"
        
---
# Grafana Dashboard ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: gatekeeper-dashboard
  namespace: monitoring
data:
  gatekeeper-security.json: |
    {
      "dashboard": {
        "title": "Gatekeeper Säkerhet och Compliance",
        "tags": ["security", "compliance", "svenska"],
        "panels": [
          {
            "title": "Policy Violations över tid",
            "type": "graph",
            "targets": [
              {
                "expr": "rate(gatekeeper_violations_total[5m])",
                "legendFormat": "{{ violation_kind }} violations/min"
              }
            ],
            "alert": {
              "conditions": [
                {
                  "query": {"params": ["A", "5m", "now"]},
                  "reducer": {"type": "avg"},
                  "evaluator": {"params": [5], "type": "gt"}
                }
              ],
              "executionErrorState": "alerting",
              "for": "5m",
              "frequency": "10s",
              "handler": 1,
              "name": "Policy Violations Alert",
              "noDataState": "no_data"
            }
          },
          {
            "title": "Compliance Status per Namespace",
            "type": "table",
            "targets": [
              {
                "expr": "gatekeeper_compliance_score_by_namespace",
                "format": "table"
              }
            ]
          },
          {
            "title": "GDPR Dataklassificering Coverage",
            "type": "pie",
            "targets": [
              {
                "expr": "count by (dataclassification) (kube_pod_labels{label_se_gdpr_dataclassification!=\"\"})"
              }
            ]
          }
        ]
      }
    }

## Automatiserad Compliance Monitoring och Enterprise Observability

Kontinuerlig compliance monitoring utgör ryggraden i moderna Policy as Code-implementationer för svenska enterprise-miljöer. Effective monitoring går betydligt längre än traditional logging och omfattar real-time policy evaluation, predictive compliance analysis och automated remediation capabilities som säkerställer att organisationer maintainar regulatory adherence även när infrastructure evolves rapidly.

Svenska organisationer möter unique monitoring challenges på grund av strikta regulatory requirements kring data residency, audit trails och incident reporting. GDPR-compliance kräver comprehensive logging av all data processing activities, medan MSB:s säkerhetskrav för kritisk infrastruktur mandatar real-time threat detection och rapid incident response capabilities.

Modern compliance monitoring platforms för Infrastructure as Code integrerar multiple data sources: infrastructure state från cloud providers, policy evaluation results från OPA/Gatekeeper, application logs från containerized workloads, och security events från SIEM systems. Denna comprehensive observability möjliggör holistic security posture assessment och enables proactive risk management.

### Enterprise Compliance Observability Platform

```python
# monitoring/enterprise_compliance_platform.py
import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import boto3
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from elasticsearch import Elasticsearch
from prometheus_client import CollectorRegistry, Gauge, Counter, push_to_gateway
import streamlit as st

@dataclass
class ComplianceMetric:
    """Compliance metric representation"""
    name: str
    value: float
    timestamp: datetime
    framework: str  # GDPR, MSB, ISO27001, etc.
    severity: str
    source: str
    metadata: Dict[str, Any]

@dataclass 
class PolicyViolationEvent:
    """Policy violation event representation"""
    id: str
    timestamp: datetime
    resource_id: str
    resource_type: str
    policy_name: str
    violation_type: str
    severity: str
    message: str
    regulation_reference: str
    remediation_suggestion: str
    auto_remediable: bool
    compliance_impact: Dict[str, Any]

class EnterpriseCompliancePlatform:
    """
    Comprehensive compliance monitoring platform för svenska enterprise-miljöer
    """
    
    def __init__(self, config_file: str = "compliance-platform-config.json"):
        with open(config_file, 'r') as f:
            self.config = json.load(f)
            
        # Initialize clients
        self.aws_config = boto3.client('config')
        self.aws_cloudwatch = boto3.client('cloudwatch')
        self.aws_cloudtrail = boto3.client('cloudtrail')
        self.elasticsearch = Elasticsearch(self.config['elasticsearch']['hosts'])
        
        # Metrics registry
        self.metrics_registry = CollectorRegistry()
        self.setup_metrics()
        
        # Logging setup
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def setup_metrics(self):
        """Setup Prometheus metrics för compliance monitoring"""
        self.compliance_score_gauge = Gauge(
            'compliance_score_by_framework',
            'Compliance score per regulatory framework',
            ['framework', 'environment'],
            registry=self.metrics_registry
        )
        
        self.policy_violations_counter = Counter(
            'policy_violations_total',
            'Total policy violations',
            ['severity', 'framework', 'resource_type'],
            registry=self.metrics_registry
        )
        
        self.remediation_success_gauge = Gauge(
            'automated_remediation_success_rate',
            'Success rate för automated remediation',
            ['remediation_type'],
            registry=self.metrics_registry
        )
    
    async def run_continuous_monitoring(self):
        """Main loop för continuous compliance monitoring"""
        self.logger.info("🚀 Starting continuous compliance monitoring...")
        
        while True:
            try:
                # Parallel execution av monitoring tasks
                monitoring_tasks = [
                    self.monitor_aws_config_compliance(),
                    self.monitor_kubernetes_policies(),
                    self.monitor_terraform_state_drift(),
                    self.monitor_data_sovereignty_compliance(),
                    self.analyze_security_posture_trends(),
                    self.check_automated_remediation_status()
                ]
                
                results = await asyncio.gather(*monitoring_tasks, return_exceptions=True)
                
                # Process results och update metrics
                await self.process_monitoring_results(results)
                
                # Update dashboards
                await self.update_compliance_dashboards()
                
                # Check för alerts
                await self.evaluate_alerting_conditions()
                
                # Sleep före next iteration
                await asyncio.sleep(self.config['monitoring']['interval_seconds'])
                
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(60)  # Retry after 1 minute
```

Implementation av comprehensive Policy as Code i svenska enterprise-miljöer kräver systematic approach som respekterar existing organizational structures samtidigt som den introducerar modern automation capabilities. Successful implementations karakteriseras av gradual adoption, strong stakeholder buy-in och careful integration med existing governance frameworks.

### Integration med svenska säkerhetsmyndigheter

För organisationer inom kritisk infrastruktur kräver compliance monitoring integration med svenska säkerhetsmyndigheter och automated incident reporting capabilities. Detta inkluderar integration med MSB:s incidentrapporteringssystem och automated generation av compliance reports för regulatory authorities.

```python
# integration/swedish_authorities_integration.py
import json
import asyncio
from datetime import datetime
from typing import Dict, List
import requests
from cryptography.fernet import Fernet

class SwedishAuthoritiesIntegration:
    """
    Integration med svenska säkerhetsmyndigheter för compliance reporting
    """
    
    def __init__(self):
        self.msb_api_endpoint = "https://api.msb.se/incident-reporting/v2"
        self.fi_api_endpoint = "https://api.fi.se/compliance-reporting/v1"
        self.encryption_key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.encryption_key)
        
    async def report_security_incident_to_msb(self, incident_data: Dict) -> Dict:
        """Report säkerhetsincident till MSB enligt MSBFS 2020:6"""
        
        # Encrypt sensitive data
        encrypted_data = self._encrypt_sensitive_data(incident_data)
        
        msb_report = {
            "incident_id": incident_data['id'],
            "timestamp": datetime.now().isoformat(),
            "severity": self._map_severity_to_msb_scale(incident_data['severity']),
            "affected_systems": encrypted_data['systems'],
            "incident_type": incident_data['type'],
            "impact_assessment": {
                "confidentiality": incident_data.get('impact', {}).get('confidentiality', 'unknown'),
                "integrity": incident_data.get('impact', {}).get('integrity', 'unknown'),
                "availability": incident_data.get('impact', {}).get('availability', 'unknown')
            },
            "remediation_actions": incident_data.get('remediation', []),
            "lessons_learned": incident_data.get('lessons_learned', ''),
            "regulatory_compliance": {
                "gdpr_relevant": incident_data.get('gdpr_impact', False),
                "personal_data_affected": incident_data.get('personal_data_count', 0)
            }
        }
        
        try:
            response = await self._send_to_msb(msb_report)
            return {"status": "success", "msb_reference": response.get('reference_id')}
        except Exception as e:
            return {"status": "error", "message": str(e)}
```

## Praktiska implementationsexempel och svenska organisationer

Implementation av comprehensive Policy as Code i svenska enterprise-miljöer kräver systematic approach som respekterar existing organizational structures samtidigt som den introducerar modern automation capabilities. Successful implementations karakteriseras av gradual adoption, strong stakeholder buy-in och careful integration med existing governance frameworks.

Svenska organisationer som har successful implementerat Policy as Code har typically följt en phased approach: börjat med non-critical environments för experimentation, byggt up policy libraries gradually och establish proven governance processes innan rollout till production environments. Denna approach minimerar risk samtidigt som den ger teams tid att develop competence och confidence med new tools och processes.

### Implementation roadmap för svenska organisationer

**Fas 1: Foundation och Planning (Månader 1-3)**
- Stakeholder alignment och executive buy-in
- Regulatory requirements mapping (GDPR, MSB, branschspecifika krav)
- Technical architecture planning och tool selection
- Team training och competence development
- Pilot project selection och planning

**Fas 2: Pilot Implementation (Månader 4-6)**
- Non-production environment implementation
- Basic policy library development
- CI/CD pipeline integration
- Monitoring och alerting setup
- Initial automation development

**Fas 3: Production Rollout (Månader 7-12)**
- Production environment deployment
- Comprehensive policy coverage
- Advanced automation implementation
- Integration med existing SIEM/monitoring systems
- Compliance reporting automation

**Fas 4: Optimization och Scale (Månader 13+)**
- Advanced policy analytics
- Predictive compliance monitoring
- Cross-organization policy sharing
- Continuous improvement processes
- Advanced automation capabilities

## Sammanfattning och framtidsperspektiv

Policy as Code representerar en fundamental transformation inom Infrastructure as Code som möjliggör automated governance, enhanced security och consistent regulatory compliance. För svenska organisationer erbjuder denna approach unprecedented capabilities för att hantera complex compliance landscapes samtidigt som development velocity maintainas.

Integration av OSCAL (Open Security Controls Assessment Language) med traditional Policy as Code approaches skapar powerful synergies som möjliggör standardized security control representation, automated compliance assessment och seamless integration mellan olika security tools. Svenska organisationer som adopterar OSCAL-based approaches positionerar sig för framtida regulatory changes och growing compliance complexity.

Successful Policy as Code implementation kräver more än technology - det kräver organizational commitment, cultural change och systematic approach till governance automation. Svenska organisationer som investerar i comprehensive Policy as Code capabilities uppnår significant benefits: reduced manual oversight, faster compliance responses, improved security posture och enhanced ability att demonstrate regulatory adherence.

Framtiden för Policy as Code inom svenska organisationer karakteriseras av continued evolution toward intelligent automation, predictive compliance analytics och seamless integration med emerging technologies som artificial intelligence och machine learning. Organizations som etablerar strong Policy as Code foundations idag kommer vara well-positioned för dessa future developments.

Det continuing utvecklandet av regulatory frameworks, combined med increasing sophistication av cyber threats, gör Policy as Code essential för alla svenska organisationer som opererar within regulated industries. Investment i Policy as Code capabilities delivers compounding returns genom improved security, reduced compliance costs och enhanced operational efficiency.

Som vi move forward till [kapitel 12 om compliance och regelefterlevnad](12_compliance.md), bygger vi vidare på dessa technical foundations för att explore organizational och processaspekter av comprehensive governance strategy, med particular focus på svenska regulatory environment och practical implementation guidance.

## Källor och referenser

- Open Policy Agent Community. "OPA Policy as Code Best Practices." OPA Documentation, 2024.
- NIST. "OSCAL - Open Security Controls Assessment Language." NIST Special Publication, 2024.
- Kubernetes SIG Security. "Gatekeeper Policy Engine Architecture Guide." CNCF Documentation, 2024.
- European Union. "GDPR Implementation Guidelines för Cloud Infrastructure." EU Publications, 2024.
- Myndigheten för samhällsskydd och beredskap. "MSBFS 2020:6 - Säkerhetskrav för kritisk infrastruktur." MSB Föreskrifter, 2024.
- HashiCorp. "Terraform Sentinel Policy Framework." HashiCorp Enterprise Documentation, 2024.
- Cloud Security Alliance. "Policy as Code Implementation Guidelines." CSA Publications, 2024.
- ISO/IEC 27001:2022. "Information Security Management Systems - Requirements." International Organization for Standardization, 2024.

## Praktiska implementationsexempel

Verkliga implementationer av Policy as Code kräver integration med befintliga utvecklingsverktyg och processer. Genom att bygga policy validation i CI/CD pipelines säkerställs att compliance kontrolleras automatiskt innan infrastrukturändringar deployeras till produktion.

Enterprise-grade policy management inkluderar policy lifecycle management, version control av policies, och comprehensive audit trails av policy decisions. Detta möjliggör organizations att demonstrate compliance mot regulators och maintain consistent governance across complex infrastructure environments.

## Sammanfattning

Policy as Code representerar kritisk evolution inom Infrastructure as Code som möjliggör automated governance, security enforcement och regulatory compliance. Genom att behandla policies som kod kan organisationer uppnå samma fördelar som IaC erbjuder: version control, testing, automation och consistency.

Svenska organisationer som implementerar comprehensive Policy as Code capabilities positionerar sig starkt för future regulatory changes och growing compliance requirements. Investment i policy automation delivers compounding benefits genom reduced manual oversight, faster compliance responses och improved security posture.

Integration med nästa kapitels diskussion om [compliance och regelefterlevnad](14_kapitel13.md) bygger vidare på dessa tekniska foundations för att adressera organizational och processaspekter av comprehensive governance strategy.

## Källor och referenser

- Open Policy Agent. "Policy as Code Documentation." OPA Community, 2023.
- Kubernetes SIG Security. "Gatekeeper Policy Engine." CNCF Projects, 2023.  
- HashiCorp. "Sentinel Policy Framework." HashiCorp Enterprise, 2023.
- NIST. "Security and Privacy Controls för Information Systems." NIST Special Publication 800-53, 2023.
- European Union. "General Data Protection Regulation Implementation Guide." EU Publications, 2023.
- MSB. "Säkerhetskrav för kritisk infrastruktur." Myndigheten för samhällsskydd och beredskap, 2023.