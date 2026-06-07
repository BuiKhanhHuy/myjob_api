import * as cdk from 'aws-cdk-lib';
import * as rds from 'aws-cdk-lib/aws-rds';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';
import { Construct } from 'constructs';
import { DatabaseStackProps } from './types';
import { config } from './config';


/**
 * Parse RDS instance type from string like "db.t3.medium"
 * Returns instance class and size for RDS
 */
function parseRdsInstanceType(instanceTypeString: string): { instanceClass: ec2.InstanceClass; instanceSize: ec2.InstanceSize } {
  // Remove "db." prefix if present
  const type = instanceTypeString.replace(/^db\./, '');
  
  // Parse format: t3.medium -> InstanceClass.T3, InstanceSize.MEDIUM
  const parts = type.split('.');
  if (parts.length !== 2) {
    throw new Error(`Invalid instance type format: ${instanceTypeString}. Expected format: db.t3.medium`);
  }

  const [family, size] = parts;
  
  // Map family to InstanceClass
  const instanceClassMap: { [key: string]: ec2.InstanceClass } = {
    't3': ec2.InstanceClass.T3,
    't4g': ec2.InstanceClass.T4G,
    'm5': ec2.InstanceClass.M5,
    'm6i': ec2.InstanceClass.M6I,
    'r5': ec2.InstanceClass.R5,
    'r6i': ec2.InstanceClass.R6I,
  };

  const instanceClass = instanceClassMap[family.toLowerCase()];
  if (!instanceClass) {
    throw new Error(`Unsupported instance family: ${family}. Supported: ${Object.keys(instanceClassMap).join(', ')}`);
  }

  // Map size to InstanceSize
  const sizeMap: { [key: string]: ec2.InstanceSize } = {
    'micro': ec2.InstanceSize.MICRO,
    'small': ec2.InstanceSize.SMALL,
    'medium': ec2.InstanceSize.MEDIUM,
    'large': ec2.InstanceSize.LARGE,
    'xlarge': ec2.InstanceSize.XLARGE,
    '2xlarge': ec2.InstanceSize.XLARGE2,
    '4xlarge': ec2.InstanceSize.XLARGE4,
    '8xlarge': ec2.InstanceSize.XLARGE8,
    '12xlarge': ec2.InstanceSize.XLARGE12,
    '16xlarge': ec2.InstanceSize.XLARGE16,
    '24xlarge': ec2.InstanceSize.XLARGE24,
  };

  const instanceSize = sizeMap[size.toLowerCase()];
  if (!instanceSize) {
    throw new Error(`Unsupported instance size: ${size}. Supported: ${Object.keys(sizeMap).join(', ')}`);
  }

  return { instanceClass, instanceSize };
}

/**
 * Database Stack
 * Creates RDS MySQL instance with Multi-AZ configuration
 */
export class DatabaseStack extends cdk.Stack {
  public readonly dbInstance: rds.IDatabaseInstance;

  constructor(scope: Construct, id: string, props: DatabaseStackProps) {
    super(scope, id, props);

    // Get the secret from secretsmanager
    const dbSecret = secretsmanager.Secret.fromSecretNameV2(
      this,
      'RdsSecret',
      props.rdsSecretName
    );

    // ============================================
    // RDS MySQL Instance
    // ============================================
    this.dbInstance = new rds.DatabaseInstance(this, 'Database', {
      engine: rds.DatabaseInstanceEngine.mysql({
        version: rds.MysqlEngineVersion.VER_8_0,
      }),
      instanceType: (() => {
        const { instanceClass, instanceSize } = parseRdsInstanceType(config.database.instanceType);
        return ec2.InstanceType.of(instanceClass, instanceSize);
      })(),
      vpc: props.vpc,
      vpcSubnets: {
        subnetType: ec2.SubnetType.PRIVATE_ISOLATED,
      },
      securityGroups: [props.databaseSecurityGroup],
      credentials: rds.Credentials.fromSecret(dbSecret),
      databaseName: config.database.databaseName,
      allocatedStorage: config.database.allocatedStorage,
      maxAllocatedStorage: config.database.maxAllocatedStorage,
      multiAz: config.database.multiAz,
      backupRetention: cdk.Duration.days(config.database.backupRetentionDays),
      deletionProtection: false, // Set to true for production
      removalPolicy: cdk.RemovalPolicy.DESTROY, // Change to RETAIN for production
      storageEncrypted: true,
      enablePerformanceInsights: true,
      performanceInsightRetention: rds.PerformanceInsightRetention.MONTHS_1,
    });

    // ============================================
    // Outputs
    // ============================================
    new cdk.CfnOutput(this, 'DatabaseEndpoint', {
      value: this.dbInstance.instanceEndpoint.hostname,
      description: 'RDS MySQL Endpoint',
      exportName: `${this.stackName}-DatabaseEndpoint`,
    });

    new cdk.CfnOutput(this, 'DatabasePort', {
      value: this.dbInstance.instanceEndpoint.port.toString(),
      description: 'RDS MySQL Port',
    });

    new cdk.CfnOutput(this, 'DatabaseName', {
      value: config.database.databaseName,
      description: 'Database Name',
    });
  }
}

