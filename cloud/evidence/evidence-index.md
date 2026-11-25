# Evidence index

Status values: **done**, **partial**, **missing**, **waiting on teammate**. Every captured command must retain its real UTC timestamp and full output. PNG captures and captions are added as generated.

| Requirement | Acceptance criterion | Proof file | Status |
|---|---|---|---|
| A — non-root CLI identity | STS ARN is not root | `account/identity.session`, `account/identity.png`, `account/identity.md` | done |
| A/C — no root usage throughout project | Root is never used; CloudTrail query returns no root events | `account/root-identity.session`, `account/root-identity.png`, `account/root-identity.md` | **failed by user-directed root login on 2026-11-25** |
| A — root MFA and no root keys | Account summary verifies settings | `account/safety-concise.session`, `account/safety-concise.png`, `account/safety.md` | done |
| A — current IAM user MFA | MFA device listed | `account/safety-concise.session`, `account/safety-concise.png`, `account/safety.md` | done |
| A — budget alerts | $25, $50, $100 alerts configured | `budget/notifications.session`, `budget/notifications.png`, `budget/notifications.md` | done (delivery test pending) |
| A — safe imperfect baseline | Terraform and explanation | `bucket/baseline.session`, `bucket/baseline.png`, `bucket/baseline.md`, `../../audit/baseline.md` | done (initial Prowler pending) |
| A — initial Prowler | Raw report and CRITICAL/HIGH counts | `../../audit/prowler-initial/grp01-initial.csv`, `../../audit/prowler-initial/grp01-initial.ocsf.json`, `../../audit/prowler-initial/summary.png`, `../../audit/prowler-initial/summary-caption.md` | done; 0 CRITICAL, 113 HIGH failed rows |
| B — private encrypted versioned docs bucket | Configuration and anonymous denial | `bucket/` | missing |
| B — segmented VPC and safe Security Groups | Subnets and SG listing | `vpc/` | missing |
| B — CloudTrail and tested alert | Configuration and delivered notification | `cloudtrail/` | missing |
| C — external secret and retrieval | Secret metadata and successful retrieval without value in evidence | `secrets/` | missing |
| C — full Git history secret scan | Zero findings across history | `secrets/gitleaks.txt` | missing |
| C — final Prowler | Raw report and before/after table | `../../audit/prowler-final/` | missing |
| C — least privilege and no root use | Scoped policy and CloudTrail query | `iam/` | missing |
| D — budget alert test and policy denial | Notification and access denied result | `budget/` | missing |
| E — report and naming annex | Six parts, captions, cloud listings | `../../audit/report/` | partial |
| F — local Kubernetes hardening | Workloads and blocked traffic | `k8s/` | missing |
