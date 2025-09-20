# Microservices-arkitektur som kod

![Microservices-arkitektur](images/diagram_13_kapitel12.png)

Microservices-arkitektur revolutionerar hur stora system designas och implementeras genom att dela upp monolitiska applikationer i mindre, oberoende tjänster. Infrastructure as Code spelar en kritisk roll för att hantera komplexiteten och säkerställa konsistent deployment av distribuerade microservices-system.

## Microservices design principles för IaC

Microservices architecture bygger på principen om loosely coupled, highly cohesive services som kan utvecklas, deployeras och skalas oberoende. Varje service äger sin egen data och business logic, kommunicerar genom well-defined APIs, och kan implementeras med olika teknologier baserat på specific requirements.

Service boundaries definieras genom domain-driven design principles där varje microservice representerar en bounded context inom business domain. Detta organisational pattern påverkar Infrastructure as Code genom att varje service kräver sin egen infrastructure definition, deployment pipeline, och operational monitoring.

Single responsibility principle appliceras på service level, vilket innebär att varje microservice har ett specifikt, väldefinierat ansvar. För Infrastructure as Code betyder detta att infrastructure components också organiseras kring service boundaries, vilket möjliggör independent scaling, deployment, och maintenance av different system parts.

## Service discovery och communication patterns

Service discovery mechanisms möjliggör dynamic location och communication mellan microservices utan hard-coded endpoints. Infrastructure as Code implementerar service registries, DNS-based discovery, eller service mesh solutions som automatically handle service location och load balancing.

Communication patterns mellan microservices inkluderar synchronous REST/gRPC calls för immediate responses och asynchronous messaging för eventual consistency scenarios. Message brokers som Apache Kafka eller RabbitMQ definieras through infrastructure code för reliable, scalable inter-service communication.

API gateways fungerar som unified entry points för external clients och implement cross-cutting concerns som authentication, rate limiting, och request routing. Gateway configurations definieras as code för consistent policy enforcement och traffic management across service topologies.

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
# user-service.yaml
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
---
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
---
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