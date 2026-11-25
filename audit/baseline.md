# Safe baseline plan

The before state must be real. Planned GRP01 project-only deviations before hardening:

1. A private, empty `cloud-docs-grp01` bucket with public access blocked, no Terraform-managed explicit encryption resource, and versioning not enabled. AWS automatically supplies SSE-S3; the real `get-bucket-encryption` response reports `AES256`. The actual before/after encryption change must therefore be framed as explicit configuration and policy, not a transition from plaintext.
2. No new CloudTrail trail until after the initial audit. AWS Event History remains available for management events.
3. A project VPC and Security Group with no inbound rules and default outbound access. This avoids public inbound exposure while leaving an outbound least-privilege finding to fix.

These are deliberately temporary, safe omissions to create a measurable before/after audit. Do not claim a finding until the initial Prowler report actually shows it. Existing resources from other projects are excluded from deliberate changes.

**Status:** baseline applied on 2026-11-25: Terraform created one empty S3 bucket, one public-access block, and one notification-only project budget. Initial Prowler audit is running. A failed IAM attempt before the root login created nothing and is recorded in `docs/journal.md`.
