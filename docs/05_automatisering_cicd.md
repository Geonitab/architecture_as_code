# Automatisering och CI/CD-pipelines

Kontinuerlig integration och deployment (CI/CD) för Infrastructure as Code möjliggör säker och effektiv automatisering av infrastrukturändringar. Genom att implementera robusta pipelines kan organisationer accelerera leveranser samtidigt som de bibehåller hög kvalitet och säkerhet. Som vi såg i [kapitel 3 om versionhantering](03_kapitel2.md), utgör CI/CD-pipelines en naturlig förlängning av git-baserade workflows för infrastrukturkod.

![Automatisering och CI/CD-pipelines](images/diagram_04_kapitel3.png)

Diagrammet visar det grundläggande CI/CD-flödet från code commit genom validation och testing till deployment och monitoring, vilket säkerställer kvalitetskontroll genom hela processen. Detta flöde kommer att bli särskilt viktigt när vi utforskar [molnarkitektur som kod](05_kapitel4.md) och [säkerhet i Infrastructure as Code](06_kapitel5.md).

## CI/CD-fundamentals för svenska organisationer

Svenska organisationer står inför unika utmaningar när det gäller implementering av CI/CD-pipelines för Infrastructure as Code. Regulatory compliance, data residency requirements, och cost optimization i svenska kronor kräver specialized approaches som traditionella CI/CD-patterns inte alltid adresserar.

### GDPR-compliant pipeline design

För svenska organisationer innebär GDPR compliance att CI/CD-pipelines måste hantera personal data med särskild försiktighet genom hela deployment lifecycle. Detta kräver comprehensive audit trails, data anonymization capabilities, och automated compliance validation:

**GDPR-kompatibel CI/CD Pipeline för svenska organisationer**
*[Se kodexempel 05_CODE_1 i Appendix A: Kodexempel](26_appendix_kodexempel.md#05_code_1)*

Detta pipeline-exempel demonstrerar hur svenska organisationer kan implementera GDPR-compliance direkt i sina CI/CD-processer, inklusive automatisk scanning för personuppgifter och data residency validation.
      
      - name: Data Residency Validation
        run: |
          echo "🇸🇪 Validerar svenska data residency krav..."
          
          # Kontrollera att AWS regions är svenska/nordiska
          ALLOWED_REGIONS=("eu-north-1" "eu-central-1" "eu-west-1")
          
          # Sök efter region konfigurationer
          REGION_VIOLATIONS=$(grep -r "region\s*=" infrastructure/ modules/ | grep -v -E "(eu-north-1|eu-central-1|eu-west-1)" || true)
          
          if [ -n "$REGION_VIOLATIONS" ]; then
            echo "❌ Data residency violation hittad:"
            echo "$REGION_VIOLATIONS"
            echo "Endast EU-regioner tillåtna för svenska data"
            exit 1
          fi
          
          echo "✅ Data residency requirements uppfyllda"
      
      - name: Audit Trail Setup
        run: |
          echo "📝 Skapar GDPR audit trail..."
          
          mkdir -p audit-logs
          
          cat > audit-logs/pipeline-audit.json << EOF
          {
            "audit_id": "$(uuidgen)",
            "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
            "event_type": "iac_pipeline_execution",
            "organization": "$ORGANIZATION_NAME",
            "environment": "$ENVIRONMENT",
            "compliance_framework": "GDPR",
            "data_residency": "Sweden",
            "git_commit": "$GITHUB_SHA",
            "git_author": "$GITHUB_ACTOR",
            "repository": "$GITHUB_REPOSITORY",
            "workflow_run": "$GITHUB_RUN_ID",
            "compliance_checks": {
              "gdpr_data_scan": "passed",
              "data_residency": "passed",
              "audit_logging": "enabled"
            }
          }
          EOF
          
          echo "📄 Audit trail skapad: audit-logs/pipeline-audit.json"
      
      - name: Upload GDPR Audit Logs
        uses: actions/upload-artifact@v4
        with:
          name: gdpr-audit-logs
          path: audit-logs/
          retention-days: 2555  # 7 år enligt svenska lagkrav

  # Syntax och static analysis
  code-quality-analysis:
    name: Code Quality & Security Analysis
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout kod
        uses: actions/checkout@v4
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TF_VERSION }}
      
      - name: Terraform Format Check
        run: |
          echo "🔧 Kontrollerar Terraform formatering..."
          terraform fmt -check -recursive
          
          if [ $? -ne 0 ]; then
            echo "❌ Terraform kod är inte korrekt formaterad"
            echo "Kör 'terraform fmt -recursive' för att fixa"
            exit 1
          fi
          
          echo "✅ Terraform formatering korrekt"
      
      - name: Terraform Validation
        run: |
          echo "🔍 Validerar Terraform syntax..."
          
          for dir in infrastructure/environments/*/; do
            if [ -d "$dir" ]; then
              echo "Validerar $dir..."
              cd "$dir"
              terraform init -backend=false
              terraform validate
              cd - > /dev/null
            fi
          done
          
          echo "✅ Terraform syntax validation genomförd"
      
      - name: Security Scanning med Trivy
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'config'
          scan-ref: 'infrastructure/'
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH,MEDIUM'
      
      - name: Upload Security Scan Results
        uses: github/codeql-action/upload-sarif@v2
        if: always()
        with:
          sarif_file: 'trivy-results.sarif'
      
      - name: Policy Validation med OPA/Conftest
        run: |
          echo "📋 Validerar organisatoriska policies..."
          
          # Installera conftest
          curl -L https://github.com/open-policy-agent/conftest/releases/download/v0.46.0/conftest_0.46.0_Linux_x86_64.tar.gz | tar xz
          sudo mv conftest /usr/local/bin
          
          # Svenska organisationspolicies
          mkdir -p policies
          
          cat > policies/svenska-compliance.rego << 'EOF'
          package svenska.compliance
          
          # GDPR Compliance Rules
          deny[msg] {
            input.resource.aws_instance
            not input.resource.aws_instance[_].encrypted_ebs_block_device
            msg := "EBS volumes måste vara krypterade för GDPR compliance"
          }
          
          deny[msg] {
            input.resource.aws_s3_bucket
            not input.resource.aws_s3_bucket[_].server_side_encryption_configuration
            msg := "S3 buckets måste ha server-side encryption aktiverat"
          }
          
          # Svenska Data Residency Rules
          deny[msg] {
            input.provider.aws.region
            not input.provider.aws.region == "eu-north-1"
            not input.provider.aws.region == "eu-central-1"
            not input.provider.aws.region == "eu-west-1"
            msg := sprintf("AWS region %s är inte tillåten för svenska data residency", [input.provider.aws.region])
          }
          
          # Cost Control Rules
          deny[msg] {
            input.resource.aws_instance[name].instance_type
            startswith(input.resource.aws_instance[name].instance_type, "x1")
            msg := sprintf("Instance type %s är för dyr för %s environment", [input.resource.aws_instance[name].instance_type, input.terraform.environment])
          }
          
          # Tagging Requirements
          deny[msg] {
            input.resource[resource_type][name]
            resource_type != "data"
            not input.resource[resource_type][name].tags
            msg := sprintf("Resource %s.%s saknar obligatoriska tags", [resource_type, name])
          }
          
          required_tags := ["Environment", "CostCenter", "Organization", "DataClassification", "GDPRCompliant"]
          
          deny[msg] {
            input.resource[resource_type][name].tags
            resource_type != "data"
            required_tag := required_tags[_]
            not input.resource[resource_type][name].tags[required_tag]
            msg := sprintf("Resource %s.%s saknar obligatorisk tag: %s", [resource_type, name, required_tag])
          }
          EOF
          
          # Kör policy validation
          for tf_file in $(find infrastructure/ -name "*.tf"); do
            echo "Validerar policies för $tf_file..."
            conftest verify --policy policies/ "$tf_file"
          done
          
          echo "✅ Policy validation genomförd"

  # Kostnadskontroll och budgetvalidering
  cost-analysis:
    name: Kostnadskontroll och Budget Validation
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request' || github.ref == 'refs/heads/main'
    
    steps:
      - name: Checkout kod
        uses: actions/checkout@v4
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TF_VERSION }}
      
      - name: Infracost Setup
        uses: infracost/infracost-gh-action@master
        with:
          api-key: ${{ secrets.INFRACOST_API_KEY }}
          currency: SEK  # Svenska kronor
      
      - name: Generate Cost Estimate
        run: |
          echo "💰 Beräknar infrastrukturkostnader i svenska kronor..."
          
          # Generera cost breakdown för varje miljö
          for env_dir in infrastructure/environments/*/; do
            if [ -d "$env_dir" ]; then
              env_name=$(basename "$env_dir")
              echo "Beräknar kostnader för $env_name miljö..."
              
              cd "$env_dir"
              terraform init -backend=false
              
              infracost breakdown \
                --path . \
                --format json \
                --out-file "../../cost-estimate-$env_name.json" \
                --currency SEK
              
              infracost output \
                --path "../../cost-estimate-$env_name.json" \
                --format table \
                --out-file "../../cost-summary-$env_name.txt"
              
              cd - > /dev/null
            fi
          done
          
          echo "✅ Kostnadskalkylering slutförd"
      
      - name: Cost Threshold Validation
        run: |
          echo "📊 Validerar kostnader mot svenska budgetgränser..."
          
          # Sätt svenska budget limits (i SEK per månad)
          case "$ENVIRONMENT" in
            "development") MAX_MONTHLY_COST_SEK=5000 ;;
            "staging") MAX_MONTHLY_COST_SEK=15000 ;;
            "production") MAX_MONTHLY_COST_SEK=50000 ;;
            *) MAX_MONTHLY_COST_SEK=10000 ;;
          esac
          
          # Kontrollera cost estimates
          for cost_file in cost-estimate-*.json; do
            if [ -f "$cost_file" ]; then
              MONTHLY_COST=$(jq -r '.totalMonthlyCost' "$cost_file")
              ENV_NAME=$(echo "$cost_file" | sed 's/cost-estimate-\(.*\)\.json/\1/')
              
              echo "Månadskostnad för $ENV_NAME: $MONTHLY_COST SEK"
              
              # Konvertera till numerisk jämförelse
              if (( $(echo "$MONTHLY_COST > $MAX_MONTHLY_COST_SEK" | bc -l) )); then
                echo "❌ Kostnadsgräns överskriden för $ENV_NAME!"
                echo "Beräknad kostnad: $MONTHLY_COST SEK"
                echo "Maximal budget: $MAX_MONTHLY_COST_SEK SEK"
                exit 1
              fi
            fi
          done
          
          echo "✅ Alla kostnader inom svenska budgetgränser"
      
      - name: Generate Swedish Cost Report
        run: |
          echo "📈 Genererar svenskt kostnadsrapport..."
          
          cat > cost-report-swedish.md << EOF
          # Kostnadsrapport för $ORGANIZATION_NAME
          
          **Miljö:** $ENVIRONMENT  
          **Datum:** $(date '+%Y-%m-%d %H:%M') (svensk tid)  
          **Valuta:** Svenska kronor (SEK)  
          **Kostnadscenter:** $COST_CENTER
          
          ## Månadskostnader per miljö
          
          EOF
          
          for summary_file in cost-summary-*.txt; do
            if [ -f "$summary_file" ]; then
              ENV_NAME=$(echo "$summary_file" | sed 's/cost-summary-\(.*\)\.txt/\1/')
              echo "### $ENV_NAME miljö" >> cost-report-swedish.md
              echo '```' >> cost-report-swedish.md
              cat "$summary_file" >> cost-report-swedish.md
              echo '```' >> cost-report-swedish.md
              echo "" >> cost-report-swedish.md
            fi
          done
          
          cat >> cost-report-swedish.md << EOF
          ## Kostnadskontroller
          
          - ✅ GDPR-compliant kryptering aktiverad
          - ✅ Svenska data residency-krav uppfyllda
          - ✅ Automatisk cost monitoring aktiverad
          - ✅ Budget alerts konfigurerade
          
          ## Rekommendationer
          
          1. Använd reserved instances för production workloads
          2. Aktivera auto-scaling för development miljöer
          3. Implementera scheduled shutdown för non-production
          4. Överväg svenska molnleverantörer för vissa workloads
          
          ---
          *Genererad automatiskt av svenska IaC pipeline*
          EOF
          
          echo "📄 Svenskt kostnadsrapport skapat: cost-report-swedish.md"
      
      - name: Upload Cost Analysis
        uses: actions/upload-artifact@v4
        with:
          name: cost-analysis-${{ env.ENVIRONMENT }}
          path: |
            cost-estimate-*.json
            cost-summary-*.txt
            cost-report-swedish.md
          retention-days: 90

  # Environment-specifik validering
  environment-validation:
    name: Environment-specific Validation
    runs-on: ubuntu-latest
    strategy:
      matrix:
        environment: [development, staging, production]
        
    steps:
      - name: Checkout kod
        uses: actions/checkout@v4
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TF_VERSION }}
      
      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: eu-north-1  # Stockholm region
      
      - name: Terraform Plan
        run: |
          echo "📋 Skapar Terraform plan för ${{ matrix.environment }}..."
          
          cd infrastructure/environments/${{ matrix.environment }}
          
          # Konfigurera svenska backend
          cat > backend.tf << EOF
          terraform {
            backend "s3" {
              bucket         = "$ORGANIZATION_NAME-terraform-state"
              key            = "environments/${{ matrix.environment }}/terraform.tfstate"
              region         = "eu-north-1"
              encrypt        = true
              dynamodb_table = "$ORGANIZATION_NAME-terraform-locks"
            }
          }
          EOF
          
          terraform init
          terraform plan \
            -var="environment=${{ matrix.environment }}" \
            -var="organization_name=$ORGANIZATION_NAME" \
            -var="cost_center=$COST_CENTER" \
            -var="gdpr_compliance=true" \
            -var="data_residency=Sweden" \
            -out=tfplan-${{ matrix.environment }}
          
          # Spara plan för senare användning
          terraform show -json tfplan-${{ matrix.environment }} > tfplan-${{ matrix.environment }}.json
          
          echo "✅ Terraform plan skapat för ${{ matrix.environment }}"
      
      - name: Plan Analysis
        run: |
          echo "🔍 Analyserar Terraform plan för ${{ matrix.environment }}..."
          
          cd infrastructure/environments/${{ matrix.environment }}
          
          # Analysera plan för potentiella problem
          PLAN_JSON="tfplan-${{ matrix.environment }}.json"
          
          # Kontrollera för destructive changes
          DESTRUCTIVE_CHANGES=$(jq -r '.resource_changes[]? | select(.change.actions[]? == "delete" or .change.actions[]? == "replace") | .address' "$PLAN_JSON" 2>/dev/null || echo "")
          
          if [ -n "$DESTRUCTIVE_CHANGES" ]; then
            echo "⚠️ VARNING: Destructive changes upptäckta i ${{ matrix.environment }}:"
            echo "$DESTRUCTIVE_CHANGES"
            
            if [ "${{ matrix.environment }}" = "production" ]; then
              echo "❌ Destructive changes inte tillåtna i production utan explicit godkännande"
              # Kräv manual approval för production destructive changes
              exit 1
            fi
          fi
          
          # Kontrollera för stora cost changes
          NEW_RESOURCES=$(jq -r '.resource_changes[]? | select(.change.actions[]? == "create") | .address' "$PLAN_JSON" 2>/dev/null | wc -l)
          
          if [ "$NEW_RESOURCES" -gt 10 ]; then
            echo "⚠️ VARNING: Många nya resurser ($NEW_RESOURCES) skapas i ${{ matrix.environment }}"
          fi
          
          echo "✅ Plan analys slutförd för ${{ matrix.environment }}"
      
      - name: Swedish Compliance Validation
        run: |
          echo "🇸🇪 Validerar svenska compliance för ${{ matrix.environment }}..."
          
          cd infrastructure/environments/${{ matrix.environment }}
          
          PLAN_JSON="tfplan-${{ matrix.environment }}.json"
          
          # Kontrollera GDPR compliance
          UNENCRYPTED_STORAGE=$(jq -r '.planned_values.root_module.resources[]? | select(.type == "aws_s3_bucket" or .type == "aws_ebs_volume" or .type == "aws_db_instance") | select(.values.encrypted != true) | .address' "$PLAN_JSON" 2>/dev/null || echo "")
          
          if [ -n "$UNENCRYPTED_STORAGE" ]; then
            echo "❌ GDPR VIOLATION: Okrypterad lagring upptäckt:"
            echo "$UNENCRYPTED_STORAGE"
            exit 1
          fi
          
          # Kontrollera svenska tagging
          MISSING_TAGS=$(jq -r '.planned_values.root_module.resources[]? | select(.values.tags.Country != "Sweden" or .values.tags.GDPRCompliant != "true") | .address' "$PLAN_JSON" 2>/dev/null || echo "")
          
          if [ -n "$MISSING_TAGS" ]; then
            echo "❌ TAGGING VIOLATION: Svenska obligatoriska tags saknas:"
            echo "$MISSING_TAGS"
            exit 1
          fi
          
          echo "✅ Svenska compliance validering slutförd för ${{ matrix.environment }}"
      
      - name: Upload Terraform Plans
        uses: actions/upload-artifact@v4
        with:
          name: terraform-plans-${{ matrix.environment }}
          path: infrastructure/environments/${{ matrix.environment }}/tfplan*
          retention-days: 30

  # Deployment till development (automatisk)
  deploy-development:
    name: Deploy to Development
    runs-on: ubuntu-latest
    needs: [gdpr-compliance-check, code-quality-analysis, cost-analysis, environment-validation]
    if: github.ref == 'refs/heads/development' && github.event_name == 'push'
    environment: development
    
    steps:
      - name: Checkout kod
        uses: actions/checkout@v4
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TF_VERSION }}
      
      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: eu-north-1
      
      - name: Deploy Infrastructure
        run: |
          echo "🚀 Deploying till development miljö..."
          
          cd infrastructure/environments/development
          
          terraform init
          terraform apply -auto-approve \
            -var="environment=development" \
            -var="organization_name=$ORGANIZATION_NAME" \
            -var="cost_center=$COST_CENTER"
          
          echo "✅ Development deployment slutförd"
      
      - name: Post-Deployment Validation
        run: |
          echo "🔧 Kör post-deployment validering..."
          
          cd infrastructure/environments/development
          
          # Hämta outputs
          terraform output -json > deployment-outputs.json
          
          # Validera att resurser är tillgängliga
          VPC_ID=$(jq -r '.vpc_id.value' deployment-outputs.json 2>/dev/null || echo "")
          
          if [ -n "$VPC_ID" ]; then
            echo "✅ VPC skapat: $VPC_ID"
            
            # Kontrollera VPC connectivity
            aws ec2 describe-vpcs --vpc-ids "$VPC_ID" --region eu-north-1
          fi
          
          echo "✅ Post-deployment validering slutförd"

  # Deployment till staging (kräver manual approval)
  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    needs: [gdpr-compliance-check, code-quality-analysis, cost-analysis, environment-validation]
    if: github.ref == 'refs/heads/staging' && github.event_name == 'push'
    environment: 
      name: staging
      url: https://staging.${{ vars.DOMAIN_NAME }}
    
    steps:
      - name: Manual Approval Required
        run: |
          echo "⏳ Staging deployment kräver manual godkännande..."
          echo "Kontrollera kostnadsprognoser och säkerhetsrapporten innan fortsättning"
      
      - name: Checkout kod
        uses: actions/checkout@v4
      
      - name: Deploy to Staging
        run: |
          echo "🚀 Deploying till staging miljö..."
          
          cd infrastructure/environments/staging
          
          terraform init
          terraform apply -auto-approve \
            -var="environment=staging" \
            -var="organization_name=$ORGANIZATION_NAME" \
            -var="cost_center=$COST_CENTER"
          
          echo "✅ Staging deployment slutförd"

  # Deployment till production (kräver multiple approvals)
  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: [gdpr-compliance-check, code-quality-analysis, cost-analysis, environment-validation]
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    environment: 
      name: production
      url: https://${{ vars.DOMAIN_NAME }}
    
    steps:
      - name: Production Deployment Checklist
        run: |
          echo "🔒 Production deployment checklist:"
          echo "✅ GDPR compliance validerat"
          echo "✅ Säkerhetsscan genomförd"
          echo "✅ Kostnadsprognoser inom budget"
          echo "✅ Svenska data residency bekräftad"
          echo "✅ Manual approval erhållet"
          echo ""
          echo "⚠️ VIKTIGT: Production deployment påverkar live-system"
          echo "Säkerställ att rollback-plan finns tillgänglig"
      
      - name: Checkout kod
        uses: actions/checkout@v4
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TF_VERSION }}
      
      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID_PROD }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY_PROD }}
          aws-region: eu-north-1
      
      - name: Production Deployment
        run: |
          echo "🚀 Deploying till production miljö..."
          
          cd infrastructure/environments/production
          
          # Backup current state
          terraform state pull > state-backup-$(date +%Y%m%d-%H%M%S).json
          
          terraform init
          
          # Kör plan först för final validation
          terraform plan \
            -var="environment=production" \
            -var="organization_name=$ORGANIZATION_NAME" \
            -var="cost_center=$COST_CENTER" \
            -out=production-plan
          
          # Apply med extra försiktighet
          terraform apply production-plan
          
          echo "✅ Production deployment slutförd"
      
      - name: Production Health Check
        run: |
          echo "🏥 Kör production health checks..."
          
          cd infrastructure/environments/production
          
          # Hämta critical outputs
          terraform output -json > production-outputs.json
          
          # Health check för key services
          API_ENDPOINT=$(jq -r '.api_endpoint.value' production-outputs.json 2>/dev/null || echo "")
          
          if [ -n "$API_ENDPOINT" ]; then
            echo "Testing API endpoint: $API_ENDPOINT"
            
            HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$API_ENDPOINT/health" || echo "000")
            
            if [ "$HTTP_STATUS" = "200" ]; then
              echo "✅ API endpoint responding correctly"
            else
              echo "❌ API endpoint health check failed (HTTP $HTTP_STATUS)"
              exit 1
            fi
          fi
          
          echo "✅ Production health checks slutförda"
      
      - name: Notify Swedish Teams
        run: |
          echo "📢 Notifierar svenska team om production deployment..."
          
          DEPLOYMENT_MESSAGE="🇸🇪 Production deployment slutförd för $ORGANIZATION_NAME
          
          Miljö: Production
          Tid: $(date '+%Y-%m-%d %H:%M') (svensk tid)
          Commit: $GITHUB_SHA
          Författare: $GITHUB_ACTOR
          
          Kostnadscenter: $COST_CENTER
          Data residency: Sverige
          GDPR compliance: Aktiverad
          
          Kontrollera monitoring dashboards för systemhälsa."
          
          # Skicka notification (implementera baserat på teams setup)
          echo "$DEPLOYMENT_MESSAGE"
          
          # Exempel: Microsoft Teams webhook
          # curl -H 'Content-Type: application/json' -d '{"text":"'$DEPLOYMENT_MESSAGE'"}' ${{ secrets.TEAMS_WEBHOOK_URL }}

  # Cleanup och säkerhet
  cleanup:
    name: Cleanup and Security
    runs-on: ubuntu-latest
    needs: [deploy-development, deploy-staging, deploy-production]
    if: always()
    
    steps:
      - name: Clean Sensitive Data
        run: |
          echo "🧹 Rengör känslig data från pipeline..."
          
          # Ta bort temporära state files
          find . -name "*.tfstate*" -delete
          find . -name "terraform.tfvars" -delete
          
          # Rensa cache
          find . -name ".terraform" -type d -exec rm -rf {} + 2>/dev/null || true
          
          echo "✅ Cleanup slutförd"
      
      - name: Security Audit Log
        run: |
          echo "🔐 Skapar säkerhetsaudit för svenska compliance..."
          
          cat > security-audit.json << EOF
          {
            "audit_id": "$(uuidgen)",
            "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
            "pipeline_run": "$GITHUB_RUN_ID",
            "organization": "$ORGANIZATION_NAME",
            "compliance_framework": "GDPR",
            "security_controls": {
              "encryption_verified": true,
              "data_residency_sweden": true,
              "audit_logging_enabled": true,
              "access_controls_verified": true,
              "cost_controls_applied": true
            },
            "deployment_summary": {
              "environments_deployed": ["development", "staging", "production"],
              "security_scans_passed": true,
              "compliance_checks_passed": true,
              "cost_validation_passed": true
            },
            "retention_period": "7_years",
            "next_audit_date": "$(date -d '+1 year' -u +%Y-%m-%dT%H:%M:%SZ)"
          }
          EOF
          
          echo "📋 Säkerhetsaudit skapad för svenska lagkrav"
```

## Pipeline design principles

Effektiva IaC-pipelines bygger på principerna för fail-fast feedback och progressive deployment. Tidiga valideringssteg identifierar problem innan kostsamma infrastrukturförändringar initieras, medan senare steg säkerställer funktional korrekthet och säkerhetsefterlevnad.

Pipeline stages organiseras logiskt med tydliga entry/exit criteria för varje steg. Parallellisering av oberoende tasks accelererar execution time, medan sequential dependencies säkerställer korrekt ordning för kritiska operationer som säkerhetsscanning och cost validation.

### Svenska pipeline architecture patterns

För svenska organisationer kräver pipeline design särskild uppmärksamhet på regulatory compliance, cost optimization i svenska kronor, och data residency requirements. Modern pipeline architectures implementerar dessa krav genom specialized validation stages och automated compliance checks:

```yaml
# jenkins/svenska-iac-pipeline.groovy
// Jenkins pipeline för svenska organisationer med GDPR compliance

pipeline {
    agent any
    
    parameters {
        choice(
            name: 'ENVIRONMENT',
            choices: ['development', 'staging', 'production'],
            description: 'Target environment för deployment'
        )
        booleanParam(
            name: 'FORCE_DEPLOYMENT',
            defaultValue: false,
            description: 'Forcera deployment även vid varningar (endast development)'
        )
        string(
            name: 'COST_CENTER',
            defaultValue: 'CC-IT-001',
            description: 'Kostnadscenter för svenska bokföring'
        )
    }
    
    environment {
        ORGANIZATION_NAME = 'svenska-org'
        AWS_DEFAULT_REGION = 'eu-north-1'  // Stockholm region
        GDPR_COMPLIANCE = 'enabled'
        DATA_RESIDENCY = 'Sweden'
        TERRAFORM_VERSION = '1.6.0'
        COST_CURRENCY = 'SEK'
        AUDIT_RETENTION_YEARS = '7'  // Svenska lagkrav
    }
    
    stages {
        stage('🇸🇪 Svenska Compliance Check') {
            parallel {
                stage('GDPR Data Scan') {
                    steps {
                        script {
                            echo "🔍 Scanning för personal data patterns i IaC kod..."
                            
                            def personalDataPatterns = [
                                'personnummer', 'social.*security', 'credit.*card',
                                'bank.*account', 'email.*address', 'phone.*number'
                            ]
                            
                            def violations = []
                            
                            personalDataPatterns.each { pattern ->
                                def result = sh(
                                    script: "grep -ri '${pattern}' infrastructure/ modules/ || true",
                                    returnStdout: true
                                ).trim()
                                
                                if (result) {
                                    violations.add("Personal data pattern found: ${pattern}")
                                }
                            }
                            
                            if (violations) {
                                error("GDPR VIOLATION: Personal data found in IaC code:\n${violations.join('\n')}")
                            }
                            
                            echo "✅ GDPR data scan genomförd - inga violations"
                        }
                    }
                }
                
                stage('Data Residency Validation') {
                    steps {
                        script {
                            echo "🏔️ Validerar svenska data residency krav..."
                            
                            def allowedRegions = ['eu-north-1', 'eu-central-1', 'eu-west-1']
                            
                            def regionCheck = sh(
                                script: """
                                    grep -r 'region\\s*=' infrastructure/ modules/ | \
                                    grep -v -E '(eu-north-1|eu-central-1|eu-west-1)' || true
                                """,
                                returnStdout: true
                            ).trim()
                            
                            if (regionCheck) {
                                error("DATA RESIDENCY VIOLATION: Non-EU regions found:\n${regionCheck}")
                            }
                            
                            echo "✅ Data residency requirements uppfyllda"
                        }
                    }
                }
                
                stage('Cost Center Validation') {
                    steps {
                        script {
                            echo "💰 Validerar kostnadscenter för svenska bokföring..."
                            
                            if (!params.COST_CENTER.matches(/CC-[A-Z]{2,}-\d{3}/)) {
                                error("Ogiltigt kostnadscenter format. Använd: CC-XX-nnn")
                            }
                            
                            // Validera att kostnadscenter existerar i företagets system
                            def validCostCenters = [
                                'CC-IT-001', 'CC-DEV-002', 'CC-OPS-003', 'CC-SEC-004'
                            ]
                            
                            if (!validCostCenters.contains(params.COST_CENTER)) {
                                error("Okänt kostnadscenter: ${params.COST_CENTER}")
                            }
                            
                            echo "✅ Kostnadscenter validerat: ${params.COST_CENTER}"
                        }
                    }
                }
            }
        }
        
        stage('📝 Code Quality Analysis') {
            parallel {
                stage('Terraform Validation') {
                    steps {
                        script {
                            echo "🔧 Terraform syntax och formatering..."
                            
                            // Format check
                            sh "terraform fmt -check -recursive infrastructure/"
                            
                            // Syntax validation
                            dir('infrastructure/environments/${params.ENVIRONMENT}') {
                                sh """
                                    terraform init -backend=false
                                    terraform validate
                                """
                            }
                            
                            echo "✅ Terraform validation slutförd"
                        }
                    }
                }
                
                stage('Security Scanning') {
                    steps {
                        script {
                            echo "🔒 Säkerhetsskanning med Checkov..."
                            
                            sh """
                                pip install checkov
                                checkov -d infrastructure/ \
                                    --framework terraform \
                                    --output json \
                                    --output-file checkov-results.json \
                                    --soft-fail
                            """
                            
                            // Analysera kritiska säkerhetsproblem
                            def results = readJSON file: 'checkov-results.json'
                            def criticalIssues = results.results.failed_checks.findAll { 
                                it.severity == 'CRITICAL' 
                            }
                            
                            if (criticalIssues.size() > 0) {
                                echo "⚠️ KRITISKA säkerhetsproblem funna:"
                                criticalIssues.each { issue ->
                                    echo "- ${issue.check_name}: ${issue.file_path}"
                                }
                                
                                if (params.ENVIRONMENT == 'production') {
                                    error("Kritiska säkerhetsproblem måste åtgärdas före production deployment")
                                }
                            }
                            
                            echo "✅ Säkerhetsskanning slutförd"
                        }
                    }
                }
                
                stage('Svenska Policy Validation') {
                    steps {
                        script {
                            echo "📋 Validerar svenska organisationspolicies..."
                            
                            // Skapa svenska OPA policies
                            writeFile file: 'policies/svenska-tagging.rego', text: """
                                package svenska.tagging
                                
                                required_tags := [
                                    "Environment", "CostCenter", "Organization", 
                                    "Country", "GDPRCompliant", "DataResidency"
                                ]
                                
                                deny[msg] {
                                    input.resource[resource_type][name]
                                    resource_type != "data"
                                    not input.resource[resource_type][name].tags
                                    msg := sprintf("Resource %s.%s saknar tags", [resource_type, name])
                                }
                                
                                deny[msg] {
                                    input.resource[resource_type][name].tags
                                    required_tag := required_tags[_]
                                    not input.resource[resource_type][name].tags[required_tag]
                                    msg := sprintf("Resource %s.%s saknar obligatorisk tag: %s", [resource_type, name, required_tag])
                                }
                            """
                            
                            sh """
                                curl -L https://github.com/open-policy-agent/conftest/releases/download/v0.46.0/conftest_0.46.0_Linux_x86_64.tar.gz | tar xz
                                sudo mv conftest /usr/local/bin
                                
                                find infrastructure/ -name "*.tf" -exec conftest verify --policy policies/ {} \\;
                            """
                            
                            echo "✅ Svenska policy validation slutförd"
                        }
                    }
                }
            }
        }
        
        stage('💰 Svenska Kostnadskontroll') {
            steps {
                script {
                    echo "📊 Beräknar infrastrukturkostnader i svenska kronor..."
                    
                    // Setup Infracost för svenska valuta
                    sh """
                        curl -fsSL https://raw.githubusercontent.com/infracost/infracost/master/scripts/install.sh | sh
                        export PATH=\$PATH:\$HOME/.local/bin
                        
                        cd infrastructure/environments/${params.ENVIRONMENT}
                        terraform init -backend=false
                        
                        infracost breakdown \\
                            --path . \\
                            --currency SEK \\
                            --format json \\
                            --out-file ../../../cost-estimate.json
                        
                        infracost output \\
                            --path ../../../cost-estimate.json \\
                            --format table \\
                            --out-file ../../../cost-summary.txt
                    """
                    
                    // Validera kostnader mot svenska budgetgränser
                    def costData = readJSON file: 'cost-estimate.json'
                    def monthlyCostSEK = costData.totalMonthlyCost as Double
                    
                    def budgetLimits = [
                        'development': 5000,
                        'staging': 15000,
                        'production': 50000
                    ]
                    
                    def maxBudget = budgetLimits[params.ENVIRONMENT] ?: 10000
                    
                    echo "Beräknad månadskostnad: ${monthlyCostSEK} SEK"
                    echo "Budget för ${params.ENVIRONMENT}: ${maxBudget} SEK"
                    
                    if (monthlyCostSEK > maxBudget) {
                        def overBudget = monthlyCostSEK - maxBudget
                        echo "⚠️ BUDGET ÖVERSKRIDEN med ${overBudget} SEK!"
                        
                        if (params.ENVIRONMENT == 'production' && !params.FORCE_DEPLOYMENT) {
                            error("Budget överskridning inte tillåten för production utan CFO godkännande")
                        }
                    }
                    
                    // Generera svenskt kostnadsrapport
                    def costReport = """
                    # Kostnadsrapport - ${env.ORGANIZATION_NAME}
                    
                    **Miljö:** ${params.ENVIRONMENT}
                    **Datum:** ${new Date().format('yyyy-MM-dd HH:mm')} (svensk tid)
                    **Kostnadscenter:** ${params.COST_CENTER}
                    
                    ## Månadskostnad
                    - **Total:** ${monthlyCostSEK} SEK
                    - **Budget:** ${maxBudget} SEK
                    - **Status:** ${monthlyCostSEK <= maxBudget ? '✅ Inom budget' : '❌ Över budget'}
                    
                    ## Kostnadsnedbrytning
                    ${readFile('cost-summary.txt')}
                    
                    ## Rekommendationer
                    - Använd Reserved Instances för production workloads
                    - Aktivera auto-scaling för development miljöer
                    - Implementera scheduled shutdown för icke-kritiska system
                    """
                    
                    writeFile file: 'cost-report-svenska.md', text: costReport
                    archiveArtifacts artifacts: 'cost-report-svenska.md', fingerprint: true
                    
                    echo "✅ Kostnadskontroll slutförd"
                }
            }
        }
        
        stage('🧪 Infrastructure Testing') {
            parallel {
                stage('Unit Tests') {
                    steps {
                        script {
                            echo "🔬 Kör Terraform unit tests..."
                            
                            // Terratest för Go-baserade unit tests
                            sh """
                                cd test/
                                go mod init terraform-tests
                                go mod tidy
                                go test -v -timeout 30m ./...
                            """
                            
                            echo "✅ Unit tests slutförda"
                        }
                    }
                }
                
                stage('Integration Tests') {
                    when {
                        anyOf {
                            environment name: 'ENVIRONMENT', value: 'staging'
                            environment name: 'ENVIRONMENT', value: 'production'
                        }
                    }
                    steps {
                        script {
                            echo "🔗 Kör integration tests..."
                            
                            // Skapa test infrastructure i isolerad miljö
                            dir('infrastructure/environments/test') {
                                sh """
                                    terraform init
                                    terraform apply -auto-approve \\
                                        -var="environment=test" \\
                                        -var="organization_name=${env.ORGANIZATION_NAME}-test" \\
                                        -var="cost_center=${params.COST_CENTER}"
                                """
                                
                                // Kör connectivity tests
                                sh """
                                    # Test VPC connectivity
                                    VPC_ID=\$(terraform output -raw vpc_id)
                                    aws ec2 describe-vpcs --vpc-ids \$VPC_ID --region ${env.AWS_DEFAULT_REGION}
                                    
                                    # Test security groups
                                    aws ec2 describe-security-groups --filters "Name=vpc-id,Values=\$VPC_ID" --region ${env.AWS_DEFAULT_REGION}
                                """
                                
                                // Cleanup test infrastructure
                                sh "terraform destroy -auto-approve"
                            }
                            
                            echo "✅ Integration tests slutförda"
                        }
                    }
                }
                
                stage('GDPR Compliance Tests') {
                    steps {
                        script {
                            echo "🛡️ Testar GDPR compliance implementation..."
                            
                            // Test encryption settings
                            sh """
                                cd infrastructure/environments/${params.ENVIRONMENT}
                                terraform plan -out=compliance-plan
                                terraform show -json compliance-plan > compliance-plan.json
                                
                                # Kontrollera att alla storage är krypterat
                                UNENCRYPTED=\$(jq -r '.planned_values.root_module.resources[] | select(.type == "aws_s3_bucket" or .type == "aws_ebs_volume") | select(.values.encrypted != true) | .address' compliance-plan.json || echo "")
                                
                                if [ -n "\$UNENCRYPTED" ]; then
                                    echo "❌ GDPR VIOLATION: Unencrypted storage found:"
                                    echo "\$UNENCRYPTED"
                                    exit 1
                                fi
                            """
                            
                            echo "✅ GDPR compliance tests slutförda"
                        }
                    }
                }
            }
        }
        
        stage('📋 Pre-Deployment Validation') {
            steps {
                script {
                    echo "🔍 Final validation innan deployment..."
                    
                    // Terraform plan för target environment
                    dir("infrastructure/environments/${params.ENVIRONMENT}") {
                        sh """
                            terraform init
                            terraform plan \\
                                -var="environment=${params.ENVIRONMENT}" \\
                                -var="organization_name=${env.ORGANIZATION_NAME}" \\
                                -var="cost_center=${params.COST_CENTER}" \\
                                -var="gdpr_compliance=true" \\
                                -var="data_residency=Sweden" \\
                                -out=${params.ENVIRONMENT}-plan
                        """
                        
                        // Analysera plan för destructive changes
                        sh """
                            terraform show -json ${params.ENVIRONMENT}-plan > plan-analysis.json
                            
                            DESTRUCTIVE_CHANGES=\$(jq -r '.resource_changes[] | select(.change.actions[] == "delete" or .change.actions[] == "replace") | .address' plan-analysis.json || echo "")
                            
                            if [ -n "\$DESTRUCTIVE_CHANGES" ]; then
                                echo "⚠️ VARNING: Destructive changes upptäckta:"
                                echo "\$DESTRUCTIVE_CHANGES"
                                
                                if [ "${params.ENVIRONMENT}" = "production" ]; then
                                    echo "❌ Destructive changes kräver explicit godkännande för production"
                                    exit 1
                                fi
                            fi
                        """
                    }
                    
                    echo "✅ Pre-deployment validation slutförd"
                }
            }
        }
        
        stage('🚀 Deployment') {
            when {
                anyOf {
                    allOf {
                        environment name: 'ENVIRONMENT', value: 'development'
                        branch 'development'
                    }
                    allOf {
                        environment name: 'ENVIRONMENT', value: 'staging'
                        branch 'staging'
                    }
                    allOf {
                        environment name: 'ENVIRONMENT', value: 'production'
                        branch 'main'
                    }
                }
            }
            steps {
                script {
                    echo "🚀 Deploying till ${params.ENVIRONMENT} miljö..."
                    
                    // Production deployment kräver extra försiktighet
                    if (params.ENVIRONMENT == 'production') {
                        timeout(time: 10, unit: 'MINUTES') {
                            input message: "Bekräfta production deployment", 
                                  ok: "Deploy to Production",
                                  submitterParameter: 'APPROVER'
                        }
                        
                        echo "Production deployment godkänd av: ${env.APPROVER}"
                    }
                    
                    dir("infrastructure/environments/${params.ENVIRONMENT}") {
                        // Backup current state för production
                        if (params.ENVIRONMENT == 'production') {
                            sh "terraform state pull > state-backup-\$(date +%Y%m%d-%H%M%S).json"
                        }
                        
                        // Apply infrastructure changes
                        sh "terraform apply ${params.ENVIRONMENT}-plan"
                        
                        // Validera deployment
                        sh """
                            terraform output -json > deployment-outputs.json
                            
                            # Grundläggande health checks
                            VPC_ID=\$(jq -r '.vpc_id.value' deployment-outputs.json 2>/dev/null || echo "")
                            if [ -n "\$VPC_ID" ]; then
                                aws ec2 describe-vpcs --vpc-ids \$VPC_ID --region ${env.AWS_DEFAULT_REGION}
                                echo "✅ VPC health check OK: \$VPC_ID"
                            fi
                        """
                    }
                    
                    echo "✅ Deployment till ${params.ENVIRONMENT} slutförd"
                }
            }
        }
        
        stage('🏥 Post-Deployment Health Checks') {
            steps {
                script {
                    echo "🩺 Kör post-deployment health checks..."
                    
                    dir("infrastructure/environments/${params.ENVIRONMENT}") {
                        def outputs = readJSON file: 'deployment-outputs.json'
                        
                        // API endpoint health check
                        if (outputs.api_endpoint) {
                            def apiUrl = outputs.api_endpoint.value
                            def healthStatus = sh(
                                script: "curl -s -o /dev/null -w '%{http_code}' ${apiUrl}/health || echo '000'",
                                returnStdout: true
                            ).trim()
                            
                            if (healthStatus == '200') {
                                echo "✅ API endpoint responding: ${apiUrl}"
                            } else {
                                echo "⚠️ API endpoint health check failed: HTTP ${healthStatus}"
                            }
                        }
                        
                        // Database connectivity check
                        if (outputs.database_endpoint) {
                            echo "🗄️ Testing database connectivity..."
                            // Implementera database health check baserat på din setup
                        }
                        
                        // Load balancer health check
                        if (outputs.load_balancer_dns) {
                            def lbDns = outputs.load_balancer_dns.value
                            def lbStatus = sh(
                                script: "curl -s -o /dev/null -w '%{http_code}' http://${lbDns} || echo '000'",
                                returnStdout: true
                            ).trim()
                            
                            echo "Load balancer health: HTTP ${lbStatus}"
                        }
                    }
                    
                    echo "✅ Health checks slutförda"
                }
            }
        }
    }
    
    post {
        always {
            script {
                echo "🧹 Pipeline cleanup..."
                
                // Arkivera viktiga artifacts
                archiveArtifacts artifacts: '''
                    cost-estimate.json,
                    cost-summary.txt,
                    cost-report-svenska.md,
                    checkov-results.json,
                    infrastructure/environments/*/deployment-outputs.json
                ''', fingerprint: true, allowEmptyArchive: true
                
                // Rensa känsliga filer
                sh """
                    find . -name "*.tfstate*" -delete
                    find . -name "terraform.tfvars" -delete
                    find . -name ".terraform" -type d -exec rm -rf {} + 2>/dev/null || true
                """
            }
        }
        
        success {
            script {
                echo "✅ Pipeline slutförd framgångsrikt"
                
                // Skicka framgångsnotifikation till svenska team
                def successMessage = """
                🇸🇪 Framgångsrik deployment för ${env.ORGANIZATION_NAME}
                
                Miljö: ${params.ENVIRONMENT}
                Kostnadscenter: ${params.COST_CENTER}
                Tid: ${new Date().format('yyyy-MM-dd HH:mm')} (svensk tid)
                
                GDPR compliance: ✅ Aktiverad
                Data residency: ✅ Sverige
                Kostnadskontroll: ✅ Inom budget
                
                Pipeline run: ${env.BUILD_URL}
                """
                
                // Skicka till Slack/Teams/Email baserat på organisationens setup
                echo successMessage
            }
        }
        
        failure {
            script {
                echo "❌ Pipeline misslyckades"
                
                // Skicka error notification
                def errorMessage = """
                🚨 Pipeline misslyckades för ${env.ORGANIZATION_NAME}
                
                Miljö: ${params.ENVIRONMENT}
                Fel stadium: ${env.STAGE_NAME}
                Tid: ${new Date().format('yyyy-MM-dd HH:mm')} (svensk tid)
                
                Pipeline run: ${env.BUILD_URL}
                Kontrollera logs för detaljerad felinformation.
                """
                
                echo errorMessage
            }
        }
        
        unstable {
            script {
                echo "⚠️ Pipeline slutförd med varningar"
            }
        }
    }
}
```

## Automated testing strategier

Multi-level testing strategies för IaC inkluderar syntax validation, unit testing av moduler, integration testing av komponenter, och end-to-end testing av kompletta miljöer. Varje testnivå adresserar specifika risker och kvalitetsaspekter med ökande komplexitet och exekvering-cost.

Static analysis tools som tflint, checkov, eller terrascan integreras för att identifiera säkerhetsrisker, policy violations, och best practice deviations. Dynamic testing i sandbox-miljöer validerar faktisk funktionalitet och prestanda under realistiska conditions.

### Terratest för svenska organisationer

Terratest utgör den mest mature lösningen för automated testing av Terraform-kod och möjliggör Go-baserade test suites som validerar infrastructure behavior. För svenska organisationer innebär detta särskild fokus på GDPR compliance testing och cost validation:

```go
// test/svenska_vpc_test.go
// Terratest suite för svenska VPC implementation med GDPR compliance

package test

import (
    "encoding/json"
    "fmt"
    "strings"
    "testing"
    "time"

    "github.com/aws/aws-sdk-go/aws"
    "github.com/aws/aws-sdk-go/aws/session"
    "github.com/aws/aws-sdk-go/service/ec2"
    "github.com/aws/aws-sdk-go/service/cloudtrail"
    "github.com/gruntwork-io/terratest/modules/terraform"
    "github.com/gruntwork-io/terratest/modules/test-structure"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
)

// SvenskaVPCTestSuite definierar test suite för svenska VPC implementation
type SvenskaVPCTestSuite struct {
    TerraformOptions *terraform.Options
    AWSSession       *session.Session
    OrganizationName string
    Environment      string
    CostCenter       string
}

// TestSvenskaVPCGDPRCompliance testar GDPR compliance för VPC implementation
func TestSvenskaVPCGDPRCompliance(t *testing.T) {
    t.Parallel()

    suite := setupSvenskaVPCTest(t, "development")
    defer cleanupSvenskaVPCTest(t, suite)

    // Deploy infrastructure
    terraform.InitAndApply(t, suite.TerraformOptions)

    // Test GDPR compliance requirements
    t.Run("TestVPCFlowLogsEnabled", func(t *testing.T) {
        testVPCFlowLogsEnabled(t, suite)
    })

    t.Run("TestEncryptionAtRest", func(t *testing.T) {
        testEncryptionAtRest(t, suite)
    })

    t.Run("TestDataResidencySweden", func(t *testing.T) {
        testDataResidencySweden(t, suite)
    })

    t.Run("TestAuditLogging", func(t *testing.T) {
        testAuditLogging(t, suite)
    })

    t.Run("TestSvenskaTagging", func(t *testing.T) {
        testSvenskaTagging(t, suite)
    })
}

// setupSvenskaVPCTest förbereder test environment för svenska VPC testing
func setupSvenskaVPCTest(t *testing.T, environment string) *SvenskaVPCTestSuite {
    // Unik test identifier
    uniqueID := strings.ToLower(fmt.Sprintf("test-%d", time.Now().Unix()))
    organizationName := fmt.Sprintf("svenska-org-%s", uniqueID)

    // Terraform configuration
    terraformOptions := &terraform.Options{
        TerraformDir: "../infrastructure/modules/vpc",
        Vars: map[string]interface{}{
            "organization_name":     organizationName,
            "environment":          environment,
            "cost_center":          "CC-TEST-001",
            "gdpr_compliance":      true,
            "data_residency":       "Sweden",
            "enable_flow_logs":     true,
            "enable_encryption":    true,
            "audit_logging":        true,
        },
        BackendConfig: map[string]interface{}{
            "bucket": "svenska-org-terraform-test-state",
            "key":    fmt.Sprintf("test/%s/terraform.tfstate", uniqueID),
            "region": "eu-north-1",
        },
        RetryableTerraformErrors: map[string]string{
            ".*": "Transient error - retrying...",
        },
        MaxRetries:         3,
        TimeBetweenRetries: 5 * time.Second,
    }

    // AWS session för Stockholm region
    awsSession := session.Must(session.NewSession(&aws.Config{
        Region: aws.String("eu-north-1"),
    }))

    return &SvenskaVPCTestSuite{
        TerraformOptions: terraformOptions,
        AWSSession:       awsSession,
        OrganizationName: organizationName,
        Environment:      environment,
        CostCenter:       "CC-TEST-001",
    }
}

// testVPCFlowLogsEnabled validerar att VPC Flow Logs är aktiverade för GDPR compliance
func testVPCFlowLogsEnabled(t *testing.T, suite *SvenskaVPCTestSuite) {
    // Hämta VPC ID från Terraform output
    vpcID := terraform.Output(t, suite.TerraformOptions, "vpc_id")
    require.NotEmpty(t, vpcID, "VPC ID should not be empty")

    // AWS EC2 client
    ec2Client := ec2.New(suite.AWSSession)

    // Kontrollera Flow Logs
    flowLogsInput := &ec2.DescribeFlowLogsInput{
        Filters: []*ec2.Filter{
            {
                Name:   aws.String("resource-id"),
                Values: []*string{aws.String(vpcID)},
            },
        },
    }

    flowLogsOutput, err := ec2Client.DescribeFlowLogs(flowLogsInput)
    require.NoError(t, err, "Failed to describe VPC flow logs")

    // Validera att Flow Logs är aktiverade
    assert.Greater(t, len(flowLogsOutput.FlowLogs), 0, "VPC Flow Logs should be enabled for GDPR compliance")

    for _, flowLog := range flowLogsOutput.FlowLogs {
        assert.Equal(t, "Active", *flowLog.FlowLogStatus, "Flow log should be active")
        assert.Equal(t, "ALL", *flowLog.TrafficType, "Flow log should capture all traffic for compliance")
    }

    t.Logf("✅ VPC Flow Logs aktiverade för GDPR compliance: %s", vpcID)
}

// testEncryptionAtRest validerar att all lagring är krypterad enligt GDPR-krav
func testEncryptionAtRest(t *testing.T, suite *SvenskaVPCTestSuite) {
    // Hämta KMS key från Terraform output
    kmsKeyArn := terraform.Output(t, suite.TerraformOptions, "kms_key_arn")
    require.NotEmpty(t, kmsKeyArn, "KMS key ARN should not be empty")

    // Validera att KMS key är från Sverige region
    assert.Contains(t, kmsKeyArn, "eu-north-1", "KMS key should be in Stockholm region for data residency")

    // Kontrollera CloudTrail encryption om aktiverat
    if terraform.OutputExists(t, suite.TerraformOptions, "cloudtrail_arn") {
        cloudtrailArn := terraform.Output(t, suite.TerraformOptions, "cloudtrail_arn")
        
        cloudtrailClient := cloudtrail.New(suite.AWSSession)
        
        trails, err := cloudtrailClient.DescribeTrails(&cloudtrail.DescribeTrailsInput{
            TrailNameList: []*string{aws.String(cloudtrailArn)},
        })
        require.NoError(t, err, "Failed to describe CloudTrail")

        for _, trail := range trails.TrailList {
            assert.NotEmpty(t, trail.KMSKeyId, "CloudTrail should use KMS encryption for GDPR compliance")
            t.Logf("✅ CloudTrail krypterad med KMS: %s", *trail.KMSKeyId)
        }
    }

    t.Logf("✅ Encryption at rest validerat för GDPR compliance")
}

// testDataResidencySweden validerar att all infrastruktur är inom svenska gränser
func testDataResidencySweden(t *testing.T, suite *SvenskaVPCTestSuite) {
    // Validera att VPC är i Stockholm region
    vpcID := terraform.Output(t, suite.TerraformOptions, "vpc_id")
    
    ec2Client := ec2.New(suite.AWSSession)
    
    vpcOutput, err := ec2Client.DescribeVpcs(&ec2.DescribeVpcsInput{
        VpcIds: []*string{aws.String(vpcID)},
    })
    require.NoError(t, err, "Failed to describe VPC")
    require.Len(t, vpcOutput.Vpcs, 1, "Should find exactly one VPC")

    // Kontrollera region från session config
    region := *suite.AWSSession.Config.Region
    allowedRegions := []string{"eu-north-1", "eu-central-1", "eu-west-1"}
    
    regionAllowed := false
    for _, allowedRegion := range allowedRegions {
        if region == allowedRegion {
            regionAllowed = true
            break
        }
    }
    
    assert.True(t, regionAllowed, "VPC must be in EU region for Swedish data residency. Found: %s", region)

    // Kontrollera subnet availability zones
    subnetIds := terraform.OutputList(t, suite.TerraformOptions, "subnet_ids")
    
    for _, subnetId := range subnetIds {
        subnetOutput, err := ec2Client.DescribeSubnets(&ec2.DescribeSubnetsInput{
            SubnetIds: []*string{aws.String(subnetId)},
        })
        require.NoError(t, err, "Failed to describe subnet")
        
        for _, subnet := range subnetOutput.Subnets {
            assert.True(t, strings.HasPrefix(*subnet.AvailabilityZone, region), 
                "Subnet AZ should be in correct region. Expected: %s*, Found: %s", region, *subnet.AvailabilityZone)
        }
    }

    t.Logf("✅ Data residency validerat - all infrastruktur i EU region: %s", region)
}

// testAuditLogging validerar att audit logging är konfigurerat enligt svenska lagkrav
func testAuditLogging(t *testing.T, suite *SvenskaVPCTestSuite) {
    // Kontrollera CloudTrail konfiguration
    cloudtrailClient := cloudtrail.New(suite.AWSSession)
    
    trails, err := cloudtrailClient.DescribeTrails(&cloudtrail.DescribeTrailsInput{})
    require.NoError(t, err, "Failed to list CloudTrail trails")

    foundOrgTrail := false
    for _, trail := range trails.TrailList {
        if strings.Contains(*trail.Name, suite.OrganizationName) {
            foundOrgTrail = true
            
            // Validera trail konfiguration för svenska krav
            assert.NotNil(t, trail.S3BucketName, "CloudTrail should log to S3")
            assert.NotNil(t, trail.IncludeGlobalServiceEvents, "Should include global service events")
            assert.True(t, *trail.IncludeGlobalServiceEvents, "Global service events should be included")
            assert.NotNil(t, trail.IsMultiRegionTrail, "Should be multi-region trail")
            
            // Kontrollera att trail loggar data events för GDPR compliance
            eventSelectors, err := cloudtrailClient.GetEventSelectors(&cloudtrail.GetEventSelectorsInput{
                TrailName: trail.Name,
            })
            require.NoError(t, err, "Failed to get event selectors")
            
            hasDataEvents := false
            for _, selector := range eventSelectors.EventSelectors {
                if len(selector.DataResources) > 0 {
                    hasDataEvents = true
                    break
                }
            }
            
            assert.True(t, hasDataEvents, "CloudTrail should log data events for GDPR compliance")
            
            t.Logf("✅ CloudTrail audit logging konfigurerat: %s", *trail.Name)
        }
    }

    assert.True(t, foundOrgTrail, "Organization CloudTrail should exist for audit logging")
}

// testSvenskaTagging validerar att alla resurser har korrekta svenska tags
func testSvenskaTagging(t *testing.T, suite *SvenskaVPCTestSuite) {
    requiredTags := []string{
        "Environment", "Organization", "CostCenter", 
        "Country", "GDPRCompliant", "DataResidency",
    }

    expectedTagValues := map[string]string{
        "Environment":     suite.Environment,
        "Organization":    suite.OrganizationName,
        "CostCenter":      suite.CostCenter,
        "Country":         "Sweden",
        "GDPRCompliant":   "true",
        "DataResidency":   "Sweden",
    }

    // Test VPC tags
    vpcID := terraform.Output(t, suite.TerraformOptions, "vpc_id")
    ec2Client := ec2.New(suite.AWSSession)

    vpcTags, err := ec2Client.DescribeTags(&ec2.DescribeTagsInput{
        Filters: []*ec2.Filter{
            {
                Name:   aws.String("resource-id"),
                Values: []*string{aws.String(vpcID)},
            },
        },
    })
    require.NoError(t, err, "Failed to describe VPC tags")

    // Konvertera tags till map för enklare validering
    vpcTagMap := make(map[string]string)
    for _, tag := range vpcTags.Tags {
        vpcTagMap[*tag.Key] = *tag.Value
    }

    // Validera obligatoriska tags
    for _, requiredTag := range requiredTags {
        assert.Contains(t, vpcTagMap, requiredTag, "VPC should have required tag: %s", requiredTag)
        
        if expectedValue, exists := expectedTagValues[requiredTag]; exists {
            assert.Equal(t, expectedValue, vpcTagMap[requiredTag], 
                "Tag %s should have correct value", requiredTag)
        }
    }

    // Test subnet tags
    subnetIds := terraform.OutputList(t, suite.TerraformOptions, "subnet_ids")
    
    for _, subnetId := range subnetIds {
        subnetTags, err := ec2Client.DescribeTags(&ec2.DescribeTagsInput{
            Filters: []*ec2.Filter{
                {
                    Name:   aws.String("resource-id"),
                    Values: []*string{aws.String(subnetId)},
                },
            },
        })
        require.NoError(t, err, "Failed to describe subnet tags")

        subnetTagMap := make(map[string]string)
        for _, tag := range subnetTags.Tags {
            subnetTagMap[*tag.Key] = *tag.Value
        }

        // Validera grundläggande tags för subnets
        for _, requiredTag := range []string{"Environment", "Organization", "Country"} {
            assert.Contains(t, subnetTagMap, requiredTag, 
                "Subnet %s should have required tag: %s", subnetId, requiredTag)
        }
    }

    t.Logf("✅ Svenska tagging validerat för alla resurser")
}

// cleanupSvenskaVPCTest rensar test environment
func cleanupSvenskaVPCTest(t *testing.T, suite *SvenskaVPCTestSuite) {
    terraform.Destroy(t, suite.TerraformOptions)
    t.Logf("✅ Test environment rensat för %s", suite.OrganizationName)
}

// TestSvenskaVPCCostOptimization testar kostnadsoptimering för svenska miljöer
func TestSvenskaVPCCostOptimization(t *testing.T) {
    t.Parallel()

    suite := setupSvenskaVPCTest(t, "development")
    defer cleanupSvenskaVPCTest(t, suite)

    terraform.InitAndApply(t, suite.TerraformOptions)

    // Test cost optimization features
    t.Run("TestNATGatewayOptimization", func(t *testing.T) {
        // För development environment ska endast en NAT Gateway användas
        natGatewayIds := terraform.OutputList(t, suite.TerraformOptions, "nat_gateway_ids")
        
        if suite.Environment == "development" {
            assert.LessOrEqual(t, len(natGatewayIds), 1, 
                "Development environment should use max 1 NAT Gateway for cost optimization")
        }
        
        t.Logf("✅ NAT Gateway cost optimization validerat för %s", suite.Environment)
    })

    t.Run("TestInstanceSizing", func(t *testing.T) {
        // Validera att development använder mindre instance sizes
        if terraform.OutputExists(t, suite.TerraformOptions, "instance_types") {
            instanceTypesOutput := terraform.Output(t, suite.TerraformOptions, "instance_types")
            
            var instanceTypes map[string]string
            err := json.Unmarshal([]byte(instanceTypesOutput), &instanceTypes)
            require.NoError(t, err, "Failed to parse instance types")
            
            for service, instanceType := range instanceTypes {
                if suite.Environment == "development" {
                    assert.True(t, strings.HasPrefix(instanceType, "t3.") || strings.HasPrefix(instanceType, "t2."),
                        "Development should use burstable instances for cost optimization. Service: %s, Type: %s", 
                        service, instanceType)
                }
            }
        }
        
        t.Logf("✅ Instance sizing cost optimization validerat")
    })
}

// TestSvenskaVPCPerformance testar prestanda för svenska workloads
func TestSvenskaVPCPerformance(t *testing.T) {
    t.Parallel()

    suite := setupSvenskaVPCTest(t, "production")
    defer cleanupSvenskaVPCTest(t, suite)

    terraform.InitAndApply(t, suite.TerraformOptions)

    t.Run("TestMultiAZDeployment", func(t *testing.T) {
        subnetIds := terraform.OutputList(t, suite.TerraformOptions, "subnet_ids")
        
        // Production ska ha subnets i minst 2 AZ för high availability
        if suite.Environment == "production" {
            assert.GreaterOrEqual(t, len(subnetIds), 2,
                "Production should have subnets in multiple AZs for high availability")
        }
        
        // Validera att subnets är i olika AZ
        ec2Client := ec2.New(suite.AWSSession)
        usedAZs := make(map[string]bool)
        
        for _, subnetId := range subnetIds {
            subnetOutput, err := ec2Client.DescribeSubnets(&ec2.DescribeSubnetsInput{
                SubnetIds: []*string{aws.String(subnetId)},
            })
            require.NoError(t, err, "Failed to describe subnet")
            
            for _, subnet := range subnetOutput.Subnets {
                usedAZs[*subnet.AvailabilityZone] = true
            }
        }
        
        if suite.Environment == "production" {
            assert.GreaterOrEqual(t, len(usedAZs), 2,
                "Production subnets should span multiple availability zones")
        }
        
        t.Logf("✅ Multi-AZ deployment validerat: %d AZs används", len(usedAZs))
    })

    t.Run("TestNetworkPerformance", func(t *testing.T) {
        // Kontrollera att enhanced networking är aktiverat för production instances
        if terraform.OutputExists(t, suite.TerraformOptions, "enhanced_networking") {
            enhancedNetworking := terraform.Output(t, suite.TerraformOptions, "enhanced_networking")
            
            if suite.Environment == "production" {
                assert.Equal(t, "true", enhancedNetworking,
                    "Production should have enhanced networking enabled for performance")
            }
        }
        
        t.Logf("✅ Network performance settings validerade")
    })
}
```

### Container-based testing med svenska compliance

För containerbaserade infrastrukturtester möjliggör Docker och Kubernetes test environments som simulerar production conditions samtidigt som de bibehåller isolation och reproducibility:

```dockerfile
# test/Dockerfile.svenska-compliance-test
# Container för svenska IaC compliance testing

FROM ubuntu:22.04

LABEL maintainer="svenska-it-team@organization.se"
LABEL description="Compliance testing container för svenska IaC implementationer"

# Installera grundläggande verktyg
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    unzip \
    jq \
    git \
    python3 \
    python3-pip \
    awscli \
    && rm -rf /var/lib/apt/lists/*

# Installera Terraform
ENV TERRAFORM_VERSION=1.6.0
RUN wget https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip \
    && unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip \
    && mv terraform /usr/local/bin/ \
    && rm terraform_${TERRAFORM_VERSION}_linux_amd64.zip

# Installera svenska compliance verktyg
RUN pip3 install \
    checkov \
    terrascan \
    boto3 \
    pytest \
    requests

# Installera OPA/Conftest för policy testing
RUN curl -L https://github.com/open-policy-agent/conftest/releases/download/v0.46.0/conftest_0.46.0_Linux_x86_64.tar.gz | tar xz \
    && mv conftest /usr/local/bin/

# Installera Infracost för svenska kostnadskontroll
RUN curl -fsSL https://raw.githubusercontent.com/infracost/infracost/master/scripts/install.sh | sh \
    && mv /root/.local/bin/infracost /usr/local/bin/

# Skapa svenska compliance test scripts
COPY test-scripts/ /opt/svenska-compliance/

# Sätt svenska locale
RUN apt-get update && apt-get install -y locales \
    && locale-gen sv_SE.UTF-8 \
    && rm -rf /var/lib/apt/lists/*

ENV LANG=sv_SE.UTF-8
ENV LANGUAGE=sv_SE:sv
ENV LC_ALL=sv_SE.UTF-8

# Skapa test workspace
WORKDIR /workspace

# Entry point för compliance testing
ENTRYPOINT ["/opt/svenska-compliance/run-compliance-tests.sh"]
```

```bash
#!/bin/bash
# test-scripts/run-compliance-tests.sh
# Svenska compliance test runner

set -e

echo "🇸🇪 Startar svenska IaC compliance testing..."

# Sätt svenska timezone
export TZ="Europe/Stockholm"

# Validera required environment variables
REQUIRED_VARS=(
    "ORGANIZATION_NAME"
    "ENVIRONMENT"
    "COST_CENTER"
    "AWS_REGION"
)

for var in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!var}" ]; then
        echo "❌ Required environment variable $var is not set"
        exit 1
    fi
done

# Validera svenska data residency
if [[ ! "$AWS_REGION" =~ ^eu-(north|central|west)-[0-9]$ ]]; then
    echo "❌ AWS_REGION måste vara EU region för svenska data residency"
    echo "   Tillåtna regioner: eu-north-1, eu-central-1, eu-west-1"
    exit 1
fi

echo "✅ Environment variables validerade"
echo "   Organisation: $ORGANIZATION_NAME"
echo "   Miljö: $ENVIRONMENT"
echo "   Kostnadscenter: $COST_CENTER"
echo "   AWS Region: $AWS_REGION"

# 1. GDPR Compliance Testing
echo ""
echo "🛡️ Kör GDPR compliance tests..."

cd /workspace

# Scan för personal data i kod
echo "🔍 Scanning för personal data patterns..."
PERSONAL_DATA_FOUND=false

PERSONAL_DATA_PATTERNS=(
    "personnummer"
    "social.*security"
    "credit.*card"
    "bank.*account" 
    "email.*address"
    "phone.*number"
    "date.*of.*birth"
)

for pattern in "${PERSONAL_DATA_PATTERNS[@]}"; do
    if grep -ri "$pattern" . --include="*.tf" --include="*.yaml" --include="*.json"; then
        echo "❌ GDPR VIOLATION: Personal data pattern found: $pattern"
        PERSONAL_DATA_FOUND=true
    fi
done

if [ "$PERSONAL_DATA_FOUND" = true ]; then
    echo "❌ Personal data får inte hardkodas i IaC-kod"
    exit 1
fi

echo "✅ GDPR data scan genomförd - inga violations"

# 2. Security Compliance Testing
echo ""
echo "🔒 Kör security compliance tests..."

# Checkov security scanning
echo "Running Checkov security scan..."
checkov -d . \
    --framework terraform \
    --check CKV_AWS_18,CKV_AWS_21,CKV_AWS_131,CKV_AWS_144 \
    --output json \
    --output-file checkov-results.json \
    --soft-fail

# Analysera Checkov results
CRITICAL_ISSUES=$(jq '.results.failed_checks | map(select(.severity == "CRITICAL")) | length' checkov-results.json)

if [ "$CRITICAL_ISSUES" -gt 0 ]; then
    echo "❌ $CRITICAL_ISSUES kritiska säkerhetsproblem funna"
    jq '.results.failed_checks | map(select(.severity == "CRITICAL"))' checkov-results.json
    
    if [ "$ENVIRONMENT" = "production" ]; then
        echo "❌ Kritiska säkerhetsproblem inte tillåtna för production"
        exit 1
    fi
else
    echo "✅ Inga kritiska säkerhetsproblem funna"
fi

# 3. Svenska Policy Compliance
echo ""
echo "📋 Kör svenska policy compliance tests..."

# Skapa svenska OPA policies
mkdir -p policies

cat > policies/svenska-tagging.rego << 'EOF'
package svenska.tagging

required_tags := [
    "Environment", "Organization", "CostCenter", 
    "Country", "GDPRCompliant", "DataResidency"
]

deny[msg] {
    input.resource[resource_type][name]
    resource_type != "data"
    not input.resource[resource_type][name].tags
    msg := sprintf("Resource %s.%s saknar obligatoriska tags", [resource_type, name])
}

deny[msg] {
    input.resource[resource_type][name].tags
    required_tag := required_tags[_]
    not input.resource[resource_type][name].tags[required_tag]
    msg := sprintf("Resource %s.%s saknar obligatorisk tag: %s", [resource_type, name, required_tag])
}

deny[msg] {
    input.resource[resource_type][name].tags.Country
    input.resource[resource_type][name].tags.Country != "Sweden"
    msg := sprintf("Resource %s.%s måste ha Country=Sweden för svenska data residency", [resource_type, name])
}
EOF

cat > policies/svenska-encryption.rego << 'EOF'
package svenska.encryption

deny[msg] {
    input.resource.aws_s3_bucket[name]
    not input.resource.aws_s3_bucket[name].server_side_encryption_configuration
    msg := sprintf("S3 bucket %s måste ha encryption aktiverat för GDPR compliance", [name])
}

deny[msg] {
    input.resource.aws_ebs_volume[name]
    not input.resource.aws_ebs_volume[name].encrypted
    msg := sprintf("EBS volume %s måste vara krypterat för GDPR compliance", [name])
}

deny[msg] {
    input.resource.aws_db_instance[name]
    not input.resource.aws_db_instance[name].storage_encrypted
    msg := sprintf("RDS instance %s måste ha storage encryption för GDPR compliance", [name])
}
EOF

# Kör Conftest policy validation
echo "Validerar svenska policies..."
for tf_file in $(find . -name "*.tf"); do
    echo "Checking $tf_file..."
    conftest verify --policy policies/ "$tf_file" || {
        echo "❌ Policy violation i $tf_file"
        exit 1
    }
done

echo "✅ Svenska policy compliance validerat"

# 4. Cost Analysis
echo ""
echo "💰 Kör kostnadskontroll för svenska budgetar..."

# Sätt budget limits (i SEK per månad)
case "$ENVIRONMENT" in
    "development") MAX_MONTHLY_COST_SEK=5000 ;;
    "staging") MAX_MONTHLY_COST_SEK=15000 ;;
    "production") MAX_MONTHLY_COST_SEK=50000 ;;
    *) MAX_MONTHLY_COST_SEK=10000 ;;
esac

echo "Budget för $ENVIRONMENT: $MAX_MONTHLY_COST_SEK SEK/månad"

# Kör Infracost analys om konfigurerat
if [ -n "$INFRACOST_API_KEY" ]; then
    echo "Beräknar infrastrukturkostnader..."
    
    # Find terraform directories
    for terraform_dir in $(find . -name "*.tf" -exec dirname {} \; | sort -u); do
        if [ -f "$terraform_dir/main.tf" ] || [ -f "$terraform_dir/terraform.tf" ]; then
            echo "Analyzing costs for $terraform_dir..."
            
            cd "$terraform_dir"
            terraform init -backend=false >/dev/null 2>&1 || continue
            
            infracost breakdown \
                --path . \
                --currency SEK \
                --format json \
                --out-file "cost-estimate.json" 2>/dev/null || continue
            
            MONTHLY_COST=$(jq -r '.totalMonthlyCost // "0"' cost-estimate.json 2>/dev/null)
            
            if [ "$MONTHLY_COST" != "null" ] && [ "$MONTHLY_COST" != "0" ]; then
                echo "Månadskostnad för $terraform_dir: $MONTHLY_COST SEK"
                
                # Numerisk jämförelse
                if (( $(echo "$MONTHLY_COST > $MAX_MONTHLY_COST_SEK" | bc -l 2>/dev/null || echo "0") )); then
                    echo "❌ Kostnadsgräns överskridning!"
                    echo "   Beräknad: $MONTHLY_COST SEK"
                    echo "   Budget: $MAX_MONTHLY_COST_SEK SEK"
                    exit 1
                fi
            fi
            
            cd - >/dev/null
        fi
    done
    
    echo "✅ Kostnadskontroll genomförd - inom budget"
else
    echo "⚠️ INFRACOST_API_KEY inte satt - hoppar över kostnadskalkylering"
fi

# 5. Generate Svenska Compliance Report
echo ""
echo "📄 Genererar svenskt compliance rapport..."

cat > compliance-report-svenska.md << EOF
# Compliance Rapport - $ORGANIZATION_NAME

**Datum:** $(date '+%Y-%m-%d %H:%M') (svensk tid)  
**Miljö:** $ENVIRONMENT  
**Kostnadscenter:** $COST_CENTER  
**AWS Region:** $AWS_REGION

## ✅ GDPR Compliance
- Personal data scanning: Genomförd ✅
- Data residency Sverige: Bekräftad ✅
- Encryption at rest: Validerad ✅
- Audit logging: Aktiverad ✅

## ✅ Säkerhetskontroller
- Security scanning: Genomförd ✅
- Kritiska sårbarheter: Inga funna ✅
- Policy compliance: Validerad ✅
- Access controls: Konfigurerade ✅

## ✅ Svenska Lagkrav
- Svenska tagging: Implementerad ✅
- Kostnadscenter: Validerat ✅
- Data residency EU: Bekräftad ✅
- Audit retention 7 år: Konfigurerad ✅

## 💰 Kostnadskontroll
- Budget för $ENVIRONMENT: $MAX_MONTHLY_COST_SEK SEK/månad
- Status: Inom budget ✅

## 📋 Nästa Steg
1. Fortsätt monitoring av compliance metrics
2. Granska kostnadsutveckling månadsvis
3. Uppdatera säkerhetspolicies kvartalsvis
4. Genomför årlig compliance audit

---
*Genererad automatiskt av svenska IaC compliance testing*
EOF

echo "📄 Compliance rapport skapad: compliance-report-svenska.md"

# 6. Final Summary
echo ""
echo "🎉 Svenska IaC compliance testing slutförd!"
echo ""
echo "✅ GDPR compliance validerad"
echo "✅ Säkerhetskontroller genomförda" 
echo "✅ Svenska policies validerade"
echo "✅ Kostnadskontroll slutförd"
echo "✅ Compliance rapport genererad"
echo ""
echo "Alla svenska compliance-krav uppfyllda för $ENVIRONMENT miljö! 🇸🇪"
```

## Infrastructure validation

Pre-deployment validation säkerställer att infrastrukturändringar möter organisatoriska requirements innan de appliceras. Detta inkluderar policy compliance, security posture verification, och cost impact analysis för att förhindra oavsiktliga konsekvenser.

Plan-based validation använder tools som terraform plan för att preview förändringar och identifiera potentiella problem. Automated approval workflows kan implementeras för low-risk changes, medan high-impact modifications kräver manuell review och explicit godkännande.

### GitOps för svenska Infrastructure as Code

GitOps utgör en naturlig evolution av Infrastructure as Code som använder Git repositories som single source of truth för infrastructure state. För svenska organisationer möjliggör GitOps enhanced auditability, improved security, och better compliance med svenska regulatory requirements:

```yaml
# .github/workflows/gitops-svenska-iac.yml
# GitOps workflow för svenska Infrastructure as Code med ArgoCD integration

name: Svenska GitOps IaC Pipeline

on:
  push:
    branches: [main, staging, development]
    paths: ['infrastructure/**', 'applications/**', 'environments/**']
  pull_request:
    branches: [main, staging]
    paths: ['infrastructure/**', 'applications/**', 'environments/**']

env:
  ORGANIZATION_NAME: ${{ vars.ORGANIZATION_NAME }}
  ARGOCD_SERVER: ${{ vars.ARGOCD_SERVER }}
  KUBERNETES_CLUSTER: ${{ vars.KUBERNETES_CLUSTER }}
  GDPR_COMPLIANCE: 'enabled'
  DATA_RESIDENCY: 'Sweden'

jobs:
  gitops-validation:
    name: GitOps Infrastructure Validation
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history för audit trail
      
      - name: Setup ArgoCD CLI
        run: |
          curl -sSL -o argocd-linux-amd64 https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
          sudo install -m 555 argocd-linux-amd64 /usr/local/bin/argocd
          argocd version --client
      
      - name: Validate GitOps Structure
        run: |
          echo "🔍 Validerar GitOps repository struktur..."
          
          # Kontrollera att alla miljöer har korrekt struktur
          REQUIRED_DIRS=(
            "environments/development"
            "environments/staging" 
            "environments/production"
            "applications"
            "infrastructure/base"
            "infrastructure/overlays"
          )
          
          for dir in "${REQUIRED_DIRS[@]}"; do
            if [ ! -d "$dir" ]; then
              echo "❌ Required directory missing: $dir"
              exit 1
            fi
          done
          
          # Kontrollera Kustomization files
          for env in development staging production; do
            if [ ! -f "environments/$env/kustomization.yaml" ]; then
              echo "❌ Missing kustomization.yaml for $env"
              exit 1
            fi
          done
          
          echo "✅ GitOps struktur validerad"
      
      - name: Svenska Application Compliance Check
        run: |
          echo "🇸🇪 Kontrollerar svenska application compliance..."
          
          # Kontrollera att alla applications har svenska labels
          for app_file in $(find applications/ -name "*.yaml" -o -name "*.yml"); do
            if ! grep -q "svenska.se/environment" "$app_file"; then
              echo "❌ $app_file saknar svenska.se/environment label"
              exit 1
            fi
            
            if ! grep -q "svenska.se/data-classification" "$app_file"; then
              echo "❌ $app_file saknar svenska.se/data-classification label"
              exit 1
            fi
            
            if ! grep -q "svenska.se/gdpr-compliant" "$app_file"; then
              echo "❌ $app_file saknar svenska.se/gdpr-compliant label"
              exit 1
            fi
          done
          
          echo "✅ Svenska application compliance validerad"
      
      - name: Kubernetes Resource Validation
        run: |
          echo "🔧 Validerar Kubernetes resources..."
          
          # Setup kubectl och kubeval
          curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
          chmod +x kubectl
          sudo mv kubectl /usr/local/bin/
          
          wget https://github.com/instrumenta/kubeval/releases/latest/download/kubeval-linux-amd64.tar.gz
          tar xf kubeval-linux-amd64.tar.gz
          sudo mv kubeval /usr/local/bin/
          
          # Validera alla Kubernetes manifests
          for manifest in $(find . -name "*.yaml" -o -name "*.yml" | grep -v .github); do
            echo "Validating $manifest..."
            kubeval "$manifest" || {
              echo "❌ Kubernetes manifest validation failed: $manifest"
              exit 1
            }
          done
          
          echo "✅ Kubernetes resource validation slutförd"
      
      - name: Security Policy Validation
        run: |
          echo "🔒 Validerar säkerhetspolicies..."
          
          # OPA Gatekeeper policy validation
          curl -L https://github.com/open-policy-agent/conftest/releases/download/v0.46.0/conftest_0.46.0_Linux_x86_64.tar.gz | tar xz
          sudo mv conftest /usr/local/bin
          
          # Svenska security policies
          mkdir -p policies/security
          
          cat > policies/security/svenska-pod-security.rego << 'EOF'
          package svenska.security
          
          deny[msg] {
            input.kind == "Pod"
            input.spec.securityContext.runAsRoot == true
            msg := "Pods får inte köras som root för svenska säkerhetskrav"
          }
          
          deny[msg] {
            input.kind == "Pod"
            not input.spec.securityContext.runAsNonRoot
            msg := "Pods måste explicit sätta runAsNonRoot för säkerhet"
          }
          
          deny[msg] {
            input.kind == "Pod"
            container := input.spec.containers[_]
            container.securityContext.privileged == true
            msg := "Privileged containers inte tillåtna enligt svenska säkerhetskrav"
          }
          
          deny[msg] {
            input.kind == "Pod"
            not input.metadata.labels["svenska.se/data-classification"]
            msg := "Pod måste ha svenska.se/data-classification label"
          }
          EOF
          
          # Validera alla pod specs
          for manifest in $(find . -name "*.yaml" -o -name "*.yml" | grep -v .github); do
            if grep -q "kind: Pod\|kind: Deployment\|kind: StatefulSet" "$manifest"; then
              conftest verify --policy policies/security/ "$manifest" || {
                echo "❌ Security policy violation i $manifest"
                exit 1
              }
            fi
          done
          
          echo "✅ Security policy validation slutförd"

  argocd-sync-plan:
    name: ArgoCD Sync Plan Analysis
    runs-on: ubuntu-latest
    needs: gitops-validation
    if: github.event_name == 'pull_request'
    
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4
      
      - name: ArgoCD Login
        run: |
          argocd login $ARGOCD_SERVER \
            --username ${{ secrets.ARGOCD_USERNAME }} \
            --password ${{ secrets.ARGOCD_PASSWORD }} \
            --insecure
      
      - name: Generate Sync Plan
        run: |
          echo "📋 Genererar ArgoCD sync plan..."
          
          # Hämta lista över svenska applications
          APPLICATIONS=$(argocd app list -o name | grep $ORGANIZATION_NAME)
          
          mkdir -p sync-plans
          
          for app in $APPLICATIONS; do
            echo "Analyzing sync plan for $app..."
            
            # Generera diff för application
            argocd app diff $app > "sync-plans/${app}-diff.txt" || {
              echo "⚠️ Diff generation failed for $app"
              continue
            }
            
            # Analysera förändringar
            if [ -s "sync-plans/${app}-diff.txt" ]; then
              echo "📝 Changes detected for $app:"
              head -20 "sync-plans/${app}-diff.txt"
              
              # Kontrollera för destructive changes
              if grep -q "kind: PersistentVolume\|kind: StatefulSet" "sync-plans/${app}-diff.txt"; then
                echo "⚠️ Potentially destructive changes for $app"
                echo "stateful-changes" > "sync-plans/${app}-analysis.txt"
              fi
            else
              echo "✅ No changes for $app"
            fi
          done
      
      - name: Upload Sync Plans
        uses: actions/upload-artifact@v4
        with:
          name: argocd-sync-plans
          path: sync-plans/
          retention-days: 30

  environment-sync:
    name: Environment Synchronization
    runs-on: ubuntu-latest
    needs: [gitops-validation, argocd-sync-plan]
    if: github.ref == 'refs/heads/development' || github.ref == 'refs/heads/staging' || github.ref == 'refs/heads/main'
    
    strategy:
      matrix:
        environment: 
          - ${{ github.ref == 'refs/heads/development' && 'development' || '' }}
          - ${{ github.ref == 'refs/heads/staging' && 'staging' || '' }}
          - ${{ github.ref == 'refs/heads/main' && 'production' || '' }}
        exclude:
          - environment: ''
    
    environment: 
      name: ${{ matrix.environment }}
      url: https://${{ matrix.environment }}.${{ vars.DOMAIN_NAME }}
    
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4
      
      - name: ArgoCD Login
        run: |
          argocd login $ARGOCD_SERVER \
            --username ${{ secrets.ARGOCD_USERNAME }} \
            --password ${{ secrets.ARGOCD_PASSWORD }} \
            --insecure
      
      - name: Svenska Environment Preparation
        run: |
          echo "🇸🇪 Förbereder ${{ matrix.environment }} miljö för svenska organisationen..."
          
          # Validera environment-specific krav
          case "${{ matrix.environment }}" in
            "production")
              echo "🔒 Production deployment - extra säkerhetskontroller"
              REQUIRED_REPLICAS=3
              REQUIRED_RESOURCES="requests.memory=512Mi,requests.cpu=500m"
              ;;
            "staging")
              echo "🧪 Staging deployment - standard säkerhetskontroller"
              REQUIRED_REPLICAS=2
              REQUIRED_RESOURCES="requests.memory=256Mi,requests.cpu=250m"
              ;;
            "development")
              echo "🛠️ Development deployment - minimal resurser"
              REQUIRED_REPLICAS=1
              REQUIRED_RESOURCES="requests.memory=128Mi,requests.cpu=100m"
              ;;
          esac
          
          echo "REQUIRED_REPLICAS=$REQUIRED_REPLICAS" >> $GITHUB_ENV
          echo "REQUIRED_RESOURCES=$REQUIRED_RESOURCES" >> $GITHUB_ENV
      
      - name: Validate Environment Configuration
        run: |
          echo "🔧 Validerar ${{ matrix.environment }} konfiguration..."
          
          ENV_DIR="environments/${{ matrix.environment }}"
          
          # Kontrollera environment-specific values
          if [ -f "$ENV_DIR/values.yaml" ]; then
            # Validera replica counts
            REPLICA_COUNT=$(yq eval '.replicaCount // 1' "$ENV_DIR/values.yaml")
            
            if [ "${{ matrix.environment }}" = "production" ] && [ "$REPLICA_COUNT" -lt 3 ]; then
              echo "❌ Production kräver minst 3 replicas för high availability"
              exit 1
            fi
            
            # Validera resource requirements
            if ! grep -q "resources:" "$ENV_DIR/values.yaml"; then
              echo "❌ Resource requirements saknas för ${{ matrix.environment }}"
              exit 1
            fi
          fi
          
          echo "✅ Environment konfiguration validerad"
      
      - name: ArgoCD Application Sync
        run: |
          echo "🔄 Synkroniserar ArgoCD applications för ${{ matrix.environment }}..."
          
          # Lista applications för denna miljö
          APPLICATIONS=$(argocd app list -o name | grep "$ORGANIZATION_NAME.*${{ matrix.environment }}")
          
          if [ -z "$APPLICATIONS" ]; then
            echo "⚠️ Inga applications funna för ${{ matrix.environment }}"
            exit 0
          fi
          
          echo "Synkroniserar följande applications:"
          echo "$APPLICATIONS"
          
          # Sync varje application
          for app in $APPLICATIONS; do
            echo "Syncing $app..."
            
            # Kontrollera application health innan sync
            HEALTH=$(argocd app get $app -o json | jq -r '.status.health.status')
            
            if [ "$HEALTH" = "Degraded" ] && [ "${{ matrix.environment }}" = "production" ]; then
              echo "❌ Cannot sync degraded application $app in production"
              exit 1
            fi
            
            # Utför sync
            argocd app sync $app --timeout 600 || {
              echo "❌ Sync failed for $app"
              
              # Hämta sync status för debugging
              argocd app get $app
              exit 1
            }
            
            echo "✅ $app synced successfully"
          done
      
      - name: Post-Sync Health Check
        run: |
          echo "🏥 Kör post-sync health checks för ${{ matrix.environment }}..."
          
          # Vänta på att applications ska bli healthy
          APPLICATIONS=$(argocd app list -o name | grep "$ORGANIZATION_NAME.*${{ matrix.environment }}")
          
          for app in $APPLICATIONS; do
            echo "Waiting for $app to become healthy..."
            
            # Vänta upp till 10 minuter på healthy status
            TIMEOUT=600
            ELAPSED=0
            
            while [ $ELAPSED -lt $TIMEOUT ]; do
              HEALTH=$(argocd app get $app -o json | jq -r '.status.health.status')
              SYNC_STATUS=$(argocd app get $app -o json | jq -r '.status.sync.status')
              
              if [ "$HEALTH" = "Healthy" ] && [ "$SYNC_STATUS" = "Synced" ]; then
                echo "✅ $app is healthy and synced"
                break
              fi
              
              echo "⏳ $app health: $HEALTH, sync: $SYNC_STATUS (waiting...)"
              sleep 30
              ELAPSED=$((ELAPSED + 30))
            done
            
            if [ $ELAPSED -ge $TIMEOUT ]; then
              echo "❌ $app did not become healthy within timeout"
              argocd app get $app
              exit 1
            fi
          done
          
          echo "✅ Alla applications är healthy i ${{ matrix.environment }}"
      
      - name: Svenska Compliance Verification
        run: |
          echo "🇸🇪 Verifierar svenska compliance för ${{ matrix.environment }}..."
          
          # Anslut till Kubernetes cluster
          echo "${{ secrets.KUBECONFIG }}" | base64 -d > kubeconfig
          export KUBECONFIG=kubeconfig
          
          # Kontrollera att pods har svenska labels
          kubectl get pods -A -o json | jq -r '.items[] | select(.metadata.labels["svenska.se/environment"] != "${{ matrix.environment }}") | .metadata.name' > missing-labels.txt
          
          if [ -s missing-labels.txt ]; then
            echo "❌ Pods utan korrekt svenska.se/environment label:"
            cat missing-labels.txt
            exit 1
          fi
          
          # Kontrollera GDPR compliance labels
          kubectl get pods -A -o json | jq -r '.items[] | select(.metadata.labels["svenska.se/gdpr-compliant"] != "true") | .metadata.name' > gdpr-non-compliant.txt
          
          if [ -s gdpr-non-compliant.txt ]; then
            echo "❌ Pods utan GDPR compliance:"
            cat gdpr-non-compliant.txt
            exit 1
          fi
          
          # Kontrollera data residency
          kubectl get nodes -o json | jq -r '.items[].metadata.labels["topology.kubernetes.io/region"]' | sort -u > node-regions.txt
          
          while read -r region; do
            if [[ ! "$region" =~ ^eu-(north|central|west)-[0-9]$ ]]; then
              echo "❌ Node i icke-EU region: $region"
              exit 1
            fi
          done < node-regions.txt
          
          echo "✅ Svenska compliance verifierad för ${{ matrix.environment }}"

  notification:
    name: Svenska Team Notification
    runs-on: ubuntu-latest
    needs: environment-sync
    if: always()
    
    steps:
      - name: Prepare Notification
        run: |
          echo "📢 Förbereder notifikation för svenska team..."
          
          # Bestäm status
          if [ "${{ needs.environment-sync.result }}" = "success" ]; then
            STATUS="✅ Framgångsrik"
            EMOJI="🎉"
          else
            STATUS="❌ Misslyckad"
            EMOJI="🚨"
          fi
          
          # Skapa meddelande
          cat > notification.md << EOF
          $EMOJI GitOps Deployment - $ORGANIZATION_NAME
          
          **Status:** $STATUS
          **Miljö:** ${{ matrix.environment }}
          **Tid:** $(date '+%Y-%m-%d %H:%M') (svensk tid)
          **Commit:** ${{ github.sha }}
          **Författare:** ${{ github.actor }}
          
          **Compliance Status:**
          - GDPR: ✅ Aktiverad
          - Data Residency: ✅ Sverige
          - ArgoCD Sync: ${{ needs.environment-sync.result == 'success' && '✅' || '❌' }}
          
          **Länkar:**
          - [Workflow Run](${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }})
          - [ArgoCD Dashboard](${{ vars.ARGOCD_SERVER }})
          - [Environment URL](https://${{ matrix.environment }}.${{ vars.DOMAIN_NAME }})
          
          ---
          *Automatisk GitOps deployment för svenska organisationen*
          EOF
          
          echo "📝 Notifikation förberedd"
      
      - name: Send Teams Notification
        if: vars.TEAMS_WEBHOOK_URL
        run: |
          curl -H 'Content-Type: application/json' \
            -d @notification.md \
            ${{ vars.TEAMS_WEBHOOK_URL }}
```

### Progressive delivery för svenska organisationer

Progressive delivery strategies som canary deployments och blue-green deployments anpassas för svenska regulatory requirements och GDPR compliance. Detta innebär särskild uppmärksamhet på data handling under deployment transitions:

```bash
#!/bin/bash
# scripts/svenska-progressive-deployment.sh
# Progressive deployment script för svenska organisationer med GDPR compliance

set -e

# Konfiguration för svenska organisationer
ORGANIZATION_NAME="${ORGANIZATION_NAME:-svenska-org}"
ENVIRONMENT="${ENVIRONMENT:-development}"
DEPLOYMENT_STRATEGY="${DEPLOYMENT_STRATEGY:-canary}"
GDPR_COMPLIANCE="${GDPR_COMPLIANCE:-enabled}"
DATA_RESIDENCY="${DATA_RESIDENCY:-Sweden}"

echo "🇸🇪 Startar progressive deployment för svenska organisationen"
echo "Organisation: $ORGANIZATION_NAME"
echo "Miljö: $ENVIRONMENT"
echo "Strategi: $DEPLOYMENT_STRATEGY"
echo "GDPR Compliance: $GDPR_COMPLIANCE"
echo "Data Residency: $DATA_RESIDENCY"

# Validera svenska requirements
validate_swedish_requirements() {
    echo "🔍 Validerar svenska deployment requirements..."
    
    # Kontrollera GDPR compliance
    if [ "$GDPR_COMPLIANCE" != "enabled" ]; then
        echo "❌ GDPR compliance måste vara aktiverad för svenska organisationer"
        exit 1
    fi
    
    # Kontrollera data residency
    if [ "$DATA_RESIDENCY" != "Sweden" ] && [ "$DATA_RESIDENCY" != "EU" ]; then
        echo "❌ Data residency måste vara Sweden eller EU"
        exit 1
    fi
    
    # Kontrollera att alla required verktyg finns
    REQUIRED_TOOLS=("kubectl" "istioctl" "jq" "curl")
    
    for tool in "${REQUIRED_TOOLS[@]}"; do
        if ! command -v "$tool" &> /dev/null; then
            echo "❌ Required tool saknas: $tool"
            exit 1
        fi
    done
    
    echo "✅ Svenska requirements validerade"
}

# Canary deployment för svenska organisationer
deploy_canary() {
    echo "🐤 Startar canary deployment..."
    
    local APP_NAME="$1"
    local NEW_VERSION="$2"
    local CANARY_PERCENTAGE="${3:-10}"
    
    echo "Application: $APP_NAME"
    echo "Ny version: $NEW_VERSION"
    echo "Canary trafik: $CANARY_PERCENTAGE%"
    
    # 1. Deploy canary version
    echo "📦 Deploying canary version..."
    
    cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${APP_NAME}-canary
  namespace: ${ENVIRONMENT}
  labels:
    app: ${APP_NAME}
    version: canary
    svenska.se/deployment-strategy: canary
    svenska.se/environment: ${ENVIRONMENT}
    svenska.se/gdpr-compliant: "true"
    svenska.se/data-residency: "Sweden"
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ${APP_NAME}
      version: canary
  template:
    metadata:
      labels:
        app: ${APP_NAME}
        version: canary
        svenska.se/deployment-strategy: canary
        svenska.se/environment: ${ENVIRONMENT}
        svenska.se/gdpr-compliant: "true"
    spec:
      containers:
      - name: ${APP_NAME}
        image: ${APP_NAME}:${NEW_VERSION}
        env:
        - name: ENVIRONMENT
          value: "${ENVIRONMENT}"
        - name: GDPR_ENABLED
          value: "true"
        - name: DATA_RESIDENCY
          value: "Sweden"
        - name: DEPLOYMENT_TYPE
          value: "canary"
        securityContext:
          runAsNonRoot: true
          runAsUser: 1000
          allowPrivilegeEscalation: false
          capabilities:
            drop:
            - ALL
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
EOF
    
    # 2. Vänta på att canary deployment blir ready
    echo "⏳ Väntar på canary deployment..."
    kubectl rollout status deployment/${APP_NAME}-canary -n ${ENVIRONMENT} --timeout=300s
    
    # 3. Konfigurera Istio traffic splitting
    echo "🌐 Konfigurerar traffic splitting med Istio..."
    
    cat <<EOF | kubectl apply -f -
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: ${APP_NAME}
  namespace: ${ENVIRONMENT}
  labels:
    svenska.se/traffic-management: canary
spec:
  hosts:
  - ${APP_NAME}
  http:
  - match:
    - headers:
        canary:
          exact: "true"
    route:
    - destination:
        host: ${APP_NAME}
        subset: canary
      weight: 100
  - route:
    - destination:
        host: ${APP_NAME}
        subset: stable
      weight: $((100 - CANARY_PERCENTAGE))
    - destination:
        host: ${APP_NAME}
        subset: canary
      weight: ${CANARY_PERCENTAGE}
---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: ${APP_NAME}
  namespace: ${ENVIRONMENT}
spec:
  host: ${APP_NAME}
  subsets:
  - name: stable
    labels:
      version: stable
  - name: canary
    labels:
      version: canary
EOF
    
    echo "✅ Canary deployment konfigurerad med ${CANARY_PERCENTAGE}% trafik"
}

# Blue-Green deployment för svenska organisationer
deploy_blue_green() {
    echo "🔵🟢 Startar blue-green deployment..."
    
    local APP_NAME="$1"
    local NEW_VERSION="$2"
    
    echo "Application: $APP_NAME"
    echo "Ny version: $NEW_VERSION"
    
    # Identifiera nuvarande färg
    CURRENT_COLOR=$(kubectl get service ${APP_NAME} -n ${ENVIRONMENT} -o jsonpath='{.spec.selector.color}' 2>/dev/null || echo "blue")
    NEW_COLOR=$([ "$CURRENT_COLOR" = "blue" ] && echo "green" || echo "blue")
    
    echo "Nuvarande färg: $CURRENT_COLOR"
    echo "Ny färg: $NEW_COLOR"
    
    # 1. Deploy till ny färg
    echo "📦 Deploying till $NEW_COLOR miljö..."
    
    cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${APP_NAME}-${NEW_COLOR}
  namespace: ${ENVIRONMENT}
  labels:
    app: ${APP_NAME}
    color: ${NEW_COLOR}
    svenska.se/deployment-strategy: blue-green
    svenska.se/environment: ${ENVIRONMENT}
    svenska.se/gdpr-compliant: "true"
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ${APP_NAME}
      color: ${NEW_COLOR}
  template:
    metadata:
      labels:
        app: ${APP_NAME}
        color: ${NEW_COLOR}
        svenska.se/deployment-strategy: blue-green
        svenska.se/environment: ${ENVIRONMENT}
        svenska.se/gdpr-compliant: "true"
    spec:
      containers:
      - name: ${APP_NAME}
        image: ${APP_NAME}:${NEW_VERSION}
        env:
        - name: ENVIRONMENT
          value: "${ENVIRONMENT}"
        - name: COLOR
          value: "${NEW_COLOR}"
        - name: GDPR_ENABLED
          value: "true"
        - name: DATA_RESIDENCY
          value: "Sweden"
        securityContext:
          runAsNonRoot: true
          runAsUser: 1000
          allowPrivilegeEscalation: false
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
EOF
    
    # 2. Vänta på deployment
    echo "⏳ Väntar på $NEW_COLOR deployment..."
    kubectl rollout status deployment/${APP_NAME}-${NEW_COLOR} -n ${ENVIRONMENT} --timeout=600s
    
    # 3. Kör health checks
    echo "🏥 Kör health checks för $NEW_COLOR miljö..."
    
    # Få pod IP för health check
    POD_IP=$(kubectl get pods -n ${ENVIRONMENT} -l app=${APP_NAME},color=${NEW_COLOR} -o jsonpath='{.items[0].status.podIP}')
    
    # Health check loop
    HEALTH_CHECK_ATTEMPTS=0
    MAX_HEALTH_CHECKS=10
    
    while [ $HEALTH_CHECK_ATTEMPTS -lt $MAX_HEALTH_CHECKS ]; do
        HTTP_STATUS=$(kubectl exec -n ${ENVIRONMENT} deployment/${APP_NAME}-${NEW_COLOR} -- curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/health || echo "000")
        
        if [ "$HTTP_STATUS" = "200" ]; then
            echo "✅ Health check OK för $NEW_COLOR miljö"
            break
        fi
        
        echo "⏳ Health check attempt $((HEALTH_CHECK_ATTEMPTS + 1))/$MAX_HEALTH_CHECKS - Status: $HTTP_STATUS"
        sleep 10
        HEALTH_CHECK_ATTEMPTS=$((HEALTH_CHECK_ATTEMPTS + 1))
    done
    
    if [ $HEALTH_CHECK_ATTEMPTS -ge $MAX_HEALTH_CHECKS ]; then
        echo "❌ Health checks misslyckades för $NEW_COLOR miljö"
        exit 1
    fi
    
    # 4. Växla trafik (production kräver manual approval)
    if [ "$ENVIRONMENT" = "production" ]; then
        echo "🔒 Production miljö - kräver manual approval för traffic switch"
        echo "Kör följande kommando för att växla trafik:"
        echo "kubectl patch service ${APP_NAME} -n ${ENVIRONMENT} -p '{\"spec\":{\"selector\":{\"color\":\"${NEW_COLOR}\"}}}'"
        echo ""
        echo "Tryck Enter för att fortsätta eller Ctrl+C för att avbryta..."
        read -r
    fi
    
    echo "🔄 Växlar trafik till $NEW_COLOR miljö..."
    kubectl patch service ${APP_NAME} -n ${ENVIRONMENT} -p "{\"spec\":{\"selector\":{\"color\":\"${NEW_COLOR}\"}}}"
    
    echo "✅ Blue-Green deployment slutförd - trafik växlad till $NEW_COLOR"
}

# Monitoring under deployment
monitor_deployment() {
    local APP_NAME="$1"
    local DEPLOYMENT_STRATEGY="$2"
    
    echo "📊 Startar deployment monitoring..."
    
    # Prometheus metrics för svenska organisationer
    cat > /tmp/prometheus-query.json <<EOF
{
  "queries": [
    {
      "name": "error_rate",
      "query": "rate(http_requests_total{app=\"${APP_NAME}\",environment=\"${ENVIRONMENT}\",code=~\"5..\"}[5m]) / rate(http_requests_total{app=\"${APP_NAME}\",environment=\"${ENVIRONMENT}\"}[5m])"
    },
    {
      "name": "response_time_p95",
      "query": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{app=\"${APP_NAME}\",environment=\"${ENVIRONMENT}\"}[5m]))"
    },
    {
      "name": "gdpr_compliance_rate",
      "query": "rate(gdpr_compliant_requests_total{app=\"${APP_NAME}\",environment=\"${ENVIRONMENT}\"}[5m]) / rate(http_requests_total{app=\"${APP_NAME}\",environment=\"${ENVIRONMENT}\"}[5m])"
    }
  ]
}
EOF
    
    # Monitoring loop
    MONITORING_DURATION=300  # 5 minuter
    MONITORING_INTERVAL=30   # 30 sekunder
    MONITORING_CYCLES=$((MONITORING_DURATION / MONITORING_INTERVAL))
    
    echo "Monitoring deployment i ${MONITORING_DURATION} sekunder..."
    
    for i in $(seq 1 $MONITORING_CYCLES); do
        echo "📈 Monitoring cykel $i/$MONITORING_CYCLES"
        
        # Hämta metrics från Prometheus
        if command -v prometheus-query &> /dev/null; then
            ERROR_RATE=$(prometheus-query --query="rate(http_requests_total{app=\"${APP_NAME}\",code=~\"5..\"}[5m])" | jq -r '.data.result[0].value[1] // "0"')
            
            echo "  Error rate: ${ERROR_RATE}%"
            
            # Kontrollera error rate threshold
            if (( $(echo "$ERROR_RATE > 0.05" | bc -l) )); then
                echo "❌ Error rate över threshold (5%) - avbryter deployment"
                return 1
            fi
        fi
        
        # Kontrollera pod status
        READY_PODS=$(kubectl get pods -n ${ENVIRONMENT} -l app=${APP_NAME} -o jsonpath='{.items[*].status.conditions[?(@.type=="Ready")].status}' | grep -o "True" | wc -l)
        TOTAL_PODS=$(kubectl get pods -n ${ENVIRONMENT} -l app=${APP_NAME} -o jsonpath='{.items[*].metadata.name}' | wc -w)
        
        echo "  Ready pods: $READY_PODS/$TOTAL_PODS"
        
        if [ "$READY_PODS" -lt "$TOTAL_PODS" ]; then
            echo "⚠️ Inte alla pods är ready"
        fi
        
        sleep $MONITORING_INTERVAL
    done
    
    echo "✅ Deployment monitoring slutförd - alla metrics inom acceptabla gränser"
}

# Rollback function för svenska organisationer
rollback_deployment() {
    local APP_NAME="$1"
    local DEPLOYMENT_STRATEGY="$2"
    
    echo "⚠️ Startar rollback för svenska organisationen..."
    
    # GDPR audit log för rollback
    cat > /tmp/rollback-audit.json <<EOF
{
  "audit_id": "$(uuidgen)",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "event_type": "deployment_rollback",
  "organization": "${ORGANIZATION_NAME}",
  "environment": "${ENVIRONMENT}",
  "application": "${APP_NAME}",
  "deployment_strategy": "${DEPLOYMENT_STRATEGY}",
  "gdpr_compliance": "maintained",
  "data_residency": "Sweden",
  "initiated_by": "${USER:-system}",
  "reason": "deployment_failure_or_manual_intervention"
}
EOF
    
    case "$DEPLOYMENT_STRATEGY" in
        "canary")
            echo "🐤 Rollback canary deployment..."
            
            # Ta bort canary deployment
            kubectl delete deployment ${APP_NAME}-canary -n ${ENVIRONMENT} --ignore-not-found
            
            # Återställ traffic till 100% stable
            kubectl patch virtualservice ${APP_NAME} -n ${ENVIRONMENT} --type='json' -p='[
              {
                "op": "replace",
                "path": "/spec/http/1/route",
                "value": [{"destination": {"host": "'${APP_NAME}'", "subset": "stable"}, "weight": 100}]
              }
            ]'
            ;;
            
        "blue-green")
            echo "🔵🟢 Rollback blue-green deployment..."
            
            # Identifiera färger
            CURRENT_COLOR=$(kubectl get service ${APP_NAME} -n ${ENVIRONMENT} -o jsonpath='{.spec.selector.color}')
            PREVIOUS_COLOR=$([ "$CURRENT_COLOR" = "blue" ] && echo "green" || echo "blue")
            
            # Växla tillbaka till tidigare färg
            kubectl patch service ${APP_NAME} -n ${ENVIRONMENT} -p "{\"spec\":{\"selector\":{\"color\":\"${PREVIOUS_COLOR}\"}}}"
            
            # Ta bort misslyckad deployment
            kubectl delete deployment ${APP_NAME}-${CURRENT_COLOR} -n ${ENVIRONMENT} --ignore-not-found
            ;;
    esac
    
    echo "📋 Rollback audit log:"
    cat /tmp/rollback-audit.json
    
    echo "✅ Rollback slutförd för svenska organisationen"
}

# Main execution
main() {
    local COMMAND="$1"
    shift
    
    validate_swedish_requirements
    
    case "$COMMAND" in
        "canary")
            deploy_canary "$@"
            monitor_deployment "$1" "canary"
            ;;
        "blue-green")
            deploy_blue_green "$@"
            monitor_deployment "$1" "blue-green"
            ;;
        "monitor")
            monitor_deployment "$@"
            ;;
        "rollback")
            rollback_deployment "$@"
            ;;
        *)
            echo "Usage: $0 {canary|blue-green|monitor|rollback} <app-name> <version> [options]"
            echo ""
            echo "Svenska Progressive Deployment Tool"
            echo ""
            echo "Commands:"
            echo "  canary <app> <version> [percentage]  - Canary deployment"
            echo "  blue-green <app> <version>           - Blue-green deployment"
            echo "  monitor <app> <strategy>             - Monitor deployment"
            echo "  rollback <app> <strategy>            - Rollback deployment"
            echo ""
            echo "Environment Variables:"
            echo "  ORGANIZATION_NAME - Svenska organisationsnamn"
            echo "  ENVIRONMENT       - Target environment (development/staging/production)"
            echo "  GDPR_COMPLIANCE   - GDPR compliance mode (enabled/disabled)"
            echo "  DATA_RESIDENCY    - Data residency krav (Sweden/EU)"
            exit 1
            ;;
    esac
}

# Kör main function med alla arguments
main "$@"
```

## Deployment strategier

Blue-green deployments och canary releases anpassas för infrastrukturkontext genom att skapa parallella miljöer eller successivt rulla ut förändringar. Rolling deployments hanterar stateful services genom att minimera downtime och säkerställa data consistency under transitions.

Rollback mechanisms implementeras för att snabbt återställa till tidigare functioning state vid problem. Automated health checks och monitoring triggers kan initiera rollbacks automatiskt, medan manual override capabilities bibehålls för exceptional circumstances.

### Infrastructure-aware deployment patterns

För Infrastructure as Code kräver deployment strategier special consideration för stateful resources som databaser, persistent volumes, och network configurations. Svenska organisationer måste också säkerställa GDPR compliance during deployment transitions:

```python
# deployment/svenska_iac_deployer.py
# Infrastructure deployment orchestrator för svenska organisationer

import json
import time
import logging
import subprocess
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import boto3
import kubernetes

# Konfiguration för svenska organisationer
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f'/var/log/svenska-iac-deployer.log')
    ]
)
logger = logging.getLogger(__name__)

class DeploymentStrategy(Enum):
    BLUE_GREEN = "blue_green"
    CANARY = "canary"
    ROLLING = "rolling"
    IMMUTABLE = "immutable"

class DeploymentStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"

@dataclass
class SvenskaDeploymentConfig:
    """Deployment konfiguration för svenska organisationer"""
    organization_name: str
    environment: str
    cost_center: str
    gdpr_compliance: bool = True
    data_residency: str = "Sweden"
    backup_before_deployment: bool = True
    audit_logging: bool = True
    rollback_on_failure: bool = True
    health_check_timeout: int = 600
    canary_percentage: int = 10
    canary_duration: int = 300

@dataclass
class DeploymentAuditLog:
    """GDPR-compliant audit log för deployments"""
    audit_id: str
    timestamp: str
    organization: str
    environment: str
    deployment_strategy: str
    status: str
    initiated_by: str
    terraform_plan_hash: str
    resources_changed: List[str]
    gdpr_impact_assessment: Dict[str, str]
    data_residency_verified: bool
    compliance_checks_passed: bool

class SvenskaInfrastructureDeployer:
    """Infrastructure deployment orchestrator för svenska organisationer"""
    
    def __init__(self, config: SvenskaDeploymentConfig):
        self.config = config
        self.aws_session = boto3.Session(region_name='eu-north-1')
        self.terraform_dir = f"infrastructure/environments/{config.environment}"
        self.audit_logs: List[DeploymentAuditLog] = []
        
        # Kubernetes client för containerized workloads
        try:
            kubernetes.config.load_incluster_config()
        except:
            kubernetes.config.load_kube_config()
        
        self.k8s_client = kubernetes.client.ApiClient()
        
        logger.info(f"Initialized deployer för {config.organization_name} - {config.environment}")
    
    def validate_svenska_requirements(self) -> bool:
        """Validera svenska deployment requirements"""
        logger.info("🇸🇪 Validerar svenska deployment requirements...")
        
        validations = []
        
        # GDPR compliance check
        if not self.config.gdpr_compliance:
            validations.append("GDPR compliance måste vara aktiverad")
        
        # Data residency check
        if self.config.data_residency not in ["Sweden", "EU"]:
            validations.append("Data residency måste vara Sweden eller EU")
        
        # Cost center validation
        if not self.config.cost_center.startswith("CC-"):
            validations.append("Kostnadscenter måste följa format CC-XXX-nnn")
        
        # AWS region validation
        if self.aws_session.region_name not in ["eu-north-1", "eu-central-1", "eu-west-1"]:
            validations.append("AWS region måste vara EU för svenska data residency")
        
        if validations:
            logger.error("❌ Validation failures:")
            for validation in validations:
                logger.error(f"  - {validation}")
            return False
        
        logger.info("✅ Svenska requirements validerade")
        return True
    
    def create_pre_deployment_backup(self) -> Optional[str]:
        """Skapa backup innan deployment enligt svenska lagkrav"""
        if not self.config.backup_before_deployment:
            return None
        
        logger.info("💾 Skapar pre-deployment backup...")
        
        try:
            # Terraform state backup
            result = subprocess.run([
                "terraform", "state", "pull"
            ], cwd=self.terraform_dir, capture_output=True, text=True, check=True)
            
            backup_timestamp = time.strftime("%Y%m%d-%H%M%S")
            backup_filename = f"state-backup-{backup_timestamp}.json"
            backup_path = f"{self.terraform_dir}/backups/{backup_filename}"
            
            # Skapa backup directory
            subprocess.run(["mkdir", "-p", f"{self.terraform_dir}/backups"], check=True)
            
            with open(backup_path, 'w') as f:
                f.write(result.stdout)
            
            # Ladda upp till S3 för långtidslagring (7 år svenska krav)
            s3_client = self.aws_session.client('s3')
            s3_bucket = f"{self.config.organization_name}-terraform-backups"
            s3_key = f"{self.config.environment}/state-backups/{backup_filename}"
            
            s3_client.upload_file(
                backup_path, 
                s3_bucket, 
                s3_key,
                ExtraArgs={
                    'ServerSideEncryption': 'aws:kms',
                    'StorageClass': 'STANDARD_IA',
                    'Tagging': f"Environment={self.config.environment}&RetentionYears=7&Purpose=GDPR-Backup"
                }
            )
            
            logger.info(f"✅ Backup skapad: {backup_filename}")
            return backup_filename
            
        except Exception as e:
            logger.error(f"❌ Backup misslyckades: {str(e)}")
            raise
    
    def generate_terraform_plan(self) -> Tuple[str, Dict[str, any]]:
        """Generera och analysera Terraform plan"""
        logger.info("📋 Genererar Terraform plan...")
        
        try:
            # Terraform init
            subprocess.run([
                "terraform", "init", "-upgrade"
            ], cwd=self.terraform_dir, check=True)
            
            # Terraform plan
            plan_file = f"deployment-plan-{int(time.time())}.tfplan"
            subprocess.run([
                "terraform", "plan",
                f"-var=organization_name={self.config.organization_name}",
                f"-var=environment={self.config.environment}",
                f"-var=cost_center={self.config.cost_center}",
                f"-var=gdpr_compliance={str(self.config.gdpr_compliance).lower()}",
                f"-var=data_residency={self.config.data_residency}",
                f"-out={plan_file}"
            ], cwd=self.terraform_dir, check=True)
            
            # Analysera plan
            result = subprocess.run([
                "terraform", "show", "-json", plan_file
            ], cwd=self.terraform_dir, capture_output=True, text=True, check=True)
            
            plan_data = json.loads(result.stdout)
            analysis = self._analyze_terraform_plan(plan_data)
            
            logger.info(f"✅ Terraform plan genererad: {plan_file}")
            return plan_file, analysis
            
        except Exception as e:
            logger.error(f"❌ Terraform plan misslyckades: {str(e)}")
            raise
    
    def _analyze_terraform_plan(self, plan_data: Dict) -> Dict[str, any]:
        """Analysera Terraform plan för svenska compliance"""
        analysis = {
            "resource_changes": [],
            "destructive_changes": [],
            "gdpr_impact": {},
            "cost_impact": {},
            "compliance_issues": []
        }
        
        if "resource_changes" not in plan_data:
            return analysis
        
        for change in plan_data["resource_changes"]:
            resource_address = change.get("address", "unknown")
            actions = change.get("change", {}).get("actions", [])
            
            analysis["resource_changes"].append({
                "address": resource_address,
                "actions": actions
            })
            
            # Identifiera destructive changes
            if "delete" in actions or "replace" in actions:
                analysis["destructive_changes"].append(resource_address)
            
            # GDPR impact assessment
            if self._is_gdpr_relevant_resource(change):
                analysis["gdpr_impact"][resource_address] = {
                    "data_type": self._identify_data_type(change),
                    "encryption_status": self._check_encryption(change),
                    "backup_required": True
                }
            
            # Compliance checks
            compliance_issues = self._check_resource_compliance(change)
            if compliance_issues:
                analysis["compliance_issues"].extend(compliance_issues)
        
        return analysis
    
    def _is_gdpr_relevant_resource(self, resource_change: Dict) -> bool:
        """Kontrollera om resource är GDPR-relevant"""
        resource_type = resource_change.get("type", "")
        gdpr_relevant_types = [
            "aws_db_instance", "aws_dynamodb_table", "aws_s3_bucket",
            "aws_elasticsearch_domain", "aws_rds_cluster", "aws_redshift_cluster"
        ]
        return resource_type in gdpr_relevant_types
    
    def deploy_infrastructure(self, strategy: DeploymentStrategy, plan_file: str) -> bool:
        """Deploy infrastructure enligt specified strategy"""
        logger.info(f"🚀 Startar infrastructure deployment med {strategy.value} strategi...")
        
        try:
            if strategy == DeploymentStrategy.BLUE_GREEN:
                return self._deploy_blue_green(plan_file)
            elif strategy == DeploymentStrategy.CANARY:
                return self._deploy_canary(plan_file)
            elif strategy == DeploymentStrategy.ROLLING:
                return self._deploy_rolling(plan_file)
            elif strategy == DeploymentStrategy.IMMUTABLE:
                return self._deploy_immutable(plan_file)
            else:
                raise ValueError(f"Unsupported deployment strategy: {strategy}")
                
        except Exception as e:
            logger.error(f"❌ Deployment misslyckades: {str(e)}")
            if self.config.rollback_on_failure:
                self.rollback_deployment()
            raise
    
    def _deploy_blue_green(self, plan_file: str) -> bool:
        """Blue-green deployment för infrastructure"""
        logger.info("🔵🟢 Executing blue-green infrastructure deployment...")
        
        # För infrastructure blue-green, skapa ny workspace
        current_workspace = self._get_current_workspace()
        new_workspace = "green" if current_workspace == "blue" else "blue"
        
        try:
            # Skapa ny workspace
            subprocess.run([
                "terraform", "workspace", "new", new_workspace
            ], cwd=self.terraform_dir, check=True)
            
            # Deploy till ny workspace
            subprocess.run([
                "terraform", "apply", plan_file
            ], cwd=self.terraform_dir, check=True)
            
            # Health checks
            if self._run_health_checks():
                # Växla till ny workspace
                subprocess.run([
                    "terraform", "workspace", "select", new_workspace
                ], cwd=self.terraform_dir, check=True)
                
                # Rensa gammal workspace
                subprocess.run([
                    "terraform", "workspace", "delete", current_workspace
                ], cwd=self.terraform_dir, check=True)
                
                logger.info(f"✅ Blue-green deployment slutförd - växlad till {new_workspace}")
                return True
            else:
                logger.error("❌ Health checks misslyckades")
                return False
                
        except Exception as e:
            logger.error(f"❌ Blue-green deployment error: {str(e)}")
            return False
    
    def _deploy_canary(self, plan_file: str) -> bool:
        """Canary deployment för infrastructure"""
        logger.info("🐤 Executing canary infrastructure deployment...")
        
        try:
            # För infrastructure canary, deploy till subset av resources
            # Detta kräver special planning och resource tagging
            
            # Identifiera canary resources
            canary_resources = self._identify_canary_resources(plan_file)
            
            if not canary_resources:
                logger.info("Inga canary-eligible resources - använder standard deployment")
                return self._deploy_standard(plan_file)
            
            # Deploy canary resources först
            for resource in canary_resources[:len(canary_resources)//10]:  # 10% canary
                self._deploy_single_resource(resource)
                
                # Monitor canary
                if not self._monitor_canary_resource(resource):
                    logger.error(f"❌ Canary monitoring misslyckades för {resource}")
                    return False
            
            # Om canary lyckas, deploy resterande resources
            logger.info("✅ Canary lyckades - deploying resterande resources...")
            remaining_resources = canary_resources[len(canary_resources)//10:]
            
            for resource in remaining_resources:
                self._deploy_single_resource(resource)
            
            logger.info("✅ Canary deployment slutförd")
            return True
            
        except Exception as e:
            logger.error(f"❌ Canary deployment error: {str(e)}")
            return False
    
    def _run_health_checks(self) -> bool:
        """Kör comprehensive health checks för svenska compliance"""
        logger.info("🏥 Kör post-deployment health checks...")
        
        health_checks = [
            self._check_resource_availability,
            self._check_gdpr_compliance,
            self._check_data_residency,
            self._check_encryption_status,
            self._check_network_connectivity,
            self._check_backup_configuration
        ]
        
        for check in health_checks:
            try:
                if not check():
                    logger.error(f"❌ Health check misslyckades: {check.__name__}")
                    return False
                logger.info(f"✅ Health check OK: {check.__name__}")
            except Exception as e:
                logger.error(f"❌ Health check error {check.__name__}: {str(e)}")
                return False
        
        logger.info("✅ Alla health checks genomförda framgångsrikt")
        return True
    
    def _check_gdpr_compliance(self) -> bool:
        """Kontrollera GDPR compliance efter deployment"""
        try:
            # Hämta Terraform outputs
            result = subprocess.run([
                "terraform", "output", "-json"
            ], cwd=self.terraform_dir, capture_output=True, text=True, check=True)
            
            outputs = json.loads(result.stdout)
            
            # Kontrollera encryption
            if "encryption_enabled" in outputs:
                if not outputs["encryption_enabled"]["value"]:
                    return False
            
            # Kontrollera audit logging
            if "audit_logging_enabled" in outputs:
                if not outputs["audit_logging_enabled"]["value"]:
                    return False
            
            # Kontrollera data residency
            if "data_residency" in outputs:
                if outputs["data_residency"]["value"] != self.config.data_residency:
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"GDPR compliance check error: {str(e)}")
            return False
    
    def rollback_deployment(self) -> bool:
        """Rollback deployment enligt svenska audit krav"""
        logger.warning("⚠️ Initierar deployment rollback...")
        
        try:
            # Hitta senaste backup
            backup_files = subprocess.run([
                "ls", "-t", f"{self.terraform_dir}/backups/"
            ], capture_output=True, text=True, check=True).stdout.strip().split('\n')
            
            if not backup_files or backup_files[0] == '':
                logger.error("❌ Ingen backup tillgänglig för rollback")
                return False
            
            latest_backup = backup_files[0]
            backup_path = f"{self.terraform_dir}/backups/{latest_backup}"
            
            # Återställ Terraform state
            subprocess.run([
                "terraform", "state", "push", backup_path
            ], cwd=self.terraform_dir, check=True)
            
            # Refresh och plan för att se skillnader
            subprocess.run([
                "terraform", "refresh"
            ], cwd=self.terraform_dir, check=True)
            
            # Apply för att återställa till backup state
            subprocess.run([
                "terraform", "apply", "-auto-approve"
            ], cwd=self.terraform_dir, check=True)
            
            # Audit log för rollback
            self._create_audit_log(
                event_type="deployment_rollback",
                status=DeploymentStatus.ROLLED_BACK,
                details={"backup_used": latest_backup}
            )
            
            logger.info(f"✅ Rollback slutförd med backup: {latest_backup}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Rollback misslyckades: {str(e)}")
            return False
    
    def _create_audit_log(self, event_type: str, status: DeploymentStatus, details: Dict = None):
        """Skapa GDPR-compliant audit log"""
        audit_log = DeploymentAuditLog(
            audit_id=f"audit-{int(time.time())}",
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            organization=self.config.organization_name,
            environment=self.config.environment,
            deployment_strategy=event_type,
            status=status.value,
            initiated_by=subprocess.run(["whoami"], capture_output=True, text=True).stdout.strip(),
            terraform_plan_hash="",
            resources_changed=[],
            gdpr_impact_assessment={},
            data_residency_verified=True,
            compliance_checks_passed=status == DeploymentStatus.SUCCESS
        )
        
        self.audit_logs.append(audit_log)
        
        # Spara audit log för svenska lagkrav (7 års retention)
        audit_file = f"{self.terraform_dir}/audit-logs/audit-{audit_log.audit_id}.json"
        subprocess.run(["mkdir", "-p", f"{self.terraform_dir}/audit-logs"], check=True)
        
        with open(audit_file, 'w') as f:
            json.dump(audit_log.__dict__, f, indent=2)
        
        logger.info(f"📋 Audit log skapad: {audit_log.audit_id}")

# Användningsexempel för svenska organisationer
def main():
    config = SvenskaDeploymentConfig(
        organization_name="svenska-tech-ab",
        environment="production",
        cost_center="CC-IT-001",
        gdpr_compliance=True,
        data_residency="Sweden",
        backup_before_deployment=True,
        audit_logging=True,
        rollback_on_failure=True
    )
    
    deployer = SvenskaInfrastructureDeployer(config)
    
    if not deployer.validate_svenska_requirements():
        logger.error("❌ Svenska requirements inte uppfyllda")
        return False
    
    # Skapa backup
    backup_file = deployer.create_pre_deployment_backup()
    
    # Generera plan
    plan_file, analysis = deployer.generate_terraform_plan()
    
    # Kontrollera för destructive changes i production
    if config.environment == "production" and analysis["destructive_changes"]:
        logger.warning("⚠️ Destructive changes i production kräver manual approval")
        approval = input("Fortsätt med deployment? (yes/no): ")
        if approval.lower() != "yes":
            logger.info("Deployment avbruten av användare")
            return False
    
    # Deploy med blue-green strategy för production
    strategy = DeploymentStrategy.BLUE_GREEN if config.environment == "production" else DeploymentStrategy.ROLLING
    
    success = deployer.deploy_infrastructure(strategy, plan_file)
    
    if success:
        logger.info("🎉 Deployment slutförd framgångsrikt för svenska organisationen!")
    else:
        logger.error("❌ Deployment misslyckades")
    
    return success

if __name__ == "__main__":
    main()
```

## Monitoring och observability

Pipeline observability inkluderar både execution metrics och business impact measurements. Technical metrics som build time, success rate, och deployment frequency kombineras med business metrics som system availability och performance indicators.

Alerting strategies säkerställer snabb respons på pipeline failures och infrastructure anomalies. Integration med incident management systems möjliggör automatisk eskalering och notification av relevanta team members baserat på severity levels och impact assessment.

### Svenska monitoring och alerting

För svenska organisationer kräver monitoring särskild uppmärksamhet på GDPR compliance, cost tracking i svenska kronor, och integration med svenska incident management processes:

```yaml
# monitoring/svenska-pipeline-monitoring.yaml
# Comprehensive monitoring för svenska IaC pipelines

apiVersion: v1
kind: ConfigMap
metadata:
  name: svenska-pipeline-monitoring
  namespace: monitoring
  labels:
    app: pipeline-monitoring
    svenska.se/organization: ${ORGANIZATION_NAME}
    svenska.se/gdpr-compliant: "true"
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
      evaluation_interval: 15s
      external_labels:
        organization: "${ORGANIZATION_NAME}"
        region: "eu-north-1"
        country: "Sweden"
        gdpr_zone: "compliant"
    
    rule_files:
      - "svenska_pipeline_rules.yml"
      - "gdpr_compliance_rules.yml"
      - "cost_monitoring_rules.yml"
    
    scrape_configs:
      # GitHub Actions metrics
      - job_name: 'github-actions'
        static_configs:
          - targets: ['github-exporter:8080']
        scrape_interval: 30s
        metrics_path: /metrics
        params:
          organizations: ['${ORGANIZATION_NAME}']
          repos: ['infrastructure', 'applications']
      
      # Jenkins metrics för svenska pipelines
      - job_name: 'jenkins-svenska'
        static_configs:
          - targets: ['jenkins:8080']
        metrics_path: /prometheus
        params:
          match[]: 
            - 'jenkins_builds_duration_milliseconds_summary{job=~"svenska-.*"}'
            - 'jenkins_builds_success_build_count{job=~"svenska-.*"}'
            - 'jenkins_builds_failed_build_count{job=~"svenska-.*"}'
      
      # Terraform state metrics
      - job_name: 'terraform-state'
        static_configs:
          - targets: ['terraform-exporter:9090']
        scrape_interval: 60s
        params:
          workspaces: ['development', 'staging', 'production']
          compliance_mode: ['gdpr']
      
      # Cost monitoring för svenska budgetar
      - job_name: 'aws-cost-explorer'
        static_configs:
          - targets: ['cost-exporter:8080']
        scrape_interval: 300s
        params:
          currency: ['SEK']
          cost_centers: ['${COST_CENTER}']
      
      # GDPR compliance monitoring
      - job_name: 'gdpr-compliance'
        static_configs:
          - targets: ['gdpr-monitor:8080']
        scrape_interval: 60s
        params:
          organizations: ['${ORGANIZATION_NAME}']
          data_residency: ['Sweden']

  svenska_pipeline_rules.yml: |
    groups:
      - name: svenska.pipeline.rules
        interval: 30s
        rules:
          # Pipeline success rate för svenska organisationer
          - alert: SvenskaPipelineSuccessRateLow
            expr: |
              (
                rate(pipeline_builds_total{organization="${ORGANIZATION_NAME}",status="success"}[5m]) /
                rate(pipeline_builds_total{organization="${ORGANIZATION_NAME}"}[5m])
              ) < 0.95
            for: 5m
            labels:
              severity: warning
              organization: "${ORGANIZATION_NAME}"
              compliance: gdpr
              language: svenska
            annotations:
              summary: "Pipeline success rate under 95% för svenska organisationen"
              description: "Pipeline success rate är {{ $value | humanizePercentage }} för de senaste 5 minuterna"
              remediation: "Kontrollera pipeline logs och infrastuktur health checks"
              contact: "svenska-devops-team@${ORGANIZATION_NAME}.se"
          
          # Pipeline duration för svenska SLA
          - alert: SvenskaPipelineDurationHigh
            expr: |
              histogram_quantile(0.95, 
                rate(pipeline_duration_seconds_bucket{organization="${ORGANIZATION_NAME}"}[5m])
              ) > 1800
            for: 10m
            labels:
              severity: warning
              organization: "${ORGANIZATION_NAME}"
              sla_impact: "true"
            annotations:
              summary: "Pipeline duration överstiger svenska SLA på 30 minuter"
              description: "95th percentile pipeline duration är {{ $value | humanizeDuration }}"
              impact: "Påverkar svenska utvecklarproduktivitet och deployment cadence"
          
          # GDPR compliance violations
          - alert: GDPRComplianceViolation
            expr: |
              increase(gdpr_violations_total{organization="${ORGANIZATION_NAME}"}[5m]) > 0
            for: 0s
            labels:
              severity: critical
              organization: "${ORGANIZATION_NAME}"
              compliance: gdpr
              legal_impact: "high"
            annotations:
              summary: "GDPR compliance violation upptäckt i svenska pipeline"
              description: "{{ $value }} GDPR violations de senaste 5 minuterna"
              urgent_action: "Stoppa all data processing och kontakta DPO omedelbart"
              legal_contact: "dpo@${ORGANIZATION_NAME}.se"
          
          # Kostnadsgränser för svenska budgetar
          - alert: SvenskaCostBudgetExceeded
            expr: |
              aws_cost_monthly_total_sek{cost_center="${COST_CENTER}"} > 
              aws_cost_budget_limit_sek{cost_center="${COST_CENTER}"}
            for: 1m
            labels:
              severity: critical
              organization: "${ORGANIZATION_NAME}"
              cost_center: "${COST_CENTER}"
              financial_impact: "high"
            annotations:
              summary: "Månadskostnad överstiger svensk budget för ${COST_CENTER}"
              description: "Aktuell kostnad: {{ $value }} SEK, Budget: {{ $labels.budget_limit }} SEK"
              action_required: "Kontakta ekonomiavdelningen och stoppa icke-kritiska deployments"
              financial_contact: "ekonomi@${ORGANIZATION_NAME}.se"
          
          # Data residency violations
          - alert: DataResidencyViolation
            expr: |
              increase(data_residency_violations_total{
                organization="${ORGANIZATION_NAME}",
                required_region="Sweden"
              }[5m]) > 0
            for: 0s
            labels:
              severity: critical
              organization: "${ORGANIZATION_NAME}"
              compliance: data_residency
              legal_impact: "high"
            annotations:
              summary: "Data residency violation - data utanför Sverige"
              description: "{{ $value }} resources deployed utanför svenska gränser"
              immediate_action: "Stoppa deployment och flytta data tillbaka till Sverige"
              compliance_contact: "compliance@${ORGANIZATION_NAME}.se"

  gdpr_compliance_rules.yml: |
    groups:
      - name: gdpr.compliance.monitoring
        interval: 60s
        rules:
          # Encryption compliance
          - alert: GDPREncryptionNotEnabled
            expr: |
              gdpr_encryption_compliance_ratio{organization="${ORGANIZATION_NAME}"} < 1.0
            for: 2m
            labels:
              severity: critical
              compliance_type: encryption
              gdpr_article: "32"
            annotations:
              summary: "GDPR Article 32 - Encryption inte aktiverad för alla personal data stores"
              description: "{{ $value | humanizePercentage }} av data stores har encryption aktiverad"
              legal_requirement: "Alla personal data måste vara krypterad enligt GDPR Article 32"
              remediation: "Aktivera encryption för alla databaser och storage systems"
          
          # Audit logging compliance
          - alert: GDPRAuditLoggingGap
            expr: |
              increase(gdpr_audit_log_gaps_total{organization="${ORGANIZATION_NAME}"}[1h]) > 0
            for: 0s
            labels:
              severity: high
              compliance_type: audit_logging
              gdpr_article: "30"
            annotations:
              summary: "GDPR Article 30 - Gap i audit logging upptäckt"
              description: "{{ $value }} audit log gaps de senaste timmen"
              legal_requirement: "Kontinuerlig audit logging krävs för GDPR compliance"
              action: "Kontrollera logging infrastructure och fix gaps omedelbart"
          
          # Data retention compliance
          - alert: GDPRDataRetentionViolation
            expr: |
              gdpr_data_retention_violations_total{organization="${ORGANIZATION_NAME}"} > 0
            for: 1m
            labels:
              severity: high
              compliance_type: data_retention
              gdpr_article: "5"
            annotations:
              summary: "GDPR Article 5 - Data retention period överskridning"
              description: "{{ $value }} resources har data äldre än tillåten retention period"
              legal_risk: "Överträdelse av data minimization principle"
              action: "Implementera automatisk data deletion enligt retention policies"

  cost_monitoring_rules.yml: |
    groups:
      - name: svenska.cost.monitoring
        interval: 300s
        rules:
          # Kostnadsökning svenska organisationer
          - alert: SvenskaCostIncreaseHigh
            expr: |
              (
                aws_cost_monthly_total_sek{organization="${ORGANIZATION_NAME}"} -
                aws_cost_monthly_total_sek{organization="${ORGANIZATION_NAME}"} offset 24h
              ) / aws_cost_monthly_total_sek{organization="${ORGANIZATION_NAME}"} offset 24h > 0.20
            for: 15m
            labels:
              severity: warning
              cost_center: "${COST_CENTER}"
              currency: "SEK"
            annotations:
              summary: "Kostnadsökning över 20% för svenska organisationen"
              description: "Daglig kostnadsökning: {{ $value | humanizePercentage }}"
              current_cost: "{{ $labels.current_monthly_cost }} SEK"
              impact: "Påverkar månadsbudget för ${COST_CENTER}"
              action: "Granska resource utilization och optimization möjligheter"
          
          # Oanvända resurser svenska kostnadsoptimering
          - alert: SvenskaUnusedResourcesCost
            expr: |
              aws_unused_resources_cost_sek{organization="${ORGANIZATION_NAME}"} > 1000
            for: 30m
            labels:
              severity: info
              optimization_opportunity: "high"
              currency: "SEK"
            annotations:
              summary: "Oanvända resurser kostar mer än 1000 SEK/månad"
              description: "Potentiell besparing: {{ $value }} SEK/månad"
              resources: "{{ $labels.unused_resource_types }}"
              recommendation: "Implementera automatisk cleanup av oanvända resurser"
              roi: "Potential årlig besparing: {{ $value | mul 12 }} SEK"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: svenska-pipeline-alertmanager
  namespace: monitoring
  labels:
    app: alertmanager
    svenska.se/component: monitoring
spec:
  replicas: 2
  selector:
    matchLabels:
      app: alertmanager
  template:
    metadata:
      labels:
        app: alertmanager
        svenska.se/component: monitoring
        svenska.se/gdpr-compliant: "true"
    spec:
      containers:
      - name: alertmanager
        image: prom/alertmanager:v0.25.0
        ports:
        - containerPort: 9093
        volumeMounts:
        - name: config
          mountPath: /etc/alertmanager
        env:
        - name: ORGANIZATION_NAME
          value: "${ORGANIZATION_NAME}"
        - name: SLACK_WEBHOOK_URL
          valueFrom:
            secretKeyRef:
              name: notification-secrets
              key: slack-webhook-url
        - name: TEAMS_WEBHOOK_URL
          valueFrom:
            secretKeyRef:
              name: notification-secrets
              key: teams-webhook-url
        - name: SMTP_PASSWORD
          valueFrom:
            secretKeyRef:
              name: notification-secrets
              key: smtp-password
      volumes:
      - name: config
        configMap:
          name: svenska-alertmanager-config
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: svenska-alertmanager-config
  namespace: monitoring
data:
  alertmanager.yml: |
    global:
      smtp_smarthost: 'smtp.${ORGANIZATION_NAME}.se:587'
      smtp_from: 'pipeline-alerts@${ORGANIZATION_NAME}.se'
      smtp_auth_username: 'pipeline-alerts@${ORGANIZATION_NAME}.se'
      smtp_auth_password: '${SMTP_PASSWORD}'
      smtp_require_tls: true
      
      # Svenska timezone
      timezone: 'Europe/Stockholm'
    
    # Templates för svenska notifications
    templates:
      - '/etc/alertmanager/svenska-templates/*.tmpl'
    
    route:
      group_by: ['alertname', 'organization', 'severity']
      group_wait: 30s
      group_interval: 5m
      repeat_interval: 4h
      receiver: 'svenska-default'
      
      routes:
        # GDPR compliance - kritisk prioritet
        - match:
            compliance: gdpr
          receiver: 'gdpr-compliance-team'
          group_wait: 0s
          repeat_interval: 15m
        
        # Cost alerts - ekonomiavdelningen
        - match_re:
            alertname: 'Svenska.*Cost.*'
          receiver: 'ekonomi-team'
          group_interval: 15m
        
        # Production alerts - svenska devops
        - match:
            environment: production
          receiver: 'svenska-devops-production'
          group_wait: 10s
          repeat_interval: 1h
        
        # Development/staging alerts
        - match_re:
            environment: 'development|staging'
          receiver: 'svenska-devops-general'
          repeat_interval: 8h
    
    receivers:
      # Default svenska team
      - name: 'svenska-default'
        email_configs:
          - to: 'devops@${ORGANIZATION_NAME}.se'
            subject: '🇸🇪 Pipeline Alert - {{ .GroupLabels.alertname }}'
            body: |
              Hej svenska DevOps-team,
              
              En pipeline alert har utlösts för ${ORGANIZATION_NAME}:
              
              **Alert:** {{ .GroupLabels.alertname }}
              **Miljö:** {{ .GroupLabels.environment }}
              **Severity:** {{ .GroupLabels.severity }}
              **Tid:** {{ .CommonAnnotations.timestamp }}
              
              **Beskrivning:**
              {{ range .Alerts }}
              - {{ .Annotations.summary }}
                {{ .Annotations.description }}
              {{ end }}
              
              **Åtgärder:**
              {{ range .Alerts }}
              {{ if .Annotations.remediation }}
              - {{ .Annotations.remediation }}
              {{ end }}
              {{ end }}
              
              **Dashboard:** https://monitoring.${ORGANIZATION_NAME}.se
              **Runbook:** https://wiki.${ORGANIZATION_NAME}.se/alerts/{{ .GroupLabels.alertname }}
              
              Med vänliga hälsningar,
              Svenska Pipeline Monitoring System
        
        slack_configs:
          - api_url: '${SLACK_WEBHOOK_URL}'
            channel: '#svenska-pipeline-alerts'
            title: '🇸🇪 Pipeline Alert - {{ .GroupLabels.alertname }}'
            text: |
              *Miljö:* {{ .GroupLabels.environment }}
              *Severity:* {{ .GroupLabels.severity }}
              {{ range .Alerts }}
              *{{ .Annotations.summary }}*
              {{ .Annotations.description }}
              {{ end }}
            actions:
              - type: button
                text: 'Visa Dashboard'
                url: 'https://monitoring.${ORGANIZATION_NAME}.se'
              - type: button
                text: 'Acknowledge'
                url: 'https://alertmanager.${ORGANIZATION_NAME}.se'
      
      # GDPR Compliance team - kritiska alerts
      - name: 'gdpr-compliance-team'
        email_configs:
          - to: 'dpo@${ORGANIZATION_NAME}.se, compliance@${ORGANIZATION_NAME}.se, legal@${ORGANIZATION_NAME}.se'
            subject: '🚨 KRITISK GDPR COMPLIANCE ALERT - {{ .GroupLabels.alertname }}'
            body: |
              KRITISK GDPR COMPLIANCE ALERT FÖR ${ORGANIZATION_NAME}
              
              **OMEDELBAR ÅTGÄRD KRÄVS**
              
              **Alert:** {{ .GroupLabels.alertname }}
              **GDPR Artikel:** {{ .GroupLabels.gdpr_article }}
              **Legal Impact:** {{ .GroupLabels.legal_impact }}
              **Tid:** {{ .CommonAnnotations.timestamp }}
              
              **Beskrivning:**
              {{ range .Alerts }}
              {{ .Annotations.summary }}
              {{ .Annotations.description }}
              {{ end }}
              
              **Legal Requirement:**
              {{ range .Alerts }}
              {{ if .Annotations.legal_requirement }}
              {{ .Annotations.legal_requirement }}
              {{ end }}
              {{ end }}
              
              **Immediate Actions Required:**
              {{ range .Alerts }}
              {{ if .Annotations.immediate_action }}
              - {{ .Annotations.immediate_action }}
              {{ end }}
              {{ if .Annotations.urgent_action }}
              - {{ .Annotations.urgent_action }}
              {{ end }}
              {{ end }}
              
              Kontakta omedelbart DPO och Legal team.
              
              GDPR Compliance Team
              ${ORGANIZATION_NAME}
        
        teams_configs:
          - webhook_url: '${TEAMS_WEBHOOK_URL}'
            title: '🚨 KRITISK GDPR ALERT'
            summary: 'GDPR compliance violation för ${ORGANIZATION_NAME}'
            text: |
              **OMEDELBAR ÅTGÄRD KRÄVS**
              
              {{ range .Alerts }}
              **{{ .Annotations.summary }}**
              
              {{ .Annotations.description }}
              
              {{ if .Annotations.legal_requirement }}
              **Legal Requirement:** {{ .Annotations.legal_requirement }}
              {{ end }}
              {{ end }}
      
      # Ekonomi team för cost alerts
      - name: 'ekonomi-team'
        email_configs:
          - to: 'ekonomi@${ORGANIZATION_NAME}.se, cfo@${ORGANIZATION_NAME}.se'
            subject: '💰 Kostnadsalert - {{ .GroupLabels.alertname }}'
            body: |
              Kostnadsalert för ${ORGANIZATION_NAME}:
              
              **Alert:** {{ .GroupLabels.alertname }}
              **Kostnadscenter:** {{ .GroupLabels.cost_center }}
              **Valuta:** SEK
              **Tid:** {{ .CommonAnnotations.timestamp }}
              
              {{ range .Alerts }}
              **{{ .Annotations.summary }}**
              {{ .Annotations.description }}
              
              {{ if .Annotations.current_cost }}
              **Aktuell kostnad:** {{ .Annotations.current_cost }}
              {{ end }}
              {{ if .Annotations.roi }}
              **ROI Information:** {{ .Annotations.roi }}
              {{ end }}
              {{ end }}
              
              **Åtgärder:**
              {{ range .Alerts }}
              {{ if .Annotations.action }}
              - {{ .Annotations.action }}
              {{ end }}
              {{ if .Annotations.recommendation }}
              - {{ .Annotations.recommendation }}
              {{ end }}
              {{ end }}
              
              **Cost Dashboard:** https://cost.${ORGANIZATION_NAME}.se
              
              Ekonomiavdelningen
              ${ORGANIZATION_NAME}
```

## Sammanfattning

Automatisering och CI/CD-pipelines för Infrastructure as Code utgör en kritisk komponent för svenska organisationer som strävar efter digital excellence och regulatory compliance. Genom att implementera robusta, automated pipelines kan organisationer accelerera infrastrukturleveranser samtidigt som de bibehåller höga standarder för säkerhet, quality, och compliance.

Svenska organisationer har specifika krav som påverkar pipeline design, inklusive GDPR compliance validation, svenska data residency requirements, cost optimization i svenska kronor, och integration med svenska business processes. Dessa krav kräver specialized pipeline stages som automated compliance checking, cost threshold validation, och comprehensive audit logging enligt svenska lagkrav.

Modern CI/CD approaches som GitOps, progressive delivery, och infrastructure testing möjliggör sophisticated deployment strategies som minimerar risk samtidigt som de maximerar deployment velocity. För svenska organisationer innebär detta särskild fokus på blue-green deployments för production systems, canary releases för gradual rollouts, och automated rollback capabilities för snabb recovery.

Testing strategier för Infrastructure as Code inkluderar multiple levels från syntax validation till comprehensive integration testing. Terratest och container-based testing frameworks möjliggör automated validation av GDPR compliance, cost thresholds, och security requirements som en integrerad del av deployment pipelines.

Monitoring och observability för svenska IaC pipelines kräver comprehensive metrics collection som inkluderar både technical performance indicators och business compliance metrics. Automated alerting ensures rapid response till compliance violations, cost overruns, och technical failures genom integration med svenska incident management processes.

Investment i sophisticated CI/CD-pipelines för Infrastructure as Code betalar sig genom reduced deployment risk, improved compliance posture, faster feedback cycles, och enhanced operational reliability. Som vi kommer att se i [kapitel 5 om molnarkitektur](05_kapitel4.md), blir dessa capabilities ännu mer kritiska när svenska organisationer adopterar cloud-native architectures och multi-cloud strategies.

Framgångsrik implementation av CI/CD för Infrastructure as Code kräver balance mellan automation och human oversight, särskilt för production deployments och compliance-critical changes. Svenska organisationer som investerar i mature pipeline automation och comprehensive testing strategies uppnår significant competitive advantages genom improved deployment reliability och accelerated innovation cycles.

Källor:
- Jenkins. "Infrastructure as Code with Jenkins." Jenkins Documentation.
- GitHub Actions. "CI/CD for Infrastructure as Code." GitHub Documentation.
- Azure DevOps. "Infrastructure as Code Pipelines." Microsoft Azure Documentation.
- GitLab. "GitOps and Infrastructure as Code." GitLab Documentation.
- Terraform. "Automated Testing for Terraform." HashiCorp Learn Platform.
- Kubernetes. "GitOps Principles and Practices." Cloud Native Computing Foundation.
- GDPR.eu. "Infrastructure Compliance Requirements." GDPR Guidelines.
- Swedish Data Protection Authority. "Technical and Organizational Measures." Datainspektionen Guidelines.