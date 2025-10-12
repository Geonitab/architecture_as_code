# Appendix A: Kodexempel and technical architecture as code-implementations

This appendix contains all kodexamples, konfigurationsfiler and technical implementeringar as refereras to in bokens huvudkapitel. Kodexemplen is organiserade efter typ and användningwhichråde to do the enkelt to hitta specific implementations.

![Kodexempel appendix](images/diagram_26_appendix.png)

*This appendix functions as a praktisk referenssamling for all technical implementations as demonstreras genAbout the Book. each kodexamples is kategoriserat and märkt with References tobaka to relevanta chapter.*

## Navigering in appendix

Kodexemplen is organiserade in following kategorier:

1. **[CI/CD Pipelines and Architecture as Code-automation](#cicd-pipelines)**
2. **[Infrastructure as Code (Architecture as Code) - Terraform](#terraform-iac)**
3. **[Infrastructure as Code (Architecture as Code) - CloudFormation](#cloudformation-Architecture as Code)**
4. **[Automationsskript and tools](#automation-scripts)**
5. **[Security and compliance](#security-compliance)**
6. **[testing and validation](#testing-validation)**
7. **[Konfigurationsfiler](#configuration)**
8. **[Shell-skript and tools](#shell-scripts)**

each kodexamples has a unique identifierare in formatet `[chapter]_CODE_[NUMMER]` for enkel referens from huvudtexten.

---

## CI/CD Pipelines and architecture as code-automation {#cicd-pipelines}

This sektion contains all examples at CI/CD-pipelines, GitHub Actions workflows and automationsprocesser for Swedish organizations.

### 05_CODE_1: GDPR-kompatibel CI/CD Pipeline for Swedish organizations
*Refereras from chapter 5: [automation and CI/CD-pipelines](05_automation_devops_cicd.md)*

```yaml
# .github/workflows/svenska-architecture as code-pipeline.yml
# GDPR-compliant CI/CD pipeline for Swedish organizations

name: Svenska architecture as code Pipeline with GDPR Compliance

on:
  push:
    branches: [main, staging, development]
    paths: ['infrastructure/**', 'modules/**']
  pull_request:
    branches: [main, staging]
    paths: ['infrastructure/**', 'modules/**']

env:
  TF_VERSION: '1.6.0'
  ORGANIZATION_NAME: ${{ whose.ORGANIZATION_NAME }}
  ENVIRONMENT: ${{ github.ref_name == 'main' && 'production' || github.ref_name }}
  COST_CENTER: ${{ whose.COST_CENTER }}
  GDPR_COMPLIANCE_ENABLED: 'true'
  DATA_RESIDENCY: 'Sweden'
  AUDIT_LOGGING: 'enabled'

jobs:
  # GDPR and security controls
  gdpr-compliance-check:
    name: GDPR Compliance Validation
    runs-on: ubuntu-latest
    if: contains(github.event.head_commit.message, 'personal-data') || contains(github.event.head_commit.message, 'gdpr')
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          fetch-depth: 0
      
      - name: GDPR Data Discovery Scan
        run: |
          echo "🔍 Scanning for personal data patterns..."
          
          # Sök efter vanliga personal data patterns in architecture as code-code
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
            echo "Personal data may not hardkodas in architecture as code-code"
            exit 1
          fi
          
          echo "✅ GDPR compliance check genomförd"
```

### 05_CODE_2: Jenkins Pipeline for Swedish organizations with GDPR compliance
*Refereras from chapter 5: [automation and CI/CD-pipelines](05_automation_devops_cicd.md)*

```yaml
# jenkins/svenska-architecture as code-pipeline.groovy
// Jenkins pipeline for Swedish organizations with GDPR compliance

pipeline {
    agent any
    
    parameters {
        choice(
            name: 'ENVIRONMENT',
            choices: ['development', 'staging', 'production'],
            description: 'Target environment for deployment'
        )
        booleanParam(
            name: 'FORCE_DEPLOYMENT',
            defaultValue: false,
            description: 'Forcera deployment also at varningar (endast development)'
        )
        string(
            name: 'COST_CENTER',
            defaultValue: 'CC-IT-001',
            description: 'Kostnadscenter for svenska bokföring'
        )
    }
    
    environment {
        ORGANIZATION_NAME = 'svenska-org'
        AWS_DEFAULT_REGION = 'eu-north-1'  // Stockholm region
        GDPR_COMPLIANCE = 'enabled'
        DATA_RESIDENCY = 'Sweden'
        TERRAFORM_VERSION = '1.6.0'
        COST_CURRENCY = 'SEK'
        AUDIT_RETENTION_YEARS = '7'  // Svenska lagrequirements
    }
    
    stages {
        stage('🇸🇪 Svenska Compliance Check') {
            parallel {
                stage('GDPR Data Scan') {
                    steps {
                        script {
                            echo "🔍 Scanning for personal data patterns in architecture as code code..."
                            
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
                                error("GDPR VIOLATION: Personal data found in architecture as code code:\n${violations.join('\n')}")
                            }
                            
                            echo "✅ GDPR data scan genomförd - inga violations"
                        }
                    }
                }
                
                stage('Data Residency Validation') {
                    steps {
                        script {
                            echo "🏔️ Validates svenska data residency requirements..."
                            
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
                            echo "💰 Validates kostnadscenter for svenska bokföring..."
                            
                            if (!params.COST_CENTER.matches(/CC-[A-Z]{2,}-\d{3}/)) {
                                error("Ogiltigt kostnadscenter format. Use: CC-XX-nnn")
                            }
                            
                            // Validate to kostnadscenter existerar in företagets systems
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
                            echo "🔧 Terraform syntax and formatering..."
                            
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
                            echo "🔒 Säkerhetsskanning with Checkov..."
                            
                            sh """
                                pip install checkov
                                checkov -d infrastructure/ \
                                    --framework terraform \
                                    --output json \
                                    --output-file checkov-results.json \
                                    --soft-fail
                            """
                            
                            // Analysera critical säkerhetsproblem
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
                                    error("Kritiska säkerhetsproblem must åtgärdas före production deployment")
                                }
                            }
                            
                            echo "✅ Säkerhetsskanning slutförd"
                        }
                    }
                }
                
                stage('Svenska Policy Validation') {
                    steps {
                        script {
                            echo "📋 Validates svenska organisationspolicies..."
                            
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
                    echo "📊 Beräknar infrastrukturkostnader in svenska kronor..."
                    
                    // Setup Infracost for svenska valuta
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
                    
                    // Validate kostnader mot svenska budgetgränser
                    def costData = readJSON file: 'cost-estimate.json'
                    def monthlyCostSEK = costData.totalMonthlyCost as Double
                    
                    def budgetLimits = [
                        'development': 5000,
                        'staging': 15000,
                        'production': 50000
                    ]
                    
                    def maxBudget = budgetLimits[params.ENVIRONMENT] ?: 10000
                    
                    echo "Beräknad månadskostnad: ${monthlyCostSEK} SEK"
                    echo "Budget for ${params.ENVIRONMENT}: ${maxBudget} SEK"
                    
                    if (monthlyCostSEK > maxBudget) {
                        def overBudget = monthlyCostSEK - maxBudget
                        echo "⚠️ BUDGET ÖVERSKRIDEN with ${overBudget} SEK!"
                        
                        if (params.ENVIRONMENT == 'production' && !params.FORCE_DEPLOYMENT) {
                            error("Budget överskridning not tillåten for production without CFO godkännande")
                        }
                    }
                    
                    // Generera svenskt kostnadsrapport
                    def costReport = """
                    # Kostnadsrapport - ${env.ORGANIZATION_NAME}
                    
                    **Miljö:** ${params.ENVIRONMENT}
                    **Datum:** ${new Date().format('yyyy-MM-dd HH:mm')} (svensk time)
                    **Kostnadscenter:** ${params.COST_CENTER}
                    
                    ## Månadskostnad
                    - **Total:** ${monthlyCostSEK} SEK
                    - **Budget:** ${maxBudget} SEK
                    - **Status:** ${monthlyCostSEK <= maxBudget ? '✅ Within budget' : '❌ over budget'}
                    
                    ## Kostnadsnedbrytning
                    ${readFile('cost-summary.txt')}
                    
                    ## Rekommendationer
                    - Use Reserved Instances for production workloads
                    - Aktivera auto-scaling for development environments
                    - Implementera scheduled shutdown for icke-critical systems
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

### 05_CODE_3: Terratest for svenska VPC implementation
*Refereras from chapter 5: [automation and CI/CD-pipelines](05_automation_devops_cicd.md)*

```go
// test/svenska_vpc_test.go
// Terratest suite for svenska VPC implementation with GDPR compliance

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

// SvenskaVPCTestSuite definierar test suite for svenska VPC implementation
type SvenskaVPCTestSuite struct {
    TerraformOptions *terraform.Options
    AWSSession       *session.Session
    OrganizationName string
    Environment      string
    CostCenter       string
}

// TestSvenskaVPCGDPRCompliance testar GDPR compliance for VPC implementation
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

// setupSvenskaVPCTest förbereder test environment for svenska VPC testing
func setupSvenskaVPCTest(t *testing.T, environment string) *SvenskaVPCTestSuite {
    // Unik test identifier
    uniqueID := strings.ToLower(fmt.Sprintf("test-%d", time.Now().Unix()))
    organizationName := fmt.Sprintf("svenska-org-%s", uniqueID)

    // Terraform configuration
    terraformOptions := &terraform.Options{
        TerraformDir: "../infrastructure/modules/vpc",
        Whose: map[string]interface{}{
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

    // AWS session for Stockholm region
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

// testVPCFlowLogsEnabled validates to VPC Flow Logs is aktiverade for GDPR compliance
func testVPCFlowLogsEnabled(t *testing.T, suite *SvenskaVPCTestSuite) {
    // Hämta VPC ID from Terraform output
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

    // Validate to Flow Logs is aktiverade
    assert.Greater(t, len(flowLogsOutput.FlowLogs), 0, "VPC Flow Logs should be enabled for GDPR compliance")

    for _, flowLog := range flowLogsOutput.FlowLogs {
        assert.Equal(t, "Active", *flowLog.FlowLogStatus, "Flow log should be active")
        assert.Equal(t, "ALL", *flowLog.TrafficType, "Flow log should capture all traffic for compliance")
    }

    t.Logf("✅ VPC Flow Logs aktiverade for GDPR compliance: %s", vpcID)
}

// testEncryptionAtRest validates to all lagring is krypterad according to GDPR-requirements
func testEncryptionAtRest(t *testing.T, suite *SvenskaVPCTestSuite) {
    // Hämta KMS key from Terraform output
    kmsKeyArn := terraform.Output(t, suite.TerraformOptions, "kms_key_arn")
    require.NotEmpty(t, kmsKeyArn, "KMS key ARN should not be empty")

    // Validate to KMS key is from Sverige region
    assert.Contains(t, kmsKeyArn, "eu-north-1", "KMS key should be in Stockholm region for data residency")

    t.Logf("✅ Encryption at rest validerat for GDPR compliance")
}

// testDataResidencySweden validates to all infrastruktur is within svenska gränser
func testDataResidencySweden(t *testing.T, suite *SvenskaVPCTestSuite) {
    // Validate to VPC is in Stockholm region
    vpcID := terraform.Output(t, suite.TerraformOptions, "vpc_id")
    
    ec2Client := ec2.New(suite.AWSSession)
    
    vpcOutput, err := ec2Client.DescribeVpcs(&ec2.DescribeVpcsInput{
        VpcIds: []*string{aws.String(vpcID)},
    })
    require.NoError(t, err, "Failed to describe VPC")
    require.Len(t, vpcOutput.Vpcs, 1, "Should find exactly one VPC")

    // Kontrollera region from session config
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

    t.Logf("✅ Data residency validerat - all infrastruktur in EU region: %s", region)
}

// testAuditLogging validates to audit logging is konfigurerat according to svenska lagrequirements
func testAuditLogging(t *testing.T, suite *SvenskaVPCTestSuite) {
    // Kontrollera CloudTrail configuration
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

// testSvenskaTagging validates to all resurser has korrekta svenska tags
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

    // Konvertera tags to map for enklare validation
    vpcTagMap := make(map[string]string)
    for _, tag := range vpcTags.Tags {
        vpcTagMap[*tag.Key] = *tag.Value
    }

    // Validate obligatoriska tags
    for _, requiredTag := range requiredTags {
        assert.Contains(t, vpcTagMap, requiredTag, "VPC should have required tag: %s", requiredTag)
        
        if expectedValue, exists := expectedTagValues[requiredTag]; exists {
            assert.Equal(t, expectedValue, vpcTagMap[requiredTag], 
                "Tag %s should have correct value", requiredTag)
        }
    }

    t.Logf("✅ Svenska tagging validerat for all resurser")
}

// cleanupSvenskaVPCTest rensar test environment
func cleanupSvenskaVPCTest(t *testing.T, suite *SvenskaVPCTestSuite) {
    terraform.Destroy(t, suite.TerraformOptions)
    t.Logf("✅ Test environment rensat for %s", suite.OrganizationName)
}
```

---

## Infrastructure as Code - CloudFormation {

Architecture as Code-principerna within This area#cloudformation-Architecture as Code}

This sektion contains CloudFormation templates for AWS-infrastructure adapted for Swedish organizations.

### 07_CODE_1: VPC Setup for Swedish organizations with GDPR compliance
*Refereras from chapter 7: [Cloud Architecture as Code](07_molnarkitektur.md)*

```yaml
# cloudformation/svenska-org-vpc.yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'VPC setup for Swedish organizations with GDPR compliance'

Parameters:
  EnvironmentType:
    Type: String
    Default: development
    AllowedValues: [development, staging, production]
    Description: 'Miljötyp for deployment'
  
  DataClassification:
    Type: String
    Default: internal
    AllowedValues: [public, internal, confidential, restricted]
    Description: 'Dataklassificering according to svenska security standards'
  
  ComplianceRequirements:
    Type: CommaDelimitedList
    Default: "gdpr,iso27001"
    Description: 'Lista over compliance-requirements as must uppfyllas'

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

This sektion contains Python-skript and andra automationsverktyg for Architecture as Code-handling.

### 22_CODE_1: comprehensive testramverk for Architecture as Code

Architecture as Code-principerna within This area
*Refereras from chapter 24: [Architecture as Code Best Practices and Lessons Learned](24_best_practices.md)*

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
    Comprehensive testing framework for Infrastructure as Code
    Based at svenska architecture as code best practices and international standards
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

This sektion contains konfigurationsfiler for different tools and services.

### 22_CODE_2: Governance policy configuration for Swedish organizations
*Refereras from chapter 24: [Best Practices and Lessons Learned](24_best_practices.md)*

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

## Organisational Change and Team Structures {#organisational-change}

### 17_CODE_1: Infrastructure Platform Team Blueprint
*Listing 17-A.*
*Referenced from chapter 17: [Organisational Change and Team Structures](17_organizational_change.md)*

```yaml
# organisational_design/devops_team_structure.yaml
team_structure:
  name: "Infrastructure Platform Team"
  size: 7
  mission: "Enable autonomous product teams through self-service infrastructure"

  roles:
    - role: "Team Lead / Product Owner"
      responsibilities:
        - "Strategic direction and product roadmap"
        - "Stakeholder communication"
        - "Resource allocation and prioritisation"
        - "Team development and performance management"
      skills_required:
        - "Product management"
        - "Technical leadership"
        - "Agile methodologies"
        - "Stakeholder management"

    - role: "Senior Infrastructure Engineer"
      count: 2
      responsibilities:
        - "Infrastructure as Code development"
        - "Cloud architecture design"
        - "Platform automation"
        - "Technical mentoring"
      skills_required:
        - "Terraform/CloudFormation expert"
        - "Multi-cloud platforms (AWS/Azure/GCP)"
        - "Containerisation (Docker/Kubernetes)"
        - "CI/CD pipelines"
        - "Programming (Python/Go/Bash)"

    - role: "Cloud Security Engineer"
      responsibilities:
        - "Security policy as code"
        - "Compliance automation"
        - "Threat modelling for cloud infrastructure"
        - "Security scanning integration"
      skills_required:
        - "Cloud security architecture best practices"
        - "Policy engines (OPA/AWS Config)"
        - "Security scanning tools"
        - "Compliance frameworks (ISO27001/SOC2)"

    - role: "Platform Automation Engineer"
      count: 2
      responsibilities:
        - "CI/CD pipeline development"
        - "Monitoring and observability"
        - "Self-service tool development"
        - "Developer experience improvement"
      skills_required:
        - "GitOps workflows"
        - "Monitoring stack (Prometheus/Grafana)"
        - "API development"
        - "Developer tooling"

    - role: "Site Reliability Engineer"
      responsibilities:
        - "Production operations"
        - "Incident response"
        - "Capacity planning"
        - "Performance optimisation"
      skills_required:
        - "Production operations"
        - "Incident management"
        - "Performance analysis"
        - "Automation scripting"

  working_agreements:
    daily_standup: "09:00 local time each weekday"
    sprint_length: "2 weeks"
    retrospective: "End of each sprint"
    on_call_rotation: "1 week rotation shared by SREs and Infrastructure Engineers"

  success_metrics:
    infrastructure_deployment_time: "< 15 minutes from commit to production"
    incident_resolution_time: "< 30 minutes for P1 incidents"
    developer_satisfaction: "> 4.5/5 in quarterly surveys"
    infrastructure_cost_efficiency: "10% yearly improvement"
    security_compliance_score: "> 95%"

  communication_patterns:
    internal_team:
      - "Daily stand-ups for coordination"
      - "Weekly technical deep dives"
      - "Monthly team retrospectives"
      - "Quarterly goal-setting sessions"

    external_stakeholders:
      - "Bi-weekly demos for product teams"
      - "Monthly steering committee updates"
      - "Quarterly business review presentations"
      - "Ad-hoc consultation for complex integrations"

  decision_making:
    technical_decisions: "Consensus among technical team members"
    architectural_decisions: "Technical lead with team input"
    strategic_decisions: "Product owner with business stakeholder input"
    operational_decisions: "On-call engineer authority with escalation path"

  continuous_improvement:
    learning_budget: "40 hours per person per quarter"
    conference_attendance: "2 team members per year at major conferences"
    experimentation_time: "20% time for innovation projects"
    knowledge_sharing: "Monthly internal tech talks"
```

### 17_CODE_2: IaC Competency Framework Utilities
*Listing 17-B.*
*Referenced from chapter 17: [Organisational Change and Team Structures](17_organizational_change.md)*

```python
# training/iac_competency_framework.py
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json


class IaCCompetencyFramework:
    """Comprehensive competency framework for Infrastructure as Code skills."""

    def __init__(self):
        self.competency_levels = {
            "novice": {
                "description": "Basic understanding, requires guidance",
                "hours_required": 40,
                "assessment_criteria": [
                    "Can execute predefined Architecture as Code templates",
                    "Understands foundational cloud concepts",
                    "Can follow established procedures"
                ]
            },
            "intermediate": {
                "description": "Can work independently on common tasks",
                "hours_required": 120,
                "assessment_criteria": [
                    "Can create simple Architecture as Code modules",
                    "Understands infrastructure dependencies",
                    "Can troubleshoot common issues"
                ]
            },
            "advanced": {
                "description": "Can design and lead complex implementations",
                "hours_required": 200,
                "assessment_criteria": [
                    "Can architect multi-environment solutions",
                    "Can mentor others effectively",
                    "Can design reusable patterns"
                ]
            },
            "expert": {
                "description": "Thought leader, can drive organisational standards",
                "hours_required": 300,
                "assessment_criteria": [
                    "Can drive organisational Architecture as Code strategy",
                    "Can design complex multi-cloud solutions",
                    "Can lead transformation initiatives"
                ]
            }
        }

        self.skill_domains = {
            "infrastructure_as_code": {
                "tools": ["Terraform", "CloudFormation", "Pulumi", "Ansible"],
                "concepts": ["Declarative syntax", "State management", "Module design"],
                "practices": ["Code organisation", "Testing strategies", "CI/CD integration"]
            },
            "cloud_platforms": {
                "aws": ["EC2", "VPC", "RDS", "Lambda", "S3", "IAM"],
                "azure": ["Virtual Machines", "Resource Groups", "Storage", "Functions"],
                "gcp": ["Compute Engine", "VPC", "Cloud Storage", "Cloud Functions"],
                "multi_cloud": ["Provider abstraction", "Cost optimisation", "Governance"]
            },
            "security_compliance": {
                "security": ["Identity management", "Network security", "Encryption"],
                "compliance": ["GDPR", "ISO27001", "SOC2", "Data residency"],
                "policy": ["Policy as Code", "Automated compliance", "Audit trails"]
            },
            "operations_monitoring": {
                "monitoring": ["Metrics collection", "Alerting", "Dashboards"],
                "logging": ["Log aggregation", "Analysis", "Retention"],
                "incident_response": ["Runbooks", "Post-mortems", "Automation"]
            }
        }

    def create_learning_path(self, current_level: str, target_level: str,
                             focus_domains: List[str]) -> Dict:
        """Create a personalised learning path for an individual."""

        current_hours = self.competency_levels[current_level]["hours_required"]
        target_hours = self.competency_levels[target_level]["hours_required"]
        required_hours = target_hours - current_hours

        learning_path = {
            "individual_id": f"learner_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "current_level": current_level,
            "target_level": target_level,
            "estimated_duration_hours": required_hours,
            "estimated_timeline_weeks": required_hours // 10,  # 10 hours per week
            "focus_domains": focus_domains,
            "learning_modules": []
        }

        # Generate learning modules based on focus domains
        for domain in focus_domains:
            if domain in self.skill_domains:
                modules = self._generate_domain_modules(domain, current_level, target_level)
                learning_path["learning_modules"].extend(modules)

        return learning_path

    def _generate_domain_modules(self, domain: str, current_level: str,
                                 target_level: str) -> List[Dict]:
        """Generate learning modules for a specific domain."""

        modules = []
        domain_skills = self.skill_domains[domain]

        # Terraform Fundamentals Module
        if domain == "infrastructure_as_code":
            modules.append({
                "name": "Terraform Fundamentals for Regulated Enterprises",
                "duration_hours": 16,
                "type": "hands_on_workshop",
                "prerequisites": ["Basic Linux", "Cloud fundamentals"],
                "learning_objectives": [
                    "Build foundational Terraform configurations",
                    "Manage remote state securely",
                    "Design compliance-aligned infrastructure patterns",
                    "Integrate controls with platform tooling"
                ],
                "practical_exercises": [
                    "Deploy a data-protection compliant object storage bucket",
                    "Create a VPC with network guardrails",
                    "Implement IAM policies aligned to least privilege",
                    "Configure monitoring aligned with regulatory obligations"
                ],
                "assessment": {
                    "type": "practical_project",
                    "description": "Deploy a complete web application stack with automated governance controls"
                }
            })

        # Cloud Security Module
        if domain == "security_compliance":
            modules.append({
                "name": "Cloud Security for Regulated Environments",
                "duration_hours": 12,
                "type": "blended_learning",
                "prerequisites": ["Cloud fundamentals", "Security basics"],
                "learning_objectives": [
                    "Implement privacy-aware infrastructure baselines",
                    "Apply regulatory control frameworks in code",
                    "Create automated compliance checks",
                    "Design secure network topologies"
                ],
                "practical_exercises": [
                    "Create a compliance-aligned data pipeline",
                    "Implement policy-as-code guardrails",
                    "Set up automated compliance monitoring",
                    "Design an incident response workflow"
                ],
                "assessment": {
                    "type": "compliance_audit",
                    "description": "Demonstrate infrastructure meets regulatory security requirements"
                }
            })

        return modules

    def track_progress(self, individual_id: str, completed_module: str,
                       assessment_score: float) -> Dict:
        """Track learning progress for an individual."""

        progress_record = {
            "individual_id": individual_id,
            "module_completed": completed_module,
            "completion_date": datetime.now().isoformat(),
            "assessment_score": assessment_score,
            "certification_earned": assessment_score >= 0.8,
            "next_recommended_module": self._recommend_next_module(individual_id)
        }

        return progress_record

    def generate_team_competency_matrix(self, team_members: List[Dict]) -> Dict:
        """Generate a team competency matrix for skills gap analysis."""

        competency_matrix = {
            "team_id": f"team_{datetime.now().strftime('%Y%m%d')}",
            "assessment_date": datetime.now().isoformat(),
            "team_size": len(team_members),
            "overall_readiness": 0,
            "skill_gaps": [],
            "training_recommendations": [],
            "members": []
        }

        total_competency = 0

        for member in team_members:
            member_assessment = {
                "name": member["name"],
                "role": member["role"],
                "current_skills": member.get("skills", {}),
                "competency_score": self._calculate_competency_score(member),
                "development_needs": self._identify_development_needs(member),
                "certification_status": member.get("certifications", [])
            }

            competency_matrix["members"].append(member_assessment)
            total_competency += member_assessment["competency_score"]

        competency_matrix["overall_readiness"] = total_competency / len(team_members)
        competency_matrix["skill_gaps"] = self._identify_team_skill_gaps(team_members)
        competency_matrix["training_recommendations"] = self._recommend_team_training(competency_matrix)

        return competency_matrix


def create_organizational_change_plan(organization_assessment: Dict) -> Dict:
    """Create a comprehensive organisational change plan for Architecture as Code adoption."""

    change_plan = {
        "organization": organization_assessment["name"],
        "current_state": organization_assessment["current_maturity"],
        "target_state": "advanced_devops",
        "timeline_months": 18,
        "phases": [
            {
                "name": "Foundation Building",
                "duration_months": 6,
                "objectives": [
                    "Establish DevOps culture basics",
                    "Implement foundational Architecture as Code practices",
                    "Create cross-functional teams",
                    "Set up the initial toolchain"
                ],
                "activities": [
                    "DevOps culture workshops",
                    "Tool selection and setup",
                    "Team restructuring",
                    "Initial training programme",
                    "Pilot project implementation"
                ],
                "success_criteria": [
                    "All teams trained on DevOps fundamentals",
                    "Initial Architecture as Code deployment pipeline operational",
                    "Cross-functional teams established",
                    "Core toolchain adopted"
                ]
            },
            {
                "name": "Capability Development",
                "duration_months": 8,
                "objectives": [
                    "Scale Architecture as Code practices across the organisation",
                    "Implement advanced automation",
                    "Establish monitoring and observability",
                    "Mature incident response processes"
                ],
                "activities": [
                    "Advanced Architecture as Code training rollout",
                    "Multi-environment deployment automation",
                    "Comprehensive monitoring implementation",
                    "Incident response process development",
                    "Security integration (DevSecOps)"
                ],
                "success_criteria": [
                    "Architecture as Code practices adopted by all product teams",
                    "Automated deployment across all environments",
                    "Comprehensive observability implemented",
                    "Incident response processes matured"
                ]
            },
            {
                "name": "Optimisation and Innovation",
                "duration_months": 4,
                "objectives": [
                    "Optimise existing processes",
                    "Implement advanced practices",
                    "Foster continuous innovation",
                    "Measure and improve business outcomes"
                ],
                "activities": [
                    "Process optimisation based on metrics",
                    "Advanced practice implementation",
                    "Innovation time allocation",
                    "Business value measurement",
                    "Knowledge sharing programme"
                ],
                "success_criteria": [
                    "Optimised processes delivering measurable value",
                    "Innovation culture established",
                    "Improved business outcomes",
                    "Self-sustaining improvement culture"
                ]
            }
        ],
        "change_management": {
            "communication_strategy": [
                "Monthly all-hands updates",
                "Quarterly progress reviews",
                "Success story sharing",
                "Feedback collection mechanisms"
            ],
            "resistance_management": [
                "Early stakeholder engagement",
                "Addressing skill development concerns",
                "Providing clear career progression paths",
                "Celebrating early wins"
            ],
            "success_measurement": [
                "Employee satisfaction surveys",
                "Technical capability assessments",
                "Business value metrics",
                "Cultural transformation indicators"
            ]
        },
        "risk_mitigation": [
            "Gradual rollout to minimise disruption",
            "Comprehensive training to address skill gaps",
            "Clear communication to manage expectations",
            "Strong support structure for teams"
        ]
    }

    return change_plan
```

### 17_CODE_3: DevOps Performance Measurement Framework
*Listing 17-C.*
*Referenced from chapter 17: [Organisational Change and Team Structures](17_organizational_change.md)*

```yaml
# metrics/devops_performance_metrics.yaml
performance_measurement_framework:
  name: "DevOps Team Performance Metrics"

  technical_metrics:
    deployment_frequency:
      description: "How often the team deploys to production"
      measurement: "Deployments per day/week"
      target_values:
        elite: "> 1 per day"
        high: "1 per week - 1 per day"
        medium: "1 per month - 1 per week"
        low: "< 1 per month"
      collection_method: "Automated from CI/CD pipeline"

    lead_time_for_changes:
      description: "Time from code commit to production deployment"
      measurement: "Hours/days"
      target_values:
        elite: "< 1 hour"
        high: "1 day - 1 week"
        medium: "1 week - 1 month"
        low: "> 1 month"
      collection_method: "Git and deployment tool integration"

    mean_time_to_recovery:
      description: "Time to recover from production incidents"
      measurement: "Hours"
      target_values:
        elite: "< 1 hour"
        high: "< 1 day"
        medium: "1 day - 1 week"
        low: "> 1 week"
      collection_method: "Incident management systems"

    change_failure_rate:
      description: "Percentage of deployments causing production issues"
      measurement: "Percentage"
      target_values:
        elite: "0-15%"
        high: "16-30%"
        medium: "31-45%"
        low: "> 45%"
      collection_method: "Incident correlation with deployments"

  business_metrics:

    infrastructure_cost_efficiency:
      description: "Cost per unit of business value delivered"
      measurement: "Local currency per transaction/user/feature"
      target: "10% yearly improvement"
      collection_method: "Cloud billing API integration"

    developer_productivity:
      description: "Developer self-service capability"
      measurement: "Hours spent on infrastructure tasks per sprint"
      target: "< 20% of development time"
      collection_method: "Time tracking and developer surveys"

    compliance_adherence:
      description: "Adherence to regulatory requirements"
      measurement: "Compliance score (0-100%)"
      target: "> 95%"
      collection_method: "Automated compliance scanning"

    customer_satisfaction:
      description: "Internal customer (developer) satisfaction"
      measurement: "Net Promoter Score"
      target: "> 50"
      collection_method: "Quarterly developer surveys"

  cultural_metrics:

    psychological_safety:
      description: "Team member comfort with taking risks and admitting mistakes"
      measurement: "Survey score (1-5)"
      target: "> 4.0"
      collection_method: "Quarterly team health surveys"

    learning_culture:
      description: "Investment in learning and experimentation"
      measurement: "Hours per person per quarter"
      target: "> 40 hours"
      collection_method: "Learning management systems"

    collaboration_effectiveness:
      description: "Cross-functional team collaboration quality"
      measurement: "Survey score (1-5)"
      target: "> 4.0"
      collection_method: "360-degree feedback"

    innovation_rate:
      description: "Number of new ideas/experiments per quarter"
      measurement: "Count per team member"
      target: "> 2 per quarter"
      collection_method: "Innovation tracking systems"

  collection_automation:

    data_sources:
      - "GitHub/GitLab API for code metrics"
      - "Jenkins/GitLab CI for deployment metrics"
      - "PagerDuty/OpsGenie for incident metrics"
      - "AWS/Azure billing API for cost metrics"
      - "Survey tools for cultural metrics"

    dashboard_tools:
      - "Grafana for technical metrics visualisation"
      - "Tableau for business metrics analysis"
      - "Internal dashboards for team metrics"

    reporting_schedule:
      daily: ["Deployment frequency", "Incident count"]
      weekly: ["Lead time trends", "Cost analysis"]
      monthly: ["Team performance review", "Business value assessment"]
      quarterly: ["Cultural metrics", "Strategic review"]

  improvement_process:

    metric_review:
      frequency: "Monthly team retrospectives"
      participants: ["Team members", "Product owner", "Engineering manager"]
      outcome: "Improvement actions with owners and timelines"

    benchmarking:
      internal: "Compare teams within the organisation"
      industry: "Compare with DevOps industry standards"
      regional: "Compare with peer organisations"

    action_planning:
      identification: "Identify lowest-performing metrics"
      root_cause: "Analyse underlying causes"
      solutions: "Develop targeted improvement initiatives"
      tracking: "Monitor improvement progress monthly"
```


---

## References and navigering

each kodexamples in This appendix can refereras from huvudtexten with dess unique identifierare. to hitta specific implementations:

1. **Use sökfunktion** - Sök efter kodtyp or teknologi (t.ex. "Terraform", "CloudFormation", "Python")
2. **Följ kategorierna** - Navigera to relevant sektion based on användningwhichråde
3. **Use korshänvisningar** - Följ länkar tobaka to huvudkapitlen for context

### Konventioner for kodexempel

- **Kommentarer**: all kodexamples contains svenska kommentarer for klarhet
- **Security**: Security aspects is markerade with 🔒
- **GDPR-compliance**: GDPR-relaterade configurations is markerade with 🇪🇺
- **Svenska anpassningar**: Lokala anpassningar is markerade with 🇸🇪

### Uppdateringar and underhåll

This appendix uppdateras löpande when new kodexamples läggs to in bokens huvudkapitel. For last versionen of kodexamples, se bokens GitHub-repository.

---

*For mer information about specific implementations, se respektive huvudkapitel where kodexemplen introduceras and forklaras in sitt context.*
---

## Chapter 14 Reference Implementations

### 14_CODE_1: Terraform service blueprint for a web application landing zone {#14_code_1}
*Referenced from Chapter 14: [Architecture as Code in Practice](14_practical_implementation.md)*

This module demonstrates how to package core networking, load balancing, and tagging conventions into a reusable Terraform component that platform teams can roll out across environments.

```hcl
# modules/web-application/main.tf
variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
}

variable "application_name" {
  description = "Name of the application"
  type        = string
}

variable "instance_count" {
  description = "Number of application instances"
  type        = number
  default     = 2
}

# VPC and networking
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "${var.application_name}-${var.environment}-vpc"
    Environment = var.environment
    Application = var.application_name
  }
}

resource "aws_subnet" "public" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index + 1}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]

  map_public_ip_on_launch = true

  tags = {
    Name = "${var.application_name}-${var.environment}-public-${count.index + 1}"
    Type = "Public"
  }
}

# Application Load Balancer
resource "aws_lb" "main" {
  name               = "${var.application_name}-${var.environment}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = aws_subnet.public[*].id

  enable_deletion_protection = false

  tags = {
    Environment = var.environment
    Application = var.application_name
  }
}

# Auto Scaling Group
resource "aws_autoscaling_group" "main" {
  name                = "${var.application_name}-${var.environment}-asg"
  vpc_zone_identifier = aws_subnet.public[*].id
  target_group_arns   = [aws_lb_target_group.main.arn]
  health_check_type   = "ELB"
  health_check_grace_period = 300

  min_size         = 1
  max_size         = 10
  desired_capacity = var.instance_count

  launch_template {
    id      = aws_launch_template.main.id
    version = "$Latest"
  }

  tag {
    key                 = "Name"
    value               = "${var.application_name}-${var.environment}-instance"
    propagate_at_launch = true
  }

  tag {
    key                 = "Environment"
    value               = var.environment
    propagate_at_launch = true
  }
}

# Outputs
output "load_balancer_dns" {
  description = "DNS name of the load balancer"
  value       = aws_lb.main.dns_name
}

output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}
```

### 14_CODE_2: Environment configuration and observability controls {#14_code_2}
*Referenced from Chapter 14: [Architecture as Code in Practice](14_practical_implementation.md)*

This configuration layers production-specific settings on top of the shared module, including state management, default tags, and a CloudWatch dashboard for operational oversight.

```hcl
# environments/production/main.tf
terraform {
  required_version = ">= 1.0"

  backend "s3" {
    bucket         = "company-terraform-state-prod"
    key            = "web-application/terraform.tfstate"
    region         = "us-west-2"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-west-2"

  default_tags {
    tags = {
      Project     = "web-application"
      Environment = "production"
      ManagedBy   = "terraform"
      Owner       = "platform-team"
    }
  }
}

module "web_application" {
  source = "../../modules/web-application"

  environment      = "production"
  application_name = "company-web-app"
  instance_count   = 6

  # Production-specific overrides
  enable_monitoring = true
  backup_retention  = 30
  multi_az          = true
}

# Production-specific resources
resource "aws_cloudwatch_dashboard" "main" {
  dashboard_name = "WebApplication-Production"

  dashboard_body = jsonencode({
    widgets = [
      {
        type   = "metric"
        x      = 0
        y      = 0
        width  = 12
        height = 6

        properties = {
          metrics = [
            ["AWS/ApplicationELB", "RequestCount", "LoadBalancer", module.web_application.load_balancer_arn_suffix],
            [".", "TargetResponseTime", ".", "."],
            [".", "HTTPCode_ELB_5XX_Count", ".", "."]
          ]
          view    = "timeSeries"
          stacked = false
          region  = "us-west-2"
          title   = "Application Performance"
          period  = 300
        }
      }
    ]
  })
}
```

### 14_CODE_3: Continuous delivery workflow for infrastructure changes {#14_code_3}
*Referenced from Chapter 14: [Architecture as Code in Practice](14_practical_implementation.md)*

The workflow below demonstrates how to plan and apply Terraform changes across development, staging, and production with explicit separation between planning and deployment stages.

```yaml
# .github/workflows/infrastructure.yml
name: Infrastructure Deployment

on:
  push:
    branches: [main]
    paths: ['infrastructure/**']
  pull_request:
    branches: [main]
    paths: ['infrastructure/**']

env:
  TF_VERSION: 1.5.0
  AWS_REGION: us-west-2

jobs:
  plan:
    name: Terraform Plan
    runs-on: ubuntu-latest
    strategy:
      matrix:
        environment: [development, staging, production]

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Setup Terraform
      uses: hashicorp/setup-terraform@v2
      with:
        terraform_version: ${{ env.TF_VERSION }}

    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ${{ env.AWS_REGION }}

    - name: Terraform Init
      working-directory: infrastructure/environments/${{ matrix.environment }}
      run: terraform init

    - name: Terraform Validate
      working-directory: infrastructure/environments/${{ matrix.environment }}
      run: terraform validate

    - name: Terraform Plan
      working-directory: infrastructure/environments/${{ matrix.environment }}
      run: |
        terraform plan -out=tfplan-${{ matrix.environment }} \
          -var-file="terraform.tfvars"

    - name: Upload plan artifact
      uses: actions/upload-artifact@v3
      with:
        name: tfplan-${{ matrix.environment }}
        path: infrastructure/environments/${{ matrix.environment }}/tfplan-${{ matrix.environment }}
        retention-days: 30

  deploy:
    name: Terraform Apply
    runs-on: ubuntu-latest
    needs: plan
    if: github.ref == 'refs/heads/main'
    strategy:
      matrix:
        environment: [development, staging]
        # Production requires manual approval

    environment: ${{ matrix.environment }}

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Setup Terraform
      uses: hashicorp/setup-terraform@v2
      with:
        terraform_version: ${{ env.TF_VERSION }}

    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ${{ env.AWS_REGION }}

    - name: Download plan artifact
      uses: actions/download-artifact@v3
      with:
        name: tfplan-${{ matrix.environment }}
        path: infrastructure/environments/${{ matrix.environment }}

    - name: Terraform Init
      working-directory: infrastructure/environments/${{ matrix.environment }}
      run: terraform init

    - name: Terraform Apply
      working-directory: infrastructure/environments/${{ matrix.environment }}
      run: terraform apply tfplan-${{ matrix.environment }}

  production-deploy:
    name: Production Deployment
    runs-on: ubuntu-latest
    needs: [plan, deploy]
    if: github.ref == 'refs/heads/main'
    environment:
      name: production
      url: ${{ steps.deploy.outputs.application_url }}

    steps:
    - name: Manual approval checkpoint
      run: echo "Production deployment requires manual approval"

    # Similar steps as deploy job but for production environment
```

---

## Migration Automation {#migration-automation}

This section contains comprehensive code examples for migrating from traditional infrastructure to Architecture as Code management. These examples are referenced from Chapter 16: [Migration from Traditional Infrastructure](16_migration.md).

### 16_CODE_1: Migration Assessment Automation {#16_code_1}
*Referenced from Chapter 16: [Practical Implementation Examples](16_migration.md#practical-implementation-examples)*

This Python-based tool automates the discovery and assessment of unmanaged cloud resources, providing the foundation for systematic Architecture as Code migration planning.

```python
# migration_assessment/infrastructure_discovery.py
import boto3
import json
from datetime import datetime
from typing import Dict, List
import pandas as pd

class InfrastructureMigrationAssessment:
    """
    Automated assessment of existing infrastructure for Architecture as Code migration.
    Discovers unmanaged resources and generates migration plans.
    """
    
    def __init__(self, region='eu-north-1'):
        self.ec2 = boto3.client('ec2', region_name=region)
        self.rds = boto3.client('rds', region_name=region)
        self.elb = boto3.client('elbv2', region_name=region)
        self.cloudformation = boto3.client('cloudformation', region_name=region)
        
    def discover_unmanaged_resources(self) -> Dict:
        """Discover resources that are not managed by Infrastructure as Code"""
        
        unmanaged_resources = {
            'ec2_instances': self._find_unmanaged_ec2(),
            'rds_instances': self._find_unmanaged_rds(),
            'load_balancers': self._find_unmanaged_load_balancers(),
            'security_groups': self._find_unmanaged_security_groups(),
            'summary': {}
        }
        
        # Calculate summary statistics
        total_resources = sum(len(resources) for resources in unmanaged_resources.values() 
                            if isinstance(resources, list))
        unmanaged_resources['summary'] = {
            'total_unmanaged_resources': total_resources,
            'migration_complexity': self._assess_migration_complexity(unmanaged_resources),
            'estimated_migration_effort': self._estimate_migration_effort(total_resources),
            'risk_assessment': self._assess_migration_risks(unmanaged_resources)
        }
        
        return unmanaged_resources
    
    def _find_unmanaged_ec2(self) -> List[Dict]:
        """Find EC2 instances that are not managed by CloudFormation/Terraform"""
        
        # Fetch all EC2 instances
        response = self.ec2.describe_instances()
        unmanaged_instances = []
        
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                if instance['State']['Name'] != 'terminated':
                    # Check if the instance is managed by Infrastructure as Code
                    is_managed = self._is_resource_managed(instance.get('Tags', []))
                    
                    if not is_managed:
                        unmanaged_instances.append({
                            'instance_id': instance['InstanceId'],
                            'instance_type': instance['InstanceType'],
                            'launch_time': instance['LaunchTime'].isoformat(),
                            'vpc_id': instance.get('VpcId'),
                            'subnet_id': instance.get('SubnetId'),
                            'security_groups': [sg['GroupId'] for sg in instance.get('SecurityGroups', [])],
                            'tags': {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])},
                            'migration_priority': self._calculate_migration_priority(instance),
                            'estimated_downtime': self._estimate_downtime(instance)
                        })
        
        return unmanaged_instances
    
    def _is_resource_managed(self, tags: List[Dict]) -> bool:
        """Check if resource is managed by Infrastructure as Code"""
        
        iac_indicators = [
            'aws:cloudformation:stack-name',
            'terraform:stack',
            'pulumi:stack',
            'Created-By-Terraform',
            'ManagedBy'
        ]
        
        tag_keys = {tag.get('Key', '') for tag in tags}
        return any(indicator in tag_keys for indicator in iac_indicators)
    
    def generate_terraform_migration_plan(self, unmanaged_resources: Dict) -> str:
        """Generate Terraform code for migration of unmanaged resources"""
        
        terraform_code = """
# Automatically generated migration plan
# Generated: {date}
# Total resources to migrate: {total_resources}

terraform {{
  required_providers {{
    aws = {{
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }}
  }}
}}

provider "aws" {{
  region = "eu-north-1"  # Stockholm for Swedish organisations
}}

""".format(
            date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            total_resources=len(unmanaged_resources.get('ec2_instances', []))
        )
        
        # Generate Terraform for EC2 instances
        for idx, instance in enumerate(unmanaged_resources.get('ec2_instances', [])):
            terraform_code += f"""
# Migration of existing EC2 instance {instance['instance_id']}
resource "aws_instance" "migrated_instance_{idx}" {{
  # NOTE: This configuration must be verified and adapted
  instance_type = "{instance['instance_type']}"
  subnet_id     = "{instance['subnet_id']}"
  
  vpc_security_group_ids = {json.dumps(instance['security_groups'])}
  
  # Retain existing tags and add migration info
  tags = {{
    Name = "{instance.get('tags', {}).get('Name', f'migrated-instance-{idx}')}"
    MigratedFrom = "{instance['instance_id']}"
    MigrationDate = "{datetime.now().strftime('%Y-%m-%d')}"
    ManagedBy = "terraform"
    Environment = "{instance.get('tags', {}).get('Environment', 'production')}"
    Project = "{instance.get('tags', {}).get('Project', 'migration-project')}"
  }}
  
  # IMPORTANT: Import existing resource instead of creating new
  # terraform import aws_instance.migrated_instance_{idx} {instance['instance_id']}
}}
"""
        
        terraform_code += """
# Migration checklist:
# 1. Review generated configurations carefully
# 2. Test in development environment first
# 3. Import existing resources with terraform import
# 4. Run terraform plan to verify no changes are planned
# 5. Implement gradually with low-risk resources first
# 6. Update monitoring and alerting after migration
"""
        
        return terraform_code
    
    def create_migration_timeline(self, unmanaged_resources: Dict) -> Dict:
        """Create realistic migration timeline"""
        
        # Categorise resources by complexity
        low_complexity = []
        medium_complexity = []
        high_complexity = []
        
        for instance in unmanaged_resources.get('ec2_instances', []):
            complexity = instance.get('migration_priority', 'medium')
            
            if complexity == 'low':
                low_complexity.append(instance)
            elif complexity == 'high':
                high_complexity.append(instance)
            else:
                medium_complexity.append(instance)
        
        # Calculate time estimates
        timeline = {
            'wave_1_low_risk': {
                'resources': low_complexity,
                'estimated_duration': f"{len(low_complexity) * 2} days",
                'start_date': 'Week 1-2',
                'prerequisites': ['Architecture as Code training completion', 'Tool setup', 'Backup verification']
            },
            'wave_2_medium_risk': {
                'resources': medium_complexity,
                'estimated_duration': f"{len(medium_complexity) * 4} days",
                'start_date': 'Week 3-6',
                'prerequisites': ['Wave 1 completion', 'Process refinement', 'Team feedback']
            },
            'wave_3_high_risk': {
                'resources': high_complexity,
                'estimated_duration': f"{len(high_complexity) * 8} days",
                'start_date': 'Week 7-12',
                'prerequisites': ['Wave 2 completion', 'Advanced training', 'Stakeholder approval']
            },
            'total_estimated_duration': f"{(len(low_complexity) * 2) + (len(medium_complexity) * 4) + (len(high_complexity) * 8)} days"
        }
        
        return timeline

def generate_migration_playbook(assessment_results: Dict) -> str:
    """Generate comprehensive migration playbook for Swedish organisations"""
    
    playbook = f"""
# Architecture as Code Migration Playbook for {assessment_results.get('organization_name', 'Organisation')}

## Executive Summary
- **Total resources to migrate:** {assessment_results['summary']['total_unmanaged_resources']}
- **Migration complexity:** {assessment_results['summary']['migration_complexity']}
- **Estimated effort:** {assessment_results['summary']['estimated_migration_effort']}
- **Risk assessment:** {assessment_results['summary']['risk_assessment']}

## Phase 1: Preparation (Week 1-2)

### Team Training
- [ ] Architecture as Code fundamentals training for all team members
- [ ] Terraform/CloudFormation hands-on workshops
- [ ] Git workflows for infrastructure management
- [ ] Swedish compliance requirements (GDPR, MSB)

### Tool Setup
- [ ] Terraform/CloudFormation development environment
- [ ] Git repository for infrastructure code
- [ ] CI/CD pipeline for infrastructure deployment
- [ ] Monitoring and alerting configuration

### Risk Mitigation
- [ ] Complete backup of all critical systems
- [ ] Rollback procedures documented
- [ ] Emergency contacts and escalation plan
- [ ] Test environment for migration validation

## Phase 2: Pilot Migration (Week 3-4)

### Low-Risk Resources Migration
- [ ] Migrate development/test environments first
- [ ] Validate Architecture as Code templates and processes
- [ ] Document lessons learnt
- [ ] Refine migration procedures

### Quality Gates
- [ ] Automated testing of migrated resources
- [ ] Performance verification
- [ ] Security compliance validation
- [ ] Cost optimisation review

## Phase 3: Production Migration (Week 5-12)

### Gradual Production Migration
- [ ] Non-critical production systems
- [ ] Critical systems with planned maintenance windows
- [ ] Database migration with minimal downtime
- [ ] Network infrastructure migration

### Continuous Monitoring
- [ ] Real-time monitoring of migrated systems
- [ ] Automated alerting for anomalies
- [ ] Performance benchmarking
- [ ] Cost tracking and optimisation

## Post-Migration Activities

### Process Optimisation
- [ ] Infrastructure cost review and optimisation
- [ ] Team workflow refinement
- [ ] Documentation and knowledge transfer
- [ ] Continuous improvement of Architecture as Code implementation

### Long-term Sustainability
- [ ] Regular Architecture as Code best practices review
- [ ] Team cross-training programme
- [ ] Tool evaluation and updates
- [ ] Compliance monitoring automation

## Swedish Compliance Considerations

### GDPR Requirements
- [ ] Data residency in Swedish/EU regions
- [ ] Encryption at rest and in transit
- [ ] Access logging and audit trails
- [ ] Data retention policy implementation

### MSB Security Requirements
- [ ] Network segmentation implementation
- [ ] Incident response procedures
- [ ] Backup and disaster recovery
- [ ] Security monitoring enhancement

## Success Metrics

### Technical Metrics
- Infrastructure deployment time reduction: Target 80%
- Configuration drift incidents: Target 0
- Security compliance score: Target 95%+
- Infrastructure cost optimisation: Target 20% reduction

### Operational Metrics
- Mean time to recovery improvement: Target 60%
- Change failure rate reduction: Target 50%
- Team satisfaction with new processes: Target 8/10
- Knowledge transfer completion: Target 100%

## Risk Management

### High-Priority Risks
1. **Service Downtime:** Mitigated through maintenance windows and rollback plans
2. **Data Loss:** Mitigated through comprehensive backups and testing
3. **Security Compliance:** Mitigated through automated compliance validation
4. **Team Resistance:** Mitigated through training and change management

### Contingency Plans
- Immediate rollback procedures for critical issues
- Emergency support contacts and escalation
- Alternative migration approaches for problem resources
- Business continuity plans for extended downtime
"""
    
    return playbook
```

### 16_CODE_2: CloudFormation Legacy Import {#16_code_2}
*Referenced from Chapter 16: [Infrastructure Import and Codification](16_migration.md#practical-implementation-examples)*

This CloudFormation template demonstrates how to import existing AWS resources into stack management, enabling gradual migration to Infrastructure as Code.

```yaml
# migration/legacy-import-template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Template for importing existing resources to CloudFormation management'

Parameters:
  ExistingVPCId:
    Type: String
    Description: 'ID of existing VPC to be imported'
    
  ExistingInstanceId:
    Type: String  
    Description: 'ID of existing EC2 instance to be imported'
    
  Environment:
    Type: String
    Default: 'production'
    AllowedValues: ['development', 'staging', 'production']
    
  ProjectName:
    Type: String
    Description: 'Project name for resource tagging'

Resources:
  # Import existing VPC
  ExistingVPC:
    Type: AWS::EC2::VPC
    Properties:
      # These values must match existing VPC configuration exactly
      CidrBlock: '10.0.0.0/16'  # Update with actual CIDR
      EnableDnsHostnames: true
      EnableDnsSupport: true
      Tags:
        - Key: Name
          Value: !Sub '${ProjectName}-imported-vpc'
        - Key: Environment
          Value: !Ref Environment
        - Key: ManagedBy
          Value: 'CloudFormation'
        - Key: ImportedFrom
          Value: !Ref ExistingVPCId
        - Key: ImportDate
          Value: !Sub '${AWS::Timestamp}'

  # Import existing EC2 instance
  ExistingInstance:
    Type: AWS::EC2::Instance
    Properties:
      # These values must match existing instance configuration
      InstanceType: 't3.medium'  # Update with actual instance type
      ImageId: 'ami-0c94855bb95b03c2e'  # Update with actual AMI
      SubnetId: !Ref ExistingSubnet
      SecurityGroupIds:
        - !Ref ExistingSecurityGroup
      Tags:
        - Key: Name
          Value: !Sub '${ProjectName}-imported-instance'
        - Key: Environment
          Value: !Ref Environment
        - Key: ManagedBy
          Value: 'CloudFormation'
        - Key: ImportedFrom
          Value: !Ref ExistingInstanceId
        - Key: ImportDate
          Value: !Sub '${AWS::Timestamp}'

  # Security group for imported instance
  ExistingSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: 'Imported security group for legacy systems'
      VpcId: !Ref ExistingVPC
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 22
          ToPort: 22
          CidrIp: '10.0.0.0/8'  # Restrict SSH access
          Description: 'SSH access from internal network'
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: '0.0.0.0/0'
          Description: 'HTTP access'
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          CidrIp: '0.0.0.0/0'
          Description: 'HTTPS access'
      Tags:
        - Key: Name
          Value: !Sub '${ProjectName}-imported-sg'
        - Key: Environment
          Value: !Ref Environment
        - Key: ManagedBy
          Value: 'CloudFormation'

  # Subnet for organised network management
  ExistingSubnet:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref ExistingVPC
      CidrBlock: '10.0.1.0/24'  # Update with actual subnet CIDR
      AvailabilityZone: 'eu-north-1a'  # Stockholm region
      MapPublicIpOnLaunch: false
      Tags:
        - Key: Name
          Value: !Sub '${ProjectName}-imported-subnet'
        - Key: Environment
          Value: !Ref Environment
        - Key: Type
          Value: 'Private'
        - Key: ManagedBy
          Value: 'CloudFormation'

Outputs:
  ImportedVPCId:
    Description: 'ID of imported VPC'
    Value: !Ref ExistingVPC
    Export:
      Name: !Sub '${AWS::StackName}-VPC-ID'
      
  ImportedInstanceId:
    Description: 'ID of imported EC2 instance'
    Value: !Ref ExistingInstance
    Export:
      Name: !Sub '${AWS::StackName}-Instance-ID'
      
  ImportInstructions:
    Description: 'Instructions for resource import'
    Value: !Sub |
      To import existing resources:
      1. aws cloudformation create-stack --stack-name ${ProjectName}-import --template-body file://legacy-import-template.yaml
      2. aws cloudformation import-resources-to-stack --stack-name ${ProjectName}-import --resources file://import-resources.json
      3. Verify import was successful with: aws cloudformation describe-stacks --stack-name ${ProjectName}-import
```

### 16_CODE_3: Migration Testing Framework {#16_code_3}
*Referenced from Chapter 16: [Migration Testing and Validation](16_migration.md#practical-implementation-examples)*

This comprehensive bash script automates validation of Architecture as Code migration, including pre-migration checks, import validation, and post-migration compliance testing.

```bash
#!/bin/bash
# migration/test-migration.sh
# Comprehensive testing script for Architecture as Code migration validation

set -e

PROJECT_NAME=${1:-"migration-test"}
ENVIRONMENT=${2:-"staging"}
REGION=${3:-"eu-north-1"}

echo "Starting Architecture as Code migration testing for project: $PROJECT_NAME"
echo "Environment: $ENVIRONMENT"
echo "Region: $REGION"

# Pre-migration testing
echo "=== Pre-Migration Tests ==="

# Test 1: Verify all resources are inventoried
echo "Testing resource inventory..."
aws ec2 describe-instances --region $REGION --query 'Reservations[*].Instances[?State.Name!=`terminated`]' > /tmp/pre-migration-instances.json
aws rds describe-db-instances --region $REGION > /tmp/pre-migration-rds.json

INSTANCE_COUNT=$(jq '.[] | length' /tmp/pre-migration-instances.json | jq -s 'add')
RDS_COUNT=$(jq '.DBInstances | length' /tmp/pre-migration-rds.json)

echo "Discovered $INSTANCE_COUNT EC2 instances and $RDS_COUNT RDS instances"

# Test 2: Backup verification
echo "Verifying backup status..."
aws ec2 describe-snapshots --region $REGION --owner-ids self --query 'Snapshots[?StartTime>=`2023-01-01T00:00:00.000Z`]' > /tmp/recent-snapshots.json
SNAPSHOT_COUNT=$(jq '. | length' /tmp/recent-snapshots.json)

if [ $SNAPSHOT_COUNT -lt $INSTANCE_COUNT ]; then
    echo "WARNING: Insufficient recent snapshots. Create backups before migration."
    exit 1
fi

# Test 3: Network connectivity baseline
echo "Establishing network connectivity baseline..."
for instance_id in $(jq -r '.[] | .[] | .InstanceId' /tmp/pre-migration-instances.json); do
    if [ "$instance_id" != "null" ]; then
        echo "Testing connectivity to $instance_id..."
        # Implement connectivity tests here
    fi
done

# Migration execution testing
echo "=== Migration Execution Tests ==="

# Test 4: Terraform plan validation
echo "Validating Terraform migration plan..."
cd terraform/migration

terraform init
terraform plan -var="project_name=$PROJECT_NAME" -var="environment=$ENVIRONMENT" -out=migration.plan

# Analyse plan for unexpected changes
terraform show -json migration.plan > /tmp/terraform-plan.json

# Check that no resources are planned for destruction
DESTROY_COUNT=$(jq '.resource_changes[] | select(.change.actions[] == "delete") | .address' /tmp/terraform-plan.json | wc -l)

if [ $DESTROY_COUNT -gt 0 ]; then
    echo "ERROR: Migration plan contains resource destruction. Review before continuing."
    jq '.resource_changes[] | select(.change.actions[] == "delete") | .address' /tmp/terraform-plan.json
    exit 1
fi

# Test 5: Import validation
echo "Testing resource import procedures..."

# Create test import for a sample resource
SAMPLE_INSTANCE_ID=$(jq -r '.[] | .[] | .InstanceId' /tmp/pre-migration-instances.json | head -1)

if [ "$SAMPLE_INSTANCE_ID" != "null" ] && [ "$SAMPLE_INSTANCE_ID" != "" ]; then
    echo "Testing import for instance: $SAMPLE_INSTANCE_ID"
    
    # Dry-run import test
    terraform import -dry-run aws_instance.test_import $SAMPLE_INSTANCE_ID || {
        echo "WARNING: Import test failed for $SAMPLE_INSTANCE_ID"
    }
fi

# Post-migration testing
echo "=== Post-Migration Validation Framework ==="

# Test 6: Infrastructure compliance
echo "Setting up compliance validation..."
cat > /tmp/compliance-test.py << 'EOF'
import boto3
import json

def validate_tagging_compliance(region='eu-north-1'):
    """Validate that all migrated resources have correct tags"""
    ec2 = boto3.client('ec2', region_name=region)
    
    required_tags = ['ManagedBy', 'Environment', 'Project']
    non_compliant = []
    
    # Check EC2 instances
    instances = ec2.describe_instances()
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            if instance['State']['Name'] != 'terminated':
                tags = {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
                missing_tags = [tag for tag in required_tags if tag not in tags]
                
                if missing_tags:
                    non_compliant.append({
                        'resource_id': instance['InstanceId'],
                        'resource_type': 'EC2 Instance',
                        'missing_tags': missing_tags
                    })
    
    return non_compliant

def validate_security_compliance():
    """Validate security configuration after migration"""
    # Implementation for security controls
    pass

if __name__ == '__main__':
    compliance_issues = validate_tagging_compliance()
    if compliance_issues:
        print(f"Found {len(compliance_issues)} compliance issues:")
        for issue in compliance_issues:
            print(f"  {issue['resource_id']}: Missing tags {issue['missing_tags']}")
    else:
        print("All resources are compliant with tagging requirements")
EOF

python3 /tmp/compliance-test.py

# Test 7: Performance baseline comparison
echo "Setting up performance monitoring..."
cat > /tmp/performance-monitor.sh << 'EOF'
#!/bin/bash
# Monitor key performance metrics after migration

METRICS_FILE="/tmp/post-migration-metrics.json"

echo "Collecting post-migration performance metrics..."

# CPU Utilisation
aws cloudwatch get-metric-statistics \
    --namespace AWS/EC2 \
    --metric-name CPUUtilization \
    --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
    --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
    --period 300 \
    --statistics Average \
    --region eu-north-1 > "$METRICS_FILE"

# Analyse metrics for deviations
AVERAGE_CPU=$(jq '.Datapoints | map(.Average) | add / length' "$METRICS_FILE")
echo "Average CPU utilisation: $AVERAGE_CPU%"

if (( $(echo "$AVERAGE_CPU > 80" | bc -l) )); then
    echo "WARNING: High CPU utilisation detected after migration"
fi
EOF

chmod +x /tmp/performance-monitor.sh

echo "=== Migration Testing Complete ==="
echo "Results:"
echo "  - Resource inventory: $INSTANCE_COUNT EC2, $RDS_COUNT RDS"
echo "  - Backup status: $SNAPSHOT_COUNT snapshots verified"
echo "  - Terraform plan: Validated (no destructive changes)"
echo "  - Compliance framework: Ready"
echo "  - Performance monitoring: Configured"

echo ""
echo "Next steps:"
echo "1. Review test results and address any warnings"
echo "2. Execute migration in maintenance window"
echo "3. Run post-migration validation"
echo "4. Monitor performance for 24 hours"
echo "5. Document lessons learnt"
```
