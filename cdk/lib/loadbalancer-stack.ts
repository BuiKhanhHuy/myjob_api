import * as cdk from 'aws-cdk-lib';
import * as elbv2 from 'aws-cdk-lib/aws-elasticloadbalancingv2';
import { Construct } from 'constructs';
import { LoadBalancerStackProps } from './types';

/**
 * Load Balancer Stack
 * Creates Application Load Balancer with WAF protection
 */
export class LoadBalancerStack extends cdk.Stack {
  public readonly alb: elbv2.IApplicationLoadBalancer;
  public readonly targetGroup: elbv2.IApplicationTargetGroup;

  constructor(scope: Construct, id: string, props: LoadBalancerStackProps) {
    super(scope, id, props);

    // ALB will be created in Phase 4
    // For now, just define the structure
    
    // TODO: Phase 4 - Implement Application Load Balancer
    // TODO: Phase 4 - Implement Target Group
    // TODO: Phase 4 - Implement WAF rules
  }
}

