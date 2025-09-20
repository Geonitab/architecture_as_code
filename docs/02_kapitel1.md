# Grundläggande principer för Infrastructure as Code

Infrastructure as Code bygger på flera fundamentala principer som säkerställer framgångsrik implementation och långsiktig hållbarhet. Dessa principer utgör grunden för hur organisationer bör tänka kring kodbaserad infrastruktur. Som vi såg i [inledningen](01_inledning.md), representerar IaC en fundamental transformation av infrastrukturhantering, och dessa principer guidar denna transformation på ett praktiskt och strategiskt plan.

![Grundläggande principer diagram](images/diagram_02_kapitel1.png)

Diagrammet visar det naturliga flödet från deklarativ kod genom versionskontroll och automatisering till reproducerbarhet och skalbarhet - de fem grundpelarna inom IaC. Denna progression från deklarativ kod till skalbar infrastruktur skapar grunden för det versionhanterade arbetssätt som vi kommer att fördjupa oss i [kapitel 3](03_kapitel2.md).

## Deklarativ vs imperativ approach

Den deklarativa approachen innebär att beskriva önskat slutläge istället för stegen för att nå dit. Detta skiljer sig från imperativ programmering där varje steg måste specificeras explicit. Deklarativ IaC-kod fokuserar på "vad" istället för "hur", vilket möjliggör högre abstraktion och mindre felbenägenhet.

Exempel på deklarativ kod inkluderar Terraform HCL, CloudFormation YAML, eller Kubernetes manifests. Dessa verktyg tar ansvar för att beräkna och utföra nödvändiga förändringar för att uppnå det specificerade tillståndet, vilket reducerar komplexitet för utvecklaren.

### Praktiska fördelar med deklarativ IaC

**Cognitive Load Reduction** utgör en av de mest betydande fördelarna med deklarativ approach. Svenska utvecklare och operations teams behöver inte hålla reda på complex state transitions eller worry about execution order - de kan fokusera på desired outcomes istället för implementation details.

```hcl
# Deklarativ Terraform exempel för svensk AWS infrastructure
resource "aws_vpc" "svenska_production" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name = "Svenska-Production-VPC"
    Environment = "production"
    DataResidency = "Sweden"
    ComplianceLevel = "GDPR"
    CostCenter = "infrastructure"
  }
}

resource "aws_subnet" "public_subnets" {
  count = length(var.availability_zones)
  
  vpc_id                  = aws_vpc.svenska_production.id
  cidr_block              = "10.0.${count.index + 1}.0/24"
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = true
  
  tags = {
    Name = "Public-Subnet-${count.index + 1}"
    Type = "public"
    Environment = "production"
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.svenska_production.id
  
  tags = {
    Name = "Svenska-Production-IGW"
    Environment = "production"
  }
}
```

**Error Prevention and Recovery**: Deklarativ systems kan automatiskt detect och correct configuration drift, vilket är särskilt värdefullt för svenska organisationer med compliance requirements som kräver consistent infrastructure state.

**Multi-Environment Consistency**: Samma deklarativ kod kan användas across development, staging och production environments med endast parameter changes, vilket säkerställer consistency och reduces environment-specific bugs.

### Imperativ approach och dess limitations

Traditionell imperativ infrastructure management kräver explicit specification av varje action:

```bash
# Imperativ approach - fel-prone och svår att maintain
aws ec2 create-vpc --cidr-block 10.0.0.0/16
VPC_ID=$(aws ec2 describe-vpcs --filters "Name=cidr,Values=10.0.0.0/16" --query 'Vpcs[0].VpcId' --output text)

aws ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.0.1.0/24 --availability-zone eu-north-1a
SUBNET_ID=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" --query 'Subnets[0].SubnetId' --output text)

aws ec2 create-internet-gateway
IGW_ID=$(aws ec2 describe-internet-gateways --query 'InternetGateways[0].InternetGatewayId' --output text)

aws ec2 attach-internet-gateway --internet-gateway-id $IGW_ID --vpc-id $VPC_ID
```

Denna approach introducerar flera problems:
- **State Tracking Complexity**: Manual tracking av resource IDs och dependencies
- **Error Handling**: Complex error recovery och rollback logic required
- **Race Conditions**: Potential timing issues mellan dependent operations
- **Reproducibility Issues**: Scripts may behave differently in different environments

## Idempotens och konvergens

Idempotens säkerställer att upprepade körningar av samma IaC-kod producerar identiska resultat, oavsett nuvarande systemtillstånd. Detta är kritiskt för tillförlitlighet och möjliggör säker automatisering utan risk för oavsiktliga förändringar.

Konvergens refererar till systemets förmåga att automatiskt korrigera avvikelser från önskat tillstånd. Modern IaC-verktyg implementerar kontinuerlig konvergens genom att regelbundet kontrollera och korrigera infrastrukturtillstånd enligt definierade specifikationer.

### Idempotens i praktiken

Idempotent operations kan köras multiple times utan adverse effects. För svenska organisationer innebär detta:

**Säker Automation**: Automated systems kan retry operations utan fear av duplicating resources eller creating inconsistent states.

**Disaster Recovery**: Infrastructure kan rebuilt exactly från kod efter major incidents, vilket är kritiskt för business continuity.

**Development Workflow**: Developers kan apply same configuration repeatedly under utveckling utan accumulating resources eller unexpected behaviors.

```python
# Exempel på idempotent infrastructure validation
import boto3
import json

class SwedishVPCValidator:
    """
    Idempotent validator för svensk VPC infrastructure
    """
    
    def __init__(self, region='eu-north-1'):
        self.ec2 = boto3.client('ec2', region_name=region)
        self.expected_config = {
            'vpc_cidr': '10.0.0.0/16',
            'enable_dns_hostnames': True,
            'enable_dns_support': True,
            'required_tags': {
                'DataResidency': 'Sweden',
                'ComplianceLevel': 'GDPR',
                'Environment': 'production'
            }
        }
    
    def validate_and_converge(self, vpc_name: str) -> dict:
        """
        Idempotent function som ensures VPC matches expected configuration
        """
        
        # Find existing VPC
        vpcs = self.ec2.describe_vpcs(
            Filters=[
                {'Name': 'tag:Name', 'Values': [vpc_name]},
                {'Name': 'state', 'Values': ['available']}
            ]
        )
        
        if not vpcs['Vpcs']:
            # VPC doesn't exist - create it
            return self._create_vpc(vpc_name)
        
        vpc = vpcs['Vpcs'][0]
        vpc_id = vpc['VpcId']
        
        # Validate existing VPC configuration
        issues_found = []
        
        # Check CIDR block
        if vpc['CidrBlock'] != self.expected_config['vpc_cidr']:
            issues_found.append({
                'type': 'cidr_mismatch',
                'current': vpc['CidrBlock'],
                'expected': self.expected_config['vpc_cidr']
            })
        
        # Check DNS settings
        dns_attrs = self.ec2.describe_vpc_attribute(
            VpcId=vpc_id, Attribute='enableDnsHostnames'
        )
        if not dns_attrs['EnableDnsHostnames']['Value']:
            self._fix_dns_settings(vpc_id)
            issues_found.append({'type': 'dns_hostnames_fixed'})
        
        # Validate tags
        tag_issues = self._validate_tags(vpc_id, vpc.get('Tags', []))
        if tag_issues:
            self._fix_tags(vpc_id, tag_issues)
            issues_found.extend(tag_issues)
        
        # Return result
        return {
            'vpc_id': vpc_id,
            'action': 'validated' if not issues_found else 'converged',
            'issues_resolved': issues_found,
            'compliant': len(issues_found) == 0
        }
    
    def _create_vpc(self, vpc_name: str) -> dict:
        """Create new VPC med Swedish compliance settings"""
        
        response = self.ec2.create_vpc(CidrBlock=self.expected_config['vpc_cidr'])
        vpc_id = response['Vpc']['VpcId']
        
        # Enable DNS settings
        self.ec2.modify_vpc_attribute(
            VpcId=vpc_id, 
            EnableDnsHostnames={'Value': True}
        )
        self.ec2.modify_vpc_attribute(
            VpcId=vpc_id, 
            EnableDnsSupport={'Value': True}
        )
        
        # Apply required tags
        tags = [
            {'Key': 'Name', 'Value': vpc_name},
            {'Key': 'DataResidency', 'Value': 'Sweden'},
            {'Key': 'ComplianceLevel', 'Value': 'GDPR'},
            {'Key': 'Environment', 'Value': 'production'},
            {'Key': 'CreatedBy', 'Value': 'infrastructure-as-code'},
            {'Key': 'ManagedBy', 'Value': 'terraform'}
        ]
        
        self.ec2.create_tags(Resources=[vpc_id], Tags=tags)
        
        return {
            'vpc_id': vpc_id,
            'action': 'created',
            'compliant': True
        }
    
    def _validate_tags(self, vpc_id: str, current_tags: list) -> list:
        """Validate VPC tags mot svenska compliance requirements"""
        
        current_tag_dict = {tag['Key']: tag['Value'] for tag in current_tags}
        missing_tags = []
        
        for key, expected_value in self.expected_config['required_tags'].items():
            if key not in current_tag_dict:
                missing_tags.append({
                    'type': 'missing_tag',
                    'key': key,
                    'expected_value': expected_value
                })
            elif current_tag_dict[key] != expected_value:
                missing_tags.append({
                    'type': 'incorrect_tag_value',
                    'key': key,
                    'current_value': current_tag_dict[key],
                    'expected_value': expected_value
                })
        
        return missing_tags
```

### Konvergens och drift detection

Configuration drift occurs när actual infrastructure state divergerar från intended state defined in code. Svenska organisationer kräver robust drift detection och automatic remediation:

**Continuous Monitoring**: Systems kontinuerligt monitor infrastructure state och detect deviations från defined configurations.

**Automatic Remediation**: När drift detected, systems kan automatically apply corrections för att restore intended state.

**Audit and Compliance**: Drift detection och remediation provides comprehensive audit trails för compliance reporting.

```yaml
# Kubernetes CronJob för continuous infrastructure validation
apiVersion: batch/v1
kind: CronJob
metadata:
  name: svensk-infrastructure-validator
  namespace: infrastructure-ops
spec:
  schedule: "*/15 * * * *"  # Kör varje 15:e minut
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: validator
            image: svenska-org/infrastructure-validator:latest
            env:
            - name: AWS_REGION
              value: "eu-north-1"
            - name: COMPLIANCE_LEVEL
              value: "GDPR"
            - name: SLACK_WEBHOOK_URL
              valueFrom:
                secretKeyRef:
                  name: notification-secrets
                  key: slack-webhook
            command:
            - /bin/sh
            - -c
            - |
              echo "🔍 Startar infrastruktur-validering..."
              
              # Validera VPC configuration
              python3 /app/validate_vpc.py --config /config/production.json
              
              # Kontrollera security groups
              python3 /app/validate_security_groups.py --compliance GDPR
              
              # Verifiera data residency
              python3 /app/validate_data_residency.py --required-region eu-north-1
              
              # Rapportera resultatet
              if [ $? -eq 0 ]; then
                echo "✅ All infrastructure validation passed"
              else
                echo "❌ Infrastructure validation failed - remediation required"
                curl -X POST $SLACK_WEBHOOK_URL \
                  -H 'Content-type: application/json' \
                  --data '{"text":"🚨 Infrastructure drift detected - remediation in progress"}'
              fi
          restartPolicy: OnFailure
```

## Immutable infrastruktur

Principen om immutable infrastruktur innebär att infrastrukturkomponenter aldrig modifieras efter deployment. Istället ersätts hela komponenter när förändringar behövs. Detta eliminerar configuration drift och säkerställer konsistens mellan miljöer.

Immutable infrastruktur stödjs av containerteknologier och cloud-native tjänster som möjliggör snabb skapelse och förstörelse av infrastrukturresurser. Detta approach reducerar också säkerhetsrisker genom att minimera systemets attackyta över tid.

### Fördelar med immutable infrastructure

**Configuration Drift Elimination**: Eftersom servers aldrig modificeras after initial deployment, kan configuration drift inte occur. Detta är särskilt värdefullt för svenska finansiella institutioner med strict compliance requirements.

**Predictable Deployments**: Varje deployment skapar completely new infrastructure med known configurations, vilket eliminerar dependency på previous system states.

**Enhanced Security**: Immutable servers minimerar attack vectors genom att reduce opportunities för persistent malware eller unauthorized modifications.

**Simplified Rollback**: Rolling back till previous version innebär simply redirecting traffic till previously deployed infrastructure rather than complex in-place changes.

### Implementation patterns för svenska organisationer

**Blue-Green Deployments**: Maintain två identical production environments där endast en active at a time. This enables zero-downtime deployments med instant rollback capabilities.

```hcl
# Terraform exempel för blue-green deployment setup
resource "aws_launch_configuration" "app_blue" {
  name_prefix     = "svenska-app-blue-"
  image_id        = var.app_ami_blue
  instance_type   = "t3.medium"
  security_groups = [aws_security_group.app.id]
  
  # Immutable server configuration
  user_data = templatefile("${path.module}/user_data.sh", {
    app_version = var.blue_version
    environment = "production"
    color = "blue"
  })
  
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_launch_configuration" "app_green" {
  name_prefix     = "svenska-app-green-"
  image_id        = var.app_ami_green
  instance_type   = "t3.medium"
  security_groups = [aws_security_group.app.id]
  
  user_data = templatefile("${path.module}/user_data.sh", {
    app_version = var.green_version
    environment = "production"
    color = "green"
  })
  
  lifecycle {
    create_before_destroy = true
  }
}

# Auto Scaling Groups för blue och green environments
resource "aws_autoscaling_group" "app_blue" {
  name                 = "svenska-app-blue-asg"
  launch_configuration = aws_launch_configuration.app_blue.name
  min_size             = var.active_environment == "blue" ? 2 : 0
  max_size             = var.active_environment == "blue" ? 10 : 0
  desired_capacity     = var.active_environment == "blue" ? 3 : 0
  
  vpc_zone_identifier = var.private_subnet_ids
  target_group_arns   = var.active_environment == "blue" ? [aws_lb_target_group.app.arn] : []
  
  tag {
    key                 = "Name"
    value               = "Svenska-App-Blue"
    propagate_at_launch = true
  }
  
  tag {
    key                 = "Environment"
    value               = "production"
    propagate_at_launch = true
  }
  
  tag {
    key                 = "DeploymentColor"
    value               = "blue"
    propagate_at_launch = true
  }
}

resource "aws_autoscaling_group" "app_green" {
  name                 = "svenska-app-green-asg"
  launch_configuration = aws_launch_configuration.app_green.name
  min_size             = var.active_environment == "green" ? 2 : 0
  max_size             = var.active_environment == "green" ? 10 : 0
  desired_capacity     = var.active_environment == "green" ? 3 : 0
  
  vpc_zone_identifier = var.private_subnet_ids
  target_group_arns   = var.active_environment == "green" ? [aws_lb_target_group.app.arn] : []
  
  tag {
    key                 = "Name"
    value               = "Svenska-App-Green"
    propagate_at_launch = true
  }
  
  tag {
    key                 = "Environment"
    value               = "production"
    propagate_at_launch = true
  }
  
  tag {
    key                 = "DeploymentColor"
    value               = "green"
    propagate_at_launch = true
  }
}
```

**Container-Based Immutability**: Leveraging containerization för complete immutability från application layer down till runtime environment.

```dockerfile
# Multi-stage Docker build för svenska application
FROM node:18-alpine AS builder
WORKDIR /app

# Copy dependency files
COPY package*.json ./
RUN npm ci --only=production

# Copy source code
COPY src/ ./src/
COPY public/ ./public/

# Build application
RUN npm run build

# Production stage - immutable runtime environment
FROM nginx:alpine
LABEL maintainer="svenska-org@example.com"
LABEL version="${BUILD_VERSION}"
LABEL environment="production"
LABEL compliance="GDPR"

# Copy built application
COPY --from=builder /app/build /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Swedish timezone och locale settings
RUN apk add --no-cache tzdata && \
    cp /usr/share/zoneinfo/Europe/Stockholm /etc/localtime && \
    echo "Europe/Stockholm" > /etc/timezone

# Security hardening
RUN addgroup -g 1001 -S nginx && \
    adduser -S -D -H -u 1001 -h /var/cache/nginx -s /sbin/nologin -G nginx -g nginx nginx && \
    chown -R nginx:nginx /usr/share/nginx/html && \
    chmod -R 755 /usr/share/nginx/html

USER nginx

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
```

### Immutable infrastructure challenges och solutions

**State Management**: Immutable infrastructure requires external state persistence för databases, user sessions och application data.

```hcl
# Terraform för external state management
resource "aws_efs_file_system" "shared_storage" {
  creation_token   = "svenska-shared-storage"
  performance_mode = "generalPurpose"
  encrypted        = true
  
  tags = {
    Name = "Svenska-Shared-Storage"
    Purpose = "immutable-infrastructure-state"
    DataClassification = "internal"
  }
}

resource "aws_rds_instance" "app_database" {
  identifier = "svenska-app-db"
  
  engine         = "postgres"
  engine_version = "15.4"
  instance_class = "db.t3.medium"
  
  allocated_storage     = 100
  max_allocated_storage = 1000
  storage_encrypted     = true
  
  db_name  = "svenska_app"
  username = "app_user"
  password = var.database_password
  
  # Network settings
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.database.id]
  
  # Backup och recovery
  backup_retention_period = 35  # GDPR compliance requirement
  backup_window          = "03:00-04:00"  # Swedish night hours
  maintenance_window     = "Sun:04:00-Sun:05:00"
  
  # Monitoring
  performance_insights_enabled = true
  monitoring_interval         = 60
  
  tags = {
    Name = "Svenska-App-Database"
    Environment = "production"
    DataClassification = "sensitive"
    BackupRequired = "true"
  }
}
```

**Cost Optimization**: Immutable infrastructure kan increase costs through resource duplication during deployments. Swedish organizations implement several strategies för cost control:

```python
# Automated cost optimization för immutable infrastructure
import boto3
import json
from datetime import datetime, timedelta

class SwedishCostOptimizer:
    """
    Cost optimization för immutable infrastructure deployments
    """
    
    def __init__(self, region='eu-north-1'):
        self.ec2 = boto3.client('ec2', region_name=region)
        self.cost_explorer = boto3.client('ce', region_name='us-east-1')
        self.sns = boto3.client('sns', region_name=region)
        
    def optimize_deployment_costs(self, deployment_id: str) -> dict:
        """
        Optimize costs during blue-green deployment
        """
        
        # Get current deployment info
        deployment_info = self._get_deployment_info(deployment_id)
        
        optimizations = []
        
        # 1. Use spot instances för non-production traffic
        if deployment_info['environment'] == 'staging':
            spot_savings = self._recommend_spot_instances(deployment_info)
            optimizations.extend(spot_savings)
        
        # 2. Schedule automatic cleanup för old deployments
        cleanup_schedule = self._schedule_deployment_cleanup(deployment_info)
        optimizations.append(cleanup_schedule)
        
        # 3. Optimize instance sizes based på actual usage
        sizing_recommendations = self._analyze_instance_sizing(deployment_info)
        optimizations.extend(sizing_recommendations)
        
        # 4. Use reserved instances för predictable workloads
        ri_recommendations = self._recommend_reserved_instances(deployment_info)
        optimizations.extend(ri_recommendations)
        
        # Calculate total potential savings
        total_savings_sek = sum(opt.get('monthly_savings_sek', 0) for opt in optimizations)
        
        return {
            'deployment_id': deployment_id,
            'total_monthly_savings_sek': total_savings_sek,
            'optimizations': optimizations,
            'implementation_priority': self._prioritize_optimizations(optimizations)
        }
    
    def _schedule_deployment_cleanup(self, deployment_info: dict) -> dict:
        """
        Schedule automatic cleanup för gamla deployments
        """
        
        return {
            'type': 'automated_cleanup',
            'description': 'Automatisk rensning av gamla blue-green deployments',
            'schedule': 'After 48 hours of successful deployment',
            'monthly_savings_sek': 45000,  # Estimated based on instance costs
            'implementation': {
                'cloudwatch_rule': {
                    'schedule_expression': 'rate(24 hours)',
                    'targets': ['cleanup-lambda-function']
                },
                'lambda_function': 'svenska-deployment-cleanup',
                'iam_permissions': [
                    'ec2:DescribeInstances',
                    'ec2:TerminateInstances',
                    'autoscaling:UpdateAutoScalingGroup'
                ]
            },
            'safety_checks': [
                'Verify deployment health för 48 hours',
                'Ensure traffic successfully routed to new deployment',
                'Confirm monitoring och alerting functional'
            ]
        }
```

## Testbarhet och kvalitetssäkring

IaC-kod ska behandlas som vilken annan kod som helst, vilket innebär omfattande testning på flera nivåer. Unit-tester validerar enskilda moduler, integration-tester verifierar komponentinteraktion, och end-to-end-tester säkerställer hela systemets funktionalitet.

Teststrategier inkluderar statisk kodanalys, policy validation, och infrastrukturtestning i isolerade miljöer. Automated testing pipelines säkerställer att förändringar valideras innan de når produktionsmiljöer, vilket minskar risken för störningar och säkerhetsbrister.

### Comprehensive testing strategy för svenska IaC

**Unit Testing**: Validera individual infrastructure components independently:

```python
# Python unittest för Terraform module validation
import unittest
import json
import subprocess
from pathlib import Path

class TestSwedishVPCModule(unittest.TestCase):
    """
    Unit tests för svensk VPC Terraform module
    """
    
    @classmethod
    def setUpClass(cls):
        """Setup test environment"""
        cls.module_path = Path(__file__).parent / "terraform" / "modules" / "svenska-vpc"
        cls.test_vars = {
            "vpc_cidr": "10.0.0.0/16",
            "environment": "test",
            "availability_zones": ["eu-north-1a", "eu-north-1b"],
            "enable_nat_gateway": True,
            "enable_vpn_gateway": False
        }
    
    def test_vpc_configuration_valid(self):
        """Test that VPC configuration är valid"""
        
        # Create test terraform.tfvars file
        with open(self.module_path / "test.tfvars", "w") as f:
            for key, value in self.test_vars.items():
                if isinstance(value, list):
                    f.write(f'{key} = {json.dumps(value)}\n')
                elif isinstance(value, str):
                    f.write(f'{key} = "{value}"\n')
                else:
                    f.write(f'{key} = {str(value).lower()}\n')
        
        # Run terraform validate
        result = subprocess.run(
            ["terraform", "validate"],
            cwd=self.module_path,
            capture_output=True,
            text=True
        )
        
        self.assertEqual(result.returncode, 0, f"Terraform validation failed: {result.stderr}")
    
    def test_required_outputs_present(self):
        """Test that alla required outputs är defined"""
        
        expected_outputs = [
            "vpc_id",
            "vpc_cidr_block", 
            "public_subnet_ids",
            "private_subnet_ids",
            "internet_gateway_id",
            "nat_gateway_ids"
        ]
        
        # Read outputs.tf file
        outputs_file = self.module_path / "outputs.tf"
        with open(outputs_file, "r") as f:
            outputs_content = f.read()
        
        for output in expected_outputs:
            self.assertIn(f'output "{output}"', outputs_content, 
                         f"Required output {output} not found")
    
    def test_swedish_compliance_tags(self):
        """Test that Swedish compliance tags är correctly configured"""
        
        # Read main.tf file
        main_file = self.module_path / "main.tf"
        with open(main_file, "r") as f:
            main_content = f.read()
        
        required_tag_keys = [
            "DataResidency",
            "ComplianceLevel", 
            "Environment",
            "CostCenter"
        ]
        
        for tag_key in required_tag_keys:
            self.assertIn(tag_key, main_content,
                         f"Required Swedish compliance tag {tag_key} not found")
    
    def test_security_group_restrictions(self):
        """Test that security groups follow Swedish security requirements"""
        
        # Run terraform plan
        result = subprocess.run(
            ["terraform", "plan", "-var-file=test.tfvars", "-out=test.tfplan"],
            cwd=self.module_path,
            capture_output=True,
            text=True
        )
        
        self.assertEqual(result.returncode, 0, "Terraform plan failed")
        
        # Convert plan to JSON
        result = subprocess.run(
            ["terraform", "show", "-json", "test.tfplan"],
            cwd=self.module_path,
            capture_output=True,
            text=True
        )
        
        plan_data = json.loads(result.stdout)
        
        # Check för forbidden security group rules
        for resource in plan_data.get('planned_values', {}).get('root_module', {}).get('resources', []):
            if resource.get('type') == 'aws_security_group':
                values = resource.get('values', {})
                
                # Check ingress rules
                for rule in values.get('ingress', []):
                    cidr_blocks = rule.get('cidr_blocks', [])
                    
                    # Should not allow SSH from anywhere
                    if rule.get('from_port') == 22 and '0.0.0.0/0' in cidr_blocks:
                        self.fail("SSH access från internet detected - violates Swedish security requirements")
                    
                    # Should not allow unrestricted access on non-web ports
                    if rule.get('from_port') not in [80, 443] and '0.0.0.0/0' in cidr_blocks:
                        self.fail(f"Unrestricted access on port {rule.get('from_port')} detected")

if __name__ == '__main__':
    unittest.main()
```

**Integration Testing**: Validera how infrastructure components work together:

```yaml
# Terratest integration tests för Swedish infrastructure
version: '3.8'

services:
  terratest:
    build:
      context: .
      dockerfile: Dockerfile.terratest
    environment:
      - AWS_REGION=eu-north-1
      - TF_VAR_environment=integration-test
      - COMPLIANCE_LEVEL=GDPR
    volumes:
      - ./tests:/tests
      - ./terraform:/terraform
      - ~/.aws:/root/.aws:ro
    command: |
      go test -v ./tests/integration_test.go \
        -run TestSwedishInfrastructureIntegration \
        -timeout 30m
```

```go
// integration_test.go - Terratest integration tests
package test

import (
    "testing"
    "time"
    
    "github.com/gruntwork-io/terratest/modules/terraform"
    "github.com/gruntwork-io/terratest/modules/aws"
    "github.com/stretchr/testify/assert"
)

func TestSwedishInfrastructureIntegration(t *testing.T) {
    t.Parallel()
    
    // AWS region för testing
    awsRegion := "eu-north-1"
    
    // Terraform options
    terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
        TerraformDir: "../terraform/environments/integration",
        Vars: map[string]interface{}{
            "environment": "integration-test",
            "vpc_cidr": "10.100.0.0/16",
            "enable_flow_logs": true,
            "compliance_level": "GDPR",
        },
        EnvVars: map[string]string{
            "AWS_DEFAULT_REGION": awsRegion,
        },
    })
    
    // Cleanup efter test
    defer terraform.Destroy(t, terraformOptions)
    
    // Deploy infrastructure
    terraform.InitAndApply(t, terraformOptions)
    
    // Get output values
    vpcId := terraform.Output(t, terraformOptions, "vpc_id")
    publicSubnetIds := terraform.OutputList(t, terraformOptions, "public_subnet_ids")
    privateSubnetIds := terraform.OutputList(t, terraformOptions, "private_subnet_ids")
    
    // Validate VPC exists och har correct configuration
    vpc := aws.GetVpcById(t, vpcId, awsRegion)
    assert.Equal(t, "10.100.0.0/16", vpc.CidrBlock)
    
    // Validate subnets exist och är correctly configured
    assert.GreaterOrEqual(t, len(publicSubnetIds), 2, "Should have at least 2 public subnets")
    assert.GreaterOrEqual(t, len(privateSubnetIds), 2, "Should have at least 2 private subnets")
    
    // Test subnet connectivity
    for _, subnetId := range publicSubnetIds {
        subnet := aws.GetSubnetById(t, subnetId, awsRegion)
        assert.True(t, subnet.MapPublicIpOnLaunch, "Public subnet should auto-assign public IPs")
    }
    
    // Validate Swedish compliance tags
    validateSwedishComplianceTags(t, vpcId, awsRegion)
    
    // Test security group restrictions
    validateSecurityGroupCompliance(t, vpcId, awsRegion)
    
    // Test data residency compliance
    validateDataResidency(t, vpcId, awsRegion)
}

func validateSwedishComplianceTags(t *testing.T, vpcId string, region string) {
    vpc := aws.GetVpcById(t, vpcId, region)
    
    requiredTags := map[string]string{
        "DataResidency": "Sweden",
        "ComplianceLevel": "GDPR",
        "Environment": "integration-test",
    }
    
    for key, expectedValue := range requiredTags {
        actualValue, exists := vpc.Tags[key]
        assert.True(t, exists, "Required tag %s not found", key)
        assert.Equal(t, expectedValue, actualValue, "Tag %s has incorrect value", key)
    }
}

func validateSecurityGroupCompliance(t *testing.T, vpcId string, region string) {
    // Get all security groups för VPC
    securityGroups := aws.GetSecurityGroupsByVpcId(t, vpcId, region)
    
    for _, sg := range securityGroups {
        // Check ingress rules för compliance violations
        for _, rule := range sg.IngressRules {
            // SSH should not be open till internet
            if rule.FromPort == 22 && contains(rule.CidrBlocks, "0.0.0.0/0") {
                t.Errorf("Security group %s allows SSH from internet - violates Swedish security requirements", sg.GroupId)
            }
            
            // Non-web ports should not be open till internet
            if rule.FromPort != 80 && rule.FromPort != 443 && contains(rule.CidrBlocks, "0.0.0.0/0") {
                t.Errorf("Security group %s allows unrestricted access on non-web port %d", sg.GroupId, rule.FromPort)
            }
        }
    }
}

func validateDataResidency(t *testing.T, vpcId string, region string) {
    // Ensure all resources är created in Swedish/EU regions
    allowedRegions := []string{"eu-north-1", "eu-west-1", "eu-central-1"}
    assert.Contains(t, allowedRegions, region, "VPC created in non-compliant region för Swedish data residency")
}

func contains(slice []string, item string) bool {
    for _, s := range slice {
        if s == item {
            return true
        }
    }
    return false
}
```

**End-to-End Testing**: Validera complete infrastructure workflows:

```python
# End-to-end testing för Swedish infrastructure
import pytest
import boto3
import requests
import time
from typing import Dict, List

class TestSwedishInfrastructureE2E:
    """
    End-to-end tests för complete Swedish infrastructure stack
    """
    
    @pytest.fixture(scope="class")
    def infrastructure_stack(self):
        """Deploy complete infrastructure stack för testing"""
        
        # Deploy infrastructure using Terraform
        import subprocess
        import json
        
        result = subprocess.run([
            "terraform", "apply", "-auto-approve",
            "-var-file=test.tfvars"
        ], capture_output=True, text=True, cwd="terraform/e2e")
        
        if result.returncode != 0:
            pytest.fail(f"Infrastructure deployment failed: {result.stderr}")
        
        # Get outputs
        result = subprocess.run([
            "terraform", "output", "-json"
        ], capture_output=True, text=True, cwd="terraform/e2e")
        
        outputs = json.loads(result.stdout)
        
        yield {
            'load_balancer_dns': outputs['load_balancer_dns']['value'],
            'vpc_id': outputs['vpc_id']['value'],
            'database_endpoint': outputs['database_endpoint']['value'],
            'monitoring_dashboard': outputs['monitoring_dashboard']['value']
        }
        
        # Cleanup
        subprocess.run([
            "terraform", "destroy", "-auto-approve",
            "-var-file=test.tfvars"
        ], cwd="terraform/e2e")
    
    def test_application_accessibility(self, infrastructure_stack):
        """Test that application är accessible via load balancer"""
        
        lb_dns = infrastructure_stack['load_balancer_dns']
        
        # Wait för load balancer to be ready
        max_retries = 30
        för retry in range(max_retries):
            try:
                response = requests.get(f"https://{lb_dns}/health", timeout=10)
                if response.status_code == 200:
                    break
            except requests.RequestException:
                pass
            
            time.sleep(10)
        else:
            pytest.fail("Application not accessible after waiting")
        
        # Test application endpoints
        response = requests.get(f"https://{lb_dns}/health")
        assert response.status_code == 200
        
        health_data = response.json()
        assert health_data['status'] == 'healthy'
        assert 'database' in health_data['checks']
        assert health_data['checks']['database'] == 'connected'
    
    def test_ssl_certificate_validity(self, infrastructure_stack):
        """Test SSL certificate configuration"""
        
        lb_dns = infrastructure_stack['load_balancer_dns']
        
        import ssl
        import socket
        
        context = ssl.create_default_context()
        
        with socket.create_connection((lb_dns, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=lb_dns) as ssock:
                cert = ssock.getpeercert()
                
                # Validate certificate properties
                assert cert['subject'][0][0][1] == lb_dns
                
                # Check that certificate is not expired
                import datetime
                not_after = datetime.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                assert not_after > datetime.datetime.now()
    
    def test_database_connectivity_and_encryption(self, infrastructure_stack):
        """Test database connectivity och encryption"""
        
        import psycopg2
        import os
        
        db_endpoint = infrastructure_stack['database_endpoint']
        
        # Test database connection
        conn = psycopg2.connect(
            host=db_endpoint,
            database=os.getenv('DB_NAME', 'testdb'),
            user=os.getenv('DB_USER', 'testuser'),
            password=os.getenv('DB_PASSWORD'),
            sslmode='require'  # Force SSL
        )
        
        cursor = conn.cursor()
        
        # Test that connection är encrypted
        cursor.execute("SELECT ssl_is_used();")
        ssl_status = cursor.fetchone()[0]
        assert ssl_status is True, "Database connection är not encrypted"
        
        # Test basic database operations
        cursor.execute("CREATE TABLE IF NOT EXISTS test_table (id SERIAL PRIMARY KEY, data TEXT);")
        cursor.execute("INSERT INTO test_table (data) VALUES ('test data');")
        cursor.execute("SELECT data FROM test_table WHERE data = 'test data';")
        
        result = cursor.fetchone()
        assert result[0] == 'test data'
        
        # Cleanup
        cursor.execute("DROP TABLE test_table;")
        conn.commit()
        conn.close()
    
    def test_monitoring_and_alerting(self, infrastructure_stack):
        """Test monitoring dashboard accessibility"""
        
        dashboard_url = infrastructure_stack['monitoring_dashboard']
        
        # Test dashboard accessibility
        response = requests.get(dashboard_url, timeout=10)
        assert response.status_code == 200
        
        # Test that essential metrics är available
        # This would involve checking Grafana API för expected dashboards
        # För brevity, testing basic accessibility here
        assert 'grafana' in response.text.lower() or 'dashboard' in response.text.lower()
    
    def test_compliance_validation(self, infrastructure_stack):
        """Test GDPR och Swedish compliance requirements"""
        
        vpc_id = infrastructure_stack['vpc_id']
        
        # Use boto3 för compliance validation
        ec2 = boto3.client('ec2', region_name='eu-north-1')
        
        # Test VPC tags för compliance
        vpcs = ec2.describe_vpcs(VpcIds=[vpc_id])
        vpc = vpcs['Vpcs'][0]
        
        tags = {tag['Key']: tag['Value'] för tag in vpc.get('Tags', [])}
        
        # Required Swedish compliance tags
        assert tags.get('DataResidency') == 'Sweden'
        assert tags.get('ComplianceLevel') == 'GDPR'
        assert 'Environment' in tags
        
        # Test that all resources är in compliant region
        assert vpc['State'] == 'available'
        
        # Test flow logs för audit compliance
        flow_logs = ec2.describe_flow_logs(
            Filters=[{'Name': 'resource-id', 'Values': [vpc_id]}]
        )
        
        assert len(flow_logs['FlowLogs']) > 0, "VPC Flow Logs not enabled för audit compliance"
```

### Policy as Code validation

Svenska organisationer implement policy validation som integral del av testing strategy:

```rego
# Open Policy Agent (OPA) policies för Swedish compliance
package svenska.security

import rego.v1

# GDPR compliance validation
gdpr_encryption_required if {
    input.resource_type in ["aws_s3_bucket", "aws_rds_instance", "aws_ebs_volume"]
    input.resource_attributes.tags.DataClassification in ["personal", "sensitive"]
    not is_encrypted
}

is_encrypted if {
    input.resource_type == "aws_s3_bucket"
    input.resource_attributes.server_side_encryption_configuration
}

is_encrypted if {
    input.resource_type == "aws_rds_instance" 
    input.resource_attributes.storage_encrypted == true
}

is_encrypted if {
    input.resource_type == "aws_ebs_volume"
    input.resource_attributes.encrypted == true
}

# MSB säkerhetskrav - Network security
network_security_violation if {
    input.resource_type == "aws_security_group"
    rule := input.resource_attributes.ingress_rules[_]
    rule.cidr_blocks[_] == "0.0.0.0/0"
    rule.from_port != 443
    rule.from_port != 80
}

# Data residency validation för Swedish organizations
data_residency_violation if {
    input.resource_type in ["aws_s3_bucket", "aws_rds_instance"]
    input.resource_attributes.tags.DataClassification == "personal"
    not swedish_region_compliant
}

swedish_region_compliant if {
    allowed_regions := {"eu-north-1", "eu-west-1", "eu-central-1"}
    input.resource_attributes.region in allowed_regions
}

# Comprehensive violation check
violations contains violation if {
    gdpr_encryption_required
    violation := {
        "type": "gdpr_encryption_violation",
        "message": "Personal data resources must be encrypted",
        "resource": input.resource_id,
        "regulation": "GDPR Artikel 32"
    }
}

violations contains violation if {
    network_security_violation
    violation := {
        "type": "network_security_violation", 
        "message": "Security groups should not allow unrestricted internet access",
        "resource": input.resource_id,
        "regulation": "MSB säkerhetskrav"
    }
}

violations contains violation if {
    data_residency_violation
    violation := {
        "type": "data_residency_violation",
        "message": "Personal data must remain within Sweden/EU",
        "resource": input.resource_id,
        "regulation": "Svenska dataskyddslagen"
    }
}
```

## Säkerhet by design

Infrastructure as Code möjliggör implementation av security controls från början av development lifecycle istället för som efterhandspåtanke. För svenska organisationer innebär detta systematisk implementation av GDPR requirements, MSB säkerhetskrav och andra compliance frameworks.

### Security automation patterns

**Automated Security Scanning**: Integrera security scanning i CI/CD pipelines för early detection av vulnerabilities:

```yaml
# GitHub Actions workflow för security scanning
name: Infrastructure Security Scan

on:
  pull_request:
    paths: ['terraform/**', 'kubernetes/**']

jobs:
  security-scan:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout kod
      uses: actions/checkout@v4
      
    - name: Setup Terraform
      uses: hashicorp/setup-terraform@v2
      
    - name: Terraform Security Scan med tfsec
      uses: aquasecurity/tfsec-action@v1.0.3
      with:
        working_directory: terraform
        
    - name: Checkov Infrastructure Scan
      uses: bridgecrewio/checkov-action@master
      with:
        directory: terraform
        framework: terraform
        
    - name: OPA Policy Validation
      run: |
        opa fmt --diff policies/
        opa test policies/
        
    - name: Swedish Compliance Check
      run: |
        python scripts/validate_swedish_compliance.py \
          --terraform-dir terraform \
          --policies-dir policies \
          --compliance-frameworks GDPR,MSB
```

**Least Privilege by Default**: Implementera minimal necessary permissions genom Infrastructure as Code:

```hcl
# IAM roles med least privilege för Swedish applications
resource "aws_iam_role" "app_role" {
  name = "svenska-app-execution-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
        Condition = {
          StringEquals = {
            "aws:RequestedRegion" = ["eu-north-1", "eu-west-1"]
          }
        }
      }
    ]
  })
  
  tags = {
    Application = "svenska-app"
    SecurityLevel = "restricted"
    DataAccess = "application-only"
  }
}

# Minimal permissions för application access
resource "aws_iam_policy" "app_policy" {
  name = "svenska-app-minimal-permissions"
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject"
        ]
        Resource = "arn:aws:s3:::svenska-app-data/*"
        Condition = {
          StringEquals = {
            "s3:x-amz-server-side-encryption" = "AES256"
          }
        }
      },
      {
        Effect = "Allow"
        Action = [
          "rds-db:connect"
        ]
        Resource = aws_rds_instance.app_database.arn
        Condition = {
          StringEquals = {
            "rds-db:db-user-name" = "app_user"
          }
        }
      }
    ]
  })
}
```

## Sammanfattning

De grundläggande principerna för Infrastructure as Code - deklarativ approach, idempotens, immutable infrastructure, testbarhet och security by design - utgör grunden för framgångsrik implementation av modern infrastrukturhantering. För svenska organisationer är dessa principer särskilt viktiga eftersom de möjliggör systematisk implementation av compliance requirements samtidigt som de förbättrar operational efficiency och risk management.

Framgångsrik tillämpning av dessa principer kräver både teknisk förståelse och organisatorisk commitment för change management och continuous improvement. Som vi kommer att se i [nästa kapitel om versionhantering](03_kapitel2.md), bygger practical implementation av Infrastructure as Code på robust version control och code management practices som stödjer dessa fundamentala principer.

Svenska organisationer som invest tid i att properly implementera dessa principer från början av sin IaC journey kommer att se significant benefits i form av reduced operational overhead, improved security posture och faster innovation cycles. Investment i solid fundamentals pays dividends through entire infrastructure lifecycle.

## Källor och referenser

- Puppet Labs. "Infrastructure as Code: A Brief Introduction." Puppet Documentation.
- Red Hat. "Infrastructure as Code Principles and Best Practices." Red Hat Developer.
- Google Cloud. "Infrastructure as Code on Google Cloud." Google Cloud Architecture Center.
- HashiCorp. "Terraform Best Practices Guide." HashiCorp Documentation, 2024.
- NIST. "Framework för Improving Critical Infrastructure Cybersecurity." NIST Cybersecurity Framework, 2024.
- AWS. "Security Pillar - AWS Well-Architected Framework." Amazon Web Services, 2024.
- Kubernetes SIG Security. "Pod Security Standards." Kubernetes Documentation, 2024.
- OWASP. "Infrastructure as Code Security Verification Standard." OWASP Foundation, 2024.
- European Banking Authority. "Guidelines on ICT and security risk management." EBA Guidelines, 2024.
- MSB. "Vägledning för informationssäkerhet i kritisk infrastruktur." Myndigheten för samhällsskydd och beredskap, 2024.