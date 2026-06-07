import * as cdk from 'aws-cdk-lib';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as autoscaling from 'aws-cdk-lib/aws-autoscaling';
import * as ssm from 'aws-cdk-lib/aws-ssm';
import * as iam from 'aws-cdk-lib/aws-iam';
import { Construct } from 'constructs';
import { EcsStackProps } from './types';
import { config } from './config';

/**
 * ECS Stack
 * Creates ECS Cluster (EC2 launch type), Task Definitions, and Services for Django and Celery
 */
export class EcsStack extends cdk.Stack {
  public readonly ecsCluster: ecs.ICluster;
  public readonly djangoService: ecs.IBaseService;
  public readonly celeryWorkerService: ecs.IBaseService;
  public readonly celeryBeatService: ecs.IBaseService;

  constructor(scope: Construct, id: string, props: EcsStackProps) {
    super(scope, id, props);

    // // ============================================
    // // ECS Cluster (EC2 launch type)
    // // ============================================
    // const cluster = new ecs.Cluster(this, 'Cluster', {
    //   vpc: props.vpc,
    //   clusterName: `${this.stackName}-Cluster`,
    //   containerInsights: true, // Enable CloudWatch Container Insights
    // });
    // this.ecsCluster = cluster;

    // // ============================================
    // // EC2 Auto Scaling Group for ECS Cluster
    // // ============================================
    // const autoScalingGroup = new autoscaling.AutoScalingGroup(this, 'AutoScalingGroup', {
    //   vpc: props.vpc,
    //   instanceType: ec2.InstanceType.of(
    //     ec2.InstanceClass.T3,
    //     ec2.InstanceSize.MEDIUM
    //   ),
    //   machineImage: ecs.EcsOptimizedImage.amazonLinux2(),
    //   minCapacity: config.ecs.ec2.minCapacity,
    //   maxCapacity: config.ecs.ec2.maxCapacity,
    //   desiredCapacity: config.ecs.ec2.desiredCapacity,
    //   vpcSubnets: {
    //     subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS,
    //   },
    //   securityGroup: props.ecsSecurityGroup,
    // });

    // // Attach Auto Scaling Group to ECS Cluster
    // const capacityProvider = new ecs.AsgCapacityProvider(this, 'AsgCapacityProvider', {
    //   autoScalingGroup,
    //   enableManagedTerminationProtection: false,
    // });
    
    // cluster.addAsgCapacityProvider(capacityProvider);

    // // ============================================
    // // Task Execution Role (for ECS to pull images, write logs, etc.)
    // // ============================================
    // const taskExecutionRole = new iam.Role(this, 'TaskExecutionRole', {
    //   assumedBy: new iam.ServicePrincipal('ecs-tasks.amazonaws.com'),
    //   managedPolicies: [
    //     iam.ManagedPolicy.fromAwsManagedPolicyName('service-role/AmazonECSTaskExecutionRolePolicy'),
    //   ],
    // });

    // // Grant permissions to read SSM parameters
    // taskExecutionRole.addToPolicy(
    //   new iam.PolicyStatement({
    //     effect: iam.Effect.ALLOW,
    //     actions: [
    //       'ssm:GetParameters',
    //       'ssm:GetParameter',
    //       'ssm:GetParametersByPath',
    //     ],
    //     resources: [
    //       `arn:aws:ssm:${this.region}:${this.account}:parameter/myjob/*`,
    //     ],
    //   })
    // );

    // // ============================================
    // // Task Role (for application to access AWS services)
    // // ============================================
    // const taskRole = new iam.Role(this, 'TaskRole', {
    //   assumedBy: new iam.ServicePrincipal('ecs-tasks.amazonaws.com'),
    // });

    // // Grant permissions to read SSM parameters
    // taskRole.addToPolicy(
    //   new iam.PolicyStatement({
    //     effect: iam.Effect.ALLOW,
    //     actions: [
    //       'ssm:GetParameters',
    //       'ssm:GetParameter',
    //       'ssm:GetParametersByPath',
    //     ],
    //     resources: [
    //       `arn:aws:ssm:${this.region}:${this.account}:parameter/myjob/*`,
    //     ],
    //   })
    // );

    // // ============================================
    // // Django Task Definition
    // // ============================================
    // const djangoTaskDefinition = new ecs.Ec2TaskDefinition(this, 'DjangoTaskDef', {
    //   executionRole: taskExecutionRole,
    //   taskRole: taskRole,
    //   networkMode: ecs.NetworkMode.BRIDGE,
    // });

    // const djangoContainer = djangoTaskDefinition.addContainer('django', {
    //   image: ecs.ContainerImage.fromRegistry('nginx:latest'), // TODO: Replace with your ECR image
    //   memoryLimitMiB: config.ecs.django.memory,
    //   cpu: config.ecs.django.cpu,
      
    //   // Environment Variables từ config
    //   environment: props.environment as unknown as { [key: string]: string },
      
    //   // Secrets từ SSM Parameter Store
    //   secrets: {
    //     // Database credentials từ SSM
    //     DB_USER: ecs.Secret.fromSsmParameter(
    //       ssm.StringParameter.fromStringParameterName(
    //         this,
    //         'DBUserParam',
    //         `${config.database.rdsSecretName}/username`
    //       )
    //     ),
    //     DB_PASSWORD: ecs.Secret.fromSsmParameter(
    //       ssm.StringParameter.fromStringParameterName(
    //         this,
    //         'DBPasswordParam',
    //         `${config.database.rdsSecretName}/password`
    //       )
    //     ),
        
    //     // Redis password từ SSM
    //     REDIS_PASSWORD: ecs.Secret.fromSsmParameter(
    //       ssm.StringParameter.fromStringParameterName(
    //         this,
    //         'RedisPasswordParam',
    //         config.redis.redisSecretName
    //       )
    //     ),
        
    //     // Django SECRET_KEY từ SSM
    //     DJANGO_SECRET_KEY: ecs.Secret.fromSsmParameter(
    //       ssm.StringParameter.fromStringParameterName(
    //         this,
    //         'DjangoSecretKeyParam',
    //         '/myjob/production/app/SECRET_KEY'
    //       )
    //     ),
    //   },
      
    //   logging: ecs.LogDrivers.awsLogs({
    //     streamPrefix: 'django',
    //     logRetention: cdk.aws_logs.RetentionDays.ONE_WEEK,
    //   }),
    // });

    // // Add port mapping for Django (port 8000)
    // djangoContainer.addPortMappings({
    //   containerPort: 8000,
    //   protocol: ecs.Protocol.TCP,
    // });

    // // ============================================
    // // Django ECS Service
    // // ============================================
    // const djangoService = new ecs.Ec2Service(this, 'DjangoService', {
    //   cluster: cluster,
    //   taskDefinition: djangoTaskDefinition,
    //   desiredCount: config.ecs.django.desiredCount,
    //   serviceName: 'django',
    //   assignPublicIp: false,
    //   securityGroups: [props.ecsSecurityGroup],
    // });

    // this.djangoService = djangoService;

    // // Attach to ALB target group
    // djangoService.attachToApplicationTargetGroup(props.targetGroup);

    // // Auto Scaling for Django Service
    // const djangoScaling = djangoService.autoScaleTaskCount({
    //   minCapacity: config.ecs.django.minCapacity,
    //   maxCapacity: config.ecs.django.maxCapacity,
    // });

    // djangoScaling.scaleOnCpuUtilization('CpuScaling', {
    //   targetUtilizationPercent: 70,
    //   scaleInCooldown: cdk.Duration.seconds(60),
    //   scaleOutCooldown: cdk.Duration.seconds(60),
    // });

    // djangoScaling.scaleOnMemoryUtilization('MemoryScaling', {
    //   targetUtilizationPercent: 80,
    //   scaleInCooldown: cdk.Duration.seconds(60),
    //   scaleOutCooldown: cdk.Duration.seconds(60),
    // });

    // // ============================================
    // // Celery Worker Task Definition
    // // ============================================
    // const celeryWorkerTaskDefinition = new ecs.Ec2TaskDefinition(this, 'CeleryWorkerTaskDef', {
    //   executionRole: taskExecutionRole,
    //   taskRole: taskRole,
    //   networkMode: ecs.NetworkMode.BRIDGE,
    // });

    // const celeryWorkerContainer = celeryWorkerTaskDefinition.addContainer('celery-worker', {
    //   image: ecs.ContainerImage.fromRegistry('nginx:latest'), // TODO: Replace with your ECR image
    //   memoryLimitMiB: config.ecs.celeryWorker.memory,
    //   cpu: config.ecs.celeryWorker.cpu,
      
    //   // Environment Variables
    //   environment: props.environment as unknown as { [key: string]: string },
      
    //   // Secrets từ SSM
    //   secrets: {
    //     DB_USER: ecs.Secret.fromSsmParameter(
    //       ssm.StringParameter.fromStringParameterName(
    //         this,
    //         'CeleryWorkerDBUserParam',
    //         `${config.database.rdsSecretName}/username`
    //       )
    //     ),
    //     DB_PASSWORD: ecs.Secret.fromSsmParameter(
    //       ssm.StringParameter.fromStringParameterName(
    //         this,
    //         'CeleryWorkerDBPasswordParam',
    //         `${config.database.rdsSecretName}/password`
    //       )
    //     ),
    //     REDIS_PASSWORD: ecs.Secret.fromSsmParameter(
    //       ssm.StringParameter.fromStringParameterName(
    //         this,
    //         'CeleryWorkerRedisPasswordParam',
    //         config.redis.redisSecretName
    //       )
    //     ),
    //     DJANGO_SECRET_KEY: ecs.Secret.fromSsmParameter(
    //       ssm.StringParameter.fromStringParameterName(
    //         this,
    //         'CeleryWorkerDjangoSecretKeyParam',
    //         '/myjob/production/app/SECRET_KEY'
    //       )
    //     ),
    //   },
      
    //   command: ['celery', '-A', 'myjob_api', 'worker', '--loglevel=info'],
      
    //   logging: ecs.LogDrivers.awsLogs({
    //     streamPrefix: 'celery-worker',
    //     logRetention: cdk.aws_logs.RetentionDays.ONE_WEEK,
    //   }),
    // });

    // // ============================================
    // // Celery Worker ECS Service
    // // ============================================
    // const celeryWorkerService = new ecs.Ec2Service(this, 'CeleryWorkerService', {
    //   cluster: cluster,
    //   taskDefinition: celeryWorkerTaskDefinition,
    //   desiredCount: config.ecs.celeryWorker.desiredCount,
    //   serviceName: 'celery-worker',
    //   assignPublicIp: false,
    //   securityGroups: [props.ecsSecurityGroup],
    // });

    // this.celeryWorkerService = celeryWorkerService;

    // // Auto Scaling for Celery Worker Service
    // const celeryWorkerScaling = celeryWorkerService.autoScaleTaskCount({
    //   minCapacity: config.ecs.celeryWorker.minCapacity,
    //   maxCapacity: config.ecs.celeryWorker.maxCapacity,
    // });

    // celeryWorkerScaling.scaleOnCpuUtilization('CpuScaling', {
    //   targetUtilizationPercent: 70,
    //   scaleInCooldown: cdk.Duration.seconds(60),
    //   scaleOutCooldown: cdk.Duration.seconds(60),
    // });

    // // ============================================
    // // Celery Beat Task Definition
    // // ============================================
    // const celeryBeatTaskDefinition = new ecs.Ec2TaskDefinition(this, 'CeleryBeatTaskDef', {
    //   executionRole: taskExecutionRole,
    //   taskRole: taskRole,
    //   networkMode: ecs.NetworkMode.BRIDGE,
    // });

    // const celeryBeatContainer = celeryBeatTaskDefinition.addContainer('celery-beat', {
    //   image: ecs.ContainerImage.fromRegistry('nginx:latest'), // TODO: Replace with your ECR image
    //   memoryLimitMiB: config.ecs.celeryBeat.memory,
    //   cpu: config.ecs.celeryBeat.cpu,
      
    //   // Environment Variables
    //   environment: props.environment as unknown as { [key: string]: string },
      
    //   // Secrets từ SSM
    //   secrets: {
    //     DB_USER: ecs.Secret.fromSsmParameter(
    //       ssm.StringParameter.fromStringParameterName(
    //         this,
    //         'CeleryBeatDBUserParam',
    //         `${config.database.rdsSecretName}/username`
    //       )
    //     ),
    //     DB_PASSWORD: ecs.Secret.fromSsmParameter(
    //       ssm.StringParameter.fromStringParameterName(
    //         this,
    //         'CeleryBeatDBPasswordParam',
    //         `${config.database.rdsSecretName}/password`
    //       )
    //     ),
    //     DJANGO_SECRET_KEY: ecs.Secret.fromSsmParameter(
    //       ssm.StringParameter.fromStringParameterName(
    //         this,
    //         'CeleryBeatDjangoSecretKeyParam',
    //         '/myjob/production/app/SECRET_KEY'
    //       )
    //     ),
    //   },
      
    //   command: ['celery', '-A', 'myjob_api', 'beat', '--loglevel=info'],
      
    //   logging: ecs.LogDrivers.awsLogs({
    //     streamPrefix: 'celery-beat',
    //     logRetention: cdk.aws_logs.RetentionDays.ONE_WEEK,
    //   }),
    // });

    // // ============================================
    // // Celery Beat ECS Service (Singleton - only 1 instance)
    // // ============================================
    // this.celeryBeatService = new ecs.Ec2Service(this, 'CeleryBeatService', {
    //   cluster: cluster,
    //   taskDefinition: celeryBeatTaskDefinition,
    //   desiredCount: config.ecs.celeryBeat.desiredCount, // Always 1
    //   serviceName: 'celery-beat',
    //   assignPublicIp: false,
    //   securityGroups: [props.ecsSecurityGroup],
    // });

    // // ============================================
    // // Outputs
    // // ============================================
    // new cdk.CfnOutput(this, 'ClusterName', {
    //   value: this.ecsCluster.clusterName,
    //   description: 'ECS Cluster Name',
    // });

    // new cdk.CfnOutput(this, 'DjangoServiceName', {
    //   value: this.djangoService.serviceName,
    //   description: 'Django Service Name',
    // });
  }
}

