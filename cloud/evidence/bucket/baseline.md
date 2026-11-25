# Private bucket baseline capture

- **Context:** Phase A deliberately incomplete configuration for the empty project bucket on 2026-11-25. The original real terminal recording is `baseline.session`; `baseline.png` is its full Freeze render, with `[GRP01]` and actual hostname `morgoth`.
- **Commands shown:** `rtk proxy aws s3api get-public-access-block --bucket cloud-docs-grp01 --profile cloud`; `rtk proxy aws s3api get-bucket-encryption --bucket cloud-docs-grp01 --profile cloud`; `rtk proxy aws s3api get-bucket-versioning --bucket cloud-docs-grp01 --profile cloud`, preceded by `date -u`.
- **Expected:** Public access blocked; AWS default SSE-S3 present; no versioning state yet.
- **Actual:** All four public-access-block values are `true`; encryption reports `AES256`; the versioning query returns no configuration. UTC timestamp `Wed Nov 25 10:17:35 UTC 2026`.
- **Interpretation:** The baseline is private and encrypted by AWS default but not versioned. Phase B will explicitly manage encryption, versioning, and bucket policy. No data was uploaded.
