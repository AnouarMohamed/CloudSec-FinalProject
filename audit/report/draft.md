# AtlasLog security audit — GRP01 (draft for Anouar to review)

**Scope:** University integrator project, six course parts. Cloud evidence is collected from AWS account `227755136916` through the `cloud` CLI profile. The profile was initially an IAM user and was later switched to root at the user's explicit direction; the no-root grading requirement therefore cannot be claimed. Other parts are owned by teammates; their findings are deliberately left blank until they provide real exports. Every figure must use a caption with context, command/configuration, expected result, actual result, and interpretation.

**Capture method:** Current-state `terminal-*.png` figures are direct, unretouched screenshots of a live GNOME Ptyxis terminal running on a private Xvfb display. The terminal session was recorded with `script`; the PNGs are lossless conversions of raw XWD window captures. Its real hostname inside an isolated UTS namespace was `atl-cloud-GRP01`, visible with the `[GRP01]` prompt prefix; the physical workstation remained `morgoth`. This capture environment is not a group-named project VM. Historical baseline images remain labeled as Freeze renderings of actual earlier recorded sessions. Exact commands, complete output, and UTC dates are in the screenshots and associated raw sessions.

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
| [WAITING ON TEAMMATE: PingCastle and BloodHound initial exports]; cloud CLI initially used IAM user `anouar-admin` with MFA, a naming discrepancy | [WAITING ON TEAMMATE: PingCastle and BloodHound final exports]; scoped project workload role created. Root CLI use on 2026-11-25 prevents a "root never used" claim; `zakaria-admin` still lacks MFA | [WAITING ON TEAMMATE: AD identity controls]; scoped read policy for project bucket and secret; user-directed root build-identity exception | [WAITING ON TEAMMATE: AD evidence]; `cloud/evidence/iam/terminal-role-trust.png`, `terminal-role-policy.png`; `cloud/evidence/account/terminal-identity.png` |

## 6. Cloud

| Before | After | Measures | Verifiable evidence |
|---|---|---|---|
| Empty private `cloud-docs-grp01` bucket: public access blocked; AWS default SSE-S3; versioning off. No project CloudTrail trail. Initial Prowler: 0 CRITICAL and 113 HIGH failed rows account-wide | Project bucket versioned and explicitly encrypted; anonymous request refused. Segmented VPC and no project SG ingress. Multi-Region CloudTrail delivered logs and a root-use alert to SQS. Secret retrieved from Secrets Manager. Final full-account Prowler: 0 CRITICAL and 97 HIGH failed rows; supplemental secret scan: 2 HIGH. Local kind bonus tested. | Terraform bucket policy, SSE-S3, versioning, routes/SGs, trail and EventBridge/SQS; secret externalization; project-bucket explicit deny; local Kubernetes controls | `cloud/evidence/bucket/`, `vpc/`, `cloudtrail/`, `secrets/`, `prowler/`, `deny/`, `k8s/`; `audit/prowler-initial/`, `audit/prowler-final/` |

**Figure 6.1 — Private bucket before hardening.** Context: GRP01 bucket immediately after the Phase A apply on 2026-11-25. Commands: `aws s3api get-public-access-block`, `get-bucket-encryption`, and `get-bucket-versioning` for `cloud-docs-grp01`. Expected: private bucket, AWS default SSE-S3, no versioning state. Actual: all four block-public-access settings `true`; `AES256`; no versioning response. Interpretation: the initial bucket is safe from public ACL/policy grants but lacks the required versioning and explicit hardening policy. Proof: [baseline.png](../../cloud/evidence/bucket/baseline.png) and [caption](../../cloud/evidence/bucket/baseline.md).

**Figure 6.2 — Project budget notifications.** Context: current budget check on 2026-11-25. Commands shown in the capture: `aws budgets describe-notifications-for-budget` for `cloud-budget-grp01` and `aws notificationscontacts list-email-contacts`. Expected: thresholds at $25, $50, and $100 on a $100 monthly budget and an active recipient. Actual: notifications at 25%, 50%, and 100%; email contact `inactive`. Interpretation: thresholds are configured, but receipt is unproven until the owner activates the contact and actual spend crosses a threshold. Proof: [live budget screenshot](../../cloud/evidence/budget/terminal-status.png) and [caption](../../cloud/evidence/budget/terminal-status.md).

**Figure 6.3 — Bucket hardening and anonymous refusal.** Context: after Phase B apply on 2026-11-25. Commands shown in the captures: `get-public-access-block`, `get-bucket-encryption`, `get-bucket-versioning`, and anonymous `head-bucket --no-sign-request` against `cloud-docs-grp01`. Expected: private, `AES256`, versioning enabled, anonymous refusal. Actual: all four public access blocks true, `AES256`, `Enabled`, and `403 Forbidden`. Interpretation: project bucket acceptance met; Terraform also shows the deny policy. Proof: [configuration screenshot](../../cloud/evidence/bucket/terminal-config.png), [anonymous refusal screenshot](../../cloud/evidence/bucket/terminal-anonymous.png), and their adjacent captions.

**Figure 6.4 — VPC segmentation and restricted Security Groups.** Context: project VPC in eu-west-3 after Phase B. Commands shown in the captures: `describe-subnets`, `describe-security-groups`, and `describe-route-tables` scoped to `vpc-0d069fce4ce5ff50a`. Expected: public/private subnets and no SSH/RDP ingress from the internet. Actual: public subnet has an internet-gateway route, private subnet only local route, and all three Security Groups have empty ingress. Interpretation: project VPC passes; unrelated us-east-1 SG remains open in the account-wide audit. Proof: [subnets and groups screenshot](../../cloud/evidence/vpc/terminal-segmentation.png), [routes screenshot](../../cloud/evidence/vpc/terminal-routes-compact.png), and their adjacent captions.

**Figure 6.5 — CloudTrail logs and received alert.** Context: multi-Region management trail after Phase B. Commands shown in the captures: `describe-trails`, `get-event-selectors`, `get-trail-status`, log-bucket configuration and object listing, and real SQS receive through `cloud/read_root_alert.py`. Expected: active all-management-event trail, private encrypted log bucket, actual root-use notification. Actual: logging and multi-Region true, delivered `.json.gz` object, no delivery error; SQS message for `LookupEvents` shows identity type `Root`. Interpretation: logging and SQS alert delivery worked; email delivery was not tested. Proof: [trail screenshot](../../cloud/evidence/cloudtrail/terminal-trail.png), [log-bucket screenshot](../../cloud/evidence/cloudtrail/terminal-log-bucket.png), [log-delivery screenshot](../../cloud/evidence/cloudtrail/terminal-log-delivery.png), [alert screenshot](../../cloud/evidence/cloudtrail/terminal-alert.png), and adjacent captions.

**Figure 6.6 — External application secret.** Context: Phase C fictional secret demo. Command shown in the live capture: `python cloud/secret_demo.py get`; the earlier put/get session is retained in the evidence folder. Expected: a secret can be retrieved without its value in the capture. Actual: a 43-character retrieval succeeded; value withheld. Interpretation: secret externalization demonstrated, without a running app or rotation claim. Proof: [live retrieval screenshot](../../cloud/evidence/secrets/terminal-retrieval.png) and [caption](../../cloud/evidence/secrets/terminal-retrieval.md).

**Figure 5.1 — Scoped project role and MFA gap.** Context: Phase C IAM check. Commands shown in the captures: `iam get-role`, `get-role-policy`, `sts get-caller-identity`, and `list-mfa-devices` for two existing users. Expected: scoped workload permissions and MFA for every human user. Actual: project role reads only project S3 objects and one secret; `anouar-admin` has MFA; `zakaria-admin` has none; the current CLI ARN is root. Interpretation: workload policy is scoped, but the account-wide MFA and no-root criteria are unmet. Proof: [role trust screenshot](../../cloud/evidence/iam/terminal-role-trust.png), [role policy screenshot](../../cloud/evidence/iam/terminal-role-policy.png), [identity and MFA screenshot](../../cloud/evidence/account/terminal-identity.png), and adjacent captions.

**Figure 6.7 — Final Prowler audit.** Context: Phase C full account scan plus a supplemental GRP01 secret scan on 2026-11-25. Commands shown in the capture: `python audit/summarize_prowler.py` on the initial, final, and targeted CSVs. Expected: zero CRITICAL and HIGH. Actual: full scan 0 CRITICAL, 97 HIGH, versus 0 and 113 initially; targeted secret scan 2 HIGH. Interpretation: the zero-HIGH goal is unmet, and the full scan omitted the project secret. See [comparison](../prowler-final/comparison.md) and [exceptions](../prowler-final/project-exceptions.md). Proof: [live comparison screenshot](../../cloud/evidence/prowler/terminal-comparison.png) and [caption](../../cloud/evidence/prowler/terminal-comparison.md).

**Figure 6.8 — Project policy denial.** Context: Phase D explicit bucket-policy test. Command shown in the capture: `aws s3api list-objects-v2 --bucket cloud-docs-grp01 --profile cloud --region eu-west-3`. Expected: ListBucket is denied. Actual: AWS returned `AccessDenied` and named an explicit resource-policy deny; the Terraform policy contains `DenyProjectBucketListingForDemonstration`. Interpretation: a scoped policy denial was tested without enabling AWS Organizations. The attempt used the user-directed root CLI session and does not cure that grading gap. Proof: [live refusal screenshot](../../cloud/evidence/deny/terminal-refusal.png) and [caption](../../cloud/evidence/deny/terminal-refusal.md).

**Figure 6.9 — Local Kubernetes traffic isolation.** Context: kind cluster with Calico on 2026-11-25. Commands shown in the capture: `kubectl get pods`, `get networkpolicy`, and `kubectl exec` curl from allowed and blocked clients to the same web pod IP. Expected: only the allowed client connects. Actual: `GRP01 web ready` from the allowed client; timeout and exit 28 from the blocked client. Interpretation: the default-deny and explicit allow policies were effective in this local test. Proof: [live network screenshot](../../cloud/evidence/k8s/terminal-network.png) and [caption](../../cloud/evidence/k8s/terminal-network.md).

**Figure 6.10 — Local Kubernetes workload controls.** Context: same kind cluster. Commands shown in the captures: `kubectl get deployment -o json` with selected security/resource fields, `kubectl auth can-i`, Secret metadata listing, and namespace label listing. Expected: restricted pod security, bounded resources, no Secret-reading API permission, and no committed secret value. Actual: non-root UID 10001, read-only root filesystem, dropped capabilities, `RuntimeDefault` seccomp, requests/limits, `can-i` returned `no`, runtime Secret exists, and `restricted` namespace labels are active. Interpretation: local workload hardening is configured and observed; it is not a managed-cluster claim. Proof: [Pod Security screenshot](../../cloud/evidence/k8s/terminal-pod-security-final.png), [RBAC and Secret screenshot](../../cloud/evidence/k8s/terminal-rbac-secret.png), and adjacent captions.

**Figure 6.11 — Repo and Git history secrets scan.** Context: live terminal Gitleaks scan on 2026-11-25. Commands shown in the capture: `gitleaks dir . --redact --verbose` and `gitleaks git . --redact --verbose`. Expected: zero detected secrets. Actual: `no leaks found` in approximately 258.12 MB of current files and 9 commits/about 59.62 MB of Git history. Interpretation: Gitleaks found no matching pattern at scan time; this is detector evidence, not a mathematical guarantee, and later commits need a fresh scan. Proof: [live scan screenshot](../../cloud/evidence/secrets/terminal-gitleaks.png) and [caption](../../cloud/evidence/secrets/terminal-gitleaks.md).

### Figure caption template

**Figure N — [title].** Context: [where and when]. Command/configuration: `[exact command or setting]`. Expected: [acceptance criterion]. Actual: [verbatim result summary supported by raw evidence]. Interpretation: [what this proves and any limit]. Source: `[proof file]`.

## Sources used for interpretation

- [AWS CloudTrail pricing and first management-event copy](https://aws.amazon.com/cloudtrail/pricing/).
- [AWS S3 default encryption](https://docs.aws.amazon.com/AmazonS3/latest/userguide/default-bucket-encryption.html).
- [AWS IAM root best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/root-user-best-practices.html).
- [CIS AWS Foundations Benchmark](https://www.cisecurity.org/benchmark/amazon_web_services).
- [AWS Budgets email verification](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-email-recipients.html).
- [Kubernetes NetworkPolicy](https://kubernetes.io/docs/concepts/services-networking/network-policies/).
- [Kubernetes Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/).
- [Calico on kind](https://docs.tigera.io/calico/latest/getting-started/kubernetes/kind).

The report text is a draft. No teammate result or unrun command is asserted as fact.
