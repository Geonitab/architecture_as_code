# Migration from Traditional Infrastructure

![Migrationsprocess](images/diagram_18_kapitel17.png)

*Migration from Traditional Infrastructure to Architecture as Code (Architecture as Code) requires systematic planering, stegvis Architecture as Code-implementation and continuous validation. Diagram shows The Structureerade processen from assessment to complete Architecture as Code-adoption.*

## Overall Description

Migration from traditional, manuellt konfigurerad infrastructure to Architecture as Code represents a of the most critical transformationerna for modern IT-organisationer. This process requires not endast technical omStructureering without also organisatorisk change and cultural anpassning to code-based way of working.

European organisations face unique migreringsChallenges through legacy-systems as developed over decennier, regulatory requirements as begränsar forändringstakt, and need of to balance innovation with operational stability. Successful migration requires comprehensive planning as minimizes risker while The enables snabb value realization.

Modern migrationsstrategier must accommodera hybrid scenarios where legacy infrastructure coexisterar with Architecture as Code-managed resources under extended transition periods. This hybrid approach enables gradual migration as reduces business risk while the enables imwithiate benefits from Architecture as Code adoption.

Cloud-native migration pathways offers opportuniteter to modernisera architecture while infrastructure management are codified. European companies can leverage This transformation to implement sustainability initiatives, improve cost efficiency and enhance security posture through systematic Architecture as Code adoption.

## Assessment and planning faser

Comprehensive infrastructure assessment forms foundationen for successful Architecture as Code migration. This includes inventory of existing resources, dependency mapping, risk assessment and cost-benefit analysis as informerar migration strategy and timeline planning.

Discovery automation tools that AWS Application Discovery Service, Azure Migrate and Google Cloud migration tools can accelerate assessment processen through automated resource inventory and dependency detection. These tools genererar data as can inform Architecture as Code template generation and migration prioritization.

Risk assessment must identify critical systems, single points of failure and compliance dependencies as affects migration approach. European financial institutions and healthcare organisations must particularly consider regulatory implications and downtime restrictions as affects migration windows.

Migration wave planning balancerar technical dependencies with business priorities to minimize risk and maximize value realization. Pilot projects with non-critical systems enables team learning and process refinement before critical systems migration påbörjas.

## Lift-and-shift vs re-architecting

| Migration Strategy | Description | Benefits | Challenges | Best Suited For |
|-------------------|-------------|----------|------------|-----------------|
| Lift-and-shift | Direct migration to cloud with minimal changes | Fastest time to cloud, lower initial cost, minimal application changes | Limited cloud-native benefits, may require follow-up optimisation, higher long-term operational costs | Applications with tight timelines, limited modernisation budget, compliance-driven moves |
| Re-architecting | Complete redesign for cloud-native patterns | Maximum cloud value, improved scalability and resilience, cost optimisation, innovation enablement | Highest initial investment, longest timeline, requires deep cloud expertise | Strategic applications, high business value systems, global expansion needs |
| Lift-and-improve (Hybrid) | Selective re-architecting of critical components while keeping most unchanged | Balances speed-to-market with modernisation, immediate cloud benefits, iterative improvement path | Complexity in managing hybrid architecture, requires careful component selection | Phased modernisation, risk-balanced approach, majority of enterprise migrations |
| Application retirement | Remove legacy applications with limited business value | Reduces migration scope, eliminates maintenance costs, simplifies portfolio | Requires business stakeholder alignment, data archival strategy | Low-value legacy applications, redundant systems, end-of-life software |

## Gradual kodifiering of infrastruktur

Infrastructure inventory automation through tools that Terraform import, CloudFormation drift detection and Azure Resource Manager templates enables systematic conversion of existing resources to Architecture as Code management. Automated discovery can generate initial Architecture as Code configurations as require refinement but accelerate kodification process.

Template standardisation through reusable modules and organisational patterns ensures consistency across migrated infrastructure while the reduces future maintenance overhead. European government agencies have successfully implemented standardized Architecture as Code templates for common infrastructure patterns across different departments.

Configuration drift elimination through Architecture as Code adoption requires systematic reconciliation between existing resource configurations and desired Architecture as Code state. Gradual enforcement of Architecture as Code-managed configuration ensures infrastructure stability while the eliminates manual configuration inconsistencies.

Version control integration for infrastructure changes enables systematic tracking of migration progress samt provides rollback capabilities for problematic changes. Git-based workflows for infrastructure management etablishes foundation for collaborative infrastructure development and operational transparency.

## Team transition and competence development

Skills development programs must prepare traditional systems administrators and network engineers for Architecture as Code-based workflows. Training curricula should encompass Infrastructure as Code tools, cloud platforms, DevOps practices and automation scripting for comprehensive capability development.

Organisational structure evolution from traditional silos to cross-functional teams enables effective Architecture as Code adoption. European telecommunications companies have successfully transitioned from separate development and operations teams to integrated DevOps teams as manage architecture as code.

Cultural transformation from manual processes to automated workflows requires change management programs as address resistance and promotes automation adoption. Success stories from early adopters can motivate broader organisational acceptance of Architecture as Code practices.

Mentorship programs pairing experienced cloud engineers with traditional infrastructure teams accelerates knowledge transfer and reduces adoption friction. External consulting support can supplement internal capabilities during initial migration phases for complex enterprise environments.

## Praktiska example

### Migration Assessment Automation
```python
# migration_assessment/infrastructure_discovery.py
import boto3
import json
from datetime import datetime
from typing import Dict, List
import pandas as pd

class InfrastructureMigrationAssessment:
    """
    Automatiserad bedömning of existing infrastruktur for architecture as code-migration
    """
    
    def __init__(self, region='eu-west-1'):
        self.ec2 = boto3.client('ec2', region_name=region)
        self.rds = boto3.client('rds', region_name=region)
        self.elb = boto3.client('elbv2', region_name=region)
        self.cloudformation = boto3.client('cloudformation', region_name=region)
        
    def discover_unmanaged_resources(self) -> Dict:
        """Upptäck resurser as not is managed of architecture as code"""
        
        unmanaged_resources = {
            'ec2_instances': self._find_unmanaged_ec2(),
            'rds_instances': self._find_unmanaged_rds(),
            'load_balancers': self._find_unmanaged_load_balancers(),
            'security_groups': self._find_unmanaged_security_groups(),
            'summary': {}
        }
        
        # Beräkna summary statistics
        total_resources = sum(len(resources) for resources in unmanaged_resources.values() if isinstance(resources, list))
        unmanaged_resources['summary'] = {
            'total_unmanaged_resources': total_resources,
            'migration_complexity': self._assess_migration_complexity(unmanaged_resources),
            'estimated_migration_effort': self._estimate_migration_effort(total_resources),
            'risk_assessment': self._assess_migration_risks(unmanaged_resources)
        }
        
        return unmanaged_resources
    
    def _find_unmanaged_ec2(self) -> List[Dict]:
        """Hitta EC2-instanser as not is managed of CloudFormation/Terraform"""
        
        # Hämta all EC2-instanser
        response = self.ec2.describe_instances()
        unmanaged_instances = []
        
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                if instance['State']['Name'] != 'terminated':
                    # Kontrollera about instansen is managed of architecture as code
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
        """Kontrollera about resurs is managed of architecture as code"""
        
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
        """Generera Terraform-code for migration of unmanaged resources"""
        
        terraform_code = """
# automatically genererad migration plan
# Genererat: {date}
# Totalt antal resurser to migrera: {total_resources}

terraform {{
  required_providers {{
    aws = {{
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }}
  }}
}}

provider "aws" {{
  region = "eu-west-1"  # Configurable for any EU region
}}

""".format(
            date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            total_resources=len(unmanaged_resources.get('ec2_instances', []))
        )
        
        # Generera Terraform for EC2-instanser
        for in, instance in enumerate(unmanaged_resources.get('ec2_instances', [])):
            terraform_code += f"""
# Migration of existing EC2-instans {instance['instance_id']}
resource "aws_instance" "migrated_instance_{in}" {{
  # OBSERVERA: This configuration must verifieras and adapted
  instance_type = "{instance['instance_type']}"
  subnet_id     = "{instance['subnet_id']}"
  
  vpc_security_group_ids = {json.dumps(instance['security_groups'])}
  
  # Behåll existing tags and lägg to migration-info
  tags = {{
    Name = "{instance.get('tags', {}).get('Name', f'migrated-instance-{in}')}"
    MigratedFrom = "{instance['instance_id']}"
    MigrationDate = "{datetime.now().strftime('%Y-%m-%d')}"
    ManagedBy = "terraform"
    Environment = "{instance.get('tags', {}).get('Environment', 'production')}"
    Project = "{instance.get('tags', {}).get('Project', 'migration-project')}"
  }}
  
  # VIKTIGT: Importera existing resurs instead of create new
  # terraform import aws_instance.migrated_instance_{in} {instance['instance_id']}
}}
"""
        
        terraform_code += """
# Migration checklist:
# 1. Granska genererade configurations noggrant
# 2. Testa in development-environment first  
# 3. Importera existing resurser with terraform import
# 4. Kör terraform plan to verifiera to inga changes planeras
# 5. Implementera gradual with låg-risk resurser first
# 6. Uppdatera monitoring and alerting efter migration
"""
        
        return terraform_code
    
    def create_migration_timeline(self, unmanaged_resources: Dict) -> Dict:
        """Skapa realistisk migrationstidplan"""
        
        # Kategorisera resurser efter komplexitet
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
        
        # Beräkna tidsestimater
        timeline = {
            'wave_1_low_risk': {
                'resources': low_complexity,
                'estimated_duration': f"{len(low_complexity) * 2} dagar",
                'start_date': 'Vecka 1-2',
                'prerequisites': ['architecture as code training completion', 'Tool setup', 'Backup verification']
            },
            'wave_2_medium_risk': {
                'resources': medium_complexity,
                'estimated_duration': f"{len(medium_complexity) * 4} dagar", 
                'start_date': 'Vecka 3-6',
                'prerequisites': ['Wave 1 completion', 'Process refinement', 'Team feedback']
            },
            'wave_3_high_risk': {
                'resources': high_complexity,
                'estimated_duration': f"{len(high_complexity) * 8} dagar",
                'start_date': 'Vecka 7-12',
                'prerequisites': ['Wave 2 completion', 'Advanced training', 'Stakeholder approval']
            },
            'total_estimated_duration': f"{(len(low_complexity) * 2) + (len(medium_complexity) * 4) + (len(high_complexity) * 8)} dagar"
        }
        
        return timeline

def generate_migration_playbook(assessment_results: Dict) -> str:
    """Generera comprehensive migration playbook for European organizations"""
    
    playbook = f"""
# architecture as code Migration Playbook for {assessment_results.get('organization_name', 'Organization')}

## Executive Summary
- **Totalt antal resurser to migrera:** {assessment_results['summary']['total_unmanaged_resources']}
- **Migrations-komplexitet:** {assessment_results['summary']['migration_complexity']}
- **Estimerad effort:** {assessment_results['summary']['estimated_migration_effort']}
- **Risk-bedömning:** {assessment_results['summary']['risk_assessment']}

## Fas 1: Förberedelse (Vecka 1-2)

### Team Training
- [ ] architecture as code grundutbildning for all teammedlemmar
- [ ] Terraform/CloudFormation hands-on workshops
- [ ] Git workflows for infrastructure management
- [ ] EU compliance-requirements (GDPR, data sovereignty)

### Tool Setup
- [ ] Terraform/CloudFormation development environment
- [ ] Git repository for infrastructure code
- [ ] CI/CD pipeline for infrastructure deployment
- [ ] Monitoring and alerting configuration

### Risk Mitigation
- [ ] Fullständig backup of all critical systems
- [ ] Rollback procedures documentserade
- [ ] Emergency contacts and eskalationsplan
- [ ] Test environment for migration validation

## Fas 2: Pilot Migration (Vecka 3-4)

### Low-Risk Resources Migration
- [ ] Migrera development/test environments first
- [ ] Validate architecture as code templates and processes
- [ ] Dokumentera lessons learned
- [ ] Refinera migration procedures

### Quality Gates
- [ ] Automated testing of migrerade resurser
- [ ] Performance verification
- [ ] Security compliance validation
- [ ] Cost optimization review

## Fas 3: Production Migration (Vecka 5-12)

### Gradual Production Migration
- [ ] Non-critical production systems
- [ ] Critical systems with planerade maintenance windows
- [ ] Database migration with minimal downtime
- [ ] Network infrastructure migration

### Continuous Monitoring
- [ ] Real-time monitoring of migrerade systems
- [ ] Automated alerting for anomalier
- [ ] Performance benchmarking
- [ ] Cost tracking and optimization

## Post-Migration Activities

### Process Optimization
- [ ] Infrastructure cost review and optimization
- [ ] Team workflow refinement
- [ ] Documentation and knowledge transfer
- [ ] Continuous improvement architecture as code-implementation

### Long-term Sustainability
- [ ] Regular architecture as code architecture as code best practices review
- [ ] Team cross-training program
- [ ] Tool evaluation and updates
- [ ] Compliance monitoring automation

## EU Compliance Considerations

### GDPR Requirements
- [ ] Data residency in EU regioner
- [ ] Encryption at rest and in transit
- [ ] Access logging and audit trails
- [ ] Data retention policy implementation

### EU Security Requirements
- [ ] Network segmentation implementation
- [ ] Incident response procedures
- [ ] Backup and disaster recovery
- [ ] Security monitoring enhancement

## Success Metrics

### Technical Metrics
- Infrastructure deployment time reduction: Target 80%
- Configuration drift incidents: Target 0
- Security compliance score: Target 95%+
- Infrastructure cost optimization: Target 20% reduction

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

### CloudFormation Legacy Import
```yaml
# migration/legacy-import-template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Template for import of existing resurser to CloudFormation management'

Parameters:
  ExistingVPCId:
    Type: String
    Description: 'ID for existing VPC as should importeras'
    
  ExistingInstanceId:
    Type: String  
    Description: 'ID for existing EC2-instans as should importeras'
    
  Environment:
    Type: String
    Default: 'production'
    AllowedValues: ['development', 'staging', 'production']
    
  ProjectName:
    Type: String
    Description: 'Namn at projektet for resource tagging'

Resources:
  # Import of existing VPC
  ExistingVPC:
    Type: AWS::EC2::VPC
    Properties:
      # These värden must matcha existing VPC-configuration exakt
      CidrBlock: '10.0.0.0/16'  # Uppdatera with faktiskt CIDR
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

  # Import of existing EC2-instans
  ExistingInstance:
    Type: AWS::EC2::Instance
    Properties:
      # These värden must matcha existing instans-configuration
      InstanceType: 't3.medium'  # Uppdatera with actual instance type
      ImageId: 'ami-0c94855bb95b03c2e'  # Uppdatera with actual AMI
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

  # Security group for importerad instans
  ExistingSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: 'Imported security group for legacy systems'
      VpcId: !Ref ExistingVPC
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 22
          ToPort: 22
          CidrIp: '10.0.0.0/8'  # Begränsa SSH access
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

  # Subnet for organiserad nätverkshantering
  ExistingSubnet:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref ExistingVPC
      CidrBlock: '10.0.1.0/24'  # Uppdatera with faktiskt subnet CIDR
      AvailabilityZone: !Select [0, !GetAZs '']  # First available AZ in selected region
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
    Description: 'ID for importerad VPC'
    Value: !Ref ExistingVPC
    Export:
      Name: !Sub '${AWS::StackName}-VPC-ID'
      
  ImportedInstanceId:
    Description: 'ID for importerad EC2-instans'
    Value: !Ref ExistingInstance
    Export:
      Name: !Sub '${AWS::StackName}-Instance-ID'
      
  ImportInstructions:
    Description: 'Instruktioner for resource import'
    Value: !Sub |
      to importera existing resurser:
      1. aws cloudformation create-stack --stack-name ${ProjectName}-import --template-body file://legacy-import-template.yaml
      2. aws cloudformation import-resources-to-stack --stack-name ${ProjectName}-import --resources file://import-resources.json
      3. Verifiera to import var successful with: aws cloudformation describe-stacks --stack-name ${ProjectName}-import
```

### Migration Testing Framework  
```bash
#!/bin/bash
# migration/test-migration.sh
# Comprehensive testing script for architecture as code migration validation

set -e

PROJECT_NAME=${1:-"migration-test"}
ENVIRONMENT=${2:-"staging"}
REGION=${3:-"eu-west-1"}

echo "Starting architecture as code migration testing for projekt: $PROJECT_NAME"
echo "Environment: $ENVIRONMENT"
echo "Region: $REGION"

# Pre-migration testing
echo "=== Pre-Migration Tests ==="

# Test 1: Verifiera to all resurser is inventerade
echo "Testing resource inventory..."
aws ec2 describe-instances --region $REGION --query 'Reservations[*].Instances[?State.Name!=`terminated`]' > /tmp/pre-migration-instances.json
aws rds describe-db-instances --region $REGION > /tmp/pre-migration-rds.json

INSTANCE_COUNT=$(jq '.[] | length' /tmp/pre-migration-instances.json | jq -s 'add')
RDS_COUNT=$(jq '.DBInstances | length' /tmp/pre-migration-rds.json)

echo "Upptäckte $INSTANCE_COUNT EC2-instanser and $RDS_COUNT RDS-instanser"

# Test 2: Backup verification
echo "Verifying backup status..."
aws ec2 describe-snapshots --region $REGION --owner-ids self --query 'Snapshots[?StartTime>=`2023-01-01T00:00:00.000Z`]' > /tmp/recent-snapshots.json
SNAPSHOT_COUNT=$(jq '. | length' /tmp/recent-snapshots.json)

if [ $SNAPSHOT_COUNT -lt $INSTANCE_COUNT ]; then
    echo "WARNING: Insufficient recent snapshots. Skapa backups före migration."
    exit 1
fi

# Test 3: Network connectivity baseline
echo "Establishing network connectivity baseline..."
for instance_id in $(jq -r '.[] | .[] | .InstanceId' /tmp/pre-migration-instances.json); do
    if [ "$instance_id" != "null" ]; then
        echo "Testing connectivity to $instance_id..."
        # Implementera connectivity tests here
    fi
done

# Migration execution testing
echo "=== Migration Execution Tests ==="

# Test 4: Terraform plan validation
echo "Validating Terraform migration plan..."
cd terraform/migration

terraform init
terraform plan -var="project_name=$PROJECT_NAME" -var="environment=$ENVIRONMENT" -out=migration.plan

# Analysera plan for oväntade changes
terraform show -json migration.plan > /tmp/terraform-plan.json

# Kontrollera to inga resurser planeras for destruction
DESTROY_COUNT=$(jq '.resource_changes[] | select(.change.actions[] == "delete") | .address' /tmp/terraform-plan.json | wc -l)

if [ $DESTROY_COUNT -gt 0 ]; then
    echo "ERROR: Migration plan contains resource destruction. Granska before fortsättning."
    jq '.resource_changes[] | select(.change.actions[] == "delete") | .address' /tmp/terraform-plan.json
    exit 1
fi

# Test 5: Import validation
echo "Testing resource import procedures..."

# Skapa test import for a sample resource
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

def validate_tagging_compliance(region='eu-west-1'):
    """Validate to all migrerade resurser has korrekta tags"""
    ec2 = boto3.client('ec2', region_name=region)
    
    required_tags = ['ManagedBy', 'Environment', 'Project']
    non_compliant = []
    
    # Kontrollera EC2 instances
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
    """Validate säkerhetskonfiguration efter migration"""
    # implementation for security controls
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
# Monitor key performance metrics efter migration

METRICS_FILE="/tmp/post-migration-metrics.json"

echo "Collecting post-migration performance metrics..."

# CPU Utilization
aws cloudwatch get-metric-statistics \
    --namespace AWS/EC2 \
    --metric-name CPUUtilization \
    --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
    --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
    --period 300 \
    --statistics Average \
    --region $REGION > "$METRICS_FILE"

# Analysera metrics for avvikelser
AVERAGE_CPU=$(jq '.Datapoints | map(.Average) | add / length' "$METRICS_FILE")
echo "Average CPU utilization: $AVERAGE_CPU%"

if (( $(echo "$AVERAGE_CPU > 80" | bc -l) )); then
    echo "WARNING: High CPU utilization detected after migration"
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
echo "5. Document lessons learned"
```

## Summary

The modern Architecture as Code methodology represents the future of infrastructure management for global organisations. Migration from traditional infrastructure to Architecture as Code requires systematic planning, gradual implementation, and comprehensive testing. Organisations that successfully execute this migration position themselves for increased agility, improved security, and significant cost benefits.

Success factors include comprehensive assessment, realistic timeline planning, extensive team training, and robust testing frameworks. Hybrid migration strategies enable risk minimisation whilst delivering immediate value from Architecture as Code adoption.

Investment in proper migration planning and execution results in long-term benefits through improved operational efficiency, enhanced security posture, and reduced technical debt. Organisations that follow systematic migration approaches can expect successful transformation to modern, Architecture as Code-based infrastructure management.

## Bridging Technical and Organisational Change

Technical migration success depends fundamentally on organisational readiness. The most sophisticated automation pipelines, testing frameworks, and migration strategies fail without the cultural foundations, team structures, and leadership practices that enable people to thrive in code-based delivery environments.

Part E examines the organisational transformation that must accompany technical change. [Chapter 17 on Organisational Change](17_organizational_change.md) explores how teams evolve from siloed functions to cross-functional collaboration. [Chapter 18 on Team Structure](18_team_structure.md) provides concrete patterns for organising teams around Architecture as Code practices. The subsequent chapters demonstrate how management practices, AI-enabled collaboration, and digitalisation strategies complete the transformation from traditional to code-centric operating models.

## Sources and References

- AWS. "Large-Scale Migration and Modernisation Guide." Amazon Web Services, 2023.
- Microsoft. "Azure Migration Framework and Architecture as Code best practices." Microsoft Azure Documentation, 2023.
- Google Cloud. "Infrastructure Migration Strategies." Google Cloud Architecture Centre, 2023.
- Gartner. "Infrastructure Migration Trends in European Markets." Gartner Research, 2023.
- ITIL Foundation. "IT Service Management for Cloud Migration." AXELOS, 2023.
- European Commission. "Digital Transformation Guidelines for Public Sector." EU Digital Strategy, 2023.