# Live terminal capture — anonymous S3 refusal

- **Context:** Phase B unauthenticated access test for `cloud-docs-grp01`, 2026-11-25 UTC.
- **Commands shown:** `date -u`; `rtk proxy aws s3api head-bucket --bucket cloud-docs-grp01 --no-sign-request --region eu-west-3`.
- **Expected:** Anonymous `HeadBucket` is refused.
- **Actual:** AWS returned `403 Forbidden`.
- **Interpretation:** The observed anonymous request was denied; this does not test every possible S3 API action.
- **Method:** Genuine Ptyxis window on private Xvfb, raw session [ptyxis-live.session](../terminal-live/ptyxis-live.session). The visible `atl-cloud-GRP01` hostname is real within an isolated UTS namespace on physical host `morgoth`; it is not a project VM.
