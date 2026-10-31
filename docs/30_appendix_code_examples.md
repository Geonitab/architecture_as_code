\appendix

# Code examples and technical architecture as code implementations {#appendix-code-examples}

Appendix A collects the extended code listings, configuration files, and technical implementations that the chapters refer to by identifier. The examples are organised by theme so that readers can quickly locate the implementation that matches their current need.

*This appendix acts as a practical reference library for the book's extended technical demonstrations. Each code listing is
categorised and labelled with backlinks to the relevant chapter so the narrative and executable artefacts stay in sync.*

## Navigating the appendix

The code examples are grouped into the following categories:

1. **[CI/CD pipelines and Architecture as Code automation](#cicd-pipelines)**
2. **[Infrastructure as Code (Architecture as Code) – Terraform](#terraform-iac)**
3. **[Infrastructure as Code (Architecture as Code) – CloudFormation](#cloudformation-architecture-as-code)**
4. **[Automation scripts and tooling](#automation-scripts)**
5. **[Configuration files](#configuration)**
6. **[Testing strategies (Chapter 13)](#chapter-13-testing)**
7. **[Organisational change and team structures (Chapter 17)](#organisational-change)**
8. **[Architecture as Code in practice (Chapter 14)](#chapter-14-implementations)**
9. **[Cost optimisation and resource management (Chapter 15)](#chapter-15-implementations)**
10. **[Security and compliance (Chapter 10)](#security-compliance)**
11. **[Structurizr workspace examples (Chapter 6)](#structurizr-workspaces)**

Each example has a unique identifier in the format `[chapter]_CODE_[NUMBER]` for easy cross-reference with the main text.

## CI/CD Pipelines and Architecture as Code Automation {#cicd-pipelines}

This section contains all CI/CD pipeline examples, GitHub Actions workflows, and automation processes for organisations.

### 05_CODE_1: GDPR-compliant CI/CD pipeline for organisations {#05_code_1}
*Referenced from chapter 5: [Automation, DevOps and CI/CD for Infrastructure as Code](05_automation_devops_cicd.md)*

```yaml
# .github/workflows/architecture-as-code-pipeline.yml
# GDPR-compliant CI/CD pipeline for organisations

name: Architecture as Code Pipeline with GDPR Compliance

on:
  push:
    branches: [main, staging, development]
    paths:
      - 'infrastructure/**'
      - 'modules/**'
  pull_request:
    branches: [main, staging]
    paths:
      - 'infrastructure/**'
      - 'modules/**'

env:
  TF_VERSION: '1.17.1'
  ORGANISATION_NAME: ${{ vars.ORGANISATION_NAME }}
  ENVIRONMENT: ${{ github.ref_name == 'main' && 'production' || github.ref_name }}
  COST_CENTRE: ${{ vars.COST_CENTRE }}
  GDPR_COMPLIANCE_ENABLED: 'true'
  DATA_RESIDENCY: 'EU'
  AUDIT_LOGGING: 'enabled'

jobs:
  gdpr-compliance-check:
    name: GDPR Compliance Validation
    runs-on: ubuntu-latest
    # The scan runs on every push and pull request that touches infrastructure
    # paths. It is deliberately not gated on commit-message keywords:
    # github.event.head_commit only exists for push events, and keywords are
    # not a reliable compliance signal. Complement this pattern scan with
    # dedicated policy tools (Checkov, Trivy, Conftest) as required CI gates.

    steps:
      - name: Check out code
        uses: actions/checkout@v7
        with:
          fetch-depth: 0

      - name: GDPR data discovery scan
        run: |
          echo "# Search: Scanning for personal data indicators across EU jurisdictions..."

          PERSONAL_DATA_PATTERNS=(
            "national\\s+identity"
            "passport\\s+number"
            "social.*security"
            "tax\\s+identification"
            "vat\\s+number"
            "iban"
            "bic"
            "eori"
            "driver'?s\\s+licence"
            "health\\s+insurance\\s+number"
            "email.*address"
            "phone.*number"
            "date.*of.*birth"
          )

          VIOLATIONS_FOUND=false

          for pattern in "${PERSONAL_DATA_PATTERNS[@]}"; do
            if grep -R -i -E "$pattern" infrastructure/ modules/ 2>/dev/null; then
              echo "# WARNING: GDPR - Potential personal data reference detected for pattern: $pattern"
              VIOLATIONS_FOUND=true
            fi
          done

          if [ "$VIOLATIONS_FOUND" = true ]; then
            echo "# FAIL: GDPR compliance check failed"
            echo "Personal data must not be hard coded in Architecture as Code assets."
            exit 1
          fi

          echo "# Pass: GDPR compliance check completed successfully"
```

### 05_CODE_2: Jenkins pipeline for organisations with GDPR compliance {#05_code_2}
*Referenced from chapter 5: [Automation, DevOps and CI/CD for Infrastructure as Code](05_automation_devops_cicd.md)*

```groovy
// jenkins/architecture-as-code-pipeline.groovy
// Jenkins pipeline for organisations with GDPR compliance

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
            description: 'Force deployment even when warnings are raised (development only)'
        )
        string(
            name: 'COST_CENTER',
            defaultValue: 'CC-IT-001',
            description: 'Cost centre used for financial reporting'
        )
    }

    environment {
        ORGANISATION_NAME = 'example-org'
        AWS_DEFAULT_REGION = 'eu-west-1'
        GDPR_COMPLIANCE = 'enabled'
        DATA_RESIDENCY = 'EU'
        TERRAFORM_VERSION = '1.17.1'
        CONFTEST_VERSION = '0.64.0'
        COST_CURRENCY = 'EUR'
        AUDIT_RETENTION_YEARS = '7'  // e.g. seven years under national accounting legislation
    }

    stages {
        stage('Compliance Check') {
            parallel {
                stage('GDPR Data Scan') {
                    steps {
                        script {
                            echo "# Search: Scanning for personal data indicators across EU member states..."

                            def personalDataPatterns = [
                                'national\\s+identity', 'passport\\s+number', 'social.*security',
                                'tax\\s+identification', 'vat\\s+number', 'iban', 'bic',
                                'eori', "driver'?s\\s+licence", 'health\\s+insurance\\s+number',
                                'email.*address', 'phone.*number', 'date.*of.*birth'
                            ]

                            def violations = []

                            personalDataPatterns.each { pattern ->
                                def result = sh(
                                    script: "grep -R -i -E '${pattern}' infrastructure/ modules/ || true",
                                    returnStdout: true
                                ).trim()

                                if (result) {
                                    violations.add("Personal data pattern found for expression: ${pattern}")
                                }
                            }

                            if (violations) {
                                error("GDPR VIOLATION: Potential personal data detected in Architecture as Code assets:\n${violations.join('\n')}")
                            }

                            echo "# Pass: GDPR data scan completed successfully"
                        }
                    }
                }

                stage('Data Residency Validation') {
                    steps {
                        script {
                            echo "# Config: Validating data residency requirements..."

                            def allowedRegions = ['eu-west-1', 'eu-central-1', 'eu-west-2']

                            def regionCheck = sh(
                                script: """
                                    grep -R 'region\\s*=' infrastructure/ modules/ | \
                                    grep -v -E '(eu-west-1|eu-central-1|eu-west-2)' || true
                                """,
                                returnStdout: true
                            ).trim()

                            if (regionCheck) {
                                error("DATA RESIDENCY VIOLATION: Non-approved regions detected:\n${regionCheck}")
                            }

                            echo "# Pass: Data residency requirements satisfied"
                        }
                    }
                }

                stage('Cost Center Validation') {
                    steps {
                        script {
                            echo "# Billing: Validating cost centre for accounting..."

                            if (!params.COST_CENTER.matches(/CC-[A-Z]{2,}-\d{3}/)) {
                                error("Invalid cost centre format. Use: CC-XX-nnn")
                            }

                            // Validate the cost centre exists in the organisation's systems
                            def validCostCenters = [
                                'CC-IT-001', 'CC-DEV-002', 'CC-OPS-003', 'CC-SEC-004'
                            ]

                            if (!validCostCenters.contains(params.COST_CENTER)) {
                                error("Unknown cost centre: ${params.COST_CENTER}")
                            }

                            echo "# Pass: Cost centre validated: ${params.COST_CENTER}"
                        }
                    }
                }
            }
        }

        stage('Code Quality Analysis') {
            parallel {
                stage('Terraform Validation') {
                    steps {
                        script {
                            echo "🔧 Terraform syntax and formatting..."

                            // Format check
                            sh "terraform fmt -check -recursive infrastructure/"

                            // Syntax validation. Double quotes are required: Groovy only
                            // interpolates ${params.ENVIRONMENT} inside GStrings.
                            dir("infrastructure/environments/${params.ENVIRONMENT}") {
                                sh """
                                    terraform init -backend=false
                                    terraform validate
                                """
                            }

                            echo "# Pass: Terraform validation completed"
                        }
                    }
                }

                stage('Security Scanning') {
                    steps {
                        script {
                            echo "# Auth: Security scan with Checkov..."

                            // -o selects the report format and --output-file-path the output
                            // folder; Checkov writes the JSON report to <folder>/results_json.json
                            sh """
                                pip install checkov
                                checkov -d infrastructure/ \
                                    --framework terraform \
                                    -o json \
                                    --output-file-path checkov-results \
                                    --soft-fail
                            """

                            // Checkov only fills the "severity" field with metadata downloaded
                            // from the Prisma Cloud platform, so gate on explicit check IDs instead
                            def criticalChecks = [
                                'CKV_AWS_16',  // RDS storage encrypted at rest
                                'CKV_AWS_17',  // RDS instance not publicly accessible
                                'CKV_AWS_19',  // S3 bucket encrypted at rest
                                'CKV_AWS_24',  // No SSH ingress from 0.0.0.0/0
                                'CKV_AWS_25'   // No RDP ingress from 0.0.0.0/0
                            ]
                            def results = readJSON file: 'checkov-results/results_json.json'
                            def criticalIssues = results.results.failed_checks.findAll {
                                criticalChecks.contains(it.check_id)
                            }

                            if (criticalIssues.size() > 0) {
                                echo "# WARNING: Critical security issues found:"
                                criticalIssues.each { issue ->
                                    echo "- ${issue.check_id} ${issue.check_name}: ${issue.file_path}"
                                }

                                if (params.ENVIRONMENT == 'production') {
                                    error("Critical security issues must be resolved before production deployment")
                                }
                            }

                            echo "# Pass: Security scan completed"
                        }
                    }
                }

                stage('Policy Validation') {
                    steps {
                        script {
                            echo "📋 Validating organisational policies..."

                            // OPA 1.0 syntax (if/contains); import rego.v1 keeps the policy
                            // valid on OPA 0.59 and later as well
                            writeFile file: 'policies/a-tagging.rego', text: """
                                package a.tagging

                                import rego.v1

                                required_tags := [
                                    "Environment", "CostCenter", "Organization",
                                    "Country", "GDPRCompliant", "DataResidency"
                                ]

                                deny contains msg if {
                                    some resource_type, name
                                    resource := input.resource[resource_type][name]
                                    not resource.tags
                                    msg := sprintf("Resource %s.%s is missing tags", [resource_type, name])
                                }

                                deny contains msg if {
                                    some resource_type, name
                                    tags := input.resource[resource_type][name].tags
                                    some required_tag in required_tags
                                    not tags[required_tag]
                                    msg := sprintf("Resource %s.%s is missing required tag: %s", [resource_type, name, required_tag])
                                }
                            """

                            // "conftest test" evaluates policies against input files ("verify" only
                            // runs Rego unit tests). The namespace must match the package (the default
                            // is "main"), and a non-zero exit code fails the stage when a rule denies.
                            sh """
                                curl -L https://github.com/open-policy-agent/conftest/releases/download/v${env.CONFTEST_VERSION}/conftest_${env.CONFTEST_VERSION}_Linux_x86_64.tar.gz | tar xz
                                sudo mv conftest /usr/local/bin

                                conftest test --policy policies/ --namespace a.tagging --parser hcl2 infrastructure/
                            """

                            echo "# Pass: Policy validation completed"
                        }
                    }
                }
            }
        }

        stage('Cost Control') {
            steps {
                script {
                    echo "📊 Calculating infrastructure costs in euros..."

                    // The install script in infracost/infracost installs the 0.10.x CLI (the 2.x
                    // CLI lives in infracost/cli). "breakdown" has no --currency flag: the
                    // currency is stored once in the CLI configuration. INFRACOST_API_KEY must
                    // be supplied as a Jenkins credential.
                    sh """
                        curl -fsSL https://raw.githubusercontent.com/infracost/infracost/master/scripts/install.sh | sh
                        export PATH=\$PATH:\$HOME/.local/bin
                        infracost configure set currency ${env.COST_CURRENCY}

                        cd infrastructure/environments/${params.ENVIRONMENT}
                        terraform init -backend=false

                        infracost breakdown \\
                            --path . \\
                            --format json \\
                            --out-file ../../../cost-estimate.json

                        infracost output \\
                            --path ../../../cost-estimate.json \\
                            --format table \\
                            --out-file ../../../cost-summary.txt
                    """

                    // Validate costs against budget thresholds
                    def costData = readJSON file: 'cost-estimate.json'
                    def monthlyCostEUR = costData.totalMonthlyCost as Double

                    def budgetLimits = [
                        'development': 5000,
                        'staging': 15000,
                        'production': 50000
                    ]

                    def maxBudget = budgetLimits[params.ENVIRONMENT] ?: 10000

                    echo "Calculated monthly cost: ${monthlyCostEUR} EUR"
                    echo "Budget for ${params.ENVIRONMENT}: ${maxBudget} EUR"

                    if (monthlyCostEUR > maxBudget) {
                        def overBudget = monthlyCostEUR - maxBudget
                        echo "# WARNING: Budget exceeded by ${overBudget} EUR!"

                        if (params.ENVIRONMENT == 'production' && !params.FORCE_DEPLOYMENT) {
                            error("Budget overrun not permitted for production without CFO approval")
                        }
                    }

                    // Generate the cost report
                    def costReport = """
                    # Cost Report - ${env.ORGANISATION_NAME}

                    **Environment:** ${params.ENVIRONMENT}
                    **Date:** ${new Date().format('yyyy-MM-dd HH:mm')} (local time)
                    **Cost centre:** ${params.COST_CENTER}

                    ## Monthly cost
                    - **Total:** ${monthlyCostEUR} EUR
                    - **Budget:** ${maxBudget} EUR
                    - **Status:** ${monthlyCostEUR <= maxBudget ? '# Pass: Within budget' : '# FAIL: over budget'}

                    ## Cost breakdown
                    ${readFile('cost-summary.txt')}

                    ## Recommendations
                    - Use Reserved Instances for production workloads
                    - Enable auto-scaling for development environments
                    - Implement scheduled shutdowns for non-critical systems
                    """

                    writeFile file: 'cost-report-a.md', text: costReport
                    archiveArtifacts artifacts: 'cost-report-a.md', fingerprint: true

                    echo "# Pass: Cost control completed"
                }
            }
        }
    }
}
```

### 05_CODE_3: Terratest for VPC implementation {#05_code_3}
*Referenced from chapter 5: [Automation, DevOps and CI/CD for Infrastructure as Code](05_automation_devops_cicd.md)*

```go
// test/a_vpc_test.go
// Terratest suite for VPC implementation with GDPR compliance
//
// Expected outputs of the module under test: vpc_id, aws_region, kms_key_arn
// and flow_log_group_name. Uses AWS SDK for Go v2 (v1 reached end of support
// on 31 July 2025) through the clients that Terratest builds.

package test

import (
    "context"
    "fmt"
    "strings"
    "testing"
    "time"

    awssdk "github.com/aws/aws-sdk-go-v2/aws"
    "github.com/aws/aws-sdk-go-v2/service/cloudtrail"
    "github.com/aws/aws-sdk-go-v2/service/cloudwatchlogs"
    "github.com/aws/aws-sdk-go-v2/service/ec2"
    ec2types "github.com/aws/aws-sdk-go-v2/service/ec2/types"
    "github.com/aws/aws-sdk-go-v2/service/kms"
    kmstypes "github.com/aws/aws-sdk-go-v2/service/kms/types"
    "github.com/gruntwork-io/terratest/modules/aws"
    "github.com/gruntwork-io/terratest/modules/terraform"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
)

// allowedRegions lists the EU regions approved for personal data (GDPR Articles 44–49)
var allowedRegions = []string{"eu-west-1", "eu-central-1", "eu-west-2", "eu-north-1"}

// EuropeanVPCTestSuite defines the reusable Terratest suite for the VPC implementation
type EuropeanVPCTestSuite struct {
    TerraformOptions *terraform.Options
    Region           string
    OrganisationName string
    Environment      string
    CostCentre       string
}

// TestEuropeanVPCGDPRCompliance validates GDPR compliance expectations for the VPC implementation
func TestEuropeanVPCGDPRCompliance(t *testing.T) {
    t.Parallel()

    suite := setupEuropeanVPCTest(t, "development")
    defer cleanupEuropeanVPCTest(t, suite)

    // Deploy infrastructure
    terraform.InitAndApply(t, suite.TerraformOptions)

    // Test GDPR compliance requirements
    t.Run("TestVPCFlowLogsEnabled", func(t *testing.T) {
        testVPCFlowLogsEnabled(t, suite)
    })

    t.Run("TestEncryptionAtRest", func(t *testing.T) {
        testEncryptionAtRest(t, suite)
    })

    t.Run("TestDataResidencyEU", func(t *testing.T) {
        testDataResidencyEU(t, suite)
    })

    t.Run("TestAuditLogging", func(t *testing.T) {
        testAuditLogging(t, suite)
    })

    t.Run("TestEuropeanTagging", func(t *testing.T) {
        testEuropeanTagging(t, suite)
    })
}

// setupEuropeanVPCTest prepares the temporary test environment for VPC validation
func setupEuropeanVPCTest(t *testing.T, environment string) *EuropeanVPCTestSuite {
    // Unique test identifier
    uniqueID := strings.ToLower(fmt.Sprintf("test-%d", time.Now().Unix()))
    organisationName := fmt.Sprintf("a-org-%s", uniqueID)
    region := "eu-west-1"

    // Terraform configuration
    terraformOptions := &terraform.Options{
        TerraformDir: "../infrastructure/modules/vpc",
        Vars: map[string]interface{}{
            "organization_name": organisationName,
            "environment":       environment,
            "aws_region":        region,
            "cost_center":       "CC-TEST-001",
            "gdpr_compliance":   true,
            "data_residency":    "EU",
            "enable_flow_logs":  true,
            "enable_encryption": true,
            "audit_logging":     true,
        },
        BackendConfig: map[string]interface{}{
            "bucket": "a-org-terraform-test-state",
            "key":    fmt.Sprintf("test/%s/terraform.tfstate", uniqueID),
            "region": region,
        },
        RetryableTerraformErrors: map[string]string{
            ".*": "Transient error - retrying...",
        },
        MaxRetries:         3,
        TimeBetweenRetries: 5 * time.Second,
    }

    return &EuropeanVPCTestSuite{
        TerraformOptions: terraformOptions,
        Region:           region,
        OrganisationName: organisationName,
        Environment:      environment,
        CostCentre:       "CC-TEST-001",
    }
}

// testVPCFlowLogsEnabled validates that VPC Flow Logs are enabled for GDPR compliance
func testVPCFlowLogsEnabled(t *testing.T, suite *EuropeanVPCTestSuite) {
    // Fetch the VPC ID from Terraform output
    vpcID := terraform.Output(t, suite.TerraformOptions, "vpc_id")
    require.NotEmpty(t, vpcID, "VPC ID should not be empty")

    // AWS EC2 client (SDK v2) built by Terratest
    ec2Client := aws.NewEc2Client(t, suite.Region)

    // Check Flow Logs configuration; the input field is Filter, not Filters
    flowLogsOutput, err := ec2Client.DescribeFlowLogs(context.Background(), &ec2.DescribeFlowLogsInput{
        Filter: []ec2types.Filter{
            {
                Name:   awssdk.String("resource-id"),
                Values: []string{vpcID},
            },
        },
    })
    require.NoError(t, err, "Failed to describe VPC flow logs")

    // Validate that VPC Flow Logs are enabled
    require.NotEmpty(t, flowLogsOutput.FlowLogs, "VPC Flow Logs should be enabled for GDPR compliance")

    for _, flowLog := range flowLogsOutput.FlowLogs {
        assert.Equal(t, "ACTIVE", awssdk.ToString(flowLog.FlowLogStatus), "Flow log should be active")
        assert.Equal(t, ec2types.TrafficTypeAll, flowLog.TrafficType, "Flow log should capture all traffic for compliance")
    }

    t.Logf("# Pass: VPC Flow Logs enabled for GDPR compliance: %s", vpcID)
}

// testEncryptionAtRest validates that the audit data written by the module is encrypted with a customer managed key
func testEncryptionAtRest(t *testing.T, suite *EuropeanVPCTestSuite) {
    // Get KMS key from Terraform output
    kmsKeyArn := terraform.Output(t, suite.TerraformOptions, "kms_key_arn")
    require.NotEmpty(t, kmsKeyArn, "KMS key ARN should not be empty")

    // The key must be an enabled customer managed key in the EU region
    kmsClient := aws.NewKmsClient(t, suite.Region)
    keyOutput, err := kmsClient.DescribeKey(context.Background(), &kms.DescribeKeyInput{
        KeyId: awssdk.String(kmsKeyArn),
    })
    require.NoError(t, err, "Failed to describe KMS key")
    assert.True(t, keyOutput.KeyMetadata.Enabled, "KMS key must be enabled")
    assert.Equal(t, kmstypes.KeyManagerTypeCustomer, keyOutput.KeyMetadata.KeyManager, "Encryption must use a customer managed key")
    assert.Contains(t, kmsKeyArn, suite.Region, "KMS key should be in the EU region used for data residency")

    // The flow-log destination (CloudWatch Logs) must be encrypted with that key
    logGroupName := terraform.Output(t, suite.TerraformOptions, "flow_log_group_name")
    logsClient := aws.NewCloudWatchLogsClient(t, suite.Region)
    groups, err := logsClient.DescribeLogGroups(context.Background(), &cloudwatchlogs.DescribeLogGroupsInput{
        LogGroupNamePrefix: awssdk.String(logGroupName),
    })
    require.NoError(t, err, "Failed to describe the flow log group")
    require.NotEmpty(t, groups.LogGroups, "Flow log group should exist")
    assert.Equal(t, kmsKeyArn, awssdk.ToString(groups.LogGroups[0].KmsKeyId), "Flow logs must be encrypted with the customer managed key")

    t.Logf("# Pass: Encryption at rest validated for GDPR compliance")
}

// testDataResidencyEU validates that the VPC was created in an approved EU region
func testDataResidencyEU(t *testing.T, suite *EuropeanVPCTestSuite) {
    // The module reports the region it deployed into; it must be on the EU allow list
    region := terraform.Output(t, suite.TerraformOptions, "aws_region")
    assert.Contains(t, allowedRegions, region, "VPC must be in an approved EU region for data residency")

    // VPC IDs are regional: a successful lookup in that region proves where the VPC lives
    vpcID := terraform.Output(t, suite.TerraformOptions, "vpc_id")
    vpc := aws.GetVpcById(t, vpcID, region)
    require.Equal(t, vpcID, vpc.Id, "VPC should be resolvable in the approved region")

    t.Logf("# Pass: Data residency validated - VPC %s is in EU region %s", vpcID, region)
}

// testAuditLogging validates that audit logging is configured according to legal requirements
func testAuditLogging(t *testing.T, suite *EuropeanVPCTestSuite) {
    // Check the CloudTrail configuration matches organisational expectations
    cfg, err := aws.NewAuthenticatedSession(suite.Region)
    require.NoError(t, err, "Failed to create AWS configuration")
    cloudtrailClient := cloudtrail.NewFromConfig(*cfg)

    trails, err := cloudtrailClient.DescribeTrails(context.Background(), &cloudtrail.DescribeTrailsInput{})
    require.NoError(t, err, "Failed to list CloudTrail trails")

    foundOrgTrail := false
    for _, trail := range trails.TrailList {
        if strings.Contains(awssdk.ToString(trail.Name), suite.OrganisationName) {
            foundOrgTrail = true
            t.Logf("# Pass: CloudTrail audit logging configured: %s", awssdk.ToString(trail.Name))
        }
    }

    assert.True(t, foundOrgTrail, "Organisation CloudTrail should exist for audit logging")
}

// testEuropeanTagging confirms that all resources expose the expected governance tags
func testEuropeanTagging(t *testing.T, suite *EuropeanVPCTestSuite) {
    requiredTags := []string{
        "Environment", "Organization", "CostCenter",
        "Country", "GDPRCompliant", "DataResidency",
    }

    expectedTagValues := map[string]string{
        "Environment":   suite.Environment,
        "Organization":  suite.OrganisationName,
        "CostCenter":    suite.CostCentre,
        "Country":       "EU",
        "GDPRCompliant": "true",
        "DataResidency": "EU",
    }

    // Terratest returns the VPC tags as a map (signature: t, vpcID, region)
    vpcID := terraform.Output(t, suite.TerraformOptions, "vpc_id")
    vpcTagMap := aws.GetTagsForVpc(t, vpcID, suite.Region)

    // Validate mandatory governance tags
    for _, requiredTag := range requiredTags {
        assert.Contains(t, vpcTagMap, requiredTag, "VPC should have required tag: %s", requiredTag)

        if expectedValue, exists := expectedTagValues[requiredTag]; exists {
            assert.Equal(t, expectedValue, vpcTagMap[requiredTag],
                "Tag %s should have correct value", requiredTag)
        }
    }

    t.Logf("# Pass: Tagging validated for all resources")
}

// cleanupEuropeanVPCTest removes the Terraform deployment after the tests complete
func cleanupEuropeanVPCTest(t *testing.T, suite *EuropeanVPCTestSuite) {
    terraform.Destroy(t, suite.TerraformOptions)
    t.Logf("# Pass: Test environment removed for %s", suite.OrganisationName)
}
```

---

## Infrastructure as Code (Architecture as Code) – Terraform {#terraform-iac}

Terraform underpins many Architecture as Code transformations by codifying consistent guardrails, data residency requirements, and provider-specific integrations across estates.

### 21_CODE_1: Multi-cloud enterprise landing zone {#21_code_1}
*Referenced from Chapter 21: [Digitalisation through Code-based Infrastructure](21_digitalisation.md)*

```hcl
# terraform/main.tf - Multi-cloud setup for global enterprise
terraform {
  required_version = ">= 1.11"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 5.0"
    }
  }
}

variable "aws_eu_region" {
  description = "AWS region for EU data residency (e.g. eu-west-1, eu-central-1, eu-north-1)"
  type        = string
  default     = "eu-west-1"
}

variable "azure_eu_region" {
  description = "Azure region for EU data residency (e.g. westeurope, northeurope, swedencentral)"
  type        = string
  default     = "westeurope"
}

variable "environment" {
  description = "Deployment environment (development, staging, production)"
  type        = string
}

variable "project_name" {
  description = "Project identifier used for naming and cost allocation"
  type        = string
}

variable "cost_centre" {
  description = "Cost centre code used by finance"
  type        = string
}

variable "data_classification" {
  description = "Highest data classification processed by the landing zone"
  type        = string
  default     = "confidential"
}

# AWS for global services with EU data residency
provider "aws" {
  region = var.aws_eu_region
}

# Azure for Microsoft integrations with EU compliance. The azurerm provider has
# no location argument: the region is set per resource, so it is passed to the
# Azure module below. subscription_id is read from ARM_SUBSCRIPTION_ID in CI.
provider "azurerm" {
  features {}
}

# Common resource tagging for cost management and EU compliance
locals {
  common_tags = {
    Organisation = "Global Enterprise Ltd"
    Environment  = var.environment
    Project      = var.project_name
    CostCentre   = var.cost_centre
    DataClass    = var.data_classification
    EUCompliance = "GDPR"
    Regulator    = "EDPB"
  }
}

module "aws_infrastructure" {
  source = "./modules/aws"
  region = var.aws_eu_region
  tags   = local.common_tags
}

module "azure_infrastructure" {
  source   = "./modules/azure"
  location = var.azure_eu_region
  tags     = local.common_tags
}

# Optional: add EU-native providers (e.g., OVHcloud, Scaleway) via additional modules
```

---

## Infrastructure as Code – CloudFormation {#cloudformation-architecture-as-code}

Architecture as Code principles in this area emphasise resilient AWS foundations and strong governance.

This section contains CloudFormation templates for AWS infrastructure adapted for organisations.

### 07_CODE_1: VPC Setup for organisations with GDPR compliance {#07_code_1}
*Referenced from Chapter 7: [Containerisation and Orchestration as Code](07_containerisation.md)*

```yaml
# cloudformation/a-org-vpc.yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'VPC setup for organisations with GDPR compliance'

Parameters:
  EnvironmentType:
    Type: String
    Default: development
    AllowedValues: [development, staging, production]
    Description: 'Environment type for deployment'

  DataClassification:
    Type: String
    Default: internal
    AllowedValues: [public, internal, confidential, restricted]
    Description: 'Data classification according to security standards'

  # Fn::Contains is only available in the Rules section, so each compliance
  # requirement is modelled as its own true/false parameter
  RequireGDPR:
    Type: String
    Default: 'true'
    AllowedValues: ['true', 'false']
    Description: 'Whether GDPR controls must be applied to the stack'

  RequireISO27001:
    Type: String
    Default: 'true'
    AllowedValues: ['true', 'false']
    Description: 'Whether ISO/IEC 27001 controls must be applied to the stack'

Conditions:
  IsProduction: !Equals [!Ref EnvironmentType, production]
  RequiresGDPR: !Equals [!Ref RequireGDPR, 'true']
  RequiresISO27001: !Equals [!Ref RequireISO27001, 'true']

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
          Value: 'EU'
        - Key: Region
          Value: 'eu-west-1'
```

---

## Automation Scripts {#automation-scripts}

This section contains Python scripts and other automation tooling for Architecture as Code operations.

### 24_CODE_1: Comprehensive test framework for Architecture as Code {#24_code_1}

Architecture as Code principles within this area emphasise automated validation and transparent feedback.
*Referenced from chapter 24: [Best Practices and Lessons Learned](24_best_practices.md)*

```python
# testing/comprehensive_iac_testing.py
import json
from dataclasses import dataclass
from typing import Any, Callable, List

import boto3
from botocore.exceptions import ClientError


@dataclass
class CheckResult:
    """Outcome of one infrastructure check.

    Named CheckResult rather than TestCase so that pytest does not try to
    collect the dataclass as a test class.
    """
    name: str
    description: str
    test_type: str
    severity: str
    expected_result: Any
    actual_result: Any = None
    status: str = "pending"


class ComprehensiveIaCTesting:
    """
    Comprehensive testing framework for Infrastructure as Code.
    Based on Architecture as Code best practices and international standards.
    """

    def __init__(self, region='eu-west-1'):
        self.region = region
        self.ec2 = boto3.client('ec2', region_name=region)
        self.rds = boto3.client('rds', region_name=region)
        self.s3 = boto3.client('s3', region_name=region)
        self.iam = boto3.client('iam', region_name=region)
        self.elbv2 = boto3.client('elbv2', region_name=region)

    def test_infrastructure_security(self, vpc_id: str) -> List[CheckResult]:
        """Run the security checks and return one result per check."""
        return [
            self._test_encryption_at_rest(),
            self._test_encryption_in_transit(),
            self._test_vpc_flow_logs(vpc_id),
            self._test_security_groups(vpc_id),
            self._test_iam_policies(),
            self._test_s3_bucket_policies(),
            self._test_rds_security(),
        ]

    @staticmethod
    def _run(check: CheckResult, findings_fn: Callable[[], List[str]]) -> CheckResult:
        """Execute a check; a non-empty findings list means the check failed."""
        try:
            findings = findings_fn()
            if findings:
                check.status = "failed"
                check.actual_result = findings
            else:
                check.status = "passed"
                check.actual_result = check.expected_result
        except ClientError as error:
            check.status = "error"
            check.actual_result = f"AWS API error: {error}"
        return check

    def _test_encryption_at_rest(self) -> CheckResult:
        """Verify all S3 buckets default to KMS encryption with customer managed keys."""
        def findings() -> List[str]:
            weak = []
            for bucket in self.s3.list_buckets()['Buckets']:
                try:
                    config = self.s3.get_bucket_encryption(Bucket=bucket['Name'])
                except ClientError as error:
                    if error.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
                        weak.append(f"{bucket['Name']}: no default encryption")
                        continue
                    raise
                for rule in config['ServerSideEncryptionConfiguration']['Rules']:
                    if rule['ApplyServerSideEncryptionByDefault']['SSEAlgorithm'] != 'aws:kms':
                        weak.append(f"{bucket['Name']}: not using KMS")
            return weak

        return self._run(CheckResult(
            name="Encryption at Rest Validation",
            description="Verify all S3 buckets use KMS default encryption",
            test_type="security",
            severity="high",
            expected_result="All S3 buckets encrypted with KMS",
        ), findings)

    def _test_encryption_in_transit(self) -> CheckResult:
        """Verify load balancer listeners only accept TLS or redirect to it."""
        def findings() -> List[str]:
            insecure = []
            for lb in self.elbv2.describe_load_balancers()['LoadBalancers']:
                listeners = self.elbv2.describe_listeners(LoadBalancerArn=lb['LoadBalancerArn'])['Listeners']
                for listener in listeners:
                    redirects = any(action['Type'] == 'redirect' for action in listener['DefaultActions'])
                    if listener['Protocol'] == 'HTTP' and not redirects:
                        insecure.append(f"{lb['LoadBalancerName']}: plain HTTP on port {listener['Port']}")
            return insecure

        return self._run(CheckResult(
            name="Encryption in Transit Validation",
            description="Verify load balancers terminate TLS",
            test_type="security",
            severity="high",
            expected_result="All listeners use TLS",
        ), findings)

    def _test_vpc_flow_logs(self, vpc_id: str) -> CheckResult:
        """Verify an active flow log captures all traffic for the VPC."""
        def findings() -> List[str]:
            logs = self.ec2.describe_flow_logs(
                Filters=[{'Name': 'resource-id', 'Values': [vpc_id]}]
            )['FlowLogs']
            active = [log for log in logs if log['FlowLogStatus'] == 'ACTIVE' and log['TrafficType'] == 'ALL']
            return [] if active else [f"{vpc_id}: no active flow log capturing ALL traffic"]

        return self._run(CheckResult(
            name="VPC Flow Logs Validation",
            description="Verify VPC flow logs are active",
            test_type="security",
            severity="medium",
            expected_result="Flow logs active for all traffic",
        ), findings)

    def _test_security_groups(self, vpc_id: str) -> CheckResult:
        """Verify no security group exposes administrative ports to the internet."""
        def findings() -> List[str]:
            exposed = []
            groups = self.ec2.describe_security_groups(
                Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}]
            )['SecurityGroups']
            for group in groups:
                for permission in group['IpPermissions']:
                    open_to_world = any(r.get('CidrIp') == '0.0.0.0/0' for r in permission.get('IpRanges', []))
                    if open_to_world and permission.get('FromPort') in (22, 3389):
                        exposed.append(f"{group['GroupId']}: port {permission['FromPort']} open to 0.0.0.0/0")
            return exposed

        return self._run(CheckResult(
            name="Security Group Validation",
            description="Verify SSH and RDP are not open to the internet",
            test_type="security",
            severity="critical",
            expected_result="No administrative ports exposed",
        ), findings)

    def _test_iam_policies(self) -> CheckResult:
        """Verify no customer managed IAM policy grants Action * on Resource *."""
        def findings() -> List[str]:
            wildcard = []
            for policy in self.iam.list_policies(Scope='Local')['Policies']:
                version = self.iam.get_policy_version(
                    PolicyArn=policy['Arn'], VersionId=policy['DefaultVersionId']
                )
                statements = version['PolicyVersion']['Document']['Statement']
                if isinstance(statements, dict):
                    statements = [statements]
                for statement in statements:
                    if (statement.get('Effect') == 'Allow'
                            and statement.get('Action') == '*'
                            and statement.get('Resource') == '*'):
                        wildcard.append(f"{policy['PolicyName']}: allows * on *")
            return wildcard

        return self._run(CheckResult(
            name="IAM Policy Validation",
            description="Verify least-privilege IAM policies",
            test_type="security",
            severity="high",
            expected_result="No wildcard administrator policies",
        ), findings)

    def _test_s3_bucket_policies(self) -> CheckResult:
        """Verify every bucket policy denies requests that do not use TLS."""
        def findings() -> List[str]:
            missing = []
            for bucket in self.s3.list_buckets()['Buckets']:
                try:
                    document = json.loads(self.s3.get_bucket_policy(Bucket=bucket['Name'])['Policy'])
                except ClientError as error:
                    if error.response['Error']['Code'] == 'NoSuchBucketPolicy':
                        missing.append(f"{bucket['Name']}: no bucket policy")
                        continue
                    raise
                statements = document['Statement']
                if isinstance(statements, dict):
                    statements = [statements]
                enforces_tls = any(
                    statement.get('Effect') == 'Deny'
                    and str(statement.get('Condition', {}).get('Bool', {}).get('aws:SecureTransport', '')).lower() == 'false'
                    for statement in statements
                )
                if not enforces_tls:
                    missing.append(f"{bucket['Name']}: policy does not deny non-TLS access")
            return missing

        return self._run(CheckResult(
            name="S3 Bucket Policy Validation",
            description="Verify bucket policies enforce TLS",
            test_type="security",
            severity="medium",
            expected_result="All buckets deny non-TLS requests",
        ), findings)

    def _test_rds_security(self) -> CheckResult:
        """Verify RDS instances are encrypted, private and backed up."""
        def findings() -> List[str]:
            issues = []
            for db in self.rds.describe_db_instances()['DBInstances']:
                identifier = db['DBInstanceIdentifier']
                if not db.get('StorageEncrypted'):
                    issues.append(f"{identifier}: storage not encrypted")
                if db.get('PubliclyAccessible'):
                    issues.append(f"{identifier}: publicly accessible")
                if db.get('BackupRetentionPeriod', 0) < 7:
                    issues.append(f"{identifier}: backup retention below 7 days")
            return issues

        return self._run(CheckResult(
            name="RDS Security Validation",
            description="Verify RDS encryption, network exposure and backups",
            test_type="security",
            severity="high",
            expected_result="All RDS instances encrypted, private and backed up",
        ), findings)
```

---

## Configuration Files {#configuration}

This section contains configuration files for different tools and services.

### 24_CODE_2: Governance policy configuration for organisations {#24_code_2}
*Referenced from chapter 24: [Best Practices and Lessons Learned](24_best_practices.md)*

```yaml
# governance/a-governance-policy.yaml
governance_framework:
  organization: "Organization AB"
  compliance_standards: ["GDPR", "ISO27001", "SOC2"]
  data_residency: "EU"
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
      monthly_limit: "10000 EUR"
      alert_threshold: "80%"
      auto_shutdown: "enabled"
    
    staging:
      monthly_limit: "25000 EUR"
      alert_threshold: "85%"
      auto_shutdown: "disabled"
    
    production:
      monthly_limit: "100000 EUR"
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
      // (Vitest 1.0 and later nest the limits under "thresholds")
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 80,
        statements: 80,
      },
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
    region: string = 'eu-west-1'
  ): TerraformConfig {
    // Validate EU regions for GDPR compliance
    const euRegions = ['eu-west-1', 'eu-central-1', 'eu-west-2'];
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
    encrypted: boolean = true,
    // Major version only: RDS selects a supported minor release. Check the
    // RDS PostgreSQL release calendar before pinning a specific version.
    engineVersion: string = '16'
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
        engine_version: engineVersion,
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

Comprehensive Vitest suite validating the Terraform configuration generator with GDPR compliance checks and regional restrictions.

```typescript
// src/generators/terraform-config.test.ts
import { describe, expect, it } from 'vitest';
import { TerraformConfigGenerator } from './terraform-config';

describe('TerraformConfigGenerator', () => {
  const generator = new TerraformConfigGenerator();

  it('creates a GDPR-compliant VPC for production in the EU', () => {
    const config = generator.generateVPCConfig('production', 'eu-west-2');

    expect(config.region).toBe('eu-west-2');
    expect(config.resources[0].properties.tags.GdprCompliant).toBe('true');
    expect(config.resources[0].properties.tags.DataResidency).toBe('EU');
  });

  it('refuses to generate VPCs outside approved EU regions', () => {
    expect(() => generator.generateVPCConfig('production', 'us-east-1')).toThrowError(
      'Region must be within EU for GDPR compliance'
    );
  });

  it('enforces encryption for production databases', () => {
    expect(() => generator.generateRDSConfig('production', 'db.r6g.large', false)).toThrowError(
      'Production databases must have encryption enabled'
    );

    const resource = generator.generateRDSConfig('production', 'db.r6g.large', true);
    expect(resource.properties.storage_encrypted).toBe(true);
    expect(resource.properties.multi_az).toBe(true);
    expect(resource.properties.tags.EncryptionEnabled).toBe('true');
  });

  it('creates leaner development databases whilst retaining encryption', () => {
    const resource = generator.generateRDSConfig('development');

    expect(resource.properties.allocated_storage).toBe(20);
    expect(resource.properties.multi_az).toBe(false);
    expect(resource.properties.storage_encrypted).toBe(true);
  });
});
```

### 13_CODE_D: Infrastructure Validator {#13_code_d}
*Listing 13-D.*
*Referenced from Chapter 13: [Testing Strategies](13_testing_strategies.md)*

Infrastructure validation module that checks resources against organisational policies and compliance requirements.

```typescript
// src/validators/infrastructure-validator.ts
export interface ResourceTag {
  key: string;
  value: string;
}

export interface SecurityRule {
  protocol: 'tcp' | 'udp' | 'icmp';
  port: number;
  cidr: string;
}

export interface ClassifiedResource {
  id: string;
  classification: 'public' | 'internal' | 'confidential';
  encrypted: boolean;
}

export interface ResourceDefinition {
  id: string;
  type: string;
  tags: ResourceTag[];
  securityRules?: SecurityRule[];
  data?: ClassifiedResource;
}

export interface ValidationResult {
  id: string;
  errors: string[];
  warnings: string[];
}

export class InfrastructureValidator {
  constructor(private readonly mandatoryTags: string[]) {}

  validate(resources: ResourceDefinition[]): ValidationResult[] {
    return resources.map((resource) => ({
      id: resource.id,
      errors: [
        ...this.validateMandatoryTags(resource),
        ...this.validateSecurityRules(resource),
        ...this.validateDataClassification(resource),
      ],
      warnings: this.collectWarnings(resource),
    }));
  }

  private validateMandatoryTags(resource: ResourceDefinition): string[] {
    const presentKeys = resource.tags.map((tag) => tag.key);
    return this.mandatoryTags
      .filter((tag) => !presentKeys.includes(tag))
      .map((tag) => `Missing mandatory tag: ${tag}`);
  }

  private validateSecurityRules(resource: ResourceDefinition): string[] {
    if (!resource.securityRules?.length) {
      return [];
    }

    return resource.securityRules
      .filter((rule) => rule.protocol === 'tcp' && rule.port === 22 && rule.cidr === '0.0.0.0/0')
      .map(() => 'SSH must not be open to the internet');
  }

  private validateDataClassification(resource: ResourceDefinition): string[] {
    if (!resource.data) {
      return [];
    }

    if (resource.data.classification === 'confidential' && !resource.data.encrypted) {
      return ['Confidential resources must be encrypted'];
    }

    return [];
  }

  private collectWarnings(resource: ResourceDefinition): string[] {
    if (!resource.securityRules?.length) {
      return ['No security rules defined; ensure defence-in-depth controls exist'];
    }

    const usesWildcard = resource.securityRules.some((rule) => rule.cidr === '0.0.0.0/0');
    return usesWildcard ? ['Wildcard CIDR detected; confirm zero-trust posture'] : [];
  }
}
```

### 13_CODE_E: Infrastructure Validator Tests {#13_code_e}
*Listing 13-E.*
*Referenced from Chapter 13: [Testing Strategies](13_testing_strategies.md)*

Comprehensive Vitest suite covering mandatory tags, security groups and compliance policies.

```typescript
// src/validators/infrastructure-validator.test.ts
import { describe, expect, it } from 'vitest';
import { InfrastructureValidator } from './infrastructure-validator';

const validator = new InfrastructureValidator(['Environment', 'CostCentre', 'Owner']);

describe('InfrastructureValidator', () => {
  it('flags resources missing mandatory tags', () => {
    const [result] = validator.validate([
      {
        id: 'vpc-001',
        type: 'aws_vpc',
        tags: [
          { key: 'Environment', value: 'production' },
          { key: 'Owner', value: 'platform-team' },
        ],
      },
    ]);

    expect(result.errors).toContain('Missing mandatory tag: CostCentre');
  });

  it('detects internet-facing SSH rules', () => {
    const [result] = validator.validate([
      {
        id: 'sg-123',
        type: 'aws_security_group',
        tags: [
          { key: 'Environment', value: 'staging' },
          { key: 'CostCentre', value: 'IT-042' },
          { key: 'Owner', value: 'security-team' },
        ],
        securityRules: [
          { protocol: 'tcp', port: 22, cidr: '0.0.0.0/0' },
        ],
      },
    ]);

    expect(result.errors).toContain('SSH must not be open to the internet');
    expect(result.warnings).toContain('Wildcard CIDR detected; confirm zero-trust posture');
  });

  it('enforces encryption for confidential data sets', () => {
    const [result] = validator.validate([
      {
        id: 's3-logs',
        type: 'aws_s3_bucket',
        tags: [
          { key: 'Environment', value: 'production' },
          { key: 'CostCentre', value: 'FIN-001' },
          { key: 'Owner', value: 'risk-office' },
        ],
        data: {
          id: 'audit-logs',
          classification: 'confidential',
          encrypted: false,
        },
      },
    ]);

    expect(result.errors).toContain('Confidential resources must be encrypted');
  });

  it('passes compliant resources without errors', () => {
    const [result] = validator.validate([
      {
        id: 'db-analytics',
        type: 'aws_db_instance',
        tags: [
          { key: 'Environment', value: 'production' },
          { key: 'CostCentre', value: 'DATA-007' },
          { key: 'Owner', value: 'data-platform' },
        ],
        securityRules: [
          { protocol: 'tcp', port: 5432, cidr: '10.0.0.0/16' },
        ],
        data: {
          id: 'analytics',
          classification: 'internal',
          encrypted: true,
        },
      },
    ]);

    expect(result.errors).toHaveLength(0);
    expect(result.warnings).toHaveLength(0);
  });
});
```

### 13_CODE_F: GitHub Actions Vitest Workflow {#13_code_f}
*Listing 13-F.*
*Referenced from Chapter 13: [Testing Strategies](13_testing_strategies.md)*

CI/CD workflow demonstrating automated infrastructure code testing with coverage reporting.

```yaml
# .github/workflows/infrastructure-vitest.yml
name: Infrastructure Code Tests

on:
  pull_request:
    paths:
      - 'src/**'
      - 'package.json'
      - 'pnpm-lock.yaml'
      - 'vitest.config.ts'

permissions:
  contents: read
  checks: write   # required by dorny/test-reporter to publish the check run

jobs:
  vitest:
    runs-on: ubuntu-latest

    steps:
      - name: Check out repository
        uses: actions/checkout@v7

      # pnpm must exist before setup-node runs "pnpm store path" for the cache
      - name: Install pnpm
        uses: pnpm/action-setup@v6
        with:
          version: 10

      - name: Use Node.js 22
        uses: actions/setup-node@v7
        with:
          node-version: 22
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      # The junit reporter produces the test results that the reporter step reads;
      # coverage/ only contains Istanbul coverage data
      - name: Run Vitest with coverage and JUnit output
        run: pnpm vitest run --coverage --reporter=default --reporter=junit --outputFile=reports/junit.xml

      - name: Upload coverage report
        if: always()
        uses: actions/upload-artifact@v7
        with:
          name: vitest-coverage
          path: coverage/

      - name: Summarise test results
        if: always()
        uses: dorny/test-reporter@v3
        with:
          name: Vitest
          path: reports/junit.xml
          reporter: java-junit
```

### 13_CODE_G: Requirements as Code Definition {#13_code_g}
*Listing 13-G.*
*Referenced from Chapter 13: [Testing Strategies](13_testing_strategies.md)*

YAML-based requirements definition enabling traceability from business requirements to automated tests with compliance mapping and test specifications.

```yaml
# requirements/catalogue.yaml
metadata:
  version: 1
  generated: 2024-04-15
  owner: platform-risk-office

requirements:
  - id: SEC-001
    title: Encrypt customer data at rest
    priority: high
    classification: gdpr
    rationale: Protect personally identifiable information across EU jurisdictions.
    tests:
      - id: test-encryption-s3
        description: Validate that S3 buckets containing GDPR data enable default encryption.
        tooling: opa
      - id: test-encryption-rds
        description: Confirm RDS instances with GDPR tags have storage encryption enabled.
        tooling: terratest

  - id: PERF-003
    title: Maintain API latency under 250ms at p95
    priority: medium
    classification: service-level
    rationale: Preserve customer experience during peak trading windows.
    tests:
      - id: test-load-run
        description: Execute k6 load test to validate latency thresholds.
        tooling: k6
      - id: test-auto-scaling
        description: Verify auto-scaling triggers at 70% CPU utilisation.
        tooling: terraform

  - id: GOV-010
    title: Ensure ownership metadata is present for every resource
    priority: high
    classification: governance
    rationale: Support cost allocation and on-call routing.
    tests:
      - id: test-tag-enforcement
        description: Confirm mandatory tags (Environment, CostCentre, Owner) exist on provisioned resources.
        tooling: policy-as-code
```

### 13_CODE_H: Requirements Validation Framework {#13_code_h}
*Listing 13-H.*
*Referenced from Chapter 13: [Testing Strategies](13_testing_strategies.md)*

Python framework for automated validation of requirements against Infrastructure as Code implementations, including test execution and compliance coverage reporting.

```python
# requirements/validator.py
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List

import yaml


@dataclass
class Requirement:
    id: str
    title: str
    classification: str
    priority: str
    tests: List[Dict[str, str]]
    rationale: str = ""  # present in catalogue.yaml; Requirement(**item) fails without it


class RequirementValidator:
    def __init__(self, catalogue: Iterable[Requirement]):
        self.catalogue = list(catalogue)

    @classmethod
    def from_file(cls, path: Path) -> 'RequirementValidator':
        data = yaml.safe_load(path.read_text())
        requirements = [Requirement(**item) for item in data['requirements']]
        return cls(requirements)

    def coverage_summary(self, executed_tests: Iterable[str]) -> Dict[str, float]:
        executed = set(executed_tests)
        total = len(self.catalogue)
        covered = sum(1 for requirement in self.catalogue if self._is_covered(requirement, executed))
        return {
            'total_requirements': total,
            'covered_requirements': covered,
            'coverage_percentage': round((covered / total) * 100, 2) if total else 100.0,
        }

    def missing_tests(self, executed_tests: Iterable[str]) -> Dict[str, List[str]]:
        executed = set(executed_tests)
        missing: Dict[str, List[str]] = {}
        for requirement in self.catalogue:
            outstanding = [test['id'] for test in requirement.tests if test['id'] not in executed]
            if outstanding:
                missing[requirement.id] = outstanding
        return missing

    @staticmethod
    def _is_covered(requirement: Requirement, executed: set[str]) -> bool:
        return all(test['id'] in executed for test in requirement.tests)


def load_validator(catalogue_path: str) -> RequirementValidator:
    return RequirementValidator.from_file(Path(catalogue_path))
```

### 13_CODE_I: Terratest for GDPR-Compliant Infrastructure {#13_code_i}
*Listing 13-I.*
*Referenced from Chapter 13: [Testing Strategies](13_testing_strategies.md)*

Comprehensive Terratest example demonstrating testing of Terraform infrastructure with GDPR compliance validation, data residency requirements and organisational tagging standards for regulated environments.

```go
// test/terraform_gdpr_test.go
package test

import (
    "context"
    "testing"

    awssdk "github.com/aws/aws-sdk-go-v2/aws"
    "github.com/aws/aws-sdk-go-v2/service/s3"
    s3types "github.com/aws/aws-sdk-go-v2/service/s3/types"
    "github.com/gruntwork-io/terratest/modules/aws"
    "github.com/gruntwork-io/terratest/modules/terraform"
    "github.com/stretchr/testify/require"
)

func TestPlatformStackGDPRCompliance(t *testing.T) {
    t.Parallel()

    region := "eu-west-1"
    terraformOptions := &terraform.Options{
        TerraformDir: "../infrastructure",
        Vars: map[string]interface{}{
            "environment": "staging",
            "region":      region,
        },
    }

    defer terraform.Destroy(t, terraformOptions)
    terraform.InitAndApply(t, terraformOptions)

    vpcID := terraform.Output(t, terraformOptions, "vpc_id")
    require.NotEmpty(t, vpcID)

    flowLogsEnabled := terraform.Output(t, terraformOptions, "vpc_flow_logs_enabled")
    require.Equal(t, "true", flowLogsEnabled, "VPC flow logs must be enabled for GDPR auditing")

    // Terratest has no S3 encryption helper: call the AWS SDK (v2) through the
    // client that Terratest builds for the region
    bucketID := terraform.Output(t, terraformOptions, "logging_bucket_id")
    s3Client := aws.NewS3Client(t, region)
    encryption, err := s3Client.GetBucketEncryption(context.Background(), &s3.GetBucketEncryptionInput{
        Bucket: awssdk.String(bucketID),
    })
    require.NoError(t, err, "Logging bucket must have server-side encryption configured")
    rules := encryption.ServerSideEncryptionConfiguration.Rules
    require.NotEmpty(t, rules)
    require.Equal(t, s3types.ServerSideEncryptionAes256, rules[0].ApplyServerSideEncryptionByDefault.SSEAlgorithm)

    // Terratest's signature is GetTagsForVpc(t, vpcID, region)
    tags := aws.GetTagsForVpc(t, vpcID, region)
    require.Equal(t, "true", tags["GdprCompliant"])
    require.Equal(t, "EU", tags["DataResidency"])
}
```

### 13_CODE_J: Policy-as-Code Testing with OPA {#13_code_j}
*Listing 13-J.*
*Referenced from Chapter 13: [Testing Strategies](13_testing_strategies.md)*

Open Policy Agent (OPA) test examples demonstrating validation of S3 bucket encryption, EC2 security group requirements and GDPR data classification compliance.

```rego
# policies/infrastructure/security.rego
package infrastructure.security

import rego.v1

deny contains msg if {
  input.resource.type == "aws_s3_bucket"
  not input.resource.encryption.enabled
  msg := sprintf("Bucket %s must enable server-side encryption", [input.resource.id])
}

deny contains msg if {
  input.resource.type == "aws_security_group_rule"
  input.resource.protocol == "tcp"
  input.resource.port == 22
  input.resource.cidr == "0.0.0.0/0"
  msg := sprintf("SSH rule %s exposes port 22 to the internet", [input.resource.id])
}

deny contains msg if {
  input.resource.type == "aws_db_instance"
  input.resource.tags["Classification"] == "confidential"
  not input.resource.encryption.enabled
  msg := sprintf("RDS instance %s storing confidential data must be encrypted", [input.resource.id])
}

# policies/infrastructure/security_test.rego
package infrastructure.security_test

import rego.v1

# deny is a set: test membership with "in" rather than indexing results[0],
# which would be a membership test for the value 0 and never succeed

test_enforces_bucket_encryption if {
  results := data.infrastructure.security.deny with input as {
    "resource": {
      "id": "audit-logs",
      "type": "aws_s3_bucket",
      "encryption": {"enabled": false}
    }
  }

  "Bucket audit-logs must enable server-side encryption" in results
}

test_blocks_internet_ssh if {
  results := data.infrastructure.security.deny with input as {
    "resource": {
      "id": "sg-rule-1",
      "type": "aws_security_group_rule",
      "protocol": "tcp",
      "port": 22,
      "cidr": "0.0.0.0/0"
    }
  }

  "SSH rule sg-rule-1 exposes port 22 to the internet" in results
}

test_requires_encrypted_confidential_databases if {
  results := data.infrastructure.security.deny with input as {
    "resource": {
      "id": "rds-analytics",
      "type": "aws_db_instance",
      "tags": {"Classification": "confidential"},
      "encryption": {"enabled": false}
    }
  }

  "RDS instance rds-analytics storing confidential data must be encrypted" in results
}

test_allows_encrypted_bucket if {
  results := data.infrastructure.security.deny with input as {
    "resource": {
      "id": "audit-logs",
      "type": "aws_s3_bucket",
      "encryption": {"enabled": true}
    }
  }

  count(results) == 0
}
```

### 13_CODE_K: Kubernetes Infrastructure Test Suite {#13_code_k}
*Listing 13-K.*
*Referenced from Chapter 13: [Testing Strategies](13_testing_strategies.md)*

Comprehensive Kubernetes infrastructure test suite demonstrating validation of resource quotas, Pod Security Admission levels, network policies and GDPR-compliant encrypted storage classes using ConfigMap-based test runners and Kubernetes Jobs.

```yaml
# k8s/tests/infrastructure-validation.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: infrastructure-test-runner
data:
  tests.sh: |
    #!/usr/bin/env bash
    set -euo pipefail

    echo "Validating namespace resource quotas..."
    # kubectl exits 0 even when nothing is found, so count the rows instead
    quota_count="$(kubectl get resourcequota -A --no-headers 2>/dev/null | wc -l)"
    if [ "$quota_count" -eq 0 ]; then
      echo "# FAIL: Resource quotas missing"; exit 1
    fi

    echo "Validating Pod Security Admission levels..."
    # PSA labels are set on namespaces, not on pods: every workload namespace
    # must carry pod-security.kubernetes.io/enforce
    kubectl get namespaces -o json | jq -e '
      [.items[]
        | select(.metadata.name | test("^kube-") | not)
        | select(.metadata.labels["pod-security.kubernetes.io/enforce"] == null)]
      | length == 0' > /dev/null || {
      echo "# FAIL: Namespaces without a Pod Security Admission enforce level"; exit 1;
    }

    echo "Validating encrypted persistent storage..."
    # Encryption is a StorageClass parameter of the CSI driver (EBS: encrypted: "true"),
    # not an annotation on the PersistentVolume
    kubectl get storageclass -o json | jq -e '
      [.items[] | select((.parameters.encrypted // "false") != "true")] | length == 0' > /dev/null || {
      echo "# FAIL: All storage classes must enable encryption"; exit 1;
    }

    echo "# Pass: Infrastructure validation passed"
---
apiVersion: batch/v1
kind: Job
metadata:
  name: infrastructure-validation
spec:
  template:
    spec:
      restartPolicy: Never
      serviceAccountName: platform-auditor
      containers:
        - name: validator
          # alpine/k8s bundles kubectl, bash and jq. Keep the kubectl minor version
          # within one release of the cluster and pin by digest in production.
          image: alpine/k8s:1.35.9
          command: ["/bin/bash", "/scripts/tests.sh"]
          volumeMounts:
            - name: test-scripts
              mountPath: /scripts
      volumes:
        - name: test-scripts
          configMap:
            name: infrastructure-test-runner
            defaultMode: 0555
```

### 13_CODE_L: Infrastructure Testing Pipeline {#13_code_l}
*Listing 13-L.*
*Referenced from Chapter 13: [Testing Strategies](13_testing_strategies.md)*

Complete GitHub Actions workflow demonstrating infrastructure testing pipeline with static analysis (Terraform fmt, Checkov, OPA), unit testing (Terratest), integration testing with temporary environments, compliance validation (GDPR, encryption, regional restrictions), and performance testing with cost analysis.

```yaml
# .github/workflows/infrastructure-pipeline.yml
name: Infrastructure Quality Gate

on:
  pull_request:
    paths:
      - 'infrastructure/**'
      - 'modules/**'
      - 'policies/**'
      - 'test/**'

env:
  TF_VERSION: 1.17.1

jobs:
  static-analysis:
    name: Static Analysis
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: hashicorp/setup-terraform@v4
        with:
          terraform_version: ${{ env.TF_VERSION }}
      - name: Terraform fmt
        run: terraform fmt -check -recursive
      # validate needs initialised providers and modules; -backend=false skips the remote state
      - name: Terraform init and validate
        working-directory: infrastructure
        run: |
          terraform init -backend=false
          terraform validate
      - name: Checkov security scan
        uses: bridgecrewio/checkov-action@v12
        with:
          directory: infrastructure

  policy:
    name: Policy-as-Code
    runs-on: ubuntu-latest
    needs: static-analysis
    steps:
      - uses: actions/checkout@v7
      # OPA is not part of the ubuntu-latest image
      - uses: open-policy-agent/setup-opa@v2
        with:
          version: latest
      - name: Evaluate OPA policies
        run: |
          opa test policies/infrastructure -v

  unit-tests:
    name: Terratest Suite
    runs-on: ubuntu-latest
    needs: policy
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-go@v7
        with:
          go-version-file: test/go.mod
      # terraform_wrapper must be off: Terratest parses the raw Terraform output
      - uses: hashicorp/setup-terraform@v4
        with:
          terraform_version: ${{ env.TF_VERSION }}
          terraform_wrapper: false
      - name: Execute Terratest
        run: go test ./test -timeout 45m

  integration:
    name: Ephemeral Environment Validation
    runs-on: ubuntu-latest
    needs: unit-tests
    env:
      TF_IN_AUTOMATION: true
    steps:
      - uses: actions/checkout@v7
      - uses: hashicorp/setup-terraform@v4
        with:
          terraform_version: ${{ env.TF_VERSION }}
          terraform_wrapper: false
      - name: Terraform init
        run: terraform init
      - name: Create workspace
        run: terraform workspace new pr-${{ github.event.number }} || terraform workspace select pr-${{ github.event.number }}
      - name: Terraform plan (ephemeral)
        run: terraform plan -out=tfplan
      - name: Terraform apply (ephemeral)
        run: terraform apply -auto-approve tfplan
      - name: Execute integration scripts
        run: ./scripts/validate-integration.sh
      - name: Terraform destroy
        if: always()
        run: terraform destroy -auto-approve

  compliance:
    name: Compliance Checks
    runs-on: ubuntu-latest
    needs: integration
    steps:
      - uses: actions/checkout@v7
      - name: Run requirements coverage
        run: |
          python3 -m pip install -r requirements.txt
          python3 requirements/report.py --catalogue requirements/catalogue.yaml --results reports/test-results.json

  performance:
    name: Performance and Cost Review
    runs-on: ubuntu-latest
    needs: compliance
    steps:
      - uses: actions/checkout@v7
      # k6 is not part of the ubuntu-latest image
      - uses: grafana/setup-k6-action@v1
      - name: Execute k6 performance tests
        run: k6 run tests/performance/k6-load-test.js
      - name: Analyse cost impact
        run: python3 scripts/cost_analysis.py --plan outputs/terraform-plan.json

  summary:
    name: Quality Summary
    runs-on: ubuntu-latest
    needs: [performance]
    steps:
      - uses: actions/checkout@v7
      - name: Collate results
        run: ./scripts/summarise-quality-gates.sh
```

---

## Organisational Change and Team Structures {#organisational-change}

### 17_CODE_1: Infrastructure Platform Team Blueprint {#17_code_1}
*Listing 17-A.*
*Referenced from chapter 17: [Organisational Change and Team Structures](17_organisational_change.md)*

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

### 17_CODE_2: IaC Competency Framework Utilities {#17_code_2}
*Listing 17-B.*
*Referenced from chapter 17: [Organisational Change and Team Structures](17_organisational_change.md)*

```python
# training/iac_competency_framework.py
from datetime import datetime
from typing import Dict, List, Optional


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

        # Standard module sequence used for next-module recommendations
        self.module_sequence = [
            "Terraform Fundamentals for Regulated Enterprises",
            "Cloud Security for Regulated Environments"
        ]

        # Completed modules per individual (persist this in a real system)
        self.progress: Dict[str, List[str]] = {}

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

        self.progress.setdefault(individual_id, []).append(completed_module)

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
        """Generate a team competency matrix for skills gap analysis.

        Each member is a dict with "name", "role" and "skills", where "skills"
        maps a skill domain to a competency level (novice ... expert).
        """

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

        if team_members:
            competency_matrix["overall_readiness"] = round(total_competency / len(team_members), 1)
        competency_matrix["skill_gaps"] = self._identify_team_skill_gaps(team_members)
        competency_matrix["training_recommendations"] = self._recommend_team_training(competency_matrix)

        return competency_matrix

    def _level_index(self, level: str) -> int:
        """Position of a competency level (novice = 0 ... expert = 3); unknown levels count as novice."""
        levels = list(self.competency_levels)
        return levels.index(level) if level in levels else 0

    def _recommend_next_module(self, individual_id: str) -> Optional[str]:
        """Recommend the first module in the standard sequence not yet completed."""
        completed = self.progress.get(individual_id, [])
        return next((module for module in self.module_sequence if module not in completed), None)

    def _calculate_competency_score(self, member: Dict) -> float:
        """Score 0-100: mean level across all skill domains, expert in every domain = 100."""
        skills = member.get("skills", {})
        max_index = len(self.competency_levels) - 1
        total = sum(self._level_index(skills.get(domain, "novice")) for domain in self.skill_domains)
        return round(100 * total / (max_index * len(self.skill_domains)), 1)

    def _identify_development_needs(self, member: Dict) -> List[str]:
        """Skill domains in which the member is below intermediate level."""
        skills = member.get("skills", {})
        threshold = self._level_index("intermediate")
        return [domain for domain in self.skill_domains
                if self._level_index(skills.get(domain, "novice")) < threshold]

    def _identify_team_skill_gaps(self, team_members: List[Dict]) -> List[str]:
        """Skill domains in which no team member has reached advanced level."""
        threshold = self._level_index("advanced")
        gaps = []
        for domain in self.skill_domains:
            best = max(
                (self._level_index(member.get("skills", {}).get(domain, "novice")) for member in team_members),
                default=0
            )
            if best < threshold:
                gaps.append(domain)
        return gaps

    def _recommend_team_training(self, competency_matrix: Dict) -> List[str]:
        """Translate team-wide skill gaps into training recommendations."""
        recommendations = []
        for domain in competency_matrix["skill_gaps"]:
            modules = self._generate_domain_modules(domain, "novice", "advanced")
            if modules:
                recommendations.extend(f"{domain}: {module['name']}" for module in modules)
            else:
                recommendations.append(f"{domain}: commission a domain-specific workshop (no standard module defined)")
        return recommendations


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

### 17_CODE_3: DevOps Performance Measurement Framework {#17_code_3}
*Listing 17-C.*
*Referenced from chapter 17: [Organisational Change and Team Structures](17_organisational_change.md)*

```yaml
# metrics/devops_performance_metrics.yaml
performance_measurement_framework:
  name: "DevOps Team Performance Metrics"

  technical_metrics:
    # Performance levels follow the four clusters of the DORA Accelerate State of
    # DevOps Report 2024. The report gives representative cluster values, not
    # ranges, so treat them as benchmarks and set organisation-specific targets.
    deployment_frequency:
      description: "How often the team deploys to production"
      measurement: "Deployments per day/week"
      target_values:
        elite: "On demand (multiple deploys per day)"
        high: "Between once per day and once per week"
        medium: "Between once per week and once per month"
        low: "Between once per month and once every six months"
      collection_method: "Automated from CI/CD pipeline"

    lead_time_for_changes:
      description: "Time from code commit to production deployment"
      measurement: "Hours/days"
      target_values:
        elite: "Less than one day"
        high: "Between one day and one week"
        medium: "Between one week and one month"
        low: "Between one month and six months"
      collection_method: "Git and deployment tool integration"

    failed_deployment_recovery_time:
      description: "Time to recover from a failed deployment (DORA's successor to time to restore service)"
      measurement: "Hours"
      target_values:
        elite: "Less than one hour"
        high: "Less than one day"
        medium: "Less than one day"
        low: "Between one week and one month"
      collection_method: "Incident management systems"

    change_failure_rate:
      description: "Percentage of deployments causing production issues"
      measurement: "Percentage"
      target_values:
        elite: "5%"
        high: "20%"
        medium: "10%"
        low: "40%"
      collection_method: "Incident correlation with deployments"

    rework_rate:
      description: "Percentage of deployments that are unplanned fixes of earlier changes (the fifth DORA metric since 2024)"
      measurement: "Percentage"
      target: "Track together with change failure rate; set organisation-specific targets"
      collection_method: "Deployment metadata (planned versus unplanned deployments)"
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
      industry: "Compare with the DORA Accelerate State of DevOps Report clusters"
      regional: "Compare with peer organisations"

    action_planning:
      identification: "Identify lowest-performing metrics"
      root_cause: "Analyse underlying causes"
      solutions: "Develop targeted improvement initiatives"
      tracking: "Monitor improvement progress monthly"
```

The performance levels in `technical_metrics` follow the four clusters of the DORA Accelerate State of DevOps Report 2024 [Source [49]](33_references.md#source-49). The report publishes representative values per cluster rather than target ranges, and it tracks five metrics (deployment frequency, lead time for changes, change failure rate, failed deployment recovery time and rework rate), so organisations should treat the values as benchmarks and set their own targets.


---

## References and Navigation

Each code example in this appendix can be referenced from the main text using its unique identifier. To find specific implementations:

1. **Use search function** - Search for code type or technology (e.g., "Terraform", "CloudFormation", "Python")
2. **Follow the categories** - Navigate to the relevant section based on use case
3. **Use cross-references** - Follow links back to the main chapters for context

### Conventions for Code Examples

- **Identifiers**: Every listing is numbered `[chapter]_CODE_[number]` (or lettered, as in 13_CODE_A) and carries a stable anchor for cross-references
- **Backlinks**: The italic line under each heading names the chapter that introduces the listing
- **Language tags**: Code fences carry the language (`yaml`, `hcl`, `rego`, `go`, `python`, `typescript`, `json`, `groovy`, `structurizr`) used by the build and by syntax highlighting
- **Comments**: All code examples contain comments for clarity, and version pins are refreshed at each review of the manuscript

### Updates and Maintenance

This appendix is updated regularly when new code examples are added to the book's main chapters. For the latest version of code examples, see the book's GitHub repository.

- - -

_For more information about specific implementations, see the respective main chapters where the code examples are introduced and explained in their context._

- - -

## Chapter 14 Reference Implementations {#chapter-14-implementations}

The extended Terraform implementation that once appeared inline in Chapter 14 is preserved here so that readers can access the full listing without interrupting the main narrative. Cross-references in the chapter point to these appendix entries for quick navigation.

> **Note:** Moving the code to Appendix A keeps Chapter 14 focused on adoption strategy while still providing the complete infrastructure example for practitioners.

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

variable "instance_type" {
  description = "EC2 instance type for the application tier"
  type        = string
  default     = "t3.small"
}

variable "enable_monitoring" {
  description = "Enable detailed CloudWatch monitoring on the instances"
  type        = bool
  default     = false
}

data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-2023.*-x86_64"]
  }
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

# An internet-facing load balancer requires an internet gateway and a public route
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.application_name}-${var.environment}-igw"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "${var.application_name}-${var.environment}-public-rt"
  }
}

resource "aws_route_table_association" "public" {
  count          = length(aws_subnet.public)
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

# Security groups
resource "aws_security_group" "alb" {
  name        = "${var.application_name}-${var.environment}-alb-sg"
  description = "Allow web traffic from the internet to the load balancer"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP (redirected to HTTPS by the listener)"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "app" {
  name        = "${var.application_name}-${var.environment}-app-sg"
  description = "Allow traffic from the load balancer only"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "Application port from the ALB"
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
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

resource "aws_lb_target_group" "main" {
  name     = "${var.application_name}-${var.environment}-tg"
  port     = 8080
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id

  health_check {
    path    = "/health"
    matcher = "200"
  }
}

# Launch template for the application instances
resource "aws_launch_template" "main" {
  name_prefix   = "${var.application_name}-${var.environment}-"
  image_id      = data.aws_ami.amazon_linux.id
  instance_type = var.instance_type

  vpc_security_group_ids = [aws_security_group.app.id]

  monitoring {
    enabled = var.enable_monitoring
  }

  metadata_options {
    http_tokens = "required" # IMDSv2 only
  }

  tag_specifications {
    resource_type = "instance"
    tags = {
      Environment = var.environment
      Application = var.application_name
    }
  }
}

# Auto Scaling Group
resource "aws_autoscaling_group" "main" {
  name                      = "${var.application_name}-${var.environment}-asg"
  vpc_zone_identifier       = aws_subnet.public[*].id
  target_group_arns         = [aws_lb_target_group.main.arn]
  health_check_type         = "ELB"
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

output "load_balancer_arn_suffix" {
  description = "ARN suffix of the load balancer, used as the CloudWatch metric dimension"
  value       = aws_lb.main.arn_suffix
}

output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}
```

### 14_CODE_2: Environment configuration and observability controls {#14_code_2}
*Referenced from Chapter 14: [Architecture as Code in Practice](14_practical_implementation.md)*

This configuration layers production-specific settings on top of the shared module, including state management, default tags, log retention, and a CloudWatch dashboard for operational oversight. The S3 backend uses Terraform's native state locking (`use_lockfile = true`, Terraform 1.11 or later): DynamoDB-based locking is deprecated since Terraform 1.11 in favour of S3-native locking [Source [17]](33_references.md#source-17). Backend blocks cannot reference variables, so environment-specific backend values belong in a `backend.hcl` file passed to `terraform init -backend-config`.

```hcl
# environments/production/main.tf
terraform {
  required_version = ">= 1.11"

  backend "s3" {
    bucket  = "company-terraform-state-prod"
    key     = "web-application/terraform.tfstate"
    region  = "eu-west-1"
    encrypt = true
    # S3-native state locking (Terraform 1.11+); the DynamoDB lock table is deprecated
    use_lockfile = true
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = "eu-west-1"

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

  # Production-specific overrides (declared as variables in the module)
  instance_type     = "t3.large"
  enable_monitoring = true
}

# Production-specific resources
resource "aws_cloudwatch_log_group" "application" {
  name              = "/company-web-app/production"
  retention_in_days = 365 # retention control for operational and audit logs
}

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
          region  = "eu-west-1"
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

The workflow below demonstrates how to plan and apply Terraform changes across development, staging, and production with explicit separation between planning and deployment stages. It authenticates to AWS through GitHub's OIDC provider rather than long-lived access keys, and production deployments are gated by the protection rules of the `production` environment.

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

permissions:
  id-token: write   # OIDC federation with AWS instead of long-lived access keys
  contents: read

env:
  TF_VERSION: 1.17.1
  AWS_REGION: eu-west-1

jobs:
  plan:
    name: Terraform Plan
    runs-on: ubuntu-latest
    strategy:
      matrix:
        environment: [development, staging, production]

    steps:
    - name: Checkout code
      uses: actions/checkout@v7

    - name: Setup Terraform
      uses: hashicorp/setup-terraform@v4
      with:
        terraform_version: ${{ env.TF_VERSION }}

    - name: Configure AWS credentials (OIDC)
      uses: aws-actions/configure-aws-credentials@v6
      with:
        role-to-assume: ${{ vars.AWS_DEPLOY_ROLE_ARN }}
        aws-region: ${{ env.AWS_REGION }}

    - name: Terraform Init
      working-directory: infrastructure/environments/${{ matrix.environment }}
      run: terraform init

    - name: Terraform Validate
      working-directory: infrastructure/environments/${{ matrix.environment }}
      run: terraform validate

    # terraform.tfvars is loaded automatically, so no -var-file is needed
    - name: Terraform Plan
      working-directory: infrastructure/environments/${{ matrix.environment }}
      run: terraform plan -out=tfplan-${{ matrix.environment }}

    # Artifact names must be unique per job since upload-artifact v4
    - name: Upload plan artifact
      uses: actions/upload-artifact@v7
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
      uses: actions/checkout@v7

    - name: Setup Terraform
      uses: hashicorp/setup-terraform@v4
      with:
        terraform_version: ${{ env.TF_VERSION }}

    - name: Configure AWS credentials (OIDC)
      uses: aws-actions/configure-aws-credentials@v6
      with:
        role-to-assume: ${{ vars.AWS_DEPLOY_ROLE_ARN }}
        aws-region: ${{ env.AWS_REGION }}

    - name: Download plan artifact
      uses: actions/download-artifact@v8
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
    # The protection rules of the "production" environment enforce the manual approval
    environment: production

    steps:
    - name: Manual approval checkpoint
      run: echo "Production deployment approved through the environment protection rule"

    # Repeat the deploy steps for the production environment here
```

---

## Chapter 15 Reference Implementations {#chapter-15-implementations}

### 15_CODE_1: Cost-aware Terraform infrastructure configuration {#15_code_1}
*Referenced from Chapter 15: [Cost Optimisation and Resource Management](15_cost_optimization.md)*

This Terraform configuration demonstrates comprehensive cost optimisation strategies including budget management, cost allocation tagging, and intelligent instance type selection using spot instances and mixed instance policies. The input variables are declared inline so that the listing validates on its own.

```hcl
# cost_optimized_infrastructure.tf
terraform {
  required_version = ">= 1.11"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

# Input variables (normally kept in variables.tf)
variable "project_name" {
  description = "Project identifier used for naming and cost allocation"
  type        = string
}

variable "environment" {
  description = "Deployment environment (development, staging, production)"
  type        = string
}

variable "aws_region" {
  description = "EU region in which the workload runs, e.g. eu-west-1"
  type        = string
  default     = "eu-west-1"
}

variable "cost_centre" {
  description = "Cost centre code used by finance"
  type        = string
}

variable "team_email" {
  description = "Distribution list of the owning team"
  type        = string
}

variable "finance_email" {
  description = "Finance contact for budget notifications"
  type        = string
}

variable "budget_threshold" {
  description = "Alert threshold recorded on the resources, e.g. 80%"
  type        = string
  default     = "80%"
}

variable "monthly_budget_limit_usd" {
  description = "Monthly budget limit in USD (AWS bills in USD)"
  type        = string
}

variable "max_spot_price" {
  description = "Maximum hourly Spot price in USD; null caps bids at the On-Demand price"
  type        = string
  default     = null
}

variable "private_subnet_ids" {
  description = "Private subnet IDs for the Auto Scaling group"
  type        = list(string)
}

variable "min_instances" {
  description = "Minimum number of instances"
  type        = number
  default     = 1
}

variable "max_instances" {
  description = "Maximum number of instances"
  type        = number
  default     = 6
}

variable "desired_instances" {
  description = "Desired number of instances"
  type        = number
  default     = 2
}

data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-2023.*-x86_64"]
  }
}

# Cost allocation tags for all infrastructure
locals {
  cost_tags = {
    CostCentre  = var.cost_centre
    Project     = var.project_name
    Environment = var.environment
    Owner       = var.team_email
    BudgetAlert = var.budget_threshold
    # timeadd takes duration units (h, m, s), not arithmetic: 720h is 30 days.
    # timestamp() changes on every plan, so expect a tag diff on each run.
    ReviewDate = formatdate("YYYY-MM-DD", timeadd(timestamp(), "720h"))
    Region     = var.aws_region
  }
}

# Budget with automatic alerts (EUR equivalent tracked separately for EU reporting)
resource "aws_budgets_budget" "project_budget" {
  name         = "${var.project_name}-budget"
  budget_type  = "COST"
  limit_amount = var.monthly_budget_limit_usd # AWS bills in USD
  limit_unit   = "USD"
  time_unit    = "MONTHLY"

  # cost_filter blocks replaced the removed cost_filters map;
  # tag filters use the form "user:<key>$<value>"
  cost_filter {
    name   = "TagKeyValue"
    values = ["user:Project${"$"}${var.project_name}"]
  }

  cost_filter {
    name   = "Region"
    values = [var.aws_region] # Filter by EU region
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 80
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = [var.team_email, var.finance_email]
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 100
    threshold_type             = "PERCENTAGE"
    notification_type          = "FORECASTED"
    subscriber_email_addresses = [var.team_email, var.finance_email]
  }
}

# Cost-optimised EC2 with Spot instances
resource "aws_launch_template" "cost_optimized" {
  name_prefix = "${var.project_name}-cost-opt-"
  image_id    = data.aws_ami.amazon_linux.id

  # Mixed instance types for cost optimisation
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

  # Spot instance preference for cost optimisation
  instance_market_options {
    market_type = "spot"
    spot_options {
      max_price = var.max_spot_price
    }
  }

  tag_specifications {
    resource_type = "instance"
    tags          = local.cost_tags
  }
}

# Auto Scaling with cost considerations
resource "aws_autoscaling_group" "cost_aware" {
  name                = "${var.project_name}-cost-aware-asg"
  vpc_zone_identifier = var.private_subnet_ids
  min_size            = var.min_instances
  max_size            = var.max_instances
  desired_capacity    = var.desired_instances

  # Mixed instance type strategy for cost optimisation
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

### 15_CODE_2: Kubernetes cost optimisation manifests {#15_code_2}
*Referenced from Chapter 15: [Cost Optimisation and Resource Management](15_cost_optimization.md)*

These Kubernetes manifests demonstrate resource quotas, limit ranges, and autoscaling configurations for cost-effective workload management. Because the Vertical Pod Autoscaler and the Horizontal Pod Autoscaler must not act on the same resource metric, the VPA controls memory requests while the HPA scales replicas on CPU utilisation.

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
# VPA and HPA must not act on the same resource metric (VPA known limitations):
# the VPA right-sizes memory requests, the HPA below scales replicas on CPU only.
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
      controlledResources: ["memory"]
      maxAllowed:
        memory: "2Gi"
      minAllowed:
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

### 15_CODE_3: AWS cost monitoring and optimisation automation {#15_code_3}
*Referenced from Chapter 15: [Cost Optimisation and Resource Management](15_cost_optimization.md)*

This Python script provides automated cost analysis, rightsizing recommendations, and identification of unused resources for AWS environments. All helper methods are implemented against the Cost Explorer, EC2, ELBv2 and CloudWatch APIs; the Spot-instance estimate is an explicitly labelled heuristic rather than an AWS recommendation API call.

```python
# cost_monitoring/cost_optimizer.py
import boto3
from datetime import datetime, timedelta
from typing import Dict, List

class AWSCostOptimizer:
    """
    Automated cost optimisation for AWS resources across EU regions
    """

    def __init__(self, region='eu-west-1', eu_regions=None):
        """
        Initialise cost optimiser for EU regions.

        Args:
            region: Primary AWS region (defaults to eu-west-1, Ireland)
            eu_regions: List of EU regions to analyse (defaults to major EU regions)
        """
        if eu_regions is None:
            # Default EU regions for multi-region cost analysis
            eu_regions = ['eu-west-1', 'eu-central-1', 'eu-west-2', 'eu-west-3', 'eu-south-1', 'eu-north-1']

        self.region = region
        self.eu_regions = eu_regions
        self.cost_explorer = boto3.client('ce', region_name=region)
        self.ec2 = boto3.client('ec2', region_name=region)
        self.rds = boto3.client('rds', region_name=region)
        self.cloudwatch = boto3.client('cloudwatch', region_name=region)

    def analyze_cost_trends(self, days_back=30) -> Dict:
        """Analyse cost trends for the last period across EU regions"""

        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days_back)

        response = self.cost_explorer.get_cost_and_usage(
            TimePeriod={
                'Start': start_date.strftime('%Y-%m-%d'),
                'End': end_date.strftime('%Y-%m-%d')
            },
            Granularity='DAILY',
            Metrics=['BlendedCost'],
            # Cost Explorer accepts at most two GroupBy entries; the regions are
            # constrained through the Filter instead of a third grouping
            GroupBy=[
                {'Type': 'DIMENSION', 'Key': 'SERVICE'},
                {'Type': 'TAG', 'Key': 'Project'}
            ],
            Filter={
                'Dimensions': {
                    'Key': 'REGION',
                    'Values': self.eu_regions
                }
            }
        )

        return self._process_cost_data(response)

    def _process_cost_data(self, response: Dict) -> Dict:
        """Aggregate Cost Explorer results per service, per project tag and per day"""

        totals_by_service: Dict[str, float] = {}
        totals_by_project: Dict[str, float] = {}
        daily_totals: List[Dict] = []

        for day in response.get('ResultsByTime', []):
            day_total = 0.0
            for group in day.get('Groups', []):
                service, project = group['Keys']  # project arrives as "Project$<value>"
                amount = float(group['Metrics']['BlendedCost']['Amount'])
                totals_by_service[service] = totals_by_service.get(service, 0.0) + amount
                totals_by_project[project] = totals_by_project.get(project, 0.0) + amount
                day_total += amount
            daily_totals.append({'date': day['TimePeriod']['Start'], 'cost_usd': round(day_total, 2)})

        return {
            'period_total_usd': round(sum(day['cost_usd'] for day in daily_totals), 2),
            'by_service_usd': {k: round(v, 2) for k, v in sorted(totals_by_service.items(), key=lambda item: -item[1])},
            'by_project_usd': {k: round(v, 2) for k, v in totals_by_project.items()},
            'daily_usd': daily_totals
        }

    def identify_rightsizing_opportunities(self) -> List[Dict]:
        """Identify EC2 instances that can be rightsized across EU regions"""

        rightsizing_response = self.cost_explorer.get_rightsizing_recommendation(
            Service='AmazonEC2',
            Configuration={
                'BenefitsConsidered': True,
                'RecommendationTarget': 'SAME_INSTANCE_FAMILY'
            },
            Filter={
                'Dimensions': {
                    'Key': 'REGION',
                    'Values': self.eu_regions
                }
            }
        )

        opportunities = []

        for recommendation in rightsizing_response.get('RightsizingRecommendations', []):
            if recommendation['RightsizingType'] == 'Modify':
                current = recommendation['CurrentInstance']
                target = recommendation['ModifyRecommendationDetail']['TargetInstances'][0]
                opportunities.append({
                    'instance_id': current['ResourceId'],
                    'current_type': current['InstanceName'],
                    'recommended_type': target['InstanceName'],
                    'estimated_monthly_savings_usd': float(target['EstimatedMonthlySavings']),
                    # CurrentInstance exposes ResourceUtilization (not UtilizationMetrics)
                    'utilisation': current.get('ResourceUtilization', {}),
                    'region': current.get('ResourceDetails', {}).get('EC2ResourceDetails', {}).get('Region', 'unknown')
                })

        return opportunities

    def get_unused_resources(self) -> Dict:
        """Identify unused resources that can be terminated across EU regions"""

        unused_resources = {
            'unattached_volumes': self._find_unattached_ebs_volumes(),
            'unused_elastic_ips': self._find_unused_elastic_ips(),
            'idle_load_balancers': self._find_idle_load_balancers(),
            'stopped_instances': self._find_stopped_instances()
        }

        return unused_resources

    def generate_cost_optimization_plan(self, project_tag: str) -> Dict:
        """Generate comprehensive cost optimisation plan for EU regions"""

        plan = {
            'project': project_tag,
            'analysis_date': datetime.now().isoformat(),
            'eu_regions_analysed': self.eu_regions,
            'current_monthly_cost_usd': self._get_current_monthly_cost(project_tag),
            'recommendations': {
                'rightsizing': self.identify_rightsizing_opportunities(),
                'unused_resources': self.get_unused_resources(),
                'reserved_instances': self._analyze_reserved_instance_opportunities(),
                'spot_instances': self._analyze_spot_instance_opportunities()
            },
            'potential_monthly_savings_usd': 0,
            'notes': 'Costs are in USD (AWS billing currency). Convert to EUR using current exchange rate for EU financial reporting.'
        }

        # Calculate total potential savings
        total_savings = 0
        for rec_type, recommendations in plan['recommendations'].items():
            if isinstance(recommendations, list):
                total_savings += sum(rec.get('estimated_monthly_savings_usd', 0) for rec in recommendations)
            elif isinstance(recommendations, dict) and rec_type == 'unused_resources':
                for resources in recommendations.values():
                    total_savings += sum(rec.get('estimated_monthly_savings_usd', 0) for rec in resources)
            elif isinstance(recommendations, dict):
                total_savings += recommendations.get('estimated_monthly_savings_usd', 0)

        plan['potential_monthly_savings_usd'] = round(total_savings, 2)
        plan['savings_percentage'] = (total_savings / plan['current_monthly_cost_usd']) * 100 if plan['current_monthly_cost_usd'] > 0 else 0

        return plan

    def _get_current_monthly_cost(self, project_tag: str) -> float:
        """Month-to-date cost of the project tag across the EU regions"""

        today = datetime.now().date()
        start = today.replace(day=1)
        if start == today:  # Cost Explorer requires End to be later than Start
            start = (today - timedelta(days=1)).replace(day=1)

        response = self.cost_explorer.get_cost_and_usage(
            TimePeriod={'Start': start.strftime('%Y-%m-%d'), 'End': today.strftime('%Y-%m-%d')},
            Granularity='MONTHLY',
            Metrics=['BlendedCost'],
            Filter={
                'And': [
                    {'Dimensions': {'Key': 'REGION', 'Values': self.eu_regions}},
                    {'Tags': {'Key': 'Project', 'Values': [project_tag]}}
                ]
            }
        )
        return round(sum(float(result['Total']['BlendedCost']['Amount']) for result in response['ResultsByTime']), 2)

    def _find_unattached_ebs_volumes(self) -> List[Dict]:
        """Find unattached EBS volumes across EU regions"""

        unattached_volumes = []

        for region in self.eu_regions:
            ec2_regional = boto3.client('ec2', region_name=region)
            response = ec2_regional.describe_volumes(
                Filters=[{'Name': 'status', 'Values': ['available']}]
            )

            for volume in response['Volumes']:
                # Calculate monthly cost based on volume size and type
                monthly_cost = self._calculate_ebs_monthly_cost(volume, region)

                unattached_volumes.append({
                    'volume_id': volume['VolumeId'],
                    'size_gb': volume['Size'],
                    'volume_type': volume['VolumeType'],
                    'region': region,
                    'estimated_monthly_savings_usd': monthly_cost,
                    'creation_date': volume['CreateTime'].isoformat()
                })

        return unattached_volumes

    def _find_unused_elastic_ips(self) -> List[Dict]:
        """Find allocated Elastic IPs that are not associated with any resource"""

        unused = []

        for region in self.eu_regions:
            ec2_regional = boto3.client('ec2', region_name=region)
            for address in ec2_regional.describe_addresses()['Addresses']:
                if 'AssociationId' not in address:
                    unused.append({
                        'allocation_id': address.get('AllocationId'),
                        'public_ip': address['PublicIp'],
                        'region': region,
                        # Public IPv4 addresses are billed per hour (USD 0.005/h ≈ USD 3.65/month)
                        'estimated_monthly_savings_usd': round(0.005 * 730, 2)
                    })

        return unused

    def _find_idle_load_balancers(self, days: int = 14) -> List[Dict]:
        """Find application load balancers without any requests over the look-back period"""

        idle = []
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)

        for region in self.eu_regions:
            elbv2 = boto3.client('elbv2', region_name=region)
            cloudwatch = boto3.client('cloudwatch', region_name=region)

            for load_balancer in elbv2.describe_load_balancers()['LoadBalancers']:
                if load_balancer['Type'] != 'application':
                    continue
                # The CloudWatch dimension is the ARN part after "loadbalancer/"
                dimension_value = load_balancer['LoadBalancerArn'].split('loadbalancer/')[1]
                statistics = cloudwatch.get_metric_statistics(
                    Namespace='AWS/ApplicationELB',
                    MetricName='RequestCount',
                    Dimensions=[{'Name': 'LoadBalancer', 'Value': dimension_value}],
                    StartTime=start_time,
                    EndTime=end_time,
                    Period=86400,
                    Statistics=['Sum']
                )
                if sum(point['Sum'] for point in statistics['Datapoints']) == 0:
                    idle.append({
                        'load_balancer': load_balancer['LoadBalancerName'],
                        'region': region,
                        # Representative hourly ALB charge in EU regions (USD 0.0252/h)
                        'estimated_monthly_savings_usd': round(0.0252 * 730, 2)
                    })

        return idle

    def _find_stopped_instances(self) -> List[Dict]:
        """Find stopped instances; their EBS volumes and Elastic IPs are still billed"""

        stopped = []

        for region in self.eu_regions:
            ec2_regional = boto3.client('ec2', region_name=region)
            paginator = ec2_regional.get_paginator('describe_instances')
            pages = paginator.paginate(Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])

            for page in pages:
                for reservation in page['Reservations']:
                    for instance in reservation['Instances']:
                        stopped.append({
                            'instance_id': instance['InstanceId'],
                            'instance_type': instance['InstanceType'],
                            'region': region,
                            'attached_volumes': [
                                mapping['Ebs']['VolumeId']
                                for mapping in instance.get('BlockDeviceMappings', []) if 'Ebs' in mapping
                            ],
                            'state_transition': instance.get('StateTransitionReason', '')
                        })

        return stopped

    def _analyze_reserved_instance_opportunities(self) -> List[Dict]:
        """Use Cost Explorer's reservation purchase recommendations for EC2"""

        response = self.cost_explorer.get_reservation_purchase_recommendation(
            Service='Amazon Elastic Compute Cloud - Compute',
            LookbackPeriodInDays='THIRTY_DAYS',
            TermInYears='ONE_YEAR',
            PaymentOption='NO_UPFRONT'
        )

        opportunities = []

        for recommendation in response.get('Recommendations', []):
            for detail in recommendation.get('RecommendationDetails', []):
                instance = detail.get('InstanceDetails', {}).get('EC2InstanceDetails', {})
                opportunities.append({
                    'instance_type': instance.get('InstanceType'),
                    'region': instance.get('Region'),
                    'recommended_instances': int(detail.get('RecommendedNumberOfInstancesToPurchase', 0)),
                    'estimated_monthly_savings_usd': float(detail.get('EstimatedMonthlySavingsAmount', 0))
                })

        return opportunities

    def _analyze_spot_instance_opportunities(self) -> Dict:
        """Estimate savings from moving instances tagged SpotEligible=true to Spot capacity"""

        candidates = []

        for region in self.eu_regions:
            ec2_regional = boto3.client('ec2', region_name=region)
            paginator = ec2_regional.get_paginator('describe_instances')
            pages = paginator.paginate(Filters=[
                {'Name': 'tag:SpotEligible', 'Values': ['true']},
                {'Name': 'instance-state-name', 'Values': ['running']}
            ])
            for page in pages:
                for reservation in page['Reservations']:
                    candidates.extend(reservation['Instances'])

        if not candidates:
            return {}

        # Heuristic, not an AWS API: Spot capacity is typically 60-90 % cheaper than
        # On-Demand. A conservative 60 % saving on a representative On-Demand rate
        # of USD 0.05/hour is assumed; replace with Pricing API data in production.
        on_demand_monthly_usd = len(candidates) * 0.05 * 730

        return {
            'eligible_instances': [instance['InstanceId'] for instance in candidates],
            'recommended_max_price': '0.05',  # cap Spot bids at the On-Demand price
            'estimated_monthly_savings_usd': round(on_demand_monthly_usd * 0.6, 2)
        }

    def _calculate_ebs_monthly_cost(self, volume: Dict, region: str) -> float:
        """Calculate monthly cost for EBS volume in specific EU region"""

        # Example pricing for EU regions (USD per GB/month)
        # Prices vary slightly by region - these are representative values
        regional_pricing = {
            'eu-west-1': {  # Ireland
                'gp3': 0.088,
                'gp2': 0.110,
                'io1': 0.138,
                'io2': 0.138,
                'st1': 0.048,
                'sc1': 0.026
            },
            'eu-central-1': {  # Frankfurt
                'gp3': 0.095,
                'gp2': 0.119,
                'io1': 0.149,
                'io2': 0.149,
                'st1': 0.052,
                'sc1': 0.028
            }
        }

        # Default to eu-west-1 pricing if region not found
        pricing = regional_pricing.get(region, regional_pricing['eu-west-1'])
        cost_per_gb = pricing.get(volume['VolumeType'], 0.110)  # Default to gp2
        return volume['Size'] * cost_per_gb

def generate_terraform_cost_optimizations(cost_plan: Dict) -> str:
    """Generate Terraform code to implement cost optimisations"""

    terraform_code = """
# Automatically generated cost optimisations
# Generated: {date}
# Project: {project}
# EU Regions: {regions}
# Potential monthly savings: ${savings:.2f} USD
# Note: Convert to EUR using current exchange rate for financial reporting

""".format(
        date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        project=cost_plan['project'],
        regions=', '.join(cost_plan.get('eu_regions_analysed', [])),
        savings=cost_plan['potential_monthly_savings_usd']
    )

    # Generate spot instance configurations. Every literal HCL brace must be
    # doubled ({{ }}) because the template is rendered with str.format.
    if cost_plan['recommendations']['spot_instances']:
        terraform_code += """
# Spot Instance Configuration for cost optimisation
resource "aws_launch_template" "spot_optimized" {{
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
      CostOptimisation = "spot-instance"
      EstimatedSavings = "${estimated_savings}"
    }}
  }}
}}
""".format(
            project=cost_plan['project'],
            max_spot_price=cost_plan['recommendations']['spot_instances'].get('recommended_max_price', '0.10'),
            estimated_savings=cost_plan['recommendations']['spot_instances'].get('estimated_monthly_savings_usd', 0)
        )

    return terraform_code
```

## Security and compliance {#security-compliance}

### 10_CODE_1: Advanced Policy-as-Code module for EU compliance {#10_code_1}
*Referenced from Chapter 10: [Policy and Security as Code in Detail](10_policy_and_security.md).* This Rego module consolidates encryption validation, network segmentation checks inspired by MSB guidance, and GDPR Article 44 data residency controls. It generates a composite compliance score so teams can fail builds or raise alerts when thresholds are breached. The module is written in OPA 1.0 syntax: since OPA 1.0 (December 2024) the `if` and `contains` keywords are mandatory in rule definitions, and `import rego.v1` keeps the module compatible with OPA 0.59 and later [Source [44]](33_references.md#source-44). Fall-back values are expressed with `default` functions, because a second definition that matched every input would conflict with the specific definitions at evaluation time.

```rego
package se.enterprise.security

import rego.v1

# Resource types that must encrypt data at rest and in transit
encryption_required_services := {
    "aws_s3_bucket",
    "aws_db_instance",
    "aws_rds_cluster",
    "aws_efs_file_system",
    "aws_dynamodb_table",
    "aws_redshift_cluster",
    "aws_elasticsearch_domain",
    "aws_opensearch_domain"
}

# Resource types that may hold personal data and are subject to residency checks
sovereignty_scoped_services := encryption_required_services

administrative_ports := {22, 3389, 5432, 3306, 1433, 27017, 6379, 9200, 5601}
allowed_public_ports := {80, 443}
eu_regions := {"eu-north-1", "eu-west-1", "eu-west-2", "eu-west-3", "eu-central-1", "eu-south-1"}

encryption_compliant contains resource if {
    resource := input.resources[_]
    resource.type in encryption_required_services
    encryption := get_encryption_status(resource)
    validation := validate_encryption_strength(encryption)
    validation.compliant
}

get_encryption_status(resource) := result if {
    resource.type == "aws_s3_bucket"
    result := {
        "at_rest": has_s3_encryption(resource),
        "in_transit": has_s3_ssl_policy(resource),
        "key_management": object.get(resource.attributes, "kms_key_type", "none")
    }
}

get_encryption_status(resource) := result if {
    resource.type != "aws_s3_bucket"
    result := {
        "at_rest": object.get(resource.attributes, "storage_encrypted", false),
        "in_transit": object.get(resource.attributes, "force_ssl", false),
        "key_management": object.get(resource.attributes, "kms_key_type", "none")
    }
}

default has_s3_encryption(_) := false

has_s3_encryption(resource) := true if {
    resource.attributes.server_side_encryption.enabled == true
}

default has_s3_ssl_policy(_) := false

has_s3_ssl_policy(resource) := true if {
    resource.attributes.enforce_tls == true
}

default validate_encryption_strength(_) := {
    "compliant": false,
    "strength": "none",
    "recommendations": ["Enable encryption at rest and enforce TLS in transit"]
}

validate_encryption_strength(encryption) := result if {
    encryption.at_rest == true
    encryption.in_transit == true
    key_validation := validate_key_management(encryption.key_management)
    result := {
        "compliant": key_validation.approved,
        "strength": key_validation.strength,
        "recommendations": key_validation.recommendations
    }
}

# "default" supplies the fall-back value. A catch-all definition such as
# validate_key_management(_) := {...} would match every input alongside the
# specific definitions and raise a conflict error at evaluation time.
default validate_key_management(_) := {
    "approved": false,
    "strength": "low",
    "recommendations": [
        "Configure an approved KMS key",
        "Document ownership within the OSCAL profile"
    ]
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

network_security_violations contains violation if {
    resource := input.resources[_]
    resource.type == "aws_security_group"
    some rule in resource.attributes.ingress
    "0.0.0.0/0" in rule.cidr_blocks
    violation := classify_exposure(resource, rule)
    violation.severity in {"critical", "high"}
}

# One call per ingress rule keeps the function single-valued; a function that
# iterated over all rules of a group would yield several outputs for the same
# input and fail with a conflict error.
classify_exposure(sg, rule) := violation if {
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

classify_exposure(sg, rule) := violation if {
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

data_sovereignty_compliant contains resource if {
    resource := input.resources[_]
    resource.type in sovereignty_scoped_services
    classification := determine_classification(resource)
    validate_region(resource, classification).compliant
}

# The DataClassification tag is authoritative; naming heuristics only apply
# when the tag is absent, so the definitions never produce conflicting values.
default determine_classification(_) := "internal"

determine_classification(resource) := classification if {
    classification := resource.attributes.tags.DataClassification
    classification != ""
}

determine_classification(resource) := "personal" if {
    not has_classification_tag(resource)
    personal_data_indicated(resource)
}

has_classification_tag(resource) if {
    resource.attributes.tags.DataClassification != ""
}

personal_data_indicated(resource) if {
    contains(lower(resource.attributes.name), "personal")
}

personal_data_indicated(resource) if {
    resource.type in {"aws_db_instance", "aws_rds_cluster"}
    some indicator in {"user", "customer", "gdpr", "pii"}
    contains(lower(resource.attributes.identifier), indicator)
}

validate_region(resource, classification) := result if {
    classification == "personal"
    result := {
        "compliant": region_is_eu(resource),
        "requirement": "GDPR Articles 44–49"
    }
}

validate_region(_, classification) := result if {
    classification != "personal"
    result := {
        "compliant": true,
        "requirement": "Internal data – EU residency not mandatory"
    }
}

default region_is_eu(_) := false

region_is_eu(resource) := true if {
    get_resource_region(resource) in eu_regions
}

default get_resource_region(_) := "unknown"

get_resource_region(resource) := region if {
    region := resource.attributes.region
    region != ""
}

get_resource_region(resource) := region if {
    not resource.attributes.region
    az := resource.attributes.availability_zone
    region := substring(az, 0, count(az) - 1)
}

compliance_assessment := result if {
    encryption_violations := [create_encryption_violation(resource) |
        some resource in input.resources
        resource.type in encryption_required_services
        not resource in encryption_compliant
    ]

    network_violations := [v | some v in network_security_violations]

    sovereignty_violations := [create_sovereignty_violation(resource) |
        some resource in input.resources
        resource.type in sovereignty_scoped_services
        not resource in data_sovereignty_compliant
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

create_encryption_violation(resource) := violation if {
    violation := {
        "type": "encryption_required",
        "severity": "critical",
        "resource": resource.type,
        "message": "Mandatory encryption is disabled",
        "remediation": "Enable encryption at rest and enforce TLS in transit",
        "reference": "GDPR Article 32"
    }
}

create_sovereignty_violation(resource) := violation if {
    violation := {
        "type": "data_sovereignty",
        "severity": "critical",
        "resource": resource.type,
        "message": sprintf("Personal data stored outside approved EU regions (%v)", [get_resource_region(resource)]),
        "remediation": "Move the workload to an EU region or document an adequacy decision",
        "reference": "GDPR Articles 44–49"
    }
}

calculate_score(violations) := score if {
    penalties := [severity_penalties[violation.severity] | some violation in violations]
    # max() takes a collection; there is no math.max built-in
    score := max([0, 100 - sum(penalties)])
}

severity_penalties := {
    "critical": 25,
    "high": 15,
    "medium": 10,
    "low": 5
}

assess_regulator(name, violations) := summary if {
    summary := {
        "name": name,
        "open_findings": count([v | some v in violations; contains(lower(v.reference), lower(name))])
    }
}
```

### 10_CODE_2: OSCAL profile for regulated financial services {#10_code_2}
*Referenced from Chapter 10.* This OSCAL profile merges controls from NIST SP 800-53 with GDPR Article 32 and MSB network segmentation expectations. Parameters clarify the encryption standard and key management practices adopted by the organisation. The `regional-catalog.json` import refers to the organisation's own OSCAL catalogue, which encodes the GDPR articles and the MSB guidance as controls (`gdpr-*`, `msb-*`) and is not reproduced here; control selections use glob patterns such as `ac-*`, not regular expressions.

```json
{
  "profile": {
    "uuid": "374b0628-2bd1-4392-8eb2-d22caf68ea36",
    "metadata": {
      "title": "Financial Institutions Security Profile",
      "published": "2024-01-15T11:00:00Z",
      "last-modified": "2024-01-15T11:00:00Z",
      "version": "2.1",
      "oscal-version": "1.1.2",
      "props": [
        { "name": "organization", "ns": "https://example.org/ns/architecture-as-code", "value": "Financial Sector" },
        { "name": "jurisdiction", "ns": "https://example.org/ns/architecture-as-code", "value": "EU" }
      ]
    },
    "imports": [
      {
        "href": "https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json",
        "include-controls": [
          { "matching": [ { "pattern": "ac-*" }, { "pattern": "au-*" }, { "pattern": "sc-*" } ] }
        ]
      },
      {
        "href": "regional-catalog.json",
        "include-controls": [
          { "matching": [ { "pattern": "gdpr-*" }, { "pattern": "msb-*" } ] }
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
                  "prose": "Payment service providers must use FIPS 140-3 validated cryptographic modules and review key material every 90 days."
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
*Referenced from Chapter 10.* Component definitions document how Terraform modules satisfy regulatory expectations. This example captures Amazon RDS, Amazon S3, and AWS Network Firewall implementations used throughout the financial profile. Every control implementation, implemented requirement and statement carries an RFC 4122 UUID as the OSCAL schema requires, the implementation status is recorded with the `implementation-status` property defined for the component model, and a `terraform-resource-type` property links each component to the Terraform resources it covers.

```json
{
  "component-definition": {
    "uuid": "5ac80bee-3d0f-47f6-b816-d55fbc5c9039",
    "metadata": {
      "title": "AWS Components for Regulated Workloads",
      "published": "2024-01-15T12:00:00Z",
      "last-modified": "2024-01-15T12:00:00Z",
      "version": "1.5",
      "oscal-version": "1.1.2"
    },
    "components": [
      {
        "uuid": "719170d2-ebec-4766-9d46-607f5ae81816",
        "type": "software",
        "title": "Amazon RDS MySQL",
        "description": "Managed relational database configured for GDPR Article 32 compliance.",
        "props": [
          { "name": "terraform-resource-type", "ns": "https://example.org/ns/architecture-as-code", "value": "aws_db_instance" }
        ],
        "control-implementations": [
          {
            "uuid": "1c662e9e-9134-4359-8f59-85005f543d99",
            "source": "regional-catalog.json",
            "description": "GDPR Article 32 and MSB segmentation controls satisfied by the RDS module.",
            "implemented-requirements": [
              {
                "uuid": "998cccd7-ab07-4b75-b444-627fba538160",
                "control-id": "gdpr-art32-1.1",
                "description": "Encryption at rest enabled with customer managed KMS keys.",
                "props": [
                  { "name": "implementation-status", "value": "implemented" },
                  { "name": "kms-key-type", "ns": "https://example.org/ns/architecture-as-code", "value": "customer-managed" },
                  { "name": "rotation", "ns": "https://example.org/ns/architecture-as-code", "value": "365 days" }
                ],
                "statements": [
                  {
                    "statement-id": "gdpr-art32-1.1_smt",
                    "uuid": "59e73e39-0efb-4493-bedc-70f6bca0611e",
                    "description": "Default encryption uses AES-256 with keys rotated every 365 days."
                  }
                ]
              },
              {
                "uuid": "c824abfc-246e-48e3-bf10-aef5b3b1819b",
                "control-id": "msb-3.2.1.1",
                "description": "Database subnet groups isolated from public subnets.",
                "props": [
                  { "name": "implementation-status", "value": "implemented" }
                ],
                "statements": [
                  {
                    "statement-id": "msb-3.2.1.1_smt",
                    "uuid": "d3db7e38-2a26-4e88-b319-eb6f0f089547",
                    "description": "Only application load balancers within the VPC may initiate connections."
                  }
                ]
              }
            ]
          }
        ]
      },
      {
        "uuid": "b164e25e-6622-48ef-9e5e-b8cc24ceb799",
        "type": "software",
        "title": "Amazon S3 Secure Bucket",
        "description": "Object storage with automatic encryption and access logging.",
        "props": [
          { "name": "terraform-resource-type", "ns": "https://example.org/ns/architecture-as-code", "value": "aws_s3_bucket" }
        ],
        "control-implementations": [
          {
            "uuid": "c50ab6e7-b57e-48a8-8715-56ad77048883",
            "source": "regional-catalog.json",
            "description": "Transport encryption and Zero Trust access controls provided by the S3 module.",
            "implemented-requirements": [
              {
                "uuid": "f0764ddb-6199-4674-9d7c-f6ab376174e2",
                "control-id": "gdpr-art32-1.2",
                "description": "Enforced TLS 1.2 for all data in transit.",
                "props": [
                  { "name": "implementation-status", "value": "implemented" }
                ],
                "statements": [
                  {
                    "statement-id": "gdpr-art32-1.2_smt",
                    "uuid": "6b55187a-91c7-4786-a4c5-f38973c84485",
                    "description": "S3 bucket policies block non-TLS requests and log denials."
                  }
                ]
              },
              {
                "uuid": "f6a0b7f2-c439-4a61-90f5-1458b56ef14f",
                "control-id": "msb-3.2.1.2",
                "description": "Zero Trust verification for access using IAM conditions.",
                "props": [
                  { "name": "implementation-status", "value": "planned" }
                ],
                "statements": [
                  {
                    "statement-id": "msb-3.2.1.2_smt",
                    "uuid": "28cc8f8f-79de-4c62-b01f-ef7f669d1ea3",
                    "description": "IAM policies require device posture attributes for privileged access."
                  }
                ]
              }
            ]
          }
        ]
      },
      {
        "uuid": "73bf97fd-af40-4371-a871-5d74429d1b15",
        "type": "software",
        "title": "AWS Network Firewall",
        "description": "Edge inspection enforcing MSB segmentation and logging requirements.",
        "props": [
          { "name": "terraform-resource-type", "ns": "https://example.org/ns/architecture-as-code", "value": "aws_networkfirewall_firewall" }
        ],
        "control-implementations": [
          {
            "uuid": "296a7ba0-1922-40d3-8b49-d2601cfe0bb2",
            "source": "regional-catalog.json",
            "description": "Network segmentation controls enforced at the inspection layer.",
            "implemented-requirements": [
              {
                "uuid": "f14faba2-f852-4aec-8079-58dcbc3f12c0",
                "control-id": "msb-3.2.1",
                "description": "Micro-segmentation between payment and support zones.",
                "props": [
                  { "name": "implementation-status", "value": "implemented" }
                ],
                "statements": [
                  {
                    "statement-id": "msb-3.2.1_smt",
                    "uuid": "5d6e6b2c-e415-4996-9104-39fe282d01b2",
                    "description": "Stateful rules restrict lateral movement and mirror traffic to a central collector."
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
*Referenced from Chapter 10.* This Python utility parses the Terraform configuration, matches the declared resource types with the component definitions through their `terraform-resource-type` property, and produces an OSCAL 1.1.2 System Security Plan with the mandatory system characteristics, system implementation and flattened control implementation. The script is designed to run inside CI so every deployment updates the compliance evidence set; validate the output with `oscal-cli validate` in the same pipeline.

```python
"""Generate OSCAL System Security Plans from Terraform configurations."""
from __future__ import annotations

import json
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List

import boto3
import hcl2

# Namespace for the organisation's own OSCAL properties (not NIST-defined names)
AAC_NS = "https://example.org/ns/architecture-as-code"


@dataclass
class ComponentDefinition:
    """Representation of an OSCAL component definition file."""

    path: Path
    content: Dict[str, Any]

    @property
    def components(self) -> List[Dict[str, Any]]:
        return self.content["component-definition"].get("components", [])


def implementation_state(requirement: Dict[str, Any]) -> str:
    """Read the implementation-status property of a component requirement."""
    for prop in requirement.get("props", []):
        if prop.get("name") == "implementation-status":
            return prop["value"]
    return "implemented"


class OSCALSSPGenerator:
    """Build an OSCAL 1.1.2 System Security Plan from source files."""

    def __init__(self, terraform_directory: Path, component_paths: Iterable[Path]):
        self.terraform_directory = terraform_directory
        self.component_paths = list(component_paths)
        self.sts = boto3.client("sts")

    def generate(self, profile_href: str, system_name: str) -> Dict[str, Any]:
        resource_types = self._parse_terraform()
        definitions = self._load_components()
        components = self._match_components(resource_types, definitions)

        now = datetime.now(timezone.utc).isoformat()
        return {
            "system-security-plan": {
                "uuid": str(uuid.uuid4()),
                "metadata": {
                    "title": f"System Security Plan – {system_name}",
                    "published": now,
                    "last-modified": now,
                    "version": "1.0",
                    "oscal-version": "1.1.2",
                    "roles": [{"id": "platform-engineer", "title": "Platform engineer"}],
                    "props": [
                        {"name": "organization", "ns": AAC_NS, "value": "Enterprise"},
                        {"name": "system-name", "ns": AAC_NS, "value": system_name}
                    ]
                },
                "import-profile": {"href": profile_href},
                "system-characteristics": {
                    # An AWS account ID is not an RFC 4122 UUID, so it is typed with the
                    # organisation's own identifier scheme instead
                    "system-ids": [{"identifier-type": AAC_NS, "id": f"aws-account-{self._account_id()}"}],
                    "system-name": system_name,
                    "description": f"Automated SSP generated from Terraform for {system_name}",
                    "security-sensitivity-level": "moderate",
                    "system-information": {
                        "information-types": [
                            {
                                "uuid": str(uuid.uuid4()),
                                "title": "Customer and payment data",
                                "description": "Personal data processed under GDPR Article 32 obligations."
                            }
                        ]
                    },
                    "status": {"state": "operational"},
                    "authorization-boundary": {
                        "description": "All AWS resources managed by the Terraform root module of this system."
                    }
                },
                "system-implementation": {
                    "users": [
                        {
                            "uuid": str(uuid.uuid4()),
                            "title": "Platform engineering team",
                            "role-ids": ["platform-engineer"]
                        }
                    ],
                    "components": [self._system_component(component) for component in components]
                },
                "control-implementation": {
                    "description": "Control implementations inherited from the matched component definitions.",
                    "implemented-requirements": self._implemented_requirements(components)
                }
            }
        }

    def _parse_terraform(self) -> List[str]:
        """Return the Terraform resource types declared in the configuration."""
        resource_types: List[str] = []
        for tf_file in sorted(self.terraform_directory.rglob("*.tf")):
            with tf_file.open("r", encoding="utf-8") as handle:
                data = hcl2.load(handle)
            for block in data.get("resource", []):
                resource_types.extend(block.keys())
        return resource_types

    def _load_components(self) -> List[ComponentDefinition]:
        definitions: List[ComponentDefinition] = []
        for path in self.component_paths:
            with path.open("r", encoding="utf-8") as handle:
                definitions.append(ComponentDefinition(path, json.load(handle)))
        return definitions

    @staticmethod
    def _resource_types(component: Dict[str, Any]) -> List[str]:
        """Terraform resource types covered by a component (prop terraform-resource-type)."""
        return [
            prop["value"] for prop in component.get("props", [])
            if prop.get("name") == "terraform-resource-type"
        ]

    def _match_components(
        self, resource_types: List[str], definitions: List[ComponentDefinition]
    ) -> List[Dict[str, Any]]:
        """Select the defined components whose resource types exist in the estate."""
        deployed = set(resource_types)
        return [
            component
            for definition in definitions
            for component in definition.components
            if deployed & set(self._resource_types(component))
        ]

    @staticmethod
    def _system_component(component: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "uuid": component["uuid"],
            "type": component["type"],
            "title": component["title"],
            "description": component["description"],
            "status": {"state": "operational"}
        }

    @staticmethod
    def _implemented_requirements(components: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Flatten component control implementations into SSP implemented requirements."""
        by_control: Dict[str, Dict[str, Any]] = {}
        for component in components:
            for implementation in component.get("control-implementations", []):
                for requirement in implementation.get("implemented-requirements", []):
                    entry = by_control.setdefault(requirement["control-id"], {
                        "uuid": str(uuid.uuid4()),
                        "control-id": requirement["control-id"],
                        "by-components": []
                    })
                    entry["by-components"].append({
                        "component-uuid": component["uuid"],
                        "uuid": str(uuid.uuid4()),
                        "description": requirement["description"],
                        "implementation-status": {"state": implementation_state(requirement)}
                    })
        return list(by_control.values())

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
        profile_href="profiles/financial-profile.json",
        system_name="Payments Platform"
    )
    save_ssp(Path("artifacts/system-security-plan.json"), plan)
```

## Structurizr workspace examples {#structurizr-workspaces}

The Structurizr DSL allows teams to create comprehensive, multi-view architecture descriptions in source control. This section collects reference workspaces that bring together people, systems, deployment topologies, and styling guidance in a single definition, demonstrating how to narrate complex platforms through Architecture as Code.

### 06_CODE_5: Real-world Structurizr workspace for a complete e-commerce platform {#06_code_5}
*Referenced from chapter 6: [Structurizr](06_structurizr.md)*

This workspace shows how to model a full retail platform using Structurizr, combining customer-facing applications, service layers, data stores, and deployment details. It highlights how tags, perspectives, and multiple views work together to explain the same system to different audiences.

```structurizr
workspace "E-Commerce Platform" "Complete architecture for online retail" {

    !docs docs
    !adrs adrs

    model {
        # People
        customer = person "Customer" "Online shopper"
        merchant = person "Merchant" "Seller managing products"
        admin = person "Administrator" "Platform operator"

        # External Systems
        paymentProvider = softwareSystem "Payment Provider" "Stripe/PayPal" {
            tags "External System"
        }

        emailService = softwareSystem "Email Service" "SendGrid" {
            tags "External System"
        }

        shippingCarrier = softwareSystem "Shipping Carrier" "FedEx/UPS API" {
            tags "External System"
        }

        # Main Platform
        ecommercePlatform = softwareSystem "E-Commerce Platform" {

            # Frontend Layer
            webApp = container "Web Application" "Customer-facing storefront" "React, Next.js" {
                tags "Frontend" "Critical Path"

                productCatalog = component "Product Catalog" "Browse and search products"
                shoppingCart = component "Shopping Cart" "Manage cart items"
                checkout = component "Checkout" "Order placement flow"
            }

            mobileApp = container "Mobile App" "iOS and Android apps" "React Native" {
                tags "Frontend" "Mobile"
            }

            adminPanel = container "Admin Panel" "Merchant and admin interface" "Vue.js" {
                tags "Frontend" "Internal"
            }

            # API Layer
            apiGateway = container "API Gateway" "Authenticates and routes requests" "Kong, Node.js" {
                tags "Infrastructure" "Critical Path"

                authMiddleware = component "Auth Middleware" "JWT validation"
                rateLimiter = component "Rate Limiter" "Throttles requests"
                router = component "Router" "Routes to services"
            }

            # Core Services
            group "Core Domain Services" {
                productService = container "Product Service" "Product catalog management" "Java, Spring Boot" {
                    tags "Microservice" "Core"

                    productController = component "Product Controller" "REST API"
                    productRepository = component "Product Repository" "Data access"
                    searchService = component "Search Service" "Elasticsearch integration"
                }

                orderService = container "Order Service" "Order lifecycle management" "Java, Spring Boot" {
                    tags "Microservice" "Core" "Critical Path"

                    orderController = component "Order Controller" "REST API"
                    orderRepository = component "Order Repository" "Data access"
                    orderStateMachine = component "Order State Machine" "Manages order states"
                    perspectives {
                        "Security" "PII data, requires encryption at rest"
                        "Compliance" "GDPR compliance, 30-day data retention"
                    }
                }

                inventoryService = container "Inventory Service" "Stock management" "Go" {
                    tags "Microservice" "Core"
                }

                userService = container "User Service" "User account management" "Node.js" {
                    tags "Microservice" "Core"
                }
            }

            # Supporting Services
            group "Supporting Services" {
                paymentService = container "Payment Service" "Payment processing" "Python, FastAPI" {
                    tags "Microservice" "PCI-DSS"
                    perspectives {
                        "Security" "PCI-DSS scope, no card data storage"
                        "Compliance" "PCI-DSS Level 1 certified"
                    }
                }

                notificationService = container "Notification Service" "Email and SMS notifications" "Python" {
                    tags "Microservice"
                }

                recommendationService = container "Recommendation Service" "Product recommendations" "Python, TensorFlow" {
                    tags "Microservice" "ML"
                }
            }

            # Data Layer
            group "Data Stores" {
                productDb = container "Product Database" "Product catalog data" "PostgreSQL" {
                    tags "Database" "Primary Storage"
                }

                orderDb = container "Order Database" "Order data" "PostgreSQL" {
                    tags "Database" "Primary Storage"
                }

                userDb = container "User Database" "User profiles and auth" "PostgreSQL" {
                    tags "Database" "Primary Storage"
                }

                searchIndex = container "Search Index" "Product search" "Elasticsearch" {
                    tags "Database" "Search"
                }

                cache = container "Cache" "Session and data cache" "Redis" {
                    tags "Database" "Cache"
                }
            }

            # Infrastructure
            messageBus = container "Message Bus" "Event-driven communication" "RabbitMQ" {
                tags "Infrastructure" "Messaging"
            }

            # Relationships - Frontend to Gateway
            webApp -> apiGateway "API calls" "HTTPS/JSON"
            mobileApp -> apiGateway "API calls" "HTTPS/JSON"
            adminPanel -> apiGateway "API calls" "HTTPS/JSON"

            # Relationships - Gateway to Services
            apiGateway -> productService "Routes /products/*" "HTTP/REST"
            apiGateway -> orderService "Routes /orders/*" "HTTP/REST"
            apiGateway -> userService "Routes /users/*" "HTTP/REST"

            # Relationships - Services to Databases
            productService -> productDb "Reads/writes" "JDBC"
            productService -> searchIndex "Indexes products" "HTTP"
            orderService -> orderDb "Reads/writes" "JDBC"
            userService -> userDb "Reads/writes" "JDBC"
            inventoryService -> productDb "Updates stock" "JDBC"

            # Relationships - Services to Cache
            productService -> cache "Caches products" "Redis Protocol"
            userService -> cache "Caches sessions" "Redis Protocol"

            # Relationships - Async via Message Bus
            orderService -> messageBus "Publishes OrderCreated" "AMQP"
            messageBus -> inventoryService "OrderCreated event" "AMQP"
            messageBus -> notificationService "OrderCreated event" "AMQP"
            paymentService -> messageBus "Publishes PaymentCompleted" "AMQP"
            messageBus -> paymentService "OrderCreated event" "AMQP"

            # Relationships - Supporting services to external systems
            # (dynamic views may only use relationships that exist in the model)
            paymentService -> paymentProvider "Charges cards" "HTTPS/REST"
            notificationService -> emailService "Sends emails" "HTTPS/REST"
        }

        # External Integrations
        ecommercePlatform -> paymentProvider "Processes payments" "HTTPS/REST"
        ecommercePlatform -> emailService "Sends emails" "HTTPS/REST"
        ecommercePlatform -> shippingCarrier "Creates shipments" "HTTPS/REST"
        emailService -> customer "Delivers confirmation emails" "SMTP"

        # User Interactions
        customer -> webApp "Browses and purchases"
        customer -> mobileApp "Browses and purchases"
        merchant -> adminPanel "Manages products"
        admin -> adminPanel "Platform administration"

        # Production Deployment
        deploymentEnvironment "Production" {
            deploymentNode "AWS Cloud" {
                tags "AWS"

                deploymentNode "CloudFront CDN" {
                    containerInstance webApp
                }

                deploymentNode "ECS Cluster" {
                    tags "Container Orchestration"

                    deploymentNode "API Gateway Tasks" {
                        containerInstance apiGateway
                    }

                    deploymentNode "Service Tasks" {
                        instances 3
                        containerInstance productService
                        containerInstance orderService
                        containerInstance userService
                        containerInstance inventoryService
                        containerInstance paymentService
                        containerInstance notificationService
                    }
                }

                deploymentNode "RDS" {
                    tags "Managed Database"

                    deploymentNode "Primary" {
                        containerInstance productDb
                        containerInstance orderDb
                        containerInstance userDb
                    }

                    deploymentNode "Read Replicas" {
                        instances 2
                        containerInstance productDb
                        containerInstance orderDb
                    }
                }

                deploymentNode "ElastiCache" {
                    containerInstance cache
                }

                deploymentNode "Elasticsearch Service" {
                    containerInstance searchIndex
                }

                deploymentNode "Amazon MQ" {
                    containerInstance messageBus
                }
            }
        }
    }

    views {
        # System Context
        systemContext ecommercePlatform "SystemContext" {
            include *
            autoLayout lr
            description "High-level view showing how the e-commerce platform fits in the ecosystem"
        }

        # Container View
        container ecommercePlatform "Containers" {
            include *
            autoLayout tb
            description "Container-level architecture showing major applications and data stores"
        }

        # Core Services Focus
        container ecommercePlatform "CoreServices" {
            include element.tag==Core
            include element.tag==Database
            include element.tag==Infrastructure
            autoLayout
            description "Focus on core domain services"
        }

        # Component View - Product Service
        component productService "ProductServiceComponents" {
            include *
            autoLayout
            description "Internal structure of Product Service"
        }

        # Component View - Order Service
        component orderService "OrderServiceComponents" {
            include *
            autoLayout
            description "Internal structure of Order Service"
        }

        # Dynamic View - Order Flow
        dynamic ecommercePlatform "OrderPlacementFlow" {
            title "Customer Order Placement"
            # Steps are numbered automatically; manual numbers would render as "1. 1. ..."

            customer -> webApp "Submits order"
            webApp -> apiGateway "POST /api/orders"
            apiGateway -> orderService "CreateOrder()"
            orderService -> orderDb "SaveOrder()"
            orderService -> messageBus "Publish OrderCreated"
            messageBus -> inventoryService "OrderCreated event"
            inventoryService -> productDb "Reserve items"
            messageBus -> paymentService "OrderCreated event"
            paymentService -> paymentProvider "Charge customer"
            paymentService -> messageBus "Publish PaymentCompleted"
            messageBus -> notificationService "PaymentCompleted event"
            notificationService -> emailService "Send confirmation"
            emailService -> customer "Confirmation email"

            autoLayout
            description "Sequence of events when customer places order"
        }

        # Deployment View
        deployment ecommercePlatform "Production" "ProductionDeployment" {
            include *
            autoLayout
            description "Production deployment on AWS"
        }

        # Filtered Views
        container ecommercePlatform "ExternalIntegrations" {
            include "element.tag==External System"
            include "->element.tag==External System->"
            autoLayout
            description "External system dependencies"
        }

        container ecommercePlatform "DataLayer" {
            include element.tag==Database
            include ->element.tag==Database->
            autoLayout
            description "Data storage architecture"
        }

        # Styling
        styles {
            element "Person" {
                shape person
                background #08427b
                colour #ffffff
                fontSize 22
            }

            element "Software System" {
                background #1168bd
                colour #ffffff
                shape roundedbox
            }

            element "External System" {
                background #999999
                colour #ffffff
            }

            element "Container" {
                background #438dd5
                colour #ffffff
                shape roundedbox
            }

            element "Component" {
                background #85bbf0
                colour #000000
                shape component
            }

            element "Database" {
                shape cylinder
                background #438dd5
            }

            element "Infrastructure" {
                shape hexagon
            }

            element "Frontend" {
                background #ff6b6b
            }

            element "Core" {
                background #51cf66
            }

            element "Critical Path" {
                border solid
                strokeWidth 4
            }

            relationship "Relationship" {
                thickness 2
                colour #707070
                routing orthogonal
                fontSize 12
            }
        }

        themes https://static.structurizr.com/themes/default/theme.json
    }

    configuration {
        scope softwaresystem
    }
}
```


## Sources

1. **HashiCorp.** *Terraform Language Documentation.* HashiCorp Developer Documentation. Available at: [https://developer.hashicorp.com/terraform/language](https://developer.hashicorp.com/terraform/language) [Source [140]](33_references.md#source-140)
2. **HashiCorp.** *Backend Type: s3.* HashiCorp Developer Documentation. Available at: [https://developer.hashicorp.com/terraform/language/backend/s3](https://developer.hashicorp.com/terraform/language/backend/s3) [Source [17]](33_references.md#source-17)
3. **Kubernetes Project (2024).** *Kubernetes Documentation: Concepts.* Kubernetes. [Source [13]](33_references.md#source-13)
4. **Structurizr.** *Structurizr DSL language reference.* Structurizr documentation. Available at: [https://docs.structurizr.com/dsl/language](https://docs.structurizr.com/dsl/language) [Source [38]](33_references.md#source-38)
5. **Open Policy Agent (2024).** *Policy as Code Overview.* CNCF OPA Project. [Source [10]](33_references.md#source-10)
6. **Open Policy Agent.** *OPA v1.0 upgrade guide.* Available at: [https://www.openpolicyagent.org/docs/v0-upgrade](https://www.openpolicyagent.org/docs/v0-upgrade) [Source [44]](33_references.md#source-44)
7. **DORA (2024).** *Accelerate State of DevOps Report 2024.* Google Cloud / DORA. Available at: [https://dora.dev/research/2024/dora-report/](https://dora.dev/research/2024/dora-report/) [Source [49]](33_references.md#source-49)
