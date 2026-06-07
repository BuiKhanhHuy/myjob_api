import * as cdk from 'aws-cdk-lib';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as rds from 'aws-cdk-lib/aws-rds';
import * as elasticache from 'aws-cdk-lib/aws-elasticache';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as elbv2 from 'aws-cdk-lib/aws-elasticloadbalancingv2';
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';
import * as acm from 'aws-cdk-lib/aws-certificatemanager';

/**
 * EC2 Stack Props
 */
export interface Ec2StackProps extends BaseStackProps {}

/**
 * Common stack properties interface
 */
export interface BaseStackProps extends cdk.StackProps {
  readonly env: cdk.Environment;
}

/**
 * Network Stack Props
 */
export interface NetworkStackProps extends BaseStackProps {}

/**
 * Secrets Stack Props
 */
export interface SecretsStackProps extends BaseStackProps {}

/**
 * Database Stack Props
 */
export interface DatabaseStackProps extends BaseStackProps {
  readonly vpc: ec2.IVpc;
  readonly databaseSecurityGroup: ec2.ISecurityGroup;
  readonly rdsSecretName: string;
}

/**
 * Cache Stack Props
 */
export interface CacheStackProps extends BaseStackProps {
  readonly vpc: ec2.IVpc;
  readonly redisSecurityGroup: ec2.ISecurityGroup;
  readonly redisSecretName: string;
}

/**
 * Load Balancer Stack Props
 */
export interface LoadBalancerStackProps extends BaseStackProps {
  readonly vpc: ec2.IVpc;
  readonly albSecurityGroup: ec2.ISecurityGroup;
}

/**
 * Domain Stack Props
 */
export interface DomainStackProps extends BaseStackProps {
  readonly domainName: string;
  readonly adminSubdomain: string;
  readonly apiSubdomain: string;
  readonly elasticIp: string;
}

/**
 * ECS Stack Props
 */
export interface EcsStackProps extends BaseStackProps {
  readonly vpc: ec2.IVpc;
  readonly ecsSecurityGroup: ec2.ISecurityGroup;
  readonly alb: elbv2.IApplicationLoadBalancer;
  readonly targetGroup: elbv2.IApplicationTargetGroup;
  readonly database: rds.IDatabaseInstance;
  readonly redisReplicationGroup: elasticache.CfnReplicationGroup;
  readonly certificate: acm.ICertificate;
  readonly adminDomain: string;
  readonly apiDomain: string;
  readonly environment: {
    APP_ENV: string;
    DEBUG: string;
    APPEND_SLASH: string;
    ALLOWED_HOSTS: string;
    CSRF_TRUSTED_ORIGINS: string;
    DB_ENGINE: string;
    DB_HOST: string;
    DB_NAME: string;
    DB_PASSWORD: string;
    DB_PORT: number;
    DB_USER: string;
    EMAIL_HOST: string;
    EMAIL_HOST_PASSWORD: string;
    EMAIL_HOST_USER: string;
    EMAIL_PORT: string;
    SERVICE_REDIS_HOST: string;
    SERVICE_REDIS_PASSWORD: string;
    SERVICE_REDIS_PORT: string;
    SERVICE_REDIS_USERNAME: string;
    SERVICE_REDIS_DB: string;
    SOCIAL_AUTH_FACEBOOK_KEY: string;
    SOCIAL_AUTH_FACEBOOK_SECRET: string;
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY: string;
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET: string;
    FIREBASE_API_KEY: string;
    FIREBASE_AUTH_DOMAIN: string;
    FIREBASE_PROJECT_ID: string;
    FIREBASE_STORAGE_BUCKET: string;
    FIREBASE_MESSAGING_SENDER_ID: string;
    FIREBASE_APP_ID: string;
    FIREBASE_CREDENTIALS_PATH: string;
    SMS_API_KEY: string;
    CLOUDINARY_CLOUD_NAME: string;
    CLOUDINARY_API_KEY: string;
    CLOUDINARY_API_SECRET: string;
    WEB_JOB_SEEKER_CLIENT_URL: string;
    WEB_EMPLOYER_CLIENT_URL: string;
  };
}

/**
 * Monitoring Stack Props
 */
export interface MonitoringStackProps extends BaseStackProps {
  readonly alb: elbv2.IApplicationLoadBalancer;
  readonly targetGroup: elbv2.IApplicationTargetGroup;
  readonly ecsCluster: ecs.ICluster;
  readonly djangoService: ecs.IBaseService;
  readonly celeryWorkerService: ecs.IBaseService;
  readonly database: rds.IDatabaseInstance;
  readonly redisReplicationGroup: elasticache.CfnReplicationGroup;
}

/**
 * Pipeline Stack Props
 */
export interface PipelineStackProps extends BaseStackProps {
  readonly ecsCluster: ecs.ICluster;
  readonly djangoService: ecs.IBaseService;
  readonly celeryWorkerService: ecs.IBaseService;
  readonly celeryBeatService: ecs.IBaseService;
}