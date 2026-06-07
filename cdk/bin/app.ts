#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { NetworkStack } from '../lib/network-stack';
import { DatabaseStack } from '../lib/database-stack';
import { CacheStack } from '../lib/cache-stack';
import { Ec2Stack } from '../lib/ec2-stack';
import { config } from '../lib/config';

const app = new cdk.App();

const enviromentName = app.node.tryGetContext('environment');
if (!enviromentName) {
  throw new Error('Environment is required. Run with: --context environment=production');
}

const env: cdk.Environment = {
  account: config.aws.account,
  region: config.aws.region,
};

const tags: { [key: string]: string } = {
  Project: config.tags.project,
  Environment: enviromentName,
  ManagedBy: 'CDK',
  Owner: config.tags.owner,
};
if (config.tags.costCenter) {
  tags.CostCenter = config.tags.costCenter;
}

const stackPrefix = `MyJob-${enviromentName}`;

// ============================================
// Phase 1: Network Infrastructure
// (dùng cho ECS deployment — không cần cho EC2 quick deploy)
// ============================================
const networkStack = new NetworkStack(app, `${stackPrefix}-Network`, {
  env,
  description: 'Network infrastructure with VPC, subnets, and security groups',
});

// ============================================
// Phase 2: Data Layer
// (dùng cho ECS deployment — không cần cho EC2 quick deploy)
// ============================================
const databaseStack = new DatabaseStack(app, `${stackPrefix}-Database`, {
  env,
  vpc: networkStack.vpc,
  databaseSecurityGroup: networkStack.databaseSecurityGroup,
  rdsSecretName: config.database.rdsSecretName,
  description: 'RDS MySQL database with Multi-AZ',
});

const cacheStack = new CacheStack(app, `${stackPrefix}-Cache`, {
  env,
  vpc: networkStack.vpc,
  redisSecurityGroup: networkStack.redisSecurityGroup,
  redisSecretName: config.redis.redisSecretName,
  description: 'ElastiCache Redis for Celery and caching',
});

// ============================================
// Phase 3: EC2 Quick Deploy
// EC2 + Docker Compose (Django + MySQL + Redis + Celery)
// Truy cập qua SSM Session Manager, không cần SSH key
// ============================================
const ec2Stack = new Ec2Stack(app, `${stackPrefix}-Ec2`, {
  env,
  description: 'EC2 instance running Django API via Docker Compose',
});

// ============================================
// Apply tags
// ============================================
// NOTE: DomainStack bị bỏ — buikhanhhuy.click nằm ở account khác.
// Sau khi deploy, lấy ElasticIpAddress từ output rồi tạo A record thủ công:
//   Route53 (account kia) → buikhanhhuy.click → Create record
//   Type: A | Name: api | Value: <ElasticIpAddress>
const activeStacks = [networkStack, databaseStack, cacheStack, ec2Stack];
activeStacks.forEach((stack) => {
  Object.entries(tags).forEach(([key, value]) => {
    cdk.Tags.of(stack).add(key, value);
  });
});

app.synth();
