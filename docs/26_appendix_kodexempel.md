# Appendix A: Kodexempel och tekniska implementationer

Denna appendix innehåller alla kodexempel, konfigurationsfiler och tekniska implementationer som refereras till i bokens huvudkapitel. Kodexemplen är organiserade efter typ och användningsområde för att göra det enkelt att hitta specifika implementationer.

![Kodexempel appendix](images/diagram_26_appendix.png)

*Denna appendix fungerar som en praktisk referenssamling för alla tekniska implementationer som demonstreras genom boken. Varje kodexempel är kategoriserat och märkt med referenser tillbaka till relevanta kapitel.*

## Navigering i appendix

Kodexemplen är organiserade i följande kategorier:

1. **[CI/CD Pipelines och automatisering](#cicd-pipelines)**
2. **[Infrastructure as Code - Terraform](#terraform-iac)**
3. **[Infrastructure as Code - CloudFormation](#cloudformation-iac)**
4. **[Automationsskript och verktyg](#automation-scripts)**
5. **[Säkerhet och compliance](#security-compliance)**
6. **[Testning och validering](#testing-validation)**
7. **[Konfigurationsfiler](#configuration)**
8. **[Shell-skript och verktyg](#shell-scripts)**

Varje kodexempel har en unik identifierare i formatet `[KAPITEL]_CODE_[NUMMER]` för enkel referens från huvudtexten.

---

## CI/CD Pipelines och automatisering {#cicd-pipelines}

Denna sektion innehåller alla exempel på CI/CD-pipelines, GitHub Actions workflows och automationsprocesser för svenska organisationer.

### 05_CODE_1: GDPR-kompatibel CI/CD Pipeline för svenska organisationer
*Refereras från Kapitel 5: [Automatisering och CI/CD-pipelines](05_automatisering_cicd.md)*

```yaml
# .github/workflows/svenska-iac-pipeline.yml
# GDPR-compliant CI/CD pipeline för svenska organisationer

name: Svenska IaC Pipeline med GDPR Compliance

on:
  push:
    branches: [main, staging, development]
    paths: ['infrastructure/**', 'modules/**']
  pull_request:
    branches: [main, staging]
    paths: ['infrastructure/**', 'modules/**']

env:
  TF_VERSION: '1.6.0'
  ORGANIZATION_NAME: ${{ vars.ORGANIZATION_NAME }}
  ENVIRONMENT: ${{ github.ref_name == 'main' && 'production' || github.ref_name }}
  COST_CENTER: ${{ vars.COST_CENTER }}
  GDPR_COMPLIANCE_ENABLED: 'true'
  DATA_RESIDENCY: 'Sweden'
  AUDIT_LOGGING: 'enabled'

jobs:
  # GDPR och säkerhetskontroller
  gdpr-compliance-check:
    name: GDPR Compliance Validation
    runs-on: ubuntu-latest
    if: contains(github.event.head_commit.message, 'personal-data') || contains(github.event.head_commit.message, 'gdpr')
    
    steps:
      - name: Checkout kod
        uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          fetch-depth: 0
      
      - name: GDPR Data Discovery Scan
        run: |
          echo "🔍 Scanning för personal data patterns..."
          
          # Sök efter vanliga personal data patterns i IaC-kod
          PERSONAL_DATA_PATTERNS=(
            "personnummer"
            "social.*security"
            "credit.*card"
            "bank.*account"
            "email.*address"
            "phone.*number"
            "date.*of.*birth"
            "passport.*number"
          )
          
          VIOLATIONS_FOUND=false
          
          for pattern in "${PERSONAL_DATA_PATTERNS[@]}"; do
            if grep -ri "$pattern" infrastructure/ modules/ 2>/dev/null; then
              echo "⚠️ GDPR VARNING: Potentiell personal data hittad: $pattern"
              VIOLATIONS_FOUND=true
            fi
          done
          
          if [ "$VIOLATIONS_FOUND" = true ]; then
            echo "❌ GDPR compliance check misslyckades"
            echo "Personal data får inte hardkodas i IaC-kod"
            exit 1
          fi
          
          echo "✅ GDPR compliance check genomförd"
```

---

## Infrastructure as Code - CloudFormation {#cloudformation-iac}

Denna sektion innehåller CloudFormation templates för AWS-infrastruktur anpassad för svenska organisationer.

### 07_CODE_1: VPC Setup för svenska organisationer med GDPR compliance
*Refereras från Kapitel 7: [Molnarkitektur som kod](07_molnarkitektur.md)*

```yaml
# cloudformation/svenska-org-vpc.yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'VPC setup för svenska organisationer med GDPR compliance'

Parameters:
  EnvironmentType:
    Type: String
    Default: development
    AllowedValues: [development, staging, production]
    Description: 'Miljötyp för deployment'
  
  DataClassification:
    Type: String
    Default: internal
    AllowedValues: [public, internal, confidential, restricted]
    Description: 'Dataklassificering enligt svenska säkerhetsstandarder'
  
  ComplianceRequirements:
    Type: CommaDelimitedList
    Default: "gdpr,iso27001"
    Description: 'Lista över compliance-krav som måste uppfyllas'

Conditions:
  IsProduction: !Equals [!Ref EnvironmentType, production]
  RequiresGDPR: !Contains [!Ref ComplianceRequirements, gdpr]
  RequiresISO27001: !Contains [!Ref ComplianceRequirements, iso27001]

Resources:
  VPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: !If [IsProduction, '10.0.0.0/16', '10.1.0.0/16']
      EnableDnsHostnames: true
      EnableDnsSupport: true
      Tags:
        - Key: Name
          Value: !Sub '${AWS::StackName}-vpc'
        - Key: Environment
          Value: !Ref EnvironmentType
        - Key: DataClassification
          Value: !Ref DataClassification
        - Key: GDPRCompliant
          Value: !If [RequiresGDPR, 'true', 'false']
        - Key: ISO27001Compliant
          Value: !If [RequiresISO27001, 'true', 'false']
        - Key: Country
          Value: 'Sweden'
        - Key: Region
          Value: 'eu-north-1'
```

---

## Automation Scripts {#automation-scripts}

Denna sektion innehåller Python-skript och andra automationsverktyg för Infrastructure as Code-hantering.

### 22_CODE_1: Omfattande testramverk för Infrastructure as Code
*Refereras från Kapitel 22: [Best practices och lärda läxor](22_best_practices.md)*

```python
# testing/comprehensive_iac_testing.py
import pytest
import boto3
import json
import yaml
from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class TestCase:
    name: str
    description: str
    test_type: str
    severity: str
    expected_result: Any
    actual_result: Any = None
    status: str = "pending"
    execution_time: float = 0.0

class ComprehensiveIaCTesting:
    """
    Comprehensive testing framework för Infrastructure as Code
    Based på svenska best practices och international standards
    """
    
    def __init__(self, region='eu-north-1'):
        self.region = region
        self.ec2 = boto3.client('ec2', region_name=region)
        self.rds = boto3.client('rds', region_name=region)
        self.s3 = boto3.client('s3', region_name=region)
        self.iam = boto3.client('iam', region_name=region)
        self.test_results = []
        
    def test_infrastructure_security(self, stack_name: str) -> List[TestCase]:
        """Test comprehensive security configuration"""
        
        security_tests = [
            self._test_encryption_at_rest(),
            self._test_encryption_in_transit(),
            self._test_vpc_flow_logs(),
            self._test_security_groups(),
            self._test_iam_policies(),
            self._test_s3_bucket_policies(),
            self._test_rds_security()
        ]
        
        return security_tests
    
    def _test_encryption_at_rest(self) -> TestCase:
        """Verify all storage resources use encryption at rest"""
        test = TestCase(
            name="Encryption at Rest Validation",
            description="Verify all storage uses encryption",
            test_type="security",
            severity="high",
            expected_result="All storage encrypted"
        )
        
        try:
            # Test S3 bucket encryption
            buckets = self.s3.list_buckets()['Buckets']
            unencrypted_buckets = []
            
            for bucket in buckets:
                bucket_name = bucket['Name']
                try:
                    encryption = self.s3.get_bucket_encryption(Bucket=bucket_name)
                    if not encryption.get('ServerSideEncryptionConfiguration'):
                        unencrypted_buckets.append(bucket_name)
                except self.s3.exceptions.ClientError:
                    unencrypted_buckets.append(bucket_name)
            
            if unencrypted_buckets:
                test.status = "failed"
                test.actual_result = f"Unencrypted buckets: {unencrypted_buckets}"
            else:
                test.status = "passed"
                test.actual_result = "All S3 buckets encrypted"
                
        except Exception as e:
            test.status = "error"
            test.actual_result = f"Test error: {str(e)}"
            
        return test
```

---

## Configuration Files {#configuration}

Denna sektion innehåller konfigurationsfiler för olika verktyg och tjänster.

### 22_CODE_2: Governance policy configuration för svenska organisationer
*Refereras från Kapitel 22: [Best practices och lärda läxor](22_best_practices.md)*

```yaml
# governance/svenska-governance-policy.yaml
governance_framework:
  organization: "Svenska Organization AB"
  compliance_standards: ["GDPR", "ISO27001", "SOC2"]
  data_residency: "Sweden"
  regulatory_authority: "Integritetsskyddsmyndigheten (IMY)"

policy_enforcement:
  automated_checks:
    pre_deployment:
      - "cost_estimation"
      - "security_scanning"
      - "compliance_validation"
      - "resource_tagging"
    
    post_deployment:
      - "security_monitoring"
      - "cost_monitoring"
      - "performance_monitoring"
      - "compliance_auditing"
  
  manual_approvals:
    production_deployments:
      approvers: ["Tech Lead", "Security Team", "Compliance Officer"]
      criteria:
        - "Security review completed"
        - "Cost impact assessed"
        - "GDPR compliance verified"
        - "Business stakeholder approval"
    
    emergency_changes:
      approvers: ["Incident Commander", "Security Lead"]
      max_approval_time: "30 minutes"
      post_incident_review: "required"

cost_governance:
  budget_controls:
    development: 
      monthly_limit: "10000 SEK"
      alert_threshold: "80%"
      auto_shutdown: "enabled"
    
    staging:
      monthly_limit: "25000 SEK"
      alert_threshold: "85%"
      auto_shutdown: "disabled"
    
    production:
      monthly_limit: "100000 SEK"
      alert_threshold: "90%"
      auto_shutdown: "disabled"
      escalation: "immediate"

security_policies:
  data_protection:
    encryption:
      at_rest: "mandatory"
      in_transit: "mandatory"
      key_management: "AWS KMS with customer managed keys"
    
    access_control:
      principle: "least_privilege"
      mfa_required: true
      session_timeout: "8 hours"
      privileged_access_review: "quarterly"
    
    monitoring:
      security_events: "all_logged"
      anomaly_detection: "enabled"
      incident_response: "24/7"
      retention_period: "7 years"

compliance_monitoring:
  gdpr_requirements:
    data_mapping: "automated"
    consent_management: "integrated"
    right_to_erasure: "implemented"
    data_breach_notification: "automated"
    
  audit_requirements:
    frequency: "quarterly"
    scope: "all_infrastructure"
    external_auditor: "required_annually"
    evidence_collection: "automated"
```

---

## Referenser och navigering

Varje kodexempel i denna appendix kan refereras från huvudtexten med dess unika identifierare. För att hitta specifika implementationer:

1. **Använd sökfunktion** - Sök efter kodtyp eller teknologi (t.ex. "Terraform", "CloudFormation", "Python")
2. **Följ kategorierna** - Navigera till relevant sektion baserat på användningsområde
3. **Använd korshänvisningar** - Följ länkar tillbaka till huvudkapitlen för kontext

### Konventioner för kodexempel

- **Kommentarer**: Alla kodexempel innehåller svenska kommentarer för klarhet
- **Säkerhet**: Säkerhetsaspekter är markerade med 🔒
- **GDPR-compliance**: GDPR-relaterade konfigurationer är markerade med 🇪🇺
- **Svenska anpassningar**: Lokala anpassningar är markerade med 🇸🇪

### Uppdateringar och underhåll

Denna appendix uppdateras löpande när nya kodexempel läggs till i bokens huvudkapitel. För senaste versionen av kodexempel, se bokens GitHub-repository.

---

*För mer information om specifika implementationer, se respektive huvudkapitel där kodexemplen introduceras och förklaras i sitt sammanhang.*