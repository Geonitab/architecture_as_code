# Appendix A: Kodexempel och tekniska arkitektur som kod-implementationer

Denna appendix innehåller alla kodexempel, konfigurationsfiler och tekniska implementeringar som refereras till i bokens huvudkapitel. Kodexemplen är organiserade efter typ och användningsområde för att göra det enkelt att hitta specifika implementationer.

![Kodexempel appendix](images/diagram_26_appendix.png)

*Denna appendix fungerar som en praktisk referenssamling för alla tekniska implementationer som demonstreras genom boken. Varje kodexempel är kategoriserat och märkt med referenser tillbaka till relevanta kapitel.*

## Navigering i appendix

Kodexemplen är organiserade i följande kategorier:

1. **[CI/CD Pipelines och arkitektur som kod-automatisering](#cicd-pipelines)**
2. **[Infrastructure as Code (arkitektur som kod) - Terraform](#terraform-iac)**
3. **[Infrastructure as Code (arkitektur som kod) - CloudFormation](#cloudformation-arkitektur som kod)**
4. **[Automationsskript och verktyg](#automation-scripts)**
5. **[Säkerhet och compliance](#security-compliance)**
6. **[Testning och validering](#testing-validation)**
7. **[Konfigurationsfiler](#configuration)**
8. **[Shell-skript och verktyg](#shell-scripts)**

Varje kodexempel har en unik identifierare i formatet `[KAPITEL]_CODE_[NUMMER]` för enkel referens från huvudtexten.

---

## CI/CD Pipelines och arkitektur som kod-automatisering {#cicd-pipelines}

Denna sektion innehåller alla exempel på CI/CD-pipelines, GitHub Actions workflows och automationsprocesser för svenska organisationer.

### 05_CODE_1: GDPR-kompatibel CI/CD Pipeline för svenska organisationer
*Refereras från Kapitel 5: [Automatisering och CI/CD-pipelines](05_automatisering_cicd.md)*

```yaml
# .github/workflows/svenska-arkitektur som kod-pipeline.yml
# GDPR-compliant CI/CD pipeline för svenska organisationer

name: Svenska Arkitektur som kod Pipeline med GDPR Compliance

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
          
          # Sök efter vanliga personal data patterns i Arkitektur som kod-kod
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
            echo "Personal data får inte hardkodas i Arkitektur som kod-kod"
            exit 1
          fi
          
          echo "✅ GDPR compliance check genomförd"
```

### 05_CODE_2: Jenkins Pipeline för svenska organisationer med GDPR compliance
*Refereras från Kapitel 5: [Automatisering och CI/CD-pipelines](05_automatisering_cicd.md)*

```yaml
# jenkins/svenska-arkitektur som kod-pipeline.groovy
// Jenkins pipeline för svenska organisationer med GDPR compliance

pipeline {
    agent any
    
    parameters {
        choice(
            name: 'ENVIRONMENT',
            choices: ['development', 'staging', 'production'],
            description: 'Target environment för deployment'
        )
        booleanParam(
            name: 'FORCE_DEPLOYMENT',
            defaultValue: false,
            description: 'Forcera deployment även vid varningar (endast development)'
        )
        string(
            name: 'COST_CENTER',
            defaultValue: 'CC-IT-001',
            description: 'Kostnadscenter för svenska bokföring'
        )
    }
    
    environment {
        ORGANIZATION_NAME = 'svenska-org'
        AWS_DEFAULT_REGION = 'eu-north-1'  // Stockholm region
        GDPR_COMPLIANCE = 'enabled'
        DATA_RESIDENCY = 'Sweden'
        TERRAFORM_VERSION = '1.6.0'
        COST_CURRENCY = 'SEK'
        AUDIT_RETENTION_YEARS = '7'  // Svenska lagkrav
    }
    
    stages {
        stage('🇸🇪 Svenska Compliance Check') {
            parallel {
                stage('GDPR Data Scan') {
                    steps {
                        script {
                            echo "🔍 Scanning för personal data patterns i Arkitektur som kod kod..."
                            
                            def personalDataPatterns = [
                                'personnummer', 'social.*security', 'credit.*card',
                                'bank.*account', 'email.*address', 'phone.*number'
                            ]
                            
                            def violations = []
                            
                            personalDataPatterns.each { pattern ->
                                def result = sh(
                                    script: "grep -ri '${pattern}' infrastructure/ modules/ || true",
                                    returnStdout: true
                                ).trim()
                                
                                if (result) {
                                    violations.add("Personal data pattern found: ${pattern}")
                                }
                            }
                            
                            if (violations) {
                                error("GDPR VIOLATION: Personal data found in Arkitektur som kod code:\n${violations.join('\n')}")
                            }
                            
                            echo "✅ GDPR data scan genomförd - inga violations"
                        }
                    }
                }
                
                stage('Data Residency Validation') {
                    steps {
                        script {
                            echo "🏔️ Validerar svenska data residency krav..."
                            
                            def allowedRegions = ['eu-north-1', 'eu-central-1', 'eu-west-1']
                            
                            def regionCheck = sh(
                                script: """
                                    grep -r 'region\\s*=' infrastructure/ modules/ | \
                                    grep -v -E '(eu-north-1|eu-central-1|eu-west-1)' || true
                                """,
                                returnStdout: true
                            ).trim()
                            
                            if (regionCheck) {
                                error("DATA RESIDENCY VIOLATION: Non-EU regions found:\n${regionCheck}")
                            }
                            
                            echo "✅ Data residency requirements uppfyllda"
                        }
                    }
                }
                
                stage('Cost Center Validation') {
                    steps {
                        script {
                            echo "💰 Validerar kostnadscenter för svenska bokföring..."
                            
                            if (!params.COST_CENTER.matches(/CC-[A-Z]{2,}-\d{3}/)) {
                                error("Ogiltigt kostnadscenter format. Använd: CC-XX-nnn")
                            }
                            
                            // Validera att kostnadscenter existerar i företagets system
                            def validCostCenters = [
                                'CC-IT-001', 'CC-DEV-002', 'CC-OPS-003', 'CC-SEC-004'
                            ]
                            
                            if (!validCostCenters.contains(params.COST_CENTER)) {
                                error("Okänt kostnadscenter: ${params.COST_CENTER}")
                            }
                            
                            echo "✅ Kostnadscenter validerat: ${params.COST_CENTER}"
                        }
                    }
                }
            }
        }
        
        stage('📝 Code Quality Analysis') {
            parallel {
                stage('Terraform Validation') {
                    steps {
                        script {
                            echo "🔧 Terraform syntax och formatering..."
                            
                            // Format check
                            sh "terraform fmt -check -recursive infrastructure/"
                            
                            // Syntax validation
                            dir('infrastructure/environments/${params.ENVIRONMENT}') {
                                sh """
                                    terraform init -backend=false
                                    terraform validate
                                """
                            }
                            
                            echo "✅ Terraform validation slutförd"
                        }
                    }
                }
                
                stage('Security Scanning') {
                    steps {
                        script {
                            echo "🔒 Säkerhetsskanning med Checkov..."
                            
                            sh """
                                pip install checkov
                                checkov -d infrastructure/ \
                                    --framework terraform \
                                    --output json \
                                    --output-file checkov-results.json \
                                    --soft-fail
                            """
                            
                            // Analysera kritiska säkerhetsproblem
                            def results = readJSON file: 'checkov-results.json'
                            def criticalIssues = results.results.failed_checks.findAll { 
                                it.severity == 'CRITICAL' 
                            }
                            
                            if (criticalIssues.size() > 0) {
                                echo "⚠️ KRITISKA säkerhetsproblem funna:"
                                criticalIssues.each { issue ->
                                    echo "- ${issue.check_name}: ${issue.file_path}"
                                }
                                
                                if (params.ENVIRONMENT == 'production') {
                                    error("Kritiska säkerhetsproblem måste åtgärdas före production deployment")
                                }
                            }
                            
                            echo "✅ Säkerhetsskanning slutförd"
                        }
                    }
                }
                
                stage('Svenska Policy Validation') {
                    steps {
                        script {
                            echo "📋 Validerar svenska organisationspolicies..."
                            
                            // Skapa svenska OPA policies
                            writeFile file: 'policies/svenska-tagging.rego', text: """
                                package svenska.tagging
                                
                                required_tags := [
                                    "Environment", "CostCenter", "Organization", 
                                    "Country", "GDPRCompliant", "DataResidency"
                                ]
                                
                                deny[msg] {
                                    input.resource[resource_type][name]
                                    resource_type != "data"
                                    not input.resource[resource_type][name].tags
                                    msg := sprintf("Resource %s.%s saknar tags", [resource_type, name])
                                }
                                
                                deny[msg] {
                                    input.resource[resource_type][name].tags
                                    required_tag := required_tags[_]
                                    not input.resource[resource_type][name].tags[required_tag]
                                    msg := sprintf("Resource %s.%s saknar obligatorisk tag: %s", [resource_type, name, required_tag])
                                }
                            """
                            
                            sh """
                                curl -L https://github.com/open-policy-agent/conftest/releases/download/v0.46.0/conftest_0.46.0_Linux_x86_64.tar.gz | tar xz
                                sudo mv conftest /usr/local/bin
                                
                                find infrastructure/ -name "*.tf" -exec conftest verify --policy policies/ {} \\;
                            """
                            
                            echo "✅ Svenska policy validation slutförd"
                        }
                    }
                }
            }
        }
        
        stage('💰 Svenska Kostnadskontroll') {
            steps {
                script {
                    echo "📊 Beräknar infrastrukturkostnader i svenska kronor..."
                    
                    // Setup Infracost för svenska valuta
                    sh """
                        curl -fsSL https://raw.githubusercontent.com/infracost/infracost/master/scripts/install.sh | sh
                        export PATH=\$PATH:\$HOME/.local/bin
                        
                        cd infrastructure/environments/${params.ENVIRONMENT}
                        terraform init -backend=false
                        
                        infracost breakdown \\
                            --path . \\
                            --currency SEK \\
                            --format json \\
                            --out-file ../../../cost-estimate.json
                        
                        infracost output \\
                            --path ../../../cost-estimate.json \\
                            --format table \\
                            --out-file ../../../cost-summary.txt
                    """
                    
                    // Validera kostnader mot svenska budgetgränser
                    def costData = readJSON file: 'cost-estimate.json'
                    def monthlyCostSEK = costData.totalMonthlyCost as Double
                    
                    def budgetLimits = [
                        'development': 5000,
                        'staging': 15000,
                        'production': 50000
                    ]
                    
                    def maxBudget = budgetLimits[params.ENVIRONMENT] ?: 10000
                    
                    echo "Beräknad månadskostnad: ${monthlyCostSEK} SEK"
                    echo "Budget för ${params.ENVIRONMENT}: ${maxBudget} SEK"
                    
                    if (monthlyCostSEK > maxBudget) {
                        def overBudget = monthlyCostSEK - maxBudget
                        echo "⚠️ BUDGET ÖVERSKRIDEN med ${overBudget} SEK!"
                        
                        if (params.ENVIRONMENT == 'production' && !params.FORCE_DEPLOYMENT) {
                            error("Budget överskridning inte tillåten för production utan CFO godkännande")
                        }
                    }
                    
                    // Generera svenskt kostnadsrapport
                    def costReport = """
                    # Kostnadsrapport - ${env.ORGANIZATION_NAME}
                    
                    **Miljö:** ${params.ENVIRONMENT}
                    **Datum:** ${new Date().format('yyyy-MM-dd HH:mm')} (svensk tid)
                    **Kostnadscenter:** ${params.COST_CENTER}
                    
                    ## Månadskostnad
                    - **Total:** ${monthlyCostSEK} SEK
                    - **Budget:** ${maxBudget} SEK
                    - **Status:** ${monthlyCostSEK <= maxBudget ? '✅ Inom budget' : '❌ Över budget'}
                    
                    ## Kostnadsnedbrytning
                    ${readFile('cost-summary.txt')}
                    
                    ## Rekommendationer
                    - Använd Reserved Instances för production workloads
                    - Aktivera auto-scaling för development miljöer
                    - Implementera scheduled shutdown för icke-kritiska system
                    """
                    
                    writeFile file: 'cost-report-svenska.md', text: costReport
                    archiveArtifacts artifacts: 'cost-report-svenska.md', fingerprint: true
                    
                    echo "✅ Kostnadskontroll slutförd"
                }
            }
        }
    }
}
```

### 05_CODE_3: Terratest för svenska VPC implementation
*Refereras från Kapitel 5: [Automatisering och CI/CD-pipelines](05_automatisering_cicd.md)*

```go
// test/svenska_vpc_test.go
// Terratest suite för svenska VPC implementation med GDPR compliance

package test

import (
    "encoding/json"
    "fmt"
    "strings"
    "testing"
    "time"

    "github.com/aws/aws-sdk-go/aws"
    "github.com/aws/aws-sdk-go/aws/session"
    "github.com/aws/aws-sdk-go/service/ec2"
    "github.com/aws/aws-sdk-go/service/cloudtrail"
    "github.com/gruntwork-io/terratest/modules/terraform"
    "github.com/gruntwork-io/terratest/modules/test-structure"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
)

// SvenskaVPCTestSuite definierar test suite för svenska VPC implementation
type SvenskaVPCTestSuite struct {
    TerraformOptions *terraform.Options
    AWSSession       *session.Session
    OrganizationName string
    Environment      string
    CostCenter       string
}

// TestSvenskaVPCGDPRCompliance testar GDPR compliance för VPC implementation
func TestSvenskaVPCGDPRCompliance(t *testing.T) {
    t.Parallel()

    suite := setupSvenskaVPCTest(t, "development")
    defer cleanupSvenskaVPCTest(t, suite)

    // Deploy infrastructure
    terraform.InitAndApply(t, suite.TerraformOptions)

    // Test GDPR compliance requirements
    t.Run("TestVPCFlowLogsEnabled", func(t *testing.T) {
        testVPCFlowLogsEnabled(t, suite)
    })

    t.Run("TestEncryptionAtRest", func(t *testing.T) {
        testEncryptionAtRest(t, suite)
    })

    t.Run("TestDataResidencySweden", func(t *testing.T) {
        testDataResidencySweden(t, suite)
    })

    t.Run("TestAuditLogging", func(t *testing.T) {
        testAuditLogging(t, suite)
    })

    t.Run("TestSvenskaTagging", func(t *testing.T) {
        testSvenskaTagging(t, suite)
    })
}

// setupSvenskaVPCTest förbereder test environment för svenska VPC testing
func setupSvenskaVPCTest(t *testing.T, environment string) *SvenskaVPCTestSuite {
    // Unik test identifier
    uniqueID := strings.ToLower(fmt.Sprintf("test-%d", time.Now().Unix()))
    organizationName := fmt.Sprintf("svenska-org-%s", uniqueID)

    // Terraform configuration
    terraformOptions := &terraform.Options{
        TerraformDir: "../infrastructure/modules/vpc",
        Vars: map[string]interface{}{
            "organization_name":     organizationName,
            "environment":          environment,
            "cost_center":          "CC-TEST-001",
            "gdpr_compliance":      true,
            "data_residency":       "Sweden",
            "enable_flow_logs":     true,
            "enable_encryption":    true,
            "audit_logging":        true,
        },
        BackendConfig: map[string]interface{}{
            "bucket": "svenska-org-terraform-test-state",
            "key":    fmt.Sprintf("test/%s/terraform.tfstate", uniqueID),
            "region": "eu-north-1",
        },
        RetryableTerraformErrors: map[string]string{
            ".*": "Transient error - retrying...",
        },
        MaxRetries:         3,
        TimeBetweenRetries: 5 * time.Second,
    }

    // AWS session för Stockholm region
    awsSession := session.Must(session.NewSession(&aws.Config{
        Region: aws.String("eu-north-1"),
    }))

    return &SvenskaVPCTestSuite{
        TerraformOptions: terraformOptions,
        AWSSession:       awsSession,
        OrganizationName: organizationName,
        Environment:      environment,
        CostCenter:       "CC-TEST-001",
    }
}

// testVPCFlowLogsEnabled validerar att VPC Flow Logs är aktiverade för GDPR compliance
func testVPCFlowLogsEnabled(t *testing.T, suite *SvenskaVPCTestSuite) {
    // Hämta VPC ID från Terraform output
    vpcID := terraform.Output(t, suite.TerraformOptions, "vpc_id")
    require.NotEmpty(t, vpcID, "VPC ID should not be empty")

    // AWS EC2 client
    ec2Client := ec2.New(suite.AWSSession)

    // Kontrollera Flow Logs
    flowLogsInput := &ec2.DescribeFlowLogsInput{
        Filters: []*ec2.Filter{
            {
                Name:   aws.String("resource-id"),
                Values: []*string{aws.String(vpcID)},
            },
        },
    }

    flowLogsOutput, err := ec2Client.DescribeFlowLogs(flowLogsInput)
    require.NoError(t, err, "Failed to describe VPC flow logs")

    // Validera att Flow Logs är aktiverade
    assert.Greater(t, len(flowLogsOutput.FlowLogs), 0, "VPC Flow Logs should be enabled for GDPR compliance")

    for _, flowLog := range flowLogsOutput.FlowLogs {
        assert.Equal(t, "Active", *flowLog.FlowLogStatus, "Flow log should be active")
        assert.Equal(t, "ALL", *flowLog.TrafficType, "Flow log should capture all traffic for compliance")
    }

    t.Logf("✅ VPC Flow Logs aktiverade för GDPR compliance: %s", vpcID)
}

// testEncryptionAtRest validerar att all lagring är krypterad enligt GDPR-krav
func testEncryptionAtRest(t *testing.T, suite *SvenskaVPCTestSuite) {
    // Hämta KMS key från Terraform output
    kmsKeyArn := terraform.Output(t, suite.TerraformOptions, "kms_key_arn")
    require.NotEmpty(t, kmsKeyArn, "KMS key ARN should not be empty")

    // Validera att KMS key är från Sverige region
    assert.Contains(t, kmsKeyArn, "eu-north-1", "KMS key should be in Stockholm region for data residency")

    t.Logf("✅ Encryption at rest validerat för GDPR compliance")
}

// testDataResidencySweden validerar att all infrastruktur är inom svenska gränser
func testDataResidencySweden(t *testing.T, suite *SvenskaVPCTestSuite) {
    // Validera att VPC är i Stockholm region
    vpcID := terraform.Output(t, suite.TerraformOptions, "vpc_id")
    
    ec2Client := ec2.New(suite.AWSSession)
    
    vpcOutput, err := ec2Client.DescribeVpcs(&ec2.DescribeVpcsInput{
        VpcIds: []*string{aws.String(vpcID)},
    })
    require.NoError(t, err, "Failed to describe VPC")
    require.Len(t, vpcOutput.Vpcs, 1, "Should find exactly one VPC")

    // Kontrollera region från session config
    region := *suite.AWSSession.Config.Region
    allowedRegions := []string{"eu-north-1", "eu-central-1", "eu-west-1"}
    
    regionAllowed := false
    for _, allowedRegion := range allowedRegions {
        if region == allowedRegion {
            regionAllowed = true
            break
        }
    }
    
    assert.True(t, regionAllowed, "VPC must be in EU region for Swedish data residency. Found: %s", region)

    t.Logf("✅ Data residency validerat - all infrastruktur i EU region: %s", region)
}

// testAuditLogging validerar att audit logging är konfigurerat enligt svenska lagkrav
func testAuditLogging(t *testing.T, suite *SvenskaVPCTestSuite) {
    // Kontrollera CloudTrail konfiguration
    cloudtrailClient := cloudtrail.New(suite.AWSSession)
    
    trails, err := cloudtrailClient.DescribeTrails(&cloudtrail.DescribeTrailsInput{})
    require.NoError(t, err, "Failed to list CloudTrail trails")

    foundOrgTrail := false
    for _, trail := range trails.TrailList {
        if strings.Contains(*trail.Name, suite.OrganizationName) {
            foundOrgTrail = true
            t.Logf("✅ CloudTrail audit logging konfigurerat: %s", *trail.Name)
        }
    }

    assert.True(t, foundOrgTrail, "Organization CloudTrail should exist for audit logging")
}

// testSvenskaTagging validerar att alla resurser har korrekta svenska tags
func testSvenskaTagging(t *testing.T, suite *SvenskaVPCTestSuite) {
    requiredTags := []string{
        "Environment", "Organization", "CostCenter", 
        "Country", "GDPRCompliant", "DataResidency",
    }

    expectedTagValues := map[string]string{
        "Environment":     suite.Environment,
        "Organization":    suite.OrganizationName,
        "CostCenter":      suite.CostCenter,
        "Country":         "Sweden",
        "GDPRCompliant":   "true",
        "DataResidency":   "Sweden",
    }

    // Test VPC tags
    vpcID := terraform.Output(t, suite.TerraformOptions, "vpc_id")
    ec2Client := ec2.New(suite.AWSSession)

    vpcTags, err := ec2Client.DescribeTags(&ec2.DescribeTagsInput{
        Filters: []*ec2.Filter{
            {
                Name:   aws.String("resource-id"),
                Values: []*string{aws.String(vpcID)},
            },
        },
    })
    require.NoError(t, err, "Failed to describe VPC tags")

    // Konvertera tags till map för enklare validering
    vpcTagMap := make(map[string]string)
    for _, tag := range vpcTags.Tags {
        vpcTagMap[*tag.Key] = *tag.Value
    }

    // Validera obligatoriska tags
    for _, requiredTag := range requiredTags {
        assert.Contains(t, vpcTagMap, requiredTag, "VPC should have required tag: %s", requiredTag)
        
        if expectedValue, exists := expectedTagValues[requiredTag]; exists {
            assert.Equal(t, expectedValue, vpcTagMap[requiredTag], 
                "Tag %s should have correct value", requiredTag)
        }
    }

    t.Logf("✅ Svenska tagging validerat för alla resurser")
}

// cleanupSvenskaVPCTest rensar test environment
func cleanupSvenskaVPCTest(t *testing.T, suite *SvenskaVPCTestSuite) {
    terraform.Destroy(t, suite.TerraformOptions)
    t.Logf("✅ Test environment rensat för %s", suite.OrganizationName)
}
```

---

## Infrastructure as Code - CloudFormation {

Arkitektur som kod-principerna inom detta område#cloudformation-arkitektur som kod}

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

Arkitektur som kod-principerna inom detta område
*Refereras från Kapitel 22: [arkitektur som kod best practices och lärda läxor](22_best_practices.md)*

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
    Based på svenska arkitektur som kod best practices och international standards
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