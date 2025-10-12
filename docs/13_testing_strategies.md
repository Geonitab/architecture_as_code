# Teststrategier for infrastruktukod

![Test pyramid for architecture as code](images/diagram_17_kapitel16.png)

*comprehensive teststrategi for Architecture as Code (Architecture as Code) requires multiple testing-levels from unit tests to end-to-end validation. The diagram illustrates the Structureerade forloppet from snabba utvecklartester to comprehensive integrationsvalidering.*

## Overall Description

testing of Architecture as Code differs Fundamental from traditional programvarutestning by focus at arkitekturkonfiguration, resurskompatibilitet and miljökonsekvens instead for affärslogik. Effective testing of Architecture as Code ensures Architecture as Code produces forväntade resultat konsekvent over different environments.

Modern Architecture as Code-testing encompasses multiple dimensioner: syntaktisk validation of code, policy compliance checking, kostnadsprognoser, säkerhetssårbarhetanalys and functional testing of deployed infrastructure. This multilevel approach identifierar problem early in utvecklingscykeln when the is billigare and enklare to fixa.

organizations with strict compliance-requirements must implement comprehensive testing as validates both technical funktionalitet and regulatory conformance. This includes GDPR data protection controls, financial services regulations and government security standards as must verifieras automatically.

Test automation for Architecture as Code enables continuous integration and continuous deployment patterns as accelererar delivery while the reduces risk for produktionsstörningar. Infrastructure testing pipelines can run parallellt with application testing to ensure end-to-end quality assurance.

## Unit testing for architecture as code

Unit testing for Architecture as Code focuses on validation of individual moduler and resources without to faktiskt deploya infrastructure. This enables snabb feedback and early detection of konfigurationsfel, which is kritiskt for developer productivity and code quality.

Terraform testing tools that Terratest, terraform-compliance and checkov enables automated validation of HCL-code mot predefined policies and Architecture as Code best practices. These tools can integreras in IDE:er for real-time feedback under development samt in CI/CD pipelines for automated quality gates.

Unit tests for Architecture as Code should validate resource configurations, variable validations, output consistency and module interface contracts. This is particularly viktigt for reusable modules as is used across multiple projects where changes can ha wide-ranging impact at dependent resources.

Mock testing strategies for cloud resources enables testing without faktiska cloud costs, which is essentiellt for frequent testing cycles. Verktyg that LocalStack and cloud provider simulators can simulate cloud services locally for comprehensive testing without infrastructure provisioning costs.

## Testhantering with Vitest for architecture as code

Vitest is A modernt testramverk byggt for Vite-ekosystemet as offers snabb and effective testing of JavaScript/TypeScript-code. For Architecture as Code-projekt as uses Architecture as Code with modern tools is Vitest particularly relevant to testa konfigurationsgeneratorer, validation scripts and automation tools as often skrivs in TypeScript or JavaScript.

### Varfor Vitest is relevant for architecture as code

Many modern Architecture as Code workflows includes TypeScript/JavaScript-components to generera, validate or transformera infrastructure configurations. Vitest enables snabb unit testing of These components with forstklassig TypeScript-support, which is kritiskt to ensure korrekt konfigurationsgenerering before deployment.

Vitest's snabba execution and watch mode enables tight development feedback loops when man develops infrastructure configuration generators or policy validation scripts. This is particularly valuable for Architecture as Code-projekt where konfigurationsfel can leda to costly infrastructure mistakes.

Integration with Vite build tooling means to same utvecklingsmiljö can be used for both application code and infrastructure-relaterad code, which reduces context switching and improves developer experience for team as arbetar with both application and infrastructure code.

### Konfiguration of Vitest for Architecture as Code-projekt

to integrera Vitest in A Architecture as Code-projekt needs vi forst installera necessary dependencies and konfigurera test environment:

```bash
# Installera Vitest and relaterade dependencies
npm install -D vitest @vitest/ui
npm install -D @types/node  # For Node.js APIs

# For coverage rapportering
npm install -D @vitest/coverage-v8
```

Skapa a `vitest.config.ts` File in projekt root:

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import path from 'path';

export default defineConfig({
  test: {
    // Use globals to undvika imports in each testfil
    globals: true,
    
    // Test environment (node for infrastructure tooling)
    environment: 'node',
    
    // Coverage configuration
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'dist/',
        '**/*.config.ts',
        '**/types/**',
      ],
      // Kräv minst 80% coverage for infrastructure code
      lines: 80,
      functions: 80,
      branches: 80,
      statements: 80,
    },
    
    // Test timeout for infrastructure operations
    testTimeout: 30000,
    
    // Inkludera test filer
    include: ['**/*.{test,spec}.{js,mjs,cjs,ts,mts,cts}'],
    
    // Exclude patterns
    exclude: [
      'node_modules',
      'dist',
      '.terraform',
      '**/*.d.ts',
    ],
  },
  
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@infra': path.resolve(__dirname, './infrastructure'),
    },
  },
});
```

### Praktiska example for Infrastructure as Code testing

#### examples 1: Testa Terraform Configuration Generator

```typescript
// src/generators/terraform-config.ts
export interface TerraformConfig {
  provider: string;
  region: string;
  environment: string;
  resources: ResourceConfig[];
}

export interface ResourceConfig {
  type: string;
  name: string;
  properties: Record<string, any>;
}

export class TerraformConfigGenerator {
  generateVPCConfig(
    environment: string,
    region: string = 'eu-north-1'
  ): TerraformConfig {
    // Validate regioner for GDPR compliance
    const swedishRegions = ['eu-north-1', 'eu-west-1'];
    if (!swedishRegions.includes(region)) {
      throw new Error('Region must vara within EU for GDPR compliance');
    }

    return {
      provider: 'aws',
      region,
      environment,
      resources: [
        {
          type: 'aws_vpc',
          name: `vpc-${environment}`,
          properties: {
            cidr_block: '10.0.0.0/16',
            enable_dns_hostnames: true,
            enable_dns_support: true,
            tags: {
              Name: `vpc-${environment}`,
              Environment: environment,
              ManagedBy: 'Terraform',
              GdprCompliant: 'true',
              DataResidency: 'Sweden',
            },
          },
        },
      ],
    };
  }

  generateRDSConfig(
    environment: string,
    instanceClass: string = 'db.t3.micro',
    encrypted: boolean = true
  ): ResourceConfig {
    // Säkerställ encryption for production
    if (environment === 'production' && !encrypted) {
      throw new Error('Production databaser must ha encryption aktiverad');
    }

    return {
      type: 'aws_db_instance',
      name: `rds-${environment}`,
      properties: {
        allocated_storage: environment === 'production' ? 100 : 20,
        engine: 'postgres',
        engine_version: '14.7',
        instance_class: instanceClass,
        storage_encrypted: encrypted,
        backup_retention_period: environment === 'production' ? 30 : 7,
        multi_az: environment === 'production',
        tags: {
          Environment: environment,
          GdprCompliant: 'true',
          EncryptionEnabled: encrypted.toString(),
        },
      },
    };
  }
}
```

```typescript
// src/generators/terraform-config.test.ts
import { describe, it, expect } from 'vitest';
import { TerraformConfigGenerator } from './terraform-config';

describe('TerraformConfigGenerator', () => {
  const generator = new TerraformConfigGenerator();

  describe('generateVPCConfig', () => {
    it('should generera VPC config for regioner', () => {
      const config = generator.generateVPCConfig('production', 'eu-north-1');
      
      expect(config.provider).toBe('aws');
      expect(config.region).toBe('eu-north-1');
      expect(config.environment).toBe('production');
      expect(config.resources).toHaveLength(1);
    });

    it('should include GDPR compliance tags', () => {
      const config = generator.generateVPCConfig('production');
      const vpc = config.resources[0];
      
      expect(vpc.properties.tags).toMatchObject({
        GdprCompliant: 'true',
        DataResidency: 'Sweden',
      });
    });

    it('should kasta fel for non-EU regions', () => {
      expect(() => {
        generator.generateVPCConfig('production', 'us-east-1');
      }).toThrow('Region must vara within EU for GDPR compliance');
    });

    it('should aktivera DNS support and hostnames', () => {
      const config = generator.generateVPCConfig('development');
      const vpc = config.resources[0];
      
      expect(vpc.properties.enable_dns_hostnames).toBe(true);
      expect(vpc.properties.enable_dns_support).toBe(true);
    });
  });

  describe('generateRDSConfig', () => {
    it('should kräva encryption for production environments', () => {
      expect(() => {
        generator.generateRDSConfig('production', 'db.t3.micro', false);
      }).toThrow('Production databaser must ha encryption aktiverad');
    });

    it('should generera korrekt RDS config for production', () => {
      const config = generator.generateRDSConfig('production');
      
      expect(config.type).toBe('aws_db_instance');
      expect(config.properties.storage_encrypted).toBe(true);
      expect(config.properties.multi_az).toBe(true);
      expect(config.properties.backup_retention_period).toBe(30);
      expect(config.properties.allocated_storage).toBe(100);
    });

    it('should use lägre resurser for development environment', () => {
      const config = generator.generateRDSConfig('development');
      
      expect(config.properties.allocated_storage).toBe(20);
      expect(config.properties.backup_retention_period).toBe(7);
      expect(config.properties.multi_az).toBeUndefined();
    });

    it('should include GDPR compliance tags', () => {
      const config = generator.generateRDSConfig('production');
      
      expect(config.properties.tags).toMatchObject({
        GdprCompliant: 'true',
        EncryptionEnabled: 'true',
      });
    });
  });
});
```

#### examples 2: Testa Infrastructure Validation Scripts

```typescript
// src/validators/infrastructure-validator.ts
export interface ValidationResult {
  valid: boolean;
  errors: string[];
  warnings: string[];
}

export class InfrastructureValidator {
  validateResourceTags(
    tags: Record<string, string>,
    requiredTags: string[] = ['Environment', 'ManagedBy']
  ): ValidationResult {
    const errors: string[] = [];
    const warnings: string[] = [];

    // Kontrollera required tags
    for (const tag of requiredTags) {
      if (!tags[tag]) {
        errors.push(`Saknar required tag: ${tag}`);
      }
    }

    // Validate GDPR compliance for organizations
    if (tags['DataClassification']) {
      const validClassifications = ['public', 'internal', 'confidential', 'personal'];
      if (!validClassifications.includes(tags['DataClassification'])) {
        errors.push(
          `Ogiltig DataClassification: ${tags['DataClassification']}`
        );
      }
    }

    // Warn about GdprCompliant tag saknas for känslig data
    if (tags['DataClassification'] === 'personal' && !tags['GdprCompliant']) {
      warnings.push('GdprCompliant tag rekommentheir for personal data');
    }

    return {
      valid: errors.length === 0,
      errors,
      warnings,
    };
  }

  validateSecurityGroup(
    rules: Array<{ port: number; cidr: string }>
  ): ValidationResult {
    const errors: string[] = [];
    const warnings: string[] = [];

    for (const rule of rules) {
      // Kontrollera öppna portar
      if (rule.cidr === '0.0.0.0/0') {
        if ([22, 3389, 3306, 5432].includes(rule.port)) {
          errors.push(
            `Port ${rule.port} should not vara öppen mot internet (0.0.0.0/0)`
          );
        }
      }

      // Varning for vanliga portar
      if (rule.cidr === '0.0.0.0/0' && [80, 443].includes(rule.port)) {
        warnings.push(
          `Port ${rule.port} is öppen mot internet - verifiera to this is avsiktligt`
        );
      }
    }

    return {
      valid: errors.length === 0,
      errors,
      warnings,
    };
  }
}
```

```typescript
// src/validators/infrastructure-validator.test.ts
import { describe, it, expect } from 'vitest';
import { InfrastructureValidator } from './infrastructure-validator';

describe('InfrastructureValidator', () => {
  const validator = new InfrastructureValidator();

  describe('validateResourceTags', () => {
    it('should validate to required tags exists', () => {
      const tags = {
        Environment: 'production',
        ManagedBy: 'Terraform',
      };

      const result = validator.validateResourceTags(tags);
      
      expect(result.valid).toBe(true);
      expect(result.errors).toHaveLength(0);
    });

    it('should rapportera fel when required tags saknas', () => {
      const tags = {
        Environment: 'production',
      };

      const result = validator.validateResourceTags(tags);
      
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Saknar required tag: ManagedBy');
    });

    it('should validate DataClassification värden', () => {
      const tags = {
        Environment: 'production',
        ManagedBy: 'Terraform',
        DataClassification: 'invalid-value',
      };

      const result = validator.validateResourceTags(tags);
      
      expect(result.valid).toBe(false);
      expect(result.errors[0]).toContain('Ogiltig DataClassification');
    });

    it('should varna about GdprCompliant tag saknas for personal data', () => {
      const tags = {
        Environment: 'production',
        ManagedBy: 'Terraform',
        DataClassification: 'personal',
      };

      const result = validator.validateResourceTags(tags);
      
      expect(result.warnings).toContain(
        'GdprCompliant tag rekommentheir for personal data'
      );
    });

    it('should acceptera giltiga DataClassification värden', () => {
      const validClassifications = ['public', 'internal', 'confidential', 'personal'];
      
      for (const classification of validClassifications) {
        const tags = {
          Environment: 'production',
          ManagedBy: 'Terraform',
          DataClassification: classification,
        };

        const result = validator.validateResourceTags(tags);
        expect(result.valid).toBe(true);
      }
    });
  });

  describe('validateSecurityGroup', () => {
    it('should blockera SSH öppet mot internet', () => {
      const rules = [{ port: 22, cidr: '0.0.0.0/0' }];
      
      const result = validator.validateSecurityGroup(rules);
      
      expect(result.valid).toBe(false);
      expect(result.errors[0]).toContain('Port 22 should not vara öppen');
    });

    it('should blockera databas portar öppna mot internet', () => {
      const rules = [
        { port: 3306, cidr: '0.0.0.0/0' },  // MySQL
        { port: 5432, cidr: '0.0.0.0/0' },  // PostgreSQL
      ];
      
      const result = validator.validateSecurityGroup(rules);
      
      expect(result.valid).toBe(false);
      expect(result.errors).toHaveLength(2);
    });

    it('should varna for HTTP/HTTPS öppet mot internet', () => {
      const rules = [
        { port: 80, cidr: '0.0.0.0/0' },
        { port: 443, cidr: '0.0.0.0/0' },
      ];
      
      const result = validator.validateSecurityGroup(rules);
      
      expect(result.valid).toBe(true);
      expect(result.warnings).toHaveLength(2);
    });

    it('should acceptera restricted CIDR blocks', () => {
      const rules = [
        { port: 22, cidr: '10.0.0.0/8' },
        { port: 3306, cidr: '192.168.1.0/24' },
      ];
      
      const result = validator.validateSecurityGroup(rules);
      
      expect(result.valid).toBe(true);
      expect(result.errors).toHaveLength(0);
    });
  });
});
```

### Integration in CI/CD Pipeline

Vitest can integreras in CI/CD pipelines for automated testing of infrastructure code:

```yaml
# .github/workflows/infrastructure-validation.yml
name: Infrastructure Code Validation

on:
  pull_request:
    paths:
      - 'src/**'
      - 'infrastructure/**'
      - 'tests/**'
  push:
    branches: [main, develop]

jobs:
  vitest-validation:
    runs-on: ubuntu-latest
    name: Vitest Infrastructure Tests
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - name: Install Dependencies
        run: npm ci
      
      - name: Run Vitest Tests
        run: npm run test:vitest
        
      - name: Generate Coverage Report
        run: npm run test:coverage
        
      - name: Upload Coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage/coverage-final.json
          flags: infrastructure-code
          
      - name: Comment PR with Coverage
        if: github.event_name == 'pull_request'
        uses: romeovs/lcov-reporter-action@v0.3.1
        with:
          lcov-file: ./coverage/lcov.info
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

Lägg to test scripts in `package.json`:

```json
{
  "scripts": {
    "test:vitest": "vitest run",
    "test:watch": "vitest watch",
    "test:coverage": "vitest run --coverage",
    "test:ui": "vitest --ui"
  }
}
```

### Recommendations for testorganisering

**FilStructure for Infrastructure Code Tests:**

```
project/
├── src/
│   ├── generators/
│   │   ├── terraform-config.ts
│   │   └── terraform-config.test.ts
│   ├── validators/
│   │   ├── infrastructure-validator.ts
│   │   └── infrastructure-validator.test.ts
│   └── utils/
│       ├── compliance-checker.ts
│       └── compliance-checker.test.ts
├── tests/
│   ├── integration/
│   │   └── end-to-end.test.ts
│   └── fixtures/
│       └── sample-configs.ts
├── vitest.config.ts
└── package.json
```

**Best Practices for Infrastructure Testing with Vitest:**

1. **Snabba unit tests:** Håll unit tests snabba (<100ms per test) to enable effective watch mode under development.

2. **Isolerade tester:** each test should be oberoende and be able to köras in valfri ordning without side effects.

3. **Beskrivande test namn:** Use clear test descriptions as documents expected behavior: `'should kasta fel for non-EU regions'`.

4. **Test fixtures:** Use shared test fixtures for common infrastructure configurations, but var forsiktig with mutable state.

5. **Coverage goals:** Sikta at minst 80% code coverage for infrastructure configuration and validation code, but focus at meaningful tests rather than coverage metrics.

6. **Mock externa beroenden:** Use Vitest's mocking capabilities to mocka cloud provider SDKs and external APIs:

```typescript
import { vi } from 'vitest';
import * as AWS from 'aws-sdk';

vi.mock('aws-sdk', () => ({
  EC2: vi.fn(() => ({
    describeInstances: vi.fn().mockResolvedValue({
      Reservations: [],
    }),
  })),
}));
```

7. **Snapshot testing:** Use snapshot tests to validate generated configuration files:

```typescript
it('should generera korrekt terraform config', () => {
  const config = generator.generateFullConfig('production');
  expect(config).toMatchSnapshot();
});
```

### Automation and Watch Mode

a of Vitest's biggest Benefits is watch mode as enables continuous testing under development:

```bash
# Starta watch mode for automated re-testing
npm run test:watch

# Kör endast relaterade tester when filer changes
npm run test:watch -- --changed

# Kör tests with UI for interaktiv debugging
npm run test:ui
```

This enables tight feedback loops where infrastructure code changes owithelbart valitheir, which reduces tiden between code change and feedback from seconds to milliseconds.

For organizations with strict compliance requirements can automated testing with Vitest ensure to infrastructure configurations konsekvent meets GDPR requirements, security policies and organizational standards before deployment.

## Integrationstesting and miljövalidering

Integration testing for Architecture as Code verifierar to different infrastructure components functions tosammans korrekt and to deployed infrastructure meets performance and security requirements. This requires temporary test environments as closely mirror production configurations.

End-to-end testing workflows must validate entire deployment pipelines from source code changes to functional infrastructure. This includes testing of CI/CD pipeline configurations, secret management, monitoring setup and rollback procedures as is critical for production stability.

Environment parity testing ensures infrastructure behaves consistently across development, staging and production environments. This testing identifierar environment-specific issues as can cause deployment failures or performance discrepancies between environments.

Chaos engineering principles can appliceras at infrastructure testing by systematiskt introduce failures in test environments to validate resilience and recovery mechanisms. This is particularly valuable for mission-critical systems as requires high availability guarantees.

## Security and compliance testing

Security testing for Architecture as Code must validate both infrastructure configuration security and operational security controls. This includes scanning for common security misconfigurations, chosention of encryption settings and verification of network security policies.

Compliance testing automation ensures infrastructure configurations meets regulatory requirements kontinuerligt. organizations must validate GDPR compliance, financial regulations and government security standards through automated testing as can provide audit trails for compliance reporting.

Policy-as-code frameworks that Open Policy Agent (OPA) and AWS Config Rules enables declarative definition of compliance policies as can enforced automatically under infrastructure deployment. This preventative approach is mer effective than reactive compliance monitoring.

Vulnerability scanning for infrastructure dependencies must include container images, operating systems configurations and third-party software components. Integration with security scanning tools in CI/CD pipelines ensures security vulnerabilities identifieras before deployment to production.

## Performance and skalbarhetstesting

Performance testing for Architecture as Code focuses on validation of infrastructure capacity, response times and resource utilization under various load conditions. This is critical for applications as requires predictable performance characteristics under varying traffic patterns.

Load testing strategies must validate auto-scaling configurations, resource limits and failover mechanisms under realistic traffic scenarios. Infrastructure performance testing can include database performance under load, network throughput validation and storage in/O capacity verification.

Skalabilitetstesting verifierar to infrastructure can handle projected growth efficiently through automated scaling mechanisms. This includes testing of horizontal scaling for stateless services and validation of data partitioning strategies for stateful systems.

Capacity planning validation through performance testing helps optimize resource configurations for cost-effectiveness while performance requirements uppfylls. This is particularly important for organizations as balanserar cost optimization with service level requirements.

## Requirements as Code and testbarhet

![Requirements and testing relation](images/diagram_12_requirements_testing.png)

*The relationship between business requirements, functional requirements and verification methods illustrerar how Architecture as Code enables traceable testing from higher abstraction levels down to concrete Architecture as Code-implementations.*

Requirements-as-Code represents A paradigm shift where business requirements and compliance-requirements are codified in machine-readable form together with infrastructure-the code. This enables automated validation of to infrastructureen verkligen meets the specificerade requirementsen through entire utvecklingslivscykeln.

by definiera Requirements as Code are created a direkt koppling between business requirements, functional requirements and the automated tester as verifierar Architecture as Code-implementationen. This traceability is critical for organisationer as must demonstrate compliance and for utvecklingsteam as needs understand affärsconsequences of technical decisions.

### Kravtraceability in praktiken

Requirements traceability for Architecture as Code means to each infrastructurekomponent can kopplas tobaka to specific business requirements or compliance-requirements. This is particularly viktigt for organizations as must meet GDPR, finansiella regulations or myndighetsrequirements.

Verktyg that Open Policy Agent (OPA) enables uttryck of compliance-requirements as policies as can evalueras automatically mot infrastructure-configurations. These policies becomes testable requirements as can köras kontinuerligt to ensure ongoing compliance.

Requirement validation testing ensures infrastructure not only is technical korrekt without also meets business intent. This includes validation of security requirements, performance-requirements, togänglighetsrequirements and kostnadsramar as defined of business stakeholders.

### Automated Requirements Verification

```yaml
# requirements/security-requirements.yaml
apiVersion: policy/v1
kind: RequirementSet
metadata:
  name: swedish-security-requirements
  version: "1.0"
spec:
  requirements:
    - id: SEC-001
      type: security
      description: "all S3 buckets must ha encryption aktiverad"
      priority: critical
      compliance: ["GDPR", "ISO27001"]
      tests:
        - type: static-analysis
          tool: checkov
          rule: CKV_AWS_141
        - type: runtime-test
          script: test_s3_encryption.py
    
    - id: SEC-002  
      type: security
      description: "RDS instanser must use encrypted storage"
      priority: critical
      compliance: ["GDPR"]
      tests:
        - type: terraform-test
          file: test_rds_encryption_test.go
        - type: policy-test
          file: rds_encryption.rego
          
    - id: PERF-001
      type: performance
      description: "Auto-scaling must vara konfigurerat for production workloads"
      priority: high
      tests:
        - type: integration-test
          file: test_autoscaling_integration.py
        - type: load-test
          tool: k6
          script: autoscaling_load_test.js
```

```python
# test/requirements_validation.py
"""
Automatiserad validation of requirements mot Infrastructure as Code
"""
import yaml
import subprocess
import json
from typing import Dict, List, Any

class RequirementValidator:
    def __init__(self, requirements_file: str):
        with open(requirements_file, 'r') as f:
            self.requirements = yaml.safe_load(f)
    
    def validate_all_requirements(self) -> Dict[str, Any]:
        """Kör all requirements-relaterade tester and sammanställ resultat"""
        results = {
            'passed': [],
            'failed': [],
            'skipped': [],
            'summary': {}
        }
        
        for req in self.requirements['spec']['requirements']:
            req_id = req['id']
            print(f"Validates requirements {req_id}: {req['description']}")
            
            req_result = self._validate_requirement(req)
            
            if req_result['status'] == 'passed':
                results['passed'].append(req_result)
            elif req_result['status'] == 'failed':
                results['failed'].append(req_result)
            else:
                results['skipped'].append(req_result)
        
        results['summary'] = {
            'total': len(self.requirements['spec']['requirements']),
            'passed': len(results['passed']),
            'failed': len(results['failed']),
            'skipped': len(results['skipped']),
            'compliance_coverage': self._calculate_compliance_coverage()
        }
        
        return results
    
    def _validate_requirement(self, requirement: Dict) -> Dict[str, Any]:
        """Validate A enskilt requirements by run associerade tester"""
        req_id = requirement['id']
        test_results = []
        
        for test in requirement.get('tests', []):
            test_result = self._execute_test(test, req_id)
            test_results.append(test_result)
        
        # Avgör overall status for requirementset
        if all(t['passed'] for t in test_results):
            status = 'passed'
        elif any(t['passed'] == False for t in test_results):
            status = 'failed'
        else:
            status = 'skipped'
        
        return {
            'requirement_id': req_id,
            'description': requirement['description'],
            'priority': requirement['priority'],
            'compliance': requirement.get('compliance', []),
            'status': status,
            'test_results': test_results
        }
    
    def _execute_test(self, test_config: Dict, req_id: str) -> Dict[str, Any]:
        """Exekvera A specific test based on dess typ"""
        test_type = test_config['type']
        
        if test_type == 'static-analysis':
            return self._run_static_analysis_test(test_config, req_id)
        elif test_type == 'terraform-test':
            return self._run_terraform_test(test_config, req_id)
        elif test_type == 'policy-test':
            return self._run_policy_test(test_config, req_id)
        elif test_type == 'integration-test':
            return self._run_integration_test(test_config, req_id)
        elif test_type == 'load-test':
            return self._run_load_test(test_config, req_id)
        else:
            return {
                'test_type': test_type,
                'passed': None,
                'message': f'Okänd testtyp: {test_type}',
                'requirement_id': req_id
            }
    
    def _run_static_analysis_test(self, test_config: Dict, req_id: str) -> Dict[str, Any]:
        """Kör static analysis test with Checkov"""
        tool = test_config.get('tool', 'checkov')
        rule = test_config.get('rule')
        
        try:
            cmd = f"{tool} --check {rule} --directory terraform/ --output json"
            result = subprocess.run(cmd.split(), capture_output=True, text=True)
            
            if result.returncode == 0:
                return {
                    'test_type': 'static-analysis',
                    'tool': tool,
                    'rule': rule,
                    'passed': True,
                    'message': 'Static analysis passed',
                    'requirement_id': req_id
                }
            else:
                return {
                    'test_type': 'static-analysis', 
                    'tool': tool,
                    'rule': rule,
                    'passed': False,
                    'message': f'Static analysis failed: {result.stderr}',
                    'requirement_id': req_id
                }
        except Exception as e:
            return {
                'test_type': 'static-analysis',
                'passed': None,
                'message': f'Error running static analysis: {str(e)}',
                'requirement_id': req_id
            }
    
    def _calculate_compliance_coverage(self) -> Dict[str, float]:
        """Beräkna compliance coverage for different regulations"""
        compliance_mapping = {}
        
        for req in self.requirements['spec']['requirements']:
            for compliance in req.get('compliance', []):
                if compliance not in compliance_mapping:
                    compliance_mapping[compliance] = {'total': 0, 'tested': 0}
                
                compliance_mapping[compliance]['total'] += 1
                
                if req.get('tests'):
                    compliance_mapping[compliance]['tested'] += 1
        
        coverage = {}
        for compliance, stats in compliance_mapping.items():
            if stats['total'] > 0:
                coverage[compliance] = stats['tested'] / stats['total'] * 100
            else:
                coverage[compliance] = 0
        
        return coverage
```

## Praktiska example

### Terraform Unit Testing with Terratest
```go
// test/terraform_test.go
package test

import (
    "testing"
    "github.com/gruntwork-io/terratest/modules/terraform"
    "github.com/gruntwork-io/terratest/modules/test-structure"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
)

func TestTerraformInfrastructure(t *testing.T) {
    t.Parallel()

    // Sätt upp test environment
    terraformDir := "../terraform/swedish-infrastructure"
    
    // Generera unique suffix for test resources
    uniqueId := test-structure.UniqueId()
    
    terraformOptions := &terraform.Options{
        TerraformDir: terraformDir,
        Whose: map[string]interface{}{
            "environment":      "test",
            "project_name":     "architecture as code-test-" + uniqueId,
            "region":          "eu-north-1", // Stockholm for requirements
            "enable_gdpr_logs": true,
            "data_classification": "internal",
        },
        BackendConfig: map[string]interface{}{
            "bucket": "terraform-state-test-" + uniqueId,
            "region": "eu-north-1",
        },
    }

    // Cleanup resources efter test
    defer terraform.Destroy(t, terraformOptions)

    // Kör terraform init and plan
    terraform.InitAndPlan(t, terraformOptions)

    // Validate to plan contains förväntade resources
    planStruct := terraform.InitAndPlanAndShowWithStruct(t, terraformOptions)
    
    // Test: Validate to all resurser has korrekta tags
    for _, resource := range planStruct.PlannedValues.RootModule.Resources {
        if resource.Type == "aws_instance" || resource.Type == "aws_rds_instance" {
            tags := resource.AttributeValues["tags"].(map[string]interface{})
            
            assert.Equal(t, "architecture as code-test-" + uniqueId, tags["Project"])
            assert.Equal(t, "test", tags["Environment"])
            assert.Equal(t, "internal", tags["DataClassification"])
            
            // Validate GDPR compliance tags
            assert.Contains(t, tags, "GdprApplicable")
            assert.Contains(t, tags, "DataRetention")
        }
    }

    // Test: Validate säkerhetskonfiguration
    for _, resource := range planStruct.PlannedValues.RootModule.Resources {
        if resource.Type == "aws_s3_bucket" {
            // Validate to S3 buckets has encryption enabled
            encryption := resource.AttributeValues["server_side_encryption_configuration"]
            assert.NotNil(t, encryption, "S3 bucket must ha encryption konfigurerad")
        }
        
        if resource.Type == "aws_rds_instance" {
            // Validate to RDS instances has encryption at rest
            encrypted := resource.AttributeValues["storage_encrypted"].(bool)
            assert.True(t, encrypted, "RDS instans must ha storage encryption aktiverad")
        }
    }

    // Kör terraform apply
    terraform.Apply(t, terraformOptions)

    // Test: Validate faktiska infrastructure deployment
    validateInfrastructureDeployment(t, terraformOptions, uniqueId)
}

func validateInfrastructureDeployment(t *testing.T, terraformOptions *terraform.Options, uniqueId string) {
    // Hämta outputs from terraform
    vpcId := terraform.Output(t, terraformOptions, "vpc_id")
    require.NotEmpty(t, vpcId, "VPC ID should not vara tom")

    dbEndpoint := terraform.Output(t, terraformOptions, "database_endpoint")
    require.NotEmpty(t, dbEndpoint, "Database endpoint should not vara tom")

    // Test: Validate nätverkskonfiguration
    validateNetworkConfiguration(t, vpcId)
    
    // Test: Validate database connectivity
    validateDatabaseConnectivity(t, dbEndpoint)
    
    // Test: Validate monitoring and logging
    validateMonitoringSetup(t, terraformOptions)
}

func validateNetworkConfiguration(t *testing.T, vpcId string) {
    // implementation for nätverksvalidering
    // Kontrollera subnets, routing tables, security groups etc.
}

func validateDatabaseConnectivity(t *testing.T, endpoint string) {
    // implementation for databasconnectivity testing
    // Kontrollera to databas is accessible and responsiv
}

func validateMonitoringSetup(t *testing.T, terraformOptions *terraform.Options) {
    // implementation for monitoring validation
    // Kontrollera CloudWatch metrics, alarms, logging etc.
}
```

### Policy-as-Code Testing with OPA
```rego
# policies/aws_security_test.rego
package aws.security.test

import rego.v1

# Test: S3 Buckets must ha encryption
test_s3_encryption_required if {
    input_s3_without_encryption := {
        "resource_type": "aws_s3_bucket",
        "attributes": {
            "bucket": "test-bucket",
            "server_side_encryption_configuration": null
        }
    }
    
    not aws.security.s3_encryption_required with input as input_s3_without_encryption
}

test_s3_encryption_allowed if {
    input_s3_with_encryption := {
        "resource_type": "aws_s3_bucket", 
        "attributes": {
            "bucket": "test-bucket",
            "server_side_encryption_configuration": [{
                "rule": [{
                    "apply_server_side_encryption_by_default": [{
                        "sse_algorithm": "AES256"
                    }]
                }]
            }]
        }
    }
    
    aws.security.s3_encryption_required with input as input_s3_with_encryption
}

# Test: EC2 instances must ha säkerhetgrupper konfigurerade
test_ec2_security_groups_required if {
    input_ec2_without_sg := {
        "resource_type": "aws_instance",
        "attributes": {
            "instance_type": "t3.micro",
            "vpc_security_group_ids": []
        }
    }
    
    not aws.security.ec2_security_groups_required with input as input_ec2_without_sg
}

# Test: GDPR compliance
test_gdpr_data_classification_required if {
    input_without_classification := {
        "resource_type": "aws_rds_instance",
        "attributes": {
            "tags": {
                "Environment": "production",
                "Project": "customer-app"
            }
        }
    }
    
    not sweden.gdpr.data_classification_required with input as input_without_classification
}

test_gdpr_data_classification_valid if {
    input_with_classification := {
        "resource_type": "aws_rds_instance",
        "attributes": {
            "tags": {
                "Environment": "production", 
                "Project": "customer-app",
                "DataClassification": "personal",
                "GdprApplicable": "true",
                "DataRetention": "7years"
            }
        }
    }
    
    sweden.gdpr.data_classification_required with input as input_with_classification
}
```

## Kubernetes integrationstestning

### Kubernetes Infrastructure Testing

Architecture as Code-principerna within This area
```yaml
# test/k8s-test-suite.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: infrastructure-tests
  namespace: testing
data:
  test-runner.sh: |
    #!/bin/bash
    set -e
    
    echo "Starting Infrastructure as Code testing for Kubernetes..."
    
    # Test 1: Validate resource quotas
    echo "Testing resource quotas..."
    kubectl get resourcequota -n production -o json | \
    jq '.items[0].status.used | to_entries[] | select(.value == "0")' | \
    if [ $(wc -l) -gt 0 ]; then
      echo "WARNING: Unused resource quotas detected"
    fi
    
    # Test 2: Validate security policies
    echo "Testing Pod Security Policies..."
    kubectl get psp | grep -E "(privileged|hostNetwork)" && \
    echo "ERROR: Privileged security policies detected" && exit 1
    
    # Test 3: Validate network policies
    echo "Testing Network Policies..."
    NAMESPACES=$(kubectl get ns --no-headers -o custom-columns=":metadata.name")
    for ns in $NAMESPACES; do
      if [ "$ns" != "kube-systems" ] && [ "$ns" != "kube-public" ]; then
        if ! kubectl get networkpolicy -n $ns --no-headers 2>/dev/null | grep -q .; then
          echo "WARNING: No network policies in namespace $ns"
        fi
      fi
    done
    
    # Test 4: Validate compliance requirements
    echo "Testing GDPR compliance for persistent volumes..."
    kubectl get pv -o json | \
    jq -r '.items[] | select(.spec.csi.driver == "ebs.csi.aws.com") | 
           select(.spec.csi.volumeAttributes.encrypted != "true") | 
           .metadata.name' | \
    if [ $(wc -l) -gt 0 ]; then
      echo "ERROR: Unencrypted persistent volumes detected"
      exit 1
    fi
    
    echo "All infrastructure tests passed!"
```

```yaml
---
apiVersion: batch/v1
kind: Job
metadata:
  name: infrastructure-test-job
  namespace: testing
spec:
  template:
    spec:
      containers:
      - name: test-runner
        image: bitnami/kubectl:latest
        command: ["/bin/bash"]
        args: ["/scripts/test-runner.sh"]
        volumeMounts:
        - name: test-scripts
          mountPath: /scripts
        env:
        - name: KUBECONFIG
          value: /etc/kubeconfig/config
      volumes:
      - name: test-scripts
        configMap:
          name: infrastructure-tests
          defaultMode: 0755
      - name: kubeconfig
        secret:
          secretName: kubeconfig
      restartPolicy: Never
  backoffLimit: 3
```

## Pipeline automation for infrastrukturtestning

### CI/CD Pipeline for Infrastructure Testing

Architecture as Code-principerna within This area
```yaml
# .github/workflows/infrastructure-testing.yml
name: Infrastructure Testing Pipeline

on:
  pull_request:
    paths: 
      - 'terraform/**'
      - 'kubernetes/**'
      - 'policies/**'
  push:
    branches: [main, develop]

jobs:
  static-analysis:
    runs-on: ubuntu-latest
    name: Static Code Analysis
    steps:
      - uses: actions/checkout@v4
      
      - name: Terraform Format Check
        run: terraform fmt -check -recursive terraform/
        
      - name: Terraform Validation
        run: |
          cd terraform
          terraform init -backend=false
          terraform validate
          
      - name: Security Scanning with Checkov
        uses: bridgecrewio/checkov-action@master
        with:
          directory: terraform/
          framework: terraform
          output_format: cli,sarif
          output_file_path: reports/checkov-report.sarif
          
      - name: Policy Testing with OPA
        run: |
          # Installera OPA
          curl -L -o opa https://openpolicyagent.org/downloads/v0.57.0/opa_linux_amd64_static
          chmod +x opa
          
          # Kör policy tests
          ./opa test policies/

  unit-testing:
    runs-on: ubuntu-latest
    name: Unit Testing with Terratest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Go
        uses: actions/setup-go@v4
        with:
          go-version: '1.21'
          
      - name: Install Dependencies
        run: |
          cd test
          go mod download
          
      - name: Run Unit Tests
        run: |
          cd test
          go test -v -timeout 30m
        env:
          AWS_DEFAULT_REGION: eu-north-1
          TF_VAR_test_mode: true

  integration-testing:
    runs-on: ubuntu-latest
    name: Integration Testing
    if: github.event_name == 'push'
    needs: [static-analysis, unit-testing]
    steps:
      - uses: actions/checkout@v4
      
      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: eu-north-1
          
      - name: Deploy Test Infrastructure
        run: |
          cd terraform/test-environment
          terraform init
          terraform plan -var="test_run_id=${{ github.run_id }}"
          terraform apply -auto-approve -var="test_run_id=${{ github.run_id }}"
          
      - name: Run Integration Tests
        run: |
          cd test/integration
          go test -v -timeout 45m -tags=integration
          
      - name: Cleanup Test Infrastructure
        if: always()
        run: |
          cd terraform/test-environment
          terraform destroy -auto-approve -var="test_run_id=${{ github.run_id }}"

  compliance-validation:
    runs-on: ubuntu-latest
    name: Compliance Validation
    steps:
      - uses: actions/checkout@v4
      
      - name: GDPR Compliance Check
        run: |
          # Kontrollera to all databaser has encryption
          grep -r "storage_encrypted.*=.*true" terraform/ || \
          (echo "ERROR: Icke-krypterade databaser upptäckta" && exit 1)
          
          # Kontrollera data classification tags
          grep -r "DataClassification" terraform/ || \
          (echo "ERROR: Data classification tags saknas" && exit 1)
          
      - name: Security Standards
        run: |
          # MSB security requirements for critical infrastruktur
          ./scripts/msb-compliance-check.sh terraform/
          
          # Validate to regioner is used
          if grep -r "us-" terraform/ --include="*.tf"; then
            echo "WARNING: Amerikanska regioner upptäckta - kontrollera data sovereignty"
          fi

  performance-testing:
    runs-on: ubuntu-latest
    name: Performance Testing
    if: contains(github.event.pull_request.title, 'performance') || github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      
      - name: Infrastructure Performance Tests
        run: |
          # Kör load tests mot test infrastruktur
          cd test/performance
          ./run-load-tests.sh
          
      - name: Cost Analysis
        run: |
          # Beräkna förvänkade kostnader for infrastructure changes
          ./scripts/cost-analysis.sh terraform/
```

## Summary


The modern Architecture as Code methodology represents framtiden for infrastructure management in organizations.
Comprehensive testing strategies for Architecture as Code is essential to ensure reliable, secure and cost-effective infrastructure deployments. a väl designad test pyramid with unit tests, integration tests and end-to-end validation can dramatiskt reducera production issues and improve developer confidence.

organizations must particularly focus at compliance testing as validates GDPR requirements, financial regulations and government security standards. Automated policy testing with tools that OPA enables continuous compliance verification without manual overhead.

Investment in robust Architecture as Code testing frameworks pays off through reduced production incidents, faster development cycles and improved regulatory compliance. Modern testing tools and cloud-native testing strategies enables comprehensive validation without prohibitive costs or complexity.

## Sources and referenser

- Terratest Documentation. "Infrastructure Testing for Terraform." Gruntwork, 2023.
- Open Policy Agent. "Policy Testing Architecture as Code best practices." CNCF OPA Project, 2023.
- AWS. "Infrastructure Testing Strategy Guide." Amazon Web Services, 2023.
- Kubernetes. "Testing Infrastructure and Applications." Kubernetes Documentation, 2023.
- NIST. "Security Testing for Cloud Infrastructure." NIST Cybersecurity Framework, 2023.
- CSA. "Cloud Security Testing Guidelines." Cloud Security Alliance, 2023.
- Vitest. "Next Generation Testing Framework." Vitest Documentation, 2024.