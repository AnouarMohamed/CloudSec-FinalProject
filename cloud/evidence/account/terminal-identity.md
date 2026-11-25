# Live terminal capture — AWS identity and human MFA

- **Context:** Phase A/C account check, 2026-11-25 UTC.
- **Commands shown:** `date -u`; `hostname`; `rtk proxy aws sts get-caller-identity --profile cloud`; `rtk proxy aws iam list-mfa-devices --user-name anouar-admin --profile cloud --query 'MFADevices[*].SerialNumber' --output json`; `rtk proxy aws iam list-mfa-devices --user-name zakaria-admin --profile cloud --query 'MFADevices[*].SerialNumber' --output json`.
- **Expected:** The build profile is an IAM user, and both human users have MFA.
- **Actual:** STS returned account `227755136916` with ARN `arn:aws:iam::227755136916:root`; `anouar-admin` has one MFA device and `zakaria-admin` returned `[]`.
- **Interpretation:** The no-root and all-human-MFA criteria are unmet. This capture does not establish who operated prior sessions.
- **Method:** Genuine Ptyxis window captured from a private Xvfb display without cropping or retouching. The continuous raw recording is [ptyxis-live.session](../terminal-live/ptyxis-live.session). `atl-cloud-GRP01` is the real hostname inside an isolated UTS namespace; the physical host is `morgoth`, not a project VM.
