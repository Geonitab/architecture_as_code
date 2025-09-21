# Containerisering och orkestrering

Containerisering som kod möjliggör portabel och konsistent deployment av applikationer genom standardiserade runtime-miljöer. Detta kapitel utforskar hur containerinfrastruktur kan kodifieras för orchestration, scaling och service management.

![Containerisering och orkestrering](images/diagram_08_containerisering.png)

*Container orchestration som kod integrerar containerizederade applikationer med infrastructure management för skalbar och resilient arkitektur.*

## Containerinfrastruktur som kod

Container Infrastructure as Code bygger på image definitions, runtime configurations och orchestration policies som versionshanteras och automatiskt deployable. Docker och containerd fungerar som runtime layers medan Kubernetes, Docker Swarm och Amazon ECS tillhandahåller orchestration.

Container images definieras genom Dockerfiles som specificerar application dependencies, runtime environment och configuration, vilket möjliggör reproducible builds och consistent deployments.

## Kubernetes som Infrastructure as Code

Kubernetes-resurser definieras genom YAML/JSON manifests som beskriver desired state för pods, services, deployments och andra Kubernetes objects. Denna deklarativa approach möjliggör GitOps workflows för container orchestration.

```yaml
# Kubernetes deployment manifest
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-application
  namespace: production
  labels:
    app: web-application
    version: v1.2.0
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-application
  template:
    metadata:
      labels:
        app: web-application
        version: v1.2.0
    spec:
      containers:
      - name: web-app
        image: myregistry/web-app:v1.2.0
        ports:
        - containerPort: 8080
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: web-application-service
  namespace: production
spec:
  selector:
    app: web-application
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
  type: LoadBalancer
```

## Helm och package management

Helm Charts möjliggör templating och packaging av Kubernetes applications som reusable, configurable components. Infrastructure as Code för Kubernetes inkluderar Helm chart definitions och values files för environment-specific configurations.

```yaml
# Helm values.yaml
replicaCount: 3

image:
  repository: myregistry/web-app
  tag: v1.2.0
  pullPolicy: IfNotPresent

service:
  type: LoadBalancer
  port: 80

ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: app.example.com
      paths:
        - path: /
          pathType: Prefix

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80
```

## Container security som kod

Container security policies definieras genom Pod Security Standards, Network Policies och RBAC configurations som säkerställer säker runtime environment och least-privilege access.

```yaml
# Pod Security Policy
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: restricted
spec:
  privileged: false
  allowPrivilegeEscalation: false
  requiredDropCapabilities:
    - ALL
  volumes:
    - 'configMap'
    - 'emptyDir'
    - 'projected'
    - 'secret'
    - 'downwardAPI'
    - 'persistentVolumeClaim'
  runAsUser:
    rule: 'MustRunAsNonRoot'
  seLinux:
    rule: 'RunAsAny'
  fsGroup:
    rule: 'RunAsAny'
```

## Monitoring och observability

Container monitoring som kod inkluderar metrics collection, logging configuration och alerting rules definierade som code. Prometheus, Grafana och Jaeger kan konfigureras genom Infrastructure as Code för comprehensive observability.

## CI/CD för containeriserade applikationer

Container CI/CD pipelines inkluderar image building, security scanning, testing och automated deployment till olika miljöer. Infrastructure as Code möjliggör consistent pipeline definitions och deployment strategies.

```yaml
# GitHub Actions för container CI/CD
name: Container CI/CD
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Build Docker image
      run: |
        docker build -t myapp:${{ github.sha }} .
        
    - name: Run security scan
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: myapp:${{ github.sha }}
        format: sarif
        output: trivy-results.sarif
        
    - name: Run tests
      run: |
        docker run --rm myapp:${{ github.sha }} npm test
        
    - name: Push to registry
      if: github.ref == 'refs/heads/main'
      run: |
        docker tag myapp:${{ github.sha }} myregistry/myapp:${{ github.sha }}
        docker push myregistry/myapp:${{ github.sha }}
```

## Sammanfattning

Containerisering och orkestrering som kod möjliggör portabel, skalbar och säker deployment av applikationer. Genom att kodifiera container infrastructure uppnås consistency, reproducibility och automated operations.

Källor:
- Kubernetes Documentation. The Kubernetes Authors, 2024.
- Docker Documentation. Docker Inc., 2024.
- Helm Documentation. The Helm Authors, 2024.
- CNCF. "Cloud Native Computing Foundation Landscape." CNCF, 2024.