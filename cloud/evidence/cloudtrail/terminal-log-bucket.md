# Live terminal capture — CloudTrail log-bucket settings

- **Context:** Phase B dedicated `cloud-trail-logs-grp01` bucket, 2026-11-25 UTC.
- **Commands shown:** `date -u`; `rtk proxy aws s3api get-public-access-block --bucket cloud-trail-logs-grp01 --profile cloud --region eu-west-3`; `rtk proxy aws s3api get-bucket-encryption --bucket cloud-trail-logs-grp01 --profile cloud --region eu-west-3 --query 'ServerSideEncryptionConfiguration.Rules[*].ApplyServerSideEncryptionByDefault.SSEAlgorithm' --output json`; `rtk proxy aws s3api list-objects-v2 --bucket cloud-trail-logs-grp01 --max-keys 1 --profile cloud --region eu-west-3 --query 'Contents[*].[Key,Size]' --output table`.
- **Expected:** All public-access blocks, default encryption, and delivered log data.
- **Actual:** All four block settings are `true`; default encryption is `AES256`. The one listed object is a zero-byte `CloudTrail-Digest/` folder marker.
- **Interpretation:** This image proves privacy and encryption configuration but the displayed marker alone does **not** prove log-file delivery. Use the separate live log-object capture and trail status for delivery.
- **Method:** Genuine Ptyxis window on private Xvfb, raw session [ptyxis-live.session](../terminal-live/ptyxis-live.session). `atl-cloud-GRP01` is a real isolated UTS namespace hostname on physical host `morgoth`, not a project VM.
