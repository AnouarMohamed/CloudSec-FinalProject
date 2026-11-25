# Phase C targeted remediation

Context: GRP01 targeted remediations on 2026-11-25 UTC after the first full after audit.

Commands: `aws iam get-role --role-name cloud-app-read-grp01`; `aws secretsmanager get-resource-policy --secret-id cloud-app-secret-grp01`; `aws ec2 describe-network-acls --filters Name=vpc-id,Values=vpc-0d069fce4ce5ff50a`, with the shown query and output options. The `[GRP01]` prompt and `date -u` are visible in the image.

Expected: service role trust limited to this account, secret resource policy limited to the project role, and no allow-all entry in the project default NACL.

Actual: role trust has `aws:SourceAccount=227755136916`; the secret policy grants only `GetSecretValue` to `cloud-app-read-grp01`; both directions of the project default NACL contain only AWS's terminal deny rule.

Interpretation: this was an intermediate configuration. The service principal was subsequently changed from EC2 to ECS tasks to use AWS's documented `SourceAccount`/`SourceArn` trust pattern; see `remediation-final.md` for the current state. Original `remediation.session`; rendered `remediation.png`. The 12-digit account ID is intentionally visible and is not an access credential.
