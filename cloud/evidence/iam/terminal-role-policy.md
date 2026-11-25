# Live terminal capture — workload role permissions

- **Context:** Phase C inline policy `cloud-app-read-grp01`, 2026-11-25 UTC.
- **Commands shown:** `date -u`; `rtk proxy aws iam get-role-policy --role-name cloud-app-read-grp01 --policy-name cloud-app-read-grp01 --profile cloud --query PolicyDocument --output json`.
- **Expected:** Project workload permissions limited to needed S3 and Secrets Manager reads.
- **Actual:** The two Allow statements grant `s3:GetObject` on `arn:aws:s3:::cloud-docs-grp01/*` and `secretsmanager:GetSecretValue` on the one `cloud-app-secret-grp01` ARN.
- **Interpretation:** The displayed inline policy is narrow; this is a policy inspection, not a successful workload access test. It does not make the root build identity least privileged.
- **Method:** Genuine Ptyxis window on private Xvfb, recorded in [ptyxis-repair.session](../terminal-live/ptyxis-repair.session). `atl-cloud-GRP01` is the real hostname inside an isolated UTS namespace on physical host `morgoth`, not a project VM. The window was captured without cropping or retouching.
