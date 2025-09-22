# Containerisering och orkestrering som kod

![Containerisering och orkestrering](images/diagram_11_kapitel10.png)

Arkitektur som kod-metodiken utgör grunden för containerteknologi och orkestrering representerar paradigmskifte i hur applikationer deployeras och skalas. Genom att definiera container-infrastruktur som kod möjliggörs portable, skalbar och reproducerbar application deployment across olika miljöer och cloud providers.

## Container-teknologiens roll inom IaC

Containers erbjuder application-level virtualization som paketerar applikationer med alla dependencies i isolated, portable units. För Infrastructure as Code (arkitektur som kod) innebär detta att application deployment kan standardiseras och automatiseras genom code-based definitions som säkerställer consistency mellan development, testing och production environments.

Docker har etablerat sig som de facto standard för containerization, medan podman och andra alternativ erbjuder daemon-less approaches för enhanced security. Container images definieras genom Dockerfiles som executable infrastructure code, vilket möjliggör version control och automated building av application artifacts.

Container registries fungerar som centralized repositories för image distribution och versioning. Private registries säkerställer corporate security requirements, medan image scanning och vulnerability assessment integreras i CI/CD pipelines för automated security validation innan deployment.

## Kubernetes som orchestration platform

Kubernetes har emergerat som leading container orchestration platform genom dess declarative configuration model och extensive ecosystem. YAML-based manifests definierar desired state för applications, services, och infrastructure components, vilket alignar perfekt med Infrastructure as Code (arkitektur som kod) principles.

Kubernetes objects som Deployments, Services, ConfigMaps, och Secrets möjliggör comprehensive application lifecycle management through code. Pod specifications, resource quotas, network policies, och persistent volume claims kan alla definieras declaratively och managed through version control systems.

Helm charts extend Kubernetes capabilities genom templating och package management för complex applications. Chart repositories enable reusable infrastructure patterns och standardized deployment procedures across different environments och organizational units.

## Service mesh och advanced networking

Service mesh architectures som Istio och Linkerd implementeras through Infrastructure as Code för att hantera inter-service communication, security policies, och observability. These platforms abstract networking complexity från application developers while providing fine-grained control through configuration files.

Traffic management policies definieras as code för load balancing, circuit breaking, retry mechanisms, och canary deployments. Security policies för mutual TLS, access control, och authentication/authorization can be version controlled och automatically applied across service topologies.

Observability configurations för tracing, metrics collection, och logging integration managed through declarative specifications. This enables comprehensive monitoring och debugging capabilities while maintaining consistency across distributed service architectures.

## Infrastructure automation med container platforms

Arkitektur som kod-principerna inom detta område

Container-native infrastructure tools som Crossplane och Operator Framework extend Kubernetes för complete infrastructure management. These platforms möjliggör provisioning och management av cloud resources through Kubernetes-native APIs och custom resource definitions.

GitOps workflows implement continuous delivery för both applications och infrastructure through Git repositories som single source of truth. Tools som ArgoCD och Flux automate deployment processes genom continuous monitoring av Git state och automatic reconciliation av cluster state.

Multi-cluster management platforms centralize policy enforcement, resource allocation, och governance across distributed Kubernetes environments. Federation och cluster API specifications standardize cluster lifecycle management through declarative configurations.

## Persistent storage och data management

Persistent volume management för containerized applications kräver careful consideration av performance, availability, och backup requirements. Storage classes och persistent volume claims definieras as infrastructure code för automated provisioning och lifecycle management.

Database operators för PostgreSQL, MongoDB, och andra systems enable database-as-code deployment patterns. These operators handle complex operations som backup scheduling, high availability configuration, och automated recovery through custom resource definitions.

Data protection strategies implementeras through backup operators och disaster recovery procedures definierade as code. This ensures consistent data protection policies across environments och automated recovery capabilities during incidents.

## Praktiska exempel

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

### Helm Chart för Application Stack
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

### Docker Compose för Development Environment
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

### Terraform för Kubernetes Cluster
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

## Sammanfattning


Den moderna arkitektur som kod-metodiken representerar framtiden för infrastrukturhantering i svenska organisationer.
Containerisering och orkestrering som kod transformerar application deployment från manual, error-prone processes till automated, reliable workflows. Kubernetes och associerade verktyg möjliggör sophisticated application management genom declarative configurations, medan GitOps patterns säkerställer consistent och auditable deployment processes. Success kräver comprehensive understanding av container networking, storage management, och security implications.

## Källor och referenser

- Kubernetes Documentation. "Concepts and Architecture." The Kubernetes Project.
- Docker Inc. "Docker arkitektur som kod best practices." Docker Documentation.
- Cloud Native Computing Foundation. "CNCF Landscape." Cloud Native Technologies.
- Helm Community. "Chart Development Guide." Helm Documentation.
- Istio Project. "Service Mesh Architecture." Istio Service Mesh.