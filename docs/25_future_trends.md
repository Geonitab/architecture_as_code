# Future Trends and Development in Architecture as Code {#future-trends}

## Introduction

Architecture as Code stands at the threshold of comprehensive transformation driven by advances in artificial intelligence, quantum research, distributed infrastructure, and sustainability. The discipline has matured from foundational automation towards a strategic capability that binds technology, governance, and organisational design into a single codified practice. Looking ahead, Architecture as Code will be shaped by systems that learn continuously, platforms that provide seamless developer experiences, and governance models that express policies as executable artefacts.

The future will be characterised by intelligent automation capable of making complex decisions based on historical data, real-time metrics, and predictive analysis. Machine learning models will optimise resource allocation, anticipate system failures, and implement security improvements without the need for constant human intervention. Organisations therefore need flexible architectures, clear strategic intent, and teams that are prepared to iterate as new technologies mature.

Sustainability and ethical stewardship are equally pressing drivers. Carbon-aware computing, renewable energy optimisation, and circular economy principles are moving from optional considerations to core design requirements. Architecture as Code provides the tooling and repeatable processes necessary to embed these commitments into everyday operations, ensuring that future infrastructure is not only efficient but also responsible.

## Emerging Technology Drivers

### Artificial Intelligence and Machine Learning Integration

Artificial intelligence transforms reactive infrastructure into proactive ecosystems. Predictive scaling uses historical datasets and machine learning models to anticipate capacity requirements and to scale resources before demand spikes occur. Anomaly detection systems powered by unsupervised learning identify unusual patterns that may indicate security threats, performance degradation, or configuration drift, triggering automated remediation routines based on defined policies.

Advanced AI services extend optimisation across performance, cost, resilience, and environmental impact. These services ingest observability data, apply reinforcement learning or optimisation heuristics, and propose or execute configuration changes. The result is infrastructure that adjusts to business cycles, regulatory obligations, and sustainability targets without sacrificing stability or transparency.

European organisations operate within a structured regulatory environment shaped by the EU AI Act (Regulation (EU) 2024/1689), in force since 1 August 2024 with its obligations phased in over the following years, which establishes a risk-based framework for artificial intelligence systems [Source [125]](33_references.md#source-125). Architecture as Code implementations must account for transparency requirements, human oversight mechanisms, and documentation obligations prescribed by the regulation. Organisations participating in EU-funded programmes such as Horizon Europe and the Digital Europe Programme gain access to collaborative research initiatives, shared datasets, and interoperable AI platforms that accelerate responsible innovation whilst maintaining compliance with European ethical standards.

### Quantum Computing and Security Evolution

The emergence of quantum capabilities necessitates a re-evaluation of cryptographic choices and automation practices. Post-quantum algorithms must become standard components of infrastructure definitions to ensure long-term resilience. NIST published the first three post-quantum cryptographic standards on 13 August 2024, and organisations should evaluate them for inclusion in their Architecture as Code baselines:

- **ML-KEM** (Module-Lattice-Based Key Encapsulation Mechanism, formerly CRYSTALS-Kyber), standardised as FIPS 203 — the primary algorithm for key encapsulation and key establishment.
- **ML-DSA** (Module-Lattice-Based Digital Signature Algorithm, formerly CRYSTALS-Dilithium), standardised as FIPS 204 — the primary algorithm for digital signatures.
- **SLH-DSA** (Stateless Hash-Based Digital Signature Algorithm, formerly SPHINCS+), standardised as FIPS 205 — a hash-based signature scheme providing diversity against lattice-based attack advances.

The list is not closed: in March 2025 NIST selected HQC, a code-based scheme, as a backup key-encapsulation mechanism alongside ML-KEM, and standardisation of the Falcon signature algorithm (FN-DSA) is still under way. During the transition, hybrid patterns that combine classical and quantum-safe methods will allow organisations to protect sensitive workloads while migration plans mature; NIST's draft transition plan (NIST IR 8547) identifies the quantum-vulnerable standards to be retired and proposes a timetable for their deprecation and eventual disallowance [Source [122]](33_references.md#source-122).

European organisations benefit from collaborative quantum computing programmes that provide shared infrastructure and research capabilities. The **EU Quantum Flagship** initiative brings together research institutions, industry partners, and member states to accelerate quantum technology development across Europe. This €1 billion programme provides organisations with access to quantum computing testbeds, post-quantum cryptography research, and standardisation efforts that support infrastructure modernisation.

The **European Quantum Communication Infrastructure (EuroQCI)** initiative establishes secure quantum communication networks across EU member states, enabling ultra-secure data transmission based on quantum key distribution. Architecture as Code implementations can leverage EuroQCI endpoints for critical communications, embedding quantum-safe channels into declarative infrastructure patterns. This pan-European infrastructure ensures that security architectures remain resilient against quantum threats whilst maintaining interoperability across national boundaries.

Collaboration with **EuroHPC Joint Undertaking** testbeds enables organisations to explore hybrid classical-quantum workload orchestration within shared European infrastructure. These facilities provide production-grade environments where Architecture as Code workflows can orchestrate interactions between quantum accelerators and traditional compute resources, abstracting specialised hardware behind automated pipelines and reusable modules. Quantum algorithms can tackle complex scheduling, routing, and resource allocation problems that challenge classical systems, offering novel optimisation strategies for European organisations.

Security and cryptography guidance aligns with recommendations from **ENISA** (European Union Agency for Cybersecurity), whose 2021 study surveys the post-quantum candidates and mitigation options [Source [126]](33_references.md#source-126), and with the **European Commission's post-quantum cryptography transition roadmap**, set in motion by its Recommendation of 11 April 2024 [Source [127]](33_references.md#source-127). These frameworks provide actionable guidance for migrating to quantum-resistant algorithms, assessing cryptographic agility, and maintaining security postures during the multi-year transition to post-quantum standards. By codifying these migration strategies within Infrastructure as Code patterns, organisations ensure consistent implementation of quantum-safe cryptography across their EU deployments.

### Edge Computing and Distributed Infrastructure

The shift from centralised data centres to distributed edge resources changes how infrastructure is designed and governed. Edge platforms bring processing closer to data sources and users, reducing latency for real-time applications such as industrial automation, immersive media, and critical communications. Architecture as Code must therefore manage fleets of heterogeneous devices, dynamic network conditions, and context-aware policies.

Fifth-generation (5G) networks reinforce this trend by enabling near-real-time orchestration. Autonomous edge nodes interpret declarative policies, adapt to local conditions, and synchronise with central systems when connectivity allows. Declarative blueprints, robust secret management, and consistent observability pipelines are essential to maintain reliability across diverse geographies.

### Environmental Sustainability and Green Computing

Environmental sustainability is becoming a pivotal design factor, driven by policy frameworks such as the European Union's Green Deal. The EU Green Deal establishes ambitious targets for carbon neutrality by 2050 and provides a comprehensive regulatory foundation for sustainable infrastructure practices. Architecture as Code enables organisations to align technical decisions with these commitments by encoding energy profiles, emissions budgets, and compliance thresholds directly into infrastructure definitions.

Carbon-aware scheduling shifts compute-intensive workloads to time periods and regions with cleaner energy mixes, while adaptive cooling policies respond to weather and grid signals. By integrating real-time carbon intensity data from EU electricity grids, infrastructure can automatically migrate non-critical workloads to zones with higher renewable energy availability. The Green Software Foundation's Software Carbon Intensity specification, published as ISO/IEC 21031:2024, gives teams a consistent way to score the effect of such decisions [Source [120]](33_references.md#source-120). This approach supports both environmental responsibility and regulatory compliance across EU member states.

European leadership in sustainable computing is exemplified by the Climate Neutral Data Centre Pact, the self-regulatory initiative of CISPE and EUDCA in which signatory operators commit to making their data centres climate neutral by 2030. European datacentres increasingly leverage renewable energy sources, advanced cooling technologies including free cooling and liquid immersion, and heat reuse strategies that channel waste heat into district heating networks. The EU Code of Conduct for Energy Efficiency in Data Centres provides benchmarking frameworks that organisations can reference when selecting hosting providers and designing infrastructure policies.

Circular economy principles extend the lifecycle of hardware and software components. Automated asset registries track utilisation, maintenance, and retirement criteria; orchestration pipelines rebalance workloads to maximise efficiency; and observability platforms provide the data foundation required to demonstrate progress towards sustainability pledges. These capabilities align with the EU's Circular Economy Action Plan and EU Taxonomy requirements, ensuring that infrastructure investments contribute to resource efficiency and waste reduction targets.

#### Carbon-Aware Infrastructure Implementation

The following example demonstrates a carbon-aware scheduling system that selects optimal EU regions based on real-time carbon intensity data. It maps AWS EU regions to the national grid zones used by the Electricity Maps API—the same kind of signal that the Green Software Foundation's Carbon Aware SDK exposes to schedulers [Source [121]](33_references.md#source-121)—and falls back to indicative values when live data are unavailable:

```python
# sustainability/carbon_aware_scheduling.py
import os
import requests
from datetime import datetime, timezone
from typing import Dict, Optional

class CarbonAwareScheduler:
    """
    Carbon-aware infrastructure scheduling for EU organisations
    Implements EU Green Deal aligned workload placement
    """
    
    def __init__(self):
        # Documented base URL of the Electricity Maps API (v3)
        self.electricity_maps_api = "https://api.electricitymaps.com/v3"
        # AWS EU regions mapped to the Electricity Maps zone of the national
        # grid that powers them. The renewable ratios are indicative fallback
        # values only; live API data supersede them whenever available.
        self.eu_regions = {
            'eu-north-1':   {'location': 'Europe (Stockholm)', 'zone': 'SE', 'typical_renewable_ratio': 0.70},
            'eu-west-1':    {'location': 'Europe (Ireland)',   'zone': 'IE', 'typical_renewable_ratio': 0.40},
            'eu-west-3':    {'location': 'Europe (Paris)',     'zone': 'FR', 'typical_renewable_ratio': 0.25},
            'eu-central-1': {'location': 'Europe (Frankfurt)', 'zone': 'DE', 'typical_renewable_ratio': 0.50},
            'eu-south-1':   {'location': 'Europe (Milan)',     'zone': 'IT', 'typical_renewable_ratio': 0.40},
            'eu-south-2':   {'location': 'Europe (Spain)',     'zone': 'ES', 'typical_renewable_ratio': 0.50},
        }
        
    def _fetch(self, path: str, zone: str) -> Optional[Dict]:
        """Call one Electricity Maps endpoint for a zone; None on any failure"""
        try:
            response = requests.get(
                f"{self.electricity_maps_api}{path}",
                params={'zone': zone},
                headers={'auth-token': os.environ.get('ELECTRICITY_MAPS_API_KEY', '')},
                timeout=10,
            )
            if response.status_code == 200:
                return response.json()
        except requests.RequestException:
            pass
        return None

    def get_carbon_intensity(self, region: str) -> Dict:
        """Fetch real-time carbon intensity and renewable share for an EU region"""
        
        if region not in self.eu_regions:
            raise ValueError(f"Unknown region {region!r}: add it to eu_regions first")
        zone = self.eu_regions[region]['zone']
        
        # carbonIntensity is served by /carbon-intensity/latest, whereas the
        # renewable share is only exposed by /power-breakdown/latest
        intensity = self._fetch("/carbon-intensity/latest", zone)
        breakdown = self._fetch("/power-breakdown/latest", zone)
        
        if (intensity and intensity.get('carbonIntensity') is not None
                and breakdown and breakdown.get('renewablePercentage') is not None):
            return {
                'carbon_intensity': intensity['carbonIntensity'],
                'renewable_ratio': breakdown['renewablePercentage'] / 100,
                'timestamp': intensity.get('datetime'),
                'zone': zone,
                'source': 'electricity-maps'
            }
        
        # Fallback to indicative values when live data are unavailable
        return {
            'carbon_intensity': 300,
            'renewable_ratio': self.eu_regions[region]['typical_renewable_ratio'],
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'zone': zone,
            'source': 'fallback'
        }
    
    def schedule_carbon_aware_workload(self, workload_config: Dict) -> Dict:
        """Schedule workload based on carbon intensity across EU regions"""
        
        region_analysis = {}
        for region in self.eu_regions.keys():
            carbon_data = self.get_carbon_intensity(region)
            
            # Calculate carbon score (lower is better)
            carbon_score = (
                carbon_data['carbon_intensity'] * 0.7 +
                (1 - carbon_data['renewable_ratio']) * 100 * 0.3
            )
            
            region_analysis[region] = {
                'carbon_intensity': carbon_data['carbon_intensity'],
                'renewable_ratio': carbon_data['renewable_ratio'],
                'carbon_score': carbon_score,
                'location': self.eu_regions[region]['location']
            }
        
        # Select most sustainable region
        best_region = min(region_analysis.items(), 
                         key=lambda x: x[1]['carbon_score'])
        
        return {
            'recommended_region': best_region[0],
            'carbon_intensity': best_region[1]['carbon_intensity'],
            'renewable_ratio': best_region[1]['renewable_ratio'],
            'location': best_region[1]['location'],
            'terraform_config': self._generate_terraform_config(
                best_region[0], workload_config
            )
        }
    
    def _generate_terraform_config(self, region: str, 
                                   workload_config: Dict) -> str:
        """Generate Terraform configuration for carbon-optimised deployment"""
        
        return f'''
# Carbon-aware infrastructure deployment aligned with EU Green Deal
terraform {{
  required_providers {{
    aws = {{
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }}
  }}
}}

provider "aws" {{
  region = "{region}"
  
  default_tags {{
    tags = {{
      CarbonOptimised        = "true"
      SustainabilityPolicy   = "eu-green-deal-aligned"
      RegionSelection        = "renewable-energy-optimised"
      ComplianceFramework    = "EU-Green-Deal"
    }}
  }}
}}

# Latest Amazon Linux 2023 image available in the selected region
data "aws_ami" "eu_optimised" {{
  most_recent = true
  owners      = ["amazon"]

  filter {{
    name   = "name"
    values = ["al2023-ami-2023.*-x86_64"]
  }}
}}

# EC2 instances optimised for energy efficiency
resource "aws_instance" "carbon_optimised" {{
  count         = {workload_config.get('instance_count', 2)}
  ami           = data.aws_ami.eu_optimised.id
  instance_type = "{workload_config.get('instance_type', 't3.medium')}"
  
  # Use spot instances for cost and sustainability
  instance_market_options {{
    market_type = "spot"
  }}
  
  tags = {{
    Name                = "carbon-optimised-worker-${{count.index + 1}}"
    EUGreenDealAligned = "true"
  }}
}}

# Scheduled scaling for the carbon-aware autoscaling group. The group itself
# (aws_autoscaling_group.carbon_aware) is defined in the shared baseline
# module and omitted here for brevity.
resource "aws_autoscaling_schedule" "scale_down_high_carbon" {{
  scheduled_action_name  = "scale-down-high-carbon-periods"
  min_size              = 1
  max_size              = 3
  desired_capacity      = 1
  autoscaling_group_name = aws_autoscaling_group.carbon_aware.name
  
  # Schedule can be adjusted based on regional carbon intensity patterns
  recurrence = "0 18 * * *"  # Example: scale down during high-carbon periods
}}
'''
```

This implementation demonstrates how organisations can integrate EU-wide carbon intensity data into infrastructure provisioning decisions. The region-to-zone mapping can be extended to other regions and providers, supporting the portability and compliance requirements established by the EU Green Deal framework. The generated Terraform is deliberately an excerpt: the AMI data source is declared, whereas the autoscaling group that the schedule targets is assumed to come from the shared baseline module.

## Platform Engineering and Developer Experience

Platform engineering is evolving into a distinct discipline that provides curated experiences, reliable self-service capabilities, and compliant pathways for delivering change, as the CNCF Platforms White Paper describes [Source [129]](33_references.md#source-129). Golden paths encapsulate reference architectures, security controls, and automated quality gates. When codified as reusable modules, these pathways reduce cognitive load for delivery teams and shorten the time between an idea and production deployment.

Modern platforms couple this experience layer with feedback mechanisms that monitor developer productivity, governance adherence, and customer outcomes. Architecture as Code ensures that platform enhancements are versioned, tested, and reviewable. The resulting operating model allows organisations to evolve their capabilities quickly without compromising on auditability or resilience.

## Financial Stewardship and FinOps Evolution

FinOps practices, as codified in the FinOps Foundation's framework [Source [124]](33_references.md#source-124), are maturing in parallel with technical automation. Instead of reacting to invoices, organisations are embedding real-time cost telemetry, emissions reporting, and budget guardrails into their Architecture as Code pipelines. Intelligent policies highlight underused resources, compare purchasing options, and recommend rightsizing actions while balancing availability and compliance.

This financial observability extends to sustainability metrics, turning carbon accounting into an operational concern rather than an annual report. Teams make informed trade-offs between cost, performance, and environmental impact, guided by dashboards and automated insights that are derived from the same declarative definitions used to provision infrastructure.

Market signals reinforce the need for this financial discipline. MarketsandMarkets (2022) [Source [47]](33_references.md#source-47) projected that the Infrastructure as Code market would grow from USD 0.8 billion in 2022 to USD 2.3 billion by 2027—equating to roughly 24 per cent compound annual growth—a forecast whose horizon is now close. Gartner's press release of 13 November 2023 forecast worldwide public cloud end-user spending of USD 678.8 billion in 2024, an increase of 20.4 per cent [Source [45]](33_references.md#source-45); its November 2024 update put 2024 at USD 595.7 billion and forecast USD 723.4 billion for 2025 [Source [46]](33_references.md#source-46). Together these analyses confirm that executive teams expect Architecture as Code programmes to convert rising automation budgets into measurable efficiency, regulatory resilience, and sustainability outcomes.

## Advanced GitOps and Automation Patterns

GitOps principles continue to expand beyond continuous delivery. Multi-cluster orchestration coordinates deployments across distributed estates, ensuring that security patches and configuration updates propagate reliably. Data platforms increasingly adopt GitOps practices to manage pipelines, schemas, and governance policies, aligning analytics operations with infrastructure automation.

Progressive delivery techniques—such as feature flags, automated canaries, and policy-as-code approvals—are now bundled with Architecture as Code workflows. These capabilities provide a controlled mechanism for experimentation while preserving audit trails. The convergence of GitOps, policy engines, and event-driven automation ensures that changes are safe, reversible, and observable.

## Security, Privacy, and Regulatory Evolution

Zero-trust principles are becoming default assumptions. Identity-centric controls extend to machines, services, and data flows, with micro-segmentation expressed through reusable templates. Continuous verification combines runtime attestation, behavioural analytics, and automated enforcement to maintain confidence in every interaction.

Privacy-by-design requires consent management, data minimisation, and lifecycle governance to be embedded directly into code. Regulatory technology (RegTech) integrations supply real-time oversight by reconciling infrastructure states against legislative requirements. Automated reporting, backed by immutable logs, simplifies audits and demonstrates compliance to international regulators and partners.

## Organisation and Workforce Transformation

Future-ready organisations adopt remote-first and hybrid operating models supported by cloud-native collaboration tools. Architecture as Code contributes by ensuring that environments can be provisioned consistently regardless of geography, enabling asynchronous operations that span time zones and cultures. Teams focus on strategic design and oversight while automation handles routine provisioning, compliance checks, and recovery procedures.

Skills transformation remains critical. Platform engineers, infrastructure developers, and DevSecOps practitioners require fluency in software engineering, automation tooling, and data-driven decision-making. Continuous learning programmes, mentorship, and communities of practice sustain these competencies as new technologies emerge. Human-centred leadership emphasises psychological safety, inclusive decision-making, and ethical considerations when deploying autonomous systems.

## Architectural Innovation Horizons

Serverless computing is expanding beyond stateless functions into container-based services, event-driven automation, and managed data stores that eliminate much of the operational overhead traditionally associated with infrastructure. Architecture as Code allows teams to express these patterns declaratively, orchestrating integrations between serverless offerings and existing platforms.

Infrastructure mesh concepts apply service-mesh thinking to the infrastructure layer, providing consistent policy enforcement, observability, and connectivity across clouds and on-premises estates. Immutable infrastructure principles extend from images and deployment artefacts to networking, policy definitions, and even data pipelines, ensuring that every change is implemented through version-controlled updates rather than mutable configuration.

## Cloud and Digital Sovereignty in Europe

Digital sovereignty is gaining prominence as organisations seek control over data residency, privacy, and supply-chain risk. European initiatives such as Gaia-X provide federated infrastructure frameworks that enable organisations to maintain sovereignty whilst benefiting from cloud scalability. Gaia-X's data space model supports interoperability between European cloud providers, reducing vendor lock-in and ensuring compliance with EU regulations including GDPR and the Data Governance Act.

Chapter 15 outlines how multi-region design, egress budgeting, and FinOps automation keep sovereignty-aligned estates financially sustainable. Future-ready teams should unite those practices with sovereignty guardrails by codifying residency rules, approved EU providers, and cross-border data exchange limits directly in policy modules. This harmonised approach keeps cost optimisation, compliance, and sovereignty obligations synchronised across Architecture as Code pipelines.

Architecture as Code enables transparent choices about hosting locations, encryption standards, and vendor dependencies. European organisations can leverage multiple cloud providers—ranging from EU-headquartered platforms such as OVHcloud, Scaleway, and Open Telekom Cloud to the EU sovereign offerings of global hyperscalers (the AWS European Sovereign Cloud, generally available since January 2026; the EU Data Boundary for the Microsoft Cloud; or Google Cloud's Sovereign Controls by Partners and Data Boundary offerings)—whilst policy modules automatically decline services that fall outside those safeguards. Codifying these distinctions keeps residency, contractual requirements, and lawful access controls aligned across delivery pipelines.

International collaboration across industry consortia, open-source communities, and regulatory alliances drives interoperability and shared innovation. Programmes such as the European Cloud Initiative, Digital Europe Programme, and Horizon Europe funding streams support collaborative research and development in cloud-native architectures. Codified architectures provide the lingua franca for these partnerships, allowing patterns to be exchanged, audited, and improved collectively across European and global organisations.

## Implementation Strategies for Future Readiness

### Building Adaptive Capabilities

Preparing for the future requires investment in adaptive capabilities rather than a reliance on individual technologies. Flexible architectures, modular codebases, and automated testing create a foundation that can absorb new paradigms with minimal disruption. Rich observability data and telemetry pipelines underpin experimentation, enabling teams to iterate confidently.

### Skills Development and Organisational Adaptation

Technical excellence must be matched by cultural evolution. Organisations should foster cross-functional teams that blend architecture, security, finance, and sustainability expertise. Governance frameworks need to accommodate higher levels of automation while preserving accountability. By treating leadership playbooks, communication cadences, and ethical guidelines as code, organisations maintain alignment as the pace of change accelerates.

## Conclusion

The future of Architecture as Code is shaped by the convergence of intelligent automation, quantum resilience, distributed infrastructure, and responsible stewardship. Organisations that embrace platform thinking, integrate financial and regulatory insights, and invest in human-centred skills development will create architectures that are resilient, transparent, and sustainable.

By combining proven practices with emerging innovations, Architecture as Code evolves from a delivery mechanism into a strategic discipline. The organisations that thrive will be those that balance experimentation with governance, embrace automation without neglecting ethics, and cultivate teams who can interpret complex ecosystems with clarity and confidence.

## Sources

1. **European Parliament and Council (2024).** *Regulation (EU) 2024/1689 laying down harmonised rules on artificial intelligence (Artificial Intelligence Act).* Official Journal of the European Union, L series, 12 July 2024. [https://eur-lex.europa.eu/eli/reg/2024/1689/oj](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) [Source [125]](33_references.md#source-125)
2. **European Commission (n.d.).** *Horizon Europe.* Research and innovation. [https://research-and-innovation.ec.europa.eu/funding/funding-opportunities/funding-programmes-and-open-calls/horizon-europe_en](https://research-and-innovation.ec.europa.eu/funding/funding-opportunities/funding-programmes-and-open-calls/horizon-europe_en) (accessed 2026-10-30).
3. **European Commission (n.d.).** *The Digital Europe Programme.* Shaping Europe's digital future. [https://digital-strategy.ec.europa.eu/en/activities/digital-programme](https://digital-strategy.ec.europa.eu/en/activities/digital-programme) (accessed 2026-10-30).
4. **European Commission (n.d.).** *Quantum Technologies Flagship.* Shaping Europe's digital future. [https://digital-strategy.ec.europa.eu/en/policies/quantum-technologies-flagship](https://digital-strategy.ec.europa.eu/en/policies/quantum-technologies-flagship) (accessed 2026-10-30).
5. **European Commission (n.d.).** *European Quantum Communication Infrastructure (EuroQCI).* Shaping Europe's digital future. [https://digital-strategy.ec.europa.eu/en/policies/european-quantum-communication-infrastructure-euroqci](https://digital-strategy.ec.europa.eu/en/policies/european-quantum-communication-infrastructure-euroqci) (accessed 2026-10-30).
6. **EuroHPC Joint Undertaking (n.d.).** *Our quantum computers.* EuroHPC JU. [https://eurohpc-ju.europa.eu/supercomputers/our-quantum-computers_en](https://eurohpc-ju.europa.eu/supercomputers/our-quantum-computers_en) (accessed 2026-10-30).
7. **NIST (2024).** *NIST Releases First 3 Finalized Post-Quantum Encryption Standards* (FIPS 203, FIPS 204 and FIPS 205). News release, 13 August 2024. [https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)
8. **NIST (2025).** *HQC Announced as a 4th Round Selection.* CSRC news, 11 March 2025. [https://csrc.nist.gov/News/2025/hqc-announced-as-a-4th-round-selection](https://csrc.nist.gov/News/2025/hqc-announced-as-a-4th-round-selection)
9. **NIST (2024).** *Transition to Post-Quantum Cryptography Standards.* NIST IR 8547 (initial public draft), 12 November 2024. [https://doi.org/10.6028/NIST.IR.8547.ipd](https://doi.org/10.6028/NIST.IR.8547.ipd) [Source [122]](33_references.md#source-122)
10. **ENISA (2021).** *Post-Quantum Cryptography: Current state and quantum mitigation.* European Union Agency for Cybersecurity, 3 May 2021. [https://www.enisa.europa.eu/publications/post-quantum-cryptography-current-state-and-quantum-mitigation](https://www.enisa.europa.eu/publications/post-quantum-cryptography-current-state-and-quantum-mitigation) [Source [126]](33_references.md#source-126)
11. **European Commission (2024).** *Commission Recommendation of 11 April 2024 on a Coordinated Implementation Roadmap for the transition to Post-Quantum Cryptography.* Shaping Europe's digital future. [https://digital-strategy.ec.europa.eu/en/library/recommendation-coordinated-implementation-roadmap-transition-post-quantum-cryptography](https://digital-strategy.ec.europa.eu/en/library/recommendation-coordinated-implementation-roadmap-transition-post-quantum-cryptography) [Source [127]](33_references.md#source-127)
12. **European Commission (n.d.).** *The European Green Deal.* [https://commission.europa.eu/strategy-and-policy/priorities-2019-2024/european-green-deal_en](https://commission.europa.eu/strategy-and-policy/priorities-2019-2024/european-green-deal_en) (accessed 2026-10-30).
13. **Green Software Foundation (2024).** *Software Carbon Intensity (SCI) Specification* (ISO/IEC 21031:2024). Green Software Foundation. [https://sci.greensoftware.foundation/](https://sci.greensoftware.foundation/) [Source [120]](33_references.md#source-120)
14. **Green Software Foundation (n.d.).** *Carbon Aware SDK.* Green Software Foundation. [https://github.com/Green-Software-Foundation/carbon-aware-sdk](https://github.com/Green-Software-Foundation/carbon-aware-sdk) (accessed 2026-10-30). [Source [121]](33_references.md#source-121)
15. **CISPE & EUDCA (n.d.).** *Climate Neutral Data Centre Pact.* Self-regulatory initiative. [https://www.climateneutraldatacentre.net/](https://www.climateneutraldatacentre.net/) (accessed 2026-10-30).
16. **European Commission Joint Research Centre (n.d.).** *European Code of Conduct for Energy Efficiency in Data Centres.* [https://joint-research-centre.ec.europa.eu/scientific-activities-z/energy-efficiency/energy-efficiency-products/code-conduct-ict/european-code-conduct-energy-efficiency-data-centres_en](https://joint-research-centre.ec.europa.eu/scientific-activities-z/energy-efficiency/energy-efficiency-products/code-conduct-ict/european-code-conduct-energy-efficiency-data-centres_en) (accessed 2026-10-30).
17. **CNCF TAG App Delivery (2023).** *CNCF Platforms White Paper* (v1.0). Cloud Native Computing Foundation. [https://tag-app-delivery.cncf.io/whitepapers/platforms/](https://tag-app-delivery.cncf.io/whitepapers/platforms/) [Source [129]](33_references.md#source-129)
18. **FinOps Foundation (n.d.).** *FinOps Framework.* FinOps Foundation. [https://www.finops.org/framework/](https://www.finops.org/framework/) (accessed 2026-10-30). [Source [124]](33_references.md#source-124)
19. **FinOps Foundation (2026).** *State of FinOps 2026 Report.* FinOps Foundation. [https://data.finops.org/](https://data.finops.org/) (accessed 2026-10-30).
20. **MarketsandMarkets (2022).** *Infrastructure as Code Market – Global Forecast to 2027.* Report TC 8140, August 2022 (press release 3 May 2023). [https://www.marketsandmarkets.com/Market-Reports/infrastructure-as-code-market-115458264.html](https://www.marketsandmarkets.com/Market-Reports/infrastructure-as-code-market-115458264.html) [Source [47]](33_references.md#source-47)
21. **Gartner (2023).** *Gartner Forecasts Worldwide Public Cloud End-User Spending to Reach $679 Billion in 2024.* Press release, 13 November 2023. [https://www.gartner.com/en/newsroom/press-releases/2023-11-13-gartner-forecasts-worldwide-public-cloud-end-user-spending-to-reach-679-billion-in-20240](https://www.gartner.com/en/newsroom/press-releases/2023-11-13-gartner-forecasts-worldwide-public-cloud-end-user-spending-to-reach-679-billion-in-20240) [Source [45]](33_references.md#source-45)
22. **Gartner (2024).** *Gartner Forecasts Worldwide Public Cloud End-User Spending to Total $723 Billion in 2025.* Press release, 19 November 2024. [https://www.gartner.com/en/newsroom/press-releases/2024-11-19-gartner-forecasts-worldwide-public-cloud-end-user-spending-to-total-723-billion-dollars-in-2025](https://www.gartner.com/en/newsroom/press-releases/2024-11-19-gartner-forecasts-worldwide-public-cloud-end-user-spending-to-total-723-billion-dollars-in-2025) [Source [46]](33_references.md#source-46)
23. **Gaia-X European Association for Data and Cloud AISBL (n.d.).** *Gaia-X: A Federated Secure Data Infrastructure.* [https://gaia-x.eu/](https://gaia-x.eu/) (accessed 2026-10-30).
