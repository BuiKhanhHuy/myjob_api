import * as cdk from 'aws-cdk-lib';
import * as route53 from 'aws-cdk-lib/aws-route53';
import { Construct } from 'constructs';
import { DomainStackProps } from './types';

/**
 * Domain Stack
 * Tạo Route53 A record trỏ api.<domain> → EC2 Elastic IP.
 * Yêu cầu Hosted Zone của domain đã tồn tại trên Route53 (fromLookup).
 */
export class DomainStack extends cdk.Stack {
  public readonly hostedZone: route53.IHostedZone;

  constructor(scope: Construct, id: string, props: DomainStackProps) {
    super(scope, id, props);

    // Lookup existing hosted zone — domain phải đã có trên Route53
    this.hostedZone = route53.HostedZone.fromLookup(this, 'HostedZone', {
      domainName: props.domainName,
    });

    // A record: api.buikhanhhuy.com → EC2 Elastic IP
    new route53.ARecord(this, 'ApiARecord', {
      zone: this.hostedZone,
      recordName: props.apiSubdomain,
      target: route53.RecordTarget.fromIpAddresses(props.elasticIp),
      ttl: cdk.Duration.minutes(5),
      comment: 'MyJob API EC2 instance',
    });

    new cdk.CfnOutput(this, 'ApiEndpoint', {
      value: `http://${props.apiSubdomain}.${props.domainName}`,
      description: 'API endpoint (HTTP — chạy certbot để bật HTTPS)',
    });
  }
}
