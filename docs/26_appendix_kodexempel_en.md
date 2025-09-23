# Appendix A: Kodexempel and technical Architecture as Code-implebuttationer

this Appendix innehåller all kodexempel, konfigurationsfiler and technical implebuttationar that refereras to in The book's huvudkapitel. Kodexemplen is organiserade after typ and användningthatråde for to göra det enkelt to hitta specific implebuttationer.

![Kodexempel Appendix](images/diagram_26_appendix.png)

*this Appendix fungerar that en praktisk referenssamling for all technical implebuttationer that demonstreras through boken. Varje kodexempel is kategoriserat and märkt with referenser tobaka to relevanta chapter.*

## Navigering in Appendix

Kodexemplen is organiserade in följande kategorier:

1. **[CI/CD Pipelines and Architecture as Code-automation](#cicd-pipelines)**
2. **[Infrastructure as Code (Architecture as Code) - Terraform](#terraform-IaC)**
3. **[Infrastructure as Code (Architecture as Code) - CloudFormation](#cloudformation-Architecture as Code)**
4. **[Automationsskript and tools](#automation-scripts)**
5. **[Säkerhet and compliance](#security-compliance)**
6. **[testing and validering](#testing-validation)**
7. **[Konfigurationsfiler](#configuration)**
8. **[Shell-skript and tools](#shell-scripts)**

Varje kodexempel have en unik identifierare in formatet `[chapter]_CODE_[NUMMER]` for enkel referens from huvudtexten.

---

## CI/CD Pipelines and Architecture as Code-automation {#cicd-pipelines}

this sektion innehåller all exempel on CI/CD-pipelines, GitHub Actions workflows and automationsprocesses for Swedish organizations.

### 05_CODE_1: GDPR-kompatibel CI/CD Pipeline for Swedish organizations
*Refereras from chapter 5: [automation and CI/CD-pipelines](05_automatisering_cicd.md)*

```yaml
# .github/workflows/Swedish-Architecture as Code-pipeline.yml
# GDPR-compliant CI/CD pipeline for Swedish organizations

name: Swedish Architecture as Code Pipeline with GDPR Compliance

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
 ENVIRONbutT: ${{ github.ref_name == 'main' && 'production' || github.ref_name }}
 COST_CENTER: ${{ vars.COST_CENTER }}
 GDPR_COMPLIANCE_ENABLED: 'true'
 DATA_RESIDENCY: 'Sweden'
 AUDIT_LOGGING: 'enabled'

jobs:
 # GDPR and säkerhetskontroller
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
 
 # Sök after vanliga personal data patterns in Architecture as Code-code
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
 echo "Personal data får not hardkodas in Architecture as Code-code"
 exit 1
 fi
 
 echo "✅ GDPR compliance check throughförd"
```

### 05_CODE_2: Jenkins Pipeline for Swedish organizations with GDPR compliance
*Refereras from chapter 5: [automation and CI/CD-pipelines](05_automatisering_cicd.md)*

```yaml
# Jenkins/Swedish-Architecture as Code-pipeline.groovy
// Jenkins pipeline for Swedish organizations with GDPR compliance

pipeline {
 agent any
 
 parameters {
 choice(
 name: 'ENVIRONbutT',
 choices: ['development', 'staging', 'production'],
 description: 'Target environbutt for deployment'
 )
 booleanParam(
 name: 'FORCE_DEPLOYbutT',
 defaultValue: false,
 description: 'Forcera deployment also at varningar (endast development)'
 )
 string(
 name: 'COST_CENTER',
 defaultValue: 'CC-IT-001',
 description: 'Kostnadscenter for Swedish bokföring'
 )
 }
 
 environbutt {
 ORGANIZATION_NAME = 'Swedish-org'
 AWS_DEFAULT_REGION = 'eu-north-1' // Stockholm region
 GDPR_COMPLIANCE = 'enabled'
 DATA_RESIDENCY = 'Sweden'
 TERRAFORM_VERSION = '1.6.0'
 COST_CURRENCY = 'SEK'
 AUDIT_RETENTION_YEARS = '7' // Swedish lagkrav
 }
 
 stages {
 stage('🇸🇪 Swedish Compliance Check') {
 parallel {
 stage('GDPR Data Scan') {
 steps {
 script {
 echo "🔍 Scanning for personal data patterns in Architecture as Code code..."
 
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
 error("GDPR VIOLATION: Personal data found in Architecture as Code code:\n${violations.join('\n')}")
 }
 
 echo "✅ GDPR data scan throughförd - inga violations"
 }
 }
 }
 
 stage('Data Residency Validation') {
 steps {
 script {
 echo "🏔️ Validerar Swedish data residency requirements..."
 
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
 
 echo "✅ Data residency requirebutts uppfyllda"
 }
 }
 }
 
 stage('Cost Center Validation') {
 steps {
 script {
 echo "💰 Validerar kostnadscenter for Swedish bokföring..."
 
 if (!params.COST_CENTER.matches(/CC-[A-Z]{2,}-\d{3}/)) {
 error("Ogiltigt kostnadscenter format. Använd: CC-XX-nnn")
 }
 
 // Validera to kostnadscenter existerar in companiesets system
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
 dir('infrastructure/environbutts/${params.ENVIRONbutT}') {
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
 
 if (params.ENVIRONbutT == 'production') {
 error("Kritiska säkerhetsproblem must åtgärdas före production deployment")
 }
 }
 
 echo "✅ Säkerhetsskanning slutförd"
 }
 }
 }
 
 stage('Swedish Policy Validation') {
 steps {
 script {
 echo "📋 Validerar Swedish organizationspolicies..."
 
 // Skapa Swedish OPA policies
 writeFile file: 'policies/Swedish-tagging.rego', text: """
 package Swedish.tagging
 
 required_tags := [
 "Environbutt", "CostCenter", "Organization", 
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
 
 echo "✅ Swedish policy validation slutförd"
 }
 }
 }
 }
 }
 
 stage('💰 Swedish Kostnadskontroll') {
 steps {
 script {
 echo "📊 Beräknar infrastrukturkostnader in Swedish kronor..."
 
 // Setup Infracost for Swedish valuta
 sh """
 curl -fsSL https://raw.githubusercontent.com/infracost/infracost/master/scripts/install.sh | sh
 export PATH=\$PATH:\$HOME/.local/bin
 
 cd infrastructure/environbutts/${params.ENVIRONbutT}
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
 
 // Validera kostnader mot Swedish budgetgränser
 def costData = readJSON file: 'cost-estimate.json'
 def monthlyCostSEK = costData.totalMonthlyCost as Double
 
 def budgetLimits = [
 'development': 5000,
 'staging': 15000,
 'production': 50000
 ]
 
 def maxBudget = budgetLimits[params.ENVIRONbutT] ?: 10000
 
 echo "Beräknad månadskostnad: ${monthlyCostSEK} SEK"
 echo "Budget for ${params.ENVIRONbutT}: ${maxBudget} SEK"
 
 if (monthlyCostSEK > maxBudget) {
 def overBudget = monthlyCostSEK - maxBudget
 echo "⚠️ BUDGET ÖVERSKRIDEN with ${overBudget} SEK!"
 
 if (params.ENVIRONbutT == 'production' && !params.FORCE_DEPLOYbutT) {
 error("Budget överskridning not toåten for production without CFO godkännande")
 }
 }
 
 // Generera svenskt kostnadsrapport
 def costReport = """
 # Kostnadsrapport - ${env.ORGANIZATION_NAME}
 
 **Miljö:** ${params.ENVIRONbutT}
 **Datum:** ${new Date().format('yyyy-MM-dd HH:mm')} (svensk tid)
 **Kostnadscenter:** ${params.COST_CENTER}
 
 ## Månadskostnad
 - **Total:** ${monthlyCostSEK} SEK
 - **Budget:** ${maxBudget} SEK
 - **Status:** ${monthlyCostSEK <= maxBudget ? '✅ within budget' : '❌ over budget'}
 
 ## Kostnadsnedbrytning
 ${readFile('cost-summary.txt')}
 
 ## Rekombutdationer
 - Använd Reserved Instances for production workloads
 - Aktivera auto-scaling for development miljöer
 - implement scheduled shutdown for icke-kritiska system
 """
 
 writeFile file: 'cost-report-Swedish.md', text: costReport
 archiveArtifacts artifacts: 'cost-report-Swedish.md', fingerprint: true
 
 echo "✅ Kostnadskontroll slutförd"
 }
 }
 }
 }
}
```

### 05_CODE_3: Terratest for Swedish VPC implebuttation
*Refereras from chapter 5: [automation and CI/CD-pipelines](05_automatisering_cicd.md)*

```go
// test/Swedish_vpc_test.go
// Terratest suite for Swedish VPC implebuttation with GDPR compliance

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

// SwedishVPCTestSuite definierar test suite for Swedish VPC implebuttation
type SwedishVPCTestSuite struct {
 TerraformOptions *terraform.Options
 AWSSession *session.Session
 OrganizationName string
 Environbutt string
 CostCenter string
}

// TestSwedishVPCGDPRCompliance testar GDPR compliance for VPC implebuttation
func TestSwedishVPCGDPRCompliance(t *testing.T) {
 t.Parallel()

 suite := setupSwedishVPCTest(t, "development")
 defer cleanupSwedishVPCTest(t, suite)

 // Deploy infrastructure
 terraform.InitAndApply(t, suite.TerraformOptions)

 // Test GDPR compliance requirebutts
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

 t.Run("TestSwedishTagging", func(t *testing.T) {
 testSwedishTagging(t, suite)
 })
}

// setupSwedishVPCTest förbereder test environbutt for Swedish VPC testing
func setupSwedishVPCTest(t *testing.T, environbutt string) *SwedishVPCTestSuite {
 // Unik test identifier
 uniqueID := strings.ToLower(fmt.Sprintf("test-%d", time.Now().Unix()))
 organizationName := fmt.Sprintf("Swedish-org-%s", uniqueID)

 // Terraform configuration
 terraformOptions := &terraform.Options{
 TerraformDir: "../infrastructure/modules/vpc",
 Vars: map[string]interface{}{
 "organization_name": organizationName,
 "environbutt": environbutt,
 "cost_center": "CC-TEST-001",
 "gdpr_compliance": true,
 "data_residency": "Sweden",
 "enable_flow_logs": true,
 "enable_encryption": true,
 "audit_logging": true,
 },
 BackendConfig: map[string]interface{}{
 "bucket": "Swedish-org-terraform-test-state",
 "key": fmt.Sprintf("test/%s/terraform.tfstate", uniqueID),
 "region": "eu-north-1",
 },
 RetryableTerraformErrors: map[string]string{
 ".*": "Transient error - retrying...",
 },
 MaxRetries: 3,
 TimeBetweenRetries: 5 * time.Second,
 }

 // AWS session for Stockholm region
 awsSession := session.Must(session.NewSession(&aws.Config{
 Region: aws.String("eu-north-1"),
 }))

 return &SwedishVPCTestSuite{
 TerraformOptions: terraformOptions,
 AWSSession: awsSession,
 OrganizationName: organizationName,
 Environbutt: environbutt,
 CostCenter: "CC-TEST-001",
 }
}

// testVPCFlowLogsEnabled validerar to VPC Flow Logs is aktiverade for GDPR compliance
func testVPCFlowLogsEnabled(t *testing.T, suite *SwedishVPCTestSuite) {
 // Hämta VPC ID from Terraform output
 vpcID := terraform.Output(t, suite.TerraformOptions, "vpc_id")
 require.NotEmpty(t, vpcID, "VPC ID should not be empty")

 // AWS EC2 client
 ec2Client := ec2.New(suite.AWSSession)

 // Kontrollera Flow Logs
 flowLogsInput := &ec2.DescribeFlowLogsInput{
 Filters: []*ec2.Filter{
 {
 Name: aws.String("resource-id"),
 Values: []*string{aws.String(vpcID)},
 },
 },
 }

 flowLogsOutput, err := ec2Client.DescribeFlowLogs(flowLogsInput)
 require.NoError(t, err, "Failed to describe VPC flow logs")

 // Validera to Flow Logs is aktiverade
 assert.Greater(t, len(flowLogsOutput.FlowLogs), 0, "VPC Flow Logs should be enabled for GDPR compliance")

 for _, flowLog := range flowLogsOutput.FlowLogs {
 assert.Equal(t, "Active", *flowLog.FlowLogStatus, "Flow log should be active")
 assert.Equal(t, "ALL", *flowLog.TrafficType, "Flow log should capture all traffic for compliance")
 }

 t.Logf("✅ VPC Flow Logs aktiverade for GDPR compliance: %s", vpcID)
}

// testEncryptionAtRest validerar to all lagring is krypterad according to GDPR-requirements
func testEncryptionAtRest(t *testing.T, suite *SwedishVPCTestSuite) {
 // Hämta KMS key from Terraform output
 kmsKeyArn := terraform.Output(t, suite.TerraformOptions, "kms_key_arn")
 require.NotEmpty(t, kmsKeyArn, "KMS key ARN should not be empty")

 // Validera to KMS key is from Sverige region
 assert.Contains(t, kmsKeyArn, "eu-north-1", "KMS key should be in Stockholm region for data residency")

 t.Logf("✅ Encryption at rest validerat for GDPR compliance")
}

// testDataResidencySweden validerar to all infrastructure is within Swedish gränser
func testDataResidencySweden(t *testing.T, suite *SwedishVPCTestSuite) {
 // Validera to VPC is in Stockholm region
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

 t.Logf("✅ Data residency validerat - all infrastructure in EU region: %s", region)
}

// testAuditLogging validerar to audit logging is konfigurerat according to Swedish lagkrav
func testAuditLogging(t *testing.T, suite *SwedishVPCTestSuite) {
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

// testSwedishTagging validerar to all resurser have korrekta Swedish tags
func testSwedishTagging(t *testing.T, suite *SwedishVPCTestSuite) {
 requiredTags := []string{
 "Environbutt", "Organization", "CostCenter", 
 "Country", "GDPRCompliant", "DataResidency",
 }

 expectedTagValues := map[string]string{
 "Environbutt": suite.Environbutt,
 "Organization": suite.OrganizationName,
 "CostCenter": suite.CostCenter,
 "Country": "Sweden",
 "GDPRCompliant": "true",
 "DataResidency": "Sweden",
 }

 // Test VPC tags
 vpcID := terraform.Output(t, suite.TerraformOptions, "vpc_id")
 ec2Client := ec2.New(suite.AWSSession)

 vpcTags, err := ec2Client.DescribeTags(&ec2.DescribeTagsInput{
 Filters: []*ec2.Filter{
 {
 Name: aws.String("resource-id"),
 Values: []*string{aws.String(vpcID)},
 },
 },
 })
 require.NoError(t, err, "Failed to describe VPC tags")

 // Konvertera tags to map for enklare validering
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

 t.Logf("✅ Swedish tagging validerat for all resurser")
}

// cleanupSwedishVPCTest rensar test environbutt
func cleanupSwedishVPCTest(t *testing.T, suite *SwedishVPCTestSuite) {
 terraform.Destroy(t, suite.TerraformOptions)
 t.Logf("✅ Test environbutt rensat for %s", suite.OrganizationName)
}
```

---

## Infrastructure as Code - CloudFormation {

Architecture as Code-principlesna within This område#cloudformation-Architecture as Code}

this sektion innehåller CloudFormation templates for AWS-infrastructure anpassad for Swedish organizations.

### 07_CODE_1: VPC Setup for Swedish organizations with GDPR compliance
*Refereras from chapter 7: [MolnArchitecture as Code](07_molnarkitektur.md)*

```yaml
# Cloudformation/Swedish-org-vpc.yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'VPC setup for Swedish organizations with GDPR compliance'

Parameters:
 EnvironbuttType:
 Type: String
 Default: development
 AllowedValues: [development, staging, production]
 Description: 'Miljötyp for deployment'
 
 DataClassification:
 Type: String
 Default: internal
 AllowedValues: [public, internal, confidential, restricted]
 Description: 'Dataklassificering according to Swedish säkerhetsstandarder'
 
 ComplianceRequirebutts:
 Type: CommaDelimitedList
 Default: "gdpr,iso27001"
 Description: 'Lista over compliance-requirements that must uppfyllas'

Conditions:
 IsProduction: !Equals [!Ref EnvironbuttType, production]
 RequiresGDPR: !Contains [!Ref ComplianceRequirebutts, gdpr]
 RequiresISO27001: !Contains [!Ref ComplianceRequirebutts, iso27001]

ReSources:
 VPC:
 Type: AWS::EC2::VPC
 Properties:
 CidrBlock: !If [IsProduction, '10.0.0.0/16', '10.1.0.0/16']
 EnableDnsHostnames: true
 EnableDnsSupport: true
 Tags:
 - Key: Name
 Value: !Sub '${AWS::StackName}-vpc'
 - Key: Environbutt
 Value: !Ref EnvironbuttType
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

this sektion innehåller Python-skript andra automationsverktyg for Infrastructure as Code-hantering.

### 22_CODE_1: comprehensive testramverk for Infrastructure as Code

Architecture as Code-principlesna within This område
*Refereras from chapter 22: [Architecture as Code best practices and lärda läxor](22_best_practices.md)*

```python
# Testing/comprehensive_iac_testing.py
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
 Based on Swedish Architecture as Code best practices and international standards
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
 """Verify all storage reSources use encryption at rest"""
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

this sektion innehåller konfigurationsfiler for olika tools and tjänster.

### 22_CODE_2: Governance policy configuration for Swedish organizations
*Refereras from chapter 22: [Best practices and lärda läxor](22_best_practices.md)*

```yaml
# Governance/Swedish-governance-policy.yaml
governance_framework:
 organization: "Swedish Organization AB"
 compliance_standards: ["GDPR", "ISO27001", "SOC2"]
 data_residency: "Sweden"
 regulatory_authority: "Integritetsskyddsmyndigheten (IMY)"

policy_enforcebutt:
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
 key_managebutt: "AWS KMS with customer managed keys"
 
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
 gdpr_requirebutts:
 data_mapping: "automated"
 consent_managebutt: "integrated"
 right_to_erasure: "implebutted"
 data_breach_notification: "automated"
 
 audit_requirebutts:
 frequency: "quarterly"
 scope: "all_infrastructure"
 external_auditor: "required_annually"
 evidence_collection: "automated"
```

---

## Referenser and navigering

Varje kodexempel in this Appendix can refereras from huvudtexten with dess unika identifierare. For to hitta specific implebuttationer:

1. **Använd sökfunktion** - Sök after kodtyp or teknologi (t.ex. "Terraform", "CloudFormation", "Python")
2. **Följ kategorierna** - Navigera to relevant sektion baserat on användningthatråde
3. **Använd korshänvisningar** - Följ länkar tobaka to huvudkapitlen for kontext

### Konventioner for kodexempel

- **Kombuttarer**: all kodexempel innehåller Swedish kombuttarer for klarhet
- **Säkerhet**: Säkerhetsaspekter is markerade with 🔒
- **GDPR-compliance**: GDPR-relaterade configurations is markerade with 🇪🇺
- **Swedish anpassningar**: Lokala anpassningar is markerade with 🇸🇪

### Uppdateringar and underhåll

this Appendix uppdateras löpande när nya kodexempel läggs to in The book's huvudkapitel. For senaste versionen of kodexempel, se The book's GitHub-repository.

---

*for mer information om specific implebuttationer, se respektive huvudkapitel where kodexemplen introduceras and förklaras in sitt sammanhang.*