import * as dotenv from 'dotenv';

// Load environment variables from .env file
// .env chỉ chứa service keys (Cloudinary, Firebase, SMS, etc.)
// AWS config (account, region) được hardcode trong config.ts hoặc lấy từ AWS context
dotenv.config();

/**
 * AWS Configuration
 */
export interface AwsConfig {
  account: string;
  region: string;
}

/**
 * Domain Configuration
 */
export interface DomainConfig {
  domainName: string;
  adminSubdomain: string;
  apiSubdomain: string;
}

/**
 * VPC Configuration
 */
export interface VpcConfig {
  cidr: string;
  maxAzs: number;
}

/**
 * Database Configuration
 */
export interface DatabaseConfig {
  instanceType: string;
  allocatedStorage: number;
  maxAllocatedStorage: number;
  databaseName: string;
  backupRetentionDays: number;
  multiAz: boolean;
  rdsSecretName: string;
}

/**
 * Redis Configuration
 */
export interface RedisConfig {
  nodeType: string;
  numCacheNodes: number;
  redisSecretName: string;
}

/**
 * ECS EC2 Configuration
 */
export interface EcsEc2Config {
  instanceType: string;
  minCapacity: number;
  maxCapacity: number;
  desiredCapacity: number;
}

/**
 * ECS Service Configuration
 */
export interface EcsServiceConfig {
  desiredCount: number;
  minCapacity: number;
  maxCapacity: number;
  cpu: number;
  memory: number;
}

/**
 * ECS Configuration
 */
export interface EcsConfig {
  launchType: 'EC2' | 'FARGATE';
  ec2: EcsEc2Config;
  django: EcsServiceConfig;
  celeryWorker: EcsServiceConfig;
  celeryBeat: EcsServiceConfig;
}

/**
 * Repository Configuration
 */
export interface RepositoryConfig {
  ecrRepositoryName: string;
  codeCommitRepositoryName: string;
  codeCommitBranch: string;
}

/**
 * Security Configuration
 */
export interface SecurityConfig {
  adminWhitelistIps: string[];
}

/**
 * CloudWatch Configuration
 */
export interface CloudWatchConfig {
  alarmEmail: string;
}

/**
 * EC2 Deployment Configuration
 */
export interface Ec2Config {
  instanceType: string;
  envSecretName: string;
  githubRepoUrl: string;
}

/**
 * Tags Configuration
 */
export interface TagsConfig {
  project: string;
  owner: string;
  costCenter?: string;
}

/**
 * Complete Application Configuration
 */
export interface AppConfig {
  aws: AwsConfig;
  domain: DomainConfig;
  vpc: VpcConfig;
  database: DatabaseConfig;
  redis: RedisConfig;
  ecs: EcsConfig;
  ec2: Ec2Config;
  repository: RepositoryConfig;
  security: SecurityConfig;
  cloudWatch: CloudWatchConfig;
  tags: TagsConfig;
}

/**
 * Load and validate application configuration
 * Infrastructure config được hardcode (không thay đổi nhiều, không sensitive)
 * Chỉ service keys được load từ .env
 */
export function loadConfig(): AppConfig {
  return {
    // ============================================
    // AWS Config
    // ============================================
    aws: {
      account: '225632393809',
      region: 'ap-southeast-1',
    },
    
    // ============================================
    // Domain Config
    // ============================================
    domain: {
      domainName: 'buikhanhhuy.click',
      adminSubdomain: 'admin',
      apiSubdomain: 'api',
    },
    
    // ============================================
    // VPC Config
    // ============================================
    vpc: {
      cidr: '10.0.0.0/16',
      maxAzs: 2,
    },

    // ============================================
    // Database Config
    // ============================================
    database: {
      instanceType: 'db.t3.medium',
      allocatedStorage: 100,
      maxAllocatedStorage: 500,
      databaseName: 'myjob_db',
      backupRetentionDays: 7,
      multiAz: true,
      rdsSecretName: '/myjob/production/db/secret',
    },
    
    // ============================================
    // Redis Config
    // ============================================
    redis: {
      nodeType: 'cache.t3.micro',
      numCacheNodes: 1,
      redisSecretName: '/myjob/production/redis/secret',
    },
    
    // ============================================
    // ECS Config
    // ============================================
    ecs: {
      launchType: 'EC2',
      ec2: {
        instanceType: 't3.medium',
        minCapacity: 2,
        maxCapacity: 5,
        desiredCapacity: 2,
      },
      django: {
        desiredCount: 2,
        minCapacity: 2,
        maxCapacity: 10,
        cpu: 512,
        memory: 1024,
      },
      celeryWorker: {
        desiredCount: 2,
        minCapacity: 2,
        maxCapacity: 8,
        cpu: 1024,
        memory: 2048,
      },
      celeryBeat: {
        desiredCount: 1,
        minCapacity: 1,
        maxCapacity: 1,
        cpu: 256,
        memory: 512,
      },
    },
    
    // ============================================
    // EC2 Quick Deploy Config
    // ============================================
    ec2: {
      instanceType: 't3.small', // Free Tier eligible (ap-southeast-1) — 2GB RAM
      envSecretName: 'myjob/production/env', // AWS Secrets Manager secret chứa nội dung file .env
      githubRepoUrl: 'https://github.com/BuiKhanhHuy/myjob_api.git',
    },

    // ============================================
    // Repository Config
    // ============================================
    repository: {
      ecrRepositoryName: 'myjob-api',
      codeCommitRepositoryName: 'myjob-api',
      codeCommitBranch: 'main',
    },
    
    // ============================================
    // Security Config
    // ============================================
    security: {
      adminWhitelistIps: [], // Có thể thêm IPs nếu cần
    },
    
    // ============================================
    // CloudWatch Config
    // ============================================
    cloudWatch: {
      alarmEmail: 'khuy220@gmail.com',
    },
    
    // ============================================
    // Tags Config
    // ============================================
    tags: {
      project: 'MyJob',
      owner: 'Bui Khanh Huy',
      costCenter: 'Engineering',
    },
  };
}

/**
 * Singleton config instance
 * Load once and reuse throughout the application
 */
export const config = loadConfig();

