# Scoped workload role capture

- **Context:** Phase C role and inline policy after Terraform apply on 2026-11-25. `scoped-role.session` is the real terminal recording; `scoped-role.png` renders the full visible commands and output with `[GRP01]`, real hostname `morgoth`, and UTC timestamp.
- **Commands shown:** `rtk proxy aws iam get-role --role-name cloud-app-read-grp01 --profile cloud --query 'Role.{Arn:Arn,AssumeRolePolicyDocument:AssumeRolePolicyDocument,Tags:Tags}'` and `rtk proxy aws iam get-role-policy --role-name cloud-app-read-grp01 --policy-name cloud-app-read-grp01 --profile cloud --query '{RoleName:RoleName,PolicyName:PolicyName,PolicyDocument:PolicyDocument}'`, following `date -u`.
- **Expected:** A project-named, tagged workload role with only project document read and secret read actions.
- **Actual:** Role `cloud-app-read-grp01` trusts the EC2 service; its policy grants `s3:GetObject` on `cloud-docs-grp01/*` and `secretsmanager:GetSecretValue` on the one project secret. Tags are Project=Cloud, Group=01, Owner=Anouar Mohamed. Timestamp `Wed Nov 25 10:54:59 UTC 2026`.
- **Interpretation:** The defined workload role is scoped. No EC2 instance is launched, and this is not evidence that the root build identity or all account IAM users follow least privilege.
