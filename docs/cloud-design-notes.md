# GRP01 cloud design notes (draft)

These notes explain the applied settings in plain language for the oral defense. They are not a substitute for CLI proof; the evidence index is authoritative for implementation status.

## S3 documents bucket

- Keep all four **bucket-level** public-access blocks enabled, and use a policy that explicitly denies non-TLS requests and requests from principals outside this account. A real anonymous `HeadBucket` request returned `403`, though this single result cannot separate the effects of the overlapping controls. The full Prowler scan found account-level Public Access Block absent; enabling it changes the whole account and needs separate approval under rule 7. [AWS S3 public-access blocking](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html).
- SSE-S3 encryption is explicitly managed in Terraform. AWS already returned `AES256` for the Phase A bucket because S3 automatically encrypts new uploads; the before/after claim is about explicit configuration, not previously unencrypted data. Versioning is enabled to recover from accidental overwrite or deletion. [AWS S3 default encryption](https://docs.aws.amazon.com/AmazonS3/latest/userguide/default-bucket-encryption.html).
- Deny requests with `aws:SecureTransport=false`. For service-delivery buckets, exclude AWS service principals from that deny when their network context might be redacted, so logging still works. [AWS S3 policy guidance](https://docs.aws.amazon.com/AmazonS3/latest/userguide/amazon-s3-policy-keys.html).

## VPC and Security Groups

- The isolated VPC has one public subnet (internet route) and one private subnet (local route only). No NAT gateway or instances are needed for the evidence. A subnet is public because of its route table, not because it has an instance.
- All project Security Groups have no ingress, including SSH/RDP. The two named groups allow only local VPC TCP 443 egress. An empty ingress set is a strong default for a demonstration VPC.
- The first after scan flagged AWS's allow-all default Network ACL for this VPC. Terraform now adopts that NACL and leaves only its default deny entries. This makes the demo VPC subnet traffic fully isolated until explicitly allowed; the public subnet remains public by route-table definition but cannot carry a workload without a deliberate ACL change.

## CloudTrail and tested alert

- The multi-Region trail records all management events and no data events. The first management-event delivery copy is free; S3 storage and requests remain billable. [AWS CloudTrail pricing](https://aws.amazon.com/cloudtrail/pricing/).
- The dedicated private log bucket grants only the CloudTrail service `s3:GetBucketAcl` and `s3:PutObject` on the account log path, constrained to the trail ARN and owner-full-control ACL. A wrong policy can cause retry charges, so confirm delivery after apply. [AWS CloudTrail bucket policy](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/create-s3-bucket-policy-for-cloudtrail.html).
- The EventBridge rule matches root CloudTrail management events, including read-only calls, and delivers to a private SQS queue. A real `LookupEvents` root call was received. Email delivery has not been claimed. [AWS EventBridge management events](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-service-event-cloudtrail.html).

## Secrets and workload IAM

- Terraform manages only the Secrets Manager container. The random fictional value was sent via stdin from process memory and retrieved without printing it. Secrets Manager costs about $0.40 per secret-month plus API requests. [AWS Secrets Manager pricing](https://aws.amazon.com/secrets-manager/pricing/).
- `cloud-app-read-grp01` is a defined example ECS task role with only `s3:GetObject` on project documents and `secretsmanager:GetSecretValue` for the one project secret. Its trust requires `aws:SourceAccount` to equal this account and `aws:SourceArn` to match ECS tasks in this account and Region, following AWS's documented pattern. The secret has a resource policy granting reads only to the project role, with public-policy blocking enabled. No ECS task was launched; do not claim active workload use. [AWS ECS task role guidance](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-iam-roles.html).
- Automatic rotation is disabled for the fictional demo value. Secrets Manager's generic rotation requires a Lambda rotation implementation; this value has no consumer or real credential to rotate. The corresponding Prowler HIGH remains a documented exception, not a claim of remediation.

## Cost and trust boundaries

- Project resources use names containing `grp01` and tags `Project=Cloud`, `Group=01`, `Owner=Anouar Mohamed`. Existing `gridguard`/CloudFormation resources are not part of this workstream.
- No EKS, EC2, NAT gateway, load balancer, or continuously running cloud compute was launched. The local Kubernetes bonus is planned for kind. The project budget is notification-only at $25, $50, and $100 of monthly gross cost.
- The budget email contact is currently inactive. An activation email was requested; the owner must confirm it in the AWS console. Actual-spend thresholds cannot be tested responsibly without spending at least $25 and waiting for AWS's billing evaluation. [AWS Budgets email verification](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-email-recipients.html).
- The user-directed root CLI login on 2026-11-25 is a grading exception. Do not say root was unused or that the build identity followed least privilege. Scoped project workload roles can still demonstrate least privilege for workloads.
