import * as cdk from 'aws-cdk-lib';
import * as elasticache from 'aws-cdk-lib/aws-elasticache';
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';
import { Construct } from 'constructs';
import { CacheStackProps } from './types';
import { config } from './config';

export class CacheStack extends cdk.Stack {
  public readonly redisReplicationGroup: elasticache.CfnReplicationGroup;
  public readonly redisSubnetGroup: elasticache.CfnSubnetGroup;

  constructor(scope: Construct, id: string, props: CacheStackProps) {
    super(scope, id, props);

    // ============================================
    // Subnet group (PRIVATE_ISOLATED)
    // ============================================
    const isolatedSubnets = props.vpc.isolatedSubnets.map(
      subnet => subnet.subnetId
    );

    this.redisSubnetGroup = new elasticache.CfnSubnetGroup(
      this,
      'RedisSubnetGroup',
      {
        description: 'Subnet group for Redis',
        subnetIds: isolatedSubnets,
      }
    );

    // ============================================
    // Redis Secret
    // ============================================
    const redisSecret = secretsmanager.Secret.fromSecretNameV2(
      this,
      'RedisSecret',
      props.redisSecretName
    );

    // ============================================
    // Redis Replication Group (AUTH + TLS)
    // ============================================
    this.redisReplicationGroup = new elasticache.CfnReplicationGroup(
      this,
      'RedisReplicationGroup',
      {
        replicationGroupDescription: 'Redis for Celery and caching',

        engine: 'redis',
        engineVersion: '7.0',
        cacheNodeType: config.redis.nodeType,

        numNodeGroups: 1,
        replicasPerNodeGroup: 1, // 1 primary + 1 replica

        cacheSubnetGroupName: this.redisSubnetGroup.ref,
        securityGroupIds: [props.redisSecurityGroup.securityGroupId],

        authToken: redisSecret
          .secretValueFromJson('authToken')
          .unsafeUnwrap(),
        // Enable transit encryption
        transitEncryptionEnabled: true,
        atRestEncryptionEnabled: true,

        automaticFailoverEnabled: true,
      }
    );

    this.redisReplicationGroup.addDependency(this.redisSubnetGroup);

    // ============================================
    // Outputs
    // ============================================
    new cdk.CfnOutput(this, 'RedisEndpoint', {
      value: this.redisReplicationGroup.attrPrimaryEndPointAddress,
      exportName: `${this.stackName}-RedisEndpoint`,
    });

    new cdk.CfnOutput(this, 'RedisPort', {
      value: this.redisReplicationGroup.attrPrimaryEndPointPort,
    });
  }
}
