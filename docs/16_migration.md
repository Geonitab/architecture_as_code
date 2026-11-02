# Migration from Traditional Infrastructure {#migration}

![Migration Process](images/diagram_18_chapter16.png)

*Figure 16.1: Migration from Traditional Infrastructure to Architecture as Code requires systematic planning, step-by-step Architecture as Code implementation and continuous validation. Diagram shows the structured process from assessment to complete Architecture as Code adoption.*

## Overall Description

Migration from traditional, manually configured infrastructure to Architecture as Code represents one of the most critical transformations for modern IT organisations. This process requires not only technical restructuring but also organisational change and cultural adaptation to code-based ways of working.

European organisations face unique migration challenges through legacy systems that have developed over decades, regulatory requirements that constrain the pace of change, and the need to balance innovation with operational stability. Successful migration requires comprehensive planning that minimises risks whilst enabling rapid value realisation.

Modern migration strategies must accommodate hybrid scenarios where legacy infrastructure coexists with Architecture as Code-managed resources during extended transition periods. This hybrid approach enables gradual migration that reduces business risk whilst enabling immediate benefits from Architecture as Code adoption.

Cloud-native migration pathways offer opportunities to modernise architecture whilst infrastructure management is codified. European companies can leverage this transformation to implement sustainability initiatives, improve cost efficiency and enhance security posture through systematic Architecture as Code adoption.

## Assessment and planning phases

Comprehensive infrastructure assessment forms the foundation for successful Architecture as Code migration. This includes inventory of existing resources, dependency mapping, risk assessment and cost-benefit analysis that informs migration strategy and timeline planning.

Discovery automation tools such as AWS Application Discovery Service, Azure Migrate and Google Cloud's migration tooling can accelerate the assessment process through automated resource inventory and dependency detection. Google Cloud's migration guidance makes assessment and discovery of the existing environment the first of its four migration phases ([Source [99]](33_references.md#source-99)), and Microsoft's Cloud Adoption Framework likewise builds its migration plan on a documented inventory of workloads and their dependencies ([Source [97]](33_references.md#source-97)). These tools generate data that can inform Architecture as Code template generation and migration prioritisation.

Risk assessment must identify critical systems, single points of failure and compliance dependencies that affect migration approach. European financial institutions and healthcare organisations must particularly consider regulatory implications and downtime restrictions that affect migration windows.

Migration wave planning balances technical dependencies with business priorities to minimise risk and maximise value realisation. Pilot projects with non-critical systems enable team learning and process refinement before critical systems migration commences.

## Lift-and-shift vs re-architecting

| Migration Strategy | Description | Benefits | Challenges | Best Suited For |
|-------------------|-------------|----------|------------|-----------------|
| Lift-and-shift | Direct migration to cloud with minimal changes | Fastest time to cloud, lower initial cost, minimal application changes | Limited cloud-native benefits, may require follow-up optimisation, higher long-term operational costs | Applications with tight timelines, limited modernisation budget, compliance-driven moves |
| Re-architecting | Complete redesign for cloud-native patterns | Maximum cloud value, improved scalability and resilience, cost optimisation, innovation enablement | Highest initial investment, longest timeline, requires deep cloud expertise | Strategic applications, high business value systems, global expansion needs |
| Lift-and-improve (Hybrid) | Selective re-architecting of critical components while keeping most unchanged | Balances speed-to-market with modernisation, immediate cloud benefits, iterative improvement path | Complexity in managing hybrid architecture, requires careful component selection | Phased modernisation, risk-balanced approach, majority of enterprise migrations |
| Application retirement | Remove legacy applications with limited business value | Reduces migration scope, eliminates maintenance costs, simplifies portfolio | Requires business stakeholder alignment, data archival strategy | Low-value legacy applications, redundant systems, end-of-life software |

## Gradual codification of infrastructure

Infrastructure inventory automation through tools such as Terraform `import` blocks, the CloudFormation IaC generator and resource import ([Source [96]](33_references.md#source-96)), and Azure Resource Manager template export enables systematic conversion of existing resources to Architecture as Code management. Automated discovery can generate initial Architecture as Code configurations that require refinement but accelerate the codification process.

Template standardisation through reusable modules and organisational patterns ensures consistency across migrated infrastructure whilst reducing future maintenance overhead. Public-sector organisations, where many departments provision similar workloads under the same regulatory regime, are natural candidates for standardised Architecture as Code templates covering common infrastructure patterns.

Configuration drift elimination through Architecture as Code adoption requires systematic reconciliation between existing resource configurations and desired Architecture as Code state. Gradual enforcement of Architecture as Code-managed configuration ensures infrastructure stability whilst eliminating manual configuration inconsistencies.

Version control integration for infrastructure changes enables systematic tracking of migration progress and provides rollback capabilities for problematic changes. Git-based workflows for infrastructure management establish the foundation for collaborative infrastructure development and operational transparency.

## Team transition and competence development

Skills development programmes must prepare traditional systems administrators and network engineers for Architecture as Code-based workflows. Training curricula should encompass Infrastructure as Code tools, cloud platforms, DevOps practices and automation scripting for comprehensive capability development.

Organisational structure evolution from traditional silos to cross-functional teams enables effective Architecture as Code adoption. Integrated DevOps teams that own Architecture as Code end to end replace the hand-offs between separate development and operations groups.

Cultural transformation from manual processes to automated workflows requires change management programmes that address resistance and promote automation adoption. Success stories from early adopters can motivate broader organisational acceptance of Architecture as Code practices.

Mentorship programmes pairing experienced cloud engineers with traditional infrastructure teams accelerates knowledge transfer and reduces adoption friction. External consulting support can supplement internal capabilities during initial migration phases for complex enterprise environments.

## Practical Examples

### Migration Assessment Automation

The comprehensive automation playbook for assessing unmanaged infrastructure resources and orchestrating their migration into a codified estate now resides in [Appendix D: Templates and Tools](appendix_templates_and_tools.md). Practitioners can reference the appendix for the full Python implementation, generated Terraform scaffolding, and migration playbook generator that support large-scale discovery and planning.

### CloudFormation Legacy Import

Importing existing resources into CloudFormation is a change-set operation of type `IMPORT`, not a `create-stack` call, which would create new resources instead. Every imported resource needs a `DeletionPolicy`, the operation may neither create nor delete resources, and the property values in the template must describe the existing configuration ([Source [96]](33_references.md#source-96)). The template below therefore declares the VPC, subnet, security group, and instance as imported resources and leaves hardening changes to a later stack update.

```yaml
# migration/legacy-import-template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Template for importing existing resources into CloudFormation management'

Parameters:
  Environment:
    Type: String
    Default: 'production'
    AllowedValues: ['development', 'staging', 'production']

  ProjectName:
    Type: String
    Description: 'Name of the project for resource tagging'

  ImportDate:
    Type: String
    Description: 'Date on which resources were imported into CloudFormation management (e.g. 2026-03-28)'

  ExistingImageId:
    Type: AWS::EC2::Image::Id
    Description: >-
      AMI of the existing instance. The value must match the running instance exactly:
      ImageId is a create-only property, so a different value would schedule a replacement
      at the next update. New instances created after the import should instead resolve the
      current Amazon Linux 2023 image through the public SSM parameter
      /aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64
      (parameter type AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>).

Resources:
  # Every imported resource carries DeletionPolicy: Retain so that the legacy estate
  # survives a stack deletion or a rolled-back import. Property values are recorded
  # as-is during the import; run drift detection afterwards and reconcile differences
  # (such as the governance tags below) with an ordinary stack update.
  ExistingVPC:
    Type: AWS::EC2::VPC
    DeletionPolicy: Retain
    Properties:
      # These values must match the existing VPC configuration exactly
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
        - Key: ImportDate
          Value: !Ref ImportDate

  ExistingSubnet:
    Type: AWS::EC2::Subnet
    DeletionPolicy: Retain
    Properties:
      # These values must match the existing subnet configuration exactly
      VpcId: !Ref ExistingVPC
      CidrBlock: '10.0.1.0/24'  # Update with actual subnet CIDR
      AvailabilityZone: 'eu-west-1a'  # Update with the subnet's actual Availability Zone
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

  ExistingSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    DeletionPolicy: Retain
    Properties:
      # Description and ingress rules must match the existing group exactly;
      # tighten the rules in a separate update once the import has completed
      GroupDescription: 'Legacy application security group'  # Update with the actual description
      VpcId: !Ref ExistingVPC
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 22
          ToPort: 22
          CidrIp: '10.0.0.0/8'
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

  ExistingInstance:
    Type: AWS::EC2::Instance
    DeletionPolicy: Retain
    Properties:
      # These values must match the existing instance configuration exactly
      InstanceType: 't3.medium'  # Update with actual instance type
      ImageId: !Ref ExistingImageId
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
        - Key: ImportDate
          Value: !Ref ImportDate

Outputs:
  ImportedVPCId:
    Description: 'ID of the imported VPC'
    Value: !Ref ExistingVPC
    Export:
      Name: !Sub '${AWS::StackName}-VPC-ID'

  ImportedInstanceId:
    Description: 'ID of the imported EC2 instance'
    Value: !Ref ExistingInstance
    Export:
      Name: !Sub '${AWS::StackName}-Instance-ID'
```

The identifiers of the existing resources are supplied separately. Each entry names the resource type, the logical ID used in the template, and the resource's primary identifier as defined in the CloudFormation registry schema (`VpcId`, `SubnetId`, `Id` for security groups, and `InstanceId`):

```json
[
  {
    "ResourceType": "AWS::EC2::VPC",
    "LogicalResourceId": "ExistingVPC",
    "ResourceIdentifier": { "VpcId": "vpc-0123456789abcdef0" }
  },
  {
    "ResourceType": "AWS::EC2::Subnet",
    "LogicalResourceId": "ExistingSubnet",
    "ResourceIdentifier": { "SubnetId": "subnet-0123456789abcdef0" }
  },
  {
    "ResourceType": "AWS::EC2::SecurityGroup",
    "LogicalResourceId": "ExistingSecurityGroup",
    "ResourceIdentifier": { "Id": "sg-0123456789abcdef0" }
  },
  {
    "ResourceType": "AWS::EC2::Instance",
    "LogicalResourceId": "ExistingInstance",
    "ResourceIdentifier": { "InstanceId": "i-0123456789abcdef0" }
  }
]
```

The import itself is a reviewed change set followed by drift detection, so that the template is proven to describe reality before any further update touches the resources:

```bash
# migration/import-legacy-resources.sh
PROJECT_NAME=${1:?project name required}
EXISTING_AMI_ID=${2:?AMI ID of the existing instance required}

# 1. Validate the template and create an IMPORT change set
aws cloudformation validate-template --template-body file://legacy-import-template.yaml
aws cloudformation create-change-set \
  --stack-name "${PROJECT_NAME}-import" \
  --change-set-name legacy-import \
  --change-set-type IMPORT \
  --template-body file://legacy-import-template.yaml \
  --resources-to-import file://resources-to-import.json \
  --parameters ParameterKey=ProjectName,ParameterValue="${PROJECT_NAME}" \
               ParameterKey=ImportDate,ParameterValue="$(date -u +%Y-%m-%d)" \
               ParameterKey=ExistingImageId,ParameterValue="${EXISTING_AMI_ID}"
aws cloudformation wait change-set-create-complete \
  --stack-name "${PROJECT_NAME}-import" --change-set-name legacy-import

# 2. Review the planned import, then execute it
aws cloudformation describe-change-set \
  --stack-name "${PROJECT_NAME}-import" --change-set-name legacy-import
aws cloudformation execute-change-set \
  --stack-name "${PROJECT_NAME}-import" --change-set-name legacy-import
aws cloudformation wait stack-import-complete --stack-name "${PROJECT_NAME}-import"

# 3. Confirm that the template matches the live configuration (detection is asynchronous)
DRIFT_ID=$(aws cloudformation detect-stack-drift \
  --stack-name "${PROJECT_NAME}-import" --query StackDriftDetectionId --output text)
aws cloudformation describe-stack-drift-detection-status --stack-drift-detection-id "$DRIFT_ID"
aws cloudformation describe-stack-resource-drifts --stack-name "${PROJECT_NAME}-import"
```

### Migration Testing Framework  
```bash
#!/bin/bash
# migration/test-migration.sh
# Comprehensive testing script for Architecture as Code migration validation

set -e

PROJECT_NAME=${1:-"migration-test"}
ENVIRONMENT=${2:-"staging"}
REGION=${3:-"eu-west-1"}

echo "Starting Architecture as Code migration testing for project: $PROJECT_NAME"
echo "Environment: $ENVIRONMENT"
echo "Region: $REGION"

# Pre-migration testing
echo "=== Pre-Migration Tests ==="

# Test 1: Verify that all resources are inventoried
echo "Testing resource inventory..."
aws ec2 describe-instances --region $REGION --query 'Reservations[*].Instances[?State.Name!=`terminated`]' > /tmp/pre-migration-instances.json
aws rds describe-db-instances --region $REGION > /tmp/pre-migration-rds.json

INSTANCE_COUNT=$(jq '[.[] | length] | add // 0' /tmp/pre-migration-instances.json)
RDS_COUNT=$(jq '.DBInstances | length' /tmp/pre-migration-rds.json)

echo "Discovered $INSTANCE_COUNT EC2 instances and $RDS_COUNT RDS instances"

# Test 2: Backup verification
echo "Verifying backup status..."
SNAPSHOT_SINCE=$(date -u -d '7 days ago' +%Y-%m-%dT%H:%M:%S.000Z)  # "recent" means within the last week
aws ec2 describe-snapshots --region "$REGION" --owner-ids self --query "Snapshots[?StartTime>=\`${SNAPSHOT_SINCE}\`]" > /tmp/recent-snapshots.json
SNAPSHOT_COUNT=$(jq 'length' /tmp/recent-snapshots.json)

if [ "$SNAPSHOT_COUNT" -lt "$INSTANCE_COUNT" ]; then
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
    
    # Validate import using Terraform 1.5+ import blocks:
    # Declare an import block in your configuration, then run:
    #   terraform plan
    # This previews the import without making changes.
    echo "To validate import for $SAMPLE_INSTANCE_ID, declare an import block and run: terraform plan"
fi

# Post-migration testing
echo "=== Post-Migration Validation Framework ==="

# Test 6: Infrastructure compliance
echo "Setting up compliance validation..."
cat > /tmp/compliance-test.py << 'EOF'
import boto3
import json

def validate_tagging_compliance(region='eu-west-1'):
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

def validate_security_compliance(resource):
    """Validate security configuration after migration"""
    # Illustrative stub: replace with actual compliance checks
    # e.g., using Checkov, Trivy, or custom policy rules
    raise NotImplementedError("Implement compliance validation for your environment")

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
# Usage: performance-monitor.sh <instance-id> [region]
set -euo pipefail

INSTANCE_ID=${1:?usage: performance-monitor.sh <instance-id> [region]}
REGION=${2:-eu-west-1}
METRICS_FILE="/tmp/post-migration-metrics.json"

echo "Collecting post-migration performance metrics for $INSTANCE_ID..."

# CPU utilisation for one instance. Basic monitoring publishes 5-minute datapoints,
# so --period 300 works without detailed monitoring; the InstanceId dimension is
# required because aggregate statistics only cover instances with detailed monitoring.
aws cloudwatch get-metric-statistics \
    --namespace AWS/EC2 \
    --metric-name CPUUtilization \
    --dimensions Name=InstanceId,Value="$INSTANCE_ID" \
    --start-time "$(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S)" \
    --end-time "$(date -u +%Y-%m-%dT%H:%M:%S)" \
    --period 300 \
    --statistics Average \
    --region "$REGION" > "$METRICS_FILE"

# Analyse metrics for deviations; guard against an empty result set
AVERAGE_CPU=$(jq -r '[.Datapoints[].Average] | if length > 0 then (add / length) else "none" end' "$METRICS_FILE")

if [ "$AVERAGE_CPU" = "none" ]; then
    echo "No CPUUtilization datapoints returned for $INSTANCE_ID in the last hour"
    exit 0
fi

echo "Average CPU utilisation: $AVERAGE_CPU%"

if (( $(echo "$AVERAGE_CPU > 80" | bc -l) )); then
    echo "WARNING: High CPU utilisation detected after migration"
fi
EOF

chmod +x /tmp/performance-monitor.sh

if [ -n "$SAMPLE_INSTANCE_ID" ] && [ "$SAMPLE_INSTANCE_ID" != "null" ]; then
    /tmp/performance-monitor.sh "$SAMPLE_INSTANCE_ID" "$REGION"
fi

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
echo "5. Document lessons learned"
```

## Summary

Migration is rarely a single project; it is a sequence of small, reversible steps, each of which shrinks the part of the estate that is still managed by hand. Migration from traditional infrastructure to Architecture as Code requires systematic planning, gradual implementation, and comprehensive testing. Organisations that successfully execute this migration position themselves for increased agility, improved security, and significant cost benefits.

Success factors include comprehensive assessment, realistic timeline planning, extensive team training, and robust testing frameworks. Hybrid migration strategies enable risk minimisation whilst delivering immediate value from Architecture as Code adoption.

Investment in proper migration planning and execution results in long-term benefits through improved operational efficiency, enhanced security posture, and reduced technical debt. Organisations that follow systematic migration approaches can expect successful transformation to modern, Architecture as Code-based infrastructure management.

## Bridging Technical and Organisational Change

Technical migration success depends fundamentally on organisational readiness. The most sophisticated automation pipelines, testing frameworks, and migration strategies fail without the cultural foundations, team structures, and leadership practices that enable people to thrive in code-based delivery environments.

Part E examines the organisational transformation that must accompany technical change. [Chapter 17 on Organisational Change](17_organisational_change.md) explores how teams evolve from siloed functions to cross-functional collaboration. [Chapter 18 on Team Structure](18_team_structure.md) provides concrete patterns for organising teams around Architecture as Code practices. The subsequent chapters demonstrate how management practices, the interplay between the soft as code disciplines, AI-enabled collaboration, and digitalisation strategies complete the transformation from traditional to code-centric operating models.

## Sources

1. **Amazon Web Services.** *Import AWS resources into a CloudFormation stack.* AWS CloudFormation User Guide, [https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/resource-import.html](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/resource-import.html) (accessed 2026-10-30). [Source [96]](33_references.md#source-96)
2. **Microsoft Learn (2025).** *Plan your migration.* Cloud Adoption Framework for Azure (Migrate), 1 August 2025, [https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/migrate/plan-migration](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/migrate/plan-migration). [Source [97]](33_references.md#source-97)
3. **Google Cloud (2024).** *Migrate to Google Cloud: Get started.* Cloud Architecture Center, last reviewed 20 November 2024, [https://docs.cloud.google.com/architecture/migration-to-gcp-getting-started](https://docs.cloud.google.com/architecture/migration-to-gcp-getting-started). [Source [99]](33_references.md#source-99)
