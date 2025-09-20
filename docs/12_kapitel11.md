# Policy och säkerhet som kod i detalj

![Policy och säkerhet som kod](images/diagram_12_kapitel11.png)

*Policy as Code representerar nästa evolutionssteg inom Infrastructure as Code där säkerhet, compliance och governance automatiseras genom programmerbara regler. Diagrammet visar integreringen av policy enforcement i hela utvecklingslivscykeln från design till produktion.*

## Övergripande beskrivning

Policy as Code transformerar hur organisationer hanterar säkerhet och compliance från reaktiva manuella processer till proaktiva automatiserade system. Som vi såg i [kapitel 6 om säkerhet](06_kapitel5.md), är säkerhet en kritisk komponent i Infrastructure as Code, men i detta kapitel fördjupar vi oss i den avancerade implementeringen av policy-drivna säkerhetslösningar.

Traditionella säkerhetsmodeller baserade på manuella granskningar och statiska policydokument är otillräckliga för moderna molnmiljöer som kontinuerligt förändras genom Infrastructure as Code. Policy as Code möjliggör automatisk validering av säkerhetskrav i realtid, kontinuerlig compliance-övervakning och snabb respons på nya hot och regulatoriska förändringar.

Svenska organisationer står inför komplexa compliance-krav inklusive GDPR, MSB:s säkerhesskrav för kritisk infrastruktur, och branschspecifika regleringar. Policy as Code erbjuder en strukturerad approach för att hantera dessa krav genom kodbaserade definitioner som kan versionshanteras, testats och deployeras konsistent över hela organisationen.

Denna djupgående behandling av Policy as Code bygger vidare på grundläggande säkerhetsprinciper från tidigare kapitel och förbereder läsaren för de avancerade compliance- och regelefterlevnadsstrategier som behandlas i [kapitel 14](14_kapitel13.md).

## Open Policy Agent (OPA) och Rego

Open Policy Agent har etablerats som de facto standarden för policy as code implementation genom sin flexibla arkitektur och kraftfulla deklarativa policy-språk Rego. OPA kan integreras i alla stadier av Infrastructure as Code-livscykeln från utvecklingstid genom CI/CD-pipelines till runtime policy enforcement.

Rego-språket möjliggör uttrycksfull och läsbar policy-definition som kan hantera komplexa business logic och regulatory requirements. Policy-utvecklare kan skapa återanvändbara bibliotek av policy-moduler som täcker vanliga säkerhetspattern, compliance-frameworks och organisatoriska standarder.

### Grundläggande Rego-implementation

```rego
# policies/swedish_compliance.rego
package sweden.security

import rego.v1

# GDPR Article 32 - Säkerhet i behandlingen
encryption_required if {
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

# MSB säkerhetskrav - Nätverkssegmentering
network_segmentation_violation if {
    input.resource_type == "aws_security_group"
    rule := input.resource_attributes.ingress_rules[_]
    rule.cidr_blocks[_] == "0.0.0.0/0"
    rule.from_port != 443
    rule.from_port != 80
}

# Svenska datasuveränitetsregler
data_sovereignty_violation if {
    input.resource_type in ["aws_s3_bucket", "aws_rds_instance"]
    input.resource_attributes.tags.DataClassification == "personal"
    not swedish_region_compliant
}

swedish_region_compliant if {
    allowed_regions := {"eu-north-1", "eu-west-1", "eu-central-1"}
    input.resource_attributes.region in allowed_regions
}

# Sammansatt compliance-bedömning
compliance_violations contains violation if {
    encryption_required
    violation := {
        "type": "encryption_required",
        "severity": "high",
        "message": "Persondata måste krypteras enligt GDPR Artikel 32",
        "resource": input.resource_id,
        "remediation": "Aktivera kryptering för denna resurs"
    }
}

compliance_violations contains violation if {
    network_segmentation_violation
    violation := {
        "type": "network_exposure",
        "severity": "critical", 
        "message": "Otillåten nätverksexponering enligt MSB-riktlinjer",
        "resource": input.resource_id,
        "remediation": "Begränsa inkommande trafik till specifika källor"
    }
}

compliance_violations contains violation if {
    data_sovereignty_violation
    violation := {
        "type": "data_sovereignty",
        "severity": "critical",
        "message": "Persondata måste lagras inom EU/Sverige",
        "resource": input.resource_id,
        "remediation": "Flytta resurs till godkänd svensk/EU-region"
    }
}
```

## Gatekeeper och Kubernetes Policy Enforcement

Kubernetes-miljöer kräver specialiserade policy enforcement-mekanismer som kan hantera dynamiska containerbaserade workloads. Gatekeeper, baserat på OPA, tillhandahåller admission control capabilities som validerar Kubernetes-resurser innan de deployeras.

Constraint Templates definierar återanvändbara policy-pattern som kan instansieras med specifika parametrar för olika environments och use cases. Detta möjliggör policy standardisering samtidigt som flexibilitet bibehålls för olika teams och projekt.

### Kubernetes Security Policies

```yaml
# gatekeeper/constraint-template.yaml
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: swedishsecurityrequirements
spec:
  crd:
    spec:
      names:
        kind: SwedishSecurityRequirements
      validation:
        openAPIV3Schema:
          type: object
          properties:
            labels:
              type: array
              items:
                type: string
            maxMemory:
              type: string
            maxCPU:
              type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package swedishsecurityrequirements
        
        import rego.v1
        
        violation[{"msg": msg}] {
          input.review.object.kind == "Pod"
          not input.review.object.metadata.labels["se.gdpr.dataclassification"]
          msg := "Pod måste ha GDPR-dataklassificering enligt svenska regelverk"
        }
        
        violation[{"msg": msg}] {
          input.review.object.kind == "Pod"
          container := input.review.object.spec.containers[_]
          not container.securityContext.runAsNonRoot
          msg := sprintf("Container %v måste köras som non-root enligt MSB-säkerhetskrav", [container.name])
        }
        
        violation[{"msg": msg}] {
          input.review.object.kind == "Pod"
          container := input.review.object.spec.containers[_]
          not container.securityContext.readOnlyRootFilesystem
          msg := sprintf("Container %v måste använda read-only root filesystem", [container.name])
        }

---
apiVersion: config.gatekeeper.sh/v1alpha1
kind: SwedishSecurityRequirements
metadata:
  name: swedish-pod-security
spec:
  match:
    - apiGroups: [""]
      kinds: ["Pod"]
  parameters:
    labels: ["se.gdpr.dataclassification", "se.msb.securityclass"]
    maxMemory: "2Gi"
    maxCPU: "1000m"
```

## Terraform Policy Integration

Terraform policy enforcement implementeras genom flera verktyg och approaches som validerar Infrastructure as Code före deployment. Sentinel policies, HashiCorp Consul-Connect integration och custom policy engines möjliggör comprehensive governance av infrastructure changes.

Terratest frameworks kombinerar policy validation med infrastructure testing för att säkerställa både functional correctness och compliance adherence. Policy-driven testing approaches möjliggör automated validation av komplexa regulatory requirements genom kod.

### Sentinel Policy Implementation

```python
# policies/terraform_validation.py
import json
import subprocess
from typing import Dict, List, Any
import hcl2

class TerraformPolicyValidator:
    """
    Comprehensive policy validation för Terraform configurations
    """
    
    def __init__(self, policy_directory: str = "policies/"):
        self.policy_directory = policy_directory
        self.violation_handlers = {
            "encryption": self._handle_encryption_violation,
            "network_security": self._handle_network_violation,
            "data_sovereignty": self._handle_sovereignty_violation,
            "resource_tagging": self._handle_tagging_violation
        }
    
    def validate_terraform_plan(self, plan_file_path: str) -> Dict[str, Any]:
        """Validera Terraform plan mot svenska compliance-krav"""
        
        # Ladda Terraform plan
        with open(plan_file_path, 'r') as f:
            plan_data = json.load(f)
        
        violations = []
        warnings = []
        
        for resource_change in plan_data.get('resource_changes', []):
            resource_violations = self._validate_resource(resource_change)
            violations.extend(resource_violations)
        
        # Generera compliance rapport
        compliance_report = {
            "timestamp": "2024-01-15T10:30:00Z",
            "plan_file": plan_file_path,
            "total_resources": len(plan_data.get('resource_changes', [])),
            "violations": violations,
            "warnings": warnings,
            "compliance_score": self._calculate_compliance_score(violations),
            "recommendations": self._generate_recommendations(violations)
        }
        
        return compliance_report
    
    def _validate_resource(self, resource_change: Dict) -> List[Dict]:
        """Validera enskild resurs mot policies"""
        violations = []
        resource_type = resource_change.get('type')
        resource_config = resource_change.get('change', {}).get('after', {})
        
        # GDPR-compliance för databaser
        if resource_type in ['aws_rds_instance', 'aws_dynamodb_table']:
            if not self._check_encryption(resource_config):
                violations.append({
                    "type": "encryption_required",
                    "severity": "high",
                    "resource": resource_change.get('address'),
                    "message": "Databas måste ha kryptering aktiverad enligt GDPR",
                    "regulation": "GDPR Artikel 32",
                    "remediation": "Sätt encryption = true för denna resurs"
                })
        
        # Nätverkssäkerhet enligt MSB
        if resource_type == 'aws_security_group':
            network_violations = self._validate_network_security(resource_config)
            violations.extend(network_violations)
        
        # Svenska datasuveränitetskrav
        if resource_type in ['aws_s3_bucket', 'aws_rds_instance']:
            if not self._check_data_sovereignty(resource_config):
                violations.append({
                    "type": "data_sovereignty",
                    "severity": "critical",
                    "resource": resource_change.get('address'),
                    "message": "Resurs måste placeras i svensk/EU-region för persondata",
                    "regulation": "Dataskyddslagen",
                    "remediation": "Använd region eu-north-1 eller eu-west-1"
                })
        
        # Resurstagging för kostnadskontroll
        tagging_violations = self._validate_resource_tagging(resource_config)
        violations.extend(tagging_violations)
        
        return violations
    
    def _validate_network_security(self, security_group_config: Dict) -> List[Dict]:
        """Validera nätverkssäkerhet enligt MSB-riktlinjer"""
        violations = []
        
        for rule in security_group_config.get('ingress', []):
            # Kontrollera för öppna portar från internet
            if '0.0.0.0/0' in rule.get('cidr_blocks', []):
                if rule.get('from_port') not in [80, 443]:
                    violations.append({
                        "type": "network_exposure",
                        "severity": "critical",
                        "message": f"Port {rule.get('from_port')} exponerad mot internet",
                        "regulation": "MSB säkerhetskrav för kritisk infrastruktur",
                        "remediation": "Begränsa access till specifika IP-adresser"
                    })
        
        return violations
    
    def _check_encryption(self, resource_config: Dict) -> bool:
        """Kontrollera om resurs har kryptering aktiverad"""
        # RDS encryption check
        if 'storage_encrypted' in resource_config:
            return resource_config.get('storage_encrypted', False)
        
        # S3 encryption check
        if 'server_side_encryption_configuration' in resource_config:
            return bool(resource_config['server_side_encryption_configuration'])
        
        # EBS encryption check
        if 'encrypted' in resource_config:
            return resource_config.get('encrypted', False)
        
        return False
    
    def _check_data_sovereignty(self, resource_config: Dict) -> bool:
        """Kontrollera datasuveränitet för svenska organisationer"""
        # Lista över godkända regioner för persondata
        approved_regions = {
            'eu-north-1',    # Stockholm
            'eu-west-1',     # Irland
            'eu-central-1'   # Frankfurt
        }
        
        # Kontrollera region setting
        region = resource_config.get('region') or resource_config.get('availability_zone', '').split('-')[0:2]
        if isinstance(region, list):
            region = '-'.join(region)
        
        return region in approved_regions
    
    def _validate_resource_tagging(self, resource_config: Dict) -> List[Dict]:
        """Validera att resurser har korrekt tagging för kostnadskontroll"""
        violations = []
        required_tags = {
            'Project', 'Environment', 'Owner', 'CostCenter', 'DataClassification'
        }
        
        resource_tags = set(resource_config.get('tags', {}).keys())
        missing_tags = required_tags - resource_tags
        
        if missing_tags:
            violations.append({
                "type": "resource_tagging",
                "severity": "medium",
                "message": f"Saknade obligatoriska tags: {', '.join(missing_tags)}",
                "regulation": "Intern policy för kostnadsstyrning",
                "remediation": f"Lägg till tags: {missing_tags}"
            })
        
        return violations
    
    def _calculate_compliance_score(self, violations: List[Dict]) -> float:
        """Beräkna compliance score baserat på violations"""
        if not violations:
            return 100.0
        
        severity_weights = {
            'critical': 25,
            'high': 15,
            'medium': 10,
            'low': 5
        }
        
        total_penalty = sum(
            severity_weights.get(v.get('severity'), 5) 
            for v in violations
        )
        
        # Cap at 0 minimum
        return max(0.0, 100.0 - total_penalty)
    
    def _generate_recommendations(self, violations: List[Dict]) -> List[str]:
        """Generera åtgärdsrekommendationer baserat på violations"""
        recommendations = []
        
        violation_types = set(v.get('type') for v in violations)
        
        if 'encryption_required' in violation_types:
            recommendations.append(
                "Implementera automatisk kryptering för alla databaser och storage genom Terraform modules"
            )
        
        if 'network_exposure' in violation_types:
            recommendations.append(
                "Använd AWS Systems Manager Session Manager istället för direkta SSH-anslutningar"
            )
        
        if 'data_sovereignty' in violation_types:
            recommendations.append(
                "Konfigurera provider alias för att säkerställa deployment i godkända regioner"
            )
        
        if 'resource_tagging' in violation_types:
            recommendations.append(
                "Skapa Terraform locals för standardiserade tags och använd i alla resurser"
            )
        
        return recommendations

def integrate_with_cicd_pipeline():
    """Exempel på CI/CD pipeline integration"""
    
    pipeline_config = """
    # .github/workflows/terraform-policy-validation.yml
    name: Terraform Policy Validation
    
    on:
      pull_request:
        paths: ['infrastructure/**']
    
    jobs:
      policy-validation:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4
          
          - name: Setup Terraform
            uses: hashicorp/setup-terraform@v2
            with:
              terraform_version: 1.6.0
          
          - name: Terraform Plan
            working-directory: infrastructure
            run: |
              terraform init
              terraform plan -out=tfplan.binary
              terraform show -json tfplan.binary > tfplan.json
          
          - name: Policy Validation
            run: |
              python scripts/terraform_policy_validator.py tfplan.json > policy_report.json
          
          - name: Upload Policy Report
            uses: actions/upload-artifact@v3
            with:
              name: policy-compliance-report
              path: policy_report.json
          
          - name: Comment PR
            uses: actions/github-script@v6
            with:
              script: |
                const fs = require('fs');
                const report = JSON.parse(fs.readFileSync('policy_report.json'));
                
                const comment = `
                ## 🔒 Policy Compliance Report
                
                **Compliance Score:** ${report.compliance_score}/100
                **Violations:** ${report.violations.length}
                
                ${report.violations.length > 0 ? '### ⚠️ Policy Violations' : '### ✅ All Policies Passed'}
                
                ${report.violations.map(v => 
                  `- **${v.severity.toUpperCase()}**: ${v.message} (${v.regulation})`
                ).join('\\n')}
                
                ${report.recommendations.length > 0 ? 
                  '### 💡 Recommendations\\n' + 
                  report.recommendations.map(r => `- ${r}`).join('\\n') : ''
                }
                `;
                
                github.rest.issues.createComment({
                  issue_number: context.issue.number,
                  owner: context.repo.owner,
                  repo: context.repo.repo,
                  body: comment
                });
    """
    
    return pipeline_config
```

## Automatiserad Compliance Monitoring

Kontinuerlig compliance monitoring kräver real-time övervakning av infrastrukturtillstånd och automatisk detection av policy violations. Cloud-native monitoring services integreras med policy engines för comprehensive governance capabilities.

Swedish regulatory requirements för logging, audit trails och incident response implementeras genom automated monitoring systems som kan detektera avvikelser och trigga appropriate response actions. Integration med SIEM systems möjliggör correlation av security events med infrastructure changes.

### Compliance Monitoring Dashboard

```python
# monitoring/compliance_dashboard.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import boto3
import json

class SwedishComplianceDashboard:
    """
    Real-time compliance dashboard för svenska säkerhetskrav
    """
    
    def __init__(self):
        self.aws_client = boto3.client('config')
        self.cloudtrail_client = boto3.client('cloudtrail')
        
    def main(self):
        """Huvudfunktion för Streamlit dashboard"""
        st.set_page_config(
            page_title="Svenska Compliance Dashboard",
            page_icon="🔒",
            layout="wide"
        )
        
        st.title("🇸🇪 Svenska Säkerhets- och Compliance Dashboard")
        st.subheader("Infrastructure as Code Compliance Monitoring")
        
        # Sidebar för filterval
        with st.sidebar:
            st.header("Filter")
            time_range = st.selectbox(
                "Tidsperiod",
                ["Senaste 24 timmarna", "Senaste veckan", "Senaste månaden"]
            )
            
            compliance_frameworks = st.multiselect(
                "Compliance Framework",
                ["GDPR", "MSB Säkerhetskrav", "ISO 27001", "SOC 2"],
                default=["GDPR", "MSB Säkerhetskrav"]
            )
        
        # Huvudpaneler
        col1, col2, col3, col4 = st.columns(4)
        
        # Hämta compliance data
        compliance_data = self._get_compliance_metrics()
        
        with col1:
            st.metric(
                "Overall Compliance Score", 
                f"{compliance_data['overall_score']:.1f}%",
                delta=f"{compliance_data['score_change']:+.1f}%"
            )
        
        with col2:
            st.metric(
                "Critical Violations", 
                compliance_data['critical_violations'],
                delta=compliance_data['critical_change']
            )
        
        with col3:
            st.metric(
                "GDPR Compliance", 
                f"{compliance_data['gdpr_score']:.1f}%",
                delta=f"{compliance_data['gdpr_change']:+.1f}%"
            )
        
        with col4:
            st.metric(
                "MSB Compliance", 
                f"{compliance_data['msb_score']:.1f}%",
                delta=f"{compliance_data['msb_change']:+.1f}%"
            )
        
        # Violations timeline
        st.subheader("Policy Violations Over Time")
        violations_df = self._get_violations_timeline()
        
        fig_timeline = px.line(
            violations_df, 
            x='timestamp', 
            y='count',
            color='severity',
            title="Policy Violations per Day"
        )
        st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Compliance breakdown by service
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Compliance by AWS Service")
            service_compliance = self._get_service_compliance()
            
            fig_services = px.bar(
                service_compliance,
                x='service',
                y='compliance_score',
                color='compliance_score',
                color_continuous_scale='RdYlGn',
                title="Service Compliance Scores"
            )
            st.plotly_chart(fig_services, use_container_width=True)
        
        with col2:
            st.subheader("Top Policy Violations")
            top_violations = self._get_top_violations()
            
            for violation in top_violations:
                with st.expander(f"{violation['policy_name']} ({violation['count']} violations)"):
                    st.write(f"**Severity:** {violation['severity']}")
                    st.write(f"**Regulation:** {violation['regulation']}")
                    st.write(f"**Description:** {violation['description']}")
                    st.write(f"**Remediation:** {violation['remediation']}")
        
        # Recent violations table
        st.subheader("Recent Policy Violations")
        recent_violations = self._get_recent_violations()
        
        if not recent_violations.empty:
            st.dataframe(
                recent_violations,
                column_config={
                    "timestamp": st.column_config.DatetimeColumn("Time"),
                    "resource": st.column_config.TextColumn("Resource"),
                    "policy": st.column_config.TextColumn("Policy"),
                    "severity": st.column_config.SelectboxColumn(
                        "Severity",
                        options=["Critical", "High", "Medium", "Low"]
                    ),
                    "status": st.column_config.SelectboxColumn(
                        "Status",
                        options=["Open", "In Progress", "Resolved"]
                    )
                },
                use_container_width=True
            )
        else:
            st.info("Inga policy violations de senaste 24 timmarna! 🎉")
        
        # Remediation recommendations
        st.subheader("Automated Remediation Recommendations")
        recommendations = self._get_remediation_recommendations()
        
        for rec in recommendations:
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{rec['title']}**")
                    st.write(rec['description'])
                with col2:
                    if st.button(f"Apply Fix", key=rec['id']):
                        self._apply_remediation(rec['id'])
                        st.success("Remediation applied!")
                        st.experimental_rerun()
    
    def _get_compliance_metrics(self) -> dict:
        """Hämta compliance metrics från AWS Config"""
        try:
            response = self.aws_client.get_aggregate_compliance_details_by_config_rule(
                ConfigurationAggregatorName='swedish-compliance-aggregator',
                ConfigRuleName='gdpr-encryption-enabled',
                AccountId='123456789012',
                AwsRegion='eu-north-1'
            )
            
            # Simulera data för demonstration
            return {
                'overall_score': 87.3,
                'score_change': +2.1,
                'critical_violations': 3,
                'critical_change': -2,
                'gdpr_score': 91.2,
                'gdpr_change': +1.5,
                'msb_score': 84.7,
                'msb_change': +3.2
            }
        except Exception:
            # Fallback data för demonstration
            return {
                'overall_score': 87.3,
                'score_change': +2.1,
                'critical_violations': 3,
                'critical_change': -2,
                'gdpr_score': 91.2,
                'gdpr_change': +1.5,
                'msb_score': 84.7,
                'msb_change': +3.2
            }
    
    def _get_violations_timeline(self) -> pd.DataFrame:
        """Hämta violations timeline data"""
        dates = pd.date_range(
            start=datetime.now() - timedelta(days=30),
            end=datetime.now(),
            freq='D'
        )
        
        # Simulera violations data
        data = []
        for date in dates:
            for severity in ['Critical', 'High', 'Medium', 'Low']:
                count = max(0, int(10 * (1 + 0.5 * (date.day % 7 - 3))))
                if severity == 'Critical':
                    count = count // 5
                elif severity == 'High':
                    count = count // 3
                elif severity == 'Medium':
                    count = count // 2
                
                data.append({
                    'timestamp': date,
                    'severity': severity,
                    'count': count
                })
        
        return pd.DataFrame(data)
    
    def _get_service_compliance(self) -> pd.DataFrame:
        """Hämta compliance scores per AWS service"""
        services = [
            'EC2', 'S3', 'RDS', 'Lambda', 'VPC', 
            'IAM', 'CloudFormation', 'CloudWatch'
        ]
        
        data = []
        for service in services:
            score = 75 + (hash(service) % 25)  # Simulerad score
            data.append({
                'service': service,
                'compliance_score': score
            })
        
        return pd.DataFrame(data)
    
    def _get_top_violations(self) -> list:
        """Hämta mest frekventa policy violations"""
        return [
            {
                'policy_name': 'GDPR Encryption Required',
                'count': 12,
                'severity': 'High',
                'regulation': 'GDPR Artikel 32',
                'description': 'Databaser med persondata saknar kryptering',
                'remediation': 'Aktivera storage_encrypted = true'
            },
            {
                'policy_name': 'MSB Network Segmentation',
                'count': 8,
                'severity': 'Critical',
                'regulation': 'MSB Säkerhetskrav',
                'description': 'Security groups exponerar portar mot internet',
                'remediation': 'Begränsa ingress till specifika IP-adresser'
            },
            {
                'policy_name': 'Resource Tagging',
                'count': 15,
                'severity': 'Medium',
                'regulation': 'Intern policy',
                'description': 'Resurser saknar obligatoriska tags',
                'remediation': 'Lägg till Project, Environment, Owner tags'
            }
        ]
    
    def _get_recent_violations(self) -> pd.DataFrame:
        """Hämta senaste policy violations"""
        data = [
            {
                'timestamp': datetime.now() - timedelta(hours=2),
                'resource': 'aws_rds_instance.production_db',
                'policy': 'GDPR Encryption Required',
                'severity': 'High',
                'status': 'Open',
                'regulation': 'GDPR Art. 32'
            },
            {
                'timestamp': datetime.now() - timedelta(hours=4),
                'resource': 'aws_security_group.web_sg',
                'policy': 'MSB Network Security',
                'severity': 'Critical',
                'status': 'In Progress',
                'regulation': 'MSB Säkerhetskrav'
            }
        ]
        
        return pd.DataFrame(data)
    
    def _get_remediation_recommendations(self) -> list:
        """Hämta automated remediation recommendations"""
        return [
            {
                'id': 'encrypt_rds_1',
                'title': 'Enable RDS Encryption',
                'description': 'Automatically enable encryption for RDS instance prod-db-1',
                'automation': 'terraform apply -target=aws_rds_instance.prod_db'
            },
            {
                'id': 'fix_sg_2',
                'title': 'Restrict Security Group',
                'description': 'Remove 0.0.0.0/0 ingress rule from web-security-group',
                'automation': 'aws ec2 revoke-security-group-ingress --group-id sg-123'
            }
        ]
    
    def _apply_remediation(self, remediation_id: str):
        """Apply automated remediation"""
        # Implementation would trigger actual remediation
        pass

if __name__ == "__main__":
    dashboard = SwedishComplianceDashboard()
    dashboard.main()
```

## Praktiska implementationsexempel

Verkliga implementationer av Policy as Code kräver integration med befintliga utvecklingsverktyg och processer. Genom att bygga policy validation i CI/CD pipelines säkerställs att compliance kontrolleras automatiskt innan infrastrukturändringar deployeras till produktion.

Enterprise-grade policy management inkluderar policy lifecycle management, version control av policies, och comprehensive audit trails av policy decisions. Detta möjliggör organizations att demonstrate compliance mot regulators och maintain consistent governance across complex infrastructure environments.

## Sammanfattning

Policy as Code representerar kritisk evolution inom Infrastructure as Code som möjliggör automated governance, security enforcement och regulatory compliance. Genom att behandla policies som kod kan organisationer uppnå samma fördelar som IaC erbjuder: version control, testing, automation och consistency.

Svenska organisationer som implementerar comprehensive Policy as Code capabilities positionerar sig starkt för future regulatory changes och growing compliance requirements. Investment i policy automation delivers compounding benefits genom reduced manual oversight, faster compliance responses och improved security posture.

Integration med nästa kapitels diskussion om [compliance och regelefterlevnad](14_kapitel13.md) bygger vidare på dessa tekniska foundations för att adressera organizational och processaspekter av comprehensive governance strategy.

## Källor och referenser

- Open Policy Agent. "Policy as Code Documentation." OPA Community, 2023.
- Kubernetes SIG Security. "Gatekeeper Policy Engine." CNCF Projects, 2023.  
- HashiCorp. "Sentinel Policy Framework." HashiCorp Enterprise, 2023.
- NIST. "Security and Privacy Controls för Information Systems." NIST Special Publication 800-53, 2023.
- European Union. "General Data Protection Regulation Implementation Guide." EU Publications, 2023.
- MSB. "Säkerhetskrav för kritisk infrastruktur." Myndigheten för samhällsskydd och beredskap, 2023.