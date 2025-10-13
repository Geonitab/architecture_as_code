# Cloud Architecture as Code

Cloud Architecture as Code represents the natural development of Architecture as Code in cloud-based environments. By utilising cloud providers' APIs and services, organisations can create scalable, resilient, and cost-effective architectures entirely through Architecture as Code. As we saw in [chapter 2 about Fundamental principles](02_kapitel1.md), this method is fundamental for modern organisations as they strive for digital transformation and operational excellence.

![Cloud Architecture as Code](images/diagram_05_kapitel4.png)

The diagram illustrates the progression from multi-cloud environments through provider abstraction and resource management to state management and cross-region deployment capabilities. This progression enables the type of scalable Architecture as Code automation that we will delve into in [chapter 4 about CI/CD pipelines](04_kapitel3.md) and the organisational change as discussed in [chapter 10](10_kapitel9.md).

## Cloud Providers' Ecosystem for Architecture as Code

Swedish organisations face a rich selection of cloud providers, each with their own strengths and specialisations. To achieve successful cloud adoption, organisations must understand each provider's unique capabilities and how these can be leveraged through Architecture as Code approaches.

### Amazon Web Services (AWS) and Swedish organisations

AWS dominates the global cloud market and has established a strong presence in Sweden through data centres in the Stockholm region. For Swedish organisations, AWS offers comprehensive services that are particularly relevant for local compliance requirements and performance needs.

**AWS CloudFormation** is AWS's native Infrastructure as Code service and enables declarative definition of AWS resources through JSON or YAML templates. CloudFormation handles resource dependencies automatically and ensures infrastructure deployments are reproducible and recoverable:

For a detailed CloudFormation template to implement VPC configuration for Swedish organisations with GDPR compliance, see [07_CODE_1: VPC Configuration for Swedish organisations](#07_CODE_1) in Appendix A.

**AWS CDK (Cloud Development Kit)** revolutionizes Architecture as Code by enabling the definition of cloud resources with programming languages such as TypeScript, Python, Java, and C#. For Swedish development teams who already master these languages, it reduces the CDK learning curve and enables reuse of existing programming skills:

```typescript
// cdk/swedish-org-infrastructure.ts
import * as cdk from 'AWS CDK Library';
import * as ec2 from 'AWS CDK library for EC2';
import * as rds from 'aws-cdk-lib/aws-rds';
import * as logs from 'AWS CDK library for AWS Logs';
import * as kms from 'aws-cdk-lib/aws-kms';
import { Construct } from 'constructs';

export interface SvenskaOrgInfrastructureProps extends cdk.StackProps {
  environment: 'development' | 'preparing' | 'production';
  dataClassification: 'public' | 'internal' | 'confidential' | 'limited';
  complianceRequirements: string[];
  costCenter: string;
  organizationalUnit: string;
}

export class SvenskaOrgInfrastructureStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: SvenskaOrgInfrastructureProps) {
    super(scope, id, props);

    // Define common tags for all resources
    const commonTags = {
      Environment: props.environment,
      DataClassification: props.dataClassification,
      CostCenter: props.costCenter,
      OrganizationalUnit: props.organizationalUnit,
      Country: 'Sweden',
      Region: 'eu-north-1',
      ComplianceRequirements: props.complianceRequirements.join(','),
      ManagedBy: 'AWS Cloud Development Kit',
      LastUpdated: new Date().toISOString().split('T')[0]
    };

    // Create VPC with Swedish security requirements
    const vpc = new ec2.Vpc(this, 'SwedishOrgVPC', {
      cidr: props.environment === 'production' ? '10.0.0.0/16' : '10.1.0.0/16',
      maxAzs: props.environment === 'production' ? 3 : 2,
      enableDnsHostnames: true,
      enableDnsSupport: true,
      subnetConfiguration: [
        {
          cidrMask: 24,
          name: 'Public',
          subnetType: ec2.SubnetType.PUBLIC,
        },
        {
          cidrMask: 24,
          name: 'Private',
          subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS,
        },
        {
          cidrMask: 24,
          name: 'Database',
          subnetType: ec2.SubnetType.PRIVATE_ISOLATED,
        }
      ],
      flowLogs: {
        cloudwatch: {
          logRetention: logs.RetentionDays.THREE_MONTHS
        }
      }
    });

    // Apply common tags at VPC
    Object.entries(commonTags).forEach(([key, value]) => {
      cdk.Tags.of(vpc).add(key, value);
    });

    // GDPR-compliant KMS key for database encryption
    const databaseEncryptionKey = new kms.Key(this, 'Database Encryption Key', {
      description: 'KMS key for database encryption according to GDPR requirements',
      enableKeyRotation: true,
      removalPolicy: props.environment === 'production' ? 
        cdk.RemovalPolicy.RETAIN : cdk.RemovalPolicy.DESTROY
    });

    // Database subnet group for isolated database tier
    const dbSubnetGroup = new rds.SubnetGroup(this, 'Database Subnet Group', {
      vpc,
      description: 'Subnet group for GDPR-compliant databases',
      vpcSubnets: {
        subnetType: ec2.SubnetType.PRIVATE_ISOLATED
      }
    });

    // RDS instance with Swedish security requirements
    if (props.environment === 'production') {
      const database = new rds.DatabaseInstance(this, 'Primary Database', {
        engine: rds.DatabaseInstanceEngine.postgres({
          version: rds.PostgresEngineVersion.VER_15_4
        }),
        instanceType: ec2.InstanceType.of(ec2.InstanceClass.R5, ec2.InstanceSize.LARGE),
        vpc,
        subnetGroup: dbSubnetGroup,
        storageEncrypted: true,
        storageEncryptionKey: databaseEncryptionKey,
        backupRetention: cdk.Duration.days(30),
        deletionProtection: true,
        deleteAutomatedBackups: false,
        enablePerformanceInsights: true,
        monitoringInterval: cdk.Duration.seconds(60),
        cloudwatchLogsExports: ['PostgreSQL'],
        parameters: {
          // Swedish time zone and locale
          'timezone': 'Europe/Stockholm',
          'LC messages': 'sv_SE.UTF-8',
          'lc_monetary': 'sv_SE.UTF-8',
          'lc_numeric': 'sv_SE.UTF-8',
          'lc_time': 'sv_SE.UTF-8',
          // GDPR-relevant settings
          'log statement': 'all',
          'log_min_duration_statement': 'Zero',
          'shared_preload_libraries': 'pg_stat_statements',
          // Security settings
          'SSL': 'on',
          'SSL Ciphers': 'HIGH:!aNULL:!MD5',
          'ssl_prefer_server_ciphers': 'on'
        }
      });

      // Apply Swedish compliance tags
      cdk.Tags.of(database).add('Data Residency', 'Sweden');
      cdk.Tags.of(database).add('Compliant with GDPR', 'true');
      cdk.Tags.of(database).add('Compliant with ISO 27001', 'true');
      cdk.Tags.of(database).add('Backup Retention', '30 days');
    }

    // Security groups with Swedish security standards
    const webSecurityGroup = new ec2.SecurityGroup(this, 'Web Security Group', {
      vpc,
      description: 'Security group for the web tier according to Swedish security requirements',
      allowAllOutbound: false
    });

    // Restrict incoming traffic to HTTPS only
    webSecurityGroup.addIngressRule(
      ec2.Peer.anyIpv4(),
      ec2.Port.tcp(443),
      'HTTPS from the internet'
    );

    // Allow outgoing traffic only to necessary services
    webSecurityGroup.addEgressRule(
      ec2.Peer.anyIpv4(),
      ec2.Port.tcp(443),
      'HTTPS outgoing'
    );

    // Application security group with restrictive access
    const appSecurityGroup = new ec2.SecurityGroup(this, 'Application Security Group', {
      vpc,
      description: 'Application tier security group',
      allowAllOutbound: false
    });

    appSecurityGroup.addIngressRule(
      webSecurityGroup,
      ec2.Port.tcp(8080),
      'Traffic from web tier'
    );

    // Database security group - only from app tier
    const dbSecurityGroup = new ec2.SecurityGroup(this, 'Database Security Group', {
      vpc,
      description: 'Database tier security group with limited access',
      allowAllOutbound: false
    });

    dbSecurityGroup.addIngressRule(
      appSecurityGroup,
      ec2.Port.tcp(5432),
      'PostgreSQL in the application layer'
    );

    // VPC Endpoints for AWS services (avoid data exfiltration over the internet)
    const s3Endpoint = vpc.addGatewayEndpoint('S3 Endpoint', {
      service: ec2.GatewayVpcEndpointAwsService.S3
    });

    const ec2Endpoint = vpc.addInterfaceEndpoint('EC2 Endpoint', {
      service: ec2.InterfaceVpcEndpointAwsService.EC2,
      privateDnsEnabled: true
    });

    const rdsEndpoint = vpc.addInterfaceEndpoint('RDS Endpoint', {
      service: ec2.InterfaceVpcEndpointAwsService.RDS,
      privateDnsEnabled: true
    });

    // Using CloudWatch for monitoring and logging to comply with GDPR
    const monitoringLogGroup = new logs.LogGroup(this, 'Monitoring Log Group', {
      logGroupName: `/aws/svenska-org/${props.environment}/monitoring`,
      retention: logs.RetentionDays.THREE_MONTHS,
      encryptionKey: databaseEncryptionKey
    });

    // Outputs for cross-stack references
    new cdk.CfnOutput(this, 'VPC ID', {
      value: vpc.vpcId,
      description: 'VPC ID for the Swedish organisation',
      exportName: `${this.stackName}-VPC-ID`
    });

    new cdk.CfnOutput(this, 'Compliance Status', {
      value: JSON.stringify({
        gdprCompliant: props.complianceRequirements.includes('General Data Protection Regulation'),
        iso27001Compliant: props.complianceRequirements.includes('ISO 27001'),
        dataResidency: 'Sweden',
        encryptionEnabled: true,
        auditLoggingEnabled: true
      }),
      description: 'Status of compliance for the deployed infrastructure'
    });
  }

  // Method to merge two Swedish holiday schedules for cost optimisation
  addSwedishHolidayScheduling(resource: cdk.Resource) {
    const swedishHolidays = [
      '2024-01-01', // New Year's Day
      'January 6, 2024', // Epiphany
      '2024-03-29', // Good Friday
      'April 1, 2024', // Easter Monday
      '2024-05-01', // May Day
      'May 9, 2024', // Ascension Day
      'May 20, 2024', // Whit Monday
      'June 21, 2024', // Midsummer's Eve
      'June 22, 2024', // Midsummer Day
      'November 2, 2024', // All Saints' Day
      'December 24, 2024', // Christmas Eve
      'December 25, 2024', // Christmas Day
      'December 26, 2024', // Boxing Day
      'December 31, 2024'  // New Year's Eve
    ];

    cdk.Tags.of(resource).add('Swedish Holidays', swedishHolidays.join(','));
    cdk.Tags.of(resource).add('Cost Optimisation', 'Swedish Schedule');
  }
}

// Example of usage
const app = new cdk.App();

new SvenskaOrgInfrastructureStack(app, 'SwedishOrgDev', {
  environment: 'development',
  dataClassification: 'internal',
  complianceRequirements: ['General Data Protection Regulation'],
  costCenter: 'CC-1001',
  organizationalUnit: 'IT Development',
  env: {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region: 'eu-north-1'
  }
});

new SvenskaOrgInfrastructureStack(app, 'SwedishOrgProd', {
  environment: 'production',
  dataClassification: 'confidential',
  complianceRequirements: ['General Data Protection Regulation', 'ISO 27001'],
  costCenter: 'CC-2001',
  organizationalUnit: 'IT Production',
  env: {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region: 'eu-north-1'
  }
});
```

### Microsoft Azure for Swedish organisations

Microsoft Azure has developed a strong position in Sweden, particularly within the public sector and traditional enterprise organisations. Azure Resource Manager (ARM) templates and Bicep form Microsoft's primary Architecture as Code offerings.

**Azure Resource Manager (ARM) Templates** enables declarative definition of Azure resources through JSON-based templates. For Swedish organisations that already use Microsoft products, ARM templates form a natural extension of existing Microsoft skills:

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "metadata": {
    "description": "Azure infrastructure for Swedish organisations that complies with GDPR",
    "writer": "Swedish IT Department"
  },
  "parameters": {
    "environment type": {
      "type": "string",
      "default value": "development",
      "permissible values": ["development", "preparing", "production"],
      "metadata": {
        "description": "Environment type for deployment"
      }
    },
    "data classification": {
      "type": "string",
      "default value": "internal",
      "permissible values": ["public", "internal", "confidential", "limited"],
      "metadata": {
        "description": "Data classification according to Swedish security standards"
      }
    },
    "organizationName": {
      "type": "string",
      "default value": "Swedish organisation",
      "metadata": {
        "description": "Organisation name for resource naming"
      }
    },
    "Cost Centre": {
      "type": "string",
      "metadata": {
        "description": "Cost centre for invoicing"
      }
    },
    "GDPR compliance": {
      "type": "bool",
      "default value": true,
      "metadata": {
        "description": "Enable GDPR compliance features"
      }
    }
  },
  "variables": {
    "resourcePrefix": "[concat(parameters('organizationName'), '-', parameters('environmentType'))]",
    "location": "Central Sweden",
    "Virtual Network Name": "[concat(variables('resourcePrefix'), '-vnet')]",
    "Subnet Names": {
      "web": "[concat(variables('resourcePrefix'), '-web-subnet')]",
      "app": "[concat(variables('resourcePrefix'), '-app-subnet')]",
      "database": "[concat(variables('resourcePrefix'), '-db-subnet')]"
    },
    "NSG Names": {
      "web": "[concat(variables('resourcePrefix'), '-web-nsg')]",
      "app": "[concat(variables('resourcePrefix'), '-app-nsg')]",
      "database": "[concat(variables('resourcePrefix'), '-db-nsg')]"
    },
    "common tags": {
      "Environment": "[parameters('environmentType')]",
      "Data Classification": "[parameters('dataClassification')]",
      "Cost Centre": "[parameters('costCenter')]",
      "Country": "Sweden",
      "Region": "Central Sweden",
      "Compliant with GDPR": "[string(parameters('gdprCompliance'))]",
      "Managed By": "ARM Template",
      "Last Deployed": "[utcNow()]"
    }
  },
  "resources": [
    {
      "type": "Microsoft Network Virtual Networks",
      "apiVersion": "2023-04-01",
      "name": "[variables('vnetName')]",
      "location": "[variables('location')]",
      "labels": "[variables('commonTags')]",
      "properties": {
        "address space": {
          "address prefixes": [
            "[if(equals(parameters('environmentType'), 'production'), '10.0.0.0/16', '10.1.0.0/16')]"
          ]
        },
        "Enable DDoS Protection": "[equals(parameters('environmentType'), 'production')]",
        "sub-networks": [
          {
            "name": "[variables('subnetNames').web]",
            "properties": {
              "addressPrefix": "[if(equals(parameters('environmentType'), 'production'), '10.0.1.0/24', '10.1.1.0/24')]",
              "Network Security Group": {
                "ID": "[resourceId('Microsoft.Network/networkSecurityGroups', variables('nsgNames').web)]"
              },
              "service endpoints": [
                {
                  "service": "Microsoft Storage",
                  "places": ["Central Sweden", "Southern Sweden"]
                },
                {
                  "service": "Microsoft Key Vault",
                  "places": ["Central Sweden", "Southern Sweden"]
                }
              ]
            }
          },
          {
            "name": "[variables('subnetNames').app]",
            "properties": {
              "addressPrefix": "[if(equals(parameters('environmentType'), 'production'), '10.0.2.0/24', '10.1.2.0/24')]",
              "Network Security Group": {
                "ID": "[resourceId('Microsoft.Network/networkSecurityGroups', variables('nsgNames').app)]"
              },
              "service endpoints": [
                {
                  "service": "Microsoft SQL",
                  "places": ["Central Sweden", "Southern Sweden"]
                }
              ]
            }
          },
          {
            "name": "[variables('subnetNames').database]",
            "properties": {
              "addressPrefix": "[if(equals(parameters('environmentType'), 'production'), '10.0.3.0/24', '10.1.3.0/24')]",
              "Network Security Group": {
                "ID": "[resourceId('Microsoft.Network/networkSecurityGroups', variables('nsgNames').database)]"
              },
              "groups of representatives": [
                {
                  "name": "Microsoft DB for PostgreSQL Flexible Servers",
                  "properties": {
                    "serviceName": "Microsoft DB for PostgreSQL Flexible Servers"
                  }
                }
              ]
            }
          }
        ]
      },
      "depends on": [
        "[resourceId('Microsoft.Network/networkSecurityGroups', variables('nsgNames').web)]",
        "[resourceId('Microsoft.Network/networkSecurityGroups', variables('nsgNames').app)]",
        "[resourceId('Microsoft.Network/networkSecurityGroups', variables('nsgNames').database)]"
      ]
    },
    {
      "type": "Microsoft Network Security Groups",
      "apiVersion": "2023-04-01",
      "name": "[variables('nsgNames').web]",
      "location": "[variables('location')]",
      "labels": "[union(variables('commonTags'), createObject('Tier', 'Web'))]",
      "properties": {
        "securityRules": [
          {
            "name": "Permit HTTPS inbound connections",
            "properties": {
              "description": "Allow HTTPS traffic from the internet",
              "protocol": "TCP",
              "Source Port Range": "*",
              "destination port range": "443",
              "Source Address Prefix": "Internet",
              "destination address prefix": "*",
              "access": "Permit",
              "priority": 100,
              "direction": "Arriving"
            }
          },
          {
            "name": "Permit HTTP Redirect",
            "properties": {
              "description": "Allow HTTP to redirect to HTTPS",
              "protocol": "TCP",
              "Source Port Range": "*",
              "destination port range": "eighty",
              "Source Address Prefix": "Internet",
              "destination address prefix": "*",
              "access": "Permit",
              "priority": 110,
              "direction": "Arriving"
            }
          },
          {
            "name": "Block all incoming connections",
            "properties": {
              "description": "Block all other incoming traffic",
              "protocol": "*",
              "Source Port Range": "*",
              "destination port range": "*",
              "Source Address Prefix": "*",
              "destination address prefix": "*",
              "access": "Refuse",
              "priority": 4096,
              "direction": "Arriving"
            }
          }
        ]
      }
    },
    {
      "condition": "[parameters('gdprCompliance')]",
      "type": "Microsoft Key Vault vaults",
      "apiVersion": "2023-02-01",
      "name": "[concat(variables('resourcePrefix'), '-kv')]",
      "location": "[variables('location')]",
      "labels": "[union(variables('commonTags'), createObject('Purpose', 'GDPR-Compliance'))]",
      "properties": {
        "SKU": {
          "family": "A",
          "name": "standard"
        },
        "tenant identifier": "[subscription().tenantId]",
        "Enabled for deployment": false,
        "Enabled for Disk Encryption": true,
        "Enabled for template deployment": true,
        "Enable Soft Delete": true,
        "Number of days to retain soft-deleted items": 90,
        "Enable Purge Protection": "[equals(parameters('environmentType'), 'production')]",
        "Enable RBAC Authorisation": true,
        "Network ACLs": {
          "defaultAction": "Refuse",
          "circumvent": "Azure Services",
          "Virtual network rules": [
            {
              "ID": "[resourceId('Microsoft.Network/virtualNetworks/subnets', variables('vnetName'), variables('subnetNames').app)]",
              "ignoreMissingVnetServiceEndpoint": false
            }
          ]
        }
      },
      "depends on": [
        "[resourceId('Microsoft.Network/virtualNetworks', variables('vnetName'))]"
      ]
    }
  ],
  "outputs": {
    "vnetId": {
      "type": "string",
      "value": "[resourceId('Microsoft.Network/virtualNetworks', variables('vnetName'))]",
      "metadata": {
        "description": "Resource ID for the created virtual network"
      }
    },
    "Subnet IDs": {
      "type": "object",
      "value": {
        "web": "[resourceId('Microsoft.Network/virtualNetworks/subnets', variables('vnetName'), variables('subnetNames').web)]",
        "app": "[resourceId('Microsoft.Network/virtualNetworks/subnets', variables('vnetName'), variables('subnetNames').app)]",
        "database": "[resourceId('Microsoft.Network/virtualNetworks/subnets', variables('vnetName'), variables('subnetNames').database)]"
      },
      "metadata": {
        "description": "Resource IDs for all created subnets"
      }
    },
    "Compliance Status": {
      "type": "object",
      "value": {
        "GDPR Compliant": "[parameters('gdprCompliance')]",
        "data residency": "Sweden",
        "Encryption Enabled": true,
        "Audit logging is enabled": true,
        "network segmentation": true,
        "Access Control Enabled": true
      },
      "metadata": {
        "description": "Status of compliance for the deployed infrastructure"
      }
    }
  }
}
```

**Azure Bicep** represents the next generation of ARM templates with improved syntax and developer experience. Bicep compiles to ARM templates but offers more readable and maintainable code:

```bicep
// bicep/swedish-org-infrastructure.bicep
// Azure Bicep for Swedish organisations that comply with GDPR

@description('Environment type for deployment')
@allowed(['development', 'preparing', 'production'])
param environmentType string = 'development'

@description('Data classification according to Swedish security standards')
@allowed(['public', 'internal', 'confidential', 'limited'])
param dataClassification string = 'internal'

@description('Organisation name for resource naming')
param organizationName string = 'Swedish organisation'

@description('Cost centre for invoicing')
param costCenter string

@description('Enable GDPR compliance features')
param gdprCompliance bool = true

@description('List of compliance requirements')
param complianceRequirements array = ['General Data Protection Regulation']

// Variables for consistent naming and configuration
var resourcePrefix = '${organizationName}-${environmentType}'
var location = 'Central Sweden'
var isProduction = environmentType == 'production'

// Common tags for all resources
var commonTags = {
  Environment: environmentType
  DataClassification: dataClassification
  CostCenter: costCenter
  Country: 'Sweden'
  Region: 'Central Sweden'
  GDPRCompliant: string(gdprCompliance)
  ComplianceRequirements: join(complianceRequirements, ',')
  ManagedBy: 'Azure Bicep'
  LastDeployed: utcNow('yyyy-MM-dd')
}

// Log Analytics Workspace designed for Swedish organisations
resource logAnalytics 'Microsoft Operational Insights workspaces version 2023-09-01' = if (gdprCompliance) {
  name: '${resourcePrefix}-law'
  location: location
  tags: union(commonTags, {
    Purpose: 'Logging for GDPR Compliance'
  })
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: isProduction ? 90 : 30
    features: {
      searchVersion: 1
      legacy: false
      enableLogAccessUsingOnlyResourcePermissions: true
    }
    workspaceCapping: {
      dailyQuotaGb: isProduction ? 50 : 10
    }
    publicNetworkAccessForIngestion: 'Not enabled'
    publicNetworkAccessForQuery: 'Not enabled'
  }
}

// Secure storage for managing secrets and encryption keys
resource keyVault 'Microsoft Key Vault version 2023-02-01' = if (gdprCompliance) {
  name: '${resourcePrefix}-kv'
  location: location
  tags: union(commonTags, {
    Purpose: 'Secret Management'
  })
  properties: {
    sku: {
      family: 'A'
      name: 'standard'
    }
    tenantId: subscription().tenantId
    enabledForDeployment: false
    enabledForDiskEncryption: true
    enabledForTemplateDeployment: true
    enableSoftDelete: true
    softDeleteRetentionInDays: 90
    enablePurgeProtection: isProduction
    enableRbacAuthorization: true
    networkAcls: {
      defaultAction: 'Refuse'
      bypass: 'Azure Services'
    }
  }
}

// Virtual Network with Swedish security requirements
resource vnet 'Microsoft.Network/virtualNetworks@2023-04-01' = {
  name: '${resourcePrefix}-vnet'
  location: location
  tags: commonTags
  properties: {
    addressSpace: {
      addressPrefixes: [
        isProduction ? '10.0.0.0/16' : '10.1.0.0/16'
      ]
    }
    enableDdosProtection: isProduction
    subnets: [
      {
        name: 'web subnet'
        properties: {
          addressPrefix: isProduction ? '10.0.1.0/24' : '10.1.1.0/24'
          networkSecurityGroup: {
            id: webNsg.id
          }
          serviceEndpoints: [
            {
              service: 'Microsoft Storage'
              locations: ['Central Sweden', 'Southern Sweden']
            }
            {
              service: 'Microsoft Key Vault'
              locations: ['Central Sweden', 'Southern Sweden']
            }
          ]
        }
      }
      {
        name: 'application subnet'
        properties: {
          addressPrefix: isProduction ? '10.0.2.0/24' : '10.1.2.0/24'
          networkSecurityGroup: {
            id: appNsg.id
          }
          serviceEndpoints: [
            {
              service: 'Microsoft SQL'
              locations: ['Central Sweden', 'Southern Sweden']
            }
          ]
        }
      }
      {
        name: 'database subnet'
        properties: {
          addressPrefix: isProduction ? '10.0.3.0/24' : '10.1.3.0/24'
          networkSecurityGroup: {
            id: dbNsg.id
          }
          delegations: [
            {
              name: 'Microsoft DB for PostgreSQL Flexible Servers'
              properties: {
                serviceName: 'Microsoft DB for PostgreSQL Flexible Servers'
              }
            }
          ]
        }
      }
    ]
  }
}

// Network Security Groups with restrictive security rules
resource webNsg 'Microsoft.Network/networkSecurityGroups@2023-04-01' = {
  name: '${resourcePrefix}-web-nsg'
  location: location
  tags: union(commonTags, { Tier: 'Web' })
  properties: {
    securityRules: [
      {
        name: 'Permit HTTPS inbound connections'
        properties: {
          description: 'Allow HTTPS traffic from the internet'
          protocol: 'TCP'
          sourcePortRange: '*'
          destinationPortRange: '443'
          sourceAddressPrefix: 'Internet'
          destinationAddressPrefix: '*'
          access: 'Permit'
          priority: 100
          direction: 'Arriving'
        }
      }
      {
        name: 'Permit HTTP Redirect'
        properties: {
          description: 'Allow HTTP to redirect to HTTPS'
          protocol: 'TCP'
          sourcePortRange: '*'
          destinationPortRange: 'eighty'
          sourceAddressPrefix: 'Internet'
          destinationAddressPrefix: '*'
          access: 'Permit'
          priority: 110
          direction: 'Arriving'
        }
      }
    ]
  }
}

resource appNsg 'Microsoft.Network/networkSecurityGroups@2023-04-01' = {
  name: '${resourcePrefix}-app-nsg'
  location: location
  tags: union(commonTags, { Tier: 'Application' })
  properties: {
    securityRules: [
      {
        name: 'Allow Web to App'
        properties: {
          description: 'Allow traffic from the web tier to the app tier'
          protocol: 'TCP'
          sourcePortRange: '*'
          destinationPortRange: '8,080'
          sourceAddressPrefix: isProduction ? '10.0.1.0/24' : '10.1.1.0/24'
          destinationAddressPrefix: '*'
          access: 'Permit'
          priority: 100
          direction: 'Arriving'
        }
      }
    ]
  }
}

resource dbNsg 'Microsoft.Network/networkSecurityGroups@2023-04-01' = {
  name: '${resourcePrefix}-db-nsg'
  location: location
  tags: union(commonTags, { Tier: 'Database' })
  properties: {
    securityRules: [
      {
        name: 'Permit Application to Access Database'
        properties: {
          description: 'Allow database connections from app tier'
          protocol: 'TCP'
          sourcePortRange: '*'
          destinationPortRange: '5,432'
          sourceAddressPrefix: isProduction ? '10.0.2.0/24' : '10.1.2.0/24'
          destinationAddressPrefix: '*'
          access: 'Permit'
          priority: 100
          direction: 'Arriving'
        }
      }
    ]
  }
}

// PostgreSQL Flexible Server for data storage compliant with GDPR
resource postgresServer 'Microsoft.DBforPostgreSQL/flexibleServers@2023-06-01-preview' = if (isProduction) {
  name: '${resourcePrefix}-postgres'
  location: location
  tags: union(commonTags, {
    DatabaseEngine: 'PostgreSQL'
    DataResidency: 'Sweden'
  })
  sku: {
    name: 'Standard_D4s_v3'
    tier: 'General Purpose'
  }
  properties: {
    administratorLogin: 'pgAdmin'
    administratorLoginPassword: 'TempPassword123!' // Will come to changes via Key Vault
    version: 'fifteen'
    storage: {
      storageSizeGB: 128
      autoGrow: 'Enabled'
    }
    backup: {
      backupRetentionDays: 35
      geoRedundantBackup: 'Enabled'
    }
    network: {
      delegatedSubnetResourceId: '${vnet.id}/subnets/database-subnet'
      privateDnsZoneArmResourceId: postgresPrivateDnsZone.id
    }
    highAvailability: {
      mode: 'Zone Redundant'
    }
    maintenanceWindow: {
      customWindow: 'Enabled'
      dayOfWeek: 6 // Saturday
      startHour: 2
      startMinute: 0
    }
  }
}

// Private DNS Zone for PostgreSQL
resource postgresPrivateDnsZone 'Microsoft.Network/privateDnsZones@2020-06-01' = if (isProduction) {
  name: '${resourcePrefix}-postgres.private.postgres.database.azure.com'
  location: 'worldwide'
  tags: commonTags
}

resource postgresPrivateDnsZoneVnetLink 'Microsoft.Network/privateDnsZones/virtualNetworkLinks@2020-06-01' = if (isProduction) {
  parent: postgresPrivateDnsZone
  name: '${resourcePrefix}-postgres-vnet-link'
  location: 'worldwide'
  properties: {
    registrationEnabled: false
    virtualNetwork: {
      id: vnet.id
    }
  }
}

// Settings for GDPR compliance logging diagnostics
resource vnetDiagnostics 'Microsoft Insights diagnostic settings version 2021-05-01-preview' = if (gdprCompliance) {
  name: '${resourcePrefix}-vnet-diagnostics'
  scope: vnet
  properties: {
    workspaceId: logAnalytics.id
    logs: [
      {
        categoryGroup: 'all logs'
        enabled: true
        retentionPolicy: {
          enabled: true
          days: isProduction ? 90 : 30
        }
      }
    ]
    metrics: [
      {
        category: 'AllMetrics'
        enabled: true
        retentionPolicy: {
          enabled: true
          days: isProduction ? 90 : 30
        }
      }
    ]
  }
}

// Outputs for cross-template references
output vnetId string = vnet.id
output subnetIds object = {
  web: '${vnet.id}/subnets/web-subnet'
  app: '${vnet.id}/subnets/app-subnet'
  database: '${vnet.id}/subnets/database-subnet'
}

output complianceStatus object = {
  gdprCompliant: gdprCompliance
  dataResidency: 'Sweden'
  encryptionEnabled: true
  auditLoggingEnabled: gdprCompliance
  networkSegmentation: true
  accessControlEnabled: true
  backupRetention: isProduction ? 'thirty-five days' : '7 days'
}

output keyVaultId string = gdprCompliance ? keyVault.id : ''
output logAnalyticsWorkspaceId string = gdprCompliance ? logAnalytics.id : ''
```

### Google Cloud Platform for Swedish innovation organisations

Google Cloud Platform (GCP) attracts Swedish tech companies and startups through its machine learning capabilities and innovative services. Google Cloud Deployment Manager and the Terraform Google Provider form the primary Infrastructure as Code tools for GCP.

**Google Cloud Deployment Manager** uses YAML or Python for Architecture as Code definitions and integrates naturally with Google Cloud services:

```yaml
# gcp/swedish-org-infrastructure.yaml
# Deployment Manager template for Swedish organisations

resources:
  # VPC Network for Swedish data residency
  - name: svenska-org-vpc
    type: compute.v1.network
    properties:
      description: "VPC for Swedish organisations that comply with GDPR"
      autoCreateSubnetworks: false
      routingConfig:
        routingMode: REGIONAL
    metadata:
      labels:
        environment: $(ref.environment)
        data-classification: $(ref.dataClassification)
        country: sweden
        gdpr-compliant: "true"

  # Subnets with Swedish region requirements
  - name: web-subnet
    type: compute.v1.subnetwork
    properties:
      description: "Web tier subnet for Swedish applications"
      network: $(ref.svenska-org-vpc.selfLink)
      ipCidrRange: "10.0.1.0/24"
      region: europe-north1
      enableFlowLogs: true
      logConfig:
        enable: true
        flowSampling: 1.0
        aggregationInterval: INTERVAL_5_SEC
        metadata: INCLUDE_ALL_METADATA
      secondaryIpRanges:
        - rangeName: pods
          ipCidrRange: "10.1.0.0/16"
        - rangeName: services
          ipCidrRange: "10.2.0.0/20"

  - name: app-subnet
    type: compute.v1.subnetwork
    properties:
      description: "Application layer subnet"
      network: $(ref.svenska-org-vpc.selfLink)
      ipCidrRange: "10.0.2.0/24"
      region: europe-north1
      enableFlowLogs: true
      logConfig:
        enable: true
        flowSampling: 1.0
        aggregationInterval: INTERVAL_5_SEC

  - name: database-subnet
    type: compute.v1.subnetwork
    properties:
      description: "Database tier subnet with private access"
      network: $(ref.svenska-org-vpc.selfLink)
      ipCidrRange: "10.0.3.0/24"
      region: europe-north1
      enableFlowLogs: true
      purpose: PRIVATE_SERVICE_CONNECT

  # Cloud SQL for GDPR-compliant databases
  - name: svenska-org-postgres
    type: sqladmin.v1beta4.instance
    properties:
      name: svenska-org-postgres-$(ref.environment)
      region: europe-north1
      databaseVersion: POSTGRES_15
      settings:
        tier: db-custom-4-16384
        edition: ENTERPRISE
        availabilityType: REGIONAL
        dataDiskType: PD_SSD
        dataDiskSizeGb: 100
        storageAutoResize: true
        storageAutoResizeLimit: 500
        
        # Swedish time zone and locale
        databaseFlags:
          - name: timezone
            value: "Europe/Stockholm"
          - name: lc_messages
            value: "sv_SE.UTF-8"
          - name: log_statement
            value: "all"
          - name: log_min_duration_statement
            value: "Zero"
          - name: ssl
            value: "on"
        
        # Backup and recovery for Swedish requirements
        backupConfiguration:
          enabled: true
          startTime: "2:00 PM"
          location: "europe-north1"
          backupRetentionSettings:
            retentionUnit: COUNT
            retainedBackups: 30
          transactionLogRetentionDays: 7
          pointInTimeRecoveryEnabled: true
        
        # Security settings
        ipConfiguration:
          ipv4Enabled: false
          privateNetwork: $(ref.svenska-org-vpc.selfLink)
          enablePrivatePathForGoogleCloudServices: true
          authorizedNetworks: []
          requireSsl: true
        
        # Maintenance for Swedish working hours
        maintenanceWindow:
          hour: 2
          day: 6  # Saturday
          updateTrack: stable
        
        deletionProtectionEnabled: true
        
        # Logging for GDPR compliance
        insights:
          queryInsightsEnabled: true
          recordApplicationTags: true
          recordClientAddress: true
          queryStringLength: 4500
          queryPlansPerMinute: 20

  # Cloud KMS for encryption of sensitive data
  - name: svenska-org-keyring
    type: cloudkms.v1.keyRing
    properties:
      parent: projects/$(env.project)/locations/europe-north1
      keyRingId: svenska-org-keyring-$(ref.environment)

  - name: database-encryption-key
    type: cloudkms.v1.cryptoKey
    properties:
      parent: $(ref.svenska-org-keyring.name)
      cryptoKeyId: database-encryption-key
      purpose: ENCRYPT_DECRYPT
      versionTemplate:
        algorithm: GOOGLE_SYMMETRIC_ENCRYPTION
        protectionLevel: SOFTWARE
      rotationPeriod: 7776000s  # 90 days
      nextRotationTime: $(ref.nextRotationTime)

  # Firewall rules for secure network traffic
  - name: allow-web-to-app
    type: compute.v1.firewall
    properties:
      description: "Allow HTTPS traffic from web to app tier"
      network: $(ref.svenska-org-vpc.selfLink)
      direction: INGRESS
      priority: 1000
      sourceRanges:
        - "10.0.1.0/24"
      targetTags:
        - "application server"
      allowed:
        - IPProtocol: tcp
          ports: ["8,080"]

  - name: allow-app-to-database
    type: compute.v1.firewall
    properties:
      description: "Allow database connections from app tier"
      network: $(ref.svenska-org-vpc.selfLink)
      direction: INGRESS
      priority: 1000
      sourceRanges:
        - "10.0.2.0/24"
      targetTags:
        - "database server"
      allowed:
        - IPProtocol: tcp
          ports: ["5,432"]

  - name: deny-all-ingress
    type: compute.v1.firewall
    properties:
      description: "Block all other incoming traffic"
      network: $(ref.svenska-org-vpc.selfLink)
      direction: INGRESS
      priority: 65534
      sourceRanges:
        - "0.0.0.0/0"
      denied:
        - IPProtocol: all

  # Cloud Logging to ensure GDPR compliance
  - name: svenska-org-log-sink
    type: logging.v2.sink
    properties:
      name: svenska-org-compliance-sink
      destination: storage.googleapis.com/svenska-org-audit-logs-$(ref.environment)
      filter: |
        resource.type="GCE instance" OR
        resource.type="Cloud SQL Database" OR
        resource.type="GCE Network" OR
        protoPayload.authenticationInfo.principalEmail!=""
      uniqueWriterIdentity: true

  # Cloud storage for audit logs with Swedish data residency
  - name: svenska-org-audit-logs
    type: storage.v1.bucket
    properties:
      name: svenska-org-audit-logs-$(ref.environment)
      location: EUROPE-NORTH1
      storageClass: STANDARD
      versioning:
        enabled: true
      lifecycle:
        rule:
          - action:
              type: SetStorageClass
              storageClass: NEARLINE
            condition:
              age: 30
          - action:
              type: SetStorageClass  
              storageClass: COLDLINE
            condition:
              age: 90
          - action:
              type: Delete
            condition:
              age: 2555  # 7 years for Swedish requirements
      retentionPolicy:
        retentionPeriod: 220752000  # 7 years in seconds
      iamConfiguration:
        uniformBucketLevelAccess:
          enabled: true
      encryption:
        defaultKmsKeyName: $(ref.database-encryption-key.name)

outputs:
  - name: vpcId
    value: $(ref.svenska-org-vpc.id)
  - name: subnetIds
    value:
      web: $(ref.web-subnet.id)
      app: $(ref.app-subnet.id)
      database: $(ref.database-subnet.id)
  - name: complianceStatus
    value:
      gdprCompliant: true
      dataResidency: "Sweden"
      encryptionEnabled: true
      auditLoggingEnabled: true
      backupRetention: "30 days"
      logRetention: "seven years"
```

## Cloud-native architecture as code patterns

Cloud-native Infrastructure as Code patterns leverage cloud-specific services and capabilities to create optimal architectures. These patterns include serverless computing, managed databases, auto-scaling groups, and event-driven architectures, eliminating traditional infrastructure management.

Microservices-based architectures are implemented through container orchestration, service mesh, and API gateways defined as code. This enables loose coupling, independent scaling, and technology diversification while operational complexity is managed through automation.

### Container-First Architecture Pattern

Modern cloud architecture builds on containerisation as the fundamental abstraction for application deployment. For Swedish organisations, this means that infrastructure definitions focus on container orchestration platforms such as Kubernetes, AWS ECS, Azure Container Instances, or Google Cloud Run:

```terraform
# terraform/container-platform.tf
# Container platform for Swedish organisations

resource "Kubernetes namespace" "application_namespace" {
  count = length(var.environments)
  
  metadata {
    name = "${var.organization_name}-${var.environments[count.index]}"
    
    labels = {
      "app.kubernetes.io/managed-by" = "terraform"
      "svenska.se/environment"       = var.environments[count.index]
      "svenska.se/data-classification" = var.data_classification
      "svenska.se/cost-centre"       = var.cost_center
      "svenska.se/gdpr-compliant"    = "true"
      "svenska.se/backup policy"     = var.environments[count.index] == "production" ? "daily" : "weekly"
    }
    
    annotations = {
      "svenska.se/contact-email"     = var.contact_email
      "svenska.se/created-date"      = timestamp()
      "svenska.se/compliance-review" = var.compliance_review_date
    }
  }
}

# Resource Quotas for cost control and resource governance
resource "Kubernetes Resource Quota" "Namespace quota" {
  count = length(var.environments)
  
  metadata {
    name      = "${var.organization_name}-${var.environments[count.index]}-quota"
    namespace = kubernetes_namespace.application_namespace[count.index].metadata[0].name
  }
  
  spec {
    hard = {
      "CPU requests"    = var.environments[count.index] == "production" ? "eight" : "two"
      "requests memory" = var.environments[count.index] == "production" ? "16GB" : "4GB"
      "CPU limits"      = var.environments[count.index] == "production" ? "sixteen" : "four"
      "memory limits"   = var.environments[count.index] == "production" ? "32 GB" : "8 GB"
      "persistent volume claims" = var.environments[count.index] == "production" ? "ten" : "three"
      "requests.storage" = var.environments[count.index] == "production" ? "100 GiB" : "20 GB"
      "count pods"      = var.environments[count.index] == "production" ? "fifty" : "ten"
      "count/services"  = var.environments[count.index] == "production" ? "twenty" : "five"
    }
  }
}

# Network policies for micro-segmentation and security
resource "Kubernetes Network Policy" "deny all by default" {
  count = length(var.environments)
  
  metadata {
    name      = "deny all by default"
    namespace = kubernetes_namespace.application_namespace[count.index].metadata[0].name
  }
  
  spec {
    pod_selector {}
    policy_types = ["Entry", "Exit"]
  }
}

resource "Kubernetes Network Policy" "Allow web to app" {
  count = length(var.environments)
  
  metadata {
    name      = "Allow web to app"
    namespace = kubernetes_namespace.application_namespace[count.index].metadata[0].name
  }
  
  spec {
    pod_selector {
      match_labels = {
        "app.kubernetes.io/component" = "app"
      }
    }
    
    policy_types = ["Entry"]
    
    ingress {
      from {
        pod_selector {
          match_labels = {
            "app.kubernetes.io/component" = "web"
          }
        }
      }
      ports {
        protocol = "TCP"
        port     = "8,080"
      }
    }
  }
}

# Pod Security Standards for Swedish security requirements
resource "Kubernetes Pod Security Policy" "Swedish_org_psp" {
  metadata {
    name = "${var.organization_name}-pod-security-policy"
  }
  
  spec {
    privileged                 = false
    allow_privilege_escalation = false
    required_drop_capabilities = ["ALL"]
    volumes                    = ["configuration map", "emptyDir", "projected", "secret", "downward API", "persistent volume claim"]
    
    run_as_user {
      rule = "Must run as non-root"
    }
    
    run_as_group {
      rule = "MustRunAs"
      range {
        min = 1
        max = 65535
      }
    }
    
    supplemental_groups {
      rule = "MustRunAs"
      range {
        min = 1
        max = 65535
      }
    }
    
    fs_group {
      rule = "RunAsAny"
    }
    
    se_linux {
      rule = "RunAsAny"
    }
  }
}

# Service Mesh setup for Swedish microservices
resource "Kubernetes manifest" "istio namespace" {
  count = var.enable_service_mesh ? length(var.environments) : 0
  
  manifest = {
    apiVersion = "v1"
    kind       = "Namespace"
    metadata = {
      name = "${var.organization_name}-${var.environments[count.index]}-istio"
      labels = {
        "istio-injection" = "activated"
        "svenska.se/service-mesh" = "istio"
        "svenska.se/mtls-mode" = "rigorous"
      }
    }
  }
}

resource "Kubernetes manifest" "Istio Peer Authentication" {
  count = var.enable_service_mesh ? length(var.environments) : 0
  
  manifest = {
    apiVersion = "security.istio.io/v1beta1"
    kind       = "Peer Authentication"
    metadata = {
      name      = "default"
      namespace = kubernetes_manifest.istio_namespace[count.index].manifest.metadata.name
    }
    spec = {
      mtls = {
        mode = "STRICT"
      }
    }
  }
}

# Ensuring GDPR compliance using Pod Disruption Budgets
resource "Kubernetes Pod Disruption Budget" "application PDB" {
  count = length(var.environments)
  
  metadata {
    name      = "${var.organization_name}-app-pdb"
    namespace = kubernetes_namespace.application_namespace[count.index].metadata[0].name
  }
  
  spec {
    min_available = var.environments[count.index] == "production" ? "two" : "one"
    selector {
      match_labels = {
        "Application name in Kubernetes" = var.organization_name
        "app.kubernetes.io/component" = "app"
      }
    }
  }
}
```

### Serverless-first pattern for Swedish innovation organisations

Serverless architectures enable unprecedented scalability and cost efficiency for Swedish organisations. Architecture as Code for serverless focuses on function definitions, event routing, and managed service integrations:

```terraform
# terraform/serverless-platform.tf
# Serverless platform designed for organisations in Sweden

# AWS Lambda functions with Swedish compliance requirements
resource "AWS Lambda function" "Swedish API Gateway" {
  filename         = "svenska-api-${var.version}.zip"
  function_name    = "${var.organization_name}-api-gateway-${var.environment}"
  role            = aws_iam_role.lambda_execution_role.arn
  handler         = "index.handler"
  source_code_hash = filebase64sha256("svenska-api-${var.version}.zip")
  runtime         = "Node.js version 18.x"
  timeout         = 30
  memory_size     = 512
  
  environment {
    variables = {
      ENVIRONMENT           = var.environment
      DATA_CLASSIFICATION   = var.data_classification
      GDPR_ENABLED         = "true"
      LOG_LEVEL            = var.environment == "production" ? "Information" : "DEBUG"
      SWEDISH_TIMEZONE     = "Europe/Stockholm"
      COST_CENTER          = var.cost_center
      COMPLIANCE_MODE      = "Swedish GDPR"
    }
  }
  
  vpc_config {
    subnet_ids         = var.private_subnet_ids
    security_group_ids = [aws_security_group.lambda_sg.id]
  }
  
  tracing_config {
    mode = "Active"
  }
  
  dead_letter_config {
    target_arn = aws_sqs_queue.dlq.arn
  }
  
  tags = merge(local.common_tags, {
    Function = "API Gateway"
    Runtime  = "Node.js18"
  })
}

# Using event-driven architecture with SQS for organisations in Sweden
resource "aws_sqs_queue" "Swedish_event_queue" {
  name                       = "${var.organization_name}-events-${var.environment}"
  delay_seconds              = 0
  max_message_size           = 262144
  message_retention_seconds  = 1209600  # 14 days
  receive_wait_time_seconds  = 20
  visibility_timeout_seconds = 120
  
  kms_master_key_id = aws_kms_key.svenska_org_key.arn
  
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.dlq.arn
    maxReceiveCount     = 3
  })
  
  tags = merge(local.common_tags, {
    MessageRetention = "14 days"
    Purpose         = "Processing of Events"
  })
}

resource "aws_sqs_queue" "dlq" {
  name                      = "${var.organization_name}-dlq-${var.environment}"
  message_retention_seconds = 1209600  # 14 days
  kms_master_key_id        = aws_kms_key.svenska_org_key.arn
  
  tags = merge(local.common_tags, {
    Purpose = "Undelivered Message Queue"
  })
}

# DynamoDB for Swedish data residency
resource "AWS DynamoDB Table" "Swedish_data_store" {
  name           = "${var.organization_name}-data-${var.environment}"
  billing_mode   = "Pay per request"
  hash_key       = "ID"
  range_key      = "timestamp"
  stream_enabled = true
  stream_view_type = "New and Old Images"
  
  attribute {
    name = "ID"
    type = "S"
  }
  
  attribute {
    name = "timestamp"
    type = "S"
  }
  
  attribute {
    name = "data_subject_id"
    type = "S"
  }
  
  global_secondary_index {
    name     = "Data Subject Index"
    hash_key = "data_subject_id"
    projection_type = "ALL"
  }
  
  ttl {
    attribute_name = "ttl"
    enabled        = true
  }
  
  server_side_encryption {
    enabled     = true
    kms_key_arn = aws_kms_key.svenska_org_key.arn
  }
  
  point_in_time_recovery {
    enabled = var.environment == "production"
  }
  
  tags = merge(local.common_tags, {
    DataType       = "Personal Data"
    GDPRCompliant  = "true"
    DataResidency  = "Sweden"
  })
}

# API Gateway with Swedish security requirements
resource "AWS API Gateway REST API" "Swedish API" {
  name        = "${var.organization_name}-api-${var.environment}"
  description = "API Gateway for the Swedish organisation with GDPR compliance"
  
  endpoint_configuration {
    types = ["REGIONAL"]
  }
  
  policy = jsonencode({
    Version = "October 17, 2012"
    Statement = [
      {
        Effect = "Permit"
        Principal = "*"
        Action = "execute API: Invoke"
        Resource = "*"
        Condition = {
          IpAddress = {
            "AWS source IP" = var.allowed_ip_ranges
          }
        }
      }
    ]
  })
  
  tags = local.common_tags
}

# Using CloudWatch Logs to ensure GDPR compliance and maintain audit trails
resource "AWS CloudWatch Log Group" "lambda_logs" {
  name              = "/aws/lambda/${aws_lambda_function.svenska_api_gateway.function_name}"
  retention_in_days = var.environment == "production" ? 90 : 30
  kms_key_id       = aws_kms_key.svenska_org_key.arn
  
  tags = merge(local.common_tags, {
    LogRetention = var.environment == "production" ? "90 days" : "30 days"
    Purpose      = "General Data Protection Regulation Compliance"
  })
}

# Step Functions for Swedish business processes
resource "AWS Step Functions state machine" "Swedish_workflow" {
  name     = "${var.organization_name}-workflow-${var.environment}"
  role_arn = aws_iam_role.step_functions_role.arn
  
  definition = jsonencode({
    Comment = "The Swedish organisation's GDPR-compliant workflow"
    StartAt = "Validate Input"
    States = {
      ValidateInput = {
        Type = "Task"
        Resource = aws_lambda_function.input_validator.arn
        Next = "Process Data"
        Retry = [
          {
            ErrorEquals     = ["Lambda Service Exception", "Lambda.AWS Lambda Exception"]
            IntervalSeconds = 2
            MaxAttempts     = 3
            BackoffRate     = 2.0
          }
        ]
        Catch = [
          {
            ErrorEquals = ["Task Failed"]
            Next        = "FailureHandler"
          }
        ]
      }
      ProcessData = {
        Type = "Task"
        Resource = aws_lambda_function.data_processor.arn
        Next = "Audit Log"
      }
      AuditLog = {
        Type = "Task"
        Resource = aws_lambda_function.audit_logger.arn
        Next = "Achievement"
      }
      Success = {
        Type = "Achieve"
      }
      FailureHandler = {
        Type = "Task"
        Resource = aws_lambda_function.failure_handler.arn
        End = true
      }
    }
  })
  
  logging_configuration {
    log_destination        = "${aws_cloudwatch_log_group.step_functions_logs.arn}:*"
    include_execution_data = true
    level                 = "ALL"
  }
  
  tracing_configuration {
    enabled = true
  }
  
  tags = merge(local.common_tags, {
    WorkflowType = "GDPR Data Processing"
    Purpose      = "Business Process Automation"
  })
}

# EventBridge for event-driven Swedish organisations
resource "AWS CloudWatch Event Bus" "Swedish_event_bus" {
  name = "${var.organization_name}-events-${var.environment}"
  
  tags = merge(local.common_tags, {
    Purpose = "Event-Driven Architecture"
  })
}

resource "AWS CloudWatch Event Rule" "GDPR Data Request" {
  name           = "${var.organization_name}-gdpr-request-${var.environment}"
  description    = "Requests for rights by data subjects under GDPR"
  event_bus_name = aws_cloudwatch_event_bus.svenska_event_bus.name
  
  event_pattern = jsonencode({
    source      = ["Swedish GDPR"]
    detail-type = ["Request by Data Subject"]
    detail = {
      requestType = ["access", "correction", "effacement", "portability"]
    }
  })
  
  tags = merge(local.common_tags, {
    GDPRFunction = "Rights of the Data Subject"
  })
}

resource "AWS CloudWatch Event Target" "GDPR processor" {
  rule           = aws_cloudwatch_event_rule.gdpr_data_request.name
  event_bus_name = aws_cloudwatch_event_bus.svenska_event_bus.name
  target_id      = "GDPRProcessor"
  arn           = aws_sfn_state_machine.svenska_workflow.arn
  role_arn      = aws_iam_role.eventbridge_role.arn
  
  input_transformer {
    input_paths = {
      dataSubjectId = "$.detail.dataSubjectId"
      requestType   = "$.detail.requestType"
      timestamp     = "$.time"
    }
    input_template = jsonencode({
      dataSubjectId    = "<dataSubjectId>"
      requestType      = "<requestType>"
      processingTime   = "<timestamp>"
      complianceMode   = "Swedish GDPR"
      environment      = var.environment
    })
  }
}
```

### Hybrid cloud pattern for Swedish enterprise organisations

Many Swedish organisations require hybrid cloud approaches that combine on-premises infrastructure with public cloud services to meet regulatory, performance, or legacy system requirements.

```terraform
# terraform/hybrid-cloud.tf
# Hybrid cloud infrastructure for Swedish enterprise organisations

# AWS Direct Connect for dedicated connectivity
resource "AWS Direct Connect connection" "Swedish_org_dx" {
  name            = "${var.organization_name}-dx-${var.environment}"
  bandwidth       = var.environment == "production" ? "10Gbps" : "1Gbps"
  location        = "Stockholm Interxion STO1"  # Swedish data centres
  provider_name   = "Interxion"
  
  tags = merge(local.common_tags, {
    ConnectionType = "Direct Connect"
    Location      = "Stockholm"
    Bandwidth     = var.environment == "production" ? "10Gbps" : "1Gbps"
  })
}

# Private virtual gateway for VPN connection
resource "AWS VPN Gateway" "Swedish_org_vgw" {
  vpc_id            = var.vpc_id
  availability_zone = var.primary_az
  
  tags = merge(local.common_tags, {
    Name = "${var.organization_name}-vgw-${var.environment}"
    Type = "VPN Gateway"
  })
}

# Customer gateway for on-site connectivity
resource "AWS Customer Gateway" "Swedish_org_cgw" {
  bgp_asn    = 65000
  ip_address = var.on_premises_public_ip
  type       = "ipsec.1"
  
  tags = merge(local.common_tags, {
    Name = "${var.organization_name}-cgw-${var.environment}"
    Location = "On-Premises Stockholm"
  })
}

# VPN between sites for secure hybrid connection
resource "AWS VPN Connection" "Swedish_org_VPN" {
  vpn_gateway_id      = aws_vpn_gateway.svenska_org_vgw.id
  customer_gateway_id = aws_customer_gateway.svenska_org_cgw.id
  type               = "ipsec.1"
  static_routes_only = false
  
  tags = merge(local.common_tags, {
    Name = "${var.organization_name}-vpn-${var.environment}"
    Type = "Site-to-Site VPN"
  })
}

# AWS Storage Gateway for hybrid storage
resource "AWS Storage Gateway Gateway" "swedish_org_storage_gw" {
  gateway_name   = "${var.organization_name}-storage-gw-${var.environment}"
  gateway_timezone = "GMT+1:00"  # Swedish hour
  gateway_type     = "FILE_S3"
  
  tags = merge(local.common_tags, {
    Name = "${var.organization_name}-storage-gateway"
    Type = "File-Gateway"
    Location = "Locally Hosted"
  })
}

# S3 bucket for hybrid file shares with Swedish data residency
resource "AWS S3 Bucket" "Hybrid File Share" {
  bucket = "${var.organization_name}-hybrid-files-${var.environment}"
  
  tags = merge(local.common_tags, {
    Purpose = "Hybrid File Share"
    DataResidency = "Sweden"
  })
}

resource "AWS S3 bucket server-side encryption configuration" "Hybrid Encryption" {
  bucket = aws_s3_bucket.hybrid_file_share.id
  
  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.svenska_org_key.arn
      sse_algorithm     = "AWS Key Management Service (KMS)"
    }
    bucket_key_enabled = true
  }
}

# AWS Database Migration Service for synchronizing hybrid data
resource "AWS DMS Replication Instance" "Swedish_org_dms" {
  replication_instance_class   = var.environment == "production" ? "dms.t3.large" : "dms.t3.micro"
  replication_instance_id     = "${var.organization_name}-dms-${var.environment}"
  
  allocated_storage            = var.environment == "production" ? 100 : 20
  apply_immediately           = var.environment != "production"
  auto_minor_version_upgrade  = true
  availability_zone           = var.primary_az
  engine_version              = "3.4.7"
  multi_az                    = var.environment == "production"
  publicly_accessible         = false
  replication_subnet_group_id = aws_dms_replication_subnet_group.svenska_org_dms_subnet.id
  vpc_security_group_ids      = [aws_security_group.dms_sg.id]
  
  tags = merge(local.common_tags, {
    Purpose = "Hybrid Data Migration"
  })
}

resource "AWS DMS Replication Subnet Group" "swedish_org_dms_subnet" {
  replication_subnet_group_description = "DMS subnet group for the Swedish organisation"
  replication_subnet_group_id          = "${var.organization_name}-dms-subnet-${var.environment}"
  subnet_ids                            = var.private_subnet_ids
  
  tags = local.common_tags
}

# AWS App Mesh for a hybrid service mesh
resource "AWS App Mesh Mesh" "Swedish_org_mesh" {
  name = "${var.organization_name}-mesh-${var.environment}"
  
  spec {
    egress_filter {
      type = "Allow all"
    }
  }
  
  tags = merge(local.common_tags, {
    MeshType = "Hybrid Service Mesh"
  })
}

# Route53 Resolver for hybrid DNS
resource "AWS Route 53 Resolver Endpoint" "arriving" {
  name      = "${var.organization_name}-resolver-inbound-${var.environment}"
  direction = "Arriving"
  
  security_group_ids = [aws_security_group.resolver_sg.id]
  
  dynamic "IP Address" {
    for_each = var.private_subnet_ids
    content {
      subnet_id = ip_address.value
    }
  }
  
  tags = merge(local.common_tags, {
    ResolverType = "Arriving"
    Purpose      = "Hybrid DNS"
  })
}

resource "AWS Route 53 Resolver Endpoint" "going out" {
  name      = "${var.organization_name}-resolver-outbound-${var.environment}"
  direction = "OUTBOUND"
  
  security_group_ids = [aws_security_group.resolver_sg.id]
  
  dynamic "IP Address" {
    for_each = var.private_subnet_ids
    content {
      subnet_id = ip_address.value
    }
  }
  
  tags = merge(local.common_tags, {
    ResolverType = "Outgoing"
    Purpose      = "Hybrid DNS"
  })
}

# Security Groups for hybrid connectivity
resource "AWS Security Group" "dms_sg" {
  name_prefix = "${var.organization_name}-dms-"
  description = "Security group for DMS replication instance"
  vpc_id      = var.vpc_id
  
  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = [var.on_premises_cidr]
    description = "All traffic originating from on-site"
  }
  
  egress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "All outgoing traffic"
  }
  
  tags = merge(local.common_tags, {
    Name = "${var.organization_name}-dms-sg"
  })
}

resource "AWS Security Group" "solve_sg" {
  name_prefix = "${var.organization_name}-resolver-"
  description = "Security group for Route53 Resolver endpoints"
  vpc_id      = var.vpc_id
  
  ingress {
    from_port   = 53
    to_port     = 53
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr, var.on_premises_cidr]
    description = "DNS TCP from VPC and on-premises"
  }
  
  ingress {
    from_port   = 53
    to_port     = 53
    protocol    = "udp"
    cidr_blocks = [var.vpc_cidr, var.on_premises_cidr]
    description = "DNS UDP from VPC and on-premises"
  }
  
  egress {
    from_port   = 53
    to_port     = 53
    protocol    = "tcp"
    cidr_blocks = [var.on_premises_cidr]
    description = "DNS TCP to on-premises"
  }
  
  egress {
    from_port   = 53
    to_port     = 53
    protocol    = "udp"
    cidr_blocks = [var.on_premises_cidr]
    description = "DNS UDP to on-premises"
  }
  
  tags = merge(local.common_tags, {
    Name = "${var.organization_name}-resolver-sg"
  })
}
```

## Multi-cloud strategies

Multi-cloud Infrastructure as Code strategies enable the distribution of workloads across multiple cloud providers to optimise cost, performance, and resilience. Provider-agnostic tools such as Terraform or Pulumi are used to abstract provider-specific differences and enable portability.

Hybrid cloud Architecture as Code implementations combine on-premises infrastructure with public cloud services through VPN connections, dedicated links, and edge computing. Consistent deployment and management processes across environments ensure operational efficiency and security compliance.

### Terraform for multi-cloud abstraction

Terraform forms the most mature solution for multi-cloud Infrastructure as Code through its comprehensive provider ecosystem. For Swedish organisations, Terraform enables unified management of AWS, Azure, Google Cloud, and on-premises resources through a consistent declarative syntax:

```hcl
# terraform/multi-cloud/main.tf
# Multi-cloud infrastructure designed for organisations in Sweden

terraform {
  required_version = "greater than or equal to 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.0"
    }
  }
  
  backend "s3" {
    bucket  = "swedish-org-terraform-state"
    key     = "multi-cloud/terraform.tfstate"
    region  = "eu-north-1"
    encrypt = true
  }
}

# AWS Provider for the Stockholm region
provider "aws" {
  region = "eu-north-1"
  alias  = "Stockholm"
  
  default_tags {
    tags = {
      Project         = var.project_name
      Environment     = var.environment
      Country         = "Sweden"
      DataResidency   = "Sweden"
      ManagedBy       = "Terraform"
      CostCenter      = var.cost_center
      GDPRCompliant   = "true"
    }
  }
}

# Azure Provider for Sweden Central
provider "azurerm" {
  features {
    key_vault {
      purge_soft_delete_on_destroy = false
    }
  }
  alias = "Sweden"
}

# Google Cloud Provider for Europe North 1
provider "google" {
  project = var.gcp_project_id
  region  = "europe-north1"
  alias   = "Finland"
}

# Local values for consistent naming across providers
locals {
  resource_prefix = "${var.organization_name}-${var.environment}"
  
  common_tags = {
    Project         = var.project_name
    Environment     = var.environment
    Organization    = var.organization_name
    Country         = "Sweden"
    DataResidency   = "Nordic"
    ManagedBy       = "Terraform"
    CostCenter      = var.cost_center
    GDPRCompliant   = "true"
    CreatedDate     = formatdate("YYYY-MM-DD", timestamp())
  }
  
  # Requirements for GDPR data storage location
  data_residency_requirements = {
    personal_data      = "Sweden"
    sensitive_data     = "Sweden"
    financial_data     = "Sweden"
    health_data        = "Sweden"
    operational_data   = "Nordic"
    public_data        = "Global"
  }
}

# AWS setup for main workloads
module "AWS infrastructure" {
  source = "./modules/aws"
  providers = {
    aws = aws.stockholm
  }
  
  organization_name    = var.organization_name
  environment         = var.environment
  resource_prefix     = local.resource_prefix
  common_tags         = local.common_tags
  
  # Configuration specific to AWS
  vpc_cidr           = var.aws_vpc_cidr
  availability_zones = var.aws_availability_zones
  enable_nat_gateway = var.environment == "production"
  enable_vpn_gateway = true
  
  # Data location and regulatory adherence
  data_classification      = var.data_classification
  compliance_requirements  = var.compliance_requirements
  backup_retention_days    = var.environment == "production" ? 90 : 30
  
  # Reducing expenses
  enable_spot_instances    = var.environment != "production"
  enable_scheduled_scaling = true
}

# Azure setup for disaster recovery
module "Azure infrastructure" {
  source = "./modules/azure"
  providers = {
    azurerm = azurerm.sweden
  }
  
  organization_name   = var.organization_name
  environment        = "${var.environment}-dr"
  resource_prefix    = "${local.resource_prefix}-dr"
  common_tags        = merge(local.common_tags, { Purpose = "Disaster Recovery" })
  
  # Configuration specific to Azure
  location                = "Central Sweden"
  vnet_address_space     = var.azure_vnet_cidr
  enable_ddos_protection = var.environment == "production"
  
  # Settings specific to DR
  enable_cross_region_backup = true
  backup_geo_redundancy     = "GRS"
  dr_automation_enabled     = var.environment == "production"
}

# Google Cloud for data analysis and machine learning tasks
module "GCP Infrastructure" {
  source = "./modules/gcp"
  providers = {
    google = google.finland
  }
  
  organization_name = var.organization_name
  environment      = "${var.environment}-analytics"
  resource_prefix  = "${local.resource_prefix}-analytics"
  common_labels    = {
    for k, v in local.common_tags : 
    lower(replace(k, "_", "-")) => lower(v)
  }
  
  # Configuration specific to GCP
  region                = "europe-north1"
  network_name         = "${local.resource_prefix}-analytics-vpc"
  enable_private_google_access = true
  
  # Features specific to analytics and machine learning
  enable_bigquery      = true
  enable_dataflow      = true
  enable_vertex_ai     = var.environment == "production"
  
  # Data governance for Swedish requirements
  enable_data_catalog  = true
  enable_dlp_api      = true
  data_residency_zone = "europe-north1"
}

# Networking across providers for hybrid connectivity
resource "AWS Customer Gateway" "Azure Gateway" {
  provider   = aws.stockholm
  bgp_asn    = 65515
  ip_address = module.azure_infrastructure.vpn_gateway_public_ip
  type       = "ipsec.1"
  
  tags = merge(local.common_tags, {
    Name = "${local.resource_prefix}-azure-cgw"
    Type = "Azure Connection"
  })
}

resource "AWS VPN Connection" "AWS to Azure connection" {
  provider            = aws.stockholm
  vpn_gateway_id      = module.aws_infrastructure.vpn_gateway_id
  customer_gateway_id = aws_customer_gateway.azure_gateway.id
  type               = "ipsec.1"
  static_routes_only = false
  
  tags = merge(local.common_tags, {
    Name = "${local.resource_prefix}-aws-azure-vpn"
    Connection = "AWS and Azure Hybrid"
  })
}

# Centralised services available on all cloud platforms
resource "Kubernetes namespace" "shared services" {
  count = length(var.kubernetes_clusters)
  
  metadata {
    name = "shared services"
    labels = merge(local.common_tags, {
      "app.kubernetes.io/managed-by" = "terraform"
      "svenska.se/shared-service"    = "true"
    })
  }
}

# Monitoring multiple cloud environments using Prometheus federation
resource "Kubernetes manifest" "Prometheus Federation" {
  count = length(var.kubernetes_clusters)
  
  manifest = {
    apiVersion = "v1"
    kind       = "ConfigMap"
    metadata = {
      name      = "Prometheus federation configuration"
      namespace = kubernetes_namespace.shared_services[count.index].metadata[0].name
    }
    data = {
      "prometheus.yml" = yamlencode({
        global = {
          scrape_interval = "15 seconds"
          external_labels = {
            cluster   = var.kubernetes_clusters[count.index].name
            region    = var.kubernetes_clusters[count.index].region
            provider  = var.kubernetes_clusters[count.index].provider
          }
        }
        
        scrape_configs = [
          {
            job_name = "federate"
            scrape_interval = "15 seconds"
            honor_labels = true
            metrics_path = "/federate"
            params = {
              "match[]" = [
                "{job=~\"kubernetes-.*\"}",
                "{__name__=~\"job:.*\"}",
                "{__name__=~\"svenska_org:.*\"}"
              ]
            }
            static_configs = var.kubernetes_clusters[count.index].prometheus_endpoints
          }
        ]
        
        rule_files = [
          "/etc/prometheus/rules/*.yml"
        ]
      })
    }
  }
}

# Cross-cloud DNS for discovering services
data "AWS Route 53 Zone" "main" {
  provider = aws.stockholm
  name     = var.dns_zone_name
}

resource "AWS Route 53 Record" "Azure Services" {
  provider = aws.stockholm
  count    = length(var.azure_service_endpoints)
  
  zone_id = data.aws_route53_zone.primary.zone_id
  name    = var.azure_service_endpoints[count.index].name
  type    = "CNAME"
  ttl     = 300
  records = [var.azure_service_endpoints[count.index].endpoint]
}

resource "AWS Route 53 Record" "GCP services" {
  provider = aws.stockholm
  count    = length(var.gcp_service_endpoints)
  
  zone_id = data.aws_route53_zone.primary.zone_id
  name    = var.gcp_service_endpoints[count.index].name
  type    = "CNAME"
  ttl     = 300
  records = [var.gcp_service_endpoints[count.index].endpoint]
}

# Synchronization of security groups across providers
data "outer" "Azure IP ranges" {
  program = ["python3", "${path.module}/scripts/get-azure-ip-ranges.py"]
  
  query = {
    subscription_id = var.azure_subscription_id
    resource_group  = module.azure_infrastructure.resource_group_name
  }
}

resource "AWS Security Group Rule" "Permit Azure traffic" {
  provider          = aws.stockholm
  count            = length(data.external.azure_ip_ranges.result.ip_ranges)
  
  type              = "entry"
  from_port         = 443
  to_port           = 443
  protocol          = "tcp"
  cidr_blocks       = [data.external.azure_ip_ranges.result.ip_ranges[count.index]]
  security_group_id = module.aws_infrastructure.app_security_group_id
  description       = "HTTPS from Azure ${count.index + 1}"
}

# Optimising expenses across multiple cloud platforms
resource "AWS Budgets Budget" "multi-cloud budget" {
  provider = aws.stockholm
  count    = var.environment == "production" ? 1 : 0
  
  name     = "${local.resource_prefix}-multi-cloud-budget"
  budget_type = "Cost"
  limit_amount = var.monthly_budget_limit
  limit_unit   = "USD"
  time_unit    = "Monthly"
  
  cost_filters {
    tag = {
      Project = [var.project_name]
    }
  }
  
  notification {
    comparison_operator        = "Greater Than"
    threshold                 = 80
    threshold_type            = "Percentage"
    notification_type         = "ACTUAL"
    subscriber_email_addresses = var.budget_notification_emails
  }
  
  notification {
    comparison_operator        = "Greater Than"
    threshold                 = 100
    threshold_type            = "Percentage"
    notification_type          = "Predicted"
    subscriber_email_addresses = var.budget_notification_emails
  }
}

# Strategy for backing up data across multiple cloud services
resource "AWS S3 Bucket" "cross-cloud backup" {
  provider = aws.stockholm
  bucket   = "${local.resource_prefix}-cross-cloud-backup"
  
  tags = merge(local.common_tags, {
    Purpose = "Backup Across Multiple Clouds"
  })
}

resource "AWS S3 Bucket Replication Configuration" "cross-region replication" {
  provider   = aws.stockholm
  depends_on = [aws_s3_bucket_versioning.backup_versioning]
  
  role   = aws_iam_role.replication_role.arn
  bucket = aws_s3_bucket.cross_cloud_backup.id
  
  rule {
    id     = "replication across regions"
    status = "Enabled"
    
    destination {
      bucket        = "arn:aws:s3:::${local.resource_prefix}-cross-cloud-backup-replica"
      storage_class = "Standard Infrequent Access"
      
      encryption_configuration {
        replica_kms_key_id = aws_kms_key.backup_key.arn
      }
    }
  }
}

# Results for integration across different providers
output "AWS VPC ID" {
  description = "AWS VPC Identifier for cross-provider networking"
  value       = module.aws_infrastructure.vpc_id
}

output "Azure Virtual Network ID" {
  description = "Azure VNet Identifier for cross-provider networking"
  value       = module.azure_infrastructure.vnet_id
}

output "GCP Network ID" {
  description = "GCP VPC Network Identifier for cross-provider networking"
  value       = module.gcp_infrastructure.network_id
}

output "multi-cloud endpoints" {
  description = "Service endpoints across all cloud providers"
  value = {
    aws_api_endpoint   = module.aws_infrastructure.api_gateway_endpoint
    azure_app_url      = module.azure_infrastructure.app_service_url
    gcp_analytics_url  = module.gcp_infrastructure.analytics_endpoint
  }
}

output "compliance status" {
  description = "Status of compliance across all cloud providers"
  value = {
    aws_gdpr_compliant   = module.aws_infrastructure.gdpr_compliant
    azure_gdpr_compliant = module.azure_infrastructure.gdpr_compliant
    gcp_gdpr_compliant   = module.gcp_infrastructure.gdpr_compliant
    data_residency_zones = local.data_residency_requirements
    cross_cloud_backup   = aws_s3_bucket.cross_cloud_backup.arn
  }
}
```

### Pulumi for programmatic multi-cloud Infrastructure as Code

The Architecture as Code principles within this area

Pulumi offers an alternative approach to multi-cloud Architecture as Code by enabling the use of common programming languages such as TypeScript, Python, Go, and C#. For Swedish development teams who prefer a programmatic approach over declarative configuration:

```typescript
// pulumi/multi-cloud/index.ts
// Using Pulumi for multi-cloud infrastructure in Swedish organisations

import * as aws from "@pulumi/aws";
import * as azure from "@pulumi/azure-native";
import * as gcp from "@pulumi/gcp";
import * as kubernetes from "@pulumi/kubernetes";
import * as pulumi from "@pulumi/pulumi";

// Configuration for Swedish organisations
const config = new pulumi.Config();
const organizationName = config.require("organizationName");
const environment = config.require("environment");
const dataClassification = config.get("data classification") || "internal";
const complianceRequirements = config.getObject<string[]>("regulatory obligations") || ["General Data Protection Regulation"];

// Common Swedish tags/labels for all providers
const swedishTags = {
    Organization: organizationName,
    Environment: environment,
    Country: "Sweden",
    DataResidency: "Nordic",
    GDPRCompliant: "true",
    ManagedBy: "Pulumi",
    CostCenter: config.require("Cost Centre"),
    CreatedDate: new Date().toISOString().split('T')[0]
};

// Provider configurations for Swedish regions
const awsProvider = new aws.Provider("aws-stockholm", {
    region: "eu-north-1",
    defaultTags: {
        tags: swedishTags
    }
});

const azureProvider = new azure.Provider("azure Sweden", {
    location: "Central Sweden"
});

const gcpProvider = new gcp.Provider("GCP Finland", {
    project: config.require("gcpProjectId"),
    region: "europe-north1"
});

// AWS setup for main workloads
class AWSInfrastructure extends pulumi.ComponentResource {
    public readonly vpc: aws.ec2.Vpc;
    public readonly subnets: aws.ec2.Subnet[];
    public readonly database: aws.rds.Instance;
    public readonly apiGateway: aws.apigateway.RestApi;
    
    constructor(name: string, args: any, opts?: pulumi.ComponentResourceOptions) {
        super("Swedish: aws: Infrastructure", name, {}, opts);
        
        // VPC with Swedish security requirements
        this.vpc = new aws.ec2.Vpc(`${name}-vpc`, {
            cidrBlock: environment === "production" ? "10.0.0.0/16" : "10.1.0.0/16",
            enableDnsHostnames: true,
            enableDnsSupport: true,
            tags: {
                Name: `${organizationName}-${environment}-vpc`,
                Purpose: "Main Infrastructure"
            }
        }, { provider: awsProvider, parent: this });
        
        // Private subnets for Swedish data residency
        this.subnets = [];
        const azs = aws.getAvailabilityZones({
            state: "available"
        }, { provider: awsProvider });
        
        azs.then(zones => {
            zones.names.slice(0, 2).forEach((az, index) => {
                const subnet = new aws.ec2.Subnet(`${name}-private-subnet-${index}`, {
                    vpcId: this.vpc.id,
                    cidrBlock: environment === "production" ? 
                        `10.0.${index + 1}.0/24` : 
                        `10.1.${index + 1}.0/24`,
                    availabilityZone: az,
                    mapPublicIpOnLaunch: false,
                    tags: {
                        Name: `${organizationName}-private-subnet-${index}`,
                        Type: "Private",
                        DataResidency: "Sweden"
                    }
                }, { provider: awsProvider, parent: this });
                
                this.subnets.push(subnet);
            });
        });
        
        // RDS PostgreSQL for Swedish GDPR requirements
        const dbSubnetGroup = new aws.rds.SubnetGroup(`${name}-db-subnet-group`, {
            subnetIds: this.subnets.map(s => s.id),
            tags: {
                Name: `${organizationName}-db-subnet-group`,
                Purpose: "Database GDPR Compliance"
            }
        }, { provider: awsProvider, parent: this });
        
        this.database = new aws.rds.Instance(`${name}-postgres`, {
            engine: "Postgres",
            engineVersion: "15.4",
            instanceClass: environment === "production" ? "db.r5.large" : "db.t3.micro",
            allocatedStorage: environment === "production" ? 100 : 20,
            storageEncrypted: true,
            dbSubnetGroupName: dbSubnetGroup.name,
            backupRetentionPeriod: environment === "production" ? 30 : 7,
            backupWindow: "03:00-04:00",  // Swedish at night
            maintenanceWindow: "Saturday 4:00 AM to Saturday 5:00 AM",  // Saturday night Swedish time
            deletionProtection: environment === "production",
            enabledCloudwatchLogsExports: ["PostgreSQL"],
            tags: {
                Name: `${organizationName}-postgres`,
                DataType: "Personal Data",
                GDPRCompliant: "true",
                BackupStrategy: environment === "production" ? "30 days" : "7 days"
            }
        }, { provider: awsProvider, parent: this });
        
        // API Gateway with Swedish security requirements
        this.apiGateway = new aws.apigateway.RestApi(`${name}-api`, {
            name: `${organizationName}-api-${environment}`,
            description: "API Gateway for the Swedish organisation with GDPR compliance",
            endpointConfiguration: {
                types: "REGIONAL"
            },
            policy: JSON.stringify({
                Version: "October 17, 2012",
                Statement: [{
                    Effect: "Permit",
                    Principal: "*",
                    Action: "execute API: Invoke",
                    Resource: "*",
                    Condition: {
                        IpAddress: {
                            "AWS source IP": args.allowedIpRanges || ["0.0.0.0/0"]
                        }
                    }
                }]
            })
        }, { provider: awsProvider, parent: this });
        
        this.registerOutputs({
            vpcId: this.vpc.id,
            subnetIds: this.subnets.map(s => s.id),
            databaseEndpoint: this.database.endpoint,
            apiGatewayUrl: this.apiGateway.executionArn
        });
    }
}

// Azure setup for disaster recovery
class AzureInfrastructure extends pulumi.ComponentResource {
    public readonly resourceGroup: azure.resources.ResourceGroup;
    public readonly vnet: azure.network.VirtualNetwork;
    public readonly sqlServer: azure.sql.Server;
    public readonly appService: azure.web.WebApp;
    
    constructor(name: string, args: any, opts?: pulumi.ComponentResourceOptions) {
        super("Swedish: Azure: Infrastructure", name, {}, opts);
        
        // Resource Group for Swedish DR Environment
        this.resourceGroup = new azure.resources.ResourceGroup(`${name}-rg`, {
            resourceGroupName: `${organizationName}-${environment}-dr-rg`,
            location: "Central Sweden",
            tags: {
                ...swedishTags,
                Purpose: "Disaster Recovery"
            }
        }, { provider: azureProvider, parent: this });
        
        // Virtual Network for Swedish data residency
        this.vnet = new azure.network.VirtualNetwork(`${name}-vnet`, {
            virtualNetworkName: `${organizationName}-${environment}-dr-vnet`,
            resourceGroupName: this.resourceGroup.name,
            location: this.resourceGroup.location,
            addressSpace: {
                addressPrefixes: [environment === "production" ? "172.16.0.0/16" : "172.17.0.0/16"]
            },
            subnets: [
                {
                    name: "application subnet",
                    addressPrefix: environment === "production" ? "172.16.1.0/24" : "172.17.1.0/24",
                    serviceEndpoints: [
                        { service: "Microsoft SQL", locations: ["Central Sweden"] },
                        { service: "Microsoft Storage", locations: ["Central Sweden"] }
                    ]
                },
                {
                    name: "database subnet",
                    addressPrefix: environment === "production" ? "172.16.2.0/24" : "172.17.2.0/24",
                    delegations: [{
                        name: "Microsoft SQL Managed Instances",
                        serviceName: "Microsoft SQL Managed Instances"
                    }]
                }
            ],
            tags: {
                ...swedishTags,
                NetworkType: "Disaster Recovery"
            }
        }, { provider: azureProvider, parent: this });
        
        // SQL Server for GDPR-compliant data backup
        this.sqlServer = new azure.sql.Server(`${name}-sql`, {
            serverName: `${organizationName}-${environment}-dr-sql`,
            resourceGroupName: this.resourceGroup.name,
            location: this.resourceGroup.location,
            administratorLogin: "sqladmin",
            administratorLoginPassword: args.sqlAdminPassword,
            version: "12.0",
            minimalTlsVersion: "1.2",
            tags: {
                ...swedishTags,
                DatabaseType: "Disaster Recovery",
                DataResidency: "Sweden"
            }
        }, { provider: azureProvider, parent: this });
        
        // App Service for Swedish applications
        const appServicePlan = new azure.web.AppServicePlan(`${name}-asp`, {
            name: `${organizationName}-${environment}-dr-asp`,
            resourceGroupName: this.resourceGroup.name,
            location: this.resourceGroup.location,
            sku: {
                name: environment === "production" ? "P1v2" : "B1",
                tier: environment === "production" ? "PremiumV2" : "Basic"
            },
            tags: swedishTags
        }, { provider: azureProvider, parent: this });
        
        this.appService = new azure.web.WebApp(`${name}-app`, {
            name: `${organizationName}-${environment}-dr-app`,
            resourceGroupName: this.resourceGroup.name,
            location: this.resourceGroup.location,
            serverFarmId: appServicePlan.id,
            siteConfig: {
                alwaysOn: environment === "production",
                ftpsState: "Not enabled",
                minTlsVersion: "1.2",
                http20Enabled: true,
                appSettings: [
                    { name: "ENVIRONMENT", value: `${environment}-dr` },
                    { name: "Data Classification", value: dataClassification },
                    { name: "GDPR Enabled", value: "true" },
                    { name: "Sweden Time Zone", value: "Europe/Stockholm" },
                    { name: "Compliance Mode", value: "Swedish GDPR" }
                ]
            },
            tags: {
                ...swedishTags,
                AppType: "Disaster Recovery"
            }
        }, { provider: azureProvider, parent: this });
        
        this.registerOutputs({
            resourceGroupName: this.resourceGroup.name,
            vnetId: this.vnet.id,
            sqlServerName: this.sqlServer.name,
            appServiceUrl: this.appService.defaultHostName.apply(hostname => `https:// ${hostname}`)
        });
    }
}

// Google Cloud platform for data analytics
class GCPInfrastructure extends pulumi.ComponentResource {
    public readonly network: gcp.compute.Network;
    public readonly bigQueryDataset: gcp.bigquery.Dataset;
    public readonly cloudFunction: gcp.cloudfunctions.Function;
    
    constructor(name: string, args: any, opts?: pulumi.ComponentResourceOptions) {
        super("Swedish:GCP:Infrastructure", name, {}, opts);
        
        // VPC Network for Swedish analytics
        this.network = new gcp.compute.Network(`${name}-network`, {
            name: `${organizationName}-${environment}-analytics-vpc`,
            description: "VPC for Swedish analytics and ML workloads",
            autoCreateSubnetworks: false
        }, { provider: gcpProvider, parent: this });
        
        // Subnet for Swedish data residency
        const analyticsSubnet = new gcp.compute.Subnetwork(`${name}-analytics-subnet`, {
            name: `${organizationName}-analytics-subnet`,
            ipCidrRange: "10.2.0.0/24",
            region: "europe-north1",
            network: this.network.id,
            enableFlowLogs: true,
            logConfig: {
                enable: true,
                flowSampling: 1.0,
                aggregationInterval: "5-Second Interval",
                metadata: "Include all metadata"
            },
            secondaryIpRanges: [
                {
                    rangeName: "pods",
                    ipCidrRange: "10.3.0.0/16"
                },
                {
                    rangeName: "services", 
                    ipCidrRange: "10.4.0.0/20"
                }
            ]
        }, { provider: gcpProvider, parent: this });
        
        // BigQuery Dataset for Swedish data analytics
        this.bigQueryDataset = new gcp.bigquery.Dataset(`${name}-analytics-dataset`, {
            datasetId: `${organizationName}_${environment}_analytics`,
            friendlyName: `Svenska ${organizationName} Analytics Dataset`,
            description: "Analytics dataset for the Swedish organisation with GDPR compliance",
            location: "europe-north1",
            defaultTableExpirationMs: environment === "production" ? 
                7 * 24 * 60 * 60 * 1000 : // 7 days for production
                24 * 60 * 60 * 1000,      // 1 day for development/staging
            
            access: [
                {
                    role: "Owner",
                    userByEmail: args.dataOwnerEmail
                },
                {
                    role: "READER", 
                    specialGroup: "project readers"
                }
            ],
            
            labels: {
                organization: organizationName.toLowerCase(),
                environment: environment,
                country: "Sweden",
                gdpr_compliant: "true",
                data_residency: "Nordic"
            }
        }, { provider: gcpProvider, parent: this });
        
        // Cloud Function for Swedish GDPR data processing
        const functionSourceBucket = new gcp.storage.Bucket(`${name}-function-source`, {
            name: `${organizationName}-${environment}-function-source`,
            location: "EUROPE-NORTH1",
            uniformBucketLevelAccess: true,
            labels: {
                purpose: "cloud function source",
                data_residency: "Sweden"
            }
        }, { provider: gcpProvider, parent: this });
        
        const functionSourceObject = new gcp.storage.BucketObject(`${name}-function-zip`, {
            name: "swedish-gdpr-processor.zip",
            bucket: functionSourceBucket.name,
            source: new pulumi.asset.FileAsset("./functions/swedish-gdpr-processor.zip")
        }, { provider: gcpProvider, parent: this });
        
        this.cloudFunction = new gcp.cloudfunctions.Function(`${name}-gdpr-processor`, {
            name: `${organizationName}-gdpr-processor-${environment}`,
            description: "GDPR data processing function for the Swedish organisation",
            runtime: "Node.js 18",
            availableMemoryMb: 256,
            timeout: 60,
            entryPoint: "Handle GDPR Request",
            region: "europe-north1",
            
            sourceArchiveBucket: functionSourceBucket.name,
            sourceArchiveObject: functionSourceObject.name,
            
            httpsTrigger: {},
            
            environmentVariables: {
                ENVIRONMENT: environment,
                DATA_CLASSIFICATION: dataClassification,
                GDPR_ENABLED: "true",
                SWEDISH_TIMEZONE: "Europe/Stockholm",
                BIGQUERY_DATASET: this.bigQueryDataset.datasetId,
                COMPLIANCE_MODE: "Swedish GDPR"
            },
            
            labels: {
                organization: organizationName.toLowerCase(),
                environment: environment,
                function_type: "GDPR processor",
                data_residency: "Sweden"
            }
        }, { provider: gcpProvider, parent: this });
        
        this.registerOutputs({
            networkId: this.network.id,
            bigQueryDatasetId: this.bigQueryDataset.datasetId,
            cloudFunctionUrl: this.cloudFunction.httpsTriggerUrl
        });
    }
}

// Primary multi-cloud deployment
const awsInfra = new AWSInfrastructure("aws-primary", {
    allowedIpRanges: config.getObject<string[]>("allowedIpRanges") || ["0.0.0.0/0"]
});

const azureInfra = new AzureInfrastructure("Azure DR", {
    sqlAdminPassword: config.requireSecret("SQL Admin Password")
});

const gcpInfra = new GCPInfrastructure("GCP Analytics", {
    dataOwnerEmail: config.require("data owner email")
});

// Setup for monitoring across multiple cloud platforms
const crossCloudMonitoring = new kubernetes.core.v1.Namespace("cross-cloud monitoring", {
    metadata: {
        name: "observing",
        labels: {
            "app.kubernetes.io/managed-by": "pulumi",
            "svenska.se/monitoring-type": "cross-cloud"
        }
    }
});

// Export important results for integration across different providers
export const multiCloudEndpoints = {
    aws: {
        apiGatewayUrl: awsInfra.apiGateway.executionArn,
        vpcId: awsInfra.vpc.id
    },
    azure: {
        appServiceUrl: azureInfra.appService.defaultHostName.apply(hostname => `https:// ${hostname}`),
        resourceGroupName: azureInfra.resourceGroup.name
    },
    gcp: {
        analyticsUrl: gcpInfra.cloudFunction.httpsTriggerUrl,
        networkId: gcpInfra.network.id
    }
};

export const complianceStatus = {
    gdprCompliant: true,
    dataResidencyZones: {
        aws: "eu-north-1 (Stockholm)",
        azure: "Central Sweden",
        gcp: "Europe-North1 (Finland)"
    },
    encryptionEnabled: true,
    auditLoggingEnabled: true,
    crossCloudBackupEnabled: true
};
```

## Serverless infrastructure

Serverless Infrastructure as Code focuses on function definitions, event triggers, and managed service configurations instead of traditional server management. This approach reduces operational overhead and enables automatic scaling based on actual usage patterns.

Event-driven architectures are implemented through cloud functions, message queues, and data streams defined as Architecture as Code. Integration between services is managed through IAM policies, API definitions, and network configurations that ensure security and performance requirements.

### Function-as-a-Service (FaaS) patterns for Swedish organisations

Serverless functions form the core of modern cloud-native architecture and enable unprecedented scalability and cost efficiency. For Swedish organisations, this means that FaaS patterns in infrastructure definitions focus on business logic instead of the underlying compute resources.

```yaml
# serverless.yml
# Serverless Framework for organisations in Sweden

service: svenska-org-serverless
frameworkVersion: 'three'

provider:
  name: aws
  runtime: nodejs18.x
  region: eu-north-1  # Stockholm region for Swedish data residency
  stage: ${opt:stage, 'development'}
  memorySize: 256
  timeout: 30
  
  # Swedish environment variables
  environment:
    STAGE: ${self:provider.stage}
    REGION: ${self:provider.region}
    DATA_CLASSIFICATION: ${env:DATA_CLASSIFICATION, 'internal'}
    GDPR_ENABLED: true
    SWEDISH_TIMEZONE: Europe/Stockholm
    COST_CENTER: ${env:COST_CENTER}
    ORGANIZATION: ${env:ORGANIZATION_NAME}
    COMPLIANCE_REQUIREMENTS: ${env:COMPLIANCE_REQUIREMENTS, 'General Data Protection Regulation'}
  
  # IAM Roles for Swedish security requirements
  iam:
    role:
      statements:
        - Effect: Allow
          Action:
            - logs:CreateLogGroup
            - logs:CreateLogStream
            - logs:PutLogEvents
          Resource: 
            - arn:aws:logs:${self:provider.region}:*:*
        - Effect: Allow
          Action:
            - dynamodb:Query
            - dynamodb:Scan
            - dynamodb:GetItem
            - dynamodb:PutItem
            - dynamodb:UpdateItem
            - dynamodb:DeleteItem
          Resource:
            - arn:aws:dynamodb:${self:provider.region}:*:table/${self:service}-${self:provider.stage}-*
        - Effect: Allow
          Action:
            - kms:Decrypt
            - kms:Encrypt
            - kms:GenerateDataKey
          Resource:
            - arn:aws:kms:${self:provider.region}:*:key/*
          Condition:
            StringEquals:
              'kms:ViaService': 
                - dynamodb.${self:provider.region}.amazonaws.com
                - s3.${self:provider.region}.amazonaws.com
  
  # VPC setup for Swedish security requirements
  vpc:
    securityGroupIds:
      - ${env:SECURITY_GROUP_ID}
    subnetIds:
      - ${env:PRIVATE_SUBNET_1_ID}
      - ${env:PRIVATE_SUBNET_2_ID}
  
  # CloudWatch Logs in accordance with GDPR compliance
  logs:
    restApi: true
    frameworkLambda: true
  
  # Tracing for Swedish monitoring
  tracing:
    lambda: true
    apiGateway: true
  
  # Tags for Swedish governance
  tags:
    Organization: ${env:ORGANIZATION_NAME}
    Environment: ${self:provider.stage}
    Country: Sweden
    DataResidency: Sweden
    GDPRCompliant: true
    ManagedBy: Serverless-Framework
    CostCenter: ${env:COST_CENTER}
    CreatedDate: ${env:DEPLOY_DATE}

# Swedish serverless functions
functions:
  # GDPR Data Subject Rights API
  gdprDataSubjectAPI:
    handler: src/handlers/gdpr.dataSubjectRequestHandler
    description: GDPR data subject rights API for svenska organisationen
    memorySize: 512
    timeout: 60
    reservedConcurrency: 50
    environment:
      GDPR_TABLE_NAME: ${self:service}-${self:provider.stage}-gdpr-requests
      AUDIT_TABLE_NAME: ${self:service}-${self:provider.stage}-audit-log
      ENCRYPTION_KEY_ARN: ${env:GDPR_KMS_KEY_ARN}
      DATA_RETENTION_DAYS: ${env:DATA_RETENTION_DAYS, 'ninety'}
    events:
      - http:
          path: /gdpr/data-subject-request
          method: post
          cors:
            origin: ${env:ALLOWED_ORIGINS, '*'}
            headers:
              - Content-Type
              - X-Amz-Date
              - Authorization
              - X-Api-Key
              - X-Amz-Security-Token
              - X-Amz-User-Agent
              - X-Swedish-Org-Token
          authorizer:
            name: gdprAuthorizer
            type: COGNITO_USER_POOLS
            arn: ${env:COGNITO_USER_POOL_ARN}
          request:
            schemas:
              application/json: ${file(schemas/gdpr-request.json)}
    tags:
      Function: GDPR-Data-Subject-Rights
      DataType: Personal-Data
      ComplianceLevel: Critical

  # Swedish audit logging function
  auditLogger:
    handler: src/handlers/audit.logEventHandler
    description: Audit logging for svenska compliance-requirements
    memorySize: 256
    timeout: 30
    environment:
      AUDIT_TABLE_NAME: ${self:service}-${self:provider.stage}-audit-log
      LOG_RETENTION_YEARS: ${env:LOG_RETENTION_YEARS, 'seven'}
      SWEDISH_LOCALE: sv_SE.UTF-8
    events:
      - stream:
          type: dynamodb
          arn:
            Fn::GetAtt: [GdprRequestsTable, StreamArn]
          batchSize: 10
          startingPosition: LATEST
          maximumBatchingWindowInSeconds: 5
    deadLetter:
      targetArn: 
        Fn::GetAtt: [AuditDLQ, Arn]
    tags:
      Function: Audit-Logging
      RetentionPeriod: 7-years
      ComplianceType: Swedish-Requirements

  # Cost control for Swedish organisations
  costMonitoring:
    handler: src/handlers/cost.monitoringHandler
    description: Kostnadskontroll and budgetvarningar for Swedish organizations
    memorySize: 256
    timeout: 120
    environment:
      BUDGET_TABLE_NAME: ${self:service}-${self:provider.stage}-budgets
      NOTIFICATION_TOPIC_ARN: ${env:COST_NOTIFICATION_TOPIC_ARN}
      SWEDISH_CURRENCY: SEK
      COST_ALLOCATION_TAGS: Environment,CostCenter,Organization
    events:
      - schedule:
          rate: cron(0 8 * * ? *)  # 08:00 Swedish time every day
          description: Daglig kostnadskontroll for svenska organisationen
          input:
            checkType: daily
            currency: SEK
            timezone: Europe/Stockholm
      - schedule:
          rate: cron(0 8 ? * MON *)  # 08:00 Mondays for weekly report
          description: Veckovis kostnadskontroll
          input:
            checkType: weekly
            generateReport: true
    tags:
      Function: Cost-Monitoring
      Schedule: Daily-Weekly
      Currency: SEK

  # Swedish data processing pipeline
  dataProcessor:
    handler: src/handlers/data.processingHandler
    description: Data processing pipeline for Swedish organizations
    memorySize: 1024
    timeout: 900  # 15 minutes for batch processing
    reservedConcurrency: 10
    environment:
      DATA_BUCKET_NAME: ${env:DATA_BUCKET_NAME}
      PROCESSED_BUCKET_NAME: ${env:PROCESSED_BUCKET_NAME}
      ENCRYPTION_KEY_ARN: ${env:DATA_ENCRYPTION_KEY_ARN}
      GDPR_ANONYMIZATION_ENABLED: true
      SWEDISH_DATA_RESIDENCY: true
    events:
      - s3:
          bucket: ${env:DATA_BUCKET_NAME}
          event: s3:ObjectCreated:*
          rules:
            - prefix: incoming/
            - suffix: .json
    layers:
      - ${env:PANDAS_LAYER_ARN}  # Libraries for processing data
    tags:
      Function: Data-Processing
      DataType: Batch-Processing
      AnonymizationEnabled: true

# Swedish DynamoDB tables
resources:
  Resources:
    # Table of GDPR requests
    GdprRequestsTable:
      Type: AWS::DynamoDB::Table
      Properties:
        TableName: ${self:service}-${self:provider.stage}-gdpr-requests
        BillingMode: PAY_PER_REQUEST
        AttributeDefinitions:
          - AttributeName: requestId
            AttributeType: S
          - AttributeName: dataSubjectId
            AttributeType: S
          - AttributeName: createdAt
            AttributeType: S
        KeySchema:
          - AttributeName: requestId
            KeyType: HASH
        GlobalSecondaryIndexes:
          - IndexName: DataSubjectIndex
            KeySchema:
              - AttributeName: dataSubjectId
                KeyType: HASH
              - AttributeName: createdAt
                KeyType: RANGE
            Projection:
              ProjectionType: ALL
        StreamSpecification:
          StreamViewType: NEW_AND_OLD_IMAGES
        PointInTimeRecoverySpecification:
          PointInTimeRecoveryEnabled: ${self:provider.stage, 'production', true, false}
        SSESpecification:
          SSEEnabled: true
          KMSMasterKeyId: ${env:GDPR_KMS_KEY_ARN}
        TimeToLiveSpecification:
          AttributeName: ttl
          Enabled: true
        Tags:
          - Key: Purpose
            Value: GDPR-Data-Subject-Requests
          - Key: DataType
            Value: Personal-Data
          - Key: Retention
            Value: ${env:DATA_RETENTION_DAYS, 'ninety'}-days
          - Key: Country
            Value: Sweden

    # Audit log table for Swedish compliance
    AuditLogTable:
      Type: AWS::DynamoDB::Table
      Properties:
        TableName: ${self:service}-${self:provider.stage}-audit-log
        BillingMode: PAY_PER_REQUEST
        AttributeDefinitions:
          - AttributeName: eventId
            AttributeType: S
          - AttributeName: timestamp
            AttributeType: S
          - AttributeName: userId
            AttributeType: S
        KeySchema:
          - AttributeName: eventId
            KeyType: HASH
          - AttributeName: timestamp
            KeyType: RANGE
        GlobalSecondaryIndexes:
          - IndexName: UserAuditIndex
            KeySchema:
              - AttributeName: userId
                KeyType: HASH
              - AttributeName: timestamp
                KeyType: RANGE
            Projection:
              ProjectionType: ALL
        PointInTimeRecoverySpecification:
          PointInTimeRecoveryEnabled: true
        SSESpecification:
          SSEEnabled: true
          KMSMasterKeyId: ${env:AUDIT_KMS_KEY_ARN}
        Tags:
          - Key: Purpose
            Value: Compliance-Audit-Logging
          - Key: Retention
            Value: 7-years
          - Key: ComplianceType
            Value: Swedish-Requirements

    # Dead Letter Queue for Swedish error handling
    AuditDLQ:
      Type: AWS::SQS::Queue
      Properties:
        QueueName: ${self:service}-${self:provider.stage}-audit-dlq
        MessageRetentionPeriod: 1209600  # 14 days
        KmsMasterKeyId: ${env:AUDIT_KMS_KEY_ARN}
        Tags:
          - Key: Purpose
            Value: Dead-Letter-Queue
          - Key: Component
            Value: Audit-systems

    # CloudWatch Dashboard for Swedish monitoring
    ServerlessMonitoringDashboard:
      Type: AWS::CloudWatch::Dashboard
      Properties:
        DashboardName: ${self:service}-${self:provider.stage}-svenska-monitoring
        DashboardBody: 
          Fn::Sub: |
            {
              "widgets": [
                {
                  "type": "metric",
                  "x": 0,
                  "y": 0,
                  "width": 12,
                  "height": 6,
                  "properties": {
                    "metrics": [
                      [ "AWS Lambda", "Invocations", "FunctionName", "${GdprDataSubjectAPILambdaFunction}" ],
                      [ ".", "Mistakes", ".", "." ],
                      [ ".", "Length of time", ".", "." ]
                    ],
                    "view": "time series",
                    "piled": false,
                    "area": "${AWS::Region}",
                    "title": "GDPR Function Metrics",
                    "period": 300
                  }
                },
                {
                  "type": "metric", 
                  "x": 0,
                  "y": 6,
                  "width": 12,
                  "height": 6,
                  "properties": {
                    "metrics": [
                      [ "AWS/DynamoDB", "Consumed Read Capacity Units", "TableName", "${GdprRequestsTable}" ],
                      [ ".", "Consumed Write Capacity Units", ".", "." ]
                    ],
                    "view": "time series",
                    "piled": false,
                    "area": "${AWS::Region}",
                    "title": "GDPR Table Capacity",
                    "period": 300
                  }
                }
              ]
            }

  Outputs:
    GdprApiEndpoint:
      Description: GDPR API endpoint for svenska data subject requests
      Value:
        Fn::Join:
          - ''
          - - https://
            - Ref: RestApiApigEvent
            - .execute-api.
            - ${self:provider.region}
            - .amazonaws.com/
            - ${self:provider.stage}
            - /gdpr/data-subject-request
      Export:
        Name: ${self:service}-${self:provider.stage}-gdpr-api-endpoint

    ComplianceStatus:
      Description: Compliance status for serverless infrastructure
      Value:
        Fn::Sub: |
          {
            "GDPR Compliant": true,
            "data residency": "Sweden",
            "Audit logging is enabled": true,
            "Encryption Enabled": true,
            "Retention Policies": {
              "GDPR Data": "${env:DATA_RETENTION_DAYS, '90'} days",
              "audit logs": "7 years"
            }
          }

# Swedish plugins for extended functionality
plugins:
  - serverless-webpack
  - serverless-offline
  - serverless-domain-manager
  - serverless-prune-plugin
  - serverless-plugin-tracing
  - serverless-plugin-aws-alerts

# Custom setup for Swedish organisations
custom:
  # Webpack for creating optimised bundles
  webpack:
    webpackConfig: 'webpack.config.js'
    includeModules: true
    packager: 'npm'
    excludeFiles: src/**/*.test.js

  # Domain management for Swedish domains
  customDomain:
    domainName: ${env:CUSTOM_DOMAIN_NAME, ''}
    stage: ${self:provider.stage}
    certificateName: ${env:SSL_CERTIFICATE_NAME, ''}
    createRoute53Record: true
    endpointType: 'regional'
    securityPolicy: tls_1_2
    apiType: rest

  # Automated trimming to reduce costs
  prune:
    automatic: true
    number: 5  # Keep the last 5 versions

  # CloudWatch alerts for Svenska monitoring
  alerts:
    stages:
      - production
      - staging
    topics:
      alarm: ${env:ALARM_TOPIC_ARN}
    definitions:
      functionErrors:
        metric: errors
        threshold: 5
        statistic: Sum
        period: 300
        evaluationPeriods: 2
        comparisonOperator: GreaterThanThreshold
        treatMissingData: notBreaching
      functionDuration:
        metric: duration
        threshold: 10000  # 10 seconds
        statistic: Average
        period: 300
        evaluationPeriods: 2
        comparisonOperator: GreaterThanThreshold
    alarms:
      - functionErrors
      - functionDuration
```

### Event-driven architecture for Swedish organisations

Event-driven architectures form the foundation for modern serverless systems and enable loose coupling between services. For Swedish organisations, this means a particular focus on GDPR-compliant event processing and audit trails:

```python
# serverless/event_processing.py
# GDPR-compliant event-driven architecture for organisations in Sweden

import json
import boto3
import logging
import os
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

# Configuration for Swedish organisations
SWEDISH_TIMEZONE = 'Europe/Stockholm'
ORGANIZATION_NAME = os.environ.get('ORGANIZATION_NAME', 'Swedish organisation')
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'development')
GDPR_ENABLED = os.environ.get('GDPR Enabled', 'true').lower() == 'true'
DATA_CLASSIFICATION = os.environ.get('Data Classification', 'internal')

# AWS clients with Swedish configuration
dynamodb = boto3.resource('DynamoDB', region_name='eu-north-1')
sns = boto3.client('etc.', region_name='eu-north-1')
sqs = boto3.client('sqs', region_name='eu-north-1')
s3 = boto3.client('s3', region_name='eu-north-1')

# Logging configuration for Swedish compliance
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class EventType(Enum):
    """Swedish event types for GDPR compliance"""
    GDPR_DATA_REQUEST = "GDPR Data Request"
    GDPR_DATA_DELETION = "GDPR Data Deletion"
    GDPR_DATA_RECTIFICATION = "GDPR Data Rectification"
    GDPR_DATA_PORTABILITY = "GDPR Data Portability"
    USER_REGISTRATION = "User Registration"
    USER_LOGIN = "user login"
    USER_LOGOUT = "User Logout"
    DATA_PROCESSING = "data processing"
    AUDIT_LOG = "audit log"
    COST_ALERT = "cost alert"
    SECURITY_INCIDENT = "security incident"

@dataclass
class SwedishEvent:
    """Standardised event structure for Swedish organisations"""
    event_id: str
    event_type: EventType
    timestamp: str
    source: str
    data_subject_id: Optional[str]
    data_classification: str
    gdpr_lawful_basis: Optional[str]
    payload: Dict[str, Any]
    metadata: Dict[str, Any]
    
    def __post_init__(self):
        """Validate Swedish GDPR requirements"""
        if self.data_classification in ['personal', 'delicate'] and not self.data_subject_id:
            raise ValueError("Data subject ID is required for personal/sensitive data")
        
        if GDPR_ENABLED and self.data_classification == 'personal' and not self.gdpr_lawful_basis:
            raise ValueError("GDPR lawful basis is required for processing personal data")

class SwedishEventProcessor:
    """Event handler for Swedish organisations that complies with GDPR"""
    
    def __init__(self):
        self.event_table = dynamodb.Table(f'{ORGANIZATION_NAME}-{ENVIRONMENT}-events')
        self.audit_table = dynamodb.Table(f'{ORGANIZATION_NAME}-{ENVIRONMENT}-audit-log')
        self.gdpr_table = dynamodb.Table(f'{ORGANIZATION_NAME}-{ENVIRONMENT}-gdpr-requests')
        
    def process_event(self, event: SwedishEvent) -> Dict[str, Any]:
        """Process event with Swedish compliance requirements"""
        try:
            # Record event for audit purposes
            self._audit_log_event(event)
            
            # Save event in DynamoDB
            self._store_event(event)
            
            # Procedure determined by event type
            result = self._route_event(event)
            
            # Processing specific to GDPR
            if GDPR_ENABLED and event.data_classification in ['personal', 'delicate']:
                self._process_gdpr_requirements(event)
            
            logger.info(f"Successfully processed event {event.event_id} of type {event.event_type.value}")
            return {"status": "success", "event_id": event.event_id, "outcome": result}
            
        except Exception as e:
            logger.error(f"Error processing event {event.event_id}: {str(e)}")
            self._handle_event_error(event, e)
            raise
    
    def _audit_log_event(self, event: SwedishEvent) -> None:
        """Create audit log entry for Swedish compliance"""
        audit_entry = {
            'audit_id': f"audit-{event.event_id}",
            'timestamp': event.timestamp,
            'event type': event.event_type.value,
            'source': event.source,
            'data_subject_id': event.data_subject_id,
            'data classification': event.data_classification,
            'GDPR Lawful Basis': event.gdpr_lawful_basis,
            'organisation': ORGANIZATION_NAME,
            'environment': ENVIRONMENT,
            'compliance flags': {
                'GDPR processed': GDPR_ENABLED,
                'audit logged': True,
                'data residency': 'Sweden',
                'Encryption Used': True
            },
            'retention until': self._calculate_retention_date(event.data_classification),
            'ttl': self._calculate_ttl(event.data_classification)
        }
        
        self.audit_table.put_item(Item=audit_entry)
    
    def _store_event(self, event: SwedishEvent) -> None:
        """Save event in DynamoDB with Swedish encryption"""
        event_item = {
            'event_id': event.event_id,
            'event type': event.event_type.value,
            'timestamp': event.timestamp,
            'source': event.source,
            'data_subject_id': event.data_subject_id,
            'data classification': event.data_classification,
            'GDPR Lawful Basis': event.gdpr_lawful_basis,
            'payload': json.dumps(event.payload),
            'metadata': event.metadata,
            'ttl': self._calculate_ttl(event.data_classification)
        }
        
        self.event_table.put_item(Item=event_item)
    
    def _route_event(self, event: SwedishEvent) -> Dict[str, Any]:
        """Send the event to the correct processor"""
        processors = {
            EventType.GDPR_DATA_REQUEST: self._process_gdpr_request,
            EventType.GDPR_DATA_DELETION: self._process_gdpr_deletion,
            EventType.GDPR_DATA_RECTIFICATION: self._process_gdpr_rectification,
            EventType.GDPR_DATA_PORTABILITY: self._process_gdpr_portability,
            EventType.USER_REGISTRATION: self._process_user_registration,
            EventType.DATA_PROCESSING: self._process_data_processing,
            EventType.COST_ALERT: self._process_cost_alert,
            EventType.SECURITY_INCIDENT: self._process_security_incident
        }
        
        processor = processors.get(event.event_type, self._default_processor)
        return processor(event)
    
    def _process_gdpr_request(self, event: SwedishEvent) -> Dict[str, Any]:
        """Handle GDPR data subject requests in accordance with Swedish requirements"""
        request_data = event.payload
        
        # Check GDPR request format
        required_fields = ['request type', 'data subject email', 'verification token']
        if not all(field in request_data for field in required_fields):
            raise ValueError("The GDPR request format is invalid")
        
        # Create GDPR request entry
        gdpr_request = {
            'request_id': f"gdpr-{event.event_id}",
            'timestamp': event.timestamp,
            'request type': request_data['request type'],
            'data_subject_id': event.data_subject_id,
            'data subject email': request_data['data subject email'],
            'verification token': request_data['verification token'],
            'status': 'pending',
            'The lawful basis used': event.gdpr_lawful_basis,
            'processing deadline': self._calculate_gdpr_deadline(),
            'organisation': ORGANIZATION_NAME,
            'environment': ENVIRONMENT,
            'metadata': {
                'source IP': request_data.get('source IP'),
                'user agent': request_data.get('user agent'),
                'swedish_locale': True,
                'data residency': 'Sweden'
            }
        }
        
        self.gdpr_table.put_item(Item=gdpr_request)
        
        # Send a notification to the GDPR team
        self._send_gdpr_notification(gdpr_request)
        
        return {
            "request_id": gdpr_request['request_id'],
            "status": "created",
            "processing deadline": gdpr_request['processing deadline']
        }
    
    def _process_gdpr_deletion(self, event: SwedishEvent) -> Dict[str, Any]:
        """Handle GDPR data deletion in accordance with Swedish requirements"""
        deletion_data = event.payload
        data_subject_id = event.data_subject_id
        
        # List all databases and tables that may contain personal data
        data_stores = [
            {'type': 'DynamoDB', 'table': f'{ORGANIZATION_NAME}-{ENVIRONMENT}-users'},
            {'type': 'DynamoDB', 'table': f'{ORGANIZATION_NAME}-{ENVIRONMENT}-profiles'},
            {'type': 'DynamoDB', 'table': f'{ORGANIZATION_NAME}-{ENVIRONMENT}-activities'},
            {'type': 's3', 'pail': f'{ORGANIZATION_NAME}-{ENVIRONMENT}-user-data'},
            {'type': 'rds', 'database': f'{ORGANIZATION_NAME}_production'}
        ]
        
        deletion_results = []
        
        for store in data_stores:
            try:
                if store['type'] == 'DynamoDB':
                    result = self._delete_from_dynamodb(store['table'], data_subject_id)
                elif store['type'] == 's3':
                    result = self._delete_from_s3(store['pail'], data_subject_id)
                elif store['type'] == 'rds':
                    result = self._delete_from_rds(store['database'], data_subject_id)
                
                deletion_results.append({
                    'shop': store,
                    'status': 'success',
                    'deleted records': result.get('number of items deleted', 0)
                })
                
            except Exception as e:
                deletion_results.append({
                    'shop': store,
                    'status': 'mistake',
                    'mistake': str(e)
                })
                logger.error(f"Error deleting from {store}: {str(e)}")
        
        # Deleting logs for auditing purposes
        deletion_audit = {
            'deletion ID': f"deletion-{event.event_id}",
            'timestamp': event.timestamp,
            'data_subject_id': data_subject_id,
            'deletion results': deletion_results,
            'Total stores processed': len(data_stores),
            'successful deletions': sum(1 for r in deletion_results if r['status'] == 'success'),
            'compliant with GDPR': all(r['status'] == 'success' for r in deletion_results)
        }
        
        self.audit_table.put_item(Item=deletion_audit)
        
        return deletion_audit
    
    def _process_cost_alert(self, event: SwedishEvent) -> Dict[str, Any]:
        """Process cost alert for Swedish budget control"""
        cost_data = event.payload
        
        # Convert to Swedish kronor if necessary
        if cost_data.get('currency') != 'sack':
            sek_amount = self._convert_to_sek(
                cost_data['amount'], 
                cost_data.get('currency', 'USD')
            )
            cost_data['amount in SEK'] = sek_amount
        
        # Create Swedish cost alert
        alert_message = self._format_swedish_cost_alert(cost_data)
        
        # Send to Swedish notification channels
        sns.publish(
            TopicArn=os.environ.get('COST_ALERT_TOPIC_ARN'),
            Subject=f"Kostnadsvarning - {ORGANIZATION_NAME} {ENVIRONMENT}",
            Message=alert_message,
            MessageAttributes={
                'Organisation': {'Data Type': 'String', 'StringValue': ORGANIZATION_NAME},
                'Environment': {'Data Type': 'String', 'StringValue': ENVIRONMENT},
                'Alert Type': {'Data Type': 'String', 'StringValue': 'cost'},
                'Currency': {'Data Type': 'String', 'StringValue': 'sack'},
                'Language': {'Data Type': 'String', 'StringValue': 'Swedish'}
            }
        )
        
        return {
            "Alert sent": True,
            "currency": "sack",
            "amount": cost_data.get('amount in SEK', cost_data['amount'])
        }
    
    def _calculate_retention_date(self, data_classification: str) -> str:
        """Calculate retention date according to Swedish legal requirements"""
        retention_periods = {
            'public': 365,      # 1 year
            'internal': 1095,   # 3 years
            'personal': 2555,   # 7 years according to the Accounting Act
            'delicate': 2555,  # 7 years
            'financial': 2555   # 7 years according to the Accounting Act
        }
        
        days = retention_periods.get(data_classification, 365)
        retention_date = datetime.now(timezone.utc) + timedelta(days=days)
        return retention_date.isoformat()
    
    def _calculate_ttl(self, data_classification: str) -> int:
        """Calculate TTL for DynamoDB according to Swedish requirements"""
        current_time = int(datetime.now(timezone.utc).timestamp())
        retention_days = {
            'public': 365,
            'internal': 1095,
            'personal': 2555,
            'delicate': 2555,
            'financial': 2555
        }
        
        days = retention_days.get(data_classification, 365)
        return current_time + (days * 24 * 60 * 60)
    
    def _format_swedish_cost_alert(self, cost_data: Dict[str, Any]) -> str:
        """Format cost alert in Swedish"""
        return f"""
Kostnadsvarning for {ORGANIZATION_NAME}

Miljö: {ENVIRONMENT}
Current kostnad: {cost_data.get('amount in SEK', cost_data['amount']):.2f} SEK
Budget: {cost_data.get('budget_sek', cost_data.get('budget', 'Not applicable'))} SEK
Procent of budget: {cost_data.get('percentage', 'Not applicable')}%

Datum: {datetime.now().strftime('%Y-%m-%d %H:%M')} (svensk time)

Kostnadscenter: {cost_data.get('cost centre', 'Not applicable')}
Tjänster: {','.join(cost_data.get('services', []))}

For mer information, kontakta IT-avdelningen.
        """.strip()

# Lambda function handlers for Swedish event processing
def gdpr_event_handler(event, context):
    """Lambda handler for GDPR events"""
    processor = SwedishEventProcessor()
    
    try:
        # Parse incoming event
        if 'Records' in event:
            # SQS/SNS event
            results = []
            for record in event['Records']:
                event_data = json.loads(record['body'])
                swedish_event = SwedishEvent(**event_data)
                result = processor.process_event(swedish_event)
                results.append(result)
            return {"processed events": len(results), "results": results}
        else:
            # Direct invocation
            swedish_event = SwedishEvent(**event)
            result = processor.process_event(swedish_event)
            return result
            
    except Exception as e:
        logger.error(f"Error in GDPR event handler: {str(e)}")
        return {
            "status": "mistake",
            "mistake": str(e),
            "event_id": event.get('event_id', 'unknown')
        }

def cost_monitoring_handler(event, context):
    """Lambda handler for Swedish cost monitoring"""
    processor = SwedishEventProcessor()
    
    try:
        # Fetch current costs from Cost Explorer
        cost_explorer = boto3.client('this', region_name='eu-north-1')
        
        end_date = datetime.now().strftime('Year-Month-Day')
        start_date = (datetime.now() - timedelta(days=1)).strftime('Year-Month-Day')
        
        response = cost_explorer.get_cost_and_usage(
            TimePeriod={'Start': start_date, 'End': end_date},
            Granularity='Daily',
            Metrics=['Blended Cost'],
            GroupBy=[
                {'Type': 'Dimension', 'Key': 'Service'},
                {'Type': 'TAG', 'Key': 'Environment'},
                {'Type': 'TAG', 'Key': 'Cost Centre'}
            ]
        )
        
        # Create cost event
        cost_event = SwedishEvent(
            event_id=f"cost-{int(datetime.now().timestamp())}",
            event_type=EventType.COST_ALERT,
            timestamp=datetime.now(timezone.utc).isoformat(),
            source="AWS Cost Monitoring",
            data_subject_id=None,
            data_classification="internal",
            gdpr_lawful_basis=None,
            payload={
                "cost data": response,
                "currency": "USD",
                "date range": {"start": start_date, "end": end_date}
            },
            metadata={
                "organisation": ORGANIZATION_NAME,
                "environment": ENVIRONMENT,
                "Monitoring type": "daily"
            }
        )
        
        result = processor.process_event(cost_event)
        return result
        
    except Exception as e:
        logger.error(f"Error in cost monitoring handler: {str(e)}")
        return {"status": "mistake", "mistake": str(e)}
```

## Practical architecture as code implementation examples

to demonstrate Cloud Architecture as Code in practice for Swedish organisations, complete implementation examples are presented here to show how real-world scenarios can be solved:

### Implementation Example 1: Swedish E-commerce Solution

```terraform
# terraform/ecommerce-platform/main.tf
# Complete e-commerce solution for Swedish organisations

module "Swedish e-commerce infrastructure" {
  source = "./modules/ecommerce"
  
  # Organisation configuration
  organization_name = "Swedish trade"
  environment      = var.environment
  region          = "eu-north-1"  # Stockholm for Swedish data residency
  
  # GDPR and compliance requirements
  gdpr_compliance_enabled = true
  data_residency_region   = "Sweden"
  audit_logging_enabled   = true
  encryption_at_rest      = true
  
  # E-commerce specific requirements
  enable_payment_processing = true
  enable_inventory_management = true
  enable_customer_analytics = true
  enable_gdpr_customer_portal = true
  
  # Swedish localisation requirements
  supported_languages    = ["s.v.", "a"]
  default_currency      = "sack"
  tax_calculation_rules = "Swedish VAT"
  
  # Security and performance
  enable_waf                = true
  enable_ddos_protection   = true
  enable_cdn               = true
  ssl_certificate_domain   = var.domain_name
  
  # Backup and disaster recovery
  backup_retention_days        = 90
  enable_cross_region_backup  = true
  disaster_recovery_region    = "EU Central 1"
  
  tags = {
    Project       = "Swedish E-commerce"
    BusinessUnit  = "Retail"
    CostCenter    = "CC-RETAIL-001"
    Compliance    = "GDPR, PCI-DSS"
    DataType      = "Customer, Payment, Inventory"
  }
}
```

### Implementation Example 2: Swedish Healthtech Platform

```yaml
# kubernetes/healthtech-platform.yaml
# Kubernetes deployment for Swedish healthtech with particular security requirements

apiVersion: v1
kind: Namespace
metadata:
  name: svenska-healthtech
  labels:
    app.kubernetes.io/name: svenska-healthtech
    svenska.se/data-classification: "delicate"
    svenska.se/gdpr-compliant: "true"
    svenska.se/hipaa-compliant: "true"
    svenska.se/patient-data: "true"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: patient-portal
  namespace: svenska-healthtech
spec:
  replicas: 3
  selector:
    matchLabels:
      app: patient-portal
  template:
    metadata:
      labels:
        app: patient-portal
        svenska.se/component: "interacting with patients"
        svenska.se/data-access: "patient data"
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 2000
      containers:
      - name: patient-portal
        image: svenska-healthtech/patient-portal:v1.2.0
        ports:
        - containerPort: 8080
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: connection-string
        - name: GDPR_ENABLED
          value: "true"
        - name: PATIENT_DATA_ENCRYPTION
          value: "AES-256"
        - name: AUDIT_LOGGING
          value: "activated"
        - name: SWEDISH_LOCALE
          value: "sv_SE.UTF-8"
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
            - ALL
        resources:
          requests:
            memory: "256 MiB"
            cpu: "250 meters"
          limits:
            memory: "512 MiB"
            cpu: "500 meters"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
```

## Summary


The modern Architecture as Code methodology represents the future for infrastructure management in Swedish organisations.
Cloud Architecture as Code represents a fundamental evolution of Architecture as Code for Swedish organisations operating in cloud-native environments. By utilising cloud provider-specific services and capabilities, organisations can achieve unprecedented scalability, resilience, and cost-efficiency while meeting Swedish compliance requirements.

The different cloud provider ecosystems - AWS, Azure, and Google Cloud Platform - each offer unique value for Swedish organisations. AWS dominates through a comprehensive service portfolio and a strong presence in the Stockholm region. Azure attracts Swedish enterprise organisations through strong Microsoft integration and the Sweden Central data centre. Google Cloud Platform appeals to innovation-focused organisations with its machine learning capabilities and advanced analytics services.

Multi-cloud strategies enable optimal distribution of workloads to maximize performance, minimize costs, and ensure resilience. Tools like Terraform and Pulumi abstract provider-specific differences and enable consistent management across different cloud environments. For Swedish organisations, this means the opportunity to combine AWS for primary workloads, Azure for disaster recovery, and Google Cloud for analytics and machine learning.

Serverless architectures are revolutionizing how Swedish organisations think about infrastructure management by eliminating traditional server administration and enabling automatic scaling based on actual demand. Function-as-a-Service patterns, event-driven architectures, and managed services reduce operational overhead while ensuring GDPR compliance through built-in security and audit capabilities.

Container-first approaches with Kubernetes as an orchestration platform form the foundation for modern cloud-native applications. For Swedish organisations, this enables portable workloads that can run across different cloud providers while consistent security policies and compliance requirements are maintained.

Hybrid cloud implementations combine on-premises infrastructure with public cloud services for Swedish organisations that have legacy systems or specific regulatory requirements. This approach enables gradual cloud migration while sensitive data can be retained within Swedish borders according to data residency requirements.

Swedish organisations implementing Cloud Architecture as Code can achieve significant competitive advantages through reduced time-to-market, improved scalability, enhanced security, and optimised costs. At the same time, it ensures that proper implementation of Architecture as Code patterns meets GDPR compliance, Swedish data residency, and other regulatory requirements automatically as part of the deployment processes.

Investment in Cloud Architecture as Code pays for itself through improved developer productivity, reduced operational overhead, enhanced system reliability, and better disaster recovery capabilities. As we will see in [chapter 6 about security](06_kapitel5.md), these benefits are particularly important when security and compliance requirements are integrated as a natural part of infrastructure definition and deployment processes.

Sources:
- AWS. "Architecture as Code on AWS." Amazon Web Services Architecture Centre.
- Google Cloud. "Architecture as Code Architecture as Code best practices." Google Cloud Documentation.
- Microsoft Azure. "Azure Resource Manager Templates." Azure Documentation.
- HashiCorp. "Terraform Multi-Cloud Infrastructure." HashiCorp Learn Platform.
- Pulumi. "Cloud Programming Model." Pulumi Documentation.
- Kubernetes. "Cloud Native Applications." Cloud Native Computing Foundation.
- GDPR.eu. "GDPR Compliance for Cloud Infrastructure." GDPR Guidelines.
- Swedish Data Protection Authority. "Cloud Services and Data Protection." Datainspektionen Guidelines.
