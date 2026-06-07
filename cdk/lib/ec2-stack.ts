import * as cdk from 'aws-cdk-lib';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as iam from 'aws-cdk-lib/aws-iam';
import { Construct } from 'constructs';
import { config } from './config';

export class Ec2Stack extends cdk.Stack {
  public readonly instance: ec2.Instance;
  public readonly elasticIpAddress: string;

  constructor(scope: Construct, id: string, props: cdk.StackProps) {
    super(scope, id, props);

    // Default VPC — no custom VPC needed for quick deploy
    const vpc = ec2.Vpc.fromLookup(this, 'DefaultVpc', { isDefault: true });

    // Security Group: allow HTTP + HTTPS, no SSH (SSM is used instead)
    const securityGroup = new ec2.SecurityGroup(this, 'ApiSecurityGroup', {
      vpc,
      description: 'MyJob API EC2 security group',
      allowAllOutbound: true,
    });
    securityGroup.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(80), 'HTTP');
    securityGroup.addIngressRule(ec2.Peer.anyIpv6(), ec2.Port.tcp(80), 'HTTP IPv6');
    securityGroup.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(443), 'HTTPS');
    securityGroup.addIngressRule(ec2.Peer.anyIpv6(), ec2.Port.tcp(443), 'HTTPS IPv6');

    // IAM Role: SSM access + Secrets Manager read
    const role = new iam.Role(this, 'Ec2InstanceRole', {
      assumedBy: new iam.ServicePrincipal('ec2.amazonaws.com'),
      managedPolicies: [
        iam.ManagedPolicy.fromAwsManagedPolicyName('AmazonSSMManagedInstanceCore'),
        iam.ManagedPolicy.fromAwsManagedPolicyName('SecretsManagerReadWrite'),
      ],
    });

    // User data: bootstraps the EC2 on first boot
    const userData = ec2.UserData.forLinux();
    userData.addCommands(
      'set -e',
      'exec > /var/log/user-data.log 2>&1',

      // Swap 2GB — bắt buộc cho t2.micro (chỉ có 1GB RAM)
      'fallocate -l 2G /swapfile',
      'chmod 600 /swapfile',
      'mkswap /swapfile',
      'swapon /swapfile',
      "echo '/swapfile none swap sw 0 0' >> /etc/fstab",
      'sysctl vm.swappiness=10',
      "echo 'vm.swappiness=10' >> /etc/sysctl.conf",

      // System packages
      'dnf update -y',
      'dnf install -y docker git nginx jq certbot python3-certbot-nginx',

      // Docker
      'systemctl start docker',
      'systemctl enable docker',
      'usermod -aG docker ec2-user',

      // Docker Compose v2 plugin
      'mkdir -p /usr/libexec/docker/cli-plugins',
      'curl -SL "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-linux-x86_64" \\',
      '  -o /usr/libexec/docker/cli-plugins/docker-compose',
      'chmod +x /usr/libexec/docker/cli-plugins/docker-compose',
      'ln -sf /usr/libexec/docker/cli-plugins/docker-compose /usr/local/bin/docker-compose',

      // Clone repo
      'cd /opt',
      `git clone ${config.ec2.githubRepoUrl} myjob_api`,
      'cd myjob_api',

      // Pull .env from Secrets Manager (plaintext secret = full .env content)
      `aws secretsmanager get-secret-value \\`,
      `  --region ${config.aws.region} \\`,
      `  --secret-id ${config.ec2.envSecretName} \\`,
      `  --query SecretString --output text > .env`,

      // Start production docker-compose (no ngrok, gunicorn)
      'docker compose -f docker-compose.prod.yaml up -d --build',

      // Write nginx reverse-proxy config
      // Single-quoted heredoc marker prevents shell expansion of nginx variables like $host
      `cat > /etc/nginx/conf.d/myjob-api.conf << 'NGINX_EOF'`,
      'server {',
      '    listen 80;',
      `    server_name ${config.domain.apiSubdomain}.${config.domain.domainName};`,
      '    client_max_body_size 20M;',
      '    location / {',
      '        proxy_pass http://127.0.0.1:8000;',
      '        proxy_set_header Host $host;',
      '        proxy_set_header X-Real-IP $remote_addr;',
      '        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;',
      '        proxy_set_header X-Forwarded-Proto $scheme;',
      '        proxy_read_timeout 90;',
      '        proxy_connect_timeout 90;',
      '    }',
      '}',
      'NGINX_EOF',

      // Remove nginx default site and start
      'rm -f /etc/nginx/conf.d/default.conf',
      'nginx -t',
      'systemctl start nginx',
      'systemctl enable nginx',
    );

    // EC2 instance in a public subnet so Elastic IP works
    this.instance = new ec2.Instance(this, 'ApiInstance', {
      vpc,
      instanceType: new ec2.InstanceType(config.ec2.instanceType),
      machineImage: ec2.MachineImage.latestAmazonLinux2023(),
      securityGroup,
      role,
      userData,
      vpcSubnets: { subnetType: ec2.SubnetType.PUBLIC },
    });
    cdk.Tags.of(this.instance).add('Name', 'myjob-api');

    // Elastic IP — static public address that survives instance stop/start
    const eip = new ec2.CfnEIP(this, 'ApiEIP', {
      instanceId: this.instance.instanceId,
      tags: [{ key: 'Name', value: 'myjob-api-eip' }],
    });

    this.elasticIpAddress = eip.attrPublicIp;

    // Outputs
    new cdk.CfnOutput(this, 'InstanceId', {
      value: this.instance.instanceId,
      description: 'EC2 Instance ID (dùng cho SSM)',
    });

    new cdk.CfnOutput(this, 'ElasticIpAddress', {
      value: eip.attrPublicIp,
      description: 'Elastic IP của EC2',
    });

    new cdk.CfnOutput(this, 'SsmCommand', {
      value: cdk.Fn.join('', [
        `aws ssm start-session --target `,
        this.instance.instanceId,
        ` --region ${config.aws.region}`,
      ]),
      description: 'Lệnh SSH qua SSM Session Manager',
    });

    new cdk.CfnOutput(this, 'UserDataLog', {
      value: 'sudo cat /var/log/user-data.log',
      description: 'Xem log bootstrap trên EC2',
    });
  }
}
