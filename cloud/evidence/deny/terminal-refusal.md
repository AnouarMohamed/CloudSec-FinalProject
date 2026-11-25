# Live terminal capture — explicit bucket-policy refusal

- **Context:** Phase D denial test against project docs bucket, 2026-11-25 UTC.
- **Commands shown:** `date -u`; `rtk proxy aws s3api list-objects-v2 --bucket cloud-docs-grp01 --profile cloud --region eu-west-3`.
- **Expected:** The resource-policy `s3:ListBucket` Deny blocks listing.
- **Actual:** AWS returned `AccessDenied`, identifying an explicit deny in a resource-based policy for `arn:aws:s3:::cloud-docs-grp01`.
- **Interpretation:** A real project policy denial was observed. The caller was the user-directed root profile; this does not establish an SCP or least-privilege human IAM identity.
- **Method:** Genuine Ptyxis window on private Xvfb, raw session [ptyxis-live.session](../terminal-live/ptyxis-live.session). `atl-cloud-GRP01` is a real isolated UTS namespace hostname on physical host `morgoth`, not a project VM.
