# GRP01 cloud design notes (draft)

These notes explain planned settings in plain language for the oral defense. They are not proof that a resource has been applied; the evidence index is authoritative for implementation status.

## S3 documents bucket

- Keep account and bucket public-access blocking enabled, then add a policy that explicitly denies non-TLS requests and requests from principals outside this account. Public blocking prevents accidental grants; the explicit deny adds a policy-level boundary that can be demonstrated with a refused anonymous request. [AWS S3 public-access blocking](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html).
- Set and manage SSE-S3 encryption explicitly in Terraform. AWS already returns `AES256` for the Phase A bucket because S3 automatically encrypts new uploads; the before/after claim is about explicit configuration, not previously unencrypted data. Enable versioning to recover from accidental overwrite or deletion. [AWS S3 default encryption](https://docs.aws.amazon.com/AmazonS3/latest/userguide/default-bucket-encryption.html).
- Deny requests with `aws:SecureTransport=false`. For service-delivery buckets, exclude AWS service principals from that deny when their network context might be redacted, so logging still works. [AWS S3 policy guidance](https://docs.aws.amazon.com/AmazonS3/latest/userguide/amazon-s3-policy-keys.html).

## VPC and Security Groups

- Build an isolated VPC with one public subnet (internet route) and one private subnet (local route only). No NAT gateway or instances are needed for the evidence. A subnet is public because of its route table, not because it has an instance.
- Allow no SSH or RDP ingress, and restrict project Security Group rules to the VPC or project subnet where a rule is needed. An empty ingress set is a strong default for a demonstration VPC.

## CloudTrail and tested alert

- Use a multi-Region trail with all management events and no data-event selectors. The first management-event delivery copy is free; S3 storage and requests remain billable. [AWS CloudTrail pricing](https://aws.amazon.com/cloudtrail/pricing/).
- The dedicated private log bucket grants only the CloudTrail service `s3:GetBucketAcl` and `s3:PutObject` on the account log path, constrained to the trail ARN and owner-full-control ACL. A wrong policy can cause retry charges, so confirm delivery after apply. [AWS CloudTrail bucket policy](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/create-s3-bucket-policy-for-cloudtrail.html).
- Use an EventBridge rule for real CloudTrail management events and deliver the matching alert to a private SQS queue for a verifiable receive test. The email notification channel may need user confirmation before it can be claimed as delivered. [AWS EventBridge CloudTrail event reference](https://docs.aws.amazon.com/eventbridge/latest/ref/events-ref-cloudtrail.html).

## Cost and trust boundaries

- Project resources use names containing `grp01` and tags `Project=Cloud`, `Group=01`, `Owner=Anouar Mohamed`. Existing `gridguard`/CloudFormation resources are not part of this workstream.
- No EKS, EC2, NAT gateway, load balancer, or continuously running compute is planned. The local Kubernetes bonus uses kind. The project budget is notification-only at $25, $50, and $100 of monthly gross cost.
- The user-directed root CLI login on 2026-11-25 is a grading exception. Do not say root was unused or that the build identity followed least privilege. Scoped project workload roles can still demonstrate least privilege for workloads.
