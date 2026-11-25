# Hardened documents bucket capture

- **Context:** Phase B verification on 2026-11-25. `hardened.session` is the actual terminal recording, and `hardened.png` renders its complete visible commands and output with `[GRP01]`, actual hostname `morgoth`, and UTC time.
- **Commands shown:** `rtk proxy aws s3api get-public-access-block --bucket cloud-docs-grp01 --profile cloud`; `get-bucket-encryption`; `get-bucket-versioning`; and `rtk proxy aws s3api head-bucket --bucket cloud-docs-grp01 --no-sign-request --region eu-west-3`, following `date -u`.
- **Expected:** All public access blocks true, `AES256`, versioning enabled, anonymous request refused.
- **Actual:** All four public access blocks true; `AES256`; versioning `Enabled`; anonymous `HeadBucket` returned `403 Forbidden` at `Wed Nov 25 10:36:03 UTC 2026`.
- **Interpretation:** The project bucket is private, encrypted, versioned, and refuses anonymous access. Its Terraform policy also denies non-TLS requests and outside-account principals; the capture proves the anonymous refusal but does not isolate which of the overlapping controls caused it.
