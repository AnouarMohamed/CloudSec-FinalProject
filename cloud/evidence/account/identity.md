# Identity capture

- **Context:** GRP01 project CLI identity check on 2026-11-25, recorded with `script` and rendered without retouching using Freeze. The prompt shows the real hostname `morgoth` and `[GRP01]` label. The first capture attempt failed due to missing CLI region; the original failed session is kept in `identity-failed-no-region.session`.
- **Command shown:** `rtk proxy aws sts get-caller-identity --profile cloud` (which executes `aws sts get-caller-identity --profile cloud`), preceded by `date -u` in the same recorded session.
- **Expected:** Account ID present and IAM user ARN, not root.
- **Actual:** Account `227755136916`; ARN `arn:aws:iam::227755136916:user/anouar-admin`; UTC timestamp `Wed Nov 25 09:54:32 UTC 2026`.
- **Interpretation:** The active CLI identity is not root. The username does not satisfy the project's `prenom.nom` naming rule and does not have admin permissions; that separate issue is open.
- **Proof:** `identity.session` is the original recording; `identity.png` is its full rendered image.
