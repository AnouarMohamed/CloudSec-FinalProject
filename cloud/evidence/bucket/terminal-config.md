# Live terminal capture — private documents bucket configuration

- **Context:** Phase B hardened `cloud-docs-grp01`, 2026-11-25 UTC.
- **Commands shown:** `date -u`; `rtk proxy aws s3api get-public-access-block --bucket cloud-docs-grp01 --profile cloud --region eu-west-3`; `rtk proxy aws s3api get-bucket-encryption --bucket cloud-docs-grp01 --profile cloud --region eu-west-3 --query 'ServerSideEncryptionConfiguration.Rules[*].ApplyServerSideEncryptionByDefault.SSEAlgorithm' --output json`; `rtk proxy aws s3api get-bucket-versioning --bucket cloud-docs-grp01 --profile cloud --region eu-west-3`.
- **Expected:** Four public-access block switches enabled, default encryption, and versioning.
- **Actual:** All four switches are `true`; default encryption is `AES256`; versioning is `Enabled`.
- **Interpretation:** These three configuration checks pass. Anonymous access is tested separately in [terminal-anonymous.png](terminal-anonymous.png); the restrictive policy is defined in Terraform.
- **Method:** Genuine Ptyxis window on private Xvfb, raw session [ptyxis-live.session](../terminal-live/ptyxis-live.session). The visible `atl-cloud-GRP01` hostname exists in an isolated UTS namespace on physical host `morgoth`; it is not a project VM.
