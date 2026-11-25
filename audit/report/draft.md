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
| [WAITING ON TEAMMATE: PingCastle and BloodHound initial exports]; cloud CLI initially used IAM user `anouar-admin` with MFA, a naming discrepancy | [WAITING ON TEAMMATE: PingCastle and BloodHound final exports]; scoped project workload role created. Root CLI use on 2026-11-25 prevents a "root never used" claim; `zakaria-admin` still lacks MFA | [WAITING ON TEAMMATE: AD identity controls]; scoped read policy for project bucket and secret; user-directed root build-identity exception | [WAITING ON TEAMMATE: AD evidence]; `cloud/evidence/iam/scoped-role.png`, `human-mfa.png`; `cloud/evidence/account/root-identity.png` |

## 6. Cloud

| Before | After | Measures | Verifiable evidence |
|---|---|---|---|
| Empty private `cloud-docs-grp01` bucket: public access blocked; AWS default SSE-S3; versioning off. No project CloudTrail trail. Initial Prowler: 0 CRITICAL and 113 HIGH failed rows account-wide | Project bucket versioned and explicitly encrypted; anonymous request refused. Segmented VPC and no project SG ingress. Multi-Region CloudTrail delivered logs and a root-use alert to SQS. Secret retrieved from Secrets Manager. [PENDING: final Prowler comparison] | Terraform bucket policy, SSE-S3, versioning, routes/SGs, trail and EventBridge/SQS; secret externalization | `cloud/evidence/bucket/baseline.png`, `hardened.png`; `cloud/evidence/vpc/`; `cloud/evidence/cloudtrail/`; `cloud/evidence/secrets/retrieval.png`; `audit/prowler-initial/`; [PENDING: final audit] |

**Figure 6.1 — Private bucket before hardening.** Context: GRP01 bucket immediately after the Phase A apply on 2026-11-25. Commands: `aws s3api get-public-access-block`, `get-bucket-encryption`, and `get-bucket-versioning` for `cloud-docs-grp01`. Expected: private bucket, AWS default SSE-S3, no versioning state. Actual: all four block-public-access settings `true`; `AES256`; no versioning response. Interpretation: the initial bucket is safe from public ACL/policy grants but lacks the required versioning and explicit hardening policy. Proof: [baseline.png](../../cloud/evidence/bucket/baseline.png) and [caption](../../cloud/evidence/bucket/baseline.md).

**Figure 6.2 — Project budget notifications.** Context: post-apply budget check on 2026-11-25. Commands: `aws budgets describe-notifications-for-budget` for `cloud-budget-grp01` and `aws notificationscontacts list-email-contacts`. Expected: thresholds at $25, $50, and $100 on a $100 monthly budget and an active recipient. Actual: notifications at 25%, 50%, and 100%, all `OK`; email contact `inactive`. Interpretation: thresholds are configured, but receipt is unproven until the owner activates the contact and actual spend crosses a threshold. Proof: [notifications.png](../../cloud/evidence/budget/notifications.png), [contact-status.png](../../cloud/evidence/budget/contact-status.png), and adjacent captions.

**Figure 6.3 — Bucket hardening and anonymous refusal.** Context: after Phase B apply on 2026-11-25. Commands: `get-public-access-block`, `get-bucket-encryption`, `get-bucket-versioning`, and anonymous `head-bucket --no-sign-request` against `cloud-docs-grp01`. Expected: private, `AES256`, versioning enabled, anonymous refusal. Actual: all four public access blocks true, `AES256`, `Enabled`, and `403 Forbidden`. Interpretation: project bucket acceptance met; Terraform also shows the deny policy. Proof: [hardened.png](../../cloud/evidence/bucket/hardened.png) and [caption](../../cloud/evidence/bucket/hardened.md).

**Figure 6.4 — VPC segmentation and restricted Security Groups.** Context: project VPC in eu-west-3 after Phase B. Commands: `describe-subnets`, `describe-security-groups`, and `describe-route-tables` scoped to `vpc-0d069fce4ce5ff50a`. Expected: public/private subnets and no SSH/RDP ingress from the internet. Actual: public subnet has an internet-gateway route, private subnet only local route, and all three Security Groups have empty ingress. Interpretation: project VPC passes; unrelated us-east-1 SG remains open in the account-wide audit. Proof: [segmentation.png](../../cloud/evidence/vpc/segmentation.png), [routes.png](../../cloud/evidence/vpc/routes.png), and [caption](../../cloud/evidence/vpc/segmentation.md).

**Figure 6.5 — CloudTrail logs and received alert.** Context: multi-Region management trail after Phase B. Commands: `describe-trails`, `get-event-selectors`, `get-trail-status`, S3 log listing, EventBridge rule query, and real SQS receive through `cloud/read_root_alert.py`. Expected: active all-management-event trail, private encrypted log bucket, actual root-use notification. Actual: logging and multi-Region true, delivered `.json.gz` object, no delivery error; SQS message for `LookupEvents` shows identity type `Root`. Interpretation: logging and SQS alert delivery worked; email delivery was not tested. Proof: [config.png](../../cloud/evidence/cloudtrail/config.png), [delivery.png](../../cloud/evidence/cloudtrail/delivery.png), [alert.png](../../cloud/evidence/cloudtrail/alert.png), and their adjacent captions.

**Figure 6.6 — External application secret.** Context: Phase C fictional secret demo. Commands: `cloud/secret_demo.py put` and `get`. Expected: secret created/retrieved without value in code, state, or screenshot. Actual: same version ID on put/get and 43-character retrieval success; value withheld. Interpretation: secret externalization demonstrated, without a running app or rotation claim. Proof: [retrieval.png](../../cloud/evidence/secrets/retrieval.png) and [caption](../../cloud/evidence/secrets/retrieval.md).

**Figure 5.1 — Scoped project role and MFA gap.** Context: Phase C IAM check. Commands: `iam get-role`, `get-role-policy`, `list-users`, and `list-mfa-devices` for two existing users. Expected: scoped workload permissions and MFA for every human user. Actual: project role reads only project S3 objects and one secret; `anouar-admin` has MFA; `zakaria-admin` has none. Interpretation: workload policy is scoped, but the account-wide MFA criterion is incomplete and root use invalidates no-root. Proof: [scoped-role.png](../../cloud/evidence/iam/scoped-role.png), [human-mfa.png](../../cloud/evidence/iam/human-mfa.png), and adjacent captions.

### Figure caption template

**Figure N — [title].** Context: [where and when]. Command/configuration: `[exact command or setting]`. Expected: [acceptance criterion]. Actual: [verbatim result summary supported by raw evidence]. Interpretation: [what this proves and any limit]. Source: `[proof file]`.

## Sources used for interpretation

- [AWS CloudTrail pricing and first management-event copy](https://aws.amazon.com/cloudtrail/pricing/).
- [AWS S3 default encryption](https://docs.aws.amazon.com/AmazonS3/latest/userguide/default-bucket-encryption.html).
- [AWS IAM root best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/root-user-best-practices.html).
- [CIS AWS Foundations Benchmark](https://www.cisecurity.org/benchmark/amazon_web_services).
- [AWS Budgets email verification](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-email-recipients.html).

The report text is a draft. No teammate result or unrun command is asserted as fact.
