# Phase D explicit denial

Context: GRP01 docs bucket after the reviewed Phase D Terraform change on 2026-11-25 UTC. The original terminal recording is `refusal.session`; `refusal.png` is its unedited rendering.

Commands: `aws s3api list-objects-v2 --bucket cloud-docs-grp01 --profile cloud --region eu-west-3` and `aws s3api get-bucket-policy --bucket cloud-docs-grp01 --profile cloud --region eu-west-3 --query Policy --output text`, shown with the `[GRP01]` prompt and `date -u`.

Expected: an explicit project-bucket policy denies `s3:ListBucket` even to an otherwise authorized principal. Actual: AWS returned `AccessDenied` and explicitly attributed the refusal to a resource-based policy; the following policy output contains `DenyProjectBucketListingForDemonstration` on `s3:ListBucket` for `Principal: *`.

Interpretation: the project has a tested IAM-equivalent denial without enabling AWS Organizations. This test used the user-directed root CLI session; it does not satisfy the no-root criterion. The bucket is empty and the policy still permits `PutBucketPolicy` for management. The extra IAM deny-demo role is not used because AWS refused `AssumeRole` from root; the failed test remains described in the journal.
