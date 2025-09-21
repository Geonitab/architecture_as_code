# Molnarkitektur som kod

Molnarkitektur som kod möjliggör definition och hantering av hela molninfrastrukturen genom deklarativ kod. Detta kapitel utforskar hur molnresurser kan kodifieras för att uppnå skalbarhet, kostnadseffektivitet och operational excellence.

![Molnarkitektur som kod](images/diagram_07_molnarkitektur.png)

*Molnarkitektur som kod integrerar olika molntjänster och resurser i en koherent, versionshanterad definition som möjliggör repeatability och governance.*

## Grundprinciper för molnarkitektur som kod

Molnarkitektur som kod bygger på cloud-native principer där infrastruktur definieras som immutable, declarative specifications. Detta möjliggör automatisk skalning, disaster recovery och multi-region deployments.

Cloud providers erbjuder native verktyg som AWS CloudFormation, Azure Resource Manager och Google Cloud Deployment Manager, samt tredjepartsverktyg som Terraform och Pulumi för molnarkitektur som kod.

## Infrastructure as Code för olika molnleverantörer

### AWS CloudFormation
```yaml
# AWS CloudFormation template
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Scalable web application infrastructure'

Parameters:
  Environment:
    Type: String
    Default: production
    AllowedValues: [development, staging, production]

Resources:
  VPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16
      EnableDnsHostnames: true
      EnableDnsSupport: true
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-vpc'

  PublicSubnet:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: 10.0.1.0/24
      AvailabilityZone: !Select [0, !GetAZs '']
      MapPublicIpOnLaunch: true
```

### Azure Resource Manager
```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "environment": {
      "type": "string",
      "defaultValue": "production",
      "allowedValues": ["development", "staging", "production"]
    }
  },
  "resources": [
    {
      "type": "Microsoft.Network/virtualNetworks",
      "apiVersion": "2023-04-01",
      "name": "[concat(parameters('environment'), '-vnet')]",
      "location": "[resourceGroup().location]",
      "properties": {
        "addressSpace": {
          "addressPrefixes": ["10.0.0.0/16"]
        }
      }
    }
  ]
}
```

## Multi-cloud arkitektur som kod

Multi-cloud strategier kräver abstraktion layers som Terraform eller Pulumi för att hantera infrastruktur över flera molnleverantörer med gemensamma arbetssätt och governance.

```hcl
# Terraform multi-cloud exempel
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

# AWS resources
resource "aws_s3_bucket" "primary_storage" {
  bucket = "primary-data-${var.environment}"
}

# Azure resources
resource "azurerm_storage_account" "backup_storage" {
  name                     = "backup${var.environment}"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "GRS"
}
```

## Serverless arkitektur som kod

Serverless arkitekturer definieras genom event-driven komponenter och managed services som skalas automatiskt baserat på demand. Infrastructure as Code för serverless inkluderar funktionsdefinitioner, triggers och resurskonfigurationer.

```yaml
# AWS SAM template för serverless
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Globals:
  Function:
    Timeout: 30
    Runtime: python3.9
    Environment:
      Variables:
        ENVIRONMENT: !Ref Environment

Resources:
  ProcessingFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/
      Handler: app.lambda_handler
      Events:
        Api:
          Type: Api
          Properties:
            Path: /process
            Method: post
        Schedule:
          Type: Schedule
          Properties:
            Schedule: rate(5 minutes)
```

## Cost optimization och resource management

Molnarkitektur som kod möjliggör automatisk cost optimization genom resource tagging, scheduled scaling och policy-driven resource management. Infrastructure definitions kan inkludera cost constraints och budget alerts.

## Security och compliance i molnet

Molnsäkerhet som kod inkluderar identity and access management (IAM), network security groups, encryption configurations och compliance policies definierade som kod.

## Sammanfattning

Molnarkitektur som kod möjliggör skalbar, kostnadseffektiv och säker hantering av molninfrastruktur. Genom att kodifiera molnresurser uppnås repeatability, governance och operational excellence.

Källor:
- AWS Well-Architected Framework. Amazon Web Services, 2024.
- Azure Architecture Center. Microsoft Azure, 2024.
- Google Cloud Architecture Framework. Google Cloud, 2024.
- Terraform Documentation. HashiCorp, 2024.