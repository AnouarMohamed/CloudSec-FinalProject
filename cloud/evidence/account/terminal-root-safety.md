# Live terminal capture — root MFA and access-key settings

- **Context:** Phase A account-summary check, 2026-11-25 UTC.
- **Commands shown:** `date -u`; `rtk proxy aws iam get-account-summary --profile cloud --query 'SummaryMap.{RootMFA:AccountMFAEnabled,RootKeys:AccountAccessKeysPresent}' --output json`.
- **Expected:** Root MFA enabled and no root access keys.
- **Actual:** The account summary returned `RootMFA: 1` and `RootKeys: 0`.
- **Interpretation:** These two root-account settings pass. They do not establish that root was never used; [terminal-identity.png](terminal-identity.png) shows the current profile's root ARN.
- **Method:** Genuine Ptyxis window on private Xvfb, recorded in [ptyxis-repair.session](../terminal-live/ptyxis-repair.session). `atl-cloud-GRP01` is the real hostname inside an isolated UTS namespace on physical host `morgoth`, not a project VM. The window was captured without cropping or retouching.
