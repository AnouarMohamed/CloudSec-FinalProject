# IAM human MFA inventory capture

- **Context:** Read-only IAM check on 2026-11-25. `human-mfa.session` is the real terminal recording; `human-mfa.png` renders the complete visible commands/output, `[GRP01]`, actual hostname `morgoth`, and UTC time.
- **Commands shown:** `rtk proxy aws iam list-users --profile cloud --query 'Users[].UserName'`; `rtk proxy aws iam list-mfa-devices --user-name anouar-admin --profile cloud --query 'MFADevices[].SerialNumber'`; same `list-mfa-devices` command for `zakaria-admin`, following `date -u`.
- **Expected:** Both human IAM users would have MFA to meet the acceptance criterion.
- **Actual:** `anouar-admin` has a U2F device; `zakaria-admin` returns `[]`. Timestamp `Wed Nov 25 10:55:23 UTC 2026`.
- **Interpretation:** Account-wide human MFA criterion is unmet. `zakaria-admin` is an existing user outside this project's Terraform state; its owner must register MFA. No MFA setting was changed by this read-only check. Root MFA was verified separately in `account/safety-concise.png`.
