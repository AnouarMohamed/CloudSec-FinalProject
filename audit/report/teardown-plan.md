# GRP01 teardown plan (draft; not executed)

The project AWS resources are still deployed for review. `AGENTS.md` rule 7 requires Anouar's approval before `terraform destroy` or deletion of buckets that hold evidence. Preserve the raw Prowler files and terminal sessions locally. The CloudTrail log bucket is additional AWS-side evidence and is currently growing.

At the final 2026-11-25 inventory, Terraform manages the GRP01 budget, two S3 buckets, one active multi-Region CloudTrail trail, an EventBridge root-use rule and SQS queue, one Secrets Manager secret, two IAM roles with inline policies (workload and deny-demo), and the VPC with subnets, routes, gateway, NACL, and Security Groups. S3 storage/requests, Secrets Manager storage/requests, SQS requests, EventBridge events, and CloudTrail's delivered log storage are potentially billable. The trail bucket held at least 991,439 bytes in the queried page at 16:00 UTC and will grow while logging stays on. The docs bucket was empty before the test policy denied listing; it has not accepted project data. The budget recipient was still `inactive`. No EC2 instance, EKS control plane, NAT gateway, load balancer, or public IPv4 address was launched. Local kind cluster `grp01` is running on this machine, without AWS hourly charges.

After explicit teardown approval:

1. Export any desired CloudTrail logs to a protected location outside the bucket and verify the local copy. Keep the existing repo evidence.
2. Review `terraform plan -destroy -out=teardown.tfplan` in `cloud/terraform/`; inspect for changes to anything outside GRP01. Do not apply it until approved.
3. Stop the trail before removing its delivery bucket, then empty only `s3://cloud-trail-logs-grp01` after evidence preservation. The docs bucket should still be empty. Do not use a recursive S3 delete against any other bucket.
4. Apply the reviewed destroy plan only after approval. The unused `cloud-deny-demo-grp01` role is included. Secrets Manager uses a 7-day recovery window, so the secret may remain pending deletion after Terraform completes; confirm its AWS status and charges. Verify the GRP01 resources are gone with CLI and `terraform state list`.
5. If the local kind cluster exists, remove it with `kind delete cluster --name grp01` after its evidence is reviewed. This local cluster is not an AWS billable resource.

The exact deletion sequence must be reviewed again against live state at teardown time; no command in this file is evidence of deletion.
