# Säkerhet i Infrastructure as Code

![Säkerhet som kod workflow](images/diagram_06_kapitel5.png)

*Säkerhet måste integreras från början i Infrastructure as Code-processer genom automatiserad policy enforcement, kontinuerlig monitoring och proaktiv sårbarhetshantering. Diagrammet illustrerar den iterativa säkerhetsprocessen från design till produktion.*

## Övergripande beskrivning

Säkerhet inom Infrastructure as Code kräver en fundamental förskjutning från reaktiv till proaktiv säkerhetstänk. Traditionella säkerhetsmodeller som fokuserar på perimeterskydd och manuella säkerhetskontroller är otillräckliga för moderna, dynamiska molnmiljöer som byggs med IaC.

Security-by-design principer måste genomsyra hela infrastrukturdefinitionen, från initial arkitekturdesign till kontinuerlig drift och monitoring. Detta inkluderar automatiserad implementation av säkerhetspolicies, kontinuerlig sårbarhetsscanning och real-time threat detection som är inbyggd i infrastrukturkoden.

Svenska organisationer står inför unika säkerhetsutmaningar inklusive GDPR-compliance, kritisk infrastruktursskydd enligt MSB:s riktlinjer och sektorsspecifika regulatoriska krav. IaC-baserade säkerhetslösningar möjliggör consistent enforcement av dessa krav across alla miljöer och deployment-scenarier.

Modern hotlandskap kräver att säkerhetskontrollen kan anpassas snabbt till nya threats och attack vectors. Infrastructure as Code erbjuder agiliteten att implementera säkerhetsförbättringar genom kod-updates som kan deployeras konsistent och spårbart across hela organisationens infrastruktur.

## Security-by-design principer

Security-by-design innebär att säkerhetshänsyn integreras från första design-fasen av infrastrukturprojekt istället för att läggas till som en efterkonstruktion. Detta approach resulterar i mer robusta säkerhetslösningar och reducerad kostnad för säkerhetsimplementering.

Zero Trust Architecture representerar en fundamental security-by-design princip där ingen användare eller enhet trusted implicitly, oavsett location eller autentisering. IaC möjliggör systematic implementation av Zero Trust genom nätverkssegmentering, mikrosegmentering och granular access controls definierade som kod.

Defense in Depth strategier implementeras genom multiple säkerhetslager definierade i infrastructure code. Detta inkluderar nätverkssäkerhet, host-based security, application-level security och data encryption som alla konfigureras konsistent genom IaC-templates och modules.

Least Privilege Access principles enforcement genom IaC säkerställer att användare och services endast beviljas minimum permissions nödvändiga för deras funktioner. IAM policies, security groups och RBAC-konfigurationer kan definieras granularly och auditeras kontinuerligt genom kod.

## Policy as Code implementation

Policy as Code representerar paradigmskiftet från manuella säkerhetspolicies till automatiserat policy enforcement genom programmatiska definitioner. Open Policy Agent (OPA), AWS Config Rules och Azure Policy möjliggör deklarativ definition av säkerhetspolicies som kan enforced automatically.

Regulatory compliance automation genom Policy as Code är särskilt värdefullt för svenska organisationer som måste följa GDPR, PCI-DSS, ISO 27001 och andra standards. Policies kan definieras en gång och automatiskt appliceras across alla cloud environments och development lifecycle stages.

Continuous compliance monitoring genom policy enforcement engines detekterar policy violations real-time och kan automatiskt remediera säkerhetsissues eller blockera non-compliant deployments. Detta preventative approach är mer effective än reactive compliance auditing.

Custom policy development för organisationsspecifika säkerhetskrav möjliggör flexibel enforcement av internal security standards. Svenska företag kan utveckla policies för datasuveränitetskrav, branschspecifika regulations och organizational security frameworks.

## Secrets management och data protection

Comprehensive secrets management utgör foundationen för säker IaC implementation. Secrets som API keys, databas-credentials och encryption keys måste hanteras genom dedicated secret management systems istället för att hardkodas i infrastructure configurations.

HashiCorp Vault, AWS Secrets Manager, Azure Key Vault och Kubernetes Secrets erbjuder programmatic interfaces för secret retrieval som kan integreras seamlessly i IaC workflows. Dynamic secrets generation och automatic rotation reducerar risk för credential compromise.

Data encryption at rest och in transit måste konfigureras som standard i alla infrastructure components. IaC templates kan enforça encryption för databaser, storage systems och kommunikationskanaler genom standardized modules och policy validations.

Key management lifecycle including key generation, distribution, rotation och revocation måste automatiseras genom IaC-integrated key management services. Svenska organisationer med höga säkerhetskrav kan implementera HSM-backed key management för kritiska encryption keys.

## Nätverkssäkerhet och mikrosegmentering

Network security design genom IaC möjliggör systematic implementation av defense-in-depth network architectures. VPC design, subnet segmentation, routing tables och network ACLs kan definieras som immutable infrastructure som följer established security patterns.

Mikrosegmentering genom software-defined networking isolerar applications och services med granular network policies. Kubernetes Network Policies, AWS Security Groups och Azure Network Security Groups kan konfigureras för zero-trust networking där kommunikation måste explicitly tillåtas.

Network monitoring och intrusion detection systems kan integreras i IaC deployments för automated security monitoring. Flow logs, traffic analysis och anomaly detection provides continuous visibility into network security posture och potential threats.

Service mesh security med verktyg som Istio, Linkerd eller AWS App Mesh implementerar encryption, authentication och authorization på service-to-service kommunikation level. Dessa säkerhetskontroller kan konfigureras genom IaC för consistent security enforcement.

## Praktiska exempel

### Comprehensive Security Module
```hcl
# modules/security-foundation/main.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Security basline för svenska organisationer
locals {
  security_tags = {
    SecurityBaseline = "swedish-gov-baseline"
    ComplianceFramework = "iso27001-gdpr"
    DataClassification = var.data_classification
    ThreatModel = "updated"
    SecurityContact = var.security_team_email
  }
  
  # Svenska säkerhetskrav
  required_encryption = true
  audit_logging_required = true
  gdpr_compliance = var.data_classification != "public"
}

# KMS Key för organisationsdata
resource "aws_kms_key" "org_key" {
  description              = "Organisationsnyckel för ${var.organization_name}"
  customer_master_key_spec = "SYMMETRIC_DEFAULT"
  key_usage               = "ENCRYPT_DECRYPT"
  deletion_window_in_days = 30
  
  # Automated key rotation
  enable_key_rotation = true
  
  # Policy som tillåter endast authorized användning
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "Enable IAM User Permissions"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        }
        Action   = "kms:*"
        Resource = "*"
      },
      {
        Sid    = "Allow CloudWatch Logs"
        Effect = "Allow"
        Principal = {
          Service = "logs.${data.aws_region.current.name}.amazonaws.com"
        }
        Action = [
          "kms:Encrypt",
          "kms:Decrypt",
          "kms:ReEncrypt*",
          "kms:GenerateDataKey*",
          "kms:DescribeKey"
        ]
        Resource = "*"
      }
    ]
  })

  tags = merge(local.security_tags, {
    Name = "${var.organization_name}-master-key"
  })
}

# Security Group med defense-in-depth
resource "aws_security_group" "secure_application" {
  name_prefix = "${var.application_name}-secure-"
  vpc_id      = var.vpc_id

  # Ingen inbound traffic by default (zero trust)
  # Explicit allow rules måste läggas till per use case
  
  # Outbound - endast nödvändig traffic
  egress {
    description = "HTTPS för externa API calls"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    description = "DNS queries"
    from_port   = 53
    to_port     = 53
    protocol    = "udp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.security_tags, {
    Name = "${var.application_name}-secure-sg"
    NetworkSegment = "application-tier"
  })
}

# CloudTrail för comprehensive audit logging
resource "aws_cloudtrail" "security_audit" {
  count = local.audit_logging_required ? 1 : 0
  
  name           = "${var.organization_name}-security-audit"
  s3_bucket_name = aws_s3_bucket.audit_logs[0].bucket
  
  # Inkludera data events för känslig data
  event_selector {
    read_write_type                 = "All"
    include_management_events      = true
    
    data_resource {
      type   = "AWS::S3::Object"
      values = ["${aws_s3_bucket.audit_logs[0].arn}/*"]
    }
  }
  
  # Aktivera log file integrity validation
  enable_log_file_validation = true
  
  # Multi-region trail för komplett coverage
  is_multi_region_trail = true
  
  # KMS encryption för audit logs
  kms_key_id = aws_kms_key.org_key.arn

  tags = merge(local.security_tags, {
    Name = "${var.organization_name}-security-audit"
    Purpose = "compliance-audit-logging"
  })
}

# S3 bucket för säker log lagring
resource "aws_s3_bucket" "audit_logs" {
  count  = local.audit_logging_required ? 1 : 0
  bucket = "${var.organization_name}-security-audit-logs-${random_id.bucket_suffix.hex}"

  tags = merge(local.security_tags, {
    Name = "${var.organization_name}-audit-logs"
    DataType = "audit-logs"
  })
}

# Secure bucket configuration
resource "aws_s3_bucket_encryption" "audit_logs" {
  count  = local.audit_logging_required ? 1 : 0
  bucket = aws_s3_bucket.audit_logs[0].id

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        kms_master_key_id = aws_kms_key.org_key.arn
        sse_algorithm     = "aws:kms"
      }
      bucket_key_enabled = true
    }
  }
}

resource "aws_s3_bucket_versioning" "audit_logs" {
  count  = local.audit_logging_required ? 1 : 0
  bucket = aws_s3_bucket.audit_logs[0].id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_public_access_block" "audit_logs" {
  count  = local.audit_logging_required ? 1 : 0
  bucket = aws_s3_bucket.audit_logs[0].id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Random suffix för bucket names
resource "random_id" "bucket_suffix" {
  byte_length = 8
}

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}
```

### GDPR Compliance Policy
```rego
# policies/gdpr_compliance.rego
package sweden.gdpr

import rego.v1

# GDPR Article 32 - Security of processing
personal_data_encryption_required if {
    input.resource_type in ["aws_rds_instance", "aws_s3_bucket", "aws_ebs_volume"]
    contains(input.attributes.tags.DataClassification, "personal")
    not encryption_enabled
}

encryption_enabled if {
    input.resource_type == "aws_rds_instance"
    input.attributes.storage_encrypted == true
}

encryption_enabled if {
    input.resource_type == "aws_s3_bucket"
    input.attributes.server_side_encryption_configuration
}

encryption_enabled if {
    input.resource_type == "aws_ebs_volume"
    input.attributes.encrypted == true
}

# GDPR Article 30 - Records of processing activities
data_processing_documentation_required if {
    input.resource_type in ["aws_rds_instance", "aws_dynamodb_table"]
    contains(input.attributes.tags.DataClassification, "personal")
    not data_processing_documented
}

data_processing_documented if {
    required_tags := {"DataController", "DataProcessor", "LegalBasis", "DataRetention"}
    input.attributes.tags
    tags_present := {tag | tag := required_tags[_]; input.attributes.tags[tag]}
    count(tags_present) == count(required_tags)
}

# GDPR Article 25 - Data protection by design and by default
default_deny_access if {
    input.resource_type == "aws_security_group"
    rule := input.attributes.ingress_rules[_]
    rule.cidr_blocks[_] == "0.0.0.0/0"
    rule.from_port != 443  # Endast HTTPS tillåten från internet
}

# Svenska dataskyddslagen specifika krav
swedish_data_sovereignty if {
    input.resource_type in ["aws_rds_instance", "aws_s3_bucket"]
    contains(input.attributes.tags.DataClassification, "personal")
    not swedish_region_used
}

swedish_region_used if {
    # Acceptera endast svenska/EU regioner för persondata
    allowed_regions := {"eu-north-1", "eu-west-1", "eu-central-1"}
    input.attributes.availability_zone
    region := split(input.attributes.availability_zone, "-")[0:2] | join("-", .)
    allowed_regions[region]
}

# Violation sammandrag för rapportering
gdpr_violations contains violation if {
    personal_data_encryption_required
    violation := {
        "type": "encryption_required",
        "resource": input.resource_id,
        "message": "Personal data must be encrypted according to GDPR Article 32",
        "severity": "high"
    }
}

gdpr_violations contains violation if {
    data_processing_documentation_required
    violation := {
        "type": "documentation_required", 
        "resource": input.resource_id,
        "message": "Data processing activities must be documented according to GDPR Article 30",
        "severity": "medium"
    }
}

gdpr_violations contains violation if {
    swedish_data_sovereignty
    violation := {
        "type": "data_sovereignty",
        "resource": input.resource_id, 
        "message": "Personal data must be stored in Swedish/EU regions",
        "severity": "critical"
    }
}
```

### Security Monitoring Automation
```python
# security_monitoring/threat_detection.py
import boto3
import json
from datetime import datetime, timedelta
from typing import Dict, List
import pandas as pd

class SecurityMonitoringAutomation:
    """
    Automatiserad säkerhetsmonitoring för IaC-miljöer
    """
    
    def __init__(self, region='eu-north-1'):
        self.cloudtrail = boto3.client('cloudtrail', region_name=region)
        self.guardduty = boto3.client('guardduty', region_name=region)
        self.config = boto3.client('config', region_name=region)
        self.sns = boto3.client('sns', region_name=region)
        
    def detect_infrastructure_anomalies(self, hours_back=24) -> List[Dict]:
        """Upptäck onormala infrastrukturändringar"""
        
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=hours_back)
        
        # Hämta CloudTrail events för infrastrukturändringar
        events = self.cloudtrail.lookup_events(
            StartTime=start_time,
            EndTime=end_time,
            LookupAttributes=[
                {
                    'AttributeKey': 'EventName',
                    'AttributeValue': 'CreateSecurityGroup'
                },
                {
                    'AttributeKey': 'EventName', 
                    'AttributeValue': 'AuthorizeSecurityGroupIngress'
                },
                {
                    'AttributeKey': 'EventName',
                    'AttributeValue': 'CreateRole'
                }
            ]
        )
        
        anomalies = []
        
        for event in events.get('Events', []):
            # Analysera för misstänkta säkerhetsförändringar
            if self._is_suspicious_security_change(event):
                anomalies.append({
                    'event_id': event['EventId'],
                    'event_name': event['EventName'],
                    'user': event.get('Username', 'Unknown'),
                    'source_ip': event.get('SourceIPAddress', 'Unknown'),
                    'timestamp': event['EventTime'].isoformat(),
                    'risk_level': self._calculate_risk_level(event),
                    'details': event.get('CloudTrailEvent', {})
                })
        
        return anomalies
    
    def validate_compliance_status(self) -> Dict:
        """Validera compliance status för svenska regelverk"""
        
        compliance_results = {
            'gdpr_compliance': self._check_gdpr_compliance(),
            'msb_requirements': self._check_msb_requirements(),
            'iso27001_controls': self._check_iso27001_controls(),
            'overall_score': 0,
            'critical_findings': [],
            'recommendations': []
        }
        
        # Beräkna overall compliance score
        scores = [compliance_results[key] for key in compliance_results if isinstance(compliance_results[key], (int, float))]
        compliance_results['overall_score'] = sum(scores) / len(scores) if scores else 0
        
        return compliance_results
    
    def _check_gdpr_compliance(self) -> float:
        """Kontrollera GDPR compliance"""
        
        # Hämta compliance evaluations från AWS Config
        evaluations = self.config.get_compliance_details_by_config_rule(
            ConfigRuleName='gdpr-encryption-enabled'
        )
        
        total_resources = len(evaluations.get('EvaluationResults', []))
        compliant_resources = len([
            eval for eval in evaluations.get('EvaluationResults', [])
            if eval['ComplianceType'] == 'COMPLIANT'
        ])
        
        return (compliant_resources / total_resources) * 100 if total_resources > 0 else 0
    
    def _check_msb_requirements(self) -> float:
        """Kontrollera MSB säkerhetskrav"""
        
        # Implementera MSB-specifika kontroller
        msb_rules = [
            'msb-network-segmentation',
            'msb-access-logging', 
            'msb-incident-response',
            'msb-backup-encryption'
        ]
        
        total_score = 0
        for rule in msb_rules:
            try:
                compliance = self.config.get_compliance_details_by_config_rule(
                    ConfigRuleName=rule
                )
                # Beräkna compliance för denna regel
                rule_compliance = self._calculate_rule_compliance(compliance)
                total_score += rule_compliance
            except:
                # Regel existerar inte eller access issue
                pass
        
        return total_score / len(msb_rules) if msb_rules else 0
    
    def generate_security_report(self, include_remediation=True) -> Dict:
        """Generera comprehensive säkerhetsrapport"""
        
        report = {
            'report_date': datetime.now().isoformat(),
            'infrastructure_anomalies': self.detect_infrastructure_anomalies(),
            'compliance_status': self.validate_compliance_status(),
            'security_findings': self._get_security_findings(),
            'threat_intelligence': self._get_threat_intelligence(),
            'remediation_plan': []
        }
        
        if include_remediation:
            report['remediation_plan'] = self._generate_remediation_plan(report)
        
        return report
    
    def _generate_remediation_plan(self, security_report: Dict) -> List[Dict]:
        """Generera automatisk remediering plan"""
        
        remediation_actions = []
        
        # Analysera critical findings och skapa åtgärdsplan
        for finding in security_report.get('security_findings', []):
            if finding.get('severity') == 'CRITICAL':
                remediation_actions.append({
                    'finding_id': finding['id'],
                    'action_type': 'automated_fix',
                    'terraform_module': self._get_remediation_module(finding),
                    'estimated_time': '5 minutes',
                    'risk_level': 'low'
                })
        
        return remediation_actions
    
    def send_security_alerts(self, findings: List[Dict], topic_arn: str):
        """Skicka säkerhetsalerts till svenska säkerhetsteam"""
        
        critical_findings = [f for f in findings if f.get('severity') == 'CRITICAL']
        
        if critical_findings:
            message = {
                'alert_type': 'CRITICAL_SECURITY_FINDING',
                'timestamp': datetime.now().isoformat(),
                'findings_count': len(critical_findings),
                'findings': critical_findings,
                'recommended_actions': [
                    'Granska infrastrukturändringar omedelbart',
                    'Verifiera användaraktivitet',
                    'Kontrollera compliance status',
                    'Implementera automated remediation'
                ],
                'compliance_impact': 'Potentiell GDPR/MSB regelverksbrott'
            }
            
            self.sns.publish(
                TopicArn=topic_arn,
                Message=json.dumps(message, indent=2),
                Subject=f'KRITISK: Säkerhetsincident upptäckt - {len(critical_findings)} findings'
            )
```

## Sammanfattning

Säkerhet inom Infrastructure as Code kräver systematisk integration av säkerhetsprinciper i alla aspekter av infrastrukturdefinition och deployment. Security-by-design, Policy as Code och automated compliance monitoring möjliggör proaktiv säkerhetshantering som kan anpassas till svenska regulatoriska krav.

Framgångsrik implementation av IaC-säkerhet resulterar i reducerad attack surface, snabbare incident response och förbättrad regulatory compliance. Investment i comprehensive security automation through code betalar sig genom minskade säkerhetsincidenter och compliance costs.

Svenska organisationer som implementerar dessa säkerhetsstrategier positionerar sig för framgångsrik digitalisering samtidigt som de möter växande cybersecurity threats och regulatoriska krav.

## Källor och referenser

- NIST. "Cybersecurity Framework för Infrastructure as Code." NIST Special Publication, 2023.
- MSB. "Säkerhetskrav för kritisk infrastruktur." Myndigheten för samhällsskydd och beredskap, 2023.
- ENISA. "Cloud Security Guidelines för EU-organisationer." European Union Agency for Cybersecurity, 2023.
- AWS. "Security Best Practices för Infrastructure as Code." Amazon Web Services Security, 2023.
- Open Policy Agent. "Policy as Code Implementation Guide." CNCF OPA Documentation, 2023.
- Zero Trust Architecture. "NIST Special Publication 800-207." National Institute of Standards, 2023.