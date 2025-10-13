# Appendix A: Kodexempel and technical architecture as code-implementations

This appendix contains all kodexamples, konfigurationsfiler and technical implementeringar as refereras to in bokens huvudkapitel. Kodexemplen is organiserade efter typ and användningwhichråde to do the enkelt to hitta specific implementations.

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

---

## Chapter 13: Testing Strategies Reference Implementations {#chapter-13-testing}

This section contains comprehensive code examples referenced in Chapter 13: Testing Strategies for Infrastructure as Code.

### 13_CODE_A: Vitest Configuration for Infrastructure as Code Projects {#13_code_a}
*Listing 13-A.*
*Referenced from Chapter 13: [Testing Strategies](13_testing_strategies.md)*

This configuration demonstrates how to set up Vitest for testing infrastructure configuration generators and validation scripts.

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import path from 'path';

export default defineConfig({
  test: {
    // Use globals to avoid imports in each test file
    globals: true,
    
    // Test environment (node for infrastructure tooling)
    environment: 'node',
    
    // Coverage configuration
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'dist/',
        '**/*.config.ts',
        '**/types/**',
      ],
      // Require at least 80% coverage for infrastructure code
      lines: 80,
      functions: 80,
      branches: 80,
      statements: 80,
    },
    
    // Test timeout for infrastructure operations
    testTimeout: 30000,
    
    // Include test files
    include: ['**/*.{test,spec}.{js,mjs,cjs,ts,mts,cts}'],
    
    // Exclude patterns
    exclude: [
      'node_modules',
      'dist',
      '.terraform',
      '**/*.d.ts',
    ],
  },
  
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@infra': path.resolve(__dirname, './infrastructure'),
    },
  },
});
```

### 13_CODE_B: Terraform Configuration Generator {#13_code_b}
*Listing 13-B.*
*Referenced from Chapter 13: [Testing Strategies](13_testing_strategies.md)*

This TypeScript module demonstrates programmatic generation of Terraform configurations with built-in compliance validation.

```typescript
// src/generators/terraform-config.ts
export interface TerraformConfig {
  provider: string;
  region: string;
  environment: string;
  resources: ResourceConfig[];
}

export interface ResourceConfig {
  type: string;
  name: string;
  properties: Record<string, any>;
}

export class TerraformConfigGenerator {
  generateVPCConfig(
    environment: string,
    region: string = 'eu-north-1'
  ): TerraformConfig {
    // Validate EU regions for GDPR compliance
    const euRegions = ['eu-north-1', 'eu-west-1', 'eu-central-1'];
    if (!euRegions.includes(region)) {
      throw new Error('Region must be within EU for GDPR compliance');
    }

    return {
      provider: 'aws',
      region,
      environment,
      resources: [
        {
          type: 'aws_vpc',
          name: `vpc-${environment}`,
          properties: {
            cidr_block: '10.0.0.0/16',
            enable_dns_hostnames: true,
            enable_dns_support: true,
            tags: {
              Name: `vpc-${environment}`,
              Environment: environment,
              ManagedBy: 'Terraform',
              GdprCompliant: 'true',
              DataResidency: 'EU',
            },
          },
        },
      ],
    };
  }

  generateRDSConfig(
    environment: string,
    instanceClass: string = 'db.t3.micro',
    encrypted: boolean = true
  ): ResourceConfig {
    // Ensure encryption for production
    if (environment === 'production' && !encrypted) {
      throw new Error('Production databases must have encryption enabled');
    }

    return {
      type: 'aws_db_instance',
      name: `rds-${environment}`,
      properties: {
        allocated_storage: environment === 'production' ? 100 : 20,
        engine: 'postgres',
        engine_version: '14.7',
        instance_class: instanceClass,
        storage_encrypted: encrypted,
        backup_retention_period: environment === 'production' ? 30 : 7,
        multi_az: environment === 'production',
        tags: {
          Environment: environment,
          GdprCompliant: 'true',
          EncryptionEnabled: encrypted.toString(),
        },
      },
    };
  }
}
```

### 13_CODE_C: Terraform Configuration Generator Tests {#13_code_c}
*Listing 13-C.*
*Referenced from Chapter 13: [Testing Strategies](13_testing_strategies.md)*

Comprehensive test suite demonstrating validation of configuration generators with GDPR compliance checks.

(See Chapter 13 for full test implementation covering VPC configuration, GDPR compliance tags, regional restrictions and RDS encryption requirements)

### 13_CODE_D: Infrastructure Validator {#13_code_d}
*Listing 13-D.*
*Referenced from Chapter 13: [Testing Strategies](13_testing_strategies.md)*

Infrastructure validation module that checks resources against organisational policies and compliance requirements.

(See Chapter 13 for full implementation covering resource tag validation, data classification checks and security group rule verification)

### 13_CODE_E: Infrastructure Validator Tests {#13_code_e}
*Listing 13-E.*
*Referenced from Chapter 13: [Testing Strategies](13_testing_strategies.md)*

Comprehensive test suite for infrastructure validation covering tags, security groups and compliance policies.

(See Chapter 13 for full test suite demonstrating tag requirement validation, security group port restrictions and GDPR compliance warnings)

### 13_CODE_F: GitHub Actions Vitest Workflow {#13_code_f}
*Listing 13-F.*
*Referenced from Chapter 13: [Testing Strategies](13_testing_strategies.md)*

CI/CD workflow demonstrating automated infrastructure code testing with coverage reporting.

(See Chapter 13 for complete GitHub Actions workflow including test execution, coverage generation and PR comment integration)

### 13_CODE_G: Requirements as Code Definition {#13_code_g}
*Listing 13-G.*
*Referenced from Chapter 13: [Testing Strategies](13_testing_strategies.md)*

YAML-based requirements definition enabling traceability from business requirements to automated tests with compliance mapping and test specifications.

(See Chapter 13 for YAML schema demonstrating security requirements, performance requirements and associated test specifications)

### 13_CODE_H: Requirements Validation Framework {#13_code_h}
*Listing 13-H.*
*Referenced from Chapter 13: [Testing Strategies](13_testing_strategies.md)*

Python framework for automated validation of requirements against Infrastructure as Code implementations, including test execution and compliance coverage reporting.

(See Chapter 13 for Python implementation of RequirementValidator class with test execution and compliance coverage calculation)

### 13_CODE_I: Terratest for GDPR-Compliant Infrastructure {#13_code_i}
*Listing 13-I.*
*Referenced from Chapter 13: [Testing Strategies](13_testing_strategies.md)*

Comprehensive Terratest example demonstrating testing of Terraform infrastructure with GDPR compliance validation, data residency requirements and organisational tagging standards for regulated environments.

(See Chapter 13 for Go implementation demonstrating VPC flow logs validation, encryption verification, data residency checks and audit logging validation)

### 13_CODE_J: Policy-as-Code Testing with OPA {#13_code_j}
*Listing 13-J.*
*Referenced from Chapter 13: [Testing Strategies](13_testing_strategies.md)*

Open Policy Agent (OPA) test examples demonstrating validation of S3 bucket encryption, EC2 security group requirements and GDPR data classification compliance.

(See Chapter 13 for Rego policy tests covering S3 encryption requirements, EC2 security group configuration and GDPR data classification validation)

### 13_CODE_K: Kubernetes Infrastructure Test Suite {#13_code_k}
*Listing 13-K.*
*Referenced from Chapter 13: [Testing Strategies](13_testing_strategies.md)*

Comprehensive Kubernetes infrastructure test suite demonstrating validation of resource quotas, pod security policies, network policies and GDPR-compliant persistent volume encryption using ConfigMap-based test runners and Kubernetes Jobs.

(See Chapter 13 for Kubernetes ConfigMap and Job manifests implementing infrastructure validation tests)

### 13_CODE_L: Infrastructure Testing Pipeline {#13_code_l}
*Listing 13-L.*
*Referenced from Chapter 13: [Testing Strategies](13_testing_strategies.md)*

Complete GitHub Actions workflow demonstrating infrastructure testing pipeline with static analysis (Terraform fmt, Checkov, OPA), unit testing (Terratest), integration testing with temporary environments, compliance validation (GDPR, encryption, regional restrictions), and performance testing with cost analysis.

(See Chapter 13 for complete GitHub Actions YAML workflow covering all testing stages from static analysis through to production deployment validation)

---

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

## Chapter 15 Reference Implementations

### 15_CODE_1: Cost-aware Terraform infrastructure configuration {#15_code_1}
*Referenced from Chapter 15: [Cost Optimization and Resource Management](15_cost_optimization.md)*

This Terraform configuration demonstrates comprehensive cost optimization strategies including budget management, cost allocation tagging, and intelligent instance type selection using spot instances and mixed instance policies.

```hcl
# cost_optimized_infrastructure.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Cost allocation tags for all infrastruktur
locals {
  cost_tags = {
    CostCenter     = var.cost_center
    Project        = var.project_name
    Environment    = var.environment
    Owner          = var.team_email
    BudgetAlert    = var.budget_threshold
    ReviewDate     = formatdate("YYYY-MM-DD", timeadd(timestamp(), "30*24h"))
  }
}

# Budget with automatiska alerts
resource "aws_budgets_budget" "project_budget" {
  name         = "${var.project_name}-budget"
  budget_type  = "COST"
  limit_amount = var.monthly_budget_limit
  limit_unit   = "USD"
  time_unit    = "MONTHLY"
  
  cost_filters = {
    Tag = {
      Project = [var.project_name]
    }
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                 = 80
    threshold_type            = "PERCENTAGE"
    notification_type         = "ACTUAL"
    subscriber_email_addresses = [var.team_email, var.finance_email]
  }

  notification {
    comparison_operator        = "GREATER_THAN"  
    threshold                 = 100
    threshold_type            = "PERCENTAGE"
    notification_type          = "FORECASTED"
    subscriber_email_addresses = [var.team_email, var.finance_email]
  }
}

# Cost-optimerad EC2 with Spot instances
resource "aws_launch_template" "cost_optimized" {
  name_prefix   = "${var.project_name}-cost-opt-"
  image_id      = data.aws_ami.amazon_linux.id
  
  # Mischade instance types for cost optimization
  instance_requirements {
    memory_mib {
      min = 2048
      max = 8192
    }
    vcpu_count {
      min = 1
      max = 4
    }
    instance_generations = ["current"]
  }

  # Spot instance preference for kostnadsoptimering
  instance_market_options {
    market_type = "spot"
    spot_options {
      max_price = var.max_spot_price
    }
  }

  tag_specifications {
    resource_type = "instance"
    tags = local.cost_tags
  }
}

# Auto Scaling with kostnadshänsyn
resource "aws_autoscaling_group" "cost_aware" {
  name                = "${var.project_name}-cost-aware-asg"
  vpc_zone_identifier = var.private_subnet_ids
  min_size            = var.min_instances
  max_size            = var.max_instances
  desired_capacity    = var.desired_instances

  # Blandad instanstyp-strategi for kostnadsoptimering
  mixed_instances_policy {
    instances_distribution {
      on_demand_base_capacity                  = 1
      on_demand_percentage_above_base_capacity = 20
      spot_allocation_strategy                 = "diversified"
    }

    launch_template {
      launch_template_specification {
        launch_template_id = aws_launch_template.cost_optimized.id
        version            = "$Latest"
      }
    }
  }

  tag {
    key                 = "Name"
    value               = "${var.project_name}-cost-optimized"
    propagate_at_launch = true
  }

  dynamic "tag" {
    for_each = local.cost_tags
    content {
      key                 = tag.key
      value               = tag.value
      propagate_at_launch = true
    }
  }
}
```

### 15_CODE_2: Kubernetes cost optimization manifests {#15_code_2}
*Referenced from Chapter 15: [Cost Optimization and Resource Management](15_cost_optimization.md)*

These Kubernetes manifests demonstrate resource quotas, limit ranges, and autoscaling configurations for cost-effective workload management.

```yaml
# kubernetes/cost-optimization-quota.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: cost-control-quota
  namespace: production
spec:
  hard:
    requests.cpu: "20"
    requests.memory: 40Gi
    limits.cpu: "40"
    limits.memory: 80Gi
    persistentvolumeclaims: "10"
    count/pods: "50"
    count/services: "10"
---
# kubernetes/cost-optimization-limits.yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: cost-control-limits
  namespace: production
spec:
  limits:
  - default:
      cpu: "500m"
      memory: "1Gi"
    defaultRequest:
      cpu: "100m"
      memory: "256Mi"
    max:
      cpu: "2"
      memory: "4Gi"
    min:
      cpu: "50m"
      memory: "128Mi"
    type: Container
---
# kubernetes/vertical-pod-autoscaler.yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: cost-optimized-vpa
  namespace: production
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-application
  updatePolicy:
    updateMode: "Auto"
  resourcePolicy:
    containerPolicies:
    - containerName: app
      maxAllowed:
        cpu: "1"
        memory: "2Gi"
      minAllowed:
        cpu: "100m"
        memory: "256Mi"
---
# kubernetes/horizontal-pod-autoscaler.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: cost-aware-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-application
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 100
        periodSeconds: 60
```

### 15_CODE_3: AWS cost monitoring and optimization automation {#15_code_3}
*Referenced from Chapter 15: [Cost Optimization and Resource Management](15_cost_optimization.md)*

This Python script provides automated cost analysis, rightsizing recommendations, and identification of unused resources for AWS environments.

```python
# cost_monitoring/cost_optimizer.py
import boto3
import json
from datetime import datetime, timedelta
from typing import Dict, List
import pandas as pd

class AWSCostOptimizer:
    """
    Automatiserad kostnadsoptimering for AWS-resurser
    """
    
    def __init__(self, region='eu-north-1'):
        self.cost_explorer = boto3.client('ce', region_name=region)
        self.ec2 = boto3.client('ec2', region_name=region)
        self.rds = boto3.client('rds', region_name=region)
        self.cloudwatch = boto3.client('cloudwatch', region_name=region)
        
    def analyze_cost_trends(self, days_back=30) -> Dict:
        """Analysera kostnadstrender for last perioden"""
        
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days_back)
        
        response = self.cost_explorer.get_cost_and_usage(
            TimePeriod={
                'Start': start_date.strftime('%Y-%m-%d'),
                'End': end_date.strftime('%Y-%m-%d')
            },
            Granularity='DAILY',
            Metrics=['BlendedCost'],
            GroupBy=[
                {'Type': 'DIMENSION', 'Key': 'SERVICE'},
                {'Type': 'TAG', 'Key': 'Project'}
            ]
        )
        
        return self._process_cost_data(response)
    
    def identify_rightsizing_opportunities(self) -> List[Dict]:
        """Identifiera EC2-instanser as can rightsizas"""
        
        rightsizing_response = self.cost_explorer.get_rightsizing_recommendation(
            Service='AmazonEC2',
            Configuration={
                'BenefitsConsidered': True,
                'RecommendationTarget': 'SAME_INSTANCE_FAMILY'
            }
        )
        
        opportunities = []
        
        for recommendation in rightsizing_response.get('RightsizingRecommendations', []):
            if recommendation['RightsizingType'] == 'Modify':
                opportunities.append({
                    'instance_id': recommendation['CurrentInstance']['ResourceId'],
                    'current_type': recommendation['CurrentInstance']['InstanceName'],
                    'recommended_type': recommendation['ModifyRecommendationDetail']['TargetInstances'][0]['InstanceName'],
                    'estimated_monthly_savings': float(recommendation['ModifyRecommendationDetail']['TargetInstances'][0]['EstimatedMonthlySavings']),
                    'utilization': recommendation['CurrentInstance']['UtilizationMetrics']
                })
        
        return opportunities
    
    def get_unused_resources(self) -> Dict:
        """Identifiera oanvända resurser as can termineras"""
        
        unused_resources = {
            'unattached_volumes': self._find_unattached_ebs_volumes(),
            'unused_elastic_ips': self._find_unused_elastic_ips(),
            'idle_load_balancers': self._find_idle_load_balancers(),
            'stopped_instances': self._find_stopped_instances()
        }
        
        return unused_resources
    
    def generate_cost_optimization_plan(self, project_tag: str) -> Dict:
        """Generera comprehensive kostnadsoptimeringsplan"""
        
        plan = {
            'project': project_tag,
            'analysis_date': datetime.now().isoformat(),
            'current_monthly_cost': self._get_current_monthly_cost(project_tag),
            'recommendations': {
                'rightsizing': self.identify_rightsizing_opportunities(),
                'unused_resources': self.get_unused_resources(),
                'reserved_instances': self._analyze_reserved_instance_opportunities(),
                'spot_instances': self._analyze_spot_instance_opportunities()
            },
            'potential_monthly_savings': 0
        }
        
        # Beräkna total potentiell besparing
        total_savings = 0
        for rec_type, recommendations in plan['recommendations'].items():
            if isinstance(recommendations, list):
                total_savings += sum(rec.get('estimated_monthly_savings', 0) for rec in recommendations)
            elif isinstance(recommendations, dict):
                total_savings += recommendations.get('estimated_monthly_savings', 0)
        
        plan['potential_monthly_savings'] = total_savings
        plan['savings_percentage'] = (total_savings / plan['current_monthly_cost']) * 100 if plan['current_monthly_cost'] > 0 else 0
        
        return plan
    
    def _find_unattached_ebs_volumes(self) -> List[Dict]:
        """Hitta icke-anslutna EBS-volymer"""
        
        response = self.ec2.describe_volumes(
            Filters=[{'Name': 'status', 'Values': ['available']}]
        )
        
        unattached_volumes = []
        for volume in response['Volumes']:
            # Beräkna månadskostnad based on volymstorlek and typ
            monthly_cost = self._calculate_ebs_monthly_cost(volume)
            
            unattached_volumes.append({
                'volume_id': volume['VolumeId'],
                'size_gb': volume['Size'],
                'volume_type': volume['VolumeType'],
                'estimated_monthly_savings': monthly_cost,
                'creation_date': volume['CreateTime'].isoformat()
            })
        
        return unattached_volumes
    
    def _calculate_ebs_monthly_cost(self, volume: Dict) -> float:
        """Beräkna månadskostnad for EBS-volym"""
        
        # Prisexempel for eu-north-1 (Stockholm)
        pricing = {
            'gp3': 0.096,  # USD per GB/månad
            'gp2': 0.114,
            'io1': 0.142,
            'io2': 0.142,
            'st1': 0.050,
            'sc1': 0.028
        }
        
        cost_per_gb = pricing.get(volume['VolumeType'], 0.114)  # Default to gp2
        return volume['Size'] * cost_per_gb

def generate_terraform_cost_optimizations(cost_plan: Dict) -> str:
    """Generera Terraform-code to implement kostnadsoptimeringar"""
    
    terraform_code = """
# automatically genererade kostnadsoptimeringar
# Genererat: {date}
# Projekt: {project}
# Potentiell månadsbesparing: ${savings:.2f}

""".format(
        date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        project=cost_plan['project'],
        savings=cost_plan['potential_monthly_savings']
    )
    
    # Generera spot instance configurations
    if cost_plan['recommendations']['spot_instances']:
        terraform_code += """
# Spot Instance Configuration for kostnadsoptimering
resource "aws_launch_template" "spot_optimized" {
  name_prefix   = "{project}-spot-"
  
  instance_market_options {{
    market_type = "spot"
    spot_options {{
      max_price = "{max_spot_price}"
    }}
  }}
  
  # Cost allocation tags
  tag_specifications {{
    resource_type = "instance"
    tags = {{
      Project = "{project}"
      CostOptimization = "spot-instance"
      EstimatedSavings = "${estimated_savings}"
    }}
  }}
}}
""".format(
            project=cost_plan['project'],
            max_spot_price=cost_plan['recommendations']['spot_instances'].get('recommended_max_price', '0.10'),
            estimated_savings=cost_plan['recommendations']['spot_instances'].get('estimated_monthly_savings', 0)
        )
    
    return terraform_code
```

## Security and compliance {#security-compliance}

### 10_CODE_1: Advanced Policy-as-Code module for Swedish compliance {#10_code_1}
*Referenced from Chapter 10: [Policy and Security as Code in Detail](10_policy_and_security.md).* This Rego module consolidates encryption validation, network segmentation checks inspired by MSB guidance, and GDPR Article 44 data residency controls. It generates a composite compliance score so teams can fail builds or raise alerts when thresholds are breached.

```rego
package se.enterprise.security

import rego.v1

encryption_required_services := {
    "aws_s3_bucket",
    "aws_rds_instance",
    "aws_rds_cluster",
    "aws_efs_file_system",
    "aws_dynamodb_table",
    "aws_redshift_cluster",
    "aws_elasticsearch_domain"
}

administrative_ports := {22, 3389, 5432, 3306, 1433, 27017, 6379, 9200, 5601}
allowed_public_ports := {80, 443}
eu_regions := {"eu-north-1", "eu-west-1", "eu-west-2", "eu-west-3", "eu-central-1", "eu-south-1"}

encryption_compliant[resource] {
    resource := input.resources[_]
    resource.type in encryption_required_services
    encryption := get_encryption_status(resource)
    validation := validate_encryption_strength(encryption)
    validation.compliant
}

get_encryption_status(resource) := result {
    resource.type == "aws_s3_bucket"
    result := {
        "at_rest": has_s3_encryption(resource),
        "in_transit": has_s3_ssl_policy(resource),
        "key_management": resource.attributes.kms_key_type
    }
}

get_encryption_status(resource) := result {
    resource.type == "aws_rds_instance"
    result := {
        "at_rest": resource.attributes.storage_encrypted,
        "in_transit": resource.attributes.force_ssl,
        "key_management": resource.attributes.kms_key_type
    }
}

validate_encryption_strength(encryption) := result {
    encryption.at_rest
    encryption.in_transit
    key_validation := validate_key_management(encryption.key_management)
    result := {
        "compliant": key_validation.approved,
        "strength": key_validation.strength,
        "recommendations": key_validation.recommendations
    }
}

validate_key_management("customer_managed") := {
    "approved": true,
    "strength": "high",
    "recommendations": []
}

validate_key_management("aws_managed") := {
    "approved": true,
    "strength": "medium",
    "recommendations": [
        "Consider migrating to customer managed keys for greater control",
        "Enable automatic key rotation"
    ]
}

validate_key_management(_) := {
    "approved": false,
    "strength": "low",
    "recommendations": [
        "Configure an approved KMS key",
        "Document ownership within the OSCAL profile"
    ]
}

network_security_violations[violation] {
    resource := input.resources[_]
    resource.type == "aws_security_group"
    violation := check_ingress_rules(resource)
    violation.severity in ["critical", "high"]
}

check_ingress_rules(sg) := violation {
    rule := sg.attributes.ingress[_]
    rule.cidr_blocks[_] == "0.0.0.0/0"
    rule.from_port in administrative_ports
    violation := {
        "type": "critical_port_exposure",
        "severity": "critical",
        "port": rule.from_port,
        "security_group": sg.attributes.name,
        "message": sprintf("Administrative port %v is exposed to the internet", [rule.from_port]),
        "remediation": "Restrict access to dedicated management networks",
        "reference": "MSB 3.2.1 Network Segmentation"
    }
}

check_ingress_rules(sg) := violation {
    rule := sg.attributes.ingress[_]
    rule.cidr_blocks[_] == "0.0.0.0/0"
    not rule.from_port in allowed_public_ports
    not rule.from_port in administrative_ports
    violation := {
        "type": "non_standard_port_exposure",
        "severity": "high",
        "port": rule.from_port,
        "security_group": sg.attributes.name,
        "message": sprintf("Non-standard port %v is exposed to the internet", [rule.from_port]),
        "remediation": "Validate the business requirement and narrow the CIDR range",
        "reference": "MSB 3.2.2 Minimal Exposure"
    }
}

data_sovereignty_compliant[resource] {
    resource := input.resources[_]
    resource.type in {
        "aws_s3_bucket", "aws_rds_instance", "aws_rds_cluster",
        "aws_dynamodb_table", "aws_elasticsearch_domain",
        "aws_redshift_cluster", "aws_efs_file_system"
    }
    classification := determine_classification(resource)
    result := validate_region(resource, classification)
    result.compliant
}

determine_classification(resource) := classification {
    classification := resource.attributes.tags["DataClassification"]
    classification != ""
}

determine_classification(resource) := "personal" {
    contains(lower(resource.attributes.name), "personal")
}

determine_classification(resource) := "personal" {
    resource.type in ["aws_rds_instance", "aws_rds_cluster"]
    indicators := {"user", "customer", "gdpr", "pii"}
    some indicator in indicators
    contains(lower(resource.attributes.identifier), indicator)
}

determine_classification(_) := "internal"

validate_region(resource, "personal") := {
    "compliant": get_resource_region(resource) in eu_regions,
    "requirement": "GDPR Articles 44–49"
}

validate_region(resource, _) := {
    "compliant": true,
    "requirement": "Internal data — EU residency not mandatory"
}

get_resource_region(resource) := region {
    region := resource.attributes.region
    region != ""
}

get_resource_region(resource) := region {
    az := resource.attributes.availability_zone
    region := substring(az, 0, count(az) - 1)
}

get_resource_region(_) := "unknown"

compliance_assessment := result {
    encryption_violations := [
        create_encryption_violation(resource) |
        resource := input.resources[_];
        resource.type in encryption_required_services;
        not encryption_compliant[resource]
    ]

    network_violations := [v | v := network_security_violations[_]]

    sovereignty_violations := [
        create_sovereignty_violation(resource) |
        resource := input.resources[_];
        resource.type in encryption_required_services;
        not data_sovereignty_compliant[resource]
    ]

    violations := array.concat(array.concat(encryption_violations, network_violations), sovereignty_violations)

    result := {
        "overall_score": calculate_score(violations),
        "violations": violations,
        "regulators": {
            "gdpr": assess_regulator("GDPR", violations),
            "msb": assess_regulator("MSB", violations),
            "iso27001": assess_regulator("ISO 27001", violations)
        }
    }
}

create_encryption_violation(resource) := {
    "type": "encryption_required",
    "severity": "critical",
    "resource": resource.type,
    "message": "Mandatory encryption is disabled",
    "remediation": "Enable encryption at rest and enforce TLS in transit",
    "reference": "GDPR Article 32"
}

create_sovereignty_violation(resource) := {
    "type": "data_sovereignty",
    "severity": "critical",
    "resource": resource.type,
    "message": sprintf("Personal data stored outside approved EU regions (%v)", [get_resource_region(resource)]),
    "remediation": "Move the workload to an EU region or document an adequacy decision",
    "reference": "GDPR Articles 44–49"
}

calculate_score(violations) := score {
    penalties := [penalty |
        violation := violations[_];
        penalty := severity_penalties[violation.severity]
    ]
    score := math.max(0, 100 - sum(penalties))
}

severity_penalties := {
    "critical": 25,
    "high": 15,
    "medium": 10,
    "low": 5
}

assess_regulator(name, violations) := {
    "name": name,
    "open_findings": count([v | v := violations[_]; contains(lower(v.reference), lower(name))])
}
```

### 10_CODE_2: OSCAL profile for regulated Swedish financial services {#10_code_2}
*Referenced from Chapter 10.* This OSCAL profile merges controls from NIST SP 800-53 with GDPR Article 32 and MSB network segmentation expectations. Parameters clarify the encryption standard and key management practices adopted by the organisation.

```json
{
  "profile": {
    "uuid": "87654321-4321-8765-4321-876543218765",
    "metadata": {
      "title": "Swedish Financial Institutions Security Profile",
      "published": "2024-01-15T11:00:00Z",
      "last-modified": "2024-01-15T11:00:00Z",
      "version": "2.1",
      "oscal-version": "1.1.2",
      "props": [
        { "name": "organization", "value": "Swedish Financial Sector" },
        { "name": "jurisdiction", "value": "Sweden" }
      ]
    },
    "imports": [
      {
        "href": "https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json",
        "include-controls": [
          { "matching": [ { "pattern": "ac-.*" }, { "pattern": "au-.*" }, { "pattern": "sc-.*" } ] }
        ]
      },
      {
        "href": "swedish-regional-catalog.json",
        "include-controls": [
          { "matching": [ { "pattern": "gdpr-.*" }, { "pattern": "msb-.*" } ] }
        ]
      }
    ],
    "merge": {
      "combine": { "method": "merge" }
    },
    "modify": {
      "set-parameters": [
        {
          "param-id": "gdpr-art32-1_prm1",
          "values": ["AES-256-GCM"]
        },
        {
          "param-id": "gdpr-art32-1_prm2",
          "values": ["AWS KMS customer managed keys backed by HSM"]
        },
        {
          "param-id": "msb-3.2.1_prm1",
          "values": ["Zero Trust segmentation enforced via AWS Network Firewall"]
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
                  "id": "gdpr-art32-1_fin-guidance",
                  "name": "guidance",
                  "title": "Finansinspektionen Supplement",
                  "prose": "Payment service providers must use FIPS 140-2 validated encryption modules and review key material every 90 days."
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
                  "id": "msb-3.2.1_fin-requirement",
                  "name": "requirement",
                  "title": "Financial Sector Isolation",
                  "prose": "Critical payment workloads must be isolated in dedicated network segments with inspection by AWS Network Firewall and VPC Traffic Mirroring."
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

### 10_CODE_3: OSCAL component definitions for reusable cloud modules {#10_code_3}
*Referenced from Chapter 10.* Component definitions document how Terraform modules satisfy regulatory expectations. This example captures Amazon RDS, Amazon S3, and AWS Network Firewall implementations used throughout the Swedish financial profile.

```json
{
  "component-definition": {
    "uuid": "11223344-5566-7788-99aa-bbccddeeff00",
    "metadata": {
      "title": "AWS Components for Swedish Regulated Workloads",
      "published": "2024-01-15T12:00:00Z",
      "last-modified": "2024-01-15T12:00:00Z",
      "version": "1.5",
      "oscal-version": "1.1.2"
    },
    "components": [
      {
        "uuid": "comp-aws-rds-mysql",
        "type": "software",
        "title": "Amazon RDS MySQL",
        "description": "Managed relational database configured for GDPR Article 32 compliance.",
        "control-implementations": [
          {
            "source": "swedish-regional-catalog.json",
            "implemented-requirements": [
              {
                "control-id": "gdpr-art32-1.1",
                "description": "Encryption at rest enabled with customer managed KMS keys.",
                "statements": [
                  {
                    "statement-id": "gdpr-art32-1.1_smt",
                    "description": "Default encryption uses AES-256 with keys rotated every 365 days.",
                    "implementation-status": { "state": "implemented" }
                  }
                ],
                "props": [
                  { "name": "kms-key-type", "value": "customer-managed" },
                  { "name": "rotation", "value": "365 days" }
                ]
              },
              {
                "control-id": "msb-3.2.1.1",
                "description": "Database subnet groups isolated from public subnets.",
                "statements": [
                  {
                    "statement-id": "msb-3.2.1.1_smt",
                    "description": "Only application load balancers within the VPC may initiate connections.",
                    "implementation-status": { "state": "implemented" }
                  }
                ]
              }
            ]
          }
        ]
      },
      {
        "uuid": "comp-aws-s3",
        "type": "software",
        "title": "Amazon S3 Secure Bucket",
        "description": "Object storage with automatic encryption and access logging.",
        "control-implementations": [
          {
            "source": "swedish-regional-catalog.json",
            "implemented-requirements": [
              {
                "control-id": "gdpr-art32-1.2",
                "description": "Enforced TLS 1.2 for all data in transit.",
                "statements": [
                  {
                    "statement-id": "gdpr-art32-1.2_smt",
                    "description": "S3 bucket policies block non-TLS requests and log denials.",
                    "implementation-status": { "state": "implemented" }
                  }
                ]
              },
              {
                "control-id": "msb-3.2.1.2",
                "description": "Zero Trust verification for access using IAM conditions.",
                "statements": [
                  {
                    "statement-id": "msb-3.2.1.2_smt",
                    "description": "IAM policies require device posture attributes for privileged access.",
                    "implementation-status": { "state": "planned" }
                  }
                ]
              }
            ]
          }
        ]
      },
      {
        "uuid": "comp-aws-network-firewall",
        "type": "software",
        "title": "AWS Network Firewall",
        "description": "Edge inspection enforcing MSB segmentation and logging requirements.",
        "control-implementations": [
          {
            "source": "swedish-regional-catalog.json",
            "implemented-requirements": [
              {
                "control-id": "msb-3.2.1",
                "description": "Micro-segmentation between payment and support zones.",
                "statements": [
                  {
                    "statement-id": "msb-3.2.1_smt",
                    "description": "Stateful rules restrict lateral movement and mirror traffic to a central collector.",
                    "implementation-status": { "state": "implemented" }
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

### 10_CODE_4: Automated OSCAL System Security Plan generator {#10_code_4}
*Referenced from Chapter 10.* This Python utility ingests Terraform state, merges it with component definitions, and produces a machine-readable OSCAL SSP. The script is designed to run inside CI so every deployment updates the compliance evidence set.

```python
"""Generate OSCAL System Security Plans from Terraform configurations."""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List

import boto3
import hcl2


@dataclass
class ComponentDefinition:
    """Representation of an OSCAL component definition file."""

    path: Path
    content: Dict[str, Any]


class OSCALSSPGenerator:
    """Build an OSCAL-compliant System Security Plan from source files."""

    def __init__(self, terraform_directory: Path, component_paths: Iterable[Path]):
        self.terraform_directory = terraform_directory
        self.component_paths = list(component_paths)
        self.sts = boto3.client("sts")

    def generate(self, profile_href: str, system_name: str) -> Dict[str, Any]:
        resources = self._parse_terraform()
        components = self._load_components()
        mappings = self._map_resources_to_components(resources, components)
        implementations = self._build_control_implementations(mappings)

        now = datetime.utcnow().isoformat() + "Z"
        return {
            "system-security-plan": {
                "uuid": self._uuid(),
                "metadata": {
                    "title": f"System Security Plan – {system_name}",
                    "published": now,
                    "last-modified": now,
                    "version": "1.0",
                    "oscal-version": "1.1.2",
                    "props": [
                        {"name": "organization", "value": "Swedish Enterprise"},
                        {"name": "system-name", "value": system_name}
                    ]
                },
                "import-profile": {"href": profile_href},
                "system-characteristics": {
                    "system-ids": [
                        {
                            "identifier-type": "https://ietf.org/rfc/rfc4122",
                            "id": self._account_id()
                        }
                    ],
                    "system-name": system_name,
                    "description": f"Automated SSP generated from Terraform for {system_name}",
                    "security-sensitivity-level": "moderate"
                },
                "control-implementation": {
                    "implemented-requirements": implementations
                }
            }
        }

    def _parse_terraform(self) -> List[Dict[str, Any]]:
        resources: List[Dict[str, Any]] = []
        for tf_file in self.terraform_directory.rglob("*.tf"):
            with tf_file.open("r", encoding="utf-8") as handle:
                data = hcl2.load(handle)
                resources.extend(data.get("resource", []))
        return resources

    def _load_components(self) -> List[ComponentDefinition]:
        components: List[ComponentDefinition] = []
        for path in self.component_paths:
            with path.open("r", encoding="utf-8") as handle:
                components.append(ComponentDefinition(path, json.load(handle)))
        return components

    def _map_resources_to_components(
        self,
        resources: List[Dict[str, Any]],
        components: List[ComponentDefinition],
    ) -> Dict[str, ComponentDefinition]:
        mappings: Dict[str, ComponentDefinition] = {}
        for resource in resources:
            resource_type = next(iter(resource.keys()))
            for component in components:
                if resource_type in json.dumps(component.content):
                    mappings[resource_type] = component
        return mappings

    def _build_control_implementations(
        self, mappings: Dict[str, ComponentDefinition]
    ) -> List[Dict[str, Any]]:
        implementations: List[Dict[str, Any]] = []
        for component in mappings.values():
            definition = component.content["component-definition"]
            for comp in definition.get("components", []):
                implementations.extend(
                    comp.get("control-implementations", [])
                )
        return implementations

    def _uuid(self) -> str:
        return datetime.utcnow().strftime("ssp-%Y%m%d%H%M%S")

    def _account_id(self) -> str:
        return self.sts.get_caller_identity()["Account"]


def load_component_paths(directory: Path) -> List[Path]:
    return sorted(directory.glob("*.json"))


def save_ssp(output_path: Path, ssp: Dict[str, Any]) -> None:
    output_path.write_text(json.dumps(ssp, indent=2), encoding="utf-8")


if __name__ == "__main__":
    tf_dir = Path("infrastructure")
    components_dir = Path("oscal/components")
    generator = OSCALSSPGenerator(tf_dir, load_component_paths(components_dir))
    plan = generator.generate(
        profile_href="profiles/swedish-financial-profile.json",
        system_name="Payments Platform"
    )
    save_ssp(Path("artifacts/system-security-plan.json"), plan)
```
