# Account and IAM user MFA capture

- **Context:** GRP01 account safety checks on 2026-11-25, before any project resources were created. `safety-concise.session` is the real `script` recording; `safety-concise.png` is a full Freeze render. The prompt shows actual hostname `morgoth` and `[GRP01]` label.
- **Commands shown:** `rtk proxy aws iam get-account-summary --query 'SummaryMap.{RootMFA:AccountMFAEnabled,RootKeys:AccountAccessKeysPresent}' --profile cloud`; `rtk proxy aws iam list-mfa-devices --user-name anouar-admin --query 'MFADevices[].UserName' --profile cloud`, preceded by `date -u`.
- **Expected:** Root MFA enabled, no root access keys, and the current human IAM user has an MFA device.
- **Actual:** `RootMFA: 1`, `RootKeys: 0`, and the MFA device query returns `anouar-admin`. UTC timestamp `Wed Nov 25 09:56:24 UTC 2026`.
- **Interpretation:** These settings were present at capture time. This does not prove root was never used; CloudTrail event history must be queried separately. The user chose to keep `anouar-admin`, so the `prenom.nom` naming discrepancy remains documented.
