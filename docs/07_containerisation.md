# Containerisation and Orchestration as Code

![Containerisation and Orchestration](images/diagram_11_chapter10.png)

Architecture as Code underpins modern container platforms by turning deployment practices into repeatable definitions. When infrastructure and runtime configuration are described in version-controlled files, teams gain portable, scalable, and reproducible delivery pipelines that function reliably across data centres and cloud providers.

## Industry trend data driving Architecture as Code adoption

The Cloud Native Computing Foundation's *State of Cloud Native Development 2024* report (Source [7]) confirms that distributed architectures are now the norm: 67% of surveyed organisations run microservices in production and 58% operate event-driven workloads alongside them. The same research notes that 52% are investing in internal developer platforms to tame the resulting estate. Together these figures highlight why Architecture as Code is essential. When the majority of teams orchestrate dozens of loosely coupled services and event flows, formal boundary definitions, shared contracts, and automated governance become mandatory to avoid integration drift. Codifying those boundaries as part of an Architecture as Code programme provides the repeatability and audit trail that the report identifies as critical for scaling cloud-native delivery.

## The role of container technology within Architecture as Code

Containers package an application together with its libraries and runtime dependencies inside isolated units. Within an Architecture as Code approach, those units are described declaratively so that the same package can be built, tested, and promoted through each stage without configuration drift. The result is predictable application behaviour and simpler collaboration between development, operations, and security teams.

Docker popularised this model and remains the industry reference point, while projects such as Podman provide daemon-less alternatives that suit security-conscious environments. Image definitions are written in Dockerfiles (or equivalent build instructions) so that they can be stored in Git, reviewed, and rebuilt automatically as part of the CI/CD process. Linters and automated tests can validate these artefacts in the same way that application code is reviewed.

Once images are produced they are stored in container registries, which act as central repositories for distribution and version control. Private registries support enterprise governance by enforcing access control, image signing, and vulnerability scanning before any workload reaches production. Registry policies can be expressed as code to guarantee compliance across teams.

## Kubernetes as an orchestration platform

Kubernetes has become the canonical orchestration layer thanks to its declarative design and expansive ecosystem. YAML manifests capture the desired state for workloads, services, and platform components, meaning the entire runtime can be documented alongside the application source. The Kubernetes control plane continuously reconciles the actual state with those declarations, enforcing Architecture as Code in real time.

Native Kubernetes objects—Deployments, StatefulSets, Services, ConfigMaps, Secrets, and many others—cover the full application lifecycle. Teams describe pod specifications, resource requests, network segmentation, and persistent storage needs directly in code. Version control and peer review help prevent configuration drift while providing a complete audit history for compliance purposes.

Helm augments Kubernetes with templating and release management features, enabling reusable deployment patterns for complex stacks. Chart repositories encapsulate organisational standards so that teams can provision consistent environments quickly, whether the target is development, staging, or production.

## Service mesh and advanced networking

Service meshes such as Istio and Linkerd introduce a programmable data plane that handles inter-service communication, observability, and security concerns. Policy definitions, routing rules, and cryptographic requirements are written as configuration files, allowing networking specialists to iterate safely without touching application code.

Traffic shaping features—including circuit breaking, retries, fault injection, and canary roll-outs—are specified as code and stored alongside the services they protect. Mutual TLS, zero-trust access rules, and identity management policies follow the same pattern, making it straightforward to extend security best practice across microservice estates.

Observability is likewise driven by declaration. Distributed tracing, metrics scraping, and log aggregation are enabled through manifests that describe collectors, exporters, and retention policies. This consistency simplifies root-cause analysis because every cluster exposes telemetry in a standardised format.

## Infrastructure automation with container platforms

Kubernetes-native automation frameworks extend the platform to cover underlying infrastructure. Crossplane, the Operator Framework, and similar projects expose cloud resources as custom resource definitions (CRDs), meaning databases, message queues, or networking components can be provisioned through the same API surface as application workloads.

GitOps practices complement this model by treating Git repositories as the source of truth. Continuous delivery tools such as Argo CD and Flux reconcile the declared state with the running clusters, applying changes automatically when a pull request is merged. Rollbacks become a matter of reverting commits, and audit trails are preserved for every environment.

Large organisations often operate multiple clusters across regions. Multi-cluster management suites provide centralised policy enforcement, workload placement, and governance. Federation APIs and the Cluster API specification capture cluster lifecycle operations in code, standardising creation, upgrades, and decommissioning.

## Persistent storage and data management

Stateful workloads still rely on robust storage. Kubernetes addresses this with persistent volumes, storage classes, and dynamic provisioners, all of which are defined declaratively. Performance, redundancy, and backup requirements can be embedded into these definitions so that new workloads inherit compliant defaults automatically.

Database operators—for PostgreSQL, MongoDB, MySQL, and many others—take the concept further by managing clustering, backups, failover, and version upgrades. These controllers watch for configuration changes and adjust the database fleet accordingly, providing database-as-code capabilities without extensive manual intervention.

Data protection remains critical. Backup schedules, retention policies, and disaster recovery runbooks can be codified through operators or infrastructure-as-code tooling. Automated tests and scheduled recovery drills verify that restorations meet business continuity objectives.

## Practical examples

### Kubernetes Deployment Configuration
```yaml
# app-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-application
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-application
  template:
    metadata:
      labels:
        app: web-application
    spec:
      containers:
      - name: app
        image: registry.company.com/web-app:v1.2.3
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: url
---
apiVersion: v1
kind: Service
metadata:
  name: web-application-service
spec:
  selector:
    app: web-application
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer
```

### Helm Chart for Application Stack
```yaml
# values.yaml
application:
  name: web-application
  image:
    repository: registry.company.com/web-app
    tag: "v1.2.3"
    pullPolicy: IfNotPresent

  replicas: 3

  resources:
    requests:
      memory: "256Mi"
      cpu: "250m"
    limits:
      memory: "512Mi"
      cpu: "500m"

database:
  enabled: true
  type: postgresql
  version: "14"
  persistence:
    size: 10Gi
    storageClass: "fast-ssd"

monitoring:
  enabled: true
  prometheus:
    scrapeInterval: 30s
  grafana:
    dashboards: true
```

### Docker Compose for Development Environment
```yaml
# docker-compose.yml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/appdb
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    volumes:
      - ./app:/app
      - /app/node_modules

  db:
    image: postgres:14
    environment:
      POSTGRES_DB: appdb
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

### Terraform for Kubernetes Cluster
```hcl
# kubernetes-cluster.tf
resource "google_container_cluster" "primary" {
  name     = "production-cluster"
  location = "us-central1"

  remove_default_node_pool = true
  initial_node_count       = 1

  network    = google_compute_network.vpc.name
  subnetwork = google_compute_subnetwork.subnet.name

  release_channel {
    channel = "STABLE"
  }

  workload_identity_config {
    workload_pool = "${var.project_id}.svc.id.goog"
  }

  addons_config {
    horizontal_pod_autoscaling {
      disabled = false
    }
    network_policy_config {
      disabled = false
    }
  }
}

resource "google_container_node_pool" "primary_nodes" {
  name       = "primary-node-pool"
  location   = "us-central1"
  cluster    = google_container_cluster.primary.name
  node_count = 3

  node_config {
    preemptible  = false
    machine_type = "e2-medium"

    service_account = google_service_account.kubernetes.email
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }

  autoscaling {
    min_node_count = 1
    max_node_count = 10
  }

  management {
    auto_repair  = true
    auto_upgrade = true
  }
}
```

## Summary

Architecture as Code provides a common language for development, operations, and security teams. By expressing container platforms, orchestration logic, networking, and data safeguards as code, organisations can automate delivery, scale confidently, and apply governance consistently. Kubernetes and its surrounding ecosystem offer the building blocks, while GitOps workflows keep every environment aligned with the declared intent. Mastery of these practices delivers resilient platforms that adapt quickly to changing requirements.

## Transition to Security and Governance

The automation capabilities and deployment velocity enabled by containerisation and CI/CD pipelines create new security challenges and governance requirements. As containers move through development, testing, and production environments at increasing speed, security controls must keep pace without becoming bottlenecks.

The next part of this book explores how security, policy enforcement, and governance frameworks integrate into Architecture as Code practices. [Chapter 9A on Security Fundamentals](09a_security_fundamentals.md) and [Chapter 9B on Advanced Security Patterns](09b_security_patterns.md) examine threat modelling, Zero Trust Architecture, and security-by-design principles specifically tailored for containerised, automated environments. [Chapter 10 on Policy and Security as Code](10_policy_and_security.md) demonstrates how tools like Open Policy Agent enforce security requirements automatically, whilst [Chapters 11 and 12](11_governance_as_code.md) show how governance and compliance become executable code rather than static documentation.

## Sources and references

- Kubernetes Documentation. "Concepts and Architecture." The Kubernetes Project.
- Docker Inc. "Docker Architecture as Code best practices." Docker Documentation.
- Cloud Native Computing Foundation. "State of Cloud Native Development 2024." CNCF Research.
- Cloud Native Computing Foundation. "CNCF Landscape." Cloud Native Technologies.
- Helm Community. "Chart Development Guide." Helm Documentation.
- Istio Project. "Service Mesh Architecture." Istio Service Mesh.
