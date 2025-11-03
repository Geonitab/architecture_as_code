# Appendix D: Templates and Tools {.unnumbered}

Architecture as Code initiatives rely on reusable templates and interactive tools to keep governance, maturity assessments, and compliance evidence consistent. This appendix curates the canonical assets published alongside the book so that practitioners can embed them directly into their delivery workflows.

## Architecture as Code Maturity Model

The [Architecture as Code Maturity Model](architecture_as_code_maturity_model.md) describes six adoption levels spanning foundational automation through to fully codified enterprise governance. Each level contains assessment prompts, operating model guidance, and measurable outcomes that help teams benchmark their progress.

## Architecture as Code Maturity Radar Tool

The [Maturity Radar Tool](maturity_model_radar.html) offers an interactive visualisation of the maturity model. It enables leadership teams to capture current-state and target-state indicators, compare trajectories across business units, and export radar charts for strategy reviews.

## Control Mapping Matrix Template

The [Control Mapping Matrix Template](appendix_d_control_mapping_matrix_template.md) provides a reusable table for expressing "assure once, comply many" evidence flows. Use it to link automated assurance artefacts to ISO 27001, SOC 2, NIST 800-53, GDPR, and internal policies so that governance teams can reuse validated outputs without bespoke reporting.

## Implementation Guidance

1. **Version the artefacts:** Store local copies of the templates in version control so changes trigger peer review and automated validation.
2. **Integrate with pipelines:** Reference the templates from CI/CD jobs to keep evidence manifests, maturity assessments, and control mappings synchronised with production systems.
3. **Tailor for context:** Extend the templates with sector-specific obligations or additional metrics, but retain the canonical structure to preserve comparability across programmes.

## Migration Assessment Automation

```python
# migration_assessment/infrastructure_discovery.py
import boto3
import json
from datetime import datetime
from typing import Dict, List
import pandas as pd

class InfrastructureMigrationAssessment:
    """
    Automated assessment of existing infrastructure for architecture as code migration
    """

    def __init__(self, region='eu-west-1'):
        self.ec2 = boto3.client('ec2', region_name=region)
        self.rds = boto3.client('rds', region_name=region)
        self.elb = boto3.client('elbv2', region_name=region)
        self.cloudformation = boto3.client('cloudformation', region_name=region)

    def discover_unmanaged_resources(self) -> Dict:
        """Discover resources that are not managed by architecture as code"""

        unmanaged_resources = {
            'ec2_instances': self._find_unmanaged_ec2(),
            'rds_instances': self._find_unmanaged_rds(),
            'load_balancers': self._find_unmanaged_load_balancers(),
            'security_groups': self._find_unmanaged_security_groups(),
            'summary': {},
        }

        # Calculate summary statistics
        total_resources = sum(len(resources) for resources in unmanaged_resources.values() if isinstance(resources, list))
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
                    # Check if the instance is managed by architecture as code
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
        """Check if resource is managed by architecture as code"""

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
# Total number of resources to migrate: {total_resources}

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
# 4. Run terraform plan to verify that no changes are planned
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
                'prerequisites': ['architecture as code training completion', 'Tool setup', 'Backup verification']
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
    """Generate comprehensive migration playbook for European organisations"""

    playbook = f"""
# architecture as code Migration Playbook for {assessment_results.get('organization_name', 'Organization')}

## Executive Summary
- **Total number of resources to migrate:** {assessment_results['summary']['total_unmanaged_resources']}
- **Migration complexity:** {assessment_results['summary']['migration_complexity']}
- **Estimated effort:** {assessment_results['summary']['estimated_migration_effort']}
- **Risk assessment:** {assessment_results['summary']['risk_assessment']}

## Phase 1: Preparation (Week 1-2)

### Team Training
- [ ] architecture as code foundation training for all team members
- [ ] Terraform/CloudFormation hands-on workshops
- [ ] Git workflows for infrastructure management
- [ ] EU compliance requirements (GDPR, data sovereignty)

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
- [ ] Validate architecture as code templates and processes
- [ ] Document lessons learned
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
- [ ] Continuous improvement architecture as code implementation

### Long-term Sustainability
- [ ] Regular architecture as code best practices review
- [ ] Team cross-training programme
- [ ] Tool evaluation and updates
- [ ] Compliance monitoring automation

## EU Compliance Considerations

### GDPR Requirements
- [ ] Data residency in EU regions
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
