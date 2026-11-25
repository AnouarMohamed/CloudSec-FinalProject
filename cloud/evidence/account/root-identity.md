# Root identity exception capture

- **Context:** On 2026-11-25 the user explicitly directed the agent to switch the `cloud` profile to root after an IAM permissions denial. The browser-based AWS CLI login created temporary credentials; no root access keys were created or requested. This is a documented exception to the original project rule.
- **Command shown:** `rtk proxy aws sts get-caller-identity --profile cloud`, preceded by `date -u` in a real `script` session. The prompt shows `[GRP01]` and the real hostname `morgoth`.
- **Expected:** The identity selected in browser login is returned by STS.
- **Actual:** Account `227755136916`, ARN `arn:aws:iam::227755136916:root`, UTC timestamp `Wed Nov 25 10:09:54 UTC 2026`.
- **Interpretation:** Root was used. The project cannot claim that root was never used, and a zero-root-events query cannot be an acceptance proof. The original session is `root-identity.session`; `root-identity.png` is its full Freeze render.
