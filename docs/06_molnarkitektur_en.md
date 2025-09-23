# MolnArchitecture as Code

MolnArchitecture as Code representerar den naturliga utvecklingen of Architecture as Code in molnbaserade miljöer. Through to utnyttja molnleverantörers API:er and tjänster can organizations skapa skalbara, motståndskraftiga and kostnadseffektiva arkitekturer helt through Architecture as Code. That vi såg in [chapter 2 om fundamental principles](02_kapitel1.md), is this metod fundamental for moderna organizations that strävar after digital omvandling and operativ excellens.

![MolnArchitecture as Code](images/diagram_05_kapitel4.png)

The diagram illustrates progression from multi-cloud environbutts through provider abstraction and resource managebutt to state managebutt and cross-region deployment capabilities. This progression enables den typ of skalbar Architecture as Code-automation that vi will to fördjupa in [chapter 4 om CI/CD-pipelines](04_kapitel3.md) and den organizational förändring that diskuteras in [chapter 10](10_kapitel9.md).

## Molnleverantörers ecosystem for Architecture as Code

Swedish organizations står inför ett rikt utbud of molnleverantörer, var and en with their egna styrkor and specialiseringar. For to uppnå framgångsrik cloud adoption must organizations understand varje leverantörs unika capabilities and how these can utnyttjas through Architecture as Code approaches.

### Amazon Web Services (AWS) and Swedish organizations

AWS dominerar den globala molnmarknaden and have etablerat stark närvaro in Sverige through datacenters in Stockholm-regionen. For Swedish organizations erbjuder AWS comprehensive tjänster that is särskilt relevanta for lokala compliance-requirements and prestanda-behov.

**AWS CloudFormation** utgör AWS:s native Infrastructure as Code-tjänst that enables deklarativ definition of AWS-resurser through JSON or YAML templates. CloudFormation hanterar resource dependencies automatically and ensures to infrastructure deployments is reproducerbara and återställningscapable:

for en detaljerad CloudFormation template that implebutterar VPC configuration for Swedish organizations with GDPR compliance, se [07_CODE_1: VPC configuration for Swedish organizations](#07_CODE_1) in Appendix A.

**AWS CDK (Cloud Developbutt Kit)** revolutionerar Infrastructure as Code through to enablesa definition of cloud reSources with programmeringsspråk that TypeScript, Python, Java and C#. For Swedish utvecklarteam that redan behärskar these språk reducerar CDK learning curve and enables återanvändning of befintliga programmeringskunskaper:

```typescript
// cdk/Swedish-org-infrastructure.ts
import * as cdk from 'aws-cdk-lib';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as rds from 'aws-cdk-lib/aws-rds';
import * as logs from 'aws-cdk-lib/aws-logs';
import * as kms from 'aws-cdk-lib/aws-kms';
import { Construct } from 'constructs';

export interface SwedishOrgInfrastructureProps extends cdk.StackProps {
 environbutt: 'development' | 'staging' | 'production';
 dataClassification: 'public' | 'internal' | 'confidential' | 'restricted';
 complianceRequirebutts: string[];
 costCenter: string;
 organizationalUnit: string;
}

export class SwedishOrgInfrastructureStack extends cdk.Stack {
 constructor(scope: Construct, id: string, props: SwedishOrgInfrastructureProps) {
 super(scope, id, props);

 // Definiera common tags for all resurser
 const commonTags = {
 Environbutt: props.environbutt,
 DataClassification: props.dataClassification,
 CostCenter: props.costCenter,
 OrganizationalUnit: props.organizationalUnit,
 Country: 'Sweden',
 Region: 'eu-north-1',
 ComplianceRequirebutts: props.complianceRequirebutts.join(','),
 ManagedBy: 'AWS-CDK',
 LastUpdated: new Date().toISOString().split('T')[0]
 };

 // Skapa VPC with Swedish säkerhetskrav
 const vpc = new ec2.Vpc(this, 'SwedishOrgVPC', {
 cidr: props.environbutt === 'production' ? '10.0.0.0/16' : '10.1.0.0/16',
 maxAzs: props.environbutt === 'production' ? 3 : 2,
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

 // toämpa common tags on VPC
 Object.entries(commonTags).forEach(([key, value]) => {
 cdk.Tags.of(vpc).add(key, value);
 });

 // GDPR-compliant KMS key for databaskryptering
 const databaseEncryptionKey = new kms.Key(this, 'DatabaseEncryptionKey', {
 description: 'KMS key for databaskryptering according to GDPR-requirements',
 enableKeyRotation: true,
 removalPolicy: props.environbutt === 'production' ? 
 cdk.RemovalPolicy.RETAIN : cdk.RemovalPolicy.DESTROY
 });

 // Database subnet group for isolerad databas-tier
 const dbSubnetGroup = new rds.SubnetGroup(this, 'DatabaseSubnetGroup', {
 vpc,
 description: 'Subnet group for GDPR-compliant databaser',
 vpcSubnets: {
 subnetType: ec2.SubnetType.PRIVATE_ISOLATED
 }
 });

 // RDS instans with Swedish säkerhetskrav
 if (props.environbutt === 'production') {
 const database = new rds.DatabaseInstance(this, 'PrimaryDatabase', {
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
 cloudwatchLogsExports: ['postgresql'],
 parameters: {
 // Swedish tidszon and locale
 'timezone': 'Europe/Stockholm',
 'lc_messages': 'sv_SE.UTF-8',
 'lc_monetary': 'sv_SE.UTF-8',
 'lc_numeric': 'sv_SE.UTF-8',
 'lc_time': 'sv_SE.UTF-8',
 // GDPR-relevanta inställningar
 'log_statebutt': 'all',
 'log_min_duration_statebutt': '0',
 'shared_preload_libraries': 'pg_stat_statebutts',
 // Säkerhetsinställningar
 'ssl': 'on',
 'ssl_ciphers': 'HIGH:!aNULL:!MD5',
 'ssl_prefer_server_ciphers': 'on'
 }
 });

 // toämpa Swedish compliance tags
 cdk.Tags.of(database).add('DataResidency', 'Sweden');
 cdk.Tags.of(database).add('GDPRCompliant', 'true');
 cdk.Tags.of(database).add('ISO27001Compliant', 'true');
 cdk.Tags.of(database).add('BackupRetention', '30-days');
 }

 // Security groups with Swedish säkerhetsstandarder
 const webSecurityGroup = new ec2.SecurityGroup(this, 'WebSecurityGroup', {
 vpc,
 description: 'Security group for web tier according to Swedish säkerhetskrav',
 allowAllOutbound: false
 });

 // Begränsa inkommande trafik to HTTPS endast
 webSecurityGroup.addIngressRule(
 ec2.Peer.anyIpv4(),
 ec2.Port.tcp(443),
 'HTTPS from internet'
 );

 // toåt utgående trafik endast to nödvändiga tjänster
 webSecurityGroup.addEgressRule(
 ec2.Peer.anyIpv4(),
 ec2.Port.tcp(443),
 'HTTPS utgående'
 );

 // Application security group with restriktiv access
 const appSecurityGroup = new ec2.SecurityGroup(this, 'AppSecurityGroup', {
 vpc,
 description: 'Security group for application tier',
 allowAllOutbound: false
 });

 appSecurityGroup.addIngressRule(
 webSecurityGroup,
 ec2.Port.tcp(8080),
 'Trafik from web tier'
 );

 // Database security group - endast from app tier
 const dbSecurityGroup = new ec2.SecurityGroup(this, 'DatabaseSecurityGroup', {
 vpc,
 description: 'Security group for database tier with minimal access',
 allowAllOutbound: false
 });

 dbSecurityGroup.addIngressRule(
 appSecurityGroup,
 ec2.Port.tcp(5432),
 'PostgreSQL from application tier'
 );

 // VPC Endpoints for AWS services (undviker data exfiltration via internet)
 const s3Endpoint = vpc.addGatewayEndpoint('S3Endpoint', {
 service: ec2.GatewayVpcEndpointAwsService.S3
 });

 const ec2Endpoint = vpc.addInterfaceEndpoint('EC2Endpoint', {
 service: ec2.InterfaceVpcEndpointAwsService.EC2,
 privateDnsEnabled: true
 });

 const rdsEndpoint = vpc.addInterfaceEndpoint('RDSEndpoint', {
 service: ec2.InterfaceVpcEndpointAwsService.RDS,
 privateDnsEnabled: true
 });

 // CloudWatch for monitoring and GDPR compliance logging
 const monitoringLogGroup = new logs.LogGroup(this, 'MonitoringLogGroup', {
 logGroupName: `/aws/Swedish-org/${props.environbutt}/monitoring`,
 retention: logs.RetentionDays.THREE_MONTHS,
 encryptionKey: databaseEncryptionKey
 });

 // Outputs for cross-stack references
 new cdk.CfnOutput(this, 'VPCId', {
 value: vpc.vpcId,
 description: 'VPC ID for Swedish organizationen',
 exportName: `${this.stackName}-VPC-ID`
 });

 new cdk.CfnOutput(this, 'ComplianceStatus', {
 value: JSON.stringify({
 gdprCompliant: props.complianceRequirebutts.includes('gdpr'),
 iso27001Compliant: props.complianceRequirebutts.includes('iso27001'),
 dataResidency: 'Sweden',
 encryptionEnabled: true,
 auditLoggingEnabled: true
 }),
 description: 'Compliance status for deployed infrastructure'
 });
 }

 // Metod for to lägga to Swedish holidayschedules for cost optimization
 addSwedishHolidayScheduling(resource: cdk.Resource) {
 const swedishHolidays = [
 '2024-01-01', // Nyårsdagen
 '2024-01-06', // Trettondedag jul
 '2024-03-29', // Långfredagen
 '2024-04-01', // Annandag påsk
 '2024-05-01', // Första maj
 '2024-05-09', // Kristi himmelsfärdsdag
 '2024-05-20', // Annandag pingst
 '2024-06-21', // Midthatmarafton
 '2024-06-22', // Midthatmardagen
 '2024-11-02', // all helgons dag
 '2024-12-24', // Julafton
 '2024-12-25', // Juldagen
 '2024-12-26', // Annandag jul
 '2024-12-31' // Nyårsafton
 ];

 cdk.Tags.of(resource).add('SwedishHolidays', swedishHolidays.join(','));
 cdk.Tags.of(resource).add('CostOptimization', 'SwedishSchedule');
 }
}

// Usage example
const app = new cdk.App();

new SwedishOrgInfrastructureStack(app, 'SwedishOrgDev', {
 environbutt: 'development',
 dataClassification: 'internal',
 complianceRequirebutts: ['gdpr'],
 costCenter: 'CC-1001',
 organizationalUnit: 'IT-Developbutt',
 env: {
 account: process.env.CDK_DEFAULT_ACCOUNT,
 region: 'eu-north-1'
 }
});

new SwedishOrgInfrastructureStack(app, 'SwedishOrgProd', {
 environbutt: 'production',
 dataClassification: 'confidential',
 complianceRequirebutts: ['gdpr', 'iso27001'],
 costCenter: 'CC-2001',
 organizationalUnit: 'IT-Production',
 env: {
 account: process.env.CDK_DEFAULT_ACCOUNT,
 region: 'eu-north-1'
 }
});
```

### Microsoft Azure for Swedish organizations

Microsoft Azure have utvecklat stark position in Sverige, särskilt within offentlig sektor and traditional enterprise-organizations. Azure Resource Manager (ARM) templates and Bicep utgör Microsofts primary Infrastructure as Code offerings.

**Azure Resource Manager (ARM) Templates** enables deklarativ definition of Azure-resurser through JSON-baserade templates. For Swedish organizations that redan använder Microsoft-produkter utgör ARM templates en naturlig extension of befintliga Microsoft-skickigheter:

```json
{
 "$schema": "https://schema.managebutt.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
 "contentVersion": "1.0.0.0",
 "metadata": {
 "description": "Azure infrastructure for Swedish organizations with GDPR compliance",
 "author": "Swedish IT-avdelningen"
 },
 "parameters": {
 "environbuttType": {
 "type": "string",
 "defaultValue": "development",
 "allowedValues": ["development", "staging", "production"],
 "metadata": {
 "description": "Miljötyp for deployment"
 }
 },
 "dataClassification": {
 "type": "string",
 "defaultValue": "internal",
 "allowedValues": ["public", "internal", "confidential", "restricted"],
 "metadata": {
 "description": "Dataklassificering according to Swedish säkerhetsstandarder"
 }
 },
 "organizationName": {
 "type": "string",
 "defaultValue": "Swedish-org",
 "metadata": {
 "description": "organizationsnamn for resource naming"
 }
 },
 "costCenter": {
 "type": "string",
 "metadata": {
 "description": "Kostnadscenter for fakturering"
 }
 },
 "gdprCompliance": {
 "type": "bool",
 "defaultValue": true,
 "metadata": {
 "description": "Aktivera GDPR compliance features"
 }
 }
 },
 "variables": {
 "resourcePrefix": "[concat(parameters('organizationName'), '-', parameters('environbuttType'))]",
 "location": "Sweden Central",
 "vnetName": "[concat(variables('resourcePrefix'), '-vnet')]",
 "subnetNames": {
 "web": "[concat(variables('resourcePrefix'), '-web-subnet')]",
 "app": "[concat(variables('resourcePrefix'), '-app-subnet')]",
 "database": "[concat(variables('resourcePrefix'), '-db-subnet')]"
 },
 "nsgNames": {
 "web": "[concat(variables('resourcePrefix'), '-web-nsg')]",
 "app": "[concat(variables('resourcePrefix'), '-app-nsg')]",
 "database": "[concat(variables('resourcePrefix'), '-db-nsg')]"
 },
 "commonTags": {
 "Environbutt": "[parameters('environbuttType')]",
 "DataClassification": "[parameters('dataClassification')]",
 "CostCenter": "[parameters('costCenter')]",
 "Country": "Sweden",
 "Region": "Sweden Central",
 "GDPRCompliant": "[string(parameters('gdprCompliance'))]",
 "ManagedBy": "ARM-Template",
 "LastDeployed": "[utcNow()]"
 }
 },
 "reSources": [
 {
 "type": "Microsoft.Network/virtualNetworks",
 "apiVersion": "2023-04-01",
 "name": "[variables('vnetName')]",
 "location": "[variables('location')]",
 "tags": "[variables('commonTags')]",
 "properties": {
 "addressSpace": {
 "addressPrefixes": [
 "[if(equals(parameters('environbuttType'), 'production'), '10.0.0.0/16', '10.1.0.0/16')]"
 ]
 },
 "enableDdosProtection": "[equals(parameters('environbuttType'), 'production')]",
 "subnets": [
 {
 "name": "[variables('subnetNames').web]",
 "properties": {
 "addressPrefix": "[if(equals(parameters('environbuttType'), 'production'), '10.0.1.0/24', '10.1.1.0/24')]",
 "networkSecurityGroup": {
 "id": "[resourceId('Microsoft.Network/networkSecurityGroups', variables('nsgNames').web)]"
 },
 "serviceEndpoints": [
 {
 "service": "Microsoft.Storage",
 "locations": ["Sweden Central", "Sweden South"]
 },
 {
 "service": "Microsoft.KeyVault",
 "locations": ["Sweden Central", "Sweden South"]
 }
 ]
 }
 },
 {
 "name": "[variables('subnetNames').app]",
 "properties": {
 "addressPrefix": "[if(equals(parameters('environbuttType'), 'production'), '10.0.2.0/24', '10.1.2.0/24')]",
 "networkSecurityGroup": {
 "id": "[resourceId('Microsoft.Network/networkSecurityGroups', variables('nsgNames').app)]"
 },
 "serviceEndpoints": [
 {
 "service": "Microsoft.Sql",
 "locations": ["Sweden Central", "Sweden South"]
 }
 ]
 }
 },
 {
 "name": "[variables('subnetNames').database]",
 "properties": {
 "addressPrefix": "[if(equals(parameters('environbuttType'), 'production'), '10.0.3.0/24', '10.1.3.0/24')]",
 "networkSecurityGroup": {
 "id": "[resourceId('Microsoft.Network/networkSecurityGroups', variables('nsgNames').database)]"
 },
 "delegations": [
 {
 "name": "Microsoft.DBforPostgreSQL/flexibleServers",
 "properties": {
 "serviceName": "Microsoft.DBforPostgreSQL/flexibleServers"
 }
 }
 ]
 }
 }
 ]
 },
 "dependsOn": [
 "[resourceId('Microsoft.Network/networkSecurityGroups', variables('nsgNames').web)]",
 "[resourceId('Microsoft.Network/networkSecurityGroups', variables('nsgNames').app)]",
 "[resourceId('Microsoft.Network/networkSecurityGroups', variables('nsgNames').database)]"
 ]
 },
 {
 "type": "Microsoft.Network/networkSecurityGroups",
 "apiVersion": "2023-04-01",
 "name": "[variables('nsgNames').web]",
 "location": "[variables('location')]",
 "tags": "[union(variables('commonTags'), createObject('Tier', 'Web'))]",
 "properties": {
 "securityRules": [
 {
 "name": "Allow-HTTPS-Inbound",
 "properties": {
 "description": "toåt HTTPS trafik from internet",
 "protocol": "Tcp",
 "sourcePortRange": "*",
 "destinationPortRange": "443",
 "sourceAddressPrefix": "Internet",
 "destinationAddressPrefix": "*",
 "access": "Allow",
 "priority": 100,
 "direction": "Inbound"
 }
 },
 {
 "name": "Allow-HTTP-Redirect",
 "properties": {
 "description": "toåt HTTP for redirect to HTTPS",
 "protocol": "Tcp",
 "sourcePortRange": "*",
 "destinationPortRange": "80",
 "sourceAddressPrefix": "Internet",
 "destinationAddressPrefix": "*",
 "access": "Allow",
 "priority": 110,
 "direction": "Inbound"
 }
 },
 {
 "name": "Deny-All-Inbound",
 "properties": {
 "description": "Neka all övrig inkommande trafik",
 "protocol": "*",
 "sourcePortRange": "*",
 "destinationPortRange": "*",
 "sourceAddressPrefix": "*",
 "destinationAddressPrefix": "*",
 "access": "Deny",
 "priority": 4096,
 "direction": "Inbound"
 }
 }
 ]
 }
 },
 {
 "condition": "[parameters('gdprCompliance')]",
 "type": "Microsoft.KeyVault/vaults",
 "apiVersion": "2023-02-01",
 "name": "[concat(variables('resourcePrefix'), '-kv')]",
 "location": "[variables('location')]",
 "tags": "[union(variables('commonTags'), createObject('Purpose', 'GDPR-Compliance'))]",
 "properties": {
 "sku": {
 "family": "A",
 "name": "standard"
 },
 "tenantId": "[subscription().tenantId]",
 "enabledForDeploybutt": false,
 "enabledForDiskEncryption": true,
 "enabledForTemplateDeploybutt": true,
 "enableSoftDelete": true,
 "softDeleteRetentionInDays": 90,
 "enablePurgeProtection": "[equals(parameters('environbuttType'), 'production')]",
 "enableRbacAuthorization": true,
 "networkAcls": {
 "defaultAction": "Deny",
 "bypass": "AzureServices",
 "virtualNetworkRules": [
 {
 "id": "[resourceId('Microsoft.Network/virtualNetworks/subnets', variables('vnetName'), variables('subnetNames').app)]",
 "ignoreMissingVnetServiceEndpoint": false
 }
 ]
 }
 },
 "dependsOn": [
 "[resourceId('Microsoft.Network/virtualNetworks', variables('vnetName'))]"
 ]
 }
 ],
 "outputs": {
 "vnetId": {
 "type": "string",
 "value": "[resourceId('Microsoft.Network/virtualNetworks', variables('vnetName'))]",
 "metadata": {
 "description": "Resource ID for det skapade virtual network"
 }
 },
 "subnetIds": {
 "type": "object",
 "value": {
 "web": "[resourceId('Microsoft.Network/virtualNetworks/subnets', variables('vnetName'), variables('subnetNames').web)]",
 "app": "[resourceId('Microsoft.Network/virtualNetworks/subnets', variables('vnetName'), variables('subnetNames').app)]",
 "database": "[resourceId('Microsoft.Network/virtualNetworks/subnets', variables('vnetName'), variables('subnetNames').database)]"
 },
 "metadata": {
 "description": "Resource IDs for all skapade subnets"
 }
 },
 "complianceStatus": {
 "type": "object",
 "value": {
 "gdprCompliant": "[parameters('gdprCompliance')]",
 "dataResidency": "Sweden",
 "encryptionEnabled": true,
 "auditLoggingEnabled": true,
 "networkSegbuttation": true,
 "accessControlEnabled": true
 },
 "metadata": {
 "description": "Compliance status for deployed infrastructure"
 }
 }
 }
}
```

**Azure Bicep** representerar nästa generation of ARM templates with förbättrad syntax and developer experience. Bicep kompilerar to ARM templates but erbjuder mer läsbar and maintainable code:

```bicep
// bicep/Swedish-org-infrastructure.bicep
// Azure Bicep for Swedish organizations with GDPR compliance

@description('Miljötyp for deployment')
@allowed(['development', 'staging', 'production'])
param environbuttType string = 'development'

@description('Dataklassificering according to Swedish säkerhetsstandarder')
@allowed(['public', 'internal', 'confidential', 'restricted'])
param dataClassification string = 'internal'

@description('organizationsnamn for resource naming')
param organizationName string = 'Swedish-org'

@description('Kostnadscenter for fakturering')
param costCenter string

@description('Aktivera GDPR compliance features')
param gdprCompliance bool = true

@description('Lista over compliance-requirements')
param complianceRequirebutts array = ['gdpr']

// Variabler for konsistent naming and configuration
var resourcePrefix = '${organizationName}-${environbuttType}'
var location = 'Sweden Central'
var isProduction = environbuttType == 'production'

// Common tags for all resurser
var commonTags = {
 Environbutt: environbuttType
 DataClassification: dataClassification
 CostCenter: costCenter
 Country: 'Sweden'
 Region: 'Sweden Central'
 GDPRCompliant: string(gdprCompliance)
 ComplianceRequirebutts: join(complianceRequirebutts, ',')
 ManagedBy: 'Azure-Bicep'
 LastDeployed: utcNow('yyyy-MM-dd')
}

// Log Analytics Workspace for Swedish organizations
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2023-09-01' = if (gdprCompliance) {
 name: '${resourcePrefix}-law'
 location: location
 tags: union(commonTags, {
 Purpose: 'GDPR-Compliance-Logging'
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
 publicNetworkAccessForIngestion: 'Disabled'
 publicNetworkAccessForQuery: 'Disabled'
 }
}

// Key Vault for säker hantering of secrets and encryption keys
resource keyVault 'Microsoft.KeyVault/vaults@2023-02-01' = if (gdprCompliance) {
 name: '${resourcePrefix}-kv'
 location: location
 tags: union(commonTags, {
 Purpose: 'Secret-Managebutt'
 })
 properties: {
 sku: {
 family: 'A'
 name: 'standard'
 }
 tenantId: subscription().tenantId
 enabledForDeploybutt: false
 enabledForDiskEncryption: true
 enabledForTemplateDeploybutt: true
 enableSoftDelete: true
 softDeleteRetentionInDays: 90
 enablePurgeProtection: isProduction
 enableRbacAuthorization: true
 networkAcls: {
 defaultAction: 'Deny'
 bypass: 'AzureServices'
 }
 }
}

// Virtual Network with Swedish säkerhetskrav
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
 name: 'web-subnet'
 properties: {
 addressPrefix: isProduction ? '10.0.1.0/24' : '10.1.1.0/24'
 networkSecurityGroup: {
 id: webNsg.id
 }
 serviceEndpoints: [
 {
 service: 'Microsoft.Storage'
 locations: ['Sweden Central', 'Sweden South']
 }
 {
 service: 'Microsoft.KeyVault'
 locations: ['Sweden Central', 'Sweden South']
 }
 ]
 }
 }
 {
 name: 'app-subnet'
 properties: {
 addressPrefix: isProduction ? '10.0.2.0/24' : '10.1.2.0/24'
 networkSecurityGroup: {
 id: appNsg.id
 }
 serviceEndpoints: [
 {
 service: 'Microsoft.Sql'
 locations: ['Sweden Central', 'Sweden South']
 }
 ]
 }
 }
 {
 name: 'database-subnet'
 properties: {
 addressPrefix: isProduction ? '10.0.3.0/24' : '10.1.3.0/24'
 networkSecurityGroup: {
 id: dbNsg.id
 }
 delegations: [
 {
 name: 'Microsoft.DBforPostgreSQL/flexibleServers'
 properties: {
 serviceName: 'Microsoft.DBforPostgreSQL/flexibleServers'
 }
 }
 ]
 }
 }
 ]
 }
}

// Network Security Groups with restriktiva säkerhetsregler
resource webNsg 'Microsoft.Network/networkSecurityGroups@2023-04-01' = {
 name: '${resourcePrefix}-web-nsg'
 location: location
 tags: union(commonTags, { Tier: 'Web' })
 properties: {
 securityRules: [
 {
 name: 'Allow-HTTPS-Inbound'
 properties: {
 description: 'toåt HTTPS trafik from internet'
 protocol: 'Tcp'
 sourcePortRange: '*'
 destinationPortRange: '443'
 sourceAddressPrefix: 'Internet'
 destinationAddressPrefix: '*'
 access: 'Allow'
 priority: 100
 direction: 'Inbound'
 }
 }
 {
 name: 'Allow-HTTP-Redirect'
 properties: {
 description: 'toåt HTTP for redirect to HTTPS'
 protocol: 'Tcp'
 sourcePortRange: '*'
 destinationPortRange: '80'
 sourceAddressPrefix: 'Internet'
 destinationAddressPrefix: '*'
 access: 'Allow'
 priority: 110
 direction: 'Inbound'
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
 name: 'Allow-Web-To-App'
 properties: {
 description: 'toåt trafik from web tier to app tier'
 protocol: 'Tcp'
 sourcePortRange: '*'
 destinationPortRange: '8080'
 sourceAddressPrefix: isProduction ? '10.0.1.0/24' : '10.1.1.0/24'
 destinationAddressPrefix: '*'
 access: 'Allow'
 priority: 100
 direction: 'Inbound'
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
 name: 'Allow-App-To-DB'
 properties: {
 description: 'toåt databasanslutningar from app tier'
 protocol: 'Tcp'
 sourcePortRange: '*'
 destinationPortRange: '5432'
 sourceAddressPrefix: isProduction ? '10.0.2.0/24' : '10.1.2.0/24'
 destinationAddressPrefix: '*'
 access: 'Allow'
 priority: 100
 direction: 'Inbound'
 }
 }
 ]
 }
}

// PostgreSQL Flexible Server for GDPR-compliant data storage
resource postgresServer 'Microsoft.DBforPostgreSQL/flexibleServers@2023-06-01-preview' = if (isProduction) {
 name: '${resourcePrefix}-postgres'
 location: location
 tags: union(commonTags, {
 DatabaseEngine: 'PostgreSQL'
 DataResidency: 'Sweden'
 })
 sku: {
 name: 'Standard_D4s_v3'
 tier: 'GeneralPurpose'
 }
 properties: {
 administratorLogin: 'pgadmin'
 administratorLoginPassword: 'TempPassword123!' // will to ändras via Key Vault
 version: '15'
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
 mode: 'ZoneRedundant'
 }
 maintenanceWindow: {
 customWindow: 'Enabled'
 dayOfWeek: 6 // Lördag
 startHour: 2
 startMinute: 0
 }
 }
}

// Private DNS Zone for PostgreSQL
resource postgresPrivateDnsZone 'Microsoft.Network/privateDnsZones@2020-06-01' = if (isProduction) {
 name: '${resourcePrefix}-postgres.private.postgres.database.azure.com'
 location: 'global'
 tags: commonTags
}

resource postgresPrivateDnsZoneVnetLink 'Microsoft.Network/privateDnsZones/virtualNetworkLinks@2020-06-01' = if (isProduction) {
 parent: postgresPrivateDnsZone
 name: '${resourcePrefix}-postgres-vnet-link'
 location: 'global'
 properties: {
 registrationEnabled: false
 virtualNetwork: {
 id: vnet.id
 }
 }
}

// Diagnostic Settings for GDPR compliance logging
resource vnetDiagnostics 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = if (gdprCompliance) {
 name: '${resourcePrefix}-vnet-diagnostics'
 scope: vnet
 properties: {
 workspaceId: logAnalytics.id
 logs: [
 {
 categoryGroup: 'allLogs'
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
 networkSegbuttation: true
 accessControlEnabled: true
 backupRetention: isProduction ? '35-days' : '7-days'
}

output keyVaultId string = gdprCompliance ? keyVault.id : ''
output logAnalyticsWorkspaceId string = gdprCompliance ? logAnalytics.id : ''
```

### Google Cloud platform for Swedish innovationsorganizations

Google Cloud platform (GCP) attraherar Swedish tech-companies and startups through their machine learning capabilities and innovativa tjänster. Google Cloud Deploybutt Manager and Terraform Google Provider utgör primary Architecture as Code tools for GCP.

**Google Cloud Deploybutt Manager** använder YAML or Python for Infrastructure as Code definitions and integrerar naturligt with Google Cloud services:

```yaml
# Gcp/Swedish-org-infrastructure.yaml
# Deploybutt Manager template for Swedish organizations

reSources:
 # VPC Network for svensk data residency
 - name: Swedish-org-vpc
 type: compute.v1.network
 properties:
 description: "VPC for Swedish organizations with GDPR compliance"
 autoCreateSubnetworks: false
 routingConfig:
 routingMode: REGIONAL
 metadata:
 labels:
 environbutt: $(ref.environbutt)
 data-classification: $(ref.dataClassification)
 country: sweden
 gdpr-compliant: "true"

 # Subnets with Swedish regionkrav
 - name: web-subnet
 type: compute.v1.subnetwork
 properties:
 description: "Web tier subnet for Swedish applikationer"
 network: $(ref.Swedish-org-vpc.selfLink)
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
 description: "Application tier subnet"
 network: $(ref.Swedish-org-vpc.selfLink)
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
 description: "Database tier subnet with privat åtkomst"
 network: $(ref.Swedish-org-vpc.selfLink)
 ipCidrRange: "10.0.3.0/24"
 region: europe-north1
 enableFlowLogs: true
 purpose: PRIVATE_SERVICE_CONNECT

 # Cloud SQL for GDPR-compliant databaser
 - name: Swedish-org-postgres
 type: sqladmin.v1beta4.instance
 properties:
 name: Swedish-org-postgres-$(ref.environbutt)
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
 
 # Swedish tidszon and locale
 databaseFlags:
 - name: timezone
 value: "Europe/Stockholm"
 - name: lc_messages
 value: "sv_SE.UTF-8"
 - name: log_statebutt
 value: "all"
 - name: log_min_duration_statebutt
 value: "0"
 - name: ssl
 value: "on"
 
 # Backup and recovery for Swedish requirements
 backupConfiguration:
 enabled: true
 startTime: "02:00"
 location: "europe-north1"
 backupRetentionSettings:
 retentionUnit: COUNT
 retainedBackups: 30
 transactionLogRetentionDays: 7
 pointInTimeRecoveryEnabled: true
 
 # Säkerhetsinställningar
 ipConfiguration:
 ipv4Enabled: false
 privateNetwork: $(ref.Swedish-org-vpc.selfLink)
 enablePrivatePathForGoogleCloudServices: true
 authorizedNetworks: []
 requireSsl: true
 
 # Maintenance for Swedish arbetstider
 maintenanceWindow:
 hour: 2
 day: 6 # Lördag
 updateTrack: stable
 
 deletionProtectionEnabled: true
 
 # GDPR compliance logging
 insights:
 queryInsightsEnabled: true
 recordApplicationTags: true
 recordClientAddress: true
 queryStringLength: 4500
 queryPlansPerMinute: 20

 # Cloud KMS for kryptering of känslig data
 - name: Swedish-org-keyring
 type: cloudkms.v1.keyRing
 properties:
 parent: projects/$(env.project)/locations/europe-north1
 keyRingId: Swedish-org-keyring-$(ref.environbutt)

 - name: database-encryption-key
 type: cloudkms.v1.cryptoKey
 properties:
 parent: $(ref.Swedish-org-keyring.name)
 cryptoKeyId: database-encryption-key
 purpose: ENCRYPT_DECRYPT
 versionTemplate:
 algorithm: GOOGLE_SYMMETRIC_ENCRYPTION
 protectionLevel: SOFTWARE
 rotationPeriod: 7776000s # 90 dagar
 nextRotationTime: $(ref.nextRotationTime)

 # Firewall rules for säker nätverkstrafik
 - name: allow-web-to-app
 type: compute.v1.firewall
 properties:
 description: "toåt HTTPS trafik from web to app tier"
 network: $(ref.Swedish-org-vpc.selfLink)
 direction: INGRESS
 priority: 1000
 sourceRanges:
 - "10.0.1.0/24"
 targetTags:
 - "app-server"
 allowed:
 - IPProtocol: tcp
 ports: ["8080"]

 - name: allow-app-to-database
 type: compute.v1.firewall
 properties:
 description: "toåt databasanslutningar from app tier"
 network: $(ref.Swedish-org-vpc.selfLink)
 direction: INGRESS
 priority: 1000
 sourceRanges:
 - "10.0.2.0/24"
 targetTags:
 - "database-server"
 allowed:
 - IPProtocol: tcp
 ports: ["5432"]

 - name: deny-all-ingress
 type: compute.v1.firewall
 properties:
 description: "Neka all övrig inkommande trafik"
 network: $(ref.Swedish-org-vpc.selfLink)
 direction: INGRESS
 priority: 65534
 sourceRanges:
 - "0.0.0.0/0"
 denied:
 - IPProtocol: all

 # Cloud Logging for GDPR compliance
 - name: Swedish-org-log-sink
 type: logging.v2.sink
 properties:
 name: Swedish-org-compliance-sink
 destination: storage.googleapis.com/Swedish-org-audit-logs-$(ref.environbutt)
 filter: |
 resource.type="gce_instance" OR
 resource.type="cloud_sql_database" OR
 resource.type="gce_network" OR
 protoPayload.authenticationInfo.principalEmail!=""
 uniqueWriterIdentity: true

 # Cloud Storage for audit logs with Swedish data residency
 - name: Swedish-org-audit-logs
 type: storage.v1.bucket
 properties:
 name: Swedish-org-audit-logs-$(ref.environbutt)
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
 age: 2555 # 7 år for Swedish requirements
 retentionPolicy:
 retentionPeriod: 220752000 # 7 år in sekunder
 iamConfiguration:
 uniformBucketLevelAccess:
 enabled: true
 encryption:
 defaultKmsKeyName: $(ref.database-encryption-key.name)

outputs:
 - name: vpcId
 value: $(ref.Swedish-org-vpc.id)
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
 backupRetention: "30-days"
 logRetention: "7-years"
```

## Cloud-native Architecture as Code patterns

Cloud-native Infrastructure as Code patterns utnyttjar molnspecific tjänster and capabilities for to skapa optimala arkitekturer. These patterns includes serverless computing, managed databases, auto-scaling groups, and event-driven architectures that eliminerar traditional infrastrukturhantering.

Microservices-baserade arkitekturer is implebutted through containerorkestrering, service mesh, and API gateways definierade as code. This enables loose coupling, independent scaling, and teknologidiversifiering as well asidigt that operationell komplexitet is managed through automation.

### Container-First arkitekturpattern

Modern molnarkitektur builds on containerisering that fundamental abstraktion for applikationsdeployment. For Swedish organizations innebär This to infrastrukturdefinitioner fokuserar on container orchestration platforms that Kubernetes, AWS ECS, Azure Container Instances, or Google Cloud Run:

```terraform
# Terraform/container-platform.tf
# Container platform for Swedish organizations

resource "kubernetes_namespace" "application_namespace" {
 count = length(var.environbutts)
 
 metadata {
 name = "${var.organization_name}-${var.environbutts[count.index]}"
 
 labels = {
 "app.kubernetes.io/managed-by" = "terraform"
 "Swedish.se/environbutt" = var.environbutts[count.index]
 "Swedish.se/data-classification" = var.data_classification
 "Swedish.se/cost-center" = var.cost_center
 "Swedish.se/gdpr-compliant" = "true"
 "Swedish.se/backup-policy" = var.environbutts[count.index] == "production" ? "daily" : "weekly"
 }
 
 annotations = {
 "Swedish.se/contact-email" = var.contact_email
 "Swedish.se/created-date" = timestamp()
 "Swedish.se/compliance-review" = var.compliance_review_date
 }
 }
}

# Resource Quotas for kostnadskontroll and resource governance
resource "kubernetes_resource_quota" "namespace_quota" {
 count = length(var.environbutts)
 
 metadata {
 name = "${var.organization_name}-${var.environbutts[count.index]}-quota"
 namespace = kubernetes_namespace.application_namespace[count.index].metadata[0].name
 }
 
 spec {
 hard = {
 "requests.cpu" = var.environbutts[count.index] == "production" ? "8" : "2"
 "requests.memory" = var.environbutts[count.index] == "production" ? "16Gi" : "4Gi"
 "limits.cpu" = var.environbutts[count.index] == "production" ? "16" : "4"
 "limits.memory" = var.environbutts[count.index] == "production" ? "32Gi" : "8Gi"
 "persistentvolumeclaims" = var.environbutts[count.index] == "production" ? "10" : "3"
 "requests.storage" = var.environbutts[count.index] == "production" ? "100Gi" : "20Gi"
 "count/pods" = var.environbutts[count.index] == "production" ? "50" : "10"
 "count/services" = var.environbutts[count.index] == "production" ? "20" : "5"
 }
 }
}

# Network Policies for mikrosegbuttering and säkerhet
resource "kubernetes_network_policy" "default_deny_all" {
 count = length(var.environbutts)
 
 metadata {
 name = "default-deny-all"
 namespace = kubernetes_namespace.application_namespace[count.index].metadata[0].name
 }
 
 spec {
 pod_selector {}
 policy_types = ["Ingress", "Egress"]
 }
}

resource "kubernetes_network_policy" "allow_web_to_app" {
 count = length(var.environbutts)
 
 metadata {
 name = "allow-web-to-app"
 namespace = kubernetes_namespace.application_namespace[count.index].metadata[0].name
 }
 
 spec {
 pod_selector {
 match_labels = {
 "app.kubernetes.io/component" = "application"
 }
 }
 
 policy_types = ["Ingress"]
 
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
 port = "8080"
 }
 }
 }
}

# Pod Security Standards for Swedish säkerhetskrav
resource "kubernetes_pod_security_policy" "Swedish_org_psp" {
 metadata {
 name = "${var.organization_name}-pod-security-policy"
 }
 
 spec {
 privileged = false
 allow_privilege_escalation = false
 required_drop_capabilities = ["ALL"]
 volumes = ["configMap", "emptyDir", "projected", "secret", "downwardAPI", "persistentVolumeClaim"]
 
 run_as_user {
 rule = "MustRunAsNonRoot"
 }
 
 run_as_group {
 rule = "MustRunAs"
 range {
 min = 1
 max = 65535
 }
 }
 
 supplebuttal_groups {
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

# Service Mesh configuration for Swedish mikroservices
resource "kubernetes_manifest" "istio_namespace" {
 count = var.enable_service_mesh ? length(var.environbutts) : 0
 
 manifest = {
 apiVersion = "v1"
 kind = "Namespace"
 metadata = {
 name = "${var.organization_name}-${var.environbutts[count.index]}-istio"
 labels = {
 "istio-injection" = "enabled"
 "Swedish.se/service-mesh" = "istio"
 "Swedish.se/mtls-mode" = "strict"
 }
 }
 }
}

resource "kubernetes_manifest" "istio_peer_authentication" {
 count = var.enable_service_mesh ? length(var.environbutts) : 0
 
 manifest = {
 apiVersion = "security.istio.io/v1beta1"
 kind = "PeerAuthentication"
 metadata = {
 name = "default"
 namespace = kubernetes_manifest.istio_namespace[count.index].manifest.metadata.name
 }
 spec = {
 mtls = {
 mode = "STRICT"
 }
 }
 }
}

# GDPR compliance through Pod Disruption Budgets
resource "kubernetes_pod_disruption_budget" "application_pdb" {
 count = length(var.environbutts)
 
 metadata {
 name = "${var.organization_name}-app-pdb"
 namespace = kubernetes_namespace.application_namespace[count.index].metadata[0].name
 }
 
 spec {
 min_available = var.environbutts[count.index] == "production" ? "2" : "1"
 selector {
 match_labels = {
 "app.kubernetes.io/name" = var.organization_name
 "app.kubernetes.io/component" = "application"
 }
 }
 }
}
```

### Serverless-first pattern for Swedish innovationsorganizations

Serverless arkitekturer enables unprecedented skalbarhet and kostnadseffektivitet for Swedish organizations. Infrastructure as Code for serverless fokuserar on function definitions, event routing, and managed service integrations:

```terraform
# Terraform/serverless-platform.tf
# Serverless platform for Swedish organizations

# AWS Lambda funktioner with Swedish compliance-requirements
resource "aws_lambda_function" "Swedish_api_gateway" {
 filename = "Swedish-api-${var.version}.zip"
 function_name = "${var.organization_name}-api-gateway-${var.environbutt}"
 role = aws_iam_role.lambda_execution_role.arn
 handler = "index.handler"
 source_code_hash = filebase64sha256("Swedish-api-${var.version}.zip")
 runtime = "nodejs18.x"
 timeout = 30
 memory_size = 512
 
 environbutt {
 variables = {
 ENVIRONbutT = var.environbutt
 DATA_CLASSIFICATION = var.data_classification
 GDPR_ENABLED = "true"
 LOG_LEVEL = var.environbutt == "production" ? "INFO" : "DEBUG"
 SWEDISH_TIMEZONE = "Europe/Stockholm"
 COST_CENTER = var.cost_center
 COMPLIANCE_MODE = "Swedish-gdpr"
 }
 }
 
 vpc_config {
 subnet_ids = var.private_subnet_ids
 security_group_ids = [aws_security_group.lambda_sg.id]
 }
 
 tracing_config {
 mode = "Active"
 }
 
 dead_letter_config {
 target_arn = aws_sqs_queue.dlq.arn
 }
 
 tags = merge(local.common_tags, {
 Function = "API-Gateway"
 Runtime = "Node.js18"
 })
}

# Event-driven arkitektur with SQS for Swedish organizations
resource "aws_sqs_queue" "Swedish_event_queue" {
 name = "${var.organization_name}-events-${var.environbutt}"
 delay_seconds = 0
 max_message_size = 262144
 message_retention_seconds = 1209600 # 14 dagar
 receive_wait_time_seconds = 20
 visibility_timeout_seconds = 120
 
 kms_master_key_id = aws_kms_key.Swedish_org_key.arn
 
 redrive_policy = jsonencode({
 deadLetterTargetArn = aws_sqs_queue.dlq.arn
 maxReceiveCount = 3
 })
 
 tags = merge(local.common_tags, {
 MessageRetention = "14-days"
 Purpose = "Event-processing"
 })
}

resource "aws_sqs_queue" "dlq" {
 name = "${var.organization_name}-dlq-${var.environbutt}"
 message_retention_seconds = 1209600 # 14 dagar
 kms_master_key_id = aws_kms_key.Swedish_org_key.arn
 
 tags = merge(local.common_tags, {
 Purpose = "Dead-Letter-Queue"
 })
}

# DynamoDB for svenskt data residency
resource "aws_dynamodb_table" "Swedish_data_store" {
 name = "${var.organization_name}-data-${var.environbutt}"
 billing_mode = "PAY_PER_REQUEST"
 hash_key = "id"
 range_key = "timestamp"
 stream_enabled = true
 stream_view_type = "NEW_AND_OLD_IMAGES"
 
 attribute {
 name = "id"
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
 name = "DataSubjectIndex"
 hash_key = "data_subject_id"
 projection_type = "ALL"
 }
 
 ttl {
 attribute_name = "ttl"
 enabled = true
 }
 
 server_side_encryption {
 enabled = true
 kms_key_arn = aws_kms_key.Swedish_org_key.arn
 }
 
 point_in_time_recovery {
 enabled = var.environbutt == "production"
 }
 
 tags = merge(local.common_tags, {
 DataType = "Personal-Data"
 GDPRCompliant = "true"
 DataResidency = "Sweden"
 })
}

# API Gateway with Swedish säkerhetskrav
resource "aws_api_gateway_rest_api" "Swedish_api" {
 name = "${var.organization_name}-api-${var.environbutt}"
 description = "API Gateway for Swedish organizationen with GDPR compliance"
 
 endpoint_configuration {
 types = ["REGIONAL"]
 }
 
 policy = jsonencode({
 Version = "2012-10-17"
 Statebutt = [
 {
 Effect = "Allow"
 Principal = "*"
 Action = "execute-api:Invoke"
 Resource = "*"
 Condition = {
 IpAddress = {
 "aws:sourceIp" = var.allowed_ip_ranges
 }
 }
 }
 ]
 })
 
 tags = local.common_tags
}

# CloudWatch Logs for GDPR compliance and auditability
resource "aws_cloudwatch_log_group" "lambda_logs" {
 name = "/aws/lambda/${aws_lambda_function.Swedish_api_gateway.function_name}"
 retention_in_days = var.environbutt == "production" ? 90 : 30
 kms_key_id = aws_kms_key.Swedish_org_key.arn
 
 tags = merge(local.common_tags, {
 LogRetention = var.environbutt == "production" ? "90-days" : "30-days"
 Purpose = "GDPR-Compliance"
 })
}

# Step Functions for Swedish business processes
resource "aws_sfn_state_machine" "Swedish_workflow" {
 name = "${var.organization_name}-workflow-${var.environbutt}"
 role_arn = aws_iam_role.step_functions_role.arn
 
 definition = jsonencode({
 Combutt = "Swedish the organization's GDPR-compliant workflow"
 StartAt = "ValidateInput"
 States = {
 ValidateInput = {
 Type = "Task"
 Resource = aws_lambda_function.input_validator.arn
 Next = "processData"
 Retry = [
 {
 ErrorEquals = ["Lambda.ServiceException", "Lambda.AWSLambdaException"]
 IntervalSeconds = 2
 MaxAttempts = 3
 BackoffRate = 2.0
 }
 ]
 Catch = [
 {
 ErrorEquals = ["States.TaskFailed"]
 Next = "FailureHandler"
 }
 ]
 }
 processData = {
 Type = "Task"
 Resource = aws_lambda_function.data_processor.arn
 Next = "AuditLog"
 }
 AuditLog = {
 Type = "Task"
 Resource = aws_lambda_function.audit_logger.arn
 Next = "Success"
 }
 Success = {
 Type = "Succeed"
 }
 FailureHandler = {
 Type = "Task"
 Resource = aws_lambda_function.failure_handler.arn
 End = true
 }
 }
 })
 
 logging_configuration {
 log_destination = "${aws_cloudwatch_log_group.step_functions_logs.arn}:*"
 include_execution_data = true
 level = "ALL"
 }
 
 tracing_configuration {
 enabled = true
 }
 
 tags = merge(local.common_tags, {
 WorkflowType = "GDPR-Data-processing"
 Purpose = "Business-process-Automation"
 })
}

# EventBridge for event-driven Swedish organizationer
resource "aws_cloudwatch_event_bus" "Swedish_event_bus" {
 name = "${var.organization_name}-events-${var.environbutt}"
 
 tags = merge(local.common_tags, {
 Purpose = "Event-Driven-Architecture"
 })
}

resource "aws_cloudwatch_event_rule" "gdpr_data_request" {
 name = "${var.organization_name}-gdpr-request-${var.environbutt}"
 description = "GDPR data subject rights requests"
 event_bus_name = aws_cloudwatch_event_bus.Swedish_event_bus.name
 
 event_pattern = jsonencode({
 source = ["Swedish.gdpr"]
 detail-type = ["Data Subject Request"]
 detail = {
 requestType = ["access", "rectification", "erasure", "portability"]
 }
 })
 
 tags = merge(local.common_tags, {
 GDPRFunction = "Data-Subject-Rights"
 })
}

resource "aws_cloudwatch_event_target" "gdpr_processor" {
 rule = aws_cloudwatch_event_rule.gdpr_data_request.name
 event_bus_name = aws_cloudwatch_event_bus.Swedish_event_bus.name
 target_id = "GDPRprocessor"
 arn = aws_sfn_state_machine.Swedish_workflow.arn
 role_arn = aws_iam_role.eventbridge_role.arn
 
 input_transformer {
 input_paths = {
 dataSubjectId = "$.detail.dataSubjectId"
 requestType = "$.detail.requestType"
 timestamp = "$.time"
 }
 input_template = jsonencode({
 dataSubjectId = "<dataSubjectId>"
 requestType = "<requestType>"
 processingTime = "<timestamp>"
 complianceMode = "Swedish-gdpr"
 environbutt = var.environbutt
 })
 }
}
```

### Hybrid cloud pattern for Swedish enterprise-organizations

Många Swedish organizations kräver hybrid cloud approaches that kombinerar on-premises infrastructure with public cloud services for to uppfylla regulatory, performance, or legacy system requirebutts:

```terraform
# Terraform/hybrid-cloud.tf
# Hybrid cloud infrastructure for Swedish enterprise-organizations

# AWS Direct Connect for dedicerad konnektivitet
resource "aws_dx_connection" "Swedish_org_dx" {
 name = "${var.organization_name}-dx-${var.environbutt}"
 bandwidth = var.environbutt == "production" ? "10Gbps" : "1Gbps"
 location = "Stockholm Interxion STO1" # Swedish datacenter
 provider_name = "Interxion"
 
 tags = merge(local.common_tags, {
 ConnectionType = "Direct-Connect"
 Location = "Stockholm"
 Bandwidth = var.environbutt == "production" ? "10Gbps" : "1Gbps"
 })
}

# Virtual Private Gateway for VPN connectivity
resource "aws_vpn_gateway" "Swedish_org_vgw" {
 vpc_id = var.vpc_id
 availability_zone = var.primary_az
 
 tags = merge(local.common_tags, {
 Name = "${var.organization_name}-vgw-${var.environbutt}"
 Type = "VPN-Gateway"
 })
}

# Customer Gateway for on-premises connectivity
resource "aws_customer_gateway" "Swedish_org_cgw" {
 bgp_asn = 65000
 ip_address = var.on_premises_public_ip
 type = "ipsec.1"
 
 tags = merge(local.common_tags, {
 Name = "${var.organization_name}-cgw-${var.environbutt}"
 Location = "On-Premises-Stockholm"
 })
}

# Site-to-Site VPN for säker hybrid connectivity
resource "aws_vpn_connection" "Swedish_org_vpn" {
 vpn_gateway_id = aws_vpn_gateway.Swedish_org_vgw.id
 customer_gateway_id = aws_customer_gateway.Swedish_org_cgw.id
 type = "ipsec.1"
 static_routes_only = false
 
 tags = merge(local.common_tags, {
 Name = "${var.organization_name}-vpn-${var.environbutt}"
 Type = "Site-to-Site-VPN"
 })
}

# AWS Storage Gateway for hybrid storage
resource "aws_storagegateway_gateway" "Swedish_org_storage_gw" {
 gateway_name = "${var.organization_name}-storage-gw-${var.environbutt}"
 gateway_timezone = "GMT+1:00" # Svensk tid
 gateway_type = "FILE_S3"
 
 tags = merge(local.common_tags, {
 Name = "${var.organization_name}-storage-gateway"
 Type = "File-Gateway"
 Location = "On-Premises"
 })
}

# S3 bucket for hybrid file shares with Swedish data residency
resource "aws_s3_bucket" "hybrid_file_share" {
 bucket = "${var.organization_name}-hybrid-files-${var.environbutt}"
 
 tags = merge(local.common_tags, {
 Purpose = "Hybrid-File-Share"
 DataResidency = "Sweden"
 })
}

resource "aws_s3_bucket_server_side_encryption_configuration" "hybrid_encryption" {
 bucket = aws_s3_bucket.hybrid_file_share.id
 
 rule {
 apply_server_side_encryption_by_default {
 kms_master_key_id = aws_kms_key.Swedish_org_key.arn
 sse_algorithm = "aws:kms"
 }
 bucket_key_enabled = true
 }
}

# AWS Database Migration Service for hybrid data sync
resource "aws_dms_replication_instance" "Swedish_org_dms" {
 replication_instance_class = var.environbutt == "production" ? "dms.t3.large" : "dms.t3.micro"
 replication_instance_id = "${var.organization_name}-dms-${var.environbutt}"
 
 allocated_storage = var.environbutt == "production" ? 100 : 20
 apply_immediately = var.environbutt != "production"
 auto_minor_version_upgrade = true
 availability_zone = var.primary_az
 engine_version = "3.4.7"
 multi_az = var.environbutt == "production"
 publicly_accessible = false
 replication_subnet_group_id = aws_dms_replication_subnet_group.Swedish_org_dms_subnet.id
 vpc_security_group_ids = [aws_security_group.dms_sg.id]
 
 tags = merge(local.common_tags, {
 Purpose = "Hybrid-Data-Migration"
 })
}

resource "aws_dms_replication_subnet_group" "Swedish_org_dms_subnet" {
 replication_subnet_group_description = "DMS subnet group for Swedish organizationen"
 replication_subnet_group_id = "${var.organization_name}-dms-subnet-${var.environbutt}"
 subnet_ids = var.private_subnet_ids
 
 tags = local.common_tags
}

# AWS App Mesh for hybrid service mesh
resource "aws_appmesh_mesh" "Swedish_org_mesh" {
 name = "${var.organization_name}-mesh-${var.environbutt}"
 
 spec {
 egress_filter {
 type = "ALLOW_ALL"
 }
 }
 
 tags = merge(local.common_tags, {
 MeshType = "Hybrid-Service-Mesh"
 })
}

# Route53 Resolver for hybrid DNS
resource "aws_route53_resolver_endpoint" "inbound" {
 name = "${var.organization_name}-resolver-inbound-${var.environbutt}"
 direction = "INBOUND"
 
 security_group_ids = [aws_security_group.resolver_sg.id]
 
 dynamic "ip_address" {
 for_each = var.private_subnet_ids
 content {
 subnet_id = ip_address.value
 }
 }
 
 tags = merge(local.common_tags, {
 ResolverType = "Inbound"
 Purpose = "Hybrid-DNS"
 })
}

resource "aws_route53_resolver_endpoint" "outbound" {
 name = "${var.organization_name}-resolver-outbound-${var.environbutt}"
 direction = "OUTBOUND"
 
 security_group_ids = [aws_security_group.resolver_sg.id]
 
 dynamic "ip_address" {
 for_each = var.private_subnet_ids
 content {
 subnet_id = ip_address.value
 }
 }
 
 tags = merge(local.common_tags, {
 ResolverType = "Outbound"
 Purpose = "Hybrid-DNS"
 })
}

# Security Groups for hybrid connectivity
resource "aws_security_group" "dms_sg" {
 name_prefix = "${var.organization_name}-dms-"
 description = "Security group for DMS replication instance"
 vpc_id = var.vpc_id
 
 ingress {
 from_port = 0
 to_port = 65535
 protocol = "tcp"
 cidr_blocks = [var.on_premises_cidr]
 description = "All traffic from on-premises"
 }
 
 egress {
 from_port = 0
 to_port = 65535
 protocol = "tcp"
 cidr_blocks = ["0.0.0.0/0"]
 description = "All outbound traffic"
 }
 
 tags = merge(local.common_tags, {
 Name = "${var.organization_name}-dms-sg"
 })
}

resource "aws_security_group" "resolver_sg" {
 name_prefix = "${var.organization_name}-resolver-"
 description = "Security group for Route53 Resolver endpoints"
 vpc_id = var.vpc_id
 
 ingress {
 from_port = 53
 to_port = 53
 protocol = "tcp"
 cidr_blocks = [var.vpc_cidr, var.on_premises_cidr]
 description = "DNS TCP from VPC and on-premises"
 }
 
 ingress {
 from_port = 53
 to_port = 53
 protocol = "udp"
 cidr_blocks = [var.vpc_cidr, var.on_premises_cidr]
 description = "DNS UDP from VPC and on-premises"
 }
 
 egress {
 from_port = 53
 to_port = 53
 protocol = "tcp"
 cidr_blocks = [var.on_premises_cidr]
 description = "DNS TCP to on-premises"
 }
 
 egress {
 from_port = 53
 to_port = 53
 protocol = "udp"
 cidr_blocks = [var.on_premises_cidr]
 description = "DNS UDP to on-premises"
 }
 
 tags = merge(local.common_tags, {
 Name = "${var.organization_name}-resolver-sg"
 })
}
```

## Multi-cloud strategier

Multi-cloud Infrastructure as Code strategier enables distribution of workloads across flera molnleverantörer for to optimera kostnad, prestanda, and resiliens. Provider-agnostic tools that Terraform or Pulumi används for to abstrahera leverantörspecific skillnader and enablesa portabilitet.

Hybrid cloud Architecture as Code-implebuttations kombinerar on-premises infrastructure with public cloud services through VPN connections, dedicated links, and edge computing. Consistent deployment and managebutt processes across environbutts ensures operational efficiency and säkerhetskompliance.

### Terraform for multi-cloud abstraktion

Terraform utgör den mest mogna lösningen for multi-cloud Infrastructure as Code through sitt comprehensive provider ecosystem. For Swedish organizations enables Terraform unified managebutt of AWS, Azure, Google Cloud, and on-premises resurser through en konsistent deklarativ syntax:

```hcl
# Terraform/multi-cloud/main.tf
# Multi-cloud infrastructure for Swedish organizations

terraform {
 required_version = ">= 1.0"
 
 required_providers {
 aws = {
 source = "hashicorp/aws"
 version = "~> 5.0"
 }
 azurerm = {
 source = "hashicorp/azurerm"
 version = "~> 3.0"
 }
 google = {
 source = "hashicorp/google"
 version = "~> 4.0"
 }
 kubernetes = {
 source = "hashicorp/kubernetes"
 version = "~> 2.0"
 }
 }
 
 backend "s3" {
 bucket = "Swedish-org-terraform-state"
 key = "multi-cloud/terraform.tfstate"
 region = "eu-north-1"
 encrypt = true
 }
}

# AWS Provider for Stockholm region
provider "aws" {
 region = "eu-north-1"
 alias = "stockholm"
 
 default_tags {
 tags = {
 Project = var.project_name
 Environbutt = var.environbutt
 Country = "Sweden"
 DataResidency = "Sweden"
 ManagedBy = "Terraform"
 CostCenter = var.cost_center
 GDPRCompliant = "true"
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
 alias = "sweden"
}

# Google Cloud Provider for europe-north1
provider "google" {
 project = var.gcp_project_id
 region = "europe-north1"
 alias = "finland"
}

# Local values for konsistent naming across providers
locals {
 resource_prefix = "${var.organization_name}-${var.environbutt}"
 
 common_tags = {
 Project = var.project_name
 Environbutt = var.environbutt
 Organization = var.organization_name
 Country = "Sweden"
 DataResidency = "Nordic"
 ManagedBy = "Terraform"
 CostCenter = var.cost_center
 GDPRCompliant = "true"
 CreatedDate = formatdate("YYYY-MM-DD", timestamp())
 }
 
 # GDPR data residency requirebutts
 data_residency_requirebutts = {
 personal_data = "Sweden"
 sensitive_data = "Sweden"
 financial_data = "Sweden"
 health_data = "Sweden"
 operational_data = "Nordic"
 public_data = "Global"
 }
}

# AWS Infrastructure for primary workloads
module "aws_infrastructure" {
 source = "./modules/aws"
 providers = {
 aws = aws.stockholm
 }
 
 organization_name = var.organization_name
 environbutt = var.environbutt
 resource_prefix = local.resource_prefix
 common_tags = local.common_tags
 
 # AWS-specific configuration
 vpc_cidr = var.aws_vpc_cidr
 availability_zones = var.aws_availability_zones
 enable_nat_gateway = var.environbutt == "production"
 enable_vpn_gateway = true
 
 # Data residency and compliance
 data_classification = var.data_classification
 compliance_requirebutts = var.compliance_requirebutts
 backup_retention_days = var.environbutt == "production" ? 90 : 30
 
 # Cost optimization
 enable_spot_instances = var.environbutt != "production"
 enable_scheduled_scaling = true
}

# Azure Infrastructure for disaster recovery
module "azure_infrastructure" {
 source = "./modules/azure"
 providers = {
 azurerm = azurerm.sweden
 }
 
 organization_name = var.organization_name
 environbutt = "${var.environbutt}-dr"
 resource_prefix = "${local.resource_prefix}-dr"
 common_tags = merge(local.common_tags, { Purpose = "Disaster-Recovery" })
 
 # Azure-specific configuration
 location = "Sweden Central"
 vnet_address_space = var.azure_vnet_cidr
 enable_ddos_protection = var.environbutt == "production"
 
 # DR-specific settings
 enable_cross_region_backup = true
 backup_geo_redundancy = "GRS"
 dr_automation_enabled = var.environbutt == "production"
}

# Google Cloud for analytics and ML workloads
module "gcp_infrastructure" {
 source = "./modules/gcp"
 providers = {
 google = google.finland
 }
 
 organization_name = var.organization_name
 environbutt = "${var.environbutt}-analytics"
 resource_prefix = "${local.resource_prefix}-analytics"
 common_labels = {
 for k, v in local.common_tags : 
 lower(replace(k, "_", "-")) => lower(v)
 }
 
 # GCP-specific configuration
 region = "europe-north1"
 network_name = "${local.resource_prefix}-analytics-vpc"
 enable_private_google_access = true
 
 # Analytics and ML-specific features
 enable_bigquery = true
 enable_dataflow = true
 enable_vertex_ai = var.environbutt == "production"
 
 # Data governance for Swedish requirements
 enable_data_catalog = true
 enable_dlp_api = true
 data_residency_zone = "europe-north1"
}

# Cross-provider networking for hybrid connectivity
resource "aws_customer_gateway" "azure_gateway" {
 provider = aws.stockholm
 bgp_asn = 65515
 ip_address = module.azure_infrastructure.vpn_gateway_public_ip
 type = "ipsec.1"
 
 tags = merge(local.common_tags, {
 Name = "${local.resource_prefix}-azure-cgw"
 Type = "Azure-Connection"
 })
}

resource "aws_vpn_connection" "aws_azure_connection" {
 provider = aws.stockholm
 vpn_gateway_id = module.aws_infrastructure.vpn_gateway_id
 customer_gateway_id = aws_customer_gateway.azure_gateway.id
 type = "ipsec.1"
 static_routes_only = false
 
 tags = merge(local.common_tags, {
 Name = "${local.resource_prefix}-aws-azure-vpn"
 Connection = "AWS-Azure-Hybrid"
 })
}

# Shared services across all clouds
resource "kubernetes_namespace" "shared_services" {
 count = length(var.kubernetes_clusters)
 
 metadata {
 name = "shared-services"
 labels = merge(local.common_tags, {
 "app.kubernetes.io/managed-by" = "terraform"
 "Swedish.se/shared-service" = "true"
 })
 }
}

# Multi-cloud monitoring with Prometheus federation
resource "kubernetes_manifest" "prometheus_federation" {
 count = length(var.kubernetes_clusters)
 
 manifest = {
 apiVersion = "v1"
 kind = "ConfigMap"
 metadata = {
 name = "prometheus-federation-config"
 namespace = kubernetes_namespace.shared_services[count.index].metadata[0].name
 }
 data = {
 "prometheus.yml" = yamlencode({
 global = {
 scrape_interval = "15s"
 external_labels = {
 cluster = var.kubernetes_clusters[count.index].name
 region = var.kubernetes_clusters[count.index].region
 provider = var.kubernetes_clusters[count.index].provider
 }
 }
 
 scrape_configs = [
 {
 job_name = "federate"
 scrape_interval = "15s"
 honor_labels = true
 metrics_path = "/federate"
 params = {
 "match[]" = [
 "{job=~\"kubernetes-.*\"}",
 "{__name__=~\"job:.*\"}",
 "{__name__=~\"Swedish_org:.*\"}"
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

# Cross-cloud DNS for service discovery
data "aws_route53_zone" "primary" {
 provider = aws.stockholm
 name = var.dns_zone_name
}

resource "aws_route53_record" "azure_services" {
 provider = aws.stockholm
 count = length(var.azure_service_endpoints)
 
 zone_id = data.aws_route53_zone.primary.zone_id
 name = var.azure_service_endpoints[count.index].name
 type = "CNAME"
 ttl = 300
 records = [var.azure_service_endpoints[count.index].endpoint]
}

resource "aws_route53_record" "gcp_services" {
 provider = aws.stockholm
 count = length(var.gcp_service_endpoints)
 
 zone_id = data.aws_route53_zone.primary.zone_id
 name = var.gcp_service_endpoints[count.index].name
 type = "CNAME"
 ttl = 300
 records = [var.gcp_service_endpoints[count.index].endpoint]
}

# Cross-provider security groups synchronization
data "external" "azure_ip_ranges" {
 program = ["python3", "${path.module}/scripts/get-azure-ip-ranges.py"]
 
 query = {
 subscription_id = var.azure_subscription_id
 resource_group = module.azure_infrastructure.resource_group_name
 }
}

resource "aws_security_group_rule" "allow_azure_traffic" {
 provider = aws.stockholm
 count = length(data.external.azure_ip_ranges.result.ip_ranges)
 
 type = "ingress"
 from_port = 443
 to_port = 443
 protocol = "tcp"
 cidr_blocks = [data.external.azure_ip_ranges.result.ip_ranges[count.index]]
 security_group_id = module.aws_infrastructure.app_security_group_id
 description = "HTTPS from Azure ${count.index + 1}"
}

# Multi-cloud cost optimization
resource "aws_budgets_budget" "multi_cloud_budget" {
 provider = aws.stockholm
 count = var.environbutt == "production" ? 1 : 0
 
 name = "${local.resource_prefix}-multi-cloud-budget"
 budget_type = "COST"
 limit_amount = var.monthly_budget_limit
 limit_unit = "USD"
 time_unit = "MONTHLY"
 
 cost_filters {
 tag = {
 Project = [var.project_name]
 }
 }
 
 notification {
 comparison_operator = "GREATER_THAN"
 threshold = 80
 threshold_type = "PERCENTAGE"
 notification_type = "ACTUAL"
 subscriber_email_addresses = var.budget_notification_emails
 }
 
 notification {
 comparison_operator = "GREATER_THAN"
 threshold = 100
 threshold_type = "PERCENTAGE"
 notification_type = "FORECASTED"
 subscriber_email_addresses = var.budget_notification_emails
 }
}

# Multi-cloud backup strategy
resource "aws_s3_bucket" "cross_cloud_backup" {
 provider = aws.stockholm
 bucket = "${local.resource_prefix}-cross-cloud-backup"
 
 tags = merge(local.common_tags, {
 Purpose = "Cross-Cloud-Backup"
 })
}

resource "aws_s3_bucket_replication_configuration" "cross_region_replication" {
 provider = aws.stockholm
 depends_on = [aws_s3_bucket_versioning.backup_versioning]
 
 role = aws_iam_role.replication_role.arn
 bucket = aws_s3_bucket.cross_cloud_backup.id
 
 rule {
 id = "cross-region-replication"
 status = "Enabled"
 
 destination {
 bucket = "arn:aws:s3:::${local.resource_prefix}-cross-cloud-backup-replica"
 storage_class = "STANDARD_IA"
 
 encryption_configuration {
 replica_kms_key_id = aws_kms_key.backup_key.arn
 }
 }
 }
}

# Outputs for cross-provider integration
output "aws_vpc_id" {
 description = "AWS VPC ID for cross-provider networking"
 value = module.aws_infrastructure.vpc_id
}

output "azure_vnet_id" {
 description = "Azure VNet ID for cross-provider networking"
 value = module.azure_infrastructure.vnet_id
}

output "gcp_network_id" {
 description = "GCP VPC Network ID for cross-provider networking"
 value = module.gcp_infrastructure.network_id
}

output "multi_cloud_endpoints" {
 description = "Service endpoints across all cloud providers"
 value = {
 aws_api_endpoint = module.aws_infrastructure.api_gateway_endpoint
 azure_app_url = module.azure_infrastructure.app_service_url
 gcp_analytics_url = module.gcp_infrastructure.analytics_endpoint
 }
}

output "compliance_status" {
 description = "Compliance status across all cloud providers"
 value = {
 aws_gdpr_compliant = module.aws_infrastructure.gdpr_compliant
 azure_gdpr_compliant = module.azure_infrastructure.gdpr_compliant
 gcp_gdpr_compliant = module.gcp_infrastructure.gdpr_compliant
 data_residency_zones = local.data_residency_requirebutts
 cross_cloud_backup = aws_s3_bucket.cross_cloud_backup.arn
 }
}
```

### Pulumi for programmatisk multi-cloud Infrastructure as Code

Architecture as Code-principlesna within This område

Pulumi erbjuder en alternativ approach to multi-cloud Architecture as Code through to enablesa användning of vanliga programmeringsspråk that TypeScript, Python, Go, and C#. For Swedish utvecklarteam that föredrar programmatisk approach over deklarativ configuration:

```typescript
// pulumi/multi-cloud/index.ts
// Multi-cloud infrastructure with Pulumi for Swedish organizations

import * as aws from "@pulumi/aws";
import * as azure from "@pulumi/azure-native";
import * as gcp from "@pulumi/gcp";
import * as kubernetes from "@pulumi/kubernetes";
import * as pulumi from "@pulumi/pulumi";

// configuration for Swedish organizations
const config = new pulumi.Config();
const organizationName = config.require("organizationName");
const environbutt = config.require("environbutt");
const dataClassification = config.get("dataClassification") || "internal";
const complianceRequirebutts = config.getObject<string[]>("complianceRequirebutts") || ["gdpr"];

// Swedish common tags/labels for all providers
const swedishTags = {
 Organization: organizationName,
 Environbutt: environbutt,
 Country: "Sweden",
 DataResidency: "Nordic",
 GDPRCompliant: "true",
 ManagedBy: "Pulumi",
 CostCenter: config.require("costCenter"),
 CreatedDate: new Date().toISOString().split('T')[0]
};

// Provider configurations for Swedish regioner
const awsProvider = new aws.Provider("aws-stockholm", {
 region: "eu-north-1",
 defaultTags: {
 tags: swedishTags
 }
});

const azureProvider = new azure.Provider("azure-sweden", {
 location: "Sweden Central"
});

const gcpProvider = new gcp.Provider("gcp-finland", {
 project: config.require("gcpProjectId"),
 region: "europe-north1"
});

// AWS Infrastructure for primary workloads
class AWSInfrastructure extends pulumi.ComponentResource {
 public readonly vpc: aws.ec2.Vpc;
 public readonly subnets: aws.ec2.Subnet[];
 public readonly database: aws.rds.Instance;
 public readonly apiGateway: aws.apigateway.RestApi;
 
 constructor(name: string, args: any, opts?: pulumi.ComponentResourceOptions) {
 super("Swedish:aws:Infrastructure", name, {}, opts);
 
 // VPC with Swedish säkerhetskrav
 this.vpc = new aws.ec2.Vpc(`${name}-vpc`, {
 cidrBlock: environbutt === "production" ? "10.0.0.0/16" : "10.1.0.0/16",
 enableDnsHostnames: true,
 enableDnsSupport: true,
 tags: {
 Name: `${organizationName}-${environbutt}-vpc`,
 Purpose: "Primary-Infrastructure"
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
 cidrBlock: environbutt === "production" ? 
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
 
 // RDS PostgreSQL for Swedish GDPR-requirements
 const dbSubnetGroup = new aws.rds.SubnetGroup(`${name}-db-subnet-group`, {
 subnetIds: this.subnets.map(s => s.id),
 tags: {
 Name: `${organizationName}-db-subnet-group`,
 Purpose: "Database-GDPR-Compliance"
 }
 }, { provider: awsProvider, parent: this });
 
 this.database = new aws.rds.Instance(`${name}-postgres`, {
 engine: "postgres",
 engineVersion: "15.4",
 instanceClass: environbutt === "production" ? "db.r5.large" : "db.t3.micro",
 allocatedStorage: environbutt === "production" ? 100 : 20,
 storageEncrypted: true,
 dbSubnetGroupName: dbSubnetGroup.name,
 backupRetentionPeriod: environbutt === "production" ? 30 : 7,
 backupWindow: "03:00-04:00", // Swedish nattetid
 maintenanceWindow: "sat:04:00-sat:05:00", // Lördag natt svensk tid
 deletionProtection: environbutt === "production",
 enabledCloudwatchLogsExports: ["postgresql"],
 tags: {
 Name: `${organizationName}-postgres`,
 DataType: "Personal-Data",
 GDPRCompliant: "true",
 BackupStrategy: environbutt === "production" ? "30-days" : "7-days"
 }
 }, { provider: awsProvider, parent: this });
 
 // API Gateway with Swedish säkerhetskrav
 this.apiGateway = new aws.apigateway.RestApi(`${name}-api`, {
 name: `${organizationName}-api-${environbutt}`,
 description: "API Gateway for Swedish organizationen with GDPR compliance",
 endpointConfiguration: {
 types: "REGIONAL"
 },
 policy: JSON.stringify({
 Version: "2012-10-17",
 Statebutt: [{
 Effect: "Allow",
 Principal: "*",
 Action: "execute-api:Invoke",
 Resource: "*",
 Condition: {
 IpAddress: {
 "aws:sourceIp": args.allowedIpRanges || ["0.0.0.0/0"]
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

// Azure Infrastructure for disaster recovery
class AzureInfrastructure extends pulumi.ComponentResource {
 public readonly resourceGroup: azure.reSources.ResourceGroup;
 public readonly vnet: azure.network.VirtualNetwork;
 public readonly sqlServer: azure.sql.Server;
 public readonly appService: azure.web.WebApp;
 
 constructor(name: string, args: any, opts?: pulumi.ComponentResourceOptions) {
 super("Swedish:azure:Infrastructure", name, {}, opts);
 
 // Resource Group for Swedish DR-miljö
 this.resourceGroup = new azure.reSources.ResourceGroup(`${name}-rg`, {
 resourceGroupName: `${organizationName}-${environbutt}-dr-rg`,
 location: "Sweden Central",
 tags: {
 ...swedishTags,
 Purpose: "Disaster-Recovery"
 }
 }, { provider: azureProvider, parent: this });
 
 // Virtual Network for Swedish data residency
 this.vnet = new azure.network.VirtualNetwork(`${name}-vnet`, {
 virtualNetworkName: `${organizationName}-${environbutt}-dr-vnet`,
 resourceGroupName: this.resourceGroup.name,
 location: this.resourceGroup.location,
 addressSpace: {
 addressPrefixes: [environbutt === "production" ? "172.16.0.0/16" : "172.17.0.0/16"]
 },
 subnets: [
 {
 name: "app-subnet",
 addressPrefix: environbutt === "production" ? "172.16.1.0/24" : "172.17.1.0/24",
 serviceEndpoints: [
 { service: "Microsoft.Sql", locations: ["Sweden Central"] },
 { service: "Microsoft.Storage", locations: ["Sweden Central"] }
 ]
 },
 {
 name: "database-subnet",
 addressPrefix: environbutt === "production" ? "172.16.2.0/24" : "172.17.2.0/24",
 delegations: [{
 name: "Microsoft.Sql/managedInstances",
 serviceName: "Microsoft.Sql/managedInstances"
 }]
 }
 ],
 tags: {
 ...swedishTags,
 NetworkType: "Disaster-Recovery"
 }
 }, { provider: azureProvider, parent: this });
 
 // SQL Server for GDPR-compliant backup
 this.sqlServer = new azure.sql.Server(`${name}-sql`, {
 serverName: `${organizationName}-${environbutt}-dr-sql`,
 resourceGroupName: this.resourceGroup.name,
 location: this.resourceGroup.location,
 administratorLogin: "sqladmin",
 administratorLoginPassword: args.sqlAdminPassword,
 version: "12.0",
 minimalTlsVersion: "1.2",
 tags: {
 ...swedishTags,
 DatabaseType: "Disaster-Recovery",
 DataResidency: "Sweden"
 }
 }, { provider: azureProvider, parent: this });
 
 // App Service for Swedish applikationer
 const appServicePlan = new azure.web.AppServicePlan(`${name}-asp`, {
 name: `${organizationName}-${environbutt}-dr-asp`,
 resourceGroupName: this.resourceGroup.name,
 location: this.resourceGroup.location,
 sku: {
 name: environbutt === "production" ? "P1v2" : "B1",
 tier: environbutt === "production" ? "PremiumV2" : "Basic"
 },
 tags: swedishTags
 }, { provider: azureProvider, parent: this });
 
 this.appService = new azure.web.WebApp(`${name}-app`, {
 name: `${organizationName}-${environbutt}-dr-app`,
 resourceGroupName: this.resourceGroup.name,
 location: this.resourceGroup.location,
 serverFarmId: appServicePlan.id,
 siteConfig: {
 alwaysOn: environbutt === "production",
 ftpsState: "Disabled",
 minTlsVersion: "1.2",
 http20Enabled: true,
 appSettings: [
 { name: "ENVIRONbutT", value: `${environbutt}-dr` },
 { name: "DATA_CLASSIFICATION", value: dataClassification },
 { name: "GDPR_ENABLED", value: "true" },
 { name: "SWEDEN_TIMEZONE", value: "Europe/Stockholm" },
 { name: "COMPLIANCE_MODE", value: "Swedish-gdpr" }
 ]
 },
 tags: {
 ...swedishTags,
 AppType: "Disaster-Recovery"
 }
 }, { provider: azureProvider, parent: this });
 
 this.registerOutputs({
 resourceGroupName: this.resourceGroup.name,
 vnetId: this.vnet.id,
 sqlServerName: this.sqlServer.name,
 appServiceUrl: this.appService.defaultHostName.apply(hostname => `https://${hostname}`)
 });
 }
}

// Google Cloud Infrastructure for analytics
class GCPInfrastructure extends pulumi.ComponentResource {
 public readonly network: gcp.compute.Network;
 public readonly bigQueryDataset: gcp.bigquery.Dataset;
 public readonly cloudFunction: gcp.cloudfunctions.Function;
 
 constructor(name: string, args: any, opts?: pulumi.ComponentResourceOptions) {
 super("Swedish:gcp:Infrastructure", name, {}, opts);
 
 // VPC Network for Swedish analytics
 this.network = new gcp.compute.Network(`${name}-network`, {
 name: `${organizationName}-${environbutt}-analytics-vpc`,
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
 aggregationInterval: "INTERVAL_5_SEC",
 metadata: "INCLUDE_ALL_METADATA"
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
 datasetId: `${organizationName}_${environbutt}_analytics`,
 friendlyName: `Swedish ${organizationName} Analytics Dataset`,
 description: "Analytics dataset for Swedish organizationen with GDPR compliance",
 location: "europe-north1",
 defaultTableExpirationMs: environbutt === "production" ? 
 7 * 24 * 60 * 60 * 1000 : // 7 dagar for production
 24 * 60 * 60 * 1000, // 1 dag for dev/staging
 
 access: [
 {
 role: "OWNER",
 userByEmail: args.dataOwnerEmail
 },
 {
 role: "READER", 
 specialGroup: "projectReaders"
 }
 ],
 
 labels: {
 organization: organizationName.toLowerCase(),
 environbutt: environbutt,
 country: "sweden",
 gdpr_compliant: "true",
 data_residency: "nordic"
 }
 }, { provider: gcpProvider, parent: this });
 
 // Cloud Function for Swedish GDPR data processing
 const functionSourceBucket = new gcp.storage.Bucket(`${name}-function-source`, {
 name: `${organizationName}-${environbutt}-function-source`,
 location: "EUROPE-NORTH1",
 uniformBucketLevelAccess: true,
 labels: {
 purpose: "cloud-function-source",
 data_residency: "sweden"
 }
 }, { provider: gcpProvider, parent: this });
 
 const functionSourceObject = new gcp.storage.BucketObject(`${name}-function-zip`, {
 name: "Swedish-gdpr-processor.zip",
 bucket: functionSourceBucket.name,
 source: new pulumi.asset.FileAsset("./functions/Swedish-gdpr-processor.zip")
 }, { provider: gcpProvider, parent: this });
 
 this.cloudFunction = new gcp.cloudfunctions.Function(`${name}-gdpr-processor`, {
 name: `${organizationName}-gdpr-processor-${environbutt}`,
 description: "GDPR data processing function for Swedish organizationen",
 runtime: "nodejs18",
 availableMemoryMb: 256,
 timeout: 60,
 entryPoint: "processGDPRRequest",
 region: "europe-north1",
 
 sourceArchiveBucket: functionSourceBucket.name,
 sourceArchiveObject: functionSourceObject.name,
 
 httpsTrigger: {},
 
 environbuttVariables: {
 ENVIRONbutT: environbutt,
 DATA_CLASSIFICATION: dataClassification,
 GDPR_ENABLED: "true",
 SWEDISH_TIMEZONE: "Europe/Stockholm",
 BIGQUERY_DATASET: this.bigQueryDataset.datasetId,
 COMPLIANCE_MODE: "Swedish-gdpr"
 },
 
 labels: {
 organization: organizationName.toLowerCase(),
 environbutt: environbutt,
 function_type: "gdpr_processor",
 data_residency: "sweden"
 }
 }, { provider: gcpProvider, parent: this });
 
 this.registerOutputs({
 networkId: this.network.id,
 bigQueryDatasetId: this.bigQueryDataset.datasetId,
 cloudFunctionUrl: this.cloudFunction.httpsTriggerUrl
 });
 }
}

// Main multi-cloud deployment
const awsInfra = new AWSInfrastructure("aws-primary", {
 allowedIpRanges: config.getObject<string[]>("allowedIpRanges") || ["0.0.0.0/0"]
});

const azureInfra = new AzureInfrastructure("azure-dr", {
 sqlAdminPassword: config.requireSecret("sqlAdminPassword")
});

const gcpInfra = new GCPInfrastructure("gcp-analytics", {
 dataOwnerEmail: config.require("dataOwnerEmail")
});

// Cross-cloud monitoring setup
const crossCloudMonitoring = new kubernetes.core.v1.Namespace("cross-cloud-monitoring", {
 metadata: {
 name: "monitoring",
 labels: {
 "app.kubernetes.io/managed-by": "pulumi",
 "Swedish.se/monitoring-type": "cross-cloud"
 }
 }
});

// Export key outputs for cross-provider integration
export const multiCloudEndpoints = {
 aws: {
 apiGatewayUrl: awsInfra.apiGateway.executionArn,
 vpcId: awsInfra.vpc.id
 },
 azure: {
 appServiceUrl: azureInfra.appService.defaultHostName.apply(hostname => `https://${hostname}`),
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
 azure: "Sweden Central",
 gcp: "europe-north1 (Finland)"
 },
 encryptionEnabled: true,
 auditLoggingEnabled: true,
 crossCloudBackupEnabled: true
};
```

## Serverless infrastructure

Serverless Infrastructure as Code fokuserar on function definitions, event triggers, and managed service configurations istället for traditional server managebutt. This approach reducerar operationell overhead and enables automatic scaling baserat on actual usage patterns.

Event-driven architectures is implebutted through cloud functions, message queues, and data streams definierade that Architecture as Code. Integration between services is managed through IAM policies, API definitions, and network configurations that ensures security and performance requirebutts.

### Function-as-a-Service (FaaS) patterns for Swedish organizations

Serverless funktioner utgör kärnan in modern cloud-native arkitektur and enables unprecedented skalbarhet and kostnadseffektivitet. For Swedish organizations innebär FaaS-patterns to infrastrukturdefinitioner fokuserar on business logic istället for underlying compute reSources:

```yaml
# Serverless.yml
# Serverless Framework for Swedish organizations

service: Swedish-org-serverless
frameworkVersion: '3'

provider:
 name: aws
 runtime: nodejs18.x
 region: eu-north-1 # Stockholm region for Swedish data residency
 stage: ${opt:stage, 'development'}
 memorySize: 256
 timeout: 30
 
 # Swedish environbutt variables
 environbutt:
 STAGE: ${self:provider.stage}
 REGION: ${self:provider.region}
 DATA_CLASSIFICATION: ${env:DATA_CLASSIFICATION, 'internal'}
 GDPR_ENABLED: true
 SWEDISH_TIMEZONE: Europe/Stockholm
 COST_CENTER: ${env:COST_CENTER}
 ORGANIZATION: ${env:ORGANIZATION_NAME}
 COMPLIANCE_REQUIREbutTS: ${env:COMPLIANCE_REQUIREbutTS, 'gdpr'}
 
 # IAM Roles for Swedish säkerhetskrav
 iam:
 role:
 statebutts:
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
 
 # VPC configuration for Swedish säkerhetskrav
 vpc:
 securityGroupIds:
 - ${env:SECURITY_GROUP_ID}
 subnetIds:
 - ${env:PRIVATE_SUBNET_1_ID}
 - ${env:PRIVATE_SUBNET_2_ID}
 
 # CloudWatch Logs for GDPR compliance
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
 Environbutt: ${self:provider.stage}
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
 description: GDPR data subject rights API for Swedish organizationen
 memorySize: 512
 timeout: 60
 reservedConcurrency: 50
 environbutt:
 GDPR_TABLE_NAME: ${self:service}-${self:provider.stage}-gdpr-requests
 AUDIT_TABLE_NAME: ${self:service}-${self:provider.stage}-audit-log
 ENCRYPTION_KEY_ARN: ${env:GDPR_KMS_KEY_ARN}
 DATA_RETENTION_DAYS: ${env:DATA_RETENTION_DAYS, '90'}
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
 description: Audit logging for Swedish compliance-requirements
 memorySize: 256
 timeout: 30
 environbutt:
 AUDIT_TABLE_NAME: ${self:service}-${self:provider.stage}-audit-log
 LOG_RETENTION_YEARS: ${env:LOG_RETENTION_YEARS, '7'}
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
 ComplianceType: Swedish-Requirebutts

 # Kostnadskontroll for Swedish organizations
 costMonitoring:
 handler: src/handlers/cost.monitoringHandler
 description: Kostnadskontroll and budgetvarningar for Swedish organizations
 memorySize: 256
 timeout: 120
 environbutt:
 BUDGET_TABLE_NAME: ${self:service}-${self:provider.stage}-budgets
 NOTIFICATION_TOPIC_ARN: ${env:COST_NOTIFICATION_TOPIC_ARN}
 SWEDISH_CURRENCY: SEK
 COST_ALLOCATION_TAGS: Environbutt,CostCenter,Organization
 events:
 - schedule:
 rate: cron(0 8 * * ? *) # 08:00 svensk tid varje dag
 description: Daglig kostnadskontroll for Swedish organizationen
 input:
 checkType: daily
 currency: SEK
 timezone: Europe/Stockholm
 - schedule:
 rate: cron(0 8 ? * MON *) # 08:00 måndagar for veckorapport
 description: Veckovis kostnadskontroll
 input:
 checkType: weekly
 generateReport: true
 tags:
 Function: Cost-Monitoring
 Schedule: Daily-Weekly
 Currency: SEK

 # Swedish data processing pipeline
 dataprocessor:
 handler: src/handlers/data.processingHandler
 description: Data processing pipeline for Swedish organizations
 memorySize: 1024
 timeout: 900 # 15 minuter for batch processing
 reservedConcurrency: 10
 environbutt:
 DATA_BUCKET_NAME: ${env:DATA_BUCKET_NAME}
 processED_BUCKET_NAME: ${env:processED_BUCKET_NAME}
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
 - ${env:PANDAS_LAYER_ARN} # Data processing libraries
 tags:
 Function: Data-processing
 DataType: Batch-processing
 AnonymizationEnabled: true

# Swedish DynamoDB tables
reSources:
 ReSources:
 # GDPR requests table
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
 Value: ${env:DATA_RETENTION_DAYS, '90'}-days
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
 Value: Swedish-Requirebutts

 # Dead Letter Queue for Swedish error handling
 AuditDLQ:
 Type: AWS::SQS::Queue
 Properties:
 QueueName: ${self:service}-${self:provider.stage}-audit-dlq
 MessageRetentionPeriod: 1209600 # 14 dagar
 KmsMasterKeyId: ${env:AUDIT_KMS_KEY_ARN}
 Tags:
 - Key: Purpose
 Value: Dead-Letter-Queue
 - Key: Component
 Value: Audit-System

 # CloudWatch Dashboard for Swedish monitoring
 ServerlessMonitoringDashboard:
 Type: AWS::CloudWatch::Dashboard
 Properties:
 DashboardName: ${self:service}-${self:provider.stage}-Swedish-monitoring
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
 [ "AWS/Lambda", "Invocations", "FunctionName", "${GdprDataSubjectAPILambdaFunction}" ],
 [ ".", "Errors", ".", "." ],
 [ ".", "Duration", ".", "." ]
 ],
 "view": "timeSeries",
 "stacked": false,
 "region": "${AWS::Region}",
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
 [ "AWS/DynamoDB", "ConsumedReadCapacityUnits", "TableName", "${GdprRequestsTable}" ],
 [ ".", "ConsumedWriteCapacityUnits", ".", "." ]
 ],
 "view": "timeSeries",
 "stacked": false,
 "region": "${AWS::Region}",
 "title": "GDPR Table Capacity",
 "period": 300
 }
 }
 ]
 }

 Outputs:
 GdprApiEndpoint:
 Description: GDPR API endpoint for Swedish data subject requests
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
 "gdprCompliant": true,
 "dataResidency": "Sweden",
 "auditLoggingEnabled": true,
 "encryptionEnabled": true,
 "retentionPolicies": {
 "gdprData": "${env:DATA_RETENTION_DAYS, '90'} days",
 "auditLogs": "7 years"
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

# Custom configuration for Swedish organizations
custom:
 # Webpack for optimized bundles
 webpack:
 webpackConfig: 'webpack.config.js'
 includeModules: true
 packager: 'npm'
 excludeFiles: src/**/*.test.js

 # Domain managebutt for Swedish domains
 customDomain:
 domainName: ${env:CUSTOM_DOMAIN_NAME, ''}
 stage: ${self:provider.stage}
 certificateName: ${env:SSL_CERTIFICATE_NAME, ''}
 createRoute53Record: true
 endpointType: 'regional'
 securityPolicy: tls_1_2
 apiType: rest

 # Automated pruning for cost optimization
 prune:
 automatic: true
 number: 5 # Behåll 5 senaste versionerna

 # CloudWatch Alerts for Swedish monitoring
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
 threshold: 10000 # 10 sekunder
 statistic: Average
 period: 300
 evaluationPeriods: 2
 comparisonOperator: GreaterThanThreshold
 alarms:
 - functionErrors
 - functionDuration
```

### Event-driven arkitektur for Swedish organizations

Event-driven arkitekturer utgör grunden for modern serverless systems and enables loose coupling between services. For Swedish organizations innebär This särskild fokus on GDPR-compliant event processing and audit trails:

```python
# Serverless/event_processing.py
# Event-driven architecture for Swedish organizations with GDPR compliance

import json
import boto3
import logging
import os
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

# Configuration for Swedish organizations
SWEDISH_TIMEZONE = 'Europe/Stockholm'
ORGANIZATION_NAME = os.environ.get('ORGANIZATION_NAME', 'Swedish-org')
ENVIRONbutT = os.environ.get('ENVIRONbutT', 'development')
GDPR_ENABLED = os.environ.get('GDPR_ENABLED', 'true').lower() == 'true'
DATA_CLASSIFICATION = os.environ.get('DATA_CLASSIFICATION', 'internal')

# AWS clients with Swedish configuration
dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
sns = boto3.client('sns', region_name='eu-north-1')
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
 GDPR_DATA_REQUEST = "gdpr.data_request"
 GDPR_DATA_DELETION = "gdpr.data_deletion"
 GDPR_DATA_RECTIFICATION = "gdpr.data_rectification"
 GDPR_DATA_PORTABILITY = "gdpr.data_portability"
 USER_REGISTRATION = "user.registration"
 USER_LOGIN = "user.login"
 USER_LOGOUT = "user.logout"
 DATA_processING = "data.processing"
 AUDIT_LOG = "audit.log"
 COST_ALERT = "cost.alert"
 SECURITY_INCIDENT = "security.incident"

@dataclass
class SwedishEvent:
 """Standardiserad event structure for Swedish organizations"""
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
 """Validera Swedish GDPR-requirements"""
 if self.data_classification in ['personal', 'sensitive'] and not self.data_subject_id:
 raise ValueError("Data subject ID krävs for personal/sensitive data")
 
 if GDPR_ENABLED and self.data_classification == 'personal' and not self.gdpr_lawful_basis:
 raise ValueError("GDPR lawful basis krävs for personal data processing")

class SwedishEventprocessor:
 """Event processor for Swedish organizations with GDPR compliance"""
 
 def __init__(self):
 self.event_table = dynamodb.Table(f'{ORGANIZATION_NAME}-{ENVIRONbutT}-events')
 self.audit_table = dynamodb.Table(f'{ORGANIZATION_NAME}-{ENVIRONbutT}-audit-log')
 self.gdpr_table = dynamodb.Table(f'{ORGANIZATION_NAME}-{ENVIRONbutT}-gdpr-requests')
 
 def process_event(self, event: SwedishEvent) -> Dict[str, Any]:
 """process event with Swedish compliance-requirements"""
 try:
 # Log event for audit trail
 self._audit_log_event(event)
 
 # Spara event in DynamoDB
 self._store_event(event)
 
 # process baserat on event type
 result = self._route_event(event)
 
 # GDPR-specific processing
 if GDPR_ENABLED and event.data_classification in ['personal', 'sensitive']:
 self._process_gdpr_requirebutts(event)
 
 logger.info(f"Successfully processed event {event.event_id} of type {event.event_type.value}")
 return {"status": "success", "event_id": event.event_id, "result": result}
 
 except Exception as e:
 logger.error(f"Error processing event {event.event_id}: {str(e)}")
 self._handle_event_error(event, e)
 raise
 
 def _audit_log_event(self, event: SwedishEvent) -> None:
 """Skapa audit log entry for Swedish compliance"""
 audit_entry = {
 'audit_id': f"audit-{event.event_id}",
 'timestamp': event.timestamp,
 'event_type': event.event_type.value,
 'source': event.source,
 'data_subject_id': event.data_subject_id,
 'data_classification': event.data_classification,
 'gdpr_lawful_basis': event.gdpr_lawful_basis,
 'organization': ORGANIZATION_NAME,
 'environbutt': ENVIRONbutT,
 'compliance_flags': {
 'gdpr_processed': GDPR_ENABLED,
 'audit_logged': True,
 'data_residency': 'Sweden',
 'encryption_used': True
 },
 'retention_until': self._calculate_retention_date(event.data_classification),
 'ttl': self._calculate_ttl(event.data_classification)
 }
 
 self.audit_table.put_item(Item=audit_entry)
 
 def _store_event(self, event: SwedishEvent) -> None:
 """Spara event in DynamoDB with Swedish kryptering"""
 event_item = {
 'event_id': event.event_id,
 'event_type': event.event_type.value,
 'timestamp': event.timestamp,
 'source': event.source,
 'data_subject_id': event.data_subject_id,
 'data_classification': event.data_classification,
 'gdpr_lawful_basis': event.gdpr_lawful_basis,
 'payload': json.dumps(event.payload),
 'metadata': event.metadata,
 'ttl': self._calculate_ttl(event.data_classification)
 }
 
 self.event_table.put_item(Item=event_item)
 
 def _route_event(self, event: SwedishEvent) -> Dict[str, Any]:
 """Route event to appropriate processor"""
 processors = {
 EventType.GDPR_DATA_REQUEST: self._process_gdpr_request,
 EventType.GDPR_DATA_DELETION: self._process_gdpr_deletion,
 EventType.GDPR_DATA_RECTIFICATION: self._process_gdpr_rectification,
 EventType.GDPR_DATA_PORTABILITY: self._process_gdpr_portability,
 EventType.USER_REGISTRATION: self._process_user_registration,
 EventType.DATA_processING: self._process_data_processing,
 EventType.COST_ALERT: self._process_cost_alert,
 EventType.SECURITY_INCIDENT: self._process_security_incident
 }
 
 processor = processors.get(event.event_type, self._default_processor)
 return processor(event)
 
 def _process_gdpr_request(self, event: SwedishEvent) -> Dict[str, Any]:
 """process GDPR data subject request according to Swedish requirements"""
 request_data = event.payload
 
 # Validera GDPR request format
 required_fields = ['request_type', 'data_subject_email', 'verification_token']
 if not all(field in request_data for field in required_fields):
 raise ValueError("Invalid GDPR request format")
 
 # Skapa GDPR request entry
 gdpr_request = {
 'request_id': f"gdpr-{event.event_id}",
 'timestamp': event.timestamp,
 'request_type': request_data['request_type'],
 'data_subject_id': event.data_subject_id,
 'data_subject_email': request_data['data_subject_email'],
 'verification_token': request_data['verification_token'],
 'status': 'pending',
 'lawful_basis_used': event.gdpr_lawful_basis,
 'processing_deadline': self._calculate_gdpr_deadline(),
 'organization': ORGANIZATION_NAME,
 'environbutt': ENVIRONbutT,
 'metadata': {
 'source_ip': request_data.get('source_ip'),
 'user_agent': request_data.get('user_agent'),
 'swedish_locale': True,
 'data_residency': 'Sweden'
 }
 }
 
 self.gdpr_table.put_item(Item=gdpr_request)
 
 # Skicka notification to GDPR team
 self._send_gdpr_notification(gdpr_request)
 
 return {
 "request_id": gdpr_request['request_id'],
 "status": "created",
 "processing_deadline": gdpr_request['processing_deadline']
 }
 
 def _process_gdpr_deletion(self, event: SwedishEvent) -> Dict[str, Any]:
 """process GDPR data deletion according to Swedish requirements"""
 deletion_data = event.payload
 data_subject_id = event.data_subject_id
 
 # Lista all databaser and tabor that can innehålla personal data
 data_stores = [
 {'type': 'dynamodb', 'table': f'{ORGANIZATION_NAME}-{ENVIRONbutT}-users'},
 {'type': 'dynamodb', 'table': f'{ORGANIZATION_NAME}-{ENVIRONbutT}-profiles'},
 {'type': 'dynamodb', 'table': f'{ORGANIZATION_NAME}-{ENVIRONbutT}-activities'},
 {'type': 's3', 'bucket': f'{ORGANIZATION_NAME}-{ENVIRONbutT}-user-data'},
 {'type': 'rds', 'database': f'{ORGANIZATION_NAME}_production'}
 ]
 
 deletion_results = []
 
 for store in data_stores:
 try:
 if store['type'] == 'dynamodb':
 result = self._delete_from_dynamodb(store['table'], data_subject_id)
 elif store['type'] == 's3':
 result = self._delete_from_s3(store['bucket'], data_subject_id)
 elif store['type'] == 'rds':
 result = self._delete_from_rds(store['database'], data_subject_id)
 
 deletion_results.append({
 'store': store,
 'status': 'success',
 'records_deleted': result.get('deleted_count', 0)
 })
 
 except Exception as e:
 deletion_results.append({
 'store': store,
 'status': 'error',
 'error': str(e)
 })
 logger.error(f"Error deleting from {store}: {str(e)}")
 
 # Log deletion for audit
 deletion_audit = {
 'deletion_id': f"deletion-{event.event_id}",
 'timestamp': event.timestamp,
 'data_subject_id': data_subject_id,
 'deletion_results': deletion_results,
 'total_stores_processed': len(data_stores),
 'successful_deletions': sum(1 for r in deletion_results if r['status'] == 'success'),
 'gdpr_compliant': all(r['status'] == 'success' for r in deletion_results)
 }
 
 self.audit_table.put_item(Item=deletion_audit)
 
 return deletion_audit
 
 def _process_cost_alert(self, event: SwedishEvent) -> Dict[str, Any]:
 """process cost alert for Swedish budgetkontroll"""
 cost_data = event.payload
 
 # Konvertera to Swedish kronor om nödvändigt
 if cost_data.get('currency') != 'SEK':
 sek_amount = self._convert_to_sek(
 cost_data['amount'], 
 cost_data.get('currency', 'USD')
 )
 cost_data['amount_sek'] = sek_amount
 
 # Skapa svensk cost alert
 alert_message = self._format_swedish_cost_alert(cost_data)
 
 # Skicka to Swedish notification channels
 sns.publish(
 TopicArn=os.environ.get('COST_ALERT_TOPIC_ARN'),
 Subject=f"Kostnadsvarning - {ORGANIZATION_NAME} {ENVIRONbutT}",
 Message=alert_message,
 MessageAttributes={
 'Organization': {'DataType': 'String', 'StringValue': ORGANIZATION_NAME},
 'Environbutt': {'DataType': 'String', 'StringValue': ENVIRONbutT},
 'AlertType': {'DataType': 'String', 'StringValue': 'cost'},
 'Currency': {'DataType': 'String', 'StringValue': 'SEK'},
 'Language': {'DataType': 'String', 'StringValue': 'Swedish'}
 }
 )
 
 return {
 "alert_sent": True,
 "currency": "SEK",
 "amount": cost_data.get('amount_sek', cost_data['amount'])
 }
 
 def _calculate_retention_date(self, data_classification: str) -> str:
 """Beräkna retention date according to Swedish lagkrav"""
 retention_periods = {
 'public': 365, # 1 år
 'internal': 1095, # 3 år 
 'personal': 2555, # 7 år according to bokföringslagen
 'sensitive': 2555, # 7 år
 'financial': 2555 # 7 år according to bokföringslagen
 }
 
 days = retention_periods.get(data_classification, 365)
 retention_date = datetime.now(timezone.utc) + timedelta(days=days)
 return retention_date.isoformat()
 
 def _calculate_ttl(self, data_classification: str) -> int:
 """Beräkna TTL for DynamoDB according to Swedish requirements"""
 current_time = int(datetime.now(timezone.utc).timestamp())
 retention_days = {
 'public': 365,
 'internal': 1095,
 'personal': 2555,
 'sensitive': 2555,
 'financial': 2555
 }
 
 days = retention_days.get(data_classification, 365)
 return current_time + (days * 24 * 60 * 60)
 
 def _format_swedish_cost_alert(self, cost_data: Dict[str, Any]) -> str:
 """Formatera cost alert on Swedish"""
 return f"""
Kostnadsvarning for {ORGANIZATION_NAME}

Miljö: {ENVIRONbutT}
Aktuell kostnad: {cost_data.get('amount_sek', cost_data['amount']):.2f} SEK
Budget: {cost_data.get('budget_sek', cost_data.get('budget', 'N/A'))} SEK
Procent of budget: {cost_data.get('percentage', 'N/A')}%

Datum: {datetime.now().strftime('%Y-%m-%d %H:%M')} (svensk tid)

Kostnadscenter: {cost_data.get('cost_center', 'N/A')}
Tjänster: {', '.join(cost_data.get('services', []))}

for mer information, kontakta IT-avdelningen.
 """.strip()

# Lambda function handlers for Swedish event processing
def gdpr_event_handler(event, context):
 """Lambda handler for GDPR events"""
 processor = SwedishEventprocessor()
 
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
 return {"processed_events": len(results), "results": results}
 else:
 # Direct invocation
 swedish_event = SwedishEvent(**event)
 result = processor.process_event(swedish_event)
 return result
 
 except Exception as e:
 logger.error(f"Error in GDPR event handler: {str(e)}")
 return {
 "status": "error",
 "error": str(e),
 "event_id": event.get('event_id', 'unknown')
 }

def cost_monitoring_handler(event, context):
 """Lambda handler for Swedish cost monitoring"""
 processor = SwedishEventprocessor()
 
 try:
 # Hämta aktuella kostnader from Cost Explorer
 cost_explorer = boto3.client('ce', region_name='eu-north-1')
 
 end_date = datetime.now().strftime('%Y-%m-%d')
 start_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
 
 response = cost_explorer.get_cost_and_usage(
 TimePeriod={'Start': start_date, 'End': end_date},
 Granularity='DAILY',
 Metrics=['BlendedCost'],
 GroupBy=[
 {'Type': 'DIbutSION', 'Key': 'SERVICE'},
 {'Type': 'TAG', 'Key': 'Environbutt'},
 {'Type': 'TAG', 'Key': 'CostCenter'}
 ]
 )
 
 # Skapa cost event
 cost_event = SwedishEvent(
 event_id=f"cost-{int(datetime.now().timestamp())}",
 event_type=EventType.COST_ALERT,
 timestamp=datetime.now(timezone.utc).isoformat(),
 source="aws-cost-monitoring",
 data_subject_id=None,
 data_classification="internal",
 gdpr_lawful_basis=None,
 payload={
 "cost_data": response,
 "currency": "USD",
 "date_range": {"start": start_date, "end": end_date}
 },
 metadata={
 "organization": ORGANIZATION_NAME,
 "environbutt": ENVIRONbutT,
 "monitoring_type": "daily"
 }
 )
 
 result = processor.process_event(cost_event)
 return result
 
 except Exception as e:
 logger.error(f"Error in cost monitoring handler: {str(e)}")
 return {"status": "error", "error": str(e)}
```

## Practical Architecture as Code-implebuttationsexempel

for to demonstrera molnArchitecture as Code in the practice for Swedish organizations, presenteras här kompletta implebuttationsexempel that visar how real-world scenarios can lösas:

### Implebuttationsexempel 1: Swedish e-handelslösning

```terraform
# Terraform/ecommerce-platform/main.tf
# Komplett e-handelslösning for Swedish organizations

module "Swedish_ecommerce_infrastructure" {
 source = "./modules/ecommerce"
 
 # organizationskonfiguration
 organization_name = "Swedish-handel"
 environbutt = var.environbutt
 region = "eu-north-1" # Stockholm for Swedish data residency
 
 # GDPR and compliance-requirements
 gdpr_compliance_enabled = true
 data_residency_region = "Sweden"
 audit_logging_enabled = true
 encryption_at_rest = true
 
 # E-handelsspecific requirements
 enable_paybutt_processing = true
 enable_inventory_managebutt = true
 enable_customer_analytics = true
 enable_gdpr_customer_portal = true
 
 # Swedish lokaliseringskrav
 supported_languages = ["sv", "en"]
 default_currency = "SEK"
 tax_calculation_rules = "swedish_vat"
 
 # Säkerhet and prestanda
 enable_waf = true
 enable_ddos_protection = true
 enable_cdn = true
 ssl_certificate_domain = var.domain_name
 
 # Backup and disaster recovery
 backup_retention_days = 90
 enable_cross_region_backup = true
 disaster_recovery_region = "eu-central-1"
 
 tags = {
 Project = "Swedish-Ecommerce"
 BusinessUnit = "Retail"
 CostCenter = "CC-RETAIL-001"
 Compliance = "GDPR,PCI-DSS"
 DataType = "Customer,Paybutt,Inventory"
 }
}
```

### Implebuttationsexempel 2: Swedish healthtech-platform

```yaml
# Kubernetes/healthtech-platform.yaml
# Kubernetes deployment for Swedish healthtech with särskilda säkerhetskrav

apiVersion: v1
kind: Namespace
metadata:
 name: Swedish-healthtech
 labels:
 app.kubernetes.io/name: Swedish-healthtech
 Swedish.se/data-classification: "sensitive"
 Swedish.se/gdpr-compliant: "true"
 Swedish.se/hipaa-compliant: "true"
 Swedish.se/patient-data: "true"
---
apiVersion: apps/v1
kind: Deploybutt
metadata:
 name: patient-portal
 namespace: Swedish-healthtech
spec:
 replicas: 3
 selector:
 matchLabels:
 app: patient-portal
 template:
 metadata:
 labels:
 app: patient-portal
 Swedish.se/component: "patient-facing"
 Swedish.se/data-access: "patient-data"
 spec:
 securityContext:
 runAsNonRoot: true
 runAsUser: 1000
 fsGroup: 2000
 containers:
 - name: patient-portal
 image: Swedish-healthtech/patient-portal:v1.2.0
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
 value: "enabled"
 - name: SWEDISH_LOCALE
 value: "sv_SE.UTF-8"
 securityContext:
 allowPrivilegeEscalation: false
 readOnlyRootFilesystem: true
 capabilities:
 drop:
 - ALL
 reSources:
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
 readinessProbe:
 httpGet:
 path: /ready
 port: 8080
 initialDelaySeconds: 5
 periodSeconds: 5
```

## Sammanfattning

Den moderna Architecture as Code-methodologyen representerar framtiden for infrastrukturhantering in Swedish organizations.
MolnArchitecture as Code representerar en fundamental evolution of Infrastructure as Code for Swedish organizations that opererar in cloud-native miljöer. Through to utnyttja cloud provider-specific tjänster and capabilities can organizations uppnå unprecedented skalbarhet, resiliens and kostnadseffektivitet as well asidigt that Swedish compliance-requirements uppfylls.

De olika cloud provider-ecosystebut - AWS, Azure, and Google Cloud Platform - erbjuder var sitt unika värde for Swedish organizations. AWS dominerar through comprehensive tjänsteportfölj and stark närvaro in Stockholm-regionen. Azure attraherar Swedish enterprise-organizations through stark Microsoft-integration and Sweden Central datacenter. Google Cloud Platform lockar innovationsorganizations with their machine learning capabilities and advanced analytics services.

Multi-cloud strategier enables optimal distribution of workloads for to maximera prestanda, minimera kostnader and säkerställa resiliens. Tools that Terraform and Pulumi abstraherar provider-specific skillnader and enables konsistent managebutt across olika cloud environbutts. For Swedish organizations innebär This möjligheten to kombinera AWS for primary workloads, Azure for disaster recovery, and Google Cloud for analytics and machine learning.

Serverless arkitekturer revolutionerar how Swedish organizations tänker kring infrastructure managebutt through to eliminera traditional server administration and enablesa automatic scaling baserat on actual demand. Function-as-a-Service patterns, event-driven architectures, and managed services reducerar operational overhead as well asidigt that de ensures GDPR compliance through built-in security and audit capabilities.

Container-first approaches with Kubernetes that orchestration platform utgör grunden for modern cloud-native applications. For Swedish organizations enables This portable workloads that can köras across olika cloud providers as well asidigt that consistent security policies and compliance requirebutts upprätthålls.

Hybrid cloud implebuttations kombinerar on-premises infrastructure with public cloud services for Swedish organizations that have legacy systems or specific regulatory requirebutts. This approach enables gradual cloud migration as well asidigt that känslig data can behållas within Swedish gränser according to data residency requirebutts.

Swedish organizations that implebutterar molnArchitecture as Code can uppnå significant competitive advantages through reduced time-to-market, improved scalability, enhanced security, and optimized costs. As well asidigt ensures proper implebuttation of Infrastructure as Code patterns to GDPR compliance, svensk data residency, and other regulatory requirebutts uppfylls automatically that en del of deployment processesna.

Investbutt in molnArchitecture as Code betalar sig through improved developer productivity, reduced operational overhead, enhanced system reliability, and better disaster recovery capabilities. That vi will to se in [chapter 6 om säkerhet](06_kapitel5.md), is these benefits särskilt viktiga när security and compliance requirebutts integreras that en natural del of infrastructure definition and deployment processes.

Sources:
- AWS. "Infrastructure as Code on AWS." Amazon Web Services Architecture Center.
- Google Cloud. "Infrastructure as Code Architecture as Code best practices." Google Cloud Docubuttation.
- Microsoft Azure. "Azure Resource Manager Templates." Azure Docubuttation.
- HashiCorp. "Terraform Multi-Cloud Infrastructure." HashiCorp Learn Platform.
- Pulumi. "Cloud Programming Model." Pulumi Docubuttation.
- Kubernetes. "Cloud Native Applications." Cloud Native Computing Foundation.
- GDPR.eu. "GDPR Compliance for Cloud Infrastructure." GDPR Guidelines.
- Swedish Data Protection Authority. "Cloud Services and Data Protection." Datainspektionen Guidelines.