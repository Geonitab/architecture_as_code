# Migration från traditionell infrastruktur

![Migrationsprocess](images/diagram_18_kapitel17.png)

*Migration från traditionell infrastruktur till Infrastructure as Code kräver systematisk planering, stegvis implementation och kontinuerlig validering. Diagrammet visar den strukturerade processen från assessment till fullständig IaC-adoption.*

## Övergripande beskrivning

Migration från traditionell, manuellt konfigurerad infrastruktur till Infrastructure as Code representerar en av de mest kritiska transformationerna för moderna IT-organisationer. Denna process kräver inte endast teknisk omstrukturering utan också organisatorisk förändring och kulturell adaption till kodbaserade arbetssätt.

Svenska organisationer står inför unika migreringsutmaningar genom legacy-system som utvecklats över decennier, regulatoriska krav som begränsar förändringstakt, och behovet av att balansera innovation med operational stability. Successful migration kräver comprehensive planning som minimerar risker samtidigt som den möjliggör snabb value realization.

Modern migrationsstrategier måste accommodera hybrid scenarios där legacy infrastructure coexisterar med IaC-managed resources under extended transition periods. Detta hybrid approach möjliggör gradual migration som reducerar business risk samtidigt som det möjliggör immediate benefits från IaC adoption.

Cloud-native migration pathways erbjuder opportuniteter att modernisera arkitektur samtidigt som infrastructure management kodifieras. Svenska företag kan leverage denna transformation för att implementera sustainability initiatives, improve cost efficiency och enhance security posture genom systematic IaC adoption.

## Assessment och planning faser

Comprehensive infrastructure assessment utgör foundationen för successful IaC migration. Detta inkluderar inventory av existing resources, dependency mapping, risk assessment och cost-benefit analysis som informerar migration strategy och timeline planning.

Discovery automation verktyg som AWS Application Discovery Service, Azure Migrate och Google Cloud migration tools kan accelerate assessment processen genom automated resource inventory och dependency detection. Dessa verktyg genererar data som kan inform IaC template generation och migration prioritization.

Risk assessment måste identifiera critical systems, single points of failure och compliance dependencies som påverkar migration approach. Svenska financial institutions och healthcare organizations måste särskilt consider regulatory implications och downtime restrictions som påverkar migration windows.

Migration wave planning balancerar technical dependencies med business priorities för att minimize risk och maximize value realization. Pilot projects med non-critical systems möjliggör team learning och process refinement innan critical system migration påbörjas.

## Lift-and-shift vs re-architecting

Lift-and-shift migration representerar den snabbaste vägen till cloud adoption men limiterar potential benefits från cloud-native capabilities. Denna approach är lämplig för applications med tight timelines eller limited modernization budget, men kräver follow-up optimization för long-term value.

Re-architecting för cloud-native patterns möjliggör maximum value från cloud investment genom improved scalability, resilience och cost optimization. Svenska retail companies som Klarna har demonstrerat hur re-architecting enables global expansion och innovation acceleration through cloud-native infrastructure.

Hybrid approaches som "lift-and-improve" balancerar speed-to-market med modernization benefits genom selective re-architecting av critical components samtidigt som majority av application förblir unchanged. Detta approach kan deliver immediate cloud benefits samtidigt som det möjliggör iterative modernization.

Application portfolio analysis hjälper determine optimal migration strategy per application baserat på technical fit, business value och modernization potential. Legacy applications med limited business value kan candidate för retirement rather than migration, vilket reducerar overall migration scope.

## Gradvis kodifiering av infrastruktur

Infrastructure inventory automation genom tools som Terraform import, CloudFormation drift detection och Azure Resource Manager templates enables systematic conversion av existing resources till IaC management. Automated discovery kan generate initial IaC configurations som require refinement men accelerate kodification process.

Template standardization genom reusable modules och organizational patterns ensures consistency across migrated infrastructure samtidigt som det reduces future maintenance overhead. Svenska government agencies har successfully implemented standardized IaC templates för common infrastructure patterns across different departments.

Configuration drift elimination genom IaC adoption requires systematic reconciliation mellan existing resource configurations och desired IaC state. Gradual enforcement av IaC-managed configuration ensures infrastructure stability samtidigt som det eliminates manual configuration inconsistencies.

Version control integration för infrastructure changes enables systematic tracking av migration progress samt provides rollback capabilities för problematic changes. Git-based workflows för infrastructure management etablishes foundation för collaborative infrastructure development och operational transparency.

## Team transition och kompetensutveckling

Skills development programs måste prepare traditional system administrators och network engineers för IaC-based workflows. Training curricula ska encompass Infrastructure as Code tools, cloud platforms, DevOps practices och automation scripting för comprehensive capability development.

Organizational structure evolution från traditional silos till cross-functional teams enables effective IaC adoption. Svenska telecommunications companies som Telia har successfully transitioned från separate development och operations teams till integrated DevOps teams som manage infrastructure as code.

Cultural transformation från manual processes till automated workflows requires change management programs som address resistance och promotes automation adoption. Success stories från early adopters can motivate broader organizational acceptance av IaC practices.

Mentorship programs pairing experienced cloud engineers med traditional infrastructure teams accelerates knowledge transfer och reduces adoption friction. External consulting support kan supplement internal capabilities during initial migration phases för complex enterprise environments.

## Praktiska exempel

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
    Automatiserad bedömning av befintlig infrastruktur för IaC-migration
    """
    
    def __init__(self, region='eu-north-1'):
        self.ec2 = boto3.client('ec2', region_name=region)
        self.rds = boto3.client('rds', region_name=region)
        self.elb = boto3.client('elbv2', region_name=region)
        self.cloudformation = boto3.client('cloudformation', region_name=region)
        
    def discover_unmanaged_resources(self) -> Dict:
        """Upptäck resurser som inte hanteras av IaC"""
        
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
        """Hitta EC2-instanser som inte hanteras av CloudFormation/Terraform"""
        
        # Hämta alla EC2-instanser
        response = self.ec2.describe_instances()
        unmanaged_instances = []
        
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                if instance['State']['Name'] != 'terminated':
                    # Kontrollera om instansen är managed av IaC
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
        """Kontrollera om resurs är managed av IaC"""
        
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
        """Generera Terraform-kod för migration av unmanaged resources"""
        
        terraform_code = """
# Automatiskt genererad migration plan
# Genererat: {date}
# Totalt antal resurser att migrera: {total_resources}

terraform {{
  required_providers {{
    aws = {{
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }}
  }}
}}

provider "aws" {{
  region = "eu-north-1"  # Stockholm för svenska organisationer
}}

""".format(
            date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            total_resources=len(unmanaged_resources.get('ec2_instances', []))
        )
        
        # Generera Terraform för EC2-instanser
        for i, instance in enumerate(unmanaged_resources.get('ec2_instances', [])):
            terraform_code += f"""
# Migration av befintlig EC2-instans {instance['instance_id']}
resource "aws_instance" "migrated_instance_{i}" {{
  # OBSERVERA: Denna konfiguration måste verifieras och anpassas
  instance_type = "{instance['instance_type']}"
  subnet_id     = "{instance['subnet_id']}"
  
  vpc_security_group_ids = {json.dumps(instance['security_groups'])}
  
  # Behåll befintliga tags och lägg till migration-info
  tags = {{
    Name = "{instance.get('tags', {}).get('Name', f'migrated-instance-{i}')}"
    MigratedFrom = "{instance['instance_id']}"
    MigrationDate = "{datetime.now().strftime('%Y-%m-%d')}"
    ManagedBy = "terraform"
    Environment = "{instance.get('tags', {}).get('Environment', 'production')}"
    Project = "{instance.get('tags', {}).get('Project', 'migration-project')}"
  }}
  
  # VIKTIGT: Importera befintlig resurs istället för att skapa ny
  # terraform import aws_instance.migrated_instance_{i} {instance['instance_id']}
}}
"""
        
        terraform_code += """
# Migration checklist:
# 1. Granska genererade konfigurationer noggrant
# 2. Testa i development-miljö först  
# 3. Importera befintliga resurser med terraform import
# 4. Kör terraform plan för att verifiera att inga förändringar planeras
# 5. Implementera gradvis med låg-risk resurser först
# 6. Uppdatera monitoring och alerting efter migration
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
                'prerequisites': ['IaC training completion', 'Tool setup', 'Backup verification']
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
    """Generera comprehensive migration playbook för svenska organisationer"""
    
    playbook = f"""
# IaC Migration Playbook för {assessment_results.get('organization_name', 'Organization')}

## Executive Summary
- **Totalt antal resurser att migrera:** {assessment_results['summary']['total_unmanaged_resources']}
- **Migrations-komplexitet:** {assessment_results['summary']['migration_complexity']}
- **Estimerad effort:** {assessment_results['summary']['estimated_migration_effort']}
- **Risk-bedömning:** {assessment_results['summary']['risk_assessment']}

## Fas 1: Förberedelse (Vecka 1-2)

### Team Training
- [ ] IaC grundutbildning för alla teammedlemmar
- [ ] Terraform/CloudFormation hands-on workshops
- [ ] Git workflows för infrastructure management
- [ ] Svenska compliance-krav (GDPR, MSB)

### Tool Setup
- [ ] Terraform/CloudFormation development environment
- [ ] Git repository för infrastructure code
- [ ] CI/CD pipeline för infrastructure deployment
- [ ] Monitoring och alerting konfiguration

### Risk Mitigation
- [ ] Fullständig backup av alla kritiska system
- [ ] Rollback procedures dokumenterade
- [ ] Emergency contacts och eskalationsplan
- [ ] Test environment för migration validation

## Fas 2: Pilot Migration (Vecka 3-4)

### Low-Risk Resources Migration
- [ ] Migrera development/test miljöer först
- [ ] Validera IaC templates och processer
- [ ] Dokumentera lessons learned
- [ ] Refinera migration procedures

### Quality Gates
- [ ] Automated testing av migrerade resurser
- [ ] Performance verification
- [ ] Security compliance validation
- [ ] Cost optimization review

## Fas 3: Production Migration (Vecka 5-12)

### Gradual Production Migration
- [ ] Non-critical production systems
- [ ] Critical systems med planerade maintenance windows
- [ ] Database migration med minimal downtime
- [ ] Network infrastructure migration

### Continuous Monitoring
- [ ] Real-time monitoring av migrerade system
- [ ] Automated alerting för anomalier
- [ ] Performance benchmarking
- [ ] Cost tracking och optimization

## Post-Migration Activities

### Process Optimization
- [ ] Infrastructure cost review och optimization
- [ ] Team workflow refinement
- [ ] Documentation och knowledge transfer
- [ ] Continuous improvement implementation

### Long-term Sustainability
- [ ] Regular IaC best practices review
- [ ] Team cross-training program
- [ ] Tool evaluation och updates
- [ ] Compliance monitoring automation

## Svenska Compliance Considerations

### GDPR Requirements
- [ ] Data residency i svenska/EU regioner
- [ ] Encryption at rest och in transit
- [ ] Access logging och audit trails
- [ ] Data retention policy implementation

### MSB Security Requirements
- [ ] Network segmentation implementation
- [ ] Incident response procedures
- [ ] Backup och disaster recovery
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
- Team satisfaction med nya processer: Target 8/10
- Knowledge transfer completion: Target 100%

## Risk Management

### High-Priority Risks
1. **Service Downtime:** Mitigated genom maintenance windows och rollback plans
2. **Data Loss:** Mitigated genom comprehensive backups och testing
3. **Security Compliance:** Mitigated genom automated compliance validation
4. **Team Resistance:** Mitigated genom training och change management

### Contingency Plans
- Immediate rollback procedures för kritiska issues
- Emergency support contacts och escalation
- Alternative migration approaches för problem resources
- Business continuity plans för extended downtime
"""
    
    return playbook
```

### CloudFormation Legacy Import
```yaml
# migration/legacy-import-template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Template för import av befintliga resurser till CloudFormation management'

Parameters:
  ExistingVPCId:
    Type: String
    Description: 'ID för befintlig VPC som ska importeras'
    
  ExistingInstanceId:
    Type: String  
    Description: 'ID för befintlig EC2-instans som ska importeras'
    
  Environment:
    Type: String
    Default: 'production'
    AllowedValues: ['development', 'staging', 'production']
    
  ProjectName:
    Type: String
    Description: 'Namn på projektet för resource tagging'

Resources:
  # Import av befintlig VPC
  ExistingVPC:
    Type: AWS::EC2::VPC
    Properties:
      # Dessa värden måste matcha befintlig VPC-konfiguration exakt
      CidrBlock: '10.0.0.0/16'  # Uppdatera med faktiskt CIDR
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

  # Import av befintlig EC2-instans
  ExistingInstance:
    Type: AWS::EC2::Instance
    Properties:
      # Dessa värden måste matcha befintlig instans-konfiguration
      InstanceType: 't3.medium'  # Uppdatera med faktisk instance type
      ImageId: 'ami-0c94855bb95b03c2e'  # Uppdatera med faktisk AMI
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

  # Säkerhet group för importerad instans
  ExistingSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: 'Imported security group för legacy system'
      VpcId: !Ref ExistingVPC
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 22
          ToPort: 22
          CidrIp: '10.0.0.0/8'  # Begränsa SSH access
          Description: 'SSH access från internal network'
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

  # Subnet för organiserad nätverkshantering
  ExistingSubnet:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref ExistingVPC
      CidrBlock: '10.0.1.0/24'  # Uppdatera med faktiskt subnet CIDR
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
    Description: 'ID för importerad VPC'
    Value: !Ref ExistingVPC
    Export:
      Name: !Sub '${AWS::StackName}-VPC-ID'
      
  ImportedInstanceId:
    Description: 'ID för importerad EC2-instans'
    Value: !Ref ExistingInstance
    Export:
      Name: !Sub '${AWS::StackName}-Instance-ID'
      
  ImportInstructions:
    Description: 'Instruktioner för resource import'
    Value: !Sub |
      För att importera befintliga resurser:
      1. aws cloudformation create-stack --stack-name ${ProjectName}-import --template-body file://legacy-import-template.yaml
      2. aws cloudformation import-resources-to-stack --stack-name ${ProjectName}-import --resources file://import-resources.json
      3. Verifiera att import var framgångsrik med: aws cloudformation describe-stacks --stack-name ${ProjectName}-import
```

### Migration Testing Framework  
```bash
#!/bin/bash
# migration/test-migration.sh
# Comprehensive testing script för IaC migration validation

set -e

PROJECT_NAME=${1:-"migration-test"}
ENVIRONMENT=${2:-"staging"}
REGION=${3:-"eu-north-1"}

echo "Starting IaC migration testing för projekt: $PROJECT_NAME"
echo "Environment: $ENVIRONMENT"
echo "Region: $REGION"

# Pre-migration testing
echo "=== Pre-Migration Tests ==="

# Test 1: Verifiera att alla resurser är inventerade
echo "Testing resource inventory..."
aws ec2 describe-instances --region $REGION --query 'Reservations[*].Instances[?State.Name!=`terminated`]' > /tmp/pre-migration-instances.json
aws rds describe-db-instances --region $REGION > /tmp/pre-migration-rds.json

INSTANCE_COUNT=$(jq '.[] | length' /tmp/pre-migration-instances.json | jq -s 'add')
RDS_COUNT=$(jq '.DBInstances | length' /tmp/pre-migration-rds.json)

echo "Upptäckte $INSTANCE_COUNT EC2-instanser och $RDS_COUNT RDS-instanser"

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
        # Implementera connectivity tests här
    fi
done

# Migration execution testing
echo "=== Migration Execution Tests ==="

# Test 4: Terraform plan validation
echo "Validating Terraform migration plan..."
cd terraform/migration

terraform init
terraform plan -var="project_name=$PROJECT_NAME" -var="environment=$ENVIRONMENT" -out=migration.plan

# Analysera plan för oväntade förändringar
terraform show -json migration.plan > /tmp/terraform-plan.json

# Kontrollera att inga resurser planeras för destruction
DESTROY_COUNT=$(jq '.resource_changes[] | select(.change.actions[] == "delete") | .address' /tmp/terraform-plan.json | wc -l)

if [ $DESTROY_COUNT -gt 0 ]; then
    echo "ERROR: Migration plan innehåller resource destruction. Granska innan fortsättning."
    jq '.resource_changes[] | select(.change.actions[] == "delete") | .address' /tmp/terraform-plan.json
    exit 1
fi

# Test 5: Import validation
echo "Testing resource import procedures..."

# Skapa test import för en sample resource
SAMPLE_INSTANCE_ID=$(jq -r '.[] | .[] | .InstanceId' /tmp/pre-migration-instances.json | head -1)

if [ "$SAMPLE_INSTANCE_ID" != "null" ] && [ "$SAMPLE_INSTANCE_ID" != "" ]; then
    echo "Testing import för instance: $SAMPLE_INSTANCE_ID"
    
    # Dry-run import test
    terraform import -dry-run aws_instance.test_import $SAMPLE_INSTANCE_ID || {
        echo "WARNING: Import test failed för $SAMPLE_INSTANCE_ID"
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
    """Validera att alla migrerade resurser har korrekta tags"""
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
    """Validera säkerhetskonfiguration efter migration"""
    # Implementation för säkerhetskontroller
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
    --region eu-north-1 > "$METRICS_FILE"

# Analysera metrics för avvikelser
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
echo "4. Monitor performance för 24 hours"
echo "5. Document lessons learned"
```

## Sammanfattning

Migration från traditionell infrastruktur till Infrastructure as Code representerar en kritisk transformation som kräver systematisk planering, gradvis implementation och omfattande testing. Svenska organisationer som framgångsrikt genomför denna migration positionerar sig för ökad agility, förbättrad säkerhet och betydande kostnadsmässiga fördelar.

Framgångsfaktorer inkluderar comprehensive assessment, realistisk timeline planning, extensive team training och robust testing frameworks. Hybrid migration strategies möjliggör risk minimization samtidigt som de levererar immediate value från IaC adoption.

Investment i proper migration planning och execution resulterar i långsiktiga fördelar genom improved operational efficiency, enhanced security posture och reduced technical debt. Svenska organisationer som följer systematic migration approaches kan förvänta sig successful transformation till modern, kodbaserad infrastrukturhantering.

## Källor och referenser

- AWS. "Large-Scale Migration och Modernization Guide." Amazon Web Services, 2023.
- Microsoft. "Azure Migration Framework och Best Practices." Microsoft Azure Documentation, 2023.
- Google Cloud. "Infrastructure Migration Strategies." Google Cloud Architecture Center, 2023.
- Gartner. "Infrastructure Migration Trends in Nordic Countries." Gartner Research, 2023.
- ITIL Foundation. "IT Service Management för Cloud Migration." AXELOS, 2023.
- Swedish Government. "Digital Transformation Guidelines för Public Sector." Digitaliseringsstyrelsen, 2023.