# AtlasLog security audit — GRP01 (draft for Anouar to review)

**Scope:** University integrator project, six course parts. Cloud evidence is collected from AWS account `227755136916` through the `cloud` CLI profile. The profile was initially an IAM user and was later switched to root at the user's explicit direction; the no-root grading requirement therefore cannot be claimed. Other parts are owned by teammates; their findings are deliberately left blank until they provide real exports. Every figure must use a caption with context, command/configuration, expected result, actual result, and interpretation.

## 1. Network and perimeter

| Before | After | Measures | Verifiable evidence |
|---|---|---|---|
| [WAITING ON TEAMMATE: network topology, firewall/VPN baseline] | [WAITING ON TEAMMATE: hardened network and VPN tests] | [WAITING ON TEAMMATE: firewall, VPN, Suricata measures] | [WAITING ON TEAMMATE: Suricata alerts, packet or connectivity tests, screenshots] |

## 2. Operating systems

| Before | After | Measures | Verifiable evidence |
|---|---|---|---|
| [WAITING ON TEAMMATE: Lynis initial report] | [WAITING ON TEAMMATE: Lynis final report and score] | [WAITING ON TEAMMATE: Linux hardening changes] | [WAITING ON TEAMMATE: Lynis before/after exports and system commands] |

## 3. Data security

| Before | After | Measures | Verifiable evidence |
|---|---|---|---|
| [WAITING ON TEAMMATE: data inventory and backup/encryption baseline] | [WAITING ON TEAMMATE: encrypted data and restore test] | [WAITING ON TEAMMATE: LUKS, backup, access control] | [WAITING ON TEAMMATE: LUKS proof and backup/restore outputs] |

## 4. Virtualization

| Before | After | Measures | Verifiable evidence |
|---|---|---|---|
| [WAITING ON TEAMMATE: VM inventory and isolation baseline] | [WAITING ON TEAMMATE: final VM controls] | [WAITING ON TEAMMATE: VM, host, and virtual network configuration] | [WAITING ON TEAMMATE: hypervisor screenshots and isolation tests] |

## 5. Identity (AD and cloud IAM)

| Before | After | Measures | Verifiable evidence |
|---|---|---|---|
| [WAITING ON TEAMMATE: PingCastle and BloodHound initial exports]; cloud CLI initially used IAM user `anouar-admin` with MFA, a naming discrepancy | [WAITING ON TEAMMATE: PingCastle and BloodHound final exports]; [PENDING: scoped cloud roles]. Root CLI use on 2026-11-25 prevents a "root never used" claim | [WAITING ON TEAMMATE: AD identity controls]; [PENDING: cloud IAM least privilege for workloads]; user-directed root build-identity exception | [WAITING ON TEAMMATE: AD evidence]; [PENDING: `cloud/evidence/iam/`]; `cloud/evidence/account/` for identity transition |

## 6. Cloud

| Before | After | Measures | Verifiable evidence |
|---|---|---|---|
| Empty private `cloud-docs-grp01` bucket: public access blocked; AWS default SSE-S3; versioning off. No project CloudTrail trail. Initial Prowler report in progress | [PENDING: explicit bucket hardening, VPC, CloudTrail, final Prowler] | [PENDING: Terraform hardening and secret externalization] | `cloud/evidence/bucket/baseline.png`; `cloud/evidence/budget/notifications.png`; [PENDING: Prowler before/after and Phase B/C files] |

**Figure 6.1 — Private bucket before hardening.** Context: GRP01 bucket immediately after the Phase A apply on 2026-11-25. Commands: `aws s3api get-public-access-block`, `get-bucket-encryption`, and `get-bucket-versioning` for `cloud-docs-grp01`. Expected: private bucket, AWS default SSE-S3, no versioning state. Actual: all four block-public-access settings `true`; `AES256`; no versioning response. Interpretation: the initial bucket is safe from public ACL/policy grants but lacks the required versioning and explicit hardening policy. Proof: [baseline.png](../../cloud/evidence/bucket/baseline.png) and [caption](../../cloud/evidence/bucket/baseline.md).

**Figure 6.2 — Project budget notifications.** Context: post-apply budget check on 2026-11-25. Command: `aws budgets describe-notifications-for-budget` for `cloud-budget-grp01`. Expected: thresholds at $25, $50, and $100 on a $100 monthly budget. Actual: notifications at 25%, 50%, and 100%, all `OK`. Interpretation: thresholds are configured; receipt testing remains open. Proof: [notifications.png](../../cloud/evidence/budget/notifications.png) and [caption](../../cloud/evidence/budget/notifications.md).

### Figure caption template

**Figure N — [title].** Context: [where and when]. Command/configuration: `[exact command or setting]`. Expected: [acceptance criterion]. Actual: [verbatim result summary supported by raw evidence]. Interpretation: [what this proves and any limit]. Source: `[proof file]`.

## Sources used for interpretation

- [AWS CloudTrail pricing and first management-event copy](https://aws.amazon.com/cloudtrail/pricing/).
- [AWS S3 default encryption](https://docs.aws.amazon.com/AmazonS3/latest/userguide/default-bucket-encryption.html).
- [AWS IAM root best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/root-user-best-practices.html).
- [CIS AWS Foundations Benchmark](https://www.cisecurity.org/benchmark/amazon_web_services).

The report text is a draft. No teammate result or unrun command is asserted as fact.
