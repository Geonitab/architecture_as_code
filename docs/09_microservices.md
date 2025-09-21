# Microservices och distribuerade system

Microservices-arkitektur som kod möjliggör definition och hantering av distribuerade system genom kodifierade service definitions, inter-service communication och orchestration policies. Detta kapitel utforskar hur microservices-landskapet kan hanteras som Infrastructure as Code.

![Microservices och distribuerade system](images/diagram_09_microservices.png)

*Microservices-arkitektur som kod integrerar service definitions, communication patterns och infrastructure management för skalbar och resilient distribuerad systemarkitektur.*

## Microservices Infrastructure as Code

Microservices Infrastructure as Code omfattar service definitions, API gateways, service discovery, load balancing och inter-service communication policies. Varje service definieras med sina dependencies, resource requirements och deployment configurations.

Service mesh-arkitekturer som Istio och Linkerd möjliggör infrastructure-level management av microservices communication, security och observability genom configuration as code.

## Service definitions och deployment

Microservices definieras genom containerized applications med associerade infrastructure configurations för networking, security och resource management. Kubernetes, Docker Swarm och managed container services tillhandahåller orchestration platforms.

```yaml
# Microservice deployment configuration
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-service
  namespace: production
  labels:
    app: user-service
    version: v2.1.0
    tier: backend
spec:
  replicas: 5
  selector:
    matchLabels:
      app: user-service
  template:
    metadata:
      labels:
        app: user-service
        version: v2.1.0
    spec:
      containers:
      - name: user-service
        image: myregistry/user-service:v2.1.0
        ports:
        - containerPort: 8080
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: user-db-credentials
              key: url
        - name: REDIS_URL
          valueFrom:
            configMapKeyRef:
              name: cache-config
              key: redis-url
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 15
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: user-service
  namespace: production
  labels:
    app: user-service
spec:
  selector:
    app: user-service
  ports:
  - name: http
    protocol: TCP
    port: 80
    targetPort: 8080
  type: ClusterIP
```

## API Gateway och service mesh

API Gateway Infrastructure as Code definierar routing rules, authentication, rate limiting och API versioning för microservices. Service mesh configurations hanterar inter-service communication, circuit breakers och security policies.

```yaml
# Istio Service Mesh konfiguration
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: microservices-gateway
  namespace: production
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - api.example.com
  - port:
      number: 443
      name: https
      protocol: HTTPS
    tls:
      mode: SIMPLE
      credentialName: api-tls-secret
    hosts:
    - api.example.com
---
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: user-service-vs
  namespace: production
spec:
  hosts:
  - api.example.com
  gateways:
  - microservices-gateway
  http:
  - match:
    - uri:
        prefix: /api/v2/users
    route:
    - destination:
        host: user-service
        port:
          number: 80
      weight: 90
    - destination:
        host: user-service-canary
        port:
          number: 80
      weight: 10
    fault:
      delay:
        percentage:
          value: 0.1
        fixedDelay: 5s
```

## Inter-service communication patterns

Microservices communication patterns som synchronous HTTP/gRPC, asynchronous messaging och event-driven architectures kodifieras genom message queues, event buses och API definitions.

```yaml
# Event-driven communication med Apache Kafka
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: microservices-cluster
  namespace: production
spec:
  kafka:
    version: 3.6.0
    replicas: 3
    listeners:
      - name: plain
        port: 9092
        type: internal
        tls: false
      - name: tls
        port: 9093
        type: internal
        tls: true
    config:
      offsets.topic.replication.factor: 3
      transaction.state.log.replication.factor: 3
      transaction.state.log.min.isr: 2
      default.replication.factor: 3
      min.insync.replicas: 2
    storage:
      type: jbod
      volumes:
      - id: 0
        type: persistent-claim
        size: 100Gi
        deleteClaim: false
  zookeeper:
    replicas: 3
    storage:
      type: persistent-claim
      size: 10Gi
      deleteClaim: false
```

## Data management och consistency

Microservices data management som kod inkluderar database-per-service patterns, distributed transaction management och eventual consistency strategies. Event sourcing och CQRS patterns kan implementeras genom Infrastructure as Code.

## Security och service-to-service authentication

Microservices security som kod omfattar mutual TLS (mTLS), OAuth 2.0/JWT authentication, RBAC policies och zero-trust networking principles implementerade genom service mesh och API gateway configurations.

## Monitoring och distributed tracing

Distributed system observability som kod inkluderar metrics collection, distributed tracing, log aggregation och alerting för hela microservices-landskapet. OpenTelemetry, Prometheus och Jaeger konfigurationer hanteras som Infrastructure as Code.

## Chaos engineering och resilience

Chaos engineering för microservices implementeras genom Infrastructure as Code med tools som Chaos Monkey, Litmus och Gremlin för att testa system resilience och identify failure modes.

## Sammanfattning

Microservices och distribuerade system som kod möjliggör skalbar, resilient och manageable arkitektur för komplexa applikationslandskap. Genom kodifiering av service definitions, communication patterns och infrastructure uppnås consistency och operational excellence.

Källor:
- Microservices Patterns. Richardson, C. Manning Publications, 2018.
- Building Microservices. Newman, S. O'Reilly Media, 2021.
- Istio Documentation. Istio Authors, 2024.
- CNCF Landscape. Cloud Native Computing Foundation, 2024.