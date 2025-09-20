# Microservices-arkitektur som kod

![Microservices-arkitektur](images/diagram_13_kapitel12.png)

Microservices-arkitektur revolutionerar hur stora system designas och implementeras genom att dela upp monolitiska applikationer i mindre, oberoende tjänster. Infrastructure as Code spelar en kritisk roll för att hantera komplexiteten och säkerställa konsistent deployment av distribuerade microservices-system.

## Microservices design principles för IaC

Microservices architecture bygger på principen om loosely coupled, highly cohesive services som kan utvecklas, deployeras och skalas oberoende. Varje service äger sin egen data och business logic, kommunicerar genom well-defined APIs, och kan implementeras med olika teknologier baserat på specific requirements. För svenska organisationer innebär denna arkitektur särskilda fördelar och utmaningar som måste addresseras genom genomtänkt Infrastructure as Code-implementation.

### Svenska organisationers microservices-drivna transformation

Svenska teknikföretag som Spotify, Klarna och King har pioneerat microservices-arkitekturer som möjliggjort global skalning samtidigt som de bibehållit svenska värderingar om quality, sustainability och innovation. Deras framgångar demonstrerar hur Infrastructure as Code kan hantera komplexiteten i distribuerade system medan svenska regulatory requirements som GDPR och PCI-DSS bibehålls.

**Spotify's Squad Model i mikroservice-kontext:**
Spotify utvecklade sitt berömda Squad Model som perfekt alignar med microservices-arkitektur där varje Squad äger end-to-end ansvar för specifika business capabilities. Deras Infrastructure as Code-approach inkluderar:

```hcl
# Spotify-inspired microservice infrastructure
# terraform/spotify-inspired-microservice.tf
locals {
  squad_services = {
    "music-discovery" = {
      squad_name = "Discovery Squad"
      tribe = "Music Experience"
      chapter = "Backend Engineering"
      guild = "Data Engineering"
      business_capability = "Personalized Music Recommendations"
      data_classification = "user_behavioral"
      compliance_requirements = ["GDPR", "Music_Rights", "PCI_DSS"]
    }
    "playlist-management" = {
      squad_name = "Playlist Squad"
      tribe = "Music Experience"
      chapter = "Frontend Engineering"
      guild = "UX Engineering"
      business_capability = "Playlist Creation and Management"
      data_classification = "user_content"
      compliance_requirements = ["GDPR", "Copyright_Law"]
    }
    "payment-processing" = {
      squad_name = "Payments Squad"
      tribe = "Platform Services"
      chapter = "Backend Engineering"
      guild = "Security Engineering"
      business_capability = "Subscription and Payment Processing"
      data_classification = "financial"
      compliance_requirements = ["GDPR", "PCI_DSS", "Svenska_Betaltjänstlagen"]
    }
  }
}

# Microservice infrastructure per squad
module "squad_microservice" {
  source = "./modules/spotify-squad-service"
  
  for_each = local.squad_services
  
  service_name = each.key
  squad_config = each.value
  
  # Svenska infrastructure requirements
  region = "eu-north-1"  # Stockholm för data residency
  backup_region = "eu-west-1"  # Dublin för disaster recovery
  
  # Compliance configuration
  gdpr_compliant = true
  audit_logging = true
  data_retention_years = contains(each.value.compliance_requirements, "PCI_DSS") ? 7 : 3
  
  # Scaling configuration baserat på svenska usage patterns
  scaling_config = {
    business_hours = {
      min_replicas = 3
      max_replicas = 20
      target_cpu = 70
      schedule = "0 7 * * 1-5"  # Måndag-Fredag 07:00 CET
    }
    off_hours = {
      min_replicas = 1
      max_replicas = 5
      target_cpu = 85
      schedule = "0 19 * * 1-5"  # Måndag-Fredag 19:00 CET
    }
    weekend = {
      min_replicas = 2
      max_replicas = 8
      target_cpu = 80
      schedule = "0 9 * * 6-7"  # Helger 09:00 CET
    }
  }
  
  # Squad ownership och contacts
  ownership = {
    squad = each.value.squad_name
    tribe = each.value.tribe
    chapter = each.value.chapter
    guild = each.value.guild
    technical_contact = "${replace(each.value.squad_name, " ", "-")}@spotify.se"
    business_contact = "${each.value.tribe}@spotify.se"
    on_call_schedule = "pagerduty:${each.key}-squad"
  }
  
  tags = {
    Squad = each.value.squad_name
    Tribe = each.value.tribe
    Chapter = each.value.chapter
    Guild = each.value.guild
    BusinessCapability = each.value.business_capability
    DataClassification = each.value.data_classification
    ComplianceRequirements = join(",", each.value.compliance_requirements)
    Country = "Sweden"
    Organization = "Spotify AB"
    Environment = var.environment
    ManagedBy = "Terraform"
  }
}
```

**Klarna's regulated microservices:**
Som licensierad bank måste Klarna implementera microservices med strikt financial compliance. Deras Infrastructure as Code-approach inkluderar automated regulatory reporting och real-time risk monitoring:

```yaml
# klarna-inspired-financial-microservice.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: payment-processing-service
  namespace: klarna-financial-services
  labels:
    regulation-category: "critical-financial"
    business-function: "payment-processing"
    risk-classification: "high"
    data-sensitivity: "financial-pii"
spec:
  project: financial-services
  source:
    repoURL: https://github.com/klarna/financial-microservices
    targetRevision: main
    path: services/payment-processing
    helm:
      values: |
        financialService:
          name: payment-processing
          businessFunction: "Real-time payment processing för svenska e-handel"
          
          # Finansinspektionens krav
          regulatoryCompliance:
            finansinspektionen: true
            psd2: true
            aml: true  # Anti-Money Laundering
            gdpr: true
            pciDss: true
            swiftCompliance: true
            
          # Svenska payment rails integration
          paymentRails:
            bankgirot: true
            plusgirot: true
            swish: true
            bankid: true
            swedishBankingAPI: true
            
          # Risk management för svenska financial regulations
          riskManagement:
            realTimeMonitoring: true
            fraudDetection: "machine-learning"
            transactionLimits:
              daily: "1000000 SEK"
              monthly: "10000000 SEK"
              suspicious: "50000 SEK"
            auditTrail: "immutable-blockchain"
            
          # Svenska customer protection
          customerProtection:
            disputeHandling: true
            chargebackProtection: true
            konsumentverketCompliance: true
            finansiellaKonsumentklagomål: true
            
          security:
            encryption:
              atRest: "AES-256-GCM"
              inTransit: "TLS-1.3"
              keyManagement: "AWS-KMS-Swedish-Residency"
            authentication:
              mfa: "mandatory"
              bankidIntegration: true
              frejaidIntegration: true
            authorization:
              rbac: "granular-financial-permissions"
              policyEngine: "OPA-with-financial-rules"
              
          monitoring:
            sla: "99.99%"
            latency: "<50ms-p95"
            throughput: "10000-tps"
            alerting: "24x7-swedish-team"
            complianceMonitoring: "real-time"
            regulatoryReporting: "automated"
            
          dataManagement:
            residency: "eu-north-1"  # Stockholm
            backupRegions: ["eu-west-1"]  # Dublin endast
            retentionPolicy: "7-years-financial-records"
            anonymization: "automatic-after-retention"
            rightToBeForgotten: "gdpr-compliant"
            
  destination:
    server: https://k8s.klarna.internal
    namespace: financial-services-prod
    
  syncPolicy:
    automated:
      prune: false  # Aldrig automatisk deletion för financial services
      selfHeal: false  # Kräver manual intervention för changes
      
    # Financial services deployment windows
    syncOptions:
    - CreateNamespace=true
    - PrunePropagationPolicy=orphan  # Preserve data during updates
    
  # Extensive pre-deployment compliance validation
  hooks:
  - name: financial-compliance-validation
    template:
      container:
        image: klarna-compliance-validator:latest
        command: ["financial-compliance-check"]
        args: 
        - "--service=payment-processing"
        - "--regulations=finansinspektionen,psd2,aml,gdpr,pci-dss"
        - "--environment=production"
        - "--region=eu-north-1"
        
  - name: risk-assessment
    template:
      container:
        image: klarna-risk-assessor:latest
        command: ["assess-deployment-risk"]
        args:
        - "--service=payment-processing"
        - "--change-category=infrastructure"
        - "--business-impact=critical"
        
  - name: regulatory-approval-check
    template:
      container:
        image: klarna-approval-checker:latest
        command: ["verify-regulatory-approval"]
        args:
        - "--deployment-id={{workflow.name}}"
        - "--requires-finansinspektionen-approval=true"
```

Service boundaries definieras genom domain-driven design principles där varje microservice representerar en bounded context inom business domain. Detta organisational pattern påverkar Infrastructure as Code genom att varje service kräver sin egen infrastructure definition, deployment pipeline, och operational monitoring med särskild hänsyn till svenska organisationers consensus-baserade kultur och starka focus på quality assurance.

### Sustainable microservices för svenska environmental goals

Svenska organisationer prioriterar högt environmental sustainability, vilket kräver att microservices-arkitekturer designas med energy efficiency och carbon footprint i åtanke:

```python
# sustainability/swedish_green_microservices.py
"""
Green microservices optimization för svenska sustainability goals
"""
import asyncio
from datetime import datetime
import boto3
from kubernetes import client, config

class SwedishGreenMicroservicesOptimizer:
    """
    Optimera microservices för svenska environmental sustainability goals
    """
    
    def __init__(self):
        self.k8s_client = client.AppsV1Api()
        self.cloudwatch = boto3.client('cloudwatch', region_name='eu-north-1')
        
        # Svenska green energy availability patterns
        self.green_energy_schedule = {
            "high_renewables": [22, 23, 0, 1, 2, 3, 4, 5],  # Natt när vindkraft dominerar
            "medium_renewables": [6, 7, 18, 19, 20, 21],     # Morgon och kväll
            "low_renewables": [8, 9, 10, 11, 12, 13, 14, 15, 16, 17]  # Dag when demand is högt
        }
        
    async def optimize_for_green_energy(self, microservices_config):
        """
        Optimera microservice scheduling för svenska green energy availability
        """
        
        optimization_plan = {
            "service_schedule": {},
            "energy_savings": {},
            "carbon_reduction": {},
            "cost_impact": {}
        }
        
        for service_name, config in microservices_config.items():
            
            # Analysera service criticality och energy consumption
            criticality = config.get('criticality', 'medium')
            energy_profile = await self._analyze_energy_consumption(service_name)
            
            if criticality == 'low' and energy_profile['consumption'] == 'high':
                # Schedule compute-intensive, non-critical tasks under green energy hours
                optimization_plan["service_schedule"][service_name] = {
                    "preferred_hours": self.green_energy_schedule["high_renewables"],
                    "scaling_strategy": "time_based_green_energy",
                    "energy_source_preference": "renewable_only",
                    "carbon_optimization": True
                }
                
            elif criticality == 'medium':
                # Balance availability med green energy när möjligt
                optimization_plan["service_schedule"][service_name] = {
                    "preferred_hours": self.green_energy_schedule["medium_renewables"],
                    "scaling_strategy": "carbon_aware_scaling",
                    "energy_source_preference": "renewable_preferred",
                    "carbon_optimization": True
                }
                
            else:  # high criticality
                # Maintain availability but optimize när possible
                optimization_plan["service_schedule"][service_name] = {
                    "preferred_hours": "24x7_availability",
                    "scaling_strategy": "availability_first_green_aware",
                    "energy_source_preference": "renewable_when_available",
                    "carbon_optimization": False
                }
                
            # Beräkna potential savings
            optimization_plan["energy_savings"][service_name] = await self._calculate_energy_savings(
                service_name, optimization_plan["service_schedule"][service_name]
            )
            
        return optimization_plan
    
    async def implement_green_scheduling(self, service_name, green_schedule):
        """
        Implementera green energy-aware scheduling för microservice
        """
        
        # Skapa Kubernetes CronJob för green energy scaling
        green_scaling_cronjob = {
            "apiVersion": "batch/v1",
            "kind": "CronJob",
            "metadata": {
                "name": f"{service_name}-green-scaler",
                "namespace": "sustainability",
                "labels": {
                    "app": service_name,
                    "optimization": "green-energy",
                    "country": "sweden",
                    "sustainability": "carbon-optimized"
                }
            },
            "spec": {
                "schedule": self._convert_to_cron_schedule(green_schedule["preferred_hours"]),
                "jobTemplate": {
                    "spec": {
                        "template": {
                            "spec": {
                                "containers": [{
                                    "name": "green-scaler",
                                    "image": "svenska-sustainability/green-energy-scaler:latest",
                                    "env": [
                                        {"name": "SERVICE_NAME", "value": service_name},
                                        {"name": "OPTIMIZATION_STRATEGY", "value": green_schedule["scaling_strategy"]},
                                        {"name": "ENERGY_PREFERENCE", "value": green_schedule["energy_source_preference"]},
                                        {"name": "SWEDEN_GRID_API", "value": "https://api.svenskenergi.se/v1/renewable-percentage"},
                                        {"name": "CARBON_INTENSITY_API", "value": "https://api.electricitymap.org/v3/carbon-intensity/SE"}
                                    ],
                                    "command": ["python3"],
                                    "args": ["/scripts/green_energy_scaler.py"]
                                }],
                                "restartPolicy": "OnFailure"
                            }
                        }
                    }
                }
            }
        }
        
        # Deploy CronJob
        await self._deploy_green_scaling_job(green_scaling_cronjob)
        
    async def monitor_sustainability_metrics(self, microservices):
        """
        Monitor sustainability metrics för svenska environmental reporting
        """
        
        sustainability_metrics = {
            "carbon_footprint": {},
            "energy_efficiency": {},
            "renewable_energy_usage": {},
            "waste_reduction": {},
            "swedish_environmental_compliance": {}
        }
        
        for service_name in microservices:
            
            # Collect carbon footprint data
            carbon_data = await self._collect_carbon_metrics(service_name)
            sustainability_metrics["carbon_footprint"][service_name] = {
                "daily_co2_kg": carbon_data["co2_emissions_kg"],
                "monthly_trend": carbon_data["trend"],
                "optimization_potential": carbon_data["optimization_percentage"],
                "swedish_carbon_tax_impact": carbon_data["co2_emissions_kg"] * 1.25  # SEK per kg CO2
            }
            
            # Energy efficiency metrics
            energy_data = await self._collect_energy_metrics(service_name)
            sustainability_metrics["energy_efficiency"][service_name] = {
                "kwh_per_transaction": energy_data["energy_per_transaction"],
                "pue_score": energy_data["power_usage_effectiveness"],
                "renewable_percentage": energy_data["renewable_energy_percentage"],
                "svenska_energimyndigheten_compliance": energy_data["renewable_percentage"] >= 50
            }
            
            # Swedish environmental compliance
            compliance_status = await self._check_environmental_compliance(service_name)
            sustainability_metrics["swedish_environmental_compliance"][service_name] = {
                "miljömålsystemet_compliance": compliance_status["environmental_goals"],
                "eu_taxonomy_alignment": compliance_status["eu_taxonomy"],
                "naturvårdsverket_reporting": compliance_status["reporting_complete"],
                "circular_economy_principles": compliance_status["circular_economy"]
            }
        
        # Generera sustainability rapport för svenska stakeholders
        await self._generate_sustainability_report(sustainability_metrics)
        
        return sustainability_metrics

# Implementation för Swedish green energy optimization
async def deploy_green_microservices():
    """
    Deploy microservices med svenska sustainability optimization
    """
    
    optimizer = SwedishGreenMicroservicesOptimizer()
    
    # Exempel mikroservices configuration
    microservices_config = {
        "user-analytics": {
            "criticality": "low",
            "energy_profile": "high",
            "business_hours_dependency": False,
            "sustainability_priority": "high"
        },
        "payment-processing": {
            "criticality": "high",
            "energy_profile": "medium",
            "business_hours_dependency": True,
            "sustainability_priority": "medium"
        },
        "recommendation-engine": {
            "criticality": "medium",
            "energy_profile": "high",
            "business_hours_dependency": False,
            "sustainability_priority": "high"
        }
    }
    
    # Optimera för green energy
    optimization_plan = await optimizer.optimize_for_green_energy(microservices_config)
    
    # Implementera green scheduling
    for service_name, schedule in optimization_plan["service_schedule"].items():
        await optimizer.implement_green_scheduling(service_name, schedule)
    
    # Start monitoring
    sustainability_metrics = await optimizer.monitor_sustainability_metrics(
        list(microservices_config.keys())
    )
    
    print("✅ Svenska green microservices optimization deployed")
    print(f"🌱 Estimated CO2 reduction: {sum(s['optimization_potential'] for s in sustainability_metrics['carbon_footprint'].values())}%")
    print(f"⚡ Renewable energy usage: {sum(s['renewable_percentage'] for s in sustainability_metrics['energy_efficiency'].values())/len(sustainability_metrics['energy_efficiency'])}%")
```

Single responsibility principle appliceras på service level, vilket innebär att varje microservice har ett specifikt, väldefinierat ansvar. För Infrastructure as Code betyder detta att infrastructure components också organiseras kring service boundaries, vilket möjliggör independent scaling, deployment, och maintenance av different system parts samtidigt som svenska values om clarity, responsibility och accountability upprätthålls.

## Service discovery och communication patterns

Service discovery mechanisms möjliggör dynamic location och communication mellan microservices utan hard-coded endpoints. Infrastructure as Code implementerar service registries, DNS-based discovery, eller service mesh solutions som automatically handle service location och load balancing med särskild hänsyn till svenska regulatory requirements och high availability standards.

### Svenska enterprise service discovery patterns

Svenska företag kräver robust service discovery som kan hantera både on-premise och cloud-based services samtidigt som GDPR och data residency requirements uppfylls:

```yaml
# Svenska enterprise service discovery med Consul
# consul-config/swedish-enterprise-service-discovery.yaml
global:
  name: consul
  domain: consul
  datacenter: "stockholm-dc1"
  
  # Svenska-specifika konfigurationer
  enterprise:
    licenseSecretName: "consul-enterprise-license"
    licenseSecretKey: "key"
    
  # GDPR-compliant service mesh
  meshGateway:
    enabled: true
    replicas: 3
    
  # Svenska compliance logging
  auditLogs:
    enabled: true
    sinks:
    - type: "file"
      format: "json"
      path: "/vault/audit/consul-audit.log"
      description: "Svenska audit log för compliance"
      retention: "7y"  # Svenska lagkrav
      
  # Integration med svenska identity providers
  acls:
    manageSystemACLs: true
    bootstrapToken:
      secretName: "consul-bootstrap-token"
      secretKey: "token"
      
  # Svenska datacenter configuration  
  federation:
    enabled: true
    primaryDatacenter: "stockholm-dc1"
    primaryGateways:
    - "consul-mesh-gateway.stockholm.svc.cluster.local:443"
    
    # Secondary datacenters för disaster recovery
    secondaryDatacenters:
    - name: "goteborg-dc2"
      gateways: ["consul-mesh-gateway.goteborg.svc.cluster.local:443"]
    - name: "malmo-dc3"
      gateways: ["consul-mesh-gateway.malmo.svc.cluster.local:443"]

# Service registration för svenska microservices
server:
  replicas: 5
  bootstrapExpect: 5
  disruptionBudget:
    enabled: true
    maxUnavailable: 2
    
  # Svenska geographical distribution
  affinity: |
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: "topology.kubernetes.io/zone"
            operator: In
            values:
            - "eu-north-1a"  # Stockholm AZ1
            - "eu-north-1b"  # Stockholm AZ2
            - "eu-north-1c"  # Stockholm AZ3
            
  # Svenska enterprise storage requirements
  storage: "10Gi"
  storageClass: "gp3-encrypted"  # Encrypted storage för compliance
  
  # Enhanced svenska security
  security:
    enabled: true
    encryption:
      enabled: true
      verify: true
      additionalPort: 8301
    serverAdditionalDNSSANs:
    - "consul.stockholm.svenska-ab.internal"
    - "consul.goteborg.svenska-ab.internal"
    - "consul.malmo.svenska-ab.internal"
    
# Client agents för microservice registration
client:
  enabled: true
  grpc: true
  
  # Svenska compliance tagging
  extraConfig: |
    {
      "node_meta": {
        "datacenter": "stockholm-dc1",
        "country": "sweden",
        "compliance": "gdpr",
        "data_residency": "eu",
        "organization": "Svenska AB",
        "environment": "production"
      },
      "services": [
        {
          "name": "svenska-api-gateway",
          "tags": ["api", "gateway", "svenska", "gdpr-compliant"],
          "port": 8080,
          "check": {
            "http": "https://api.svenska-ab.se/health",
            "interval": "30s",
            "timeout": "10s"
          },
          "meta": {
            "version": "1.0.0",
            "team": "Platform Team",
            "compliance": "GDPR,ISO27001",
            "data_classification": "public"
          }
        }
      ]
    }
    
# UI för svenska operators
ui:
  enabled: true
  service:
    type: "LoadBalancer"
    annotations:
      service.beta.kubernetes.io/aws-load-balancer-ssl-cert: "arn:aws:acm:eu-north-1:123456789012:certificate/svenska-consul-cert"
      service.beta.kubernetes.io/aws-load-balancer-backend-protocol: "https"
      service.beta.kubernetes.io/aws-load-balancer-ssl-ports: "https"
      
  # Svenska access control
  ingress:
    enabled: true
    annotations:
      kubernetes.io/ingress.class: "nginx"
      nginx.ingress.kubernetes.io/auth-type: "basic"
      nginx.ingress.kubernetes.io/auth-secret: "svenska-consul-auth"
      nginx.ingress.kubernetes.io/whitelist-source-range: "10.0.0.0/8,192.168.0.0/16"  # Svenska office IPs
    hosts:
    - host: "consul.svenska-ab.internal"
      paths:
      - "/"
    tls:
    - secretName: "svenska-consul-tls"
      hosts:
      - "consul.svenska-ab.internal"
```

Communication patterns mellan microservices inkluderar synchronous REST/gRPC calls för immediate responses och asynchronous messaging för eventual consistency scenarios. Message brokers som Apache Kafka eller RabbitMQ definieras through infrastructure code för reliable, scalable inter-service communication med special consideration för svenska data protection laws.

### Advanced messaging patterns för svenska financial services

För svenska financial services som Klarna och SEB krävs särskilt robust messaging infrastructure som kan hantera high-volume transactions samtidigt som regulatory requirements uppfylls:

```hcl
# Svenska financial messaging infrastructure
# terraform/swedish-financial-messaging.tf
resource "aws_msk_cluster" "svenska_financial_messaging" {
  cluster_name           = "svenska-financial-kafka"
  kafka_version         = "3.4.0"
  number_of_broker_nodes = 6  # 3 AZs x 2 brokers för high availability
  
  broker_node_group_info {
    instance_type   = "kafka.m5.2xlarge"
    client_subnets  = aws_subnet.svenska_private[*].id
    storage_info {
      ebs_storage_info {
        volume_size = 1000  # 1TB per broker för financial transaction logs
        provisioned_throughput {
          enabled = true
          volume_throughput = 250
        }
      }
    }
    
    security_groups = [aws_security_group.svenska_kafka.id]
  }
  
  # Svenska compliance configuration
  configuration_info {
    arn      = aws_msk_configuration.svenska_financial_config.arn
    revision = aws_msk_configuration.svenska_financial_config.latest_revision
  }
  
  # Encryption för GDPR compliance
  encryption_info {
    encryption_at_rest_kms_key_id = aws_kms_key.svenska_financial_encryption.arn
    encryption_in_transit {
      client_broker = "TLS"
      in_cluster    = true
    }
  }
  
  # Enhanced monitoring för financial compliance
  open_monitoring {
    prometheus {
      jmx_exporter {
        enabled_in_broker = true
      }
      node_exporter {
        enabled_in_broker = true
      }
    }
  }
  
  # Svenska financial logging requirements
  logging_info {
    broker_logs {
      cloudwatch_logs {
        enabled   = true
        log_group = aws_cloudwatch_log_group.svenska_kafka_logs.name
      }
      firehose {
        enabled         = true
        delivery_stream = aws_kinesis_firehose_delivery_stream.svenska_financial_logs.name
      }
    }
  }
  
  tags = {
    Name = "Svenska Financial Messaging Cluster"
    Environment = var.environment
    Organization = "Svenska Financial AB"
    DataClassification = "financial"
    ComplianceFrameworks = "GDPR,PCI-DSS,Finansinspektionen"
    AuditRetention = "7-years"
    DataResidency = "Sweden"
    BusinessContinuity = "critical"
  }
}

# Kafka configuration för svenska financial requirements
resource "aws_msk_configuration" "svenska_financial_config" {
  kafka_versions = ["3.4.0"]
  name           = "svenska-financial-kafka-config"
  description    = "Kafka configuration för svenska financial services"
  
  server_properties = <<PROPERTIES
# Svenska financial transaction requirements
auto.create.topics.enable=false
delete.topic.enable=false
log.retention.hours=61320  # 7 years för financial record retention
log.retention.bytes=1073741824000  # 1TB per partition
log.segment.bytes=536870912  # 512MB segments för better management

# Security för svenska financial compliance
security.inter.broker.protocol=SSL
ssl.endpoint.identification.algorithm=HTTPS
ssl.client.auth=required

# Replication för high availability
default.replication.factor=3
min.insync.replicas=2
unclean.leader.election.enable=false

# Performance tuning för high-volume svenska financial transactions
num.network.threads=16
num.io.threads=16
socket.send.buffer.bytes=102400
socket.receive.buffer.bytes=102400
socket.request.max.bytes=104857600

# Transaction support för financial consistency
transaction.state.log.replication.factor=3
transaction.state.log.min.isr=2
PROPERTIES
}

# Topics för olika svenska financial services
resource "kafka_topic" "svenska_financial_topics" {
  for_each = {
    "payment-transactions" = {
      partitions = 12
      replication_factor = 3
      retention_ms = 220752000000  # 7 years i milliseconds
      segment_ms = 604800000      # 1 week
      min_insync_replicas = 2
      cleanup_policy = "compact,delete"
    }
    "compliance-events" = {
      partitions = 6
      replication_factor = 3
      retention_ms = 220752000000  # 7 years för compliance audit
      segment_ms = 86400000       # 1 day
      min_insync_replicas = 2
      cleanup_policy = "delete"
    }
    "customer-events" = {
      partitions = 18
      replication_factor = 3
      retention_ms = 94608000000   # 3 years för customer data (GDPR)
      segment_ms = 3600000        # 1 hour
      min_insync_replicas = 2
      cleanup_policy = "compact"
    }
    "risk-assessments" = {
      partitions = 6
      replication_factor = 3
      retention_ms = 220752000000  # 7 years för risk data
      segment_ms = 86400000       # 1 day
      min_insync_replicas = 2
      cleanup_policy = "delete"
    }
  }
  
  name               = each.key
  partitions         = each.value.partitions
  replication_factor = each.value.replication_factor
  
  config = {
    "retention.ms" = each.value.retention_ms
    "segment.ms" = each.value.segment_ms
    "min.insync.replicas" = each.value.min_insync_replicas
    "cleanup.policy" = each.value.cleanup_policy
    "compression.type" = "snappy"
    "max.message.bytes" = "10485760"  # 10MB för financial documents
  }
}

# Schema registry för svenska financial message schemas
resource "aws_msk_connect_connector" "svenska_schema_registry" {
  name = "svenska-financial-schema-registry"
  
  kafkaconnect_version = "2.7.1"
  
  capacity {
    autoscaling {
      mcu_count    = 2
      min_worker_count = 2
      max_worker_count = 10
      scale_in_policy {
        cpu_utilization_percentage = 20
      }
      scale_out_policy {
        cpu_utilization_percentage = 80
      }
    }
  }
  
  connector_configuration = {
    "connector.class" = "io.confluent.connect.avro.AvroConverter"
    "key.converter" = "org.apache.kafka.connect.storage.StringConverter"
    "value.converter" = "io.confluent.connect.avro.AvroConverter"
    "value.converter.schema.registry.url" = "https://svenska-schema-registry.svenska-ab.internal:8081"
    
    # Svenska financial schema validation
    "value.converter.schema.validation" = "true"
    "schema.compatibility" = "BACKWARD"  # Ensures backward compatibility för financial APIs
    
    # Compliance och audit configuration
    "audit.log.enable" = "true"
    "audit.log.topic" = "svenska-schema-audit"
    "svenska.compliance.mode" = "strict"
    "gdpr.data.classification" = "financial"
    "retention.policy" = "7-years-financial"
  }
  
  kafka_cluster {
    apache_kafka_cluster {
      bootstrap_servers = aws_msk_cluster.svenska_financial_messaging.bootstrap_brokers_tls
      
      vpc {
        security_groups = [aws_security_group.svenska_kafka_connect.id]
        subnets         = aws_subnet.svenska_private[*].id
      }
    }
  }
  
  service_execution_role_arn = aws_iam_role.svenska_kafka_connect.arn
  
  log_delivery {
    worker_log_delivery {
      cloudwatch_logs {
        enabled   = true
        log_group = aws_cloudwatch_log_group.svenska_kafka_connect.name
      }
    }
  }
}
```

API gateways fungerar som unified entry points för external clients och implement cross-cutting concerns som authentication, rate limiting, och request routing. Gateway configurations definieras as code för consistent policy enforcement och traffic management across service topologies med extra focus på svenska privacy laws och consumer protection regulations.

### Intelligent API gateway för svenska e-commerce

Svenska e-commerce företag som H&M och IKEA kräver intelligent API gateways som kan hantera global traffic samtidigt som svenska customer protection laws följs:

```python
# api_gateway/swedish_intelligent_gateway.py
"""
Intelligent API Gateway för svenska e-commerce med GDPR compliance
"""
import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import aioredis
import aioboto3
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx

class SwedishIntelligentAPIGateway:
    """
    Intelligent API Gateway med svenska compliance och customer protection
    """
    
    def __init__(self):
        self.app = FastAPI(
            title="Svenska Intelligent API Gateway",
            description="GDPR-compliant API Gateway för svenska e-commerce",
            version="2.0.0"
        )
        
        # Initialize clients
        self.redis = None
        self.s3_client = None
        self.session = httpx.AsyncClient()
        
        # Svenska compliance configuration
        self.gdpr_config = {
            "data_retention_days": 1095,  # 3 år för e-commerce
            "cookie_consent_required": True,
            "right_to_be_forgotten": True,
            "data_portability": True,
            "privacy_by_design": True
        }
        
        # Swedish consumer protection
        self.konsumentverket_config = {
            "cooling_off_period_days": 14,
            "price_transparency": True,
            "delivery_information_required": True,
            "return_policy_display": True,
            "dispute_resolution": True
        }
        
        # Setup middleware och routes
        self._setup_middleware()
        self._setup_routes()
        self._setup_service_discovery()
        
    async def startup(self):
        """Initialize connections"""
        self.redis = await aioredis.from_url("redis://svenska-redis-cluster:6379")
        session = aioboto3.Session()
        self.s3_client = await session.client('s3', region_name='eu-north-1').__aenter__()
    
    def _setup_middleware(self):
        """Setup middleware för svenska compliance"""
        
        # CORS för svenska domains
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=[
                "https://*.svenska-ab.se",
                "https://*.svenska-ab.com", 
                "https://svenska-ab.se",
                "https://svenska-ab.com"
            ],
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            allow_headers=["*"],
            expose_headers=["X-Svenska-Request-ID", "X-GDPR-Compliant"]
        )
        
        @self.app.middleware("http")
        async def gdpr_compliance_middleware(request: Request, call_next):
            """GDPR compliance middleware"""
            
            # Add svenska request tracking
            request_id = f"se_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(str(request.client.host))}"
            request.state.request_id = request_id
            
            # Check cookie consent för GDPR
            cookie_consent = request.headers.get("X-Cookie-Consent", "false")
            if cookie_consent.lower() != "true" and self._requires_consent(request):
                return await self._handle_missing_consent(request)
            
            # Log för GDPR audit trail
            await self._log_gdpr_request(request)
            
            response = await call_next(request)
            
            # Add svenska compliance headers
            response.headers["X-Svenska-Request-ID"] = request_id
            response.headers["X-GDPR-Compliant"] = "true"
            response.headers["X-Data-Residency"] = "EU"
            response.headers["X-Svenska-Privacy-Policy"] = "https://svenska-ab.se/privacy"
            
            return response
            
        @self.app.middleware("http")
        async def intelligent_routing_middleware(request: Request, call_next):
            """Intelligent routing baserat på svenska traffic patterns"""
            
            # Analyze request för intelligent routing
            routing_decision = await self._make_routing_decision(request)
            request.state.routing = routing_decision
            
            # Apply svenska business hours optimizations
            if self._is_swedish_business_hours():
                request.state.priority = "high"
            else:
                request.state.priority = "normal"
                
            response = await call_next(request)
            
            # Track routing performance
            await self._track_routing_performance(request, response)
            
            return response
    
    def _setup_routes(self):
        """Setup routes för svenska services"""
        
        @self.app.get("/health")
        async def health_check():
            """Health check för svenska monitoring"""
            return {
                "status": "healthy",
                "country": "sweden",
                "gdpr_compliant": True,
                "data_residency": "eu-north-1",
                "svenska_compliance": True,
                "timestamp": datetime.now().isoformat()
            }
            
        @self.app.post("/api/v1/orders")
        async def create_order(request: Request, order_data: dict):
            """Create order med svenska consumer protection"""
            
            # Validate svenska consumer protection requirements
            await self._validate_consumer_protection(order_data)
            
            # Route till appropriate microservice
            service_url = await self._discover_service("order-service")
            
            # Add svenska compliance headers
            headers = {
                "X-Svenska-Request-ID": request.state.request_id,
                "X-Consumer-Protection": "konsumentverket-compliant",
                "X-Cooling-Off-Period": "14-days",
                "X-Data-Classification": "customer-order"
            }
            
            # Forward till order microservice
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{service_url}/orders",
                    json=order_data,
                    headers=headers,
                    timeout=30.0
                )
                
            # Log för svenska audit trail
            await self._log_order_creation(order_data, response.status_code)
            
            return response.json()
            
        @self.app.get("/api/v1/customers/{customer_id}/gdpr")
        async def gdpr_data_export(request: Request, customer_id: str):
            """GDPR data export för svenska customers"""
            
            # Validate customer identity
            await self._validate_customer_identity(request, customer_id)
            
            # Collect data från all microservices
            customer_data = await self._collect_customer_data(customer_id)
            
            # Generate GDPR-compliant export
            export_data = {
                "customer_id": customer_id,
                "export_date": datetime.now().isoformat(),
                "data_controller": "Svenska AB",
                "data_processor": "Svenska AB",
                "legal_basis": "GDPR Article 20 - Right to data portability",
                "retention_period": "3 years from last interaction",
                "data": customer_data
            }
            
            # Store export för audit
            await self._store_gdpr_export(customer_id, export_data)
            
            return export_data
            
        @self.app.delete("/api/v1/customers/{customer_id}/gdpr")
        async def gdpr_data_deletion(request: Request, customer_id: str):
            """GDPR right to be forgotten för svenska customers"""
            
            # Validate deletion request
            await self._validate_deletion_request(request, customer_id)
            
            # Initiate deletion across all microservices
            deletion_tasks = await self._initiate_customer_deletion(customer_id)
            
            # Track deletion progress
            deletion_id = await self._track_deletion_progress(customer_id, deletion_tasks)
            
            return {
                "deletion_id": deletion_id,
                "customer_id": customer_id,
                "status": "initiated",
                "expected_completion": (datetime.now() + timedelta(days=30)).isoformat(),
                "legal_basis": "GDPR Article 17 - Right to erasure",
                "contact": "privacy@svenska-ab.se"
            }
    
    async def _make_routing_decision(self, request: Request) -> Dict:
        """Make intelligent routing decision baserat på svenska patterns"""
        
        # Analyze request characteristics
        client_ip = request.client.host
        user_agent = request.headers.get("User-Agent", "")
        accept_language = request.headers.get("Accept-Language", "")
        
        # Determine if Swedish user
        is_swedish_user = (
            "sv" in accept_language.lower() or
            "sweden" in user_agent.lower() or
            await self._is_swedish_ip(client_ip)
        )
        
        # Business hours detection
        is_business_hours = self._is_swedish_business_hours()
        
        # Route decision
        if is_swedish_user and is_business_hours:
            return {
                "region": "eu-north-1",  # Stockholm
                "priority": "high",
                "cache_strategy": "aggressive",
                "monitoring": "enhanced"
            }
        elif is_swedish_user:
            return {
                "region": "eu-north-1",  # Stockholm
                "priority": "normal",
                "cache_strategy": "standard",
                "monitoring": "standard"
            }
        else:
            return {
                "region": "eu-west-1",  # Dublin
                "priority": "normal",
                "cache_strategy": "standard",
                "monitoring": "basic"
            }
    
    async def _validate_consumer_protection(self, order_data: Dict):
        """Validate svenska consumer protection requirements"""
        
        required_fields = [
            "delivery_information",
            "return_policy",
            "total_price_including_vat",
            "cooling_off_notice",
            "seller_information"
        ]
        
        missing_fields = [field for field in required_fields if field not in order_data]
        
        if missing_fields:
            raise HTTPException(
                status_code=400,
                detail=f"Konsumentverket compliance violation: Missing fields {missing_fields}"
            )
        
        # Validate pricing transparency
        if not order_data.get("price_breakdown"):
            raise HTTPException(
                status_code=400,
                detail="Price breakdown required för svenska consumer protection"
            )
    
    async def _collect_customer_data(self, customer_id: str) -> Dict:
        """Collect customer data från all microservices för GDPR export"""
        
        microservices = [
            "customer-service",
            "order-service", 
            "payment-service",
            "marketing-service",
            "analytics-service"
        ]
        
        customer_data = {}
        
        for service in microservices:
            try:
                service_url = await self._discover_service(service)
                
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        f"{service_url}/customers/{customer_id}/gdpr",
                        timeout=10.0
                    )
                    
                if response.status_code == 200:
                    customer_data[service] = response.json()
                else:
                    customer_data[service] = {"error": f"Service unavailable: {response.status_code}"}
                    
            except Exception as e:
                customer_data[service] = {"error": str(e)}
        
        return customer_data
    
    def _setup_service_discovery(self):
        """Setup service discovery för mikroservices"""
        
        self.service_registry = {
            "customer-service": [
                "https://customer-svc.svenska-ab.internal:8080",
                "https://customer-svc-backup.svenska-ab.internal:8080"
            ],
            "order-service": [
                "https://order-svc.svenska-ab.internal:8080",
                "https://order-svc-backup.svenska-ab.internal:8080"
            ],
            "payment-service": [
                "https://payment-svc.svenska-ab.internal:8080"
            ],
            "marketing-service": [
                "https://marketing-svc.svenska-ab.internal:8080"
            ],
            "analytics-service": [
                "https://analytics-svc.svenska-ab.internal:8080"
            ]
        }
    
    async def _discover_service(self, service_name: str) -> str:
        """Discover healthy service instance"""
        
        instances = self.service_registry.get(service_name, [])
        
        if not instances:
            raise HTTPException(
                status_code=503,
                detail=f"Service {service_name} not available"
            )
        
        # Simple round-robin för now (could be enhanced with health checks)
        import random
        return random.choice(instances)
        
# Kubernetes deployment för Swedish Intelligent API Gateway
svenska_api_gateway_deployment = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: svenska-intelligent-api-gateway
  namespace: api-gateway
  labels:
    app: svenska-api-gateway
    version: v2.0.0
    country: sweden
    compliance: gdpr
spec:
  replicas: 3
  selector:
    matchLabels:
      app: svenska-api-gateway
  template:
    metadata:
      labels:
        app: svenska-api-gateway
        version: v2.0.0
    spec:
      containers:
      - name: api-gateway
        image: svenska-ab/intelligent-api-gateway:v2.0.0
        ports:
        - containerPort: 8080
          name: http
        - containerPort: 8443
          name: https
        env:
        - name: REDIS_URL
          value: "redis://svenska-redis-cluster:6379"
        - name: ENVIRONMENT
          value: "production"
        - name: COUNTRY
          value: "sweden"
        - name: GDPR_COMPLIANCE
          value: "strict"
        - name: DATA_RESIDENCY
          value: "eu-north-1"
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
"""
```

## Data management i distribuerade system

Database per service pattern säkerställer data ownership och isolation mellan microservices. Infrastructure as Code provisions och manages dedicated database instances för varje service, vilket möjliggör independent data schema evolution och technology choices.

Data consistency challenges i distribuerade system addresseras genom eventual consistency patterns och saga patterns för distributed transactions. Infrastructure code implementerar message queues, event stores, och coordination services som support dessa advanced consistency models.

Event-driven architectures leverage asynchronous communication patterns för loose coupling och high scalability. Event streaming platforms och event sourcing mechanisms definieras through infrastructure code för reliable event propagation och system state reconstruction.

## Service mesh implementation

Service mesh infrastructure abstracts network communication concerns från application code genom dedicated infrastructure layer. Istio, Linkerd, eller Consul Connect configurations managed as code för transparent service-to-service communication, security, och observability.

Traffic management policies implement sophisticated routing rules, circuit breakers, retry mechanisms, och canary deployments through declarative configurations. These policies enable fine-grained control över service interactions utan application code modifications.

Security policies för mutual TLS, access control, och audit logging implementeras through service mesh configurations. Zero-trust networking principles enforced through infrastructure code ensure comprehensive security posture för distributed microservices architectures.

## Deployment och scaling strategies

Independent deployment capabilities för microservices kräver sophisticated CI/CD infrastructure som handles multiple services och their interdependencies. Pipeline orchestration tools coordinate deployments while maintaining system consistency och minimizing downtime.

Scaling strategies för microservices include horizontal pod autoscaling baserat på CPU/memory metrics, custom metrics från application performance, eller predictive scaling baserat på historical patterns. Infrastructure code defines scaling policies och resource limits för each service independently.

Blue-green deployments och canary releases implementeras per service för safe deployment practices. Infrastructure as Code provisions parallel environments och traffic splitting mechanisms som enable gradual rollouts med automatic rollback capabilities.

## Monitoring och observability

Distributed tracing systems som Jaeger eller Zipkin track requests across multiple microservices för comprehensive performance analysis och debugging. Infrastructure code provisions tracing infrastructure och configures automatic instrumentation för seamless observability.

Centralized logging aggregates logs från all microservices för unified analysis och troubleshooting. Log shipping, parsing, och indexing infrastructure defined as code för scalable, searchable log management solutions.

Metrics collection för microservices architectures requires service-specific dashboards, alerting rules, och SLA monitoring. Prometheus, Grafana, och AlertManager configurations managed through infrastructure code för consistent monitoring across service portfolio.

## Praktiska exempel

### Kubernetes Microservices Deployment
```yaml
# user-service-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-service
  labels:
    app: user-service
    version: v1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: user-service
  template:
    metadata:
      labels:
        app: user-service
        version: v1
    spec:
      containers:
      - name: user-service
        image: myregistry/user-service:1.2.0
        ports:
        - containerPort: 8080
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: user-db-secret
              key: connection-string
        - name: REDIS_URL
          value: "redis://redis-service:6379"
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
```

```yaml
# user-service-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: user-service
spec:
  selector:
    app: user-service
  ports:
  - port: 80
    targetPort: 8080
  type: ClusterIP
```

### API Gateway Configuration
```yaml
# api-gateway.yaml
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: api-gateway
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - api.company.com
```

```yaml
# api-virtual-service.yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: api-routes
spec:
  hosts:
  - api.company.com
  gateways:
  - api-gateway
  http:
  - match:
    - uri:
        prefix: /users
    route:
    - destination:
        host: user-service
        port:
          number: 80
  - match:
    - uri:
        prefix: /orders
    route:
    - destination:
        host: order-service
        port:
          number: 80
  - match:
    - uri:
        prefix: /payments
    route:
    - destination:
        host: payment-service
        port:
          number: 80
```

### Docker Compose för Development
```yaml
# docker-compose.microservices.yml
version: '3.8'
services:
  user-service:
    build: ./user-service
    ports:
      - "8081:8080"
    environment:
      - DATABASE_URL=postgresql://user:pass@user-db:5432/users
      - REDIS_URL=redis://redis:6379
    depends_on:
      - user-db
      - redis

  order-service:
    build: ./order-service
    ports:
      - "8082:8080"
    environment:
      - DATABASE_URL=postgresql://user:pass@order-db:5432/orders
      - USER_SERVICE_URL=http://user-service:8080
    depends_on:
      - order-db
      - user-service

  payment-service:
    build: ./payment-service
    ports:
      - "8083:8080"
    environment:
      - DATABASE_URL=postgresql://user:pass@payment-db:5432/payments
      - ORDER_SERVICE_URL=http://order-service:8080
    depends_on:
      - payment-db

  api-gateway:
    build: ./api-gateway
    ports:
      - "8080:8080"
    environment:
      - USER_SERVICE_URL=http://user-service:8080
      - ORDER_SERVICE_URL=http://order-service:8080
      - PAYMENT_SERVICE_URL=http://payment-service:8080
    depends_on:
      - user-service
      - order-service
      - payment-service

  user-db:
    image: postgres:14
    environment:
      POSTGRES_DB: users
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - user_data:/var/lib/postgresql/data

  order-db:
    image: postgres:14
    environment:
      POSTGRES_DB: orders
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - order_data:/var/lib/postgresql/data

  payment-db:
    image: postgres:14
    environment:
      POSTGRES_DB: payments
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - payment_data:/var/lib/postgresql/data

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

volumes:
  user_data:
  order_data:
  payment_data:
```

### Terraform för Microservices Infrastructure
```hcl
# microservices-infrastructure.tf
resource "google_container_cluster" "microservices_cluster" {
  name     = "microservices-cluster"
  location = "us-central1"

  remove_default_node_pool = true
  initial_node_count       = 1

  network    = google_compute_network.vpc.name
  subnetwork = google_compute_subnetwork.subnet.name

  addons_config {
    istio_config {
      disabled = false
    }
  }
}

resource "google_sql_database_instance" "user_db" {
  name             = "user-database"
  database_version = "POSTGRES_14"
  region           = "us-central1"

  settings {
    tier = "db-f1-micro"
    
    database_flags {
      name  = "log_statement"
      value = "all"
    }
  }

  deletion_protection = false
}

resource "google_sql_database" "users" {
  name     = "users"
  instance = google_sql_database_instance.user_db.name
}

resource "google_redis_instance" "session_store" {
  name           = "session-store"
  memory_size_gb = 1
  region         = "us-central1"
  
  auth_enabled = true
  transit_encryption_mode = "SERVER_AUTHENTICATION"
}

resource "google_monitoring_alert_policy" "microservices_health" {
  display_name = "Microservices Health Check"
  combiner     = "OR"
  
  conditions {
    display_name = "Service Availability"
    
    condition_threshold {
      filter         = "resource.type=\"k8s_container\""
      comparison     = "COMPARISON_LT"
      threshold_value = 0.95
      duration       = "300s"
      
      aggregations {
        alignment_period   = "60s"
        per_series_aligner = "ALIGN_RATE"
      }
    }
  }
  
  notification_channels = [google_monitoring_notification_channel.email.name]
}
```

## Sammanfattning

Microservices-arkitektur som kod möjliggör skalbar, resilient system design genom Infrastructure as Code practices. Framgångsrik implementation kräver comprehensive consideration av service boundaries, communication patterns, data management, och operational complexity. Modern tools som Kubernetes, service mesh, och cloud-native technologies provide foundational capabilities för sophisticated microservices deployments.

## Källor och referenser

- Martin Fowler. "Microservices Architecture." Martin Fowler's Blog.
- Netflix Technology Blog. "Microservices at Netflix Scale." Netflix Engineering.
- Kubernetes Documentation. "Microservices with Kubernetes." Cloud Native Computing Foundation.
- Istio Project. "Service Mesh for Microservices." Istio Documentation.
- Sam Newman. "Building Microservices: Designing Fine-Grained Systems." O'Reilly Media.